from gradio_client import Client
import traceback

client = Client("krish623/sentiment-api")

def predict_sentiment(text: str, threshold: float = 0.70):
    try:
        result = client.predict(
            text,
            api_name="//predict"   # ✅ IMPORTANT
        )

        label = result.get("label", "Unknown")
        score = result.get("score", 0.0)

        sentiment = label if score >= threshold else "Neutral"

        return {
            "sentiment": sentiment,
            "confidence": round(score, 2)
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
