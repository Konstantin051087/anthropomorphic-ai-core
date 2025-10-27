"""
Валидатор профилей и данных персонажей
"""

import logging
import re
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)

class ProfileValidator:
    def __init__(self):
        self.allowed_emotions = ['happy', 'sad', 'angry', 'neutral', 'excited', 'calm']
        self.required_persona_fields = ['name', 'personality_traits']
        self.max_name_length = 50
        self.max_description_length = 200
        
    def validate_persona_data(self, persona_data: Dict) -> Tuple[bool, List[str]]:
        """Валидация данных персонажа"""
        errors = []
        
        # Проверка обязательных полей
        for field in self.required_persona_fields:
            if field not in persona_data:
                errors.append(f"Обязательное поле отсутствует: {field}")
        
        # Валидация имени
        if 'name' in persona_data:
            name_errors = self._validate_name(persona_data['name'])
            errors.extend(name_errors)
        
        # Валидация черт личности
        if 'personality_traits' in persona_data:
            trait_errors = self._validate_personality_traits(persona_data['personality_traits'])
            errors.extend(trait_errors)
        
        # Валидация эмоционального состояния
        if 'emotional_state' in persona_data:
            emotion_errors = self._validate_emotional_state(persona_data['emotional_state'])
            errors.extend(emotion_errors)
        
        # Валидация стиля общения
        if 'communication_style' in persona_data:
            style_errors = self._validate_communication_style(persona_data['communication_style'])
            errors.extend(style_errors)
        
        is_valid = len(errors) == 0
        logger.debug(f"🔍 Валидация персонажа: {is_valid}, ошибки: {errors}")
        
        return is_valid, errors
    
    def _validate_name(self, name: str) -> List[str]:
        """Валидация имени персонажа"""
        errors = []
        
        if not isinstance(name, str):
            errors.append("Имя должно быть строкой")
            return errors
        
        name = name.strip()
        
        if not name:
            errors.append("Имя не может быть пустым")
        
        if len(name) > self.max_name_length:
            errors.append(f"Имя слишком длинное (максимум {self.max_name_length} символов)")
        
        # Проверка на запрещенные символы
        if re.search(r'[<>{}[\]$]', name):
            errors.append("Имя содержит запрещенные символы")
        
        return errors
    
    def _validate_personality_traits(self, traits: Dict) -> List[str]:
        """Валидация черт личности"""
        errors = []
        
        if not isinstance(traits, dict):
            errors.append("Черты личности должны быть словарем")
            return errors
        
        if not traits:
            errors.append("Словарь черт личности не может быть пустым")
        
        for trait, value in traits.items():
            if not isinstance(trait, str):
                errors.append(f"Ключ черты должен быть строкой: {trait}")
            
            if not isinstance(value, bool):
                errors.append(f"Значение черты должно быть boolean: {trait}")
        
        return errors
    
    def _validate_emotional_state(self, emotional_state: Dict) -> List[str]:
        """Валидация эмоционального состояния"""
        errors = []
        
        if not isinstance(emotional_state, dict):
            errors.append("Эмоциональное состояние должно быть словарем")
            return errors
        
        # Валидация текущего настроения
        if 'current_mood' in emotional_state:
            mood = emotional_state['current_mood']
            if mood not in self.allowed_emotions:
                errors.append(f"Недопустимое настроение: {mood}. Допустимые: {', '.join(self.allowed_emotions)}")
        
        # Валидация истории эмоций
        if 'emotional_history' in emotional_state:
            history = emotional_state['emotional_history']
            if not isinstance(history, list):
                errors.append("История эмоций должна быть списком")
            else:
                for item in history:
                    if not isinstance(item, dict):
                        errors.append("Элемент истории эмоций должен быть словарем")
        
        # Валидация стабильности настроения
        if 'mood_stability' in emotional_state:
            stability = emotional_state['mood_stability']
            if not isinstance(stability, (int, float)):
                errors.append("Стабильность настроения должна быть числом")
            elif not 0 <= stability <= 1:
                errors.append("Стабильность настроения должна быть между 0 и 1")
        
        return errors
    
    def _validate_communication_style(self, style: Dict) -> List[str]:
        """Валидация стиля общения"""
        errors = []
        
        if not isinstance(style, dict):
            errors.append("Стиль общения должен быть словарем")
            return errors
        
        allowed_style_keys = ['formal', 'warm', 'supportive', 'encouraging', 'structured', 'detailed', 'objective']
        
        for key, value in style.items():
            if key not in allowed_style_keys:
                errors.append(f"Недопустимый ключ стиля общения: {key}")
            
            if not isinstance(value, bool):
                errors.append(f"Значение стиля общения должно быть boolean: {key}")
        
        return errors
    
    def validate_interaction_data(self, interaction_data: Dict) -> Tuple[bool, List[str]]:
        """Валидация данных взаимодействия"""
        errors = []
        
        # Проверка текста сообщения
        if 'text' not in interaction_data:
            errors.append("Отсутствует текст сообщения")
        else:
            text = interaction_data['text']
            if not isinstance(text, str):
                errors.append("Текст сообщения должен быть строкой")
            elif not text.strip():
                errors.append("Текст сообщения не может быть пустым")
            elif len(text) > 1000:
                errors.append("Текст сообщения слишком длинный")
        
        # Проверка ID персонажа
        if 'persona_id' not in interaction_data:
            errors.append("Отсутствует ID персонажа")
        else:
            persona_id = interaction_data['persona_id']
            if not isinstance(persona_id, int):
                errors.append("ID персонажа должен быть целым числом")
            elif persona_id < 1:
                errors.append("ID персонажа должен быть положительным числом")
        
        is_valid = len(errors) == 0
        logger.debug(f"🔍 Валидация взаимодействия: {is_valid}, ошибки: {errors}")
        
        return is_valid, errors
    
    def sanitize_text(self, text: str) -> str:
        """Очистка текста от потенциально опасных символов"""
        if not isinstance(text, str):
            return ""
        
        # Удаление потенциально опасных HTML/JS тегов
        sanitized = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
        
        # Удаление опасных символов
        sanitized = re.sub(r'[{}<>]', '', sanitized)
        
        # Обрезка длины
        sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Получение правил валидации"""
        return {
            'allowed_emotions': self.allowed_emotions,
            'required_persona_fields': self.required_persona_fields,
            'max_name_length': self.max_name_length,
            'max_description_length': self.max_description_length,
            'max_text_length': 1000
        }