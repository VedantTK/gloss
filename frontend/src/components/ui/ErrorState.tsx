import React from "react";
import { motion } from "framer-motion";

interface ErrorStateProps {
  message: string;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ message, onRetry }) => (
  <motion.div
    initial={{ opacity: 0, scale: 0.95 }}
    animate={{ opacity: 1, scale: 1 }}
    className="flex flex-col items-center justify-center py-24 text-center"
  >
    <div className="text-5xl mb-4">⚠️</div>
    <h3 className="font-display font-bold text-white text-xl mb-2">Data Unavailable</h3>
    <p className="text-white/40 font-body text-sm max-w-sm mb-6">{message}</p>
    <button
      onClick={onRetry}
      className="
        px-6 py-3 bg-jade-500/20 border border-jade-500/30 rounded-xl
        text-jade-400 font-display font-semibold text-sm
        hover:bg-jade-500/30 transition-all duration-200
        hover:shadow-glow-jade
      "
    >
      Retry
    </button>
  </motion.div>
);
