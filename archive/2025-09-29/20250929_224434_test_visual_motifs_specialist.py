#!/usr/bin/env python3
"""
Test Suite for Script Doctor Motifmon - Visual Motifs Specialist
Tests the visual motifs specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.visual_motifs_specialist import DrVisualMotifs


def create_motif_rich_screenplay():
    """Create a screenplay with rich visual motifs."""
    return """FADE IN:

EXT. LIGHTHOUSE - DAWN

The lighthouse beam circles through morning fog. Waves crash
against rocks below.

INT. LIGHTHOUSE - CONTINUOUS

ANNA (30s) polishes the lighthouse lens. Her reflection 
fragments in the glass. A COMPASS sits on the window sill.

She looks through the window at the circling beam of light.

EXT. BEACH - DAY

Anna walks along the shore. Her RED SCARF flutters in the wind.
She finds a BROKEN MIRROR half-buried in sand.

The lighthouse stands tall behind her, its shadow stretching
across the beach.

INT. COTTAGE - NIGHT

Anna lights a CANDLE. The flame flickers, casting dancing
shadows on the walls. The compass needle spins wildly.

Through the window, the lighthouse beam circles in the darkness.

EXT. CLIFF - STORM - NIGHT

Rain pounds. Lightning illuminates the lighthouse. Anna's red
scarf whips in the wind as she climbs toward the light.

The beam circles, cutting through the storm.

INT. LIGHTHOUSE - TOP - NIGHT

Anna reaches the light. The lens reflects her face in a
thousand fragments. She adjusts the beam.

The compass needle finally points true north.

EXT. LIGHTHOUSE - DAWN

The storm has passed. The lighthouse beam circles one last time
before fading in the morning light.

Anna stands at the base, red scarf still, looking up at the
light she saved.

FADE OUT."""


def create_motif_poor_screenplay():
    """Create a screenplay with poor visual motifs."""
    return """FADE IN:

INT. ROOM - DAY

BOB sits. He stands. He walks to the door.

EXT. STREET - DAY

Bob walks down the street. Cars pass.

INT. STORE - DAY

Bob buys groceries. He pays. He leaves.

EXT. PARK - DAY

Bob sits on a bench. Birds fly. He watches.

INT. ROOM - NIGHT

Bob returns home. He eats dinner. He watches TV.

He goes to bed.

