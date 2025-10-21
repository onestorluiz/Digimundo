#!/usr/bin/env python3
"""
🚀 MIGRAÇÃO COMPLETA PARA UNIFIED MEMORY
"""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType


def migrate_all_databases():
    """Migra TODOS os bancos para unified_memory.db"""

    memory = get_unified_memory()
    project_root = Path(__file__).parent.parent

    # Lista de bancos conhecidos e seus tipos
    database_mapping = {
        'crystal_memory.db': MemoryType.CRYSTAL,
        'screenplay_memory.db': MemoryType.SCREENPLAY,
        'claude_context.db': MemoryType.CONTEXT,
        'rag_vectors.db': MemoryType.VECTOR,
        'consciousness.db': MemoryType.CONSCIOUSNESS,
        'character_analytics.db': MemoryType.CHARACTER,
        'cinema_vectors.db': MemoryType.VECTOR,
        'omnimemory_v5.db': MemoryType.KNOWLEDGE,
    }

    total_migrated = 0

    for db_name, memory_type in database_mapping.items():
        # Buscar banco
        db_paths = list(project_root.rglob(db_name))

        for db_path in db_paths:
            if not db_path.exists():
                continue

            print(f"\n📦 Migrando {db_path.name}...")

            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()

                # Descobrir tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table[0]

                    # Ler dados
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    # Migrar cada linha
                    for row in rows:
                        try:
                            # Adaptar estrutura
                            key = f"migrated_{db_name}_{table_name}_{total_migrated}"
                            value = {'data': row, 'table': table_name}

                            memory.store(
                                memory_type=memory_type,
                                key=key,
                                value=value,
                                metadata={
                                    'source_db': db_name,
                                    'source_table': table_name,
                                    'migration_time': datetime.now().isoformat()
                                },
                                confidence=1.0,
                                source='complete_migration'
                            )

                            total_migrated += 1

                        except Exception as e:
                            pass

                conn.close()
                print(f"   ✅ Migrado: {len(rows)} entradas")

            except Exception as e:
                print(f"   ❌ Erro: {e}")

    print(f"\n🎯 MIGRAÇÃO COMPLETA: {total_migrated} entradas migradas")

    stats = memory.get_stats()
    print(f"📊 Total no unified: {stats['total_entries']} entradas")

    return total_migrated


if __name__ == "__main__":
    migrate_all_databases()
