from pydantic import BaseModel
from typing import Literal


class RecommendationResponse(BaseModel):
    session_id: str
    urgency_level: Literal["low", "moderate", "high", "emergency"]
    next_step: Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"]
    suggested_specialty: str | None = None
    patient_message: str
    reasoning: str
