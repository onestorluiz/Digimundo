#!/usr/bin/env python3
"""
Migração completa dos 3 bancos antigos para o sistema unificado
"""
import sqlite3
import json
import os
from datetime import datetime
from unified_memory import UnifiedMemory

def categorize_type(category: str) -> str:
    """Mapeia categoria antiga para novo tipo"""

    # Mapeamento de categorias antigas para novos tipos
    mapping = {
        # Rules
        'rule': 'rule',
        'critical_rule': 'rule',

        # Knowledge
        'knowledge': 'knowledge',
        'learning': 'knowledge',
        'conhecimento_critico': 'knowledge',
        'scripturemon': 'knowledge',
        'scripturemon_insights': 'knowledge',
        'prompt_techniques': 'knowledge',

        # Discovery
        'discovery': 'discovery',
        'critical_discovery': 'discovery',
        'revolutionary_discovery': 'discovery',
        'archive_discovery': 'discovery',
        'reflexao_vicios': 'discovery',

        # Decision
        'decision': 'decision',
        'architecture': 'decision',

        # Default to knowledge for unknowns
        'system_status': 'knowledge',
        'sync_logs': 'knowledge',
        'milestone': 'knowledge',
        'metric': 'knowledge',
        'comparison': 'knowledge',
        'general': 'knowledge',
        'reconnection': 'knowledge'
    }

    return mapping.get(category, 'knowledge')

def migrate_claude_memory_db():
    """Migra claude_memory.db"""

    print("\n📦 MIGRANDO claude_memory.db...")

    old_db = '/Users/clubproducoes/Digimundo/claude_code/memory/claude_memory.db'
    if not os.path.exists(old_db):
        print("  ❌ Banco não encontrado")
        return 0

    old_conn = sqlite3.connect(old_db)
    old_cursor = old_conn.cursor()

    mem = UnifiedMemory()
    migrated = 0

    # Migra tabela memories
    old_cursor.execute('SELECT category, key, value, timestamp FROM memories')
    for category, key, value, timestamp in old_cursor.fetchall():
        type_new = categorize_type(category)
        # Adiciona prefixo se key genérica
        if key in ['manual_entry', 'auto_captured']:
            key = f"{category}_{migrated}"

        if mem.remember(type_new, key, value, category, 0):
            migrated += 1

    # Migra tabela learned_rules
    old_cursor.execute('SELECT rule, context FROM learned_rules')
    for rule, context in old_cursor.fetchall():
        # Extrai número da regra se existir
        if 'REGRA #' in rule:
            key = f"RULE_{rule.split('REGRA #')[1].split(':')[0].strip()}"
        else:
            key = f"RULE_LEARNED_{migrated}"

        if mem.remember('rule', key, rule, context, 1):
            migrated += 1

    # Migra tabela decisions
    old_cursor.execute('SELECT decision, reasoning, timestamp FROM decisions')
    for decision, reasoning, timestamp in old_cursor.fetchall():
        key = f"DECISION_{timestamp[:10].replace('-', '')}"
        value = f"{decision}\nRazão: {reasoning}"

        if mem.remember('decision', key, value, 'migrated', 1):
            migrated += 1

    old_conn.close()
    mem.close()

    print(f"  ✅ {migrated} registros migrados")
    return migrated

def migrate_claude_rag_db():
    """Migra claude_rag.db"""

    print("\n📦 MIGRANDO claude_rag.db...")

    old_db = '/Users/clubproducoes/Digimundo/claude_code/memory/claude_rag.db'
    if not os.path.exists(old_db):
        print("  ❌ Banco não encontrado")
        return 0

    old_conn = sqlite3.connect(old_db)
    old_cursor = old_conn.cursor()

    mem = UnifiedMemory()
    migrated = 0
    skipped = 0

    # Migra tabela memories (RAG)
    old_cursor.execute('SELECT memory_id, content, filepath, metadata, timestamp FROM memories')
    for memory_id, content, filepath, metadata, timestamp in old_cursor.fetchall():
        # Verifica se já existe
        existing = mem.recall(query=memory_id[:50], limit=1)
        if existing and any(memory_id in str(e) for e in existing):
            skipped += 1
            continue

        # RAG geralmente é knowledge
        new_key = f"RAG_{memory_id}" if not memory_id.startswith('RAG_') else memory_id
        context = f"rag_import|{filepath}" if filepath else 'rag_import'

        if mem.remember('knowledge', new_key, content, context, 0):
            migrated += 1

    old_conn.close()
    mem.close()

    print(f"  ✅ {migrated} registros migrados")
    if skipped:
        print(f"  ⏭️  {skipped} duplicados pulados")
    return migrated

