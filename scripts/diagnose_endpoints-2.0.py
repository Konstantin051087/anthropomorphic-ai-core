# scripts/comprehensive_project_test-8.0.py
#!/usr/bin/env python3
"""
КОМПЛЕКСНЫЙ ТЕСТ ВСЕГО ПРОЕКТА ANTHROPOMORPHIC AI - ВЕРСИЯ 8.0
РАДИКАЛЬНОЕ ИСПРАВЛЕНИЕ ОБНАРУЖЕНИЯ ЭНДПОИНТОВ
"""

import os
import sys
import json
import logging
import importlib.metadata
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set
import urllib.request
import urllib.error
import time
import socket
import re
import ast

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class ComprehensiveProjectTest:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.project_structure = {}
        self.test_results = {
            "project": "Anthropomorphic AI Core",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_version": sys.version,
            "overall_status": "IN_PROGRESS",
            "current_stage": "1.3 - Настройка инфраструктуры",
            "stage_progress": {},
            "project_structure": {},
            "detailed_analysis": {},
            "recommendations": [],
            "score": {
                "total_tests": 0,
                "passed_tests": 0,
                "success_rate": 0
            }
        }

    def print_header(self, message: str):
        """Печать заголовка раздела"""
        print(f"\n{'='*80}")
        print(f"🔍 {message}")
        print(f"{'='*80}")

    def print_section(self, message: str):
        """Печать заголовка подраздела"""
        print(f"\n{'─'*60}")
        print(f"📁 {message}")
        print(f"{'─'*60}")

    def print_result(self, test_name: str, status: bool, details: str = "", points: int = 1):
        """Печать результата теста"""
        icon = "✅" if status else "❌"
        status_text = "ВЫПОЛНЕНО" if status else "НЕ ВЫПОЛНЕНО"
        print(f"{icon} {test_name}: {status_text}")
        if details:
            print(f"   📝 {details}")
        
        # Обновляем счетчики тестов
        self.test_results["score"]["total_tests"] += 1
        if status:
            self.test_results["score"]["passed_tests"] += points
        
        return status

    # ... (остальные методы остаются такими же до _test_subtask_1_2_1)

    def _test_subtask_1_2_1(self):
        """Подзадача 1.2.1: Детальное проектирование API endpoints - РАДИКАЛЬНОЕ ИСПРАВЛЕНИЕ"""
        subtask_results = {
            "name": "Проектирование API endpoints",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка файлов API
        api_files = [
            "api/__init__.py", "api/app.py", "api/routes.py", 
            "api/models.py", "api/dependencies.py", "api/middleware.py"
        ]
        
        for api_file in api_files:
            file_path = self.base_dir / api_file
            exists = file_path.exists()
            check_result = self.print_result(
                f"API файл: {api_file}",
                exists,
                "Найден" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "file": api_file,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # РАДИКАЛЬНОЕ ИСПРАВЛЕНИЕ: Надежное обнаружение эндпоинтов
        routes_file = self.base_dir / "api" / "routes.py"
        if routes_file.exists():
            try:
                content = routes_file.read_text()
                
                # Многоуровневое обнаружение эндпоинтов
                endpoints_found = self._reliable_endpoint_detection(content)
                
                # Ожидаемые эндпоинты
                expected_endpoints = [
                    "/chat", "/state", "/health", "/mood/update",
                    "/memory/store", "/memory/recall", "/personality/update", 
                    "/modules", "/", "/system/info"
                ]
                
                # Проверка каждого ожидаемого эндпоинта
                for expected in expected_endpoints:
                    found = False
                    details = ""
                    
                    for found_ep in endpoints_found:
                        if (found_ep["endpoint"] == expected or 
                            found_ep["endpoint"].startswith(expected) or
                            expected in found_ep["endpoint"]):
                            found = True
                            details = f"Найден как: {found_ep['endpoint']} ({found_ep['method']})"
                            break
                    
                    check_result = self.print_result(
                        f"API эндпоинт: {expected}",
                        found,
                        details if found else "Не найден в routes.py"
                    )
                    subtask_results["checks"].append({
                        "endpoint": expected,
                        "implemented": found,
                        "status": "PASS" if found else "FAIL"
                    })
                
            except Exception as e:
                self.print_result("Анализ routes.py", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_routes",
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # ПРОВЕРКА РАБОТОСПОСОБНОСТИ API
        if self._test_api_functionality():
            check_result = self.print_result(
                "API эндпоинты работают",
                True,
                "Все основные эндпоинты отвечают корректно"
            )
            subtask_results["checks"].append({
                "check": "api_functionality",
                "status": "PASS"
            })
        else:
            check_result = self.print_result(
                "API эндпоинты работают",
                False,
                "Некоторые эндпоинты не отвечают - запустите сервер: python api/app.py"
            )
            subtask_results["checks"].append({
                "check": "api_functionality", 
                "status": "FAIL"
            })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _reliable_endpoint_detection(self, content: str) -> List[Dict]:
        """Надежное многоуровневое обнаружение эндпоинтов"""
        endpoints = []
        
        # Уровень 1: Простой текстовый поиск (самый надежный)
        endpoints.extend(self._simple_text_search(content))
        
        # Уровень 2: Regex поиск
        endpoints.extend(self._regex_search(content))
        
        # Уровень 3: AST анализ
        endpoints.extend(self._ast_search(content))
        
        # Удаляем дубликаты
        unique_endpoints = []
        seen = set()
        for ep in endpoints:
            key = (ep["method"], ep["endpoint"])
            if key not in seen:
                seen.add(key)
                unique_endpoints.append(ep)
        
        return unique_endpoints

    def _simple_text_search(self, content: str) -> List[Dict]:
        """Простой текстовый поиск эндпоинтов"""
        endpoints = []
        
        # Ищем очевидные паттерны
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Поиск декораторов router
            if '@router.' in line_clean and ('("/' in line_clean or "('/" in line_clean):
                # Извлекаем метод и путь
                if 'get(' in line_clean:
                    method = 'GET'
                elif 'post(' in line_clean:
                    method = 'POST' 
                elif 'put(' in line_clean:
                    method = 'PUT'
                elif 'delete(' in line_clean:
                    method = 'DELETE'
                else:
                    method = 'UNKNOWN'
                
                # Извлекаем путь
                path_match = re.search(r'\(["\']([^"\']+)["\']', line_clean)
                if path_match:
                    path = path_match.group(1)
                    endpoints.append({
                        "method": method,
                        "endpoint": path,
                        "source": "text_search",
                        "line": i + 1
                    })
        
        return endpoints

    def _regex_search(self, content: str) -> List[Dict]:
        """Regex поиск эндпоинтов"""
        endpoints = []
        
        patterns = [
            # Стандартный формат: @router.get("/path")
            r'@router\.(get|post|put|delete)\(\s*["\']([^"\']+)["\']',
            # С пробелами: @router.get( "/path" )
            r'@router\.(get|post|put|delete)\(\s*["\']([^"\']+)["\']\s*\)',
            # С дополнительными параметрами: @router.get("/path", response_model=X)
            r'@router\.(get|post|put|delete)\([^)]*["\']([^"\']+)["\'][^)]*\)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            for method, endpoint in matches:
                endpoints.append({
                    "method": method.upper(),
                    "endpoint": endpoint,
                    "source": "regex",
                    "pattern": pattern
                })
        
        return endpoints

    def _ast_search(self, content: str) -> List[Dict]:
        """AST анализ эндпоинтов"""
        endpoints = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            # Проверяем, что это вызов router метода
                            if (isinstance(decorator.func, ast.Attribute) and
                                hasattr(decorator.func, 'attr') and
                                decorator.func.attr in ['get', 'post', 'put', 'delete']):
                                
                                method = decorator.func.attr.upper()
                                
                                # Ищем строковые аргументы (пути)
                                for arg in decorator.args:
                                    endpoint_path = None
                                    
                                    # Python < 3.8
                                    if isinstance(arg, ast.Str):
                                        endpoint_path = arg.s
                                    # Python >= 3.8  
                                    elif (hasattr(ast, 'Constant') and 
                                          isinstance(arg, ast.Constant) and 
                                          isinstance(arg.value, str)):
                                        endpoint_path = arg.value
                                    
                                    if endpoint_path:
                                        endpoints.append({
                                            "method": method,
                                            "endpoint": endpoint_path,
                                            "source": "ast",
                                            "function": node.name
                                        })
        except Exception as e:
            logger.debug(f"AST анализ не удался: {e}")
        
        return endpoints

    # ... (остальные методы остаются без изменений)

def main():
    """Основная функция"""
    print("🚀 ЗАПУСК ВЕРСИИ 8.0 КОМПЛЕКСНОГО ТЕСТА")
    print("РАДИКАЛЬНОЕ ИСПРАВЛЕНИЕ ОБНАРУЖЕНИЯ ЭНДПОИНТОВ")
    
    try:
        input("\nНажмите Enter для начала тестирования...")
    except KeyboardInterrupt:
        print("\n❌ Тестирование прервано пользователем")
        sys.exit(1)
    
    tester = ComprehensiveProjectTest()
    success = tester.run_comprehensive_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()