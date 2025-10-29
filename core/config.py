"""
Configuration settings for the Anthropomorphic AI System
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./anthropomorphic_ai.db")
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # Hugging Face
    hf_token: str = os.getenv("HF_TOKEN", "")
    
    # Environment
    environment: str = os.getenv("RENDER_ENV", "development")
    
    class Config:
        env_file = ".env"

settings = Settings()