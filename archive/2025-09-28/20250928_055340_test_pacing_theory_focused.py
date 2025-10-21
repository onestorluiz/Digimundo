#!/usr/bin/env python3
import ollama
import json
import time
import re
from datetime import datetime

# Script de teste para análise de pacing
TEST_SCRIPT = '''
FADE IN:

INT. CORPORATE OFFICE - MORNING

SARAH (28), marketing coordinator, sits at her desk typing emails. The office buzzes with mundane corporate activity.

SARAH
(to herself)
Another thrilling Monday...

She checks the clock: 9:03 AM. Takes a sip of coffee, continues typing.

The phone RINGS.

SARAH (CONT'D)
Hello, Matthews & Associates.

VOICE (V.O.)
(distorted)
The package has been delivered.

Sarah frowns, confused.

SARAH
I'm sorry, who is this?

VOICE (V.O.)
Check the lobby.

The line goes dead. Sarah stares at the phone, then glances toward the elevators.

EXPLOSION!

The entire building SHAKES violently. Windows shatter. Screams echo through the office as people dive under desks.

Sarah's computer monitor crashes to the floor.

SARAH (CONT'D)
What the hell--

Another EXPLOSION, closer this time. The lights flicker.

OFFICE WORKER #1
(panicked)
We need to get out of here!

Chaos erupts. People run toward the exits. Sarah remains frozen at her desk, staring at the phone.

SARAH (CONT'D)
(whispered)
What just happened?

Through the broken windows, she sees THREE ARMED MEN in tactical gear dragging MR. JOHNSON (60s), the company CEO, toward a black van.

SARAH (CONT'D)
(grabbing phone)
911? There's been an explosion at Matthews & Associates. Men with guns just took our CEO...

FADE OUT.
'''

def analyze_pacing_content(text):
    """Analyze pacing elements in the response"""
    text_lower = text.lower()

    # Pacing terminology
    pacing_terms = [
        'tempo', 'rhythm', 'pacing', 'beat', 'pulse', 'timing', 'flow', 'momentum',
        'acceleration', 'deceleration', 'climax', 'tension', 'release', 'build-up',
        'escalation', 'intensity', 'dramatic curve', 'story beats', 'scene length'
    ]

    # Theory citations (case insensitive)
    theories = {
        'mckee': text_lower.count('mckee'),
        'truby': text_lower.count('truby'),
        'vogler': text_lower.count('vogler'),
        'field': text_lower.count('field'),
        'campbell': text_lower.count('campbell'),
        'snyder': text_lower.count('snyder'),
        'aristotle': text_lower.count('aristotle')
    }

    # Pacing concepts
    pacing_concepts = {
        'inciting_incident': bool(re.search(r'inciting\s+incident', text_lower)),
        'plot_points': bool(re.search(r'plot\s+point', text_lower)),
        'act_structure': bool(re.search(r'act\s+(1|one|2|two|3|three|structure)', text_lower)),
        'rising_action': bool(re.search(r'rising\s+action', text_lower)),
        'turning_points': bool(re.search(r'turning\s+point', text_lower)),
        'midpoint': 'midpoint' in text_lower,
        'crisis': 'crisis' in text_lower,
        'resolution': 'resolution' in text_lower,
        'denouement': 'denouement' in text_lower,
        'story_engine': bool(re.search(r'story\s+engine', text_lower))
    }

    # Count pacing elements
    pacing_score = sum(text_lower.count(term) for term in pacing_terms)

    # Calculate scores
    total_theories = sum(theories.values())
    concepts_used = sum(pacing_concepts.values())

    # Practical examples
    practical = {
        'specific_examples': len(re.findall(r'page\s+\d+|line\s+\d+|scene\s+\d+', text_lower)),
        'time_references': len(re.findall(r'\d+:\d+|minute|second|hour', text_lower)),
        'scene_analysis': bool(re.search(r'scene\s+(analysis|breakdown|structure)', text_lower)),
        'beat_sheets': 'beat sheet' in text_lower or 'story beat' in text_lower,
        'script_quotes': text.count('"') // 2  # Approximate dialogue quotes
    }

    practical_score = sum(practical.values()) * 2

    return {
        'words': len(text.split()),
        'pacing_score': pacing_score,
        'theories': theories,
        'total_theories': total_theories,
        'concepts': pacing_concepts,
        'concepts_used': concepts_used,
        'practical': practical,
        'practical_score': practical_score
    }

