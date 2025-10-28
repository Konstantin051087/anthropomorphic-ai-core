from flask import request, jsonify
from . import api_blueprint
from shared.schemas import EmotionAnalysisRequest, EmotionAnalysisResponse
from shared.logger import get_logger
import requests
import os

logger = get_logger(__name__)

@api_blueprint.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        data = request.get_json()
        emotion_request = EmotionAnalysisRequest(**data)
        
        # Вызов AI сервиса
        ai_service_url = os.getenv('AI_SERVICE_URL', 'http://localhost:8001')
        response = requests.post(
            f"{ai_service_url}/analyze",
            json=emotion_request.dict(),
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "AI service unavailable"}), 503
            
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_blueprint.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    from database.repositories import SessionRepository
    repo = SessionRepository()
    session = repo.get_by_id(session_id)
    
    if session:
        return jsonify({
            "id": session.id,
            "input_text": session.input_text,
            "emotion": session.emotion,
            "confidence": session.confidence,
            "created_at": session.created_at.isoformat()
        })
    return jsonify({"error": "Session not found"}), 404
