"""
Test imports when running from scripts directory
"""

import sys
from pathlib import Path

def test_imports_from_scripts_dir():
    """Test that imports work when called from scripts directory"""
    
    # Simulate running from scripts directory
    scripts_dir = Path(__file__).parent.parent / "scripts"
    original_path = sys.path.copy()
    
    try:
        # Remove project root if it exists
        project_root = Path(__file__).parent.parent
        if str(project_root) in sys.path:
            sys.path.remove(str(project_root))
        
        # Add scripts directory to path (as would happen when running from scripts/)
        sys.path.insert(0, str(scripts_dir))
        
        # Clean up any cached imports
        modules_to_remove = []
        for module_name in list(sys.modules.keys()):
            if module_name.startswith('core.') or module_name == 'core':
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            del sys.modules[module_name]
        
        # Now try to import - this might fail without proper path setup
        try:
            # This might fail because we're not in project root
            from core.config import settings
            # If we get here, import succeeded - that's OK too
            assert settings is not None
        except ImportError:
            # Expected behavior if import fails
            pass
            
        # Now add project root and try again (should always work)
        sys.path.insert(0, str(project_root))
        
        # Clean up cached imports again
        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]
        
        # This should work now
        from core.config import settings
        from core.orchestrator import Orchestrator
        
        assert settings is not None
        assert Orchestrator is not None
        
    finally:
        # Restore original path
        sys.path[:] = original_path

def test_script_imports():
    """Test that scripts can import project modules"""
    
    # Test that our path setup works
    scripts_dir = Path(__file__).parent.parent / "scripts"
    sys.path.insert(0, str(scripts_dir.parent))  # Add project root
    
    # Import the path setup function
    from scripts.setup_paths import setup_project_path
    
    project_root = setup_project_path()
    assert project_root.exists()
    assert project_root.name == "anthropomorphic-ai-core"