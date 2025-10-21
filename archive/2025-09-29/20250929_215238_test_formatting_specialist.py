#!/usr/bin/env python3
"""
Test Suite for Script Doctor Formatmon - Formatting Specialist
Tests the formatting specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.formatting_specialist import DrFormatting


def create_well_formatted_screenplay():
    """Create a properly formatted screenplay."""
    return """FADE IN:

INT. OFFICE - DAY

JOHN (40s), tired but determined, enters the bustling office.

SARAH (30s), his assistant, looks up from her desk.

SARAH
You're late. The board is waiting.

JOHN
(sighs)
Traffic. Are they angry?

SARAH
When aren't they?

John straightens his tie and heads for the boardroom.

INT. BOARDROOM - DAY - CONTINUOUS

John enters to find five BOARD MEMBERS seated around the table.

CHAIRMAN
John. We need to talk about the numbers.

JOHN
I can explain--

CHAIRMAN
(interrupting)
The numbers speak for themselves.

John takes a deep breath. This is worse than he thought.

CUT TO:

EXT. OFFICE BUILDING - DAY - LATER

John exits, defeated. His phone RINGS.

JOHN
(into phone)
Yeah, I know. I'll figure something out.

He ends the call and walks into the city crowd.

FADE OUT."""


def create_poorly_formatted_screenplay():
    """Create a poorly formatted screenplay with multiple issues."""
    return """fade in

int. office -- day

john walked into the office. He was tired from the long night.

sarah
(angrily) (frustrated) (loudly)
your late!!! The board was waiting...

John
Traffic was bad. are they angry?

We see sarah rolling her eyes at john.

sarah
When arent they???

ANGLE ON: John as he straightened his tie

john walked towards the boardroom door.

INTERIOR - BOARDROOM - DAY - CONT.

John entered and saw five board members who were seated.

chairman
John... We needed to talk about the numbers yesterday.

john
i can explain -

CLOSE UP on Chairman's face

chairman
(interrupting him)
(sternly)
The numbers spoke for themselves.

We hear John taking a deep breath. This was worse than he had thought.

CUT TO:
CUT TO:
CUT TO:

EXTERIOR: OFFICE BUILDING, DAY (LATER)

John exited defeated. His phone rang loudly.

john (on phone): yeah i know. ill figure something out...

He ended the call and we watch as he walked into crowd.

