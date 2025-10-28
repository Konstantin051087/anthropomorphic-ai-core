from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
from shared.logger import get_logger
from shared.schemas import EmotionLabel, PersonaType, PersonaConfig, DEFAULT_PERSONAS
from emotional_analysis.analyzer import EmotionResult

logger = get_logger(__name__)

@dataclass
class PersonaResponse:
    """Результат применения персонажа"""
    emotion: EmotionLabel
    confidence: float
    adjusted_scores: Dict[EmotionLabel, float]
    persona_used: PersonaType

class PersonaManager:
    """Менеджер персонажей для настройки эмоциональных реакций"""
    
    def __init__(self):
        self.personas: Dict[PersonaType, PersonaConfig] = DEFAULT_PERSONAS
        self._load_custom_personas()
    
    def _load_custom_personas(self):
        """Загрузка кастомных персонажей из конфигурации"""
        # В будущем можно добавить загрузку из БД или файлов
        pass
    
    def apply_persona(self, emotion_result: EmotionResult, 
                     persona_type: PersonaType) -> PersonaResponse:
        """
        Применение персонажа к результату анализа эмоций
        
        Args:
            emotion_result: Результат анализа эмоций
            persona_type: Тип персонажа для применения
            
        Returns:
            PersonaResponse: Скорректированный результат
        """
        try:
            persona = self.personas.get(persona_type, self.personas[PersonaType.DEFAULT])
            
            # Применение эмоциональных черт персонажа
            adjusted_scores = self._adjust_scores_with_persona(
                emotion_result.emotional_scores,
                persona.emotional_traits
            )
            
            # Определение основной эмоции с учетом персонажа
            primary_emotion, confidence = self._get_adjusted_emotion(adjusted_scores)
            
            logger.debug(f"Applied persona {persona_type}: {emotion_result.primary_emotion} -> {primary_emotion}")
            
            return PersonaResponse(
                emotion=primary_emotion,
                confidence=confidence,
                adjusted_scores=adjusted_scores,
                persona_used=persona_type
            )
            
        except Exception as e:
            logger.error(f"Persona application failed: {str(e)}")
            # Возвращаем исходный результат в случае ошибки
            return PersonaResponse(
                emotion=emotion_result.primary_emotion,
                confidence=emotion_result.confidence,
                adjusted_scores=emotion_result.emotional_scores,
                persona_used=PersonaType.DEFAULT
            )
    
    def _adjust_scores_with_persona(self, original_scores: Dict[EmotionLabel, float],
                                   persona_traits: Dict[EmotionLabel, float]) -> Dict[EmotionLabel, float]:
        """Корректировка оценок с учетом черт персонажа"""
        adjusted_scores = {}
        
        for emotion in EmotionLabel:
            original_score = original_scores.get(emotion, 0.0)
            persona_weight = persona_traits.get(emotion, 0.1)  # default low weight
            
            # Комбинирование исходной оценки и веса персонажа
            adjusted_score = (original_score * 0.7) + (persona_weight * 0.3)
            adjusted_scores[emotion] = adjusted_score
        
        # Нормализация
        total = sum(adjusted_scores.values())
        if total > 0:
            adjusted_scores = {k: v/total for k, v in adjusted_scores.items()}
        
        return adjusted_scores
    
    def _get_adjusted_emotion(self, adjusted_scores: Dict[EmotionLabel, float]) -> tuple[EmotionLabel, float]:
        """Получение скорректированной эмоции"""
        primary_emotion = max(adjusted_scores.items(), key=lambda x: x[1])
        return primary_emotion[0], primary_emotion[1]
    
    def get_available_personas(self) -> List[Dict]:
        """Получение списка доступных персонажей"""
        personas_list = []
        
        for persona_type, config in self.personas.items():
            personas_list.append({
                "name": config.name.value,
                "description": config.description,
                "response_style": config.response_style,
                "temperature": config.temperature,
                "max_length": config.max_length,
                "emotional_traits": {
                    emotion.value: weight 
                    for emotion, weight in config.emotional_traits.items()
                }
            })
        
        return personas_list
    
    def add_custom_persona(self, persona_config: PersonaConfig) -> bool:
        """Добавление кастомного персонажа"""
        try:
            self.personas[persona_config.name] = persona_config
            logger.info(f"Added custom persona: {persona_config.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add custom persona: {str(e)}")
            return False
    
    def remove_persona(self, persona_type: PersonaType) -> bool:
        """Удаление персонажа (кроме дефолтного)"""
        if persona_type == PersonaType.DEFAULT:
            logger.warning("Cannot remove default persona")
            return False
        
        if persona_type in self.personas:
            del self.personas[persona_type]
            logger.info(f"Removed persona: {persona_type}")
            return True
        
        return False