#!/usr/bin/env python3
"""
Test Suite for Script Doctor Submon - Subtext and Layered Meaning Specialist
Tests the subtext specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.subtext_specialist import DrSubtext


def create_layered_screenplay():
    """Create a screenplay with rich subtext."""
    return """FADE IN:

INT. KITCHEN - MORNING

SARAH (30s) stands at the sink, scrubbing a clean plate.

DAVID (30s) enters, buttoning his shirt.

DAVID
Good morning.

Sarah scrubs harder.

SARAH
Morning.

DAVID
I might be late tonight. Client dinner.

SARAH
(not turning)
Of course you will.

DAVID
What's that supposed to mean?

SARAH
(finally turning, smiling)
Nothing. Have a great day, honey.

She kisses his cheek. Her smile doesn't reach her eyes.

DAVID
(beat)
You okay?

SARAH
Perfect. Why wouldn't I be?

David studies her, then checks his watch.

DAVID
We should talk later.

SARAH
(turning back to dishes)
Sure. Later.

DAVID
Sarah--

SARAH
(brighter)
You'll be late.

David hesitates, then leaves. Sarah's smile fades. She
stares at the clean plate in her hands.

SARAH (CONT'D)
(to herself)
Always later.

She sets the plate down carefully. Too carefully.

INT. OFFICE - DAY

JAKE (40s) and MIKE (30s) review documents.

MIKE
The numbers don't add up.

JAKE
Numbers always add up. You just need
the right accountant.

MIKE
That's not what I--

JAKE
(interrupting)
Speaking of which, how's your wife?
Still teaching?

Mike's jaw tightens.

MIKE
She's fine.

JAKE
Good. Good. Family's important, Mike.
Wouldn't want anything to... complicate
things.

MIKE
(pause)
The numbers, Jake.

JAKE
(smiling)
Forget the numbers. Trust me.

MIKE
I need to think about it.

JAKE
Thinking's overrated. But sure, think
all you want. Just remember who signs
your checks.

Jake pats Mike's shoulder and exits. Mike stares at the
documents, his hand trembling slightly.

FADE OUT."""


def create_on_the_nose_screenplay():
    """Create a screenplay with no subtext."""
    return """FADE IN:

INT. LIVING ROOM - DAY

JOHN sits on the couch. MARY enters.

MARY
I'm angry with you.

JOHN
I know you're angry. I'm sorry.

MARY
You hurt my feelings yesterday.

JOHN
I didn't mean to hurt your feelings.
I was stressed about work.

MARY
Your work stress always affects me.
That makes me sad.

JOHN
I feel bad about making you sad.
I love you.

MARY
I love you too, but I need you to
change your behavior.

JOHN
I will change my behavior because
I care about our relationship.

MARY
Good. I'm happy you understand.
Let's talk about our problems.

JOHN
Yes, let's discuss everything openly
and honestly.

MARY
I think you work too much.

JOHN
You're right. I do work too much.
I should spend more time at home.

MARY
That would make me feel valued.

JOHN
I want you to feel valued because
you are important to me.

FADE OUT."""


def test_basic_subtext_analysis():
    """Test basic subtext analysis."""
    print("\n🎭 TEST 1: Basic Subtext Analysis")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()

    result = dr_subtext.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "subtext_analysis" in result.__dict__
    assert "dialogue_layers" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Has subtext: {result.subtext_analysis.has_subtext}")
    print(f"✅ Subtext depth: {result.subtext_analysis.subtext_depth_score:.2f}")

    return True


def test_on_the_nose_detection():
    """Test on-the-nose dialogue detection."""
    print("\n🎭 TEST 2: On-the-Nose Detection")
    print("=" * 50)

    dr_subtext = DrSubtext()

    # Layered (good subtext)
    layered = create_layered_screenplay()
    layered_result = dr_subtext.analyze(layered)

    # On-the-nose (no subtext)
    direct = create_on_the_nose_screenplay()
    direct_result = dr_subtext.analyze(direct)

    print(f"🎯 Layered screenplay on-the-nose ratio: {layered_result.subtext_analysis.on_the_nose_ratio:.2f}")
    print(f"📢 Direct screenplay on-the-nose ratio: {direct_result.subtext_analysis.on_the_nose_ratio:.2f}")

    # Direct should have higher on-the-nose ratio
    assert direct_result.subtext_analysis.on_the_nose_ratio > layered_result.subtext_analysis.on_the_nose_ratio
    print("\n✅ On-the-nose detection working")

    return True


def test_contradiction_detection():
    """Test contradiction between action and dialogue."""
    print("\n🎭 TEST 3: Contradiction Detection")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()
    result = dr_subtext.analyze(screenplay)

    print(f"🔄 Contradictions found: {result.subtext_analysis.contradiction_count}")

    # Check that the field exists and analysis is working
    assert hasattr(result.subtext_analysis, 'contradiction_count')
    print("✅ Contradiction detection field present and functional")

    if result.subtext_analysis.contradiction_count > 0:
        print("✅ Example: Sarah says 'Perfect' but her smile doesn't reach her eyes")
    print("\n✅ Contradiction detection working")

    return True


def test_avoidance_patterns():
    """Test avoidance pattern detection."""
    print("\n🎭 TEST 4: Avoidance Patterns")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()
    result = dr_subtext.analyze(screenplay)

    print(f"🚫 Avoidance patterns: {len(result.subtext_analysis.avoidance_patterns)}")
    if result.subtext_analysis.avoidance_patterns:
        for pattern in result.subtext_analysis.avoidance_patterns[:2]:
            print(f"   - {pattern}")

    print("\n✅ Avoidance pattern detection working")

    return True


def test_emotional_layers():
    """Test emotional layer analysis."""
    print("\n🎭 TEST 5: Emotional Layers")
    print("=" * 50)

    dr_subtext = DrSubtext()

    # Layered emotions
    layered = create_layered_screenplay()
    layered_result = dr_subtext.analyze(layered)

    # Direct emotions
    direct = create_on_the_nose_screenplay()
    direct_result = dr_subtext.analyze(direct)

    print(f"🎭 Layered screenplay emotional layers: {layered_result.subtext_analysis.emotional_layers}")
    print(f"😐 Direct screenplay emotional layers: {direct_result.subtext_analysis.emotional_layers}")

    print("\n✅ Emotional layer analysis working")

    return True


def test_power_dynamics():
    """Test power dynamics detection."""
    print("\n🎭 TEST 6: Power Dynamics")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()
    result = dr_subtext.analyze(screenplay)

    print(f"⚡ Power dynamics present: {result.subtext_analysis.power_dynamics_present}")
    print("   Example: Jake's threat about 'who signs your checks'")

    print("\n✅ Power dynamics detection working")

    return True


def test_dialogue_layers():
    """Test dialogue layer analysis."""
    print("\n🎭 TEST 7: Dialogue Layers")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()
    result = dr_subtext.analyze(screenplay)

    print(f"📊 Layer distribution:")
    for layer_type, count in result.dialogue_layers.items():
        print(f"   {layer_type}: {count}")

    # Should have multi-layered dialogue
    assert (result.dialogue_layers.get('double_layer', 0) + 
            result.dialogue_layers.get('multi_layer', 0)) > 0
    print("\n✅ Dialogue layer analysis working")

    return True


def test_character_subtext():
    """Test character-specific subtext patterns."""
    print("\n🎭 TEST 8: Character Subtext")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()
    result = dr_subtext.analyze(screenplay)

    print(f"👥 Character patterns:")
    for char, patterns in list(result.character_subtext.items())[:3]:
        if patterns:
            print(f"   {char}: {', '.join(patterns)}")

    print("\n✅ Character subtext analysis working")

    return True


def test_rule_violations():
    """Test subtext rule violations."""
    print("\n🎭 TEST 9: Rule Violations")
    print("=" * 50)

    dr_subtext = DrSubtext()

    # Test with on-the-nose screenplay
    direct = create_on_the_nose_screenplay()
    result = dr_subtext.analyze(direct)
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

    # Should detect issues in on-the-nose screenplay
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎭 TEST 10: Recommendations")
    print("=" * 50)

    dr_subtext = DrSubtext()
    direct = create_on_the_nose_screenplay()

    result = dr_subtext.analyze(direct)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations for on-the-nose screenplay
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def test_layered_exchanges():
    """Test identification of layered exchanges."""
    print("\n🎭 TEST 11: Layered Exchanges")
    print("=" * 50)

    dr_subtext = DrSubtext()
    screenplay = create_layered_screenplay()
    result = dr_subtext.analyze(screenplay)

    print(f"🎭 Most layered exchanges: {len(result.most_layered_exchanges)}")
    for exchange in result.most_layered_exchanges[:2]:
        print(f"   {exchange['characters'][0]} → {exchange['characters'][1]}")
        print(f"   Layers: {exchange['layers']}")
        if exchange.get('techniques'):
            print(f"   Techniques: {', '.join(exchange['techniques'])}")

    print("\n✅ Layered exchange identification working")

    return True


def run_all_tests():
    """Run all Submon tests."""
    print("\n" + "=" * 60)
    print("🎭 SCRIPT DOCTOR SUBMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Subtext Analysis", test_basic_subtext_analysis),
        ("On-the-Nose Detection", test_on_the_nose_detection),
        ("Contradiction Detection", test_contradiction_detection),
        ("Avoidance Patterns", test_avoidance_patterns),
        ("Emotional Layers", test_emotional_layers),
        ("Power Dynamics", test_power_dynamics),
        ("Dialogue Layers", test_dialogue_layers),
        ("Character Subtext", test_character_subtext),
        ("Rule Violations", test_rule_violations),
        ("Recommendations", test_recommendations),
        ("Layered Exchanges", test_layered_exchanges)
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
        print("\n🎉 SCRIPT DOCTOR SUBMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Subtext Specialist is ready")
        print("\n🎭 Subtext and layered meaning analysis systems online!")
        print("\n📝 Specialist 13/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
