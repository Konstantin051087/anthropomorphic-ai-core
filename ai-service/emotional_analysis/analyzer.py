import torch
from transformers import pipeline
from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from logger import get_logger
from schemas import EmotionLabel

logger = get_logger(__name__)

@dataclass
class EmotionResult:
    primary_emotion: EmotionLabel
    confidence: float
    emotional_scores: Dict[EmotionLabel, float]
    processed_text: str

class EmotionAnalyzer:
    def __init__(self, model_name: str = "cointegrated/rubert-tiny2-cedr-emotion-detection"):
        self.model_name = model_name
        self.classifier = None
        self.labels = [emotion.value for emotion in EmotionLabel]
        self.load_models()
    
    def load_models(self):
        try:
            logger.info(f"Loading emotion model: {self.model_name}")
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name,
                top_k=None,
                function_to_apply='softmax'
            )
            logger.info("Emotion models loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load emotion models: {str(e)}")
            self.classifier = None

    def analyze(self, text: str, context: Optional[List[str]] = None, language: str = "ru") -> EmotionResult:
        try:
            processed_text = self._preprocess_text(text, context, language)
            
            if self.classifier:
                predictions = self.classifier(processed_text)[0]
                emotional_scores = {pred['label']: float(pred['score']) for pred in predictions}
            else:
                emotional_scores = self._fallback_analysis(processed_text)
            
            normalized_scores = self._normalize_scores(emotional_scores)
            primary_emotion, confidence = self._get_primary_emotion(normalized_scores)
            
            return EmotionResult(
                primary_emotion=primary_emotion,
                confidence=confidence,
                emotional_scores=normalized_scores,
                processed_text=processed_text
            )
            
        except Exception as e:
            logger.error(f"Emotion analysis failed: {str(e)}")
            return self._get_neutral_result(text)
    
    def _preprocess_text(self, text: str, context: Optional[List[str]], language: str) -> str:
        text = text.strip()
        if not text:
            return ""
        
        if context and len(context) > 0:
            recent_context = context[-3:]
            context_text = " [CONTEXT] ".join(recent_context)
            processed_text = f"{context_text} [SEP] {text}"
        else:
            processed_text = text
        
        max_length = 512
        if len(processed_text) > max_length:
            processed_text = processed_text[:max_length]
            
        return processed_text
    
    def _fallback_analysis(self, text: str) -> Dict[str, float]:
        return {emotion: 0.0 for emotion in self.labels}
    
    def _normalize_scores(self, emotional_scores: Dict[str, float]) -> Dict[EmotionLabel, float]:
        normalized = {}
        total = sum(emotional_scores.values())
        
        if total == 0:
            default_score = 1.0 / len(EmotionLabel)
            for emotion in EmotionLabel:
                normalized[emotion] = default_score
        else:
            for emotion in EmotionLabel:
                score = emotional_scores.get(emotion.value, 0.0)
                normalized[emotion] = score / total
        
        return normalized
    
    def _get_primary_emotion(self, emotional_scores: Dict[EmotionLabel, float]) -> Tuple[EmotionLabel, float]:
        primary_emotion = max(emotional_scores.items(), key=lambda x: x[1])
        return primary_emotion[0], primary_emotion[1]
    
    def _get_neutral_result(self, text: str) -> EmotionResult:
        neutral_scores = {emotion: 0.0 for emotion in EmotionLabel}
        neutral_scores[EmotionLabel.NEUTRAL] = 1.0
        
        return EmotionResult(
            primary_emotion=EmotionLabel.NEUTRAL,
            confidence=1.0,
            emotional_scores=neutral_scores,
            processed_text=text
        )
    
    def check_models_health(self) -> Dict[str, str]:
        status = {}
        try:
            if self.classifier:
                test_result = self.classifier("test", top_k=1)
                status["emotion_model"] = "healthy"
            else:
                status["emotion_model"] = "not_loaded"
        except Exception as e:
            status["emotion_model"] = f"error: {str(e)}"
        return status