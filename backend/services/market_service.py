import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from config.settings import settings
from utils.data_fetcher import fetch_bulk_history, extract_ticker_df
from services.indicators import (
    compute_rsi,
    compute_daily_change,
    compute_volatility,
    compute_volume_ratio,
    compute_price_on_date,
    compute_volume_on_date,
)
from services.index_service import get_index_tickers

logger = logging.getLogger(__name__)

def _clean_symbol(ticker: str) -> str:
    """Strip exchange suffix for display."""
    return ticker.replace(".NS", "").replace(".BO", "").replace(".L", "").replace(".TO", "").replace(".AX", "").replace(".DE", "").replace(".PA", "").replace(".SA", "").replace(".T", "")

def _compute_stock_metrics(
    ticker: str,
    df: pd.DataFrame,
    target_date: pd.Timestamp,
) -> Optional[Dict[str, Any]]:
    """
    Compute all metrics for a single stock on a given date.
    Returns None if data is insufficient or invalid.
    """
    try:
        price = compute_price_on_date(df, target_date)
        if price is None or price <= 0:
            return None

        change_pct = compute_daily_change(df, target_date)
        if change_pct is None:
            return None

        rsi = compute_rsi(df["Close"])
        volatility = compute_volatility(df)
        volume = compute_volume_on_date(df, target_date)
        volume_ratio = compute_volume_ratio(df, target_date)

        close_series = df["Close"].dropna()
        week52_high = round(float(close_series.max()), 2)
        week52_low = round(float(close_series.min()), 2)

        return {
            "symbol": _clean_symbol(ticker),
            "ticker": ticker,
            "price": price,
            "change_pct": change_pct,
            "rsi": rsi,
            "volatility": volatility,
            "volume": volume,
            "volume_ratio": volume_ratio,
            "week52_high": week52_high,
            "week52_low": week52_low,
            "trend": "up" if change_pct > 0 else "down" if change_pct < 0 else "neutral",
        }
    except Exception as e:
        logger.warning(f"Failed to compute metrics for {ticker}: {e}")
        return None

def get_index_data(index_key: str, date_str: str) -> Dict[str, Any]:
    """
    Fetch and compute metrics for the FULL index dataset without truncation.
    """
    if index_key not in settings.INDEX_CONFIGS:
        raise ValueError(f"Unknown index: {index_key}. Valid: {list(settings.INDEX_CONFIGS.keys())}")

    config = settings.INDEX_CONFIGS[index_key]
    
    try:
        tickers = get_index_tickers(index_key)
        source = "dynamic_scraping"
    except Exception as e:
        logger.warning(f"Failed dynamic fetch for {index_key}: {e}. Falling back to static configuration.")
        tickers = config.get("tickers", [])
        source = "static_fallback"

    try:
        target_date = pd.Timestamp(date_str)
    except Exception:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")

    logger.info(f"Computing FULL market summary for {index_key} on {date_str} across {len(tickers)} symbols")

    bulk_df = fetch_bulk_history(tickers, period=settings.YFINANCE_PERIOD)

    all_metrics = []
    for ticker in tickers:
        ticker_df = extract_ticker_df(bulk_df, ticker)
        if ticker_df is None or ticker_df.empty:
            continue

        metrics = _compute_stock_metrics(ticker, ticker_df, target_date)
        if metrics is not None:
            all_metrics.append(metrics)

    return {
        "index": index_key,
        "index_name": config["name"],
        "source": source,
        "date": date_str,
        "total_tickers": len(tickers),
        "total_analyzed": len(all_metrics),
        "data": all_metrics
    }

def get_top_stocks(data: List[Dict[str, Any]], n: int = 10, metric: str = "performance", reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Dynamically sorts the provided list of dictionaries.
    """
    if not data:
        return []
        
    if metric == "performance":
        # Only consider strictly positive or strictly negative for highest performers if reverse=True? 
        # Typically "top performance" means raw absolute highest sorting.
        filtered = data
        if reverse: # Gainers
            filtered = [m for m in data if m["change_pct"] > 0]
        else: # Losers
            filtered = [m for m in data if m["change_pct"] < 0]
        return sorted(filtered, key=lambda x: x["change_pct"], reverse=reverse)[:n]
    elif metric == "rsi":
        return sorted(data, key=lambda x: x["rsi"], reverse=reverse)[:n]
    elif metric == "volume":
        return sorted(data, key=lambda x: x["volume_ratio"], reverse=reverse)[:n]
    elif metric == "volatility":
        return sorted(data, key=lambda x: x["volatility"], reverse=reverse)[:n]
    else:
        raise ValueError(f"Unknown sorting metric: {metric}")
