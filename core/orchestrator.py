"""
Оркестратор для управления взаимодействием между модулями AI системы
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from core.state_manager import state_manager
from core.exceptions import ModuleInitializationError, ModuleExecutionError
from database.session import get_db
from database import crud
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Главный координатор системы, управляющий взаимодействием между модулями
    """
    
    def __init__(self):
        self._modules = {}
        self._initialized = False
        self._state_manager = state_manager
        logger.info("Инициализация оркестратора")
    
    def initialize(self) -> bool:
        """
        Инициализация всех модулей системы
        
        Returns:
            bool: True если инициализация успешна
        """
        try:
            if self._initialized:
                return True
            
            logger.info("Запуск инициализации модулей")
            
            # Обновление состояния системы
            self._state_manager.set_state("system_status", "initializing")
            self._state_manager.set_state("active_modules", [])
            
            # TODO: Инициализация реальных модулей
            # Пока используем заглушки
            self._modules = {
                "core": {"status": "active"},
                "api": {"status": "active"}, 
                "database": {"status": "active"}
            }
            
            self._initialized = True
            self._state_manager.set_state("system_status", "ready")
            self._state_manager.set_state("active_modules", list(self._modules.keys()))
            
            logger.info("Оркестратор успешно инициализирован")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка инициализации оркестратора: {e}")
            self._state_manager.set_state("system_status", "error")
            raise ModuleInitializationError("orchestrator", str(e))
    
    async def process_message(self, 
                           message: str, 
                           user_id: Optional[str] = None,
                           session_id: Optional[str] = None,
                           db: Session = None) -> Dict[str, Any]:
        """
        Обработка входящего сообщения через все модули
        
        Args:
            message: Текст сообщения
            user_id: ID пользователя
            session_id: ID сессии
            db: Сессия базы данных
            
        Returns:
            Dict с результатом обработки
        """
        try:
            logger.info(f"Обработка сообщения: '{message}'")
            
            # Обновление состояния
            self._state_manager.record_interaction({
                "type": "message",
                "content": message,
                "user_id": user_id,
                "session_id": session_id
            })
            
            # Временная реализация до интеграции с реальными модулями
            response_data = {
                "response": self._generate_response(message),
                "mood": self._get_current_mood(),
                "memory_used": False,
                "session_id": session_id or f"session_{datetime.utcnow().timestamp()}"
            }
            
            # Сохранение взаимодействия в БД
            if db:
                try:
                    crud.crud_interaction.create(db, {
                        "user_id": user_id,
                        "session_id": response_data["session_id"],
                        "message": message,
                        "response": response_data["response"],
                        "mood": response_data["mood"],
                        "timestamp": datetime.utcnow()
                    })
                except Exception as e:
                    logger.warning(f"Не удалось сохранить взаимодействие в БД: {e}")
            
            logger.info("Сообщение успешно обработано")
            return response_data
            
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")
            raise ModuleExecutionError("orchestrator", "process_message", str(e))
    
    def _generate_response(self, message: str) -> str:
        """Генерация ответа на сообщение"""
        # Временная логика ответа
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["привет", "hello", "hi"]):
            return "Привет! Я антропоморфный AI. Как я могу помочь?"
        elif any(word in message_lower for word in ["как дела", "как ты"]):
            return "У меня всё отлично! Я только начинаю развиваться, но уже могу с вами общаться."
        elif any(word in message_lower for word in ["пока", "bye", "до свидания"]):
            return "До свидания! Было приятно пообщаться."
        else:
            return f"Вы сказали: '{message}'. Я всё запоминаю и учусь на нашем общении. Система находится в стадии активной разработки."
    
    def _get_current_mood(self) -> str:
        """Получение текущего настроения системы"""
        # Временная реализация
        moods = ["neutral", "happy", "calm", "friendly"]
        return self._state_manager.get_state("current_mood", "neutral")
    
    async def store_memory(self, 
                         content: str, 
                         memory_type: str = "fact",
                         importance: float = 1.0,
                         db: Session = None) -> str:
        """
        Сохранение информации в память
        
        Args:
            content: Содержимое для сохранения
            memory_type: Тип памяти
            importance: Важность информации
            db: Сессия базы данных
            
        Returns:
            ID сохраненной памяти
        """
        try:
            logger.info(f"Сохранение в память: {content[:50]}...")
            
            # Временная реализация
            memory_id = f"memory_{datetime.utcnow().timestamp()}"
            
            if db:
                try:
                    crud.crud_memory.create(db, {
                        "content": content,
                        "memory_type": memory_type,
                        "importance": importance,
                        "timestamp": datetime.utcnow()
                    })
                except Exception as e:
                    logger.warning(f"Не удалось сохранить память в БД: {e}")
            
            return memory_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения памяти: {e}")
            raise ModuleExecutionError("orchestrator", "store_memory", str(e))
    
    async def recall_memory(self, 
                          query: str, 
                          memory_type: Optional[str] = None,
                          limit: int = 10,
                          db: Session = None) -> List[Dict[str, Any]]:
        """
        Поиск информации в памяти
        
        Args:
            query: Запрос для поиска
            memory_type: Тип памяти для фильтрации
            limit: Лимит результатов
            db: Сессия базы данных
            
        Returns:
            Список найденных воспоминаний
        """
        try:
            logger.info(f"Поиск в памяти: '{query}'")
            
            # Временная реализация
            memories = []
            
            if db:
                try:
                    db_memories = crud.crud_memory.search(db, query, memory_type, limit)
                    memories = [
                        {
                            "id": str(mem.id),
                            "content": mem.content,
                            "memory_type": mem.memory_type,
                            "timestamp": mem.timestamp.isoformat()
                        }
                        for mem in db_memories
                    ]
                except Exception as e:
                    logger.warning(f"Не удалось выполнить поиск в БД: {e}")
            
            return memories
            
        except Exception as e:
            logger.error(f"Ошибка поиска в памяти: {e}")
            raise ModuleExecutionError("orchestrator", "recall_memory", str(e))
    
    async def update_mood(self, mood: str, intensity: float = 1.0, reason: Optional[str] = None):
        """
        Обновление настроения системы
        
        Args:
            mood: Новое настроение
            intensity: Интенсивность настроения
            reason: Причина изменения
        """
        try:
            logger.info(f"Обновление настроения: {mood} (интенсивность: {intensity})")
            
            self._state_manager.set_state("current_mood", mood)
            
            # Сохранение в историю настроений
            mood_data = {
                "mood": mood,
                "intensity": intensity,
                "reason": reason,
                "timestamp": datetime.utcnow()
            }
            self._state_manager.set_state("mood_history", 
                                        self._state_manager.get_state("mood_history", []) + [mood_data])
            
        except Exception as e:
            logger.error(f"Ошибка обновления настроения: {e}")
            raise ModuleExecutionError("orchestrator", "update_mood", str(e))
    
    async def update_personality_trait(self, trait: str, value: float):
        """
        Обновление черты личности
        
        Args:
            trait: Черта личности
            value: Новое значение
        """
        try:
            logger.info(f"Обновление черты личности: {trait} = {value}")
            
            personality = self._state_manager.get_state("personality", {})
            personality[trait] = value
            self._state_manager.set_state("personality", personality)
            
        except Exception as e:
            logger.error(f"Ошибка обновления личности: {e}")
            raise ModuleExecutionError("orchestrator", "update_personality_trait", str(e))
    
    def get_system_state(self) -> Dict[str, Any]:
        """
        Получение текущего состояния системы
        
        Returns:
            Словарь с состоянием системы
        """
        return {
            "status": self._state_manager.get_state("system_status", "unknown"),
            "mood": self._state_manager.get_state("current_mood", "neutral"),
            "active_modules": self._state_manager.get_state("active_modules", []),
            "last_interaction": self._state_manager.get_state("last_interaction", {}).get("timestamp"),
            "system_health": "healthy" if self._initialized else "initializing"
        }
    
    def get_active_modules(self) -> List[str]:
        """
        Получение списка активных модулей
        
        Returns:
            Список имен активных модулей
        """
        return list(self._modules.keys())
    
    def is_initialized(self) -> bool:
        """Проверка инициализации оркестратора"""
        return self._initialized
    
    def shutdown(self):
        """Завершение работы оркестратора"""
        logger.info("Завершение работы оркестратора")
        self._initialized = False
        self._state_manager.set_state("system_status", "shutdown")