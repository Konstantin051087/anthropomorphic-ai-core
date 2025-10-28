from .models import EmotionSession, db

class SessionRepository:
    def create(self, input_text: str, emotion: str, confidence: float, user_id: str = None):
        session = EmotionSession(
            input_text=input_text,
            emotion=emotion,
            confidence=confidence,
            user_id=user_id
        )
        db.session.add(session)
        db.session.commit()
        return session
    
    def get_by_id(self, session_id: str):
        return EmotionSession.query.get(session_id)
    
    def get_user_sessions(self, user_id: str, limit: int = 100):
        return EmotionSession.query.filter_by(user_id=user_id).limit(limit).all()