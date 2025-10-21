#!/usr/bin/env python3
"""
Teste Triple-Core Completo - DrStructure
"""

import time
from triple_core.core_1_specialists.structure.dr_structure import DrStructure
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

print("="*80)
print("🎬 TESTE TRIPLE-CORE - DrStructure")
print("="*80)
print()

# Carregar screenplay de teste
print("📄 Carregando screenplay de teste...")
screenplay_text = open('workspace/inputs/test_screenplay.txt').read()
print(f"   Tamanho: {len(screenplay_text)} caracteres")
print()

# Criar especialista
print("🔧 Criando DrStructure (Narrative Architect)...")
specialist = DrStructure()
print()

# Criar wrapper
print("🎯 Criando TripleCoreWrapper")
print("   Configuração:")
print("   - Deep Context: True (McKee full book)")
print("   - Problemas: até 15")
print("   - Exemplos/problema: 7")
print("   - Total exemplos esperado: ~105")
print()

wrapper = TripleCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-optimized",
    deep_context=False  # False para testes rápidos, True para produção
)

# Executar
print("⚡ Iniciando análise Triple-Core...")
print("   Isso levará ~5-7 minutos (LLM Deep Dive)")
print()

start_time = time.time()
result = wrapper.analyze(screenplay_text)
elapsed = time.time() - start_time

# Resultados
print("="*80)
print("✅ ANÁLISE COMPLETA!")
print("="*80)
print()

print(f"📊 ESTATÍSTICAS:")
print(f"   Core 1 (Python): {len(str(result.get('python_core1', '')))} chars")
print(f"   Core 2 (Examples): {result.get('python_core2', {}).get('total_examples', 0)} exemplos")
print(f"   Core 3 (LLM): {len(result.get('llm_insights', ''))} chars")  # FIX: llm_insights, não llm_response
print(f"   Quality Score: {result.get('quality_score', 'N/A')}")
print(f"   Tempo total: {elapsed:.1f}s")
print()

# Validações
print("✅ VALIDAÇÕES:")
errors = []

# Core 1 deve ter rodado
if not result.get('python_success'):
    errors.append("❌ Core 1 (Python) falhou")
else:
    score = result.get('python_core1', {}).get('score', 0)
    print(f"   ✅ Core 1: Score {score}/100")

# Core 2 deve ter encontrado exemplos
examples_count = result.get('python_core2', {}).get('total_examples', 0)
if examples_count < 5:
    errors.append(f"❌ Core 2: Poucos exemplos ({examples_count})")
else:
    print(f"   ✅ Core 2: {examples_count} exemplos encontrados")

# Core 3 deve ter gerado resposta
llm_length = len(result.get('llm_insights', ''))  # FIX: llm_insights, não llm_response
if llm_length < 1000:
    errors.append(f"❌ Core 3: Resposta muito curta ({llm_length} chars)")
else:
    print(f"   ✅ Core 3: {llm_length} chars gerados")

# Quality score deve ser bom
quality = result.get('quality_score', 0)
if quality < 0.7:
    errors.append(f"❌ Quality score baixo: {quality}")
else:
    print(f"   ✅ Quality Score: {quality:.2f}")

print()
if errors:
    print("❌ ERROS ENCONTRADOS:")
    for err in errors:
        print(f"   {err}")
    exit(1)
else:
    print("🎉 TODOS OS TESTES PASSARAM!")
    print()
    print("📄 Outputs gerados em workspace/outputs/formatted/")
    exit(0)
