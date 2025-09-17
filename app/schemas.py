from pydantic import BaseModel
from typing import List, Optional

class Exercise(BaseModel):
    id: int
    text: str
    level: Optional[str]


class PracticeResponse(BaseModel):
    transcript: str
    corrected: str
    diffs: List[dict]
    score: int
    confidence: Optional[float]
    feedback: Optional[str]
    tts_text: Optional[str]