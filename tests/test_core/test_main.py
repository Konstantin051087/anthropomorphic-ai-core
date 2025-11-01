"""
Basic tests for main application
"""

def test_basic_import():
    """Test that core modules can be imported"""
    try:
        from core.config import settings
        from core.orchestrator import Orchestrator
        assert True
    except ImportError as e:
        assert False, f"Core modules failed to import: {e}"

def test_config_loading():
    """Test configuration loading"""
    from core.config import settings
    assert hasattr(settings.database, 'url')
    assert hasattr(settings.api, 'host')
    assert hasattr(settings.api, 'port')
    assert settings.api.port == 8000

def test_orchestrator_initialization():
    """Test orchestrator can be initialized"""
    from core.orchestrator import Orchestrator
    orchestrator = Orchestrator()
    assert orchestrator is not None
    assert hasattr(orchestrator, 'initialize_modules')
    assert hasattr(orchestrator, 'run')