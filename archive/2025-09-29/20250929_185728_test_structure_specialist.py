#!/usr/bin/env python3
"""
Test Suite for Script Doctor Structuremon - Narrative Architecture Specialist
Tests the structure specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.structure_specialist import DrStructure


def create_test_screenplay():
    """Create a simple test screenplay with clear structure."""
    return """FADE IN:

EXT. SUBURBAN HOUSE - DAY (Page 1 - Opening Image)

A perfect white picket fence. Everything pristine.

INT. KITCHEN - DAY (Pages 1-10 - Setup)

JOHN (40s) reads the newspaper. Normal morning routine.

SARAH (30s) enters, worried.

SARAH
John, we need to talk.

JOHN
What's wrong?

SARAH
I got a call. Your father... he's dead. (Page 12 - Inciting Incident)

John drops his coffee cup. It SHATTERS.

JOHN
That's impossible. He died ten years ago. (Pages 15-20 - Debate)

SARAH
That's what I thought too. But the police say otherwise.

JOHN
I have to see for myself. (Page 25 - Break into Act 2)

EXT. HIGHWAY - DAY (Pages 30-50 - Fun and Games)

John drives fast, memories flooding back. Signs of pursuit.

INT. MOTEL ROOM - NIGHT (Page 55 - Midpoint)

John discovers a VIDEO on his phone. His father is ALIVE, held captive.

FATHER (ON VIDEO)
They want the files, John. Don't give them--

Video cuts out. CRASH! Door breaks down. (Pages 60-70 - Bad Guys Close In)

EXT. ABANDONED WAREHOUSE - NIGHT (Page 75 - All Is Lost)

John cornered. No escape. Guns pointed at him.

VILLAIN
Your father dies unless you give us the decrypt key.

JOHN
I don't have it!

VILLAIN
Then he dies. (Page 80 - Break into Act 3)

JOHN
Wait! I know where it is.

INT. WAREHOUSE - FINAL SHOWDOWN - NIGHT (Page 90 - Climax)

John fights for his life and his father's. Uses hidden skills.

EXT. WAREHOUSE - DAWN (Page 110 - Final Image)

John and his father walk away. The warehouse burns behind them.

FATHER
You came for me.

JOHN
Family doesn't leave family behind.

FADE OUT.

THE END"""


def test_basic_analysis():
    """Test basic structural analysis."""
    print("\n🧪 TEST 1: Basic Structure Analysis")
    print("=" * 50)

    dr_structure = DrStructure()
    screenplay = create_test_screenplay()

    result = dr_structure.analyze(screenplay)

    # Check that all required fields are present
    assert "specialist" in result
    assert "score" in result
    assert "structural_elements" in result
    assert "act_analysis" in result

    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")

    # Check structural elements detection
    elements = result["structural_elements"]
    found_elements = [k for k, v in elements.items() if v["status"] == "found"]
    print(f"✅ Found {len(found_elements)} structural elements")

    for element_name, element_data in elements.items():
        if element_data["status"] == "found":
            print(f"   • {element_data['name']}: page {element_data['found_at']}")

    return True


def test_act_proportions():
    """Test three-act structure analysis."""
    print("\n🧪 TEST 2: Three-Act Proportions")
    print("=" * 50)

    dr_structure = DrStructure()
    screenplay = create_test_screenplay()

    result = dr_structure.analyze(screenplay)
    acts = result["act_analysis"]

    print("📊 Act Breakdown:")
    for act_name, act_data in acts.items():
        status_emoji = "✅" if act_data["status"] == "good" else "⚠️"
        print(f"{status_emoji} {act_name.upper()}:")
        print(f"   Pages: {act_data['pages']}")
        print(f"   Percentage: {act_data['percentage']:.1f}% (expected: {act_data['expected']}%)")
        print(f"   Status: {act_data['status']}")

    # Verify act analysis exists
    assert acts["act1"]["expected"] == 25
    assert acts["act2"]["expected"] == 50
    assert acts["act3"]["expected"] == 25

    print("\n✅ Act proportion analysis working correctly")
    return True


def test_rule_violations():
    """Test rule violation detection."""
    print("\n🧪 TEST 3: Rule Violation Detection")
    print("=" * 50)

    dr_structure = DrStructure()

    # Test with a badly structured screenplay
    bad_screenplay = """FADE IN:

Just a bunch of random scenes without structure.
No clear acts or plot points.
Everything happens randomly.
The end."""

    result = dr_structure.analyze(bad_screenplay)
    violations = result.get("rule_violations", [])

    print(f"📋 Found {len(violations)} violations:")
    for violation in violations:
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }.get(violation["severity"], "⚪")

        print(f"{severity_emoji} [{violation['severity'].upper()}] {violation['title']}")
        print(f"   Fix: {violation['fix']}")

    # Should detect violations in bad screenplay
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")
    return True


def test_diagnosis_generation():
    """Test diagnosis and recommendations."""
    print("\n🧪 TEST 4: Diagnosis Generation")
    print("=" * 50)

    dr_structure = DrStructure()
    screenplay = create_test_screenplay()

    result = dr_structure.analyze(screenplay)

    print("📝 DIAGNOSIS:")
    print(result["diagnosis"])

    print("\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")

    # Verify diagnosis exists
    assert "diagnosis" in result
    assert len(result["diagnosis"]) > 0
    assert "signature" in result

    print(f"\n✅ {result['signature']}")
    return True


def test_page_count_estimation():
    """Test page count estimation."""
    print("\n🧪 TEST 5: Page Count Estimation")
    print("=" * 50)

    dr_structure = DrStructure()

    # Create screenplay with known line count
    lines = ["Line " + str(i) for i in range(550)]  # Should be ~10 pages
    screenplay = "\n".join(lines)

    result = dr_structure.analyze(screenplay)
    page_count = result["page_count"]

    print(f"📄 Lines: 550")
    print(f"📄 Estimated pages: {page_count}")
    print(f"📄 Lines per page: {550 / page_count:.1f}")

    # Should be approximately 10 pages (550 / 55)
    assert 8 <= page_count <= 12
    print("✅ Page count estimation accurate")
    return True


def run_all_tests():
    """Run all Dr. Structure tests."""
    print("\n" + "=" * 60)
    print("🏥 SCRIPT DOCTOR STRUCTUREMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Analysis", test_basic_analysis),
        ("Act Proportions", test_act_proportions),
        ("Rule Violations", test_rule_violations),
        ("Diagnosis Generation", test_diagnosis_generation),
        ("Page Count Estimation", test_page_count_estimation)
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
        print("\n🎉 SCRIPT DOCTOR STRUCTUREMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Narrative Architecture Specialist is ready")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)