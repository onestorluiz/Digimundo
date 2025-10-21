#!/usr/bin/env python3
"""
🧹 Limpa bancos de dados de teste (vazios ou <1KB)
Mantém apenas unified_memory.db e outros essenciais
"""

from pathlib import Path
import os

def cleanup_test_dbs():
    """Remove DBs de teste vazios ou muito pequenos"""

    # DBs que NUNCA devem ser deletados
    keep_dbs = {
        'unified_memory.db',
        'cinema_vectors.db',
        'crystal_memory.db'
    }

    removed = 0
    kept = 0
    total_freed = 0

    # Buscar todos os .db
    for db_file in Path('.').rglob('*.db'):
        # Ignorar pastas de backup
        if 'Pre_Limpeza' in str(db_file) or 'backup' in str(db_file.parent):
            continue

        # Verificar se deve manter
        if db_file.name in keep_dbs:
            kept += 1
            continue

        # Verificar tamanho
        size = db_file.stat().st_size

        # Remover se menor que 1KB (vazio ou teste)
        if size < 1024:
            try:
                total_freed += size
                db_file.unlink()
                removed += 1
                print(f"  ❌ Removido: {db_file} ({size} bytes)")
            except Exception as e:
                print(f"  ⚠️ Erro ao remover {db_file}: {e}")
        else:
            kept += 1

    print(f"\n📊 RESULTADO:")
    print(f"  ✅ Mantidos: {kept} DBs")
    print(f"  ❌ Removidos: {removed} DBs de teste")
    print(f"  💾 Espaço liberado: {total_freed / 1024:.1f} KB")

if __name__ == "__main__":
    print("🧹 LIMPEZA DE BANCOS DE TESTE")
    print("-" * 40)

    response = input("\nRemover DBs de teste vazios (<1KB)? (s/N): ")

    if response.lower() == 's':
        cleanup_test_dbs()
    else:
        print("Cancelado.")