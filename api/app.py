import sys
import os
from pathlib import Path

# Добавляем корневую директорию в Python path
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

# Безопасные импорты с fallback
try:
    from core.config import settings, config_manager
except ImportError as e:
    print(f"⚠ Ошибка импорта core.config: {e}")
    # Fallback настройки
    class Settings:
        PROJECT_NAME = "Anthropomorphic AI"
        VERSION = "1.0.0"
        DEBUG = True
        RENDER_ENV = "development"
        CORS_ORIGINS = ["*"]
        API_HOST = "0.0.0.0"
        API_PORT = 8000
        API_RELOAD = True
    
    settings = Settings()
    config_manager = Settings()

try:
    from utils.logger import setup_logging, get_logger
    setup_logging()
except ImportError as e:
    print(f"⚠ Ошибка настройки логирования: {e}")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger("app")

# Безопасный импорт роутера
try:
    from api.routes import router
except ImportError as e:
    print(f"⚠ Ошибка импорта routes: {e}")
    from fastapi import APIRouter
    router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    logger.info(f"Запуск {settings.PROJECT_NAME} v{settings.VERSION}")
    
    try:
        # Безопасная инициализация базы данных
        from scripts.init_database import initialize_database
        if initialize_database():
            logger.info("✓ База данных инициализирована")
        else:
            logger.warning("⚠ База данных не инициализирована (возможно, временная реализация)")
    except Exception as e:
        logger.warning(f"⚠ Ошибка инициализации базы данных: {e}")
    
    yield
    
    # Shutdown
    logger.info("Завершение работы приложения...")

# Создание приложения FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Anthropomorphic AI Core API - система с антропоморфными характеристиками",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(router, prefix="/api/v1", tags=["api"])

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": f"Добро пожаловать в {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "operational",
        "environment": settings.RENDER_ENV,
        "docs": "/docs" if settings.DEBUG else "disabled in production"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.RENDER_ENV
    }

@app.get("/test-imports")
async def test_imports():
    """Тестовый endpoint для проверки импортов"""
    imports_status = {}
    
    try:
        from core.orchestrator import Orchestrator
        imports_status['core.orchestrator'] = '✅'
    except ImportError as e:
        imports_status['core.orchestrator'] = f'❌ {e}'
    
    try:
        from modules.psyche.consciousness import Consciousness
        imports_status['modules.psyche'] = '✅'
    except ImportError as e:
        imports_status['modules.psyche'] = f'❌ {e}'
    
    return {
        "imports_status": imports_status,
        "python_path": sys.path,
        "current_directory": str(Path.cwd())
    }

if __name__ == "__main__":
    # Запуск сервера при прямом выполнении файла
    logger.info(f"Запуск сервера на {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info"
    )