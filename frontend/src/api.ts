export interface SentimentResponse {
  sentiment?: string;
  confidence?: number;
  error?: string;
}

// Base URL — reads from env var in production, falls back to localhost for dev
// Set VITE_API_URL in your deployment platform (e.g. Vercel, Netlify, Render)
// Example: VITE_API_URL=https://sentiment-api.onrender.com
const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function analyzeText(text: string): Promise<SentimentResponse> {
  try {
    const res = await fetch(`${BASE_URL}/predict/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();

    // Handle backend errors
    if (!res.ok) {
      return {
        error: data?.detail || "Backend error",
      };
    }

    return {
      sentiment: data.sentiment,
      confidence: data.confidence,
    };
  } catch (error) {
    return {
      error: "Unable to connect to backend",
    };
  }
}
