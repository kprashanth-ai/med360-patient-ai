from pydantic import BaseModel


class ReportResponse(BaseModel):
    session_id: str
    findings: dict
    explanation: str
