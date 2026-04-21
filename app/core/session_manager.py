from datetime import datetime, timezone
from bson import ObjectId
from app.database import get_collection


async def load_or_create_session(session_id: str | None, user_id: str) -> dict:
    sessions = get_collection("sessions")

    if session_id:
        session = await sessions.find_one({"_id": ObjectId(session_id)})
        if session:
            return session

    new_session = {
        "_id": ObjectId(),
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "messages": [],
    }
    await sessions.insert_one(new_session)
    return new_session


async def get_session_by_id(session_id: str) -> dict | None:
    return await get_collection("sessions").find_one({"_id": ObjectId(session_id)})


async def save_message(session_id, role: str, content: str):
    message = {
        "_id": ObjectId(),
        "session_id": session_id,
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc),
    }
    await get_collection("messages").insert_one(message)
    await get_collection("sessions").update_one(
        {"_id": session_id},
        {
            "$push": {"messages": {"role": role, "content": content}},
            "$set": {"updated_at": datetime.now(timezone.utc)},
        },
    )
