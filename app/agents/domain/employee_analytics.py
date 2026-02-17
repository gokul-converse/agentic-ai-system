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

    def __init__(self):
        super().__init__(
            name="employee_analytics_agent",
            role="Employee Analytics & Chart Recommendation Agent"
        )

    def run(self, payload: dict) -> dict:
        logger.info("[EmployeeAnalyticsAgent] Started")

        # 1️⃣ Build context (SINGLE SOURCE OF TRUTH)
        context = EmployeeAnalyticsContextBuilder().build(payload)

        # Safety: context builder must guarantee x_candidates
        if not context.get("x_candidates"):
            raise ValueError("No valid x-axis candidates available")

        # 2️⃣ Ask LLM ONLY for chart type + x-axis
        prompt = employee_analytics_prompt(context)
        raw = self.call_llm(prompt)

        # Defaults (safe fallback)
        chart_type = "bar"
        x_axis = context["x_candidates"][0]

        # 3️⃣ Parse LLM response safely
        if raw:
            try:
                parsed = json.loads(raw)
                chart_type = parsed.get("chart_type", chart_type)
                x_axis = parsed.get("x_axis", x_axis)
            except Exception:
                logger.warning(
                    "[EmployeeAnalyticsAgent] Failed to parse LLM output, using defaults"
                )

        # 4️⃣ Validate chosen x-axis
        EmployeeAnalyticsValidator.validate(x_axis, context)

        # 5️⃣ FINAL RESPONSE (NO TABLE LOGIC HERE 🔥)
        return {
            "table_name": context["table_name"],
            "chart": {
                "type": chart_type,
                "x": x_axis,
                "y": context["metric"],
                "x_table_name": context["x_table_name"],
                "y_table_name": context["y_table_name"],
            }
        }
