import os
import asyncio
import tempfile
from pathlib import Path
from typing import Dict


from .logger import get_logger
from .config import settings


logger = get_logger("stt")




async def transcribe_openai(audio_path: str) -> Dict:
    """Call OpenAI's whisper or fallback mock. This is a blocking call in the SDK; run in executor."""
    try:
        import openai
    except Exception:
        openai = None


    if not openai or not settings.OPENAI_API_KEY:
    # Mock
        logger.info("OpenAI not configured; returning mock transcription")
        return {"text": "I want a cup of coffe", "confidence": 0.85}


    loop = asyncio.get_running_loop()


    def _call():
        openai.api_key = settings.OPENAI_API_KEY
        with open(audio_path, "rb") as f:
        # adapt to your openai package version
            resp = openai.Audio.transcribe("whisper-1", f)
            text = resp.get("text") or resp.get("transcript") or ""
            confidence = resp.get("confidence", 0.9)
            return {"text": text, "confidence": confidence}


    result = await loop.run_in_executor(None, _call)
    return result