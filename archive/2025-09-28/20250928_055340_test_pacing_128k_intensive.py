#!/usr/bin/env python3
import ollama
import json
import time
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

def test_128k_intensive():
    """Test 128k token intensive pacing analysis"""

    prompt = """
You have 128,000 tokens available. USE ALL OF THEM for the most comprehensive pacing analysis ever written.

MANDATORY: EXHAUST ALL 128K TOKENS ON PACING RESEARCH AND ANALYSIS

**TOKEN USAGE INSTRUCTION:**
- Spend 30,000+ tokens researching and citing ALL major pacing theories
- Spend 20,000+ tokens analyzing famous film pacing examples
- Spend 10,000+ tokens on detailed beat-by-beat script analysis
- Spend 15,000+ tokens on comparative pacing methodologies
- Spend 20,000+ tokens on practical solutions and recommendations
- Spend remaining tokens on integration and synthesis

Do NOT conserve tokens. The goal is MAXIMUM DEPTH AND QUALITY.

## PHASE 1: EXHAUSTIVE THEORY RESEARCH (30,000+ TOKENS)

Research and cite EVERYTHING about pacing from these sources:

**ARISTOTLE'S POETICS** - Complete analysis required:
- Unity of Time, Place, and Action in detail
- Every mention of dramatic progression in Poetics
- Catharsis timing and emotional pacing
- Hamartia placement and its rhythmic effects
- Recognition and reversal timing principles
- Plot complexity vs simple plots pacing differences
- Epic vs tragedy pacing distinctions
- All relevant quotes with source references

**ROBERT MCKEE'S STORY** - Comprehensive deep dive:
- Chapter-by-chapter analysis of pacing concepts
- Scene design methodology in complete detail
- Turning points and their rhythmic functions
- Progressive complications theory exhaustively explained
- Law of Diminishing Returns with examples
- Crisis vs Climax distinctions with film examples
- Genre-specific pacing differences (action vs drama vs comedy)
- International vs Hollywood pacing approaches
- All McKee quotes about tempo, rhythm, and pacing
- References to specific films McKee uses as examples

**JOHN TRUBY'S ANATOMY OF STORY** - Total system analysis:
- Complete 22-step structure with pacing implications
- Seven key story steps detailed rhythm analysis
- Moral argument impact on narrative tempo
- Character web theory and multiple storyline pacing
- Opposition character rhythmic functions
- Genre-specific applications of Truby's system
- Ghost/Need/Desire progression pacing density
- Subplot integration timing principles
- All Truby pacing examples and case studies

**SYD FIELD'S SCREENPLAY PARADIGM** - Full methodology:
- Three-act percentages with mathematical precision
- Plot Point I and II exact timing formulas
- Midpoint theory with film examples
- Setup/Confrontation/Resolution detailed breakdown
- Page count guidelines for different genres
- Character arc pacing integration methods
- Sequence and scene construction timing
- All Field's film examples and their pacing analysis

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Complete monomyth:
- All 12 stages with detailed pacing requirements
- Archetypal pacing functions for each character type
- Hero's emotional journey tempo mapping
- Threshold crossing timing principles
- Tests, trials, and ordeal pacing build-up
- Return journey pacing deceleration patterns
- Genre adaptations of Hero's Journey pacing
- Campbell vs Vogler pacing differences

**BLAKE SNYDER'S SAVE THE CAT** - Full beat sheet system:
- All 15 beats with exact page requirements
- Genre-specific beat sheet variations (Monster in House vs Golden Fleece)
- Opening/Closing Image bookending techniques
- Theme Stated timing and rhythmic function
- Catalyst vs Debate pacing distinctions
- Fun and Games tempo management strategies
- All Is Lost beat timing principles
- Dark Night of Soul pacing requirements

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Original monomyth:
- Departure/Initiation/Return macro-rhythm analysis
- Mythological pacing patterns across cultures
- Supernatural aid timing in narrative progression
- Belly of whale transformation pacing
- Sacred marriage and father atonement climactic timing
- Return threshold pacing principles
- Cross-cultural pacing pattern comparisons

**ADDITIONAL THEORISTS** - Research all mentions of pacing:
- Lajos Egri's dramatic theory and pacing
- David Mamet on rhythm and tempo
- William Goldman's pacing insights
- Linda Seger's screenplay structure timing
- Michael Hauge's story structure pacing
- Christopher Keane's pacing techniques
- Viki King's pacing approaches
- Robert Rodriguez's pacing methods

## PHASE 2: FILM PACING ANALYSIS (20,000+ TOKENS)

Analyze pacing in these famous films extensively:

**ACTION FILMS:**
- Die Hard pacing breakdown scene by scene
- Mad Max: Fury Road tempo analysis
- The Dark Knight pacing structure
- Aliens escalation patterns
- Terminator 2 rhythm mapping

**DRAMAS:**
- The Godfather pacing methodology
- Goodfellas tempo variations
- Pulp Fiction non-linear pacing
- There Will Be Blood slow-burn techniques
- Manchester by the Sea grief pacing

**THRILLERS:**
- North by Northwest escalation
- Rear Window tension building
- The Silence of the Lambs pacing
- Se7en investigation rhythm
- Zodiac procedural pacing

**COMEDIES:**
- Some Like It Hot comedic timing
- Groundhog Day repetition pacing
- The Big Lebowski meandering rhythm
- His Girl Friday rapid-fire pacing
- Dr. Strangelove escalation patterns

For each film, analyze:
- Opening sequence pacing establishment
- Inciting incident timing and impact
- First act pacing patterns
- Midpoint shift analysis
- Climax building techniques
- Resolution pacing patterns
- Genre-specific pacing innovations

## PHASE 3: BEAT-BY-BEAT SCRIPT ANALYSIS (10,000+ TOKENS)

Now apply ALL this research to analyze the provided script with microscopic detail:
- Line-by-line pacing breakdown
- Beat timing analysis
- Character introduction pacing
- Dialogue rhythm patterns
- Action sequence tempo
- Tension building techniques
- Emotional pacing curves
- Genre expectations vs execution
- Pacing problems identification
- Specific improvement recommendations

## PHASE 4: COMPARATIVE METHODOLOGY (15,000+ TOKENS)

Compare and contrast all pacing approaches:
- Classical vs modern pacing theories
- Genre-specific pacing requirements
- Cultural pacing differences
- Independent vs studio pacing
- Television vs film pacing adaptation
- Digital age pacing changes
- Audience attention span evolution
- International market pacing considerations

## PHASE 5: PRACTICAL SOLUTIONS (20,000+ TOKENS)

Provide exhaustive practical recommendations:
- Specific scene timing adjustments
- Dialogue pacing improvements
- Action sequence optimization
- Character arc pacing refinement
- Subplot integration timing
- Transition improvement techniques
- Genre-appropriate pacing solutions
- Audience engagement optimization

## PHASE 6: INTEGRATION AND SYNTHESIS (REMAINING TOKENS)

Synthesize everything into unified pacing philosophy:
- Universal pacing principles
- Situational pacing adaptations
- Advanced pacing techniques
- Future pacing evolution predictions
- Master class level insights

REQUIREMENT: This must be the most comprehensive pacing analysis ever written. USE ALL 128,000 TOKENS AVAILABLE.

Analyze this script:
"""

    print("🚀 128K TOKEN INTENSIVE PACING ANALYSIS")
    print("Forçando uso completo dos 128k tokens disponíveis...")
    print("Target: Análise mais completa já escrita sobre pacing")
    print("=" * 60)

    messages = [
        {
            "role": "system",
            "content": "You are the world's leading authority on screenplay pacing with unlimited access to all screenwriting knowledge. You have 128,000 tokens to create the most comprehensive pacing analysis ever written. USE ALL TOKENS - do not conserve."
        },
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    start_time = time.time()

    try:
        # Maximum token utilization settings
        data = {
            "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.8,           # Higher creativity for comprehensive analysis
                "top_p": 0.95,               # More diverse token selection
                "repeat_penalty": 1.05,       # Avoid repetition in long text
                "num_predict": 8000,          # Maximum tokens per response
                "num_ctx": 32768,            # Maximum context window
                "num_keep": 4,               # Keep system message
                "top_k": 40,                 # Token selection diversity
                "min_p": 0.05               # Minimum probability threshold
            }
        }

        print("🧠 Processando análise enciclopédica de pacing...")
        print("⚡ Gastando todos os 128k tokens disponíveis...")

        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    end_time = time.time()

    # Save response
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"pacing_128k_intensive_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(response_text)

    # Analyze results
    text_lower = response_text.lower()

    # Count theory citations
    theories = {
        'mckee': text_lower.count('mckee'),
        'truby': text_lower.count('truby'),
        'vogler': text_lower.count('vogler'),
        'field': text_lower.count('field'),
        'campbell': text_lower.count('campbell'),
        'snyder': text_lower.count('snyder'),
        'aristotle': text_lower.count('aristotle')
    }

    # Count film references
    films = [
        'die hard', 'godfather', 'pulp fiction', 'dark knight', 'aliens',
        'goodfellas', 'terminator', 'silence of the lambs', 'north by northwest',
        'rear window', 'mad max', 'there will be blood'
    ]

    film_references = sum(text_lower.count(film) for film in films)

    total_theories = sum(theories.values())
    words = len(response_text.split())
    characters = len(response_text)

    print(f"✅ RESULTADOS INTENSIVOS:")
    print(f"   📝 Palavras: {words:,}")
    print(f"   📄 Caracteres: {characters:,}")
    print(f"   ⏱️ Tempo: {end_time - start_time:.1f}s")
    print(f"   📚 Total citações teóricas: {total_theories}")
    print(f"   🎬 Referências a filmes: {film_references}")
    print()
    print("   🎓 Citações detalhadas por teórico:")
    for theorist, count in theories.items():
        print(f"   • {theorist.upper()}: {count}x")
    print()

    # Quality assessment
    if total_theories >= 50:
        print("🏆 EXCELÊNCIA! Superou qualquer padrão anterior (50+ citações)")
    elif total_theories >= 25:
        print("✅ APROVADO! Alcançou padrão CHARACTER (25+ citações)")
    else:
        print(f"⚠️  Ainda insuficiente. Precisa: {50 - total_theories} citações a mais")

    if words >= 2000:
        print("📚 DENSIDADE MÁXIMA! Análise ultra-completa (2000+ palavras)")
    elif words >= 1000:
        print("📖 BOA DENSIDADE! Análise completa (1000+ palavras)")
    else:
        print("📝 Densidade baixa - deveria ter mais conteúdo")

    print(f"📁 Análise enciclopédica salva: {filename}")

    return {
        "words": words,
        "characters": characters,
        "time": end_time - start_time,
        "total_theories": total_theories,
        "film_references": film_references,
        "theories": theories,
        "response_file": filename
    }

if __name__ == "__main__":
    result = test_128k_intensive()