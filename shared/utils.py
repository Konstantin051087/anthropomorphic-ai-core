import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import re
import hashlib

class JSONEncoder(json.JSONEncoder):
    """Кастомный JSON энкодер для обработки специальных типов"""
    
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)

def generate_session_id() -> str:
    """Генерация уникального ID сессии"""
    return str(uuid.uuid4())

def get_current_timestamp() -> datetime:
    """Получение текущего времени в UTC"""
    return datetime.now(timezone.utc)

def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Очистка и обрезка текста"""
    if not text:
        return ""
    
    # Удаление лишних пробелов
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Обрезка до максимальной длины
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + "..."
    
    return text

def calculate_confidence_score(scores: Dict[str, float]) -> float:
    """Расчет confidence score на основе эмоциональных оценок"""
    if not scores:
        return 0.0
    
    max_score = max(scores.values())
    total_score = sum(scores.values())
    
    if total_score == 0:
        return 0.0
    
    # Нормализация confidence score
    confidence = max_score / total_score
    return round(confidence, 4)

def hash_user_id(user_id: str) -> str:
    """Хеширование user_id для анонимизации"""
    if not user_id:
        return ""
    return hashlib.sha256(user_id.encode()).hexdigest()

def validate_emotion_label(emotion: str, allowed_emotions: List[str]) -> bool:
    """Валидация эмоциональной метки"""
    return emotion.lower() in [e.lower() for e in allowed_emotions]

def merge_context(context: Optional[List[str]], new_text: str, max_context_length: int = 5) -> List[str]:
    """Обновление контекста диалога"""
    if context is None:
        context = []
    
    context.append(new_text)
    
    # Ограничение длины контекста
    if len(context) > max_context_length:
        context = context[-max_context_length:]
    
    return context

def format_response_data(session_id: str, emotion: str, confidence: float, 
                        analyzed_text: str, persona: str) -> Dict[str, Any]:
    """Форматирование данных ответа"""
    return {
        "session_id": session_id,
        "emotion": emotion,
        "confidence": confidence,
        "analyzed_text": analyzed_text,
        "persona": persona,
        "timestamp": get_current_timestamp().isoformat(),
        "version": "1.0.0"
    }

def safe_json_dumps(data: Dict[str, Any]) -> str:
    """Безопасная сериализация в JSON"""
    try:
        return json.dumps(data, cls=JSONEncoder, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return json.dumps({"error": f"Serialization error: {str(e)}"})

def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """Безопасная десериализация из JSON"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"Deserialization error: {str(e)}"}