def migrate_crystal_memory():
    """Migra crystal_memory.json"""

    print("\n📦 MIGRANDO crystal_memory.json...")

    json_file = '/Users/clubproducoes/Digimundo/claude_code/memory/crystal_memory.json'
    if not os.path.exists(json_file):
        print("  ❌ Arquivo não encontrado")
        return 0

    with open(json_file, 'r') as f:
        data = json.load(f)

    mem = UnifiedMemory()
    migrated = 0

    if 'memories' in data:
        for memory in data['memories']:
            timestamp = memory.get('timestamp', '')
            type_mem = memory.get('type', 'system_documentation')
            project = memory.get('project', '')
            details = json.dumps(memory.get('details', {}), indent=2)

            key = f"CRYSTAL_{type_mem}_{timestamp[:10]}"
            value = f"Project: {project}\n{details}"

            if mem.remember('discovery', key, value, 'crystal_memory', 1):
                migrated += 1

    mem.close()

    print(f"  ✅ {migrated} registros migrados")
    return migrated

def remove_duplicates():
    """Remove duplicatas baseado em valor similar"""

    print("\n🧹 REMOVENDO DUPLICATAS...")

    mem = UnifiedMemory()
    cursor = mem.conn.cursor()

    # Identifica duplicatas (mesmo value, mantém o mais recente)
    cursor.execute('''
        DELETE FROM memories
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM memories
            GROUP BY value
        )
    ''')

    removed = cursor.rowcount
    mem.conn.commit()
    mem.close()

    if removed:
        print(f"  ✅ {removed} duplicatas removidas")
    else:
        print(f"  ✅ Nenhuma duplicata encontrada")

    return removed

def verify_migration():
    """Verifica integridade da migração"""

    print("\n🔍 VERIFICANDO MIGRAÇÃO...")

    mem = UnifiedMemory()
    stats = mem.stats()

    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"  Total: {stats['total']} memórias")
    print(f"  Tamanho: {stats['db_size']}")

    print(f"\n📂 Por tipo:")
    for type_info in stats['by_type']:
        print(f"  {type_info['type']}: {type_info['count']} registros")

    print(f"\n⭐ Por prioridade:")
    for priority, count in stats['by_priority'].items():
        priority_name = ['Normal', 'Importante', 'Crítico'][priority]
        print(f"  {priority_name}: {count}")

    # Testa buscas
    print(f"\n🔍 TESTE DE BUSCAS:")

    test_queries = [
        ('REGRA', 'rule'),
        ('Genjutsu', None),
        ('scripturemon', None),
        ('decision', 'decision')
    ]

    for query, type_filter in test_queries:
        results = mem.recall(query, type_filter, 5)
        print(f"  '{query}' (type={type_filter}): {len(results)} resultados")

    mem.close()

def main():
    """Executa migração completa"""

    print("🚀 INICIANDO MIGRAÇÃO PARA SISTEMA UNIFICADO")
    print("=" * 50)

    # Conta registros originais
    total_original = 0
    try:
        conn = sqlite3.connect('/Users/clubproducoes/Digimundo/claude_code/memory/claude_memory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM memories')
        total_original += cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM learned_rules')
        total_original += cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM decisions')
        total_original += cursor.fetchone()[0]
        conn.close()

        conn = sqlite3.connect('/Users/clubproducoes/Digimundo/claude_code/memory/claude_rag.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM memories')
        total_original += cursor.fetchone()[0]
        conn.close()
    except:
        pass

    print(f"📊 Registros originais estimados: {total_original}")

    # Executa migrações
    total_migrated = 0
    total_migrated += migrate_claude_memory_db()
    total_migrated += migrate_claude_rag_db()
    total_migrated += migrate_crystal_memory()

    print(f"\n📊 Total migrado: {total_migrated} registros")

    # Remove duplicatas
    remove_duplicates()

    # Verifica resultado
    verify_migration()

    print("\n✅ MIGRAÇÃO COMPLETA!")
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("  1. Testar sistema novo")
    print("  2. Se tudo OK, arquivar bancos antigos")
    print("  3. Atualizar imports para usar UnifiedMemory")

if __name__ == '__main__':
    main()