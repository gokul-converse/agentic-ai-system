import json
from app.agents.base import BaseAgent
from app.utils.logger import logger

from app.domains.employee_analytics.context_builder import EmployeeAnalyticsContextBuilder
from app.domains.employee_analytics.prompt_template import employee_analytics_prompt
from app.domains.employee_analytics.validator import EmployeeAnalyticsValidator


class EmployeeAnalyticsAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="employee_analytics_agent",
            role="Employee Analytics & Chart Recommendation Agent"
        )

    def run(self, payload: dict) -> dict:
        logger.info("[EmployeeAnalyticsAgent] Started")

        context = EmployeeAnalyticsContextBuilder().build(payload)

        raw = self.call_llm(employee_analytics_prompt(context))

        chart_type = "bar"
        x_axis = context["x_candidates"][0]

        if raw:
            try:
                parsed = json.loads(raw)
                chart_type = parsed.get("chart_type", chart_type)
                x_axis = parsed.get("x_axis", x_axis)
            except Exception:
                pass

        EmployeeAnalyticsValidator.validate(x_axis, context)

        # ---- resolve X table EXACTLY same way ----
        x_column = next(
            c for c in context["columns"] if c["name"] == x_axis
        )

        x_table_name = x_column["parent_table"]

        return {
            "table_name": context["table_name"],
            "chart": {
                "type": chart_type,
                "x": x_axis,
                "y": context["metric"],
                "x_table_name": x_axis,
                "y_table_name": context["y_table_name"],
            }
        }
