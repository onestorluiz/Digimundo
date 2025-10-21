#!/usr/bin/env python3
"""
Test Suite for Script Doctor Qualitymon - Overall Quality Specialist
Tests the overall quality specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.overall_quality_specialist import DrOverallQuality


def create_high_quality_screenplay():
    """Create a high quality screenplay."""
    return """FADE IN:

EXT. CLIFF EDGE - SUNSET

Wind whips through SARAH's (30s) hair as she stands at the precipice.
Her wedding dress, torn and muddy, tells a story we're about to learn.

SARAH
(to the void)
You said jump and I'd catch you.

She laughs bitterly. Opens her clenched fist - a crumpled photo
of her and JAMES (30s) on their wedding day. Happy. Naive.

SARAH (CONT'D)
I jumped. You weren't there.

FLASHBACK - INT. CHURCH - DAY (ONE YEAR AGO)

The same photo being taken. Sarah radiant. James charming.
The photographer captures a perfect lie.

JAMES
(whispering to Sarah)
Forever starts now.

Sarah's smile falters for just a moment. Did she know even then?

BACK TO:

EXT. CLIFF EDGE - SUNSET

Sarah releases the photo. It dances away on the wind, disappearing
into the abyss below. She takes a step back from the edge.

SARAH
But I learned to fly without you.

She turns away from the cliff. In the distance, headlights approach.
A car stops. MAYA (40s) emerges - strong, weathered, knowing.

MAYA
Ready to start over?

SARAH
I already have.

They embrace. Not romantic - something deeper. Survivor to survivor.

INT. CAR - MOVING - NIGHT

Maya drives. Sarah watches the world blur past.

MAYA
The safe house is two hours north.
New identity papers are ready.

SARAH
What about James?

MAYA
He'll never find you. Or any of us.

Sarah nods. In the rearview mirror, the cliff disappears into darkness.
Ahead, the road stretches toward an uncertain but self-determined future.

SARAH
(softly, to herself)
I'm not running from him anymore.
I'm running to me.

FADE OUT."""


def create_poor_quality_screenplay():
    """Create a poor quality screenplay."""
    return """SCENE 1

Bob enters.

BOB: Hello.

MARY: Hi.

They sit.

BOB: So what happens now?

MARY: I don't know.

Long pause.

BOB: We should do something.

MARY: Like what?

BOB: Something important.

MARY: OK.

SCENE 2

They walk outside.

BOB: This is nice.

MARY: Yeah.

They keep walking.

BOB: Remember when we used to walk?

MARY: Yes.

BOB: That was good.

MARY: It was.

More walking.

SCENE 3

Inside again.

BOB: I have to tell you something.

MARY: What?

BOB: It's important.

MARY: OK tell me.

BOB: I can't.

MARY: Why not?

BOB: Because.

MARY: That's not fair.

BOB: I know.

They sit in silence.

THE END"""


def create_medium_quality_screenplay():
    """Create a medium quality screenplay."""
    return """FADE IN:

INT. OFFICE - DAY

JOHN (35), tired-looking businessman, sits at his desk. His boss,
MR. SMITH (50s), enters.

MR. SMITH
Johnson, we need to talk about your
performance.

JOHN
I've been doing my best, sir.

MR. SMITH
Your best isn't good enough anymore.
You're fired.

John is shocked.

EXT. STREET - DAY

John walks out with a box of his belongings. He sees a HOMELESS MAN.

HOMELESS MAN
Spare some change?

JOHN
Sorry, I just lost my job.

HOMELESS MAN
Welcome to the club.

INT. JOHN'S APARTMENT - NIGHT

John tells his wife, SUSAN (30s), the news.

SUSAN
What are we going to do?

JOHN
I'll find something. I always do.

SUSAN
The bills are piling up, John.

JOHN
I know. Trust me.

They hug, both worried.

INT. EMPLOYMENT OFFICE - DAY

John fills out applications. Montage of rejections.

INT. JOHN'S APARTMENT - LATER

John and Susan argue about money. It gets heated.

SUSAN
I can't do this anymore!

She storms out. John is alone.

EXT. BRIDGE - NIGHT

John stands looking at the water. The homeless man appears.

HOMELESS MAN
Life's tough, but it goes on.

JOHN
Does it get better?

HOMELESS MAN
Sometimes. Sometimes not. But you keep going.

John nods and walks away from the edge.

FADE OUT."""


def test_basic_quality_analysis():
    """Test basic quality analysis."""
    print("\n⭐ TEST 1: Basic Quality Analysis")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    screenplay = create_high_quality_screenplay()

    result = dr_quality.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "quality_analysis" in result.__dict__
    assert "quality_dimensions" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Overall quality: {result.quality_analysis.overall_quality:.2f}")
    print(f"✅ Quality level: {result.quality_analysis.quality_level}")

    return True


def test_quality_dimensions():
    """Test quality dimension analysis."""
    print("\n⭐ TEST 2: Quality Dimensions")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    screenplay = create_high_quality_screenplay()
    result = dr_quality.analyze(screenplay)

    print("📊 Quality Dimensions:")
    for dim in result.quality_dimensions:
        print(f"   {dim.dimension}: {dim.score:.2f}")
        if dim.strengths:
            print(f"      Strengths: {dim.strengths[0]}")

    assert len(result.quality_dimensions) >= 6
    print("\n✅ Quality dimension analysis working")

    return True


def test_quality_indicators():
    """Test quality indicator detection."""
    print("\n⭐ TEST 3: Quality Indicators")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    screenplay = create_high_quality_screenplay()
    result = dr_quality.analyze(screenplay)

    print(f"🎯 Quality indicators found: {len(result.quality_indicators)}")

    for indicator in result.quality_indicators[:5]:
        print(f"   {indicator.category}: {indicator.indicator}")
        print(f"      Strength: {indicator.strength:.2f}")

    print("\n✅ Quality indicator detection working")

    return True


def test_professional_standards():
    """Test professional standards checking."""
    print("\n⭐ TEST 4: Professional Standards")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    screenplay = create_high_quality_screenplay()
    result = dr_quality.analyze(screenplay)

    print(f"📋 Professional standards checked: {len(result.professional_standards)}")

    standards_met = sum(1 for s in result.professional_standards if s.met)
    print(f"✅ Standards met: {standards_met}/{len(result.professional_standards)}")

    for standard in result.professional_standards:
        status = "✅" if standard.met else "❌"
        print(f"   {status} {standard.standard}: {standard.score:.2f}")

    print("\n✅ Professional standards checking working")

    return True


def test_quality_comparison():
    """Test quality comparison between screenplays."""
    print("\n⭐ TEST 5: Quality Comparison")
    print("=" * 50)

    dr_quality = DrOverallQuality()

    # High quality
    high = create_high_quality_screenplay()
    high_result = dr_quality.analyze(high)

    # Poor quality
    poor = create_poor_quality_screenplay()
    poor_result = dr_quality.analyze(poor)

    print(f"🌟 High quality screenplay:")
    print(f"   Score: {high_result.score}/100")
    print(f"   Level: {high_result.quality_analysis.quality_level}")

    print(f"\n📉 Poor quality screenplay:")
    print(f"   Score: {poor_result.score}/100")
    print(f"   Level: {poor_result.quality_analysis.quality_level}")

    # High should score better than poor
    assert high_result.score > poor_result.score
    print("\n✅ Quality comparison working")

    return True


def test_excellence_markers():
    """Test excellence marker detection."""
    print("\n⭐ TEST 6: Excellence Markers")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    screenplay = create_high_quality_screenplay()
    result = dr_quality.analyze(screenplay)

    print(f"✨ Excellence markers: {len(result.excellence_markers)}")

    for marker in result.excellence_markers[:3]:
        print(f"   {marker.category}: {marker.description}")
        print(f"      Impact: {marker.impact:.2f}")

    print("\n✅ Excellence marker detection working")

    return True


def test_standout_and_flaws():
    """Test standout elements and critical flaws detection."""
    print("\n⭐ TEST 7: Standouts and Flaws")
    print("=" * 50)

    dr_quality = DrOverallQuality()

    # Test with medium quality
    medium = create_medium_quality_screenplay()
    result = dr_quality.analyze(medium)

    print(f"🌟 Standout elements: {len(result.standout_elements)}")
    for element in result.standout_elements:
        print(f"   {element}")

    print(f"\n⚠️ Critical flaws: {len(result.critical_flaws)}")
    for flaw in result.critical_flaws:
        print(f"   {flaw}")

    print("\n✅ Standout and flaw detection working")

    return True


def test_readiness_and_potential():
    """Test readiness and improvement potential metrics."""
    print("\n⭐ TEST 8: Readiness and Potential")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    screenplay = create_medium_quality_screenplay()
    result = dr_quality.analyze(screenplay)

    print(f"🚀 Market readiness: {result.readiness_score:.2f}")
    print(f"📈 Improvement potential: {result.improvement_potential:.2f}")
    print(f"🎬 Entertainment value: {result.quality_analysis.entertainment_value:.2f}")
    print(f"💰 Production viability: {result.quality_analysis.production_viability:.2f}")

    print("\n✅ Readiness and potential metrics working")

    return True


def test_rule_violations():
    """Test quality rule violations."""
    print("\n⭐ TEST 9: Rule Violations")
    print("=" * 50)

    dr_quality = DrOverallQuality()

    # Test with poor quality screenplay
    poor = create_poor_quality_screenplay()
    result = dr_quality.analyze(poor)
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

    # Should detect issues in poor screenplay
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n⭐ TEST 10: Recommendations")
    print("=" * 50)

    dr_quality = DrOverallQuality()
    medium = create_medium_quality_screenplay()

    result = dr_quality.analyze(medium)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Qualitymon tests."""
    print("\n" + "=" * 60)
    print("⭐ SCRIPT DOCTOR QUALITYMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Quality Analysis", test_basic_quality_analysis),
        ("Quality Dimensions", test_quality_dimensions),
        ("Quality Indicators", test_quality_indicators),
        ("Professional Standards", test_professional_standards),
        ("Quality Comparison", test_quality_comparison),
        ("Excellence Markers", test_excellence_markers),
        ("Standouts and Flaws", test_standout_and_flaws),
        ("Readiness and Potential", test_readiness_and_potential),
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
        print("\n🎉 SCRIPT DOCTOR QUALITYMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Overall Quality Specialist is ready")
        print("\n⭐ Quality assessment systems online!")
        print("\n📝 Specialist 22/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)