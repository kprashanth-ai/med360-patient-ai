from app.services.openai_client import chat_completion
from app.prompts.report_prompts import REPORT_EXPLANATION_PROMPT


async def explain_findings(findings: dict) -> str:
    return await chat_completion(
        system_prompt=REPORT_EXPLANATION_PROMPT,
        user_message=str(findings),
    )
