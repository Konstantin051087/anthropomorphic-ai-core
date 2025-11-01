import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from core.config import settings


def setup_logging():
    """Настройка логирования для приложения"""
    
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    log_file = Path(settings.LOG_FILE)
    
    # Создание директории для логов если нужно
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    
    # Обработчик для файла с ротацией
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Основной логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Очистка старых обработчиков
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Добавление обработчиков
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Установка уровня логирования для внешних логгеров
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    
    # В продакшн режиме уменьшаем логирование некоторых библиотек
    if settings.RENDER_ENV == "production":
        logging.getLogger('transformers').setLevel(logging.WARNING)
        logging.getLogger('torch').setLevel(logging.WARNING)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('httpcore').setLevel(logging.WARNING)
    
    # Настройка логирования для нашего приложения
    app_logger = logging.getLogger('anthropomorphic_ai')
    app_logger.setLevel(log_level)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Логирование инициализировано. Уровень: {settings.LOG_LEVEL}")
    logger.info(f"Файл логов: {log_file.absolute()}")
    logger.info(f"Режим: {settings.RENDER_ENV}")


def get_logger(name: str) -> logging.Logger:
    """
    Получение логгера с указанным именем
    
    Args:
        name: Имя логгера
        
    Returns:
        Объект логгера
    """
    return logging.getLogger(f"anthropomorphic_ai.{name}")


class LoggingMiddleware:
    """Middleware для логирования HTTP запросов"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("api")
    
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            await self.log_request(scope)
        
        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                await self.log_response(scope, message)
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
    
    async def log_request(self, scope):
        """Логирование входящего запроса"""
        method = scope.get('method', 'UNKNOWN')
        path = scope.get('path', 'UNKNOWN')
        self.logger.info(f"Входящий запрос: {method} {path}")
    
    async def log_response(self, scope, message):
        """Логирование исходящего ответа"""
        method = scope.get('method', 'UNKNOWN')
        path = scope.get('path', 'UNKNOWN')
        status_code = message.get('status', 0)
        self.logger.info(f"Ответ: {method} {path} -> {status_code}")