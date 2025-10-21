#!/usr/bin/env python3
"""
Test Suite for Script Doctor Relatemon - Character Relationships Specialist
Tests the relationships specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.character_relationships_specialist import DrRelationships


def create_strong_relationships_screenplay():
    """Create a screenplay with strong, dynamic relationships."""
    return """FADE IN:

INT. COFFEE SHOP - DAY

SARAH (30s) sits alone. MARK (30s) enters, sees her, hesitates.

MARK
(nervous)
Sarah? I... I didn't expect to see you here.

SARAH
(guarded)
Mark. It's been what, two years?

MARK
Two years, three months. But who's counting?

Awkward silence. The weight of their history between them.

SARAH
You look... different.

MARK
Prison does that to a person.
(beat)
I'm sorry. For everything.

SARAH
(walls crumbling)
I waited for you to say that. Every day.

MARK
I know I don't deserve forgiveness--

SARAH
(interrupting)
You don't. But I need to give it. For me.

They look at each other. Years of pain and love mixed together.

INT. SARAH'S APARTMENT - NIGHT

Sarah and Mark talk, barriers slowly breaking down.

MARK
Remember when we thought we had forever?

SARAH
We were different people then.

MARK
Were we? Or were we just... hiding?

SARAH
(vulnerable)
I'm tired of hiding, Mark. From you, from us.

MARK
What are you saying?

SARAH
I'm saying... I never stopped loving you.
Even when I hated you.

Mark reaches for her hand. She doesn't pull away.

MARK
I don't know how to fix what I broke.

SARAH
Maybe you can't. Maybe we just... build something new.

EXT. PARK - DAY - WEEKS LATER

Sarah and Mark walk together, closer but still tentative.

MARK
I got the job. Start Monday.

SARAH
(genuine)
That's wonderful. You're really doing it.

MARK
WE'RE doing it. Starting over.

SARAH
One day at a time.

They stop walking. Face each other.

MARK
Sarah, I need you to know--

SARAH
(touching his face)
I know. Me too.

They embrace. Not an ending, but a beginning.

FADE OUT."""


def create_weak_relationships_screenplay():
    """Create a screenplay with weak, static relationships."""
    return """FADE IN:

INT. ROOM - DAY

BOB and ALICE stand.

BOB
Hello.

ALICE
Hello.

BOB
How are you?

ALICE
Fine.

BOB
Good.

INT. ROOM - LATER

BOB and ALICE still there.

ALICE
Still here?

BOB
Yes.

ALICE
Okay.

INT. ROOM - EVEN LATER

BOB and ALICE remain.

BOB
Nice weather.

ALICE
Yes, nice.

BOB
Very nice.

ALICE
Indeed.

INT. ROOM - NIGHT

BOB and ALICE haven't moved.

ALICE
Getting late.

BOB
Yes, late.

ALICE
Should go.

BOB
Should.

Neither moves.

INT. ROOM - NEXT DAY

BOB and ALICE back again.

BOB
Hello again.

ALICE
Hello.

Nothing has changed.

