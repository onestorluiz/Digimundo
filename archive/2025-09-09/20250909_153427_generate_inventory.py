#!/usr/bin/env python3
import os
import json
from pathlib import Path
from datetime import datetime

def generate_inventory():
    project_root = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
    
    # Count files
    py_files = list(project_root.rglob("*.py"))
    db_files = list(project_root.rglob("*.db"))
    bin_files = list((project_root / "bin").glob("*")) if (project_root / "bin").exists() else []
    
    # Filter out backup directories
    py_files = [f for f in py_files if "backup" not in str(f).lower()]
    db_files = [f for f in db_files if "backup" not in str(f).lower()]
    
    inventory = {
        "timestamp": datetime.now().isoformat(),
        "project_root": str(project_root),
        "statistics": {
            "python_files": len(py_files),
            "database_files": len(db_files),
            "bin_executables": len(bin_files)
        },
        "bin_files": [f.name for f in bin_files],
        "key_modules": {
            "apps": len(list((project_root / "apps").rglob("*.py"))) if (project_root / "apps").exists() else 0,
            "src": len(list((project_root / "src").rglob("*.py"))) if (project_root / "src").exists() else 0,
            "tests": len(list((project_root / "tests").rglob("*.py"))) if (project_root / "tests").exists() else 0
        },
        "databases": [str(f.relative_to(project_root)) for f in db_files[:10]]  # First 10
    }
    
    # Save JSON
    with open("reports/harmony_vFinal/system_audit/phase0_inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Generate markdown
    md_content = f"""# System Inventory Report
Generated: {inventory['timestamp']}

## Statistics
- Python files: {inventory['statistics']['python_files']}
- Database files: {inventory['statistics']['database_files']}
- Bin executables: {inventory['statistics']['bin_executables']}

## Key Modules
- apps/: {inventory['key_modules']['apps']} files
- src/: {inventory['key_modules']['src']} files
- tests/: {inventory['key_modules']['tests']} files

## Bin Directory Contents
{chr(10).join('- ' + f for f in inventory['bin_files'])}

## Database Files Found
{chr(10).join('- ' + f for f in inventory['databases']) if inventory['databases'] else 'No database files found'}
"""
    
    with open("reports/harmony_vFinal/system_audit/phase0_inventory.md", "w") as f:
        f.write(md_content)
    
    print(f"✅ Inventory generated: {len(py_files)} Python files, {len(bin_files)} bin files")

if __name__ == "__main__":
    generate_inventory()
