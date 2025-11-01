#!/usr/bin/env python3
"""
Скрипт для помощи в создании базы данных на Render
"""

import json
import sys
from pathlib import Path

def generate_db_setup_instructions():
    """Генерация инструкций по созданию БД на Render"""
    
    instructions = {
        "title": "Инструкция по созданию PostgreSQL базы данных на Render",
        "steps": [
            {
                "step": 1,
                "title": "Вход в Render Dashboard",
                "actions": [
                    "Откройте https://dashboard.render.com",
                    "Войдите в свой аккаунт"
                ]
            },
            {
                "step": 2, 
                "title": "Создание новой PostgreSQL базы данных",
                "actions": [
                    "Нажмите 'New +' в верхнем правом углу",
                    "Выберите 'PostgreSQL'"
                ]
            },
            {
                "step": 3,
                "title": "Настройка параметров базы данных",
                "actions": [
                    "**Name**: `anthropomorphic-ai-db`",
                    "**Database**: `anthropomorphic_ai`", 
                    "**User**: `ai_user`",
                    "**Region**: Выберите ближайший регион (рекомендуется Oregon)",
                    "**PostgreSQL Version**: `15`",
                    "**Plan**: `Starter` (бесплатный)"
                ]
            },
            {
                "step": 4,
                "title": "Создание базы данных",
                "actions": [
                    "Нажмите 'Create Database'",
                    "Дождитесь завершения процесса (2-3 минуты)"
                ]
            },
            {
                "step": 5,
                "title": "Получение connection string",
                "actions": [
                    "После создания перейдите в настройки базы данных",
                    "Найдите 'Internal Database URL'",
                    "Скопируйте значение (оно понадобится для настройки веб-сервиса)"
                ]
            }
        ],
        "important_notes": [
            "Бесплатная база данных автоматически приостанавливается после 90 дней неиспользования",
            "Для продакшн использования рекомендуется выбрать платный план",
            "Connection string имеет формат: postgresql://user:password@host:port/database"
        ],
        "next_steps": [
            "Создайте веб-сервис в Render",
            "Добавьте DATABASE_URL в переменные окружения веб-сервиса",
            "Задеплойте приложение"
        ]
    }
    
    return instructions

def main():
    """Основная функция"""
    print("=" * 60)
    print("ИНСТРУКЦИЯ ПО СОЗДАНИЮ БАЗЫ ДАННЫХ НА RENDER")
    print("=" * 60)
    
    instructions = generate_db_setup_instructions()
    
    print(f"\n{instructions['title']}\n")
    
    for step in instructions['steps']:
        print(f"\nШаг {step['step']}: {step['title']}")
        for action in step['actions']:
            print(f"  • {action}")
    
    print(f"\nВАЖНЫЕ ЗАМЕЧАНИЯ:")
    for note in instructions['important_notes']:
        print(f"  ⚠ {note}")
    
    print(f"\nСЛЕДУЮЩИЕ ШАГИ:")
    for next_step in instructions['next_steps']:
        print(f"  → {next_step}")
    
    # Сохранение инструкций в файл
    output_file = Path("render_db_setup_instructions.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Инструкции сохранены в {output_file}")
    print("\nПосле создания базы данных выполните:")
    print("1. python scripts/validate_deployment.py")
    print("2. python api/app.py")

if __name__ == "__main__":
    main()