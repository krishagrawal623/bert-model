import os
import traceback
from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast, pipeline

# Download and cache model at startup
MODEL_ID = "Krish623/sentiment-model"

print(f"🔄 Loading model: {MODEL_ID}...")
# Load tokenizer explicitly (the uploaded tokenizer_config.json has
# an invalid tokenizer_class "TokenizersBackend" — workaround by
# specifying DistilBertTokenizerFast directly)
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)
print("✅ Model loaded successfully!")


def predict_sentiment(text: str, threshold: float = 0.70):
    """
    Run sentiment prediction locally using the downloaded model.
    """
    try:
        print(f"🔍 Input text: {text}")

        results = classifier(text)

        print("🧠 Raw response:", results)

        if not results:
            return {"error": "Empty response"}

        # pipeline with top_k=None returns [[{label, score}, ...]]
        scores = results[0] if isinstance(results[0], list) else results

        best = max(scores, key=lambda x: x.get("score", 0))

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
        return {"error": str(e) or "Unknown error"}