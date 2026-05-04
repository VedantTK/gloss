import React from "react";
import { motion } from "framer-motion";
import { MarketSummary, IndexInfo } from "../types";
import { format, subDays } from "date-fns";

interface HeaderProps {
  indices: IndexInfo[];
  selectedCountry: string;
  onCountryChange: (country: string) => void;
  selectedIndex: string;
  onIndexChange: (index: string) => void;
  selectedDate: string;
  onDateChange: (date: string) => void;
  data: MarketSummary | null;
  loading: boolean;
  lastUpdated: Date | null;
}

export const Header: React.FC<HeaderProps> = ({
  indices,
  selectedCountry,
  onCountryChange,
  selectedIndex,
  onIndexChange,
  selectedDate,
  onDateChange,
  data,
  loading,
  lastUpdated,
}) => {
  const maxDate = format(subDays(new Date(), 1), "yyyy-MM-dd");
  
  // Get unique countries
  const countries = Array.from(new Set(indices.map(i => i.country))).sort();
  const availableIndices = indices.filter(i => i.country === selectedCountry);

  return (
    <header className="sticky top-0 z-50 border-b border-white/[0.06] bg-obsidian-950/90 backdrop-blur-xl">
      <div className="max-w-[1600px] mx-auto px-6 py-4">
        <div className="flex flex-col xl:flex-row xl:items-center gap-4">

          {/* Logo */}
          <div className="flex items-center gap-3 flex-shrink-0">
            <div className="relative">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-jade-500 to-azure-500 flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M2 12L6 8L9 11L14 4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <div className="absolute -inset-1 bg-gradient-to-br from-jade-500/20 to-azure-500/20 rounded-lg blur-sm -z-10" />
            </div>
            <div>
              <h1 className="font-display font-black text-xl text-white tracking-tight">
                Gloss
              </h1>
              <p className="text-[10px] font-mono text-white/30 uppercase tracking-widest -mt-0.5">
                Market Intelligence
              </p>
            </div>
          </div>

          {/* Controls */}
          <div className="flex flex-wrap items-center gap-3 xl:ml-8">
            {/* Country Selector */}
            <div className="relative">
              <select
                value={selectedCountry}
                onChange={(e) => onCountryChange(e.target.value)}
                className="
                  bg-obsidian-800 border border-white/[0.08] rounded-xl
                  pl-4 pr-10 py-2.5 text-sm font-display font-semibold text-white/80
                  focus:outline-none focus:border-jade-500/40 focus:ring-1 focus:ring-jade-500/20
                  transition-all duration-200 cursor-pointer appearance-none
                "
              >
                {countries.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
              <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-white/40">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M6 9l6 6 6-6"/>
                </svg>
              </div>
            </div>

            {/* Index toggle */}
            <div className="flex items-center bg-obsidian-800 border border-white/[0.08] rounded-xl p-1 overflow-x-auto max-w-full hide-scrollbar">
              {availableIndices.map((index) => (
                <button
                  key={index.key}
                  onClick={() => onIndexChange(index.key)}
                  className={`
                    relative px-4 py-2 rounded-lg text-sm font-display font-semibold
                    transition-all duration-200 whitespace-nowrap
                    ${selectedIndex === index.key
                      ? "text-white"
                      : "text-white/40 hover:text-white/70"}
                  `}
                >
                  {selectedIndex === index.key && (
                    <motion.div
                      layoutId="index-tab"
                      className="absolute inset-0 bg-gradient-to-r from-jade-500/20 to-azure-500/20 border border-white/10 rounded-lg"
                      transition={{ type: "spring", stiffness: 400, damping: 30 }}
                    />
                  )}
                  <span className="relative z-10">
                    {index.name}
                  </span>
                </button>
              ))}
            </div>

            {/* Date picker */}
            <div className="relative flex-shrink-0">
              <input
                type="date"
                value={selectedDate}
                max={maxDate}
                onChange={(e) => onDateChange(e.target.value)}
                className="
                  bg-obsidian-800 border border-white/[0.08] rounded-xl
                  px-4 py-2.5 text-sm font-mono text-white/80
                  focus:outline-none focus:border-jade-500/40 focus:ring-1 focus:ring-jade-500/20
                  transition-all duration-200 cursor-pointer
                  [color-scheme:dark]
                "
              />
            </div>
          </div>

          {/* Right side stats */}
          <div className="flex items-center gap-6 xl:ml-auto">
            {data && !loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-4"
              >
                {/* Market breadth */}
                <div className="hidden md:flex items-center gap-4">
                  <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full bg-jade-500" />
                    <span className="text-xs font-mono text-jade-400">{data.market_breadth.advances} ↑</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full bg-crimson-500" />
                    <span className="text-xs font-mono text-crimson-400">{data.market_breadth.declines} ↓</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full bg-white/20" />
                    <span className="text-xs font-mono text-white/40">{data.market_breadth.unchanged} –</span>
                  </div>
                </div>

                <div className="text-right whitespace-nowrap">
                  <div className="text-xs font-mono text-white/60">{data.index_name}</div>
                  <div className="text-[10px] font-mono text-white/25">
                    {data.total_stocks_analyzed} stocks analyzed
                  </div>
                </div>
              </motion.div>
            )}

            {/* Live indicator */}
            <div className="flex items-center gap-2 flex-shrink-0">
              <div className={`w-2 h-2 rounded-full ${loading ? "bg-aurelius-500 animate-pulse" : "bg-jade-500"}`} />
              <span className="text-xs font-mono text-white/30 whitespace-nowrap">
                {loading ? "Loading..." : lastUpdated ? `Updated ${format(lastUpdated, "HH:mm:ss")}` : "Ready"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

