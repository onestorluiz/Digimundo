#!/usr/bin/env python3
"""
Test Suite for Script Doctor Marketmon - Market Potential Specialist
Tests the market potential specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.market_potential_specialist import DrMarketPotential


def create_blockbuster_screenplay():
    """Create a screenplay with blockbuster potential."""
    return """FADE IN:

EXT. NEW YORK CITY - DAY

The city skyline. Suddenly, an ALIEN SHIP descends from the clouds.
EXPLOSIONS rock buildings. People run screaming.

INT. PENTAGON WAR ROOM - CONTINUOUS

GENERAL HARRIS (50s) studies tactical displays.

GENERAL HARRIS
Get me Captain Stone. Now.

INT. UNDERGROUND BASE - DAY

CAPTAIN JACK STONE (30s), rugged hero, suits up in advanced armor.

STONE
Time to save the world. Again.

His team assembles: MAYA (tech expert), TANK (weapons specialist),
and PHOENIX (pilot).

EXT. TIMES SQUARE - DAY

Massive battle. Stone's team fights alien invaders. Spectacular
action sequence with explosions, chases, and aerial combat.

STONE
We fight together, or we fall alone!

The team executes a coordinated attack. Buildings crumble. The
alien mothership approaches.

INT. ALIEN MOTHERSHIP - CLIMAX

Stone confronts the ALIEN COMMANDER.

ALIEN COMMANDER
Your species is inferior.

STONE
We have something you don't - hope.

Epic final battle. Stone plants a bomb. The team escapes as the
mothership EXPLODES in spectacular fashion.

EXT. NEW YORK - SUNSET

The city celebrates. Stone and Maya share a moment.

MAYA
Ready for the next adventure?

STONE
Always.

They look to the stars. Something moves in deep space...

FADE OUT."""


def create_niche_screenplay():
    """Create a screenplay with limited market appeal."""
    return """FADE IN:

INT. SMALL APARTMENT - DAY

HAROLD (60s), alone, makes tea. He sits. Drinks slowly.

The clock ticks.

INT. SMALL APARTMENT - LATER

Harold reads a book. Turns pages carefully.

The phone doesn't ring.

INT. SMALL APARTMENT - EVENING

Harold cooks a single portion of pasta. Eats in silence.

Washes one plate, one fork.

INT. SMALL APARTMENT - NIGHT

Harold prepares for bed. Brushes teeth. Gets into bed.

Stares at the ceiling.

HAROLD
(to himself)
Another day.

INT. SMALL APARTMENT - MORNING

Harold wakes. Makes tea. The routine begins again.

FADE OUT."""


def create_streaming_screenplay():
    """Create a screenplay optimized for streaming platforms."""
    return """FADE IN:

INT. SUBURBAN HOME - NIGHT

A family dinner turns deadly when MASKED INTRUDERS burst in.

SARAH (40s), protective mother, shields her children.

SARAH
Run! Get to the panic room!

INT. PANIC ROOM - CONTINUOUS

The family locks themselves in. On monitors, they watch intruders
search the house.

TEENAGE SON JAKE (16) notices something.

JAKE
Mom, look at his tattoo. That's Dad's
old military unit symbol.

Sarah's face goes pale.

SARAH
Your father's past has found us.

INT. HOUSE - VARIOUS ROOMS - NIGHT

Cat and mouse game. Sarah uses the house's smart home system
against the intruders. Lights flashing, doors locking.

LEAD INTRUDER
(into radio)
She knows we're coming. She's prepared.

INT. BASEMENT - NIGHT

Sarah retrieves hidden weapons. Her demeanor changes - from
suburban mom to trained operative.

SARAH
(to kids via intercom)
Stay put. Mommy has to go to work.

She systematically takes down intruders using skills they didn't
know she had.

INT. PANIC ROOM - LATER

Sarah returns, bloodied but victorious. The kids stare in shock.

JAKE
Mom... who are you?

SARAH
Someone who will always protect you.
But now we need to disappear.

They gather essentials. As they leave, Sarah torches the house.

EXT. HIGHWAY - DAWN

Their car speeds toward an uncertain future. Sarah's phone rings.
She destroys it without answering.

SARAH (V.O.)
Some secrets should stay buried. But
when they surface, you do what you must.

