#!/usr/bin/env python3
"""
Environment check script for CI/CD compatibility
"""

import sys
from pathlib import Path

# Setup paths first
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import importlib
import importlib.metadata

def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name, package=package_name)
        else:
            importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False

def main():
    """Main check function"""
    print("🔧 Checking environment compatibility...")
    print(f"Python version: {sys.version}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
    
    # Critical imports for the project
    critical_imports = [
        "fastapi",
        "uvicorn", 
        "sqlalchemy",
        "pydantic",
        "pydantic_settings",
        "pytest",
        "requests",
        "gradio"
    ]
    
    # Core module imports
    core_imports = [
        ("core.config", "settings"),
        ("core.orchestrator", "Orchestrator"),
        ("core.main", "main"),
        ("utils.logger", "setup_logging")
    ]
    
    print("\n📦 Checking critical packages...")
    all_passed = True
    
    for import_name in critical_imports:
        if not check_import(import_name):
            all_passed = False
    
    print("\n🔧 Checking core modules...")
    for module_path, attribute in core_imports:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, attribute):
                print(f"✅ {module_path}.{attribute} - OK")
            else:
                print(f"❌ {module_path}.{attribute} - MISSING")
                all_passed = False
        except ImportError as e:
            print(f"❌ {module_path} - FAILED: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 All environment checks passed! CI/CD ready.")
        sys.exit(0)
    else:
        print("\n💥 Some checks failed. Please fix before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()