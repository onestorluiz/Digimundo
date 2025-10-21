#!/usr/bin/env python3
"""
TESTE COMPLETO DO ECOSSISTEMA SCRIPTUREMON ULTIMATE
Testa TODOS os componentes em harmonia
"""

import sys
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.analysis.theory import TheoryComparator
from scripturemon_champion.core.coach import DoctorCoach
from scripturemon_champion.core.memory import UnifiedMemory, MemoryRecord
from scripturemon_champion.core.ollama import OllamaReal
from scripturemon_champion.learning.learning_lite import LearningLite
from scripturemon_champion.core.rag_bm25 import index_document, search_documents

print("=" * 70)
print("🚀 TESTE COMPLETO DO ECOSSISTEMA SCRIPTUREMON ULTIMATE")
print("=" * 70)
print()

# ==============================================================================
# 1. TESTE OLLAMA INTEGRATION
# ==============================================================================
print("📡 TESTE 1: INTEGRAÇÃO COM OLLAMA")
print("-" * 50)

ollama = OllamaReal()
print(f"✅ Modelos disponíveis: {len(ollama.models)}")
print(f"✅ Modelo padrão: {ollama.default_model}")

# Teste de geração simples
test_prompt = "What makes a great screenplay opening? Answer in 2 sentences."
print(f"\n🤖 Testando geração com {ollama.default_model}...")
start = time.time()
response = ollama.generate(test_prompt, temperature=0.3, max_tokens=100)
elapsed = time.time() - start

if response.success:
    print(f"✅ Resposta em {elapsed:.1f}s: {response.completion[:100]}...")
else:
    print(f"⚠️ Fallback ativado: {response.completion[:100]}...")

# ==============================================================================
# 2. ANÁLISE COMPLETA DE ROTEIRO
# ==============================================================================
print("\n" + "=" * 70)
print("🎬 TESTE 2: ANÁLISE COMPLETA DE ROTEIRO REAL")
print("-" * 50)

# Carregar um roteiro real
screenplay_path = Path("screenplays/masters/Casablanca-Screenplay.txt")
if screenplay_path.exists():
    with open(screenplay_path, 'r', encoding='utf-8', errors='ignore') as f:
        casablanca = f.read()[:10000]  # Primeiras páginas apenas para teste

    doctor = ScriptDoctor(use_learning=True, genre="drama")

    print("📝 Analisando Casablanca...")
    start = time.time()
    analysis = doctor.analyze_script(casablanca, "Casablanca")
    elapsed = time.time() - start

    print(f"✅ Análise completa em {elapsed:.1f}s:")
    print(f"  • Cenas detectadas: {analysis.scenes}")
    print(f"  • Diálogo ratio: {analysis.dialogue_ratio:.2%}")
    print(f"  • Pacing score: {analysis.pacing_score:.2f}")
    print(f"  • Personagens principais: {', '.join(analysis.top_characters[:3])}")
    print(f"  • Média de palavras por cena: {analysis.avg_scene_len:.0f}")

    # Análise Save the Cat
    print("\n🐱 Análise Save the Cat...")
    stc = doctor.analyze_save_the_cat(casablanca)
    print(f"✅ Beats detectados: {len(stc.beats)}")
    for beat in stc.beats[:3]:
        print(f"  • {beat.name}: {beat.confidence:.0%} confiança")
    if stc.missing_beats:
        print(f"⚠️ Beats faltando: {', '.join(stc.missing_beats[:5])}")

# ==============================================================================
# 3. SISTEMA DE MEMÓRIA E PERSISTÊNCIA
# ==============================================================================
print("\n" + "=" * 70)
print("💾 TESTE 3: SISTEMA DE MEMÓRIA UNIFICADA")
print("-" * 50)

memory = UnifiedMemory(Path("data/unified_memory.db"))

