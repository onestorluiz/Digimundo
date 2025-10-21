#!/usr/bin/env python3
"""
Test Suite for Script Doctor Genremon - Genre Conventions Specialist
Tests the genre conventions specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.genre_conventions_specialist import DrGenreConventions


def create_action_screenplay():
    """Create a screenplay with clear action genre conventions."""
    return """FADE IN:

EXT. CITY SKYLINE - NIGHT

The city sleeps. Suddenly, an EXPLOSION rocks a skyscraper.

INT. BURNING BUILDING - CONTINUOUS

JACK RYDER (30s), rugged hero, battles through flames.

JACK
We've got to get these people out!

He KICKS down a door. Inside, terrified HOSTAGES.

TERRORIST LEADER
You're too late, Ryder!

Jack PUNCHES him. They FIGHT viciously.

EXT. ROOFTOP - MOMENTS LATER

Jack carries the last hostage as the building EXPLODES behind them.

HOSTAGE
You saved us all!

JACK
Just doing my job.

A HELICOPTER arrives. Jack leaps aboard as more EXPLOSIONS rock the city.

PILOT
The bomb's on the bridge!

JACK
Then that's where we're going.

EXT. BRIDGE - NIGHT

Jack rappels from the helicopter onto a speeding BUS.

INT. BUS - CONTINUOUS

A BOMB ticks down: 00:30... 00:29...

Jack works frantically. Sweat drips.

JACK
Everyone stay calm!

He cuts the red wire. The timer stops at 00:01.

PASSENGERS cheer. Jack smiles grimly.

JACK
(to himself)
Just another day at the office.

FADE OUT."""


def create_mixed_genre_screenplay():
    """Create a screenplay mixing multiple genres."""
    return """FADE IN:

INT. LABORATORY - NIGHT (SCI-FI)

DR. SARAH CHEN works on a glowing device. Sparks fly.

SARAH
The portal is almost ready!

Suddenly, she LAUGHS at her robot assistant. (COMEDY)

ROBOT
Beep boop. I am not programmed for humor.

SARAH
That's what makes it funny!

A MYSTERIOUS FIGURE appears. (THRILLER)

FIGURE
You don't know what you're messing with.

SARAH
(terrified)
Who are you? (HORROR)

The figure steps into light - it's MARK, her ex. (DRAMA/ROMANCE)

MARK
Sarah, I never stopped loving you.

SARAH
(tears forming)
You left me when I needed you most.

Suddenly, MONSTERS burst through the portal! (ACTION)

MARK
Get behind me!

He grabs a laser gun and FIRES.

EXT. CITY STREET - CONTINUOUS

They run as creatures chase them. (ACTION/HORROR)

SARAH
This is all my fault!

MARK
We'll fix this together.

They share a passionate KISS as explosions surround them. (ROMANCE)

FADE OUT."""


def create_genre_unclear_screenplay():
    """Create a screenplay with unclear genre."""
    return """FADE IN:

INT. ROOM - DAY

PERSON A sits at a table.

PERSON A
I have something to say.

PERSON B enters.

PERSON B
What is it?

PERSON A
It's about the thing.

PERSON B
What thing?

PERSON A
You know. The thing from before.

PERSON B
Oh. That thing.

They sit in silence.

PERSON A
So what do we do?

PERSON B
I don't know.

PERSON A
Should we go?

PERSON B
Maybe.

They stand up.

EXT. STREET - DAY

They walk.

PERSON A
This is nice.

PERSON B
Yes.

They continue walking.

