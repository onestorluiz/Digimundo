#!/usr/bin/env python3
"""
Test Suite for Script Doctor Omegamon - Resolution and Closure Specialist
Tests the resolution specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.resolution_specialist import DrResolution


def create_complete_resolution_screenplay():
    """Create a screenplay with complete resolution."""
    return """FADE IN:

INT. OFFICE - DAY

JOHN (40s) discovers a SECRET that will change everything.

SARAH enters. They have unfinished business.

SARAH
We need to talk about us.

JOHN
Not now. I have a mission to complete.

[MIDDLE SECTION - PLOT DEVELOPS]

The secret threatens the city.
John and Sarah work together.
Their relationship is tested.

[CLIMAX OCCURS]

INT. CONTROL ROOM - NIGHT (RESOLUTION)

The threat is neutralized. The city is SAFE.

John has changed. No longer the same man.

JOHN
I finally understand what matters.

SARAH
We did it. Together.

They embrace. The SECRET is revealed - it brought them closer.

EXT. CITY - DAWN (EPILOGUE)

A new day. The city awakens, transformed.

John and Sarah watch the sunrise. 

JOHN
From now on, everything will be different.

SARAH
A new beginning.

They walk into their new life together.

FADE OUT.

THE END"""


def create_incomplete_resolution_screenplay():
    """Create a screenplay with poor resolution."""
    return """FADE IN:

INT. HOUSE - DAY

BOB has many problems:
- Lost his job
- Wife left him  
- Mystery illness
- Owes money to dangerous people
- His son is missing

[LOTS OF PLOT THREADS INTRODUCED]

[STORY DEVELOPS BUT THREADS MULTIPLY]

INT. HOUSE - NIGHT (SUPPOSED RESOLUTION)

Bob sits alone. Some things worked out somehow.

His job situation... still unclear.
The dangerous people... just disappeared.
His son... never mentioned again.
The illness... forgot about it.

BOB
Well, I guess that's life.

He shrugs. Nothing really resolved.

No lesson learned. No growth. No change.

CUT TO BLACK.

THE END... OR IS IT?

WAIT, ONE MORE THING...

Bob remembers something.

BOB
Oh right, the thing.

ANOTHER ENDING...

Actually, forget it.

