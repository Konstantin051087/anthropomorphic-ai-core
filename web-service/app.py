import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from flask import Flask
from config.settings import Config
from database.models import db
from api.routes import api_blueprint
from logger import setup_logger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация компонентов
    db.init_app(app)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Настройка логирования
    setup_logger(app)
    
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "service": "emotional-ai-web"}
    
    @app.route('/')
    def index():
        return {"message": "Emotional AI Web Service", "version": "1.0.0"}
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)