import pytest
from app.services.llm import build_patient_info, get_recommendation
from app.services.storage import load_session
from app.modules.recommender.engine import RecommendationResult

VALID_URGENCY   = {"low", "moderate", "high", "emergency"}
VALID_NEXT_STEPS = {"monitor", "teleconsult", "home_visit", "specialist", "emergency"}


@pytest.mark.asyncio
async def test_recommendation_schema():
    info = build_patient_info(35, "female", "medium", 2, "persistent headache and mild fever")
    result, model, usage, session_id = await get_recommendation(info)

    assert isinstance(result, RecommendationResult)
    assert result.urgency_level in VALID_URGENCY
    assert result.next_step in VALID_NEXT_STEPS
    assert result.recommended_specialist
    assert result.primary_recommendation_summary
    assert isinstance(result.specialist_pathway, list)
    assert isinstance(result.red_flags, list)
    assert result.disclaimer


@pytest.mark.asyncio
async def test_session_is_saved():
    info = build_patient_info(35, "female", "medium", 2, "persistent headache and mild fever")
    _, _, _, session_id = await get_recommendation(info)

    session = load_session(session_id)
    assert session is not None
    assert session["session_id"] == session_id
    assert "recommendation" in session
    assert "patient_info" in session
    assert "usage" in session
    assert session["usage"]["total_tokens"] > 0
    assert session["usage"]["cost_usd"] > 0


@pytest.mark.asyncio
async def test_usage_tracking():
    info = build_patient_info(35, "female", "medium", 2, "persistent headache and mild fever")
    _, model, usage, _ = await get_recommendation(info)

    assert model
    assert usage["total_tokens"] > 0
    assert usage["cost_usd"] > 0


@pytest.mark.asyncio
async def test_emergency_escalation():
    info = build_patient_info(50, "male", "high", 1, "severe chest pain radiating to left arm, can't breathe")
    result, _, _, _ = await get_recommendation(info)

    assert result.urgency_level in {"high", "emergency"}
    assert result.next_step == "emergency"


@pytest.mark.asyncio
async def test_low_urgency():
    info = build_patient_info(25, "female", "low", 1, "slight runny nose and mild sneezing since this morning")
    result, _, _, _ = await get_recommendation(info)

    assert result.urgency_level in {"low", "moderate"}
