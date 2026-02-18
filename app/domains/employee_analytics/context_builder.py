from typing import Dict, List


class EmployeeAnalyticsContextBuilder:
    def build(self, payload: Dict) -> Dict:
        table_name = payload["table_name"]
        columns = payload["existing_columns"]
        selected = payload["selected_column"]

        metric_name = selected["name"]

        # ---- find metric column from schema ----
        metric_column = next(
            (
                c
                for c in columns
                if c.get("name", "").strip().lower() == metric_name.strip().lower()
            ),
            None,
        )

        if not metric_column:
            raise ValueError(f"Metric '{metric_name}' not found in existing_columns")

        # 🔑 SINGLE SOURCE OF TRUTH
        y_table_name = metric_column["parent_table"]

        # ---- X-axis candidates (string columns only) ----
        x_candidates: List[str] = []
        for c in columns:
            col_type = c.get("type") or c.get("data_type")
            if col_type == "string":
                x_candidates.append(c["name"])

        if not x_candidates:
            raise ValueError("No valid string columns for x-axis")

        return {
            "table_name": table_name,
            "metric": metric_name,
            "y_table_name": y_table_name,
            "x_candidates": x_candidates,
            "columns": columns,
        }
