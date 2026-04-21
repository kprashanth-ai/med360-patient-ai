from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    phone: str | None = None
    email: str | None = None
    date_of_birth: str | None = None
    gender: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
