"""
Конфигурация для тестирования базы данных
"""

import os
import tempfile
import pytest
from ai_personality_project.database.db_config import Base, engine, SessionLocal, get_db

@pytest.fixture
def test_database():
    """Фикстура для тестовой базы данных"""
    # Создание временной базы данных в памяти
    TEST_DATABASE_URL = "sqlite:///:memory:"
    
    # Создание движка для тестов
    test_engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
    
    # Создание всех таблиц
    Base.metadata.create_all(bind=test_engine)
    
    # Создание сессии для тестов
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    return test_engine, TestingSessionLocal, override_get_db

def init_test_data(session):
    """Инициализация тестовых данных"""
    from ai_personality_project.database.models import Persona
    
    # Создание тестовых персонажей
    test_personas = [
        Persona(
            name="Тестовый помощник",
            description="Персонаж для тестирования",
            personality_traits={"friendly": True, "helpful": True},
            emotional_state={"current_mood": "neutral"}
        ),
        Persona(
            name="Тестовый советник", 
            description="Еще один тестовый персонаж",
            personality_traits={"professional": True, "analytical": True},
            emotional_state={"current_mood": "calm"}
        )
    ]
    
    for persona in test_personas:
        session.add(persona)
    
    session.commit()

class TestDatabaseConfig:
    """Конфигурация базы данных для тестов"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @classmethod
    def setup_test_database(cls):
        """Настройка тестовой базы данных"""
        from ai_personality_project.database.db_config import create_tables
        create_tables()
        
        # Инициализация тестовых данных
        from ai_personality_project.database.db_config import get_db
        db = next(get_db())
        init_test_data(db)
    
    @classmethod
    def teardown_test_database(cls):
        """Очистка тестовой базы данных"""
        from ai_personality_project.database.db_config import Base, engine
        Base.metadata.drop_all(bind=engine)