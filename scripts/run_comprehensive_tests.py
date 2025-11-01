#!/usr/bin/env python3
"""
Комплексный тестовый скрипт для проверки всей системы
"""

import sys
import os
import time
import requests
import subprocess
import threading
from pathlib import Path

# Добавление корневой директории в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_server():
    """Запуск сервера в отдельном процессе"""
    try:
        subprocess.run([sys.executable, "api/app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка запуска сервера: {e}")

def test_api_endpoints():
    """Тестирование API endpoints"""
    base_url = "http://localhost:8000"
    endpoints = [
        ("GET", "/", {}),
        ("GET", "/health", {}),
        ("GET", "/api/v1/", {}),
        ("GET", "/api/v1/health", {}),
        ("GET", "/api/v1/state", {}),
        ("GET", "/api/v1/modules", {}),
        ("POST", "/api/v1/chat", {"json": {"message": "Привет"}}),
        ("POST", "/api/v1/memory/store", {"json": {"content": "Тест", "memory_type": "fact", "importance": 5.0}}),
        ("POST", "/api/v1/memory/recall", {"json": {"query": "тест", "limit": 5}}),
        ("POST", "/api/v1/mood/update", {"json": {"mood": "happy", "intensity": 0.8}}),
        ("POST", "/api/v1/personality/update", {"json": {"trait": "openness", "value": 0.9}}),
    ]
    
    print("\n" + "="*50)
    print("ТЕСТИРОВАНИЕ API ENDPOINTS")
    print("="*50)
    
    all_passed = True
    
    for method, endpoint, kwargs in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=10, **kwargs)
            
            if response.status_code == 200:
                print(f"✓ {method} {endpoint} - {response.status_code}")
            else:
                print(f"✗ {method} {endpoint} - {response.status_code}: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"✗ {method} {endpoint} - ошибка: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Основная функция"""
    print("="*60)
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ")
    print("="*60)
    
    # Проверка зависимостей
    print("\n1. Проверка зависимостей...")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✓ Все основные зависимости установлены")
    except ImportError as e:
        print(f"✗ Отсутствует зависимость: {e}")
        return False
    
    # Запуск сервера в отдельном потоке
    print("\n2. Запуск сервера...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Даем время серверу запуститься
    print("   Ожидание запуска сервера (5 секунд)...")
    time.sleep(5)
    
    # Тестирование endpoints
    print("\n3. Тестирование API endpoints...")
    if test_api_endpoints():
        print("✓ Все endpoints работают корректно")
    else:
        print("✗ Некоторые endpoints имеют проблемы")
        return False
    
    # Запуск unit-тестов
    print("\n4. Запуск unit-тестов...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Все unit-тесты пройдены")
        else:
            print(f"✗ Unit-тесты не пройдены: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Unit-тесты превысили время выполнения")
        return False
    except Exception as e:
        print(f"✗ Ошибка запуска unit-тестов: {e}")
        return False
    
    print("\n" + "="*60)
    print("✓ ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
    print("="*60)
    print("\nСистема готова к работе!")
    print("Сервер запущен на http://localhost:8000")
    print("Документация API: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)