from flask import Flask, request, jsonify, render_template
from ai_personality_project import create_app, db
from ai_personality_project.ai_core import AICore
from ai_personality_project.database.models import Persona, Interaction
import logging
from datetime import datetime

# Создание приложения
app = create_app('development')

# Инициализация AI ядра
ai_core = AICore()

@app.before_first_request
def initialize_ai():
    """Инициализация AI компонентов при первом запросе"""
    try:
        ai_core.initialize()
        logging.info("✅ AI Core initialized successfully")
    except Exception as e:
        logging.error(f"❌ Failed to initialize AI Core: {e}")

@app.route('/')
def index():
    """Главная страница с информацией о API"""
    return jsonify({
        'message': '🎭 AI Personality Project API',
        'version': '1.0.0',
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'GET /': 'API информация',
            'GET /api/personas': 'Список персонажей',
            'POST /api/personas': 'Создание персонажа',
            'POST /api/interact': 'Взаимодействие с ИИ',
            'GET /api/personas/<id>/interactions': 'История взаимодействий'
        }
    })

@app.route('/api/personas', methods=['GET'])
def get_personas():
    """Получение списка всех персонажей"""
    try:
        personas = Persona.query.all()
        return jsonify({
            'success': True,
            'personas': [persona.to_dict() for persona in personas],
            'count': len(personas)
        })
    except Exception as e:
        logging.error(f"Error getting personas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/personas', methods=['POST'])
def create_persona():
    """Создание нового персонажа"""
    try:
        data = request.json
        
        # Валидация входных данных
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400
        
        # Проверка уникальности имени
        existing_persona = Persona.query.filter_by(name=data['name']).first()
        if existing_persona:
            return jsonify({
                'success': False,
                'error': 'Persona with this name already exists'
            }), 400
        
        # Создание нового персонажа
        new_persona = Persona(
            name=data['name'],
            personality_traits=data.get('personality_traits', {}),
            emotional_state=data.get('emotional_state', {
                'current_mood': 'neutral',
                'emotional_history': []
            })
        )
        
        db.session.add(new_persona)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'persona': new_persona.to_dict(),
            'message': 'Persona created successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating persona: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/interact', methods=['POST'])
def interact():
    """Взаимодействие с AI персонажем"""
    try:
        data = request.json
        
        # Валидация входных данных
        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON data is required'
            }), 400
        
        if 'text' not in data or 'persona_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Text and persona_id are required'
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        # Проверка существования персонажа
        persona = Persona.query.get(data['persona_id'])
        if not persona:
            return jsonify({
                'success': False,
                'error': f'Persona with id {data["persona_id"]} not found'
            }), 404
        
        # Обработка взаимодействия
        result = ai_core.process_interaction(text, data['persona_id'])
        
        # Сохранение взаимодействия в базу данных
        if result['success']:
            interaction = Interaction(
                persona_id=data['persona_id'],
                input_text=text,
                output_text=result['response'],
                emotional_analysis=result.get('emotion_analysis', {})
            )
            db.session.add(interaction)
            db.session.commit()
            
            # Обновление эмоционального состояния персонажа
            if 'emotion_analysis' in result:
                updated_state = ai_core.emotional_model.update_emotional_state(
                    persona.emotional_state or {},
                    result['emotion_analysis']
                )
                persona.emotional_state = updated_state
                db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in interaction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/personas/<int:persona_id>/interactions', methods=['GET'])
def get_persona_interactions(persona_id):
    """Получение истории взаимодействий персонажа"""
    try:
        # Проверка существования персонажа
        persona = Persona.query.get(persona_id)
        if not persona:
            return jsonify({
                'success': False,
                'error': f'Persona with id {persona_id} not found'
            }), 404
        
        # Получение взаимодействий с пагинацией
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        interactions = Interaction.query.filter_by(persona_id=persona_id)\
            .order_by(Interaction.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'persona': persona.to_dict(),
            'interactions': [{
                'id': interaction.id,
                'input_text': interaction.input_text,
                'output_text': interaction.output_text,
                'emotional_analysis': interaction.emotional_analysis,
                'created_at': interaction.created_at.isoformat()
            } for interaction in interactions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': interactions.total,
                'pages': interactions.pages
            }
        })
        
    except Exception as e:
        logging.error(f"Error getting interactions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка здоровья приложения"""
    try:
        # Проверка базы данных
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    # Проверка AI компонентов
    ai_status = 'healthy' if ai_core._initialized else 'unhealthy'
    
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'components': {
            'database': db_status,
            'ai_core': ai_status,
            'emotional_model': 'healthy' if hasattr(ai_core, 'emotional_model') else 'unhealthy',
            'persona_manager': 'healthy' if hasattr(ai_core, 'persona_manager') else 'unhealthy'
        }
    })

# Обработчики ошибок
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )