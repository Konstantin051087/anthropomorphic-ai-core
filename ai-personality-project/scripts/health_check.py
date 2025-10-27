import requests
import sys
import time

def health_check(base_url="http://localhost:5000", timeout=30):
    """Комплексная проверка работоспособности сервиса"""
    
    print("🏥 Starting comprehensive health check...")
    
    # Проверка доступности сервиса
    print("1. Checking service availability...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Main endpoint: OK")
        else:
            print(f"   ❌ Main endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Service not available: {e}")
        return False
    
    # Проверка API персонажей
    print("2. Checking personas API...")
    try:
        response = requests.get(f"{base_url}/api/personas", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'personas' in data:
                print(f"   ✅ Personas API: OK ({len(data['personas'])} personas)")
            else:
                print("   ❌ Personas API returned error")
                return False
        else:
            print(f"   ❌ Personas API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Personas API error: {e}")
        return False
    
    # Проверка взаимодействия
    print("3. Testing AI interaction...")
    try:
        test_data = {
            "text": "Привет, как дела?",
            "persona_id": 1
        }
        response = requests.post(f"{base_url}/api/interact", json=test_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'response' in data:
                print(f"   ✅ Interaction API: OK")
                print(f"   💬 Response: {data['response'][:50]}...")
            else:
                print(f"   ❌ Interaction API returned error: {data.get('error')}")
                return False
        else:
            print(f"   ❌ Interaction API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Interaction API error: {e}")
        return False
    
    # Проверка базы данных
    print("4. Checking database operations...")
    try:
        # Создание тестового персонажа
        test_persona = {
            "name": "Test Persona Health Check",
            "personality_traits": {"test": True},
            "emotional_state": {"current_mood": "neutral"}
        }
        response = requests.post(f"{base_url}/api/personas", json=test_persona, timeout=5)
        if response.status_code == 200:
            print("   ✅ Database write: OK")
        else:
            print(f"   ⚠️ Database write test failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Database test error: {e}")
    
    print("🎉 All health checks passed successfully!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Health check for AI Personality Project')
    parser.add_argument('--url', default='http://localhost:5000', help='Base URL to check')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds')
    
    args = parser.parse_args()
    
    success = health_check(args.url, args.timeout)
    sys.exit(0 if success else 1)