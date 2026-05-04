import pandas as pd
import logging
from typing import List
import httpx
from io import StringIO
from cachetools import TTLCache, cached
from config.settings import settings

logger = logging.getLogger(__name__)

index_cache = TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL_SECONDS)

def _get_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)
    resp.raise_for_status()
    return resp.text

def _scrape_wiki(url: str, col_names: List[str], suffix: str = "", replace_dot: bool = False, pad_zeros: int = 0) -> List[str]:
    """Helper to scrape wikipedia tables, finding the correct column and normalizing."""
    html = _get_html(url)
    tables = pd.read_html(StringIO(html))
    df = None
    target_col = None
    
    for tbl in tables:
        for col in col_names:
            if col in tbl.columns:
                df = tbl
                target_col = col
                break
        if df is not None:
            break
            
    if df is None:
        raise ValueError(f"Could not find table with columns {col_names} at {url}")
        
    tickers = df[target_col].dropna().astype(str).tolist()
    
    # Normalize strings
    cleaned = []
    for t in tickers:
        t = str(t).strip()
        t = t.replace("SEHK:", "").replace("NYSE:", "").replace("\xa0", "").strip()
        
        if replace_dot:
            t = t.replace(".", "-")
        # Handle zero-padding (e.g. HK stocks require 4 digits like 0700.HK)
        if pad_zeros > 0:
            if '.' in t: # Ignore floats if they snuck in
                t = t.split('.')[0]
            t = t.zfill(pad_zeros)
        if suffix and not t.endswith(suffix):
            t = f"{t}{suffix}"
        if t and t.lower() != 'nan':
            cleaned.append(t)
        
    # Remove duplicates but preserve listing sequence ranking
    seen = set()
    return [x for x in cleaned if not (x in seen or seen.add(x))]

@cached(cache=index_cache)
def get_index_tickers(index_name: str) -> List[str]:
    """
    Dynamically fetch index constituents, utilizing modular Wikipedia scraper definitions safely.
    Falls back to settings if not mapped.
    """
    index_key = index_name.lower().strip()
    logger.info(f"Dynamically fetching tickers for index: {index_key}")
    
    try:
        if index_key == "sp500":
            return _scrape_wiki("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", ["Symbol", "Ticker"], replace_dot=True)
        elif index_key == "nifty50":
            return _scrape_wiki("https://en.wikipedia.org/wiki/NIFTY_50", ["Symbol"], suffix=".NS")
        elif index_key == "sensex":
            return _scrape_wiki("https://en.wikipedia.org/wiki/BSE_SENSEX", ["Ticker", "Symbol"], suffix=".BO")
        elif index_key == "ftse100":
            return _scrape_wiki("https://en.wikipedia.org/wiki/FTSE_100_Index", ["Ticker", "EPIC"], suffix=".L")
        elif index_key == "nasdaq":
            return _scrape_wiki("https://en.wikipedia.org/wiki/Nasdaq-100", ["Ticker", "Symbol"])
        elif index_key == "djia":
            return _scrape_wiki("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", ["Symbol", "Ticker"])
        elif index_key == "tsx":
            return _scrape_wiki("https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index", ["Symbol", "Ticker"], suffix=".TO")
        elif index_key == "dax":
            return _scrape_wiki("https://en.wikipedia.org/wiki/DAX", ["Ticker", "Ticker symbol"], suffix=".DE")
        elif index_key == "cac40":
            return _scrape_wiki("https://en.wikipedia.org/wiki/CAC_40", ["Ticker", "Symbol"], suffix=".PA")
        elif index_key == "eurostoxx50":
            return _scrape_wiki("https://en.wikipedia.org/wiki/EURO_STOXX_50", ["Ticker"])
        elif index_key == "nikkei225":
            return _scrape_wiki("https://en.wikipedia.org/wiki/Nikkei_225", ["Code", "Ticker", "Symbol"], suffix=".T")
        elif index_key == "ibovespa":
            return _scrape_wiki("https://en.wikipedia.org/wiki/List_of_companies_listed_on_B3", ["Ticker"], suffix=".SA")
        elif index_key == "asx200":
            return _scrape_wiki("https://en.wikipedia.org/wiki/S%26P/ASX_200", ["Code", "Ticker"], suffix=".AX")
        elif index_key == "hsi":
            return _scrape_wiki("https://en.wikipedia.org/wiki/Hang_Seng_Index", ["Ticker", "Code"], suffix=".HK", pad_zeros=4)
        else:
            raise NotImplementedError(f"Dynamic scraping not computationally available for complex index: {index_key}")
    except Exception as e:
        logger.error(f"Error querying dynamic constituents for {index_key}: {str(e)}")
        raise e
