#!/usr/bin/env python3
"""
РАСШИРЕННЫЙ КОМПЛЕКСНЫЙ ТЕСТ ПРОЕКТА ANTHROPOMORPHIC AI
С проверкой работоспособности кода и функциональности
"""

import os
import sys
import json
import logging
import importlib
import inspect
import ast
import traceback
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set
import urllib.request
import urllib.error
import time
import socket
import subprocess
import tempfile
import contextlib

# Настройка расширенного логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class AdvancedComprehensiveProjectTest:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.test_results = {
            "project": "Anthropomorphic AI Core",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_version": sys.version,
            "overall_status": "IN_PROGRESS",
            "current_stage": "1.3 - Настройка инфраструктуры",
            "stage_progress": {},
            "code_quality_analysis": {},
            "performance_metrics": {},
            "security_checks": {},
            "dependency_analysis": {},
            "project_structure": {},
            "detailed_analysis": {},
            "recommendations": [],
            "score": {
                "total_tests": 0,
                "passed_tests": 0,
                "success_rate": 0
            }
        }
        self.import_errors = []
        self.runtime_errors = []
        self.code_issues = []

    # ========== РАСШИРЕННЫЕ ФУНКЦИИ ТЕСТИРОВАНИЯ ==========

    def test_code_execution(self):
        """Тестирование выполнения критического кода проекта"""
        self.print_header("🔧 ТЕСТИРОВАНИЕ ВЫПОЛНЕНИЯ КОДА")

        execution_tests = {
            "config_initialization": self._test_config_initialization,
            "database_models": self._test_database_models,
            "api_structure": self._test_api_structure,
            "core_modules": self._test_core_modules,
            "import_integrity": self._test_import_integrity
        }

        for test_name, test_func in execution_tests.items():
            try:
                success, details = test_func()
                self.print_result(
                    f"Выполнение кода: {test_name}",
                    success,
                    details
                )
            except Exception as e:
                self.print_result(
                    f"Выполнение кода: {test_name}",
                    False,
                    f"Критическая ошибка: {str(e)}"
                )
                self.runtime_errors.append(f"{test_name}: {str(e)}")

    def _test_config_initialization(self) -> Tuple[bool, str]:
        """Тестирование инициализации конфигурации"""
        try:
            # Динамический импорт и инициализация конфигурации
            sys.path.insert(0, str(self.base_dir))
            
            # Проверка core/config.py
            config_spec = importlib.util.spec_from_file_location(
                "config", 
                self.base_dir / "core" / "config.py"
            )
            config_module = importlib.util.module_from_spec(config_spec)
            config_spec.loader.exec_module(config_module)
            
            # Проверка наличия критических классов
            required_classes = ['Settings', 'ConfigManager', 'get_settings']
            available_classes = [name for name in dir(config_module) 
                               if not name.startswith('_')]
            
            missing_classes = [cls for cls in required_classes 
                             if cls not in available_classes]
            
            if missing_classes:
                return False, f"Отсутствуют классы: {missing_classes}"
                
            return True, "Конфигурация успешно инициализирована"
            
        except Exception as e:
            return False, f"Ошибка инициализации: {str(e)}"

    def _test_database_models(self) -> Tuple[bool, str]:
        """Тестирование моделей базы данных"""
        try:
            # Проверка моделей БД
            models_spec = importlib.util.spec_from_file_location(
                "models",
                self.base_dir / "database" / "models.py"
            )
            models_module = importlib.util.module_from_spec(models_spec)
            models_spec.loader.exec_module(models_module)
            
            # Проверка наличия основных моделей
            expected_models = [
                'SystemState', 'Memory', 'Interaction', 'MoodHistory',
                'PersonalityTrait', 'CharacterHabit', 'LearningExperience', 'SystemLog'
            ]
            
            available_models = [name for name in dir(models_module) 
                              if not name.startswith('_') and 
                              inspect.isclass(getattr(models_module, name))]
            
            missing_models = [model for model in expected_models 
                            if model not in available_models]
            
            if missing_models:
                return False, f"Отсутствуют модели: {missing_models}"
                
            # Проверка атрибутов основных моделей
            model_checks = []
            for model_name in expected_models:
                if model_name in available_models:
                    model_class = getattr(models_module, model_name)
                    if hasattr(model_class, '__tablename__'):
                        model_checks.append(f"{model_name}: OK")
                    else:
                        model_checks.append(f"{model_name}: No tablename")
            
            return True, f"Модели проверены: {', '.join(model_checks)}"
            
        except Exception as e:
            return False, f"Ошибка моделей БД: {str(e)}"

    def _test_api_structure(self) -> Tuple[bool, str]:
        """Тестирование структуры API"""
        try:
            # Проверка основного приложения API
            app_spec = importlib.util.spec_from_file_location(
                "app",
                self.base_dir / "api" / "app.py"
            )
            app_module = importlib.util.module_from_spec(app_spec)
            app_spec.loader.exec_module(app_module)
            
            # Проверка наличия приложения FastAPI
            if hasattr(app_module, 'app'):
                app = getattr(app_module, 'app')
                # Проверка базовых атрибутов FastAPI
                if hasattr(app, 'routes') and hasattr(app, 'openapi'):
                    return True, "FastAPI приложение корректно инициализировано"
                else:
                    return False, "Некорректное FastAPI приложение"
            else:
                return False, "Отсутствует объект app в api/app.py"
                
        except Exception as e:
            return False, f"Ошибка API структуры: {str(e)}"

    def _test_core_modules(self) -> Tuple[bool, str]:
        """Тестирование основных модулей core"""
        try:
            core_modules = ['orchestrator', 'main', 'config']
            results = []
            
            for module_name in core_modules:
                module_path = self.base_dir / "core" / f"{module_name}.py"
                if module_path.exists():
                    try:
                        spec = importlib.util.spec_from_file_location(
                            module_name, module_path
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        results.append(f"{module_name}: OK")
                    except Exception as e:
                        results.append(f"{module_name}: ERROR - {str(e)}")
                else:
                    results.append(f"{module_name}: MISSING")
            
            success = all("OK" in result for result in results)
            return success, f"Модули core: {', '.join(results)}"
            
        except Exception as e:
            return False, f"Ошибка тестирования core модулей: {str(e)}"

    def _test_import_integrity(self) -> Tuple[bool, str]:
        """Тестирование целостности импортов во всем проекте"""
        try:
            python_files = list(self.base_dir.rglob("*.py"))
            import_issues = []
            
            for py_file in python_files:
                if "test" in str(py_file).lower() or "venv" in str(py_file):
                    continue
                    
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Базовый синтаксический анализ
                    tree = ast.parse(content)
                    
                    # Поиск импортов
                    imports = []
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.Import, ast.ImportFrom)):
                            imports.append(ast.unparse(node))
                    
                    # Проверка доступности импортируемых модулей
                    for import_stmt in imports:
                        try:
                            # Пропускаем относительные импорты для простоты
                            if import_stmt.startswith('from .') or import_stmt.startswith('import .'):
                                continue
                                
                            # Пытаемся выполнить импорт
                            exec(import_stmt, {})
                            
                        except ImportError as e:
                            import_issues.append(f"{py_file.name}: {import_stmt} - {str(e)}")
                            
                except SyntaxError as e:
                    import_issues.append(f"{py_file.name}: SyntaxError - {str(e)}")
            
            if import_issues:
                return False, f"Проблемы импорта: {import_issues[:5]}"  # Ограничиваем вывод
            else:
                return True, "Все импорты корректны"
                
        except Exception as e:
            return False, f"Ошибка проверки импортов: {str(e)}"

    def test_code_quality(self):
        """Расширенный анализ качества кода"""
        self.print_header("📊 АНАЛИЗ КАЧЕСТВА КОДА")

        quality_checks = {
            "python_syntax": self._check_python_syntax,
            "code_complexity": self._check_code_complexity,
            "docstring_coverage": self._check_docstring_coverage,
            "function_validation": self._check_function_validation,
            "error_handling": self._check_error_handling
        }

        for check_name, check_func in quality_checks.items():
            try:
                success, details, metrics = check_func()
                self.print_result(
                    f"Качество кода: {check_name}",
                    success,
                    details
                )
                # Сохраняем метрики для детального анализа
                self.test_results["code_quality_analysis"][check_name] = {
                    "status": "PASS" if success else "FAIL",
                    "details": details,
                    "metrics": metrics
                }
            except Exception as e:
                self.print_result(
                    f"Качество кода: {check_name}",
                    False,
                    f"Ошибка анализа: {str(e)}"
                )

    def _check_python_syntax(self) -> Tuple[bool, str, Dict]:
        """Проверка синтаксиса Python"""
        python_files = list(self.base_dir.rglob("*.py"))
        syntax_errors = []
        files_checked = 0
        
        for py_file in python_files:
            if "test" in str(py_file).lower() or "venv" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                # Компиляция для проверки синтаксиса
                compile(source_code, str(py_file), 'exec')
                files_checked += 1
                
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: {str(e)}")
        
        metrics = {
            "files_checked": files_checked,
            "syntax_errors": len(syntax_errors),
            "error_details": syntax_errors
        }
        
        if syntax_errors:
            return False, f"Синтаксические ошибки в {len(syntax_errors)} файлах", metrics
        else:
            return True, f"Синтаксис корректен в {files_checked} файлах", metrics

    def _check_code_complexity(self) -> Tuple[bool, str, Dict]:
        """Базовая проверка сложности кода"""
        python_files = list(self.base_dir.rglob("*.py"))
        complexity_issues = []
        total_functions = 0
        total_lines = 0
        
        for py_file in python_files:
            if "test" in str(py_file).lower() or "venv" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Подсчет функций и методов
                functions = [node for node in ast.walk(tree) 
                           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
                total_functions += len(functions)
                
                # Подсчет строк
                lines = content.split('\n')
                total_lines += len([line for line in lines if line.strip()])
                
                # Проверка на слишком длинные функции
                for func in functions:
                    func_lines = func.end_lineno - func.lineno if func.end_lineno else 0
                    if func_lines > 100:  # Функции больше 100 строк
                        complexity_issues.append(f"{py_file.name}:{func.name} - {func_lines} строк")
                        
            except Exception as e:
                complexity_issues.append(f"{py_file.name}: ошибка анализа - {str(e)}")
        
        avg_lines_per_function = total_lines / max(total_functions, 1)
        
        metrics = {
            "total_files": len(python_files),
            "total_functions": total_functions,
            "total_lines": total_lines,
            "avg_lines_per_function": round(avg_lines_per_function, 2),
            "complexity_issues": complexity_issues
        }
        
        if complexity_issues:
            return False, f"Найдены сложные функции: {len(complexity_issues)}", metrics
        else:
            return True, f"Сложность кода в норме", metrics

    def _check_docstring_coverage(self) -> Tuple[bool, str, Dict]:
        """Проверка покрытия docstring"""
        python_files = list(self.base_dir.rglob("*.py"))
        docstring_stats = {
            "files_with_docstrings": 0,
            "functions_with_docstrings": 0,
            "total_functions": 0,
            "classes_with_docstrings": 0,
            "total_classes": 0
        }
        
        for py_file in python_files:
            if "test" in str(py_file).lower() or "venv" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Проверка docstring модуля
                if ast.get_docstring(tree):
                    docstring_stats["files_with_docstrings"] += 1
                
                # Проверка классов
                classes = [node for node in ast.walk(tree) 
                         if isinstance(node, ast.ClassDef)]
                docstring_stats["total_classes"] += len(classes)
                
                for class_node in classes:
                    if ast.get_docstring(class_node):
                        docstring_stats["classes_with_docstrings"] += 1
                
                # Проверка функций
                functions = [node for node in ast.walk(tree) 
                           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
                docstring_stats["total_functions"] += len(functions)
                
                for func_node in functions:
                    if ast.get_docstring(func_node):
                        docstring_stats["functions_with_docstrings"] += 1
                        
            except Exception as e:
                continue
        
        # Расчет покрытия
        file_coverage = (docstring_stats["files_with_docstrings"] / len(python_files)) * 100
        class_coverage = (docstring_stats["classes_with_docstrings"] / max(docstring_stats["total_classes"], 1)) * 100
        function_coverage = (docstring_stats["functions_with_docstrings"] / max(docstring_stats["total_functions"], 1)) * 100
        
        metrics = {
            **docstring_stats,
            "file_coverage_percent": round(file_coverage, 2),
            "class_coverage_percent": round(class_coverage, 2),
            "function_coverage_percent": round(function_coverage, 2)
        }
        
        if file_coverage < 50 or class_coverage < 50 or function_coverage < 50:
            return False, f"Низкое покрытие docstring: файлы={file_coverage}%, классы={class_coverage}%, функции={function_coverage}%", metrics
        else:
            return True, f"Покрытие docstring адекватное", metrics

    def _check_function_validation(self) -> Tuple[bool, str, Dict]:
        """Проверка валидации в функциях"""
        python_files = list(self.base_dir.rglob("*.py"))
        validation_issues = []
        functions_checked = 0
        
        critical_modules = ['api', 'core', 'database']
        
        for py_file in python_files:
            # Проверяем только критические модули
            if not any(module in str(py_file) for module in critical_modules):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Поиск функций
                functions = [node for node in ast.walk(tree) 
                           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
                
                for func in functions:
                    functions_checked += 1
                    func_name = func.name
                    
                    # Проверка наличия базовой обработки ошибок
                    has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(func))
                    
                    # Проверка типов аргументов (базовая)
                    args = func.args
                    has_type_hints = any(arg.annotation for arg in args.args)
                    
                    if not has_try_except and func_name not in ['__init__', 'setup']:
                        validation_issues.append(f"{py_file.name}:{func_name} - нет обработки ошибок")
                    
            except Exception as e:
                validation_issues.append(f"{py_file.name}: ошибка анализа - {str(e)}")
        
        metrics = {
            "functions_checked": functions_checked,
            "validation_issues": len(validation_issues),
            "issue_details": validation_issues
        }
        
        if validation_issues:
            return False, f"Проблемы валидации в {len(validation_issues)} функциях", metrics
        else:
            return True, f"Валидация функций корректна", metrics

    def _check_error_handling(self) -> Tuple[bool, str, Dict]:
        """Проверка обработки ошибок"""
        python_files = list(self.base_dir.rglob("*.py"))
        error_handling_stats = {
            "files_with_error_handling": 0,
            "total_try_blocks": 0,
            "specific_exceptions": 0,
            "bare_excepts": 0
        }
        
        for py_file in python_files:
            if "test" in str(py_file).lower() or "venv" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Поиск блоков try
                try_blocks = [node for node in ast.walk(tree) 
                            if isinstance(node, ast.Try)]
                
                if try_blocks:
                    error_handling_stats["files_with_error_handling"] += 1
                    error_handling_stats["total_try_blocks"] += len(try_blocks)
                
                for try_block in try_blocks:
                    for handler in try_block.handlers:
                        if handler.type is None:  # Bare except
                            error_handling_stats["bare_excepts"] += 1
                        else:
                            error_handling_stats["specific_exceptions"] += 1
                            
            except Exception as e:
                continue
        
        metrics = error_handling_stats
        
        if error_handling_stats["bare_excepts"] > 0:
            return False, f"Найдены bare excepts: {error_handling_stats['bare_excepts']}", metrics
        else:
            return True, f"Обработка ошибок корректна", metrics

    def test_performance_metrics(self):
        """Тестирование производительности и метрик"""
        self.print_header("⚡ ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")

        performance_tests = {
            "import_performance": self._test_import_performance,
            "startup_time": self._test_startup_time,
            "memory_usage": self._test_memory_usage
        }

        for test_name, test_func in performance_tests.items():
            try:
                success, details, metrics = test_func()
                self.print_result(
                    f"Производительность: {test_name}",
                    success,
                    details
                )
                self.test_results["performance_metrics"][test_name] = {
                    "status": "PASS" if success else "FAIL",
                    "details": details,
                    "metrics": metrics
                }
            except Exception as e:
                self.print_result(
                    f"Производительность: {test_name}",
                    False,
                    f"Ошибка тестирования: {str(e)}"
                )

    def _test_import_performance(self) -> Tuple[bool, str, Dict]:
        """Тестирование времени импорта критических модулей"""
        import time
        
        critical_modules = [
            "core.config",
            "database.models", 
            "api.app"
        ]
        
        import_times = {}
        
        for module_name in critical_modules:
            try:
                start_time = time.time()
                
                # Создаем временный модуль для импорта
                module_path = self.base_dir / module_name.replace('.', '/') + ".py"
                if module_path.exists():
                    spec = importlib.util.spec_from_file_location(
                        module_name, module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    end_time = time.time()
                    import_times[module_name] = round((end_time - start_time) * 1000, 2)  # мс
                else:
                    import_times[module_name] = "MISSING"
                    
            except Exception as e:
                import_times[module_name] = f"ERROR: {str(e)}"
        
        # Анализ результатов
        successful_imports = {k: v for k, v in import_times.items() 
                            if isinstance(v, (int, float))}
        
        if successful_imports:
            avg_import_time = sum(successful_imports.values()) / len(successful_imports)
            max_import_time = max(successful_imports.values())
            
            metrics = {
                "import_times": import_times,
                "average_import_time_ms": round(avg_import_time, 2),
                "max_import_time_ms": max_import_time,
                "successful_imports": len(successful_imports)
            }
            
            if max_import_time > 1000:  # Больше 1 секунды
                return False, f"Медленные импорты: до {max_import_time}мс", metrics
            else:
                return True, f"Импорты быстрые: макс {max_import_time}мс", metrics
        else:
            metrics = {"import_times": import_times}
            return False, "Нет успешных импортов", metrics

    def _test_startup_time(self) -> Tuple[bool, str, Dict]:
        """Тестирование времени запуска приложения"""
        try:
            # Тестируем запуск API приложения
            app_path = self.base_dir / "api" / "app.py"
            
            if app_path.exists():
                start_time = time.time()
                
                # Импортируем и инициализируем приложение
                spec = importlib.util.spec_from_file_location("app", app_path)
                app_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(app_module)
                
                # Проверяем, что приложение создано
                if hasattr(app_module, 'app'):
                    app = getattr(app_module, 'app')
                    startup_time = (time.time() - start_time) * 1000  # мс
                    
                    metrics = {
                        "startup_time_ms": round(startup_time, 2),
                        "app_initialized": True
                    }
                    
                    if startup_time > 5000:  # Больше 5 секунд
                        return False, f"Медленный запуск: {startup_time}мс", metrics
                    else:
                        return True, f"Быстрый запуск: {startup_time}мс", metrics
                else:
                    metrics = {"app_initialized": False}
                    return False, "Приложение не инициализировано", metrics
            else:
                metrics = {"app_exists": False}
                return False, "Файл app.py не найден", metrics
                
        except Exception as e:
            metrics = {"error": str(e)}
            return False, f"Ошибка запуска: {str(e)}", metrics

    def _test_memory_usage(self) -> Tuple[bool, str, Dict]:
        """Базовая проверка использования памяти"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Имитация нагрузки - импорт нескольких модулей
        modules_to_load = ['core.config', 'database.models']
        loaded_modules = []
        
        for module_name in modules_to_load:
            try:
                module_path = self.base_dir / module_name.replace('.', '/') + ".py"
                if module_path.exists():
                    spec = importlib.util.spec_from_file_location(
                        module_name, module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    loaded_modules.append(module)
            except:
                pass
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        metrics = {
            "initial_memory_mb": round(initial_memory, 2),
            "final_memory_mb": round(final_memory, 2),
            "memory_increase_mb": round(memory_increase, 2),
            "modules_loaded": len(loaded_modules)
        }
        
        if memory_increase > 100:  # Больше 100MB
            return False, f"Высокое использование памяти: +{memory_increase}MB", metrics
        else:
            return True, f"Использование памяти нормальное: +{memory_increase}MB", metrics

    def test_security_checks(self):
        """Проверка безопасности кода"""
        self.print_header("🔒 ПРОВЕРКА БЕЗОПАСНОСТИ")

        security_checks = {
            "environment_variables": self._check_environment_security,
            "dependencies_vulnerabilities": self._check_dependencies_security,
            "code_security_patterns": self._check_code_security_patterns
        }

        for check_name, check_func in security_checks.items():
            try:
                success, details, metrics = check_func()
                self.print_result(
                    f"Безопасность: {check_name}",
                    success,
                    details
                )
                self.test_results["security_checks"][check_name] = {
                    "status": "PASS" if success else "FAIL",
                    "details": details,
                    "metrics": metrics
                }
            except Exception as e:
                self.print_result(
                    f"Безопасность: {check_name}",
                    False,
                    f"Ошибка проверки: {str(e)}"
                )

    def _check_environment_security(self) -> Tuple[bool, str, Dict]:
        """Проверка безопасности переменных окружения"""
        env_example = self.base_dir / ".env.example"
        security_issues = []
        
        if env_example.exists():
            try:
                with open(env_example, 'r') as f:
                    content = f.read()
                
                # Проверка наличия чувствительных данных в примере
                sensitive_patterns = [
                    "SECRET_KEY=", "PASSWORD=", "TOKEN=", 
                    "API_KEY=", "PRIVATE_KEY="
                ]
                
                for pattern in sensitive_patterns:
                    if pattern in content:
                        # Проверяем, что это не пример значения
                        lines = content.split('\n')
                        for line in lines:
                            if pattern in line and not line.strip().startswith('#'):
                                if "example" not in line.lower() and "changeme" not in line.lower():
                                    security_issues.append(f"Возможная утечка в: {line.strip()}")
                
            except Exception as e:
                security_issues.append(f"Ошибка чтения .env.example: {str(e)}")
        
        metrics = {
            "security_issues_found": len(security_issues),
            "issues_details": security_issues
        }
        
        if security_issues:
            return False, f"Проблемы безопасности: {len(security_issues)}", metrics
        else:
            return True, "Переменные окружения безопасны", metrics

    def _check_dependencies_security(self) -> Tuple[bool, str, Dict]:
        """Базовая проверка безопасности зависимостей"""
        requirements_file = self.base_dir / "requirements.txt"
        security_issues = []
        
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    requirements = f.readlines()
                
                # Проверка на известные проблемные пакеты
                problematic_packages = {
                    "pickle": "Небезопасная сериализация",
                    "marshal": "Небезопасная сериализация", 
                    "yaml": "Возможные уязвимости при load()",
                    "eval": "Опасная функция выполнения кода"
                }
                
                for req in requirements:
                    req_lower = req.lower()
                    for pkg, issue in problematic_packages.items():
                        if pkg in req_lower and not req_lower.startswith('#'):
                            security_issues.append(f"{req.strip()}: {issue}")
                
            except Exception as e:
                security_issues.append(f"Ошибка анализа requirements: {str(e)}")
        
        metrics = {
            "security_issues": len(security_issues),
            "issues_details": security_issues
        }
        
        if security_issues:
            return False, f"Проблемные зависимости: {len(security_issues)}", metrics
        else:
            return True, "Зависимости безопасны", metrics

    def _check_code_security_patterns(self) -> Tuple[bool, str, Dict]:
        """Проверка паттернов безопасности в коде"""
        python_files = list(self.base_dir.rglob("*.py"))
        security_issues = []
        
        dangerous_patterns = {
            "exec(": "Опасное выполнение кода",
            "eval(": "Опасное выполнение кода", 
            "pickle.loads": "Небезопасная десериализация",
            "yaml.load": "Небезопасная загрузка YAML",
            "subprocess.run": "Возможная инъекция команд",
            "os.system": "Опасный вызов системных команд"
        }
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, description in dangerous_patterns.items():
                    if pattern in content:
                        # Игнорируем закомментированные строки и тесты
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if pattern in line and not line.strip().startswith('#'):
                                if "test" not in str(py_file).lower():
                                    security_issues.append(
                                        f"{py_file.name}:{i} - {description}"
                                    )
                
            except Exception as e:
                security_issues.append(f"{py_file.name}: ошибка анализа - {str(e)}")
        
        metrics = {
            "files_checked": len(python_files),
            "security_issues": len(security_issues),
            "issues_details": security_issues[:10]  # Ограничиваем вывод
        }
        
        if security_issues:
            return False, f"Опасные паттерны: {len(security_issues)}", metrics
        else:
            return True, "Код безопасен", metrics

    # ========== СУЩЕСТВУЮЩИЕ ФУНКЦИИ (СОХРАНЯЕМ) ==========

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
        """Сканирование и анализ структуры проекта (существующая функция)"""
        # ... существующий код ...

    def run_comprehensive_test(self):
        """Запуск расширенного комплексного тестирования"""
        self.print_header("🚀 РАСШИРЕННЫЙ КОМПЛЕКСНЫЙ ТЕСТ ПРОЕКТА")
        
        # Существующие тесты
        self.scan_project_structure()
        
        # Новые расширенные тесты
        self.test_code_execution()
        self.test_code_quality() 
        self.test_performance_metrics()
        self.test_security_checks()
        
        # Генерация улучшенного отчета
        self.generate_detailed_analysis()
        
        return self.generate_final_report()

    def generate_detailed_analysis(self):
        """Генерация детального анализа проекта"""
        analysis = {
            "import_errors": self.import_errors,
            "runtime_errors": self.runtime_errors,
            "code_issues": self.code_issues,
            "overall_health_score": self.calculate_health_score(),
            "recommendations_priority": self.prioritize_recommendations()
        }
        
        self.test_results["detailed_analysis"] = analysis

    def calculate_health_score(self) -> float:
        """Расчет общего показателя здоровья проекта"""
        total_checks = self.test_results["score"]["total_tests"]
        passed_checks = self.test_results["score"]["passed_tests"]
        
        if total_checks == 0:
            return 0.0
        
        base_score = (passed_checks / total_checks) * 100
        
        # Штрафы за критические ошибки
        penalty = len(self.import_errors) * 5 + len(self.runtime_errors) * 10
        final_score = max(0, base_score - penalty)
        
        return round(final_score, 2)

    def prioritize_recommendations(self) -> List[Dict]:
        """Приоритизация рекомендаций по критичности"""
        recommendations = []
        
        # Критические проблемы
        if self.import_errors:
            recommendations.append({
                "priority": "CRITICAL",
                "message": "Исправьте ошибки импорта",
                "details": self.import_errors[:3]
            })
        
        if self.runtime_errors:
            recommendations.append({
                "priority": "HIGH", 
                "message": "Исправьте ошибки выполнения",
                "details": self.runtime_errors[:3]
            })
        
        # Предупреждения
        security_issues = self.test_results["security_checks"].get("issues", [])
        if security_issues:
            recommendations.append({
                "priority": "HIGH",
                "message": "Устраните проблемы безопасности",
                "details": security_issues[:3]
            })
        
        return recommendations

    def generate_final_report(self):
        """Генерация финального отчета"""
        self.print_header("📊 ДЕТАЛЬНЫЙ ФИНАЛЬНЫЙ ОТЧЕТ")
        
        health_score = self.calculate_health_score()
        
        print(f"🏁 ОБЩИЙ СТАТУС: {self.test_results['overall_status']}")
        print(f"❤️  ЗДОРОВЬЕ ПРОЕКТА: {health_score}%")
        print(f"✅ ВЫПОЛНЕНО ТЕСТОВ: {self.test_results['score']['passed_tests']}/{self.test_results['score']['total_tests']}")
        
        # Детальная аналитика
        print(f"\n📈 ДЕТАЛЬНАЯ АНАЛИТИКА:")
        print(f"   • Ошибки импорта: {len(self.import_errors)}")
        print(f"   • Ошибки выполнения: {len(self.runtime_errors)}")
        print(f"   • Проблемы кода: {len(self.code_issues)}")
        
        # Рекомендации
        print(f"\n🎯 ПРИОРИТЕТНЫЕ РЕКОМЕНДАЦИИ:")
        for rec in self.prioritize_recommendations():
            print(f"   • [{rec['priority']}] {rec['message']}")
        
        # Сохранение полного отчета
        self.save_comprehensive_report()
        
        return health_score > 70  # Проект считается успешным при здоровье >70%

    def save_comprehensive_report(self):
        """Сохранение комплексного отчета"""
        report_file = self.base_dir / "advanced_comprehensive_project_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Расширенный отчет сохранен в: {report_file}")
        except Exception as e:
            print(f"\n❌ Ошибка сохранения отчета: {e}")

def main():
    """Основная функция расширенного тестирования"""
    print("🚀 ЗАПУСК РАСШИРЕННОГО КОМПЛЕКСНОГО ТЕСТА")
    print("Этот тест проверит не только структуру, но и работоспособность кода")
    
    try:
        tester = AdvancedComprehensiveProjectTest()
        success = tester.run_comprehensive_test()
        
        if success:
            print("\n🎉 ПРОЕКТ ПРОШЕЛ РАСШИРЕННОЕ ТЕСТИРОВАНИЕ!")
        else:
            print("\n🔧 ТРЕБУЮТСЯ ДОРАБОТКИ - см. рекомендации в отчете")
            
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА ТЕСТИРОВАНИЯ: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()