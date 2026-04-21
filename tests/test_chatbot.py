import pytest
from unittest.mock import AsyncMock, patch
from app.modules.chatbot.handler import build_response
from app.modules.chatbot.followup import generate_followup


@pytest.mark.asyncio
async def test_build_response_returns_string():
    with patch("app.modules.chatbot.handler.chat_completion", new=AsyncMock(return_value="You should rest and monitor.")):
        result = await build_response(
            clinical_state={"chief_complaint": "headache", "symptoms": ["headache"]},
            recommendation={"next_step": "monitor"},
        )
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_generate_followup_returns_question():
    with patch("app.modules.chatbot.followup.chat_completion", new=AsyncMock(return_value="How long have you had this headache?")):
        result = await generate_followup(
            clinical_state={"chief_complaint": "headache", "missing_info": ["duration"]}
        )
    assert "?" in result
