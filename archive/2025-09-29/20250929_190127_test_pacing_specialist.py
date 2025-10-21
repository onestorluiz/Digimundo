#!/usr/bin/env python3
"""
Test Suite for Script Doctor Pacingmon - Rhythm and Tempo Specialist
Tests the pacing specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.pacing_specialist import DrPacing


def create_well_paced_screenplay():
    """Create a screenplay with good pacing."""
    return """FADE IN:

EXT. CITY STREET - DAY

Quick establishing shot. Cars SPEED by.

INT. COFFEE SHOP - DAY

JANE (30s) checks her watch. Impatient.

MARK (30s) BURSTS through the door.

MARK
Sorry! Traffic was--

JANE
We have five minutes.

They speak in RAPID whispers.

JANE (CONT'D)
The package. Where is it?

MARK
Hidden. Safe.

EXT. ALLEY - DAY

They RUN. Fast cuts. Urgency building.

INT. WAREHOUSE - DAY

Slower pace. They catch their breath.

JANE
We wait here.

Long pause. Tension builds.

MARK
What if they find us?

JANE
They won't.

SUDDENLY -- CRASH! Door EXPLODES open.

EXT. ROOFTOP - DAY

CHASE SEQUENCE. Pure adrenaline.

They LEAP between buildings.

INT. SAFE HOUSE - NIGHT

Quiet. Finally safe. Breathing slows.

MARK
That was close.

JANE
Too close.

They share a moment of calm.

FADE OUT."""


def create_poorly_paced_screenplay():
    """Create a screenplay with bad pacing."""
    return """FADE IN:

INT. LIVING ROOM - DAY

John sits on the couch. He thinks about his life. He remembers his childhood. His mother was kind. His father was strict. He had a dog named Rover. The dog was brown. He loved that dog very much. One day the dog ran away. He was very sad. He looked for the dog everywhere. He never found the dog. This made him who he is today. A man who is careful about everything. He doesn't want to lose anything again. Not like he lost Rover. That brown dog with the white spot on his left ear. He still dreams about that dog sometimes. In the dreams, the dog comes back. But then he wakes up. And the dog is still gone. Just like his childhood. Just like his innocence. Everything is gone now. He is alone in this room. Thinking. Always thinking. Never doing. Just sitting and thinking about the past. About Rover. About everything he's lost. The wallpaper is beige. He chose it himself. It reminds him of Rover's fur. Everything reminds him of something. The coffee table is wooden. Like the stick Rover used to fetch. He can't escape the memories. They define him. They trap him. He continues to sit. Time passes. Nothing happens. He just sits.

FADE OUT."""


def test_basic_pacing_analysis():
    """Test basic pacing analysis."""
    print("\n🧪 TEST 1: Basic Pacing Analysis")
    print("=" * 50)

    dr_pacing = DrPacing()
    screenplay = create_well_paced_screenplay()

    result = dr_pacing.analyze(screenplay)

    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "pacing_curve" in result
    assert "tempo_distribution" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Scene count: {result['scene_count']}")
    print(f"✅ Average scene length: {result['average_scene_length']:.2f} pages")

    return True


def test_tempo_detection():
    """Test tempo detection in scenes."""
    print("\n🧪 TEST 2: Tempo Detection")
    print("=" * 50)

    dr_pacing = DrPacing()
    screenplay = create_well_paced_screenplay()

    result = dr_pacing.analyze(screenplay)
    tempo_dist = result["tempo_distribution"]

    print("🎵 Tempo Distribution:")
    for tempo, count in tempo_dist.items():
        print(f"   {tempo}: {count} scenes")

    # Should have variety
    assert len(tempo_dist) > 0
    print("\n✅ Tempo detection working")

    return True


def test_pacing_curve_analysis():
    """Test pacing curve analysis."""
    print("\n🧪 TEST 3: Pacing Curve Analysis")
    print("=" * 50)

    dr_pacing = DrPacing()

    # Test good pacing
    good_screenplay = create_well_paced_screenplay()
    good_result = dr_pacing.analyze(good_screenplay)
    good_curve = good_result["pacing_curve"]

    print(f"📈 Good screenplay curve: {good_curve['type']}")
    print(f"   Score: {good_curve['score']}")
    if "trajectory" in good_curve:
        print(f"   Trajectory: {[f'{t:.1f}' for t in good_curve['trajectory']]}")

    # Test bad pacing
    bad_screenplay = create_poorly_paced_screenplay()
    bad_result = dr_pacing.analyze(bad_screenplay)
    bad_curve = bad_result["pacing_curve"]

    print(f"\n📉 Bad screenplay curve: {bad_curve['type']}")
    print(f"   Score: {bad_curve['score']}")

    # Good should score higher than bad
    assert good_curve["score"] >= bad_curve["score"]
    print("\n✅ Pacing curve analysis working")

    return True


def test_white_space_analysis():
    """Test white space analysis."""
    print("\n🧪 TEST 4: White Space Analysis")
    print("=" * 50)

    dr_pacing = DrPacing()

    # Good white space
    good = create_well_paced_screenplay()
    good_result = dr_pacing.analyze(good)
    good_white = good_result["white_space_score"]

    # Bad white space (dense)
    bad = create_poorly_paced_screenplay()
    bad_result = dr_pacing.analyze(bad)
    bad_white = bad_result["white_space_score"]

    print(f"📄 Well-formatted script: {good_white}/100")
    print(f"📄 Dense script: {bad_white}/100")

    # Good should have better white space
    assert good_white >= bad_white
    print("\n✅ White space analysis working")

    return True


def test_rule_violations():
    """Test pacing rule violations."""
    print("\n🧪 TEST 5: Pacing Rule Violations")
    print("=" * 50)

    dr_pacing = DrPacing()

    # Test with problematic screenplay
    bad_screenplay = create_poorly_paced_screenplay()
    result = dr_pacing.analyze(bad_screenplay)
    violations = result.get("rule_violations", [])

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

    # Should detect issues in bad screenplay
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_dialogue_ratio():
    """Test dialogue ratio calculation."""
    print("\n🧪 TEST 6: Dialogue Ratio Analysis")
    print("=" * 50)

    dr_pacing = DrPacing()

    # Dialogue-heavy script
    dialogue_heavy = """INT. ROOM - DAY

ALICE
This is a very long speech about my feelings
and thoughts and dreams and hopes.

BOB
And this is my equally long response about
my own feelings and thoughts.

ALICE
Let me continue talking at length.

BOB
And I'll keep responding."""

    # Action-heavy script
    action_heavy = """INT. ROOM - DAY

Alice enters. She looks around. Sees something.
Picks it up. Examines it carefully. Sets it down.
Walks to window. Looks outside. Sees Bob approaching.
Opens door. Bob enters. They stare at each other.
No words needed."""

    dialogue_result = dr_pacing.analyze(dialogue_heavy)
    action_result = dr_pacing.analyze(action_heavy)

    print(f"💬 Dialogue-heavy ratio: {dialogue_result['dialogue_ratio']*100:.0f}%")
    print(f"🎬 Action-heavy ratio: {action_result['dialogue_ratio']*100:.0f}%")

    # Dialogue-heavy should have higher ratio
    assert dialogue_result["dialogue_ratio"] > action_result["dialogue_ratio"]
    print("\n✅ Dialogue ratio analysis working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🧪 TEST 7: Recommendation Generation")
    print("=" * 50)

    dr_pacing = DrPacing()
    bad_screenplay = create_poorly_paced_screenplay()

    result = dr_pacing.analyze(bad_screenplay)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Should generate recommendations for bad screenplay
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")

    return True


def run_all_tests():
    """Run all Pacingmon tests."""
    print("\n" + "=" * 60)
    print("🏥 SCRIPT DOCTOR PACINGMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Pacing Analysis", test_basic_pacing_analysis),
        ("Tempo Detection", test_tempo_detection),
        ("Pacing Curve Analysis", test_pacing_curve_analysis),
        ("White Space Analysis", test_white_space_analysis),
        ("Rule Violations", test_rule_violations),
        ("Dialogue Ratio", test_dialogue_ratio),
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
        print("\n🎉 SCRIPT DOCTOR PACINGMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Rhythm and Tempo Specialist is ready")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)