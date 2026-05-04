# Gloss – Global Market Intelligence Dashboard

A production-ready fintech dashboard for real-time and historical analysis of global equity markets. Built with FastAPI + yfinance on the backend, React + Tailwind + Framer Motion on the frontend.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Indices** | 17 global indices: NIFTY 50, S&P 500, FTSE 100, DAX, Nikkei 225, and more |
| **Panels** | Top Gainers, Top Losers, Volume Leaders, Volatility Watch |
| **Metrics** | % change, RSI (14), annualized volatility, volume ratio, 52W high/low |
| **Historical** | Select any past trading date |
| **Dynamic Constituents** | Wikipedia/NSE scraping per index – no hardcoded ticker lists |
| **Performance** | Server-side TTL cache (yfinance calls batched, not repeated) |
| **UI** | Dark mode, glassmorphism, Framer Motion, mobile responsive |

---

## 🚀 Quick Start (Docker)

```bash
git clone <repo-url> gloss && cd gloss
cp .env.example .env
docker-compose up --build
open http://localhost:3000
```

Backend API docs: `http://localhost:8000/docs`

---

## ☁️ Deploying on Render

Render hosts the backend and frontend as two **separate services** — a Web Service (FastAPI) and a Static Site (React).

### Architecture on Render

```
Browser → Render Static Site (React) → Render Web Service (FastAPI)
```

> Render does **not** use docker-compose. You deploy each service independently using individual Dockerfiles.

---

### Step 1 — Push code to GitHub

```bash
git init
git add .
git commit -m "initial commit"
gh repo create gloss --public --source=. --push
# or push to an existing remote
git remote add origin https://github.com/<you>/gloss.git
git push -u origin main
```

---

### Step 2 — Deploy the Backend (FastAPI)

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repository
3. Fill in the settings:

| Field | Value |
|---|---|
| **Name** | `gloss-backend` |
| **Root Directory** | `backend` |
| **Environment** | `Docker` |
| **Dockerfile Path** | `./Dockerfile` |
| **Instance Type** | `Free` (or Starter for better performance) |

4. Add **Environment Variables**:

| Key | Value |
|---|---|
| `DEBUG` | `false` |
| `CACHE_TTL_SECONDS` | `300` |
| `TOP_N_STOCKS` | `10` |

5. Click **Create Web Service**. Render will build and deploy; copy the URL when done.
   - It will look like: `https://gloss-backend.onrender.com`

> **Important:** Free-tier Render services spin down after 15 mins of inactivity. The first request after sleep will take ~30 seconds.

---

### Step 3 — Deploy the Frontend (React + Nginx)

1. Go to Render → **New → Web Service** (choose Docker, NOT Static Site — because we use Nginx)
2. Connect the same repository
3. Fill in the settings:

| Field | Value |
|---|---|
| **Name** | `gloss-frontend` |
| **Root Directory** | `frontend` |
| **Environment** | `Docker` |
| **Dockerfile Path** | `./Dockerfile` |
| **Instance Type** | `Free` |

4. Add **Build-time Environment Variables** (under **Advanced → Build Args**):

| Key | Value |
|---|---|
| `REACT_APP_API_URL` | `https://gloss-backend.onrender.com` |

> This is a **Docker Build Arg**, not a normal env var. In Render, go to: **Advanced → Add Build Argument** and add `REACT_APP_API_URL`.

5. Click **Create Web Service**. Your frontend will be live at: `https://gloss-frontend.onrender.com`

---

### Step 4 — Fix CORS on the Backend

Once you have your frontend URL, add it to the backend's allowed origins. Edit `backend/config/settings.py`:

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://gloss-frontend.onrender.com",  # ← add your Render URL
]
```

Then re-push to GitHub — Render auto-deploys on every push.

---

### Render Deployment Summary

```
GitHub Push
    ├── backend/Dockerfile   → Render Web Service  (https://gloss-backend.onrender.com)
    └── frontend/Dockerfile  → Render Web Service  (https://gloss-frontend.onrender.com)
```

---

## 🌐 API Reference

### `GET /api/market-summary`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `index` | string | `nifty50` | Any index key from `/api/indices` |
| `date` | string | yesterday | `YYYY-MM-DD` format |

### `GET /api/indices/{name}/tickers`
Returns the full constituent list for an index (dynamic scraping + static fallback).

### `GET /api/indices/{name}/full`
Returns all computed stock metrics for the full index.

### `GET /api/indices/{name}/top`

| Parameter | Default | Description |
|---|---|---|
| `n` | `10` | Number of results |
| `metric` | `performance` | `performance`, `rsi`, `volume`, `volatility` |
| `reverse` | `true` | Sort direction |

### `GET /api/indices`
Lists all 17 supported indices with country and region metadata.

### `GET /health`
Health check — returns `{"status": "healthy"}`.

---

## 🏗 Architecture

```
gloss/
├── backend/
│   ├── main.py                  # FastAPI routes
│   ├── config/settings.py       # Pydantic settings, index configs
│   ├── services/
│   │   ├── market_service.py    # Metrics engine, get_top_stocks()
│   │   ├── index_service.py     # Wikipedia/NSE scraping, TTL cache
│   │   └── indicators.py        # RSI, volatility, volume ratio
│   ├── utils/data_fetcher.py    # yfinance bulk download
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Header.tsx       # Country/index selector
│   │   │   ├── Dashboard.tsx
│   │   │   ├── panels/MarketPanel.tsx
│   │   │   └── ui/StockCard.tsx
│   │   ├── hooks/useMarketData.ts
│   │   ├── utils/api.ts         # Dynamic currency formatting
│   │   └── types/index.ts
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml           # Local multi-container dev
└── README.md
```

---

## ⚙️ Supported Indices

| Key | Index | Region |
|---|---|---|
| `nifty50` | NIFTY 50 | Asia-Pacific |
| `sensex` | BSE Sensex | Asia-Pacific |
| `sp500` | S&P 500 | Americas |
| `nasdaq` | Nasdaq Composite | Americas |
| `djia` | Dow Jones | Americas |
| `tsx` | S&P/TSX Composite | Americas |
| `ibovespa` | Ibovespa | Americas |
| `ftse100` | FTSE 100 | Europe |
| `dax` | DAX | Europe |
| `cac40` | CAC 40 | Europe |
| `eurostoxx50` | Euro STOXX 50 | Europe |
| `nikkei225` | Nikkei 225 | Asia-Pacific |
| `hsi` | Hang Seng | Asia-Pacific |
| `asx200` | S&P/ASX 200 | Asia-Pacific |
| `sse` | SSE Composite | Asia-Pacific |
| `tasi` | Tadawul All Share | Middle East |
| `jse` | FTSE/JSE Top 40 | Africa |

---

## 📝 Notes

- yfinance data may have a 15–20 minute delay for recent dates
- Cache TTL is 5 minutes by default (configurable via `CACHE_TTL_SECONDS` env var)
- First request per index may take 10–30s (bulk data download); subsequent requests are served from cache
- S&P 500 fetches all ~503 constituents — this takes ~45s on first request; cache keeps it fast after that
- SSE Composite, TASI, and JSE fall back to curated static lists (no clean public scraping endpoint exists)

---

## License

MIT
