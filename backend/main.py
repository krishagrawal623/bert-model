from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_sentiment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sentiment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class TextInput(BaseModel):
    text: str


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Sentiment API is running"}

# Predict endpoint
@app.post("/predict/")
def sentiment_prediction(input: TextInput):
    return predict_sentiment(input.text)
