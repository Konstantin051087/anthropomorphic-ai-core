FROM python:3.12.3-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание директории для логов
RUN mkdir -p logs

# Создание не-root пользователя для безопасности
RUN groupadd -r ai && useradd -r -g ai ai
RUN chown -R ai:ai /app
USER ai

# Экспорт порта
EXPOSE 8000

# Команда запуска
CMD ["python", "api/app.py"]