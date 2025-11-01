#!/usr/bin/env python3
"""
Architecture validation script with proper path handling
"""

import sys
import json
import importlib
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def validate_configs():
    """Validate all configuration files"""
    config_path = project_root / "data" / "configs"
    
    # Create config directory if it doesn't exist
    config_path.mkdir(parents=True, exist_ok=True)
    
    required_configs = [
        "system_config.json",
        "psyche_config.json", 
        "memory_config.json"
    ]
    
    all_configs_exist = True
    for config_file in required_configs:
        config_file_path = config_path / config_file
        if not config_file_path.exists():
            print(f"❌ Missing config: {config_file}")
            all_configs_exist = False
        else:
            # Validate JSON syntax
            try:
                with open(config_file_path, 'r') as f:
                    json.load(f)
                print(f"✅ Config valid: {config_file}")
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in {config_file}: {e}")
                all_configs_exist = False
    
    if all_configs_exist:
        print("✅ All configuration files present and valid")
    return all_configs_exist

def validate_database_models():
    """Validate database models"""
    try:
        from database.models import Base, SystemState, Memory, Interaction
        
        print("✅ Database models imported successfully")
        
        # Check that essential tables are defined - FIXED: use 'in' for dictionary
        essential_tables = ['system_state', 'memories', 'interactions']
        
        # Get table names from metadata
        table_names = [table.name for table in Base.metadata.tables.values()]
        print(f"📊 Found tables in metadata: {table_names}")
        
        for table in essential_tables:
            if table in table_names:
                print(f"✅ Table exists: {table}")
            else:
                print(f"❌ Table missing: {table}")
                return False
                
        # Additional check: verify we can instantiate model classes
        try:
            # Test that we can create instances (without saving to DB)
            system_state = SystemState()
            memory = Memory(content="test memory")
            interaction = Interaction(user_input="test", ai_response="test response")
            print("✅ Database model instances can be created")
        except Exception as e:
            print(f"❌ Cannot create model instances: {e}")
            return False
                
        return True
    except Exception as e:
        print(f"❌ Database models error: {e}")
        return False

def validate_api_spec():
    """Validate API specification"""
    try:
        from api.models import ChatRequest, ChatResponse, SystemStateResponse
        from api.routes import router
        
        # Check that essential endpoints are defined
        essential_endpoints = ['/chat', '/state', '/health']
        routes = [route.path for route in router.routes]
        
        for endpoint in essential_endpoints:
            if any(endpoint in route for route in routes):
                print(f"✅ Endpoint exists: {endpoint}")
            else:
                print(f"❌ Endpoint missing: {endpoint}")
                return False
                
        print("✅ API specification validated") 
        return True
    except Exception as e:
        print(f"❌ API specification error: {e}")
        return False

def validate_core_modules():
    """Validate core module imports"""
    try:
        from core.config import settings
        from core.orchestrator import Orchestrator
        from core.main import main
        
        print("✅ Core modules imported successfully")
        
        # Test settings
        assert hasattr(settings, 'database')
        assert hasattr(settings, 'api')
        print("✅ Settings configuration validated")
        
        # Test orchestrator
        orchestrator = Orchestrator()
        assert hasattr(orchestrator, 'initialize_modules')
        assert hasattr(orchestrator, 'process_input')
        print("✅ Orchestrator validated")
        
        return True
    except Exception as e:
        print(f"❌ Core modules error: {e}")
        return False

def validate_database_schema():
    """Validate database schema definitions"""
    try:
        from database.models import (
            SystemState, Memory, Interaction, MoodHistory, 
            PersonalityTrait, CharacterHabit, LearningExperience, SystemLog
        )
        
        # Check that all model classes are properly defined
        models = [
            ("SystemState", SystemState),
            ("Memory", Memory),
            ("Interaction", Interaction),
            ("MoodHistory", MoodHistory),
            ("PersonalityTrait", PersonalityTrait),
            ("CharacterHabit", CharacterHabit),
            ("LearningExperience", LearningExperience),
            ("SystemLog", SystemLog)
        ]
        
        for model_name, model_class in models:
            # Check that model has required attributes
            if hasattr(model_class, '__tablename__') and hasattr(model_class, '__table__'):
                print(f"✅ Model properly defined: {model_name} (table: {model_class.__tablename__})")
            else:
                print(f"❌ Model not properly defined: {model_name}")
                return False
        
        print("✅ All database models have proper schema definitions")
        return True
        
    except Exception as e:
        print(f"❌ Database schema validation error: {e}")
        return False

def create_missing_configs():
    """Create any missing configuration files"""
    config_path = project_root / "data" / "configs"
    config_path.mkdir(parents=True, exist_ok=True)
    
    configs = {
        "system_config.json": {
            "system": {
                "name": "Anthropomorphic AI Core",
                "version": "1.0.0",
                "description": "Distributed anthropomorphic AI system",
                "modules": {
                    "core": {"enabled": True, "priority": "high"},
                    "psyche": {"enabled": True, "priority": "high"},
                    "senses": {"enabled": True, "priority": "high"},
                    "mood": {"enabled": True, "priority": "medium"},
                    "memory": {"enabled": True, "priority": "high"},
                    "personality": {"enabled": True, "priority": "medium"},
                    "character": {"enabled": True, "priority": "medium"},
                    "reactions": {"enabled": True, "priority": "high"},
                    "communication": {"enabled": True, "priority": "high"},
                    "learning": {"enabled": True, "priority": "low"}
                }
            }
        },
        "psyche_config.json": {
            "psyche": {
                "consciousness": {
                    "self_awareness_level": 0.7,
                    "reflection_interval_seconds": 300
                }
            }
        },
        "memory_config.json": {
            "memory": {
                "short_term": {
                    "capacity": 20,
                    "decay_rate": 0.1
                }
            }
        }
    }
    
    created = []
    for config_file, content in configs.items():
        config_file_path = config_path / config_file
        if not config_file_path.exists():
            with open(config_file_path, 'w') as f:
                json.dump(content, f, indent=2)
            created.append(config_file)
    
    if created:
        print(f"📝 Created missing config files: {', '.join(created)}")
    
    return created

if __name__ == "__main__":
    print("🔧 Validating architecture...")
    print(f"Project root: {project_root}")
    
    # Create any missing config files first
    created_configs = create_missing_configs()
    
    checks = [
        validate_configs(),
        validate_database_models(), 
        validate_database_schema(),
        validate_api_spec(),
        validate_core_modules()
    ]
    
    if all(checks):
        print("\n🎉 Architecture validation PASSED")
        print("✅ All components are properly structured")
        print("📊 Architecture Summary:")
        print("   - Configuration files: ✅ Valid")
        print("   - Database models: ✅ Properly defined")
        print("   - API specification: ✅ Complete")
        print("   - Core modules: ✅ Functional")
    else:
        print("\n💥 Architecture validation FAILED")
        print("Please fix the reported issues")
        sys.exit(1)