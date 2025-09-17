import json
import asyncio
from typing import Dict
from .logger import get_logger
from .config import settings


logger = get_logger("llm")




async def ask_gpt_for_feedback(target: str, transcript: str) -> Dict:
    """Ask OpenAI chat to return a JSON object with correction and tips. Falls back to a heuristic if unavailable."""
    try:
        import openai
    except Exception:
        openai = None


    system_msg = (
    "You are a friendly concise English tutor. Given a target sentence and the user's actual sentence, "
    "return only a JSON object with keys: corrected, diffs, feedback, tts_text."
    )
    user_msg = f"""Target sentence: "{target}"
    User said: "{transcript}"
    Return only JSON."""


    if openai and settings.OPENAI_API_KEY:
        loop = asyncio.get_running_loop()


        def _call():
            openai.api_key = settings.OPENAI_API_KEY
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.2,
                max_tokens=300,
            )
            try:
                content = resp["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                return parsed
            except Exception as e:
                logger.exception("Failed parsing model response: %s", e)
                return None


        parsed = await loop.run_in_executor(None, _call)
        if parsed:
            return parsed


    # Fallback heuristic (similar to earlier):
    target_words = target.strip().split()
    user_words = transcript.strip().split()
    diffs = []
    for i, tw in enumerate(target_words):
        uw = user_words[i] if i < len(user_words) else ""
        if tw.lower().strip(".,!?;") != uw.lower().strip(".,!?;"):
            diffs.append({"word": uw or "", "correction": tw, "type": "mismatch"})


    feedback = "Good try. Pay attention to word endings and vowel length."
    return {
    "corrected": target,
    "diffs": diffs,
    "feedback": feedback,
    "tts_text": f"Nice try! Say: {target}",
    }