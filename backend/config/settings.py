from pydantic_settings import BaseSettings
from typing import Dict, List


class Settings(BaseSettings):
    APP_NAME: str = "Gloss Market Intelligence"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://frontend:3000",
        "http://127.0.0.1:3000",
        "http://localhost",
        "http://127.0.0.1",
    ]
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    CACHE_MAX_SIZE: int = 128
    YFINANCE_PERIOD: str = "3mo"
    TOP_N_STOCKS: int = 10

    # Index configurations
    INDEX_CONFIGS: Dict = {
        # --- India ---
        "nifty50": {
            "name": "NIFTY 50",
            "country": "India",
            "region": "Asia-Pacific",
            "benchmark": "^NSEI",
            "tickers": [
                "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
                "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
                "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "TITAN.NS",
                "BAJFINANCE.NS", "WIPRO.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "POWERGRID.NS"
            ]
        },
        "sensex": {
            "name": "Sensex",
            "country": "India",
            "region": "Asia-Pacific",
            "benchmark": "^BSESN",
            "tickers": [
                "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO",
                "HINDUNILVR.BO", "ITC.BO", "SBIN.BO", "BHARTIARTL.BO", "KOTAKBANK.BO",
                "LT.BO", "AXISBANK.BO", "ASIANPAINT.BO", "MARUTI.BO", "TITAN.BO"
            ]
        },
        # --- United States ---
        "sp500": {
            "name": "S&P 500",
            "country": "United States",
            "region": "Americas",
            "benchmark": "^GSPC",
            "tickers": [
                "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "BRK-B", 
                "TSLA", "LLY", "AVGO", "JPM", "UNH", "V", "JNJ", "XOM", "PG", "MA", "HD"
            ]
        },
        "nasdaq": {
            "name": "Nasdaq Composite",
            "country": "United States",
            "region": "Americas",
            "benchmark": "^IXIC",
            "tickers": [
                "AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOGL", "GOOG", "TSLA",
                "AVGO", "COST", "PEP", "CSCO", "TMUS", "CMCSA", "ADBE", "INTC", "AMD"
            ]
        },
        "djia": {
            "name": "Dow Jones",
            "country": "United States",
            "region": "Americas",
            "benchmark": "^DJI",
            "tickers": [
                "UNH", "MSFT", "GS", "HD", "MCD", "CAT", "AMGN", "V", "BA", "TRV",
                "HON", "AAPL", "IBM", "CVX", "JNJ", "PG", "JPM", "WMT", "CRM"
            ]
        },
        # --- Canada ---
        "tsx": {
            "name": "S&P/TSX Composite",
            "country": "Canada",
            "region": "Americas",
            "benchmark": "^GSPTSE",
            "tickers": [
                "RY.TO", "TD.TO", "SHOP.TO", "ENB.TO", "CNQ.TO", "CP.TO", "CNR.TO", 
                "BMO.TO", "BNS.TO", "CSU.TO", "ATD.TO", "TRP.TO", "CM.TO", "MFC.TO"
            ]
        },
        # --- Brazil ---
        "ibovespa": {
            "name": "Ibovespa",
            "country": "Brazil",
            "region": "Americas",
            "benchmark": "^BVSP",
            "tickers": [
                "VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "B3SA3.SA",
                "PETR3.SA", "WEGE3.SA", "BBAS3.SA", "ABEV3.SA", "RENT3.SA", "SUZB3.SA"
            ]
        },
        # --- United Kingdom ---
        "ftse100": {
            "name": "FTSE 100",
            "country": "United Kingdom",
            "region": "Europe",
            "benchmark": "^FTSE",
            "tickers": [
                "SHEL.L", "AZN.L", "BHP.L", "HSBA.L", "ULVR.L", "BP.L",
                "DGE.L", "GSK.L", "RIO.L", "BATS.L", "GLEN.L", "REL.L"
            ]
        },
        # --- Germany ---
        "dax": {
            "name": "DAX",
            "country": "Germany",
            "region": "Europe",
            "benchmark": "^GDAXI",
            "tickers": [
                "SAP.DE", "SIE.DE", "DTE.DE", "ALV.DE", "AIR.DE", "MBG.DE", 
                "BMW.DE", "BAS.DE", "MUV2.DE", "DPW.DE", "BAYN.DE"
            ]
        },
        # --- France ---
        "cac40": {
            "name": "CAC 40",
            "country": "France",
            "region": "Europe",
            "benchmark": "^FCHI",
            "tickers": [
                "MC.PA", "RMS.PA", "OR.PA", "TTE.PA", "SAN.PA", "SU.PA",
                "AIR.PA", "EL.PA", "BNP.PA", "CS.PA", "AI.PA"
            ]
        },
        # --- Eurozone ---
        "eurostoxx50": {
            "name": "Euro STOXX 50",
            "country": "Eurozone",
            "region": "Europe",
            "benchmark": "^STOXX50E",
            "tickers": [
                "ASML.AS", "MC.PA", "SAP.DE", "TTE.PA", "OR.PA", "SAN.PA",
                "SIE.DE", "SU.PA", "ALV.DE", "AIR.PA", "BNP.PA"
            ]
        },
        # --- Japan ---
        "nikkei225": {
            "name": "Nikkei 225",
            "country": "Japan",
            "region": "Asia-Pacific",
            "benchmark": "^N225",
            "tickers": [
                "7203.T", "6861.T", "8306.T", "9984.T", "9983.T",
                "6758.T", "6857.T", "8035.T", "4063.T", "9432.T"
            ]
        },
        # --- China ---
        "sse": {
            "name": "SSE Composite",
            "country": "China",
            "region": "Asia-Pacific",
            "benchmark": "000001.SS",
            "tickers": [
                "600519.SS", "601398.SS", "601288.SS", "601939.SS", "601857.SS",
                "600036.SS", "601088.SS", "601628.SS", "600900.SS", "601988.SS"
            ]
        },
        # --- Hong Kong ---
        "hsi": {
            "name": "Hang Seng Index",
            "country": "Hong Kong",
            "region": "Asia-Pacific",
            "benchmark": "^HSI",
            "tickers": [
                "0700.HK", "9988.HK", "3690.HK", "1299.HK", "0939.HK",
                "1398.HK", "0005.HK", "0388.HK", "0883.HK", "0941.HK"
            ]
        },
        # --- Australia ---
        "asx200": {
            "name": "S&P/ASX 200",
            "country": "Australia",
            "region": "Asia-Pacific",
            "benchmark": "^AXJO",
            "tickers": [
                "BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX",
                "ANZ.AX", "MQG.AX", "WES.AX", "TLS.AX", "WOW.AX"
            ]
        },
        # --- Saudi Arabia ---
        "tasi": {
            "name": "Tadawul All Share",
            "country": "Saudi Arabia",
            "region": "Middle East & Africa",
            "benchmark": "^TASI.SR",
            "tickers": [
                "2222.SR", "1120.SR", "2010.SR", "1180.SR", "1010.SR",
                "2220.SR", "1111.SR", "2350.SR", "7010.SR", "5110.SR"
            ]
        },
        # --- South Africa ---
        "jse": {
            "name": "FTSE/JSE Top 40",
            "country": "South Africa",
            "region": "Middle East & Africa",
            "benchmark": "^J200.JO",
            "tickers": [
                "NPN.JO", "PRX.JO", "CFR.JO", "AGL.JO", "FSR.JO",
                "SBK.JO", "BTI.JO", "GLN.JO", "MTN.JO", "SLM.JO"
            ]
        }
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
