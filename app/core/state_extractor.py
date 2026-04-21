from app.services.openai_client import structured_completion
from app.prompts.state_extraction_prompts import STATE_EXTRACTION_PROMPT
from app.database import get_collection


async def extract_clinical_state(message: str, session: dict) -> dict:
    history = session.get("messages", [])

    state = await structured_completion(
        system_prompt=STATE_EXTRACTION_PROMPT,
        user_message=message,
        history=history,
    )

    await get_collection("clinical_states").update_one(
        {"session_id": session["_id"]},
        {"$set": state},
        upsert=True,
    )

    return state
