def employee_analytics_summary_prompt(context: dict) -> str:
    return f"""
You are a senior data analyst.

You are given aggregated results that were already computed from the database.
DO NOT recalculate values.
DO NOT infer missing data.
ONLY summarize what is explicitly provided.

Chart Information:
- Chart Type: {context["chart_type"]}
- X Axis: {context["x_axis"]}
- Y Axis: {context["y_axis"]}
- X Source Table: {context["x_table"]}
- Y Source Table: {context["y_table"]}

Aggregated Metrics:
- Average: {context["aggregations"]["avg"]}
- Minimum: {context["aggregations"]["min"]}
- Maximum: {context["aggregations"]["max"]}
- Total: {context["aggregations"]["sum"]}

Write a concise analytical summary in 2–3 sentences.
Use professional, factual language.
"""
