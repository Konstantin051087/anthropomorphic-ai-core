"""
Middleware для FastAPI приложения
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования запросов
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Логирование входящего запроса
        logger.info(f"Входящий запрос: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Логирование ответа
        process_time = time.time() - start_time
        logger.info(
            f"Ответ: {request.method} {request.url} "
            f"- Статус: {response.status_code} "
            f"- Время: {process_time:.3f}с"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response