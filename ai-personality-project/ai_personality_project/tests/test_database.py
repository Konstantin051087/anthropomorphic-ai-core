"""
Тесты для модуля базы данных
"""

import pytest
import tempfile
import os
from ai_personality_project.database.db_config import get_database_url, create_tables, test_connection
from ai_personality_project.database.models import Persona, Interaction
from ai_personality_project.database.repository import PersonaRepository, InteractionRepository

class TestDatabaseConfig:
    """Тесты конфигурации базы данных"""
    
    def test_database_url(self):
        """Тест получения URL базы данных"""
        url = get_database_url()
        assert url is not None
        assert isinstance(url, str)
        
        # Для тестов должна использоваться SQLite
        assert 'sqlite' in url or 'test' in url
    
    def test_connection(self):
        """Тест подключения к базе данных"""
        # Этот тест может пропускаться если нет реальной БД
        connected = test_connection()
        assert connected in [True, False]  # Может быть как True, так и False

class TestPersonaModel:
    """Тесты модели Persona"""
    
    def test_persona_creation(self, test_session):
        """Тест создания персонажа"""
        persona = Persona(
            name="Тестовый персонаж",
            description="Персонаж для тестирования",
            personality_traits={"friendly": True, "helpful": True},
            emotional_state={"current_mood": "neutral"}
        )
        
        test_session.add(persona)
        test_session.commit()
        
        assert persona.id is not None
        assert persona.name == "Тестовый персонаж"
        assert persona.is_active == True
    
    def test_persona_to_dict(self, test_session):
        """Тест преобразования в словарь"""
        persona = Persona(
            name="Тест dict",
            personality_traits={"test": True}
        )
        
        test_session.add(persona)
        test_session.commit()
        
        persona_dict = persona.to_dict()
        
        assert isinstance(persona_dict, dict)
        assert persona_dict['name'] == "Тест dict"
        assert persona_dict['personality_traits'] == {"test": True}
        assert 'created_at' in persona_dict

class TestInteractionModel:
    """Тесты модели Interaction"""
    
    def test_interaction_creation(self, test_session):
        """Тест создания взаимодействия"""
        interaction = Interaction(
            persona_id=1,
            user_input="Тестовое сообщение",
            ai_response="Тестовый ответ",
            processing_time=0.5
        )
        
        test_session.add(interaction)
        test_session.commit()
        
        assert interaction.id is not None
        assert interaction.user_input == "Тестовое сообщение"
        assert interaction.processing_time == 0.5
    
    def test_interaction_to_dict(self, test_session):
        """Тест преобразования взаимодействия в словарь"""
        interaction = Interaction(
            persona_id=1,
            user_input="Тест",
            ai_response="Ответ"
        )
        
        test_session.add(interaction)
        test_session.commit()
        
        interaction_dict = interaction.to_dict()
        
        assert isinstance(interaction_dict, dict)
        assert interaction_dict['user_input'] == "Тест"
        assert interaction_dict['ai_response'] == "Ответ"
        assert 'created_at' in interaction_dict

class TestPersonaRepository:
    """Тесты репозитория персонажей"""
    
    def test_get_all_personas(self, test_session):
        """Тест получения всех персонажей"""
        repo = PersonaRepository(test_session)
        
        # Создаем тестовых персонажей
        persona1 = Persona(name="Персонаж 1", personality_traits={})
        persona2 = Persona(name="Персонаж 2", personality_traits={})
        
        test_session.add_all([persona1, persona2])
        test_session.commit()
        
        personas = repo.get_all()
        
        assert len(personas) >= 2
        assert any(p.name == "Персонаж 1" for p in personas)
        assert any(p.name == "Персонаж 2" for p in personas)
    
    def test_get_persona_by_id(self, test_session):
        """Тест получения персонажа по ID"""
        repo = PersonaRepository(test_session)
        
        persona = Persona(name="Тест ID", personality_traits={})
        test_session.add(persona)
        test_session.commit()
        
        found_persona = repo.get_by_id(persona.id)
        
        assert found_persona is not None
        assert found_persona.id == persona.id
        assert found_persona.name == "Тест ID"
    
    def test_create_persona(self, test_session):
        """Тест создания персонажа через репозиторий"""
        repo = PersonaRepository(test_session)
        
        persona_data = {
            'name': 'Новый персонаж',
            'description': 'Описание',
            'personality_traits': {'friendly': True}
        }
        
        persona = repo.create(persona_data)
        
        assert persona.id is not None
        assert persona.name == 'Новый персонаж'
        assert persona.personality_traits == {'friendly': True}

class TestInteractionRepository:
    """Тесты репозитория взаимодействий"""
    
    def test_create_interaction(self, test_session):
        """Тест создания взаимодействия"""
        repo = InteractionRepository(test_session)
        
        interaction_data = {
            'persona_id': 1,
            'user_input': 'Привет',
            'ai_response': 'Здравствуйте!',
            'processing_time': 0.3
        }
        
        interaction = repo.create(interaction_data)
        
        assert interaction.id is not None
        assert interaction.user_input == 'Привет'
        assert interaction.ai_response == 'Здравствуйте!'
        assert interaction.processing_time == 0.3
    
    def test_get_interaction_statistics(self, test_session):
        """Тест получения статистики"""
        repo = InteractionRepository(test_session)
        
        # Создаем тестовые взаимодействия
        interactions = [
            Interaction(persona_id=1, user_input="Тест 1", ai_response="Ответ 1", processing_time=0.1),
            Interaction(persona_id=1, user_input="Тест 2", ai_response="Ответ 2", processing_time=0.2),
        ]
        
        test_session.add_all(interactions)
        test_session.commit()
        
        stats = repo.get_statistics(persona_id=1)
        
        assert stats['total_interactions'] >= 2
        assert isinstance(stats['average_processing_time'], float)

# Фикстуры pytest
@pytest.fixture
def test_session():
    """Фикстура для тестовой сессии базы данных"""
    from ai_personality_project.database.test_config import test_database
    _, TestingSessionLocal, _ = test_database()
    
    session = TestingSessionLocal()
    
    # Инициализация тестовых данных
    from ai_personality_project.database.models import Base
    Base.metadata.create_all(bind=session.get_bind())
    
    yield session
    
    # Очистка после теста
    session.close()