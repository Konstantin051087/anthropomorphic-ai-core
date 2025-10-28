from flask import Flask, request, jsonify
from config.settings import Config
from database.models import db
from api.routes import api_blueprint
from shared.logger import setup_logger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация компонентов
    db.init_app(app)
    app.register_blueprint(api_blueprint)
    
    # Настройка логирования
    setup_logger(app)
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "service": "emotional-ai-web"})
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)