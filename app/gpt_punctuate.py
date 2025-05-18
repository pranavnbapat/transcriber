# app/gpt_punctuate.py

import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def punctuate_text(text: str, language: str = "hi") -> str:
    """
    Uses GPT-3.5 Turbo to add punctuation to Whisper output.

    Args:
        text (str): Raw Whisper transcription (may lack punctuation).
        language (str): Language code (like 'hi' for Hindi).

    Returns:
        str: Punctuated text.
    """
    prompt = (
        f"Please detect the language of the text and add proper punctuation and sentence boundaries. "
        f"Do not translate or rephrase. Keep the original words and language:\n\n{text}"
    )

    messages: list[ChatCompletionUserMessageParam] = [
        ChatCompletionUserMessageParam(role="user", content=prompt)
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
