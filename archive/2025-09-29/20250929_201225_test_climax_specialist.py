#!/usr/bin/env python3
"""
Test Suite for Script Doctor Peakmon - Climax and Peak Moments Specialist
Tests the climax specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.climax_specialist import DrClimax


def create_strong_climax_screenplay():
    """Create a screenplay with a strong climax."""
    # Build a full screenplay with climax at ~80%
    setup = """FADE IN:

INT. OFFICE - DAY

JOHN (40s) looks at a mysterious PACKAGE.

JOHN
This changes everything.

He HIDES the package in his desk.

"""
    
    # Add middle content to reach page ~80
    middle = """
INT. VARIOUS LOCATIONS - DAY/NIGHT

[PAGES 10-70 OF CHARACTER DEVELOPMENT AND RISING ACTION]

John discovers the truth. The stakes rise.
Enemies close in. Allies betray him.
Time is running out.

""" * 20  # Multiply to simulate more pages
    
    climax = """
EXT. ROOFTOP - NIGHT (CLIMAX)

FINAL CONFRONTATION. John faces VIKTOR.

The PACKAGE from Act 1 lies between them.

VIKTOR
You have ten seconds to choose.
Your family or the city.

JOHN
There's always another way.

John sees the BOMB TIMER: 00:09... 00:08...

ALL IS LOST. John's family held at gunpoint.
The city's fate in his hands.

JOHN (CONT'D)
(making the hardest choice)
I choose... both.

He GRABS the package, RUNS toward the edge.

VIKTOR
No!

John LEAPS off the building, package in hand.

The timer hits 00:01...

EXPLOSION! But controlled. John's sacrifice
saved everyone. He falls into the river below.

FADE OUT.

THE END"""
    
    return setup + middle + climax


def create_weak_climax_screenplay():
    """Create a screenplay with a weak climax."""
    return """FADE IN:

INT. HOUSE - DAY

Bob sits on his couch. He's been sitting here
for 90 pages. Nothing much has happened.

[PAGES OF TALKING AND THINKING]

INT. HOUSE - LATER (SUPPOSED CLIMAX)

Bob is still sitting. His phone rings.

BOB
Hello?

VOICE (O.S.)
The problem has been solved for you.

BOB
Oh. Okay. Thanks.

He hangs up. Continues sitting.

BOB (CONT'D)
(to himself)
I guess that's that then.

He turns on the TV. Watches the news.
Everything worked out somehow.

FADE OUT.

THE END"""


def test_basic_climax_analysis():
    """Test basic climax analysis."""
    print("\n🎯 TEST 1: Basic Climax Analysis")
    print("=" * 50)
    
    dr_climax = DrClimax()
    screenplay = create_strong_climax_screenplay()
    
    result = dr_climax.analyze(screenplay)
    
    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "climax_location" in result
    assert "intensity_score" in result
    
    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Climax at page {result['climax_location']['page_start']}")
    print(f"✅ Intensity: {result['intensity_score']:.2f}")
    
    return True


def test_climax_location_detection():
    """Test climax location detection."""
    print("\n🎯 TEST 2: Climax Location Detection")
    print("=" * 50)
    
    dr_climax = DrClimax()
    screenplay = create_strong_climax_screenplay()
    
    result = dr_climax.analyze(screenplay)
    location = result["climax_location"]
    
    print(f"📍 Climax location:")
    print(f"   Pages {location['page_start']}-{location['page_end']}")
    print(f"   At {location['percentage_point']:.0f}% of script")
    print(f"   Duration: {location['duration_pages']} pages")
    
    # Climax should be between 70-90% of script
    assert 70 <= location["percentage_point"] <= 90
    print("\n✅ Climax location detection working")
    
    return True


def test_intensity_calculation():
    """Test climax intensity calculation."""
    print("\n🎯 TEST 3: Intensity Calculation")
    print("=" * 50)
    
    dr_climax = DrClimax()
    
    # Strong climax
    strong = create_strong_climax_screenplay()
    strong_result = dr_climax.analyze(strong)
    
    # Weak climax
    weak = create_weak_climax_screenplay()
    weak_result = dr_climax.analyze(weak)
    
    print(f"🔥 Strong climax intensity: {strong_result['intensity_score']:.2f}")
    print(f"😴 Weak climax intensity: {weak_result['intensity_score']:.2f}")
    
    # Strong should have higher intensity
    assert strong_result["intensity_score"] > weak_result["intensity_score"]
    print("\n✅ Intensity calculation working")
    
    return True


def test_protagonist_agency():
    """Test protagonist agency detection."""
    print("\n🎯 TEST 4: Protagonist Agency")
    print("=" * 50)
    
    dr_climax = DrClimax()
    
    # Active protagonist
    strong = create_strong_climax_screenplay()
    strong_result = dr_climax.analyze(strong)
    
    # Passive protagonist
    weak = create_weak_climax_screenplay()
    weak_result = dr_climax.analyze(weak)
    
    print(f"👤 Strong screenplay:")
    print(f"   Has agency: {strong_result['protagonist_agency']['has_agency']}")
    print(f"   Agency score: {strong_result['protagonist_agency']['agency_score']:.2f}")
    
    print(f"\n👤 Weak screenplay:")
    print(f"   Has agency: {weak_result['protagonist_agency']['has_agency']}")
    print(f"   Agency score: {weak_result['protagonist_agency']['agency_score']:.2f}")
    
    # Strong should have better agency than weak
    assert strong_result["protagonist_agency"]["agency_score"] >= weak_result["protagonist_agency"]["agency_score"]
    print("\n✅ Protagonist agency detection working")
    
    return True


def test_climax_elements():
    """Test detection of climax elements."""
    print("\n🎯 TEST 5: Climax Elements Detection")
    print("=" * 50)
    
    dr_climax = DrClimax()
    screenplay = create_strong_climax_screenplay()
    result = dr_climax.analyze(screenplay)
    
    elements = result["climax_elements"]
    
    print("🌟 Essential elements:")
    for name, data in elements.items():
        status = "✅" if data["present"] else "❌"
        print(f"   {status} {name}: {data['intensity']:.2f} intensity")
    
    # Should have at least some key elements
    present_count = sum(1 for e in elements.values() if e["present"])
    assert present_count >= 2  # At least 2 elements present
    
    print("\n✅ Climax elements detection working")
    
    return True


def test_setup_payoff_tracking():
    """Test setup and payoff tracking."""
    print("\n🎯 TEST 6: Setup/Payoff Tracking")
    print("=" * 50)
    
    dr_climax = DrClimax()
    screenplay = create_strong_climax_screenplay()
    result = dr_climax.analyze(screenplay)
    
    payoffs = result["setup_payoffs"]
    
    print(f"🎁 Found {len(payoffs)} setup/payoff pairs")
    for payoff in payoffs[:3]:  # Show first 3
        print(f"   Setup p.{payoff['setup_page']}: {payoff['setup'][:30]}...")
        print(f"   Payoff p.{payoff['payoff_page']}: {payoff['payoff'][:30]}...")
        print(f"   Satisfied: {payoff['satisfied']}\n")
    
    print("✅ Setup/payoff tracking working")
    
    return True


def test_false_victory_detection():
    """Test false victory/defeat detection."""
    print("\n🎯 TEST 7: False Victory/Defeat Detection")
    print("=" * 50)
    
    dr_climax = DrClimax()
    screenplay = create_strong_climax_screenplay()
    result = dr_climax.analyze(screenplay)
    
    print(f"🎭 False moment detected: {result['has_false_moment']}")
    if result["has_false_moment"]:
        print(f"   Type: {result['false_moment_type']}")
    
    print("\n✅ False victory detection working")
    
    return True


def test_rule_violations():
    """Test climax rule violations."""
    print("\n🎯 TEST 8: Rule Violations")
    print("=" * 50)
    
    dr_climax = DrClimax()
    
    # Test with weak screenplay
    weak_screenplay = create_weak_climax_screenplay()
    result = dr_climax.analyze(weak_screenplay)
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
    
    # Should detect issues in weak screenplay
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")
    
    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎯 TEST 9: Recommendation Generation")
    print("=" * 50)
    
    dr_climax = DrClimax()
    weak_screenplay = create_weak_climax_screenplay()
    
    result = dr_climax.analyze(weak_screenplay)
    
    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")
    
    # Should generate recommendations for weak climax
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")
    
    return True


def run_all_tests():
    """Run all Peakmon tests."""
    print("\n" + "=" * 60)
    print("🎯 SCRIPT DOCTOR PEAKMON - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Basic Climax Analysis", test_basic_climax_analysis),
        ("Climax Location Detection", test_climax_location_detection),
        ("Intensity Calculation", test_intensity_calculation),
        ("Protagonist Agency", test_protagonist_agency),
        ("Climax Elements", test_climax_elements),
        ("Setup/Payoff Tracking", test_setup_payoff_tracking),
        ("False Victory Detection", test_false_victory_detection),
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
        print("\n🎉 SCRIPT DOCTOR PEAKMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Climax and Peak Moments Specialist is ready")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)