#!/usr/bin/env python3
"""
Comparação: Save the Cat Analysis
Modelo Save-the-Cat-Doctor vs Scripturemon-Ultimate
"""

import sys
import json
import time
from pathlib import Path
import ollama

def load_screenplay():
    """Carrega o roteiro"""
    screenplay_path = Path("/Users/clubproducoes/Digimundo/scripturemon-clean/content/screenplays/personal/sonhos_sem_lembrancas_t3.txt")
    return screenplay_path.read_text(encoding='utf-8', errors='ignore')

def load_save_the_cat_book():
    """Carrega o livro Save the Cat"""
    book_path = Path("/Users/clubproducoes/Digimundo/scripturemon-clean/content/theory/save_the_cat.txt")
    return book_path.read_text(encoding='utf-8', errors='ignore')

def create_prompt(screenplay, book):
    """Cria o prompt de análise"""

    prompt = f"""You are analyzing the screenplay "Sonhos sem Lembranças" using Blake Snyder's Save the Cat methodology.

SAVE THE CAT BOOK (61,438 words):
{book}

SCREENPLAY TO ANALYZE:
{screenplay}

YOUR TASK:
Analyze this screenplay using ONLY Save the Cat methodology. Be EXTREMELY SPECIFIC and reference exact scenes, page numbers, character names, and dialogue from the screenplay.

Structure your analysis in these sections:

1. LOGLINE & HIGH CONCEPT
- Write a Save the Cat logline (adjective + noun + verb + goal)
- Does it pass the irony test?
- Is it primal?
- Does it create a compelling poster?

2. GENRE (Save the Cat 10 Genres)
- Which of the 10 STC genres does this fit?
- Does the screenplay follow the genre rules?

3. THE 15 BEAT SHEET (Blake Snyder BS2)
Identify EACH beat with SPECIFIC scene references from the screenplay:
- Opening Image (page 1) - WHICH EXACT SCENE?
- Theme Stated (page 5) - WHO SAYS WHAT?
- Set-Up (pages 1-10) - LIST SPECIFIC SCENES
- Catalyst (page 12) - WHAT HAPPENS EXACTLY?
- Debate (pages 12-25) - SPECIFIC SCENES
- Break into Two (page 25) - EXACT MOMENT
- B Story (page 30) - WHO AND WHAT?
- Fun and Games (pages 30-55) - LIST SCENES
- Midpoint (page 55) - EXACT SCENE
- Bad Guys Close In (pages 55-75) - SPECIFIC EXAMPLES
- All Is Lost (page 75) - WHAT IS THE MOMENT?
- Dark Night of the Soul (pages 75-85) - WHICH SCENE?
- Break into Three (page 85) - EXACT DECISION
- Finale (pages 85-110) - HOW DOES IT RESOLVE?
- Final Image (page 110) - EXACT FINAL SCENE

4. SAVE THE CAT MOMENT
- Does the hero have a "Save the Cat" moment?
- WHICH EXACT SCENE NUMBER?
- QUOTE THE DIALOGUE OR DESCRIBE THE ACTION

5. PROBLEMS (Save the Cat Physics)
- Missing beats? WHICH ONES SPECIFICALLY?
- Pope in the Pool issues? WHICH SCENES?
- Glacier moments? WHICH PAGES?

6. SOLUTIONS (Beat-by-Beat Fixes)
- EXACT SCENE NUMBER that needs fixing
- QUOTE the current line/action
- PROVIDE the rewrite

BE SPECIFIC WITH SCENE NUMBERS, CHARACTER NAMES, AND EXACT MOMENTS. NO GENERIC ANALYSIS.

BEGIN YOUR ANALYSIS:"""

    return prompt

