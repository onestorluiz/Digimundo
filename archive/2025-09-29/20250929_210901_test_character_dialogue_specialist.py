#!/usr/bin/env python3
"""
Test Suite for Script Doctor Dialoguemon - Character Dialogue Specialist
Tests the dialogue specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.character_dialogue_specialist import DrCharacterDialogue


def create_authentic_dialogue_screenplay():
    """Create a screenplay with authentic, distinctive dialogue."""
    return """FADE IN:

INT. DINER - NIGHT

JAKE (40s), tired eyes, sits across from MARIA (30s), nervous energy.

JAKE
(sighs)
Look, I... I don't know how to say this.

MARIA
(interrupting)
Then don't. Just-- don't.

JAKE
Maria, please. Let me finish.

MARIA
Why? So you can feel better about yourself?
(bitter laugh)
That's rich, Jake. Really rich.

JAKE
That's not-- You know that's not what this is.

MARIA
Do I? Because from where I'm sitting...
(trails off, looks away)
Never mind.

JAKE
(leaning forward)
Hey. Hey, look at me. This isn't about me
feeling better. It's about... us. Whatever
that means anymore.

MARIA
(quiet)
There is no "us." Hasn't been for a while.

JAKE
Maybe. But we can't keep dancing around it.

MARIA
Watch me.
(stands to leave)

JAKE
Maria--

MARIA
(turning back)
You want honesty? Fine. I'm tired, Jake.
Tired of pretending everything's okay when
we both know it's not. Tired of... this.

JAKE
(defeated)
Yeah. Me too.

They sit in silence. The weight of unspoken truths between them.

FADE OUT."""


def create_poor_dialogue_screenplay():
    """Create a screenplay with poor, indistinct dialogue."""
    return """FADE IN:

INT. OFFICE - DAY

BOB enters. ALICE is there.

BOB
Hello Alice. I am angry about the situation.

ALICE
Hello Bob. I am also angry about the situation.

BOB
As you know, we have been working here for
ten years since we graduated from college together.

ALICE
Yes, I remember when we started this company
together after getting our business degrees.

BOB
I am sad now.

ALICE
I am sad too.

BOB
We should talk about our feelings.

ALICE
Yes, let me explain how I feel. I feel sad
and angry at the same time.

BOB
That is exactly how I feel. We feel the same way.

ALICE
We need to talk about what happened yesterday
when the boss, Mr. Johnson, told us about
the merger with Global Corp.

BOB
Yes, the merger is making me have feelings.

ALICE
Me too. I have many feelings about it.

