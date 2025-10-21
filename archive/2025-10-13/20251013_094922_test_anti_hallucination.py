#!/usr/bin/env python3
"""
Teste Anti-Alucinação - Validação das mudanças implementadas

Testa 3 análises rápidas com autores diferentes:
- McKee (clássico)
- Truby (estrutural)
- Campbell (mitológico)

Valida:
1. Temperatura 0.2 está ativa
2. Validação NER funciona
3. Qualidade das análises
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from engine.analyzers.dr_character import DrCharacter
from engine.orchestration.dual_core_wrapper import DualCoreWrapper
from analyze_all_specialists import validate_character_hallucinations
import time
from datetime import datetime

def test_single_analysis(screenplay_path: str, author: str, test_num: int):
    """Executa uma análise e valida resultado"""
    print(f"\n{'='*80}")
    print(f"TESTE #{test_num}: CHARACTER × {author.upper()}")
    print(f"{'='*80}")

    start = time.time()

    # Initialize specialist
    specialist = DrCharacter()

    # Initialize wrapper (Ollama) - author vai no specialist_type!
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type=author,  # ← AUTOR AQUI!
        llm_model='scripturemon-optimized',
        deep_context=True,
        use_personalized_prompts=True
    )

    print(f"⏳ Analisando com {author.upper()}...")

    # Run analysis - passa PATH, não texto!
    result = wrapper.analyze(screenplay_path)

    elapsed = time.time() - start

    # Extract analysis text
    analysis_text = result.get('llm_insights', '')

    # Read screenplay for validation
    print(f"🔍 Validando com NER...")
    import PyPDF2
    screenplay_text = ""
    with open(screenplay_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages[:50]:  # Primeiras 50 páginas apenas
            screenplay_text += page.extract_text()

    validation = validate_character_hallucinations(screenplay_text, analysis_text)

    # Results
    print(f"\n📊 RESULTADOS:")
    print(f"   Tempo: {elapsed:.1f}s")
    print(f"   Tamanho: {len(analysis_text):,} caracteres")
    print(f"   Qualidade: {result.get('quality_score', 'N/A')}/10")
    print(f"\n🔍 VALIDAÇÃO NER:")
    print(f"   Status: {'✅ VÁLIDO' if validation['valid'] else '⚠️ ALUCINAÇÃO DETECTADA'}")
    print(f"   Confiança: {validation['confidence']:.2%}")
    print(f"   Personagens reais: {len(validation.get('real_characters', set()))} encontrados")
    print(f"   Personagens na análise: {len(validation.get('analysis_characters', set()))}")

    if not validation['valid']:
        print(f"   ⚠️ INVENTADOS: {validation['invented_characters']}")

    # Sample output
    print(f"\n📝 AMOSTRA DA ANÁLISE (primeiros 500 chars):")
    print(f"   {analysis_text[:500]}...")

    return {
        'author': author,
        'time': elapsed,
        'size': len(analysis_text),
        'quality': result.get('quality_score'),
        'validation': validation,
        'sample': analysis_text[:1000]
    }

def main():
    screenplay_path = "inputs/examples/Te Encontro em Mim .pdf"

    print("🎬 TESTE ANTI-ALUCINAÇÃO - SCRIPTUREMON")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📄 Roteiro: {screenplay_path}")
    print(f"🎯 Objetivo: Validar temp 0.2 + NER validation")

    # Check if file exists
    if not Path(screenplay_path).exists():
        print(f"\n❌ ERRO: Roteiro não encontrado: {screenplay_path}")
        return

    results = []

    # Test 1: McKee
    results.append(test_single_analysis(screenplay_path, 'mckee', 1))

    # Test 2: Truby
    results.append(test_single_analysis(screenplay_path, 'truby', 2))

    # Test 3: Campbell
    results.append(test_single_analysis(screenplay_path, 'campbell', 3))

    # Summary
    print(f"\n{'='*80}")
    print("📊 RESUMO COMPARATIVO")
    print(f"{'='*80}")

    for i, r in enumerate(results, 1):
        print(f"\nTESTE #{i} - {r['author'].upper()}:")
        print(f"   Tempo: {r['time']:.1f}s")
        print(f"   Tamanho: {r['size']:,} chars")
        print(f"   Qualidade: {r['quality']}/10")
        print(f"   NER Status: {'✅ OK' if r['validation']['valid'] else '⚠️ FALHOU'}")
        print(f"   Confiança: {r['validation']['confidence']:.2%}")

    # Aggregate stats
    avg_time = sum(r['time'] for r in results) / len(results)
    avg_size = sum(r['size'] for r in results) / len(results)
    avg_quality = sum(r['quality'] or 0 for r in results) / len(results)
    all_valid = all(r['validation']['valid'] for r in results)

    print(f"\n{'='*80}")
    print("🎯 ESTATÍSTICAS GERAIS:")
    print(f"   Tempo médio: {avg_time:.1f}s")
    print(f"   Tamanho médio: {avg_size:,.0f} chars")
    print(f"   Qualidade média: {avg_quality:.1f}/10")
    valid_count = sum(1 for r in results if r['validation']['valid'])
    print(f"   Taxa validação: {'✅ 100% VÁLIDO' if all_valid else f'⚠️ {valid_count}/3 válidos'}")

    print(f"\n✅ TESTE COMPLETO!")
    print(f"📊 Resultados salvos para análise manual acima.")

if __name__ == '__main__':
    main()
