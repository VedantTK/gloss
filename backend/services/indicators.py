import pandas as pd
import numpy as np
from typing import Optional


def compute_rsi(series: pd.Series, period: int = 14) -> float:
    """
    Compute the RSI (Relative Strength Index) for the last value in a price series.
    Returns a float in [0, 100], or 50.0 if not enough data.
    """
    if len(series) < period + 1:
        return 50.0

    delta = series.diff().dropna()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = losses.ewm(com=period - 1, min_periods=period).mean()

    last_avg_gain = avg_gain.iloc[-1]
    last_avg_loss = avg_loss.iloc[-1]

    if last_avg_loss == 0:
        return 100.0

    rs = last_avg_gain / last_avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(float(rsi), 2)


def compute_daily_change(df: pd.DataFrame, target_date: pd.Timestamp) -> Optional[float]:
    """
    Compute the percentage daily change on or just before the target date.
    Returns None if insufficient data.
    """
    tz = df.index.tz
    if tz:
        target_ts = pd.Timestamp(target_date).tz_localize(tz) if target_date.tzinfo is None else pd.Timestamp(target_date).tz_convert(tz)
    else:
        target_ts = pd.Timestamp(target_date)

    df_up_to = df[df.index <= target_ts]
    if len(df_up_to) < 2:
        return None

    today_close = float(df_up_to["Close"].iloc[-1])
    prev_close = float(df_up_to["Close"].iloc[-2])

    if prev_close == 0:
        return None

    return round(((today_close - prev_close) / prev_close) * 100, 2)


def compute_volatility(df: pd.DataFrame, window: int = 20) -> float:
    """
    Compute annualized volatility (std dev of log returns × sqrt(252)).
    Returns 0.0 if not enough data.
    """
    if len(df) < 2:
        return 0.0

    close = df["Close"].dropna()
    if len(close) < 2:
        return 0.0

    log_returns = np.log(close / close.shift(1)).dropna()

    if len(log_returns) < window:
        window = max(2, len(log_returns))

    recent_returns = log_returns.tail(window)
    vol = float(recent_returns.std() * np.sqrt(252) * 100)
    return round(vol, 2)


def compute_volume_ratio(df: pd.DataFrame, target_date: pd.Timestamp, avg_window: int = 20) -> float:
    """
    Compute the ratio of the target date's volume to the N-day average volume.
    Returns 1.0 as default.
    """
    tz = df.index.tz
    if tz:
        target_ts = pd.Timestamp(target_date).tz_localize(tz) if target_date.tzinfo is None else pd.Timestamp(target_date).tz_convert(tz)
    else:
        target_ts = pd.Timestamp(target_date)

    df_up_to = df[df.index <= target_ts]
    if len(df_up_to) < 2:
        return 1.0

    current_vol = float(df_up_to["Volume"].iloc[-1])
    avg_vol = float(df_up_to["Volume"].iloc[-(avg_window + 1):-1].mean())

    if avg_vol == 0:
        return 1.0

    return round(current_vol / avg_vol, 2)


def compute_price_on_date(df: pd.DataFrame, target_date: pd.Timestamp) -> Optional[float]:
    """Get closing price on or before target date."""
    tz = df.index.tz
    if tz:
        target_ts = pd.Timestamp(target_date).tz_localize(tz) if target_date.tzinfo is None else pd.Timestamp(target_date).tz_convert(tz)
    else:
        target_ts = pd.Timestamp(target_date)

    df_up_to = df[df.index <= target_ts]
    if df_up_to.empty:
        return None
    return round(float(df_up_to["Close"].iloc[-1]), 2)


def compute_volume_on_date(df: pd.DataFrame, target_date: pd.Timestamp) -> int:
    """Get volume on or before target date."""
    tz = df.index.tz
    if tz:
        target_ts = pd.Timestamp(target_date).tz_localize(tz) if target_date.tzinfo is None else pd.Timestamp(target_date).tz_convert(tz)
    else:
        target_ts = pd.Timestamp(target_date)

    df_up_to = df[df.index <= target_ts]
    if df_up_to.empty:
        return 0
    return int(df_up_to["Volume"].iloc[-1])
