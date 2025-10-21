#!/usr/bin/env python3
"""
🔥 CONFIG.py - Configuração Central do UCHIMON 🔥

Define paths automaticamente baseado na localização deste arquivo.
Todos os outros scripts devem importar daqui.

Uso:
    from config import BASE_DIR, MEMORY_DIR, DB_PATH
"""

from pathlib import Path

# Detecta BASE_DIR automaticamente (diretório onde este arquivo está)
BASE_DIR = Path(__file__).parent.resolve()

# Diretórios principais
MEMORY_DIR = BASE_DIR / "MEMORY"
CONHECIMENTOS_DIR = MEMORY_DIR / "conhecimentos"
SYSTEMS_DIR = BASE_DIR / "systems"
PROTECTION_DIR = BASE_DIR / "protection"
TESTS_DIR = BASE_DIR / "tests"
DOCS_DIR = BASE_DIR / "docs"
SCRIPTS_DIR = BASE_DIR / "scripts"
ANALYSIS_DIR = BASE_DIR / "analysis"
LEIS_DIR = BASE_DIR / "🔥LEIS_UCHIMON🔥"
LIVRO_DIR = BASE_DIR / "livro_claude"

# Arquivos críticos
DB_PATH = MEMORY_DIR / "claude_memory.db"
RAG_DB_PATH = MEMORY_DIR / "claude_rag.db"
INDEX_MASTER = CONHECIMENTOS_DIR / "🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md"
PROJECT_ID = BASE_DIR / "🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh"
REGRAS = BASE_DIR / "REGRAS.md"

# Projeto relacionado (scripturemon-clean)
DIGIMUNDO_DIR = BASE_DIR.parent
SCRIPTUREMON_DIR = DIGIMUNDO_DIR / "scripturemon-clean"

# Validar que estamos no diretório correto
if not PROJECT_ID.exists():
    raise RuntimeError(
        f"❌ config.py: PROJECT_ID não encontrado!\n"
        f"   Esperado: {PROJECT_ID}\n"
        f"   BASE_DIR detectado: {BASE_DIR}\n"
        f"   Este script deve estar em: /Users/clubproducoes/Digimundo/claude_code/"
    )

# Informações do projeto
PROJECT_NAME = "UCHIMON"
VERSION = "7.0"
LAST_UPDATE = "2025-10-01"

if __name__ == "__main__":
    print("🔥 UCHIMON CONFIG 🔥")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"MEMORY_DIR: {MEMORY_DIR}")
    print(f"DB_PATH: {DB_PATH}")
    print(f"SCRIPTUREMON_DIR: {SCRIPTUREMON_DIR}")
    print(f"\n✅ Configuração válida!")
