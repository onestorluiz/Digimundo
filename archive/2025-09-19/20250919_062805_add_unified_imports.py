#!/usr/bin/env python3
"""
Adiciona import do unified memory em TODOS os arquivos que usam DB
"""
import re
from pathlib import Path

def add_unified_import(file_path):
    """Adiciona import se arquivo usa DB mas não tem unified"""
    content = file_path.read_text()

    # Se já tem unified, pular
    if 'unified_memory' in content:
        return False

    # Se usa DB, adicionar import
    if 'sqlite3' in content or '.db' in content:
        import_line = "from src.core.unified_memory_system import get_unified_memory, MemoryType\n"

        # Adicionar após outros imports
        lines = content.split('\n')
        import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_idx = i + 1

        lines.insert(import_idx, import_line)
        file_path.write_text('\n'.join(lines))
        return True

    return False

# Aplicar em todos os arquivos
count = 0
for py_file in Path("src").rglob("*.py"):
    if add_unified_import(py_file):
        count += 1
        print(f"✅ {py_file}")

print(f"\nTotal: {count} arquivos atualizados")
