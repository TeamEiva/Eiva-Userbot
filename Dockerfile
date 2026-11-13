FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg imagemagick mediainfo tesseract-ocr libmagic1 libgl1 libglib2.0-0 \
    build-essential libpq-dev libjpeg62-turbo-dev zlib1g-dev libwebp-dev \
    libfreetype6-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x start.sh

CMD ["./start.sh"]
