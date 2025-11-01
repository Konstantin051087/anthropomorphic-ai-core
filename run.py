#!/usr/bin/env python3
"""
Точка входа для запуска Anthropomorphic AI системы
"""
import sys
import os

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.app import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )