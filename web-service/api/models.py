from pydantic import BaseModel
from typing import Optional, List

class EmotionAnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    context: Optional[List[str]] = None

class EmotionAnalysisResponse(BaseModel):
    session_id: str
    emotion: str
    confidence: float
    analyzed_text: str
    persona: str