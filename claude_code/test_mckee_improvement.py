#!/usr/bin/env python3
"""
🧪 TEST: Transformar MCKEE_DIALOGUE de 8/10 para 10/10

Este script testa o BenchmarkPromptGenerator rodando análise
melhorada e comparando com benchmark atual.
"""

import sys
from pathlib import Path
import subprocess
import time
from datetime import datetime

# Add scripturemon to path
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon')

# Import benchmark generator
sys.path.insert(0, str(Path('/Users/clubproducoes/Digimundo/claude_code')))
from benchmark_prompt_generator import BenchmarkPromptGenerator

# Import scripturemon components
import PyPDF2


def read_screenplay(pdf_path: Path, max_words: int = 1000) -> str:
    """Lê roteiro PDF e retorna excerpt."""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            screenplay = ""
            for page in pdf_reader.pages:
                screenplay += page.extract_text() + "\n"

        # Pegar primeiras max_words palavras
        words = screenplay.split()
        excerpt = ' '.join(words[:max_words])
        return excerpt

    except Exception as e:
        print(f'❌ Erro ao ler PDF: {e}')
        return ""


def call_ollama_llm(prompt: str, model: str = 'scripturemon-optimized', timeout: int = None) -> str:
    """
    Chama Ollama LLM com prompt.

    Args:
        prompt: Prompt completo
        model: Nome do modelo
        timeout: Timeout em segundos (None = sem timeout)

    Returns:
        Resposta do LLM
    """
    cmd = ['ollama', 'run', model]

    run_kwargs = {
        'input': prompt,
        'capture_output': True,
        'text': True
    }

    if timeout is not None:
        run_kwargs['timeout'] = timeout
        print(f'⏱️  Timeout: {timeout}s')
    else:
        print('⏱️  Sem timeout (modo deep)')

    try:
        print('🤖 Chamando Ollama...')
        result = subprocess.run(cmd, **run_kwargs)

        if result.returncode != 0:
            raise Exception(f"Ollama failed: {result.stderr}")

        response = result.stdout.strip()

        # Remove control lines
        lines = response.split('\n')
        clean_lines = [l for l in lines if not l.startswith('[')]
        response = '\n'.join(clean_lines).strip()

        return response

    except subprocess.TimeoutExpired:
        raise Exception(f"LLM timeout after {timeout}s")
    except Exception as e:
        raise Exception(f"LLM call failed: {e}")


