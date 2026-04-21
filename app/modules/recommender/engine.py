from typing import Literal
from pydantic import BaseModel


class SpecialistPathwayItem(BaseModel):
    specialist: str
    reason: str


class RecommendationResult(BaseModel):
    recommended_specialist: str
    primary_recommendation_summary: str
    symptom_explanation: str
    specialist_pathway: list[SpecialistPathwayItem]
    red_flags: list[str]
    urgency_level: Literal["low", "moderate", "high", "emergency"]
    next_step: Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"]
    disclaimer: str
