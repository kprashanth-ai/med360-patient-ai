from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import build_patient_info, get_recommendation
from app.modules.recommender.engine import RecommendationResult

router = APIRouter()


class RecommendRequest(BaseModel):
    age: int
    gender: str
    severity: str
    duration_days: int
    symptoms: str


@router.post("/recommend", response_model=RecommendationResult)
async def recommend(request: RecommendRequest):
    patient_info = build_patient_info(
        request.age, request.gender, request.severity,
        request.duration_days, request.symptoms,
    )
    result, _, _ = await get_recommendation(patient_info)
    return result
