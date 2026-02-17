from fastapi import APIRouter
from app.agents.domain.employee_analytics import EmployeeAnalyticsAgent
from app.models.employee_analytics_models import EmployeeAnalyticsRequest

router = APIRouter(tags=["Employee Analytics"])
agent = EmployeeAnalyticsAgent()


@router.post("/employee-analytics")
def analyze_employee(payload: EmployeeAnalyticsRequest):
    return agent.run(payload.dict())
