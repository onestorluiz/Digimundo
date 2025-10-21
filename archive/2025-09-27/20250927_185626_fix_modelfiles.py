#!/usr/bin/env python3
"""
🔴 SCRIPT DE CORREÇÃO CRÍTICA - SCRIPTUREMON ULTIMATE
Corrige o problema dos especialistas criando conteúdo fictício
Baseado no PLANO_CORRECAO_SCRIPTUREMON_ULTIMATE.md
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

def fix_modelfile(filepath):
    """Corrige um modelfile individual"""
    print(f"📝 Processando: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ajustar temperatura para 0.35
    content = re.sub(r'PARAMETER temperature \d+\.\d+', 'PARAMETER temperature 0.35', content)

    # 2. Verificar se já tem a instrução crítica
    if "CRITICAL ANALYSIS INSTRUCTION" not in content:
        # Encontrar onde termina o SYSTEM
        system_end = content.rfind('"""')
        if system_end > 0:
            # Inserir antes do fechamento
            content = content[:system_end] + CRITICAL_INSTRUCTION + '\n"""' + content[system_end+3:]

    # 3. Salvar backup
    backup_path = filepath.with_suffix('.backup')
    if not backup_path.exists():
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(open(filepath, 'r').read())

    # 4. Salvar correções
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"   ✅ Corrigido: Temperature=0.35, Identidade=ANALYST")
    return True

def validate_modelfile(filepath):
    """Valida se um modelfile foi corrigido"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        "Temperature 0.35": "temperature 0.35" in content,
        "Identity ANALYST": "You are a SCREENPLAY ANALYST" in content,
        "Critical Instruction": "CRITICAL ANALYSIS INSTRUCTION" in content,
        "DO NOT create": "DO NOT:" in content and "Create fictional" in content
    }

    all_ok = all(checks.values())

    if not all_ok:
        print(f"   ⚠️ {filepath.name} - Falhas:")
        for check, status in checks.items():
            if not status:
                print(f"      ❌ {check}")

    return all_ok

def main():
    print("=" * 60)
    print("🔧 CORREÇÃO DOS MODELFILES - SCRIPTUREMON ULTIMATE")
    print("=" * 60)
    print()
    print("📋 PROBLEMA: Especialistas criando conteúdo fictício")
    print("🎯 SOLUÇÃO: Temperature 0.35 + Identidade ANALYST")
    print()

    # Listar modelfiles
    modelfiles = list(MODELFILES_DIR.glob("*.modelfile"))
    print(f"📁 Encontrados {len(modelfiles)} modelfiles para corrigir")
    print()

    # Backup geral
    backup_dir = MODELFILES_DIR / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)

    print("💾 Criando backup completo...")
    for mf in modelfiles:
        backup_path = backup_dir / mf.name
        with open(backup_path, 'w') as f:
            f.write(open(mf, 'r').read())
    print(f"   ✅ Backup em: {backup_dir}")
    print()

    # Corrigir cada modelfile
    print("🔧 APLICANDO CORREÇÕES...")
    print("-" * 40)

    fixed = 0
    for mf in sorted(modelfiles):
        if fix_modelfile(mf):
            fixed += 1

    print("-" * 40)
    print(f"✅ {fixed}/{len(modelfiles)} modelfiles corrigidos")
    print()

    # Validar correções
    print("🔍 VALIDANDO CORREÇÕES...")
    print("-" * 40)

    valid = 0
    for mf in sorted(modelfiles):
        if validate_modelfile(mf):
            valid += 1

    print("-" * 40)
    print(f"✅ {valid}/{len(modelfiles)} modelfiles validados")
    print()

    # Relatório final
    print("=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    print(f"✅ Modelfiles corrigidos: {fixed}")
    print(f"✅ Modelfiles validados: {valid}")
    print(f"✅ Temperature ajustada: 0.35")
    print(f"✅ Identidade estabelecida: ANALYST")
    print(f"✅ Instrução crítica: DO NOT CREATE")
    print()
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Testar com roteiro pequeno")
    print("2. Verificar que não cria conteúdo fictício")
    print("3. Executar análise completa")
    print()
    print("DIGIMUNDO PRESENTE 🔥")

if __name__ == "__main__":
    main()