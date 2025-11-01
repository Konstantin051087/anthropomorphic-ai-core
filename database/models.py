"""
SQLAlchemy models for Anthropomorphic AI database schema
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, 
    DateTime, Boolean, JSON, ForeignKey, Table, MetaData
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

# Use consistent metadata
Base = declarative_base()

# Association table for memory tags
memory_tags = Table(
    'memory_tags',
    Base.metadata,
    Column('memory_id', Integer, ForeignKey('memories.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class SystemState(Base):
    """Global system state and configuration"""
    __tablename__ = "system_state"
    
    id = Column(Integer, primary_key=True, index=True)
    current_mood = Column(String, default="neutral")
    mood_intensity = Column(Float, default=0.5)
    personality_traits = Column(JSON)
    system_parameters = Column(JSON)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __init__(self, **kwargs):
        if 'current_mood' not in kwargs:
            kwargs['current_mood'] = "neutral"
        if 'mood_intensity' not in kwargs:
            kwargs['mood_intensity'] = 0.5
        super().__init__(**kwargs)

class Memory(Base):
    """Memory storage for short-term and long-term memories"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    memory_type = Column(String, default="short_term")
    importance = Column(Float, default=0.5)
    emotion_context = Column(String)
    access_frequency = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    tags = relationship("Tag", secondary=memory_tags, back_populates="memories")
    
    def __init__(self, **kwargs):
        if 'memory_type' not in kwargs:
            kwargs['memory_type'] = "short_term"
        if 'importance' not in kwargs:
            kwargs['importance'] = 0.5
        if 'access_frequency' not in kwargs:
            kwargs['access_frequency'] = 0
        super().__init__(**kwargs)

class Tag(Base):
    """Tags for categorizing memories"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)
    
    # Relationships
    memories = relationship("Memory", secondary=memory_tags, back_populates="tags")

class Interaction(Base):
    """Store all user interactions for learning and analysis"""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    user_emotion = Column(String)
    ai_emotion = Column(String)
    response_quality = Column(Float)
    context_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class MoodHistory(Base):
    """Historical record of mood changes"""
    __tablename__ = "mood_history"
    
    id = Column(Integer, primary_key=True, index=True)
    emotion = Column(String, nullable=False)
    intensity = Column(Float, nullable=False)
    trigger = Column(Text)
    duration = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class PersonalityTrait(Base):
    """Personality traits and their evolution over time"""
    __tablename__ = "personality_traits"
    
    id = Column(Integer, primary_key=True, index=True)
    trait_name = Column(String, nullable=False, index=True)
    current_value = Column(Float, nullable=False)
    baseline_value = Column(Float, nullable=False)
    variability = Column(Float, default=0.1)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class CharacterHabit(Base):
    """Character habits and behavioral patterns"""
    __tablename__ = "character_habits"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_name = Column(String, nullable=False)
    description = Column(Text)
    strength = Column(Float, default=0.5)
    frequency = Column(Integer, default=0)
    last_expressed = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __init__(self, **kwargs):
        if 'strength' not in kwargs:
            kwargs['strength'] = 0.5
        if 'frequency' not in kwargs:
            kwargs['frequency'] = 0
        super().__init__(**kwargs)

class LearningExperience(Base):
    """Store learning experiences for adaptive learning"""
    __tablename__ = "learning_experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    experience_type = Column(String)
    description = Column(Text)
    lesson_learned = Column(Text)
    impact_score = Column(Float)
    applied_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __init__(self, **kwargs):
        if 'applied_count' not in kwargs:
            kwargs['applied_count'] = 0
        super().__init__(**kwargs)

class SystemLog(Base):
    """System operation logs for monitoring and debugging"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    module = Column(String)
    message = Column(Text)
    context_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Helper function to get all table names
def get_table_names():
    """Get all table names from metadata"""
    return [table.name for table in Base.metadata.tables.values()]

# Helper function to create all tables (for testing)
def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)