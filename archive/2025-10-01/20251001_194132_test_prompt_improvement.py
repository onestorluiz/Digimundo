#!/usr/bin/env python3
"""
Teste do PROMPT MELHORADO - 3 execuções para validar consistência
Verifica se novo prompt força citações do livro completo
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.subtext_specialist import DrSubtext
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time
import re


def load_screenplay():
    """Carrega roteiro do usuário"""
    screenplay_path = Path(__file__).parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

    if not screenplay_path.exists():
        print(f"❌ Roteiro não encontrado: {screenplay_path}")
        sys.exit(1)

    screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')

    # Limitar a 5000 palavras para testes
    words = screenplay.split()
    if len(words) > 5000:
        screenplay = ' '.join(words[:5000])

    return screenplay


def load_book_text():
    """Carrega texto completo do livro para validação"""
    book_path = Path(__file__).parent / "content/theory/Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"

    if not book_path.exists():
        return None

    return book_path.read_text(encoding='utf-8', errors='ignore')


def validate_citation_in_book(citation, book_text):
    """Valida se citação existe no livro e retorna posição (%)"""
    if not book_text or not citation:
        return None

    # Limpar citação (remover aspas, etc)
    citation_clean = citation.strip('"\'').lower()

    # Buscar no livro
    book_lower = book_text.lower()

    if citation_clean in book_lower:
        position = book_lower.index(citation_clean)
        percentage = (position / len(book_lower)) * 100
        return percentage

    return None


def extract_quotes(text):
    """Extrai citações entre aspas"""
    quotes = re.findall(r'"([^"]{20,})"', text)
    return quotes


def run_single_test(test_number, screenplay):
    """Executa um teste Deep Dive"""
    print(f"\n{'='*80}")
    print(f"🔥 TESTE #{test_number} - DEEP DIVE COM PROMPT MELHORADO")
    print(f"{'='*80}")

    specialist = DrSubtext()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",
        llm_timeout=300,
        use_theory=True,
        deep_context=True  # DEEP DIVE
    )

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    insights = result['llm_insights']

    print(f"\n✅ Teste #{test_number} completo em {elapsed:.1f}s")
    print(f"📊 Output: {len(insights)} chars")

    # Contar citações de página (formato antigo - alucinações)
    page_citations = re.findall(r'p\.\s*(\d+)', insights)
    page_citations = sorted([int(p) for p in page_citations]) if page_citations else []

    # Extrair citações literais (entre aspas)
    quotes = extract_quotes(insights)

    print(f"📚 Citações de página (formato antigo): {len(page_citations)}")
    if page_citations:
        print(f"   Range: p.{min(page_citations)} → p.{max(page_citations)}")

    print(f"💬 Citações literais (entre aspas): {len(quotes)}")

    return {
        'test_number': test_number,
        'elapsed': elapsed,
        'insights': insights,
        'page_citations': page_citations,
        'quotes': quotes,
        'insights_length': len(insights)
    }


def validate_quotes_in_book(results, book_text):
    """Valida todas as citações literais no livro"""
    print(f"\n{'='*80}")
    print("🔍 VALIDAÇÃO DE CITAÇÕES NO LIVRO")
    print(f"{'='*80}")

    if not book_text:
        print("⚠️ Livro não disponível para validação")
        return

    book_length = len(book_text)

    for result in results:
        test_num = result['test_number']
        quotes = result['quotes']

        print(f"\n📖 TESTE #{test_num} - {len(quotes)} citações:")

        validated = []
        for i, quote in enumerate(quotes[:10], 1):  # Limitar a 10 primeiras
            percentage = validate_citation_in_book(quote, book_text)

            if percentage is not None:
                section = "INÍCIO" if percentage < 33 else ("MEIO" if percentage < 66 else "FIM")
                validated.append({'quote': quote[:60], 'percentage': percentage, 'section': section})
                print(f"   {i}. ✅ [{section:5s}] {percentage:5.1f}% - \"{quote[:60]}...\"")
            else:
                print(f"   {i}. ❌ [NÃO ENCONTRADA] \"{quote[:60]}...\"")

        # Análise de distribuição
        if validated:
            sections = [v['section'] for v in validated]
            inicio = sections.count('INÍCIO')
            meio = sections.count('MEIO')
            fim = sections.count('FIM')

            print(f"\n   📊 Distribuição:")
            print(f"      INÍCIO: {inicio}/{len(validated)} ({inicio/len(validated)*100:.0f}%)")
            print(f"      MEIO:   {meio}/{len(validated)} ({meio/len(validated)*100:.0f}%)")
            print(f"      FIM:    {fim}/{len(validated)} ({fim/len(validated)*100:.0f}%)")


def compare_results(results):
    """Compara os 3 testes"""
    print(f"\n{'='*80}")
    print("📊 COMPARAÇÃO DOS 3 TESTES")
    print(f"{'='*80}")

    print(f"\n{'Teste':<10} {'Tempo':>10} {'Output':>10} {'Pág.Cit':>10} {'Quotes':>10}")
    print(f"{'-'*60}")

    for r in results:
        print(f"#{r['test_number']:<9} {r['elapsed']:>9.1f}s {r['insights_length']:>9}c "
              f"{len(r['page_citations']):>9} {len(r['quotes']):>9}")

    # Média
    avg_time = sum(r['elapsed'] for r in results) / len(results)
    avg_length = sum(r['insights_length'] for r in results) / len(results)
    avg_pages = sum(len(r['page_citations']) for r in results) / len(results)
    avg_quotes = sum(len(r['quotes']) for r in results) / len(results)

    print(f"{'-'*60}")
    print(f"{'MÉDIA':<10} {avg_time:>9.1f}s {avg_length:>9.0f}c "
          f"{avg_pages:>9.1f} {avg_quotes:>9.1f}")


def main():
    """Executa 3 testes e compara resultados"""
    print("\n" + "="*80)
    print("🧪 TESTE DE PROMPT MELHORADO - 3 EXECUÇÕES")
    print("="*80)

    # Carregar recursos
    screenplay = load_screenplay()
    book_text = load_book_text()

    print(f"✅ Roteiro carregado: {len(screenplay.split())} palavras")
    print(f"✅ Livro carregado: {len(book_text.split()) if book_text else 0} palavras")

    # Executar 3 testes
    results = []
    for i in range(1, 4):
        result = run_single_test(i, screenplay)
        results.append(result)

        # Pequena pausa entre testes
        if i < 3:
            print(f"\n⏸️  Aguardando 5s antes do próximo teste...")
            time.sleep(5)

    # Validar citações no livro
    validate_quotes_in_book(results, book_text)

    # Comparar resultados
    compare_results(results)

    # Salvar resultados
    output = {
        'timestamp': time.time(),
        'prompt_version': 'v2_distributed_citations',
        'tests': results
    }

    output_file = Path(__file__).parent / "test_prompt_improvement_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    print("\n" + "="*80)
    print("✅ TESTE COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
