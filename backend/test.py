import pandas as pd
from datetime import datetime
import yfinance as yf
from services.indicators import compute_daily_change, compute_price_on_date, compute_volume_on_date, compute_rsi
from utils.data_fetcher import extract_ticker_df

print("Downloading RELIANCE.NS")
bulk_df = yf.download(["RELIANCE.NS", "TCS.NS"], period="3mo", auto_adjust=True, group_by="ticker")
print("Extracting RELIANCE.NS")
df = extract_ticker_df(bulk_df, "RELIANCE.NS")
print(f"df shape: {df.shape}")

target_date = pd.Timestamp("2026-05-01")
print(f"target_date: {target_date}")

tz = df.index.tz
if tz:
    print(f"tz: {tz}")
    target_ts = pd.Timestamp(target_date).tz_localize(tz) if target_date.tzinfo is None else pd.Timestamp(target_date).tz_convert(tz)
else:
    target_ts = pd.Timestamp(target_date)

df_up_to = df[df.index <= target_ts]
print(f"df_up_to shape: {df_up_to.shape}")

if len(df_up_to) > 0:
    print(f"Latest date in df_up_to: {df_up_to.index[-1]}")

price = compute_price_on_date(df, target_date)
change = compute_daily_change(df, target_date)
print(f"price: {price}, change: {change}")
