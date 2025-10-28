from . import db
from datetime import datetime
import uuid

class EmotionSession(db.Model):
    __tablename__ = 'emotion_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    input_text = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
