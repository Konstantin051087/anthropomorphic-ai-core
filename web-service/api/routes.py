import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from flask import request, jsonify
from . import api_blueprint
from logger import get_logger
import requests

logger = get_logger(__name__)

@api_blueprint.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return {"error": "Missing 'text' in request"}, 400
        
        ai_service_url = os.getenv('AI_SERVICE_URL', 'http://localhost:8001')
        response = requests.post(
            f"{ai_service_url}/analyze",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json(), 200
        else:
            logger.error(f"AI service error: {response.status_code}")
            return {"error": "AI service unavailable"}, 503
            
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return {"error": "Internal server error"}, 500

@api_blueprint.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    from database.repositories import SessionRepository
    repo = SessionRepository()
    session = repo.get_by_id(session_id)
    
    if session:
        return {
            "id": session.id,
            "input_text": session.input_text,
            "emotion": session.emotion,
            "confidence": session.confidence,
            "created_at": session.created_at.isoformat()
        }
    return {"error": "Session not found"}, 404