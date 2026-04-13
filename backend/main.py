from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_sentiment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sentiment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bert-model.vercel.app",
        "http://localhost:3000",       # Vite dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class TextInput(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"message": "Sentiment API is running"}


@app.post("/predict/")
async def sentiment_prediction(input: TextInput):
    print("📥 Incoming request:", input.text)

    result = predict_sentiment(input.text)

    print("📤 API RESULT:", result)

    return result