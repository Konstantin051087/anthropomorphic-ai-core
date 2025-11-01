"""
Compatibility check script for different Python versions
"""

import sys
import pkg_resources

def check_compatibility():
    """Check package compatibility"""
    
    print(f"Python version: {sys.version}")
    
    try:
        with open('requirements.txt', 'r') as f:
            packages = [line.strip() for line in f if line.strip()]
        
        print("Required packages:")
        for package in packages:
            try:
                dist = pkg_resources.get_distribution(package.split('==')[0])
                print(f"  ✅ {dist.project_name} {dist.version}")
            except pkg_resources.DistributionNotFound:
                print(f"  ❌ {package} - Not installed")
                
    except Exception as e:
        print(f"Error checking compatibility: {e}")

if __name__ == "__main__":
    check_compatibility()