from typing import Any, Dict

from pydantic import BaseModel


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