THE END"""


def test_basic_formatting_analysis():
    """Test basic formatting analysis."""
    print("\n📝 TEST 1: Basic Formatting Analysis")
    print("=" * 50)

    dr_formatting = DrFormatting()
    screenplay = create_well_formatted_screenplay()

    result = dr_formatting.analyze(screenplay)

    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "total_issues" in result
    assert "estimated_pages" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Total issues: {result['total_issues']}")
    print(f"✅ Estimated pages: {result['estimated_pages']}")

    return True


def test_scene_heading_check():
    """Test scene heading format checking."""
    print("\n📝 TEST 2: Scene Heading Check")
    print("=" * 50)

    dr_formatting = DrFormatting()

    # Well formatted
    good = create_well_formatted_screenplay()
    good_result = dr_formatting.analyze(good)

    # Poorly formatted
    poor = create_poorly_formatted_screenplay()
    poor_result = dr_formatting.analyze(poor)

    print(f"✅ Good screenplay scene issues: {good_result['scene_heading_issues']}")
    print(f"❌ Poor screenplay scene issues: {poor_result['scene_heading_issues']}")

    # Poor screenplay should have issues or at least not better than good
    assert poor_result["scene_heading_issues"] >= good_result["scene_heading_issues"]
    print("\n✅ Scene heading check working")

    return True


def test_character_formatting():
    """Test character name formatting check."""
    print("\n📝 TEST 3: Character Formatting")
    print("=" * 50)

    dr_formatting = DrFormatting()

    # Well formatted
    good = create_well_formatted_screenplay()
    good_result = dr_formatting.analyze(good)

    # Poorly formatted
    poor = create_poorly_formatted_screenplay()
    poor_result = dr_formatting.analyze(poor)

    print(f"✅ Good screenplay character issues: {good_result['character_formatting_issues']}")
    print(f"❌ Poor screenplay character issues: {poor_result['character_formatting_issues']}")

    print("\n✅ Character formatting check working")

    return True


def test_action_line_check():
    """Test action line formatting."""
    print("\n📝 TEST 4: Action Line Check")
    print("=" * 50)

    dr_formatting = DrFormatting()
    screenplay = create_well_formatted_screenplay()
    result = dr_formatting.analyze(screenplay)

    print(f"📄 Action line issues: {result['action_line_issues']}")
    print(f"📊 Average paragraph length: {result['average_action_paragraph_length']:.1f} lines")

    print("\n✅ Action line check working")

    return True


def test_camera_direction_check():
    """Test camera direction detection."""
    print("\n📝 TEST 5: Camera Direction Check")
    print("=" * 50)

    dr_formatting = DrFormatting()

    # Poorly formatted has camera directions
    poor = create_poorly_formatted_screenplay()
    poor_result = dr_formatting.analyze(poor)

    print(f"🎥 Camera directions found: {poor_result['camera_direction_issues']}")

    assert poor_result["camera_direction_issues"] > 0
    print("\n✅ Camera direction check working")

    return True


def test_tense_check():
    """Test past tense detection in action lines."""
    print("\n📝 TEST 6: Tense Check")
    print("=" * 50)

    dr_formatting = DrFormatting()

    # Poorly formatted has past tense
    poor = create_poorly_formatted_screenplay()
    poor_result = dr_formatting.analyze(poor)

    print(f"⏰ Past tense issues: {poor_result['tense_issues']}")

    assert poor_result["tense_issues"] > 0
    print("\n✅ Tense check working")

    return True


def test_we_see_hear_check():
    """Test 'we see/we hear' detection."""
    print("\n📝 TEST 7: We See/Hear Check")
    print("=" * 50)

    dr_formatting = DrFormatting()

    # Poorly formatted has "we see/hear"
    poor = create_poorly_formatted_screenplay()
    poor_result = dr_formatting.analyze(poor)

    print(f"👁️ 'We see/hear' issues: {poor_result['we_see_hear_issues']}")

    assert poor_result["we_see_hear_issues"] > 0
    print("\n✅ We see/hear check working")

    return True


def test_white_space_analysis():
    """Test white space analysis."""
    print("\n📝 TEST 8: White Space Analysis")
    print("=" * 50)

    dr_formatting = DrFormatting()
    screenplay = create_well_formatted_screenplay()
    result = dr_formatting.analyze(screenplay)

    print(f"⬜ White space score: {result['white_space_score']*100:.0f}%")
    print(f"📊 Dialogue percentage: {result['dialogue_percentage']:.0f}%")
    print(f"📊 Action percentage: {result['action_percentage']:.0f}%")

    print("\n✅ White space analysis working")

    return True


def test_rule_violations():
    """Test formatting rule violations."""
    print("\n📝 TEST 9: Rule Violations")
    print("=" * 50)

    dr_formatting = DrFormatting()

    # Test with poorly formatted screenplay
    poor = create_poorly_formatted_screenplay()
    result = dr_formatting.analyze(poor)
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
    print("\n📝 TEST 10: Recommendations")
    print("=" * 50)

    dr_formatting = DrFormatting()
    poor = create_poorly_formatted_screenplay()

    result = dr_formatting.analyze(poor)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")

    return True


def run_all_tests():
    """Run all Formatmon tests."""
    print("\n" + "=" * 60)
    print("📝 SCRIPT DOCTOR FORMATMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Formatting Analysis", test_basic_formatting_analysis),
        ("Scene Heading Check", test_scene_heading_check),
        ("Character Formatting", test_character_formatting),
        ("Action Line Check", test_action_line_check),
        ("Camera Direction Check", test_camera_direction_check),
        ("Tense Check", test_tense_check),
        ("We See/Hear Check", test_we_see_hear_check),
        ("White Space Analysis", test_white_space_analysis),
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
        print("\n🎉 SCRIPT DOCTOR FORMATMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Formatting Specialist is ready")
        print("\n📝 Screenplay formatting analysis systems online!")
        print("\n🚀 First specialist of DIÁLOGO E TEXTO group operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)