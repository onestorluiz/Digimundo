#!/usr/bin/env python3
"""
Análise completa dos mapeamentos de livros de teoria
Verifica se todos os 13 livros estão corretamente mapeados
"""

import os
from pathlib import Path

# Livros disponíveis
AVAILABLE_BOOKS = {
    'Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt': 'McKee (Character)',
    'creating_character_arcs_the_masterful_author_s_guide.txt': 'Weiland',
    'Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt': 'McKee (Dialogue)',
    'making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt': 'Seger',
    'o-heroi-de-mil-faces-_alta-qualidade_atbc_-jonathan-c_-young_-joseph-campbell-paperback_-1995-cult.docx.txt': 'Campbell',
    'ontology_and_the_art_of_tragedy_an_approach_to_aristotle_s.txt': 'Aristóteles',
    'save_the_cat.txt': 'Snyder',
    'screenplay_the_foundations_of_screenwriting_-_syd_field.txt': 'Field',
    'st_o_r_y.txt': 'McKee (Story)',
    'the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt': 'Truby',
    'the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt': 'Egri',
    'the_writers_journey_mythic_structure_for_writers_2nd.txt': 'Vogler',
    'writing_short_films_structure_and_content_for_screenwriters_--_linda_j_cowgill.txt': 'Cowgill'
}

# Mapeamento atual em book_mapping (theory_indexer.py lines 700-714)
BOOK_MAPPING = {
    'mckee': ["st_o_r_y.txt"],
    'mckee_story': ["st_o_r_y.txt"],
    'mckee_character': ["Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt"],
    'mckee_dialogue': ["Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"],
    'truby': ["the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt"],
    'campbell': ["o-heroi-de-mil-faces-_alta-qualidade_atbc_-jonathan-c_-young_-joseph-campbell-paperback_-1995-cult.docx.txt"],
    'vogler': ["the_writers_journey_mythic_structure_for_writers_2nd.txt"],
    'seger': ["making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt"],
    'field': ["screenplay_the_foundations_of_screenwriting_-_syd_field.txt"],
    'snyder': ["save_the_cat.txt"],
    'egri': ["the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt"],
    'weiland': ["creating_character_arcs_the_masterful_author_s_guide.txt"],
    'aristotle': ["ontology_and_the_art_of_tragedy_an_approach_to_aristotle_s.txt"],
    'cowgill': ["writing_short_films_structure_and_content_for_screenwriters_--_linda_j_cowgill.txt"],
}

# Mapeamento atual em SPECIALIST_BOOK_MAP (theory_indexer.py lines 547-561)
SPECIALIST_BOOK_MAP = {
    'mckee': 'st_o_r_y',
    'mckee_story': 'st_o_r_y',
    'mckee_character': 'Character-_-The-Art-of-Role',
    'mckee_dialogue': 'Dialogue-_-The-Art-of-Verbal',
    'truby': 'anatomy_of_story_22_steps',
    'campbell': 'heroi-de-mil-faces',
    'vogler': 'writers_journey_mythic',
    'seger': 'making-a-good-script-great',
    'field': 'screenplay_the_foundations',
    'snyder': 'save_the_cat',
    'egri': 'art_of_dramatic_writing',
    'weiland': 'creating_character_arcs',
    'aristotle': 'ontology_and_the_art',
    'cowgill': 'writing_short_films'
}

print('='*80)
print('📚 ANÁLISE DE MAPEAMENTO DE LIVROS DE TEORIA')
print('='*80)
print()

print(f'📖 Total de livros disponíveis: {len(AVAILABLE_BOOKS)}')
print(f'🔗 Total mapeados em book_mapping: {len(BOOK_MAPPING)}')
print(f'🔗 Total mapeados em SPECIALIST_BOOK_MAP: {len(SPECIALIST_BOOK_MAP)}')
print()

# Verificar quais livros estão mapeados
mapped_books = set()
for books_list in BOOK_MAPPING.values():
    mapped_books.update(books_list)

print('✅ LIVROS MAPEADOS:')
print('-' * 80)
for book, author in AVAILABLE_BOOKS.items():
    if book in mapped_books:
        print(f'   ✅ {author:20} → {book[:50]}...')
print()

print('❌ LIVROS NÃO MAPEADOS (FALTANDO):')
print('-' * 80)
unmapped = []
for book, author in AVAILABLE_BOOKS.items():
    if book not in mapped_books:
        print(f'   ❌ {author:20} → {book[:50]}...')
        unmapped.append((author, book))
print()

if unmapped:
    print('🔧 CORREÇÕES NECESSÁRIAS:')
    print('-' * 80)
    print()

    print('1. ADICIONAR AO book_mapping (theory_indexer.py ~linha 708):')
    print()
    for author, book in unmapped:
        author_key = author.lower().split()[0]  # Primeira palavra em minúscula
        print(f"    '{author_key}': [\"{book}\"],")
    print()

    print('2. ADICIONAR AO SPECIALIST_BOOK_MAP (theory_indexer.py ~linha 555):')
    print()
    for author, book in unmapped:
        author_key = author.lower().split()[0]
        # Criar pattern de busca simplificado
        pattern = book.replace('.txt', '').replace('.docx', '').split('--')[0].strip()
        pattern = pattern.split('_')[:3]  # Primeiras 3 palavras
        pattern = '_'.join(pattern)
        print(f"    '{author_key}': '{pattern}',")
    print()

print('='*80)
print('📊 RESUMO:')
print('='*80)
print(f'   ✅ Mapeados: {len(mapped_books)}/13')
print(f'   ❌ Faltando: {len(unmapped)}/13')
print()

if len(unmapped) == 0:
    print('   🎉 TODOS OS LIVROS ESTÃO MAPEADOS!')
else:
    print(f'   ⚠️  {len(unmapped)} livro(s) precisa(m) ser mapeado(s)')
print()
print('='*80)
