"""
Зависимости для FastAPI endpoints
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.orchestrator import Orchestrator
from database.session import get_db
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Глобальный экземпляр оркестратора
_orchestrator_instance = None

def get_orchestrator() -> Orchestrator:
    """
    Dependency для получения экземпляра оркестратора
    
    Returns:
        Экземпляр Orchestrator
    """
    global _orchestrator_instance
    
    if _orchestrator_instance is None:
        logger.info("Создание нового экземпляра оркестратора")
        _orchestrator_instance = Orchestrator()
        
        # Инициализация оркестратора
        try:
            if not _orchestrator_instance.initialize():
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось инициализировать систему"
                )
        except Exception as e:
            logger.error(f"Ошибка инициализации оркестратора: {e}")
            _orchestrator_instance = None
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка инициализации системы: {str(e)}"
            )
    
    return _orchestrator_instance

def get_db_session() -> Session:
    """
    Dependency для получения сессии базы данных
    
    Returns:
        Сессия базы данных
    """
    return next(get_db())

def verify_api_key():
    """
    Dependency для проверки API ключа (заглушка для будущей реализации)
    
    Raises:
        HTTPException: Если ключ неверный
    """
    # TODO: Реализовать настоящую аутентификацию
    return True

# Dependency для проверки здоровья системы
def health_check_dependency(orchestrator: Orchestrator = Depends(get_orchestrator)):
    """
    Dependency для проверки что система готова к работе
    
    Raises:
        HTTPException: Если система не готова
    """
    if not orchestrator.is_initialized():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Система не инициализирована"
        )
    return True