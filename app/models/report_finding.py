from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class ReportFinding(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    session_id: ObjectId
    abnormal_values: list[dict] = []
    normal_values: list[dict] = []
    notable_markers: list[str] = []
    summary: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
