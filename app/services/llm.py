from app.services.openai_client import structured_completion
from app.modules.recommender.engine import RecommendationResult
from app.prompts.recommender_prompts import RECOMMENDER_SYSTEM_PROMPT
from app.tracker import record_usage

# GPT-4o pricing (per token)
_COST_PER_INPUT_TOKEN = 2.50 / 1_000_000
_COST_PER_OUTPUT_TOKEN = 10.00 / 1_000_000


def build_patient_info(age: int, gender: str, severity: str, duration: int, symptoms: str) -> str:
    return (
        f"Patient: {age}-year-old {gender}\n"
        f"Symptom severity: {severity}\n"
        f"Duration: {duration} day(s)\n"
        f"Symptoms: {symptoms}"
    )


async def get_recommendation(patient_info: str) -> tuple[RecommendationResult, str, dict]:
    result, model_used, usage = await structured_completion(
        system_prompt=RECOMMENDER_SYSTEM_PROMPT,
        user_message=patient_info,
        response_model=RecommendationResult,
    )

    cost = (
        usage.get("prompt_tokens", 0) * _COST_PER_INPUT_TOKEN
        + usage.get("completion_tokens", 0) * _COST_PER_OUTPUT_TOKEN
    )

    usage_entry = {
        **usage,
        "cost_usd": cost,
        "rate_limits": {"requests": {}, "tokens": {}},
    }

    record_usage(usage_entry)
    return result, model_used, usage_entry
