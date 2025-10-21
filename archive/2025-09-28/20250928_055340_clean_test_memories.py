#!/usr/bin/env python3
"""
LIMPEZA DE MEMÓRIAS DE TESTE
Remove dados de teste e duplicados do banco de memórias
"""

import sqlite3
import json
import shutil
from datetime import datetime
from pathlib import Path

def clean_memories():
    """Limpa memórias de teste e duplicados"""

    # Fazer backup primeiro
    db_path = Path('data/unified_memory.db')
    backup_path = Path(f'data/unified_memory_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')

    print(f"📦 Criando backup em {backup_path}")
    shutil.copy2(db_path, backup_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Contar registros antes
    cursor.execute("SELECT COUNT(*) FROM unified_memory")
    total_before = cursor.fetchone()[0]
    print(f"\n📊 Total de registros ANTES: {total_before:,}")

    print("\n🧹 INICIANDO LIMPEZA...")

    # 1. Remover registros de teste óbvios
    print("\n1️⃣ Removendo registros de teste...")
    cursor.execute("""
        DELETE FROM unified_memory
        WHERE type = 'test'
        OR key LIKE '%test%'
        OR key LIKE '%Test%'
        OR key LIKE '%TEST%'
        OR source LIKE '%test%'
        OR (value LIKE '%large_test%' AND type = 'character')
        OR (value LIKE '%test_screenplay%' AND type = 'character')
    """)
    test_removed = cursor.rowcount
    print(f"   ✅ Removidos: {test_removed:,} registros de teste")

    # 2. Remover duplicados de character appearances (mantém apenas 1 de cada)
    print("\n2️⃣ Removendo duplicados de character appearances...")
    cursor.execute("""
        DELETE FROM unified_memory
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM unified_memory
            WHERE key LIKE 'character_analytics.db:appearances:%'
            GROUP BY value
        )
        AND key LIKE 'character_analytics.db:appearances:%'
    """)
    dup_removed = cursor.rowcount
    print(f"   ✅ Removidos: {dup_removed:,} duplicados")

    # 3. Remover registros com valores NULL ou vazios
    print("\n3️⃣ Removendo registros vazios...")
    cursor.execute("""
        DELETE FROM unified_memory
        WHERE value IS NULL
        OR value = ''
        OR value = '{}'
        OR value = '[]'
    """)
    empty_removed = cursor.rowcount
    print(f"   ✅ Removidos: {empty_removed:,} registros vazios")

    # 4. Remover registros muito antigos de cache/temporários
    print("\n4️⃣ Removendo cache antigo...")
    cursor.execute("""
        DELETE FROM unified_memory
        WHERE type = 'cache'
        AND timestamp < datetime('now', '-7 days')
    """)
    cache_removed = cursor.rowcount
    print(f"   ✅ Removidos: {cache_removed:,} registros de cache antigo")

    # 5. Remover registros de migração temporária
    print("\n5️⃣ Removendo registros temporários de migração...")
    cursor.execute("""
        DELETE FROM unified_memory
        WHERE source LIKE 'p1_%test'
        OR source = 'pattern_extractor'
        OR (source = 'legacy_migration' AND value LIKE '%batch_test%')
    """)
    migration_removed = cursor.rowcount
    print(f"   ✅ Removidos: {migration_removed:,} registros de migração temporária")

    # Contar registros depois
    cursor.execute("SELECT COUNT(*) FROM unified_memory")
    total_after = cursor.fetchone()[0]

    # Commit mudanças
    conn.commit()

    # Vacuum para recuperar espaço
    print("\n🗜️ Otimizando banco de dados...")
    cursor.execute("VACUUM")

    # Estatísticas finais
    print("\n" + "="*60)
    print("📊 RESULTADO DA LIMPEZA:")
    print(f"   Registros antes: {total_before:,}")
    print(f"   Registros removidos: {total_before - total_after:,}")
    print(f"   Registros depois: {total_after:,}")
    print(f"   Redução: {((total_before - total_after) / total_before * 100):.1f}%")

    # Análise do que sobrou
    print("\n📋 COMPOSIÇÃO FINAL:")
    cursor.execute("SELECT type, COUNT(*) as cnt FROM unified_memory GROUP BY type ORDER BY cnt DESC LIMIT 10")
    for typ, cnt in cursor.fetchall():
        print(f"   {typ}: {cnt:,}")

    # Verificar qualidade
    cursor.execute("SELECT COUNT(*) FROM unified_memory WHERE value LIKE '%screenplay%' OR value LIKE '%analysis%'")
    useful_count = cursor.fetchone()[0]
    print(f"\n✨ Registros úteis de análise: {useful_count:,} ({useful_count*100//total_after}%)")

    conn.close()

    print(f"\n💾 Backup salvo em: {backup_path}")
    print("✅ Limpeza concluída!")

    return {
        'before': total_before,
        'after': total_after,
        'removed': total_before - total_after,
        'backup': str(backup_path)
    }

if __name__ == "__main__":
    results = clean_memories()