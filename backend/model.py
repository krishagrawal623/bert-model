import os
import traceback
import requests

# Call your custom model hosted on HF Spaces (free, 16GB RAM)
SPACE_URL = "https://krish623-sentiment-api.hf.space/api/predict"

print("✅ Using HF Space for model: Krish623/sentiment-model")


def predict_sentiment(text: str, threshold: float = 0.70):
    """
    Run sentiment prediction via the HF Space Gradio API.
    """
    try:
        print(f"🔍 Input text: {text}")

        response = requests.post(
            SPACE_URL,
            json={"data": [text]},
            timeout=120,
        )

        print(f"📡 Space API status: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Space error: {response.text}")
            return {"error": f"Space error ({response.status_code}): {response.text[:200]}"}

        result = response.json()
        print("🧠 Raw response:", result)

        # Gradio returns {"data": [{"label": "...", "score": ...}]}
        data = result.get("data", [None])[0]

        if data is None:
            return {"error": "Empty response from model"}

        label = data.get("label", "Unknown")
        score = data.get("score", 0.0)

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