"""
Упрощенная версия приложения для быстрого запуска
"""

from flask import Flask, request, jsonify
from ai_personality_project.ai_core import AICore
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация AI
ai_core = AICore()

@app.before_first_request
def initialize_ai():
    """Инициализация AI при первом запросе"""
    try:
        ai_core.initialize()
        logger.info("✅ AI Core инициализирован в упрощенном приложении")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации AI Core: {e}")

@app.route('/')
def home():
    """Главная страница"""
    return jsonify({
        'message': '🎭 AI Personality Project - Simplified API',
        'status': 'active',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Проверка здоровья"""
    return jsonify({
        'status': 'healthy',
        'ai_initialized': ai_core._initialized
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Упрощенный чат-интерфейс"""
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Параметр "message" обязателен'
            }), 400
        
        # Используем персонажа по умолчанию
        persona_id = data.get('persona_id', 1)
        
        result = ai_core.process_interaction(data['message'], persona_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Ошибка в чате: {e}")
        return jsonify({
            'success': False,
            'error': 'Внутренняя ошибка сервера'
        }), 500

@app.route('/personas', methods=['GET'])
def get_personas():
    """Получение списка персонажей"""
    try:
        personas = ai_core.persona_manager.list_personas()
        return jsonify({
            'success': True,
            'personas': personas
        })
    except Exception as e:
        logger.error(f"Ошибка получения персонажей: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Инициализация при запуске
    ai_core.initialize()
    
    print("🚀 Запуск упрощенного приложения AI Personality Project...")
    print("📍 Доступно по адресу: http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )