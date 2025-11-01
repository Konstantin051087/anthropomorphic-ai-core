#!/bin/bash
# Скрипт деплоя на Render
# Поддержка Python 3.12.3 и 3.13.4

set -e  # Завершить при ошибке

echo "🚀 Начало деплоя Anthropomorphic AI на Render..."

# Проверка наличия необходимых файлов
echo "📋 Проверка конфигурационных файлов..."
required_files=("render.yaml" "requirements.txt" "api/app.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Отсутствует обязательный файл: $file"
        exit 1
    fi
done

echo "✓ Все необходимые файлы присутствуют"

# Проверка Python версии
echo "🐍 Проверка версии Python..."
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo "Текущая версия Python: $python_version"

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Проверка импортов
echo "🔍 Проверка импортов модулей..."
python -c "
try:
    from core.config import settings
    from core.orchestrator import Orchestrator
    from database.models import Base
    print('✓ Основные модули импортируются корректно')
except Exception as e:
    print(f'❌ Ошибка импорта: {e}')
    exit(1)
"

# Запуск тестов
echo "🧪 Запуск базовых тестов..."
if [ -f "pytest.ini" ]; then
    python -m pytest tests/test_basic_imports.py -v
else
    echo "⚠ Файл pytest.ini не найден, пропуск тестов"
fi

# Применение миграций (если применимо)
echo "🗃️ Проверка миграций базы данных..."
if [ -f "alembic.ini" ]; then
    alembic upgrade head
    echo "✓ Миграции базы данных применены"
else
    echo "⚠ Alembic не настроен, пропуск миграций"
fi

echo "✅ Деплой готов!"
echo "📝 Следующие шаги:"
echo "   1. Настройте переменные окружения в Render Dashboard"
echo "   2. Убедитесь, что DATABASE_URL указан корректно"
echo "   3. Проверьте работу приложения по URL Render"