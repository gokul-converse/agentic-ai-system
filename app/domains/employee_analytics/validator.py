# app/domains/employee_analytics/validator.py

class EmployeeAnalyticsValidator:
    """
    Validates LLM-selected axis against available schema context.
    """

    @staticmethod
    def validate(x_axis: str, context: dict):
        
        available = context.get("available_dimensions", [])

        if not available:
            raise ValueError("No available dimensions to plot.")

        if x_axis not in available:
            raise ValueError(
                f"Invalid x_axis '{x_axis}'. "
                f"Must be one of {available}"
            )
