from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta

from database.models import (
    SystemState, 
    Memory, 
    Interaction, 
    MoodHistory,
    PersonalityTrait,
    CharacterHabit,
    LearningExperience,
    SystemLog
)

class CRUDSystemState:
    def get_current(self, db: Session) -> Optional[SystemState]:
        """Получение текущего состояния системы"""
        return db.query(SystemState).order_by(desc(SystemState.timestamp)).first()
    
    def create(self, db: Session, state_data: Dict[str, Any]) -> SystemState:
        """Создание новой записи состояния системы"""
        db_state = SystemState(**state_data)
        db.add(db_state)
        db.commit()
        db.refresh(db_state)
        return db_state
    
    def update(self, db: Session, state_id: int, update_data: Dict[str, Any]) -> SystemState:
        """Обновление состояния системы"""
        db_state = db.query(SystemState).filter(SystemState.id == state_id).first()
        if db_state:
            for key, value in update_data.items():
                setattr(db_state, key, value)
            db.commit()
            db.refresh(db_state)
        return db_state

class CRUDMemory:
    def get(self, db: Session, memory_id: int) -> Optional[Memory]:
        """Получение памяти по ID"""
        return db.query(Memory).filter(Memory.id == memory_id).first()
    
    def get_by_session(self, db: Session, session_id: str, limit: int = 50) -> List[Memory]:
        """Получение памяти по сессии"""
        return db.query(Memory).filter(
            Memory.session_id == session_id
        ).order_by(desc(Memory.timestamp)).limit(limit).all()
    
    def create(self, db: Session, memory_data: Dict[str, Any]) -> Memory:
        """Создание новой записи памяти"""
        db_memory = Memory(**memory_data)
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)
        return db_memory
    
    def search(self, db: Session, query: str, memory_type: Optional[str] = None, limit: int = 10) -> List[Memory]:
        """Поиск в памяти по содержимому"""
        search_filter = Memory.content.ilike(f"%{query}%")
        if memory_type:
            search_filter = and_(search_filter, Memory.memory_type == memory_type)
        
        return db.query(Memory).filter(search_filter).order_by(
            desc(Memory.importance),
            desc(Memory.timestamp)
        ).limit(limit).all()
    
    def update_importance(self, db: Session, memory_id: int, importance: float) -> Memory:
        """Обновление важности памяти"""
        db_memory = self.get(db, memory_id)
        if db_memory:
            db_memory.importance = importance
            db_memory.last_accessed = datetime.utcnow()
            db.commit()
            db.refresh(db_memory)
        return db_memory

class CRUDInteraction:
    def create(self, db: Session, interaction_data: Dict[str, Any]) -> Interaction:
        """Создание записи взаимодействия"""
        db_interaction = Interaction(**interaction_data)
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        return db_interaction
    
    def get_user_interactions(self, db: Session, user_id: str, limit: int = 100) -> List[Interaction]:
        """Получение взаимодействий пользователя"""
        return db.query(Interaction).filter(
            Interaction.user_id == user_id
        ).order_by(desc(Interaction.timestamp)).limit(limit).all()
    
    def get_session_interactions(self, db: Session, session_id: str) -> List[Interaction]:
        """Получение взаимодействий по сессии"""
        return db.query(Interaction).filter(
            Interaction.session_id == session_id
        ).order_by(Interaction.timestamp).all()

class CRUDMoodHistory:
    def get_current_mood(self, db: Session) -> Optional[MoodHistory]:
        """Получение текущего настроения"""
        return db.query(MoodHistory).order_by(desc(MoodHistory.timestamp)).first()
    
    def create(self, db: Session, mood_data: Dict[str, Any]) -> MoodHistory:
        """Создание записи настроения"""
        db_mood = MoodHistory(**mood_data)
        db.add(db_mood)
        db.commit()
        db.refresh(db_mood)
        return db_mood
    
    def get_mood_history(self, db: Session, hours: int = 24) -> List[MoodHistory]:
        """Получение истории настроения"""
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return db.query(MoodHistory).filter(
            MoodHistory.timestamp >= time_threshold
        ).order_by(MoodHistory.timestamp).all()

class CRUDPersonality:
    def get_traits(self, db: Session) -> Dict[str, float]:
        """Получение всех черт личности"""
        traits = db.query(PersonalityTrait).all()
        return {trait.trait_name: trait.value for trait in traits}
    
    def update_trait(self, db: Session, trait_name: str, value: float) -> PersonalityTrait:
        """Обновление черты личности"""
        db_trait = db.query(PersonalityTrait).filter(PersonalityTrait.trait_name == trait_name).first()
        if db_trait:
            db_trait.value = value
        else:
            db_trait = PersonalityTrait(trait_name=trait_name, value=value)
            db.add(db_trait)
        db.commit()
        db.refresh(db_trait)
        return db_trait

class CRUDSystemLog:
    def create(self, db: Session, log_data: Dict[str, Any]) -> SystemLog:
        """Создание записи лога"""
        db_log = SystemLog(**log_data)
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    def get_recent_logs(self, db: Session, level: Optional[str] = None, limit: int = 100) -> List[SystemLog]:
        """Получение последних логов"""
        query = db.query(SystemLog)
        if level:
            query = query.filter(SystemLog.level == level)
        return query.order_by(desc(SystemLog.timestamp)).limit(limit).all()

# Создание экземпляров CRUD классов
crud_system_state = CRUDSystemState()
crud_memory = CRUDMemory()
crud_interaction = CRUDInteraction()
crud_mood_history = CRUDMoodHistory()
crud_personality = CRUDPersonality()
crud_system_log = CRUDSystemLog()