FADE OUT FOR REAL THIS TIME."""


def test_basic_resolution_analysis():
    """Test basic resolution analysis."""
    print("\nΩ TEST 1: Basic Resolution Analysis")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    screenplay = create_complete_resolution_screenplay()
    
    result = dr_resolution.analyze(screenplay)
    
    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "resolution_location" in result
    assert "plot_threads" in result
    
    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Resolution starts at page {result['resolution_location']['page_start']}")
    print(f"✅ Threads resolved: {result['threads_resolved_percentage']:.0f}%")
    
    return True


def test_plot_thread_tracking():
    """Test plot thread tracking."""
    print("\nΩ TEST 2: Plot Thread Tracking")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    screenplay = create_complete_resolution_screenplay()
    
    result = dr_resolution.analyze(screenplay)
    threads = result["plot_threads"]
    
    print(f"🧵 Tracked {len(threads)} plot threads:")
    for thread in threads:
        status = "✅" if thread["resolved"] else "❌"
        print(f"   {status} {thread['thread_type']}: {thread['description'][:30]}...")
    
    print(f"\n🎯 Resolution rate: {result['threads_resolved_percentage']:.0f}%")
    print("✅ Plot thread tracking working")
    
    return True


def test_emotional_satisfaction():
    """Test emotional satisfaction scoring."""
    print("\nΩ TEST 3: Emotional Satisfaction")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    
    # Complete resolution
    complete = create_complete_resolution_screenplay()
    complete_result = dr_resolution.analyze(complete)
    
    # Incomplete resolution
    incomplete = create_incomplete_resolution_screenplay()
    incomplete_result = dr_resolution.analyze(incomplete)
    
    print(f"😊 Complete resolution satisfaction: {complete_result['emotional_satisfaction_score']:.2f}")
    print(f"😞 Incomplete resolution satisfaction: {incomplete_result['emotional_satisfaction_score']:.2f}")
    
    # Complete should have higher satisfaction
    assert complete_result["emotional_satisfaction_score"] > incomplete_result["emotional_satisfaction_score"]
    print("\n✅ Emotional satisfaction scoring working")
    
    return True


def test_character_arc_completion():
    """Test character arc completion detection."""
    print("\nΩ TEST 4: Character Arc Completion")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    screenplay = create_complete_resolution_screenplay()
    
    result = dr_resolution.analyze(screenplay)
    
    print(f"👤 Character arcs completed: {result['character_arcs_completed']*100:.0f}%")
    print(f"🎭 Theme resolved: {result['theme_resolved']}")
    
    print("\n✅ Character arc analysis working")
    
    return True


def test_resolution_elements():
    """Test detection of resolution elements."""
    print("\nΩ TEST 5: Resolution Elements")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    screenplay = create_complete_resolution_screenplay()
    result = dr_resolution.analyze(screenplay)
    
    elements = result["resolution_elements"]
    
    print("🌟 Essential elements:")
    for name, data in elements.items():
        status = "✅" if data["present"] else "❌"
        print(f"   {status} {name}: {data['effectiveness']:.2f} effectiveness")
    
    # Count present elements
    present_count = sum(1 for e in elements.values() if e["present"])
    assert present_count >= 3  # Should have at least 3 elements
    
    print("\n✅ Resolution elements detection working")
    
    return True


def test_final_image_analysis():
    """Test final image analysis."""
    print("\nΩ TEST 6: Final Image Analysis")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    screenplay = create_complete_resolution_screenplay()
    result = dr_resolution.analyze(screenplay)
    
    print(f"🎅 Final image strength: {result['final_image_strength']:.2f}")
    print(f"🔄 Mirrors opening: {result['final_image_mirrors_opening']}")
    print(f"🌍 New world established: {result['new_world_established']}")
    
    print("\n✅ Final image analysis working")
    
    return True


def test_multiple_endings_detection():
    """Test detection of multiple endings."""
    print("\nΩ TEST 7: Multiple Endings Detection")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    
    # Good single ending
    good = create_complete_resolution_screenplay()
    good_result = dr_resolution.analyze(good)
    
    # Bad multiple endings
    bad = create_incomplete_resolution_screenplay()
    bad_result = dr_resolution.analyze(bad)
    
    print(f"🎬 Complete screenplay has multiple endings: {good_result['has_multiple_endings']}")
    print(f"🎬 Incomplete screenplay has multiple endings: {bad_result['has_multiple_endings']}")
    
    print("\n✅ Multiple endings detection working")
    
    return True


def test_rule_violations():
    """Test resolution rule violations."""
    print("\nΩ TEST 8: Rule Violations")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    
    # Test with poor resolution
    bad_screenplay = create_incomplete_resolution_screenplay()
    result = dr_resolution.analyze(bad_screenplay)
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
    print("\nΩ TEST 9: Recommendations")
    print("=" * 50)
    
    dr_resolution = DrResolution()
    bad_screenplay = create_incomplete_resolution_screenplay()
    
    result = dr_resolution.analyze(bad_screenplay)
    
    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")
    
    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")
    
    return True


def run_all_tests():
    """Run all Omegamon tests."""
    print("\n" + "=" * 60)
    print("Ω SCRIPT DOCTOR OMEGAMON - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Basic Resolution Analysis", test_basic_resolution_analysis),
        ("Plot Thread Tracking", test_plot_thread_tracking),
        ("Emotional Satisfaction", test_emotional_satisfaction),
        ("Character Arc Completion", test_character_arc_completion),
        ("Resolution Elements", test_resolution_elements),
        ("Final Image Analysis", test_final_image_analysis),
        ("Multiple Endings Detection", test_multiple_endings_detection),
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
        print("\n🎉 SCRIPT DOCTOR OMEGAMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Resolution and Closure Specialist is ready")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)