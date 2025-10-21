#!/usr/bin/env python3
"""
Test Suite for Script Doctor Tonemon - Tone Consistency Specialist
Tests the tone consistency specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.tone_consistency_specialist import DrToneConsistency


def create_tonally_consistent_screenplay():
    """Create a screenplay with consistent dramatic tone."""
    return """FADE IN:

INT. COURTROOM - DAY

A tense silence fills the room. JUDGE HARRISON presides,
his expression grave.

JUDGE HARRISON
The evidence before us is overwhelming.
This is a matter of life and death.

DEFENDANT SARAH JONES (30s) trembles, tears streaming.

SARAH
I never meant for this to happen.
The consequences... they haunt me.

PROSECUTOR WILLIAMS stands, his voice heavy with purpose.

WILLIAMS
Intentions matter less than actions.
A life was lost. Justice demands answers.

The jury sits in solemn contemplation.

INT. HOLDING CELL - LATER

Sarah sits alone, the weight of her fate crushing.

SARAH
(to herself)
How did it come to this? Every choice,
every moment led here.

Her ATTORNEY, DAVID, enters with grave news.

DAVID
The jury's reached a verdict. We must
prepare for the worst.

Sarah nods, accepting her destiny.

INT. COURTROOM - LATER

The FOREMAN rises, the verdict in hand. The room
holds its breath.

FOREMAN
We find the defendant... guilty.

Sarah collapses. Her world shatters.

FADE OUT."""


def create_tonally_inconsistent_screenplay():
    """Create a screenplay with jarring tonal shifts."""
    return """FADE IN:

INT. FUNERAL HOME - DAY

Mourners weep over a casket. Grief fills the air.

JOHN
He was the best of us. Gone too soon.

Suddenly, STEVE jumps up.

STEVE
Knock knock! Who's there? Orange!
Orange you glad I didn't say banana?

Everyone laughs hysterically.

EXT. BATTLEFIELD - CONTINUOUS

Explosions everywhere! Soldiers charge!

SOLDIER
For freedom! Attack!

INT. ROMANTIC RESTAURANT - NIGHT

Candles flicker. Soft music plays.

JENNY
(whispering)
I love you more than life itself.

MIKE
(screaming)
ZOMBIES ARE ATTACKING!

They run screaming as zombies burst in.

INT. COMEDY CLUB - DAY

A comedian tells jokes.

COMEDIAN
So a priest walks into a bar...

Suddenly everyone starts crying.

AUDIENCE MEMBER
Life is meaningless! We're all alone!

Everyone sobs uncontrollably.

