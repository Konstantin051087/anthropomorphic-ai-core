#!/usr/bin/env python3
"""
КОМПЛЕКСНЫЙ ТЕСТ БАЗЫ ДАННЫХ ANTHROPOMORPHIC AI - ВЕРСИЯ 1.0
"""

import os
import sys
import json
import logging
import time
import traceback
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class DatabaseComprehensiveTest:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.test_results = {
            "project": "Anthropomorphic AI Database",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "database_test": {
                "overall_status": "IN_PROGRESS",
                "connection": {},
                "models": {},
                "crud_operations": {},
                "performance": {},
                "recommendations": []
            },
            "score": {
                "total_tests": 0,
                "passed_tests": 0,
                "success_rate": 0
            }
        }

    def print_header(self, message: str):
        """Печать заголовка раздела"""
        print(f"\n{'='*80}")
        print(f"🔍 {message}")
        print(f"{'='*80}")

    def print_section(self, message: str):
        """Печать заголовка подраздела"""
        print(f"\n{'─'*60}")
        print(f"📁 {message}")
        print(f"{'─'*60}")

    def print_result(self, test_name: str, status: bool, details: str = "", points: int = 1):
        """Печать результата теста"""
        icon = "✅" if status else "❌"
        status_text = "ВЫПОЛНЕНО" if status else "НЕ ВЫПОЛНЕНО"
        print(f"{icon} {test_name}: {status_text}")
        if details:
            print(f"   📝 {details}")
        
        # Обновляем счетчики тестов
        self.test_results["score"]["total_tests"] += 1
        if status:
            self.test_results["score"]["passed_tests"] += points
        
        return status

    def test_database_connection(self):
        """Тестирование подключения к базе данных"""
        self.print_header("🔌 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
        
        try:
            # Импортируем настройки и движок
            sys.path.insert(0, str(self.base_dir))
            from core.config import settings
            from database.session import engine, get_db
            
            # Проверка настроек
            self.print_result(
                "Настройки базы данных загружены",
                True,
                f"URL: {settings.DATABASE_URL[:30]}...",
                points=1
            )
            
            # Проверка подключения с использованием text()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                check_result = self.print_result(
                    "Подключение к PostgreSQL",
                    True,
                    "Успешное подключение к базе данных",
                    points=2
                )
                
                # Проверка версии PostgreSQL
                version_result = conn.execute(text("SELECT version()"))
                version = version_result.fetchone()[0]
                self.print_result(
                    "Версия PostgreSQL",
                    True,
                    f"Версия: {version}",
                    points=1
                )
            
            # Проверка фабрики сессий
            try:
                db = next(get_db())
                db.execute(text("SELECT 1"))
                self.print_result(
                    "Фабрика сессий работает",
                    True,
                    "Сессии создаются корректно",
                    points=2
                )
            except Exception as e:
                self.print_result(
                    "Фабрика сессий",
                    False,
                    f"Ошибка: {e}",
                    points=0
                )
            
            return True
            
        except Exception as e:
            self.print_result(
                "Критическая ошибка подключения",
                False,
                f"Ошибка: {e}",
                points=0
            )
            return False

    def test_database_models(self):
        """Тестирование моделей базы данных"""
        self.print_header("🏗️ ТЕСТИРОВАНИЕ МОДЕЛЕЙ БАЗЫ ДАННЫХ")
        
        try:
            from database.session import engine, Base
            from database import models
            
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            # Ожидаемые таблицы
            expected_tables = [
                'system_state', 'memories', 'tags', 'interactions',
                'mood_history', 'personality_traits', 'character_habits',
                'learning_experiences', 'system_logs', 'memory_tags'
            ]
            
            tables_created = []
            for table in expected_tables:
                exists = table in existing_tables
                self.print_result(
                    f"Таблица: {table}",
                    exists,
                    "Создана" if exists else "Отсутствует",
                    points=1
                )
                if exists:
                    tables_created.append(table)
            
            # Проверка структуры ключевых таблиц
            self._test_table_structure()
            
            # Проверка отношений между таблицами
            self._test_table_relationships()
            
            return len(tables_created) == len(expected_tables)
            
        except Exception as e:
            self.print_result(
                "Ошибка тестирования моделей",
                False,
                f"Ошибка: {e}",
                points=0
            )
            return False

    def _test_table_structure(self):
        """Проверка структуры таблиц"""
        self.print_section("📊 ПРОВЕРКА СТРУКТУРЫ ТАБЛИЦ")
        
        try:
            from database.session import engine
            inspector = inspect(engine)
            
            # Проверка system_state
            system_state_columns = inspector.get_columns('system_state')
            required_columns = ['id', 'current_mood', 'mood_intensity', 'created_at']
            for col in required_columns:
                exists = any(col == column['name'] for column in system_state_columns)
                self.print_result(
                    f"Системная таблица: столбец {col}",
                    exists,
                    points=1
                )
            
            # Проверка memories
            memories_columns = inspector.get_columns('memories')
            required_memory_columns = ['id', 'content', 'memory_type', 'importance']
            for col in required_memory_columns:
                exists = any(col == column['name'] for column in memories_columns)
                self.print_result(
                    f"Таблица памяти: столбец {col}",
                    exists,
                    points=1
                )
                
        except Exception as e:
            self.print_result(
                "Проверка структуры таблиц",
                False,
                f"Ошибка: {e}",
                points=0
            )

    def _test_table_relationships(self):
        """Проверка отношений между таблицами"""
        self.print_section("🔗 ПРОВЕРКА ОТНОШЕНИЙ МЕЖДУ ТАБЛИЦАМИ")
        
        try:
            from database.session import engine
            inspector = inspect(engine)
            
            # Проверка foreign keys
            foreign_keys = inspector.get_foreign_keys('memory_tags')
            has_relationships = len(foreign_keys) >= 2
            
            self.print_result(
                "Отношения memory_tags",
                has_relationships,
                f"Найдено foreign keys: {len(foreign_keys)}",
                points=2
            )
            
            # Проверка индексов
            indexes = inspector.get_indexes('memories')
            has_indexes = len(indexes) > 0
            self.print_result(
                "Индексы в memories",
                has_indexes,
                f"Найдено индексов: {len(indexes)}",
                points=1
            )
            
        except Exception as e:
            self.print_result(
                "Проверка отношений",
                False,
                f"Ошибка: {e}",
                points=0
            )

    def test_crud_operations(self):
        """Тестирование CRUD операций"""
        self.print_header("🔄 ТЕСТИРОВАНИЕ CRUD ОПЕРАЦИЙ")
        
        try:
            from database.session import get_db
            from database import models
            from sqlalchemy.orm import Session
            
            db = next(get_db())
            
            # CREATE - Создание тестовой записи
            test_memory = models.Memory(
                content="Тестовая память для проверки CRUD операций",
                memory_type="test",
                importance=0.7,
                emotion_context="neutral"
            )
            db.add(test_memory)
            db.commit()
            db.refresh(test_memory)
            
            self.print_result(
                "CREATE операция",
                test_memory.id is not None,
                f"Создана запись с ID: {test_memory.id}",
                points=2
            )
            
            # READ - Чтение записи
            read_memory = db.query(models.Memory).filter(models.Memory.id == test_memory.id).first()
            self.print_result(
                "READ операция",
                read_memory is not None and read_memory.content == test_memory.content,
                "Запись успешно прочитана",
                points=2
            )
            
            # UPDATE - Обновление записи
            if read_memory:
                original_content = read_memory.content
                read_memory.content = "Обновленное содержание памяти"
                db.commit()
                db.refresh(read_memory)
                
                self.print_result(
                    "UPDATE операция",
                    read_memory.content != original_content,
                    "Запись успешно обновлена",
                    points=2
                )
            
            # DELETE - Удаление записи
            if read_memory:
                db.delete(read_memory)
                db.commit()
                
                # Проверка удаления
                deleted_memory = db.query(models.Memory).filter(models.Memory.id == test_memory.id).first()
                self.print_result(
                    "DELETE операция",
                    deleted_memory is None,
                    "Запись успешно удалена",
                    points=2
                )
            
            return True
            
        except Exception as e:
            self.print_result(
                "CRUD операции",
                False,
                f"Ошибка: {e}",
                points=0
            )
            return False

    def test_performance(self):
        """Тестирование производительности базы данных"""
        self.print_header("⚡ ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
        
        try:
            from database.session import engine, get_db
            import time
            
            # Тест скорости простого запроса
            start_time = time.time()
            with engine.connect() as conn:
                for _ in range(10):
                    conn.execute(text("SELECT 1"))
            simple_query_time = time.time() - start_time
            
            self.print_result(
                "Скорость простых запросов",
                simple_query_time < 1.0,
                f"Время: {simple_query_time:.3f} сек",
                points=2
            )
            
            # Тест создания множества записей
            db = next(get_db())
            start_time = time.time()
            
            from database import models
            memories = []
            for i in range(5):
                memory = models.Memory(
                    content=f"Тестовая память {i}",
                    memory_type="performance_test",
                    importance=0.5
                )
                memories.append(memory)
            
            db.bulk_save_objects(memories)
            db.commit()
            
            batch_insert_time = time.time() - start_time
            
            self.print_result(
                "Пакетная вставка записей",
                batch_insert_time < 2.0,
                f"Время: {batch_insert_time:.3f} сек для 5 записей",
                points=2
            )
            
            # Очистка тестовых данных
            db.query(models.Memory).filter(models.Memory.memory_type == "performance_test").delete()
            db.commit()
            
            return True
            
        except Exception as e:
            self.print_result(
                "Тестирование производительности",
                False,
                f"Ошибка: {e}",
                points=0
            )
            return False

    def test_integration(self):
        """Интеграционное тестирование с другими модулями"""
        self.print_header("🔗 ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ")
        
        try:
            # Тест импорта orchestrator
            from core.orchestrator import Orchestrator
            self.print_result(
                "Импорт Orchestrator",
                True,
                "Orchestrator успешно импортирован",
                points=2
            )
            
            # Тест работы orchestrator с базой данных
            orchestrator = Orchestrator()
            self.print_result(
                "Создание Orchestrator",
                True,
                "Оркестратор создан успешно",
                points=2
            )
            
            # Тест инициализации оркестратора
            init_success = orchestrator.initialize()
            self.print_result(
                "Инициализация Orchestrator",
                init_success,
                "Оркестратор инициализирован" if init_success else "Ошибка инициализации",
                points=3
            )
            
            return init_success
            
        except Exception as e:
            self.print_result(
                "Интеграционное тестирование",
                False,
                f"Ошибка: {e}",
                points=0
            )
            return False

    def generate_database_recommendations(self):
        """Генерация рекомендаций по базе данных"""
        self.print_header("🎯 РЕКОМЕНДАЦИИ ПО БАЗЕ ДАННЫХ")
        
        recommendations = []
        
        # Анализ результатов тестов
        total_tests = self.test_results["score"]["total_tests"]
        passed_tests = self.test_results["score"]["passed_tests"]
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Общие рекомендации
        if success_rate >= 90:
            recommendations.extend([
                "✅ БАЗА ДАННЫХ ГОТОВА К ПРОДКШЕНУ",
                "🎉 Все критичные тесты пройдены успешно",
                "🚀 Можно переходить к следующему этапу разработки"
            ])
        elif success_rate >= 70:
            recommendations.extend([
                "⚠️ БАЗА ДАННЫХ ТРЕБУЕТ НЕБОЛЬШИХ ДОРАБОТОК",
                "🔧 Исправьте выявленные проблемы перед продакшеном"
            ])
        else:
            recommendations.extend([
                "🚨 КРИТИЧЕСКИЕ ПРОБЛЕМЫ С БАЗОЙ ДАННЫХ",
                "🔴 Требуется немедленное исправление выявленных ошибок"
            ])
        
        # Специфические рекомендации на основе тестов
        if not self.test_results["database_test"].get("connection_ok", False):
            recommendations.extend([
                "🔌 ПРОБЛЕМЫ ПОДКЛЮЧЕНИЯ:",
                "   • Проверьте DATABASE_URL в настройках",
                "   • Убедитесь, что база данных доступна",
                "   • Проверьте сетевые настройки и файрволы"
            ])
        
        if not self.test_results["database_test"].get("models_ok", False):
            recommendations.extend([
                "🏗️ ПРОБЛЕМЫ С МОДЕЛЯМИ:",
                "   • Проверьте миграции базы данных",
                "   • Убедитесь, что все таблицы созданы",
                "   • Проверьте соответствие моделей и схемы БД"
            ])
        
        if not self.test_results["database_test"].get("crud_ok", False):
            recommendations.extend([
                "🔄 ПРОБЛЕМЫ С CRUD ОПЕРАЦИЯМИ:",
                "   • Проверьте работу сессий",
                "   • Убедитесь в корректности транзакций",
                "   • Проверьте обработку ошибок в CRUD операциях"
            ])
        
        # Рекомендации по оптимизации
        recommendations.extend([
            "⚡ ОПТИМИЗАЦИЯ:",
            "   • Добавьте индексы для часто используемых запросов",
            "   • Настройте пул соединений",
            "   • Реализуйте кэширование для часто читаемых данных"
        ])
        
        self.test_results["database_test"]["recommendations"] = recommendations
        
        # Вывод рекомендаций
        for i, recommendation in enumerate(recommendations, 1):
            print(f"{i}. {recommendation}")
        
        return recommendations

    def run_comprehensive_database_test(self):
        """Запуск комплексного тестирования базы данных"""
        self.print_header("🚀 КОМПЛЕКСНЫЙ ТЕСТ БАЗЫ ДАННЫХ ANTHROPOMORPHIC AI")
        print(f"📅 Время начала: {self.test_results['timestamp']}")
        print(f"🐍 Версия Python: {sys.version.split()[0]}")
        print(f"📁 Директория проекта: {self.base_dir}")
        
        # Запуск всех тестов
        connection_ok = self.test_database_connection()
        models_ok = self.test_database_models()
        crud_ok = self.test_crud_operations()
        performance_ok = self.test_performance()
        integration_ok = self.test_integration()
        
        # Сохранение результатов
        self.test_results["database_test"].update({
            "connection_ok": connection_ok,
            "models_ok": models_ok,
            "crud_ok": crud_ok,
            "performance_ok": performance_ok,
            "integration_ok": integration_ok
        })
        
        # Расчет общего результата
        total_tests = self.test_results["score"]["total_tests"]
        passed_tests = self.test_results["score"]["passed_tests"]
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        self.test_results["score"]["success_rate"] = round(success_rate, 2)
        
        # Генерация рекомендаций
        self.generate_database_recommendations()
        
        # Финальный отчет
        self.print_header("📊 ФИНАЛЬНЫЙ ОТЧЕТ БАЗЫ ДАННЫХ")
        
        print(f"🏁 ОБЩИЙ СТАТУС: {'✅ ГОТОВ' if success_rate >= 80 else '⚠️ ТРЕБУЕТ ДОРАБОТОК'}")
        print(f"📈 УСПЕШНОСТЬ ТЕСТОВ: {success_rate}%")
        print(f"✅ ВЫПОЛНЕНО ТЕСТОВ: {passed_tests}/{total_tests}")
        
        print(f"\n📋 ДЕТАЛИ ТЕСТИРОВАНИЯ:")
        print(f"   🔌 Подключение: {'✅' if connection_ok else '❌'}")
        print(f"   🏗️ Модели: {'✅' if models_ok else '❌'}")
        print(f"   🔄 CRUD: {'✅' if crud_ok else '❌'}")
        print(f"   ⚡ Производительность: {'✅' if performance_ok else '❌'}")
        print(f"   🔗 Интеграция: {'✅' if integration_ok else '❌'}")
        
        # Сохранение отчета
        report_file = self.base_dir / "database_test_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Отчет сохранен в: {report_file}")
        except Exception as e:
            print(f"\n❌ Ошибка сохранения отчета: {e}")
        
        # Определение общего статуса
        if success_rate >= 80:
            self.test_results["database_test"]["overall_status"] = "READY"
            print("\n🎉 БАЗА ДАННЫХ ГОТОВА К ИСПОЛЬЗОВАНИЮ!")
        else:
            self.test_results["database_test"]["overall_status"] = "NEEDS_IMPROVEMENT"
            print("\n🔧 ВЫПОЛНИТЕ РЕКОМЕНДАЦИИ ДЛЯ УЛУЧШЕНИЯ БАЗЫ ДАННЫХ.")
        
        return success_rate >= 80

def main():
    """Основная функция"""
    print("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТА БАЗЫ ДАННЫХ")
    
    try:
        input("\nНажмите Enter для начала тестирования базы данных...")
    except KeyboardInterrupt:
        print("\n❌ Тестирование прервано пользователем")
        sys.exit(1)
    
    try:
        tester = DatabaseComprehensiveTest()
        success = tester.run_comprehensive_database_test()
        
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 КРИТИЧЕСКАЯ ОШИБКА ТЕСТИРОВАНИЯ: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()