from typing import Optional

from pydantic import BaseModel


class ChartConfig(BaseModel):
    type: str
    x: str
    y: str
    x_table_name: str
    y_table_name: str


class Aggregations(BaseModel):
    avg: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None


class EmployeeAnalyticsSummaryRequest(BaseModel):
    table_name: str
    chart: ChartConfig
    aggregations: Aggregations
