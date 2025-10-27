FROM mcr.microsoft.com/devcontainers/python:3.9

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    sqlite3 \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Настройка Python окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Создание рабочей директории
WORKDIR /workspace

# Копирование requirements для кэширования
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Настройка прав доступа
RUN chmod -R 755 /workspace && \
    chown -R vscode:vscode /workspace

# Настройка shell для лучшего опыта разработки
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Сообщение при успешной сборке
RUN echo "✅ AI Personality Project development environment is ready!"