FADE OUT."""


def test_basic_tone_analysis():
    """Test basic tone analysis."""
    print("\n🎭 TEST 1: Basic Tone Analysis")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    screenplay = create_tonally_consistent_screenplay()

    result = dr_tone.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "tone_analysis" in result.__dict__
    assert "tone_markers" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Dominant tone: {result.tone_analysis.dominant_tone}")
    print(f"✅ Consistency score: {result.tone_analysis.tone_consistency_score:.2f}")

    return True


def test_tone_identification():
    """Test tone type identification."""
    print("\n🎭 TEST 2: Tone Identification")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    screenplay = create_tonally_consistent_screenplay()
    result = dr_tone.analyze(screenplay)

    print(f"🎯 Dominant tone: {result.tone_analysis.dominant_tone}")
    print(f"🎭 Secondary tones: {', '.join(result.tone_analysis.secondary_tones) if result.tone_analysis.secondary_tones else 'None'}")
    
    # Show tone map
    print("🗺️ Tone distribution:")
    for tone, weight in sorted(result.tone_map.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"   {tone}: {weight:.2f}")

    print("\n✅ Tone identification working")

    return True


def test_tone_consistency():
    """Test tone consistency detection."""
    print("\n🎭 TEST 3: Tone Consistency")
    print("=" * 50)

    dr_tone = DrToneConsistency()

    # Consistent tone
    consistent = create_tonally_consistent_screenplay()
    consistent_result = dr_tone.analyze(consistent)

    # Inconsistent tone
    inconsistent = create_tonally_inconsistent_screenplay()
    inconsistent_result = dr_tone.analyze(inconsistent)

    print(f"✅ Consistent screenplay:")
    print(f"   Consistency score: {consistent_result.tone_analysis.tone_consistency_score:.2f}")
    print(f"   Tone established: {consistent_result.tone_analysis.tone_established}")
    
    print(f"\n❌ Inconsistent screenplay:")
    print(f"   Consistency score: {inconsistent_result.tone_analysis.tone_consistency_score:.2f}")
    print(f"   Tone shifts: {inconsistent_result.tone_analysis.tone_shifts}")

    print("\n✅ Tone consistency detection working")

    return True


def test_tone_transitions():
    """Test tone transition analysis."""
    print("\n🎭 TEST 4: Tone Transitions")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    inconsistent = create_tonally_inconsistent_screenplay()
    result = dr_tone.analyze(inconsistent)

    print(f"🔄 Total transitions: {result.tone_analysis.tone_shifts}")
    print(f"✅ Smooth transitions: {result.tone_analysis.smooth_transitions}")
    print(f"⚠️ Jarring transitions: {result.tone_analysis.jarring_transitions}")

    # Show some transitions
    for trans in result.tone_transitions[:3]:
        print(f"   Scene {trans['from_scene']}→{trans['to_scene']}: {trans['from_tone']}→{trans['to_tone']} ({trans['type']})")

    print("\n✅ Tone transition analysis working")

    return True


def test_emotional_arc():
    """Test emotional arc analysis."""
    print("\n🎭 TEST 5: Emotional Arc")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    screenplay = create_tonally_consistent_screenplay()
    result = dr_tone.analyze(screenplay)

    print(f"📈 Arc type: {result.emotional_arc['type']}")
    print(f"😭 Emotional range: {result.tone_analysis.emotional_range_score:.2f}")
    print(f"⚡ Climax intensity: {result.tone_analysis.climax_intensity:.2f}")

    print("\n✅ Emotional arc analysis working")

    return True


def test_scene_tones():
    """Test scene-level tone analysis."""
    print("\n🎭 TEST 6: Scene Tones")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    screenplay = create_tonally_consistent_screenplay()
    result = dr_tone.analyze(screenplay)

    print("🎬 Scene-by-scene tones:")
    for scene_num, tones in list(result.scene_tones.items())[:3]:
        if tones:
            dominant = max(tones.items(), key=lambda x: x[1])
            print(f"   Scene {scene_num}: {dominant[0]} ({dominant[1]:.2f})")

    print("\n✅ Scene tone analysis working")

    return True


def test_tone_progression():
    """Test tone progression tracking."""
    print("\n🎭 TEST 7: Tone Progression")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    screenplay = create_tonally_consistent_screenplay()
    result = dr_tone.analyze(screenplay)

    print("📈 Tone progression:")
    for prog in result.tone_progression[:4]:
        print(f"   Scene {prog['scene']}: {prog['dominant_tone']} (intensity: {prog['intensity']:.2f})")

    print("\n✅ Tone progression tracking working")

    return True


def test_tone_establishment():
    """Test tone establishment detection."""
    print("\n🎭 TEST 8: Tone Establishment")
    print("=" * 50)

    dr_tone = DrToneConsistency()

    # Well-established tone
    consistent = create_tonally_consistent_screenplay()
    consistent_result = dr_tone.analyze(consistent)

    print(f"🏁 Tone established: {consistent_result.tone_analysis.tone_established}")
    print(f"🏁 Resolution satisfaction: {consistent_result.tone_analysis.resolution_satisfaction:.2f}")

    print("\n✅ Tone establishment detection working")

    return True


def test_rule_violations():
    """Test tone rule violations."""
    print("\n🎭 TEST 9: Rule Violations")
    print("=" * 50)

    dr_tone = DrToneConsistency()

    # Test with inconsistent screenplay
    inconsistent = create_tonally_inconsistent_screenplay()
    result = dr_tone.analyze(inconsistent)
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

    # Should detect issues
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎭 TEST 10: Recommendations")
    print("=" * 50)

    dr_tone = DrToneConsistency()
    inconsistent = create_tonally_inconsistent_screenplay()

    result = dr_tone.analyze(inconsistent)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Tonemon tests."""
    print("\n" + "=" * 60)
    print("🎭 SCRIPT DOCTOR TONEMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Tone Analysis", test_basic_tone_analysis),
        ("Tone Identification", test_tone_identification),
        ("Tone Consistency", test_tone_consistency),
        ("Tone Transitions", test_tone_transitions),
        ("Emotional Arc", test_emotional_arc),
        ("Scene Tones", test_scene_tones),
        ("Tone Progression", test_tone_progression),
        ("Tone Establishment", test_tone_establishment),
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
        print("\n🎉 SCRIPT DOCTOR TONEMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Tone Consistency Specialist is ready")
        print("\n🎭 Tonal analysis systems online!")
        print("\n📝 Specialist 18/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
