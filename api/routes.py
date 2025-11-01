from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
import sys

from api.models import (
    ChatRequest, 
    ChatResponse, 
    SystemState,
    MemoryStoreRequest,
    MemoryRecallRequest,
    MoodUpdateRequest,
    PersonalityUpdateRequest,
    ErrorResponse
)
from core.orchestrator import Orchestrator
from core.config import settings
from core.state_manager import StateManager
from database.session import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Глобальный экземпляр оркестратора и менеджера состояния
_orchestrator = None
_state_manager = None

def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        try:
            _orchestrator = Orchestrator()
        except Exception as e:
            logger.error(f"Ошибка инициализации Orchestrator: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Система временно недоступна"
            )
    return _orchestrator

def get_state_manager():
    global _state_manager
    if _state_manager is None:
        try:
            _state_manager = StateManager()
        except Exception as e:
            logger.error(f"Ошибка инициализации StateManager: {str(e)}")
    return _state_manager

# Основные эндпоинты API
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Сообщение не может быть пустым"
            )
        
        session_id = request.session_id or str(uuid.uuid4())
        orchestrator = get_orchestrator()
        
        response_data = await orchestrator.process_chat(
            message=request.message,
            user_id=request.user_id,
            session_id=session_id,
            db=db
        )
        
        return ChatResponse(
            response=response_data.get("response", "Ответ не сгенерирован"),
            mood=response_data.get("mood", "neutral"),
            memory_used=response_data.get("memory_used", False),
            session_id=response_data.get("session_id", session_id),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Непредвиденная ошибка обработки сообщения: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )

@router.get("/state", response_model=SystemState)
async def get_system_state():
    try:
        state_manager = get_state_manager()
        orchestrator = get_orchestrator()
        
        state = None
        if state_manager:
            try:
                state = state_manager.get_current_state()
            except Exception as e:
                logger.warning(f"StateManager недоступен: {e}")
        
        if not state:
            try:
                state = await orchestrator.get_system_state()
            except Exception as e:
                logger.warning(f"Orchestrator.get_system_state недоступен: {e}")
                state = {
                    "status": "operational",
                    "mood": "neutral",
                    "active_modules": ["api", "core"],
                    "last_interaction": datetime.utcnow().isoformat(),
                    "system_health": "healthy"
                }
        
        return SystemState(
            status=state.get("status", "unknown"),
            mood=state.get("mood", "neutral"),
            active_modules=state.get("active_modules", []),
            last_interaction=state.get("last_interaction"),
            system_health=state.get("system_health", "unknown"),
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Ошибка получения состояния: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения состояния: {str(e)}"
        )

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        try:
            db.execute("SELECT 1")
            database_status = "connected"
        except Exception as e:
            logger.error(f"Ошибка подключения к БД: {e}")
            database_status = f"disconnected: {str(e)}"

        modules_status = {}
        try:
            orchestrator = get_orchestrator()
            modules_status["orchestrator"] = "healthy"
        except Exception as e:
            modules_status["orchestrator"] = f"unhealthy: {str(e)}"

        try:
            state_manager = get_state_manager()
            modules_status["state_manager"] = "healthy" if state_manager else "uninitialized"
        except Exception as e:
            modules_status["state_manager"] = f"unhealthy: {str(e)}"

        overall_status = "healthy" if database_status == "connected" else "degraded"

        return {
            "status": overall_status,
            "database": database_status,
            "modules": modules_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": getattr(settings, "VERSION", "1.0.0")
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {str(e)}"
        )

@router.post("/memory/store")
async def store_memory(request: MemoryStoreRequest, db: Session = Depends(get_db)):
    try:
        if not request.content or not request.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Содержимое памяти не может быть пустым"
            )

        orchestrator = get_orchestrator()
        memory_id = await orchestrator.store_memory(
            content=request.content,
            memory_type=request.memory_type,
            metadata=request.metadata,
            db=db
        )

        return {
            "status": "success", 
            "memory_id": memory_id,
            "message": "Память успешно сохранена"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка сохранения памяти: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сохранения памяти: {str(e)}"
        )

