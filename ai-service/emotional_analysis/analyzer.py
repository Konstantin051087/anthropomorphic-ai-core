import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import os
import sys

# Добавление пути к shared модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from logger import get_logger
from schemas import EmotionLabel

logger = get_logger(__name__)

@dataclass
class EmotionResult:
    """Результат анализа эмоций"""
    primary_emotion: EmotionLabel
    confidence: float
    emotional_scores: Dict[EmotionLabel, float]
    processed_text: str

class EmotionAnalyzer:
    """Анализатор эмоций на основе трансформеров"""
    
    def __init__(self, model_name: str = "cointegrated/rubert-tiny2-cedr-emotion-detection"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.labels = [emotion.value for emotion in EmotionLabel]
        self.load_models()
    
    def load_models(self):
        """Загрузка моделей для анализа эмоций"""
        try:
            logger.info(f"Loading emotion model: {self.model_name}")
            
            # Используем pipeline для простоты
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name,
                top_k=None,  # Возвращает все классы
                function_to_apply='softmax'
            )
            
            logger.info("Emotion models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load emotion models: {str(e)}")
            # Создаем заглушку для тестирования
            self.classifier = None
            logger.info("Using fallback emotion analyzer")

@dataclass
class EmotionResult:
    """Результат анализа эмоций"""
    primary_emotion: EmotionLabel
    confidence: float
    emotional_scores: Dict[EmotionLabel, float]
    processed_text: str

class EmotionAnalyzer:
    """Анализатор эмоций на основе трансформеров"""
    
    def __init__(self, model_name: str = "cointegrated/rubert-tiny2-cedr-emotion-detection"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.labels = [emotion.value for emotion in EmotionLabel]
        self.load_models()
    
    def load_models(self):
        """Загрузка моделей для анализа эмоций"""
        try:
            logger.info(f"Loading emotion model: {self.model_name}")
            
            # Используем pipeline для простоты
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name,
                top_k=None,  # Возвращает все классы
                function_to_apply='softmax'
            )
            
            # Альтернативно: ручная загрузка для большего контроля
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            logger.info("Emotion models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load emotion models: {str(e)}")
            raise
    
    def analyze(self, text: str, context: Optional[List[str]] = None, 
                language: str = "ru") -> EmotionResult:
        """
        Анализ эмоций в тексте
        
        Args:
            text: Текст для анализа
            context: Контекст предыдущих сообщений
            language: Язык текста
            
        Returns:
            EmotionResult: Результат анализа
        """
        try:
            # Подготовка текста с учетом контекста
            processed_text = self._preprocess_text(text, context, language)
            
            # Анализ эмоций
            if self.classifier:
                # Используем pipeline
                predictions = self.classifier(processed_text)[0]
                emotional_scores = {
                    pred['label']: float(pred['score']) 
                    for pred in predictions
                }
            else:
                # Ручной inference
                emotional_scores = self._manual_analysis(processed_text)
            
            # Нормализация scores ко всем эмоциям
            normalized_scores = self._normalize_scores(emotional_scores)
            
            # Определение основной эмоции
            primary_emotion, confidence = self._get_primary_emotion(normalized_scores)
            
            return EmotionResult(
                primary_emotion=primary_emotion,
                confidence=confidence,
                emotional_scores=normalized_scores,
                processed_text=processed_text
            )
            
        except Exception as e:
            logger.error(f"Emotion analysis failed: {str(e)}")
            # Возвращаем нейтральный результат в случае ошибки
            return self._get_neutral_result(text)
    
    def _preprocess_text(self, text: str, context: Optional[List[str]], 
                        language: str) -> str:
        """Предобработка текста"""
        # Очистка текста
        text = text.strip()
        if not text:
            return ""
        
        # Добавление контекста если есть
        if context and len(context) > 0:
            # Берем последние 3 сообщения контекста
            recent_context = context[-3:]
            context_text = " [CONTEXT] ".join(recent_context)
            processed_text = f"{context_text} [SEP] {text}"
        else:
            processed_text = text
        
        # Ограничение длины для модели
        max_length = 512
        if len(processed_text) > max_length:
            processed_text = processed_text[:max_length]
            
        return processed_text
    
    def _manual_analysis(self, text: str) -> Dict[str, float]:
        """Ручной анализ эмоций (альтернативный метод)"""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Models not loaded")
        
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        scores = predictions[0].cpu().numpy()
        
        # Сопоставление с нашими эмоциональными метками
        emotional_scores = {}
        for i, score in enumerate(scores):
            if i < len(self.labels):
                emotion = self.labels[i]
                emotional_scores[emotion] = float(score)
        
        return emotional_scores
    
    def _normalize_scores(self, emotional_scores: Dict[str, float]) -> Dict[EmotionLabel, float]:
        """Нормализация оценок эмоций"""
        normalized = {}
        total = sum(emotional_scores.values())
        
        if total == 0:
            # Равномерное распределение если все нули
            default_score = 1.0 / len(EmotionLabel)
            for emotion in EmotionLabel:
                normalized[emotion] = default_score
        else:
            # Нормализация и маппинг к нашим EmotionLabel
            for emotion in EmotionLabel:
                score = emotional_scores.get(emotion.value, 0.0)
                normalized[emotion] = score / total
        
        return normalized
    
    def _get_primary_emotion(self, emotional_scores: Dict[EmotionLabel, float]) -> Tuple[EmotionLabel, float]:
        """Определение основной эмоции"""
        primary_emotion = max(emotional_scores.items(), key=lambda x: x[1])
        return primary_emotion[0], primary_emotion[1]
    
    def _get_neutral_result(self, text: str) -> EmotionResult:
        """Возврат нейтрального результата при ошибке"""
        neutral_scores = {emotion: 0.0 for emotion in EmotionLabel}
        neutral_scores[EmotionLabel.NEUTRAL] = 1.0
        
        return EmotionResult(
            primary_emotion=EmotionLabel.NEUTRAL,
            confidence=1.0,
            emotional_scores=neutral_scores,
            processed_text=text
        )
    
    def check_models_health(self) -> Dict[str, str]:
        """Проверка состояния моделей"""
        status = {}
        try:
            if self.classifier:
                # Тестовый запрос
                test_result = self.classifier("test", top_k=1)
                status["emotion_model"] = "healthy"
            else:
                status["emotion_model"] = "not_loaded"
                
        except Exception as e:
            status["emotion_model"] = f"error: {str(e)}"
            
        return status
    
    def get_model_version(self) -> str:
        """Получение версии модели"""
        return f"{self.model_name}-v1.0"