from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация расширений
db = SQLAlchemy()

def create_app(config_class='ai_personality_project.config.testing'):
    """
    Фабрика приложений Flask
    """
    app = Flask(__name__)
    
    # Загрузка конфигурации
    if config_class == 'production':
        from ai_personality_project.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_class == 'testing':
        from ai_personality_project.config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from ai_personality_project.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Инициализация расширений
    db.init_app(app)
    
    # Импорт и регистрация моделей
    from ai_personality_project.database import models
    
    # Регистрация blueprint'ов (если будут)
    # from ai_personality_project.api import bp as api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

# Импорт в конце для избежания циклических импортов
from ai_personality_project import models