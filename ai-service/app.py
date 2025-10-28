import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from flask import Flask, request, jsonify
from emotional_analysis.analyzer import EmotionAnalyzer
from persona_management.manager import PersonaManager
from logger import setup_logger, get_logger
from schemas import EmotionAnalysisRequest, EmotionAnalysisResponse, ErrorResponse
from utils import generate_session_id, get_current_timestamp

app = Flask(__name__)
logger = get_logger(__name__)

# Инициализация компонентов
try:
    emotion_analyzer = EmotionAnalyzer()
    persona_manager = PersonaManager()
    logger.info("AI Service components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI components: {str(e)}")
    emotion_analyzer = None
    persona_manager = None

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    try:
        models_status = emotion_analyzer.check_models_health() if emotion_analyzer else {}
        
        return {
            "status": "healthy",
            "service": "emotional-ai-service",
            "timestamp": get_current_timestamp().isoformat(),
            "version": "1.0.0",
            "models": models_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}, 503

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Анализ эмоций в тексте"""
    try:
        if not emotion_analyzer:
            return ErrorResponse(
                error="AI models not loaded",
                code="MODELS_NOT_LOADED",
                timestamp=get_current_timestamp()
            ).dict(), 503
        
        data = request.get_json()
        if not data:
            return ErrorResponse(
                error="Missing JSON data",
                code="INVALID_INPUT",
                timestamp=get_current_timestamp()
            ).dict(), 400
        
        emotion_request = EmotionAnalysisRequest(**data)
        
        # Анализ эмоций
        analysis_result = emotion_analyzer.analyze(
            text=emotion_request.text,
            context=emotion_request.context,
            language=emotion_request.language
        )
        
        # Применение персонажа
        persona_response = persona_manager.apply_persona(
            emotion_result=analysis_result,
            persona_type=emotion_request.persona
        )
        
        # Формирование ответа
        response_data = EmotionAnalysisResponse(
            session_id=generate_session_id(),
            emotion=persona_response.emotion,
            confidence=persona_response.confidence,
            analyzed_text=emotion_request.text,
            persona=emotion_request.persona,
            timestamp=get_current_timestamp(),
            emotional_scores=analysis_result.emotional_scores,
            version="1.0.0"
        )
        
        logger.info(f"Analysis completed: {response_data.emotion} (confidence: {response_data.confidence:.3f})")
        return response_data.dict()
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return ErrorResponse(
            error="Internal server error",
            code="ANALYSIS_ERROR",
            details={"message": str(e)},
            timestamp=get_current_timestamp()
        ).dict(), 500

@app.route('/personas', methods=['GET'])
def get_personas():
    """Получение списка персонажей"""
    try:
        personas = persona_manager.get_available_personas() if persona_manager else []
        return {"personas": personas}
    except Exception as e:
        logger.error(f"Failed to get personas: {str(e)}")
        return ErrorResponse(
            error="Failed to retrieve personas",
            code="PERSONA_ERROR",
            timestamp=get_current_timestamp()
        ).dict(), 500

@app.route('/')
def index():
    return {"message": "Emotional AI Service", "version": "1.0.0"}

if __name__ == '__main__':
    setup_logger()
    port = int(os.environ.get('PORT', 8001))
    logger.info(f"Starting AI Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)