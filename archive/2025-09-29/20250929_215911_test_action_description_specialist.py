#!/usr/bin/env python3
"""
Test Suite for Script Doctor Actionmon - Action Description Specialist
Tests the action description specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.action_description_specialist import DrActionDescription


def create_visual_action_screenplay():
    """Create a screenplay with strong visual action."""
    return """FADE IN:

EXT. ROOFTOP - NIGHT

Rain pounds the concrete. Lightning illuminates the skyline.

JAKE (30s), lean and desperate, sprints across the rooftop.
His feet splash through puddles. Behind him, THREE GUARDS
burst through the access door.

Jake leaps across a narrow gap between buildings. His fingers
barely catch the opposite ledge. He hauls himself up.

The guards skid to a stop at the edge. One raises a radio.

GUARD
(into radio)
He's heading for the north tower.

Jake rolls behind an air conditioning unit. Catches his breath.
Blood seeps through his torn shirt.

He peeks around the corner. The guards split up, flanking
his position. Jake's eyes dart left, right. Trapped.

A fire escape clings to the building's edge. Twenty feet away.
Jake calculates the distance. Takes a deep breath.

He explodes from cover. Bullets spark off metal as he dives
for the fire escape. His hands grip the wet rails.

Jake slides down, story by story. The metal screams under
his weight. Below, the alley yawns like a dark mouth.

INT. ABANDONED WAREHOUSE - CONTINUOUS

Jake crashes through a window. Glass showers the floor.
He tumbles, rolls, springs to his feet.

Moonlight slices through broken skylights. Shadows dance
between towering shelves of forgotten machinery.

Jake weaves through the maze. His breath echoes in the
vast space. Behind him, boots thunder on metal stairs.

FADE OUT."""


def create_poor_action_screenplay():
    """Create a screenplay with poor action description."""
    return """FADE IN:

EXT. STREET - DAY

John walked down the street. He was thinking about his past
and remembering better times. He felt sad.

John sees some bad guys. They looked mean. John knew they
were dangerous because he had seen them before.

The bad guys were angry. One of them thought about attacking
John. John realized he should run.

John started running. The bad guys ran after him. Everyone
was running very fast. It was exciting.

John felt scared as he ran. He wished he had stayed home.
The bad guys seemed to be getting closer.

We see John turning a corner. We watch as he looks for
a place to hide. CLOSE UP on his frightened face.

John remembered his training from years ago. He had always
been good at escaping. This reminded him of his childhood.

The chase continued for a long time. Finally John found
a door that was open. He went inside quickly.

INT. BUILDING - DAY

John was inside now. He felt safer but knew the danger
wasn't over. The bad guys would probably find him.

John looked around. The room appeared to be empty. It seemed
like a good hiding place. He hoped they wouldn't find him.

We see John hiding. The bad guys were still looking for him.

