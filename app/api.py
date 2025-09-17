from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import uuid
from .logger import get_logger
from .utils import ensure_tmp_dir, convert_webm_to_wav, cleanup_file, similarity_score
from .stt import transcribe_openai
from .llm import ask_gpt_for_feedback
from .schemas import PracticeResponse


router = APIRouter()
logger = get_logger("api")


@router.get("/exercises")
async def get_exercises():
    return [
    {"id": 1, "text": "I would like a cup of coffee, please.", "level": "beginner"},
    {"id": 2, "text": "Could you tell me how to get to the train station?", "level": "intermediate"},
    ]


@router.post("/practice", response_model=PracticeResponse)
async def practice(audio: UploadFile = File(...), target: str = Form(...)):
    tmpdir = ensure_tmp_dir()
    uid = uuid.uuid4().hex
    webm_path = tmpdir / f"{uid}.webm"
    wav_path = tmpdir / f"{uid}.wav"


    # Save uploaded file
    async with aiofiles.open(webm_path, "wb") as f:
        content = await audio.read()
        await f.write(content)


    try:
        # Convert to WAV for STT if needed
        try:
            convert_webm_to_wav(str(webm_path), str(wav_path))
            stt_path = str(wav_path)
        except Exception:
            # if conversion fails, try transcribing webm directly
            stt_path = str(webm_path)
    except Exception as e:
        logger.error(f"Error during audio processing: {e}")
        raise HTTPException(status_code=500, detail="Audio processing failed")


        # Transcribe
        stt = await transcribe_openai(stt_path)
        transcript_text = (stt.get("text") or "").strip()
        confidence = stt.get("confidence")


        # Ask LLM for feedback
        feedback = await ask_gpt_for_feedback(target, transcript_text)


        score = similarity_score(target, transcript_text)


        return JSONResponse({
        "transcript": transcript_text,
        "corrected": feedback.get("corrected", target),
        "diffs": feedback.get("diffs", []),
        "score": score
        })