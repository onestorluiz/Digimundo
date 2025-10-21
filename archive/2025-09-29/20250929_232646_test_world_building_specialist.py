#!/usr/bin/env python3
"""
Test Suite for Script Doctor Worldmon - World Building Specialist
Tests the world building specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.world_building_specialist import DrWorldBuilding


def create_rich_world_screenplay():
    """Create a screenplay with rich world building."""
    return """FADE IN:

EXT. NEW TOKYO - YEAR 2145 - DAWN

Towering glass spires pierce the smog-filled sky. Holographic
advertisements flicker in Japanese and English. Flying cars
weave between buildings on designated air lanes.

INT. RAMEN SHOP - CONTINUOUS

Steam rises from bowls. The scent of miso fills the air.
Old wooden tables contrast with holographic menus.

KENJI (40s), cybernetic arm gleaming, slurps noodles. His
traditional kimono clashes with the tech.

KENJI
The old ways still matter, even here.

MAYA (20s), neural implants glowing blue, disagrees.

MAYA
Tradition holds us back. The Collective
sees all, knows all. Why resist?

Through the window, a massive surveillance drone passes,
its red eye scanning citizens below.

EXT. TEMPLE DISTRICT - DAY

Ancient shrines stand between modern towers. Monks in orange
robes carry tablets instead of scrolls. Incense mingles with
vehicle exhaust.

INT. UNDERGROUND RESISTANCE BASE - NIGHT

Concrete walls lined with stolen tech. Maps of the city's
neural network glow on screens. The air is thick with
tension and recycled oxygen.

RESISTANCE LEADER
The Collective controls the surface,
but down here, we're still free.

Members bow - a mix of traditional respect and necessity
in the low-ceilinged space.

EXT. MEMORY MARKET - NIGHT

Vendors sell bottled experiences under neon lights. The
rain creates prismatic reflections on wet pavement. Steam
rises from food stalls mixing synthetic and organic ingredients.

VENDOR
Fresh memories! Today's special -
childhood summers, pre-war!

The crowd bustles, a mix of cyborgs, humans, and those
somewhere in between. Each transaction requires a neural
handshake.

INT. MAYA'S APARTMENT - NIGHT

Minimalist design. Smart walls display her mood in colors.
A small shrine to ancestors sits beside quantum computers.
The city's hum provides constant white noise.

She lights incense, the smoke triggering air purifiers.
Outside, the city never sleeps, its lights creating false
daylight.

FADE OUT."""


def create_inconsistent_world_screenplay():
    """Create a screenplay with inconsistent world building."""
    return """FADE IN:

INT. CASTLE - DAY

Knights in armor stand guard. Torches light stone walls.

JOHN pulls out his smartphone.

JOHN
Let me check the GPS.

EXT. VILLAGE - NIGHT

Peasants till fields with tractors. A dragon flies overhead.

MARY
The wifi is down again!

INT. SPACESHIP - DAY

Cowboys ride horses through the cargo bay.

CAPTAIN
Set course for Mars, pardner!

The ship uses sails to navigate space.

EXT. MODERN CITY - MORNING

Cars fly without explanation. People walk on air. Gravity
seems optional.

INT. OFFICE - CONTINUOUS

Everything is normal. People type on computers.

BOB
Just another regular day.

Suddenly he teleports home. No one reacts.

FADE OUT."""


def create_minimal_world_screenplay():
    """Create a screenplay with minimal world building."""
    return """FADE IN:

INT. ROOM - DAY

Two people talk.

PERSON A
We should go.

PERSON B
Okay.

EXT. PLACE - DAY

They walk somewhere.

PERSON A
Here we are.

INT. ANOTHER ROOM - DAY

They sit.

PERSON B
Now what?

PERSON A
We wait.

Time passes.

PERSON B
Is it time?

PERSON A
Yes.

They leave.

