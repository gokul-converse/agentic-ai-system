from fastapi import APIRouter
from app.agents.domain.employee_analytics_summary import (
    EmployeeAnalyticsSummaryAgent
)

router = APIRouter(tags=["Employee Analytics Summary"])

agent = EmployeeAnalyticsSummaryAgent()


@router.post("/employee-analytics/summary")
def summarize_employee_analytics(payload: dict):
    """
    Receives chart config + DB-computed aggregations
    and returns a natural-language summary.
    """
    return agent.run(payload)
