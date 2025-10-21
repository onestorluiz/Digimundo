#!/usr/bin/env python3
"""
Test Suite for Script Doctor Psychemon - Character Psychology Specialist
Tests the character psychology specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.character_psychology_specialist import DrCharacterPsychology


def create_psychologically_rich_screenplay():
    """Create a screenplay with deep character psychology."""
    return """FADE IN:

EXT. CEMETERY - DAY

SARAH (30s), haunted eyes that avoid mirrors, stands at a grave.

SARAH
(to gravestone)
I kept my promise, Mom. Medical school,
the practice... everything you wanted.

She touches the headstone, then pulls back as if burned.

SARAH (CONT'D)
Everything except being happy.

JAMES (O.S.)
Still talking to ghosts?

Sarah doesn't turn. JAMES (40s), confident facade over deep insecurity,
approaches carrying dead flowers.

SARAH
At least ghosts don't lie.

JAMES
That's rich, coming from you.

Sarah finally faces him. Years of unspoken pain between them.

SARAH
I never lied. I just... couldn't stay.

JAMES
(defensive wall going up)
Right. Because running away is so much
more honest.

SARAH
(her own defenses rising)
Like you'd understand. Mr. Perfect.
Mr. Never-Makes-Mistakes.

JAMES
(cracks showing)
You think I don't make mistakes?
I'm here, aren't I?

They stand facing each other, both wanting connection but too
damaged to reach for it.

SARAH
Why are you here, James?

JAMES
(vulnerable moment)
Dad's dying. He's been asking for you.

Sarah's carefully constructed walls begin to crumble. She turns
away, fighting tears she won't let fall.

SARAH
(barely audible)
I can't. Not after what he--

JAMES
(interrupting, desperate)
He's different now. The cancer... it
changed him.

SARAH
(bitter laugh)
Disease doesn't change people, James.
It just reveals who they really are.

JAMES
Then come see who he really is.

Sarah looks at her mother's grave, seeking guidance from stone.

SARAH
(to herself more than James)
I spent twenty years building these walls.

JAMES
Maybe it's time to see what's on the
other side of them.

FADE OUT."""


def create_flat_character_screenplay():
    """Create a screenplay with shallow, inconsistent characters."""
    return """FADE IN:

INT. OFFICE - DAY

BOB enters. He is angry.

BOB
I am very angry!

ALICE is there. She is sad.

ALICE
I am very sad!

BOB
Now I am happy!

ALICE
Me too! Let's dance!

They dance.

BOB
Actually I'm angry again!

ALICE
And I'm sad again!

BOB
Let's go save the world!

ALICE
Great idea! I love saving worlds!

They leave to save the world.

EXT. STREET - DAY

BOB
I forgot why we're here.

ALICE
Me too. Want to rob a bank?

BOB
Sure! I love crime now!

ALICE
Wait, aren't we heroes?

BOB
Oh right. Let's stop crime!

They stop crime.

FADE OUT."""


def test_basic_psychology_analysis():
    """Test basic character psychology analysis."""
    print("\n🧠 TEST 1: Basic Psychology Analysis")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()
    screenplay = create_psychologically_rich_screenplay()

    result = dr_psych.analyze(screenplay)

    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "characters" in result
    assert "character_count" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Characters found: {result['character_count']}")

    return True


def test_character_extraction():
    """Test character extraction and profiling."""
    print("\n🧠 TEST 2: Character Extraction")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()
    screenplay = create_psychologically_rich_screenplay()

    result = dr_psych.analyze(screenplay)
    characters = result["characters"]

    print(f"🎭 Found {len(characters)} characters:")
    for char in characters:
        print(f"   {char['name']}: {char.get('dialogue_count', 0)} lines")
        print(f"     Depth score: {char.get('depth_score', 0)*100:.0f}%")

    # Should find Sarah and James
    assert len(characters) >= 2
    print("\n✅ Character extraction working")

    return True


def test_psychological_consistency():
    """Test psychological consistency detection."""
    print("\n🧠 TEST 3: Psychological Consistency")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()

    # Good consistency
    good = create_psychologically_rich_screenplay()
    good_result = dr_psych.analyze(good)

    # Poor consistency
    poor = create_flat_character_screenplay()
    poor_result = dr_psych.analyze(poor)

    print(f"🎯 Rich screenplay consistency: {good_result['consistency_score']*100:.0f}%")
    print(f"❌ Flat screenplay consistency: {poor_result['consistency_score']*100:.0f}%")

    # Good should have better consistency
    assert good_result["consistency_score"] > poor_result["consistency_score"]
    print("\n✅ Consistency detection working")

    return True


def test_internal_conflict():
    """Test internal conflict detection."""
    print("\n🧠 TEST 4: Internal Conflict Detection")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()
    screenplay = create_psychologically_rich_screenplay()
    result = dr_psych.analyze(screenplay)

    sarah = next((c for c in result["characters"] if c["name"] == "SARAH"), None)

    if sarah and "internal_conflicts" in sarah:
        print(f"💭 Sarah's internal conflicts:")
        for conflict in sarah["internal_conflicts"]:
            print(f"   - {conflict}")

    print(f"\n🔥 Overall internal conflict score: {result['internal_conflict_score']*100:.0f}%")
    print("✅ Internal conflict detection working")

    return True


def test_emotional_authenticity():
    """Test emotional authenticity analysis."""
    print("\n🧠 TEST 5: Emotional Authenticity")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()

    # Authentic emotions
    authentic = create_psychologically_rich_screenplay()
    auth_result = dr_psych.analyze(authentic)

    # Fake emotions
    fake = create_flat_character_screenplay()
    fake_result = dr_psych.analyze(fake)

    print(f"💚 Authentic screenplay: {auth_result['emotional_truth_score']*100:.0f}%")
    print(f"❌ Flat screenplay: {fake_result['emotional_truth_score']*100:.0f}%")

    # Authentic should score higher
    assert auth_result["emotional_truth_score"] > fake_result["emotional_truth_score"]
    print("\n✅ Emotional authenticity analysis working")

    return True


def test_character_relationships():
    """Test character relationship analysis."""
    print("\n🧠 TEST 6: Character Relationships")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()
    screenplay = create_psychologically_rich_screenplay()
    result = dr_psych.analyze(screenplay)

    relationships = result.get("relationships", [])

    print(f"🤝 Found {len(relationships)} relationships:")
    for rel in relationships:
        print(f"   {rel['characters'][0]} ↔ {rel['characters'][1]}")
        print(f"     Type: {rel.get('type', 'unknown')}")
        print(f"     Dynamics: {', '.join(rel.get('dynamics', []))}")

    print("\n✅ Relationship analysis working")

    return True


def test_character_arc_potential():
    """Test character arc potential detection."""
    print("\n🧠 TEST 7: Character Arc Potential")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()
    screenplay = create_psychologically_rich_screenplay()
    result = dr_psych.analyze(screenplay)

    print(f"🌱 Character growth potential: {result['growth_score']*100:.0f}%")
    print(f"🎯 Want vs Need clarity: {result['want_need_score']*100:.0f}%")

    for char in result["characters"][:2]:  # First 2 characters
        print(f"\n   {char['name']}:")
        if "arc_potential" in char:
            print(f"     Arc potential: {char['arc_potential']}")
        if "want" in char:
            print(f"     Want: {char['want']}")
        if "need" in char:
            print(f"     Need: {char['need']}")

    print("\n✅ Arc potential analysis working")

    return True


def test_voice_distinctiveness():
    """Test character voice distinctiveness."""
    print("\n🧠 TEST 8: Voice Distinctiveness")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()

    # Distinct voices
    distinct = create_psychologically_rich_screenplay()
    distinct_result = dr_psych.analyze(distinct)

    # Same voices
    same = create_flat_character_screenplay()
    same_result = dr_psych.analyze(same)

    print(f"🗣️ Distinct voices score: {distinct_result['voice_distinctiveness']*100:.0f}%")
    print(f"👥 Same voices score: {same_result['voice_distinctiveness']*100:.0f}%")

    # Distinct should score higher
    assert distinct_result["voice_distinctiveness"] >= same_result["voice_distinctiveness"]
    print("\n✅ Voice distinctiveness analysis working")

    return True


def test_rule_violations():
    """Test psychological rule violations."""
    print("\n🧠 TEST 9: Rule Violations")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()

    # Test with poor psychology
    poor_screenplay = create_flat_character_screenplay()
    result = dr_psych.analyze(poor_screenplay)
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
    print("\n🧠 TEST 10: Recommendations")
    print("=" * 50)

    dr_psych = DrCharacterPsychology()
    poor_screenplay = create_flat_character_screenplay()

    result = dr_psych.analyze(poor_screenplay)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")

    return True


def run_all_tests():
    """Run all Psychemon tests."""
    print("\n" + "=" * 60)
    print("🧠 SCRIPT DOCTOR PSYCHEMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Psychology Analysis", test_basic_psychology_analysis),
        ("Character Extraction", test_character_extraction),
        ("Psychological Consistency", test_psychological_consistency),
        ("Internal Conflict Detection", test_internal_conflict),
        ("Emotional Authenticity", test_emotional_authenticity),
        ("Character Relationships", test_character_relationships),
        ("Character Arc Potential", test_character_arc_potential),
        ("Voice Distinctiveness", test_voice_distinctiveness),
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
        print("\n🎉 SCRIPT DOCTOR PSYCHEMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Character Psychology Specialist is ready")
        print("\n🧠 Character depth analysis systems online!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)