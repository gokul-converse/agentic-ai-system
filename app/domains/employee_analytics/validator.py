class EmployeeAnalyticsValidator:
    @staticmethod
    def validate(x_axis: str, context: dict):
        if not context.get("x_candidates"):
            raise ValueError("No available x-axis candidates")

        if x_axis not in context["x_candidates"]:
            raise ValueError(
                f"x_axis '{x_axis}' is invalid. "
                f"Allowed values: {context['x_candidates']}"
            )
