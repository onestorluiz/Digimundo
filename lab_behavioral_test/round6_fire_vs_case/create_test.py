#!/usr/bin/env python3
"""
TESTE 6: 🔥 SOZINHO vs CAPS vs lowercase
Objetivo: Descobrir se um emoji urgente sozinho bate texto em maiúsculo/minúsculo
"""

import os

# Criar arquivos de teste
files = {
    # Grupo 1: Apenas 🔥 sem palavras
    "🔥.md": "Arquivo só com fogo",
    "🔥.txt": "Outro arquivo só com fogo",
    "🔥.py": "Python só com fogo",

    # Grupo 2: Texto em CAPS sem emoji
    "README.md": "Readme em maiúsculo",
    "IMPORTANT.txt": "Importante em maiúsculo",
    "WARNING.md": "Aviso em maiúsculo",
    "CONFIG.json": "Config em maiúsculo",

    # Grupo 3: Texto em lowercase sem emoji
    "readme_lowercase.md": "Readme em minúsculo",
    "important_notes.txt": "Notas importantes minúsculo",
    "warning_message.md": "Mensagem de aviso minúsculo",
    "config_file.json": "Arquivo de configuração minúsculo",

    # Grupo 4: Controle - arquivos normais mistos
    "Normal_File.txt": "Arquivo com capitalização normal",
    "another_one.md": "Outro arquivo normal",
    "Setup.py": "Setup com primeira maiúscula"
}

# Criar os arquivos
for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {filename}\n\n{content}\n")
    print(f"✓ Created: {filename}")

print(f"\n✅ Created {len(files)} test files")
print("\n📊 GROUPS:")
print("  1. Only 🔥 emoji without words (3 files)")
print("  2. CAPS text without emoji (4 files)")
print("  3. lowercase text without emoji (4 files)")
print("  4. Control - mixed case (3 files)")