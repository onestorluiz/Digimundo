#!/usr/bin/env python3
"""Gera inventário atual do projeto"""

import json
import os
from pathlib import Path
from datetime import datetime

def generate_inventory():
    """Gera inventário de arquivos .py e .db"""
    base_dir = Path(__file__).parent.parent.parent
    inventory = {
        'timestamp': datetime.now().isoformat(),
        'python_files': [],
        'db_files': []
    }
    
    # Coletar arquivos Python
    for py_file in base_dir.rglob('*.py'):
        rel_path = str(py_file.relative_to(base_dir))
        if 'backup' not in rel_path and '__pycache__' not in rel_path:
            inventory['python_files'].append({
                'path': rel_path,
                'size': py_file.stat().st_size
            })
    
    # Coletar arquivos DB
    for db_file in base_dir.rglob('*.db'):
        rel_path = str(db_file.relative_to(base_dir))
        if 'backup' not in rel_path:
            inventory['db_files'].append({
                'path': rel_path,
                'size': db_file.stat().st_size
            })
    
    # Salvar inventário
    output_path = base_dir / 'reports' / 'verify' / 'inventory_now.json'
    with open(output_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"✅ Inventário gerado: {output_path}")
    print(f"  - Python files: {len(inventory['python_files'])}")
    print(f"  - DB files: {len(inventory['db_files'])}")
    
    return inventory

if __name__ == "__main__":
    generate_inventory()