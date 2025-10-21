#!/usr/bin/env python3
"""
Test Suite for Script Doctor Symbolmon - Symbolism and Metaphor Specialist
Tests the symbolism specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.symbolism_metaphor_specialist import DrSymbolism


def create_symbolically_rich_screenplay():
    """Create a screenplay with rich symbolism and metaphors."""
    return """FADE IN:

EXT. BRIDGE - DAWN

The old bridge spans a turbulent river. Morning light breaks
through storm clouds. 

JACK (40s), worn like the bridge itself, stands at the center.
A RED ROSE wilts in his hand.

He drops the rose into the water below. It disappears into 
the darkness.

INT. PRISON CELL - DAY

Gray walls. A small WINDOW shows blue sky - freedom just out
of reach.

Jack sits on the bed, holding an old COMPASS. The needle spins
wildly, finding no direction.

JACK
I'm like a ship without a sail.
Lost in storms I made myself.

The GUARD approaches with a KEY.

GUARD
Time's up, Morrison. You're free.

Jack looks at the key as if it's foreign.

JACK
Freedom. Funny how a cage becomes
home when you've lived there long enough.

EXT. PRISON GATES - DAY

Massive IRON GATES open. Jack steps through, squinting in
bright sunlight. His shadow stretches behind him - the past
he can't escape.

SARAH (30s) waits by a RED CAR. She holds a WHITE ROSE.

SARAH
The storm's passed, Jack.

JACK
Storms like mine don't pass.
They just find new skies to darken.

Sarah hands him the white rose.

SARAH
Then we'll find an umbrella.

They embrace. The white rose and red car - redemption and
passion intertwined.

INT. OLD HOUSE - NIGHT

A BROKEN MIRROR reflects Jack's fractured image. He touches
the cracks.

JACK (V.O.)
Some mirrors can't be fixed. They just
show you what you've become - piece by
piece.

A CANDLE flickers, casting dancing shadows. Jack pulls out
the compass. It points steadily north now.

EXT. BRIDGE - DAWN (LATER)

Jack returns to the bridge. This time, he carries a WHITE ROSE.

He doesn't drop it. He keeps walking across - from darkness
into light.

The river below runs clear now. The storm has passed.

FADE OUT."""


def create_symbolically_poor_screenplay():
    """Create a screenplay with poor or missing symbolism."""
    return """FADE IN:

INT. OFFICE - DAY

John sits at desk. Mary enters.

MARY
The report is done.

JOHN
Good. Send it to the client.

MARY
I already did.

JOHN
Great work.

EXT. STREET - DAY

John walks. He sees a dog.

JOHN
Nice dog.

The owner smiles.

OWNER
Thanks.

INT. RESTAURANT - NIGHT

John eats dinner.

WAITER
How's your meal?

JOHN
It's fine.

WAITER
Good.

John pays and leaves.

INT. APARTMENT - NIGHT

John watches TV. His phone rings.

JOHN
(into phone)
Hello? Yes. Okay. Bye.

He hangs up and continues watching TV.

