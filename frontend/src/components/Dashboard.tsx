import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MarketPanel } from "./panels/MarketPanel";
import { ErrorState } from "./ui/ErrorState";
import { MarketSummary, PanelConfig } from "../types";

interface DashboardProps {
  data: MarketSummary | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  country: string;
}

const PANEL_CONFIGS: PanelConfig[] = [
  {
    key: "gainers",
    label: "Top Gainers",
    icon: "📈",
    accent: "jade",
    glowClass: "glow-jade",
    description: "Highest daily percentage gains",
  },
  {
    key: "losers",
    label: "Top Losers",
    icon: "📉",
    accent: "crimson",
    glowClass: "glow-crimson",
    description: "Highest daily percentage drops",
  },
  {
    key: "high_volume",
    label: "Volume Leaders",
    icon: "🔊",
    accent: "azure",
    glowClass: "",
    description: "Unusual volume activity vs average",
  },
  {
    key: "volatile",
    label: "Volatility Watch",
    icon: "⚡",
    accent: "violet",
    glowClass: "",
    description: "Highest annualized volatility",
  },
];

export const Dashboard: React.FC<DashboardProps> = ({ data, loading, error, onRetry, country }) => {
  if (error && !loading) {
    return <ErrorState message={error} onRetry={onRetry} />;
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={data?.date || "loading"}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6"
      >
        {PANEL_CONFIGS.map((cfg) => (
          <MarketPanel
            key={cfg.key}
            config={cfg}
            stocks={data ? data[cfg.key] : []}
            loading={loading}
            country={country}
          />
        ))}
      </motion.div>
    </AnimatePresence>
  );
};
