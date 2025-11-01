from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List, Dict, Any
import os
from pathlib import Path

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Базовая конфигурация
    PROJECT_NAME: str = "Anthropomorphic AI Core"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # База данных
    DATABASE_URL: str = Field(default="sqlite:///./test.db", env="DATABASE_URL")
    
    # API настройки
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_RELOAD: bool = Field(default=False, env="API_RELOAD")
    
    # Безопасность
    SECRET_KEY: str = Field(default="fallback-secret-key-for-development-only-2025", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Внешние сервисы
    HUGGINGFACE_TOKEN: Optional[str] = Field(None, env="HF_TOKEN")
    RENDER_ENV: str = Field(default="development", env="RENDER_ENV")
    
    # Настройки модулей
    ENABLED_MODULES: List[str] = Field(default=[
        "core", "api", "database", "memory", "mood"
    ])
    
    # Логирование
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/app.log", env="LOG_FILE")
    
    # CORS настройки
    CORS_ORIGINS: List[str] = Field(default=["*"])
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Изменено с "allow" на "ignore" для игнорирования лишних полей
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            return "sqlite:///./test.db"
        if not v.startswith(("postgresql://", "sqlite://")):
            raise ValueError("Неверный формат DATABASE_URL")
        return v
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            return "fallback-secret-key-for-development-only-2025"
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

# Создание экземпляра настроек с обработкой ошибок
try:
    settings = Settings()
    print(f"✓ Настройки загружены. Режим: {settings.RENDER_ENV}")
except Exception as e:
    print(f"⚠ Ошибка загрузки настроек: {e}. Используются настройки по умолчанию.")
    settings = Settings(
        DATABASE_URL="sqlite:///./test.db",
        SECRET_KEY="fallback-secret-key-for-development-only-2025",
        DEBUG=True,
        RENDER_ENV="development"
    )

def get_settings() -> Settings:
    """Функция для dependency injection"""
    return settings

# Дополнительные утилиты конфигурации
class ConfigManager:
    """Менеджер конфигурации для динамических настроек"""
    
    def __init__(self):
        self._module_configs = {}
        self._load_module_configs()
    
    def _load_module_configs(self):
        """Загрузка конфигураций модулей из JSON файлов"""
        config_dir = Path("data/configs")
        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                module_name = config_file.stem.replace("_config", "")
                try:
                    import json
                    with open(config_file, 'r', encoding='utf-8') as f:
                        self._module_configs[module_name] = json.load(f)
                    print(f"✓ Конфигурация загружена: {module_name}")
                except Exception as e:
                    print(f"⚠ Ошибка загрузки конфигурации {config_file}: {e}")
        else:
            print("⚠ Директория configs не найдена, используются настройки по умолчанию")
    
    def get_module_config(self, module_name: str, default: Any = None) -> Dict:
        """Получение конфигурации модуля"""
        return self._module_configs.get(module_name, default or {})
    
    def update_module_config(self, module_name: str, config: Dict):
        """Обновление конфигурации модуля"""
        self._module_configs[module_name] = config
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Получение всех конфигураций"""
        return {
            "system": {
                "project_name": settings.PROJECT_NAME,
                "version": settings.VERSION,
                "debug": settings.DEBUG,
                "api_host": settings.API_HOST,
                "api_port": settings.API_PORT,
                "render_env": settings.RENDER_ENV
            },
            "modules": self._module_configs
        }

# Глобальный экземпляр менеджера конфигурации
config_manager = ConfigManager()