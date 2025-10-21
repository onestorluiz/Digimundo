#!/usr/bin/env python3
"""
Test Suite for Script Doctor Metamon - Originality Assessment Specialist
Tests the originality assessment specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.originality_assessment_specialist import DrOriginalityAssessment


def create_original_screenplay():
    """Create a screenplay with original elements."""
    return """FADE IN:

INT. INVERTED LIBRARY - TIMELESS

Books fall upward. Gravity reverses every seventh heartbeat.
ARIA (ageless), a memory architect, sculpts forgotten dreams
into tangible narratives.

ARIA
(to her shadow, which responds)
Today we resurrect the unremembered.

Her SHADOW nods, independent. It begins gathering light
particles, weaving them into story threads.

INT. MEMORY VAULT - CONTINUOUS

Aria enters through a door that exists only when observed.
Crystallized memories float like jellyfish, each pulsing
with someone's discarded past.

She selects one - it tastes of childhood summers and
industrial accidents.

ARIA
This one died before it could become
nostalgia. Perfect.

She inserts the memory into her temporal loom. The machine
runs backward, unweaving effect from cause.

YOUNG BOY (5)
(materializing from the memory)
I'm not supposed to exist yet.

ARIA
None of us are. That's what makes us
interesting.

The Boy fragments into possibility particles. Each particle
shows a different future he'll never have.

INT. PROBABILITY GARDEN - LATER

Aria plants the memory fragments in soil made of compressed
time. Each sprout blooms into alternative histories.

SHADOW
(speaking for the first time)
What if someone remembers what never was?

ARIA
Then we'll have succeeded in failing
correctly.

The garden inverts. Roots become branches. The past grows
downward while the future burrows into yesterday.

FADE OUT."""


def create_derivative_screenplay():
    """Create a screenplay with derivative elements."""
    return """FADE IN:

INT. POLICE STATION - DAY

DETECTIVE JACK STONE (40s), grizzled, drinks coffee. His
partner died last week. This time it's personal.

JACK
I'm getting too old for this.

CAPTAIN WILLIAMS enters.

CAPTAIN
There's been another murder. Same MO.

JACK
Let me guess - the killer left a clue.

CAPTAIN
You've got 48 hours or you're off the case.

EXT. CRIME SCENE - DAY

Jack arrives. It's quiet... too quiet.

JACK
We've got company.

Bad guys attack! Jack fights them off, walking away from
an explosion without looking back.

INT. BAR - NIGHT

Jack drowns his sorrows. A BEAUTIFUL WOMAN approaches.

WOMAN
Buy a girl a drink?

JACK
I work alone, sweetheart.

WOMAN
We're not so different, you and I.

She reveals she's the killer's daughter seeking revenge.

JACK
This is just the beginning.

They team up reluctantly.

INT. WAREHOUSE - NIGHT

Final confrontation with the VILLAIN.

VILLAIN
(monologuing)
You just don't get it, do you? We're the
same! Join me!

JACK
There's no time to explain why you're wrong!

Big fight. Jack wins. The girl betrays him but then saves
him at the last second.

JACK
I've got a bad feeling about this...

It was all part of a bigger conspiracy!

FADE OUT."""


def create_mixed_originality_screenplay():
    """Create a screenplay mixing original and derivative elements."""
    return """FADE IN:

INT. COFFEE SHOP - DAY

SARAH (30s), our unlikely hero, spills coffee on her laptop.
The screen glitches, revealing code that shouldn't exist.

SARAH
We've got company.
(to herself)
Wait, why did I say that?

The code responds to her confusion, rewriting itself. Other
customers freeze mid-motion.

MYSTERIOUS STRANGER
You shouldn't have seen that.

SARAH
There's no time to explain, is there?

STRANGER
Actually, we have exactly 7 minutes of
exposition time. Tea?

They sit. Time moves in stutters around them.

STRANGER
You're part of a debugging protocol.
This reality has errors.

SARAH
Like The Matrix?

STRANGER
No, like actual debugging. You know coding?

Sarah's memories restructure. She remembers programming
languages that don't exist yet.

SARAH
I do now. The memory injection is crude
but effective.

She touches the frozen world. It pixelates, revealing
infrastructure made of pure mathematics.

