import os
import traceback
import requests

# Use the Hugging Face Inference API instead of loading the model locally
# This avoids the ~1GB+ memory footprint of transformers + torch
MODEL_ID = "Krish623/sentiment-model"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

print(f"✅ Using HF Inference API for model: {MODEL_ID}")
if HF_TOKEN:
    print("🔑 HF_TOKEN is set")
else:
    print("⚠️ HF_TOKEN not set — requests may be rate-limited")


def predict_sentiment(text: str, threshold: float = 0.70):
    """
    Run sentiment prediction via the Hugging Face Inference API.
    """
    try:
        print(f"🔍 Input text: {text}")

        headers = {}
        if HF_TOKEN:
            headers["Authorization"] = f"Bearer {HF_TOKEN}"

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=60,
        )

        print(f"📡 HF API status: {response.status_code}")

        # If model is loading (cold start), HF returns 503
        if response.status_code == 503:
            return {"error": "Model is loading, please try again in ~30 seconds."}

        if response.status_code != 200:
            print(f"❌ HF API error: {response.text}")
            return {"error": f"HF API error ({response.status_code}): {response.text[:200]}"}

        results = response.json()
        print("🧠 Raw response:", results)

        if not results:
            return {"error": "Empty response from model"}

        # HF Inference API returns [[{label, score}, ...]]
        scores = results[0] if isinstance(results[0], list) else results

        best = max(scores, key=lambda x: x.get("score", 0))

        label = best.get("label", "Unknown")
        score = best.get("score", 0.0)

        sentiment = label if score >= threshold else "Neutral"

        return {
            "sentiment": sentiment,
            "confidence": round(score, 2)
        }

    except requests.exceptions.Timeout:
        return {"error": "Model took too long to respond. Try again."}
    except Exception as e:
        print("❌ FULL ERROR ↓↓↓")
        traceback.print_exc()
        return {"error": str(e) or "Unknown error"}