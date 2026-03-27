from transformers import pipeline

# 🌐 Load model from Hugging Face
classifier = pipeline(
    "text-classification",
    model="Krish623/sentiment-model"
)

label_map = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

def predict_sentiment(text: str, threshold: float = 0.70):
    result = classifier(text, truncation=True)

    score = result[0]['score']
    label = result[0]['label']

    # If labels are already fixed in model config
    if label in ["Negative", "Neutral", "Positive"]:
        sentiment = label
    else:
        sentiment = label_map.get(label, "Neutral")

    if score < threshold:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "confidence": round(score, 2)
    }


# 🔥 Test
if __name__ == "__main__":
    print(predict_sentiment("I love this!"))
    print(predict_sentiment("This is okay"))
    print(predict_sentiment("Worst experience ever"))