#!/usr/bin/env python3
"""
Валидация инфраструктуры для Python 3.12.3/3.13.4
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class InfrastructureValidator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.errors = []
        self.warnings = []
    
    def validate_python_version(self):
        """Проверка версии Python"""
        version = sys.version_info
        expected_versions = [(3, 12, 3), (3, 13, 4)]
        current = (version.major, version.minor, version.micro)
        
        if current in expected_versions:
            logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} - совместим")
        else:
            self.warnings.append(
                f"Python {version.major}.{version.minor}.{version.micro} - "
                f"отличается от тестируемых версий"
            )
    
    def validate_environment_files(self):
        """Проверка файлов окружения"""
        env_files = [".env.example", ".env"]
        
        for env_file in env_files:
            path = self.base_dir / env_file
            if path.exists():
                logger.info(f"✅ Файл окружения найден: {env_file}")
            else:
                if env_file == ".env":
                    self.warnings.append(f"Файл {env_file} отсутствует (ожидается в продакшене)")
                else:
                    self.errors.append(f"Обязательный файл отсутствует: {env_file}")
    
    def validate_config_files(self):
        """Проверка конфигурационных файлов"""
        config_files = [
            "data/configs/system_config.json",
            "data/configs/psyche_config.json",
            "data/configs/memory_config.json", 
            "data/configs/mood_config.json"
        ]
        
        for config_file in config_files:
            path = self.base_dir / config_file
            if path.exists():
                logger.info(f"✅ Конфигурационный файл найден: {config_file}")
            else:
                self.errors.append(f"Конфигурационный файл отсутствует: {config_file}")
    
    def validate_deploy_templates(self):
        """Проверка шаблонов деплоя"""
        deploy_files = ["render.yaml", "Dockerfile", "scripts/deploy_render.sh"]
        
        for deploy_file in deploy_files:
            path = self.base_dir / deploy_file
            if path.exists():
                logger.info(f"✅ Шаблон деплоя найден: {deploy_file}")
            else:
                self.errors.append(f"Шаблон деплоя отсутствует: {deploy_file}")
    
    def validate_api_structure(self):
        """Проверка структуры API"""
        api_files = [
            "api/__init__.py",
            "api/app.py", 
            "api/routes.py",
            "api/models.py",
            "api/dependencies.py",
            "api/middleware.py"
        ]
        
        for api_file in api_files:
            path = self.base_dir / api_file
            if path.exists():
                logger.info(f"✅ API файл найден: {api_file}")
            else:
                self.errors.append(f"API файл отсутствует: {api_file}")
    
    def validate_utils_structure(self):
        """Проверка структуры утилит"""
        utils_files = [
            "utils/__init__.py",
            "utils/logger.py",
            "utils/helpers.py"
        ]
        
        for utils_file in utils_files:
            path = self.base_dir / utils_file
            if path.exists():
                logger.info(f"✅ Утилита найдена: {utils_file}")
            else:
                self.errors.append(f"Утилита отсутствует: {utils_file}")
    
    def run_validation(self):
        """Запуск полной валидации"""
        logger.info("🔍 Запуск валидации инфраструктуры...")
        
        checks = [
            self.validate_python_version,
            self.validate_environment_files, 
            self.validate_config_files,
            self.validate_deploy_templates,
            self.validate_api_structure,
            self.validate_utils_structure
        ]
        
        for check in checks:
            check()
        
        # Вывод результатов
        logger.info("\n" + "="*50)
        logger.info("РЕЗУЛЬТАТЫ ВАЛИДАЦИИ")
        logger.info("="*50)
        
        if self.errors:
            logger.error("❌ ОШИБКИ:")
            for error in self.errors:
                logger.error(f"  - {error}")
        else:
            logger.info("✅ Ошибки не обнаружены")
        
        if self.warnings:
            logger.warning("⚠ ПРЕДУПРЕЖДЕНИЯ:")
            for warning in self.warnings:
                logger.warning(f"  - {warning}")
        else:
            logger.info("✅ Предупреждения отсутствуют")
        
        if not self.errors:
            logger.info("\n🎉 ИНФРАСТРУКТУРА ГОТОВА К ДЕПЛОЮ!")
            return True
        else:
            logger.error("\n💥 Требуется исправление ошибок перед деплоем")
            return False

if __name__ == "__main__":
    validator = InfrastructureValidator()
    success = validator.run_validation()
    sys.exit(0 if success else 1)