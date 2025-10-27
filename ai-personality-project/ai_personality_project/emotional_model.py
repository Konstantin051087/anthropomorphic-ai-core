"""
Базовая модель эмоционального анализа
"""

import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)

class EmotionalModel:
    def __init__(self):
        self._initialized = False
        self.emotion_keywords = {
            'happy': {
                'words': ['рад', 'счастлив', 'хорошо', 'отлично', 'прекрасно', 'ура', 'восторг', 'любовь', 'нравится'],
                'emojis': ['😊', '😄', '🥰', '👍', '🎉'],
                'weight': 1.0
            },
            'sad': {
                'words': ['грустно', 'печально', 'плохо', 'жаль', 'несчастный', 'плач', 'слезы', 'тоска'],
                'emojis': ['😢', '😭', '😞', '💔'],
                'weight': 1.0
            },
            'angry': {
                'words': ['злой', 'сердит', 'разозлился', 'бесит', 'раздражает', 'ненавижу', 'ярость', 'гнев'],
                'emojis': ['😠', '😡', '💢'],
                'weight': 1.2
            },
            'excited': {
                'words': ['восторг', 'волнуюсь', 'интересно', 'невероятно', 'потрясающе', 'супер', 'круто'],
                'emojis': ['🤩', '🎊', '🚀'],
                'weight': 0.9
            },
            'calm': {
                'words': ['спокойно', 'умиротворенно', 'мирно', 'тихо', 'расслабленно', 'безмятежно'],
                'emojis': ['😌', '🌅', '🍃'],
                'weight': 0.8
            }
        }
        
    def initialize(self):
        """Инициализация эмоциональной модели"""
        try:
            logger.info("🔄 Инициализация EmotionalModel...")
            self._initialized = True
            logger.info("✅ EmotionalModel инициализирована")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации EmotionalModel: {e}")
            raise
    
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """Анализ эмоциональной окраски текста"""
        if not self._initialized:
            self.initialize()
            
        try:
            text_lower = text.lower().strip()
            
            # Подсчет очков для каждой эмоции
            emotion_scores = {emotion: 0.0 for emotion in self.emotion_keywords}
            
            # Анализ по ключевым словам
            for emotion, data in self.emotion_keywords.items():
                for word in data['words']:
                    if word in text_lower:
                        emotion_scores[emotion] += 1.0 * data['weight']
                
                # Анализ эмодзи
                for emoji in data['emojis']:
                    if emoji in text:
                        emotion_scores[emotion] += 2.0 * data['weight']
            
            # Анализ восклицательных знаков (интенсивность)
            exclamation_count = text.count('!')
            if exclamation_count > 0:
                # Увеличиваем оценки для эмоциональных состояний
                for emotion in ['excited', 'angry', 'happy']:
                    if emotion in emotion_scores:
                        emotion_scores[emotion] += exclamation_count * 0.5
            
            # Анализ вопросительных знаков
            question_count = text.count('?')
            if question_count > 0:
                emotion_scores['calm'] += question_count * 0.3
            
            # Если нет явных эмоций - neutral
            if sum(emotion_scores.values()) == 0:
                emotion_scores['neutral'] = 1.0
            else:
                # Нормализация оценок
                total_score = sum(emotion_scores.values())
                for emotion in emotion_scores:
                    emotion_scores[emotion] = emotion_scores[emotion] / total_score
            
            # Определение доминирующей эмоции
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            
            result = {
                'dominant_emotion': dominant_emotion[0],
                'emotion_scores': emotion_scores,
                'confidence': dominant_emotion[1],
                'text_length': len(text),
                'word_count': len(text.split())
            }
            
            logger.debug(f"📊 Анализ эмоций: '{text}' -> {dominant_emotion[0]} ({dominant_emotion[1]:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка анализа эмоций: {e}")
            return {
                'dominant_emotion': 'neutral',
                'emotion_scores': {'neutral': 1.0},
                'confidence': 0.0,
                'error': str(e)
            }
    
    def update_emotional_state(self, current_state: Dict, new_analysis: Dict) -> Dict:
        """Обновление эмоционального состояния на основе нового анализа"""
        if not current_state:
            current_state = {
                'emotional_history': [],
                'current_mood': 'neutral',
                'mood_stability': 0.5
            }
        
        # Добавление нового анализа в историю
        current_state.setdefault('emotional_history', []).append({
            'emotion': new_analysis['dominant_emotion'],
            'confidence': new_analysis['confidence'],
            'timestamp': 'current'  # В реальном приложении здесь будет timestamp
        })
        
        # Ограничение размера истории (последние 10 анализов)
        if len(current_state['emotional_history']) > 10:
            current_state['emotional_history'] = current_state['emotional_history'][-10:]
        
        # Расчет общего эмоционального состояния
        recent_emotions = [item['emotion'] for item in current_state['emotional_history'][-5:]]
        
        if recent_emotions:
            from collections import Counter
            emotion_counts = Counter(recent_emotions)
            current_state['current_mood'] = emotion_counts.most_common(1)[0][0]
            
            # Расчет стабильности настроения
            if len(recent_emotions) > 1:
                unique_emotions = len(set(recent_emotions))
                current_state['mood_stability'] = 1.0 - (unique_emotions / len(recent_emotions))
        
        return current_state
    
    def get_emotion_statistics(self) -> Dict[str, Any]:
        """Получение статистики по эмоциональной модели"""
        return {
            'initialized': self._initialized,
            'emotions_tracked': list(self.emotion_keywords.keys()),
            'keywords_per_emotion': {k: len(v['words']) for k, v in self.emotion_keywords.items()}
        }