FADE OUT."""


def test_basic_originality_analysis():
    """Test basic originality analysis."""
    print("\n✨ TEST 1: Basic Originality Analysis")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_original_screenplay()

    result = dr_meta.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "originality_analysis" in result.__dict__
    assert "original_elements" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Overall originality: {result.originality_analysis.overall_originality:.2f}")
    print(f"✅ Fingerprint: {result.fingerprint}")

    return True


def test_original_element_detection():
    """Test detection of original elements."""
    print("\n✨ TEST 2: Original Element Detection")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_original_screenplay()
    result = dr_meta.analyze(screenplay)

    print(f"🌟 Original elements: {len(result.original_elements)}")

    # Show some original elements
    for element in result.original_elements[:3]:
        print(f"   {element.element_type}: {element.description[:50]}...")
        print(f"      Uniqueness: {element.uniqueness_score:.2f}")

    assert len(result.original_elements) > 0
    print("\n✅ Original element detection working")

    return True


def test_derivative_detection():
    """Test detection of derivative elements."""
    print("\n✨ TEST 3: Derivative Detection")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_derivative_screenplay()
    result = dr_meta.analyze(screenplay)

    print(f"⚠️ Derivative elements: {len(result.derivative_elements)}")

    # Show some derivative elements
    for element in result.derivative_elements[:3]:
        print(f"   {element.element_type}: {element.similarity_to}")
        print(f"      Score: {element.derivative_score:.2f}")

    assert len(result.derivative_elements) > 0
    print("\n✅ Derivative detection working")

    return True


def test_innovation_detection():
    """Test innovation point detection."""
    print("\n✨ TEST 4: Innovation Detection")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_original_screenplay()
    result = dr_meta.analyze(screenplay)

    print(f"💡 Innovation points: {len(result.innovation_points)}")

    for innovation in result.innovation_points:
        print(f"   {innovation.innovation_type}: {innovation.description}")
        print(f"      Impact: {innovation.impact_score:.2f}")

    print("\n✅ Innovation detection working")

    return True


def test_trope_analysis():
    """Test trope usage analysis."""
    print("\n✨ TEST 5: Trope Analysis")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_derivative_screenplay()
    result = dr_meta.analyze(screenplay)

    print(f"📖 Tropes analyzed: {len(result.trope_usage)}")

    for trope in result.trope_usage[:3]:
        print(f"   {trope.trope_name}: {trope.usage_type}")
        print(f"      Freshness: {trope.freshness_score:.2f}")

    print("\n✅ Trope analysis working")

    return True


def test_originality_comparison():
    """Test originality comparison between screenplays."""
    print("\n✨ TEST 6: Originality Comparison")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()

    # Original screenplay
    original = create_original_screenplay()
    original_result = dr_meta.analyze(original)

    # Derivative screenplay
    derivative = create_derivative_screenplay()
    derivative_result = dr_meta.analyze(derivative)

    print(f"🌟 Original screenplay:")
    print(f"   Overall originality: {original_result.originality_analysis.overall_originality:.2f}")
    print(f"   Concept uniqueness: {original_result.originality_analysis.concept_uniqueness:.2f}")

    print(f"\n📋 Derivative screenplay:")
    print(f"   Overall originality: {derivative_result.originality_analysis.overall_originality:.2f}")
    print(f"   Concept uniqueness: {derivative_result.originality_analysis.concept_uniqueness:.2f}")

    # Check that originality metrics are different
    assert original_result.originality_analysis.overall_originality != derivative_result.originality_analysis.overall_originality
    print("\n✅ Originality comparison working")

    return True


def test_creativity_metrics():
    """Test creativity metrics."""
    print("\n✨ TEST 7: Creativity Metrics")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_mixed_originality_screenplay()
    result = dr_meta.analyze(screenplay)

    print(f"🎨 Creative risk: {result.creative_risk_score:.2f}")
    print(f"💰 Commercial viability: {result.commercial_viability:.2f}")
    print(f"🔄 Genre innovation: {result.genre_innovation:.2f}")

    print("\n✅ Creativity metrics working")

    return True


def test_uniqueness_map():
    """Test scene-by-scene uniqueness mapping."""
    print("\n✨ TEST 8: Uniqueness Map")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    screenplay = create_original_screenplay()
    result = dr_meta.analyze(screenplay)

    print("🗺️ Scene uniqueness scores:")
    for scene_key, uniqueness in list(result.uniqueness_map.items())[:3]:
        print(f"   {scene_key}: {uniqueness:.2f}")

    print("\n✅ Uniqueness mapping working")

    return True


def test_rule_violations():
    """Test originality rule violations."""
    print("\n✨ TEST 9: Rule Violations")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()

    # Test with derivative screenplay
    derivative = create_derivative_screenplay()
    result = dr_meta.analyze(derivative)
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
    print("\n✨ TEST 10: Recommendations")
    print("=" * 50)

    dr_meta = DrOriginalityAssessment()
    derivative = create_derivative_screenplay()

    result = dr_meta.analyze(derivative)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations for derivative screenplay
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Metamon tests."""
    print("\n" + "=" * 60)
    print("✨ SCRIPT DOCTOR METAMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Originality Analysis", test_basic_originality_analysis),
        ("Original Element Detection", test_original_element_detection),
        ("Derivative Detection", test_derivative_detection),
        ("Innovation Detection", test_innovation_detection),
        ("Trope Analysis", test_trope_analysis),
        ("Originality Comparison", test_originality_comparison),
        ("Creativity Metrics", test_creativity_metrics),
        ("Uniqueness Map", test_uniqueness_map),
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
        print("\n🎉 SCRIPT DOCTOR METAMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Originality Assessment Specialist is ready")
        print("\n🌟 Originality analysis systems online!")
        print("\n📝 Specialist 21/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)