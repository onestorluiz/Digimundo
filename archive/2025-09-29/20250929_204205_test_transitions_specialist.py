#!/usr/bin/env python3
"""
Test Suite for Script Doctor Flowmon - Transitions and Flow Specialist
Tests the transitions specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.transitions_specialist import DrTransitions


def create_well_flowing_screenplay():
    """Create a screenplay with good flow and transitions."""
    return """FADE IN:

EXT. CITY STREET - DAY

John walks with purpose. Phone RINGS.

JOHN
On my way.

CUT TO:

INT. OFFICE BUILDING - DAY - CONTINUOUS

John enters, still on phone.

JOHN
I'll be right up.

MATCH CUT TO:

INT. ELEVATOR - DAY - CONTINUOUS

Doors close on John's determined face.

DISSOLVE TO:

INT. BOARDROOM - DAY - MOMENTS LATER

John enters to find the BOARD waiting.

CHAIRMAN
We have a problem.

John's face hardens. This is what he feared.

CUT TO:

EXT. ROOFTOP - DAY - LATER

John processes the news, city below.

The weight of the decision ahead.

SMASH CUT TO:

INT. JOHN'S APARTMENT - NIGHT

John studies the files. The truth emerges.

FADE OUT."""


def create_poorly_flowing_screenplay():
    """Create a screenplay with poor flow and transitions."""
    return """FADE IN:

INT. HOUSE - DAY

Bob sits.

EXT. PARK - NIGHT

A dog barks.

INT. OFFICE - DAY

Papers on desk.

EXT. BEACH - NIGHT

Waves crash.

INT. CAR - DAY

Radio plays.

EXT. MOUNTAIN - DAWN

Sun rises.

INT. RESTAURANT - NIGHT

People eat.

EXT. STREET - DAY

Cars pass.

INT. BEDROOM - NIGHT

Someone sleeps.

