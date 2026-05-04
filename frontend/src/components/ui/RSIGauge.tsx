import React from "react";
import { getRsiColor, getRsiLabel } from "../../utils/api";

interface RSIGaugeProps {
  rsi: number;
}

export const RSIGauge: React.FC<RSIGaugeProps> = ({ rsi }) => {
  const pct = Math.min(100, Math.max(0, rsi));
  const color = rsi >= 70 ? "#f87171" : rsi <= 30 ? "#34d399" : "#fbbf24";
  const colorClass = getRsiColor(rsi);
  const label = getRsiLabel(rsi);

  return (
    <div className="space-y-1">
      <div className="flex justify-between items-center">
        <span className="text-xs text-white/40 font-mono uppercase tracking-wider">RSI</span>
        <div className="flex items-center gap-1.5">
          <span className={`text-xs font-mono font-semibold ${colorClass}`}>{rsi.toFixed(1)}</span>
          <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-mono ${
            rsi >= 70 ? "bg-crimson-500/20 text-crimson-400" :
            rsi <= 30 ? "bg-jade-500/20 text-jade-400" :
            "bg-aurelius-500/20 text-aurelius-400"
          }`}>{label}</span>
        </div>
      </div>
      <div className="h-1 bg-obsidian-600 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{
            width: `${pct}%`,
            backgroundColor: color,
            boxShadow: `0 0 8px ${color}60`,
          }}
        />
      </div>
      {/* Zone markers */}
      <div className="relative h-px">
        <div className="absolute left-[30%] w-px h-2 -top-1 bg-jade-500/30" />
        <div className="absolute left-[70%] w-px h-2 -top-1 bg-crimson-500/30" />
      </div>
    </div>
  );
};
