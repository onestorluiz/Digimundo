#!/usr/bin/env python3
"""
TESTE COMPARATIVO: Baseline vs Optimized
Compara modelo antigo (scripturemon-ultimate) vs novo (scripturemon-optimized)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time
import re


def load_screenplay():
    """Carrega primeiras ~5k palavras do roteiro para teste"""
    screenplay_path = Path(__file__).parent.parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

    if not screenplay_path.exists():
        print(f"❌ Roteiro não encontrado: {screenplay_path}")
        sys.exit(1)

    screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')

    # Limitar para teste rápido (~5k palavras)
    words = screenplay.split()[:5000]
    return ' '.join(words)


def count_citations(text):
    """Conta citações específicas"""
    return {
        'scenes': len(re.findall(r'\bscene\s+\d+|\bcena\s+\d+', text, re.IGNORECASE)),
        'quotes': len(re.findall(r'["""]([^"""]{15,})["""]', text)),
        'characters': sum([
            text.lower().count('samantha'),
            text.lower().count('alberto'),
            text.lower().count('kleber'),
            text.lower().count('yasmim')
        ]),
        'pages': len(re.findall(r'\bp[áa]gina\s+\d+|\bpage\s+\d+', text, re.IGNORECASE))
    }


def analyze_specificity(text):
    """Análise de especificidade vs genericidade"""
    # Anti-patterns (frases genéricas)
    generic_patterns = [
        r'\bcould be improved\b',
        r'\bneeds work\b',
        r'\bprecisa de desenvolvimento\b',
        r'\bpoderia ser melhorado\b',
        r'\bthe protagonist\b',
        r'\bo protagonista\b',
        r'\bthe character\b',
        r'\bthe dialogue\b',
        r'\bhas potential\b'
    ]

    generic_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in generic_patterns)

    # Specific patterns
    specific_patterns = [
        r'\bscene\s+\d+\b',
        r'\bcena\s+\d+\b',
        r'\bp[áa]gina\s+\d+\b',
        r'\bpage\s+\d+\b',
        r'\b[A-Z][a-z]+:\s*"',  # Character name + colon + quote
        r'\bmckee\s+\w+',
        r'\bcap[íi]tulo\s+\d+\b',
        r'\bchapter\s+\d+\b'
    ]

    specific_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in specific_patterns)

    return {
        'generic_count': generic_count,
        'specific_count': specific_count,
        'specificity_ratio': specific_count / (generic_count + specific_count + 1)
    }


def test_model(model_name, deep_context=False):
    """Testa um modelo específico"""
    print(f"\n{'='*80}")
    print(f"🔬 TESTANDO: {model_name}")
    print(f"   Deep Context: {'✅ SIM' if deep_context else '❌ NÃO'}")
    print(f"{'='*80}")

    screenplay = load_screenplay()
    specialist = DrDialogue()

    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model=model_name,
        use_theory=True,
        deep_context=deep_context
    )

    print(f"\n⏳ Executando análise...")
    start = time.time()

    try:
        result = wrapper.analyze(screenplay)
        elapsed = time.time() - start

        analysis = result.get('llm_insights', '')

        print(f"✅ Análise completada em {elapsed:.1f}s")

        # Métricas
        citations = count_citations(analysis)
        specificity = analyze_specificity(analysis)

        return {
            'model': model_name,
            'deep_context': deep_context,
            'success': True,
            'time': elapsed,
            'analysis': analysis,
            'length': len(analysis),
            'words': len(analysis.split()),
            'citations': citations,
            'specificity': specificity,
            'python_success': result.get('python_success', False),
            'llm_success': result.get('llm_success', False)
        }

    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

        return {
            'model': model_name,
            'deep_context': deep_context,
            'success': False,
            'error': str(e)
        }


