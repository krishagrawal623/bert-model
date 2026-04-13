import os
import time
import requests
import traceback

# Token must be set via environment variable (Render dashboard → Environment)
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError(
        "HF_TOKEN environment variable is not set. "
        "Add it in your Render dashboard under Settings → Environment."
    )

# Correct HF Inference API URL for community models
API_URL = "https://api-inference.huggingface.co/models/Krish623/sentiment-model"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def predict_sentiment(text: str, threshold: float = 0.70):
    """
    Call the Hugging Face Inference API for sentiment prediction.
    Includes retry logic to handle model cold-starts (loading from disk).
    """
    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔍 Input text: {text}  (attempt {attempt}/{max_retries})")

            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": text},
                timeout=60  # HF free tier can take 20-30s on cold start
            )

            print("📡 Status:", response.status_code)
            print("🧠 Raw response:", response.text)

            # Handle model loading (cold start) — HF returns 503
            if response.status_code == 503:
                body = response.json()
                wait_time = body.get("estimated_time", 20)
                print(f"⏳ Model is loading, retrying in {wait_time:.0f}s...")
                time.sleep(min(wait_time, 30))
                continue

            if response.status_code != 200:
                return {
                    "error": "API request failed",
                    "status_code": response.status_code,
                    "details": response.text
                }

            result = response.json()

            if not result:
                return {"error": "Empty response"}

            if isinstance(result[0], list):
                result = result[0]

            best = max(result, key=lambda x: x.get("score", 0))

            label = best.get("label", "Unknown")
            score = best.get("score", 0.0)

            sentiment = label if score >= threshold else "Neutral"

            return {
                "sentiment": sentiment,
                "confidence": round(score, 2)
            }

        except Exception as e:
            print("❌ FULL ERROR ↓↓↓")
            traceback.print_exc()
            if attempt == max_retries:
                return {"error": str(e) or "Unknown error"}
            print(f"🔄 Retrying in 5s...")
            time.sleep(5)

    return {"error": "Max retries exceeded"}