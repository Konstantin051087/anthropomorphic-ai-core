#!/usr/bin/env python3
"""
Скрипт проверки развертывания для Emotional AI
Проверяет все компоненты системы перед деплоем
"""

import os
import sys
import requests
import psycopg2
from urllib.parse import urlparse
import logging

# Добавляем путь к shared модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.logger import setup_logger
from shared.utils import get_current_timestamp

logger = setup_logger(__name__)

class DeploymentChecker:
    """Класс для проверки развертывания системы"""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.results = []
    
    def log_result(self, check_name: str, success: bool, message: str = ""):
        """Логирование результата проверки"""
        status = "PASS" if success else "FAIL"
        result = {
            "check": check_name,
            "status": status,
            "message": message,
            "timestamp": get_current_timestamp().isoformat()
        }
        
        self.results.append(result)
        
        if success:
            self.checks_passed += 1
            logger.info(f"✅ {check_name}: {message}")
        else:
            self.checks_failed += 1
            logger.error(f"❌ {check_name}: {message}")
    
    def check_environment_variables(self):
        """Проверка переменных окружения"""
        required_vars = [
            'DATABASE_URL',
            'SECRET_KEY',
            'AI_SERVICE_URL'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.log_result(
                "Environment Variables",
                False,
                f"Missing variables: {', '.join(missing_vars)}"
            )
        else:
            self.log_result(
                "Environment Variables",
                True,
                "All required environment variables are set"
            )
    
    def check_database_connection(self):
        """Проверка подключения к базе данных"""
        try:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                self.log_result("Database Connection", False, "DATABASE_URL not set")
                return
            
            # Конвертируем postgres:// в postgresql:// для psycopg2
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
            
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            
            # Проверяем возможность выполнить запрос
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            self.log_result(
                "Database Connection",
                True,
                f"Connected to database: {db_version[0] if db_version else 'Unknown'}"
            )
            
        except Exception as e:
            self.log_result("Database Connection", False, f"Connection failed: {str(e)}")
    
    def check_web_service(self):
        """Проверка веб-сервиса"""
        try:
            web_service_url = os.getenv('WEB_SERVICE_URL', 'http://localhost:5000')
            response = requests.get(f"{web_service_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Web Service",
                    True,
                    f"Service is healthy: {data.get('status', 'unknown')}"
                )
            else:
                self.log_result(
                    "Web Service",
                    False,
                    f"Health check failed with status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Web Service", False, f"Connection failed: {str(e)}")
    
    def check_ai_service(self):
        """Проверка AI сервиса"""
        try:
            ai_service_url = os.getenv('AI_SERVICE_URL', 'http://localhost:8001')
            response = requests.get(f"{ai_service_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "AI Service",
                    True,
                    f"Service is healthy: {data.get('status', 'unknown')}"
                )
            else:
                self.log_result(
                    "AI Service",
                    False,
                    f"Health check failed with status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("AI Service", False, f"Connection failed: {str(e)}")
    
    def check_dependencies(self):
        """Проверка зависимостей Python"""
        try:
            import flask
            import torch
            import transformers
            import psycopg2
            import requests
            
            self.log_result(
                "Python Dependencies",
                True,
                "All critical dependencies are available"
            )
            
        except ImportError as e:
            self.log_result("Python Dependencies", False, f"Missing dependency: {str(e)}")
    
    def check_disk_space(self):
        """Проверка свободного места на диске"""
        try:
            stat = os.statvfs('/' if os.name != 'nt' else 'C:\\\\')
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
            
            if free_gb > 1:  # Минимум 1GB свободного места
                self.log_result(
                    "Disk Space",
                    True,
                    f"Sufficient disk space: {free_gb:.1f}GB available"
                )
            else:
                self.log_result(
                    "Disk Space",
                    False,
                    f"Low disk space: {free_gb:.1f}GB available"
                )
                
        except Exception as e:
            self.log_result("Disk Space", False, f"Check failed: {str(e)}")
    
    def run_all_checks(self):
        """Запуск всех проверок"""
        logger.info("🚀 Starting deployment checks...")
        
        checks = [
            self.check_environment_variables,
            self.check_dependencies,
            self.check_disk_space,
            self.check_database_connection,
            self.check_web_service,
            self.check_ai_service
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.log_result(check.__name__, False, f"Check crashed: {str(e)}")
        
        # Сводка
        logger.info("\\n" + "="*50)
        logger.info("📊 DEPLOYMENT CHECK SUMMARY")
        logger.info("="*50)
        
        for result in self.results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            logger.info(f"{status_icon} {result['check']}: {result['message']}")
        
        logger.info("="*50)
        logger.info(f"Total: {self.checks_passed} passed, {self.checks_failed} failed")
        
        if self.checks_failed == 0:
            logger.info("🎉 All checks passed! Deployment can proceed.")
            return True
        else:
            logger.error("💥 Some checks failed! Please fix issues before deployment.")
            return False

def main():
    """Основная функция"""
    checker = DeploymentChecker()
    success = checker.run_all_checks()
    
    # Сохранение результатов в файл
    with open("deployment_check_results.json", "w") as f:
        import json
        json.dump(checker.results, f, indent=2, default=str)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()