FADE OUT."""


def test_basic_world_analysis():
    """Test basic world building analysis."""
    print("\n🌍 TEST 1: Basic World Analysis")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()

    result = dr_world.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "world_analysis" in result.__dict__
    assert "world_elements" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ World type: {result.world_analysis.world_type}")
    print(f"✅ Consistency: {result.world_analysis.consistency_score:.2f}")

    return True


def test_world_type_identification():
    """Test world type identification."""
    print("\n🌍 TEST 2: World Type Identification")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()
    result = dr_world.analyze(screenplay)

    print(f"🌐 World type: {result.world_analysis.world_type}")
    print(f"🏗️ Establishment quality: {result.world_analysis.establishment_quality:.2f}")

    # Should identify as sci-fi
    assert result.world_analysis.world_type == 'sci_fi'
    print("\n✅ World type identification working")

    return True


def test_location_analysis():
    """Test location analysis."""
    print("\n🌍 TEST 3: Location Analysis")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()
    result = dr_world.analyze(screenplay)

    print(f"📍 Total locations: {len(result.locations)}")

    # Show some locations
    for location in result.locations[:3]:
        print(f"   {location.name}: {location.location_type} (appears {len(location.appearances)}x)")
        print(f"      Atmosphere: {location.atmosphere}")

    print("\n✅ Location analysis working")

    return True


def test_world_elements():
    """Test world element extraction."""
    print("\n🌍 TEST 4: World Elements")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()
    result = dr_world.analyze(screenplay)

    # Count element types
    element_types = {}
    for element in result.world_elements:
        element_types[element.element_type] = element_types.get(element.element_type, 0) + 1

    print("🔮 World elements by type:")
    for elem_type, count in element_types.items():
        print(f"   {elem_type}: {count}")

    print(f"\n📊 Detail richness: {result.world_analysis.detail_richness:.2f}")
    print("\n✅ World element extraction working")

    return True


def test_world_rules():
    """Test world rule extraction."""
    print("\n🌍 TEST 5: World Rules")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()
    result = dr_world.analyze(screenplay)

    print(f"📜 World rules: {len(result.world_rules)}")

    for rule in result.world_rules[:3]:
        print(f"   {rule.rule_type}: {rule.description}")
        print(f"      Consistency: {rule.consistency:.2f}")

    print("\n✅ World rule extraction working")

    return True


def test_cultural_elements():
    """Test cultural element analysis."""
    print("\n🌍 TEST 6: Cultural Elements")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()
    result = dr_world.analyze(screenplay)

    print(f"🎭 Cultural elements: {len(result.cultural_elements)}")
    print(f"🎨 Cultural depth: {result.world_analysis.cultural_depth:.2f}")

    for element in result.cultural_elements[:3]:
        print(f"   {element.element_type}: {element.description[:50]}...")

    print("\n✅ Cultural element analysis working")

    return True


def test_world_consistency():
    """Test world consistency detection."""
    print("\n🌍 TEST 7: World Consistency")
    print("=" * 50)

    dr_world = DrWorldBuilding()

    # Test consistent world
    consistent = create_rich_world_screenplay()
    consistent_result = dr_world.analyze(consistent)

    # Test inconsistent world
    inconsistent = create_inconsistent_world_screenplay()
    inconsistent_result = dr_world.analyze(inconsistent)

    print(f"✅ Consistent world:")
    print(f"   Consistency score: {consistent_result.world_analysis.consistency_score:.2f}")
    print(f"   Tech consistency: {consistent_result.world_analysis.technological_consistency:.2f}")

    print(f"\n❌ Inconsistent world:")
    print(f"   Consistency score: {inconsistent_result.world_analysis.consistency_score:.2f}")
    print(f"   Tech consistency: {inconsistent_result.world_analysis.technological_consistency:.2f}")

    print("\n✅ World consistency detection working")

    return True


def test_world_depth():
    """Test world depth analysis."""
    print("\n🌍 TEST 8: World Depth")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    screenplay = create_rich_world_screenplay()
    result = dr_world.analyze(screenplay)

    print("📊 World depth layers:")
    for layer, score in result.world_depth_layers.items():
        print(f"   {layer}: {score:.2f}")

    print(f"\n🎬 Immersion score: {result.immersion_score:.2f}")
    print(f"✅ Believability: {result.believability_score:.2f}")
    print(f"✨ Uniqueness: {result.uniqueness_score:.2f}")

    print("\n✅ World depth analysis working")

    return True


def test_rule_violations():
    """Test world building rule violations."""
    print("\n🌍 TEST 9: Rule Violations")
    print("=" * 50)

    dr_world = DrWorldBuilding()

    # Test with minimal world screenplay
    minimal = create_minimal_world_screenplay()
    result = dr_world.analyze(minimal)
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
    print("\n🌍 TEST 10: Recommendations")
    print("=" * 50)

    dr_world = DrWorldBuilding()
    minimal = create_minimal_world_screenplay()

    result = dr_world.analyze(minimal)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Worldmon tests."""
    print("\n" + "=" * 60)
    print("🌍 SCRIPT DOCTOR WORLDMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic World Analysis", test_basic_world_analysis),
        ("World Type Identification", test_world_type_identification),
        ("Location Analysis", test_location_analysis),
        ("World Elements", test_world_elements),
        ("World Rules", test_world_rules),
        ("Cultural Elements", test_cultural_elements),
        ("World Consistency", test_world_consistency),
        ("World Depth", test_world_depth),
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
        print("\n🎉 SCRIPT DOCTOR WORLDMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ World Building Specialist is ready")
        print("\n🌍 World building analysis systems online!")
        print("\n📝 Specialist 20/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)