"""
Конфигурация для Google Cloud Platform
"""

import os
import logging

logger = logging.getLogger(__name__)

class GCPConfig:
    """Конфигурация GCP"""
    
    # Основные настройки проекта
    PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'ai-personality-project')
    REGION = os.getenv('GCP_REGION', 'us-central1')
    
    # Cloud SQL
    DB_INSTANCE = os.getenv('DB_INSTANCE', 'personality-db-instance')
    DB_NAME = os.getenv('DB_NAME', 'personality_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Cloud Run
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'ai-personality-service')
    SERVICE_URL = os.getenv('SERVICE_URL', '')
    
    # Cloud Storage (для моделей и данных)
    BUCKET_NAME = os.getenv('BUCKET_NAME', 'ai-personality-models')
    
    # AI Platform
    AI_MODEL_NAME = os.getenv('AI_MODEL_NAME', 'emotional_analysis_model')
    AI_MODEL_VERSION = os.getenv('AI_MODEL_VERSION', 'v1')
    
    @classmethod
    def is_gcp_environment(cls):
        """Проверка, работает ли приложение в GCP"""
        return os.getenv('K_SERVICE') is not None  # Cloud Run
    
    @classmethod
    def get_database_url(cls):
        """Получение URL для подключения к базе данных"""
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        
        if cls.is_gcp_environment():
            # Для Cloud SQL в GCP
            return f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}@/{cls.DB_NAME}?host=/cloudsql/{cls.PROJECT_ID}:{cls.REGION}:{cls.DB_INSTANCE}"
        else:
            # Локальная разработка
            return os.getenv('DEV_DATABASE_URL', 'sqlite:///personality.db')
    
    @classmethod
    def get_storage_bucket(cls):
        """Получение имени бакета Cloud Storage"""
        return cls.BUCKET_NAME
    
    @classmethod
    def validate_config(cls):
        """Валидация конфигурации GCP"""
        errors = []
        
        if cls.is_gcp_environment():
            # Проверка обязательных переменных для GCP
            if not cls.DB_PASSWORD:
                errors.append("DB_PASSWORD обязателен для GCP")
            if not cls.PROJECT_ID:
                errors.append("GCP_PROJECT_ID обязателен")
        
        if errors:
            logger.error(f"❌ Ошибки конфигурации GCP: {errors}")
            return False
        
        logger.info("✅ Конфигурация GCP валидна")
        return True
    
    @classmethod
    def get_service_info(cls):
        """Получение информации о сервисе"""
        return {
            'project_id': cls.PROJECT_ID,
            'region': cls.REGION,
            'service_name': cls.SERVICE_NAME,
            'is_gcp_environment': cls.is_gcp_environment(),
            'database_instance': cls.DB_INSTANCE,
            'storage_bucket': cls.BUCKET_NAME
        }

# Автоматическая валидация при импорте
if GCPConfig.is_gcp_environment():
    GCPConfig.validate_config()