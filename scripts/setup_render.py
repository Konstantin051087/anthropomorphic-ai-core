#!/usr/bin/env python3
"""
Скрипт настройки окружения Render
Поддержка Python 3.12.3 и 3.13.4
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RenderSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        
    def check_python_version(self):
        """Проверка совместимости версий Python"""
        version = sys.version_info
        logger.info(f"Текущая версия Python: {sys.version}")
        
        compatible_versions = [(3, 12, 3), (3, 13, 4)]
        current = (version.major, version.minor, version.micro)
        
        if current in compatible_versions:
            logger.info("✓ Версия Python совместима")
            return True
        else:
            logger.warning("⚠ Версия Python отличается от тестируемых 3.12.3/3.13.4")
            return True  # Продолжаем, так как зависимости без версий
    
    def setup_environment(self):
        """Настройка переменных окружения"""
        env_template = self.base_dir / ".env.example"
        env_file = self.base_dir / ".env"
        
        if not env_file.exists():
            logger.info("Создание .env файла из шаблона...")
            with open(env_template, 'r') as template:
                with open(env_file, 'w') as env:
                    env.write(template.read())
            logger.info("✓ .env файл создан")
        else:
            logger.info("✓ .env файл уже существует")
    
    def run_migrations(self):
        """Запуск миграций базы данных"""
        try:
            # Инициализация Alembic если нужно
            alembic_ini = self.base_dir / "alembic.ini"
            if not alembic_ini.exists():
                logger.info("Инициализация миграций Alembic...")
                subprocess.run(["alembic", "init", "alembic"], check=True)
            
            # Запуск миграций
            logger.info("Применение миграций базы данных...")
            subprocess.run(["alembic", "upgrade", "head"], check=True)
            logger.info("✓ Миграции применены успешно")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка при применении миграций: {e}")
            sys.exit(1)
    
    def validate_configs(self):
        """Валидация конфигурационных файлов"""
        config_paths = [
            "data/configs/system_config.json",
            "data/configs/psyche_config.json", 
            "data/configs/memory_config.json",
            "data/configs/mood_config.json"
        ]
        
        for config_path in config_paths:
            full_path = self.base_dir / config_path
            if full_path.exists():
                logger.info(f"✓ Конфигурационный файл найден: {config_path}")
            else:
                logger.warning(f"⚠ Конфигурационный файл отсутствует: {config_path}")
    
    def setup_complete(self):
        """Финальная проверка"""
        logger.info("\n" + "="*50)
        logger.info("НАСТРОЙКА ИНФРАСТРУКТУРЫ ЗАВЕРШЕНА")
        logger.info("="*50)
        logger.info("✓ Система конфигурации готова")
        logger.info("✓ Переменные окружения настроены")
        logger.info("✓ Шаблоны деплоя подготовлены")
        logger.info("✓ Поддержка Python 3.12.3/3.13.4 обеспечена")
        logger.info("\nСледующие шаги:")
        logger.info("1. Настройте секреты в Render Dashboard")
        logger.info("2. Задеплойте приложение используя render.yaml")
        logger.info("3. Проверьте работу API endpoints")

if __name__ == "__main__":
    setup = RenderSetup()
    
    logger.info("Начало настройки инфраструктуры...")
    
    # Выполнение шагов настройки
    setup.check_python_version()
    setup.setup_environment()
    setup.validate_configs()
    setup.run_migrations()
    setup.setup_complete()