# scripts/diagnose_endpoints_fixed.py
#!/usr/bin/env python3
"""
ИСПРАВЛЕННАЯ ДИАГНОСТИКА ЭНДПОИНТОВ
"""

import re
import ast
import json
from pathlib import Path

def analyze_routes_file():
    """Анализ файла routes.py с исправленными регулярными выражениями"""
    routes_file = Path("api/routes.py")
    
    if not routes_file.exists():
        print("❌ Файл routes.py не найден!")
        return
    
    content = routes_file.read_text()
    
    print("🔍 АНАЛИЗ routes.py - ИСПРАВЛЕННАЯ ВЕРСИЯ")
    print("=" * 80)
    
    # ИСПРАВЛЕННЫЕ РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ
    router_patterns = [
        # Формат: @router.get("/path")
        r'@router\.(get|post|put|delete)\(\s*"([^"]+)"',
        # Формат: @router.get('/path')
        r"@router\.(get|post|put|delete)\(\s*'([^']+)'",
    ]
    
    found_endpoints = []
    
    for pattern in router_patterns:
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            method = match.group(1).upper()
            endpoint = match.group(2)
            found_endpoints.append({
                "method": method,
                "endpoint": endpoint,
                "line": content[:match.start()].count('\n') + 1
            })
    
    # Вывод найденных эндпоинтов
    print("📋 НАЙДЕННЫЕ ЭНДПОИНТЫ:")
    for ep in found_endpoints:
        print(f"  {ep['method']} {ep['endpoint']} (строка {ep['line']})")
    
    # Ожидаемые эндпоинты
    expected_endpoints = [
        "/chat", "/state", "/health", "/mood/update",
        "/memory/store", "/memory/recall", "/personality/update",
        "/modules", "/", "/system/info"
    ]
    
    print("\n🎯 СРАВНЕНИЕ С ОЖИДАЕМЫМИ:")
    matches_found = 0
    for expected in expected_endpoints:
        found = any(expected == ep["endpoint"] for ep in found_endpoints)
        status = "✅" if found else "❌"
        if found: matches_found += 1
        print(f"  {status} {expected}")
    
    print(f"\n📊 РЕЗУЛЬТАТ: {matches_found}/{len(expected_endpoints)} эндпоинтов найдено")
    
    # Проверка наличия router
    if "router = APIRouter()" in content:
        print("✅ Router инициализирован")
    else:
        print("❌ Router не инициализирован")
    
    return found_endpoints

def test_api_endpoints():
    """Тестирование реальной работы API"""
    print("\n🌐 ТЕСТИРОВАНИЕ API:")
    
    import urllib.request
    import urllib.error
    import json
    
    endpoints_to_test = [
        ("/", "GET", None),
        ("/health", "GET", None),
        ("/state", "GET", None),
        ("/modules", "GET", None),
        ("/system/info", "GET", None),
        ("/chat", "POST", {"message": "test"}),
    ]
    
    for endpoint, method, data in endpoints_to_test:
        try:
            url = f"http://localhost:8000{endpoint}"
            req = urllib.request.Request(url, method=method)
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'Diagnostic-Script')
            
            if data and method == "POST":
                import json
                data_str = json.dumps(data).encode('utf-8')
                req.data = data_str
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    response_data = response.read().decode('utf-8')
                    print(f"  ✅ {method} {endpoint} - {response.status}")
                    # Для отладки показываем короткий ответ
                    if response_data:
                        try:
                            parsed = json.loads(response_data)
                            if 'message' in parsed:
                                print(f"       📨 Ответ: {parsed['message'][:50]}...")
                        except:
                            if len(response_data) < 100:
                                print(f"       📨 Ответ: {response_data}")
            except urllib.error.HTTPError as e:
                print(f"  ⚠️  {method} {endpoint} - {e.code} {e.reason}")
            except Exception as e:
                print(f"  ❌ {method} {endpoint} - Ошибка: {e}")
                
        except Exception as e:
            print(f"  🔌 {method} {endpoint} - Сервер не запущен: {e}")

def check_routes_in_app():
    """Проверка, что routes подключены в app.py"""
    print("\n🔗 ПРОВЕРКА ПОДКЛЮЧЕНИЯ ROUTES В APP.PY:")
    
    app_file = Path("api/app.py")
    if app_file.exists():
        content = app_file.read_text()
        
        # Проверяем импорт routes
        if "from api.routes import router" in content or "from .routes import router" in content:
            print("✅ Router импортирован в app.py")
        else:
            print("❌ Router не импортирован в app.py")
            
        # Проверяем подключение router
        if "app.include_router(router)" in content:
            print("✅ Router подключен к приложению")
        else:
            print("❌ Router не подключен к приложению")
            
        # Проверяем префиксы
        if "prefix=" in content:
            prefix_match = re.search(r'prefix=(["\'])([^"\']+)\1', content)
            if prefix_match:
                print(f"📌 Используется префикс: {prefix_match.group(2)}")
    else:
        print("❌ Файл app.py не найден")

if __name__ == "__main__":
    analyze_routes_file()
    check_routes_in_app()
    test_api_endpoints()