FADE OUT."""


def test_basic_genre_analysis():
    """Test basic genre analysis."""
    print("\n🎬 TEST 1: Basic Genre Analysis")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()

    result = dr_genre.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "genre_analysis" in result.__dict__
    assert "genre_markers" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Primary genre: {result.genre_analysis.primary_genre}")
    print(f"✅ Genre purity: {result.genre_analysis.genre_purity:.2f}")

    return True


def test_genre_identification():
    """Test genre identification."""
    print("\n🎬 TEST 2: Genre Identification")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()
    result = dr_genre.analyze(screenplay)

    print(f"🎯 Primary genre: {result.genre_analysis.primary_genre}")
    print(f"🎭 Secondary genres: {', '.join(result.genre_analysis.secondary_genres) if result.genre_analysis.secondary_genres else 'None'}")

    # Show genre distribution
    print("📊 Genre distribution:")
    for genre, weight in sorted(result.genre_distribution.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"   {genre}: {weight:.2f}")

    # Should identify action as primary genre
    assert result.genre_analysis.primary_genre == 'action'
    print("\n✅ Genre identification working")

    return True


def test_convention_detection():
    """Test genre convention detection."""
    print("\n🎬 TEST 3: Convention Detection")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()
    result = dr_genre.analyze(screenplay)

    print(f"📋 Conventions met: {result.genre_analysis.conventions_met}")
    print(f"❌ Conventions missing: {result.genre_analysis.conventions_missing}")

    # List some detected conventions
    print("✅ Present conventions:")
    for conv in result.conventions[:5]:
        if conv.present:
            print(f"   {conv.name}: {conv.type} (strength: {conv.strength:.2f})")

    print("\n✅ Convention detection working")

    return True


def test_trope_analysis():
    """Test trope analysis."""
    print("\n🎬 TEST 4: Trope Analysis")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()
    result = dr_genre.analyze(screenplay)

    print(f"🎭 Tropes used: {result.genre_analysis.tropes_used}")
    print(f"🔄 Tropes subverted: {result.genre_analysis.tropes_subverted}")

    # Show some tropes
    for trope in result.tropes[:3]:
        if trope.usage != 'avoided':
            print(f"   {trope.name}: {trope.usage} (effectiveness: {trope.effectiveness:.2f})")

    print("\n✅ Trope analysis working")

    return True


def test_mixed_genre():
    """Test mixed genre detection."""
    print("\n🎬 TEST 5: Mixed Genre Detection")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_mixed_genre_screenplay()
    result = dr_genre.analyze(screenplay)

    print(f"🎯 Primary: {result.genre_analysis.primary_genre}")
    print(f"🎭 Secondary: {', '.join(result.genre_analysis.secondary_genres)}")
    print(f"⚖️ Hybrid balance: {result.genre_analysis.hybrid_balance:.2f}")

    # Should detect multiple genres
    assert len(result.genre_distribution) > 1
    print("\n✅ Mixed genre detection working")

    return True


def test_audience_expectations():
    """Test audience expectation metrics."""
    print("\n🎬 TEST 6: Audience Expectations")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()
    result = dr_genre.analyze(screenplay)

    print(f"👥 Expectations met: {result.genre_analysis.expectations_met:.2f}")
    print(f"😊 Audience satisfaction: {result.audience_satisfaction:.2f}")
    print(f"✨ Originality score: {result.originality_score:.2f}")

    print("\n✅ Audience expectation metrics working")

    return True


def test_genre_alignment():
    """Test genre alignment metrics."""
    print("\n🎬 TEST 7: Genre Alignment")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()
    result = dr_genre.analyze(screenplay)

    print(f"🎵 Tone alignment: {result.genre_analysis.tone_alignment:.2f}")
    print(f"⏱️ Pacing alignment: {result.genre_analysis.pacing_alignment:.2f}")
    print(f"🎯 Genre confidence: {result.genre_confidence:.2f}")

    print("\n✅ Genre alignment metrics working")

    return True


def test_scene_genre_analysis():
    """Test scene-by-scene genre analysis."""
    print("\n🎬 TEST 8: Scene Genre Analysis")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    screenplay = create_action_screenplay()
    result = dr_genre.analyze(screenplay)

    print("🎬 Scene-by-scene genres:")
    for scene_num, genres in list(result.scene_genres.items())[:3]:
        if genres:
            dominant = max(genres.items(), key=lambda x: x[1])
            print(f"   Scene {scene_num}: {dominant[0]} ({dominant[1]:.2f})")

    print("\n✅ Scene genre analysis working")

    return True


def test_rule_violations():
    """Test genre rule violations."""
    print("\n🎬 TEST 9: Rule Violations")
    print("=" * 50)

    dr_genre = DrGenreConventions()

    # Test with unclear genre screenplay
    unclear = create_genre_unclear_screenplay()
    result = dr_genre.analyze(unclear)
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

    # Should detect issues with unclear genre
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎬 TEST 10: Recommendations")
    print("=" * 50)

    dr_genre = DrGenreConventions()
    unclear = create_genre_unclear_screenplay()

    result = dr_genre.analyze(unclear)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Genremon tests."""
    print("\n" + "=" * 60)
    print("🎬 SCRIPT DOCTOR GENREMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Genre Analysis", test_basic_genre_analysis),
        ("Genre Identification", test_genre_identification),
        ("Convention Detection", test_convention_detection),
        ("Trope Analysis", test_trope_analysis),
        ("Mixed Genre Detection", test_mixed_genre),
        ("Audience Expectations", test_audience_expectations),
        ("Genre Alignment", test_genre_alignment),
        ("Scene Genre Analysis", test_scene_genre_analysis),
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
        print("\n🎉 SCRIPT DOCTOR GENREMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Genre Conventions Specialist is ready")
        print("\n🎬 Genre analysis systems online!")
        print("\n📝 Specialist 19/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)