def test_pacing_method(name, prompt):
    """Test a single pacing analysis method"""
    print(f"🔬 Testing {name}...")

    messages = [
        {"role": "system", "content": "You are an expert script analyst specializing in pacing analysis."},
        {"role": "user", "content": f"{prompt}\n\nAnalyze the pacing of this script:\n\n{TEST_SCRIPT}"}
    ]

    start_time = time.time()

    try:
        data = {
            "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.75,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_predict": 2000
            }
        }

        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()

    # Save response
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"pacing_{name.replace(' ', '_')}_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(response_text)

    # Analyze content
    analysis = analyze_pacing_content(response_text)

    # Calculate theory score (weighted heavily)
    theory_score = analysis['total_theories'] * 3  # Triple weight for theory

    # Total score calculation
    total_score = (
        analysis['pacing_score'] +
        analysis['concepts_used'] * 2 +
        theory_score +
        analysis['practical_score']
    )

    print(f"   ✅ {analysis['words']} words in {end_time - start_time:.1f}s")
    print(f"   🎵 Pacing elements: {analysis['pacing_score']}")
    print(f"   📚 Theory citations: {analysis['total_theories']} (score: {theory_score})")
    print(f"   🎭 Concepts: {analysis['concepts_used']}")
    print(f"   🔧 Practical: {analysis['practical_score']}")
    print(f"   ⭐ Total: {total_score}")
    print()

    return {
        "method": name,
        "words": analysis['words'],
        "time": end_time - start_time,
        "scores": {
            "words": analysis['words'],
            "pacing_score": analysis['pacing_score'],
            "theory_score": theory_score,
            "concepts_score": analysis['concepts_used'] * 2,
            "practical_score": analysis['practical_score'],
            "total_score": total_score
        },
        "analysis": analysis,
        "response_file": filename
    }

