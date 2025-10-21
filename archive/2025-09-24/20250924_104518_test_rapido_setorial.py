#!/usr/bin/env python3
"""
TESTE RÁPIDO SETORIAL - Sem Ollama
"""

print("\n🚀 TESTE RÁPIDO SETORIAL (Sem Ollama)")
print("="*50)

# 1. Parser
print("\n1️⃣ PARSER:")
try:
    from improved_json_parser import robust_json_parse
    r1, c1 = robust_json_parse('{"test": true}')
    r2, c2 = robust_json_parse('```json\n{"md": true}\n```')
    parser_ok = r1 and r2 and c1 > 0.8
    print(f"  {'✅' if parser_ok else '❌'} Parser: JSON={c1:.2f}, MD={c2:.2f}")
except Exception as e:
    print(f"  ❌ Erro: {e}")
    parser_ok = False

# 2. Memória
print("\n2️⃣ MEMÓRIA:")
try:
    from rag_integration import SimpleRAG
    rag = SimpleRAG()
    stats = rag.get_stats()
    mem_ok = stats['total_memories'] > 0
    print(f"  {'✅' if mem_ok else '❌'} RAG: {stats['total_memories']} memórias")
except Exception as e:
    print(f"  ❌ Erro: {e}")
    mem_ok = False

# 3. Knowledge Packs
print("\n3️⃣ KNOWLEDGE PACKS:")
from pathlib import Path
kp_dir = Path('knowledge_packs')
if kp_dir.exists():
    packs = list(kp_dir.glob('*.txt'))
    kp_ok = len(packs) > 0
    print(f"  {'✅' if kp_ok else '❌'} Packs: {len(packs)} arquivos")
else:
    print(f"  ❌ Diretório não existe")
    kp_ok = False

# 4. Safe Parser
print("\n4️⃣ SAFE PARSER:")
try:
    from safe_json_parser_ultimate import safe_json_parse
    sp_ok = True
    print(f"  ✅ Safe parser existe")
except ImportError:
    print(f"  ❌ Safe parser não existe")
    sp_ok = False

# 5. Integração (sem Ollama)
print("\n5️⃣ INTEGRAÇÃO:")
try:
    from ollama_with_memory import OllamaWithMemory
    int_ok = True
    print(f"  ✅ Módulo de integração OK")
except Exception as e:
    print(f"  ❌ Erro: {e}")
    int_ok = False

# Resultado
print("\n" + "="*50)
print("📊 RESULTADO:")

total = 5
passou = sum([parser_ok, mem_ok, kp_ok, sp_ok, int_ok])
taxa = passou / total * 100

print(f"\nSetores OK: {passou}/{total} ({taxa:.0f}%)")
print(f"• Parser: {'✅' if parser_ok else '❌'}")
print(f"• Memória: {'✅' if mem_ok else '❌'}")
print(f"• Knowledge: {'✅' if kp_ok else '❌'}")
print(f"• Safe Parser: {'✅' if sp_ok else '❌'}")
print(f"• Integração: {'✅' if int_ok else '❌'}")

if taxa >= 80:
    print("\n✅ APROVADO PARA CORREÇÕES")
else:
    print(f"\n❌ REPROVADO - Corrigir {5-passou} setores")

print("\n🥷 DIGIMUNDO PRESENTE")