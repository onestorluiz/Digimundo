#!/usr/bin/env python3
"""
Test all 5 versions of the Contrast & Comparison Specialist
Compare their effectiveness and unique insights
"""

import json
import time
from datetime import datetime
import ollama

# Sample screenplay excerpt for testing
SAMPLE_SCREENPLAY = """
FADE IN:

INT. ABANDONED CHURCH - NIGHT

Rain hammers against stained glass. MARCUS (40s, weathered face,
priest's collar hanging loose) kneels before a broken altar.

MARCUS
(whispered prayer)
Forgive me, Father...

The door EXPLODES open. VIKTOR (50s, expensive suit now soaked)
enters with two GUNMEN. The man Marcus once called brother.

VIKTOR
Still talking to your imaginary friend?

Marcus rises slowly, turns. Their eyes meet - twenty years of
betrayal between them.

MARCUS
He listens better than you ever did.

VIKTOR
(laughs)
The saint and the sinner. Look where
your righteousness got you.

Thunder CRACKS. In the lightning flash, we see Marcus's hand
near a concealed weapon.

MARCUS
And where did your choices lead, brother?
To this? Hunting me in God's house?

VIKTOR
God left this place long ago. Just
like he left you.

A moment of silence. Just rain and breathing.

MARCUS
Maybe. But I'm still here.

VIKTOR
Not for long.

The gunmen raise their weapons. Marcus doesn't flinch.

MARCUS
You came alone. Your men are already dead.

Viktor's smile falters. Behind him, his gunmen suddenly drop.
We see MARIA (30s, nun's habit over tactical gear) in the shadows.

MARIA
(to Marcus)
Your faith might be broken, Father.
But your family isn't.
"""

# Simulated responses from the 23 specialists (abbreviated)
SPECIALISTS_RESPONSES = {
    "character_specialist": {
        "analysis": "Marcus represents the archetypal fallen priest - faith challenged but not destroyed. Viktor embodies corruption masked as pragmatism.",
        "key_elements": ["moral ambiguity", "brotherhood betrayal", "faith vs nihilism"]
    },
    "dialogue_specialist": {
        "analysis": "Dialogue operates on multiple levels - surface confrontation masking deeper spiritual warfare.",
        "key_elements": ["subtext heavy", "biblical echoes", "power through restraint"]
    },
    "structure_specialist": {
        "analysis": "Classical three-act micro-structure within single scene. Setup (prayer), confrontation (brothers meet), reversal (Maria's intervention).",
        "key_elements": ["rising tension", "false climax", "twist revelation"]
    },
    "theme_specialist": {
        "analysis": "Central theme: redemption through suffering. Secondary: family bonds transcending blood.",
        "key_elements": ["sacred vs profane", "loyalty redefined", "faith tested"]
    },
    "conflict_specialist": {
        "analysis": "Multi-layered conflict - physical (guns), emotional (betrayal), spiritual (faith), philosophical (meaning).",
        "key_elements": ["external threat", "internal struggle", "ideological opposition"]
    },
    "pacing_specialist": {
        "analysis": "Masterful rhythm - slow burn opening, accelerating confrontation, sudden reversal.",
        "key_elements": ["tension escalation", "breathing room", "explosive climax"]
    }
}

def test_contrast_version(version: int, screenplay: str, specialists: dict) -> dict:
    """Test a single contrast specialist version"""

    model_name = f"scripturemon-contrast-v{version}"

    prompt = f"""
    You are analyzing this screenplay excerpt:

    {screenplay}

    Here are the analyses from 23 specialists:
    {json.dumps(specialists, indent=2)}

    Provide your contrast and comparison analysis based on your specific approach.
    Focus on the oppositions, contrasts, and comparative elements that deepen understanding.
    """

    print(f"\n{'='*60}")
    print(f"Testing {model_name}...")
    print(f"{'='*60}")

    try:
        start_time = time.time()

        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 1000
            }
        )

        analysis_time = time.time() - start_time

        result = {
            'version': version,
            'model': model_name,
            'analysis': response['response'],
            'time': analysis_time,
            'tokens': response.get('total_duration', 0) / 1e9  # Convert to seconds
        }

        # Print summary
        print(f"✓ Analysis completed in {analysis_time:.2f}s")
        print(f"\nKey insights from v{version}:")
        print("-" * 40)
        print(response['response'][:500] + "...")

        return result

    except Exception as e:
        print(f"✗ Error testing {model_name}: {e}")
        return {
            'version': version,
            'model': model_name,
            'error': str(e)
        }

def compare_all_versions():
    """Test and compare all 5 contrast specialist versions"""

    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     CONTRAST & COMPARISON SPECIALIST - 5 VERSION TEST     ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    print("Testing screenplay: Church confrontation scene")
    print("Themes: Faith vs nihilism, brotherhood, betrayal, redemption")

    results = []

    # Test each version
    for version in range(1, 6):
        result = test_contrast_version(version, SAMPLE_SCREENPLAY, SPECIALISTS_RESPONSES)
        results.append(result)
        time.sleep(2)  # Brief pause between tests

    # Compare results
    print("\n" + "="*60)
    print("COMPARISON OF ALL 5 VERSIONS")
    print("="*60)

    version_descriptions = {
        1: "Binary Oppositions",
        2: "Classic Cinema References",
        3: "Hegelian Dialectics",
        4: "Cultural & Contextual",
        5: "Micro-Contrasts (Scene-Level)"
    }

    for result in results:
        if 'error' not in result:
            print(f"\n📊 Version {result['version']}: {version_descriptions[result['version']]}")
            print(f"   Time: {result['time']:.2f}s")
            print(f"   Focus: Analyzing through {version_descriptions[result['version']].lower()}")

            # Extract unique insight (first substantial point)
            analysis = result['analysis']
            if analysis:
                lines = analysis.split('\n')
                for line in lines:
                    if len(line.strip()) > 50:  # Find first substantial line
                        print(f"   Unique insight: {line.strip()[:150]}...")
                        break

    # Determine best version based on depth
    print("\n" + "="*60)
    print("RECOMMENDATION")
    print("="*60)

    successful_results = [r for r in results if 'error' not in r]
    if successful_results:
        # Simple heuristic: longest analysis often means most thorough
        best = max(successful_results, key=lambda x: len(x.get('analysis', '')))
        print(f"✨ Most comprehensive: Version {best['version']} ({version_descriptions[best['version']]})")
        print(f"   This version provided the deepest analysis with {len(best['analysis'])} characters")

        # Also note fastest
        fastest = min(successful_results, key=lambda x: x['time'])
        print(f"⚡ Fastest response: Version {fastest['version']} ({fastest['time']:.2f}s)")

    # Save full results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"contrast_comparison_results_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'screenplay_sample': SAMPLE_SCREENPLAY,
            'specialists_input': SPECIALISTS_RESPONSES,
            'results': results,
            'descriptions': version_descriptions
        }, f, indent=2)

    print(f"\n💾 Full results saved to: {output_file}")
    print("\nDIGIMUNDO PRESENTE 🔥")

if __name__ == "__main__":
    compare_all_versions()