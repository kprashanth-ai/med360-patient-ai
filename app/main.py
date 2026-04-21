from fastapi import FastAPI
from app.api.v1 import recommendations

app = FastAPI(
    title="Med360 Patient AI",
    version="0.1.0",
    description="AI intelligence layer for the Med360 patient app",
)

app.include_router(recommendations.router, prefix="/api/v1", tags=["Recommender"])


@app.get("/health")
async def health():
    return {"status": "ok"}