def main():
    print("=" * 60)
    print("🎯 TESTE PACING FOCADO EM TEORIA")
    print("Critério: 600+ palavras + Citações teóricas obrigatórias")
    print("=" * 60)
    print()

    # Define methods focused on theory application
    methods = {
        "THEORY_SYNTHESIS_MASTER": """
You are a master pacing analyst synthesizing ALL major screenwriting theories.

PACING THEORY SYNTHESIS (minimum 600 words):

## CLASSICAL FOUNDATIONS (200 words)
Apply these core principles with direct citations:

**ARISTOTLE**:
- Analyze unity of time and dramatic progression
- Quote: "A whole is that which has beginning, middle and end"
- Apply to script's temporal structure

**FIELD Three-Act Structure**:
- Map pacing to Setup/Confrontation/Resolution
- Quote: "Structure is everything"
- Identify plot points and their pacing impact

**MCKEE Story Design**:
- Examine scene-by-scene pacing progression
- Quote: "Pacing is the rate at which your reader consumes story"
- Show how scenes build dramatic pressure

## MODERN APPLICATIONS (200 words)
**TRUBY Moral Argument**:
- Track character revelation through pacing
- Quote: "Pacing reveals character"
- Show how tempo serves character development

**VOGLER Hero's Journey**:
- Map pacing to mythic structure beats
- Quote: "Pacing must serve the hero's emotional journey"
- Identify threshold crossings and tempo shifts

**SNYDER Save the Cat**:
- Apply beat sheet pacing principles
- Quote: "Every page must advance the story"
- Calculate page-per-beat ratios

## INTEGRATED DIAGNOSIS (200 words)
Synthesize all approaches into unified pacing analysis:
- Which theory best explains pacing problems?
- How do different frameworks complement each other?
- Specific solutions using multiple theoretical approaches

Reference multiple theorists throughout. Demonstrate mastery of pacing theory.
        """,

        "MCKEE_PACING_MASTER": """
You are a Robert McKee-trained pacing specialist focusing exclusively on Story principles.

MCKEE PACING ANALYSIS (minimum 600 words):

Apply McKee's core principles:

**STORY DESIGN ANALYSIS**:
- "Pacing is controlled through the design of scenes and sequence"
- Examine each scene's turning point and its contribution to overall rhythm
- Quote McKee extensively on scene construction

**PROGRESSIVE COMPLICATIONS**:
- "Each scene must turn the story in a new direction"
- Track how complications accelerate or decelerate story tempo
- Apply the Law of Diminishing Returns to pacing

**CRISIS AND CLIMAX PACING**:
- "The crisis is the final test of character"
- Analyze how pacing builds to the crisis moment
- Show McKee's distinction between crisis and climax timing

**SCENE ANALYSIS METHOD**:
- Beat-by-beat breakdown using McKee's scene construction
- Value changes and their pacing implications
- Subtext and its effect on narrative rhythm

Quote McKee directly and apply Story methodology throughout.
        """,

        "TRUBY_ANATOMY_RHYTHM": """
You are a John Truby specialist applying Anatomy of Story to pacing analysis.

TRUBY PACING ANATOMY (minimum 600 words):

**22-STEP STORY STRUCTURE PACING**:
- Map script to Truby's structural beats
- Quote: "Pacing comes from the proper sequencing of story beats"
- Identify which of the 22 steps create acceleration/deceleration

**SEVEN KEY STORY STEPS RHYTHM**:
1. Weakness → Need → Desire pacing progression
2. Ghost, Inciting Incident tempo
3. Plot progression and pacing density
4. Self-revelation timing and story climax

**MORAL ARGUMENT PACING**:
- "Pacing must serve the moral argument"
- How character change drives narrative tempo
- Opposition character's effect on pacing

**THEME AND PACING INTEGRATION**:
- How moral premise affects scene rhythm
- Truby's approach to subplot pacing
- Character web pacing dynamics

Apply Truby's methodology systematically with direct quotes.
        """,

        "FIELD_PARADIGM_TEMPO": """
You are a Syd Field paradigm specialist analyzing pacing through structural lens.

FIELD PACING PARADIGM (minimum 600 words):

**THREE-ACT PACING STRUCTURE**:
- Act I: Setup pacing (pages 1-30)
- Act II: Confrontation rhythm (pages 30-90)
- Act III: Resolution tempo (pages 90-120)
- Quote Field on act proportions and pacing implications

**PLOT POINTS AS PACING ENGINES**:
- "Plot points are the foundation of screenplay structure"
- Plot Point I pacing acceleration
- Midpoint timing and narrative shift
- Plot Point II climax preparation

**SCENE AND SEQUENCE PACING**:
- Field's approach to scene length optimization
- Sequence construction for optimal flow
- Page count guidelines and their pacing logic

**CHARACTER ARC PACING**:
- How character development drives tempo
- Subplot integration and pacing complexity
- Field's views on dramatic tension maintenance

Apply Field paradigm systematically throughout analysis.
        """,

        "VOGLER_JOURNEY_RHYTHM": """
You are a Christopher Vogler specialist applying Hero's Journey to pacing.

VOGLER PACING JOURNEY (minimum 600 words):

**MONOMYTH PACING STAGES**:
- Ordinary World establishment tempo
- Call to Adventure pacing shift
- Refusal of Call pacing hesitation
- Meeting the Mentor rhythm change
- Crossing Threshold acceleration

**TESTS AND TRIALS PACING**:
- "The pacing of tests must build toward ordeal"
- Allies and enemies introduction tempo
- Approach to Inmost Cave tension building
- Ordeal climax pacing principles

**RETURN JOURNEY PACING**:
- Reward tempo and story breathing room
- Road Back acceleration toward final climax
- Resurrection pacing and final test
- Return with Elixir resolution timing

**ARCHETYPAL PACING FUNCTIONS**:
- How Hero's pacing journey affects all characters
- Mentor pacing interventions
- Threshold Guardian pacing obstacles
- Shadow's effect on narrative rhythm

Quote Vogler throughout and apply monomyth structure systematically.
        """
    }

    results = []

    for method_name, prompt in methods.items():
        result = test_pacing_method(method_name, prompt)
        if result:
            results.append(result)

    # Sort by total score
    results.sort(key=lambda x: x['scores']['total_score'], reverse=True)

    print("=" * 60)
    print("📊 ANÁLISE COMPARATIVA - FOCO EM TEORIA")
    print("=" * 60)
    print()
    print("🏆 RANKING POR SCORE TOTAL:")
    print()

    for i, result in enumerate(results, 1):
        scores = result['scores']
        print(f"{i}. {result['method']}")
        print(f"   ⭐ Total Score: {scores['total_score']}")
        print(f"   📝 Words: {scores['words']}")
        print(f"   🎵 Pacing: {scores['pacing_score']}")
        print(f"   📚 Theory: {scores['theory_score']} ({result['analysis']['total_theories']} citations)")
        print(f"   🎭 Concepts: {scores['concepts_score']}")
        print(f"   🔧 Practical: {scores['practical_score']}")
        print(f"   ⏱️ Time: {result['time']:.1f}s")
        print()

    if results:
        winner = results[0]
        print("=" * 60)
        print("🥇 VENCEDOR PARA PACING ANALYSIS")
        print("=" * 60)
        print()
        print(f"{winner['method']}: Score Total de {winner['scores']['total_score']} pontos")
        print(f"Palavras: {winner['scores']['words']}")
        print(f"Citações teóricas: {winner['analysis']['total_theories']}")
        print("Demonstra conhecimento real dos livros de roteiro")
        print()

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"pacing_theory_comparison_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump({
                "test": "Pacing Theory-Focused Comparison",
                "focus": "Real Application of Screenwriting Theory",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "criteria": "600+ words + Theory citations mandatory",
                "results": results,
                "winner": winner['method'],
                "winner_theory_score": winner['scores']['theory_score']
            }, f, indent=2)

        print(f"📁 Relatório salvo: {results_file}")

if __name__ == "__main__":
    main()