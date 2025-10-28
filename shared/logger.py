import logging
import sys
import os
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.created
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

def setup_logger(name=__name__, log_level=None):
    """Настройка структурированного логирования"""
    logger = logging.getLogger(name)
    
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очистка существующих обработчиков
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Создание JSON форматера
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s %(module)s %(funcName)s'
    )
    
    # Обработчик для stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Отключение propagation для корневого логгера
    logger.propagate = False
    
    return logger

def get_logger(name):
    """Получить настроенный логгер"""
    return logging.getLogger(name)

# Инициализация корневого логгера
root_logger = setup_logger('emotional-ai')