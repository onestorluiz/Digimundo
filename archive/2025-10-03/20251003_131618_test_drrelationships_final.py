#!/usr/bin/env python3
"""
Teste Final - DrRelationships Triple-Core Completo
"""

import time
from triple_core.core_1_specialists.character.relationships.dr_relationships import DrRelationships
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

print("="*80)
print("🎬 TESTE FINAL - DrRelationships Triple-Core")
print("="*80)
print()

# Carregar screenplay REAL
print("📄 Carregando Sonhos Sem Lembranças...")
screenplay_text = open('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt').read()
print(f"   Tamanho: {len(screenplay_text):,} caracteres")
print(f"   Linhas: {len(screenplay_text.splitlines()):,}")
print()

# Criar especialista
print("🔧 Criando DrRelationships (Character Relationships Specialist)...")
specialist = DrRelationships()
print()

# Criar wrapper com deep_context=False para teste rápido
print("🎯 Criando TripleCoreWrapper")
print("   Deep Context: False (teste rápido)")
print("   Max exemplos: 7 por problema")
print()

wrapper = TripleCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-optimized",
    deep_context=False  # False para teste rápido
)

# Executar
print("⚡ Iniciando análise Triple-Core...")
print()

start_time = time.time()
result = wrapper.analyze(screenplay_text)
elapsed = time.time() - start_time

# Resultados
print("="*80)
print("✅ ANÁLISE COMPLETA!")
print("="*80)
print()

print(f"📊 ESTATÍSTICAS TRIPLE-CORE:")
print(f"   Specialist: {result.get('specialist', 'N/A')}")
print()

print(f"   CORE 1 (Python Technical):")
core1 = result.get('python_core1', {})
print(f"      Score: {core1.get('score', 0)}/100")
print(f"      Recommendations: {len(core1.get('recommendations', []))}")
print(f"      Characters: {core1.get('character_count', 0)}")
print(f"      Relationships: {core1.get('relationship_count', 0)}")
print(f"      Total interactions: {core1.get('total_interactions', 0)}")
print(f"      Central relationship: {core1.get('central_relationship', 'None')}")
print(f"      Time: {result.get('python_core1_time', 0):.1f}s")
print()

print(f"   CORE 2 (Example Finder):")
core2 = result.get('python_core2', {})
print(f"      Problemas detectados: {len(core2.get('problems_analyzed', []))}")
print(f"      Exemplos encontrados: {core2.get('total_examples', 0)}")
print(f"      Screenplays buscados: {core2.get('screenplays_searched', 0)}")
print(f"      Time: {result.get('python_core2_time', 0):.1f}s")
print()

print(f"   CORE 3 (LLM Theory):")
llm_insights = result.get('llm_insights', '')
print(f"      Output length: {len(llm_insights):,} chars")
print(f"      Time: {result.get('llm_time', 0):.1f}s")
print()

print(f"   Quality Score: {result.get('quality_score', 0):.2f}/1.0")
print(f"   Tempo total: {elapsed:.1f}s")
print()

# Validações
print("="*80)
print("✅ VALIDAÇÕES:")
print("="*80)
errors = []

# Core 1
if not result.get('python_success'):
    errors.append("❌ Core 1 falhou")

if core1.get('score', 0) < 0 or core1.get('score', 0) > 100:
    errors.append(f"❌ Core 1 score inválido: {core1.get('score', 0)}")

# Core 2
if core2.get('total_examples', 0) == 0:
    errors.append("❌ Core 2 não encontrou exemplos")

# Core 3
if result.get('quality_score', 0) < 0.7:
    errors.append(f"❌ Core 3 qualidade baixa: {result.get('quality_score', 0):.2f}")

if len(llm_insights) < 500:
    errors.append(f"❌ Teoria muito curta: {len(llm_insights)} chars")

if errors:
    print("❌ TESTE FALHOU!")
    for err in errors:
        print(f"   {err}")
    exit(1)
else:
    print("="*80)
    print("✅ TESTE PASSOU! DrRelationships 100% INTEGRADO AO TRIPLE-CORE")
    print("="*80)
    exit(0)
