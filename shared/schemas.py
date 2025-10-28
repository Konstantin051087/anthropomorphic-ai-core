from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import re

class EmotionLabel(str, Enum):
    """Поддерживаемые эмоциональные метки"""
    JOY = "joy"
    SADNESS = "sadness" 
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"
    EXCITEMENT = "excitement"
    CONFUSION = "confusion"
    ANTICIPATION = "anticipation"

class PersonaType(str, Enum):
    """Типы персонажей"""
    DEFAULT = "default"
    EMPATHETIC = "empathetic"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PROFESSIONAL = "professional"

class EmotionAnalysisRequest(BaseModel):
    """Схема запроса для анализа эмоций"""
    text: str = Field(..., min_length=1, max_length=5000, description="Текст для анализа")
    user_id: Optional[str] = Field(None, description="Идентификатор пользователя")
    context: Optional[List[str]] = Field(None, description="Контекст предыдущих сообщений")
    persona: PersonaType = Field(PersonaType.DEFAULT, description="Тип персонажа для ответа")
    language: str = Field("ru", regex="^(ru|en)$", description="Язык текста")
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace")
        return v.strip()
    
    @validator('context')
    def validate_context(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Context cannot exceed 10 messages")
        return v

class EmotionAnalysisResponse(BaseModel):
    """Схема ответа анализа эмоций"""
    session_id: str = Field(..., description="Уникальный идентификатор сессии")
    emotion: EmotionLabel = Field(..., description="Определенная эмоция")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Уверенность в определении")
    analyzed_text: str = Field(..., description="Проанализированный текст")
    persona: PersonaType = Field(..., description="Использованный персонаж")
    timestamp: datetime = Field(..., description="Время анализа")
    emotional_scores: Dict[EmotionLabel, float] = Field(..., description="Оценки по всем эмоциям")
    version: str = Field(..., description="Версия модели")

class PersonaConfig(BaseModel):
    """Конфигурация персонажа"""
    name: PersonaType = Field(..., description="Название персонажа")
    description: str = Field(..., description="Описание персонажа")
    emotional_traits: Dict[EmotionLabel, float] = Field(..., description="Эмоциональные черты")
    response_style: str = Field(..., description="Стиль ответа")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="Температура генерации")
    max_length: int = Field(100, ge=10, le=500, description="Максимальная длина ответа")

class HealthCheckResponse(BaseModel):
    """Схема ответа проверки здоровья"""
    status: str = Field(..., description="Статус сервиса")
    service: str = Field(..., description="Название сервиса")
    timestamp: datetime = Field(..., description="Время проверки")
    version: str = Field(..., description="Версия сервиса")
    dependencies: Dict[str, str] = Field(..., description="Статусы зависимостей")

class ErrorResponse(BaseModel):
    """Схема ответа ошибки"""
    error: str = Field(..., description="Текст ошибки")
    code: str = Field(..., description="Код ошибки")
    details: Optional[Dict[str, Any]] = Field(None, description="Детали ошибки")
    timestamp: datetime = Field(..., description="Время ошибки")

class TrainingRequest(BaseModel):
    """Схема запроса на обучение модели"""
    dataset_path: str = Field(..., description="Путь к датасету")
    model_name: str = Field(..., description="Название модели")
    epochs: int = Field(3, ge=1, le=10, description="Количество эпох")
    batch_size: int = Field(16, ge=1, le=64, description="Размер батча")
    learning_rate: float = Field(2e-5, ge=1e-6, le=1e-3, description="Скорость обучения")

class TrainingResponse(BaseModel):
    """Схема ответа обучения модели"""
    training_id: str = Field(..., description="ID обучения")
    status: str = Field(..., description="Статус обучения")
    model_path: Optional[str] = Field(None, description="Путь к обученной модели")
    metrics: Optional[Dict[str, float]] = Field(None, description="Метрики обучения")
    started_at: datetime = Field(..., description="Время начала")
    completed_at: Optional[datetime] = Field(None, description="Время завершения")

# Конфигурации персонажей по умолчанию
DEFAULT_PERSONAS = {
    PersonaType.DEFAULT: PersonaConfig(
        name=PersonaType.DEFAULT,
        description="Балансированный персонаж с естественными реакциями",
        emotional_traits={
            EmotionLabel.JOY: 0.3,
            EmotionLabel.NEUTRAL: 0.4,
            EmotionLabel.SADNESS: 0.1,
            EmotionLabel.ANGER: 0.05,
            EmotionLabel.FEAR: 0.05,
            EmotionLabel.SURPRISE: 0.1
        },
        response_style="balanced",
        temperature=0.7,
        max_length=150
    ),
    PersonaType.EMPATHETIC: PersonaConfig(
        name=PersonaType.EMPATHETIC,
        description="Эмпатичный персонаж с глубоким пониманием эмоций",
        emotional_traits={
            EmotionLabel.JOY: 0.4,
            EmotionLabel.SADNESS: 0.3,
            EmotionLabel.NEUTRAL: 0.2,
            EmotionLabel.SURPRISE: 0.1
        },
        response_style="empathetic",
        temperature=0.8,
        max_length=200
    )
}