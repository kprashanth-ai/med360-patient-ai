import os
from pathlib import Path
from fastapi import UploadFile

from app.config import settings
from app.modules.report_interpreter.parser import ImageBasedPDFError, extract_images_from_pdf, extract_text
from app.modules.report_interpreter.engine import ReportFindings
from app.services.openai_client import structured_completion
from app.services.storage import save_report
from app.prompts.report_prompts import REPORT_EXTRACTION_PROMPT

_COST_PER_INPUT_TOKEN  = 2.50  / 1_000_000
_COST_PER_OUTPUT_TOKEN = 10.00 / 1_000_000


async def save_upload(file: UploadFile) -> tuple[str, str]:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = str(upload_dir / file.filename)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    return file_path, file.content_type or ""


async def interpret_report(
    file_path: str,
    content_type: str,
    filename: str,
) -> tuple[ReportFindings, str, dict, str]:

    try:
        raw_text = extract_text(file_path, content_type)
        findings, model_used, usage = await structured_completion(
            system_prompt=REPORT_EXTRACTION_PROMPT,
            user_message=raw_text,
            response_model=ReportFindings,
        )
    except ImageBasedPDFError:
        images = extract_images_from_pdf(file_path)
        findings, model_used, usage = await structured_completion(
            system_prompt=REPORT_EXTRACTION_PROMPT,
            user_message="Please extract and interpret the medical report shown in the image(s).",
            response_model=ReportFindings,
            images=images,
        )

    cost = (
        usage.get("prompt_tokens", 0) * _COST_PER_INPUT_TOKEN
        + usage.get("completion_tokens", 0) * _COST_PER_OUTPUT_TOKEN
    )
    usage_entry = {**usage, "cost_usd": cost}

    report_id = save_report(
        filename=filename,
        findings=findings.model_dump(),
        model_used=model_used,
        usage=usage_entry,
    )

    return findings, model_used, usage_entry, report_id
