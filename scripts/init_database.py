#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""

import sys
import os
import logging
from pathlib import Path

# Добавление корневой директории в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.session import init_db, engine
from database.models import Base
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Инициализация базы данных"""
    try:
        logger.info("Начало инициализации базы данных...")
        logger.info(f"Database URL: {settings.DATABASE_URL}")
        
        # Создание всех таблиц
        init_db()
        
        logger.info("✓ База данных успешно инициализирована")
        
        # Проверка подключения
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("✓ Подключение к базе данных успешно")
            
        return True
        
    except Exception as e:
        logger.error(f"✗ Ошибка инициализации базы данных: {e}")
        return False

def check_database_connection():
    """Проверка подключения к базе данных"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✓ Подключение к базе данных активно")
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка подключения к базе данных: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    if initialize_database():
        print("✓ База данных готова к работе")
        sys.exit(0)
    else:
        print("✗ Ошибка инициализации базы данных")
        sys.exit(1)