def validate_10_10_quality(llm_response: str) -> dict:
    """
    Valida se resposta atende critérios 10/10.

    Returns:
        Dict com score e detalhes
    """
    import re

    score = 10.0
    issues = []

    # 1. LENGTH CHECK
    char_count = len(llm_response)
    word_count = len(llm_response.split())

    if char_count < 5000:
        gap = 5000 - char_count
        score -= (gap / 5000) * 2.0  # -2.0 max
        issues.append(f"Length too short: {char_count} chars (need 5,000+)")
    elif char_count < 5500:
        issues.append(f"Length acceptable but below ideal: {char_count} chars")
    else:
        issues.append(f"✅ Excellent length: {char_count} chars")

    # 2. QUOTE COUNT
    quote_pattern = r'"([^"]+)"'
    quotes = re.findall(quote_pattern, llm_response)
    quote_count = len(quotes)

    if quote_count < 10:
        gap = 10 - quote_count
        score -= (gap / 10) * 1.5  # -1.5 max
        issues.append(f"Not enough quotes: {quote_count} (need 10+)")
    else:
        issues.append(f"✅ Good quotes: {quote_count}")

    # 3. SCENE CITATIONS
    scene_pattern = r'\bcena\s+\d+\b'
    scenes = re.findall(scene_pattern, llm_response.lower())
    scene_count = len(set(scenes))

    if scene_count < 3:
        gap = 3 - scene_count
        score -= (gap / 3) * 1.5  # -1.5 max
        issues.append(f"Not enough scenes cited: {scene_count} (need 3+)")
    else:
        issues.append(f"✅ Good scene citations: {scene_count}")

    # 4. PAGE CITATIONS
    page_pattern = r'\bp(?:ágina|\.)\s*\d+\b'
    pages = re.findall(page_pattern, llm_response.lower())
    page_count = len(pages)

    if page_count < 5:
        gap = 5 - page_count
        score -= (gap / 5) * 1.0  # -1.0 max
        issues.append(f"Not enough pages cited: {page_count} (need 5+)")
    else:
        issues.append(f"✅ Good page citations: {page_count}")

    # 5. BEFORE/AFTER EXAMPLES
    before_after_pattern = r'(ANTES|BEFORE|DEPOIS|AFTER)'
    before_after_count = len(re.findall(before_after_pattern, llm_response, re.IGNORECASE))

    if before_after_count < 8:  # 4 examples x 2 (antes+depois)
        gap = (8 - before_after_count) / 2
        score -= (gap / 4) * 2.0  # -2.0 max
        issues.append(f"Not enough before/after: ~{before_after_count/2:.0f} examples (need 4+)")
    else:
        issues.append(f"✅ Good before/after examples: ~{before_after_count/2:.0f}")

    # 6. THEORETICAL CONNECTION
    theory_keywords = ['mckee', 'dialogue', 'subtexto', 'subtext', 'p.\\d+']
    theory_count = sum(1 for kw in theory_keywords if re.search(kw, llm_response.lower()))

    if theory_count < 3:
        score -= 1.0
        issues.append(f"Weak theoretical connection (found {theory_count}/5 keywords)")
    else:
        issues.append(f"✅ Good theoretical connection")

    # 7. DEPTH INDICATORS
    depth_indicators = [
        'porque', 'portanto', 'exemplo', 'especificamente',
        'notamos que', 'sugere que', 'recomend'
    ]
    depth_count = sum(
        llm_response.lower().count(indicator)
        for indicator in depth_indicators
    )

    if depth_count < 15:
        gap = 15 - depth_count
        score -= (gap / 15) * 1.0  # -1.0 max
        issues.append(f"Not enough depth: {depth_count} indicators (need 15+)")
    else:
        issues.append(f"✅ Good depth: {depth_count} indicators")

    # Clamp score to 0-10
    score = max(0.0, min(10.0, score))

    return {
        'score': score,
        'char_count': char_count,
        'word_count': word_count,
        'quote_count': quote_count,
        'scene_count': scene_count,
        'page_count': page_count,
        'before_after_count': before_after_count // 2,
        'depth_count': depth_count,
        'issues': issues
    }


