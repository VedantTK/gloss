import React, { useState } from "react";
import { motion } from "framer-motion";
import { format, subDays } from "date-fns";
import { Header } from "./components/Header";
import { Dashboard } from "./components/Dashboard";
import { useMarketData } from "./hooks/useMarketData";
import { useIndices } from "./hooks/useIndices";
import { IndexKey, IndexInfo } from "./types";
import "./index.css";

const DEFAULT_DATE = format(subDays(new Date(), 1), "yyyy-MM-dd");

function App() {
  const { indices, loading: indicesLoading } = useIndices();
  
  const [selectedCountry, setSelectedCountry] = useState<string>("India");
  const [selectedIndex, setSelectedIndex] = useState<IndexKey>("nifty50");
  const [selectedDate, setSelectedDate] = useState(DEFAULT_DATE);

  // Sync index when country changes
  React.useEffect(() => {
    if (indices.length > 0) {
      const availableIndices = indices.filter(i => i.country === selectedCountry);
      if (availableIndices.length > 0 && !availableIndices.find(i => i.key === selectedIndex)) {
        setSelectedIndex(availableIndices[0].key);
      }
    }
  }, [selectedCountry, indices, selectedIndex]);

  const { data, loading: marketLoading, error, lastUpdated, refetch } = useMarketData(
    selectedIndex,
    selectedDate
  );

  const activeIndexName = indices.find(i => i.key === selectedIndex)?.name || selectedIndex;
  const isLoading = indicesLoading || marketLoading;

  return (
    <div className="min-h-screen bg-obsidian-950 font-body">
      {/* Background mesh */}
      <div className="fixed inset-0 bg-mesh-dark pointer-events-none" />

      {/* Ambient glows */}
      <div className="fixed top-0 left-1/4 w-96 h-96 bg-jade-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed top-0 right-1/4 w-96 h-96 bg-azure-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-1/4 left-0 w-64 h-64 bg-violet-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <Header
        indices={indices}
        selectedCountry={selectedCountry}
        onCountryChange={setSelectedCountry}
        selectedIndex={selectedIndex}
        onIndexChange={setSelectedIndex}
        selectedDate={selectedDate}
        onDateChange={setSelectedDate}
        data={data}
        loading={isLoading}
        lastUpdated={lastUpdated}
      />

      {/* Main content */}
      <main className="relative z-10 max-w-[1600px] mx-auto px-6 py-8">
        {/* Page subtitle */}
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3">
            <div className="h-px flex-1 bg-gradient-to-r from-transparent via-white/10 to-transparent" />
            <span className="text-xs font-mono text-white/20 uppercase tracking-widest px-4">
              {selectedDate} · {activeIndexName.toUpperCase()}
            </span>
            <div className="h-px flex-1 bg-gradient-to-r from-transparent via-white/10 to-transparent" />
          </div>
        </motion.div>

        {/* Dashboard panels */}
        <Dashboard
          data={data}
          loading={isLoading}
          error={error}
          onRetry={refetch}
          country={selectedCountry}
        />

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-16 pb-8 text-center"
        >
          <p className="text-xs font-mono text-white/15">
            Data sourced via yfinance · For informational purposes only · Not financial advice
          </p>
        </motion.footer>
      </main>
    </div>
  );
}

export default App;
