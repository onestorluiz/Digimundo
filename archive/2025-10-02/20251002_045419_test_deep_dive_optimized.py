#!/usr/bin/env python3
"""
FASE 2: TESTE DEEP DIVE
Testa modelo otimizado com livro McKee COMPLETO (77k palavras)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time
import re


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
        'pages': len(re.findall(r'\bp[áa]gina\s+\d+|\bpage\s+\d+', text, re.IGNORECASE)),
        'mckee_refs': len(re.findall(r'\bmckee|\bcap[íi]tulo\s+\d+|\bchapter\s+\d+', text, re.IGNORECASE))
    }


def analyze_specificity(text):
    """Análise de especificidade vs genericidade"""
    generic_patterns = [
        r'\bcould be improved\b',
        r'\bneeds work\b',
        r'\bprecisa de desenvolvimento\b',
        r'\bpoderia ser melhorado\b',
        r'\bthe protagonist\b',
        r'\bo protagonista\b',
        r'\bthe character\b',
        r'\bhas potential\b'
    ]

    specific_patterns = [
        r'\bscene\s+\d+\b',
        r'\bcena\s+\d+\b',
        r'\bp[áa]gina\s+\d+\b',
        r'\b[A-Z][a-z]+:\s*"',
        r'\bmckee\s+\w+',
        r'\bcap[íi]tulo\s+\d+\b'
    ]

    generic_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in generic_patterns)
    specific_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in specific_patterns)

    return {
        'generic_count': generic_count,
        'specific_count': specific_count,
        'specificity_ratio': specific_count / (generic_count + specific_count + 1)
    }


def main():
    print("\n" + "="*80)
    print("🚀 FASE 2: TESTE DEEP DIVE - Modelo Otimizado + Livro McKee Completo")
    print("="*80)
    print("\nConfiguração:")
    print("  Modelo: scripturemon-optimized")
    print("  Deep Context: ✅ SIM (livro McKee completo ~77k palavras)")
    print("  Roteiro: 1000 palavras (para teste rápido)")
    print("  Timeout: 10 minutos")
    print("="*80)

    # Carregar roteiro
    screenplay_path = Path(__file__).parent.parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"
    screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
    screenplay_excerpt = ' '.join(screenplay.split()[:1000])

    print(f"\n📚 Carregando specialist...")
    specialist = DrDialogue()

    print(f"\n🔧 Inicializando wrapper com DEEP DIVE mode...")
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-optimized",
        llm_timeout=600,  # 10 minutos
        use_theory=True,
        deep_context=True  # ⚡ DEEP DIVE!
    )

    print(f"\n⏳ Executando análise DEEP DIVE...")
    print(f"   (Isso vai demorar ~5-10 minutos - aguarde...)")

    start = time.time()

    try:
        result = wrapper.analyze(screenplay_excerpt)
        elapsed = time.time() - start

        analysis = result.get('llm_insights', '')

        print(f"\n✅ ANÁLISE COMPLETA!")
        print(f"⏱️  Tempo total: {elapsed:.1f}s ({elapsed/60:.1f} minutos)")
        print(f"📏 Output: {len(analysis)} chars ({len(analysis.split())} palavras)")

        # Métricas
        citations = count_citations(analysis)
        specificity = analyze_specificity(analysis)

        print(f"\n{'='*80}")
        print("📊 MÉTRICAS DE ESPECIFICIDADE")
        print(f"{'='*80}\n")

        print(f"📍 Citações Específicas:")
        print(f"   Scene references:    {citations['scenes']}")
        print(f"   Dialogue quotes:     {citations['quotes']}")
        print(f"   Character mentions:  {citations['characters']}")
        print(f"   Page references:     {citations['pages']}")
        print(f"   McKee references:    {citations['mckee_refs']}")

        print(f"\n🎯 Análise de Qualidade:")
        print(f"   Generic phrases:     {specificity['generic_count']}")
        print(f"   Specific markers:    {specificity['specific_count']}")
        print(f"   Specificity ratio:   {specificity['specificity_ratio']:.2f}")

        # Comparar com baseline do teste anterior
        print(f"\n{'='*80}")
        print("📈 COMPARAÇÃO COM BASELINE (do teste rápido anterior)")
        print(f"{'='*80}\n")

        baseline_citations = {'scenes': 1, 'quotes': 2, 'characters': 12, 'mckee_refs': 0}
        baseline_specificity = 0.67

        improvements = {
            'Scene refs': ((citations['scenes'] / max(baseline_citations['scenes'], 1)) - 1) * 100,
            'Dialogue quotes': ((citations['quotes'] / max(baseline_citations['quotes'], 1)) - 1) * 100,
            'Character mentions': ((citations['characters'] / max(baseline_citations['characters'], 1)) - 1) * 100,
            'McKee refs': citations['mckee_refs'],  # Baseline tinha 0
            'Specificity ratio': ((specificity['specificity_ratio'] / max(baseline_specificity, 0.01)) - 1) * 100
        }

        for metric, improvement in improvements.items():
            if 'McKee' in metric:
                symbol = '✅'
                print(f"{symbol} {metric:<25} {improvement:.0f} referências (baseline: 0)")
            else:
                symbol = '⬆️' if improvement > 0 else '⬇️'
                color = '✅' if improvement > 0 else '❌'
                print(f"{color} {metric:<25} {improvement:>+7.1f}%  {symbol}")

        # Preview
        print(f"\n{'='*80}")
        print("📄 PREVIEW DA ANÁLISE (primeiros 1200 chars)")
        print(f"{'='*80}\n")
        print(analysis[:1200])
        print("\n...")

        # Avaliar qualidade
        print(f"\n{'='*80}")
        print("🎯 AVALIAÇÃO FINAL")
        print(f"{'='*80}\n")

        score = 0
        criteria = []

        if citations['scenes'] >= 3:
            score += 1
            criteria.append("✅ Scene references >= 3")
        else:
            criteria.append(f"❌ Scene references: {citations['scenes']} (meta: 3+)")

        if citations['quotes'] >= 4:
            score += 1
            criteria.append("✅ Dialogue quotes >= 4")
        else:
            criteria.append(f"⚠️  Dialogue quotes: {citations['quotes']} (meta: 4+)")

        if citations['characters'] >= 15:
            score += 1
            criteria.append("✅ Character mentions >= 15")
        else:
            criteria.append(f"⚠️  Character mentions: {citations['characters']} (meta: 15+)")

        if citations['mckee_refs'] >= 5:
            score += 1
            criteria.append("✅ McKee references >= 5")
        else:
            criteria.append(f"⚠️  McKee refs: {citations['mckee_refs']} (meta: 5+)")

        if specificity['specificity_ratio'] >= 0.8:
            score += 1
            criteria.append("✅ Specificity ratio >= 0.8")
        else:
            criteria.append(f"⚠️  Specificity: {specificity['specificity_ratio']:.2f} (meta: 0.8+)")

        if specificity['generic_count'] == 0:
            score += 1
            criteria.append("✅ Zero generic phrases")
        else:
            criteria.append(f"⚠️  Generic phrases: {specificity['generic_count']}")

        for criterion in criteria:
            print(f"  {criterion}")

        print(f"\n{'='*80}")
        print(f"SCORE: {score}/6 critérios atendidos")

        if score >= 5:
            print("🎉 EXCELENTE - Deep Dive funcionando perfeitamente!")
            result_status = "EXCELLENT"
        elif score >= 4:
            print("✅ BOM - Deep Dive melhorou significativamente")
            result_status = "GOOD"
        elif score >= 3:
            print("⚠️  REGULAR - Melhorou mas abaixo do esperado")
            result_status = "FAIR"
        else:
            print("❌ INSUFICIENTE - Deep Dive não trouxe melhoria")
            result_status = "POOR"

        print(f"{'='*80}\n")

        # Salvar resultados
        output_data = {
            'timestamp': time.time(),
            'model': 'scripturemon-optimized',
            'mode': 'deep_dive',
            'elapsed': elapsed,
            'analysis': analysis,
            'length': len(analysis),
            'words': len(analysis.split()),
            'citations': citations,
            'specificity': specificity,
            'score': score,
            'max_score': 6,
            'status': result_status,
            'improvements': improvements,
            'criteria': criteria
        }

        output_file = Path(__file__).parent.parent / "results" / "deep_dive_optimized_test.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Resultados salvos em: {output_file}\n")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE ANÁLISE: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
