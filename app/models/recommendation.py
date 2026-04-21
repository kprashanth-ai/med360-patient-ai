from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Literal


class Recommendation(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    session_id: ObjectId

    urgency_level: Literal["low", "moderate", "high", "emergency"]
    suggested_care_pathway: str
    suggested_specialty: str | None = None
    next_step: Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"]
    reasoning: str
    patient_message: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
