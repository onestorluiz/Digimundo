#!/usr/bin/env python3
"""
Re-valida todos os especialistas graduados usando o novo sistema de 3 camadas
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.validation import ScriptDoctorGraduationValidator


# Mapeamento de especialistas para tipos
SPECIALIST_TYPES = {
    'test_dialogue_v4.1_results.json': 'dialogue',
    'test_psychemon_v4.1_results.json': 'psychemon',
    'test_submon_v4.1_results.json': 'submon',
    'test_thememon_v4.1_results.json': 'thememon',
    'test_character_arcs_v4.1_results.json': 'character_arcs',
    'test_relationships_v4.1_results.json': 'relationships',
    'test_structure_v4.1_results.json': 'structure',
    'test_pacing_v4.1_results.json': 'pacing',
    'test_tone_v4.1_results.json': 'tone_consistency',
    'test_opening_v4.1_results.json': 'opening',
    'test_climax_v4.1_results.json': 'climax',
    'test_resolution_v4.1_results.json': 'resolution',
    'test_action_description_v4.1_results.json': 'action_description',
    'test_symbolism_v4.1_results.json': 'symbolism',
    'test_genre_v4.1_results.json': 'genre',
    'test_originality_v4.1_results.json': 'originality',
}


def main():
    print("\n" + "="*80)
    print("🔄 RE-VALIDANDO TODOS OS ESPECIALISTAS GRADUADOS")
    print("="*80)

    # Paths
    results_dir = Path(__file__).parent.parent / "results" / "v4.1_graduation"
    screenplay_path = Path(__file__).parent.parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"
    validation_dir = Path(__file__).parent.parent / "results" / "validation_reports"
    validation_dir.mkdir(exist_ok=True)

    # Sumário
    summary = []

    # Para cada resultado
    for result_file, specialist_type in SPECIALIST_TYPES.items():
        result_path = results_dir / result_file

        if not result_path.exists():
            print(f"\n⚠️  Skipping {result_file} (not found)")
            continue

        print(f"\n{'='*80}")
        print(f"📋 Validating: {specialist_type}")
        print(f"{'='*80}")

        # Carrega resultado
        with open(result_path, 'r', encoding='utf-8') as f:
            result = json.load(f)

        # Valida
        try:
            validator = ScriptDoctorGraduationValidator(
                screenplay_path=str(screenplay_path),
                specialist_type=specialist_type
            )

            validation_result = validator.validate(result)

            # Salva relatório
            report_path = validation_dir / f"validation_{specialist_type}"
            validator.save_validation_report(validation_result, report_path)

            # Print resultado
            grad = validation_result['graduation']
            print(f"\n{'='*80}")
            print(f"RESULTADO: {'✅ APPROVED' if grad['approved'] else '❌ NOT APPROVED'}")
            print(f"{'='*80}")
            print(f"Tier: {grad['tier']}")
            print(f"Classification: {grad['classification']}")
            print(f"Final Score: {grad['final_score']:.1f}%")
            print(f"\nScores:")
            print(f"  Technical:    {'✅' if validation_result['layer1_technical']['all_passed'] else '❌'}")
            print(f"  Specificity:  {validation_result['layer2_specificity']['percentage']:.1f}% {'✅' if validation_result['layer2_specificity']['passed'] else '❌'}")
            print(f"  Depth:        {validation_result['layer3_depth']['percentage']:.1f}% {'✅' if validation_result['layer3_depth']['passed'] else '❌'}")

            # Adiciona ao sumário
            summary.append({
                'specialist': specialist_type,
                'approved': grad['approved'],
                'tier': grad['tier'],
                'classification': grad['classification'],
                'final_score': grad['final_score'],
                'technical': validation_result['layer1_technical']['all_passed'],
                'specificity_score': validation_result['layer2_specificity']['percentage'],
                'specificity_passed': validation_result['layer2_specificity']['passed'],
                'depth_score': validation_result['layer3_depth']['percentage'],
                'depth_passed': validation_result['layer3_depth']['passed'],
                'scene_citations': validation_result['layer2_specificity']['components']['scene_citations']['count'],
                'dialogue_quotes': validation_result['layer2_specificity']['components']['dialogue_quotes']['count'],
                'character_usage': validation_result['layer2_specificity']['components']['character_names']['count'],
            })

        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            summary.append({
                'specialist': specialist_type,
                'approved': False,
                'tier': 'ERROR',
                'classification': 'ERROR',
                'final_score': 0,
                'error': str(e)
            })

    # Salva sumário
    summary_path = validation_dir / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print sumário
    print(f"\n{'='*80}")
    print("📊 SUMÁRIO FINAL")
    print(f"{'='*80}\n")

    print(f"{'Specialist':<20} {'Tier':<6} {'Final':<8} {'Spec':<8} {'Depth':<8} {'Status'}")
    print("-" * 80)

    approved_count = 0
    for item in summary:
        if 'error' in item:
            print(f"{item['specialist']:<20} {'ERROR':<6} {'N/A':<8} {'N/A':<8} {'N/A':<8} ❌ ERROR")
            continue

        status = '✅' if item['approved'] else '❌'
        if item['approved']:
            approved_count += 1

        print(f"{item['specialist']:<20} "
              f"{item['tier']:<6} "
              f"{item['final_score']:>6.1f}% "
              f"{item['specificity_score']:>6.1f}% "
              f"{item['depth_score']:>6.1f}% "
              f"{status}")

    print("-" * 80)
    print(f"\nTotal: {len(summary)} specialists")
    print(f"Approved: {approved_count} ({approved_count/len(summary)*100:.1f}%)")
    print(f"Failed: {len(summary) - approved_count} ({(len(summary) - approved_count)/len(summary)*100:.1f}%)")

    # Estatísticas detalhadas
    print(f"\n{'='*80}")
    print("📈 ESTATÍSTICAS DETALHADAS")
    print(f"{'='*80}\n")

    valid_items = [item for item in summary if 'error' not in item]

    if valid_items:
        avg_final = sum(item['final_score'] for item in valid_items) / len(valid_items)
        avg_spec = sum(item['specificity_score'] for item in valid_items) / len(valid_items)
        avg_depth = sum(item['depth_score'] for item in valid_items) / len(valid_items)

        print(f"Scores médios:")
        print(f"  Final:        {avg_final:.1f}%")
        print(f"  Specificity:  {avg_spec:.1f}%")
        print(f"  Depth:        {avg_depth:.1f}%")

        print(f"\nEspecificidade:")
        avg_scenes = sum(item['scene_citations'] for item in valid_items) / len(valid_items)
        avg_quotes = sum(item['dialogue_quotes'] for item in valid_items) / len(valid_items)
        avg_chars = sum(item['character_usage'] for item in valid_items) / len(valid_items)

        print(f"  Scene citations:  {avg_scenes:.1f} (mín: 3)")
        print(f"  Dialogue quotes:  {avg_quotes:.1f} (mín: 2)")
        print(f"  Character usage:  {avg_chars:.1f} (mín: 5)")

        # Tiers
        tier_counts = {}
        for item in valid_items:
            tier = item['tier']
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        print(f"\nDistribuição por Tier:")
        for tier in sorted(tier_counts.keys()):
            count = tier_counts[tier]
            pct = count / len(valid_items) * 100
            print(f"  {tier}: {count} ({pct:.1f}%)")

    print(f"\n{'='*80}")
    print(f"✅ Relatórios salvos em: {validation_dir}")
    print(f"📊 Sumário salvo em: {summary_path}")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