def main():
    print("\n" + "="*80)
    print("🎯 TESTE COMPARATIVO: BASELINE vs OPTIMIZED")
    print("="*80)
    print("\nObjetivo: Validar melhorias da otimização")
    print("Roteiro: Sonhos sem Lembranças (primeiras 5k palavras)")
    print("="*80)

    results = {}

    # TESTE 1: Baseline (modelo antigo, shallow mode)
    results['baseline'] = test_model('scripturemon-ultimate:latest', deep_context=False)

    # TESTE 2: Optimized (modelo novo, shallow mode para comparação justa)
    results['optimized_shallow'] = test_model('scripturemon-optimized', deep_context=False)

    # TESTE 3: Optimized Deep (modelo novo, deep mode)
    results['optimized_deep'] = test_model('scripturemon-optimized', deep_context=True)

    # COMPARAÇÃO
    print(f"\n{'='*80}")
    print("📊 COMPARAÇÃO DE RESULTADOS")
    print(f"{'='*80}\n")

    # Tabela comparativa
    print(f"{'Configuração':<25} {'Tempo':<12} {'Output':<12} {'Scenes':<10} {'Quotes':<10} {'Chars':<10} {'Spec':<10}")
    print("-" * 100)

    for key, data in results.items():
        if not data['success']:
            print(f"{key:<25} {'ERROR':<12} {'N/A':<12} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
            continue

        print(f"{key:<25} "
              f"{data['time']:>8.1f}s   "
              f"{data['words']:>6} words  "
              f"{data['citations']['scenes']:>6}     "
              f"{data['citations']['quotes']:>6}     "
              f"{data['citations']['characters']:>6}     "
              f"{data['specificity']['specificity_ratio']:>6.2f}")

    # Calcular melhorias
    if results['baseline']['success'] and results['optimized_deep']['success']:
        baseline = results['baseline']
        optimized = results['optimized_deep']

        print(f"\n{'='*80}")
        print("📈 MELHORIAS (Optimized Deep vs Baseline)")
        print(f"{'='*80}\n")

        improvements = {
            'Tempo': ((optimized['time'] / baseline['time']) - 1) * 100,
            'Output (words)': ((optimized['words'] / baseline['words']) - 1) * 100,
            'Scene citations': ((optimized['citations']['scenes'] / max(baseline['citations']['scenes'], 1)) - 1) * 100,
            'Dialogue quotes': ((optimized['citations']['quotes'] / max(baseline['citations']['quotes'], 1)) - 1) * 100,
            'Character mentions': ((optimized['citations']['characters'] / max(baseline['citations']['characters'], 1)) - 1) * 100,
            'Specificity ratio': ((optimized['specificity']['specificity_ratio'] / max(baseline['specificity']['specificity_ratio'], 0.01)) - 1) * 100
        }

        for metric, improvement in improvements.items():
            symbol = '⬇️' if improvement < 0 else '⬆️'
            color = '✅' if (improvement > 0 and 'Tempo' not in metric) or (improvement < 0 and 'Tempo' in metric) else '❌'
            print(f"{color} {metric:<25} {improvement:>+7.1f}%  {symbol}")

        # Análise de qualidade
        print(f"\n{'='*80}")
        print("🎯 ANÁLISE DE QUALIDADE")
        print(f"{'='*80}\n")

        baseline_spec = baseline['specificity']
        optimized_spec = optimized['specificity']

        print(f"BASELINE:")
        print(f"  Generic phrases: {baseline_spec['generic_count']}")
        print(f"  Specific refs:   {baseline_spec['specific_count']}")
        print(f"  Ratio:           {baseline_spec['specificity_ratio']:.2f}")

        print(f"\nOPTIMIZED:")
        print(f"  Generic phrases: {optimized_spec['generic_count']}")
        print(f"  Specific refs:   {optimized_spec['specific_count']}")
        print(f"  Ratio:           {optimized_spec['specificity_ratio']:.2f}")

        # Determinar sucesso
        success_criteria = {
            'Scene citations aumentaram': optimized['citations']['scenes'] > baseline['citations']['scenes'],
            'Quotes aumentaram': optimized['citations']['quotes'] > baseline['citations']['quotes'],
            'Specificity melhorou': optimized_spec['specificity_ratio'] > baseline_spec['specificity_ratio'],
            'Output cresceu': optimized['words'] > baseline['words'],
            'Generic phrases reduziram': optimized_spec['generic_count'] < baseline_spec['generic_count']
        }

        passed = sum(success_criteria.values())
        total = len(success_criteria)

        print(f"\n{'='*80}")
        print(f"🏆 CRITÉRIOS DE SUCESSO: {passed}/{total} ({passed/total*100:.0f}%)")
        print(f"{'='*80}\n")

        for criterion, passed in success_criteria.items():
            symbol = '✅' if passed else '❌'
            print(f"{symbol} {criterion}")

        if passed >= 4:
            print(f"\n🎉 OTIMIZAÇÃO BEM-SUCEDIDA! ({passed}/{total} critérios)")
        else:
            print(f"\n⚠️  Otimização parcial ({passed}/{total} critérios)")

    # Salvar resultados
    output_file = Path(__file__).parent.parent / "results" / "comparison_optimized_vs_baseline.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"💾 Resultados salvos: {output_file}")
    print(f"{'='*80}\n")

    # Preview das análises
    print(f"\n{'='*80}")
    print("📄 PREVIEW DAS ANÁLISES (primeiros 500 chars)")
    print(f"{'='*80}\n")

    for key, data in results.items():
        if data['success']:
            print(f"\n--- {key.upper()} ---")
            print(data['analysis'][:500] + "...")

    print(f"\n{'='*80}")
    print("✅ TESTE COMPLETO!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