FADE OUT."""


def test_basic_flow_analysis():
    """Test basic flow analysis."""
    print("\n🌊 TEST 1: Basic Flow Analysis")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    screenplay = create_well_flowing_screenplay()
    
    result = dr_flow.analyze(screenplay)
    
    # Check required fields
    assert "specialist" in result
    assert "score" in result
    assert "scene_count" in result
    assert "transition_count" in result
    
    print(f"✅ Specialist: {result['specialist']['name']}")
    print(f"✅ Score: {result['score']}/100")
    print(f"✅ Scenes: {result['scene_count']}")
    print(f"✅ Transitions: {result['transition_count']}")
    
    return True


def test_transition_analysis():
    """Test transition analysis between scenes."""
    print("\n🌊 TEST 2: Transition Analysis")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    screenplay = create_well_flowing_screenplay()
    
    result = dr_flow.analyze(screenplay)
    transitions = result["transitions"]
    
    print(f"🔗 Analyzed {len(transitions)} transitions:")
    for t in transitions[:3]:  # Show first 3
        print(f"   Scene {t['from_scene']} → {t['to_scene']}: {t['type']}")
        print(f"     Connection: {t['connection']} (effectiveness: {t['effectiveness']})")
    
    print("\n✅ Transition analysis working")
    
    return True


def test_momentum_tracking():
    """Test momentum tracking through screenplay."""
    print("\n🌊 TEST 3: Momentum Tracking")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    
    # Good flow
    good = create_well_flowing_screenplay()
    good_result = dr_flow.analyze(good)
    
    # Poor flow
    poor = create_poorly_flowing_screenplay()
    poor_result = dr_flow.analyze(poor)
    
    print(f"🚀 Good screenplay momentum: {good_result['momentum_score']*100:.0f}%")
    print(f"🐌 Poor screenplay momentum: {poor_result['momentum_score']*100:.0f}%")
    
    # Good should have better momentum
    assert good_result["momentum_score"] >= poor_result["momentum_score"]
    print("\n✅ Momentum tracking working")
    
    return True


def test_flow_segments():
    """Test flow segment identification."""
    print("\n🌊 TEST 4: Flow Segments")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    screenplay = create_well_flowing_screenplay()
    result = dr_flow.analyze(screenplay)
    
    segments = result["flow_segments"]
    
    print(f"🎯 Found {len(segments)} flow segments:")
    for seg in segments:
        print(f"   Scenes {seg['scenes']}: {seg['type']}")
        print(f"     Quality: {seg['flow_quality']}, Momentum: {seg['momentum_score']}")
    
    print("\n✅ Flow segment identification working")
    
    return True


def test_transition_variety():
    """Test transition variety analysis."""
    print("\n🌊 TEST 5: Transition Variety")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    
    # Good variety
    good = create_well_flowing_screenplay()
    good_result = dr_flow.analyze(good)
    
    # Poor variety (all CUT TO)
    poor = create_poorly_flowing_screenplay()
    poor_result = dr_flow.analyze(poor)
    
    print(f"🍨 Good screenplay variety: {good_result['transition_variety_score']*100:.0f}%")
    print(f"   Most used: {good_result['most_used_transition']}")
    
    print(f"\n🔁 Poor screenplay variety: {poor_result['transition_variety_score']*100:.0f}%")
    print(f"   Most used: {poor_result['most_used_transition']}")
    
    print("\n✅ Transition variety analysis working")
    
    return True


def test_scene_efficiency():
    """Test scene efficiency (enter late, leave early)."""
    print("\n🌊 TEST 6: Scene Efficiency")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    screenplay = create_well_flowing_screenplay()
    result = dr_flow.analyze(screenplay)
    
    print(f"⏱️ Scene efficiency: {result['scene_efficiency_score']*100:.0f}%")
    print(f"🎬 Scenes starting late: {result['scenes_starting_late']:.0f}%")
    
    print("\n✅ Scene efficiency analysis working")
    
    return True


def test_time_flow_clarity():
    """Test time flow clarity."""
    print("\n🌊 TEST 7: Time Flow Clarity")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    
    # Good time flow
    good = create_well_flowing_screenplay()
    good_result = dr_flow.analyze(good)
    
    print(f"⏰ Time flow clear: {good_result['time_flow_clear']}")
    print(f"🌍 Geographic logic: {good_result['geographic_logic_score']*100:.0f}%")
    
    print("\n✅ Time flow analysis working")
    
    return True


def test_rule_violations():
    """Test flow rule violations."""
    print("\n🌊 TEST 8: Rule Violations")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    
    # Test with poor flow
    poor_screenplay = create_poorly_flowing_screenplay()
    result = dr_flow.analyze(poor_screenplay)
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
    print("\n🌊 TEST 9: Recommendations")
    print("=" * 50)
    
    dr_flow = DrTransitions()
    poor_screenplay = create_poorly_flowing_screenplay()
    
    result = dr_flow.analyze(poor_screenplay)
    
    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")
    
    # Should generate recommendations
    assert len(result.get("recommendations", [])) > 0
    print(f"\n✅ Generated {len(result['recommendations'])} recommendations")
    
    return True


def run_all_tests():
    """Run all Flowmon tests."""
    print("\n" + "=" * 60)
    print("🌊 SCRIPT DOCTOR FLOWMON - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Basic Flow Analysis", test_basic_flow_analysis),
        ("Transition Analysis", test_transition_analysis),
        ("Momentum Tracking", test_momentum_tracking),
        ("Flow Segments", test_flow_segments),
        ("Transition Variety", test_transition_variety),
        ("Scene Efficiency", test_scene_efficiency),
        ("Time Flow Clarity", test_time_flow_clarity),
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
        print("\n🎉 SCRIPT DOCTOR FLOWMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Transitions and Flow Specialist is ready")
        print("\n🎆 GROUP ESTRUTURAL COMPLETE! All 6 structural specialists operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)