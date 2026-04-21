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
    images: list[str] | None = None,
) -> tuple[T, str, dict]:
    """
    Returns (parsed_result, model_used, usage_dict).
    usage_dict keys: prompt_tokens, completion_tokens, total_tokens.
    If images (base64 PNGs) are provided they are sent as vision content.
    """
    if images:
        user_content: list = [{"type": "text", "text": user_message}]
        for img_b64 in images:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_b64}", "detail": "high"},
            })
    else:
        user_content = user_message

    response = await _client.beta.chat.completions.parse(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
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


async def chat_completion(
    system_prompt: str,
    history: list[dict],
    response_model: Type[T],
) -> tuple[T, str, dict]:
    """
    Multi-turn chat. history is a list of {"role": "user"|"assistant", "content": str}.
    Returns (parsed_result, model_used, usage_dict).
    """
    response = await _client.beta.chat.completions.parse(
        model=settings.openai_model,
        messages=[{"role": "system", "content": system_prompt}, *history],
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
