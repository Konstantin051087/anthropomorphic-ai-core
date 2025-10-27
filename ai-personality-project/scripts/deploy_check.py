import os
import sys
import subprocess
import importlib

def check_dependencies():
    """Проверка установленных зависимостей"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'flask_sqlalchemy', 'sqlalchemy', 'transformers',
        'torch', 'numpy', 'requests', 'psutil', 'python_dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace('_', '-'))
            print(f"   ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"   ❌ {package}")
    
    return missing

def check_database():
    """Проверка подключения к базе данных"""
    print("🗄️ Checking database configuration...")
    
    try:
        from ai_personality_project import db, create_app
        app = create_app('testing')
        
        with app.app_context():
            # Проверка подключения
            db.engine.connect()
            print("   ✅ Database connection: OK")
            
            # Проверка таблиц
            from ai_personality_project.database.models import Persona
            table_exists = db.engine.has_table(Persona.__tablename__)
            print(f"   ✅ Database tables: {'OK' if table_exists else 'MISSING'}")
            
        return True
    except Exception as e:
        print(f"   ❌ Database check failed: {e}")
        return False

def check_ai_components():
    """Проверка AI компонентов"""
    print("🤖 Checking AI components...")
    
    try:
        from ai_personality_project.ai_core import AICore
        
        ai_core = AICore()
        ai_core.initialize()
        
        if ai_core._initialized:
            print("   ✅ AI Core: OK")
            
            # Тестовый вызов
            result = ai_core.process_interaction("Тестовое сообщение", 1)
            if result['success']:
                print("   ✅ AI Processing: OK")
            else:
                print(f"   ❌ AI Processing failed: {result.get('error')}")
                return False
        else:
            print("   ❌ AI Core not initialized")
            return False
            
        return True
    except Exception as e:
        print(f"   ❌ AI components check failed: {e}")
        return False

def check_environment():
    """Проверка переменных окружения"""
    print("🌍 Checking environment variables...")
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    optional_vars = ['PORT', 'HOST', 'DEBUG']
    
    all_ok = True
    
    for var in required_vars:
        if os.getenv(var):
            print(f"   ✅ {var}: SET")
        else:
            print(f"   ❌ {var}: MISSING")
            all_ok = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"   ✅ {var}: SET")
        else:
            print(f"   ⚠️ {var}: NOT SET (using default)")
    
    return all_ok

def run_tests():
    """Запуск тестов"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([
            'python', '-m', 'pytest', 
            'ai_personality_project/tests/', 
            '-v', '--tb=short'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ All tests passed")
            return True
        else:
            print(f"   ❌ Tests failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("   ❌ Tests timed out")
        return False
    except Exception as e:
        print(f"   ❌ Tests error: {e}")
        return False

def main():
    """Основная функция проверки"""
    print("🚀 AI Personality Project - Deployment Check")
    print("=" * 50)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Database", check_database),
        ("AI Components", check_ai_components),
        ("Tests", run_tests)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}")
        print("-" * 30)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"   ❌ Check failed with error: {e}")
            results.append((check_name, False))
    
    # Итоговый отчет
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT CHECK REPORT")
    print("=" * 50)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED - Ready for deployment!")
        sys.exit(0)
    else:
        print("🚨 SOME CHECKS FAILED - Please fix issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()