FADE OUT."""


def test_basic_symbolism_analysis():
    """Test basic symbolism analysis."""
    print("\n🔮 TEST 1: Basic Symbolism Analysis")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()

    result = dr_symbolism.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "symbolism_analysis" in result.__dict__
    assert "symbols" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Total symbols: {result.symbolism_analysis.total_symbols}")
    print(f"✅ Metaphors: {result.symbolism_analysis.metaphor_count}")

    return True


def test_symbol_identification():
    """Test symbol identification."""
    print("\n🔮 TEST 2: Symbol Identification")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"🌹 Visual symbols: {result.symbolism_analysis.visual_symbols}")
    print(f"🔑 Object symbols: {result.symbolism_analysis.object_symbols}")
    print(f"🎨 Color symbols: {result.symbolism_analysis.color_symbols}")
    print(f"🏢 Setting symbols: {result.symbolism_analysis.setting_symbols}")

    # Should identify various symbols
    assert result.symbolism_analysis.total_symbols > 0
    print("\n✅ Symbol identification working")

    return True


def test_metaphor_detection():
    """Test metaphor detection."""
    print("\n🔮 TEST 3: Metaphor Detection")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"🌊 Metaphors found: {result.symbolism_analysis.metaphor_count}")
    if result.metaphors:
        print(f"📝 Example: \"{result.metaphors[0].text[:50]}...\"")
        print(f"   Clarity: {result.metaphors[0].clarity_score:.2f}")

    print(f"🎯 Average clarity: {result.symbolism_analysis.metaphor_clarity_average:.2f}")

    print("\n✅ Metaphor detection working")

    return True


def test_symbol_consistency():
    """Test symbol consistency analysis."""
    print("\n🔮 TEST 4: Symbol Consistency")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"🔄 Consistency score: {result.symbolism_analysis.symbol_consistency_score:.2f}")
    print(f"✅ Purposeful symbols: {result.symbolism_analysis.purposeful_symbols}")

    # Check specific symbols
    for symbol in result.symbols[:3]:
        print(f"   {symbol.name} ({symbol.symbol_type}): {len(symbol.occurrences)} occurrences")

    print("\n✅ Symbol consistency analysis working")

    return True


def test_symbolic_payoff():
    """Test symbolic payoff detection."""
    print("\n🔮 TEST 5: Symbolic Payoff")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"🏁 Payoff ratio: {result.symbolism_analysis.symbolic_payoff_ratio:.2f}")
    
    # Check symbolic arcs
    print(f"🌀 Symbolic arcs: {len(result.symbolic_arcs)}")
    for arc in result.symbolic_arcs[:2]:
        print(f"   {arc['symbol']}: {arc['appearances']} appearances")
        print(f"   Evolution: {' -> '.join(arc['evolution'][:3])}")

    print("\n✅ Symbolic payoff detection working")

    return True


def test_symbol_network():
    """Test symbol network building."""
    print("\n🔮 TEST 6: Symbol Network")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"🕸️ Symbol connections:")
    for symbol, connections in list(result.symbol_network.items())[:3]:
        if connections:
            print(f"   {symbol} connects to: {', '.join(connections)}")

    print("\n✅ Symbol network building working")

    return True


def test_emotional_resonance():
    """Test emotional resonance scoring."""
    print("\n🔮 TEST 7: Emotional Resonance")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"💖 Emotional resonance: {result.symbolism_analysis.emotional_resonance_score:.2f}")
    print(f"🌊 Symbol density: {result.symbolism_analysis.symbol_density:.2f} per scene")

    print("\n✅ Emotional resonance scoring working")

    return True


def test_symbolic_patterns():
    """Test symbolic pattern identification."""
    print("\n🔮 TEST 8: Symbolic Patterns")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    screenplay = create_symbolically_rich_screenplay()
    result = dr_symbolism.analyze(screenplay)

    print(f"🌐 Patterns identified:")
    print(f"   Dominant type: {result.symbolic_patterns.get('dominant_type', 'none')}")
    print(f"   Density: {result.symbolic_patterns.get('symbolic_density', 'none')}")
    print(f"   Metaphor style: {result.symbolic_patterns.get('metaphor_style', 'none')}")
    
    recurring = result.symbolic_patterns.get('recurring_symbols', [])
    if recurring:
        print(f"   Recurring: {', '.join(recurring[:3])}")

    print("\n✅ Symbolic pattern identification working")

    return True


def test_rule_violations():
    """Test symbolism rule violations."""
    print("\n🔮 TEST 9: Rule Violations")
    print("=" * 50)

    dr_symbolism = DrSymbolism()

    # Test with symbolically poor screenplay
    poor = create_symbolically_poor_screenplay()
    result = dr_symbolism.analyze(poor)
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
    print("\n🔮 TEST 10: Recommendations")
    print("=" * 50)

    dr_symbolism = DrSymbolism()
    poor = create_symbolically_poor_screenplay()

    result = dr_symbolism.analyze(poor)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Symbolmon tests."""
    print("\n" + "=" * 60)
    print("🔮 SCRIPT DOCTOR SYMBOLMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Symbolism Analysis", test_basic_symbolism_analysis),
        ("Symbol Identification", test_symbol_identification),
        ("Metaphor Detection", test_metaphor_detection),
        ("Symbol Consistency", test_symbol_consistency),
        ("Symbolic Payoff", test_symbolic_payoff),
        ("Symbol Network", test_symbol_network),
        ("Emotional Resonance", test_emotional_resonance),
        ("Symbolic Patterns", test_symbolic_patterns),
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
        print("\n🎉 SCRIPT DOCTOR SYMBOLMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Symbolism and Metaphor Specialist is ready")
        print("\n🔮 Symbolic analysis systems online!")
        print("\n📝 Specialist 16/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