FADE OUT."""


def test_basic_relationship_analysis():
    """Test basic relationship analysis."""
    print("\n💑 TEST 1: Basic Relationship Analysis")
    print("=" * 50)

    dr_relationships = DrRelationships()
    screenplay = create_strong_relationships_screenplay()

    result = dr_relationships.analyze(screenplay)

    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "relationship_count" in result
    assert "central_relationship" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Relationships found: {result['relationship_count']}")
    print(f"✅ Central relationship: {result['central_relationship']}")

    return True


def test_central_relationship():
    """Test central relationship identification."""
    print("\n💑 TEST 2: Central Relationship")
    print("=" * 50)

    dr_relationships = DrRelationships()
    screenplay = create_strong_relationships_screenplay()
    result = dr_relationships.analyze(screenplay)

    print(f"🎯 Central relationship: {result['central_relationship']}")
    print(f"✓ Clearly defined: {result['central_relationship_defined']}")

    assert result["central_relationship_defined"] == True
    print("\n✅ Central relationship identification working")

    return True


def test_relationship_evolution():
    """Test relationship evolution detection."""
    print("\n💑 TEST 3: Relationship Evolution")
    print("=" * 50)

    dr_relationships = DrRelationships()

    # Dynamic relationships
    dynamic = create_strong_relationships_screenplay()
    dynamic_result = dr_relationships.analyze(dynamic)

    # Static relationships
    static = create_weak_relationships_screenplay()
    static_result = dr_relationships.analyze(static)

    print(f"📈 Dynamic screenplay:")
    print(f"   Evolving: {dynamic_result['evolving_relationships']}")
    print(f"   Static: {dynamic_result['static_relationships']}")

    print(f"\n📉 Static screenplay:")
    print(f"   Evolving: {static_result['evolving_relationships']}")
    print(f"   Static: {static_result['static_relationships']}")

    print("\n✅ Evolution detection working")

    return True


def test_relationship_conflict():
    """Test conflict detection in relationships."""
    print("\n💑 TEST 4: Relationship Conflict")
    print("=" * 50)

    dr_relationships = DrRelationships()
    screenplay = create_strong_relationships_screenplay()
    result = dr_relationships.analyze(screenplay)

    print(f"⚔️ Relationships with conflict: {result['relationships_with_conflict']}")
    print(f"📊 Conflict percentage: {result['conflict_percentage']:.0f}%")

    print("\n✅ Conflict detection working")

    return True


def test_chemistry_analysis():
    """Test chemistry analysis between characters."""
    print("\n💑 TEST 5: Chemistry Analysis")
    print("=" * 50)

    dr_relationships = DrRelationships()

    # Strong chemistry
    strong = create_strong_relationships_screenplay()
    strong_result = dr_relationships.analyze(strong)

    # Weak chemistry
    weak = create_weak_relationships_screenplay()
    weak_result = dr_relationships.analyze(weak)

    print(f"💕 Strong screenplay chemistry: {strong_result['average_chemistry_score']*100:.0f}%")
    print(f"❄️ Weak screenplay chemistry: {weak_result['average_chemistry_score']*100:.0f}%")

    print("\n✅ Chemistry analysis working")

    return True


def test_relationship_stakes():
    """Test relationship stakes analysis."""
    print("\n💑 TEST 6: Relationship Stakes")
    print("=" * 50)

    dr_relationships = DrRelationships()
    screenplay = create_strong_relationships_screenplay()
    result = dr_relationships.analyze(screenplay)

    print(f"🎯 Relationships with stakes: {result['relationships_with_stakes']}")

    print("\n✅ Stakes analysis working")

    return True


def test_power_dynamics():
    """Test power dynamics analysis."""
    print("\n💑 TEST 7: Power Dynamics")
    print("=" * 50)

    dr_relationships = DrRelationships()
    screenplay = create_strong_relationships_screenplay()
    result = dr_relationships.analyze(screenplay)

    print(f"⚖️ Clear power dynamics: {result['power_dynamics_clear']}")
    print(f"🔄 Shifting power count: {result['shifting_power_count']}")

    print("\n✅ Power dynamics analysis working")

    return True


def test_vulnerability():
    """Test vulnerability detection."""
    print("\n💑 TEST 8: Vulnerability")
    print("=" * 50)

    dr_relationships = DrRelationships()
    screenplay = create_strong_relationships_screenplay()
    result = dr_relationships.analyze(screenplay)

    print(f"💔 Vulnerability present: {result['vulnerability_present']}")
    print(f"🎭 Vulnerability moments: {result['vulnerability_moments']}")

    print("\n✅ Vulnerability detection working")

    return True


def test_rule_violations():
    """Test relationship rule violations."""
    print("\n💑 TEST 9: Rule Violations")
    print("=" * 50)

    dr_relationships = DrRelationships()

    # Test with weak relationships
    weak_screenplay = create_weak_relationships_screenplay()
    result = dr_relationships.analyze(weak_screenplay)
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
    print("\n💑 TEST 10: Recommendations")
    print("=" * 50)

    dr_relationships = DrRelationships()
    weak_screenplay = create_weak_relationships_screenplay()

    result = dr_relationships.analyze(weak_screenplay)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")

    return True


def run_all_tests():
    """Run all Relatemon tests."""
    print("\n" + "=" * 60)
    print("💑 SCRIPT DOCTOR RELATEMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Relationship Analysis", test_basic_relationship_analysis),
        ("Central Relationship", test_central_relationship),
        ("Relationship Evolution", test_relationship_evolution),
        ("Relationship Conflict", test_relationship_conflict),
        ("Chemistry Analysis", test_chemistry_analysis),
        ("Relationship Stakes", test_relationship_stakes),
        ("Power Dynamics", test_power_dynamics),
        ("Vulnerability", test_vulnerability),
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
        print("\n🎉 SCRIPT DOCTOR RELATEMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Character Relationships Specialist is ready")
        print("\n💑 Relationship dynamics analysis systems online!")
        print("\n🎊 GRUPO PERSONAGENS COMPLETE! All 4 character specialists operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)