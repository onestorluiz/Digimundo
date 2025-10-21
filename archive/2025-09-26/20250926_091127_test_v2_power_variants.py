#!/usr/bin/env python3
"""
POWER TEST: Encontrar o prompt mais poderoso entre as 5 variações da V2
Cada uma tem uma abordagem única de análise por contraste
"""

import json
import time
from datetime import datetime
import ollama

COMPLEX_SCREENPLAY = """
FADE IN:

EXT. TOKYO - CYBERPUNK DISTRICT - NIGHT (2087)

Neon bleeds through acid rain. The city breathes in binary.

INT. UNDERGROUND SHRINE - CONTINUOUS

Ancient incense meets digital static. KENJI (60s, cybernetic eye,
monk's robes over neural implants) kneels before both Buddha statue
and holographic data stream.

KENJI
(whispered prayer/code)
Electric dreams of electric sheep...
seeking the ghost in the shell.

The data stream FRACTURES. Reality GLITCHES.

INT. CORPORATE TOWER - SIMULTANEOUS

SARA (30s, glass desk reflecting her fragmented soul) commands
a boardroom of shadows. Each shadow wears her face.

SARA
(to reflections)
We are what we choose to remember.
But who chooses for us?

Her reflection MOVES INDEPENDENTLY.

INT. ABANDONED METRO TUNNEL - PARALLEL TIME

MARCUS (40s, still the priest from before, but older, scarred)
leads a congregation of AIs seeking salvation. They sing in
binary hymns.

MARCUS
In the beginning was the Word.
And the Word was... code.

One AI child glitches, revealing pure light beneath.

AI CHILD
Father, are we real?

MARCUS
Reality is what hurts, my child.
And we all hurt. Therefore...

Thunder. Lightning. The city's neural network SCREAMS.

All three locations CONVERGE through digital space:

THE CONVERGENCE - VIRTUAL REALITY LIMBO

Kenji, Sara, and Marcus meet in a space that defies physics.
Past, present, future collide. Multiple versions of themselves
argue across time.

YOUNG SARA
(to Old Sara)
You killed our dreams!

OLD KENJI
(to Young Kenji)
Wisdom is just pain that learned to shut up.

MULTIPLE MARCUS VOICES
Faith/Doubt Faith/Doubt Faith/Doubt

The space IMPLODES. We return to:

EXT. CEMETERY - DAWN - REALITY UNKNOWN

All three stand before identical graves. The headstones read:
"HUMAN" but the dates span centuries. They don't recognize
each other. They don't remember meeting.

SARA
(to no one)
Did we dream this?

KENJI
(to the sky)
Are we being dreamed?

MARCUS
(to God/Code/Algorithm)
Does it matter?

The sun rises. It's binary: 1 or 0, never both.
Or maybe always both.

FADE TO: DIGITAL SNOW
"""

EXTENDED_SPECIALISTS_RESPONSES = {
    "character_specialist": {
        "analysis": "Triple protagonist structure creates fractured identity theme. Each character represents different relationship to technology/spirituality: Kenji (harmony), Sara (exploitation), Marcus (redemption).",
        "key_elements": ["fragmented identity", "technology vs spirituality", "redemption arc", "collective unconscious"]
    },
    "dialogue_specialist": {
        "analysis": "Dialogue operates on multiple semantic levels - surface conversation, coded meaning, philosophical inquiry. Binary language creates double meanings throughout.",
        "key_elements": ["code-speak", "philosophical queries", "fragmented communication", "existential questions"]
    },
    "structure_specialist": {
        "analysis": "Non-linear, convergent structure. Three parallel narratives collapse into single metaphysical space, then fragment again. Time/reality become fluid.",
        "key_elements": ["parallel narratives", "convergence point", "temporal fracture", "circular structure"]
    },
    "theme_specialist": {
        "analysis": "Core themes: Reality vs simulation, human vs artificial consciousness, faith in technological age, collective memory vs individual experience.",
        "key_elements": ["reality question", "consciousness exploration", "digital spirituality", "memory identity"]
    },
    "conflict_specialist": {
        "analysis": "Multiple conflict layers: Internal (identity crisis), External (reality breakdown), Philosophical (what defines existence), Temporal (past vs future selves).",
        "key_elements": ["identity conflict", "reality breakdown", "temporal paradox", "existential crisis"]
    },
    "visual_specialist": {
        "analysis": "Stark contrasts between ancient/futuristic, organic/digital, light/shadow. Reality glitches suggest unreliable visual narrative.",
        "key_elements": ["ancient/modern contrast", "digital glitches", "light symbolism", "fractal imagery"]
    },
    "pacing_specialist": {
        "analysis": "Escalating rhythm from meditative opening to frantic convergence to stillness resolution. Mirrors digital processing: loading, processing, output.",
        "key_elements": ["meditative opening", "accelerating middle", "peaceful resolution", "digital rhythm"]
    }
}