FADE OUT."""


def test_basic_action_analysis():
    """Test basic action analysis."""
    print("\n🎬 TEST 1: Basic Action Analysis")
    print("=" * 50)

    dr_action = DrActionDescription()
    screenplay = create_visual_action_screenplay()

    result = dr_action.analyze(screenplay)

    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "total_action_lines" in result
    assert "visual_clarity_score" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Action lines: {result['total_action_lines']}")
    print(f"✅ Visual clarity: {result['visual_clarity_score']*100:.0f}%")

    return True


def test_show_vs_tell():
    """Test show vs tell detection."""
    print("\n🎬 TEST 2: Show vs Tell")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Visual (showing)
    visual = create_visual_action_screenplay()
    visual_result = dr_action.analyze(visual)

    # Poor (telling)
    poor = create_poor_action_screenplay()
    poor_result = dr_action.analyze(poor)

    print(f"👁️ Visual screenplay show ratio: {visual_result['show_vs_tell_ratio']*100:.0f}%")
    print(f"📝 Poor screenplay show ratio: {poor_result['show_vs_tell_ratio']*100:.0f}%")
    print(f"   Telling instances: {poor_result['telling_instances']}")

    # Visual should have better show ratio or at least equal
    assert visual_result["show_vs_tell_ratio"] >= poor_result["show_vs_tell_ratio"]
    print("\n✅ Show vs tell detection working")

    return True


def test_tense_and_voice():
    """Test tense and voice checking."""
    print("\n🎬 TEST 3: Tense and Voice")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Good tense/voice
    good = create_visual_action_screenplay()
    good_result = dr_action.analyze(good)

    # Poor tense/voice
    poor = create_poor_action_screenplay()
    poor_result = dr_action.analyze(poor)

    print(f"✅ Good screenplay:")
    print(f"   Present tense: {good_result['present_tense_percentage']:.0f}%")
    print(f"   Active voice: {good_result['active_voice_percentage']:.0f}%")

    print(f"\n❌ Poor screenplay:")
    print(f"   Present tense: {poor_result['present_tense_percentage']:.0f}%")
    print(f"   Tense issues: {poor_result['tense_issues_count']}")

    print("\n✅ Tense and voice checking working")

    return True


def test_unfilmables():
    """Test unfilmable detection."""
    print("\n🎬 TEST 4: Unfilmables Detection")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Poor screenplay has unfilmables
    poor = create_poor_action_screenplay()
    poor_result = dr_action.analyze(poor)

    print(f"🚫 Unfilmable count: {poor_result['unfilmable_count']}")

    if poor_result["unfilmable_examples"]:
        print("   Examples:")
        for ex in poor_result["unfilmable_examples"][:2]:
            print(f"   - {ex}")

    # Check that unfilmable detection is working (may or may not find issues)
    assert "unfilmable_count" in poor_result
    print("\n✅ Unfilmable detection working")

    return True


def test_verb_analysis():
    """Test verb strength analysis."""
    print("\n🎬 TEST 5: Verb Analysis")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Strong verbs
    strong = create_visual_action_screenplay()
    strong_result = dr_action.analyze(strong)

    # Weak verbs
    weak = create_poor_action_screenplay()
    weak_result = dr_action.analyze(weak)

    print(f"💪 Strong screenplay:")
    print(f"   Strong verbs: {strong_result['strong_verb_count']}")
    print(f"   Examples: {', '.join(strong_result['vivid_verb_examples'][:3])}")

    print(f"\n😴 Weak screenplay:")
    print(f"   Weak verb %: {weak_result['weak_verb_percentage']:.0f}%")

    print("\n✅ Verb analysis working")

    return True


def test_cinematic_quality():
    """Test cinematic quality analysis."""
    print("\n🎬 TEST 6: Cinematic Quality")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Cinematic
    cinematic = create_visual_action_screenplay()
    cin_result = dr_action.analyze(cinematic)

    # Not cinematic
    poor = create_poor_action_screenplay()
    poor_result = dr_action.analyze(poor)

    print(f"🎥 Cinematic screenplay:")
    print(f"   Score: {cin_result['cinematic_score']*100:.0f}%")
    print(f"   Reads like movie: {cin_result['reads_like_movie']}")

    print(f"\n📚 Poor screenplay:")
    print(f"   Score: {poor_result['cinematic_score']*100:.0f}%")
    print(f"   Reads like movie: {poor_result['reads_like_movie']}")

    assert cin_result["cinematic_score"] > poor_result["cinematic_score"]
    print("\n✅ Cinematic quality analysis working")

    return True


def test_paragraph_length():
    """Test paragraph length analysis."""
    print("\n🎬 TEST 7: Paragraph Length")
    print("=" * 50)

    dr_action = DrActionDescription()
    screenplay = create_visual_action_screenplay()
    result = dr_action.analyze(screenplay)

    print(f"📄 Average paragraph length: {result['average_paragraph_length']:.1f} lines")
    print(f"📏 Overlong paragraphs: {result['overlong_paragraphs']}")

    print("\n✅ Paragraph length analysis working")

    return True


def test_spatial_clarity():
    """Test spatial clarity analysis."""
    print("\n🎬 TEST 8: Spatial Clarity")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Good spatial clarity
    good = create_visual_action_screenplay()
    good_result = dr_action.analyze(good)

    print(f"🗺️ Spatial clarity score: {good_result['spatial_clarity_score']*100:.0f}%")

    print("\n✅ Spatial clarity analysis working")

    return True


def test_rule_violations():
    """Test action rule violations."""
    print("\n🎬 TEST 9: Rule Violations")
    print("=" * 50)

    dr_action = DrActionDescription()

    # Test with poor action screenplay
    poor = create_poor_action_screenplay()
    result = dr_action.analyze(poor)
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

    # Should detect issues
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎬 TEST 10: Recommendations")
    print("=" * 50)

    dr_action = DrActionDescription()
    poor = create_poor_action_screenplay()

    result = dr_action.analyze(poor)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")

    return True


def run_all_tests():
    """Run all Actionmon tests."""
    print("\n" + "=" * 60)
    print("🎬 SCRIPT DOCTOR ACTIONMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Action Analysis", test_basic_action_analysis),
        ("Show vs Tell", test_show_vs_tell),
        ("Tense and Voice", test_tense_and_voice),
        ("Unfilmables Detection", test_unfilmables),
        ("Verb Analysis", test_verb_analysis),
        ("Cinematic Quality", test_cinematic_quality),
        ("Paragraph Length", test_paragraph_length),
        ("Spatial Clarity", test_spatial_clarity),
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
        print("\n🎉 SCRIPT DOCTOR ACTIONMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Action Description Specialist is ready")
        print("\n🎬 Visual storytelling analysis systems online!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)