import json
from app.agents.base import BaseAgent
from app.utils.logger import logger

from app.domains.employee_analytics.context_builder import (
    EmployeeAnalyticsContextBuilder
)
from app.domains.employee_analytics.prompt_template import (
    employee_analytics_prompt
)
from app.domains.employee_analytics.validator import (
    EmployeeAnalyticsValidator
)


class EmployeeAnalyticsAgent(BaseAgent):
    """
    Employee Analytics Agent
    - Fully inherits bro's BaseAgent
    - No infra logic touched
    - Works with API / WS / Orchestrator
    """

    def __init__(self):
        super().__init__(
            name="employee_analytics_agent",
            role="Employee Analytics & Chart Recommendation Agent"
        )

    def run(self, payload: dict) -> dict:
        """
        payload = structured frontend input (NOT plain text)
        """

        logger.info("[EmployeeAnalyticsAgent] Started")

        # 1️⃣ Build context from frontend payload
        context = EmployeeAnalyticsContextBuilder().build(payload)

        # 2️⃣ Build prompt (THIS is what LLM sees)
        prompt = employee_analytics_prompt(context)

        # 3️⃣ Call LLM via inherited BaseAgent method
        raw = self.call_llm(prompt)

        # 4️⃣ Safe parse + fallback
        if not raw or raw.strip() == "{}":
            logger.warning("[EmployeeAnalyticsAgent] Using fallback logic")
            chart_type = "bar"
            x_axis = "position"
        else:
            try:
                parsed = json.loads(raw)
                chart_type = parsed.get("chart_type", "bar")
                x_axis = parsed.get("x_axis", "position")
            except Exception:
                logger.warning("[EmployeeAnalyticsAgent] Invalid LLM JSON, fallback applied")
                chart_type = "bar"
                x_axis = "position"

        # 5️⃣ Validate LLM decision
        EmployeeAnalyticsValidator.validate(x_axis, context)

        # 6️⃣ Final response (FRONTEND CONTRACT)
        return {
            "table_name": context["table_name"],
            "chart": {
                "type": chart_type,
                "x": x_axis,
                "y": context["metric"],
                "x_table_name": f"{x_axis}s",
                "y_table_name": context["table_name"]
            }
        }
