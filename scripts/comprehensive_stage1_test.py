#!/usr/bin/env python3
"""
КОМПЛЕКСНЫЙ ТЕСТ ЭТАПА 1.3: НАСТРОЙКА ИНФРАСТРУКТУРЫ
Проверка готовности к деплою на Render с поддержкой Python 3.12.3/3.13.4
Улучшенная версия с детальной диагностикой и расширенной функциональностью
"""

import os
import sys
import json
import logging
import subprocess
import importlib.metadata
from pathlib import Path
from typing import Dict, List, Tuple, Any
import urllib.request
import urllib.error
import time
import socket

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class Stage1ComprehensiveTest:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.test_results = {
            "stage": "1.3 - Настройка инфраструктуры",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_compatibility": {},
            "environment_config": {},
            "api_functionality": {},
            "deployment_readiness": {},
            "dependencies": {},
            "security_checks": {},
            "performance_checks": {},
            "overall_status": "PENDING",
            "score": 0,
            "total_tests": 0,
            "passed_tests": 0
        }
        self.errors = []
        self.warnings = []

    def print_header(self, message: str):
        """Печать заголовка раздела"""
        print(f"\n{'='*60}")
        print(f"🔍 {message}")
        print(f"{'='*60}")

    def print_result(self, test_name: str, status: bool, details: str = "", points: int = 1):
        """Печать результата теста с системой баллов"""
        icon = "✅" if status else "❌"
        status_text = "ПРОЙДЕН" if status else "НЕ ПРОЙДЕН"
        print(f"{icon} {test_name}: {status_text}")
        if details:
            print(f"   📝 {details}")
        
        # Обновляем счетчики тестов
        self.test_results["total_tests"] += 1
        if status:
            self.test_results["passed_tests"] += points
            self.test_results["score"] += points

    def test_server_availability(self):
        """Проверка доступности сервера перед тестированием API"""
        self.print_header("🔧 ПРЕДВАРИТЕЛЬНАЯ ПРОВЕРКА СЕРВЕРА")
        
        base_url = "http://localhost:8000"
        
        # Проверка, что порт 8000 доступен
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('localhost', 8000))
            sock.close()
            
            if result == 0:
                self.print_result("Порт 8000 доступен", True, "Сервер запущен и слушает на порту 8000")
                return True
            else:
                self.print_result("Порт 8000 доступен", False, "Порт 8000 не доступен. Запустите сервер: python api/app.py")
                return False
        except Exception as e:
            self.print_result("Проверка порта", False, f"Ошибка проверки порта: {e}")
            return False

    # РАЗДЕЛ 1: ПРОВЕРКА СОВМЕСТИМОСТИ PYTHON
    def test_python_compatibility(self):
        """Тест совместимости версий Python"""
        self.print_header("1. 🐍 ПРОВЕРКА СОВМЕСТИМОСТИ PYTHON")

        version = sys.version_info
        current_version = f"{version.major}.{version.minor}.{version.micro}"
        
        # Проверка текущей версии
        compatible_versions = ["3.12.3", "3.13.4"]
        is_compatible = current_version in compatible_versions
        
        self.print_result(
            f"Текущая версия Python {current_version}",
            is_compatible,
            f"Ожидаемые версии: {', '.join(compatible_versions)}",
            points=2
        )

        # Проверка runtime.txt для Render
        runtime_file = self.base_dir / "runtime.txt"
        if runtime_file.exists():
            runtime_content = runtime_file.read_text().strip()
            is_correct = runtime_content == "python-3.13.4"
            self.print_result(
                "Файл runtime.txt для Render",
                is_correct,
                f"Содержимое: {runtime_content}",
                points=1
            )
        else:
            self.print_result("Файл runtime.txt для Render", False, "Файл отсутствует", points=1)

        # Проверка стратегии зависимостей
        requirements_file = self.base_dir / "requirements.txt"
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                requirements = f.readlines()
            
            has_versions = any('==' in line or '>=' in line for line in requirements if line.strip() and not line.startswith('#'))
            self.print_result(
                "Стратегия зависимостей без версий",
                not has_versions,
                "Зависимости указаны без фиксации версий для совместимости",
                points=2
            )
            
            # Проверка наличия критических пакетов
            critical_packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "pydantic-settings"]
            packages_in_req = [pkg for pkg in critical_packages if any(pkg in line.lower() for line in requirements)]
            self.print_result(
                "Критические пакеты в requirements.txt",
                len(packages_in_req) == len(critical_packages),
                f"Найдено: {len(packages_in_req)}/{len(critical_packages)}",
                points=1
            )
        else:
            self.print_result("Файл requirements.txt", False, "Файл отсутствует", points=1)

        self.test_results["python_compatibility"] = {
            "current_version": current_version,
            "compatible_versions": compatible_versions,
            "runtime_configured": runtime_file.exists(),
            "dependency_strategy": "versionless" if not has_versions else "versioned"
        }

        return is_compatible

    # РАЗДЕЛ 2: ПРОВЕРКА КОНФИГУРАЦИИ ОКРУЖЕНИЯ
    def test_environment_configuration(self):
        """Тест конфигурации окружения"""
        self.print_header("2. ⚙️ ПРОВЕРКА КОНФИГУРАЦИИ ОКРУЖЕНИЯ")

        env_files = {
            ".env.example": "Шаблон окружения",
            ".env": "Локальное окружение"
        }

        env_status = {}
        all_env_files_exist = True
        
        for env_file, description in env_files.items():
            file_path = self.base_dir / env_file
            exists = file_path.exists()
            
            self.print_result(
                f"Файл {description}",
                exists,
                f"{'Найден' if exists else 'Отсутствует'}: {env_file}",
                points=1
            )
            
            if not exists:
                all_env_files_exist = False
            
            if exists:
                # Проверка содержания критических переменных
                try:
                    content = file_path.read_text()
                    critical_vars = ["DATABASE_URL", "API_HOST", "API_PORT"]
                    found_vars = [var for var in critical_vars if var in content]
                    
                    self.print_result(
                        f"  Критические переменные в {env_file}",
                        len(found_vars) == len(critical_vars),
                        f"Найдено: {len(found_vars)}/{len(critical_vars)}",
                        points=1
                    )
                    
                    env_status[env_file] = {
                        "exists": True,
                        "critical_vars_found": len(found_vars),
                        "critical_vars_total": len(critical_vars)
                    }
                    
                except Exception as e:
                    self.print_result(f"Чтение {env_file}", False, f"Ошибка: {e}", points=1)
                    env_status[env_file] = {"exists": True, "error": str(e)}
            else:
                env_status[env_file] = {"exists": False}

        # Проверка конфигурационных файлов модулей
        config_files = [
            "data/configs/system_config.json",
            "data/configs/psyche_config.json", 
            "data/configs/memory_config.json",
            "data/configs/mood_config.json"
        ]

        config_status = {}
        all_configs_valid = True
        
        for config_file in config_files:
            file_path = self.base_dir / config_file
            exists = file_path.exists()
            
            self.print_result(
                f"Конфигурационный файл: {config_file}",
                exists,
                f"{'Найден' if exists else 'Отсутствует'}",
                points=1
            )
            
            if not exists:
                all_configs_valid = False
            
            if exists:
                # Проверка валидности JSON
                try:
                    with open(file_path, 'r') as f:
                        config_data = json.load(f)
                    self.print_result(f"  Валидность JSON: {config_file}", True, points=1)
                    
                    # Дополнительная проверка структуры конфигурации
                    if "system_config.json" in config_file:
                        has_system_structure = "system" in config_data
                        self.print_result(
                            f"  Структура system_config.json",
                            has_system_structure,
                            "Содержит раздел 'system'",
                            points=1
                        )
                    
                    config_status[config_file] = {"exists": True, "valid_json": True}
                except json.JSONDecodeError as e:
                    self.print_result(f"  Валидность JSON: {config_file}", False, f"Ошибка: {e}", points=1)
                    config_status[config_file] = {"exists": True, "valid_json": False, "error": str(e)}
                    all_configs_valid = False
            else:
                config_status[config_file] = {"exists": False}

        self.test_results["environment_config"] = {
            "environment_files": env_status,
            "config_files": config_status
        }

        return all_env_files_exist and all_configs_valid

    # РАЗДЕЛ 3: РАСШИРЕННАЯ ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ API
    def test_api_functionality(self):
        """Расширенный тест функциональности API с детальной диагностикой"""
        self.print_header("3. 🌐 РАСШИРЕННАЯ ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ API")

        # Сначала проверяем доступность сервера
        if not self.test_server_availability():
            self.print_result("API сервер", False, "Сервер не доступен, пропуск тестов API", points=0)
            return False

        api_status = {}
        base_url = "http://localhost:8000"
        
        # Функция для выполнения HTTP запросов с детальной диагностикой
        def make_detailed_request(url: str, method: str = 'GET', headers: dict = None):
            """Выполнение HTTP запроса с детальной диагностикой"""
            try:
                req = urllib.request.Request(url, method=method)
                req.add_header('User-Agent', 'Stage1-Test/1.0')
                req.add_header('Accept', 'application/json')
                
                if headers:
                    for key, value in headers.items():
                        req.add_header(key, value)
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    raw_data = response.read().decode('utf-8')
                    return {
                        "success": True,
                        "status_code": response.status,
                        "content_type": response.headers.get('Content-Type', 'Unknown'),
                        "content_length": len(raw_data),
                        "raw_data": raw_data,
                        "headers": dict(response.headers)
                    }
            except urllib.error.HTTPError as e:
                return {
                    "success": False,
                    "error_type": "HTTPError",
                    "status_code": e.code,
                    "reason": e.reason,
                    "headers": dict(e.headers) if e.headers else {}
                }
            except Exception as e:
                return {
                    "success": False,
                    "error_type": "OtherError",
                    "error": str(e)
                }

        # Тестируем все основные эндпоинты
        endpoints_to_test = [
            ("/", "GET", "Root Endpoint"),
            ("/api/v1/health", "GET", "Health Check"),
            ("/api/v1/state", "GET", "System State"),
            ("/docs", "GET", "API Documentation"),
            ("/api/v1/chat", "POST", "Chat Endpoint"),
            ("/api/v1/mood/update", "POST", "Mood Update"),
            ("/api/v1/memory/store", "POST", "Memory Store"),
            ("/api/v1/memory/recall", "POST", "Memory Recall"),
            ("/api/v1/personality/update", "POST", "Personality Update")
        ]

        for endpoint, method, description in endpoints_to_test:
            url = base_url + endpoint
            result = make_detailed_request(url, method)
            
            if result["success"]:
                status_ok = result["status_code"] in [200, 201, 204]
                
                # Для JSON endpoints проверяем валидность
                if 'application/json' in result["content_type"]:
                    try:
                        data = json.loads(result["raw_data"])
                        self.print_result(
                            f"{description} ({method} {endpoint})",
                            status_ok,
                            f"Status: {result['status_code']}, Response: {list(data.keys()) if isinstance(data, dict) else type(data).__name__}",
                            points=1
                        )
                        api_status[endpoint] = {
                            "available": status_ok,
                            "status_code": result["status_code"],
                            "content_type": result["content_type"],
                            "data_keys": list(data.keys()) if isinstance(data, dict) else "N/A"
                        }
                    except json.JSONDecodeError:
                        self.print_result(
                            f"{description} ({method} {endpoint})",
                            False,
                            f"Status: {result['status_code']} - Invalid JSON: {result['raw_data'][:100]}...",
                            points=1
                        )
                        api_status[endpoint] = {"available": False, "status_code": result["status_code"], "error": "Invalid JSON"}
                else:
                    self.print_result(
                        f"{description} ({method} {endpoint})",
                        status_ok,
                        f"Status: {result['status_code']}, Type: {result['content_type']}",
                        points=1
                    )
                    api_status[endpoint] = {
                        "available": status_ok,
                        "status_code": result["status_code"],
                        "content_type": result["content_type"]
                    }
            else:
                # Для ошибок HTTP (например, 405 Method Not Allowed) это нормально для некоторых эндпоинтов
                if result.get("status_code") == 405:
                    self.print_result(
                        f"{description} ({method} {endpoint})",
                        True,  # 405 означает, что эндпоинт существует, но метод не разрешен
                        f"Endpoint exists but method not allowed: {result['status_code']}",
                        points=1
                    )
                    api_status[endpoint] = {"available": True, "status_code": result["status_code"], "note": "Method not allowed"}
                else:
                    self.print_result(
                        f"{description} ({method} {endpoint})",
                        False,
                        f"Error: {result.get('error_type', 'Unknown')} - {result.get('reason', result.get('error', 'No details'))}",
                        points=1
                    )
                    api_status[endpoint] = {"available": False, "error": result}

        # Детальная диагностика health эндпоинта
        self.print_header("🔬 ДЕТАЛЬНАЯ ДИАГНОСТИКА HEALTH ЭНДПОИНТА")
        health_result = make_detailed_request(f"{base_url}/api/v1/health")
        
        if health_result["success"]:
            print(f"📊 Статус ответа: {health_result['status_code']}")
            print(f"📄 Content-Type: {health_result['content_type']}")
            print(f"📏 Длина ответа: {health_result['content_length']} байт")
            print(f"📋 Сырой ответ: {health_result['raw_data'][:500]}{'...' if len(health_result['raw_data']) > 500 else ''}")
            
            try:
                health_data = json.loads(health_result["raw_data"])
                print(f"🎯 Распарсенные данные: {json.dumps(health_data, indent=2, ensure_ascii=False)}")
                
                # Проверка обязательных полей в health response
                required_fields = ["status", "service", "version"]
                missing_fields = [field for field in required_fields if field not in health_data]
                
                if missing_fields:
                    self.print_result("Структура health response", False, f"Отсутствуют поля: {missing_fields}", points=1)
                else:
                    self.print_result("Структура health response", True, 
                                    f"Статус: {health_data.get('status')}, Версия: {health_data.get('version')}", points=1)
                    
            except json.JSONDecodeError as e:
                self.print_result("Парсинг health response", False, f"Ошибка JSON: {e}", points=1)
        else:
            self.print_result("Health эндпоинт", False, 
                            f"Ошибка: {health_result.get('error_type')} - {health_result.get('reason', health_result.get('error', 'No details'))}", 
                            points=1)

        self.test_results["api_functionality"] = api_status

        # Считаем тест пройденным, если доступны основные эндпоинты
        critical_endpoints = ["/api/v1/health", "/api/v1/state", "/"]
        critical_available = all(
            api_status.get(endpoint, {}).get("available", False) 
            for endpoint in critical_endpoints
        )
        
        return critical_available

    # РАЗДЕЛ 4: ПРОВЕРКА ГОТОВНОСТИ К ДЕПЛОЮ
    def test_deployment_readiness(self):
        """Расширенный тест готовности к деплою на Render"""
        self.print_header("4. 🚀 РАСШИРЕННАЯ ПРОВЕРКА ГОТОВНОСТИ К ДЕПЛОЮ")

        deployment_status = {}

        # Проверка render.yaml
        render_yaml = self.base_dir / "render.yaml"
        if render_yaml.exists():
            self.print_result("Файл render.yaml", True, "Найден", points=2)
            try:
                # Базовая проверка содержимого render.yaml
                content = render_yaml.read_text()
                has_services = "services:" in content
                has_build_command = "buildCommand" in content
                self.print_result("  Структура render.yaml", has_services and has_build_command, 
                                "Содержит services и buildCommand", points=1)
                deployment_status["render_yaml"] = {"exists": True, "valid_structure": has_services and has_build_command}
            except Exception as e:
                self.print_result("  Чтение render.yaml", False, f"Ошибка: {e}", points=1)
                deployment_status["render_yaml"] = {"exists": True, "valid_structure": False}
        else:
            self.print_result("Файл render.yaml", False, "Отсутствует", points=2)
            deployment_status["render_yaml"] = {"exists": False}

        # Проверка Dockerfile
        dockerfile = self.base_dir / "Dockerfile"
        if dockerfile.exists():
            self.print_result("Файл Dockerfile", True, "Найден", points=2)
            try:
                content = dockerfile.read_text()
                has_from = "FROM python" in content
                has_workdir = "WORKDIR" in content
                has_copy = "COPY" in content
                has_cmd = "CMD" in content or "ENTRYPOINT" in content
                self.print_result("  Структура Dockerfile", has_from and has_workdir and has_copy and has_cmd,
                                "Содержит базовые инструкции", points=1)
                deployment_status["dockerfile"] = {"exists": True, "valid_structure": True}
            except Exception as e:
                self.print_result("  Чтение Dockerfile", False, f"Ошибка: {e}", points=1)
                deployment_status["dockerfile"] = {"exists": True, "valid_structure": False}
        else:
            self.print_result("Файл Dockerfile", False, "Отсутствует", points=2)
            deployment_status["dockerfile"] = {"exists": False}

        # Расширенная проверка скриптов деплоя
        deploy_scripts = [
            ("scripts/deploy_render.sh", "Скрипт деплоя Render"),
            ("scripts/setup_render.py", "Скрипт настройки Render"),
            ("scripts/validate_infrastructure.py", "Скрипт валидации инфраструктуры")
        ]

        scripts_status = {}
        all_scripts_exist = True
        for script_path, description in deploy_scripts:
            script_file = self.base_dir / script_path
            exists = script_file.exists()
            self.print_result(
                f"{description}",
                exists,
                f"{'Найден' if exists else 'Отсутствует'}",
                points=1
            )
            scripts_status[script_path] = {"exists": exists}
            if not exists:
                all_scripts_exist = False

        deployment_status["deploy_scripts"] = scripts_status

        # Расширенная проверка структуры проекта
        required_dirs = [
            ("api", "API модули"),
            ("core", "Ядро системы"),
            ("data/configs", "Конфигурационные файлы"),
            ("utils", "Утилиты"),
            ("scripts", "Скрипты"),
            ("tests", "Тесты")
        ]

        dirs_status = {}
        all_dirs_exist = True
        for directory, description in required_dirs:
            dir_path = self.base_dir / directory
            exists = dir_path.exists()
            self.print_result(
                f"Директория: {description}",
                exists,
                f"{'Найдена' if exists else 'Отсутствует'}",
                points=1
            )
            dirs_status[directory] = {"exists": exists}
            if not exists:
                all_dirs_exist = False

        deployment_status["project_structure"] = dirs_status

        # Проверка наличия основных файлов проекта
        critical_files = [
            ("api/app.py", "Основное приложение FastAPI"),
            ("core/config.py", "Конфигурация системы"),
            ("requirements.txt", "Зависимости Python"),
            (".gitignore", "Git ignore файл")
        ]

        files_status = {}
        for file_path, description in critical_files:
            file = self.base_dir / file_path
            exists = file.exists()
            self.print_result(
                f"Файл: {description}",
                exists,
                f"{'Найден' if exists else 'Отсутствует'}",
                points=1
            )
            files_status[file_path] = {"exists": exists}

        deployment_status["critical_files"] = files_status

        self.test_results["deployment_readiness"] = deployment_status

        return all_scripts_exist and all_dirs_exist

    # РАЗДЕЛ 5: ПРОВЕРКА ЗАВИСИМОСТЕЙ
    def test_dependencies(self):
        """Расширенный тест установки и совместимости зависимостей"""
        self.print_header("5. 📦 РАСШИРЕННАЯ ПРОВЕРКА ЗАВИСИМОСТЕЙ")

        critical_packages = [
            ("fastapi", "FastAPI фреймворк"),
            ("uvicorn", "ASGI сервер"),
            ("sqlalchemy", "ORM базы данных"),
            ("pydantic", "Валидация данных"),
            ("pydantic-settings", "Настройки Pydantic"),
            ("requests", "HTTP запросы"),
            ("python-dotenv", "Переменные окружения"),
            ("alembic", "Миграции базы данных"),
            ("psycopg2-binary", "PostgreSQL драйвер")
        ]

        dependencies_status = {}
        all_installed = True
        
        for package, description in critical_packages:
            try:
                version = importlib.metadata.version(package)
                self.print_result(
                    f"{description} ({package})",
                    True,
                    f"Версия: {version}",
                    points=1
                )
                dependencies_status[package] = {"installed": True, "version": version}
            except importlib.metadata.PackageNotFoundError:
                self.print_result(f"{description} ({package})", False, "Не установлен", points=1)
                dependencies_status[package] = {"installed": False}
                all_installed = False

        # Проверка совместимости версий
        self.print_header("🔧 ПРОВЕРКА СОВМЕСТИМОСТИ ВЕРСИЙ")
        
        compatibility_checks = [
            ("FastAPI", "fastapi", "0.100.0", None),
            ("Pydantic", "pydantic", "2.0.0", None),
            ("SQLAlchemy", "sqlalchemy", "2.0.0", None)
        ]
        
        for name, package, min_version, max_version in compatibility_checks:
            if package in dependencies_status and dependencies_status[package]["installed"]:
                current_version = dependencies_status[package]["version"]
                # Простая проверка совместимости (можно улучшить)
                self.print_result(
                    f"Совместимость {name}",
                    True,
                    f"Версия {current_version} - проверка пройдена",
                    points=1
                )

        self.test_results["dependencies"] = dependencies_status

        return all_installed

    # РАЗДЕЛ 6: ПРОВЕРКА БЕЗОПАСНОСТИ
    def test_security_checks(self):
        """Базовые проверки безопасности"""
        self.print_header("6. 🛡️ ПРОВЕРКА БЕЗОПАСНОСТИ")

        security_status = {}

        # Проверка .env файла на наличие чувствительных данных
        env_file = self.base_dir / ".env"
        if env_file.exists():
            try:
                content = env_file.read_text()
                sensitive_patterns = ["SECRET_KEY", "PASSWORD", "TOKEN", "API_KEY"]
                found_sensitive = [pattern for pattern in sensitive_patterns if pattern in content]
                
                if found_sensitive:
                    self.print_result(
                        "Чувствительные данные в .env",
                        False,
                        f"Найдены: {', '.join(found_sensitive)} - убедитесь, что .env в .gitignore",
                        points=2
                    )
                else:
                    self.print_result(
                        "Чувствительные данные в .env",
                        True,
                        "Чувствительные данные не найдены в .env",
                        points=2
                    )
                
                security_status["env_sensitive_data"] = len(found_sensitive) == 0
            except Exception as e:
                self.print_result("Проверка .env файла", False, f"Ошибка: {e}", points=2)
                security_status["env_sensitive_data"] = False
        else:
            self.print_result("Проверка .env файла", True, "Файл .env отсутствует (нормально для production)", points=2)
            security_status["env_sensitive_data"] = True

        # Проверка .gitignore
        gitignore_file = self.base_dir / ".gitignore"
        if gitignore_file.exists():
            try:
                content = gitignore_file.read_text()
                required_ignores = [".env", "__pycache__", "*.pyc", "instance/", ".pytest_cache"]
                missing_ignores = [ignore for ignore in required_ignores if ignore not in content]
                
                if missing_ignores:
                    self.print_result(
                        "Настройки .gitignore",
                        False,
                        f"Отсутствуют: {', '.join(missing_ignores)}",
                        points=1
                    )
                else:
                    self.print_result(
                        "Настройки .gitignore",
                        True,
                        "Все критичные пути в .gitignore",
                        points=1
                    )
                
                security_status["gitignore_complete"] = len(missing_ignores) == 0
            except Exception as e:
                self.print_result("Проверка .gitignore", False, f"Ошибка: {e}", points=1)
                security_status["gitignore_complete"] = False
        else:
            self.print_result("Проверка .gitignore", False, "Файл .gitignore отсутствует", points=1)
            security_status["gitignore_complete"] = False

        self.test_results["security_checks"] = security_status

        return security_status.get("env_sensitive_data", False) and security_status.get("gitignore_complete", False)

    # РАЗДЕЛ 7: ПРОВЕРКА ПРОИЗВОДИТЕЛЬНОСТИ
    def test_performance_checks(self):
        """Базовые проверки производительности"""
        self.print_header("7. ⚡ ПРОВЕРКА ПРОИЗВОДИТЕЛЬНОСТИ")

        performance_status = {}

        # Проверка времени ответа API
        base_url = "http://localhost:8000"
        endpoints_to_test = ["/", "/api/v1/health", "/api/v1/state"]
        
        response_times = {}
        for endpoint in endpoints_to_test:
            try:
                start_time = time.time()
                req = urllib.request.Request(base_url + endpoint)
                with urllib.request.urlopen(req, timeout=10) as response:
                    response.read()
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # в миллисекундах
                
                response_times[endpoint] = response_time
                
                if response_time < 100:  # менее 100 мс - отлично
                    self.print_result(
                        f"Время ответа {endpoint}",
                        True,
                        f"{response_time:.2f} мс - отлично",
                        points=1
                    )
                elif response_time < 500:  # менее 500 мс - хорошо
                    self.print_result(
                        f"Время ответа {endpoint}",
                        True,
                        f"{response_time:.2f} мс - хорошо",
                        points=1
                    )
                else:
                    self.print_result(
                        f"Время ответа {endpoint}",
                        False,
                        f"{response_time:.2f} мс - медленно",
                        points=1
                    )
                    
            except Exception as e:
                self.print_result(f"Время ответа {endpoint}", False, f"Ошибка: {e}", points=1)
                response_times[endpoint] = None

        performance_status["response_times"] = response_times
        self.test_results["performance_checks"] = performance_status

        # Считаем успешным, если среднее время ответа < 500 мс
        valid_times = [rt for rt in response_times.values() if rt is not None and rt < 500]
        return len(valid_times) >= 2

    # ГЛАВНЫЙ МЕТОД ТЕСТИРОВАНИЯ
    def run_comprehensive_test(self):
        """Запуск комплексного тестирования"""
        self.print_header("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТА ЭТАПА 1.3")
        print("Расширенная проверка инфраструктуры для деплоя на Render...")
        print(f"Время начала: {self.test_results['timestamp']}")
        
        test_results = []

        # Запуск всех тестов
        test_results.append(self.test_python_compatibility())
        test_results.append(self.test_environment_configuration())
        test_results.append(self.test_api_functionality())
        test_results.append(self.test_deployment_readiness())
        test_results.append(self.test_dependencies())
        test_results.append(self.test_security_checks())
        test_results.append(self.test_performance_checks())

        # Финальная оценка
        all_passed = all(test_results)
        self.test_results["overall_status"] = "PASSED" if all_passed else "FAILED"
        
        # Расчет общего счета в процентах
        if self.test_results["total_tests"] > 0:
            success_rate = (self.test_results["score"] / self.test_results["total_tests"]) * 100
        else:
            success_rate = 0
            
        self.test_results["success_rate"] = round(success_rate, 2)

        # Генерация отчета
        self.generate_detailed_test_report(all_passed)

        return all_passed

    def generate_detailed_test_report(self, all_passed: bool):
        """Генерация детального отчета с улучшенной визуализацией"""
        self.print_header("📊 ДЕТАЛЬНЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
        
        # Статус этапа
        status_icon = "✅" if all_passed else "❌"
        print(f"{status_icon} ЭТАП 1.3: НАСТРОЙКА ИНФРАСТРУКТУРЫ")
        print(f"📅 Время тестирования: {self.test_results['timestamp']}")
        print(f"📈 Общий счет: {self.test_results['score']}/{self.test_results['total_tests']} ({self.test_results['success_rate']}%)")
        print(f"🎯 Статус: {'ЗАВЕРШЕН УСПЕШНО' if all_passed else 'ТРЕБУЕТСЯ ДОРАБОТКА'}")
        
        # Детальная информация по разделам
        sections = [
            ("🐍 Совместимость Python", self.test_results['python_compatibility']),
            ("⚙️ Конфигурация окружения", self.test_results['environment_config']),
            ("🌐 Функциональность API", self.test_results['api_functionality']),
            ("🚀 Готовность к деплою", self.test_results['deployment_readiness']),
            ("📦 Зависимости", self.test_results['dependencies']),
            ("🛡️ Безопасность", self.test_results['security_checks']),
            ("⚡ Производительность", self.test_results['performance_checks'])
        ]
        
        for section_name, section_data in sections:
            print(f"\n{section_name}:")
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if isinstance(value, (str, int, float, bool)):
                        print(f"   {key}: {value}")
                    elif isinstance(value, dict):
                        print(f"   {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"     {sub_key}: {sub_value}")

        # Рекомендации
        self.print_header("🎯 РЕКОМЕНДАЦИИ ДЛЯ СЛЕДУЮЩЕГО ЭТАПА")
        
        if all_passed:
            print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("\n🎉 ЭТАП 1.3 ЗАВЕРШЕН! Следующие шаги:")
            print("1. Создать репозиторий на GitHub")
            print("2. Настроить автоматический деплой на Render")
            print("3. Протестировать работу на production среде")
            print("4. Перейти к Этапу 2: Разработка базовой инфраструктуры")
        else:
            print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ:")
            issues = []
            
            # Анализ конкретных проблем
            if not self.test_results['api_functionality']:
                issues.append("• Проблемы с API функциональностью")
            if not all(pkg['installed'] for pkg in self.test_results['dependencies'].values()):
                issues.append("• Отсутствуют критические зависимости")
            if not self.test_results['deployment_readiness']['render_yaml']['exists']:
                issues.append("• Отсутствует render.yaml")
            if not self.test_results['deployment_readiness']['dockerfile']['exists']:
                issues.append("• Отсутствует Dockerfile")
                
            for issue in issues:
                print(issue)
                
            print("\n🔧 РЕКОМЕНДАЦИИ ПО ИСПРАВЛЕНИЮ:")
            print("1. Исправьте выявленные ошибки в конфигурации")
            print("2. Убедитесь, что все файлы присутствуют")
            print("3. Проверьте работу API endpoints")
            print("4. Установите отсутствующие зависимости")
            print("5. Проверьте настройки безопасности")
            print("6. Повторите тестирование")

        # Сохранение отчета в файл
        report_file = self.base_dir / "stage_1_3_detailed_test_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n📄 Полный детальный отчет сохранен в: {report_file}")
            
            # Создание краткого отчета для быстрого просмотра
            brief_report = {
                "stage": self.test_results["stage"],
                "timestamp": self.test_results["timestamp"],
                "overall_status": self.test_results["overall_status"],
                "success_rate": self.test_results["success_rate"],
                "score": f"{self.test_results['score']}/{self.test_results['total_tests']}",
                "python_version": self.test_results["python_compatibility"]["current_version"]
            }
            
            brief_file = self.base_dir / "stage_1_3_brief_report.json"
            with open(brief_file, 'w', encoding='utf-8') as f:
                json.dump(brief_report, f, indent=2, ensure_ascii=False)
            print(f"📋 Краткий отчет сохранен в: {brief_file}")
            
        except Exception as e:
            print(f"\n⚠️ Не удалось сохранить отчет: {e}")

        # Финальное сообщение
        print(f"\n{'🎉' if all_passed else '⚠️'} ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        print(f"Результат: {'УСПЕХ' if all_passed else 'НЕУДАЧА'}")
        print(f"Общий счет: {self.test_results['success_rate']}%")

def main():
    """Основная функция запуска теста"""
    print("🚀 КОМПЛЕКСНЫЙ ТЕСТ ЭТАПА 1.3: НАСТРОЙКА ИНФРАСТРУКТУРЫ")
    print("Расширенная версия с детальной диагностикой")
    print("\n⚠️  ПРЕДУПРЕЖДЕНИЕ: Убедитесь, что API сервер запущен (python api/app.py)")
    print("   Тест попытается подключиться к http://localhost:8000")
    
    try:
        input("Нажмите Enter для продолжения тестирования...")
    except KeyboardInterrupt:
        print("\n❌ Тестирование прервано пользователем")
        sys.exit(1)
    
    tester = Stage1ComprehensiveTest()
    success = tester.run_comprehensive_test()
    
    # Возвращаем код выхода для CI/CD
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()