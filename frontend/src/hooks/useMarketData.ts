import { useState, useEffect, useCallback, useRef } from "react";
import { IndexKey, MarketSummary } from "../types";
import { fetchMarketSummary } from "../utils/api";

interface UseMarketDataResult {
  data: MarketSummary | null;
  loading: boolean;
  error: string | null;
  lastUpdated: Date | null;
  refetch: () => void;
}

export function useMarketData(
  index: IndexKey,
  date: string
): UseMarketDataResult {
  const [data, setData] = useState<MarketSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const fetch = useCallback(async () => {
    if (abortRef.current) abortRef.current.abort();
    abortRef.current = new AbortController();

    setLoading(true);
    setError(null);

    try {
      const result = await fetchMarketSummary(index, date);
      setData(result);
      setLastUpdated(new Date());
    } catch (err: any) {
      if (err.name !== "AbortError") {
        setError(err.message || "Failed to fetch market data");
      }
    } finally {
      setLoading(false);
    }
  }, [index, date]);

  useEffect(() => {
    fetch();
    return () => abortRef.current?.abort();
  }, [fetch]);

  return { data, loading, error, lastUpdated, refetch: fetch };
}
