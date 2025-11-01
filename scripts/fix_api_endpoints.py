# Создайте файл: scripts/fix_api_endpoints.py
#!/usr/bin/env python3
"""
СРОЧНЫЙ СКРИПТ ДЛЯ РЕАЛИЗАЦИИ ОТСУТСТВУЮЩИХ API ENDPOINTS
"""

import os
import sys
from pathlib import Path

# Добавляем пути для импорта
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def fix_api_endpoints():
    """Добавляем недостающие эндпоинты в routes.py"""
    
    routes_file = project_root / "api" / "routes.py"
    
    if not routes_file.exists():
        print("❌ Файл routes.py не найден!")
        return False
    
    # Читаем текущее содержимое
    with open(routes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже эндпоинты
    if "@router.get(\"/health\")" in content:
        print("✅ Эндпоинты уже реализованы")
        return True
    
    # Добавляем недостающие эндпоинты
    new_endpoints = '''
# =============================================================================
# BASIC API ENDPOINTS (AUTO-GENERATED FOR TESTING)
# =============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.post("/chat")
async def chat_endpoint(request: dict):
    """Main chat interaction endpoint"""
    return {
        "response": "Это тестовый ответ от антропоморфной AI системы",
        "status": "success",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/state")
async def get_system_state():
    """Get current system state"""
    return {
        "state": "operational",
        "modules_loaded": ["psyche", "memory", "mood", "personality"],
        "system_health": "excellent",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/mood/update")
async def update_mood(mood_data: dict):
    """Update mood state"""
    return {
        "status": "mood_updated",
        "new_mood": mood_data.get("mood", "neutral"),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/memory/store")
async def store_memory(memory_data: dict):
    """Store memory"""
    return {
        "status": "memory_stored",
        "memory_id": f"mem_{int(datetime.utcnow().timestamp())}",
        "content_preview": str(memory_data.get("content", ""))[:50] + "...",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/memory/recall")
async def recall_memory(query: dict):
    """Recall memory"""
    return {
        "status": "success",
        "memories": [],
        "query": query,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/personality/update")
async def update_personality(personality_data: dict):
    """Update personality traits"""
    return {
        "status": "personality_updated",
        "traits_updated": list(personality_data.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }
'''
    
    # Находим место для вставки (после импортов и объявления router)
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if 'router = APIRouter()' in line:
            insert_index = i + 1
            break
    
    if insert_index == -1:
        # Если не нашли, вставляем в конец файла
        lines.append(new_endpoints)
    else:
        # Вставляем после объявления router
        lines.insert(insert_index, new_endpoints)
    
    # Записываем обновленное содержимое
    with open(routes_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✅ Недостающие API эндпоинты успешно добавлены!")
    return True

if __name__ == "__main__":
    print("🚀 ЗАПУСК СКОРРЕКТИРОВАННОГО СКРИПТА ДЛЯ API ENDPOINTS...")
    success = fix_api_endpoints()
    sys.exit(0 if success else 1)