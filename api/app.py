from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from core.config import settings, config_manager
from utils.logger import setup_logging, get_logger
from api.routes import router as router
from api.middleware import LoggingMiddleware
from database.session import init_db, close_db_connection

# Настройка логирования до создания приложения
try:
    setup_logging()
except Exception as e:
    print(f"⚠ Ошибка настройки логирования: {e}")
    # Базовая настройка логирования как fallback
    logging.basicConfig(level=logging.INFO)
    print("✓ Базовое логирование настроено")

logger = get_logger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    logger.info(f"Запуск {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Режим: {settings.RENDER_ENV}")
    logger.info(f"DEBUG: {settings.DEBUG}")
    
    try:
        # Инициализация базы данных
        from scripts.init_database import initialize_database
        if initialize_database():
            logger.info("✓ База данных инициализирована")
        else:
            logger.error("✗ Не удалось инициализировать базу данных")
    except Exception as e:
        logger.error(f"✗ Ошибка инициализации базы данных: {e}")
    
    yield
    
    # Shutdown
    logger.info("Завершение работы приложения...")
    try:
        close_db_connection()
        logger.info("✓ Соединение с базой данных закрыто")
    except Exception as e:
        logger.error(f"✗ Ошибка при закрытии соединения с БД: {e}")

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

# Добавление middleware логирования
app.add_middleware(LoggingMiddleware)

# Глобальный обработчик исключений
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений"""
    logger.error(f"Необработанное исключение: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Внутренняя ошибка сервера",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик HTTP исключений"""
    logger.warning(f"HTTP исключение: {exc.detail} (код: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": "HTTP_ERROR"
        }
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

if __name__ == "__main__":
    # Запуск сервера при прямом выполнении файла
    logger.info(f"Запуск сервера на {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        "api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info"
    )