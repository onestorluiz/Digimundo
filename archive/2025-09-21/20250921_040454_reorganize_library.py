#!/usr/bin/env python3
"""
Reorganização da Estrutura de Diretórios
Separa corretamente: screenplays/, my_screenplays/, theory/
"""

import os
import shutil
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.insert(0, 'src')
from scripturemon_champion.rag import index_document, _INDEX as bm25_index

print("="*60)
print("REORGANIZAÇÃO DA BIBLIOTECA")
print("="*60)

# Base do projeto
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"

# Diretório atual (desorganizado)
OLD_DIR = DATA_DIR / "screenplays"

# Nova estrutura organizada
SCREENPLAYS_DIR = DATA_DIR / "screenplays"  # Roteiros mestres
MY_SCREENPLAYS_DIR = DATA_DIR / "my_screenplays"  # Meus roteiros
THEORY_DIR = DATA_DIR / "theory"  # Livros de teoria

print("\n📁 Estrutura Antiga:")
print(f"  {OLD_DIR}/")
print(f"    ├── roteiros_mestres/")
print(f"    ├── meus_filmes/")
print(f"    └── teoria/")

print("\n📁 Nova Estrutura:")
print(f"  {DATA_DIR}/")
print(f"    ├── screenplays/      # Roteiros profissionais")
print(f"    ├── my_screenplays/   # Meus roteiros")
print(f"    └── theory/           # Livros de teoria")

# Limpar índice BM25 atual
print("\n🧹 Limpando índice BM25...")
bm25_index.docs.clear()
bm25_index.tf.clear()
bm25_index.df.clear()
bm25_index.doc_len.clear()
bm25_index.N = 0
bm25_index.avgdl = 0.0

# Criar novos diretórios
SCREENPLAYS_DIR.mkdir(parents=True, exist_ok=True)
MY_SCREENPLAYS_DIR.mkdir(parents=True, exist_ok=True)
THEORY_DIR.mkdir(parents=True, exist_ok=True)

stats = {
    "screenplays": 0,
    "my_screenplays": 0,
    "theory": 0,
    "total": 0
}

def move_and_index(src_path, dest_path, category):
    """Move arquivo e reindexta no BM25"""
    try:
        # Move arquivo
        shutil.move(str(src_path), str(dest_path))

        # Lê conteúdo para indexação
        content = dest_path.read_text(encoding='utf-8', errors='ignore')[:10000]

        # ID único baseado na nova estrutura
        doc_id = f"{category}/{dest_path.stem}"

        # Metadados atualizados
        metadata = {
            "category": category,
            "filename": dest_path.name,
            "path": str(dest_path.relative_to(PROJECT_ROOT)),
            "size": dest_path.stat().st_size
        }

        # Indexa no BM25
        index_document(doc_id, content, metadata)

        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

print("\n📚 Reorganizando arquivos...")
print("-"*40)

# 1. Mover Roteiros Mestres → screenplays/
old_roteiros = OLD_DIR / "roteiros_mestres"
if old_roteiros.exists():
    print("\n→ Movendo roteiros profissionais...")
    for file_path in old_roteiros.glob("*.txt"):
        dest_path = SCREENPLAYS_DIR / file_path.name
        if move_and_index(file_path, dest_path, "screenplays"):
            stats["screenplays"] += 1
            stats["total"] += 1
            print(f"  ✅ {file_path.name[:40]}... → screenplays/")

    # Remove diretório vazio
    if not list(old_roteiros.iterdir()):
        old_roteiros.rmdir()

# 2. Mover Meus Filmes → my_screenplays/
old_meus = OLD_DIR / "meus_filmes"
if old_meus.exists():
    print("\n→ Movendo meus roteiros...")
    for file_path in old_meus.glob("*.txt"):
        dest_path = MY_SCREENPLAYS_DIR / file_path.name
        if move_and_index(file_path, dest_path, "my_screenplays"):
            stats["my_screenplays"] += 1
            stats["total"] += 1
            print(f"  ✅ {file_path.name[:40]}... → my_screenplays/")

    # Remove diretório vazio
    if not list(old_meus.iterdir()):
        old_meus.rmdir()

# 3. Mover Teoria → theory/
old_teoria = OLD_DIR / "teoria"
if old_teoria.exists():
    print("\n→ Movendo livros de teoria...")
    for file_path in old_teoria.glob("*.txt"):
        dest_path = THEORY_DIR / file_path.name
        if move_and_index(file_path, dest_path, "theory"):
            stats["theory"] += 1
            stats["total"] += 1
            print(f"  ✅ {file_path.name[:40]}... → theory/")

    # Remove diretório vazio
    if not list(old_teoria.iterdir()):
        old_teoria.rmdir()

# Remove diretório antigo se vazio
if OLD_DIR.exists() and not list(OLD_DIR.iterdir()):
    OLD_DIR.rmdir()
    print("\n✅ Diretório antigo removido")

print("\n" + "="*60)
print("📊 ESTATÍSTICAS DA REORGANIZAÇÃO")
print("="*60)
print(f"screenplays/: {stats['screenplays']} arquivos (roteiros profissionais)")
print(f"my_screenplays/: {stats['my_screenplays']} arquivos (meus roteiros)")
print(f"theory/: {stats['theory']} arquivos (livros de teoria)")
print("-"*40)
print(f"TOTAL: {stats['total']} arquivos reorganizados")
print(f"Documentos no BM25: {bm25_index.N}")
print("="*60)

# Testar busca
print("\n🔍 Testando busca no novo índice...")
from scripturemon_champion.rag import search_documents

test_queries = [
    ("save the cat", "theory"),
    ("inception", "screenplays"),
    ("sonhos", "my_screenplays")
]

for query, expected_category in test_queries:
    results = search_documents(query, top_k=1)
    if results and expected_category in results[0]['doc_id']:
        print(f"✅ '{query}' → {results[0]['doc_id']}")
    elif results:
        print(f"⚠️  '{query}' → {results[0]['doc_id']} (esperado: {expected_category})")
    else:
        print(f"❌ '{query}' - sem resultados")

print("\n✅ REORGANIZAÇÃO COMPLETA!")
print("\nNova estrutura:")
print(f"  📁 {SCREENPLAYS_DIR.relative_to(PROJECT_ROOT)}/")
print(f"  📁 {MY_SCREENPLAYS_DIR.relative_to(PROJECT_ROOT)}/")
print(f"  📁 {THEORY_DIR.relative_to(PROJECT_ROOT)}/")
print("="*60)