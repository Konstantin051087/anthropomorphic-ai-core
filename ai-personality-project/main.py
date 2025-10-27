from ai_personality_project import create_app, db
import os
from ai_personality_project.logging_config import setup_logging

# Настройка логирования
setup_logging()

app = create_app('development')

@app.before_first_request
def create_tables():
    """Создание таблиц при первом запросе"""
    db.create_all()
    print("✅ Database tables created")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting AI Personality Project...")
    print("📍 Local URL: http://localhost:5000")
    print("📍 Network URL: http://0.0.0.0:5000")
    
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'True').lower() == 'true'
    )