@router.post("/memory/recall")
async def recall_memory(request: MemoryRecallRequest, db: Session = Depends(get_db)):
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Запрос не может быть пустым"
            )

        orchestrator = get_orchestrator()
        memories = await orchestrator.recall_memory(
            query=request.query,
            memory_type=request.memory_type,
            limit=request.limit,
            db=db
        )

        return {"memories": memories[:request.limit]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка поиска в памяти: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка поиска в памяти: {str(e)}"
        )

@router.post("/mood/update")
async def update_mood(request: MoodUpdateRequest):
    try:
        if not request.mood:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Настроение не может быть пустым"
            )

        valid_moods = ["happy", "sad", "angry", "neutral", "excited", "calm"]
        if request.mood not in valid_moods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Недопустимое настроение. Допустимые значения: {', '.join(valid_moods)}"
            )

        orchestrator = get_orchestrator()
        result = await orchestrator.update_mood(
            mood=request.mood,
            intensity=request.intensity,
            reason=request.reason
        )

        return {
            "status": result.get("status", "success"),
            "mood": result.get("mood", request.mood),
            "intensity": result.get("intensity", request.intensity),
            "message": "Настроение успешно обновлено"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления настроения: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления настроения: {str(e)}"
        )

@router.post("/personality/update")
async def update_personality(request: PersonalityUpdateRequest):
    try:
        if not request.trait:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Черта личности не может быть пустой"
            )

        if request.value is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Значение черты личности не может быть пустым"
            )

        orchestrator = get_orchestrator()
        result = await orchestrator.update_personality(
            trait=request.trait,
            value=request.value,
            reason=request.reason
        )

        return {
            "status": result.get("status", "success"),
            "trait": result.get("trait", request.trait),
            "value": result.get("value", request.value),
            "message": "Черта личности успешно обновлена"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления личности: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления личности: {str(e)}"
        )

@router.get("/modules")
async def list_modules():
    try:
        orchestrator = get_orchestrator()
        modules_data = await orchestrator.get_active_modules()

        return {
            "modules": modules_data.get("modules", []),
            "status": modules_data.get("status", "unknown"),
            "total_modules": len(modules_data.get("modules", [])),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Ошибка получения модулей: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения модулей: {str(e)}"
        )

@router.get("/")
async def root():
    try:
        state_manager = get_state_manager()
        system_info = {}
        if state_manager:
            try:
                system_info = state_manager.get_system_info()
            except Exception:
                system_info = {}
    except Exception:
        system_info = {}

    return {
        "message": "Anthropomorphic AI Core API",
        "version": getattr(settings, "VERSION", "1.0.0"),
        "status": system_info.get("status", "operational"),
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "chat": "/chat (POST)",
            "state": "/state (GET)", 
            "health": "/health (GET)",
            "memory_store": "/memory/store (POST)",
            "memory_recall": "/memory/recall (POST)",
            "mood_update": "/mood/update (POST)",
            "personality_update": "/personality/update (POST)",
            "modules": "/modules (GET)"
        },
        "documentation": "/docs",
        "openapi_spec": "/openapi.json"
    }

@router.get("/system/info")
async def system_info():
    try:
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        modules_info = {}
        try:
            import importlib.metadata
            for package in ["fastapi", "uvicorn", "sqlalchemy", "pydantic"]:
                try:
                    version = importlib.metadata.version(package)
                    modules_info[package] = version
                except importlib.metadata.PackageNotFoundError:
                    modules_info[package] = "not installed"
        except Exception as e:
            modules_info["error"] = str(e)

        return {
            "system": {
                "python_version": python_version,
                "platform": sys.platform,
                "api_version": getattr(settings, "VERSION", "1.0.0")
            },
            "modules": modules_info,
            "environment": getattr(settings, "ENVIRONMENT", "development"),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Ошибка получения информации о системе: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения информации о системе: {str(e)}"
        )