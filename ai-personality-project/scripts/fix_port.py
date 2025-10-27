#!/usr/bin/env python3
"""
Скрипт для автоматического поиска свободного порта
"""

import socket
import sys

def find_free_port(start_port=5000, max_attempts=100):
    """Находит свободный порт для запуска приложения"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Не удалось найти свободный порт в диапазоне {start_port}-{start_port + max_attempts}")

def main():
    """Основная функция скрипта"""
    try:
        free_port = find_free_port()
        print(f"🎯 Найден свободный порт: {free_port}")
        
        # Записываем порт в файл для использования другими скриптами
        with open('/tmp/ai_personality_port.txt', 'w') as f:
            f.write(str(free_port))
            
        return free_port
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