def main():
    """Executa teste de melhoria."""

    print('='*80)
    print('🧪 TEST: MCKEE_DIALOGUE 8/10 → 10/10')
    print('='*80)
    print()

    # 1. SETUP
    screenplay_path = Path('/Users/clubproducoes/Digimundo/scripturemon/inputs/examples/Te Encontro em Mim .pdf')
    patterns_path = Path('/Users/clubproducoes/Digimundo/claude_code/benchmark_patterns.json')
    output_dir = Path('/Users/clubproducoes/Digimundo/claude_code/test_results')
    output_dir.mkdir(exist_ok=True)

    if not screenplay_path.exists():
        print(f'❌ Roteiro não encontrado: {screenplay_path}')
        return

    # 2. READ SCREENPLAY
    print('📖 Lendo roteiro...')
    excerpt = read_screenplay(screenplay_path, max_words=1000)
    print(f'   ✅ {len(excerpt.split())} palavras extraídas')
    print()

    # 3. GENERATE ENHANCED PROMPT
    print('🎯 Gerando prompt melhorado (visando 10/10)...')
    generator = BenchmarkPromptGenerator(patterns_path)

    base_prompt = """
Analyze this screenplay excerpt focusing on dialogue quality, authenticity,
character voice differentiation, subtext, and conflict embedded in dialogue.

Identify specific problems citing scenes, pages, and dialogue verbatim.
Provide complete before/after scene rewrites showing technical improvements.
"""

    enhanced_prompt = generator.generate_10_10_prompt(
        author_type='mckee_dialogue',
        base_prompt=base_prompt,
        screenplay_excerpt=excerpt
    )

    print(f'   ✅ Prompt gerado: {len(enhanced_prompt):,} chars')
    print()

    # Save prompt for inspection
    prompt_file = output_dir / 'enhanced_prompt_mckee.txt'
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_prompt)
    print(f'   💾 Prompt salvo: {prompt_file.name}')
    print()

    # 4. CALL LLM
    print('='*80)
    print('🤖 EXECUTANDO ANÁLISE MELHORADA (SEM TIMEOUT)')
    print('='*80)
    print()
    print('⚠️  Isso pode levar 10-30 minutos para gerar análise 10/10')
    print()

    start = time.time()

    try:
        llm_response = call_ollama_llm(
            prompt=enhanced_prompt,
            model='scripturemon-optimized',
            timeout=None  # NO TIMEOUT!
        )
        elapsed = time.time() - start

        print()
        print(f'✅ LLM completou em {elapsed:.1f}s ({elapsed/60:.1f} min)')
        print(f'📏 Output: {len(llm_response):,} chars, {len(llm_response.split()):,} palavras')
        print()

        # 5. VALIDATE QUALITY
        print('='*80)
        print('📊 VALIDANDO QUALIDADE')
        print('='*80)
        print()

        validation = validate_10_10_quality(llm_response)

        print(f'🎯 SCORE: {validation["score"]:.1f}/10')
        print()
        print('Detalhes:')
        print(f'   Chars: {validation["char_count"]:,}')
        print(f'   Words: {validation["word_count"]:,}')
        print(f'   Quotes: {validation["quote_count"]}')
        print(f'   Scenes: {validation["scene_count"]}')
        print(f'   Pages: {validation["page_count"]}')
        print(f'   Before/After: ~{validation["before_after_count"]}')
        print(f'   Depth: {validation["depth_count"]} indicators')
        print()

        print('Issues/Observations:')
        for issue in validation['issues']:
            print(f'   {issue}')
        print()

        # 6. SAVE RESULTS
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f'MCKEE_IMPROVED_{timestamp}.txt'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('='*80 + '\n')
            f.write('MCKEE_DIALOGUE - IMPROVED ANALYSIS (TARGETING 10/10)\n')
            f.write('='*80 + '\n')
            f.write(f'\nGenerated: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
            f.write(f'Duration: {elapsed:.1f}s ({elapsed/60:.1f} min)\n')
            f.write(f'Score: {validation["score"]:.1f}/10\n')
            f.write(f'Chars: {validation["char_count"]:,}\n')
            f.write(f'Words: {validation["word_count"]:,}\n')
            f.write('\n' + '='*80 + '\n')
            f.write('ANALYSIS:\n')
            f.write('='*80 + '\n\n')
            f.write(llm_response)

        print(f'💾 Resultado salvo: {output_file.name}')
        print()

        # 7. COMPARISON
        print('='*80)
        print('📊 COMPARISON - OLD vs NEW')
        print('='*80)
        print()

        print('MCKEE_DIALOGUE OLD (8/10):')
        print('   Chars: 3,536')
        print('   Words: 530')
        print('   Quotes: 7')
        print('   Scenes: 3')
        print('   Pages: 1')
        print('   Before/After: 2')
        print()

        print('MCKEE_DIALOGUE NEW (?/10):')
        print(f'   Chars: {validation["char_count"]:,}')
        print(f'   Words: {validation["word_count"]:,}')
        print(f'   Quotes: {validation["quote_count"]}')
        print(f'   Scenes: {validation["scene_count"]}')
        print(f'   Pages: {validation["page_count"]}')
        print(f'   Before/After: ~{validation["before_after_count"]}')
        print()

        improvement = validation['score'] - 8.0
        print(f'IMPROVEMENT: {improvement:+.1f} points')
        print()

        if validation['score'] >= 9.5:
            print('🎉 SUCCESS! Alcançou 10/10 (ou muito próximo)')
        elif validation['score'] >= 9.0:
            print('✅ Muito bom! Quase 10/10')
        elif validation['score'] >= 8.5:
            print('👍 Melhorou, mas pode melhorar mais')
        else:
            print('⚠️  Ainda abaixo de 9/10, precisa ajustes')

        print()
        print('='*80)
        print('✅ TESTE COMPLETO')
        print('='*80)

    except Exception as e:
        print(f'❌ ERRO: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
