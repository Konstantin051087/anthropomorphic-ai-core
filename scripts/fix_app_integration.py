# scripts/fix_app_integration.py
#!/usr/bin/env python3
"""
АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ ПОДКЛЮЧЕНИЯ ROUTER В APP.PY
"""

from pathlib import Path
import re

def fix_app_integration():
    app_file = Path("api/app.py")
    
    if not app_file.exists():
        print("❌ Файл app.py не найден")
        return False
    
    content = app_file.read_text()
    
    print("🔧 ИСПРАВЛЕНИЕ APP.PY")
    print("=" * 60)
    
    # Проверяем наличие импорта router
    if "from api.routes import router" not in content:
        print("❌ Импорт router не найден")
        # Добавляем импорт после других импортов из api
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "from api." in line or "from .routes" in line:
                # Уже есть какой-то импорт из api, пропускаем
                continue
            if "from fastapi import" in line or "import FastAPI" in line:
                # Добавляем после импортов FastAPI
                lines.insert(i + 1, "from api.routes import router")
                break
        else:
            # Если не нашли подходящее место, добавляем в начало после импортов
            for i, line in enumerate(lines):
                if line.startswith('from ') or line.startswith('import '):
                    continue
                else:
                    lines.insert(i, "from api.routes import router")
                    break
        
        content = '\n'.join(lines)
        print("✅ Добавлен импорт router")
    
    # Проверяем наличие подключения router
    if "app.include_router(router" not in content:
        print("❌ Подключение router не найдено")
        
        # Ищем место для добавления (после создания middleware)
        lines = content.split('\n')
        
        # Ищем блок после middleware
        middleware_found = False
        insert_position = -1
        
        for i, line in enumerate(lines):
            if "app.middleware" in line or "CORS" in line:
                middleware_found = True
            if middleware_found and line.strip() == "":
                insert_position = i
                break
        
        if insert_position == -1:
            # Ищем после создания app
            for i, line in enumerate(lines):
                if "app = FastAPI(" in line:
                    insert_position = i + 1
                    # Пропускаем настройки app
                    while insert_position < len(lines) and (lines[insert_position].startswith(' ') or lines[insert_position].startswith(')') or lines[insert_position].strip() == ''):
                        insert_position += 1
                    break
        
        if insert_position != -1:
            lines.insert(insert_position, "\n# Подключение API routes")
            lines.insert(insert_position + 1, "app.include_router(router, prefix=\"/api/v1\")")
            print("✅ Добавлено подключение router с префиксом /api/v1")
        else:
            # Добавляем перед событиями startup/shutdown
            for i, line in enumerate(lines):
                if "@app.on_event" in line or "startup" in line:
                    lines.insert(i, "app.include_router(router, prefix=\"/api/v1\")")
                    lines.insert(i, "# Подключение API routes")
                    print("✅ Добавлено подключение router перед событиями")
                    break
            else:
                # Добавляем в конец, перед if __name__ ...
                for i, line in enumerate(lines):
                    if 'if __name__ == "__main__":' in line:
                        lines.insert(i, "\n# Подключение API routes")
                        lines.insert(i + 1, "app.include_router(router, prefix=\"/api/v1\")")
                        print("✅ Добавлено подключение router перед запуском")
                        break
        
        content = '\n'.join(lines)
    
    # Сохраняем исправления
    app_file.write_text(content)
    
    # Проверяем результат
    if "from api.routes import router" in content and "app.include_router(router" in content:
        print("🎉 APP.PY УСПЕШНО ИСПРАВЛЕН!")
        print("📋 ПРОВЕРКА:")
        print("   ✅ Импорт router: присутствует")
        print("   ✅ Подключение router: присутствует")
        print("   ✅ Префикс: /api/v1")
        return True
    else:
        print("❌ Не удалось исправить app.py автоматически")
        return False

if __name__ == "__main__":
    success = fix_app_integration()
    if success:
        print("\n🔁 Перезапустите сервер и запустите тесты снова:")
        print("   python api/app.py")
        print("   python scripts/comprehensive_project_test_fixed.py")
    else:
        print("\n⚠️  Требуется ручное исправление app.py")