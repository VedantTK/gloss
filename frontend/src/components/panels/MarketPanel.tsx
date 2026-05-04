import React from "react";
import { motion } from "framer-motion";
import { StockMetrics, PanelType, PanelConfig } from "../../types";
import { StockCard } from "../ui/StockCard";
import { PanelSkeleton } from "../ui/Skeleton";

interface MarketPanelProps {
  config: PanelConfig;
  stocks: StockMetrics[];
  loading: boolean;
  country: string;
}

export const MarketPanel: React.FC<MarketPanelProps> = ({ config, stocks, loading, country }) => {
  const accentColors: Record<string, string> = {
    jade: "from-jade-500/20 via-jade-500/5 to-transparent border-jade-500/20",
    crimson: "from-crimson-500/20 via-crimson-500/5 to-transparent border-crimson-500/20",
    azure: "from-azure-500/20 via-azure-500/5 to-transparent border-azure-500/20",
    violet: "from-violet-500/20 via-violet-500/5 to-transparent border-violet-500/20",
  };

  const headerAccent: Record<string, string> = {
    jade: "text-jade-400",
    crimson: "text-crimson-400",
    azure: "text-azure-400",
    violet: "text-violet-400",
  };

  const dotColor: Record<string, string> = {
    jade: "bg-jade-500",
    crimson: "bg-crimson-500",
    azure: "bg-azure-500",
    violet: "bg-violet-500",
  };

  const gradClass = accentColors[config.accent] || "";
  const hdrClass = headerAccent[config.accent] || "text-white";
  const dotClass = dotColor[config.accent] || "bg-white";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="flex flex-col"
    >
      {/* Panel header */}
      <div className={`
        mb-4 p-4 rounded-xl border bg-gradient-to-b backdrop-blur-sm
        ${gradClass}
      `}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-2 h-2 rounded-full ${dotClass} shadow-lg`}
              style={{ boxShadow: `0 0 10px currentColor` }}
            />
            <div>
              <h2 className={`font-display font-bold text-base ${hdrClass}`}>
                {config.label}
              </h2>
              <p className="text-xs text-white/40 font-body mt-0.5">{config.description}</p>
            </div>
          </div>
          <span className="text-2xl">{config.icon}</span>
        </div>

        {!loading && stocks.length > 0 && (
          <div className="mt-3 pt-3 border-t border-white/[0.06]">
            <span className="text-xs font-mono text-white/30">
              {stocks.length} stocks
            </span>
          </div>
        )}
      </div>

      {/* Stocks list */}
      <div className="space-y-3 flex-1">
        {loading ? (
          <PanelSkeleton />
        ) : stocks.length === 0 ? (
          <div className="text-center py-12 text-white/20 font-body">
            No data available
          </div>
        ) : (
          stocks.map((stock, i) => (
            <StockCard
              key={stock.ticker}
              stock={stock}
              rank={i + 1}
              panelType={config.key}
              index={i}
              country={country}
            />
          ))
        )}
      </div>
    </motion.div>
  );
};