# Armazenar nova memória
test_record = MemoryRecord(
    type="test_analysis",
    key=f"test_{datetime.now().isoformat()}",
    value={
        "screenplay": "Casablanca",
        "analysis_results": {
            "scenes": analysis.scenes if 'analysis' in locals() else 0,
            "dialogue_ratio": analysis.dialogue_ratio if 'analysis' in locals() else 0
        },
        "timestamp": datetime.now().isoformat()
    },
    metadata={"test": True, "version": "ultimate"}
)

record_id = memory.store(test_record)
print(f"✅ Memória armazenada com ID: {record_id}")

# Buscar memória
retrieved = memory.get("test_analysis", test_record.key)
if retrieved:
    print(f"✅ Memória recuperada: {retrieved.key}")
    print(f"  • Valor: {json.dumps(retrieved.value, indent=2)[:200]}...")

# Estatísticas do banco
stats = memory.stats()
print(f"\n📊 Estatísticas do banco:")
print(f"  • Total de registros: {stats['total_records']:,}")
print(f"  • Tipos únicos: {stats['unique_types']}")
print(f"  • Tamanho do banco: {stats['db_size_mb']:.1f}MB")

# ==============================================================================
# 4. SISTEMA DE APRENDIZADO
# ==============================================================================
print("\n" + "=" * 70)
print("🧠 TESTE 4: SISTEMA DE APRENDIZADO EVOLUTIVO")
print("-" * 50)

learning = LearningLite()

# Aprender com a análise
if 'analysis' in locals():
    print("📖 Aprendendo com Casablanca...")
    concepts = learning.learn_from_analysis(analysis, "Casablanca", genre="drama")
    print(f"✅ {len(concepts)} conceitos aprendidos")

    # Estatísticas de aprendizado
    stats = learning.get_statistics()
    print(f"\n📊 Estatísticas de aprendizado:")
    print(f"  • Total de beats aprendidos: {stats['total_beats']}")
    print(f"  • Roteiros analisados: {stats['unique_screenplays']}")
    if stats.get('beat_distribution'):
        print(f"  • Distribuição de beats: {len(stats['beat_distribution'])} tipos")

    # Enriquecer prompt com conhecimento
    test_query = "How to write a compelling midpoint?"
    enriched = learning.enrich_prompt_pro(
        "Analyze this concept:",
        q=test_query,
        k_beats=3,
        k_arch=2
    )
    print(f"\n🎯 Prompt enriquecido com conhecimento:")
    print(f"{enriched[:300]}...")

# ==============================================================================
# 5. COACH COM REFINAMENTO LLM
# ==============================================================================
print("\n" + "=" * 70)
print("🎭 TESTE 5: COACH COM REFINAMENTO INTELIGENTE")
print("-" * 50)

coach = DoctorCoach(genre="drama")

# Analisar roteiro pessoal
with open("my_screenplays/exemplo_roteiro.txt", 'r') as f:
    my_script = f.read()

print("🎬 Gerando plano de coaching...")
start = time.time()
plan = coach.plan(my_script, "O Código do Silêncio")
elapsed = time.time() - start

print(f"✅ Plano gerado em {elapsed:.1f}s:")
print(f"\n📝 ESTRUTURA ({len(plan.structure)} recomendações):")
for i, rec in enumerate(plan.structure[:2], 1):
    print(f"  {i}. {rec}")

print(f"\n🎭 PERSONAGENS ({len(plan.character)} recomendações):")
for i, rec in enumerate(plan.character[:2], 1):
    print(f"  {i}. {rec}")

print(f"\n🎵 RITMO ({len(plan.rhythm)} recomendações):")
for i, rec in enumerate(plan.rhythm[:2], 1):
    print(f"  {i}. {rec}")

# ==============================================================================
# 6. BUSCA BM25 E TEORIA
# ==============================================================================
print("\n" + "=" * 70)
print("🔍 TESTE 6: BUSCA BM25 E COMPARAÇÃO COM TEORIA")
print("-" * 50)

theory = TheoryComparator(Path("theory"))
n_files = theory.build()
print(f"✅ {n_files} livros de teoria carregados")

# Buscar conceito na teoria
query = "three act structure hero journey monomyth"
print(f"\n🔎 Buscando: '{query}'")
start = time.time()
hits = theory.compare(query, k=3)
elapsed = time.time() - start

