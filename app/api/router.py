from fastapi import APIRouter

from app.api.v1 import (
    document_ai,
    employee_analytics,
    employee_analytics_summary,
    text_ai,
)
from app.api.ws import chat_ws

router = APIRouter()


router.include_router(text_ai.router)
router.include_router(document_ai.router)
router.include_router(chat_ws.router)
router.include_router(employee_analytics.router)
router.include_router(employee_analytics_summary.router)
