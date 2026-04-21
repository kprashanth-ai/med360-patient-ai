from fastapi import APIRouter
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.core.orchestrator import handle_chat

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await handle_chat(request)


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    from app.core.session_manager import get_session_by_id
    return await get_session_by_id(session_id)
