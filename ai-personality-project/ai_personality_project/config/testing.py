"""
Конфигурация для тестирования
"""

import os

class TestingConfig:
    # Основные настройки
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'test-secret-key'
    
    # База данных
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///test_personality.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Отключение CSRF для тестирования
    WTF_CSRF_ENABLED = False
    
    # Настройки AI для тестирования
    AI_MODEL_TIMEOUT = 2
    ENABLE_ML_FEATURES = False
    
    # Логирование
    LOG_LEVEL = 'DEBUG'
    LOG_TO_FILE = False
    
    # Безопасность
    MAX_REQUEST_SIZE = 1024 * 1024  # 1MB
    RATE_LIMIT_ENABLED = False
    
    # Тестовые данные
    TEST_PERSONAS = [
        {
            'id': 1,
            'name': 'Тестовый помощник',
            'personality_traits': {'friendly': True, 'helpful': True}
        }
    ]