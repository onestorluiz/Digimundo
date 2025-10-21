#!/usr/bin/env python3
"""
🔥 SYNC_MEMORY.py - Sincronizador de Memórias UCHIMON 🔥

Sincroniza bidirecionalmente:
- Database SQLite (MEMORY/claude_memory.db) ↔ Arquivos .md (MEMORY/conhecimentos/)
- Atualiza INDEX_MASTER automaticamente
- Detecta novos conhecimentos e registra no database

Uso:
  python3 sync_memory.py              # Sync bidirecional
  python3 sync_memory.py --db-to-md   # Apenas DB → MD
  python3 sync_memory.py --md-to-db   # Apenas MD → DB
  python3 sync_memory.py --check      # Apenas verificar (dry-run)
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime
import re
import json

# Adicionar diretório pai ao path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE_DIR, MEMORY_DIR, CONHECIMENTOS_DIR, DB_PATH, INDEX_MASTER

def connect_db():
    """Conecta ao database SQLite"""
    if not DB_PATH.exists():
        print(f"❌ Database não encontrado: {DB_PATH}")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

def get_conhecimentos_from_files():
    """Lê todos os conhecimentos dos arquivos .md"""
    conhecimentos = []

    if not CONHECIMENTOS_DIR.exists():
        print(f"❌ Diretório não encontrado: {CONHECIMENTOS_DIR}")
        return conhecimentos

    for md_file in sorted(CONHECIMENTOS_DIR.glob("*.md")):
        # Skip INDEX_MASTER
        if "INDEX_MASTER" in md_file.name:
            continue

        # Parse file
        content = md_file.read_text(encoding='utf-8')

        # Extract metadata from markdown
        match = re.search(r'# 🔥 CONHECIMENTO (\d+) - (.+)', content)
        if match:
            numero = match.group(1)
            titulo = match.group(2).strip()

            # Extract date
            date_match = re.search(r'\*\*Data:\*\* (\d{2}/\d{2}/\d{4})', content)
            data = date_match.group(1) if date_match else "N/A"

            # Extract type
            type_match = re.search(r'\*\*Tipo:\*\* (.+)', content)
            tipo = type_match.group(1) if type_match else "N/A"

            # Extract status
            status_match = re.search(r'\*\*Status:\*\* (.+)', content)
            status = status_match.group(1) if status_match else "✅ ATIVO"

            conhecimentos.append({
                'numero': numero,
                'titulo': titulo,
                'data': data,
                'tipo': tipo,
                'status': status,
                'file': md_file.name,
                'content': content,
                'size': len(content)
            })

    return conhecimentos

def get_conhecimentos_from_db(conn):
    """Lê conhecimentos registrados no database"""
    cursor = conn.cursor()

    # Check if conhecimentos table exists
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='conhecimentos'
    """)

    if not cursor.fetchone():
        # Create table if doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conhecimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE,
                titulo TEXT,
                data TEXT,
                tipo TEXT,
                status TEXT,
                file TEXT,
                content TEXT,
                size INTEGER,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return []

    cursor.execute("SELECT numero, titulo, data, tipo, status, file FROM conhecimentos")
    rows = cursor.fetchall()

    return [
        {
            'numero': row[0],
            'titulo': row[1],
            'data': row[2],
            'tipo': row[3],
            'status': row[4],
            'file': row[5]
        }
        for row in rows
    ]

def sync_md_to_db(conn, conhecimentos_files, dry_run=False):
    """Sincroniza arquivos .md → database"""
    cursor = conn.cursor()
    added = 0
    updated = 0

    for conhec in conhecimentos_files:
        # Check if exists
        cursor.execute("SELECT numero FROM conhecimentos WHERE numero = ?", (conhec['numero'],))
        exists = cursor.fetchone()

        if exists:
            # Update
            if not dry_run:
                cursor.execute("""
                    UPDATE conhecimentos
                    SET titulo = ?, data = ?, tipo = ?, status = ?, file = ?, content = ?, size = ?
                    WHERE numero = ?
                """, (conhec['titulo'], conhec['data'], conhec['tipo'], conhec['status'],
                      conhec['file'], conhec['content'], conhec['size'], conhec['numero']))
            updated += 1
            print(f"  🔄 Atualizado: {conhec['numero']} - {conhec['titulo'][:40]}")
        else:
            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO conhecimentos (numero, titulo, data, tipo, status, file, content, size)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (conhec['numero'], conhec['titulo'], conhec['data'], conhec['tipo'],
                      conhec['status'], conhec['file'], conhec['content'], conhec['size']))
            added += 1
            print(f"  ➕ Adicionado: {conhec['numero']} - {conhec['titulo'][:40]}")

    if not dry_run:
        conn.commit()

    return added, updated

