#!/usr/bin/env python3
"""
Auditoria de Qualidade dos Especialistas Triple-Core

Compara todos os 22 especialistas com o padrão de qualidade do DrDialogue (primeiro migrado).
"""

import sys
from pathlib import Path
import re
import ast

print("="*80)
print("🔍 AUDITORIA DE QUALIDADE - Triple-Core Specialists")
print("="*80)
print()

# Padrão de qualidade (baseado em DrDialogue)
QUALITY_STANDARDS = {
    'has_analyze_method': 'Deve ter método analyze()',
    'analyze_returns_dict': 'analyze() deve retornar Dict[str, Any]',
    'has_generate_diagnosis': 'Deve ter método _generate_diagnosis()',
    'returns_specialist_info': 'Deve retornar {"specialist": {...}}',
    'returns_score': 'Deve retornar {"score": int}',
    'returns_recommendations': 'Deve retornar {"recommendations": List}',
    'has_dataclasses': 'Pode ter @dataclass para estruturas internas',
    'converts_dataclasses_to_dict': 'Deve converter dataclasses para dicts no retorno'
}

# Lista de todos os 22 especialistas
specialists = [
    ("Dialogue", "triple_core/core_1_specialists/dialogue/dr_dialogue.py"),
    ("Structure", "triple_core/core_1_specialists/structure/dr_structure.py"),
    ("Pacing", "triple_core/core_1_specialists/pacing/dr_pacing.py"),
    ("Opening", "triple_core/core_1_specialists/opening/dr_opening.py"),
    ("Climax", "triple_core/core_1_specialists/climax/dr_climax.py"),
    ("Resolution", "triple_core/core_1_specialists/resolution/dr_resolution.py"),
    ("Transitions", "triple_core/core_1_specialists/transitions/dr_transitions.py"),
    ("Action", "triple_core/core_1_specialists/action/dr_action.py"),
    ("Formatting", "triple_core/core_1_specialists/formatting/dr_formatting.py"),
    ("Subtext", "triple_core/core_1_specialists/subtext/dr_subtext.py"),
    ("Theme", "triple_core/core_1_specialists/theme/dr_theme.py"),
    ("Tone", "triple_core/core_1_specialists/tone/dr_tone.py"),
    ("Voice", "triple_core/core_1_specialists/voice/dr_voice.py"),
    ("Symbolism", "triple_core/core_1_specialists/symbolism/dr_symbolism.py"),
    ("Visual Motifs", "triple_core/core_1_specialists/visual/dr_visual_motifs.py"),
    ("Genre", "triple_core/core_1_specialists/genre/dr_genre.py"),
    ("World Building", "triple_core/core_1_specialists/worldbuilding/dr_worldbuilding.py"),
    ("Psychology", "triple_core/core_1_specialists/character/psychology/dr_psychology.py"),
    ("Arcs", "triple_core/core_1_specialists/character/arcs/dr_arcs.py"),
    ("Relationships", "triple_core/core_1_specialists/character/relationships/dr_relationships.py"),
    ("Originality", "triple_core/core_1_specialists/originality/dr_originality.py"),
    ("Market", "triple_core/core_1_specialists/market/dr_market_potential.py"),
]

print(f"📋 Auditando {len(specialists)} especialistas...")
print(f"📏 Padrão de referência: DrDialogue (primeiro migrado)")
print()

audit_results = []