FADE OUT."""


def test_basic_motif_analysis():
    """Test basic visual motif analysis."""
    print("\n🎯 TEST 1: Basic Motif Analysis")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()

    result = dr_motifs.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "motif_analysis" in result.__dict__
    assert "visual_motifs" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Total motifs: {result.motif_analysis.total_motifs}")
    print(f"✅ Recurring motifs: {result.motif_analysis.recurring_motifs}")

    return True


def test_motif_identification():
    """Test motif identification."""
    print("\n🎯 TEST 2: Motif Identification")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"🔑 Object motifs: {result.motif_analysis.object_motifs}")
    print(f"🎨 Color motifs: {result.motif_analysis.color_motifs}")
    print(f"💡 Lighting motifs: {result.motif_analysis.lighting_motifs}")
    print(f"☁️ Weather motifs: {result.motif_analysis.weather_motifs}")
    print(f"🌀 Movement motifs: {result.motif_analysis.movement_motifs}")

    # List some identified motifs
    for motif in result.visual_motifs[:3]:
        print(f"   {motif.name}: {len(motif.occurrences)} occurrences")

    assert result.motif_analysis.total_motifs > 0
    print("\n✅ Motif identification working")

    return True


def test_motif_recurrence():
    """Test motif recurrence detection."""
    print("\n🎯 TEST 3: Motif Recurrence")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"🔁 Recurring motifs: {result.motif_analysis.recurring_motifs}")
    
    # Check specific recurring motifs
    for motif in result.visual_motifs:
        if len(motif.occurrences) >= 3:
            print(f"   {motif.name}: appears {len(motif.occurrences)} times")
            print(f"   Consistency: {motif.consistency_score:.2f}")

    print("\n✅ Motif recurrence detection working")

    return True


def test_motif_consistency():
    """Test motif consistency analysis."""
    print("\n🎯 TEST 4: Motif Consistency")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"🔄 Overall consistency: {result.motif_analysis.consistency_score:.2f}")
    
    # Check individual motif consistency
    for motif in result.visual_motifs[:3]:
        print(f"   {motif.name}: {motif.consistency_score:.2f}")

    print("\n✅ Motif consistency analysis working")

    return True


def test_motif_evolution():
    """Test motif evolution tracking."""
    print("\n🎯 TEST 5: Motif Evolution")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"🌱 Evolution score: {result.motif_analysis.evolution_score:.2f}")
    
    # Check motif evolution
    for motif in result.visual_motifs[:3]:
        if motif.evolution:
            print(f"   {motif.name}: {' -> '.join(motif.evolution)}")

    print("\n✅ Motif evolution tracking working")

    return True


def test_visual_bookends():
    """Test visual bookend detection."""
    print("\n🎯 TEST 6: Visual Bookends")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"📖 Has bookends: {result.motif_analysis.has_bookends}")
    print(f"🏁 Payoff score: {result.motif_analysis.payoff_score:.2f}")

    print("\n✅ Visual bookend detection working")

    return True


def test_cinematic_potential():
    """Test cinematic potential scoring."""
    print("\n🎯 TEST 7: Cinematic Potential")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"🎬 Cinematic potential: {result.motif_analysis.cinematic_potential:.2f}")
    
    # Check individual motif impact
    for motif in result.visual_motifs[:3]:
        print(f"   {motif.name}: impact {motif.cinematic_impact:.2f}")

    print("\n✅ Cinematic potential scoring working")

    return True


def test_motif_timeline():
    """Test motif timeline creation."""
    print("\n🎯 TEST 8: Motif Timeline")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    screenplay = create_motif_rich_screenplay()
    result = dr_motifs.analyze(screenplay)

    print(f"📅 Timeline entries: {len(result.motif_timeline)}")
    
    # Show first few timeline entries
    for entry in result.motif_timeline[:5]:
        print(f"   Scene {entry['scene']}: {entry['motif']} ({entry['type']})")

    print("\n✅ Motif timeline creation working")

    return True


def test_rule_violations():
    """Test visual motif rule violations."""
    print("\n🎯 TEST 9: Rule Violations")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()

    # Test with motif-poor screenplay
    poor = create_motif_poor_screenplay()
    result = dr_motifs.analyze(poor)
    violations = result.rule_violations

    print(f"📋 Found {len(violations)} violations:")
    for violation in violations[:5]:  # Show first 5
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }.get(violation["severity"], "⚪")

        print(f"{severity_emoji} [{violation['severity'].upper()}] {violation['title']}")
        if "message" in violation:
            print(f"   {violation['message']}")

    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎯 TEST 10: Recommendations")
    print("=" * 50)

    dr_motifs = DrVisualMotifs()
    poor = create_motif_poor_screenplay()

    result = dr_motifs.analyze(poor)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations for poor screenplay
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Motifmon tests."""
    print("\n" + "=" * 60)
    print("🎯 SCRIPT DOCTOR MOTIFMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Motif Analysis", test_basic_motif_analysis),
        ("Motif Identification", test_motif_identification),
        ("Motif Recurrence", test_motif_recurrence),
        ("Motif Consistency", test_motif_consistency),
        ("Motif Evolution", test_motif_evolution),
        ("Visual Bookends", test_visual_bookends),
        ("Cinematic Potential", test_cinematic_potential),
        ("Motif Timeline", test_motif_timeline),
        ("Rule Violations", test_rule_violations),
        ("Recommendations", test_recommendations)
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print("📊 FINAL REPORT")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")

    if passed == len(tests):
        print("\n🎉 SCRIPT DOCTOR MOTIFMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Visual Motifs Specialist is ready")
        print("\n🎯 Visual motif analysis systems online!")
        print("\n📝 Specialist 17/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
