import { useState } from "react";
import { analyzeResume } from "../utils/api";

/**
 * Custom hook for calling the /api/analyze endpoint.
 * Returns { analyze, loading, error, result }.
 */
export function useAnalyze() {
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);
  const [result, setResult]   = useState(null);

  const analyze = async (resumeFile, jdText) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeResume(resumeFile, jdText);
      setResult(data);
      return data;
    } catch (err) {
      const message =
        err?.response?.data?.detail ||
        err?.message ||
        "Something went wrong. Please try again.";
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { analyze, loading, error, result };
}
