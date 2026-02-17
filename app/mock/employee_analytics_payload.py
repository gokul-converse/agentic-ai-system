EMPLOYEE_ANALYTICS_SAMPLE = {
    "table_name": "employee_performance",
    "table_description": (
        "Contains employee profile, role, salary, performance score, "
        "and project contribution details used for analytics dashboards."
    ),
    "selected_column": {
        "name": "salary",
        "description": "Employee base salary used for compensation analytics.",
        "data_type": "number"
    },
    "existing_columns": [
        {"name": "employee", "type": "string"},
        {"name": "department", "type": "string"},
        {"name": "position", "type": "string"},
        {"name": "salary", "type": "number"},
        {"name": "incentive", "type": "number"},
        {"name": "performance", "type": "number"},
        {"name": "status", "type": "string"},
        {"name": "growth", "type": "string"},
        {"name": "joinDate", "type": "string"},
        {"name": "projects", "type": "number"}
    ]
}
