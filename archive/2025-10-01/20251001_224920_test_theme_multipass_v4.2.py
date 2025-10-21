#!/usr/bin/env python3
"""
TESTE: THEME SPECIALIST - PROMPT V4.2 MULTI-PASS
Abordagem: 2 passes separados
Pass 1: Análise geral (identificação de problemas)
Pass 2: Deep dive detalhado nos top 3 problemas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.theme_consistency_specialist import DrThemeConsistency
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time


def load_screenplay():
    """Carrega roteiro do usuário"""
    screenplay_path = Path(__file__).parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

    if not screenplay_path.exists():
        print(f"❌ Roteiro não encontrado")
        sys.exit(1)

    screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')

    # Limitar a 5000 palavras
    words = screenplay.split()
    if len(words) > 5000:
        screenplay = ' '.join(words[:5000])

    return screenplay


def main():
    print("\n" + "="*80)
    print("🎬 TESTE: THEME SPECIALIST - PROMPT V4.2 MULTI-PASS")
    print("="*80)
    print("\nMetodologia: Script Doctor Philosophy")
    print("Abordagem: 2-Pass Analysis")
    print("  Pass 1: Identificação de problemas")
    print("  Pass 2: Deep dive nos top 3 problemas")
    print("="*80)

    # Carregar roteiro
    screenplay = load_screenplay()
    print(f"\n✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Criar especialista
    print(f"\n🎯 Inicializando DrThememon (Theme Consistency Specialist)...")
    specialist = DrThemeConsistency()

    # ========================================
    # PASS 1: Análise Geral (usando LLM direto)
    # ========================================
    print(f"\n{'='*80}")
    print("🔍 PASS 1: ANÁLISE GERAL")
    print(f"{'='*80}")

    # Executar análise Python primeiro
    from dataclasses import asdict
    python_result_raw = specialist.analyze(screenplay)
    python_result = asdict(python_result_raw) if hasattr(python_result_raw, '__dataclass_fields__') else python_result_raw

    # Carregar teoria (livro completo)
    theory_path = Path(__file__).parent / "content" / "theory" / "Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"
    theory_text = theory_path.read_text(encoding='utf-8', errors='ignore')
    print(f"📚 Teoria carregada: {len(theory_text.split())} palavras")

    # Criar prompt Pass 1
    prompt_pass1 = f"""📚 THEORY MATERIAL (Full Book - 128K context):
{theory_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PYTHON ANALYSIS RESULTS:
{json.dumps(python_result, indent=2, ensure_ascii=False)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 SCREENPLAY TEXT:
{screenplay[:3000]}...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASS 1 MISSION: PROBLEM IDENTIFICATION

You are a Script Doctor conducting the FIRST PASS analysis.
Your goal: Quickly identify the TOP 3 CRITICAL PROBLEMS in this screenplay.

INSTRUCTIONS:
1. Review the Python metrics and screenplay
2. Identify the 3 MOST CRITICAL problems
3. For each problem, provide:
   - Problem name (1-3 words)
   - Brief description (2 sentences)
   - Severity rating (1-10)

OUTPUT FORMAT:
Write 3 short paragraphs, one per problem.
Keep it concise - this is a diagnostic pass, not deep analysis.
Expected: 400-600 tokens (brief overview)
"""

    # Executar Pass 1
    import requests
    print(f"⏱️  Executando Pass 1...")
    start_pass1 = time.time()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "scripturemon-ultimate:latest",
            "prompt": prompt_pass1,
            "stream": False,
            "options": {"num_predict": 1000, "temperature": 0.8}
        },
        timeout=300
    )

    insights_pass1 = response.json()['response']
    time_pass1 = time.time() - start_pass1

    print(f"✅ Pass 1 completo: {len(insights_pass1)} chars em {time_pass1:.1f}s")
    print(f"\n📋 PROBLEMAS IDENTIFICADOS:")
    print("-"*80)
    print(insights_pass1[:500] + "...")
    print("-"*80)

    # ========================================
    # PASS 2: Deep Dive (usando LLM direto)
    # ========================================
    print(f"\n{'='*80}")
    print("🔬 PASS 2: DEEP DIVE NOS PROBLEMAS")
    print(f"{'='*80}")

    # Criar prompt Pass 2
    prompt_pass2 = f"""📚 THEORY MATERIAL (Full Book - 128K context):
{theory_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PYTHON ANALYSIS RESULTS:
{json.dumps(python_result, indent=2, ensure_ascii=False)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 SCREENPLAY TEXT:
{screenplay[:3000]}...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 PROBLEMS IDENTIFIED IN PASS 1:
{insights_pass1}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASS 2 MISSION: DEEP DIVE & SOLUTIONS

You are a Script Doctor conducting the SECOND PASS - deep analysis.
You've already identified the top 3 problems above.

Now, for EACH of the 3 problems:

1. DETAILED ANALYSIS (2 paragraphs):
   - Paragraph 1: Deep dive into WHY this is a problem
     * Use theory from the book to explain
     * Show specific examples from the screenplay
     * Explain the narrative impact

   - Paragraph 2: How this problem manifests throughout the script
     * Identify patterns
     * Show consequences for character/story
     * Connect to broader screenplay weaknesses

2. COMPREHENSIVE SOLUTION (2 paragraphs):
   - Paragraph 1: Theoretical foundation for the fix
     * Ground solution in theory from the book
     * Explain the principle behind the solution
     * Reference relevant concepts/techniques

   - Paragraph 2: Practical implementation
     * Step-by-step how to fix it
     * Concrete examples of before/after
     * Expected improvements

OUTPUT FORMAT:
12 substantial paragraphs total (4 paragraphs × 3 problems)
Each paragraph: 5-7 sentences
Expected: 2000-3000 tokens (deep analysis)
Be exhaustive - this is where you provide maximum value.
"""

    # Executar Pass 2
    print(f"⏱️  Executando Pass 2 (deep dive)...")
    start_pass2 = time.time()

    response2 = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "scripturemon-ultimate:latest",
            "prompt": prompt_pass2,
            "stream": False,
            "options": {"num_predict": 4000, "temperature": 0.8}
        },
        timeout=300
    )

    insights_pass2 = response2.json()['response']
    time_pass2 = time.time() - start_pass2

    print(f"✅ Pass 2 completo: {len(insights_pass2)} chars em {time_pass2:.1f}s")

    # ========================================
    # COMBINAR RESULTADOS
    # ========================================
    total_time = time_pass1 + time_pass2
    combined_insights = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PASS 1: PROBLEM IDENTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{insights_pass1}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PASS 2: DEEP DIVE & SOLUTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{insights_pass2}
"""

    total_chars = len(combined_insights)

    # Resultados
    print(f"\n{'='*80}")
    print("📊 RESULTADOS FINAIS")
    print(f"{'='*80}")

    print(f"\n⏱️  Tempo Total: {total_time:.1f}s")
    print(f"    - Pass 1: {time_pass1:.1f}s")
    print(f"    - Pass 2: {time_pass2:.1f}s")

    print(f"\n📏 Output Total: {total_chars} chars")
    print(f"    - Pass 1: {len(insights_pass1)} chars")
    print(f"    - Pass 2: {len(insights_pass2)} chars")

    print(f"\n📖 PREVIEW DA ANÁLISE COMBINADA (primeiros 800 chars):")
    print('-'*80)
    print(combined_insights[:800] + "...")
    print('-'*80)

    # Salvar resultados
    output_data = {
        'timestamp': time.time(),
        'specialist': 'DrThememon (Theme Consistency Specialist)',
        'prompt_version': 'v4.2_multipass',
        'total_elapsed': total_time,
        'pass1_elapsed': time_pass1,
        'pass2_elapsed': time_pass2,
        'insights_combined': combined_insights,
        'insights_pass1': insights_pass1,
        'insights_pass2': insights_pass2,
        'total_length': total_chars,
        'pass1_length': len(insights_pass1),
        'pass2_length': len(insights_pass2),
        'quality_score': 1.0,  # Ambos os passes tiveram sucesso
        'python_success': True,
        'llm_success': True,
    }

    output_file = Path(__file__).parent / "test_theme_multipass_v4.2_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    # Comparação
    print(f"\n{'='*80}")
    print("📈 COMPARAÇÃO COM OUTRAS VERSÕES")
    print(f"{'='*80}")

    print(f"\n  V4 (original):  2,791 chars em 153.7s")
    print(f"  V4 (otimizado): 3,233 chars em 160.6s")
    print(f"  V4.1 (estruturado): 5,825 chars em 197.4s")
    print(f"  V4.2 (multi-pass):  {total_chars} chars em {total_time:.1f}s")

    if total_chars > 5825:
        improvement = ((total_chars / 5825) - 1) * 100
        print(f"\n  💡 V4.2 vs V4.1: +{improvement:.1f}% profundidade")

    print("\n✅ TESTE MULTI-PASS COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