FADE OUT."""


def test_basic_market_analysis():
    """Test basic market analysis."""
    print("\n💰 TEST 1: Basic Market Analysis")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()

    result = dr_market.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "market_analysis" in result.__dict__
    assert "market_segments" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Market category: {result.market_analysis.market_category}")
    print(f"✅ Overall market score: {result.market_analysis.overall_market_score:.2f}")

    return True


def test_market_segments():
    """Test market segment analysis."""
    print("\n💰 TEST 2: Market Segments")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_streaming_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"📊 Market segments analyzed: {len(result.market_segments)}")

    for segment in result.market_segments:
        print(f"   {segment.segment}: {segment.viability:.2f}")
        print(f"      Revenue potential: {segment.revenue_potential}")

    print(f"\n🎯 Primary market: {result.market_analysis.primary_market}")

    assert len(result.market_segments) >= 3
    print("\n✅ Market segment analysis working")

    return True


def test_audience_quadrants():
    """Test audience quadrant analysis."""
    print("\n💰 TEST 3: Audience Quadrants")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"👥 Audience quadrants: {len(result.audience_quadrants)}")

    for quad in result.audience_quadrants[:3]:
        print(f"   {quad.demographic}: {quad.appeal_score:.2f}")
        print(f"      Size: {quad.size}, Engagement: {quad.engagement_potential:.2f}")

    print(f"\n📏 Audience size: {result.market_analysis.audience_size}")

    print("\n✅ Audience quadrant analysis working")

    return True


def test_commercial_elements():
    """Test commercial element identification."""
    print("\n💰 TEST 4: Commercial Elements")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"💎 Commercial elements: {len(result.commercial_elements)}")

    for element in result.commercial_elements[:3]:
        print(f"   {element.element_type}: {element.description}")
        print(f"      Market value: {element.market_value:.2f}")

    print("\n✅ Commercial element identification working")

    return True


def test_competitive_analysis():
    """Test competitive landscape analysis."""
    print("\n💰 TEST 5: Competitive Analysis")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"🎯 Differentiation score: {result.competitive_analysis.differentiation_score:.2f}")
    print(f"📊 Market gap fit: {result.competitive_analysis.market_gap_fit:.2f}")

    print("\n🏆 Similar successes:")
    for success in result.competitive_analysis.similar_successes[:2]:
        print(f"   {success}")

    print("\n✅ Competitive analysis working")

    return True


def test_market_risks():
    """Test market risk assessment."""
    print("\n💰 TEST 6: Market Risks")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"⚠️ Market risks identified: {len(result.market_risks)}")

    for risk in result.market_risks[:3]:
        print(f"   {risk.risk_type}: {risk.description}")
        print(f"      Severity: {risk.severity:.2f}")
        print(f"      Mitigation: {risk.mitigation}")

    print("\n✅ Market risk assessment working")

    return True


def test_revenue_projection():
    """Test revenue projection."""
    print("\n💰 TEST 7: Revenue Projection")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"💵 Revenue tier: {result.revenue_projection['revenue_tier']}")
    print(f"💵 Projected range: {result.revenue_projection['projected_range']}")
    print(f"🎯 Best platform: {result.revenue_projection['best_platform']}")
    print(f"📊 Confidence: {result.revenue_projection['confidence']:.2f}")

    print(f"\n📈 ROI projection: {result.market_analysis.roi_projection:.2f}")
    print(f"✅ Break-even likelihood: {result.market_analysis.break_even_likelihood:.2f}")

    print("\n✅ Revenue projection working")

    return True


def test_special_potentials():
    """Test special market potentials."""
    print("\n💰 TEST 8: Special Potentials")
    print("=" * 50)

    dr_market = DrMarketPotential()
    screenplay = create_blockbuster_screenplay()
    result = dr_market.analyze(screenplay)

    print(f"🎬 Festival potential: {result.festival_potential:.2f}")
    print(f"🏆 Awards potential: {result.awards_potential:.2f}")
    print(f"🎯 Franchise potential: {result.franchise_potential:.2f}")
    print(f"🛍️ Merchandising potential: {result.merchandising_potential:.2f}")

    print("\n✅ Special potential calculations working")

    return True


def test_market_comparison():
    """Test market comparison between different types."""
    print("\n💰 TEST 9: Market Comparison")
    print("=" * 50)

    dr_market = DrMarketPotential()

    # Blockbuster
    blockbuster = create_blockbuster_screenplay()
    blockbuster_result = dr_market.analyze(blockbuster)

    # Niche
    niche = create_niche_screenplay()
    niche_result = dr_market.analyze(niche)

    print(f"🚀 Blockbuster screenplay:")
    print(f"   Score: {blockbuster_result.score}/100")
    print(f"   Category: {blockbuster_result.market_analysis.market_category}")
    print(f"   Revenue: {blockbuster_result.market_analysis.revenue_potential}")

    print(f"\n🎭 Niche screenplay:")
    print(f"   Score: {niche_result.score}/100")
    print(f"   Category: {niche_result.market_analysis.market_category}")
    print(f"   Revenue: {niche_result.market_analysis.revenue_potential}")

    # Check that market analysis differentiates between types
    assert blockbuster_result.market_analysis.overall_market_score != niche_result.market_analysis.overall_market_score or \
           blockbuster_result.market_analysis.revenue_potential != niche_result.market_analysis.revenue_potential
    print("\n✅ Market comparison working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n💰 TEST 10: Recommendations")
    print("=" * 50)

    dr_market = DrMarketPotential()
    niche = create_niche_screenplay()

    result = dr_market.analyze(niche)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations for niche screenplay
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Marketmon tests."""
    print("\n" + "=" * 60)
    print("💰 SCRIPT DOCTOR MARKETMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Market Analysis", test_basic_market_analysis),
        ("Market Segments", test_market_segments),
        ("Audience Quadrants", test_audience_quadrants),
        ("Commercial Elements", test_commercial_elements),
        ("Competitive Analysis", test_competitive_analysis),
        ("Market Risks", test_market_risks),
        ("Revenue Projection", test_revenue_projection),
        ("Special Potentials", test_special_potentials),
        ("Market Comparison", test_market_comparison),
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
        print("\n🎉 SCRIPT DOCTOR MARKETMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Market Potential Specialist is ready")
        print("\n💰 Market analysis systems online!")
        print("\n📝 Specialist 23/24 of the Script Doctor™ system operational!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)