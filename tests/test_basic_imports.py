"""
Basic import tests for all critical packages
"""

def test_pydantic_import():
    """Test pydantic imports"""
    try:
        from pydantic import BaseModel
        from pydantic_settings import BaseSettings
        assert True
    except ImportError as e:
        assert False, f"Pydantic import failed: {e}"

def test_fastapi_import():
    """Test FastAPI imports"""
    try:
        from fastapi import FastAPI, APIRouter
        assert True
    except ImportError as e:
        assert False, f"FastAPI import failed: {e}"

def test_sqlalchemy_import():
    """Test SQLAlchemy imports"""
    try:
        from sqlalchemy import create_engine, Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        assert True
    except ImportError as e:
        assert False, f"SQLAlchemy import failed: {e}"

def test_core_module_imports():
    """Test all core module imports"""
    try:
        from core.config import settings
        from core.orchestrator import Orchestrator
        from core.main import main
        from utils.logger import setup_logging
        assert True
    except ImportError as e:
        assert False, f"Core module import failed: {e}"