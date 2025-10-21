#!/usr/bin/env python3
"""
Teste Final - DrSubtext Triple-Core Completo
"""

import time
from triple_core.core_1_specialists.subtext.dr_subtext import DrSubtext
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

print("="*80)
print("🎬 TESTE FINAL - DrSubtext Triple-Core")
print("="*80)
print()

# Carregar screenplay REAL
print("📄 Carregando Sonhos Sem Lembranças...")
screenplay_text = open('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt').read()
print(f"   Tamanho: {len(screenplay_text):,} caracteres")
print(f"   Linhas: {len(screenplay_text.splitlines()):,}")
print()

# Criar especialista
print("🔧 Criando DrSubtext (Subtext and Layered Meaning Specialist)...")
specialist = DrSubtext()
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
subtext_analysis = core1.get('subtext_analysis')
if subtext_analysis and hasattr(subtext_analysis, 'subtext_examples'):
    print(f"      Subtext examples: {len(subtext_analysis.subtext_examples)}")
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
elif core1.get('score', 0) < 0:
    errors.append(f"❌ Core 1: Score inválido ({core1.get('score')})")
elif len(core1.get('recommendations', [])) < 1:
    errors.append("❌ Core 1: Nenhuma recomendação gerada")
else:
    print(f"✅ Core 1: {core1.get('score')}/100, {len(core1.get('recommendations', []))} recommendations")

# Core 2
if not result.get('examples_success'):
    errors.append("❌ Core 2 falhou")
elif core2.get('total_examples', 0) < 5:
    errors.append(f"❌ Core 2: Poucos exemplos ({core2.get('total_examples')})")
else:
    print(f"✅ Core 2: {core2.get('total_examples')} exemplos, {len(core2.get('problems_analyzed', []))} problemas")

# Core 3
if not result.get('llm_success'):
    errors.append("❌ Core 3 falhou")
elif len(llm_insights) < 1000:
    errors.append(f"❌ Core 3: Output muito curto ({len(llm_insights)} chars)")
else:
    print(f"✅ Core 3: {len(llm_insights):,} chars gerados")

# Quality
quality = result.get('quality_score', 0)
if quality < 0.7:
    errors.append(f"❌ Quality score baixo: {quality:.2f}")
else:
    print(f"✅ Quality Score: {quality:.2f}")

print()

if errors:
    print("❌ ERROS ENCONTRADOS:")
    for err in errors:
        print(f"   {err}")
    print()
    exit(1)
else:
    print("="*80)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("="*80)
    print()

    # Mostrar problemas mapeados
    print("🔍 PROBLEMAS MAPEADOS (Core 2 keywords):")
    for i, prob in enumerate(core2.get('problems_analyzed', []), 1):
        print(f"{i}. {prob}")
    print()

    # Mostrar recomendações Core 1
    print("💡 RECOMENDAÇÕES (Core 1):")
    for i, rec in enumerate(core1.get('recommendations', [])[:5], 1):
        print(f"{i}. {rec}")
    print()

    # Mostrar amostra do LLM
    print("📝 AMOSTRA LLM OUTPUT (primeiros 500 chars):")
    print("-"*80)
    print(llm_insights[:500])
    if len(llm_insights) > 500:
        print(f"... (+{len(llm_insights) - 500} chars)")
    print("-"*80)
    print()

    exit(0)
