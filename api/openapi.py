"""
Кастомная конфигурация OpenAPI для Anthropomorphic AI API
"""

def customize_openapi(app):
    """
    Кастомизация OpenAPI документации
    """
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        from fastapi.openapi.utils import get_openapi
        
        openapi_schema = get_openapi(
            title="Anthropomorphic AI API",
            version="1.0.0",
            description="""
            ## Anthropomorphic AI System API
            
            Полный API для взаимодействия с антропоморфной AI системой.
            
            ### Основные возможности:
            - 💬 Чат с AI системой
            - 📊 Мониторинг состояния системы  
            - 😊 Управление настроением AI
            - 🧠 Работа с памятью системы
            - 👤 Настройка личности AI
            
            ### Эндпоинты:
            - `POST /api/v1/chat` - Взаимодействие через чат
            - `GET /api/v1/state` - Состояние системы
            - `POST /api/v1/mood/update` - Обновление настроения
            - `POST /api/v1/memory/store` - Сохранение в память
            - `POST /api/v1/memory/recall` - Извлечение из памяти
            - `POST /api/v1/personality/update` - Обновление личности
            - `GET /api/v1/health` - Проверка здоровья
            """,
            routes=app.routes,
        )
        
        # Добавляем теги для группировки эндпоинтов
        openapi_schema["tags"] = [
            {
                "name": "chat",
                "description": "Операции чата с AI"
            },
            {
                "name": "system",
                "description": "Операции управления системой"
            },
            {
                "name": "mood", 
                "description": "Операции настроения AI"
            },
            {
                "name": "memory",
                "description": "Операции памяти системы"
            },
            {
                "name": "personality",
                "description": "Операции личности AI"
            },
            {
                "name": "health",
                "description": "Операции мониторинга здоровья"
            }
        ]
        
        # Присваиваем теги эндпоинтам
        for path in openapi_schema["paths"]:
            if "/chat" in path:
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["tags"] = ["chat"]
            elif "/state" in path or "/health" in path:
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["tags"] = ["system", "health"]
            elif "/mood" in path:
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["tags"] = ["mood"]
            elif "/memory" in path:
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["tags"] = ["memory"]
            elif "/personality" in path:
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["tags"] = ["personality"]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    return custom_openapi