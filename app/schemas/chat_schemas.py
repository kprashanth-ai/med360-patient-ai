from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    message: str
    urgent: bool = False
