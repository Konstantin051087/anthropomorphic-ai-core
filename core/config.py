"""
Configuration settings for the Anthropomorphic AI System
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "sqlite:///./anthropomorphic_ai.db"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # Hugging Face
    hf_token: Optional[str] = None
    
    # Environment
    environment: str = "development"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()