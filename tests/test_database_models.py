"""
Test database models and schema
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, get_table_names, create_tables

class TestDatabaseModels:
    """Test database model definitions"""
    
    def test_table_names(self):
        """Test that all expected tables are defined"""
        table_names = get_table_names()
        
        expected_tables = [
            'system_state',
            'memories', 
            'tags',
            'memory_tags',
            'interactions',
            'mood_history',
            'personality_traits',
            'character_habits',
            'learning_experiences',
            'system_logs'
        ]
        
        for table in expected_tables:
            assert table in table_names, f"Table {table} not found in metadata"
    
    def test_model_instantiation(self):
        """Test that model instances can be created"""
        from database.models import (
            SystemState, Memory, Interaction, MoodHistory,
            PersonalityTrait, CharacterHabit, LearningExperience, SystemLog
        )
        
        # Test SystemState
        system_state = SystemState()
        assert system_state.id is None
        assert system_state.current_mood == "neutral"
        
        # Test Memory
        memory = Memory(content="Test memory content")
        assert memory.content == "Test memory content"
        assert memory.memory_type == "short_term"
        
        # Test Interaction
        interaction = Interaction(
            user_input="Hello", 
            ai_response="Hi there!"
        )
        assert interaction.user_input == "Hello"
        assert interaction.ai_response == "Hi there!"
        
        # Test other models
        mood_history = MoodHistory(emotion="joy", intensity=0.8)
        personality_trait = PersonalityTrait(
            trait_name="openness", 
            current_value=0.7, 
            baseline_value=0.5
        )
        character_habit = CharacterHabit(habit_name="reflection")
        learning_experience = LearningExperience(experience_type="success")
        system_log = SystemLog(level="INFO", message="Test log")
        
        # Verify all objects are created
        assert mood_history.emotion == "joy"
        assert personality_trait.trait_name == "openness"
        assert character_habit.habit_name == "reflection"
        assert learning_experience.experience_type == "success"
        assert system_log.level == "INFO"
    
    def test_table_creation(self):
        from database.models import Memory
        """Test that tables can be created in memory database"""
        # Create in-memory SQLite database for testing
        engine = create_engine('sqlite:///:memory:')
        
        # Create all tables
        create_tables(engine)
        
        # Verify tables were created
        table_names = get_table_names()
        assert len(table_names) >= 8  # Should have at least 8 tables
        
        # Test session creation
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Verify we can add and query data
        memory = Memory(content="Test memory for database")
        session.add(memory)
        session.commit()
        
        # Query the memory back
        queried_memory = session.query(Memory).filter_by(content="Test memory for database").first()
        assert queried_memory is not None
        assert queried_memory.content == "Test memory for database"
        
        session.close()