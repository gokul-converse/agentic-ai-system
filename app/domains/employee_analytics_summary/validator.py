class EmployeeAnalyticsSummaryValidator:

    @staticmethod
    def validate(payload: dict):
        if "chart" not in payload:
            raise ValueError("Missing chart configuration")

        if "aggregations" not in payload:
            raise ValueError("Missing aggregations data")

        required_aggs = {"avg", "min", "max", "sum"}
        if not any(k in payload["aggregations"] for k in required_aggs):
            raise ValueError(
                "At least one aggregation value (avg, min, max, sum) is required"
            )
