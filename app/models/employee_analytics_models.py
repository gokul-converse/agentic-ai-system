from pydantic import BaseModel
from typing import List, Dict


class SelectedColumn(BaseModel):
    name: str
    description: str
    data_type: str


class ExistingColumn(BaseModel):
    name: str
    type: str
    description: str


class EmployeeAnalyticsRequest(BaseModel):
    table_name: str
    table_description: str
    selected_column: SelectedColumn
    existing_columns: List[ExistingColumn]
