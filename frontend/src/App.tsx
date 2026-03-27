import React, { useEffect, useState } from "react";
import { Moon, Sun, Sparkles } from "lucide-react";
import { analyzeText, SentimentResponse } from "./api";

type SentimentLabel = "positive" | "negative" | "neutral" | "unknown";

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SentimentLabel>("unknown");
  const [error, setError] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);

  // Theme bootstrap
  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (
      saved === "dark" ||
      (!saved && window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      setDarkMode(true);
    }
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResult("unknown");
    setConfidence(null);

    try {
      const res: SentimentResponse = await analyzeText(text.trim());

      if (res.error) {
        setError(res.error);
        return;
      }

      setConfidence(res.confidence ?? null);

      const raw = (res.sentiment ?? "").toLowerCase();
      if (raw === "positive" || raw === "negative" || raw === "neutral") {
        setResult(raw as SentimentLabel);
      } else {
        setResult("unknown");
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong talking to the backend.");
    } finally {
      setIsLoading(false);
    }
  };

  const sentimentColor =
    result === "positive"
      ? "text-emerald-500 bg-emerald-50 dark:bg-emerald-900/20"
      : result === "negative"
      ? "text-rose-500 bg-rose-50 dark:bg-rose-900/20"
      : result === "neutral"
      ? "text-yellow-500 bg-yellow-50 dark:bg-yellow-900/20"
      : "text-slate-500 bg-slate-50 dark:bg-slate-800/60";

  const sentimentLabel =
    result === "positive"
      ? "Positive"
      : result === "negative"
      ? "Negative"
      : result === "neutral"
      ? "Neutral"
      : "Awaiting analysis";

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-50 transition-colors">
      {/* Top bar */}
      <header className="border-b border-slate-200/70 dark:border-slate-800/70 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl">
        <div className="max-w-4xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="relative">
              <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-sky-400 to-blue-600 blur-md opacity-60" />
              <div className="relative rounded-xl bg-sky-400 dark:bg-blue-900 text-white px-2.5 py-1.5 text-xs font-semibold tracking-tight">
                X-Sentiment Pro
              </div>
            </div>
            <span className="hidden sm:inline text-xs text-slate-500 dark:text-slate-400">
              React UI connected to FastAPI sentiment backend
            </span>
          </div>

          <button
            onClick={() => setDarkMode((v) => !v)}
            className="inline-flex items-center justify-center w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            aria-label="Toggle theme"
          >
            {darkMode ? (
              <Sun className="w-4 h-4 text-yellow-400" />
            ) : (
              <Moon className="w-4 h-4 text-slate-600" />
            )}
          </button>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-4 py-10 space-y-8">
        {/* Hero */}
        <section className="space-y-3">
          <div className="inline-flex items-center gap-2 rounded-full bg-slate-100 dark:bg-slate-800 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">
            <Sparkles className="w-3.5 h-3.5 text-sky-500" />
            Live sentiment from your ML model
          </div>
          <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">
            Paste any{" "}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-sky-500 to-blue-600">
              tweet, comment, or text
            </span>{" "}
            and see the mood.
          </h1>
          <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-2xl">
            This UI sends your text directly to the FastAPI `/predict` endpoint
            and displays the sentiment predicted by your ML model.
          </p>
        </section>

        {/* Input + result card */}
        <section className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
          {/* Input card */}
          <form
            onSubmit={handleAnalyze}
            className="rounded-2xl bg-white/90 dark:bg-slate-900/80 border border-slate-200/80 dark:border-slate-800/80 shadow-sm p-5 space-y-4"
          >
            <label className="block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500 dark:text-slate-400">
              Text to analyze
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={5}
              placeholder="Type or paste the text whose sentiment you want to analyze…"
              className="w-full resize-none rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500/50"
            />

            <div className="flex items-center justify-between gap-3">
              <p className="text-[11px] text-slate-500 dark:text-slate-500">
                Backend endpoint:{" "}
                <code className="rounded bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5">
                  POST /predict
                </code>
              </p>
              <button
                type="submit"
                disabled={!text.trim() || isLoading}
                className="inline-flex items-center justify-center rounded-xl bg-sky-500 hover:bg-sky-600 disabled:bg-slate-400 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors"
              >
                {isLoading ? "Analyzing…" : "Analyze sentiment"}
              </button>
            </div>

            {error && (
              <p className="text-xs text-rose-500 bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-800 rounded-xl px-3 py-2">
                {error}
              </p>
            )}
          </form>

          {/* Result card */}
          <div className="rounded-2xl bg-white/90 dark:bg-slate-900/80 border border-slate-200/80 dark:border-slate-800/80 shadow-sm p-5 flex flex-col justify-between gap-4">
            <div>
              <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500 dark:text-slate-400 mb-2">
                Model output
              </h2>
              <div
                className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${sentimentColor}`}
              >
                <span className="w-2 h-2 rounded-full bg-current" />
                {sentimentLabel}
              </div>

              {/* Confidence bar */}
              {confidence !== null && (
                <div className="mt-3">
                  <div className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-full">
                    <div
                      className="h-2 rounded-full bg-sky-500"
                      style={{ width: `${confidence * 100}%` }}
                    />
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    {(confidence * 100).toFixed(1)}% confidence
                  </p>
                </div>
              )}
            </div>

            <p className="text-xs text-slate-500 dark:text-slate-500">
              This reflects your backend prediction (positive / negative /
              neutral). You can extend this further with explanations or emotion
              detection.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
};

export default App;
