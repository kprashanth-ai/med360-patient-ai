from typing import Literal
from pydantic import BaseModel


class CollectedPatientData(BaseModel):
    age: int
    gender: Literal["male", "female", "other"]
    severity: Literal["low", "medium", "high"]
    duration_days: int
    symptoms: str


class ChatTurn(BaseModel):
    message: str
    urgency_level: Literal["none", "low", "moderate", "high", "emergency"] = "none"
    suggested_next_step: Literal["none", "monitor", "teleconsult", "home_visit", "specialist", "emergency"] = "none"
    escalation_note: str | None = None
    ready_to_recommend: bool = False
    patient_data: CollectedPatientData | None = None
