import os, uuid, shutil, subprocess, urllib.request
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE = Path(os.getenv("DATA_DIR", "/tmp/dubflow"))
UPLOADS = BASE / "uploads"
OUTPUTS = BASE / "outputs"
UPLOADS.mkdir(parents=True, exist_ok=True)
OUTPUTS.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="DubFlow AI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs = {}

class LinkJob(BaseModel):
    url: str
    source_language: str = "auto"
    target_language: str = "ur"

@app.get("/")
def root():
    return {"app": "DubFlow AI", "status": "online", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    allowed = {".mp4",".mov",".mkv",".webm",".avi",".m4v"}
    ext = Path(file.filename or "").suffix.lower()
    if ext not in allowed:
        raise HTTPException(400, "Unsupported video format")

    job_id = str(uuid.uuid4())
    path = UPLOADS / f"{job_id}{ext}"
    with open(path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    jobs[job_id] = {"status":"uploaded", "file":str(path)}
    return {"job_id": job_id, "status":"uploaded"}

@app.post("/api/from-link")
def from_link(data: LinkJob):
    # Only direct/public URLs that the user is authorized to process.
    if not (data.url.startswith("https://") or data.url.startswith("http://")):
        raise HTTPException(400, "Invalid URL")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status":"queued",
        "url":data.url,
        "source_language":data.source_language,
        "target_language":data.target_language
    }
    return {"job_id": job_id, "status":"queued",
            "message":"Link accepted. Connect a permitted downloader/media source and AI provider to process it."}

@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return {"job_id":job_id, **jobs[job_id]}

@app.post("/api/test-ffmpeg")
def test_ffmpeg():
    try:
        p = subprocess.run(["ffmpeg","-version"], capture_output=True, text=True, timeout=10)
        return {"ok": p.returncode == 0, "ffmpeg": p.stdout.splitlines()[0] if p.stdout else "unknown"}
    except Exception as e:
        return {"ok":False, "error":str(e)}
