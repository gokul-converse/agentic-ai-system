# app/domains/employee_analytics/context_builder.py

class EmployeeAnalyticsContextBuilder:
    """
    Builds clean analytical context from frontend payload
    for chart + axis decision.
    """

    def build(self, payload: dict) -> dict:
        table_name = payload["table_name"]
        selected_column = payload["selected_column"]
        existing_columns = payload["existing_columns"]

        metric = selected_column["name"]
        metric_type = selected_column.get("data_type", "number")

        # Dimension candidates = NON-metric columns
        dimension_candidates = [
            col["name"]
            for col in existing_columns
            if col["name"] != metric
        ]

        return {
            "user_prompt": (
                f"Choose the best x-axis column to visualize "
                f"{metric} from table {table_name}"
            ),
            "table_name": table_name,
            "metric": metric,
            "metric_type": metric_type,
            "available_dimensions": dimension_candidates,
            "columns_metadata": existing_columns,
            "table_description": payload.get("table_description", "")
        }
