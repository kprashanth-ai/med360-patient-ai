from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.modules.report_interpreter.engine import ReportFindings
from app.services.report_service import interpret_report, save_upload
from app.services.storage import list_reports, load_report

router = APIRouter()


class ReportResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    report_id: str
    model_used: str
    usage: dict
    findings: ReportFindings


@router.post("/reports/upload", response_model=ReportResponse)
async def upload_report(file: UploadFile = File(...)):
    allowed = {"application/pdf", "text/plain"}
    content_type = file.content_type or ""
    if content_type not in allowed and not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=415, detail="Only PDF and plain-text reports are supported.")

    file_path, content_type = await save_upload(file)
    findings, model_used, usage, report_id = await interpret_report(
        file_path=file_path,
        content_type=content_type,
        filename=file.filename,
    )
    return ReportResponse(
        report_id=report_id,
        model_used=model_used,
        usage=usage,
        findings=findings,
    )


@router.get("/reports")
async def get_reports(limit: int = 20):
    return list_reports(limit=limit)


@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    record = load_report(report_id)
    if not record:
        raise HTTPException(status_code=404, detail="Report not found.")
    return record
