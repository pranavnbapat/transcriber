# app/main.py

import logging
import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic

from app.gpt_punctuate import punctuate_text
from app.whisper_transcriber import transcribe_file
from app.utils import BasicAuthMiddleware, BASIC_AUTH_USER, BASIC_AUTH_PASS, UPLOAD_DIR

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Whisper Transcription API",
    description="",
    version="1.0.0"
)
app.add_middleware(BasicAuthMiddleware, username=BASIC_AUTH_USER, password=BASIC_AUTH_PASS)

security = HTTPBasic()

ALLOWED_EXTENSIONS = {'.mp3', '.mp4', '.wav', '.m4a', '.avi', '.flac', '.aac', '.mov', '.webm'}
ALLOWED_MIME_PREFIXES = ('audio/', 'video/')

@app.post("/transcribe",
          summary="Transcribe audio/video file",
          description="""
          Upload an audio or video file and get its transcription using OpenAI Whisper (large-v3).

          - Uses **OpenAI Whisper (large-v3)** to transcribe or translate speech.
          - Supports **multiple languages**, automatic language detection, and long files.
          - Accepts files in formats like `.mp3`, `.mp4`, `.wav`, `.m4a`, `.avi`, etc.
          - Returns both raw transcription and punctuation-enhanced text using **GPT-3.5 Turbo**.

          Form Parameters:
          - `file`: Audio or video file to transcribe (multipart/form-data)

          Returns:
          {
            "language": "hi",
            "duration": 21.34,
            "raw_text": "Raw text from Whisper",
            "punctuated_text": "Same text with punctuation added by GPT-3.5 Turbo"
          }
          """
          )
async def transcribe_endpoint(
    file: UploadFile = File(...)
):
    filename = file.filename.lower()
    ext = os.path.splitext(filename)[1]

    # Check file extension and MIME type
    if ext not in ALLOWED_EXTENSIONS or not file.content_type.startswith(ALLOWED_MIME_PREFIXES):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: '{ext}'. Allowed types are: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        task = "transcribe"

        result = transcribe_file(file_path, task=task)

        try:
            punctuated_text = punctuate_text(result["text"], language=result["language"])
        except Exception as gpt_error:
            logger.error(f"GPT error: {gpt_error}")
            punctuated_text = (
                "⚠️ Punctuation skipped due to an internal error with GPT.\n\n"
                f"Raw transcription:\n{result['text']}"
            )

        return JSONResponse(content={
            "language": result["language"],
            "duration": result["duration"],
            "raw_text": result["text"],
            "punctuated_text": punctuated_text
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
