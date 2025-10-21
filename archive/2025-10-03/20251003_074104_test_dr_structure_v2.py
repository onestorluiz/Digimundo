#!/usr/bin/env python3
"""
Test script for DrStructure v2
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from triple_core.core_1_specialists.structure.dr_structure_v2 import DrStructure

def test_dr_structure():
    """Test DrStructure v2 with Sonhos Sem Lembranças"""

    # Initialize specialist
    dr = DrStructure()

    # Load screenplay
    screenplay_path = Path(__file__).parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

    with open(screenplay_path, 'r', encoding='utf-8') as f:
        screenplay_text = f.read()

    # Analyze
    print("=" * 80)
    print("TESTING DR STRUCTURE V2")
    print("=" * 80)
    print(f"\nAnalyzing: {screenplay_path.name}")
    print(f"Specialist: {dr.name}")
    print(f"Specialty: {dr.specialty}")
    print("\nRunning analysis...")

    result = dr.analyze(screenplay_text)

    # Display results
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)

    print(f"\n📊 SCORE: {result['score']:.1f}/100")
    print(f"📄 Total Pages: {result['total_pages']}")
    print(f"🎬 Scene Count: {result['scene_count']}")

    print("\n" + "-" * 80)
    print("ACT STRUCTURE")
    print("-" * 80)
    for act in result['acts']:
        status_emoji = "✅" if act['status'] == 'good' else "⚠️" if act['status'] == 'acceptable' else "❌"
        print(f"{status_emoji} Act {act['act']}: {act['pages']} pages ({act['percentage']:.1f}% - expected {act['expected']}%)")
        print(f"   Status: {act['status']}, Avg Intensity: {act['avg_intensity']:.2f}")
        if act['beats']:
            print(f"   Beats: {', '.join(act['beats'])}")

    print("\n" + "-" * 80)
    print("STRUCTURAL BEATS FOUND")
    print("-" * 80)
    for beat in result['beats_found']:
        conf_emoji = "🟢" if beat['confidence'] > 0.7 else "🟡" if beat['confidence'] > 0.4 else "🔴"
        print(f"{conf_emoji} {beat['name']}:")
        print(f"   Page {beat['found_at']} (expected ~{beat['expected_page']}) - Confidence: {beat['confidence']:.0%}")
        if beat['indicators']:
            print(f"   Indicators: {', '.join(beat['indicators'][:2])}")

    if result['beats_missing']:
        print("\n" + "-" * 80)
        print("❌ MISSING BEATS")
        print("-" * 80)
        for beat in result['beats_missing']:
            print(f"   - {beat}")

    print("\n" + "-" * 80)
    print("PACING ANALYSIS")
    print("-" * 80)
    pacing = result['pacing_analysis']
    print(f"Overall Pace: {pacing['overall_pace']}")
    print(f"Avg Scene Length: {pacing['avg_scene_length']} words")
    print(f"Avg Intensity: {pacing['avg_intensity']:.2f}")
    print(f"Pace Changes: {pacing['pace_changes']}")

    print("\n" + "-" * 80)
    print("DRAMATIC ARC")
    print("-" * 80)
    arc = result['dramatic_arc']
    print(f"Arc Shape: {arc['arc_shape']}")
    print(f"Peak Intensity: {arc['peak_intensity']:.2f} at {arc['peak_location_percentage']:.1f}%")
    print(f"Act Intensities: Act 1={arc['first_act_avg']:.2f}, Act 2={arc['second_act_avg']:.2f}, Act 3={arc['third_act_avg']:.2f}")

    if result['rule_violations']:
        print("\n" + "-" * 80)
        print("⚠️  RULE VIOLATIONS")
        print("-" * 80)
        for violation in result['rule_violations']:
            print(f"[{violation['severity'].upper()}] {violation['title']}")
            print(f"   {violation['message']}")

    print("\n" + "-" * 80)
    print("📋 DIAGNOSIS")
    print("-" * 80)
    print(result['diagnosis'][:500])

    print("\n" + "-" * 80)
    print("💡 RECOMMENDATIONS")
    print("-" * 80)
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. {rec}")

    print("\n" + "=" * 80)
    print("COMPARISON WITH DR DIALOGUE")
    print("=" * 80)

    # Count methods
    import inspect
    dr_methods = [m for m in dir(dr) if not m.startswith('_') and callable(getattr(dr, m))]
    private_methods = [m for m in dir(dr) if m.startswith('_') and callable(getattr(dr, m)) and not m.startswith('__')]

    print(f"\nDrStructure v2:")
    print(f"  Public methods: {len(dr_methods)}")
    print(f"  Private methods: {len(private_methods)}")
    print(f"  Total methods: {len(dr_methods) + len(private_methods)}")

    # Check file size
    file_path = Path(__file__).parent / "triple_core/core_1_specialists/structure/dr_structure_v2.py"
    with open(file_path, 'r') as f:
        lines = f.readlines()
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

    print(f"\nFile metrics:")
    print(f"  Total lines: {total_lines}")
    print(f"  Code lines: {code_lines}")
    print(f"  File size: {file_path.stat().st_size / 1024:.1f} KB")

    print("\n✅ Test completed successfully!")
    print(f"\n{result['signature']}")

    return result

if __name__ == "__main__":
    test_dr_structure()
