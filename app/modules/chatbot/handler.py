from app.services.openai_client import chat_completion
from app.prompts.chatbot_prompts import RESPONSE_SYSTEM_PROMPT


async def build_response(clinical_state: dict, recommendation: dict) -> str:
    context = f"""
Clinical State: {clinical_state}
Recommendation: {recommendation}
"""
    return await chat_completion(
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        user_message=context,
    )
