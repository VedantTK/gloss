import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from cachetools import TTLCache, cached
from threading import Lock

logger = logging.getLogger(__name__)

# Thread-safe cache
_cache = TTLCache(maxsize=128, ttl=300)
_lock = Lock()


def _cache_key(tickers: tuple, period: str) -> str:
    return f"{','.join(sorted(tickers))}::{period}"


def fetch_bulk_history(tickers: List[str], period: str = "3mo") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for multiple tickers using yfinance bulk download.
    Returns a MultiIndex DataFrame with columns: (field, ticker).
    Results are cached for TTL seconds.
    """
    key = _cache_key(tuple(tickers), period)

    with _lock:
        if key in _cache:
            logger.info(f"Cache hit for {len(tickers)} tickers")
            return _cache[key]

    logger.info(f"Fetching data for {len(tickers)} tickers, period={period}")
    try:
        df = yf.download(
            tickers=tickers,
            period=period,
            auto_adjust=True,
            progress=False,
            threads=True,
            group_by="ticker",
        )
        with _lock:
            _cache[key] = df
        return df
    except Exception as e:
        logger.error(f"yfinance bulk download failed: {e}")
        raise RuntimeError(f"Data fetch failed: {e}") from e


def extract_ticker_df(bulk_df: pd.DataFrame, ticker: str) -> Optional[pd.DataFrame]:
    """
    Extract single-ticker OHLCV DataFrame from a bulk download result.
    Handles both single and multi-ticker bulk results.
    """
    try:
        if isinstance(bulk_df.columns, pd.MultiIndex):
            # Multi-ticker bulk download: columns are (field, ticker) or (ticker, field)
            if ticker in bulk_df.columns.get_level_values(0):
                df = bulk_df.xs(ticker, axis=1, level=0).copy()
            elif ticker in bulk_df.columns.get_level_values(1):
                df = bulk_df.xs(ticker, axis=1, level=1).copy()
            else:
                return None
        else:
            # Single-ticker download: flat columns
            df = bulk_df.copy()

        df = df.dropna(how="all")
        if df.empty:
            return None
        return df
    except Exception as e:
        logger.warning(f"Could not extract {ticker}: {e}")
        return None


def get_price_on_date(df: pd.DataFrame, target_date: datetime) -> Optional[float]:
    """Get closing price on or before a given date."""
    df_up_to = df[df.index <= pd.Timestamp(target_date, tz="UTC" if df.index.tz else None)]
    if df_up_to.empty:
        return None
    return float(df_up_to["Close"].iloc[-1])


def get_price_on_prev_trading_day(df: pd.DataFrame, target_date: datetime) -> Optional[float]:
    """Get closing price on the trading day before a given date."""
    df_before = df[df.index < pd.Timestamp(target_date, tz="UTC" if df.index.tz else None)]
    if df_before.empty:
        return None
    return float(df_before["Close"].iloc[-1])
