from pathlib import Path
import shutil
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from modules.qr_service import build_payload, save_qr

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
SESSION_DIR = OUTPUT_DIR / "session"


class GenerateRequest(BaseModel):
    qr_type: str = Field(alias="type")
    values: dict[str, Any] = Field(default_factory=dict)
    fill_color: str = "#101828"
    back_color: str = "#ffffff"
    size: int = 10
    filename: str = "qrnexa"


class GenerateResponse(BaseModel):
    payload: str
    image_url: str
    filename: str


def clear_session_files():
    if SESSION_DIR.exists():
        shutil.rmtree(SESSION_DIR)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(title="QRNexa API", version="1.0.0")


@app.on_event("startup")
def startup_cleanup():
    clear_session_files()


@app.on_event("shutdown")
def shutdown_cleanup():
    clear_session_files()


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "QRNexa"}


@app.post("/api/generate", response_model=GenerateResponse)
def generate_qr(request: GenerateRequest):
    try:
        payload = build_payload(request.qr_type, request.values)
        path = save_qr(
            payload=payload,
            filename=request.filename,
            fill_color=request.fill_color,
            back_color=request.back_color,
            box_size=request.size,
            output_dir=SESSION_DIR,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        "payload": payload,
        "image_url": f"/output/session/{path.name}",
        "filename": path.name,
    }


@app.get("/output/session/{filename}")
def download_output(filename: str):
    path = SESSION_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="QR image not found.")
    return FileResponse(path, media_type="image/png", filename=filename)


app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")
