import logging
import sys
from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from services.market_service import get_index_data, get_top_stocks

# Logging setup
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade market intelligence API powered by yfinance",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "endpoints": ["/api/indices/{name}/tickers", "/api/indices/{name}/full", "/api/indices/{name}/top", "/api/market-summary", "/health"],
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/indices")
async def get_indices():
    """Return list of supported market indices."""
    return {
        "indices": [
            {
                "key": key, 
                "name": cfg["name"], 
                "country": cfg.get("country", "Global"),
                "region": cfg.get("region", "Global"),
                "ticker_count": len(cfg["tickers"])
            }
            for key, cfg in settings.INDEX_CONFIGS.items()
        ]
    }


@app.get("/api/indices/{name}/tickers")
async def get_index_tickers_api(name: str):
    """
    Get generic dynamic constituents for a specific index utilizing index_service scraping.
    """
    name = name.lower().strip()
    if name not in settings.INDEX_CONFIGS:
        raise HTTPException(status_code=404, detail=f"Unknown index {name}")
    
    from services.index_service import get_index_tickers
    
    try:
        tickers = get_index_tickers(name)
        return {
            "index": name,
            "source": "dynamic_scraping",
            "count": len(tickers),
            "tickers": tickers
        }
    except NotImplementedError as e:
        config = settings.INDEX_CONFIGS[name]
        return {
            "index": name,
            "source": "static_fallback",
            "count": len(config.get("tickers", [])),
            "tickers": config.get("tickers", []),
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Error serving dynamic constituents for {name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed fetching constituents: {str(e)}")

@app.get("/api/indices/{name}/full")
async def get_index_full(
    name: str = Path(..., description="Index key"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD")
):
    """
    Get all stock metrics computed within the entire index array.
    """
    name = name.lower().strip()
    if date is None:
        date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        
    try:
        return get_index_data(name, date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error serving full data for {name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/indices/{name}/top")
async def get_index_top(
    name: str = Path(..., description="Index key"),
    date: Optional[str] = Query(None, description="Date YYYY-MM-DD"),
    n: int = Query(10, description="Number of results"),
    metric: str = Query("performance", description="Metric to sort by (performance, rsi, volume, volatility)"),
    reverse: bool = Query(True, description="True for ascending rank, False for descending")
):
    """
    Get the top N stocks dynamically filtered.
    """
    name = name.lower().strip()
    if date is None:
        date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        
    try:
        full_data = get_index_data(name, date)
        if "data" not in full_data or not full_data["data"]:
            return {"index": name, "date": date, "metric": metric, "results": []}
            
        top_stocks = get_top_stocks(full_data["data"], n=n, metric=metric, reverse=reverse)
        
        return {
            "index": name,
            "date": date,
            "metric": metric,
            "count": len(top_stocks),
            "results": top_stocks
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error serving top data for {name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market-summary")
async def market_summary(
    index: str = Query(default="nifty50", description="Index key for the market summary"),
    date: Optional[str] = Query(
        default=None,
        description="Date in YYYY-MM-DD format. Defaults to today (or last trading day).",
    ),
):
    """
    Legacy API wrapping the new dynamic system. Returns multiple top lists in one payload.
    Used natively by the React client.
    """
    if date is None:
        date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    index = index.lower().strip()

    try:
        full_data = get_index_data(index, date)
        if "data" not in full_data or not full_data["data"]:
            return {
                "index": index,
                "index_name": settings.INDEX_CONFIGS.get(index, {}).get("name", index),
                "date": date,
                "total_stocks_analyzed": 0,
                "gainers": [],
                "losers": [],
                "high_volume": [],
                "volatile": [],
                "market_breadth": {"advances": 0, "declines": 0, "unchanged": 0},
            }
        
        all_metrics = full_data["data"]
        n = settings.TOP_N_STOCKS
        
        gainers = get_top_stocks(all_metrics, n=n, metric="performance", reverse=True)
        losers = get_top_stocks(all_metrics, n=n, metric="performance", reverse=False)
        high_volume = get_top_stocks(all_metrics, n=n, metric="volume", reverse=True)
        volatile = get_top_stocks(all_metrics, n=n, metric="volatility", reverse=True)
        
        return {
            "index": index,
            "index_name": full_data["index_name"],
            "date": date,
            "total_stocks_analyzed": len(all_metrics),
            "gainers": gainers,
            "losers": losers,
            "high_volume": high_volume,
            "volatile": volatile,
            "market_breadth": {
                "advances": len([m for m in all_metrics if m["change_pct"] > 0]),
                "declines": len([m for m in all_metrics if m["change_pct"] < 0]),
                "unchanged": len([m for m in all_metrics if m["change_pct"] == 0]),
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
