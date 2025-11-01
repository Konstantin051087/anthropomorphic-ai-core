"""
Вспомогательные функции
"""

import json
from typing import Any, Dict
from pathlib import Path

def load_json_config(path: Path) -> Dict[str, Any]:
    """Загрузка JSON конфигурации"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Ошибка загрузки конфигурации {path}: {e}")

def ensure_directory(path: Path):
    """Создание директории если не существует"""
    path.mkdir(parents=True, exist_ok=True)