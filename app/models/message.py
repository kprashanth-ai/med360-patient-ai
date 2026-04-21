from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Literal


class Message(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    session_id: ObjectId
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
