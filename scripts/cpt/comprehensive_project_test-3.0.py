#!/usr/bin/env python3
"""
КОМПЛЕКСНЫЙ ТЕСТ ВСЕГО ПРОЕКТА ANTHROPOMORPHIC AI
Исправленная версия с устранением выявленных ошибок
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

    def scan_project_structure(self):
        """Сканирование и анализ структуры проекта"""
        self.print_header("📁 АНАЛИЗ СТРУКТУРЫ ПРОЕКТА")
        
        structure = {}
        excluded_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.env'}
        excluded_files = {'.DS_Store', '*.pyc', '*.pyo'}
        
        def scan_directory(path: Path, level=0):
            """Рекурсивное сканирование директории"""
            rel_path = path.relative_to(self.base_dir)
            dir_structure = {
                "type": "directory",
                "path": str(rel_path),
                "files": [],
                "subdirs": {}
            }
            
            try:
                for item in path.iterdir():
                    if item.name in excluded_dirs:
                        continue
                    if any(item.name.endswith(ext) for ext in ['.pyc', '.pyo']):
                        continue
                    
                    if item.is_dir():
                        dir_structure["subdirs"][item.name] = scan_directory(item, level + 1)
                    else:
                        file_info = {
                            "name": item.name,
                            "size": item.stat().st_size,
                            "modified": time.ctime(item.stat().st_mtime)
                        }
                        dir_structure["files"].append(file_info)
            except PermissionError:
                dir_structure["error"] = "Permission denied"
            
            return dir_structure
        
        structure = scan_directory(self.base_dir)
        self.project_structure = structure
        self.test_results["project_structure"] = structure
        
        # Вывод структуры в консоль
        self.print_section("СТРУКТУРА ПРОЕКТА")
        self._print_tree(structure)
        
        return True

    def _print_tree(self, structure: Dict, prefix: str = ""):
        """Рекурсивный вывод дерева структуры"""
        if "path" in structure:
            print(f"{prefix}📁 {structure['path']}/")
        
        # Вывод файлов
        for file_info in structure.get("files", []):
            print(f"{prefix}   📄 {file_info['name']} ({file_info['size']} bytes)")
        
        # Рекурсивный вывод поддиректорий
        for dir_name, dir_structure in structure.get("subdirs", {}).items():
            self._print_tree(dir_structure, prefix + "   ")

    # ЭТАП 1: ПОДГОТОВИТЕЛЬНЫЙ
    def test_stage_1_preparatory(self):
        """Тестирование ЭТАПА 1: ПОДГОТОВИТЕЛЬНЫЙ"""
        self.print_header("🎯 ЭТАП 1: ПОДГОТОВИТЕЛЬНЫЙ (НЕДЕЛИ 1-2)")
        
        stage_results = {
            "status": "IN_PROGRESS",
            "tasks": {},
            "completion_percentage": 0
        }
        
        # Задача 1.1: Инициализация проекта
        task_1_1_results = self._test_task_1_1()
        stage_results["tasks"]["1.1"] = task_1_1_results
        
        # Задача 1.2: Проектирование архитектуры
        task_1_2_results = self._test_task_1_2()
        stage_results["tasks"]["1.2"] = task_1_2_results
        
        # Задача 1.3: Настройка инфраструктуры
        task_1_3_results = self._test_task_1_3()
        stage_results["tasks"]["1.3"] = task_1_3_results
        
        # Расчет прогресса этапа
        completed_tasks = sum(1 for task in stage_results["tasks"].values() if task["status"] == "COMPLETED")
        total_tasks = len(stage_results["tasks"])
        stage_results["completion_percentage"] = (completed_tasks / total_tasks) * 100
        
        if stage_results["completion_percentage"] == 100:
            stage_results["status"] = "COMPLETED"
        elif stage_results["completion_percentage"] > 0:
            stage_results["status"] = "IN_PROGRESS"
        else:
            stage_results["status"] = "NOT_STARTED"
        
        self.test_results["stage_progress"]["stage_1"] = stage_results
        return stage_results

    def _test_task_1_1(self):
        """Тестирование Задачи 1.1: Инициализация проекта"""
        self.print_section("ЗАДАЧА 1.1: Инициализация проекта")
        
        task_results = {
            "name": "Инициализация проекта",
            "status": "IN_PROGRESS",
            "subtasks": {},
            "completion_percentage": 0
        }
        
        # Подзадача 1.1.1: Создание репозитория GitHub с полной структурой каталогов
        subtask_1_1_1 = self._test_subtask_1_1_1()
        task_results["subtasks"]["1.1.1"] = subtask_1_1_1
        
        # Подзадача 1.1.2: Настройка виртуального окружения и requirements.txt
        subtask_1_1_2 = self._test_subtask_1_1_2()
        task_results["subtasks"]["1.1.2"] = subtask_1_1_2
        
        # Подзадача 1.1.3: Конфигурация лицензии, README.md, .gitignore
        subtask_1_1_3 = self._test_subtask_1_1_3()
        task_results["subtasks"]["1.1.3"] = subtask_1_1_3
        
        # Подзадача 1.1.4: Настройка CI/CD пайплайнов в .github/workflows/
        subtask_1_1_4 = self._test_subtask_1_1_4()
        task_results["subtasks"]["1.1.4"] = subtask_1_1_4
        
        # Расчет прогресса задачи
        completed_subtasks = sum(1 for subtask in task_results["subtasks"].values() if subtask["status"] == "COMPLETED")
        total_subtasks = len(task_results["subtasks"])
        task_results["completion_percentage"] = (completed_subtasks / total_subtasks) * 100
        
        if task_results["completion_percentage"] == 100:
            task_results["status"] = "COMPLETED"
        elif task_results["completion_percentage"] > 0:
            task_results["status"] = "IN_PROGRESS"
        else:
            task_results["status"] = "NOT_STARTED"
        
        return task_results

    def _test_subtask_1_1_1(self):
        """Подзадача 1.1.1: Создание репозитория GitHub с полной структурой каталогов"""
        subtask_results = {
            "name": "Создание структуры каталогов",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка наличия основных директорий
        required_dirs = [
            "api", "core", "modules", "database", "scripts", "tests", 
            "data/configs", "utils", "docs", ".github/workflows"
        ]
        
        dir_checks = []
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            exists = full_path.exists()
            check_result = self.print_result(
                f"Директория: {dir_path}",
                exists,
                "Найдена" if exists else "Отсутствует"
            )
            dir_checks.append({
                "directory": dir_path,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        subtask_results["checks"].extend(dir_checks)
        
        # Проверка наличия критических файлов
        critical_files = [
            "api/__init__.py", "api/app.py", "api/routes.py",
            "core/__init__.py", "core/config.py", "core/main.py",
            "requirements.txt", "README.md", ".gitignore"
        ]
        
        file_checks = []
        for file_path in critical_files:
            full_path = self.base_dir / file_path
            exists = full_path.exists()
            check_result = self.print_result(
                f"Файл: {file_path}",
                exists,
                "Найден" if exists else "Отсутствует"
            )
            file_checks.append({
                "file": file_path,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        subtask_results["checks"].extend(file_checks)
        
        # Определение статуса подзадачи
        all_passed = all(check["status"] == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_1_2(self):
        """Подзадача 1.1.2: Настройка виртуального окружения и requirements.txt"""
        subtask_results = {
            "name": "Настройка окружения и зависимостей",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка requirements.txt
        requirements_file = self.base_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    requirements = f.readlines()
                
                # Проверка наличия критических пакетов
                critical_packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "pydantic-settings"]
                packages_found = []
                
                for package in critical_packages:
                    found = any(package in line.lower() for line in requirements)
                    check_result = self.print_result(
                        f"Пакет в requirements.txt: {package}",
                        found,
                        "Найден" if found else "Отсутствует"
                    )
                    packages_found.append({
                        "package": package,
                        "found": found,
                        "status": "PASS" if found else "FAIL"
                    })
                
                subtask_results["checks"].extend(packages_found)
                
                # УЛУЧШЕННАЯ ПРОВЕРКА: Стратегия версий - проверка без учета комментариев
                has_versions = False
                for line in requirements:
                    clean_line = line.split('#')[0].strip()  # Удаляем комментарии
                    if clean_line and ('==' in clean_line or '>=' in clean_line):
                        has_versions = True
                        break
                        
                version_check = self.print_result(
                    "Стратегия зависимостей без версий",
                    not has_versions,
                    "Версии не зафиксированы" if not has_versions else "Версии зафиксированы - может вызвать конфликты"
                )
                subtask_results["checks"].append({
                    "check": "version_strategy",
                    "status": "PASS" if not has_versions else "FAIL",
                    "details": "versionless" if not has_versions else "versioned"
                })
                
            except Exception as e:
                self.print_result("Чтение requirements.txt", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "read_requirements",
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл requirements.txt", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "requirements_exists",
                "status": "FAIL",
                "error": "Файл requirements.txt отсутствует"
            })
        
        # Проверка установленных пакетов
        installed_checks = []
        for package in ["fastapi", "uvicorn", "sqlalchemy", "pydantic"]:
            try:
                version = importlib.metadata.version(package)
                check_result = self.print_result(
                    f"Пакет установлен: {package}",
                    True,
                    f"Версия: {version}"
                )
                installed_checks.append({
                    "package": package,
                    "installed": True,
                    "version": version,
                    "status": "PASS"
                })
            except importlib.metadata.PackageNotFoundError:
                check_result = self.print_result(
                    f"Пакет установлен: {package}",
                    False,
                    "Не установлен"
                )
                installed_checks.append({
                    "package": package,
                    "installed": False,
                    "status": "FAIL"
                })
        
        subtask_results["checks"].extend(installed_checks)
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_1_3(self):
        """Подзадача 1.1.3: Конфигурация лицензии, README.md, .gitignore"""
        subtask_results = {
            "name": "Конфигурация документации",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка README.md
        readme_file = self.base_dir / "README.md"
        if readme_file.exists():
            readme_size = readme_file.stat().st_size
            check_result = self.print_result(
                "Файл README.md",
                readme_size > 100,  # Минимум 100 байт
                f"Размер: {readme_size} байт"
            )
            subtask_results["checks"].append({
                "file": "README.md",
                "exists": True,
                "size": readme_size,
                "status": "PASS" if readme_size > 100 else "FAIL"
            })
        else:
            self.print_result("Файл README.md", False, "Отсутствует")
            subtask_results["checks"].append({
                "file": "README.md",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка .gitignore
        gitignore_file = self.base_dir / ".gitignore"
        if gitignore_file.exists():
            try:
                content = gitignore_file.read_text()
                # УЛУЧШЕННАЯ ПРОВЕРКА: Игнорируем комментарии при проверке паттернов
                lines = [line.strip() for line in content.split('\n') 
                        if line.strip() and not line.strip().startswith('#')]
                
                critical_patterns = [".env", "__pycache__", "*.pyc", "instance/", ".pytest_cache"]
                missing_patterns = [pattern for pattern in critical_patterns 
                                  if not any(pattern in line for line in lines)]
                
                check_result = self.print_result(
                    "Файл .gitignore",
                    len(missing_patterns) == 0,
                    f"Отсутствуют паттерны: {missing_patterns}" if missing_patterns else "Все критичные паттерны присутствуют"
                )
                subtask_results["checks"].append({
                    "file": ".gitignore",
                    "exists": True,
                    "complete": len(missing_patterns) == 0,
                    "missing_patterns": missing_patterns,
                    "status": "PASS" if len(missing_patterns) == 0 else "FAIL"
                })
            except Exception as e:
                self.print_result("Чтение .gitignore", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "file": ".gitignore",
                    "exists": True,
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл .gitignore", False, "Отсутствует")
            subtask_results["checks"].append({
                "file": ".gitignore",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка LICENSE
        license_files = ["LICENSE", "LICENSE.md", "LICENSE.txt"]
        license_found = False
        for license_file in license_files:
            if (self.base_dir / license_file).exists():
                license_found = True
                break
        
        check_result = self.print_result(
            "Файл лицензии",
            license_found,
            "Найден" if license_found else "Отсутствует"
        )
        subtask_results["checks"].append({
            "check": "license",
            "exists": license_found,
            "status": "PASS" if license_found else "FAIL"
        })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_1_4(self):
        """Подзадача 1.1.4: Настройка CI/CD пайплайнов в .github/workflows/"""
        subtask_results = {
            "name": "Настройка CI/CD",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        workflows_dir = self.base_dir / ".github" / "workflows"
        
        if workflows_dir.exists():
            workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
            
            if workflow_files:
                for workflow_file in workflow_files:
                    check_result = self.print_result(
                        f"Workflow файл: {workflow_file.name}",
                        True,
                        f"Найден"
                    )
                    subtask_results["checks"].append({
                        "workflow": workflow_file.name,
                        "exists": True,
                        "status": "PASS"
                    })
            else:
                self.print_result("Workflow файлы", False, "Отсутствуют в .github/workflows/")
                subtask_results["checks"].append({
                    "check": "workflow_files",
                    "exists": False,
                    "status": "FAIL"
                })
        else:
            self.print_result("Директория .github/workflows", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "workflows_dir",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка наличия основных workflow
        expected_workflows = ["ci-cd.yml", "deploy.yml"]
        for workflow in expected_workflows:
            workflow_path = workflows_dir / workflow
            exists = workflow_path.exists()
            check_result = self.print_result(
                f"Ожидаемый workflow: {workflow}",
                exists,
                "Найден" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "expected_workflow": workflow,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_task_1_2(self):
        """Тестирование Задачи 1.2: Проектирование архитектуры"""
        self.print_section("ЗАДАЧА 1.2: Проектирование архитектуры")
        
        task_results = {
            "name": "Проектирование архитектуры",
            "status": "IN_PROGRESS",
            "subtasks": {},
            "completion_percentage": 0
        }
        
        # Подзадача 1.2.1: Детальное проектирование API endpoints
        subtask_1_2_1 = self._test_subtask_1_2_1()
        task_results["subtasks"]["1.2.1"] = subtask_1_2_1
        
        # Подзадача 1.2.2: Проектирование схемы базы данных
        subtask_1_2_2 = self._test_subtask_1_2_2()
        task_results["subtasks"]["1.2.2"] = subtask_1_2_2
        
        # Подзадача 1.2.3: Определение форматов конфигурационных файлов
        subtask_1_2_3 = self._test_subtask_1_2_3()
        task_results["subtasks"]["1.2.3"] = subtask_1_2_3
        
        # Подзадача 1.2.4: Создание технических спецификаций для модулей
        subtask_1_2_4 = self._test_subtask_1_2_4()
        task_results["subtasks"]["1.2.4"] = subtask_1_2_4
        
        # Расчет прогресса задачи
        completed_subtasks = sum(1 for subtask in task_results["subtasks"].values() if subtask["status"] == "COMPLETED")
        total_subtasks = len(task_results["subtasks"])
        task_results["completion_percentage"] = (completed_subtasks / total_subtasks) * 100
        
        if task_results["completion_percentage"] == 100:
            task_results["status"] = "COMPLETED"
        elif task_results["completion_percentage"] > 0:
            task_results["status"] = "IN_PROGRESS"
        else:
            task_results["status"] = "NOT_STARTED"
        
        return task_results

    def _test_subtask_1_2_1(self):
        """Подзадача 1.2.1: Детальное проектирование API endpoints"""
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
        
        # УЛУЧШЕННАЯ ПРОВЕРКА: Проверка эндпоинтов в routes.py с игнорированием комментариев
        routes_file = self.base_dir / "api" / "routes.py"
        if routes_file.exists():
            try:
                content = routes_file.read_text()
                # Удаляем комментарии для более точной проверки
                lines = content.split('\n')
                clean_content = '\n'.join([line.split('#')[0] for line in lines])
                
                expected_endpoints = [
                    "/chat", "/state", "/health", "/mood/update",
                    "/memory/store", "/memory/recall", "/personality/update"
                ]
                
                endpoints_found = []
                for endpoint in expected_endpoints:
                    # Проверяем различные варианты написания эндпоинтов
                    patterns = [f'"/{endpoint}"', f"'{endpoint}'", f'@.*{endpoint}']
                    found = any(pattern in clean_content for pattern in patterns)
                    
                    check_result = self.print_result(
                        f"API эндпоинт: {endpoint}",
                        found,
                        "Реализован" if found else "Отсутствует"
                    )
                    endpoints_found.append({
                        "endpoint": endpoint,
                        "implemented": found,
                        "status": "PASS" if found else "FAIL"
                    })
                
                subtask_results["checks"].extend(endpoints_found)
                
            except Exception as e:
                self.print_result("Анализ routes.py", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_routes",
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # УЛУЧШЕННАЯ ПРОВЕРКА: API availability с несколькими портами
        if self._test_api_availability():
            check_result = self.print_result(
                "API сервер работает",
                True,
                "Сервер запущен и отвечает"
            )
            subtask_results["checks"].append({
                "check": "api_server",
                "status": "PASS"
            })
        else:
            check_result = self.print_result(
                "API сервер работает",
                False,
                "Сервер не отвечает - запустите: python api/app.py"
            )
            subtask_results["checks"].append({
                "check": "api_server",
                "status": "FAIL"
            })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_2_2(self):
        """Подзадача 1.2.2: Проектирование схемы базы данных"""
        subtask_results = {
            "name": "Проектирование схемы БД",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка файлов базы данных
        db_files = [
            "database/__init__.py", "database/models.py", 
            "database/crud.py", "database/session.py"
        ]
        
        for db_file in db_files:
            file_path = self.base_dir / db_file
            exists = file_path.exists()
            check_result = self.print_result(
                f"Файл БД: {db_file}",
                exists,
                "Найден" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "file": db_file,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # Проверка моделей в models.py
        models_file = self.base_dir / "database" / "models.py"
        if models_file.exists():
            try:
                content = models_file.read_text()
                expected_models = [
                    "SystemState", "Memory", "Interaction", "MoodHistory",
                    "PersonalityTrait", "CharacterHabit", "LearningExperience", "SystemLog"
                ]
                
                models_found = []
                for model in expected_models:
                    found = f"class {model}" in content
                    check_result = self.print_result(
                        f"Модель БД: {model}",
                        found,
                        "Определена" if found else "Отсутствует"
                    )
                    models_found.append({
                        "model": model,
                        "implemented": found,
                        "status": "PASS" if found else "FAIL"
                    })
                
                subtask_results["checks"].extend(models_found)
                
            except Exception as e:
                self.print_result("Анализ models.py", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_models",
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # Проверка миграций
        migrations_dir = self.base_dir / "database" / "migrations"
        if migrations_dir.exists():
            check_result = self.print_result(
                "Директория миграций",
                True,
                "Найдена"
            )
            subtask_results["checks"].append({
                "check": "migrations_dir",
                "exists": True,
                "status": "PASS"
            })
        else:
            check_result = self.print_result(
                "Директория миграций",
                False,
                "Отсутствует"
            )
            subtask_results["checks"].append({
                "check": "migrations_dir",
                "exists": False,
                "status": "FAIL"
            })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_2_3(self):
        """Подзадача 1.2.3: Определение форматов конфигурационных файлов"""
        subtask_results = {
            "name": "Форматы конфигурационных файлов",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка конфигурационных файлов
        config_files = [
            "data/configs/system_config.json",
            "data/configs/psyche_config.json",
            "data/configs/memory_config.json", 
            "data/configs/mood_config.json"
        ]
        
        for config_file in config_files:
            file_path = self.base_dir / config_file
            exists = file_path.exists()
            
            if exists:
                try:
                    with open(file_path, 'r') as f:
                        json.load(f)
                    check_result = self.print_result(
                        f"Конфигурационный файл: {config_file}",
                        True,
                        "Валидный JSON"
                    )
                    subtask_results["checks"].append({
                        "file": config_file,
                        "exists": True,
                        "valid_json": True,
                        "status": "PASS"
                    })
                except json.JSONDecodeError as e:
                    check_result = self.print_result(
                        f"Конфигурационный файл: {config_file}",
                        False,
                        f"Невалидный JSON: {e}"
                    )
                    subtask_results["checks"].append({
                        "file": config_file,
                        "exists": True,
                        "valid_json": False,
                        "status": "FAIL",
                        "error": str(e)
                    })
            else:
                check_result = self.print_result(
                    f"Конфигурационный файл: {config_file}",
                    False,
                    "Отсутствует"
                )
                subtask_results["checks"].append({
                    "file": config_file,
                    "exists": False,
                    "status": "FAIL"
                })
        
        # Проверка core/config.py
        config_py = self.base_dir / "core" / "config.py"
        if config_py.exists():
            try:
                content = config_py.read_text()
                has_settings = "class Settings" in content or "pydantic" in content.lower()
                has_config_manager = "class ConfigManager" in content or "config_manager" in content
                
                check_result = self.print_result(
                    "Файл core/config.py",
                    has_settings and has_config_manager,
                    "Содержит настройки и менеджер конфигураций" if has_settings and has_config_manager else "Неполная реализация"
                )
                subtask_results["checks"].append({
                    "file": "core/config.py",
                    "exists": True,
                    "has_settings": has_settings,
                    "has_config_manager": has_config_manager,
                    "status": "PASS" if has_settings and has_config_manager else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ core/config.py", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "file": "core/config.py",
                    "exists": True,
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_2_4(self):
        """Подзадача 1.2.4: Создание технических спецификаций для модулей"""
        subtask_results = {
            "name": "Технические спецификации модулей",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка документации
        docs_files = [
            "docs/architecture.md",
            "docs/api/endpoints.md",
            "docs/deployment/render.md"
        ]
        
        for doc_file in docs_files:
            file_path = self.base_dir / doc_file
            exists = file_path.exists()
            check_result = self.print_result(
                f"Документация: {doc_file}",
                exists,
                "Найдена" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "file": doc_file,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # Проверка модульной структуры
        modules_dirs = [
            "modules/psyche", "modules/senses", "modules/mood", "modules/memory",
            "modules/reactions", "modules/personality", "modules/character"
        ]
        
        for module_dir in modules_dirs:
            dir_path = self.base_dir / module_dir
            exists = dir_path.exists()
            check_result = self.print_result(
                f"Модуль: {module_dir}",
                exists,
                "Создан" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "module": module_dir,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # Проверка core модулей
        core_files = [
            "core/orchestrator.py", "core/state_manager.py", "core/exceptions.py"
        ]
        
        for core_file in core_files:
            file_path = self.base_dir / core_file
            exists = file_path.exists()
            check_result = self.print_result(
                f"Core модуль: {core_file}",
                exists,
                "Найден" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "file": core_file,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_task_1_3(self):
        """Тестирование Задачи 1.3: Настройка инфраструктуры"""
        self.print_section("ЗАДАЧА 1.3: Настройка инфраструктуры")
        
        task_results = {
            "name": "Настройка инфраструктуры",
            "status": "IN_PROGRESS",
            "subtasks": {},
            "completion_percentage": 0
        }
        
        # Подзадача 1.3.1: Создание базы данных на Render
        subtask_1_3_1 = self._test_subtask_1_3_1()
        task_results["subtasks"]["1.3.1"] = subtask_1_3_1
        
        # Подзадача 1.3.2: Настройка переменных окружения
        subtask_1_3_2 = self._test_subtask_1_3_2()
        task_results["subtasks"]["1.3.2"] = subtask_1_3_2
        
        # Подзадача 1.3.3: Подготовка шаблонов для деплоя
        subtask_1_3_3 = self._test_subtask_1_3_3()
        task_results["subtasks"]["1.3.3"] = subtask_1_3_3
        
        # Расчет прогресса задачи
        completed_subtasks = sum(1 for subtask in task_results["subtasks"].values() if subtask["status"] == "COMPLETED")
        total_subtasks = len(task_results["subtasks"])
        task_results["completion_percentage"] = (completed_subtasks / total_subtasks) * 100
        
        if task_results["completion_percentage"] == 100:
            task_results["status"] = "COMPLETED"
        elif task_results["completion_percentage"] > 0:
            task_results["status"] = "IN_PROGRESS"
        else:
            task_results["status"] = "NOT_STARTED"
        
        return task_results

    def _test_subtask_1_3_1(self):
        """Подзадача 1.3.1: Создание базы данных на Render"""
        subtask_results = {
            "name": "База данных на Render",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка конфигурации базы данных в render.yaml
        render_file = self.base_dir / "render.yaml"
        if render_file.exists():
            try:
                content = render_file.read_text()
                has_postgresql = "postgresql" in content.lower()
                has_database_config = "database" in content.lower() or "DATABASE_URL" in content
                
                check_result = self.print_result(
                    "Конфигурация БД в render.yaml",
                    has_postgresql and has_database_config,
                    "PostgreSQL настроен" if has_postgresql and has_database_config else "Неполная конфигурация БД"
                )
                subtask_results["checks"].append({
                    "check": "render_db_config",
                    "has_postgresql": has_postgresql,
                    "has_database_config": has_database_config,
                    "status": "PASS" if has_postgresql and has_database_config else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ render.yaml", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_render",
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл render.yaml", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "render_file",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка переменных окружения для БД
        env_example = self.base_dir / ".env.example"
        if env_example.exists():
            try:
                content = env_example.read_text()
                has_database_url = "DATABASE_URL" in content
                has_db_config = any(keyword in content for keyword in ["POSTGRES", "SQLITE", "DATABASE"])
                
                check_result = self.print_result(
                    "Конфигурация БД в .env.example",
                    has_database_url and has_db_config,
                    "Настройки БД присутствуют" if has_database_url and has_db_config else "Неполные настройки БД"
                )
                subtask_results["checks"].append({
                    "check": "env_db_config",
                    "has_database_url": has_database_url,
                    "has_db_config": has_db_config,
                    "status": "PASS" if has_database_url and has_db_config else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ .env.example", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_env_example",
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # Примечание: Фактическое создание БД на Render не может быть протестировано локально
        self.print_result(
            "Создание БД на Render",
            False,
            "Требуется ручная настройка в панели Render",
            points=0
        )
        subtask_results["checks"].append({
            "check": "render_db_creation",
            "status": "MANUAL_REQUIRED",
            "details": "Требуется ручная настройка в панели Render"
        })
        
        # Определение статуса подзадачи
        manual_checks = [check for check in subtask_results["checks"] if check.get("status") == "MANUAL_REQUIRED"]
        auto_checks = [check for check in subtask_results["checks"] if check.get("status") != "MANUAL_REQUIRED"]
        
        if manual_checks and all(check.get("status") == "PASS" for check in auto_checks):
            subtask_results["status"] = "MANUAL_ACTION_REQUIRED"
        elif all(check.get("status") == "PASS" for check in subtask_results["checks"]):
            subtask_results["status"] = "COMPLETED"
        else:
            subtask_results["status"] = "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_3_2(self):
        """Подзадача 1.3.2: Настройка переменных окружения"""
        subtask_results = {
            "name": "Настройка переменных окружения",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # УЛУЧШЕННАЯ ПРОВЕРКА: .env.example с обработкой комментариев
        env_example = self.base_dir / ".env.example"
        if env_example.exists():
            try:
                content = env_example.read_text()
                # Игнорируем комментарии и пустые строки
                lines = [line.strip() for line in content.split('\n') 
                        if line.strip() and not line.strip().startswith('#')]
                
                critical_vars = ["DATABASE_URL", "API_HOST", "API_PORT", "ENVIRONMENT", "DEBUG"]
                found_vars = [var for var in critical_vars if any(var in line for line in lines)]
                
                check_result = self.print_result(
                    "Файл .env.example",
                    len(found_vars) == len(critical_vars),
                    f"Найдено переменных: {len(found_vars)}/{len(critical_vars)}"
                )
                subtask_results["checks"].append({
                    "check": "env_example",
                    "exists": True,
                    "variables_found": len(found_vars),
                    "variables_total": len(critical_vars),
                    "status": "PASS" if len(found_vars) == len(critical_vars) else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ .env.example", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_env_example",
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл .env.example", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "env_example",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка .env (локальный)
        env_file = self.base_dir / ".env"
        if env_file.exists():
            check_result = self.print_result(
                "Локальный .env файл",
                True,
                "Найден (убедитесь, что он в .gitignore)"
            )
            subtask_results["checks"].append({
                "check": "local_env",
                "exists": True,
                "status": "PASS"
            })
        else:
            check_result = self.print_result(
                "Локальный .env файл",
                False,
                "Отсутствует (создайте из .env.example)"
            )
            subtask_results["checks"].append({
                "check": "local_env",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка core/config.py на использование переменных окружения
        config_file = self.base_dir / "core" / "config.py"
        if config_file.exists():
            try:
                content = config_file.read_text()
                uses_env_vars = "BaseSettings" in content or "env_file" in content or "os.getenv" in content
                
                check_result = self.print_result(
                    "Использование переменных окружения в config.py",
                    uses_env_vars,
                    "Настроено" if uses_env_vars else "Не настроено"
                )
                subtask_results["checks"].append({
                    "check": "config_env_usage",
                    "uses_env_vars": uses_env_vars,
                    "status": "PASS" if uses_env_vars else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ core/config.py", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_config",
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_subtask_1_3_3(self):
        """Подзадача 1.3.3: Подготовка шаблонов для деплоя"""
        subtask_results = {
            "name": "Подготовка шаблонов для деплоя",
            "status": "IN_PROGRESS",
            "checks": []
        }
        
        # Проверка render.yaml
        render_file = self.base_dir / "render.yaml"
        if render_file.exists():
            try:
                content = render_file.read_text()
                has_services = "services:" in content
                has_build_command = "buildCommand" in content
                has_start_command = "startCommand" in content
                
                check_result = self.print_result(
                    "Файл render.yaml",
                    has_services and has_build_command and has_start_command,
                    "Полная конфигурация" if has_services and has_build_command and has_start_command else "Неполная конфигурация"
                )
                subtask_results["checks"].append({
                    "check": "render_yaml",
                    "exists": True,
                    "has_services": has_services,
                    "has_build_command": has_build_command,
                    "has_start_command": has_start_command,
                    "status": "PASS" if has_services and has_build_command and has_start_command else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ render.yaml", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_render",
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл render.yaml", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "render_yaml",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка Dockerfile
        dockerfile = self.base_dir / "Dockerfile"
        if dockerfile.exists():
            try:
                content = dockerfile.read_text()
                has_from = "FROM python" in content
                has_workdir = "WORKDIR" in content
                has_copy = "COPY" in content
                has_requirements = "requirements.txt" in content
                
                check_result = self.print_result(
                    "Файл Dockerfile",
                    has_from and has_workdir and has_copy and has_requirements,
                    "Полная конфигурация" if all([has_from, has_workdir, has_copy, has_requirements]) else "Неполная конфигурация"
                )
                subtask_results["checks"].append({
                    "check": "dockerfile",
                    "exists": True,
                    "has_from": has_from,
                    "has_workdir": has_workdir,
                    "has_copy": has_copy,
                    "has_requirements": has_requirements,
                    "status": "PASS" if all([has_from, has_workdir, has_copy, has_requirements]) else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ Dockerfile", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_dockerfile",
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл Dockerfile", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "dockerfile",
                "exists": False,
                "status": "FAIL"
            })
        
        # Проверка скриптов деплоя
        deploy_scripts = [
            "scripts/deploy_render.sh",
            "scripts/setup_render.py", 
            "scripts/validate_infrastructure.py"
        ]
        
        for script in deploy_scripts:
            script_path = self.base_dir / script
            exists = script_path.exists()
            check_result = self.print_result(
                f"Скрипт деплоя: {script}",
                exists,
                "Найден" if exists else "Отсутствует"
            )
            subtask_results["checks"].append({
                "script": script,
                "exists": exists,
                "status": "PASS" if exists else "FAIL"
            })
        
        # УЛУЧШЕННАЯ ПРОВЕРКА: runtime.txt - гибкая проверка версии Python
        runtime_file = self.base_dir / "runtime.txt"
        if runtime_file.exists():
            try:
                content = runtime_file.read_text().strip()
                # Гибкая проверка версии Python
                is_correct = "python-3" in content
                check_result = self.print_result(
                    "Файл runtime.txt",
                    is_correct,
                    f"Содержимое: {content}" if is_correct else f"Ожидается python-3.x.x, найдено: {content}"
                )
                subtask_results["checks"].append({
                    "check": "runtime_txt",
                    "exists": True,
                    "content": content,
                    "status": "PASS" if is_correct else "FAIL"
                })
            except Exception as e:
                self.print_result("Анализ runtime.txt", False, f"Ошибка: {e}")
                subtask_results["checks"].append({
                    "check": "analyze_runtime",
                    "status": "FAIL",
                    "error": str(e)
                })
        else:
            self.print_result("Файл runtime.txt", False, "Отсутствует")
            subtask_results["checks"].append({
                "check": "runtime_txt",
                "exists": False,
                "status": "FAIL"
            })
        
        # Определение статуса подзадачи
        all_passed = all(check.get("status") == "PASS" for check in subtask_results["checks"])
        subtask_results["status"] = "COMPLETED" if all_passed else "IN_PROGRESS"
        
        return subtask_results

    def _test_api_availability(self, port=8000):
        """УЛУЧШЕННАЯ ПРОВЕРКА: Проверка доступности API сервера с несколькими путями"""
        api_paths = ["/health", "/api/health", "/api/v1/health"]
        
        for path in api_paths:
            try:
                req = urllib.request.Request(f"http://localhost:{port}{path}")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        return True
            except (urllib.error.URLError, socket.timeout, ConnectionRefusedError):
                continue
        return False

    def generate_recommendations(self):
        """Генерация рекомендаций на основе результатов тестирования"""
        self.print_header("🎯 РЕКОМЕНДАЦИИ ПО ПРОЕКТУ")
        
        recommendations = []
        
        # Анализ Stage 1
        stage_1 = self.test_results["stage_progress"].get("stage_1", {})
        
        if stage_1.get("status") != "COMPLETED":
            recommendations.append("🔶 ЗАВЕРШИТЕ ЭТАП 1: Проведите завершающие работы по подготовительному этапу")
        
        # Анализ по задачам
        tasks = stage_1.get("tasks", {})
        
        # Задача 1.1
        task_1_1 = tasks.get("1.1", {})
        if task_1_1.get("status") != "COMPLETED":
            recommendations.append("📁 Задача 1.1: Доработайте структуру проекта и настройки")
        
        # Задача 1.2  
        task_1_2 = tasks.get("1.2", {})
        if task_1_2.get("status") != "COMPLETED":
            recommendations.extend([
                "🏗️ Задача 1.2: Завершите проектирование архитектуры",
                "🔌 Реализуйте API endpoints в api/routes.py",
                "🚀 Запустите API сервер: python api/app.py",
                "📝 Добавьте недостающие эндпоинты: /chat, /state, /health и др."
            ])
        
        # Задача 1.3
        task_1_3 = tasks.get("1.3", {})
        if task_1_3.get("status") != "COMPLETED":
            recommendations.extend([
                "⚙️ Задача 1.3: Завершите настройку инфраструктуры для деплоя",
                "🗄️ Создайте базу данных PostgreSQL в панели Render",
                "🔧 Настройте DATABASE_URL в переменных окружения Render",
                "🐍 Проверьте совместимость пакетов с Python 3.13.4"
            ])
        
        # Конкретные рекомендации на основе проверок
        if not (self.base_dir / ".github/workflows").exists():
            recommendations.append("🔧 Создайте директорию .github/workflows для CI/CD пайплайнов")
        
        if not (self.base_dir / "database/migrations").exists():
            recommendations.append("🗃️ Настройте миграции базы данных с Alembic")
        
        if not self._test_api_availability():
            recommendations.extend([
                "🌐 Запустите API сервер: python api/app.py",
                "🔍 Проверьте конфигурацию API в api/app.py",
                "📖 Убедитесь, что эндпоинт /health реализован"
            ])
        
        # Рекомендации по версиям Python
        recommendations.extend([
            "🐍 ВНИМАНИЕ: Локально используется Python 3.12.3, на Render - 3.13.4",
            "🔍 Протестируйте совместимость всех пакетов с Python 3.13.4",
            "📋 В requirements.txt версии не указаны - это может вызвать конфликты",
            "💡 Рекомендуется протестировать с версией 3.13.4 локально перед деплоем"
        ])
        
        # Рекомендации по следующим шагам
        if stage_1.get("status") == "COMPLETED":
            recommendations.extend([
                "🎉 ЭТАП 1 ЗАВЕРШЕН! Переходите к ЭТАПУ 2: Разработка базовой инфраструктуры",
                "🚀 Создайте репозиторий на GitHub и настройте автоматический деплой на Render",
                "📊 Начните разработку системы базы данных (Этап 2.2)"
            ])
        
        self.test_results["recommendations"] = recommendations
        
        # Вывод рекомендаций в консоль
        for i, recommendation in enumerate(recommendations, 1):
            print(f"{i}. {recommendation}")
        
        return recommendations

    def run_comprehensive_test(self):
        """Запуск комплексного тестирования всего проекта"""
        self.print_header("🚀 КОМПЛЕКСНЫЙ ТЕСТ ПРОЕКТА ANTHROPOMORPHIC AI")
        print(f"📅 Время начала: {self.test_results['timestamp']}")
        print(f"🐍 Версия Python: {sys.version.split()[0]}")
        print(f"📁 Директория проекта: {self.base_dir}")
        
        # Сканирование структуры проекта
        self.scan_project_structure()
        
        # Тестирование Stage 1
        stage_1_results = self.test_stage_1_preparatory()
        
        # Расчет общего прогресса
        total_tests = self.test_results["score"]["total_tests"]
        passed_tests = self.test_results["score"]["passed_tests"]
        
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
        else:
            success_rate = 0
        
        self.test_results["score"]["success_rate"] = round(success_rate, 2)
        
        # Генерация рекомендаций
        self.generate_recommendations()
        
        # Финальный отчет
        self.print_header("📊 ФИНАЛЬНЫЙ ОТЧЕТ")
        
        print(f"🏁 ОБЩИЙ СТАТУС: {self.test_results['overall_status']}")
        print(f"🎯 ТЕКУЩИЙ ЭТАП: {self.test_results['current_stage']}")
        print(f"📈 ПРОГРЕСС: {self.test_results['score']['success_rate']}%")
        print(f"✅ ВЫПОЛНЕНО ТЕСТОВ: {self.test_results['score']['passed_tests']}/{self.test_results['score']['total_tests']}")
        
        # Детали по Stage 1
        stage_1 = self.test_results["stage_progress"]["stage_1"]
        print(f"\n🎯 ЭТАП 1 - ПОДГОТОВИТЕЛЬНЫЙ: {stage_1['status']}")
        print(f"📊 Прогресс: {stage_1['completion_percentage']}%")
        
        for task_name, task in stage_1["tasks"].items():
            print(f"   📋 {task_name}: {task['name']} - {task['status']} ({task['completion_percentage']}%)")
        
        # Сохранение полного отчета
        report_file = self.base_dir / "comprehensive_project_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Полный отчет сохранен в: {report_file}")
        except Exception as e:
            print(f"\n❌ Ошибка сохранения отчета: {e}")
        
        # Определение общего статуса
        if stage_1["status"] == "COMPLETED":
            self.test_results["overall_status"] = "STAGE_1_COMPLETED"
            print("\n🎉 ПОЗДРАВЛЯЮ! ЭТАП 1 ЗАВЕРШЕН УСПЕШНО!")
        else:
            self.test_results["overall_status"] = "IN_PROGRESS"
            print("\n🔧 ПРОЕКТ В РАЗРАБОТКЕ. ВЫПОЛНЯЙТЕ РЕКОМЕНДАЦИИ ДЛЯ ЗАВЕРШЕНИЯ ЭТАПА 1.")
        
        return self.test_results["overall_status"] == "STAGE_1_COMPLETED"

def main():
    """Основная функция"""
    print("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТА ПРОЕКТА ANTHROPOMORPHIC AI")
    print("Этот тест проверит структуру проекта и выполнение всех задач ЭТАПА 1")
    
    try:
        input("\nНажмите Enter для начала тестирования...")
    except KeyboardInterrupt:
        print("\n❌ Тестирование прервано пользователем")
        sys.exit(1)
    
    tester = ComprehensiveProjectTest()
    success = tester.run_comprehensive_test()
    
    # Код возврата для CI/CD
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()