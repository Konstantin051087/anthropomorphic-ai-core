# Совместимость версий Python

## Поддерживаемые версии
- ✅ Python 3.12.3 (локальная разработка)
- ✅ Python 3.13.4 (Render production)

## Стратегия управления зависимостями

### requirements.txt без версий
Преимущества:
- Автоматическая установка совместимых версий
- Избежание конфликтов зависимостей
- Простота поддержки

Проверенные пакеты (работают с обеими версиями Python):
- fastapi
- uvicorn  
- sqlalchemy
- pydantic
- transformers
- torch
- gradio
- pytest

## Процедура деплоя

1. **Локальная разработка** (3.12.3):
   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   pip install -r requirements.txt