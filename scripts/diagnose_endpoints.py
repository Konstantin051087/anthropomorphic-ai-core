# scripts/diagnose_endpoints.py
#!/usr/bin/env python3
"""
ДИАГНОСТИЧЕСКИЙ СКРИПТ ДЛЯ АНАЛИЗА ЭНДПОИНТОВ
"""

import re
import ast
import json
from pathlib import Path

def analyze_routes_file():
    """Анализ файла routes.py на наличие эндпоинтов"""
    routes_file = Path("api/routes.py")
    
    if not routes_file.exists():
        print("❌ Файл routes.py не найден!")
        return
    
    content = routes_file.read_text()
    
    print("🔍 АНАЛИЗ routes.py")
    print("=" * 80)
    
    # Поиск всех декораторов router
    router_patterns = [
        r'@router\.(get|post|put|delete)\([^)]*["\']([^"\']+)["\'][^)]*\)',
        r'@.*\.(get|post|put|delete)\([^)]*["\']([^"\']+)["\'][^)]*\)'
    ]
    
    found_endpoints = []
    
    for pattern in router_patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        for method, endpoint in matches:
            found_endpoints.append({
                "method": method.upper(),
                "endpoint": endpoint,
                "pattern": pattern
            })
    
    # Вывод найденных эндпоинтов
    print("📋 НАЙДЕННЫЕ ЭНДПОИНТЫ:")
    for ep in found_endpoints:
        print(f"  {ep['method']} {ep['endpoint']}")
    
    # Ожидаемые эндпоинты
    expected_endpoints = [
        "/chat", "/state", "/health", "/mood/update",
        "/memory/store", "/memory/recall", "/personality/update",
        "/modules", "/", "/system/info"
    ]
    
    print("\n🎯 СРАВНЕНИЕ С ОЖИДАЕМЫМИ:")
    for expected in expected_endpoints:
        found = any(expected in ep["endpoint"] for ep in found_endpoints)
        status = "✅" if found else "❌"
        print(f"  {status} {expected}")
    
    # AST анализ для надежности
    print("\n🔬 AST АНАЛИЗ:")
    try:
        tree = ast.parse(content)
        ast_endpoints = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        # Получаем метод и путь
                        if isinstance(decorator.func, ast.Attribute):
                            method = decorator.func.attr
                            # Ищем строковые аргументы
                            for arg in decorator.args:
                                if isinstance(arg, ast.Str):
                                    ast_endpoints.append({
                                        "method": method.upper(),
                                        "endpoint": arg.s,
                                        "function": node.name
                                    })
                                elif hasattr(ast, 'Constant') and isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                    ast_endpoints.append({
                                        "method": method.upper(),
                                        "endpoint": arg.value,
                                        "function": node.name
                                    })
        
        for ep in ast_endpoints:
            print(f"  {ep['method']} {ep['endpoint']} -> {ep['function']}")
            
    except Exception as e:
        print(f"  Ошибка AST анализа: {e}")
    
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
    
    endpoints_to_test = [
        ("/", "GET"),
        ("/health", "GET"),
        ("/state", "GET"),
        ("/chat", "POST")
    ]
    
    for endpoint, method in endpoints_to_test:
        try:
            url = f"http://localhost:8000{endpoint}"
            req = urllib.request.Request(url, method=method)
            
            # Для POST запросов добавляем минимальные данные
            if method == "POST":
                req.add_header('Content-Type', 'application/json')
            
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(f"  ✅ {method} {endpoint} - {response.status}")
            except urllib.error.HTTPError as e:
                print(f"  ⚠️  {method} {endpoint} - {e.code} {e.reason}")
            except Exception as e:
                print(f"  ❌ {method} {endpoint} - Ошибка: {e}")
                
        except Exception as e:
            print(f"  🔌 {method} {endpoint} - Сервер не запущен")

if __name__ == "__main__":
    analyze_routes_file()
    test_api_endpoints()