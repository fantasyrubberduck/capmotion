FROM python:3.11-slim

# Instal·lem FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY motion_capture.py .
CMD ["python", "motion_capture.py"]
