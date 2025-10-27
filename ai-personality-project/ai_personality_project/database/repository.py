"""
Репозиторий для работы с базой данных
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ai_personality_project.database.models import Persona, Interaction, SystemLog

logger = logging.getLogger(__name__)

class PersonaRepository:
    """Репозиторий для работы с персонажами"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Persona]:
        """Получение всех персонажей"""
        return self.db.query(Persona).filter(Persona.is_active == True).all()
    
    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        """Получение персонажа по ID"""
        return self.db.query(Persona).filter(
            Persona.id == persona_id, 
            Persona.is_active == True
        ).first()
    
    def get_by_name(self, name: str) -> Optional[Persona]:
        """Получение персонажа по имени"""
        return self.db.query(Persona).filter(
            Persona.name == name,
            Persona.is_active == True
        ).first()
    
    def create(self, persona_data: Dict[str, Any]) -> Persona:
        """Создание нового персонажа"""
        persona = Persona(**persona_data)
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        
        logger.info(f"✅ Создан новый персонаж: {persona.name} (ID: {persona.id})")
        return persona
    
    def update(self, persona_id: int, update_data: Dict[str, Any]) -> Optional[Persona]:
        """Обновление персонажа"""
        persona = self.get_by_id(persona_id)
        if persona:
            for key, value in update_data.items():
                setattr(persona, key, value)
            self.db.commit()
            self.db.refresh(persona)
            logger.info(f"✅ Обновлен персонаж: {persona.name} (ID: {persona_id})")
        return persona
    
    def update_emotional_state(self, persona_id: int, emotional_state: Dict) -> Optional[Persona]:
        """Обновление эмоционального состояния персонажа"""
        persona = self.get_by_id(persona_id)
        if persona:
            persona.emotional_state = emotional_state
            self.db.commit()
            self.db.refresh(persona)
            logger.debug(f"🎭 Обновлены эмоции персонажа {persona_id}")
        return persona

class InteractionRepository:
    """Репозиторий для работы с взаимодействиями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, interaction_data: Dict[str, Any]) -> Interaction:
        """Создание записи о взаимодействии"""
        interaction = Interaction(**interaction_data)
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        
        logger.debug(f"💬 Создано взаимодействие ID: {interaction.id}")
        return interaction
    
    def get_by_persona(self, persona_id: int, limit: int = 50) -> List[Interaction]:
        """Получение взаимодействий персонажа"""
        return self.db.query(Interaction).filter(
            Interaction.persona_id == persona_id
        ).order_by(Interaction.created_at.desc()).limit(limit).all()
    
    def get_by_conversation(self, conversation_id: str) -> List[Interaction]:
        """Получение взаимодействий по идентификатору диалога"""
        return self.db.query(Interaction).filter(
            Interaction.conversation_id == conversation_id
        ).order_by(Interaction.created_at.asc()).all()
    
    def get_statistics(self, persona_id: Optional[int] = None) -> Dict[str, Any]:
        """Получение статистики по взаимодействиям"""
        query = self.db.query(Interaction)
        
        if persona_id:
            query = query.filter(Interaction.persona_id == persona_id)
        
        total = query.count()
        
        # Среднее время обработки
        avg_time = self.db.query(
            func.avg(Interaction.processing_time)
        ).filter(Interaction.processing_time.isnot(None)).scalar() or 0
        
        return {
            'total_interactions': total,
            'average_processing_time': round(avg_time, 2),
            'persona_id': persona_id
        }

class SystemLogRepository:
    """Репозиторий для системных логов"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, level: str, module: str, message: str, details: Dict = None):
        """Создание записи в системном логе"""
        log = SystemLog(
            level=level,
            module=module,
            message=message,
            details=details or {}
        )
        self.db.add(log)
        self.db.commit()
    
    def get_recent_logs(self, level: str = None, limit: int = 100) -> List[SystemLog]:
        """Получение последних логов"""
        query = self.db.query(SystemLog)
        
        if level:
            query = query.filter(SystemLog.level == level)
        
        return query.order_by(SystemLog.created_at.desc()).limit(limit).all()

# Фабрика репозиториев
class RepositoryFactory:
    """Фабрика для создания репозиториев"""
    
    def __init__(self, db: Session):
        self.db = db
    
    @property
    def personas(self) -> PersonaRepository:
        return PersonaRepository(self.db)
    
    @property
    def interactions(self) -> InteractionRepository:
        return InteractionRepository(self.db)
    
    @property
    def system_logs(self) -> SystemLogRepository:
        return SystemLogRepository(self.db)