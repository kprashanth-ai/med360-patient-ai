from typing import Literal
from pydantic import BaseModel


class LabValue(BaseModel):
    name: str
    value: str
    unit: str | None = None
    reference_range: str | None = None
    status: Literal["normal", "abnormal", "borderline"]
    plain_meaning: str


class ReportFindings(BaseModel):
    report_type: str
    test_date: str | None = None
    abnormal_values: list[LabValue]
    normal_values: list[LabValue]
    notable_markers: list[str]
    overall_summary: str
    plain_explanation: str
    recommended_action: str
    urgency: Literal["routine", "soon", "urgent"]
