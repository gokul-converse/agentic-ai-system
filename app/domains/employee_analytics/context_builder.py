from typing import Dict, List


class EmployeeAnalyticsContextBuilder:
    def build(self, payload: Dict) -> Dict:
        table_name = payload["table_name"]
        columns = payload["existing_columns"]
        selected = payload["selected_column"]

        metric_name = selected["name"]

        # 🔒 Validate metric exists in schema
        metric_column = next(
            (
                c for c in columns
                if c.get("name", "").strip().lower()
                == metric_name.strip().lower()
            ),
            None
        )

        if not metric_column:
            raise ValueError(
                f"Metric '{metric_name}' not found in existing_columns"
            )

        # 🔥 UI-GRID RULE (THIS SOLVES EVERYTHING)
        # Each column is its OWN table
        y_table_name = metric_name

        # X-axis candidates → string columns from base grid
        x_candidates: List[str] = []
        for c in columns:
            col_type = c.get("type") or c.get("data_type")
            if (
                col_type == "string"
                and c.get("parent_table") == table_name
            ):
                x_candidates.append(c["name"])

        # Defensive fallback
        if not x_candidates:
            for c in columns:
                col_type = c.get("type") or c.get("data_type")
                if col_type == "string":
                    x_candidates.append(c["name"])

        if not x_candidates:
            raise ValueError("No valid string columns for x-axis")

        return {
            "table_name": table_name,
            "metric": metric_name,
            "x_table_name": table_name,
            "y_table_name": y_table_name,
            "metric_is_separated": metric_column.get("is_separated", False),
            "x_candidates": x_candidates,
        }
