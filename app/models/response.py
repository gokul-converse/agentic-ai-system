from pydantic import BaseModel
from typing import Dict, Any


class SummarizeResponse(BaseModel):
    summary: str

class ClassifyResponse(BaseModel):
    category: str

class SentimentResponse(BaseModel):
    sentiment: str

class InvoiceExtractionResponse(BaseModel):
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    response: Dict[str, Any]