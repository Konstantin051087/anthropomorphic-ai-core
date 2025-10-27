"""
Основное ядро AI системы
"""

import logging
from typing import Dict, Any, Optional
import random

logger = logging.getLogger(__name__)

class AICore:
    def __init__(self):
        self.emotional_model = None
        self.persona_manager = None
        self._initialized = False
        
    def initialize(self):
        """Инициализация всех компонентов AI"""
        try:
            # Ленивая загрузка компонентов
            from ai_personality_project.emotional_model import EmotionalModel
            from ai_personality_project.advanced_persona_manager import AdvancedPersonaManager
            
            logger.info("🔄 Инициализация AI Core...")
            
            self.emotional_model = EmotionalModel()
            self.persona_manager = AdvancedPersonaManager()
            
            # Инициализация компонентов
            self.emotional_model.initialize()
            self.persona_manager.initialize()
            
            self._initialized = True
            logger.info("✅ AI Core успешно инициализирован")
            
        except ImportError as e:
            logger.warning(f"Модули не найдены, используется упрощенный режим: {e}")
            self._setup_fallback_mode()
        except Exception as e:
            logger.error(f"Ошибка инициализации AI Core: {e}")
            self._setup_fallback_mode()
    
    def _setup_fallback_mode(self):
        """Резервный режим работы при ошибках"""
        logger.info("🔄 Активация резервного режима...")
        
        class FallbackEmotionalModel:
            def initialize(self): pass
            def analyze_emotion(self, text):
                emotions = ['happy', 'sad', 'angry', 'neutral', 'excited']
                return {
                    'dominant_emotion': random.choice(emotions),
                    'confidence': random.uniform(0.5, 0.9),
                    'emotion_scores': {e: random.random() for e in emotions}
                }
        
        class FallbackPersonaManager:
            def initialize(self): pass
            def get_persona(self, persona_id):
                personas = {
                    1: {'name': 'Дружелюбный помощник', 'personality_traits': {'friendly': True}},
                    2: {'name': 'Профессиональный советник', 'personality_traits': {'professional': True}}
                }
                return personas.get(persona_id, personas[1])
            def list_personas(self):
                return [
                    {'id': 1, 'name': 'Дружелюбный помощник'},
                    {'id': 2, 'name': 'Профессиональный советник'}
                ]
        
        self.emotional_model = FallbackEmotionalModel()
        self.persona_manager = FallbackPersonaManager()
        self._initialized = True
        logger.info("✅ Резервный режим активирован")
    
    def process_interaction(self, text: str, persona_id: int) -> Dict[str, Any]:
        """Обработка взаимодействия с пользователем"""
        if not self._initialized:
            self.initialize()
            
        try:
            logger.info(f"🔍 Анализ сообщения: '{text}' для персонажа {persona_id}")
            
            # Анализ эмоций
            emotion_analysis = self.emotional_model.analyze_emotion(text)
            
            # Получение персонажа
            persona = self.persona_manager.get_persona(persona_id)
            
            # Генерация ответа
            response = self._generate_response(text, emotion_analysis, persona)
            
            logger.info(f"✅ Ответ сгенерирован: {response[:50]}...")
            
            return {
                'success': True,
                'response': response,
                'emotion_analysis': emotion_analysis,
                'persona_id': persona_id,
                'persona_name': persona.get('name', 'Неизвестный')
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки взаимодействия: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Извините, произошла ошибка при обработке вашего запроса.'
            }
    
    def _generate_response(self, text: str, emotion_analysis: Dict, persona: Dict) -> str:
        """Генерация персонализированного ответа"""
        emotion = emotion_analysis.get('dominant_emotion', 'neutral')
        persona_traits = persona.get('personality_traits', {})
        
        # Базовые шаблоны ответов в зависимости от эмоции
        emotion_responses = {
            'happy': [
                "Рад слышать! ",
                "Это замечательно! ",
                "Как здорово! ",
                "Отличные новости! "
            ],
            'sad': [
                "Мне жаль это слышать. ",
                "Понимаю ваши чувства. ",
                "Это действительно грустно. ",
                "Сочувствую вам. "
            ],
            'angry': [
                "Понимаю ваше раздражение. ",
                "Давайте разберемся с этим спокойно. ",
                "Вижу, что ситуация вас расстроила. ",
                "Понимаю ваше негодование. "
            ],
            'excited': [
                "Это невероятно! ",
                "Как интересно! ",
                "Восхитительно! ",
                "Захватывающе! "
            ],
            'neutral': [
                "Понятно. ",
                "Интересно. ",
                "Я вас слушаю. ",
                "Понимаю. "
            ]
        }
        
        # Выбор базового ответа
        base_responses = emotion_responses.get(emotion, emotion_responses['neutral'])
        base_response = random.choice(base_responses)
        
        # Персонализация на основе черт характера
        if persona_traits.get('friendly'):
            friendly_phrases = [
                "Хочу помочь вам в этом вопросе. ",
                "Всегда рад поддержать вас! ",
                "Давайте вместе разберемся. "
            ]
            base_response += random.choice(friendly_phrases)
        elif persona_traits.get('professional'):
            professional_phrases = [
                "С профессиональной точки зрения, это важно рассмотреть. ",
                "Анализируя ситуацию, можно сказать. ",
                "Исходя из лучших практик. "
            ]
            base_response += random.choice(professional_phrases)
        
        # Добавление контекстного ответа
        context_phrases = [
            f"Вы сказали: '{text}'",
            f"По поводу '{text}' - это интересно.",
            f"Ваше сообщение '{text}' получило ответ."
        ]
        base_response += random.choice(context_phrases)
        
        return base_response
    
    def get_system_info(self) -> Dict[str, Any]:
        """Получение информации о системе"""
        return {
            'initialized': self._initialized,
            'components': {
                'emotional_model': self.emotional_model is not None,
                'persona_manager': self.persona_manager is not None
            },
            'personas_count': len(self.persona_manager.list_personas()) if self.persona_manager else 0
        }