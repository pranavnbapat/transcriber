# Dockerfile

FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y ffmpeg git nano && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Preload model
RUN python -c "import whisper; whisper.load_model('large-v3')"

EXPOSE 12000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "12000"]
