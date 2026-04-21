from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.report_schemas import ReportResponse
from app.modules.report_interpreter.parser import parse_report
from app.modules.report_interpreter.explainer import explain_findings

router = APIRouter()


@router.post("/reports/upload", response_model=ReportResponse)
async def upload_report(
    session_id: str = Form(...),
    file: UploadFile = File(...),
):
    findings = await parse_report(file, session_id)
    explanation = await explain_findings(findings)
    return ReportResponse(session_id=session_id, findings=findings, explanation=explanation)


@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    from app.database import get_collection
    doc = await get_collection("reports").find_one({"_id": report_id})
    return doc
