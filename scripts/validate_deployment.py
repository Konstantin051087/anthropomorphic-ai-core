#!/usr/bin/env python3
"""
Скрипт валидации окружения для деплоя
"""

import sys
import os
import subprocess
import platform
import logging
from pathlib import Path
from sqlalchemy import text

# Добавление корневой директории в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentValidator:
    """Валидатор окружения для деплоя"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def check_python_version(self):
        """Проверка версии Python"""
        required_version = (3, 12, 3)
        current_version = sys.version_info
        
        if (current_version.major, current_version.minor, current_version.micro) != required_version:
            self.errors.append(
                f"Неверная версия Python. Требуется {required_version}, установлена {current_version}"
            )
        else:
            logger.info(f"✓ Версия Python: {current_version}")
    
    def check_required_files(self):
        """Проверка наличия обязательных файлов"""
        required_files = [
            "requirements.txt",
            "runtime.txt",
            "Dockerfile",
            "render.yaml",
            "core/config.py",
            "api/app.py",
            "database/models.py",
            ".env.example"
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                self.errors.append(f"Отсутствует обязательный файл: {file_path}")
            else:
                logger.info(f"✓ Файл присутствует: {file_path}")
    
    def check_dependencies(self):
        """Проверка зависимостей"""
        try:
            # Проверка конфликтов зависимостей
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'check'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.errors.append(f"Конфликты зависимостей: {result.stderr}")
            else:
                logger.info("✓ Зависимости без конфликтов")
                
        except subprocess.TimeoutExpired:
            self.warnings.append("Проверка зависимостей превысила таймаут")
        except Exception as e:
            self.errors.append(f"Ошибка проверки зависимостей: {e}")
    
    def check_environment_variables(self):
        """Проверка переменных окружения"""
        required_vars = [
            "DATABASE_URL",
            "RENDER_ENV",
            "SECRET_KEY"
        ]
        
        for var in required_vars:
            if not hasattr(settings, var) or not getattr(settings, var):
                self.warnings.append(f"Переменная окружения {var} не установлена")
            else:
                logger.info(f"✓ Переменная окружения: {var}")
    
    def check_database_connection():
    """Проверка подключения к базе данных"""
        try:
            from database.session import engine
            with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
        logger.info("✓ Подключение к базе данных успешно")
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка подключения к базе данных: {e}")
        return False
    
    def check_directory_structure(self):
        """Проверка структуры директорий"""
        required_dirs = [
            "api",
            "core", 
            "modules",
            "database",
            "scripts",
            "tests",
            "data/configs",
            "utils",
            "docs",
            ".github/workflows"
        ]
        
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                self.errors.append(f"Отсутствует обязательная директория: {dir_path}")
            else:
                logger.info(f"✓ Директория присутствует: {dir_path}")
    
    def check_api_server(self):
        """Проверка возможности запуска API сервера"""
        try:
            # Проверка импорта основных модулей
            from api.app import app
            from core.orchestrator import Orchestrator
            from database.models import SystemState
            
            logger.info("✓ Основные модули импортируются успешно")
        except Exception as e:
            self.errors.append(f"Ошибка импорта модулей: {e}")
    
    def validate_all(self):
        """Запуск всех проверок"""
        logger.info("Запуск валидации окружения для деплоя...")
        
        checks = [
            self.check_python_version,
            self.check_required_files,
            self.check_directory_structure,
            self.check_dependencies,
            self.check_environment_variables,
            self.check_database_connection,
            self.check_api_server
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.errors.append(f"Ошибка при выполнении проверки {check.__name__}: {e}")
        
        # Вывод результатов
        if self.warnings:
            logger.warning("Предупреждения:")
            for warning in self.warnings:
                logger.warning(f"  ⚠ {warning}")
        
        if self.errors:
            logger.error("Критические ошибки:")
            for error in self.errors:
                logger.error(f"  ✗ {error}")
            return False
        else:
            logger.info("✓ Все проверки пройдены успешно!")
            return True

def main():
    """Основная функция"""
    validator = DeploymentValidator()
    success = validator.validate_all()
    
    if success:
        logger.info("Окружение готово к деплою!")
        sys.exit(0)
    else:
        logger.error("Обнаружены критические ошибки. Деплой невозможен.")
        sys.exit(1)

if __name__ == "__main__":
    main()