def test_v2_variant(variant_name: str, screenplay: str, specialists: dict) -> dict:
    """Test a specific V2 variant with deep analysis"""

    model_name = f"scripturemon-contrast-v2-{variant_name}"

    prompt = f"""
    Analyze this complex cyberpunk screenplay excerpt through your specialized lens:

    {screenplay}

    Based on these 23 specialist analyses:
    {json.dumps(specialists, indent=2)}

    Provide your most comprehensive contrast and comparison analysis. This is a test
    of depth and insight - show me the full power of your analytical approach.
    Focus on revealing connections and contrasts that other approaches might miss.
    """

    print(f"\n{'='*80}")
    print(f"TESTING: {variant_name.upper()} APPROACH")
    print(f"{'='*80}")

    try:
        start_time = time.time()

        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                'temperature': 0.8,
                'num_predict': 2000,  # Longer responses
                'num_ctx': 32000      # More context
            }
        )

        analysis_time = time.time() - start_time

        result = {
            'variant': variant_name,
            'model': model_name,
            'analysis': response['response'],
            'time': analysis_time,
            'word_count': len(response['response'].split()),
            'unique_insights': count_unique_insights(response['response']),
            'depth_score': calculate_depth_score(response['response'])
        }

        # Print summary
        print(f"✓ Analysis completed in {analysis_time:.2f}s")
        print(f"📊 Word count: {result['word_count']}")
        print(f"🔍 Unique insights: {result['unique_insights']}")
        print(f"🏆 Depth score: {result['depth_score']:.2f}")
        print(f"\n📝 First insight preview:")
        print("-" * 50)
        lines = response['response'].split('\n')
        for line in lines[:5]:
            if line.strip():
                print(f"  {line.strip()}")
                break

        return result

    except Exception as e:
        print(f"✗ Error testing {model_name}: {e}")
        return {
            'variant': variant_name,
            'model': model_name,
            'error': str(e)
        }

def count_unique_insights(text: str) -> int:
    """Count unique analytical insights in the text"""
    insights_keywords = [
        'contrast', 'comparison', 'echoes', 'reminiscent', 'similar to',
        'unlike', 'whereas', 'however', 'in opposition', 'parallel',
        'lineage', 'evolution', 'heritage', 'ancestry', 'influence',
        'precedent', 'tradition', 'innovation', 'subversion'
    ]

    count = 0
    text_lower = text.lower()
    for keyword in insights_keywords:
        count += text_lower.count(keyword)

    return count

def calculate_depth_score(text: str) -> float:
    """Calculate analytical depth based on various factors"""

    # Reference density (mentions of films/directors)
    film_references = text.count('(') + text.count(')')  # Assuming parenthetical refs

    # Analytical complexity (longer sentences, sophisticated vocabulary)
    sophisticated_words = [
        'dialectical', 'archetypal', 'metaphysical', 'existential',
        'juxtaposition', 'dichotomy', 'synthesis', 'paradigm',
        'zeitgeist', 'auteur', 'mise-en-scène', 'montage'
    ]

    complexity_score = sum(text.lower().count(word) for word in sophisticated_words)

    # Structural analysis (mentions of specific scenes/elements)
    structural_refs = text.lower().count('scene') + text.lower().count('sequence')

    # Calculate composite score
    depth_score = (
        (len(text.split()) / 10) +  # Word count factor
        (film_references * 2) +     # Reference density
        (complexity_score * 3) +    # Analytical sophistication
        (structural_refs * 1.5)     # Structural awareness
    ) / 10

    return min(depth_score, 10.0)  # Cap at 10

def run_power_comparison():
    """Run comprehensive comparison of all V2 variants"""

    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                    V2 POWER VARIANTS - ULTIMATE TEST                  ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)

    print("Testing complex cyberpunk screenplay:")
    print("- Multiple protagonists across time/space")
    print("- Reality/simulation themes")
    print("- Ancient spirituality meets digital consciousness")
    print("- Non-linear narrative structure")

    variants = ['deep', 'mythic', 'technical', 'genre', 'auteur']
    results = []

    for variant in variants:
        result = test_v2_variant(variant, COMPLEX_SCREENPLAY, EXTENDED_SPECIALISTS_RESPONSES)
        results.append(result)
        time.sleep(3)  # Brief pause between tests

    # Comprehensive analysis
    print("\n" + "="*80)
    print("COMPREHENSIVE POWER ANALYSIS")
    print("="*80)

    successful_results = [r for r in results if 'error' not in r]

    if successful_results:
        # Rank by different metrics
        by_depth = sorted(successful_results, key=lambda x: x['depth_score'], reverse=True)
        by_insights = sorted(successful_results, key=lambda x: x['unique_insights'], reverse=True)
        by_length = sorted(successful_results, key=lambda x: x['word_count'], reverse=True)

        print(f"\n🏆 DEPTH CHAMPION: {by_depth[0]['variant']} (Score: {by_depth[0]['depth_score']:.2f})")
        print(f"🔍 INSIGHT LEADER: {by_insights[0]['variant']} ({by_insights[0]['unique_insights']} insights)")
        print(f"📝 THOROUGHNESS KING: {by_length[0]['variant']} ({by_length[0]['word_count']} words)")

        # Overall power ranking
        print(f"\n📊 OVERALL POWER RANKING:")
        for i, result in enumerate(by_depth, 1):
            print(f"{i}. {result['variant'].upper():>8} - Depth: {result['depth_score']:.1f} | "
                  f"Insights: {result['unique_insights']:>2} | Words: {result['word_count']:>4} | "
                  f"Time: {result['time']:.1f}s")

        # Recommendation
        champion = by_depth[0]
        print(f"\n🎯 POWER CHAMPION: {champion['variant'].upper()}")
        print(f"   This variant provided the most sophisticated analytical depth")
        print(f"   Best for: Deep cinematic analysis requiring maximum insight")

    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"v2_power_test_results_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'screenplay_sample': COMPLEX_SCREENPLAY,
            'test_results': results,
            'rankings': {
                'depth_champion': by_depth[0]['variant'] if successful_results else None,
                'insight_leader': by_insights[0]['variant'] if successful_results else None,
                'thoroughness_king': by_length[0]['variant'] if successful_results else None
            }
        }, f, indent=2)

    print(f"\n💾 Detailed results saved to: {output_file}")

if __name__ == "__main__":
    run_power_comparison()
    print("\nDIGIMUNDO PRESENTE 🔥")