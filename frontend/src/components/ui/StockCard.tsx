import React from "react";
import { motion } from "framer-motion";
import { StockMetrics, PanelType } from "../../types";
import { formatVolume, formatPrice } from "../../utils/api";
import { RSIGauge } from "./RSIGauge";

interface StockCardProps {
  stock: StockMetrics;
  rank: number;
  panelType: PanelType;
  index: number;
  country: string;
}

const TREND_CONFIG = {
  gainers: {
    changeBg: "bg-jade-500/15 text-jade-400 border border-jade-500/20",
    border: "hover:border-jade-500/30",
    glow: "hover:shadow-glow-jade",
    rankColor: "text-jade-500",
  },
  losers: {
    changeBg: "bg-crimson-500/15 text-crimson-400 border border-crimson-500/20",
    border: "hover:border-crimson-500/30",
    glow: "hover:shadow-glow-crimson",
    rankColor: "text-crimson-500",
  },
  high_volume: {
    changeBg: "bg-azure-500/15 text-azure-400 border border-azure-500/20",
    border: "hover:border-azure-500/30",
    glow: "hover:shadow-[0_0_30px_rgba(59,130,246,0.2)]",
    rankColor: "text-azure-500",
  },
  volatile: {
    changeBg: "bg-violet-500/15 text-violet-400 border border-violet-500/20",
    border: "hover:border-violet-500/30",
    glow: "hover:shadow-[0_0_30px_rgba(139,92,246,0.2)]",
    rankColor: "text-violet-500",
  },
};

export const StockCard: React.FC<StockCardProps> = ({ stock, rank, panelType, index, country }) => {
  const cfg = TREND_CONFIG[panelType];
  const isPositive = stock.change_pct > 0;

  // Volume bar - scale relative to ratio (max 3x = full bar)
  const volBarWidth = Math.min(100, (stock.volume_ratio / 3) * 100);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06, duration: 0.35, ease: [0.25, 0.46, 0.45, 0.94] }}
      whileHover={{ y: -2, transition: { duration: 0.2 } }}
      className={`
        group relative bg-obsidian-800/80 backdrop-blur-sm
        border border-white/[0.06] rounded-xl p-4 cursor-default
        transition-all duration-300 shadow-card
        ${cfg.border} ${cfg.glow}
      `}
    >
      {/* Top row */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className={`text-xs font-mono font-bold ${cfg.rankColor} opacity-60`}>
            #{rank}
          </span>
          <span className="font-display font-bold text-white text-sm tracking-wide">
            {stock.symbol}
          </span>
        </div>
        <span className={`text-xs font-mono font-bold px-2 py-1 rounded-md ${cfg.changeBg}`}>
          {isPositive ? "+" : ""}{stock.change_pct.toFixed(2)}%
        </span>
      </div>

      {/* Price */}
      <div className="mb-3">
        <span className="font-mono font-bold text-white text-lg tracking-tight">
          {formatPrice(stock.price, country)}
        </span>
      </div>

      {/* RSI */}
      <div className="mb-3">
        <RSIGauge rsi={stock.rsi} />
      </div>

      {/* Volume bar */}
      <div className="space-y-1">
        <div className="flex justify-between items-center">
          <span className="text-xs text-white/40 font-mono uppercase tracking-wider">Volume</span>
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-mono text-white/60">{formatVolume(stock.volume)}</span>
            <span className="text-[10px] font-mono text-white/30">
              {stock.volume_ratio.toFixed(1)}x avg
            </span>
          </div>
        </div>
        <div className="h-1 bg-obsidian-600 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${volBarWidth}%` }}
            transition={{ delay: index * 0.06 + 0.3, duration: 0.6, ease: "easeOut" }}
            className="h-full rounded-full"
            style={{
              background: panelType === "high_volume"
                ? "linear-gradient(90deg, #3b82f6, #60a5fa)"
                : panelType === "volatile"
                ? "linear-gradient(90deg, #8b5cf6, #a78bfa)"
                : isPositive
                ? "linear-gradient(90deg, #10b981, #34d399)"
                : "linear-gradient(90deg, #ef4444, #f87171)",
            }}
          />
        </div>
      </div>

      {/* 52W range */}
      <div className="mt-3 pt-3 border-t border-white/[0.04] flex justify-between text-[10px] font-mono text-white/30">
        <span>52W L: {formatPrice(stock.week52_low, country)}</span>
        <span>52W H: {formatPrice(stock.week52_high, country)}</span>
      </div>

      {/* Volatility badge (for volatile panel) */}
      {panelType === "volatile" && (
        <div className="mt-1 flex justify-end">
          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-violet-500/10 text-violet-400/70">
            σ {stock.volatility.toFixed(1)}%
          </span>
        </div>
      )}
    </motion.div>
  );
};
