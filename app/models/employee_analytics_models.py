from typing import List

from pydantic import BaseModel


class ColumnSchema(BaseModel):
    name: str
    type: str | None = None
    data_type: str | None = None
    description: str | None = None
    is_separated: bool
    parent_table: str  # 🔥 REQUIRED — NO DEFAULT


class SelectedColumnSchema(BaseModel):
    name: str
    description: str | None = None
    data_type: str
    is_separated: bool
    parent_table: str  # 🔥 REQUIRED


class EmployeeAnalyticsRequest(BaseModel):
    table_name: str
    table_description: str | None = None
    selected_column: SelectedColumnSchema
    existing_columns: List[ColumnSchema]