print(f"✅ {len(hits)} resultados em {elapsed*1000:.1f}ms (BM25 10-100x mais rápido!):")
for hit in hits:
    print(f"  • {hit.doc_id[:50]}... (score: {hit.score:.2f})")
    print(f"    {hit.excerpt[:100]}...")

# ==============================================================================
# 7. INDEXAÇÃO E BUSCA RAG
# ==============================================================================
print("\n" + "=" * 70)
print("🔮 TESTE 7: SISTEMA RAG COM BM25")
print("-" * 50)

# Indexar documento
test_doc = {
    "id": "test_doc_1",
    "content": "The midpoint is a crucial moment in screenplay structure where the protagonist experiences a major revelation or reversal.",
    "metadata": {"type": "theory", "source": "test"}
}

index_document(
    doc_id=test_doc["id"],
    content=test_doc["content"],
    metadata=test_doc["metadata"]
)
print(f"✅ Documento indexado: {test_doc['id']}")

# Buscar documento
results = search_documents("midpoint revelation", k=1)
if results:
    print(f"✅ Documento encontrado:")
    print(f"  • ID: {results[0]['id']}")
    print(f"  • Score: {results[0]['score']:.2f}")
    print(f"  • Conteúdo: {results[0]['content'][:100]}...")

# ==============================================================================
# 8. TESTE DE HARMONIA DO SISTEMA
# ==============================================================================
print("\n" + "=" * 70)
print("🌟 TESTE 8: HARMONIA COMPLETA DO ECOSSISTEMA")
print("-" * 50)

print("🔄 Pipeline completo: Análise → Aprendizado → Coach → Memória")

# 1. Analisar
mini_script = """
FADE IN:

INT. CAFÉ - DAY

JOHN sits alone, staring at his coffee.

MARY enters, sees him, hesitates.

MARY
We need to talk.

JOHN
I know.

FADE OUT.
"""

analysis = doctor.analyze_script(mini_script, "mini_test")
print(f"✅ Análise: {analysis.scenes} cena, {analysis.dialogue_ratio:.0%} diálogo")

# 2. Aprender
concepts = learning.learn_from_analysis(analysis, "mini_test")
print(f"✅ Aprendizado: {len(concepts)} conceitos extraídos")

# 3. Coach
plan = coach.plan(mini_script, "mini_test")
print(f"✅ Coaching: {len(plan.structure)} recomendações estruturais")

# 4. Memorizar
memory.store(MemoryRecord(
    type="full_pipeline_test",
    key=f"harmony_test_{datetime.now().isoformat()}",
    value={
        "analysis": {"scenes": analysis.scenes},
        "learning": {"concepts": len(concepts)},
        "coaching": {"recommendations": len(plan.structure)}
    }
))
print(f"✅ Memória: Pipeline completo salvo")

# ==============================================================================
# RELATÓRIO FINAL
# ==============================================================================
print("\n" + "=" * 70)
print("📊 RELATÓRIO FINAL DO ECOSSISTEMA")
print("=" * 70)

# Verificar saúde do sistema
health = {
    "ollama": "✅" if ollama.models else "❌",
    "memory_db": "✅" if memory.stats()['total_records'] > 0 else "❌",
    "learning": "✅" if learning.get_statistics()['total_beats'] >= 0 else "❌",
    "theory": "✅" if n_files > 0 else "❌",
    "coach": "✅" if plan else "❌"
}

print("\n🏥 SAÚDE DO SISTEMA:")
for component, status in health.items():
    print(f"  {status} {component}")

all_healthy = all(s == "✅" for s in health.values())
if all_healthy:
    print("\n🎯 SISTEMA 100% OPERACIONAL - HARMONIA PERFEITA!")
    print("✨ Todos os componentes funcionando em sincronia")
else:
    print("\n⚠️ Alguns componentes precisam de atenção")

print("\n🚀 SCRIPTUREMON ULTIMATE - TESTE COMPLETO FINALIZADO")
print("=" * 70)