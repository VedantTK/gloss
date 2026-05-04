# Gloss – Global Market Intelligence Dashboard

A production-ready fintech dashboard for real-time and historical analysis of Indian equity markets. Built with FastAPI + yfinance on the backend, React + Tailwind + Framer Motion on the frontend.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Indices** | NIFTY 50, BANK NIFTY (extensible) |
| **Panels** | Top Gainers, Top Losers, Volume Leaders, Volatility Watch |
| **Metrics** | % change, RSI (14), annualized volatility, volume ratio, 52W high/low |
| **Historical** | Select any past trading date |
| **Performance** | Server-side TTL cache (yfinance calls batched, not repeated) |
| **UI** | Dark mode, glassmorphism, Framer Motion animations, mobile responsive |

---

## 🚀 Quick Start (Docker)

### Prerequisites
- Docker ≥ 24
- Docker Compose ≥ 2.x

### Steps

```bash
# 1. Clone the repo
git clone <repo-url> gloss && cd gloss

# 2. Copy environment file
cp .env.example .env

# 3. Build and run
docker-compose up --build

# 4. Open browser
open http://localhost:3000
```

The backend API docs are available at: http://localhost:8000/docs

---

## 🛠 Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run dev server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps

# Set env (create .env.local)
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local

npm start
```

---

## 🌐 API Reference

### `GET /api/market-summary`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `index` | string | `nifty50` | `nifty50` or `banknifty` |
| `date` | string | yesterday | `YYYY-MM-DD` format |

**Example:**
```
GET /api/market-summary?index=nifty50&date=2024-12-20
```

**Response:**
```json
{
  "index": "nifty50",
  "index_name": "NIFTY 50",
  "date": "2024-12-20",
  "total_stocks_analyzed": 48,
  "gainers": [
    {
      "symbol": "TCS",
      "ticker": "TCS.NS",
      "price": 4250.50,
      "change_pct": 3.12,
      "rsi": 62.4,
      "volatility": 24.1,
      "volume": 1234567,
      "volume_ratio": 1.8,
      "week52_high": 4592.0,
      "week52_low": 3200.0,
      "trend": "up"
    }
  ],
  "losers": [...],
  "high_volume": [...],
  "volatile": [...],
  "market_breadth": {
    "advances": 32,
    "declines": 15,
    "unchanged": 1
  }
}
```

### `GET /api/indices`
Returns list of all supported indices.

### `GET /health`
Health check endpoint.

---

## 🏗 Architecture

```
gloss/
├── backend/
│   ├── main.py                  # FastAPI app, routes
│   ├── config/
│   │   └── settings.py          # Pydantic settings, index configs
│   ├── services/
│   │   ├── market_service.py    # Core business logic, aggregation
│   │   └── indicators.py        # RSI, volatility, volume ratio
│   ├── utils/
│   │   └── data_fetcher.py      # yfinance bulk download, TTL cache
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── panels/MarketPanel.tsx
│   │   │   └── ui/{StockCard,RSIGauge,Skeleton,ErrorState}.tsx
│   │   ├── hooks/useMarketData.ts
│   │   ├── utils/api.ts
│   │   └── types/index.ts
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ⚙️ Extending Indices

To add a new index, edit `backend/config/settings.py`:

```python
INDEX_CONFIGS: Dict = {
    "sensex": {
        "name": "BSE SENSEX",
        "benchmark": "^BSESN",
        "tickers": ["RELIANCE.BO", "TCS.BO", ...]
    }
}
```

No other changes required — the API and frontend pick it up automatically.

---

## 📝 Notes

- yfinance data may have a 15–20 minute delay for recent dates
- Cache TTL is 5 minutes by default (configurable via env)
- First request per index may take 10–20s (bulk data download); subsequent requests are served from cache
- Historical dates beyond ~3 months may be limited; adjust `YFINANCE_PERIOD` in settings if needed

---

## License

MIT
