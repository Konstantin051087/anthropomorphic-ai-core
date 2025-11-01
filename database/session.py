# database/session.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings
import logging

logger = logging.getLogger(__name__)

from database.models import Base

# Создание движка БД
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency для получения сессии БД
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """
    Инициализация базы данных - создание таблиц
    """
    try:
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def close_db_connection():
    """
    Закрытие соединения с БД
    """
    try:
        engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")