from fastapi import APIRouter
from app.agents.domain.employee_analytics import EmployeeAnalyticsAgent
from app.mock.employee_analytics_payload import EMPLOYEE_ANALYTICS_SAMPLE

router = APIRouter()
agent = EmployeeAnalyticsAgent()


@router.post("/employee-analytics")
def analyze_employee():
    return agent.run(EMPLOYEE_ANALYTICS_SAMPLE)
