# DubFlow AI Backend

This is the backend foundation for DubFlow AI.

## What works now

- FastAPI REST API
- Health check
- Video upload endpoint
- Job IDs/status endpoint
- Direct-link job intake
- FFmpeg included in Docker
- CORS enabled for the Netlify frontend
- Render Docker deployment configuration

## Important

This package is the backend foundation, not the complete AI dubbing engine yet.
Actual speech-to-text, translation, AI voice generation and final audio/video synchronization need an AI provider or self-hosted models.

Use only videos you own or have permission to process. Do not use the service to bypass DRM, paywalls, login restrictions, or protected-platform download controls.

## Endpoints

GET /health

POST /api/upload
multipart field: file

POST /api/from-link
JSON:
{
  "url": "https://example.com/video.mp4",
  "source_language": "auto",
  "target_language": "ur"
}

GET /api/jobs/{job_id}

POST /api/test-ffmpeg
