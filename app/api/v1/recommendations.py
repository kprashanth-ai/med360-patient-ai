from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from app.services.llm import build_patient_info, get_recommendation
from app.services.storage import load_session, list_sessions
from app.modules.recommender.engine import RecommendationResult

router = APIRouter()


class RecommendRequest(BaseModel):
    age: int = Field(..., ge=1, le=120)
    gender: Literal["male", "female", "other"]
    severity: Literal["low", "medium", "high"]
    duration_days: int = Field(..., ge=1, le=3650)
    symptoms: str = Field(..., min_length=10, max_length=1000)

    @field_validator("symptoms")
    @classmethod
    def symptoms_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("symptoms cannot be blank or whitespace only")
        return v.strip()


class RecommendResponse(BaseModel):
    session_id: str
    recommendation: RecommendationResult


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    patient_info = build_patient_info(
        request.age, request.gender, request.severity,
        request.duration_days, request.symptoms,
    )
    result, _, _, session_id = await get_recommendation(patient_info)
    return RecommendResponse(session_id=session_id, recommendation=result)


@router.get("/sessions", summary="List recent sessions")
async def get_sessions(limit: int = 20):
    return list_sessions(limit=limit)


@router.get("/sessions/{session_id}", summary="Get a session by ID")
async def get_session(session_id: str):
    session = load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
