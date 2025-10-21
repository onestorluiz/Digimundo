#!/usr/bin/env python3
"""Teste do sistema de documentos"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.scripturemon.doc_resolver import build_index, find_by_name

# Testa indexação
print("🔍 Testando Document Resolver...")

# Diretórios padrão
dirs = [
    os.path.expanduser("~/Digimundo/roteiros"),
    os.path.expanduser("~/Digimundo/CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF"),
]

# Constrói índice
print(f"📁 Indexando {len(dirs)} diretórios...")
index = build_index(dirs)

print(f"✅ {len(index)} arquivos únicos indexados")

# Testa busca
tests = [
    "sonhos",
    "blade runner",
    "alien",
    "matrix"
]

for query in tests:
    results = find_by_name(query, dirs)
    if results:
        print(f"✅ '{query}': {len(results)} resultado(s)")
        for r in results[:2]:
            print(f"   • {os.path.basename(r)}")
    else:
        print(f"❌ '{query}': não encontrado")

print("\n📚 Sistema de documentos funcionando!")