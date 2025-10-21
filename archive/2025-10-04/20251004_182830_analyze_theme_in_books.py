#!/usr/bin/env python3
"""
Análise genérica de QUALQUER TEMA nos 13 livros de teoria
Permite enriquecer specialist_types com múltiplos livros
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

THEORY_DIR = Path('content/theory')

# Todos os 13 livros
BOOKS = {
    'mckee_story': 'st_o_r_y.txt',
    'mckee_character': 'Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt',
    'mckee_dialogue': 'Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt',
    'truby': 'the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt',
    'campbell': 'o-heroi-de-mil-faces-_alta-qualidade_atbc_-jonathan-c_-young_-joseph-campbell-paperback_-1995-cult.docx.txt',
    'vogler': 'the_writers_journey_mythic_structure_for_writers_2nd.txt',
    'seger': 'making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt',
    'field': 'screenplay_the_foundations_of_screenwriting_-_syd_field.txt',
    'snyder': 'save_the_cat.txt',
    'egri': 'the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt',
    'weiland': 'creating_character_arcs_the_masterful_author_s_guide.txt',
    'aristotle': 'ontology_and_the_art_of_tragedy_an_approach_to_aristotle_s.txt',
    'cowgill': 'writing_short_films_structure_and_content_for_screenwriters_--_linda_j_cowgill.txt'
}

# Temas e seus padrões de busca
THEMES = {
    'character': {
        'patterns': [
            r'\bcharacter[s]?\b', r'\bpersonage[m|ns]?\b', r'\bprotagonist\b',
            r'\bantagonist\b', r'\barc[s]?\b', r'\btransformation\b',
            r'\bmotivation\b', r'\bdesire\b', r'\bflaw[s]?\b', r'\bbackstory\b'
        ]
    },
    'structure': {
        'patterns': [
            r'\bstructure\b', r'\bestrutura\b', r'\bplot\b', r'\btrama\b',
            r'\bact[s]?\b', r'\bato[s]?\b', r'\bthree-act\b', r'\bturning point\b',
            r'\bmidpoint\b', r'\bclimax\b', r'\bresolution\b'
        ]
    },
    'theme': {
        'patterns': [
            r'\btheme[s]?\b', r'\btema[s]?\b', r'\bmeaning\b', r'\bsignificado\b',
            r'\bmessage\b', r'\bmensagem\b', r'\bcontrolling idea\b',
            r'\bmoral\b', r'\bphilosoph\w+\b'
        ]
    },
    'conflict': {
        'patterns': [
            r'\bconflict[s]?\b', r'\bconflito[s]?\b', r'\btension\b', r'\btensão\b',
            r'\bopposition\b', r'\bobstacle[s]?\b', r'\bobstáculo[s]?\b',
            r'\bantagonism\b', r'\bstruggle\b'
        ]
    },
    'scene': {
        'patterns': [
            r'\bscene[s]?\b', r'\bcena[s]?\b', r'\bsequence[s]?\b', r'\bsequência[s]?\b',
            r'\bbeat[s]?\b', r'\bmoment[s]?\b', r'\baction unit[s]?\b'
        ]
    }
}

def analyze_book_for_theme(book_path: Path, author_key: str, theme: str, patterns: list):
    """Analisa um livro em busca de conteúdo sobre um tema."""

    if not book_path.exists():
        return None

    # Tentar múltiplos encodings
    content = None
    for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
        try:
            with open(book_path, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        return None

    # Estatísticas básicas
    total_words = len(content.split())

    # Buscar menções do tema
    theme_mentions = 0
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        theme_mentions += sum(1 for _ in matches)

    # Densidade do tema (menções por 1000 palavras)
    theme_density = (theme_mentions / total_words) * 1000 if total_words > 0 else 0

    return {
        'author_key': author_key,
        'book_name': book_path.name[:60],
        'total_words': total_words,
        'theme_mentions': theme_mentions,
        'theme_density': theme_density,
        'relevance_score': min(100, theme_density * 10)
    }

def analyze_theme(theme_name: str):
    """Analisa um tema específico em todos os livros."""

    if theme_name not in THEMES:
        print(f'❌ Tema "{theme_name}" não encontrado!')
        print(f'   Temas disponíveis: {", ".join(THEMES.keys())}')
        return

    theme_info = THEMES[theme_name]
    patterns = theme_info['patterns']

    print('='*80)
    print(f'🎭 ANÁLISE PROFUNDA: {theme_name.upper()} NOS 13 LIVROS DE TEORIA')
    print('='*80)
    print()

    results = []

    for author_key, book_file in BOOKS.items():
        book_path = THEORY_DIR / book_file

        print(f'📖 Analisando {author_key.upper()}...')

        result = analyze_book_for_theme(book_path, author_key, theme_name, patterns)

        if result:
            results.append(result)
            print(f'   ✅ {result["theme_mentions"]:,} menções')
            print(f'   📊 Densidade: {result["theme_density"]:.2f}/1000 palavras')
            print(f'   🎯 Score: {result["relevance_score"]:.1f}/100')
        else:
            print(f'   ❌ Arquivo não encontrado')

        print()

    # Ordenar por relevância
    results.sort(key=lambda x: x['relevance_score'], reverse=True)

    print('='*80)
    print(f'📊 RANKING DE RELEVÂNCIA PARA {theme_name.upper()}')
    print('='*80)
    print()

    print('Rank | Autor                | Menções | Densidade | Score | Palavras')
    print('-'*80)

    for i, result in enumerate(results, 1):
        author = result['author_key'].ljust(20)
        mentions = f"{result['theme_mentions']:,}".rjust(7)
        density = f"{result['theme_density']:.1f}".rjust(9)
        score = f"{result['relevance_score']:.1f}".rjust(5)
        words = f"{result['total_words']:,}".rjust(9)

        print(f'{i:4} | {author} | {mentions} | {density} | {score} | {words}')

    print()
    print('='*80)
    print(f'🎯 RECOMENDAÇÕES PARA specialist_type="{theme_name}"')
    print('='*80)
    print()

    # Selecionar top livros (score > 20)
    top_books = [r for r in results if r['relevance_score'] > 20]

    print(f'📊 {len(top_books)} livros com conteúdo significativo sobre {theme_name}:')
    print()

    for result in top_books:
        print(f'   ✅ {result["author_key"]:20} (Score: {result["relevance_score"]:.1f})')

    print()
    print('💡 Sugestão de mapeamento enriquecido:')
    print()
    print(f"'{theme_name}': [")
    for result in top_books:
        book_file = BOOKS[result['author_key']]
        print(f'    "{book_file}",  # {result["author_key"]} (Score: {result["relevance_score"]:.1f})')
    print("],")

    print()
    print('='*80)
    print('✅ ANÁLISE COMPLETA!')
    print('='*80)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python3 analyze_theme_in_books.py <theme>')
        print()
        print('Temas disponíveis:')
        for theme in THEMES.keys():
            print(f'  - {theme}')
        sys.exit(1)

    theme = sys.argv[1].lower()
    analyze_theme(theme)
