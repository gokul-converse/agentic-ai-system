from fastapi import APIRouter

from app.agents.domain.document_classification_agent import ClassificationAgent
from app.agents.domain.sentiment_analysis_agent import SentimentAgent
from app.agents.domain.summarization_agent import SummarizationAgent
from app.models.requests import TextInput
from app.models.response import ClassifyResponse, SentimentResponse, SummarizeResponse
from app.utils.logger import logger

router = APIRouter(prefix="/text", tags=["AI Features"])

summarizer = SummarizationAgent()
classifier = ClassificationAgent()
sentimenter = SentimentAgent()


@router.post("/summarize", response_model=SummarizeResponse)
def summarize_text(payload: TextInput):
    logger.info("[API] /ai/summarize called")
    result = summarizer.summarize(payload.text)
    return {"summary": result}


@router.post("/classify", response_model=ClassifyResponse)
def classify_text(payload: TextInput):
    logger.info("[API] /ai/classify called")
    result = classifier.classify(payload.text)
    return {"category": result}


@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(payload: TextInput):
    logger.info("[API] /ai/sentiment called")
    result = sentimenter.analyse(payload.text)
    return {"sentiment": result}
