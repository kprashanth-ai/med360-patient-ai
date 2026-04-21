import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings


def _sessions_dir() -> Path:
    path = Path(settings.storage_dir) / "sessions"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_session(patient_info: dict, recommendation: dict, model_used: str, usage: dict) -> str:
    session_id = str(uuid.uuid4())
    record = {
        "session_id": session_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "patient_info": patient_info,
        "recommendation": recommendation,
        "model_used": model_used,
        "usage": {
            "prompt_tokens":     usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens":      usage.get("total_tokens", 0),
            "cost_usd":          usage.get("cost_usd", 0.0),
        },
    }
    path = _sessions_dir() / f"{session_id}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return session_id


def load_session(session_id: str) -> dict | None:
    path = _sessions_dir() / f"{session_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_sessions(limit: int = 20) -> list[dict]:
    files = sorted(_sessions_dir().glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    sessions = []
    for f in files[:limit]:
        data = json.loads(f.read_text(encoding="utf-8"))
        sessions.append({
            "session_id": data["session_id"],
            "created_at": data["created_at"],
            "recommended_specialist": data["recommendation"].get("recommended_specialist"),
            "urgency_level": data["recommendation"].get("urgency_level"),
        })
    return sessions
