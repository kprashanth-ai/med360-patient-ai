from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Report(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    session_id: ObjectId
    filename: str
    findings: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
