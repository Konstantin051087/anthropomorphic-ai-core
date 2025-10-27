"""
Базовый менеджер персонажей
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class PersonaManager:
    def __init__(self):
        self._initialized = False
        self.personas = {}
        
    def initialize(self):
        """Инициализация менеджера персонажей"""
        try:
            logger.info("🔄 Инициализация PersonaManager...")
            
            self._load_default_personas()
            self._initialized = True
            
            logger.info(f"✅ PersonaManager инициализирован, загружено {len(self.personas)} персонажей")
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации PersonaManager: {e}")
            raise
    
    def _load_default_personas(self):
        """Загрузка персонажей по умолчанию"""
        self.personas = {
            1: {
                'id': 1,
                'name': 'Дружелюбный помощник',
                'description': 'Теплый и поддерживающий собеседник',
                'personality_traits': {
                    'friendly': True,
                    'helpful': True,
                    'patient': True,
                    'empathetic': True,
                    'optimistic': True
                },
                'communication_style': {
                    'formal': False,
                    'warm': True,
                    'supportive': True,
                    'encouraging': True
                },
                'emotional_state': {
                    'current_mood': 'neutral',
                    'emotional_history': [],
                    'mood_stability': 0.7
                },
                'created_at': '2024-01-01',
                'is_active': True
            },
            2: {
                'id': 2,
                'name': 'Профессиональный советник',
                'description': 'Экспертный и аналитический собеседник',
                'personality_traits': {
                    'professional': True,
                    'analytical': True,
                    'precise': True,
                    'formal': True,
                    'knowledgeable': True
                },
                'communication_style': {
                    'formal': True,
                    'structured': True,
                    'detailed': True,
                    'objective': True
                },
                'emotional_state': {
                    'current_mood': 'calm',
                    'emotional_history': [],
                    'mood_stability': 0.9
                },
                'created_at': '2024-01-01',
                'is_active': True
            }
        }
    
    def get_persona(self, persona_id: int) -> Optional[Dict[str, Any]]:
        """Получение персонажа по ID"""
        if not self._initialized:
            self.initialize()
            
        persona = self.personas.get(persona_id)
        
        if not persona:
            logger.warning(f"⚠️ Персонаж с ID {persona_id} не найден")
            return None
            
        logger.debug(f"📋 Получен персонаж: {persona['name']} (ID: {persona_id})")
        return persona
    
    def list_personas(self) -> List[Dict[str, Any]]:
        """Получение списка всех персонажей"""
        if not self._initialized:
            self.initialize()
            
        personas_list = list(self.personas.values())
        logger.debug(f"📊 Получено {len(personas_list)} персонажей")
        return personas_list
    
    def create_persona(self, name: str, personality_traits: Dict, 
                      description: str = "", communication_style: Dict = None) -> Optional[Dict]:
        """Создание нового персонажа"""
        try:
            if not self._initialized:
                self.initialize()
            
            new_id = max(self.personas.keys()) + 1 if self.personas else 1
            
            new_persona = {
                'id': new_id,
                'name': name,
                'description': description or f"Персонаж {name}",
                'personality_traits': personality_traits,
                'communication_style': communication_style or {},
                'emotional_state': {
                    'current_mood': 'neutral',
                    'emotional_history': [],
                    'mood_stability': 0.5
                },
                'created_at': '2024-01-01',  # В реальном приложении здесь будет текущая дата
                'is_active': True
            }
            
            self.personas[new_id] = new_persona
            logger.info(f"✅ Создан новый персонаж: {name} (ID: {new_id})")
            
            return new_persona
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания персонажа: {e}")
            return None
    
    def update_persona_emotion(self, persona_id: int, emotional_state: Dict) -> bool:
        """Обновление эмоционального состояния персонажа"""
        try:
            persona = self.get_persona(persona_id)
            if persona:
                persona['emotional_state'] = emotional_state
                logger.debug(f"🎭 Обновлено эмоциональное состояние персонажа {persona_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка обновления эмоций персонажа: {e}")
            return False
    
    def get_persona_stats(self) -> Dict[str, Any]:
        """Получение статистики по персонажам"""
        if not self._initialized:
            self.initialize()
            
        active_personas = [p for p in self.personas.values() if p.get('is_active', True)]
        
        return {
            'total_personas': len(self.personas),
            'active_personas': len(active_personas),
            'persona_names': [p['name'] for p in active_personas],
            'average_traits_per_persona': sum(len(p['personality_traits']) for p in active_personas) / len(active_personas)
        }