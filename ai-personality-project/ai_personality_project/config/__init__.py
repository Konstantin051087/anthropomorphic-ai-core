"""
Конфигурация приложения
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки AI
    AI_MODEL_TIMEOUT = int(os.getenv('AI_MODEL_TIMEOUT', '30'))
    ENABLE_ML_FEATURES = os.getenv('ENABLE_ML_FEATURES', 'true').lower() == 'true'
    
    # Настройки безопасности
    MAX_REQUEST_SIZE = int(os.getenv('MAX_REQUEST_SIZE', '1048576'))  # 1MB
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    
    # Настройки логирования
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev_personality.db')
    
    # Дополнительные настройки для разработки
    AI_MODEL_TIMEOUT = 60  # Больше времени для отладки
    ENABLE_DEBUG_ENDPOINTS = True

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///personality.db')
    
    # Оптимизации для продакшена
    AI_MODEL_TIMEOUT = 10
    ENABLE_DEBUG_ENDPOINTS = False

class TestingConfig(Config):
    """Конфигурация для тестирования"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///test_personality.db')
    
    # Настройки для тестов
    AI_MODEL_TIMEOUT = 5
    ENABLE_ML_FEATURES = False

# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Получение конфигурации по имени"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])