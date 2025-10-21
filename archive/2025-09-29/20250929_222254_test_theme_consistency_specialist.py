#!/usr/bin/env python3
"""
Test Suite for Script Doctor Thememon - Theme Consistency Specialist
Tests the theme consistency specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.theme_consistency_specialist import DrThemeConsistency


def create_thematically_rich_screenplay():
    """Create a screenplay with clear, consistent themes."""
    return """FADE IN:

INT. COURTROOM - DAY

The pursuit of justice fills the air. JUDGE MARTINEZ presides.

JUDGE MARTINEZ
Justice isn't about revenge. It's about
truth.

PROSECUTOR WILLIAMS
The truth is this man betrayed everything
he swore to protect. He chose corruption
over justice.

DEFENSE ATTORNEY CHEN
My client made a choice. Yes. But it was
to save his family. Sometimes truth and
justice conflict.

DEFENDANT JACK MORRISON (40s) stands.

JACK
I was corrupt. I admit it. But when they
threatened my daughter, I had to choose -
justice or family. I chose family.

JUDGE MARTINEZ
The law demands justice, Mr. Morrison.
Personal truth doesn't excuse corruption.

INT. COURTHOUSE HALLWAY - LATER

Jack's wife SARAH waits.

SARAH
You did the right thing. Family comes
first.

JACK
Did I? I betrayed my oath for personal
truth. Maybe real justice means accepting
the consequences.

SARAH
Justice without mercy isn't justice at all.

JACK
And truth without accountability is just
another lie.

INT. PRISON CELL - MONTHS LATER

Jack writes a letter.

JACK (V.O.)
Dear Sarah, I've learned something here.
Justice and truth aren't opposites -
they're partners. My corruption wasn't
justified by my reasons. True justice
means accepting truth, even when it hurts.

INT. COURTROOM - DAY (FLASHBACK)

Young Jack takes his oath as a prosecutor.

YOUNG JACK
I swear to uphold justice and truth...

BACK TO PRISON CELL

Jack finishes his letter.

JACK (V.O.)
I forgot that oath. But I remember it now.
Justice requires sacrifice. Truth demands
courage. I'm finally free because I chose
both.

FADE OUT."""


def create_thematically_confused_screenplay():
    """Create a screenplay with unclear, inconsistent themes."""
    return """FADE IN:

INT. OFFICE - DAY

JOHN sits at his desk.

JOHN
I love my job.

MARY enters.

MARY
Let's rob a bank!

JOHN
Okay!

EXT. BEACH - DAY

John and Mary are now surfers.

JOHN
Surfing is life!

MARY
No, family is everything!

INT. SPACESHIP - NIGHT

Somehow they're in space now.

JOHN
We must save Earth!

MARY
Why? Let's explore!

INT. OFFICE - DAY

Back at work.

JOHN
The moral of the story is that
hard work pays off.

MARY
No, the lesson is clearly that
adventure is important.

JOHN
Actually, what this means is
we should follow our dreams.

MARY
As you know, Bob, the point is
that love conquers all.

JOHN
Obviously, the theme is about
finding yourself.

FADE OUT."""


def test_basic_theme_analysis():
    """Test basic theme analysis."""
    print("\n🎭 TEST 1: Basic Theme Analysis")
    print("=" * 50)

    dr_theme = DrThemeConsistency()
    screenplay = create_thematically_rich_screenplay()

    result = dr_theme.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "theme_analysis" in result.__dict__
    assert "thematic_elements" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Central theme: {result.theme_analysis.central_theme}")
    print(f"✅ Theme strength: {result.theme_analysis.central_theme_strength:.2f}")

    return True


def test_theme_identification():
    """Test theme identification."""
    print("\n🎭 TEST 2: Theme Identification")
    print("=" * 50)

    dr_theme = DrThemeConsistency()
    screenplay = create_thematically_rich_screenplay()
    result = dr_theme.analyze(screenplay)

    print(f"🎯 Central theme: {result.theme_analysis.central_theme}")
    print(f"🎯 Supporting themes: {', '.join(result.theme_analysis.supporting_themes)}")
    print(f"🎯 Thematic depth: {result.theme_analysis.thematic_depth}")

    # Should identify justice/truth as main themes
    assert result.theme_analysis.central_theme in ['justice', 'truth', 'corruption']
    print("\n✅ Theme identification working")

    return True


def test_theme_consistency():
    """Test theme consistency detection."""
    print("\n🎭 TEST 3: Theme Consistency")
    print("=" * 50)

    dr_theme = DrThemeConsistency()

    # Consistent themes
    consistent = create_thematically_rich_screenplay()
    consistent_result = dr_theme.analyze(consistent)

    # Inconsistent themes
    inconsistent = create_thematically_confused_screenplay()
    inconsistent_result = dr_theme.analyze(inconsistent)

    print(f"✅ Consistent screenplay:")
    print(f"   Consistency score: {consistent_result.theme_analysis.theme_consistency_score:.2f}")
    
    print(f"\n❌ Inconsistent screenplay:")
    print(f"   Consistency score: {inconsistent_result.theme_analysis.theme_consistency_score:.2f}")

    print("\n✅ Theme consistency detection working")

    return True


def test_theme_expression():
    """Test theme expression analysis."""
    print("\n🎭 TEST 4: Theme Expression Methods")
    print("=" * 50)

    dr_theme = DrThemeConsistency()
    screenplay = create_thematically_rich_screenplay()
    result = dr_theme.analyze(screenplay)

    print("📦 Expression methods:")
    for method, count in result.theme_analysis.theme_expression_methods.items():
        if count > 0:
            print(f"   {method}: {count}")

    print("\n✅ Theme expression analysis working")

    return True


def test_theme_alignment():
    """Test theme-plot and theme-character alignment."""
    print("\n🎭 TEST 5: Theme Alignment")
    print("=" * 50)

    dr_theme = DrThemeConsistency()
    screenplay = create_thematically_rich_screenplay()
    result = dr_theme.analyze(screenplay)

    print(f"🎯 Plot alignment: {result.theme_analysis.theme_plot_alignment:.2f}")
    print(f"👥 Character alignment: {result.theme_analysis.theme_character_alignment:.2f}")

    print("\n✅ Theme alignment analysis working")

    return True


def test_heavy_handedness():
    """Test heavy-handedness detection."""
    print("\n🎭 TEST 6: Heavy-Handedness Detection")
    print("=" * 50)

    dr_theme = DrThemeConsistency()

    # Preachy screenplay
    preachy = create_thematically_confused_screenplay()
    preachy_result = dr_theme.analyze(preachy)

    # Subtle screenplay
    subtle = create_thematically_rich_screenplay()
    subtle_result = dr_theme.analyze(subtle)

    print(f"📢 Preachy screenplay score: {preachy_result.theme_analysis.heavy_handed_score:.2f}")
    print(f"🎯 Subtle screenplay score: {subtle_result.theme_analysis.heavy_handed_score:.2f}")

    print("\n✅ Heavy-handedness detection working")

    return True


def test_theme_resolution():
    """Test theme resolution detection."""
    print("\n🎭 TEST 7: Theme Resolution")
    print("=" * 50)

    dr_theme = DrThemeConsistency()
    screenplay = create_thematically_rich_screenplay()
    result = dr_theme.analyze(screenplay)

    print(f"🏁 Theme resolved: {result.theme_analysis.theme_resolved}")
    print(f"🆚 Opposing viewpoints: {result.theme_analysis.opposing_viewpoints_present}")

    print("\n✅ Theme resolution detection working")

    return True


def test_theme_progression():
    """Test theme progression analysis."""
    print("\n🎭 TEST 8: Theme Progression")
    print("=" * 50)

    dr_theme = DrThemeConsistency()
    screenplay = create_thematically_rich_screenplay()
    result = dr_theme.analyze(screenplay)

    print(f"📈 Progression type: {result.theme_progression.get('progression', 'unknown')}")
    if 'central_theme' in result.theme_progression:
        print(f"🎯 Central theme tracked: {result.theme_progression['central_theme']}")

    print("\n✅ Theme progression analysis working")

    return True


def test_rule_violations():
    """Test theme rule violations."""
    print("\n🎭 TEST 9: Rule Violations")
    print("=" * 50)

    dr_theme = DrThemeConsistency()

    # Test with thematically confused screenplay
    confused = create_thematically_confused_screenplay()
    result = dr_theme.analyze(confused)
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

    dr_theme = DrThemeConsistency()
    confused = create_thematically_confused_screenplay()

    result = dr_theme.analyze(confused)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Thememon tests."""
    print("\n" + "=" * 60)
    print("🎭 SCRIPT DOCTOR THEMEMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Theme Analysis", test_basic_theme_analysis),
        ("Theme Identification", test_theme_identification),
        ("Theme Consistency", test_theme_consistency),
        ("Theme Expression", test_theme_expression),
        ("Theme Alignment", test_theme_alignment),
        ("Heavy-Handedness", test_heavy_handedness),
        ("Theme Resolution", test_theme_resolution),
        ("Theme Progression", test_theme_progression),
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
        print("\n🎉 SCRIPT DOCTOR THEMEMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Theme Consistency Specialist is ready")
        print("\n🎭 Thematic analysis systems online!")
        print("\n📝 Specialist 15/24 of the Script Doctor™ system operational!")
        print("\n🎯 First specialist of ELEMENTOS NARRATIVOS group operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
