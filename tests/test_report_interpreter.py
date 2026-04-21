import pytest
from unittest.mock import AsyncMock, patch
from app.modules.report_interpreter.explainer import explain_findings


@pytest.mark.asyncio
async def test_explain_findings_returns_string():
    findings = {
        "abnormal_values": [{"name": "HbA1c", "value": "8.2", "unit": "%", "reference_range": "< 5.7"}],
        "summary": "Elevated HbA1c indicating poor glucose control.",
    }
    with patch("app.modules.report_interpreter.explainer.chat_completion", new=AsyncMock(return_value="Your HbA1c is high, which may indicate diabetes.")):
        result = await explain_findings(findings)
    assert isinstance(result, str)
    assert len(result) > 0
