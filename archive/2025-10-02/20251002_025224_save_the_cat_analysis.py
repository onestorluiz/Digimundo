#!/usr/bin/env python3
"""
Análise Save the Cat: Sonhos sem Lembranças
Aplica a metodologia Blake Snyder no roteiro
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
Analyze this screenplay using ONLY Save the Cat methodology. Structure your analysis in these sections:

1. LOGLINE & HIGH CONCEPT
- Write a Save the Cat logline (adjective + noun + verb + goal)
- Does it pass the irony test?
- Is it primal?
- Does it create a compelling poster?

2. GENRE (Save the Cat 10 Genres)
- Which of the 10 STC genres does this fit?
- Monster in the House / Golden Fleece / Out of the Bottle / Dude with a Problem / Rites of Passage / Buddy Love / Whydunit / The Fool Triumphant / Institutionalized / Superhero
- Does the screenplay follow the genre rules?

3. THE 15 BEAT SHEET (Blake Snyder BS2)
Identify EACH beat with specific scene references:
- Opening Image (page 1)
- Theme Stated (page 5)
- Set-Up (pages 1-10)
- Catalyst (page 12)
- Debate (pages 12-25)
- Break into Two (page 25)
- B Story (page 30)
- Fun and Games (pages 30-55)
- Midpoint (page 55)
- Bad Guys Close In (pages 55-75)
- All Is Lost (page 75)
- Dark Night of the Soul (pages 75-85)
- Break into Three (page 85)
- Finale (pages 85-110)
- Final Image (page 110)

4. SAVE THE CAT MOMENT
- Does the hero have a "Save the Cat" moment?
- Where is it? (scene reference)
- Does it make us like the hero?

5. PROBLEMS (Save the Cat Physics)
Identify violations of STC rules:
- Missing beats?
- Wrong genre choice?
- Pope in the Pool issues (too much exposition)?
- Double Mumbo Jumbo (two magical elements)?
- Glacier moments (slow pacing)?
- Limp and eye patch (redundant character traits)?

6. SOLUTIONS (Beat-by-Beat Fixes)
For each problem, provide:
- Specific beat that needs fixing
- Exact scene reference
- Concrete rewrite suggestion following STC methodology

Be SPECIFIC. Reference exact scenes, page numbers, character names, and dialogue.
This is NOT a generic analysis - prove you read BOTH the book and the screenplay.

BEGIN YOUR ANALYSIS:"""

    return prompt

def main():
    print("\n" + "="*80)
    print("📖 ANÁLISE SAVE THE CAT: Sonhos sem Lembranças")
    print("="*80)

    # Carregar materiais
    print("\n📚 Carregando materiais...")
    screenplay = load_screenplay()
    book = load_save_the_cat_book()

    print(f"   ✅ Roteiro: {len(screenplay.split())} palavras")
    print(f"   ✅ Save the Cat: {len(book.split())} palavras")
    print(f"   📊 Total context: ~{(len(screenplay) + len(book)) // 1000}k chars")

    # Criar prompt
    print("\n🎯 Criando prompt de análise...")
    prompt = create_prompt(screenplay, book)
    print(f"   ✅ Prompt criado: {len(prompt.split())} palavras")

    # Executar análise
    print("\n🔥 Executando análise Save the Cat...")
    print("   Modelo: save-the-cat-doctor")
    print("   Context: 131k tokens")
    print("   Metodologia: Blake Snyder 15 Beat Sheet")

    start = time.time()

    try:
        response = ollama.generate(
            model='save-the-cat-doctor',
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 8192,  # Max output
            }
        )

        elapsed = time.time() - start
        analysis = response['response']

        # Resultados
        print(f"\n{'='*80}")
        print("📊 RESULTADOS")
        print(f"{'='*80}")

        print(f"\n⏱️  Tempo: {elapsed:.1f}s ({elapsed/60:.1f}min)")
        print(f"📏 Output: {len(analysis)} chars")
        print(f"📝 Output: {len(analysis.split())} palavras")

        # Preview
        print(f"\n📖 ANÁLISE SAVE THE CAT:")
        print("="*80)
        print(analysis)
        print("="*80)

        # Salvar
        output_data = {
            'timestamp': time.time(),
            'screenplay': 'Sonhos sem Lembranças',
            'methodology': 'Save the Cat (Blake Snyder)',
            'model': 'save-the-cat-doctor',
            'elapsed': elapsed,
            'analysis': analysis,
            'analysis_length': len(analysis),
            'analysis_words': len(analysis.split()),
            'book_used': 'Save the Cat (61,438 words)',
            'screenplay_length': len(screenplay.split())
        }

        output_file = Path("/Users/clubproducoes/Digimundo/scripturemon-clean/results/save_the_cat_analysis.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Análise salva em: {output_file}")

        # Análise de qualidade
        print(f"\n🔍 ANÁLISE DE QUALIDADE:")

        has_logline = 'LOGLINE' in analysis.upper()
        has_genre = 'GENRE' in analysis.upper()
        has_beat_sheet = 'BEAT' in analysis.upper() or 'BS2' in analysis.upper()
        has_save_cat = 'SAVE THE CAT' in analysis.upper()
        has_problems = 'PROBLEM' in analysis.upper()
        has_solutions = 'SOLUTION' in analysis.upper()

        score = sum([has_logline, has_genre, has_beat_sheet, has_save_cat, has_problems, has_solutions])

        print(f"   {'✅' if has_logline else '❌'} Logline & High Concept")
        print(f"   {'✅' if has_genre else '❌'} Genre Classification")
        print(f"   {'✅' if has_beat_sheet else '❌'} 15 Beat Sheet")
        print(f"   {'✅' if has_save_cat else '❌'} Save the Cat Moment")
        print(f"   {'✅' if has_problems else '❌'} Problems Identified")
        print(f"   {'✅' if has_solutions else '❌'} Solutions Provided")

        print(f"\n   📊 Completude: {score}/6")

        if score >= 5:
            print(f"\n   ✅ ANÁLISE COMPLETA E ABRANGENTE")
        elif score >= 3:
            print(f"\n   ⚠️  ANÁLISE PARCIAL - faltam elementos")
        else:
            print(f"\n   ❌ ANÁLISE INCOMPLETA")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n{'='*80}")
    print("✅ ANÁLISE SAVE THE CAT COMPLETA!")
    print("="*80)

if __name__ == "__main__":
    main()
