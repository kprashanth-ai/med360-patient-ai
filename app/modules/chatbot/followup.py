from app.services.openai_client import chat_completion
from app.prompts.chatbot_prompts import FOLLOWUP_SYSTEM_PROMPT


async def generate_followup(clinical_state: dict) -> str:
    missing = clinical_state.get("missing_info", [])
    context = f"Missing information: {missing}\nCurrent state: {clinical_state}"

    return await chat_completion(
        system_prompt=FOLLOWUP_SYSTEM_PROMPT,
        user_message=context,
    )
