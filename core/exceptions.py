class AnthropomorphicAIError(Exception):
    """Базовое исключение для системы Anthropomorphic AI"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class ModuleInitializationError(AnthropomorphicAIError):
    """Ошибка инициализации модуля"""
    
    def __init__(self, module_name: str, reason: str, details: dict = None):
        message = f"Ошибка инициализации модуля {module_name}: {reason}"
        error_code = f"MODULE_INIT_{module_name.upper()}"
        super().__init__(message, error_code, details)

class ModuleExecutionError(AnthropomorphicAIError):
    """Ошибка выполнения модуля"""
    
    def __init__(self, module_name: str, operation: str, reason: str, details: dict = None):
        message = f"Ошибка выполнения {operation} в модуле {module_name}: {reason}"
        error_code = f"MODULE_EXEC_{module_name.upper()}"
        super().__init__(message, error_code, details)

class ConfigurationError(AnthropomorphicAIError):
    """Ошибка конфигурации"""
    
    def __init__(self, config_key: str, reason: str, details: dict = None):
        message = f"Ошибка конфигурации {config_key}: {reason}"
        error_code = "CONFIG_ERROR"
        super().__init__(message, error_code, details)

class DatabaseError(AnthropomorphicAIError):
    """Ошибка базы данных"""
    
    def __init__(self, operation: str, reason: str, details: dict = None):
        message = f"Ошибка базы данных при {operation}: {reason}"
        error_code = "DATABASE_ERROR"
        super().__init__(message, error_code, details)

class APIConnectionError(AnthropomorphicAIError):
    """Ошибка подключения к API"""
    
    def __init__(self, service: str, reason: str, details: dict = None):
        message = f"Ошибка подключения к {service} API: {reason}"
        error_code = "API_CONNECTION_ERROR"
        super().__init__(message, error_code, details)

class AuthenticationError(AnthropomorphicAIError):
    """Ошибка аутентификации"""
    
    def __init__(self, service: str, reason: str, details: dict = None):
        message = f"Ошибка аутентификации в {service}: {reason}"
        error_code = "AUTH_ERROR"
        super().__init__(message, error_code, details)

class MemoryError(AnthropomorphicAIError):
    """Ошибка работы с памятью"""
    
    def __init__(self, operation: str, reason: str, details: dict = None):
        message = f"Ошибка памяти при {operation}: {reason}"
        error_code = "MEMORY_ERROR"
        super().__init__(message, error_code, details)

class TrainingError(AnthropomorphicAIError):
    """Ошибка обучения"""
    
    def __init__(self, phase: str, reason: str, details: dict = None):
        message = f"Ошибка обучения на этапе {phase}: {reason}"
        error_code = "TRAINING_ERROR"
        super().__init__(message, error_code, details)

class ValidationError(AnthropomorphicAIError):
    """Ошибка валидации данных"""
    
    def __init__(self, field: str, reason: str, details: dict = None):
        message = f"Ошибка валидации поля {field}: {reason}"
        error_code = "VALIDATION_ERROR"
        super().__init__(message, error_code, details)

class ResourceExhaustedError(AnthropomorphicAIError):
    """Ошибка исчерпания ресурсов"""
    
    def __init__(self, resource: str, reason: str, details: dict = None):
        message = f"Ресурс {resource} исчерпан: {reason}"
        error_code = "RESOURCE_EXHAUSTED"
        super().__init__(message, error_code, details)

class TimeoutError(AnthropomorphicAIError):
    """Ошибка таймаута"""
    
    def __init__(self, operation: str, timeout: float, details: dict = None):
        message = f"Таймаут операции {operation} после {timeout} секунд"
        error_code = "TIMEOUT_ERROR"
        super().__init__(message, error_code, details)