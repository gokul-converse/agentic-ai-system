from app.agents.base import BaseAgent
from app.domains.employee_analytics_summary.context_builder import (
    EmployeeAnalyticsSummaryContextBuilder,
)
from app.domains.employee_analytics_summary.prompt_template import (
    employee_analytics_summary_prompt,
)
from app.domains.employee_analytics_summary.validator import (
    EmployeeAnalyticsSummaryValidator,
)


class EmployeeAnalyticsSummaryAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="employee_analytics_summary_agent",
            role="Employee Analytics Insight & Summary Agent",
        )

    def run(self, payload: dict) -> dict:
        # 1️⃣ Validate payload structure
        EmployeeAnalyticsSummaryValidator.validate(payload)

        # 2️⃣ Build clean context for LLM
        context = EmployeeAnalyticsSummaryContextBuilder().build(payload)

        # 3️⃣ Generate prompt
        prompt = employee_analytics_summary_prompt(context)

        # 4️⃣ Call LLM
        summary = self.call_llm(prompt)

        # 5️⃣ Return summarized insight
        return {"summary": summary.strip()}
