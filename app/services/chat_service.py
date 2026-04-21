import json
import uuid
from datetime import datetime, timezone

from app.modules.chatbot.engine import ChatTurn
from app.modules.recommender.engine import RecommendationResult
from app.prompts.chatbot_prompts import CHAT_SYSTEM_PROMPT
from app.services.llm import build_patient_info, get_recommendation
from app.services.openai_client import chat_completion
from app.services.storage import load_chat, load_report, save_chat
from app.tracker import record_usage

_COST_PER_INPUT_TOKEN  = 2.50  / 1_000_000
_COST_PER_OUTPUT_TOKEN = 10.00 / 1_000_000


def start_chat(report_id: str | None = None) -> str:
    chat_id = str(uuid.uuid4())
    report_context = None
    if report_id:
        record = load_report(report_id)
        if record:
            report_context = record["findings"]

    session = {
        "chat_id": chat_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "report_context": report_context,
        "messages": [],
        "total_tokens": 0,
        "total_cost_usd": 0.0,
        "last_urgency": "none",
    }
    save_chat(chat_id, session)
    return chat_id


def attach_report(chat_id: str, report_id: str) -> dict:
    session = _require_chat(chat_id)
    record = load_report(report_id)
    if not record:
        raise ValueError(f"Report not found: {report_id}")
    session["report_context"] = record["findings"]
    save_chat(chat_id, session)
    return record["findings"]


async def send_message(chat_id: str, user_text: str) -> tuple[ChatTurn, str, dict, RecommendationResult | None]:
    session = _require_chat(chat_id)

    system = CHAT_SYSTEM_PROMPT
    if session.get("report_context"):
        system += (
            "\n\nThe patient has uploaded a medical report. Key findings:\n"
            + json.dumps(session["report_context"], indent=2)
        )

    now = datetime.now(timezone.utc).isoformat()
    session["messages"].append({"role": "user", "content": user_text, "timestamp": now})

    history = [{"role": m["role"], "content": m["content"]} for m in session["messages"]]

    turn, model_used, usage = await chat_completion(
        system_prompt=system,
        history=history,
        response_model=ChatTurn,
    )

    cost = (
        usage.get("prompt_tokens", 0) * _COST_PER_INPUT_TOKEN
        + usage.get("completion_tokens", 0) * _COST_PER_OUTPUT_TOKEN
    )
    usage_entry = {**usage, "cost_usd": cost}
    record_usage(usage_entry)

    session["messages"].append({
        "role": "assistant",
        "content": turn.message,
        "urgency_level": turn.urgency_level,
        "suggested_next_step": turn.suggested_next_step,
        "escalation_note": turn.escalation_note,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    session["total_tokens"] += usage_entry.get("total_tokens", 0)
    session["total_cost_usd"] += cost
    session["last_urgency"] = turn.urgency_level
    save_chat(chat_id, session)

    recommendation: RecommendationResult | None = None
    if turn.ready_to_recommend and turn.patient_data:
        pd = turn.patient_data
        patient_info = build_patient_info(
            pd.age, pd.gender, pd.severity, pd.duration_days, pd.symptoms
        )
        recommendation, _, rec_usage, _ = await get_recommendation(patient_info)
        session["total_tokens"] += rec_usage.get("total_tokens", 0)
        session["total_cost_usd"] += rec_usage.get("cost_usd", 0.0)
        save_chat(chat_id, session)

    return turn, model_used, usage_entry, recommendation


def _require_chat(chat_id: str) -> dict:
    session = load_chat(chat_id)
    if not session:
        raise ValueError(f"Chat session not found: {chat_id}")
    return session
