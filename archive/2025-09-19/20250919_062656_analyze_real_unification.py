#!/usr/bin/env python3
"""
🔍 ANÁLISE REAL DO NÍVEL DE UNIFICAÇÃO
Verifica quantos sistemas realmente usam o unified memory
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_database_usage():
    """Analisa uso real de bancos de dados"""

    root = Path(".")
    stats = {
        'total_py_files': 0,
        'files_with_db': 0,
        'files_using_unified': 0,
        'independent_dbs': defaultdict(list),
        'unified_users': [],
        'direct_sqlite': [],
        'memory_systems': []
    }

    # Patterns
    db_patterns = [
        r'\.db[\'"\)]',
        r'sqlite3\.connect',
        r'CREATE TABLE',
        r'memory_store',
        r'memory_bank'
    ]

    unified_patterns = [
        r'unified_memory',
        r'get_unified_memory',
        r'UnifiedMemorySystem'
    ]

    # Analisar todos os arquivos Python
    for py_file in root.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue

        stats['total_py_files'] += 1

        try:
            content = py_file.read_text()

            # Verifica uso de DB
            uses_db = any(re.search(pattern, content) for pattern in db_patterns)
            if uses_db:
                stats['files_with_db'] += 1

                # Verifica se usa unified
                uses_unified = any(re.search(pattern, content) for pattern in unified_patterns)
                if uses_unified:
                    stats['files_using_unified'] += 1
                    stats['unified_users'].append(str(py_file))
                else:
                    # Identifica qual DB usa
                    db_matches = re.findall(r'["\']([^"\']*\.db)["\']', content)
                    for db in db_matches:
                        stats['independent_dbs'][db].append(str(py_file))

                    # Verifica se usa sqlite diretamente
                    if "sqlite3.connect" in content:
                        stats['direct_sqlite'].append(str(py_file))

            # Identifica sistemas de memória
            if "memory" in py_file.name.lower():
                stats['memory_systems'].append(str(py_file))

        except Exception as e:
            pass

    return stats

def main():
    print("🔍 ANÁLISE REAL DE UNIFICAÇÃO DE MEMÓRIA")
    print("=" * 60)

    stats = analyze_database_usage()

    # Calcular porcentagem real
    if stats['files_with_db'] > 0:
        unification_percent = (stats['files_using_unified'] / stats['files_with_db']) * 100
    else:
        unification_percent = 0

    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"  Total de arquivos Python: {stats['total_py_files']}")
    print(f"  Arquivos que usam DB: {stats['files_with_db']}")
    print(f"  Arquivos usando Unified: {stats['files_using_unified']}")
    print(f"  Arquivos com SQLite direto: {len(stats['direct_sqlite'])}")

    print(f"\n🎯 NÍVEL REAL DE UNIFICAÇÃO: {unification_percent:.1f}%")

    if unification_percent < 20:
        print("  ⚠️ BAIXO - Maioria dos sistemas ainda independentes")
    elif unification_percent < 50:
        print("  ⚡ MÉDIO - Progresso iniciado mas incompleto")
    elif unification_percent < 80:
        print("  🔥 BOM - Maioria integrada")
    else:
        print("  ✅ EXCELENTE - Sistema altamente unificado")

    print(f"\n📦 BANCOS DE DADOS INDEPENDENTES ({len(stats['independent_dbs'])})")
    for db, files in stats['independent_dbs'].items():
        print(f"\n  {db}: ({len(files)} arquivos)")
        for f in files[:3]:  # Mostrar apenas 3 primeiros
            print(f"    - {f}")
        if len(files) > 3:
            print(f"    ... e mais {len(files)-3} arquivos")

    print(f"\n✅ ARQUIVOS USANDO UNIFIED MEMORY ({len(stats['unified_users'])})")
    for f in stats['unified_users']:
        print(f"  - {f}")

    print(f"\n⚠️ ARQUIVOS COM SQLITE DIRETO ({len(stats['direct_sqlite'])})")
    for f in stats['direct_sqlite'][:5]:
        print(f"  - {f}")
    if len(stats['direct_sqlite']) > 5:
        print(f"  ... e mais {len(stats['direct_sqlite'])-5} arquivos")

    print(f"\n🧠 SISTEMAS DE MEMÓRIA ENCONTRADOS ({len(stats['memory_systems'])})")
    for f in stats['memory_systems']:
        print(f"  - {f}")

    # Recomendações
    print("\n💡 RECOMENDAÇÕES PARA 100% UNIFICAÇÃO:")

    if stats['independent_dbs']:
        print("\n1. MIGRAR BANCOS INDEPENDENTES:")
        for db in list(stats['independent_dbs'].keys())[:5]:
            print(f"   - {db}")

    if stats['direct_sqlite']:
        print(f"\n2. CONVERTER {len(stats['direct_sqlite'])} ARQUIVOS COM SQLITE DIRETO")
        print("   Substituir sqlite3.connect por get_unified_memory()")

    non_unified = stats['files_with_db'] - stats['files_using_unified']
    if non_unified > 0:
        print(f"\n3. INTEGRAR {non_unified} ARQUIVOS RESTANTES")
        print("   Adicionar imports e adapters do unified_memory_system")

    print("\n" + "=" * 60)
    print(f"📊 RESUMO: {unification_percent:.1f}% UNIFICADO")
    print(f"   Faltam {non_unified} arquivos para 100%")

    return unification_percent

if __name__ == "__main__":
    percent = main()
    exit(0 if percent > 50 else 1)