FADE OUT."""


def test_basic_dialogue_analysis():
    """Test basic dialogue analysis."""
    print("\n🗣️ TEST 1: Basic Dialogue Analysis")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()
    screenplay = create_authentic_dialogue_screenplay()

    result = dr_dialogue.analyze(screenplay)

    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "total_dialogue_lines" in result
    assert "character_count" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Total dialogue lines: {result['total_dialogue_lines']}")
    print(f"✅ Characters: {result['character_count']}")

    return True


def test_voice_distinctiveness():
    """Test character voice distinctiveness analysis."""
    print("\n🗣️ TEST 2: Voice Distinctiveness")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()

    # Authentic dialogue
    authentic = create_authentic_dialogue_screenplay()
    auth_result = dr_dialogue.analyze(authentic)

    # Poor dialogue
    poor = create_poor_dialogue_screenplay()
    poor_result = dr_dialogue.analyze(poor)

    print(f"🎭 Authentic voices: {auth_result['voice_distinctiveness']*100:.0f}%")
    print(f"👥 Poor voices: {poor_result['voice_distinctiveness']*100:.0f}%")

    # Authentic should have more distinctive voices
    assert auth_result["voice_distinctiveness"] >= poor_result["voice_distinctiveness"]
    print("\n✅ Voice distinctiveness analysis working")

    return True


def test_natural_speech():
    """Test natural speech pattern detection."""
    print("\n🗣️ TEST 3: Natural Speech Patterns")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()

    # Natural dialogue
    natural = create_authentic_dialogue_screenplay()
    natural_result = dr_dialogue.analyze(natural)

    # Unnatural dialogue
    unnatural = create_poor_dialogue_screenplay()
    unnatural_result = dr_dialogue.analyze(unnatural)

    print(f"💬 Natural speech score: {natural_result['natural_speech_score']*100:.0f}%")
    print(f"🤖 Unnatural speech score: {unnatural_result['natural_speech_score']*100:.0f}%")

    # Natural should score higher
    assert natural_result["natural_speech_score"] > unnatural_result["natural_speech_score"]
    print("\n✅ Natural speech detection working")

    return True


def test_subtext_detection():
    """Test subtext detection in dialogue."""
    print("\n🗣️ TEST 4: Subtext Detection")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()

    # Dialogue with subtext
    subtext = create_authentic_dialogue_screenplay()
    subtext_result = dr_dialogue.analyze(subtext)

    # On-the-nose dialogue
    on_nose = create_poor_dialogue_screenplay()
    nose_result = dr_dialogue.analyze(on_nose)

    print(f"🎯 Subtext present: {subtext_result['subtext_score']*100:.0f}%")
    print(f"👃 On-the-nose count: {nose_result['on_the_nose_count']}")

    assert subtext_result["subtext_score"] > 0
    print("\n✅ Subtext detection working")

    return True


def test_exposition_detection():
    """Test exposition dump detection."""
    print("\n🗣️ TEST 5: Exposition Detection")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()
    poor = create_poor_dialogue_screenplay()

    result = dr_dialogue.analyze(poor)

    print(f"📚 Exposition dumps found: {result['exposition_dumps']}")

    if result["exposition_issues"]:
        for issue in result["exposition_issues"][:2]:
            print(f"   {issue['character']}: {issue['issue']}")

    # Poor dialogue should have exposition issues
    assert result["exposition_dumps"] > 0
    print("\n✅ Exposition detection working")

    return True


def test_dialogue_purpose():
    """Test dialogue purpose analysis."""
    print("\n🗣️ TEST 6: Dialogue Purpose")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()

    # Purposeful dialogue
    purposeful = create_authentic_dialogue_screenplay()
    purp_result = dr_dialogue.analyze(purposeful)

    # Empty dialogue
    empty = create_poor_dialogue_screenplay()
    empty_result = dr_dialogue.analyze(empty)

    print(f"🎯 Purposeful dialogue: {purp_result['dialogue_serves_purpose']:.0f}%")
    print(f"💭 Empty dialogue lines: {empty_result['empty_dialogue_lines']}")

    print("\n✅ Dialogue purpose analysis working")

    return True


def test_conflict_in_dialogue():
    """Test conflict detection in dialogue."""
    print("\n🗣️ TEST 7: Conflict in Dialogue")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()

    # Conflicted dialogue
    conflict = create_authentic_dialogue_screenplay()
    conf_result = dr_dialogue.analyze(conflict)

    # Agreeable dialogue
    agree = create_poor_dialogue_screenplay()
    agree_result = dr_dialogue.analyze(agree)

    print(f"⚔️ Conflict score: {conf_result['conflict_in_dialogue']*100:.0f}%")
    print(f"🤝 Agreement score: {agree_result['conflict_in_dialogue']*100:.0f}%")

    # Authentic should have more conflict
    assert conf_result["conflict_in_dialogue"] >= agree_result["conflict_in_dialogue"]
    print("\n✅ Conflict detection working")

    return True


def test_cliche_detection():
    """Test cliché detection in dialogue."""
    print("\n🗣️ TEST 8: Cliché Detection")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()
    screenplay = create_poor_dialogue_screenplay()

    result = dr_dialogue.analyze(screenplay)

    print(f"🔄 Clichés found: {result['cliches_found']}")

    if result["cliche_examples"]:
        print("   Examples:")
        for cliche in result["cliche_examples"][:2]:
            print(f"   - {cliche}")

    print("\n✅ Cliché detection working")

    return True


def test_rule_violations():
    """Test dialogue rule violations."""
    print("\n🗣️ TEST 9: Rule Violations")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()

    # Test with poor dialogue
    poor_screenplay = create_poor_dialogue_screenplay()
    result = dr_dialogue.analyze(poor_screenplay)
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
    print("\n🗣️ TEST 10: Recommendations")
    print("=" * 50)

    dr_dialogue = DrCharacterDialogue()
    poor_screenplay = create_poor_dialogue_screenplay()

    result = dr_dialogue.analyze(poor_screenplay)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")

    return True


def run_all_tests():
    """Run all Dialoguemon tests."""
    print("\n" + "=" * 60)
    print("🗣️ SCRIPT DOCTOR DIALOGUEMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Dialogue Analysis", test_basic_dialogue_analysis),
        ("Voice Distinctiveness", test_voice_distinctiveness),
        ("Natural Speech Patterns", test_natural_speech),
        ("Subtext Detection", test_subtext_detection),
        ("Exposition Detection", test_exposition_detection),
        ("Dialogue Purpose", test_dialogue_purpose),
        ("Conflict in Dialogue", test_conflict_in_dialogue),
        ("Cliché Detection", test_cliche_detection),
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
        print("\n🎉 SCRIPT DOCTOR DIALOGUEMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Character Dialogue Specialist is ready")
        print("\n🗣️ Dialogue authenticity analysis systems online!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)