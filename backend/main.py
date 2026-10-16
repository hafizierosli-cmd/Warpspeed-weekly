from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

STATIC = Path(__file__).parent / "static"

app = FastAPI(title="Weekly Warp Speed")


class Status(BaseModel):
    status: str


@app.get("/health", response_model=Status)
def health() -> Status:
    return Status(status="ok")


@app.get("/api/health", response_model=Status)
def api_health() -> Status:
    return Status(status="ok")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    # The dashboard is a self-contained page; no frontend/ is shipped, so the
    # backend serves it at the root.
    return FileResponse(STATIC / "index.html")
