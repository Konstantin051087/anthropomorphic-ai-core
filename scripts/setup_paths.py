#!/usr/bin/env python3
"""
Path setup script for all project scripts
"""

import sys
from pathlib import Path

def setup_project_path():
    """Add project root to Python path"""
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root

if __name__ == "__main__":
    root = setup_project_path()
    print(f"Project root added to path: {root}")