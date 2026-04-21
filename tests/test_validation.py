import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID = {
    "age": 35,
    "gender": "female",
    "severity": "moderate",
    "duration_days": 3,
    "symptoms": "persistent headache and mild fever for 3 days",
}


def post(payload: dict):
    return client.post("/api/v1/recommend", json=payload)


def test_valid_request_passes():
    # Only checking validation — mock would be needed for full call
    # This confirms the schema accepts a well-formed request
    response = post({**VALID, "severity": "low"})
    assert response.status_code != 422


def test_age_too_low():
    assert post({**VALID, "age": 0}).status_code == 422


def test_age_too_high():
    assert post({**VALID, "age": 121}).status_code == 422


def test_invalid_gender():
    assert post({**VALID, "gender": "unknown"}).status_code == 422


def test_invalid_severity():
    assert post({**VALID, "severity": "extreme"}).status_code == 422


def test_duration_zero():
    assert post({**VALID, "duration_days": 0}).status_code == 422


def test_duration_too_long():
    assert post({**VALID, "duration_days": 3651}).status_code == 422


def test_symptoms_too_short():
    assert post({**VALID, "symptoms": "headache"}).status_code == 422


def test_symptoms_blank():
    assert post({**VALID, "symptoms": "   "}).status_code == 422


def test_symptoms_too_long():
    assert post({**VALID, "symptoms": "a" * 1001}).status_code == 422
