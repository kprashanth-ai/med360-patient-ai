from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.core.state_extractor import extract_clinical_state
from app.core.session_manager import load_or_create_session, save_message
from app.modules.chatbot.handler import build_response
from app.modules.chatbot.followup import generate_followup
from app.modules.recommender.engine import get_recommendation
from app.modules.recommender.red_flags import detect_red_flags


async def handle_chat(request: ChatRequest) -> ChatResponse:
    session = await load_or_create_session(request.session_id, request.user_id)

    await save_message(session["_id"], role="user", content=request.message)

    clinical_state = await extract_clinical_state(request.message, session)

    red_flag = await detect_red_flags(clinical_state)
    if red_flag:
        reply = (
            "Based on what you've described, this may need urgent attention. "
            "Please seek immediate care or call emergency services."
        )
        await save_message(session["_id"], role="assistant", content=reply)
        return ChatResponse(session_id=str(session["_id"]), message=reply, urgent=True)

    if clinical_state.get("missing_info"):
        reply = await generate_followup(clinical_state)
    else:
        recommendation = await get_recommendation(str(session["_id"]))
        reply = await build_response(clinical_state, recommendation)

    await save_message(session["_id"], role="assistant", content=reply)
    return ChatResponse(session_id=str(session["_id"]), message=reply, urgent=False)
