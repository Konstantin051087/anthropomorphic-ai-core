from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MoodType(str, Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    EXCITED = "excited"
    CALM = "calm"

class MemoryType(str, Enum):
    FACT = "fact"
    EXPERIENCE = "experience"
    CONVERSATION = "conversation"
    KNOWLEDGE = "knowledge"

class PersonalityTrait(str, Enum):
    OPENNESS = "openness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    NEUROTICISM = "neuroticism"

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Сообщение пользователя")
    user_id: Optional[str] = Field(None, description="ID пользователя")
    session_id: Optional[str] = Field(None, description="ID сессии")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Ответ AI модели")
    mood: MoodType = Field(..., description="Текущее настроение AI")
    memory_used: bool = Field(False, description="Была ли использована память")
    session_id: Optional[str] = Field(None, description="ID сессии")
    timestamp: str = Field(..., description="Временная метка ответа")

class SystemState(BaseModel):
    status: str = Field(..., description="Статус системы")
    mood: MoodType = Field(..., description="Текущее настроение")
    active_modules: List[str] = Field(..., description="Активные модули")
    last_interaction: Optional[str] = Field(None, description="Последнее взаимодействие")
    system_health: str = Field(..., description="Здоровье системы")
    timestamp: str = Field(..., description="Временная метка")

class MemoryStoreRequest(BaseModel):
    content: str = Field(..., min_length=1, description="Содержимое для сохранения")
    memory_type: MemoryType = Field(..., description="Тип памяти")
    importance: float = Field(1.0, ge=0.0, le=10.0, description="Важность (0-10)")

class MemoryRecallRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Запрос для поиска")
    memory_type: Optional[MemoryType] = Field(None, description="Тип памяти для фильтрации")
    limit: int = Field(10, ge=1, le=100, description="Лимит результатов")

class MoodUpdateRequest(BaseModel):
    mood: MoodType = Field(..., description="Новое настроение")
    intensity: float = Field(1.0, ge=0.0, le=1.0, description="Интенсивность настроения")
    reason: Optional[str] = Field(None, description="Причина изменения")

class PersonalityUpdateRequest(BaseModel):
    trait: PersonalityTrait = Field(..., description="Черта личности")
    value: float = Field(..., ge=0.0, le=1.0, description="Значение черты")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Описание ошибки")
    error_code: Optional[str] = Field(None, description="Код ошибки")
    timestamp: str = Field(..., description="Временная метка ошибки")