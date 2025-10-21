#!/usr/bin/env python3
import ollama
import json
import time
from datetime import datetime

# Action-focused script for testing
TEST_SCRIPT = '''
FADE IN:

EXT. ROOFTOP - NIGHT

ALEX (35), tactical gear, sprints across the rain-slicked roof. Behind him, THREE ARMED GUARDS give chase.

GUARD 1
(into radio)
Target heading north! Cut him off!

Alex leaps across a six-foot gap to the next building. Rolls. Keeps running.

A HELICOPTER rises from below, searchlight blazing.

PILOT (V.O.)
(over loudspeaker)
Stop! There's nowhere to run!

Alex doesn't slow. He pulls a GRAPPLING GUN from his belt, fires it at a water tower on the adjacent building.

The cable goes taut. Alex jumps.

He swings across the gap as BULLETS tear through the air where he was.

MID-AIR - Alex releases the cable, crashes through a WINDOW—

INT. ABANDONED WAREHOUSE - CONTINUOUS

—rolls across broken glass. Gets up. Blood on his hands.

ALEX
(to earpiece)
I'm in. Third floor.

MAYA (V.O.)
(filtered)
Guards converging on your position.
You've got maybe thirty seconds.

Alex spots what he came for: a BRIEFCASE chained to a desk.

He pulls out THERMITE CORD, wraps it around the chain.

ALEX
Twenty seconds is all I need.

The thermite IGNITES. Sparks fly. The chain melts.

FOOTSTEPS thunder up the stairs.

Alex grabs the briefcase, runs toward the window—

The door EXPLODES inward. Guards rush in, weapons raised.

GUARD 2
Drop it!

Alex doesn't stop. He dives through the window as—

BULLETS shatter what's left of the glass.

EXT. BUILDING - CONTINUOUS

Alex falls three stories into a DUMPSTER filled with trash bags.

ALEX
(groaning)
Maya... need extraction. Now.

A BLACK SUV screeches around the corner.

MAYA (V.O.)
Already here. Move!

Alex climbs out, briefcase in hand, limping toward the vehicle as—

The helicopter's searchlight finds him.

PILOT (V.O.)
Target acquired! Open fire!

The SUV's door flies open. Alex dives in as—

MACHINE GUN FIRE tears up the pavement.

INT. SUV - CONTINUOUS

Maya floors it. The vehicle rockets forward.

MAYA
You get it?

Alex holds up the briefcase, grinning through the pain.

ALEX
Always do.

FADE OUT.
'''

def analyze_theories(text):
    """Count theory citations"""
    text_lower = text.lower()
    theories = {
        'mckee': text_lower.count('mckee'),
        'truby': text_lower.count('truby'),
        'vogler': text_lower.count('vogler'),
        'field': text_lower.count('field'),
        'campbell': text_lower.count('campbell'),
        'snyder': text_lower.count('snyder'),
        'aristotle': text_lower.count('aristotle')
    }
    return theories, sum(theories.values())

