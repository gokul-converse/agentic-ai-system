def employee_analytics_summary_prompt(context: dict) -> str:
    return f"""
You are a senior data analyst.

You are given aggregated results that were already computed from the database.
DO NOT recalculate values.
DO NOT infer missing data.
DO NOT mention the chart type 
ONLY summarize what is explicitly provided.

IMPORTANT FORMATTING RULES:
- Use **bold** for key numeric values (avg, min, max, sum).
- Use *italic* for column names and axis references.
- Use plain paragraphs (no bullet points).
- Output MUST be valid Markdown.
- Keep the summary concise (2–3 sentences).

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

Write a professional analytical summary using Markdown formatting.
"""
