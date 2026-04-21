from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Session(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: str
    messages: list[dict] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
