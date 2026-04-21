from typing import Type, TypeVar
from openai import AsyncOpenAI
from pydantic import BaseModel
from app.config import settings

_client = AsyncOpenAI(api_key=settings.openai_api_key)

T = TypeVar("T", bound=BaseModel)


async def structured_completion(
    system_prompt: str,
    user_message: str,
    response_model: Type[T],
) -> tuple[T, str, dict]:
    """
    Returns (parsed_result, model_used, usage_dict).
    usage_dict keys: prompt_tokens, completion_tokens, total_tokens.
    """
    response = await _client.beta.chat.completions.parse(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format=response_model,
    )

    usage = {}
    if response.usage:
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return response.choices[0].message.parsed, response.model, usage
