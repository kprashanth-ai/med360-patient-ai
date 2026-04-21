from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Literal


class ClinicalState(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    session_id: ObjectId

    chief_complaint: str | None = None
    symptoms: list[str] = []
    duration: str | None = None
    severity: str | None = None
    chronic_conditions: list[str] = []
    medications: list[str] = []
    red_flags: list[str] = []
    missing_info: list[str] = []
    report_findings_summary: str | None = None
    urgency_level: Literal["low", "moderate", "high", "emergency"] | None = None
    recommendation_status: Literal["pending", "ready"] = "pending"

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
