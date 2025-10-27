"""
Конфигурация подключения к базе данных
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

def get_database_url():
    """Получение URL базы данных из переменных окружения"""
    # Приоритет: DATABASE_URL -> DEV_DATABASE_URL -> SQLite по умолчанию
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        database_url = os.getenv('DEV_DATABASE_URL', 'sqlite:///personality.db')
        logger.info("⚠️ Используется база данных для разработки")
    
    # Для SQLite добавляем параметры для лучшей производительности
    if database_url.startswith('sqlite'):
        database_url += "?check_same_thread=False"
    
    logger.info(f"🔗 URL базы данных: {database_url.split('://')[0]}://...")
    return database_url

# Создание движка базы данных
DATABASE_URL = get_database_url()

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Включать для отладки SQL запросов
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_recycle=300,  # Переподключение каждые 5 минут
    )
    
    # Создание фабрики сессий
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Базовый класс для моделей
    Base = declarative_base()
    
    logger.info("✅ Конфигурация базы данных успешно загружена")
    
except Exception as e:
    logger.error(f"❌ Ошибка конфигурации базы данных: {e}")
    raise

def get_db():
    """
    Dependency для получения сессии базы данных.
    Использование:
        db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создание всех таблиц в базе данных"""
    try:
        # Импорт моделей для создания таблиц
        from ai_personality_project.database.models import Persona, Interaction
        
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Таблицы базы данных созданы/проверены")
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания таблиц: {e}")
        raise

def test_connection():
    """Тестирование подключения к базе данных"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ Подключение к базе данных успешно")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")
        return False