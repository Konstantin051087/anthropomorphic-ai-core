# Деплой на Render

## Предварительные требования

- Аккаунт на [Render.com](https://render.com)
- Репозиторий на GitHub
- Python 3.12.3

## Шаг 1: Подготовка репозитория

Убедитесь, что в репозитории присутствуют следующие файлы:

- `render.yaml` - конфигурация сервисов
- `Dockerfile` - конфигурация Docker
- `requirements.txt` - зависимости Python
- `runtime.txt` - версия Python
- `.env.example` - пример переменных окружения

## Шаг 2: Создание базы данных

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. Нажмите "New +" и выберите "PostgreSQL"
3. Заполните параметры:
   - **Name**: `anthropomorphic-ai-db`
   - **Database**: `anthropomorphic_ai`
   - **User**: `ai_user`
   - **Region**: `Oregon` (или ближайший к вам)
   - **PostgreSQL Version**: `15`
   - **Plan**: `Starter` (бесплатный)

4. После создания скопируйте "Internal Database URL"

## Шаг 3: Создание веб-сервиса

1. В Render Dashboard нажмите "New +" и выберите "Web Service"
2. Подключите ваш GitHub репозиторий
3. Заполните параметры:
   - **Name**: `anthropomorphic-ai-service`
   - **Environment**: `Python`
   - **Region**: `Oregon` (совпадает с БД)
   - **Branch**: `main`
   - **Root Directory**: `.` (корневая)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api/app.py`

## Шаг 4: Настройка переменных окружения

В настройках веб-сервиса добавьте:

```env
DATABASE_URL=postgresql://ai_user:password@host:port/anthropomorphic_ai
RENDER_ENV=production
SECRET_KEY=your-secure-secret-key-minimum-32-chars
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO