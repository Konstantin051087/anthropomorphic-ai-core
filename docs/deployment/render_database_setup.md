# Инструкция по настройке базы данных на Render

## Шаг 1: Создание PostgreSQL базы данных

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. Нажмите "New +" и выберите "PostgreSQL"
3. Заполните параметры:
   - **Name**: `anthropomorphic-ai-db`
   - **Database**: `anthropomorphic_ai`
   - **User**: `ai_user`
   - **Region**: Выберите ближайший регион
   - **PostgreSQL Version**: 15
   - **Plan**: Starter (бесплатный план)

## Шаг 2: Настройка переменных окружения

После создания базы данных:

1. Перейдите в настройки базы данных
2. Скопируйте "Internal Database URL"
3. В настройках веб-сервиса добавьте переменные окружения:

```env
DATABASE_URL=postgresql://ai_user:password@host:port/anthropomorphic_ai
RENDER_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=false