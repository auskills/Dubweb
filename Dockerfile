FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PORT=10000
ENV DATA_DIR=/tmp/dubflow

CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
