
# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI(
    title="CHI-311 Copilot API",
    description="API for predicting 311 request resolution, equity analysis, and hotspot detection.",
    version="0.1.0"
)

class RefreshMeta(BaseModel):
    data_last_updated: datetime.datetime
    model_version: str
    feature_version: str


_refresh_meta_cache = {
    "data_last_updated": datetime.datetime.now() - datetime.timedelta(days=1),
    "model_version": "v0.0.1-alpha",
    "feature_version": "v0.0.1-alpha"
}

@app.get("/health", tags=["Infrastructure"])
async def health_check():
    """A simple health check endpoint to confirm the API is running."""
    return {"status": "ok"}


@app.get("/api/refresh_meta", response_model=RefreshMeta, tags=["Metadata"])
async def get_refresh_meta():
    """
    Returns metadata about the last data and model refresh cycle.
    """
    return _refresh_meta_cache

