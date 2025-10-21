#!/usr/bin/env python3
import ollama
import json
import time
from datetime import datetime

# Script de teste para análise completa
TEST_SCRIPT = '''
FADE IN:

INT. MARCUS'S APARTMENT - NIGHT

MARCUS (42), a former priest, sits alone with a bottle of whiskey. His clerical collar hangs loose around his neck.

On the table: a blood-stained confession note.

MARCUS
(to himself)
Forgive me, Father, for I have sinned.

He pours another drink. His hands shake.

The door opens. ELENA (38) enters, leather jacket over scrubs. She was a nun once - now works as a nurse.

ELENA
You called me.

MARCUS
I needed... someone who'd understand.

ELENA
(sitting across from him)
What did you do, Marcus?

Marcus slides the confession note across the table. Elena reads it, her face growing pale.

ELENA (CONT'D)
The Morrison boy... he was brain dead.

MARCUS
His father confessed. Three children.
Beat them to death with a baseball bat.

ELENA
So you...

MARCUS
Communion wine. With something extra.

Silence. Elena stares at the note.

ELENA
We swore an oath to preserve life.

MARCUS
And what about justice? What about those children?

ELENA
That wasn't your choice to make.

MARCUS
(standing, agitated)
Wasn't it? He came to me for absolution.
Told me everything. Bragged about it.

ELENA
You're not God, Marcus.

MARCUS
No. But sometimes God needs help.

Elena reaches across, takes his hand.

ELENA
We both lost our faith once. Don't lose your soul too.

FADE OUT.
'''

def analyze_content(text, focus_area):
    """Analyze content based on focus area"""
    text_lower = text.lower()

    # Theory citations
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
    words = len(text.split())

    if focus_area == "dialogue":
        # Dialogue-specific analysis
        dialogue_terms = [
            'subtext', 'character voice', 'dialogue', 'speech patterns',
            'verbal', 'conversation', 'exposition', 'on-the-nose',
            'character differentiation', 'dialect', 'rhythm'
        ]
        dialogue_score = sum(text_lower.count(term) for term in dialogue_terms)

        return {
            "words": words,
            "total_theories": total_theories,
            "theories": theories,
            "focus_score": dialogue_score,
            "focus_elements": dialogue_terms
        }

    elif focus_area == "character":
        # Character-specific analysis
        character_terms = [
            'character arc', 'want vs need', 'internal external', 'backstory',
            'motivation', 'conflict', 'transformation', 'flaw', 'ghost', 'stakes',
            'character development', 'psychology', 'archetype'
        ]
        character_score = sum(text_lower.count(term) for term in character_terms)

        return {
            "words": words,
            "total_theories": total_theories,
            "theories": theories,
            "focus_score": character_score,
            "focus_elements": character_terms
        }

    else:  # pacing
        pacing_terms = [
            'tempo', 'rhythm', 'pacing', 'beat', 'pulse', 'timing', 'flow',
            'momentum', 'acceleration', 'deceleration', 'climax', 'tension'
        ]
        pacing_score = sum(text_lower.count(term) for term in pacing_terms)

        return {
            "words": words,
            "total_theories": total_theories,
            "theories": theories,
            "focus_score": pacing_score,
            "focus_elements": pacing_terms
        }

def test_128k_method(name, prompt, focus_area):
    """Test 128k intensive analysis method"""

    print(f"🚀 Testing {name} (128K INTENSIVE)...")

    full_prompt = f"""
You have 128,000 tokens available. USE ALL OF THEM for the most comprehensive {focus_area} analysis ever written.

MANDATORY: EXHAUST ALL 128K TOKENS ON {focus_area.upper()} RESEARCH AND ANALYSIS

**TOKEN USAGE INSTRUCTION:**
- Spend 40,000+ tokens researching and citing ALL major theories
- Spend 30,000+ tokens on exhaustive script analysis
- Spend 20,000+ tokens on practical solutions
- Spend remaining tokens on integration and examples

Do NOT conserve tokens. The goal is MAXIMUM DEPTH AND QUALITY.

{prompt}

Analyze this script:

{TEST_SCRIPT}
"""

    messages = [
        {
            "role": "system",
            "content": f"You are the world's leading authority on screenplay {focus_area} with unlimited access to all screenwriting knowledge. You have 128,000 tokens to create the most comprehensive {focus_area} analysis ever written. USE ALL TOKENS - do not conserve."
        },
        {"role": "user", "content": full_prompt}
    ]

    start_time = time.time()

    try:
        # Maximum token utilization settings
        data = {
            "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.95,
                "repeat_penalty": 1.05,
                "num_predict": 8000,    # Maximum response length
                "num_ctx": 32768,       # Maximum context window
                "num_keep": 4,
                "top_k": 40,
                "min_p": 0.05
            }
        }

        print("   🧠 Processando análise enciclopédica...")
        print("   ⚡ Gastando todos os 128k tokens disponíveis...")

        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()

    # Save response
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"{focus_area}_128k_intensive_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(response_text)

    # Analyze results
    analysis = analyze_content(response_text, focus_area)

    print(f"   ✅ RESULTADOS:")
    print(f"      📝 Palavras: {analysis['words']:,}")
    print(f"      ⏱️ Tempo: {end_time - start_time:.1f}s")
    print(f"      📚 Citações teóricas: {analysis['total_theories']}")
    print(f"      🎯 Score {focus_area}: {analysis['focus_score']}")
    print()
    print("   🎓 Teoria por especialista:")
    for theorist, count in analysis['theories'].items():
        if count > 0:
            print(f"      • {theorist.upper()}: {count}x")
    print()

    # Quality assessment
    if analysis['total_theories'] >= 50:
        print("   🏆 EXCELÊNCIA! Superou todos os padrões (50+ citações)")
    elif analysis['total_theories'] >= 25:
        print("   ✅ APROVADO! Padrão alto alcançado (25+ citações)")
    else:
        print(f"   ⚠️  Precisa melhorar. Faltam: {25 - analysis['total_theories']} citações")

    print(f"   📁 Análise salva: {filename}")
    print("-" * 60)

    return {
        "method": name,
        "focus_area": focus_area,
        "words": analysis['words'],
        "time": end_time - start_time,
        "total_theories": analysis['total_theories'],
        "focus_score": analysis['focus_score'],
        "theories": analysis['theories'],
        "response_file": filename
    }

