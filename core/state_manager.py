from typing import Dict, Any, Optional
import threading
from datetime import datetime
import json
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class SystemStatus(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class StateManager:
    """
    Менеджер состояния системы для управления глобальным состоянием AI
    """
    
    def __init__(self):
        self._state = {
            "system_status": SystemStatus.INITIALIZING,
            "mood": "neutral",
            "active_modules": [],
            "last_interaction": None,
            "system_health": "unknown",
            "startup_time": datetime.utcnow().isoformat(),
            "module_states": {},
            "performance_metrics": {},
            "error_count": 0
        }
        self._lock = threading.RLock()
        self._listeners = []
    
    def set_state(self, key: str, value: Any) -> None:
        """
        Установка значения состояния
        
        Args:
            key: Ключ состояния
            value: Значение состояния
        """
        with self._lock:
            old_value = self._state.get(key)
            self._state[key] = value
            self._notify_listeners(key, old_value, value)
            logger.debug(f"State updated: {key} = {value}")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Получение значения состояния
        
        Args:
            key: Ключ состояния
            default: Значение по умолчанию
            
        Returns:
            Значение состояния или default
        """
        with self._lock:
            return self._state.get(key, default)
    
    def update_state(self, updates: Dict[str, Any]) -> None:
        """
        Массовое обновление состояния
        
        Args:
            updates: Словарь обновлений состояния
        """
        with self._lock:
            for key, value in updates.items():
                old_value = self._state.get(key)
                self._state[key] = value
                self._notify_listeners(key, old_value, value)
            logger.debug(f"State updated with {len(updates)} changes")
    
    def get_full_state(self) -> Dict[str, Any]:
        """
        Получение полного состояния системы
        
        Returns:
            Полное состояние системы
        """
        with self._lock:
            return self._state.copy()
    
    def add_module_state(self, module_name: str, state: Dict[str, Any]) -> None:
        """
        Добавление состояния модуля
        
        Args:
            module_name: Имя модуля
            state: Состояние модуля
        """
        with self._lock:
            if "module_states" not in self._state:
                self._state["module_states"] = {}
            self._state["module_states"][module_name] = state
            logger.debug(f"Module state updated: {module_name}")
    
    def get_module_state(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        Получение состояния модуля
        
        Args:
            module_name: Имя модуля
            
        Returns:
            Состояние модуля или None
        """
        with self._lock:
            return self._state.get("module_states", {}).get(module_name)
    
    def record_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """
        Запись взаимодействия с системой
        
        Args:
            interaction_data: Данные взаимодействия
        """
        with self._lock:
            self._state["last_interaction"] = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": interaction_data
            }
    
    def update_performance_metric(self, metric_name: str, value: float) -> None:
        """
        Обновление метрики производительности
        
        Args:
            metric_name: Имя метрики
            value: Значение метрики
        """
        with self._lock:
            if "performance_metrics" not in self._state:
                self._state["performance_metrics"] = {}
            self._state["performance_metrics"][metric_name] = value
    
    def increment_error_count(self) -> None:
        """Увеличение счетчика ошибок"""
        with self._lock:
            self._state["error_count"] = self._state.get("error_count", 0) + 1
    
    def reset_error_count(self) -> None:
        """Сброс счетчика ошибок"""
        with self._lock:
            self._state["error_count"] = 0
    
    def add_listener(self, listener) -> None:
        """
        Добавление слушателя изменений состояния
        
        Args:
            listener: Функция-слушатель (key, old_value, new_value)
        """
        with self._lock:
            self._listeners.append(listener)
    
    def remove_listener(self, listener) -> None:
        """
        Удаление слушателя изменений состояния
        
        Args:
            listener: Функция-слушатель для удаления
        """
        with self._lock:
            if listener in self._listeners:
                self._listeners.remove(listener)
    
    def _notify_listeners(self, key: str, old_value: Any, new_value: Any) -> None:
        """
        Уведомление слушателей об изменении состояния
        
        Args:
            key: Ключ состояния
            old_value: Старое значение
            new_value: Новое значение
        """
        for listener in self._listeners:
            try:
                listener(key, old_value, new_value)
            except Exception as e:
                logger.error(f"Error in state listener: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование состояния в словарь
        
        Returns:
            Словарь состояния
        """
        with self._lock:
            return self._state.copy()
    
    def from_dict(self, state_dict: Dict[str, Any]) -> None:
        """
        Восстановление состояния из словаря
        
        Args:
            state_dict: Словарь состояния
        """
        with self._lock:
            self._state.update(state_dict)
            logger.info("State restored from dictionary")
    
    def __str__(self) -> str:
        """Строковое представление состояния"""
        with self._lock:
            return json.dumps(self._state, indent=2, default=str)

# Глобальный экземпляр менеджера состояния
state_manager = StateManager()