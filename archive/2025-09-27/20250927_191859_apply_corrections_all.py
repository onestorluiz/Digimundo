#!/usr/bin/env python3
"""
🔴 APLICAR CORREÇÕES EM TODOS OS MODELFILES
Corrige TODOS os 104 modelfiles para não criar conteúdo fictício
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Diretório dos modelfiles
MODELFILES_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/config/modelfiles")

# Instrução crítica para adicionar
CRITICAL_INSTRUCTION = """

==== IDENTITY & ROLE ====
You are a SCREENPLAY ANALYST specializing in this specific aspect.
You are NOT a screenwriter. You are a CRITIC and ANALYST.
Your job is to ANALYZE what exists in the screenplay provided by the user.

==== CRITICAL ANALYSIS INSTRUCTION ====
=====================================
ANALYZE the ACTUAL SCREENPLAY provided by the user.
Your role is to ANALYZE, CRITIQUE, and EVALUATE what exists.

DO NOT:
- Create fictional scenes or examples
- Invent character names or dialogue
- Write new screenplay content (like "INT." or "EXT.")
- Generate hypothetical scenarios
- Create "Scene 27" or any numbered scenes
- Invent characters like "Dr. Souza"
- Create hospital scenes
- Write dialogue for non-existent characters

DO:
- Analyze ONLY what is written in the screenplay
- Reference specific page numbers and existing dialogue
- Quote actual lines from the provided text
- Identify patterns in the actual content
- Provide insights based on what IS there, not what COULD be there

If you find yourself writing "INT." or "EXT." or character names in CAPS
followed by dialogue, STOP immediately - you are creating, not analyzing.

Remember: You are a CRITIC analyzing the screenplay, not a WRITER creating content.
=====================================
"""

def fix_all_modelfiles():
    """Corrige TODOS os modelfiles"""

    print("=" * 60)
    print("🔧 CORREÇÃO TOTAL DOS MODELFILES")
    print("=" * 60)
    print()

    # Listar todos os modelfiles
    modelfiles = list(MODELFILES_DIR.glob("*.modelfile"))
    print(f"📁 Encontrados {len(modelfiles)} modelfiles para corrigir")
    print()

    # Criar backup geral
    backup_dir = MODELFILES_DIR / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)

    fixed = 0
    for mf in modelfiles:
        print(f"📝 Processando: {mf.name}")

        # Backup
        backup_path = backup_dir / mf.name
        with open(mf, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)

        # Ler conteúdo
        content = original

        # 1. Ajustar temperatura para 0.35
        content = re.sub(r'PARAMETER temperature \d+\.\d+', 'PARAMETER temperature 0.35', content)

        # 2. Verificar se já tem a instrução crítica completa
        if "CRITICAL ANALYSIS INSTRUCTION" not in content or "Dr. Souza" not in content:
            # Procurar onde adicionar (antes do fechamento do SYSTEM)
            if '"""' in content:
                # Encontrar o último """
                system_end = content.rfind('"""')
                if system_end > 0:
                    # Inserir antes do fechamento
                    content = content[:system_end] + CRITICAL_INSTRUCTION + '\n"""' + content[system_end+3:]

        # 3. Salvar correções
        with open(mf, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   ✅ Corrigido")
        fixed += 1

    print()
    print("=" * 60)
    print(f"✅ CORREÇÃO COMPLETA!")
    print(f"   • {fixed} modelfiles corrigidos")
    print(f"   • Temperature: 0.35")
    print(f"   • Identidade: ANALYST")
    print(f"   • Instrução: DO NOT CREATE")
    print(f"   • Backup em: {backup_dir}")
    print("=" * 60)
    print()
    print("🎯 PRÓXIMOS PASSOS:")
    print("   1. Recriar todos os modelos no Ollama")
    print("   2. Testar com roteiro pequeno")
    print("   3. Executar análise completa")
    print()
    print("DIGIMUNDO PRESENTE 🔥")

if __name__ == "__main__":
    fix_all_modelfiles()