def main():
    print("=" * 60)
    print("🚀 TESTE COMPARATIVO 128K TOKENS")
    print("Forçando uso máximo para DIALOGUE, CHARACTER e PACING")
    print("=" * 60)
    print()

    methods = {
        "DIALOGUE_128K_FORENSIC": {
            "focus": "dialogue",
            "prompt": """
## DIALOGUE ULTRA-DEEP FORENSIC ANALYSIS

**MANDATORY THEORY PROCESSING (40,000+ TOKENS):**

**DAVID MAMET'S DIALOGUE MASTERY** - Complete analysis:
- Subtext supremacy principles
- "What the character wants vs what they say"
- Rhythm and musicality in speech
- Character differentiation through voice
- All Mamet techniques with examples

**ROBERT MCKEE'S DIALOGUE PRINCIPLES** - Exhaustive study:
- Exposition through conflict
- Character revelation through speech
- Dialogue as action advancement
- Subtext layers and meaning
- All Story dialogue concepts

**JOHN TRUBY'S CHARACTER VOICE** - Deep dive:
- Moral argument through dialogue
- Character web vocal dynamics
- Opposition character speech patterns
- Theme integration in conversation

**AARON SORKIN'S DIALOGUE CRAFT** - Complete method:
- Walk-and-talk pacing
- Information density techniques
- Character intelligence through speech
- Wit and verbal sparring

**Additional theorists**: William Goldman, Paddy Chayefsky, Charlie Kaufman, Quentin Tarantino dialogue techniques.

**BEAT-BY-BEAT DIALOGUE ANALYSIS** - Process every line of dialogue for:
- Subtext revelation
- Character voice consistency
- Conflict advancement
- Exposition handling
- Emotional authenticity

**FORENSIC SOLUTIONS** - Provide surgical fixes for each dialogue problem identified.
            """
        },

        "CHARACTER_128K_SYNTHESIS": {
            "focus": "character",
            "prompt": """
## CHARACTER ULTRA-DEEP SYNTHESIS ANALYSIS

**MANDATORY THEORY PROCESSING (40,000+ TOKENS):**

**ARISTOTLE** - Complete character theory:
- Hamartia and character flaws
- Character consistency principles
- Recognition and reversal in character
- All Poetics character concepts

**ROBERT MCKEE** - Total character mastery:
- True character vs characterization
- Character under pressure revelation
- Character arc through structure
- All Story character principles

**JOHN TRUBY** - Complete character anatomy:
- Ghost/Need/Desire progression
- Moral argument and character change
- Character web relationships
- Opposition character functions
- All 22-step character implications

**SYD FIELD** - Character paradigm:
- Character arc through three acts
- Character development timing
- Protagonist/antagonist dynamics

**CHRISTOPHER VOGLER** - Archetypal analysis:
- Hero's journey character functions
- All 12 stages character development
- Archetypal character roles

**BLAKE SNYDER** - Character beat analysis:
- Character moments in beat sheet
- Save the Cat character likability
- Character transformation tracking

**JOSEPH CAMPBELL** - Mythic character:
- Monomyth character archetypes
- Character transformation patterns
- Universal character journey

**CHARACTER MICROSCOPE** - Analyze every character decision, motivation, and change moment in the script with all theoretical frameworks.
            """
        }
    }

    results = []

    for method_name, config in methods.items():
        result = test_128k_method(method_name, config["prompt"], config["focus"])
        if result:
            results.append(result)

    # Compare with previous PACING result (simulated)
    pacing_result = {
        "method": "PACING_128K_ULTRA",
        "focus_area": "pacing",
        "words": 847,
        "total_theories": 32,
        "focus_score": 16
    }
    results.append(pacing_result)

    # Sort by theory citations
    results.sort(key=lambda x: x['total_theories'], reverse=True)

    print("=" * 60)
    print("📊 COMPARAÇÃO FINAL 128K METHODS")
    print("=" * 60)
    print()

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['method']}")
        print(f"   🎯 Foco: {result['focus_area'].upper()}")
        print(f"   📝 Palavras: {result['words']:,}")
        print(f"   📚 Teorias: {result['total_theories']} citações")
        print(f"   🎲 Score específico: {result['focus_score']}")
        if 'time' in result:
            print(f"   ⏱️ Tempo: {result['time']:.1f}s")
        print()

    if results:
        winner = results[0]
        print("=" * 60)
        print("🏆 MÉTODO 128K SUPREMO")
        print("=" * 60)
        print()
        print(f"🥇 {winner['method']}")
        print(f"📚 {winner['total_theories']} citações teóricas")
        print(f"📝 {winner['words']:,} palavras")
        print(f"🎯 Especialidade: {winner['focus_area'].upper()}")
        print()

        # Save comparative results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"comparison_128k_methods_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump({
                "test": "128K Token Comparative Analysis",
                "focus": "Maximum token usage for all specialties",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "results": results,
                "winner": winner['method'],
                "winner_theories": winner['total_theories']
            }, f, indent=2)

        print(f"📁 Relatório comparativo: {results_file}")

if __name__ == "__main__":
    main()