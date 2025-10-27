"""
Конфигурация системы логирования для проекта
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Кастомный форматтер с цветами для консоли"""
    
    COLORS = {
        'DEBUG': '\033[94m',     # Синий
        'INFO': '\033[92m',      # Зеленый
        'WARNING': '\033[93m',   # Желтый
        'ERROR': '\033[91m',     # Красный
        'CRITICAL': '\033[95m',  # Фиолетовый
        'RESET': '\033[0m'       # Сброс
    }
    
    def format(self, record):
        # Добавляем эмодзи в зависимости от уровня
        emoji_map = {
            'DEBUG': '🔍',
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CRITICAL': '💥'
        }
        
        record.emoji = emoji_map.get(record.levelname, '📝')
        
        # Форматируем сообщение
        log_message = super().format(record)
        
        # Добавляем цвет для консоли
        if sys.stdout.isatty():  # Только если это терминал
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            log_message = f"{color}{log_message}{self.COLORS['RESET']}"
        
        return log_message

def setup_logging():
    """Настройка системы логирования"""
    
    # Создание директории для логов
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Основной форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Цветной форматтер для консоли
    colored_formatter = ColoredFormatter(
        '%(asctime)s %(emoji)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Обработчик для файла (ротация по размеру)
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'ai_personality.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(colored_formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # Обработчик для ошибок (отдельный файл)
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'errors.log'),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Очистка существующих обработчиков
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Добавление обработчиков
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_handler)
    
    # Установка уровня логирования для внешних библиотек
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Логирование запуска системы
    startup_logger = logging.getLogger('startup')
    startup_logger.info("🚀 AI Personality Project - Система логирования инициализирована")
    startup_logger.info(f"📁 Логи сохраняются в: {os.path.abspath(log_dir)}")
    
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """Получение логгера с указанным именем"""
    return logging.getLogger(name)

def log_system_info():
    """Логирование системной информации"""
    logger = get_logger('system')
    
    logger.info("=== СИСТЕМНАЯ ИНФОРМАЦИЯ ===")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Платформа: {sys.platform}")
    logger.info(f"Рабочая директория: {os.getcwd()}")
    logger.info(f"Путь к Python: {sys.executable}")
    
    # Информация о памяти
    try:
        import psutil
        memory = psutil.virtual_memory()
        logger.info(f"Память: {memory.percent}% использовано ({memory.used // (1024**3)}GB/{memory.total // (1024**3)}GB)")
    except ImportError:
        logger.warning("psutil не установлен, информация о памяти недоступна")
    
    logger.info("=== КОНЕЦ СИСТЕМНОЙ ИНФОРМАЦИИ ===")

# Автоматическая настройка при импорте
setup_logging()
system_logger = get_logger('system')
log_system_info()