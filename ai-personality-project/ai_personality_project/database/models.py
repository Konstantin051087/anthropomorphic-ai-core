"""
Модели базы данных для AI Personality Project
"""

from ai_personality_project.database.db_config import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, Float
from sqlalchemy.sql import func
from datetime import datetime

class Persona(Base):
    """Модель персонажа"""
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    
    # Черты личности
    personality_traits = Column(JSON, nullable=False)
    communication_style = Column(JSON, default=dict)
    
    # Эмоциональное состояние
    emotional_state = Column(JSON, default=dict)
    
    # Метаданные
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'personality_traits': self.personality_traits or {},
            'communication_style': self.communication_style or {},
            'emotional_state': self.emotional_state or {},
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Persona(id={self.id}, name='{self.name}')>"

class Interaction(Base):
    """Модель взаимодействия с пользователем"""
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Ссылка на персонажа
    persona_id = Column(Integer, nullable=False)
    
    # Входные данные
    user_input = Column(Text, nullable=False)
    input_emotion = Column(JSON)  # Анализ эмоций во входном сообщении
    
    # Выходные данные
    ai_response = Column(Text, nullable=False)
    response_emotion = Column(JSON)  # Эмоциональная окраска ответа
    
    # Контекст
    conversation_id = Column(String(100))  # Идентификатор сессии/диалога
    user_id = Column(String(100))  # Идентификатор пользователя (опционально)
    
    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)  # Время обработки в секундах
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'persona_id': self.persona_id,
            'user_input': self.user_input,
            'input_emotion': self.input_emotion or {},
            'ai_response': self.ai_response,
            'response_emotion': self.response_emotion or {},
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processing_time': self.processing_time
        }
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, persona_id={self.persona_id})>"

class SystemLog(Base):
    """Модель для системных логов"""
    __tablename__ = 'system_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR
    module = Column(String(100), nullable=False)  # Модуль/компонент
    message = Column(Text, nullable=False)
    details = Column(JSON)  # Дополнительные детали
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'level': self.level,
            'module': self.module,
            'message': self.message,
            'details': self.details or {},
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Дополнительные вспомогательные функции
def init_default_data(session):
    """Инициализация базовых данных"""
    from ai_personality_project.persona_manager import PersonaManager
    
    # Проверяем, есть ли уже персонажи
    existing_personas = session.query(Persona).count()
    
    if existing_personas == 0:
        logger.info("📝 Инициализация базовых персонажей...")
        
        default_personas = [
            Persona(
                name='Дружелюбный помощник',
                description='Теплый и поддерживающий собеседник',
                personality_traits={
                    'friendly': True,
                    'helpful': True,
                    'patient': True,
                    'empathetic': True,
                    'optimistic': True
                },
                communication_style={
                    'formal': False,
                    'warm': True,
                    'supportive': True,
                    'encouraging': True
                },
                emotional_state={
                    'current_mood': 'neutral',
                    'emotional_history': [],
                    'mood_stability': 0.7
                }
            ),
            Persona(
                name='Профессиональный советник',
                description='Экспертный и аналитический собеседник',
                personality_traits={
                    'professional': True,
                    'analytical': True,
                    'precise': True,
                    'formal': True,
                    'knowledgeable': True
                },
                communication_style={
                    'formal': True,
                    'structured': True,
                    'detailed': True,
                    'objective': True
                },
                emotional_state={
                    'current_mood': 'calm',
                    'emotional_history': [],
                    'mood_stability': 0.9
                }
            )
        ]
        
        for persona in default_personas:
            session.add(persona)
        
        session.commit()
        logger.info(f"✅ Создано {len(default_personas)} базовых персонажей")