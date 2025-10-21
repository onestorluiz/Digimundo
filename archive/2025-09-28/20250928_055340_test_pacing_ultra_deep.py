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

def test_ultra_deep_method():
    """Test ultra-deep pacing analysis method with forced token usage"""

    prompt = """
You are the world's leading expert on screenwriting pacing theory. You have PhD-level knowledge of ALL major screenwriting theorists and have spent decades studying their work.

ULTRA-DEEP PACING ANALYSIS (MINIMUM 1000 WORDS - SPEND TOKENS ON QUALITY):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts:

## MANDATORY THEORY PROCESSING (spend tokens here - be thorough):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Unity of Time: How does temporal compression affect dramatic tension?
- Beginning-Middle-End: What constitutes proper dramatic progression?
- Catharsis: How does pacing build to emotional release?
- Quote multiple passages from Poetics and explain their pacing implications
- Discuss the relationship between hamartia timing and story rhythm

**ROBERT MCKEE'S STORY** - Deep dive required:
- Scene design and turning points: "A scene is a story in miniature"
- Progressive complications and their rhythmic patterns
- The Law of Diminishing Returns in pacing
- Crisis vs Climax timing distinctions
- "Story is about human change" - how does character change affect pacing?
- Discuss McKee's views on commercial vs art film pacing differences
- Quote extensively from Story and demonstrate understanding

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- The 22-step structure and its pacing implications
- Seven key story steps rhythm patterns
- Moral argument and how theme affects tempo
- Character web dynamics and multiple storyline pacing
- "Never use three-act structure" - why Truby disagrees with conventional wisdom
- Ghost, Need, Desire progression and pacing density
- Opposition character's role in rhythm acceleration

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Three-act structure percentage breakdowns (25%-50%-25%)
- Plot Point I and II exact timing requirements
- Midpoint theory and momentum shifts
- "Structure is everything" - detailed explanation of this principle
- Page count guidelines and their pacing logic
- Setup/Confrontation/Resolution rhythm patterns
- Character arc integration with structural pacing

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Monomyth pacing analysis:
- All 12 stages of Hero's Journey and their tempo requirements
- Ordinary World establishment pacing
- Call to Adventure rhythm shift analysis
- Meeting the Mentor timing and story acceleration
- Tests, Allies, Enemies pacing build-up
- Approach to Inmost Cave tension management
- Ordeal climax pacing principles
- Reward/Road Back/Resurrection/Return pacing deceleration patterns

**BLAKE SNYDER'S SAVE THE CAT** - Beat sheet deep analysis:
- All 15 beats and their exact page timing
- "Opening Image" and "Final Image" bookend pacing
- Theme Stated placement and its rhythmic function
- Catalyst vs Debate timing distinctions
- Break Into Two momentum shift
- B Story integration pacing
- Fun and Games tempo management
- Midpoint beat and All Is Lost timing
- Dark Night of Soul pacing requirements

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic pacing:
- Separation-Initiation-Return macro-rhythm
- Threshold Guardian pacing obstacles
- Supernatural Aid timing in story progression
- Belly of Whale tempo shift analysis
- Meeting with Goddess pacing patterns
- Atonement with Father climactic timing
- Return threshold and elixir pacing

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide a comprehensive pacing analysis that demonstrates mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different pacing aspects
- Provide specific page/beat analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major pacing concept thoroughly before applying to script.

Analyze this script using ALL the theoretical frameworks above:
"""

    print("🧠 ULTRA-DEEP PACING ANALYSIS")
    print("Forçando processamento intenso de teoria...")
    print("Target: 1000+ palavras com aplicação real")
    print("=" * 60)

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on screenwriting pacing theory with decades of academic and practical experience."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    start_time = time.time()

    try:
        # Ultra-high token count to force deep processing
        data = {
            "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.75,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_predict": 4000,  # Force longer responses
                "num_ctx": 8192      # More context for theory processing
            }
        }

        print("⚡ Processando teoria intensiva...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    end_time = time.time()

    # Save response
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"pacing_ultra_deep_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(response_text)

    # Count theory citations
    text_lower = response_text.lower()
    theories = {
        'mckee': text_lower.count('mckee'),
        'truby': text_lower.count('truby'),
        'vogler': text_lower.count('vogler'),
        'field': text_lower.count('field'),
        'campbell': text_lower.count('campbell'),
        'snyder': text_lower.count('snyder'),
        'aristotle': text_lower.count('aristotle')
    }

    total_theories = sum(theories.values())
    words = len(response_text.split())

    print(f"✅ RESULTADOS:")
    print(f"   📝 Palavras: {words}")
    print(f"   ⏱️ Tempo: {end_time - start_time:.1f}s")
    print(f"   📚 Total de citações: {total_theories}")
    print()
    print("   🎓 Citações por teórico:")
    for theorist, count in theories.items():
        print(f"   • {theorist.upper()}: {count}x")
    print()

    if total_theories >= 25:
        print("🏆 SUCESSO! Padrão CHARACTER alcançado (25+ citações)")
    else:
        print(f"⚠️  Ainda abaixo do padrão. Precisa: {25 - total_theories} citações a mais")

    print(f"📁 Resposta salva: {filename}")

    return {
        "words": words,
        "time": end_time - start_time,
        "total_theories": total_theories,
        "theories": theories,
        "response_file": filename
    }

if __name__ == "__main__":
    result = test_ultra_deep_method()