#!/usr/bin/env python3
"""
ИСПРАВЛЕННЫЙ КОМПЛЕКСНЫЙ ТЕСТ ЭТАПА 1.3
С улучшенной диагностикой проблем
"""

import os
import sys
import json
import logging
import importlib.metadata
from pathlib import Path
from typing import Dict, List
import urllib.request
import urllib.error

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class FixedStage1Test:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.test_results = {
            "stage": "1.3 - Настройка инфраструктуры (Исправленная версия)",
            "overall_status": "PENDING",
            "details": {}
        }

    def print_header(self, message: str):
        print(f"\n{'='*60}")
        print(f"🔍 {message}")
        print(f"{'='*60}")

    def print_result(self, test_name: str, status: bool, details: str = ""):
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}: {'ПРОЙДЕН' if status else 'НЕ ПРОЙДЕН'}")
        if details:
            print(f"   📝 {details}")

    def test_health_endpoint_fixed(self):
        """Исправленный тест health эндпоинта с детальной диагностикой"""
        self.print_header("ТЕСТ HEALTH ЭНДПОИНТА С ДИАГНОСТИКОЙ")
        
        base_url = "http://localhost:8000"
        health_url = f"{base_url}/api/v1/health"
        
        try:
            # Создаем запрос с таймаутом
            req = urllib.request.Request(health_url, method='GET')
            req.add_header('User-Agent', 'Stage1-Test/1.0')
            req.add_header('Accept', 'application/json')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                # Читаем сырые данные
                raw_data = response.read().decode('utf-8')
                status_code = response.status
                content_type = response.headers.get('Content-Type', 'Unknown')
                
                print(f"📊 Статус ответа: {status_code}")
                print(f"📄 Content-Type: {content_type}")
                print(f"📏 Длина ответа: {len(raw_data)} байт")
                print(f"📋 Первые 500 символов ответа: {raw_data[:500]}...")
                
                # Пытаемся распарсить JSON
                try:
                    if not raw_data.strip():
                        self.print_result("Health Endpoint", False, "Пустой ответ от сервера")
                        return False
                    
                    data = json.loads(raw_data)
                    
                    # Проверяем структуру ответа
                    required_fields = ["status", "service", "version"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.print_result("Health Endpoint", False, f"Отсутствуют поля: {missing_fields}")
                        return False
                    
                    self.print_result("Health Endpoint", True, f"Статус: {data.get('status')}, Версия: {data.get('version')}")
                    return True
                    
                except json.JSONDecodeError as e:
                    self.print_result("Health Endpoint", False, f"Ошибка JSON: {e}. Сырой ответ: '{raw_data}'")
                    return False
                    
        except urllib.error.HTTPError as e:
            self.print_result("Health Endpoint", False, f"HTTP ошибка: {e.code} {e.reason}")
            try:
                error_body = e.read().decode('utf-8')
                print(f"📋 Тело ошибки: {error_body[:500]}...")
            except:
                pass
            return False
            
        except urllib.error.URLError as e:
            self.print_result("Health Endpoint", False, f"URL ошибка: {e.reason}")
            return False
            
        except Exception as e:
            self.print_result("Health Endpoint", False, f"Неожиданная ошибка: {e}")
            return False

    def test_api_endpoints_comprehensive(self):
        """Комплексный тест всех API эндпоинтов"""
        self.print_header("КОМПЛЕКСНЫЙ ТЕСТ API ЭНДПОИНТОВ")
        
        base_url = "http://localhost:8000"
        endpoints = [
            ("/", "GET", "Root Endpoint"),
            ("/api/v1/health", "GET", "Health Check"), 
            ("/api/v1/state", "GET", "System State"),
            ("/docs", "GET", "API Documentation")
        ]
        
        results = {}
        
        for endpoint, method, description in endpoints:
            url = base_url + endpoint
            try:
                req = urllib.request.Request(url, method=method)
                req.add_header('Accept', 'application/json')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    status_code = response.status
                    content_type = response.headers.get('Content-Type', '')
                    
                    # Для JSON endpoints проверяем валидность
                    if 'application/json' in content_type:
                        try:
                            raw_data = response.read().decode('utf-8')
                            data = json.loads(raw_data)
                            results[endpoint] = {
                                "status": "SUCCESS", 
                                "http_status": status_code,
                                "content_type": content_type,
                                "data_keys": list(data.keys()) if isinstance(data, dict) else "N/A"
                            }
                            self.print_result(f"{description} ({endpoint})", True, f"Status: {status_code}, Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                        except json.JSONDecodeError:
                            results[endpoint] = {"status": "INVALID_JSON", "http_status": status_code}
                            self.print_result(f"{description} ({endpoint})", False, f"Status: {status_code} - Invalid JSON")
                    else:
                        results[endpoint] = {"status": "SUCCESS", "http_status": status_code, "content_type": content_type}
                        self.print_result(f"{description} ({endpoint})", True, f"Status: {status_code}, Type: {content_type}")
                        
            except Exception as e:
                results[endpoint] = {"status": "ERROR", "error": str(e)}
                self.print_result(f"{description} ({endpoint})", False, f"Error: {e}")
        
        # Считаем тест пройденным, если основные эндпоинты работают
        critical_endpoints = ["/api/v1/health", "/api/v1/state"]
        critical_success = all(
            results.get(endpoint, {}).get("status") == "SUCCESS" 
            for endpoint in critical_endpoints
        )
        
        self.test_results["details"]["api_endpoints"] = results
        return critical_success

    def run_diagnostic_test(self):
        """Запуск диагностического теста"""
        self.print_header("🚀 ДИАГНОСТИЧЕСКИЙ ТЕСТ ЭТАПА 1.3")
        
        print("Проверка специфической проблемы с health эндпоинтом...")
        
        # Тестируем health эндпоинт с улучшенной диагностикой
        health_ok = self.test_health_endpoint_fixed()
        
        # Если health не работает, запускаем полный тест API для диагностики
        if not health_ok:
            print("\n" + "🩺" * 20)
            print("ЗАПУСК РАСШИРЕННОЙ ДИАГНОСТИКИ API")
            print("🩺" * 20)
            api_ok = self.test_api_endpoints_comprehensive()
        else:
            api_ok = True
        
        # Финальный вердикт
        self.test_results["overall_status"] = "PASSED" if health_ok else "FAILED"
        
        self.print_header("📊 ДИАГНОСТИЧЕСКИЙ ОТЧЕТ")
        
        if health_ok:
            print("✅ HEALTH ЭНДПОИНТ РАБОТАЕТ КОРРЕКТНО")
            print("🎉 ЭТАП 1.3 ЗАВЕРШЕН УСПЕШНО")
        else:
            print("❌ ОБНАРУЖЕНА ПРОБЛЕМА С HEALTH ЭНДПОИНТОМ")
            print("\nВОЗМОЖНЫЕ ПРИЧИНЫ:")
            print("1. Сервер не запущен или недоступен")
            print("2. Эндпоинт возвращает не-JSON данные") 
            print("3. Ошибка в коде эндпоинта /api/v1/health")
            print("4. Проблемы с маршрутизацией в FastAPI")
            print("\nРЕКОМЕНДАЦИИ:")
            print("1. Убедитесь, что сервер запущен: python api/app.py")
            print("2. Проверьте код эндпоинта health в api/routes.py")
            print("3. Проверьте маршрутизацию в api/app.py")
            print("4. Проверьте логи сервера для деталей ошибки")
        
        return health_ok

def main():
    """Основная функция"""
    print("🩺 ДИАГНОСТИЧЕСКИЙ ТЕСТ ДЛЯ ЭТАПА 1.3")
    print("Определение проблемы с health эндпоинтом")
    
    tester = FixedStage1Test()
    success = tester.run_diagnostic_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()