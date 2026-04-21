from app.services.openai_client import structured_completion
from app.services.storage import save_session
from app.modules.recommender.engine import RecommendationResult
from app.prompts.recommender_prompts import RECOMMENDER_SYSTEM_PROMPT
from app.tracker import record_usage

_COST_PER_INPUT_TOKEN  = 2.50  / 1_000_000
_COST_PER_OUTPUT_TOKEN = 10.00 / 1_000_000


def build_patient_info(age: int, gender: str, severity: str, duration: int, symptoms: str) -> str:
    return (
        f"Patient: {age}-year-old {gender}\n"
        f"Symptom severity: {severity}\n"
        f"Duration: {duration} day(s)\n"
        f"Symptoms: {symptoms}"
    )


def _parse_patient_info(patient_info: str) -> dict:
    """Parse the formatted patient_info string back into a dict for storage."""
    result = {}
    for line in patient_info.splitlines():
        if line.startswith("Patient:"):
            result["patient"] = line.replace("Patient:", "").strip()
        elif line.startswith("Symptom severity:"):
            result["severity"] = line.replace("Symptom severity:", "").strip()
        elif line.startswith("Duration:"):
            result["duration"] = line.replace("Duration:", "").strip()
        elif line.startswith("Symptoms:"):
            result["symptoms"] = line.replace("Symptoms:", "").strip()
    return result


async def get_recommendation(patient_info: str) -> tuple[RecommendationResult, str, dict, str]:
    result, model_used, usage = await structured_completion(
        system_prompt=RECOMMENDER_SYSTEM_PROMPT,
        user_message=patient_info,
        response_model=RecommendationResult,
    )

    cost = (
        usage.get("prompt_tokens", 0) * _COST_PER_INPUT_TOKEN
        + usage.get("completion_tokens", 0) * _COST_PER_OUTPUT_TOKEN
    )

    usage_entry = {**usage, "cost_usd": cost}

    session_id = save_session(
        patient_info=_parse_patient_info(patient_info),
        recommendation=result.model_dump(),
        model_used=model_used,
        usage=usage_entry,
    )

    record_usage(usage_entry)
    return result, model_used, usage_entry, session_id
