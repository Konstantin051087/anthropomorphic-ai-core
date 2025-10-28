#!/usr/bin/env python3
"""
Скрипт мониторинга здоровья Emotional AI системы
Используется для постоянного мониторинга в продакшене
"""

import time
import requests
import json
import logging
import sys
import os
from datetime import datetime, timedelta

# Добавляем путь к shared модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.logger import setup_logger
from shared.utils import get_current_timestamp

logger = setup_logger(__name__)

class HealthMonitor:
    """Монитор здоровья системы Emotional AI"""
    
    def __init__(self, config_path=None):
        self.config = self.load_config(config_path)
        self.service_status = {}
        self.metrics_history = []
        self.max_history_size = 1000
    
    def load_config(self, config_path):
        """Загрузка конфигурации мониторинга"""
        default_config = {
            "web_service_url": os.getenv('WEB_SERVICE_URL', 'http://localhost:5000'),
            "ai_service_url": os.getenv('AI_SERVICE_URL', 'http://localhost:8001'),
            "check_interval": 60,  # seconds
            "timeout": 10,
            "alert_threshold": 3,  # consecutive failures before alert
            "services": [
                {
                    "name": "web-service",
                    "url": os.getenv('WEB_SERVICE_URL', 'http://localhost:5000') + "/health",
                    "type": "http"
                },
                {
                    "name": "ai-service", 
                    "url": os.getenv('AI_SERVICE_URL', 'http://localhost:8001') + "/health",
                    "type": "http"
                }
            ]
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.error(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def check_service_health(self, service_config):
        """Проверка здоровья отдельного сервиса"""
        service_name = service_config['name']
        url = service_config['url']
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=self.config['timeout'])
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'response_time': response_time,
                    'details': data,
                    'timestamp': get_current_timestamp().isoformat()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'response_time': response_time,
                    'error': f"HTTP {response.status_code}",
                    'timestamp': get_current_timestamp().isoformat()
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'unhealthy',
                'response_time': self.config['timeout'],
                'error': 'Request timeout',
                'timestamp': get_current_timestamp().isoformat()
            }
        except requests.exceptions.ConnectionError:
            return {
                'status': 'unhealthy', 
                'response_time': 0,
                'error': 'Connection refused',
                'timestamp': get_current_timestamp().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'response_time': 0,
                'error': str(e),
                'timestamp': get_current_timestamp().isoformat()
            }
    
    def check_system_health(self):
        """Полная проверка здоровья системы"""
        system_status = {
            'timestamp': get_current_timestamp().isoformat(),
            'overall_status': 'healthy',
            'services': {}
        }
        
        unhealthy_services = 0
        
        for service_config in self.config['services']:
            service_name = service_config['name']
            health_status = self.check_service_health(service_config)
            
            system_status['services'][service_name] = health_status
            
            if health_status['status'] != 'healthy':
                unhealthy_services += 1
                system_status['overall_status'] = 'degraded'
            
            # Обновление истории статуса
            self.update_service_history(service_name, health_status)
        
        if unhealthy_services == len(self.config['services']):
            system_status['overall_status'] = 'unhealthy'
        
        # Сохранение метрик
        self.metrics_history.append(system_status)
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history.pop(0)
        
        return system_status
    
    def update_service_history(self, service_name, health_status):
        """Обновление истории статуса сервиса"""
        if service_name not in self.service_status:
            self.service_status[service_name] = {
                'consecutive_failures': 0,
                'last_healthy': None,
                'history': []
            }
        
        service_data = self.service_status[service_name]
        service_data['history'].append(health_status)
        
        if len(service_data['history']) > 100:  # Keep last 100 checks
            service_data['history'].pop(0)
        
        if health_status['status'] == 'healthy':
            service_data['consecutive_failures'] = 0
            service_data['last_healthy'] = get_current_timestamp().isoformat()
        else:
            service_data['consecutive_failures'] += 1
    
    def should_alert(self, service_name):
        """Проверка необходимости отправки алерта"""
        if service_name not in self.service_status:
            return False
        
        service_data = self.service_status[service_name]
        return service_data['consecutive_failures'] >= self.config['alert_threshold']
    
    def generate_alert(self, service_name, health_status):
        """Генерация алерта"""
        service_data = self.service_status[service_name]
        
        alert = {
            'level': 'ERROR',
            'service': service_name,
            'message': f"Service {service_name} is unhealthy",
            'consecutive_failures': service_data['consecutive_failures'],
            'last_healthy': service_data['last_healthy'],
            'current_status': health_status,
            'timestamp': get_current_timestamp().isoformat()
        }
        
        logger.error(f"ALERT: {alert}")
        return alert
    
    def get_system_metrics(self, hours=24):
        """Получение метрик системы за указанный период"""
        cutoff_time = get_current_timestamp() - timedelta(hours=hours)
        
        recent_metrics = [
            metric for metric in self.metrics_history
            if datetime.fromisoformat(metric['timestamp'].replace('Z', '+00:00')) > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
        
        # Расчет доступности
        total_checks = len(recent_metrics)
        healthy_checks = sum(1 for m in recent_metrics if m['overall_status'] == 'healthy')
        availability = (healthy_checks / total_checks) * 100
        
        # Среднее время ответа
        avg_response_times = {}
        for service in self.config['services']:
            service_name = service['name']
            response_times = []
            
            for metric in recent_metrics:
                service_status = metric['services'].get(service_name, {})
                if service_status.get('status') == 'healthy':
                    response_times.append(service_status.get('response_time', 0))
            
            if response_times:
                avg_response_times[service_name] = sum(response_times) / len(response_times)
        
        return {
            'availability_percent': round(availability, 2),
            'total_checks': total_checks,
            'healthy_checks': healthy_checks,
            'time_period_hours': hours,
            'average_response_times': avg_response_times,
            'current_status': recent_metrics[-1] if recent_metrics else None
        }
    
    def run_continuous_monitoring(self):
        """Запуск непрерывного мониторинга"""
        logger.info("Starting continuous health monitoring...")
        
        try:
            while True:
                system_status = self.check_system_health()
                
                # Проверка алертов
                for service_config in self.config['services']:
                    service_name = service_config['name']
                    health_status = system_status['services'][service_name]
                    
                    if health_status['status'] != 'healthy' and self.should_alert(service_name):
                        alert = self.generate_alert(service_name, health_status)
                        # Здесь можно добавить отправку алерта (email, slack, etc.)
                
                # Логирование статуса
                if system_status['overall_status'] == 'healthy':
                    logger.info(f"System healthy - {len(self.config['services'])} services OK")
                else:
                    logger.warning(f"System degraded - check individual services")
                
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            logger.info("Health monitoring stopped by user")
        except Exception as e:
            logger.error(f"Health monitoring crashed: {e}")
            sys.exit(1)

def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Emotional AI Health Monitor')
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--metrics', action='store_true', help='Show metrics and exit')
    parser.add_argument('--hours', type=int, default=24, help='Hours for metrics summary')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor(args.config)
    
    if args.metrics:
        metrics = monitor.get_system_metrics(args.hours)
        print(json.dumps(metrics, indent=2))
        return
    
    if args.once:
        status = monitor.check_system_health()
        print(json.dumps(status, indent=2))
        
        # Exit with error code if system is unhealthy
        sys.exit(0 if status['overall_status'] == 'healthy' else 1)
    else:
        monitor.run_continuous_monitoring()

if __name__ == "__main__":
    main()