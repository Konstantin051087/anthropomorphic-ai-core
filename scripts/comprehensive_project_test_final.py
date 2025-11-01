# scripts/comprehensive_project_test_final.py
#!/usr/bin/env python3
"""
ФИНАЛЬНЫЙ ТЕСТ ПРОЕКТА С УЧЕТОМ ПРЕФИКСА API
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List
import urllib.request
import urllib.error
import time
import re

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class FinalProjectTest:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.api_prefix = "/api/v1"  # ✅ Учитываем префикс
        self.test_results = {
            "project": "Anthropomorphic AI Core",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_prefix": self.api_prefix,
            "overall_status": "IN_PROGRESS",
            "score": {"total_tests": 0, "passed_tests": 0, "success_rate": 0}
        }

    def print_header(self, message: str):
        print(f"\n{'='*80}")
        print(f"🔍 {message}")
        print(f"{'='*80}")

    def print_result(self, test_name: str, status: bool, details: str = ""):
        icon = "✅" if status else "❌"
        status_text = "ВЫПОЛНЕНО" if status else "НЕ ВЫПОЛНЕНО"
        print(f"{icon} {test_name}: {status_text}")
        if details:
            print(f"   📝 {details}")
        
        self.test_results["score"]["total_tests"] += 1
        if status:
            self.test_results["score"]["passed_tests"] += 1

    def test_api_endpoints_with_prefix(self):
        """Тестирование API эндпоинтов с учетом префикса"""
        self.print_header("🎯 ТЕСТИРОВАНИЕ API ЭНДПОИНТОВ (С ПРЕФИКСОМ)")
        
        # Тестируемые эндпоинты
        test_cases = [
            ("GET", "/", "Корневой эндпоинт (без префикса)"),
            ("GET", "/health", "Health check (без префикса)"),
            ("GET", f"{self.api_prefix}/state", "System state"),
            ("GET", f"{self.api_prefix}/modules", "Active modules"),
            ("GET", f"{self.api_prefix}/system/info", "System info"),
            ("POST", f"{self.api_prefix}/chat", "Chat endpoint"),
        ]
        
        working_count = 0
        for method, endpoint, description in test_cases:
            if self.test_single_endpoint(method, endpoint):
                self.print_result(f"{method} {endpoint}", True, description)
                working_count += 1
            else:
                self.print_result(f"{method} {endpoint}", False, f"{description} - не отвечает")
        
        self.print_result("Работоспособность API", working_count > 0, 
                         f"{working_count}/{len(test_cases)} эндпоинтов работают")
        
        return working_count == len(test_cases)

    def test_single_endpoint(self, method: str, endpoint: str) -> bool:
        """Тестирование одного эндпоинта"""
        try:
            url = f"http://localhost:8000{endpoint}"
            req = urllib.request.Request(url, method=method)
            req.add_header('User-Agent', 'Project-Test')
            req.add_header('Content-Type', 'application/json')
            
            # Для POST запросов добавляем тестовые данные
            if method == "POST":
                import json
                test_data = json.dumps({"message": "test"}).encode('utf-8')
                req.data = test_data
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except urllib.error.HTTPError as e:
            # 404 и другие ошибки считаем неудачей
            return False
        except Exception as e:
            return False

    def check_routes_integration(self):
        """Проверка интеграции routes в app.py"""
        self.print_header("🔗 ПРОВЕРКА ИНТЕГРАЦИИ APP.PY")
        
        app_file = self.base_dir / "api" / "app.py"
        if not app_file.exists():
            self.print_result("Файл app.py", False, "Не найден")
            return False
        
        content = app_file.read_text()
        
        checks = [
            ("Импорт router", "from api.routes import router" in content),
            ("Подключение router", "app.include_router(router" in content),
            ("Префикс /api/v1", 'prefix="/api/v1"' in content or "prefix='/api/v1'" in content),
        ]
        
        all_passed = True
        for check_name, status in checks:
            self.print_result(check_name, status)
            if not status:
                all_passed = False
        
        return all_passed

    def run_comprehensive_test(self):
        """Запуск комплексного тестирования"""
        self.print_header("🚀 ФИНАЛЬНЫЙ ТЕСТ ПРОЕКТА ANTHROPOMORPHIC AI")
        
        # Проверка интеграции
        integration_ok = self.check_routes_integration()
        if not integration_ok:
            self.print_result("Исправление интеграции", False, "Требуется исправить app.py")
            return False
        
        # Проверка API эндпоинтов
        api_ok = self.test_api_endpoints_with_prefix()
        
        # Расчет результатов
        total = self.test_results["score"]["total_tests"]
        passed = self.test_results["score"]["passed_tests"]
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        self.test_results["score"]["success_rate"] = round(success_rate, 2)
        
        self.print_header("📊 ФИНАЛЬНЫЙ ОТЧЕТ")
        print(f"✅ ВЫПОЛНЕНО ТЕСТОВ: {passed}/{total}")
        print(f"📈 УСПЕШНОСТЬ: {success_rate:.2f}%")
        print(f"🎯 ПРЕФИКС API: {self.api_prefix}")
        
        if success_rate >= 90:
            print("🎉 ПРОЕКТ ГОТОВ К ДЕПЛОЮ!")
            self.test_results["overall_status"] = "READY"
            return True
        else:
            print("🔧 ТРЕБУЮТСЯ ДОПОЛНИТЕЛЬНЫЕ ИСПРАВЛЕНИЯ")
            self.test_results["overall_status"] = "NEEDS_FIXES"
            return False

def main():
    print("🚀 ЗАПУСК ФИНАЛЬНОГО ТЕСТА ПРОЕКТА")
    print("📌 С УЧЕТОМ ПРЕФИКСА API /api/v1")
    
    try:
        input("\nНажмите Enter для начала тестирования...")
    except KeyboardInterrupt:
        print("\n❌ Тестирование прервано пользователем")
        sys.exit(1)
    
    tester = FinalProjectTest()
    success = tester.run_comprehensive_test()
    
    # Сохранение отчета
    report_file = tester.base_dir / "final_test_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(tester.test_results, f, indent=2, ensure_ascii=False)
    print(f"💾 Отчет сохранен в: {report_file}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()