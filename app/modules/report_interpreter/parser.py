import os
from fastapi import UploadFile
from app.config import settings
from app.services.openai_client import structured_completion
from app.prompts.report_prompts import REPORT_EXTRACTION_PROMPT
from app.database import get_collection
from bson import ObjectId
from datetime import datetime, timezone


async def parse_report(file: UploadFile, session_id: str) -> dict:
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, file.filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    text = _extract_text(file_path, file.content_type)

    findings = await structured_completion(
        system_prompt=REPORT_EXTRACTION_PROMPT,
        user_message=text,
    )

    record = {
        "_id": ObjectId(),
        "session_id": ObjectId(session_id),
        "filename": file.filename,
        "findings": findings,
        "created_at": datetime.now(timezone.utc),
    }
    await get_collection("reports").insert_one(record)
    await get_collection("report_findings").insert_one(
        {"session_id": ObjectId(session_id), **findings}
    )

    return findings


def _extract_text(file_path: str, content_type: str) -> str:
    if "pdf" in content_type:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    if "image" in content_type:
        # Pass image path to OpenAI vision — handled in openai_client
        return f"IMAGE_FILE:{file_path}"

    with open(file_path, "r", errors="ignore") as f:
        return f.read()
