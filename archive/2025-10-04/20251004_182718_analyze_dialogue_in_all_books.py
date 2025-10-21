#!/usr/bin/env python3
"""
Análise profunda de DIÁLOGO nos 13 livros de teoria
Identifica seções, capítulos e insights sobre diálogo em cada livro
"""

import re
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

# Padrões relacionados a diálogo (múltiplos idiomas)
DIALOGUE_PATTERNS = [
    # Inglês
    r'\bdialogue\b', r'\bdialog\b', r'\bconversation\b', r'\bspeech\b',
    r'\bverbal\b', r'\bspoken\b', r'\btalking\b', r'\bspeaking\b',
    r'\bline[s]?\b', r'\bsubtext\b', r'\bwhat.*said\b', r'\bhow.*speak\b',

    # Português
    r'\bdiálogo[s]?\b', r'\bconversa[s]?\b', r'\bfala[s]?\b',
    r'\bpalavra[s]?\b', r'\bdiz\b', r'\bdizer\b', r'\bfalando\b',
    r'\bsubtexto\b', r'\bverbaliz\w+\b',

    # Termos técnicos
    r'\bon-the-nose\b', r'\bexposition\b', r'\brevelation\b',
    r'\bcharacter voice\b', r'\btone of voice\b'
]

def analyze_book_for_dialogue(book_path: Path, author_key: str):
    """Analisa um livro em busca de conteúdo sobre diálogo."""

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

    # Buscar menções de diálogo
    dialogue_mentions = 0
    contexts = []
    chapters_about_dialogue = []

    # Contar menções totais
    for pattern in DIALOGUE_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            dialogue_mentions += 1

            # Extrair contexto (100 chars antes e depois)
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].replace('\n', ' ')

            if len(contexts) < 5:  # Guardar só 5 exemplos
                contexts.append({
                    'pattern': pattern,
                    'context': context,
                    'position': match.start()
                })

    # Buscar capítulos sobre diálogo (patterns de título)
    chapter_patterns = [
        r'chapter\s+\d+[:\s]+.*dialogue.*',
        r'capítulo\s+\d+[:\s]+.*diálogo.*',
        r'section[:\s]+.*dialogue.*',
        r'part[:\s]+.*dialogue.*',
        r'\n\s*dialogue\s*\n',
        r'\n\s*diálogo\s*\n'
    ]

    for pattern in chapter_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            # Extrair título completo
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 100)
            chapter_title = content[start:end].strip()
            chapters_about_dialogue.append(chapter_title[:150])

    # Densidade de diálogo (menções por 1000 palavras)
    dialogue_density = (dialogue_mentions / total_words) * 1000 if total_words > 0 else 0

    return {
        'author_key': author_key,
        'book_name': book_path.name[:60],
        'total_words': total_words,
        'dialogue_mentions': dialogue_mentions,
        'dialogue_density': dialogue_density,
        'sample_contexts': contexts,
        'chapters': chapters_about_dialogue,
        'relevance_score': min(100, dialogue_density * 10)  # Score 0-100
    }

print('='*80)
print('🎭 ANÁLISE PROFUNDA: DIÁLOGO NOS 13 LIVROS DE TEORIA')
print('='*80)
print()

results = []

for author_key, book_file in BOOKS.items():
    book_path = THEORY_DIR / book_file

    print(f'📖 Analisando {author_key.upper()}...')

    result = analyze_book_for_dialogue(book_path, author_key)

    if result:
        results.append(result)
        print(f'   ✅ {result["dialogue_mentions"]:,} menções de diálogo')
        print(f'   📊 Densidade: {result["dialogue_density"]:.2f} menções/1000 palavras')
        print(f'   🎯 Score de relevância: {result["relevance_score"]:.1f}/100')

        if result['chapters']:
            print(f'   📚 {len(result["chapters"])} capítulo(s) sobre diálogo encontrado(s)')
    else:
        print(f'   ❌ Arquivo não encontrado')

    print()

# Ordenar por relevância
results.sort(key=lambda x: x['relevance_score'], reverse=True)

print('='*80)
print('📊 RANKING DE RELEVÂNCIA PARA DIÁLOGO')
print('='*80)
print()

print('Rank | Autor                | Menções | Densidade | Score | Palavras')
print('-'*80)

for i, result in enumerate(results, 1):
    author = result['author_key'].ljust(20)
    mentions = f"{result['dialogue_mentions']:,}".rjust(7)
    density = f"{result['dialogue_density']:.1f}".rjust(9)
    score = f"{result['relevance_score']:.1f}".rjust(5)
    words = f"{result['total_words']:,}".rjust(9)

    print(f'{i:4} | {author} | {mentions} | {density} | {score} | {words}')

print()
print('='*80)
print('📚 CAPÍTULOS/SEÇÕES SOBRE DIÁLOGO')
print('='*80)
print()

for result in results:
    if result['chapters']:
        print(f"\n{result['author_key'].upper()}:")
        for chapter in result['chapters'][:3]:  # Mostrar até 3
            print(f"   → {chapter}")

print()
print('='*80)
print('💡 EXEMPLOS DE CONTEXTO')
print('='*80)
print()

for result in results[:3]:  # Top 3 mais relevantes
    print(f"\n{result['author_key'].upper()} - Exemplo de contexto:")
    if result['sample_contexts']:
        context = result['sample_contexts'][0]['context']
        print(f"   \"{context}...\"")

print()
print('='*80)
print('🎯 RECOMENDAÇÕES PARA specialist_type="dialogue"')
print('='*80)
print()

# Selecionar top livros para diálogo
top_dialogue_books = [r for r in results if r['relevance_score'] > 20]

print(f'📊 {len(top_dialogue_books)} livros com conteúdo significativo sobre diálogo:')
print()

for result in top_dialogue_books:
    print(f'   ✅ {result["author_key"]:20} (Score: {result["relevance_score"]:.1f})')

print()
print('💡 Sugestão de mapeamento enriquecido:')
print()
print("book_mapping = {")
print("    'dialogue': [")
for result in top_dialogue_books:
    book_file = BOOKS[result['author_key']]
    print(f'        "{book_file}",  # {result["author_key"]} (Score: {result["relevance_score"]:.1f})')
print("    ],")
print("}")

print()
print('='*80)
print('✅ ANÁLISE COMPLETA!')
print('='*80)
