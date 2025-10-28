import os
import sys

from flask import Flask, request, jsonify
from emotional_analysis.analyzer import EmotionAnalyzer
from persona_management.manager import PersonaManager
from logger import setup_logger, get_logger
from schemas import EmotionAnalysisRequest, EmotionAnalysisResponse, ErrorResponse
from utils import generate_session_id, get_current_timestamp

# Добавление пути к shared модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

app = Flask(__name__)
logger = get_logger(__name__)

# Инициализация компонентов
try:
    emotion_analyzer = EmotionAnalyzer()
    persona_manager = PersonaManager()
    logger.info("AI Service components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI components: {str(e)}")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    try:
        # Проверка доступности моделей
        models_status = emotion_analyzer.check_models_health()
        
        return jsonify({
            "status": "healthy",
            "service": "emotional-ai-service",
            "timestamp": get_current_timestamp().isoformat(),
            "version": "1.0.0",
            "models": models_status
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "service": "emotional-ai-service",
            "error": str(e)
        }), 503

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Анализ эмоций в тексте"""
    try:
        # Валидация входных данных
        data = request.get_json()
        if not data:
            return jsonify(ErrorResponse(
                error="Missing JSON data",
                code="INVALID_INPUT",
                timestamp=get_current_timestamp()
            ).dict()), 400
        
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
            version=emotion_analyzer.get_model_version()
        )
        
        logger.info(f"Emotion analysis completed: {response_data.emotion} "
                   f"(confidence: {response_data.confidence:.3f})")
        
        return jsonify(response_data.dict()), 200
        
    except Exception as e:
        logger.error(f"Emotion analysis error: {str(e)}")
        return jsonify(ErrorResponse(
            error="Internal server error during emotion analysis",
            code="ANALYSIS_ERROR",
            details={"message": str(e)},
            timestamp=get_current_timestamp()
        ).dict()), 500

@app.route('/personas', methods=['GET'])
def get_personas():
    """Получение списка доступных персонажей"""
    try:
        personas = persona_manager.get_available_personas()
        return jsonify({"personas": personas}), 200
    except Exception as e:
        logger.error(f"Failed to get personas: {str(e)}")
        return jsonify(ErrorResponse(
            error="Failed to retrieve personas",
            code="PERSONA_ERROR",
            timestamp=get_current_timestamp()
        ).dict()), 500

@app.route('/models/reload', methods=['POST'])
def reload_models():
    """Перезагрузка моделей (для обновления)"""
    try:
        emotion_analyzer.load_models()
        logger.info("Models reloaded successfully")
        return jsonify({"status": "models reloaded"}), 200
    except Exception as e:
        logger.error(f"Model reload failed: {str(e)}")
        return jsonify(ErrorResponse(
            error="Model reload failed",
            code="MODEL_RELOAD_ERROR",
            timestamp=get_current_timestamp()
        ).dict()), 500

if __name__ == '__main__':
    # Настройка логирования
    setup_logger()
    
    port = int(os.environ.get('PORT', 8001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting AI Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)