for name, file_path in specialists:
    result = {
        'name': name,
        'file_path': file_path,
        'checks': {},
        'issues': [],
        'score': 0
    }

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check 1: Has analyze method
        has_analyze = bool(re.search(r'def analyze\(', content))
        result['checks']['has_analyze_method'] = has_analyze
        if not has_analyze:
            result['issues'].append("❌ Método analyze() não encontrado")

        # Check 2: analyze returns Dict[str, Any]
        analyze_sig = re.search(r'def analyze\([^)]*\)\s*->\s*Dict\[str,\s*Any\]', content)
        result['checks']['analyze_returns_dict'] = bool(analyze_sig)
        if not analyze_sig:
            result['issues'].append("❌ analyze() não retorna Dict[str, Any]")

        # Check 3: Has _generate_diagnosis
        has_diagnosis = bool(re.search(r'def _generate_diagnosis\(', content))
        result['checks']['has_generate_diagnosis'] = has_diagnosis
        if not has_diagnosis:
            result['issues'].append("❌ Método _generate_diagnosis() não encontrado")

        # Check 4: Returns specialist info
        has_specialist_return = bool(re.search(r'"specialist":\s*\{', content))
        result['checks']['returns_specialist_info'] = has_specialist_return
        if not has_specialist_return:
            result['issues'].append("❌ Não retorna {'specialist': {...}}")

        # Check 5: Returns score
        has_score_return = bool(re.search(r'"score":\s*score', content))
        result['checks']['returns_score'] = has_score_return
        if not has_score_return:
            result['issues'].append("❌ Não retorna {'score': ...}")

        # Check 6: Returns recommendations
        has_recs = bool(re.search(r'"recommendations":', content))
        result['checks']['returns_recommendations'] = has_recs
        if not has_recs:
            result['issues'].append("⚠️ Não retorna {'recommendations': ...}")

        # Check 7: Has dataclasses (optional - some specialists don't need them)
        has_dataclasses = bool(re.search(r'@dataclass', content))
        result['checks']['has_dataclasses'] = has_dataclasses

        # Check 8: Converts to dict (if has dataclasses)
        if has_dataclasses:
            # Look for dict conversion patterns
            has_dict_conversion = bool(
                re.search(r'_to_dict\(', content) or
                re.search(r'\{[^}]*:\s*\w+\.\w+', content)  # Dict comprehension pattern
            )
            result['checks']['converts_dataclasses_to_dict'] = has_dict_conversion
            if not has_dict_conversion:
                result['issues'].append("⚠️ Tem dataclasses mas pode não converter para dict")

        # Calculate score (percentage of checks passed)
        passed = sum(1 for v in result['checks'].values() if v)
        total = len(result['checks'])
        result['score'] = (passed / total) * 100 if total > 0 else 0

    except FileNotFoundError:
        result['issues'].append(f"❌ ARQUIVO NÃO ENCONTRADO: {file_path}")
        result['score'] = 0
    except Exception as e:
        result['issues'].append(f"❌ ERRO AO ANALISAR: {e}")
        result['score'] = 0

    audit_results.append(result)

# Sort by score (lowest first to highlight issues)
audit_results.sort(key=lambda x: x['score'])

# Print results
print("="*80)
print("📊 RESULTADOS DA AUDITORIA")
print("="*80)
print()

perfect_count = 0
issues_count = 0

for result in audit_results:
    status = "✅" if result['score'] == 100 else ("⚠️" if result['score'] >= 75 else "❌")
    print(f"{status} {result['name']:20s} - {result['score']:5.1f}% ({result['file_path'].split('/')[-1]})")

    if result['issues']:
        issues_count += 1
        for issue in result['issues']:
            print(f"     {issue}")
    else:
        perfect_count += 1

print()
print("="*80)
print("📈 ESTATÍSTICAS")
print("="*80)
print()

total = len(audit_results)
avg_score = sum(r['score'] for r in audit_results) / total if total > 0 else 0

print(f"Total de especialistas: {total}")
print(f"Score médio: {avg_score:.1f}%")
print(f"Perfeitos (100%): {perfect_count}/{total} ({perfect_count/total*100:.1f}%)")
print(f"Com issues: {issues_count}/{total} ({issues_count/total*100:.1f}%)")
print()

# Quality grade
if avg_score >= 95:
    grade = "EXCELENTE ✅"
elif avg_score >= 85:
    grade = "MUITO BOM 👍"
elif avg_score >= 75:
    grade = "BOM ⚠️"
else:
    grade = "PRECISA MELHORIAS ❌"

print(f"Qualidade Geral: {grade}")
print()

# Detailed checks summary
print("="*80)
print("🔍 RESUMO DETALHADO DOS CHECKS")
print("="*80)
print()

check_names = [
    'has_analyze_method',
    'analyze_returns_dict',
    'has_generate_diagnosis',
    'returns_specialist_info',
    'returns_score',
    'returns_recommendations',
    'has_dataclasses',
    'converts_dataclasses_to_dict'
]

for check in check_names:
    passed = sum(1 for r in audit_results if r['checks'].get(check, False))
    total_applicable = sum(1 for r in audit_results if check in r['checks'])
    if total_applicable > 0:
        percentage = (passed / total_applicable) * 100
        status = "✅" if percentage == 100 else ("⚠️" if percentage >= 90 else "❌")
        print(f"{status} {check:35s}: {passed:2d}/{total_applicable:2d} ({percentage:5.1f}%)")

print()

# Exit code
if avg_score >= 95:
    print("="*80)
    print("✅ AUDITORIA PASSOU! Todos os especialistas seguem o padrão de qualidade!")
    print("="*80)
    sys.exit(0)
else:
    print("="*80)
    print("⚠️ AUDITORIA DETECTOU INCONSISTÊNCIAS!")
    print("="*80)
    print()
    print("Especialistas que precisam de atenção:")
    for result in audit_results:
        if result['score'] < 100:
            print(f"  • {result['name']} ({result['score']:.0f}%): {len(result['issues'])} issues")
    sys.exit(1)
