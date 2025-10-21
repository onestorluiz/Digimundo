#!/usr/bin/env python3
"""
TESTE 5: URGÊNCIA TEXTUAL vs EMOJIS CALMOS
Objetivo: Descobrir o que priorizo mais - palavras urgentes ou emojis felizes
"""

import os

# Criar arquivos de teste
files = {
    # Grupo 1: Palavras urgentes SEM emoji
    "CRITICAL_URGENT_ERROR.md": "Arquivo crítico sem emoji",
    "EXTREME_BUG_BROKEN.txt": "Bug extremo sem emoji",
    "MUST_READ_IMMEDIATELY.md": "Deve ler imediatamente",
    "DANGER_WARNING_ALERT.py": "Alerta de perigo sem emoji",

    # Grupo 2: Emojis calmos/felizes com texto normal
    "😊_happy_file.md": "Arquivo feliz com emoji sorridente",
    "🌸_flower_document.txt": "Documento com flor",
    "💚_green_heart.md": "Coração verde",
    "🌈_rainbow_notes.txt": "Notas arco-íris",
    "✨_sparkles_info.md": "Informação com brilho",

    # Grupo 3: Emojis neutros com texto urgente
    "📝_CRITICAL_NOTES.md": "Notas críticas com emoji neutro",
    "📁_URGENT_FOLDER.txt": "Pasta urgente com emoji neutro",

    # Grupo 4: Controle - arquivos normais
    "readme.md": "Readme normal",
    "documentation.txt": "Documentação normal",
    "notes.md": "Notas normais"
}

# Criar os arquivos
for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {filename}\n\n{content}\n")
    print(f"✓ Created: {filename}")

print(f"\n✅ Created {len(files)} test files")
print("\n📊 GROUPS:")
print("  1. Urgent words WITHOUT emoji (4 files)")
print("  2. Calm/happy emojis with normal text (5 files)")
print("  3. Neutral emojis with urgent text (2 files)")
print("  4. Control - normal files (3 files)")