#!/usr/bin/env python3
"""
Teste Simplificado - Validação rápida temperatura 0.2 + NER

Teste único com shallow mode (sem deep context) para validação rápida.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from engine.analyzers.dr_character import DrCharacter
from engine.orchestration.dual_core_wrapper import DualCoreWrapper
import time
import PyPDF2

def main():
    screenplay_path = "inputs/examples/Te Encontro em Mim .pdf"
    author = 'mckee'

    print("🎬 TESTE SIMPLIFICADO - VALIDAÇÃO TEMPERATURA 0.2 + NER")
    print(f"📄 Roteiro: {screenplay_path}")
    print(f"👤 Autor: {author.upper()}")
    print(f"🎯 Modo: SHALLOW (sem deep context, mais rápido)\n")

    # Initialize
    specialist = DrCharacter()

    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type=author,
        llm_model='scripturemon-optimized',
        deep_context=False,  # ← SHALLOW MODE
        use_personalized_prompts=False
    )

    print("⏳ Executando análise...")
    start = time.time()

    result = wrapper.analyze(screenplay_path)

    elapsed = time.time() - start

    # Extract
    analysis_text = result.get('llm_insights', '')
    quality = result.get('quality_score', 0)
    validation = result.get('validation', {})

    # Results
    print("="*80)
    print("📊 RESULTADOS")
    print("="*80)
    print(f"⏱️  Tempo: {elapsed:.1f}s")
    print(f"📏 Tamanho: {len(analysis_text):,} caracteres")
    print(f"⭐ Qualidade: {quality}/10")

    print(f"\n🔍 VALIDAÇÃO NER:")
    print(f"   Status: {'✅ VÁLIDO' if validation.get('valid') else '⚠️ ALUCINAÇÃO'}")
    print(f"   Overlap: {validation.get('overlap_ratio', 0):.1%}")
    print(f"   Personagens reais: {validation.get('screenplay_entities', 0)}")
    print(f"   Personagens na análise: {validation.get('llm_entities', 0)}")
    print(f"   Matched: {len(validation.get('matched', []))}")

    if not validation.get('valid'):
        print(f"   ⚠️ INVENTADOS: {validation.get('hallucinated', [])}")

    if 'warning' in validation:
        print(f"   ⚠️  Warning: {validation['warning']}")

    # Sample
    print(f"\n📝 AMOSTRA (primeiros 800 caracteres):")
    print(f"{analysis_text[:800]}...")

    # Check temperature indication
    if 'generica' in analysis_text.lower() or 'genérica' in analysis_text.lower():
        print(f"\n⚠️  POSSÍVEL PROBLEMA: Análise contém palavra 'genérica'")

    if len(analysis_text) < 2000:
        print(f"\n⚠️  POSSÍVEL PROBLEMA: Análise muito curta (<2000 chars)")

    print(f"\n{'='*80}")
    if validation.get('valid') and len(analysis_text) > 5000:
        print("✅ IMPLEMENTAÇÃO FUNCIONANDO CORRETAMENTE!")
        print("   - Temperatura 0.2 ativa (análise factual esperada)")
        print("   - Validação NER funcionando")
        print(f"   - Overlap: {validation.get('overlap_ratio', 0):.1%}")
        if len(validation.get('hallucinated', [])) == 0:
            print("   - Nenhum personagem inventado detectado")
    else:
        print("⚠️  VERIFICAR IMPLEMENTAÇÃO")
        if not validation.get('valid'):
            print(f"   - Personagens inventados: {validation.get('hallucinated', [])}")
        if len(analysis_text) < 5000:
            print(f"   - Análise muito curta: {len(analysis_text)} chars")
    print("="*80)

if __name__ == '__main__':
    main()
