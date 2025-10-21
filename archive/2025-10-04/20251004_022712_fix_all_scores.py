#!/usr/bin/env python3
"""
Script automático para corrigir score calculation em todos os especialistas.
Padrão correto: score = 90.0, return max(5.0, min(95.0, score))
"""

import re
from pathlib import Path

# Lista de especialistas para corrigir
FIXES = [
    # Formato: (arquivo, linha_método, padrão_antigo_score, padrão_antigo_return)

    # Grupo 1: Ambos os problemas (start 100, cap 100) - base_score = 100
    ("triple_core/core_1_specialists/theme/dr_theme.py",
     "base_score = 100", "base_score = 90",
     "max(0, min(100, base_score))", "max(5, min(95, base_score))"),

    ("triple_core/core_1_specialists/tone/dr_tone.py",
     "base_score = 100", "base_score = 90",
     "max(0, min(100, base_score))", "max(5, min(95, base_score))"),

    ("triple_core/core_1_specialists/subtext/dr_subtext.py",
     "base_score = 100", "base_score = 90",
     "max(0, min(100, base_score))", "max(5, min(95, base_score))"),

    ("triple_core/core_1_specialists/symbolism/dr_symbolism.py",
     "base_score = 100", "base_score = 90",
     "max(0, min(100, base_score))", "max(5, min(95, base_score))"),

    ("triple_core/core_1_specialists/visual/dr_visual_motifs.py",
     "base_score = 100", "base_score = 90",
     "max(0, min(100, base_score))", "max(5, min(95, base_score))"),

    # Grupo 2: Ambos os problemas - score = 100.0
    ("triple_core/core_1_specialists/transitions/dr_transitions.py",
     "score = 100.0", "score = 90.0",
     "max(0, min(100, round(score, 1)))", "max(5.0, min(95.0, round(score, 1)))"),

    ("triple_core/core_1_specialists/opening/dr_opening.py",
     "score = 100.0", "score = 90.0",
     "max(0, min(100, round(score, 1)))", "max(5.0, min(95.0, round(score, 1)))"),

    ("triple_core/core_1_specialists/climax/dr_climax.py",
     "score = 100.0", "score = 90.0",
     "max(0, min(100, round(score, 1)))", "max(5.0, min(95.0, round(score, 1)))"),

    ("triple_core/core_1_specialists/resolution/dr_resolution.py",
     "score = 100.0", "score = 90.0",
     "max(0, min(100, round(score, 1)))", "max(5.0, min(95.0, round(score, 1)))"),

    ("triple_core/core_1_specialists/character/psychology/dr_psychology.py",
     "score = 100.0", "score = 90.0",
     "max(0, min(100, round(score, 1)))", "max(5.0, min(95.0, round(score, 1)))"),

    ("triple_core/core_1_specialists/character/arcs/dr_arcs.py",
     "score = 100.0", "score = 90.0",
     "max(0.0, min(100.0, score))", "max(5.0, min(95.0, score))"),

    ("triple_core/core_1_specialists/character/relationships/dr_relationships.py",
     "score = 100.0", "score = 90.0",
     "max(0.0, min(100.0, score))", "max(5.0, min(95.0, score))"),

    ("triple_core/core_1_specialists/pacing/dr_pacing.py",
     "score = 100.0", "score = 90.0",
     "max(0, min(100, round(score, 1)))", "max(5.0, min(95.0, round(score, 1)))"),

    # Grupo 3: score = 100 (sem .0)
    ("triple_core/core_1_specialists/genre/dr_genre.py",
     "score = 100", "score = 90",
     "max(0, min(100, score))", "max(5, min(95, score))"),

    # Grupo 4: Apenas cap (dynamic score)
    ("triple_core/core_1_specialists/originality/dr_originality.py",
     None, None,  # Não mexe no score inicial (é dinâmico)
     "max(0, min(100, score))", "max(5, min(95, score))"),

    ("triple_core/core_1_specialists/market/dr_market_potential.py",
     None, None,  # Não mexe no score inicial (é dinâmico)
     "max(10, min(100, score))", "max(10, min(95, score))"),  # Mantém min=10

    # Grupo 5: Já tem cap 95, só corrigir start
    ("triple_core/core_1_specialists/dialogue/dr_dialogue.py",
     "score = 85.0", "score = 90.0",
     None, None),  # Cap já está correto (95)

    ("triple_core/core_1_specialists/structure/dr_structure.py",
     "score = 100.0", "score = 90.0",
     "min(95.0, score)", "max(5.0, min(95.0, score))"),  # Adiciona max(5.0)
]

def fix_specialist(file_path: str, old_score: str, new_score: str,
                   old_return: str, new_return: str):
    """Corrige um especialista."""
    path = Path(file_path)
    if not path.exists():
        print(f"❌ {file_path} não encontrado")
        return False

    content = path.read_text()
    original = content

    # Corrigir score inicial (se especificado)
    if old_score and new_score:
        content = content.replace(old_score, new_score)
        if content == original:
            print(f"⚠️  {file_path}: Score '{old_score}' não encontrado")

    # Corrigir return (se especificado)
    if old_return and new_return:
        content = content.replace(old_return, new_return)
        if content == original and not (old_score and new_score):
            print(f"⚠️  {file_path}: Return '{old_return}' não encontrado")

    # Salvar se houve mudanças
    if content != original:
        path.write_text(content)
        print(f"✅ {path.name} corrigido")
        return True
    else:
        print(f"⚠️  {path.name} sem mudanças")
        return False

def main():
    print("🔧 CORREÇÃO EM MASSA - SCORE CALIBRATION")
    print("="*60)
    print()

    fixed = 0
    for fix in FIXES:
        file_path = fix[0]
        old_score = fix[1]
        new_score = fix[2]
        old_return = fix[3]
        new_return = fix[4]

        if fix_specialist(file_path, old_score, new_score, old_return, new_return):
            fixed += 1

    print()
    print("="*60)
    print(f"✅ {fixed}/{len(FIXES)} especialistas corrigidos")
    print()
    print("Padrão aplicado:")
    print("  • Score inicial: 90.0 (não 100)")
    print("  • Cap máximo: 95.0 (não 100)")
    print("  • Range: max(5.0, min(95.0, score))")

if __name__ == "__main__":
    main()
