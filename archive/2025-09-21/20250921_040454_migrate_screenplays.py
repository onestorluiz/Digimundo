#!/usr/bin/env python3
"""
Migração Cuidadosa - Passo 1: Biblioteca de Roteiros
Transfere os 48 roteiros e 13 livros para o novo sistema BM25
"""

import os
import sys
import shutil
from pathlib import Path
import json

# Adiciona o novo sistema ao path
sys.path.insert(0, 'src')
from scripturemon_champion.rag import index_document
from scripturemon_champion.paths import PROJECT_ROOT, DATA_DIR

print("="*60)
print("MIGRAÇÃO PASSO 1: Biblioteca de Roteiros")
print("="*60)

# Caminhos
SOURCE_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")
TARGET_DIR = PROJECT_ROOT / "data" / "screenplays"

# Criar estrutura no novo sistema
TARGET_DIR.mkdir(parents=True, exist_ok=True)

print(f"\n📁 Origem: {SOURCE_DIR}")
print(f"📁 Destino: {TARGET_DIR}")

# Estatísticas
stats = {
    "roteiros_mestres": 0,
    "meus_filmes": 0,
    "teoria": 0,
    "total_files": 0,
    "total_size": 0,
    "indexed": 0
}

def copy_and_index_file(source_path, target_path, category):
    """Copia arquivo e indexa no BM25"""
    try:
        # Criar diretório se necessário
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Copiar arquivo
        shutil.copy2(source_path, target_path)

        # Ler conteúdo para indexação
        content = source_path.read_text(encoding='utf-8', errors='ignore')[:10000]  # Primeiros 10K chars

        # Criar ID único
        doc_id = f"{category}/{source_path.stem}"

        # Metadados
        metadata = {
            "category": category,
            "filename": source_path.name,
            "path": str(target_path.relative_to(PROJECT_ROOT)),
            "size": source_path.stat().st_size
        }

        # Indexar no BM25
        index_document(doc_id, content, metadata)

        stats["indexed"] += 1
        stats["total_size"] += source_path.stat().st_size

        return True

    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

print("\n📚 Migrando Roteiros...")
print("-"*40)

# 1. Roteiros Mestres
roteiros_dir = SOURCE_DIR / "roteiros_mestres"
if roteiros_dir.exists():
    target_subdir = TARGET_DIR / "roteiros_mestres"

    for file_path in roteiros_dir.glob("*.txt"):
        target_path = target_subdir / file_path.name
        if copy_and_index_file(file_path, target_path, "roteiros_mestres"):
            stats["roteiros_mestres"] += 1
            stats["total_files"] += 1
            print(f"  ✅ {file_path.name[:50]}")

# 2. Meus Filmes
meus_dir = SOURCE_DIR / "meus_filmes"
if meus_dir.exists():
    target_subdir = TARGET_DIR / "meus_filmes"

    for file_path in meus_dir.glob("*.txt"):
        target_path = target_subdir / file_path.name
        if copy_and_index_file(file_path, target_path, "meus_filmes"):
            stats["meus_filmes"] += 1
            stats["total_files"] += 1
            print(f"  ✅ {file_path.name[:50]}")

# 3. Teoria
teoria_dir = SOURCE_DIR / "teoria"
if teoria_dir.exists():
    target_subdir = TARGET_DIR / "teoria"

    for file_path in teoria_dir.glob("*.txt"):
        target_path = target_subdir / file_path.name
        if copy_and_index_file(file_path, target_path, "teoria"):
            stats["teoria"] += 1
            stats["total_files"] += 1
            print(f"  ✅ {file_path.name[:50]}")

# Salvar índice de migração
import datetime
index_file = TARGET_DIR / "migration_index.json"
with open(index_file, 'w', encoding='utf-8') as f:
    json.dump({
        "migration_date": datetime.datetime.now().isoformat(),
        "source": str(SOURCE_DIR),
        "target": str(TARGET_DIR),
        "stats": stats
    }, f, indent=2, ensure_ascii=False)

print("\n" + "="*60)
print("📊 ESTATÍSTICAS DA MIGRAÇÃO")
print("="*60)
print(f"Roteiros Mestres: {stats['roteiros_mestres']} arquivos")
print(f"Meus Filmes: {stats['meus_filmes']} arquivos")
print(f"Teoria: {stats['teoria']} arquivos")
print("-"*40)
print(f"TOTAL: {stats['total_files']} arquivos")
print(f"Tamanho: {stats['total_size'] / 1024 / 1024:.1f} MB")
print(f"Indexados no BM25: {stats['indexed']} documentos")
print("="*60)

# Verificar se o sistema pode buscar
print("\n🔍 Testando busca no BM25...")
from scripturemon_champion.rag import search_documents

test_queries = [
    "personagem protagonista",
    "save the cat",
    "três atos",
    "jornada do herói"
]

for query in test_queries:
    results = search_documents(query, top_k=3)
    if results:
        print(f"\n✅ '{query}' encontrou {len(results)} resultados:")
        for r in results[:2]:
            print(f"   - {r['doc_id']}: {r['score']:.2f}")
    else:
        print(f"❌ '{query}' - sem resultados")

print("\n✅ MIGRAÇÃO DA BIBLIOTECA COMPLETA!")
print("Roteiros disponíveis em:", TARGET_DIR)
print("="*60)