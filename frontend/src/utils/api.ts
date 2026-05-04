import { IndexKey, MarketSummary, IndexInfo } from "../types";

// Empty string = relative URL → Nginx proxies /api/ to the backend container.
// For local `npm start` dev, create frontend/.env.local:
//   REACT_APP_API_URL=http://localhost:8000
const API_BASE = process.env.REACT_APP_API_URL || "";

export async function fetchMarketSummary(
  index: IndexKey,
  date: string
): Promise<MarketSummary> {
  const url = `${API_BASE}/api/market-summary?index=${index}&date=${date}`;
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export async function fetchIndices(): Promise<{ indices: IndexInfo[] }> {
  const url = `${API_BASE}/api/indices`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

export function formatVolume(vol: number): string {
  if (vol >= 1_000_000_000) return `${(vol / 1_000_000_000).toFixed(1)}B`;
  if (vol >= 1_000_000) return `${(vol / 1_000_000).toFixed(1)}M`;
  if (vol >= 1_000) return `${(vol / 1_000).toFixed(0)}K`;
  return vol.toString();
}

interface CurrencyConfig {
  locale: string;
  symbol: string;
}

function getCurrencyConfig(country?: string): CurrencyConfig {
  switch (country) {
    case "India": return { locale: "en-IN", symbol: "₹" };
    case "United Kingdom": return { locale: "en-GB", symbol: "£" };
    case "Europe":
    case "Eurozone":
    case "France":
    case "Germany": return { locale: "de-DE", symbol: "€" };
    case "Japan": return { locale: "ja-JP", symbol: "¥" };
    case "China": return { locale: "zh-CN", symbol: "¥" };
    case "Hong Kong": return { locale: "en-HK", symbol: "HK$" };
    case "Australia": return { locale: "en-AU", symbol: "A$" };
    case "Canada": return { locale: "en-CA", symbol: "C$" };
    case "Brazil": return { locale: "pt-BR", symbol: "R$" };
    case "Saudi Arabia": return { locale: "ar-SA", symbol: "SAR " };
    case "South Africa": return { locale: "en-ZA", symbol: "R " };
    case "United States":
    default: return { locale: "en-US", symbol: "$" };
  }
}

export function formatPrice(price: number, country?: string): string {
  const { locale, symbol } = getCurrencyConfig(country);
  const formatted = new Intl.NumberFormat(locale, {
    maximumFractionDigits: 2,
    minimumFractionDigits: 2,
  }).format(price);
  return `${symbol}${formatted}`;
}

export function getRsiColor(rsi: number): string {
  if (rsi >= 70) return "text-crimson-400";
  if (rsi <= 30) return "text-jade-400";
  return "text-aurelius-400";
}

export function getRsiLabel(rsi: number): string {
  if (rsi >= 70) return "Overbought";
  if (rsi <= 30) return "Oversold";
  return "Neutral";
}
