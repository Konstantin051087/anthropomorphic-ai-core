#!/usr/bin/env python3
"""
Debug database metadata and table definitions
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.models import Base, get_table_names

def debug_metadata():
    """Debug database metadata"""
    print("🔍 Debugging Database Metadata")
    print("=" * 50)
    
    # Get all table names
    table_names = get_table_names()
    print(f"📊 Total tables in metadata: {len(table_names)}")
    print(f"📋 Table names: {table_names}")
    
    print("\n📖 Table details:")
    for table_name, table in Base.metadata.tables.items():
        print(f"\n🏷️  Table: {table_name}")
        print(f"   Columns: {[col.name for col in table.columns]}")
        print(f"   Primary keys: {[pk.name for pk in table.primary_key]}")
        print(f"   Foreign keys: {[fk.parent.name for fk in table.foreign_keys]}")
    
    print("\n🔍 Checking specific tables:")
    essential_tables = ['system_state', 'memories', 'interactions']
    for table in essential_tables:
        if table in table_names:
            print(f"   ✅ {table}: EXISTS")
            # Show columns for this table
            table_obj = Base.metadata.tables[table]
            columns = [col.name for col in table_obj.columns]
            print(f"      Columns: {columns}")
        else:
            print(f"   ❌ {table}: MISSING")

if __name__ == "__main__":
    debug_metadata()