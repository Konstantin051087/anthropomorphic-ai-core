"""
Тесты для API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.app import app
from database.session import get_db
from database.models import Base

# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Переопределение зависимости базы данных для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAPIEndpoints:
    """Тесты для API endpoints"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        # Создание таблиц
        Base.metadata.create_all(bind=engine)
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        # Удаление таблиц
        Base.metadata.drop_all(bind=engine)
    
    def test_root_endpoint(self):
        """Тест корневого endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_health_endpoint(self):
        """Тест health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_api_v1_root(self):
        """Тест корневого endpoint API v1"""
        response = client.get("/api/v1/")
        assert response.status_code == 200
    
    def test_chat_endpoint(self):
        """Тест chat endpoint"""
        response = client.post("/api/v1/chat", json={"message": "Привет"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "mood" in data
        assert "session_id" in data
    
    def test_chat_endpoint_empty_message(self):
        """Тест chat endpoint с пустым сообщением"""
        response = client.post("/api/v1/chat", json={"message": ""})
        assert response.status_code == 400
    
    def test_state_endpoint(self):
        """Тест state endpoint"""
        response = client.get("/api/v1/state")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "mood" in data
        assert "active_modules" in data
    
    def test_memory_store_endpoint(self):
        """Тест memory store endpoint"""
        response = client.post("/api/v1/memory/store", json={
            "content": "Тестовое воспоминание",
            "memory_type": "fact",
            "importance": 5.0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_memory_recall_endpoint(self):
        """Тест memory recall endpoint"""
        response = client.post("/api/v1/memory/recall", json={
            "query": "тест",
            "memory_type": "fact",
            "limit": 10
        })
        assert response.status_code == 200
        data = response.json()
        assert "memories" in data
    
    def test_mood_update_endpoint(self):
        """Тест mood update endpoint"""
        response = client.post("/api/v1/mood/update", json={
            "mood": "happy",
            "intensity": 0.8,
            "reason": "тест"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_personality_update_endpoint(self):
        """Тест personality update endpoint"""
        response = client.post("/api/v1/personality/update", json={
            "trait": "openness",
            "value": 0.9
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_modules_endpoint(self):
        """Тест modules endpoint"""
        response = client.get("/api/v1/modules")
        assert response.status_code == 200
        data = response.json()
        assert "modules" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])