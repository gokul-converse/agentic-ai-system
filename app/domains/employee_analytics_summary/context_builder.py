from typing import Dict


class EmployeeAnalyticsSummaryContextBuilder:
    def build(self, payload: Dict) -> Dict:
        chart = payload["chart"]
        aggregations = payload["aggregations"]

        return {
            "chart_type": chart["type"],
            "x_axis": chart["x"],
            "y_axis": chart["y"],
            "x_table": chart["x_table_name"],
            "y_table": chart["y_table_name"],
            "aggregations": {
                "avg": aggregations.get("avg"),
                "min": aggregations.get("min"),
                "max": aggregations.get("max"),
                "sum": aggregations.get("sum"),
            }
        }
