# Anthropomorphic AI Core API Documentation

## Обзор

API для антропоморфной AI модели, предоставляющее endpoints для взаимодействия с системой.

**Базовый URL**: `https://your-render-service.onrender.com`

## Аутентификация

В текущей версии аутентификация не требуется. Все endpoints открыты.

## Endpoints

### Корневой endpoint

**GET /**  
Возвращает информацию о API и доступные endpoints.

**Response:**
```json
{
  "message": "Anthropomorphic AI Core API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "chat": "/chat (POST)",
    "state": "/state (GET)",
    "health": "/health (GET)",
    "memory_store": "/memory/store (POST)",
    "memory_recall": "/memory/recall (POST)",
    "mood_update": "/mood/update (POST)",
    "personality_update": "/personality/update (POST)",
    "modules": "/modules (GET)"
  },
  "timestamp": "2025-10-31T15:04:46.123Z"
}