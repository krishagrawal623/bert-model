export interface SentimentResponse {
  sentiment?: string;
  confidence?: number;
  error?: string;
}

// Base URL (local backend)
const BASE_URL = "http://127.0.0.1:8000";

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

