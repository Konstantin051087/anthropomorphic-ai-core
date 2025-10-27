#!/bin/bash

set -e

echo "🚀 Starting AI Personality Project Deployment..."
echo "================================================"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed" 
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "✅ Virtual environment: venv/"

# Активация виртуального окружения
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

echo "✅ Dependencies installed successfully"

# Инициализация базы данных
echo "🗄️ Initializing database..."
python3 -c "
from main import app, db
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully')
"

# Запуск тестов
echo "🧪 Running tests..."
if python3 -m pytest ai_personality_project/tests/ -v; then
    echo "✅ All tests passed"
else
    echo "⚠️ Some tests failed, but continuing deployment"
fi

# Проверка здоровья
echo "🏥 Running health check..."
if python3 scripts/health_check.py; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo "================================================"
echo "🌐 To start the application run: python3 main.py"
echo "📍 Local URL: http://localhost:5000"
echo "================================================"