def test_action_ultra_synthesis():
    """Test ACTION using THEME's winning method"""

    print("🎬 ACTION ULTRA SYNTHESIS - Aplicando técnica THEME vencedora")

    # Usar EXATA estrutura que funcionou para THEME (35 citações)
    prompt = """
You are the world's leading expert on screenwriting action sequences with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP ACTION ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Spectacle and action in dramatic structure
- Physical action serving plot progression
- Unity of action and its dramatic importance
- Quote multiple passages from Poetics about action and spectacle
- Discuss relationship between action and character revelation

**ROBERT MCKEE'S STORY** - Deep dive required:
- Action as character revelation: "Action is character"
- Physical conflict expressing inner conflict
- Kinetic storytelling and visual narrative
- Action serving story values and progression
- "True character is revealed in choices made under pressure" - in action
- Quote extensively from Story about action sequences

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- Action serving the 22-step structure
- Battle sequences and moral argument
- Physical opposition revealing theme
- Action as plot weaving technique
- Character revelation through physical choices
- Violence and its narrative function

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Action in three-act structure placement
- Plot points through action sequences
- Physical conflict escalation patterns
- Action serving character arc
- Set pieces and their structural function
- Page count and action scene pacing

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Action journey analysis:
- Hero's trials through physical challenges
- Ordeal as ultimate action sequence
- Chase scenes as threshold crossings
- Combat as character transformation
- Physical journey mirroring inner journey
- Action archetypes and their functions

**BLAKE SNYDER'S SAVE THE CAT** - Action beat analysis:
- Fun and Games action sequences
- Set piece construction and placement
- Catalyst action moments
- All Is Lost physical defeats
- Finale action resolution
- Genre expectations for action

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic action:
- Physical trials in monomyth structure
- Combat with shadow/dragon archetype
- Chase as separation from ordinary world
- Physical transformation moments
- Action as ritual and initiation
- Universal action patterns across myths

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive action analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different action aspects
- Provide specific action analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified action diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major action concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on screenwriting action sequences with decades of academic and practical experience."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    start_time = time.time()

    try:
        # EXATAS configurações do THEME vencedor
        data = {
            "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.75,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_predict": 4000,    # Mesmo do THEME
                "num_ctx": 8192         # Mesmo do THEME
            }
        }

        print("   ⚡ Processamento intensivo de teoria de ação...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"action_ultra_synthesis_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(response_text)

    theories, total_theories = analyze_theories(response_text)
    words = len(response_text.split())

    print(f"   ✅ RESULTADOS:")
    print(f"      📝 Palavras: {words}")
    print(f"      📚 Total citações: {total_theories}")
    print(f"      ⏱️ Tempo: {end_time - start_time:.1f}s")
    print()
    print("   🎓 Citações por teórico:")
    for theorist, count in theories.items():
        if count > 0:
            print(f"      • {theorist.upper()}: {count}x")
    print()

    # Análise de qualidade de ação
    action_terms = [
        'chase', 'fight', 'combat', 'battle', 'conflict', 'tension',
        'kinetic', 'physical', 'movement', 'choreography', 'stunt', 'explosive'
    ]

    text_lower = response_text.lower()
    action_score = sum(text_lower.count(term) for term in action_terms)

    print(f"   💥 Score de ação específico: {action_score}")

    # Comparação com THEME
    if total_theories >= 35:
        print("   🏆 EXCELÊNCIA! Igualou THEME (35+ citações)")
    elif total_theories >= 32:
        print("   ✅ SUCESSO! Nível PACING alcançado (32+ citações)")
    elif total_theories >= 25:
        print("   ⚠️  BOM! Padrão alto alcançado (25+ citações)")
    else:
        print(f"   ❌ INSUFICIENTE. Faltam: {25 - total_theories} citações")

    print(f"   📁 Análise salva: {filename}")

    return {
        "words": words,
        "total_theories": total_theories,
        "action_score": action_score,
        "theories": theories,
        "file": filename,
        "time": end_time - start_time
    }

def main():
    print("=" * 60)
    print("🎬 TESTE ACTION ULTRA SYNTHESIS")
    print("Aplicando técnica vencedora do THEME para ACTION")
    print("=" * 60)
    print()

    result = test_action_ultra_synthesis()

    if result:
        print("\n" + "=" * 60)
        print("📊 COMPARAÇÃO COM TOP 4 MÉTODOS")
        print("=" * 60)
        print()
        print("🥇 THEME (campeão): 35 citações, 757 palavras")
        print("🥈 PACING: 32 citações, 847 palavras")
        print("🥉 CHARACTER: 17-25 citações, 608-725 palavras")
        print("4️⃣ DIALOGUE: 7-8 citações, 491-625 palavras")
        print(f"🎬 ACTION (novo): {result['total_theories']} citações, {result['words']} palavras")
        print()

        # Análise de posição
        if result['total_theories'] >= 35:
            print("🏆 ACTION: POTENCIAL NOVO CAMPEÃO! Igualou/Superou THEME!")
        elif result['total_theories'] >= 32:
            print("🥈 ACTION: EXCELENTE! Top 2 com PACING")
        elif result['total_theories'] >= 25:
            print("🥉 ACTION: BOM! Top 3 com CHARACTER")
        elif result['total_theories'] >= 17:
            print("📈 ACTION: Razoável, nível médio")
        else:
            print("⚠️ ACTION: Precisa melhorias significativas")

        print(f"\n💥 Score de ação específico: {result['action_score']}")
        print(f"⏱️ Tempo de processamento: {result['time']:.1f}s")

        # Save results
        results_data = {
            "test": "Action Ultra Synthesis Test",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": "ACTION Ultra Synthesis (THEME technique)",
            "results": result,
            "ranking": {
                "theme": {"theories": 35, "words": 757, "position": 1},
                "pacing": {"theories": 32, "words": 847, "position": 2},
                "action": {"theories": result['total_theories'], "words": result['words'], "position": "TBD"}
            }
        }

        results_filename = f"action_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Relatório detalhado: {results_filename}")

if __name__ == "__main__":
    main()