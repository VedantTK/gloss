export type IndexKey = string;

export interface IndexInfo {
  key: string;
  name: string;
  country: string;
  region: string;
  ticker_count: number;
}

export interface StockMetrics {
  symbol: string;
  ticker: string;
  price: number;
  change_pct: number;
  rsi: number;
  volatility: number;
  volume: number;
  volume_ratio: number;
  week52_high: number;
  week52_low: number;
  trend: "up" | "down" | "neutral";
}

export interface MarketBreadth {
  advances: number;
  declines: number;
  unchanged: number;
}

export interface MarketSummary {
  index: string;
  index_name: string;
  date: string;
  total_stocks_analyzed: number;
  gainers: StockMetrics[];
  losers: StockMetrics[];
  high_volume: StockMetrics[];
  volatile: StockMetrics[];
  market_breadth: MarketBreadth;
}

export type PanelType = "gainers" | "losers" | "high_volume" | "volatile";

export interface PanelConfig {
  key: PanelType;
  label: string;
  icon: string;
  accent: string;
  glowClass: string;
  description: string;
}
