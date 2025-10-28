# Emotional AI Core 🧠

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3123/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.31-yellow.svg)](https://huggingface.co/transformers/)

Реалистичный антропоморфный ИИ для анализа и генерации эмоциональных реакций на русском языке.

## 🌟 Особенности

- **Анализ эмоций** в тексте с использованием современных NLP моделей
- **Антропоморфные персонажи** с различными эмоциональными профилями
- **Многопользовательская архитектура** с изоляцией сессий
- **RESTful API** для легкой интеграции
- **Масштабируемая микросервисная архитектура**

## 🏗️ Архитектура

┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Web Service │◄──►│ AI Service │◄──►│ AI Models │
│ (Render) │ │ (Hugging Face) │ │ (Hugging Face) │
└─────────────────┘ └──────────────────┘ └─────────────────┘
│ │ │
▼ ▼ ▼
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ PostgreSQL │ │ Emotion │ │ Persona │
│ Database │ │ Analysis │ │ Management │
└─────────────────┘ └──────────────────┘ └─────────────────┘

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.12.3
- PostgreSQL 13+
- Git

### Установка

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/your-username/emotional-ai-core.git
   cd emotional-ai-core

cp .env.example .env
# Отредактируйте .env файл с вашими настройками

# Web Service
cd web-service
pip install -r requirements.txt

# AI Service  
cd ../ai-service
pip install -r requirements.txt

cd ../web-service
flask db upgrade

# Terminal 1 - AI Service
cd ai-service
python app.py

# Terminal 2 - Web Service
cd web-service  
python app.py

📚 API Документация

Анализ эмоций
Endpoint: POST /analyze

Request:

json

{
  "text": "Я очень рад сегодняшнему дню!",
  "user_id": "user123",
  "persona": "empathetic"
}

Response:

json

{
  "session_id": "uuid-string",
  "emotion": "joy",
  "confidence": 0.89,
  "analyzed_text": "Я очень рад сегодняшнему дню!",
  "persona": "empathetic",
  "timestamp": "2024-01-15T10:30:00Z",
  "emotional_scores": {
    "joy": 0.89,
    "sadness": 0.05,
    "anger": 0.02,
    "fear": 0.01,
    "surprise": 0.03
  }
}

Доступные персонажи

Endpoint: GET /personas

Response:

json

{
  "personas": [
    {
      "name": "default",
      "description": "Балансированный персонаж с естественными реакциями",
      "response_style": "balanced",
      "temperature": 0.7
    },
    {
      "name": "empathetic", 
      "description": "Эмпатичный персонаж с глубоким пониманием эмоций",
      "response_style": "empathetic",
      "temperature": 0.8
    }
  ]
}

🛠️ Развертывание

Render (Web Service + Database)

Fork репозитория на GitHub

Создайте аккаунт на Render.com

Connect your repository в Render dashboard

Автоматическое развертывание - Render автоматически обнаружит render.yaml

Hugging Face (AI Service)

Создайте Space на Hugging Face

Выберите Docker как runtime

Настройте переменные окружения в Space settings

Деплой через Git push

Google Cloud (Обучение моделей)

bash

# Активация Google Cloud SDK

gcloud auth login

# Запуск обучения

cd notebooks

python colab_training.py --config training_config.json

🔧 Конфигурация

Переменные окружения

Ключевые переменные (полный список в .env.example):

DATABASE_URL - PostgreSQL connection string

AI_SERVICE_URL - URL AI микросервиса

HF_API_TOKEN - Hugging Face API token

EMOTION_MODEL_NAME - Модель для анализа эмоций

Персонажи

Система поддерживает настройку персонажей через shared/schemas.py:

python

PersonaConfig(
    name="creative",
    description="Креативный персонаж с богатым воображением",
    emotional_traits={
        EmotionLabel.JOY: 0.4,
        EmotionLabel.SURPRISE: 0.3,
        EmotionLabel.NEUTRAL: 0.3
    },
    response_style="creative",
    temperature=0.9
)

📊 Мониторинг

Health Checks

bash

# Web Service

curl https://your-web-service.render.com/health

# AI Service

curl https://your-ai-service.hf.space/health
Метрики
Система предоставляет метрики через:

JSON логирование

Health check endpoints

Prometheus metrics (в будущих версиях)

🤝 Разработка

Структура проекта
text
emotional-ai-core/
├── web-service/          # Основной API сервис
├── ai-service/           # AI микросервис  
├── shared/               # Общие модули
├── notebooks/            # Обучение моделей
├── scripts/              # Утилиты развертывания
└── docs/                 # Документация

Тестирование

bash

# Запуск тестов развертывания

python scripts/deploy_check.py

# Мониторинг здоровья

python scripts/health_check.py --once
Code Style
bash

# Форматирование кода

black .
flake8 .

# Проверка типов

mypy .

🚧 Roadmap

Поддержка мультиязычности

Генерация эмоциональных ответов

Интеграция с голосовыми интерфейсами

Расширенная аналитика эмоций

Мобильное приложение

📄 Лицензия

MIT License - смотрите файл LICENSE для деталей.

🤝 Вклад в проект

Fork репозитория

Создайте feature branch (git checkout -b feature/amazing-feature)

Commit изменений (git commit -m 'Add amazing feature')

Push в branch (git push origin feature/amazing-feature)

Откройте Pull Request

📞 Поддержка

Issues: GitHub Issues

Email: your-email@example.com

Discord: Emotional AI Community

<div align="center">
Emotional AI Core - делаем ИИ более человечным 💫

Документация •
Примеры •
Блог