def analyze_with_model(model_name, screenplay, book):
    """Executa análise com um modelo específico"""

    print(f"\n{'='*80}")
    print(f"🔥 TESTANDO MODELO: {model_name}")
    print(f"{'='*80}")

    prompt = create_prompt(screenplay, book)

    start = time.time()

    try:
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 8192,
            }
        )

        elapsed = time.time() - start
        analysis = response['response']

        print(f"\n⏱️  Tempo: {elapsed:.1f}s ({elapsed/60:.1f}min)")
        print(f"📏 Output: {len(analysis)} chars ({len(analysis.split())} palavras)")

        # Contar especificidade
        import re
        scene_refs = len(re.findall(r'\bscene\s+\d+|\bcena\s+\d+', analysis, re.IGNORECASE))
        character_mentions = sum([
            analysis.lower().count('samantha'),
            analysis.lower().count('alberto'),
            analysis.lower().count('kleber'),
            analysis.lower().count('yasmim')
        ])
        dialogue_quotes = len(re.findall(r'["""]([^"""]{10,})["""]', analysis))

        print(f"\n📍 Especificidade:")
        print(f"   Scene references: {scene_refs}")
        print(f"   Character mentions: {character_mentions}")
        print(f"   Dialogue quotes: {dialogue_quotes}")

        return {
            'model': model_name,
            'elapsed': elapsed,
            'analysis': analysis,
            'length': len(analysis),
            'words': len(analysis.split()),
            'scene_refs': scene_refs,
            'character_mentions': character_mentions,
            'dialogue_quotes': dialogue_quotes
        }

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return None

def main():
    print("\n" + "="*80)
    print("📊 COMPARAÇÃO: Save the Cat Analysis")
    print("   save-the-cat-doctor vs scripturemon-ultimate")
    print("="*80)

    # Carregar materiais
    print("\n📚 Carregando materiais...")
    screenplay = load_screenplay()
    book = load_save_the_cat_book()

    print(f"   ✅ Roteiro: {len(screenplay.split())} palavras")
    print(f"   ✅ Save the Cat: {len(book.split())} palavras")

    # Testar modelos
    results = {}

    # Modelo 1: scripturemon-ultimate (128k context)
    result1 = analyze_with_model('scripturemon-ultimate', screenplay, book)
    if result1:
        results['scripturemon-ultimate'] = result1

    # Modelo 2: save-the-cat-doctor (especializado)
    result2 = analyze_with_model('save-the-cat-doctor', screenplay, book)
    if result2:
        results['save-the-cat-doctor'] = result2

    # Comparação
    print(f"\n{'='*80}")
    print("📊 COMPARAÇÃO FINAL")
    print(f"{'='*80}\n")

    print(f"{'Modelo':<30} {'Tempo':<12} {'Output':<12} {'Scenes':<10} {'Chars':<10} {'Quotes':<10}")
    print("-" * 80)

    for model, data in results.items():
        print(f"{model:<30} {data['elapsed']:>8.1f}s   {data['words']:>6} words  "
              f"{data['scene_refs']:>6}     {data['character_mentions']:>6}     {data['dialogue_quotes']:>6}")

    # Determinar vencedor
    if len(results) == 2:
        models = list(results.keys())
        r1 = results[models[0]]
        r2 = results[models[1]]

        print(f"\n{'='*80}")
        print("🏆 VENCEDOR")
        print(f"{'='*80}\n")

        # Critérios
        faster = models[0] if r1['elapsed'] < r2['elapsed'] else models[1]
        more_output = models[0] if r1['words'] > r2['words'] else models[1]
        more_specific = models[0] if (r1['scene_refs'] + r1['dialogue_quotes']) > (r2['scene_refs'] + r2['dialogue_quotes']) else models[1]

        print(f"⚡ Mais rápido: {faster}")
        print(f"📏 Mais output: {more_output}")
        print(f"📍 Mais específico: {more_specific}")

        # Score
        score1 = sum([faster == models[0], more_output == models[0], more_specific == models[0]])
        score2 = sum([faster == models[1], more_output == models[1], more_specific == models[1]])

        winner = models[0] if score1 > score2 else models[1]
        print(f"\n🏆 MELHOR MODELO: {winner} ({max(score1, score2)}/3 critérios)")

    # Salvar
    output_file = Path("/Users/clubproducoes/Digimundo/scripturemon-clean/results/save_the_cat_comparison.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Comparação salva em: {output_file}")

    print(f"\n{'='*80}")
    print("✅ COMPARAÇÃO COMPLETA!")
    print("="*80)

if __name__ == "__main__":
    main()
