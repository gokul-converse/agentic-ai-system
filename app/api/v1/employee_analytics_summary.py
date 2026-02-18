from fastapi import APIRouter

from app.agents.domain.employee_analytics_summary import EmployeeAnalyticsSummaryAgent
from app.models.employee_analytics_summary_models import EmployeeAnalyticsSummaryRequest

router = APIRouter(tags=["Employee Analytics Summary"])

agent = EmployeeAnalyticsSummaryAgent()


@router.post("/employee-analytics/summary")
def summarize_employee_analytics(payload: EmployeeAnalyticsSummaryRequest):
    """
    Receives chart configuration and DB-computed aggregations
    and returns a natural-language summary.
    """
    return agent.run(payload.dict())
