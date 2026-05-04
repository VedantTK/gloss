import { useState, useEffect, useCallback } from "react";
import { IndexInfo } from "../types";
import { fetchIndices } from "../utils/api";

export function useIndices() {
  const [indices, setIndices] = useState<IndexInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchIndices();
      setIndices(data.indices);
    } catch (err: any) {
      setError(err.message || "Failed to fetch indices");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { indices, loading, error, refetch: fetch };
}
