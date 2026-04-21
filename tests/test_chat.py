"""
Tests for the chat module.
No OpenAI calls — covers schema, storage, service logic, and API validation.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.chatbot.engine import ChatTurn
from app.services.storage import list_chats, load_chat, save_chat

client = TestClient(app)


# ── Schema ─────────────────────────────────────────────────────────────────────

def test_chat_turn_defaults():
    turn = ChatTurn(message="Hello")
    assert turn.urgency_level == "none"
    assert turn.suggested_next_step == "none"
    assert turn.escalation_note is None


def test_chat_turn_emergency():
    turn = ChatTurn(
        message="Please call emergency services.",
        urgency_level="emergency",
        suggested_next_step="emergency",
        escalation_note="Call 112 immediately.",
    )
    assert turn.urgency_level == "emergency"
    assert turn.escalation_note is not None


def test_chat_turn_invalid_urgency():
    with pytest.raises(Exception):
        ChatTurn(message="hi", urgency_level="critical")


def test_chat_turn_invalid_next_step():
    with pytest.raises(Exception):
        ChatTurn(message="hi", suggested_next_step="call_doctor")


# ── Storage ────────────────────────────────────────────────────────────────────

def _sample_session(chat_id: str) -> dict:
    return {
        "chat_id": chat_id,
        "created_at": "2026-04-21T00:00:00+00:00",
        "report_context": None,
        "messages": [],
        "total_tokens": 0,
        "total_cost_usd": 0.0,
        "last_urgency": "none",
    }


def test_save_and_load_chat(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings", type("s", (), {"storage_dir": str(tmp_path)})())
    session = _sample_session("test-chat-id")
    save_chat("test-chat-id", session)
    loaded = load_chat("test-chat-id")
    assert loaded is not None
    assert loaded["chat_id"] == "test-chat-id"


def test_load_chat_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings", type("s", (), {"storage_dir": str(tmp_path)})())
    assert load_chat("does-not-exist") is None


def test_list_chats(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings", type("s", (), {"storage_dir": str(tmp_path)})())
    save_chat("id-1", _sample_session("id-1"))
    save_chat("id-2", _sample_session("id-2"))
    chats = list_chats()
    assert len(chats) == 2
    assert all("chat_id" in c for c in chats)


# ── API ────────────────────────────────────────────────────────────────────────

def test_create_session():
    response = client.post("/api/v1/chat/sessions", json={})
    assert response.status_code == 200
    data = response.json()
    assert "chat_id" in data
    assert len(data["chat_id"]) > 0


def test_get_session_not_found():
    response = client.get("/api/v1/chat/sessions/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_message_to_nonexistent_session():
    response = client.post(
        "/api/v1/chat/sessions/00000000-0000-0000-0000-000000000000/message",
        json={"message": "hello"},
    )
    assert response.status_code == 404


def test_attach_nonexistent_report():
    create = client.post("/api/v1/chat/sessions", json={})
    chat_id = create.json()["chat_id"]
    response = client.post(
        f"/api/v1/chat/sessions/{chat_id}/report",
        json={"report_id": "00000000-0000-0000-0000-000000000000"},
    )
    assert response.status_code == 404


def test_list_chat_sessions():
    response = client.get("/api/v1/chat/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_session_persists_after_create():
    create = client.post("/api/v1/chat/sessions", json={})
    chat_id = create.json()["chat_id"]
    get = client.get(f"/api/v1/chat/sessions/{chat_id}")
    assert get.status_code == 200
    assert get.json()["chat_id"] == chat_id
    assert get.json()["messages"] == []
