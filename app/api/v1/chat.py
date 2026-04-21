from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.modules.chatbot.engine import ChatTurn
from app.modules.recommender.engine import RecommendationResult
from app.services.chat_service import attach_report, send_message, start_chat
from app.services.storage import list_chats, load_chat

router = APIRouter()


class StartChatRequest(BaseModel):
    report_id: str | None = None


class StartChatResponse(BaseModel):
    chat_id: str


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    chat_id: str
    model_used: str
    usage: dict
    turn: ChatTurn
    recommendation: RecommendationResult | None = None


class AttachReportRequest(BaseModel):
    report_id: str


@router.post("/chat/sessions", response_model=StartChatResponse)
async def create_session(body: StartChatRequest = StartChatRequest()):
    chat_id = start_chat(report_id=body.report_id)
    return StartChatResponse(chat_id=chat_id)


@router.post("/chat/sessions/{chat_id}/message", response_model=MessageResponse)
async def message(chat_id: str, body: MessageRequest):
    try:
        turn, model_used, usage, recommendation = await send_message(chat_id, body.message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return MessageResponse(
        chat_id=chat_id, model_used=model_used, usage=usage,
        turn=turn, recommendation=recommendation,
    )


@router.post("/chat/sessions/{chat_id}/report")
async def attach(chat_id: str, body: AttachReportRequest):
    try:
        findings = attach_report(chat_id, body.report_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"chat_id": chat_id, "report_type": findings.get("report_type"), "urgency": findings.get("urgency")}


@router.get("/chat/sessions/{chat_id}")
async def get_session(chat_id: str):
    session = load_chat(chat_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    return session


@router.get("/chat/sessions")
async def list_sessions(limit: int = 20):
    return list_chats(limit=limit)
