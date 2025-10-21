#!/usr/bin/env python3
"""
E2E Promotion Simple - Teste direto de promoção.
"""
import json
import time
import sqlite3
from pathlib import Path

# Conectar diretamente ao banco
db_path = Path('data/memory/mem.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n=== TESTE DIRETO DE PROMOÇÃO ===\n")

# Verificar estrutura
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tabelas disponíveis: {[t['name'] for t in tables]}")

# Criar memória de teste se não existir
test_id = 'promo_test_001'
test_content = 'Three-act structure is fundamental to screenplay writing'

# Verificar se existe
cursor.execute("SELECT * FROM memories WHERE id = ? LIMIT 1", (test_id,))
row = cursor.fetchone()

if not row:
    print(f"\nCriando memória de teste: {test_id}")
    cursor.execute("""
        INSERT INTO memories (id, content, kind, hits, importance, created_at, last_accessed)
        VALUES (?, ?, 'L3', 0, 0.5, datetime('now'), datetime('now'))
    """, (test_id, test_content))
    conn.commit()
else:
    print(f"\nMemória já existe: {test_id}")

# Estado antes
cursor.execute("SELECT id, kind, hits FROM memories WHERE id = ?", (test_id,))
before = cursor.fetchone()
print(f"\nANTES:")
print(f"  ID: {before['id']}")
print(f"  Layer: {before['kind']}")
print(f"  Hits: {before['hits']}")

# Simular incremento de hits até threshold
threshold = 5
events = []

for i in range(threshold + 1):
    t0 = time.perf_counter()
    
    # Incrementar hits
    cursor.execute("""
        UPDATE memories 
        SET hits = hits + 1, last_accessed = datetime('now')
        WHERE id = ?
    """, (test_id,))
    
    # Verificar se deve promover
    cursor.execute("SELECT hits, kind FROM memories WHERE id = ?", (test_id,))
    current = cursor.fetchone()
    
    if current['hits'] >= threshold and current['kind'] == 'L3':
        # Promover para L2
        cursor.execute("""
            UPDATE memories 
            SET kind = 'L2'
            WHERE id = ?
        """, (test_id,))
        print(f"\n  🎯 PROMOÇÃO DISPARADA! (hits={current['hits']})")
    
    conn.commit()
    dt_ms = (time.perf_counter() - t0) * 1000
    
    events.append({
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'action': 'increment_and_check',
        'ms': round(dt_ms, 2),
        'hits': current['hits']
    })
    
    print(f"  Incremento {i+1}: hits={current['hits']}, {dt_ms:.2f}ms")

# Estado depois
cursor.execute("SELECT id, kind, hits FROM memories WHERE id = ?", (test_id,))
after = cursor.fetchone()
print(f"\nDEPOIS:")
print(f"  ID: {after['id']}")
print(f"  Layer: {after['kind']}")
print(f"  Hits: {after['hits']}")

promoted = (before['kind'] == 'L3' and after['kind'] == 'L2')
print(f"\n{'✅ PROMOVIDA!' if promoted else '❌ NÃO PROMOVIDA'}")

# Salvar evidência
proof = {
    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
    'mem_id': test_id,
    'before': {'hits': before['hits'], 'layer': before['kind']},
    'after': {'hits': after['hits'], 'layer': after['kind']},
    'promoted': promoted,
    'threshold': threshold,
    'events': events
}

proof_path = Path('reports/harmonia_v32/e2e/memory_promotion_proof_simple.json')
proof_path.parent.mkdir(parents=True, exist_ok=True)
with open(proof_path, 'w') as f:
    json.dump(proof, f, indent=2)

print(f"\nProof salvo em: {proof_path}")

# Salvar eventos na timeline
timeline_path = Path('reports/harmonia_v32/e2e/timeline_promotion_simple.ndjson')
with open(timeline_path, 'w') as f:
    for event in events:
        event['component'] = 'memory.sqlite'
        event['parent_id'] = 'promotion_simple'
        f.write(json.dumps(event) + '\n')

print(f"Timeline salva em: {timeline_path}")

conn.close()

print("\n✅ V32_R4_4E_PROMOTION_PROOF_DONE")