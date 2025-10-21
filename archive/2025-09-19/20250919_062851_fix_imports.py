#!/usr/bin/env python3
"""
🔧 FIX IMPORTS - Corretor automático de imports quebrados
Solução minimalista para harmonizar o sistema
"""

import sys
from pathlib import Path
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


# Mapeamento de correções
REPLACEMENTS = {
    # Imports antigos para novos
    'from apps.scripturemon.screenplay_crystal_memory': 'from src.core.omnimemory_v5_minimal',
    'from apps.scripturemon.ollama_core import OllamaCore': 'from src.core.ollama_core_minimal import OllamaMinimal',
    'from apps.scripturemon.digilang_simple': '# DigiLang not needed for Script Doctor',
    'from apps.scripturemon': 'from src.core',

    # Classes renomeadas
    'ScreenplayCrystalMemory': 'OmniMemoryV5',
    'OllamaCore': 'OllamaMinimal',
    'DigiLangEncoder': '# DigiLangEncoder removed',

    # PyPDF2 removido
    'import PyPDF2': '# PyPDF2 removed - use .txt files',
    'from PyPDF2': '# PyPDF2 removed - use .txt files',
    'import pdfplumber': '# pdfplumber removed - use .txt files',
    'PyPDF2.PdfReader': '# PDF reading removed',
    'pdfplumber.open': '# PDF reading removed',

    # Outros ajustes
    'from cinema_biblioteca_analyzer': '# from src.advanced.cinema_biblioteca_analyzer',
    'from cinema_rag_llm_system': 'from src.advanced.cinema_rag_llm_system',
}

def fix_imports_in_file(filepath: Path) -> int:
    """Corrige imports em um arquivo"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        original = content
        changes = 0

        for old, new in REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
                changes += content.count(new) - original.count(new)

        if content != original:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✅ Fixed {filepath.name}: {changes} corrections")
            return changes
        else:
            print(f"⏭️  {filepath.name}: No changes needed")
            return 0

    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return 0

def main():
    """Corrige imports em todos os arquivos Python"""
    print("🔧 IMPORT FIXER - Harmonização Automática")
    print("=" * 50)

    # Diretórios para verificar
    dirs_to_fix = [
        Path('src/core'),
        Path('src/advanced'),
    ]

    total_changes = 0
    total_files = 0

    for dir_path in dirs_to_fix:
        if not dir_path.exists():
            print(f"⚠️  Directory not found: {dir_path}")
            continue

        print(f"\n📁 Fixing {dir_path}:")

        for py_file in dir_path.glob('*.py'):
            if py_file.name == '__init__.py':
                continue

            changes = fix_imports_in_file(py_file)
            total_changes += changes
            total_files += 1

    print("\n" + "=" * 50)
    print(f"📊 SUMMARY:")
    print(f"  Files processed: {total_files}")
    print(f"  Total corrections: {total_changes}")

    if total_changes > 0:
        print(f"\n✅ SUCCESS: System harmony improved!")
    else:
        print(f"\n✨ System already harmonized!")

if __name__ == "__main__":
    main()

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