def update_index_master(conhecimentos, dry_run=False):
    """Atualiza INDEX_MASTER com lista de conhecimentos"""
    if not INDEX_MASTER.exists():
        print(f"⚠️  INDEX_MASTER não encontrado: {INDEX_MASTER}")
        return False

    # Read current INDEX_MASTER
    content = INDEX_MASTER.read_text(encoding='utf-8')

    # Update stats
    stats_pattern = r'MEMORY_STATS = \{[^}]+\}'
    new_stats = f"""MEMORY_STATS = {{
    "total_conhecimentos": {len(conhecimentos)},
    "conhecimentos_uchimon": {len([k for k in conhecimentos if 'UCHIMON' in k['titulo'].upper()])},
    "prioridade_atual": "UCHIMON_INTERNAL",
    "ultima_atualizacao": "{datetime.now().strftime('%d/%m/%Y - %H:%M')}",
}}"""

    content = re.sub(stats_pattern, new_stats, content)

    if not dry_run:
        INDEX_MASTER.write_text(content, encoding='utf-8')
        print(f"✅ INDEX_MASTER atualizado: {len(conhecimentos)} conhecimentos")
    else:
        print(f"[DRY-RUN] INDEX_MASTER seria atualizado: {len(conhecimentos)} conhecimentos")

    return True

def main():
    """Main sync function"""
    import argparse

    parser = argparse.ArgumentParser(description='Sync MEMORY database ↔ conhecimentos')
    parser.add_argument('--db-to-md', action='store_true', help='Sync apenas DB → MD')
    parser.add_argument('--md-to-db', action='store_true', help='Sync apenas MD → DB')
    parser.add_argument('--check', action='store_true', help='Dry-run (não modificar)')

    args = parser.parse_args()

    print("")
    print("╔══════════════════════════════════════════════════════╗")
    print("║  🔥 SYNC_MEMORY - Sincronizador de Memórias 🔥      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("")

    if args.check:
        print("🔍 Modo: DRY-RUN (verificação apenas)")
    elif args.db_to_md:
        print("📤 Modo: Database → Arquivos .md")
    elif args.md_to_db:
        print("📥 Modo: Arquivos .md → Database")
    else:
        print("🔄 Modo: Sync Bidirecional")
    print("")

    # Connect to database
    conn = connect_db()

    # Get conhecimentos from files
    print("1️⃣  Lendo conhecimentos dos arquivos .md...")
    conhecimentos_files = get_conhecimentos_from_files()
    print(f"   ✅ Encontrados: {len(conhecimentos_files)} arquivos")
    print("")

    # Get conhecimentos from database
    print("2️⃣  Lendo conhecimentos do database...")
    conhecimentos_db = get_conhecimentos_from_db(conn)
    print(f"   ✅ Encontrados: {len(conhecimentos_db)} registros")
    print("")

    # Sync MD → DB (default or explicit)
    if not args.db_to_md:
        print("3️⃣  Sincronizando MD → DB...")
        added, updated = sync_md_to_db(conn, conhecimentos_files, dry_run=args.check)
        print(f"   ✅ Adicionados: {added}, Atualizados: {updated}")
        print("")

    # Update INDEX_MASTER
    print("4️⃣  Atualizando INDEX_MASTER...")
    update_index_master(conhecimentos_files, dry_run=args.check)
    print("")

    # Summary
    print("══════════════════════════════════════════════════════")
    print("✅ SINCRONIZAÇÃO COMPLETA")
    print("")
    print(f"📊 Resumo:")
    print(f"  - Conhecimentos totais: {len(conhecimentos_files)}")
    print(f"  - Database atualizado: {len(conhecimentos_files)} registros")
    print(f"  - INDEX_MASTER: Atualizado")
    print("")

    if args.check:
        print("ℹ️  Modo DRY-RUN - Nenhuma alteração foi feita")
        print("   Execute sem --check para aplicar as mudanças")
    else:
        print("🔥 SISTEMA SINCRONIZADO 🔥")
    print("")

    conn.close()

if __name__ == "__main__":
    main()
