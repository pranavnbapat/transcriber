# 🎙️ Whisper Transcription API

A FastAPI-based service that transcribes audio or video files using OpenAI’s [Whisper (large-v3)](https://github.com/openai/whisper) and optionally adds punctuation using GPT-3.5 Turbo. Designed to be secure, production-ready, and easy to deploy with Docker.

---

## ✨ Features

- 🎧 **Multilingual audio/video transcription** using Whisper `large-v3`
- ✍️ **Optional punctuation enhancement** using GPT-3.5 Turbo
- 🔐 **Basic Authentication** (via `.env` credentials)
- 📦 **Dockerised**, with support for pushing to GHCR
- ✅ **File type validation** (supports only audio/video)
- ⚠️ **Graceful fallback** if GPT fails – transcription is still returned

---

## 🛠️ API Endpoint

### `POST /transcribe`

#### 🔐 Authentication
Requires **HTTP Basic Auth**. Credentials are loaded from your `.env` file:

```dotenv
BASIC_AUTH_USER=yourusername
BASIC_AUTH_PASS=yourpassword
```

### 🧾 Form Fields

| Field | Type         | Required | Description                       |
|-------|--------------|----------|-----------------------------------|
| file  | UploadFile   | ✅ Yes   | Audio or video file to transcribe |

> **Note:** The `task` parameter is internally locked to `"transcribe"` for safety.

---

### ✅ Supported File Types

| Extensions                                              | MIME types       |
|---------------------------------------------------------|------------------|
| .mp3, .mp4, .wav, .m4a, .avi, .flac, .aac, .mov, .webm   | audio/*, video/* |


### 📤 Sample Response

```json
{
  "language": "hi",
  "duration": 21.34,
  "raw_text": "Raw transcription from Whisper",
  "punctuated_text": "Transcription with punctuation using GPT-3.5"
}
```

Note: If GPT fails, punctuated_text will include a fallback message and the raw text instead.

## 🚀 Quickstart

### 1. Clone and Set Up

```shell
git clone https://github.com/pranavnbapat/transcriber.git
cd transcriber
```

### 2. Create .env
```dotenv
BASIC_AUTH_USER=admin
BASIC_AUTH_PASS=strongpassword
OPENAI_API_KEY=sk-...
```

### 3. Build and Run Docker Image
```docker
docker compose up -d
```
