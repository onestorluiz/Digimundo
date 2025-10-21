#!/usr/bin/env python3
"""
Reindexação da Biblioteca
Indexa os arquivos na nova estrutura organizada
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, 'src')
from scripturemon_champion.rag import index_document, search_documents

print("="*60)
print("REINDEXAÇÃO DA BIBLIOTECA")
print("="*60)

# Base do projeto
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"

# Diretórios organizados
SCREENPLAYS_DIR = DATA_DIR / "screenplays"
MY_SCREENPLAYS_DIR = DATA_DIR / "my_screenplays"
THEORY_DIR = DATA_DIR / "theory"

stats = {"screenplays": 0, "my_screenplays": 0, "theory": 0, "total": 0}

def index_file(file_path, category):
    """Indexa um arquivo no BM25"""
    try:
        # Lê conteúdo
        content = file_path.read_text(encoding='utf-8', errors='ignore')[:10000]

        # ID único
        doc_id = f"{category}/{file_path.stem}"

        # Metadados
        metadata = {
            "category": category,
            "filename": file_path.name,
            "path": str(file_path.relative_to(PROJECT_ROOT)),
            "size": file_path.stat().st_size
        }

        # Indexa
        index_document(doc_id, content, metadata)
        return True
    except Exception as e:
        print(f"  ❌ Erro em {file_path.name}: {e}")
        return False

print("\n📚 Indexando arquivos...")
print("-"*40)

# 1. Screenplays (roteiros profissionais)
if SCREENPLAYS_DIR.exists():
    print("\n→ Indexando roteiros profissionais...")
    for file_path in SCREENPLAYS_DIR.glob("*.txt"):
        if index_file(file_path, "screenplays"):
            stats["screenplays"] += 1
            stats["total"] += 1
            print(f"  ✅ {file_path.name[:50]}")

# 2. My Screenplays (meus roteiros)
if MY_SCREENPLAYS_DIR.exists():
    print("\n→ Indexando meus roteiros...")
    for file_path in MY_SCREENPLAYS_DIR.glob("*.txt"):
        if index_file(file_path, "my_screenplays"):
            stats["my_screenplays"] += 1
            stats["total"] += 1
            print(f"  ✅ {file_path.name[:50]}")

# 3. Theory (livros de teoria)
if THEORY_DIR.exists():
    print("\n→ Indexando livros de teoria...")
    for file_path in THEORY_DIR.glob("*.txt"):
        if index_file(file_path, "theory"):
            stats["theory"] += 1
            stats["total"] += 1
            print(f"  ✅ {file_path.name[:50]}")

print("\n" + "="*60)
print("📊 ESTATÍSTICAS DA INDEXAÇÃO")
print("="*60)
print(f"screenplays/: {stats['screenplays']} documentos")
print(f"my_screenplays/: {stats['my_screenplays']} documentos")
print(f"theory/: {stats['theory']} documentos")
print("-"*40)
print(f"TOTAL: {stats['total']} documentos indexados")
print("="*60)

# Testar busca
print("\n🔍 Testando busca BM25...")
test_queries = [
    ("save the cat", "theory"),
    ("inception dream", "screenplays"),
    ("sonhos lembrancas", "my_screenplays"),
    ("three acts structure", "theory"),
    ("matrix neo", "screenplays")
]

for query, expected_category in test_queries:
    results = search_documents(query, top_k=2)
    if results:
        found = expected_category in results[0]['doc_id']
        symbol = "✅" if found else "⚠️"
        print(f"{symbol} '{query}':")
        for r in results[:2]:
            print(f"   - {r['doc_id'][:50]}: {r['score']:.2f}")
    else:
        print(f"❌ '{query}' - sem resultados")

print("\n✅ REINDEXAÇÃO COMPLETA!")
print("="*60)