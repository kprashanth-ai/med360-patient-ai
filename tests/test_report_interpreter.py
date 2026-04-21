"""
Tests for the report interpreter module.
Covers: Pydantic schema, text extraction, storage, and API validation.
No OpenAI calls are made.
"""

import json
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.report_interpreter.engine import LabValue, ReportFindings
from app.modules.report_interpreter.parser import extract_text
from app.services.storage import list_reports, load_report, save_report

client = TestClient(app)


# ── Schema / Pydantic ──────────────────────────────────────────────────────────

def _sample_findings() -> dict:
    return {
        "report_type": "Complete Blood Count",
        "test_date": "2026-04-01",
        "abnormal_values": [
            {
                "name": "Haemoglobin",
                "value": "9.2",
                "unit": "g/dL",
                "reference_range": "12.0-16.0",
                "status": "abnormal",
                "plain_meaning": "Your haemoglobin is low, which may mean anaemia.",
            }
        ],
        "normal_values": [],
        "notable_markers": ["Low haemoglobin"],
        "overall_summary": "The CBC shows mild anaemia.",
        "plain_explanation": "Your blood count shows lower-than-normal haemoglobin.",
        "recommended_action": "Discuss with your doctor at your next appointment.",
        "urgency": "routine",
    }


def test_report_findings_valid():
    findings = ReportFindings(**_sample_findings())
    assert findings.report_type == "Complete Blood Count"
    assert len(findings.abnormal_values) == 1
    assert findings.urgency == "routine"


def test_lab_value_valid():
    lv = LabValue(
        name="Glucose",
        value="110",
        unit="mg/dL",
        reference_range="70-99",
        status="borderline",
        plain_meaning="Your blood sugar is slightly above normal.",
    )
    assert lv.status == "borderline"


def test_lab_value_invalid_status():
    with pytest.raises(Exception):
        LabValue(
            name="X", value="1", status="unknown", plain_meaning="test"
        )


def test_report_findings_invalid_urgency():
    data = _sample_findings()
    data["urgency"] = "maybe"
    with pytest.raises(Exception):
        ReportFindings(**data)


def test_report_findings_optional_fields():
    data = _sample_findings()
    data["test_date"] = None
    findings = ReportFindings(**data)
    assert findings.test_date is None


# ── Parser ────────────────────────────────────────────────────────────────────

def test_extract_text_plain_file():
    content = "HbA1c: 8.2%  Reference: < 5.7%\nGlucose: 180 mg/dL"
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_path = f.name

    result = extract_text(tmp_path, "text/plain")
    assert "HbA1c" in result
    Path(tmp_path).unlink()


def test_extract_text_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_text("/nonexistent/path/report.txt", "text/plain")


def test_extract_text_image_raises():
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        f.write(b"\xff\xd8\xff")  # JPEG magic bytes
        tmp_path = f.name

    with pytest.raises(NotImplementedError):
        extract_text(tmp_path, "image/jpeg")
    Path(tmp_path).unlink()


# ── Storage ───────────────────────────────────────────────────────────────────

def test_save_and_load_report(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings", type("s", (), {"storage_dir": str(tmp_path)})())

    report_id = save_report(
        filename="test_cbc.pdf",
        findings=_sample_findings(),
        model_used="gpt-4o",
        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150, "cost_usd": 0.001},
    )

    assert report_id
    record = load_report(report_id)
    assert record is not None
    assert record["filename"] == "test_cbc.pdf"
    assert record["findings"]["report_type"] == "Complete Blood Count"
    assert record["usage"]["total_tokens"] == 150


def test_load_report_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings", type("s", (), {"storage_dir": str(tmp_path)})())
    assert load_report("nonexistent-id") is None


def test_list_reports(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings", type("s", (), {"storage_dir": str(tmp_path)})())

    save_report("a.pdf", _sample_findings(), "gpt-4o", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "cost_usd": 0.0})
    save_report("b.pdf", _sample_findings(), "gpt-4o", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "cost_usd": 0.0})

    reports = list_reports()
    assert len(reports) == 2
    assert all("report_id" in r for r in reports)


# ── API Validation ────────────────────────────────────────────────────────────

def test_upload_unsupported_type():
    response = client.post(
        "/api/v1/reports/upload",
        files={"file": ("photo.png", b"\x89PNG\r\n", "image/png")},
    )
    assert response.status_code == 415


def test_get_report_not_found():
    response = client.get("/api/v1/reports/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_reports_list_empty():
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
