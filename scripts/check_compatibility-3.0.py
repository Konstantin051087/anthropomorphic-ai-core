#!/usr/bin/env python3
"""
Compatibility check script for different Python versions
"""

import sys
from pathlib import Path

# Setup paths first
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import importlib.metadata

def check_compatibility():
    """Check package compatibility using importlib.metadata"""
    
    print(f"Python version: {sys.version}")
    print(f"Project root: {project_root}")
    
    try:
        requirements_file = project_root / "requirements.txt"
        with open(requirements_file, 'r') as f:
            packages = [line.strip().split('==')[0].split('>=')[0] 
                       for line in f if line.strip() and not line.startswith('#')]
        
        print("Required packages:")
        for package in packages:
            try:
                dist = importlib.metadata.distribution(package)
                print(f"  ✅ {dist.metadata['Name']} {dist.version}")
            except importlib.metadata.PackageNotFoundError:
                print(f"  ❌ {package} - Not installed")
                
    except Exception as e:
        print(f"Error checking compatibility: {e}")

if __name__ == "__main__":
    check_compatibility()