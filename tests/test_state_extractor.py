import pytest
from unittest.mock import AsyncMock, patch
from app.core.state_extractor import extract_clinical_state


@pytest.mark.asyncio
async def test_extracts_clinical_state():
    mock_state = {
        "chief_complaint": "headache",
        "symptoms": ["headache"],
        "duration": "2 days",
        "severity": "moderate",
        "chronic_conditions": [],
        "medications": [],
        "red_flags": [],
        "missing_info": ["severity"],
        "urgency_level": "low",
    }

    with (
        patch("app.core.state_extractor.structured_completion", new=AsyncMock(return_value=mock_state)),
        patch("app.core.state_extractor.get_collection") as mock_col,
    ):
        mock_col.return_value.update_one = AsyncMock()
        result = await extract_clinical_state(
            message="I have had a headache for 2 days",
            session={"_id": "test_session", "messages": []},
        )

    assert result["chief_complaint"] == "headache"
    assert "headache" in result["symptoms"]
