#!/usr/bin/env python3
import ollama
import json
import time
from datetime import datetime

# Script de teste estrutural
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

def test_structure_ultra_synthesis():
    """Test STRUCTURE using THEME's winning method"""

    print("🏗️ STRUCTURE ULTRA SYNTHESIS - Aplicando técnica THEME vencedora")

    # Usar EXATA estrutura que funcionou para THEME (35 citações)
    prompt = """
You are the world's leading expert on screenplay structure theory with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP STRUCTURE ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Beginning, middle, and end structure fundamentals
- Unity of action and structural coherence
- Plot as the soul of tragedy - structural primacy
- Reversal and recognition as structural elements
- Quote multiple passages from Poetics about dramatic structure
- Six elements of tragedy and their structural relationships

**ROBERT MCKEE'S STORY** - Deep dive required:
- Three-level structure: Act, Sequence, Scene
- Story spine and structural integrity
- Inciting incident placement and function
- Progressive complications building structure
- Crisis, climax, resolution architecture
- "Structure is a selection of events" - explore deeply
- Quote extensively from Story about structural design

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- 22-step story structure detailed exploration
- Seven key steps as structural foundation
- Weakness/Need setup structuring the journey
- Desire line driving structural momentum
- Battle sequence as structural climax
- Self-revelation completing structure
- Organic vs mechanical structure debate

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Three-act structure paradigm in detail
- Plot points as structural hinges
- Page count mathematics and timing
- Setup, confrontation, resolution framework
- Midpoint as structural center
- First ten pages structural importance
- Paradigm worksheet application

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Structural journey analysis:
- 12-stage hero's journey structure
- Ordinary world vs special world structure
- Threshold crossings as structural markers
- Tests, allies, enemies structuring Act II
- Ordeal at structure's center
- Return with elixir completing structure
- Circular vs linear structural patterns

**BLAKE SNYDER'S SAVE THE CAT** - Beat sheet structure:
- 15-beat structure precisely defined
- Opening image/final image bookends
- Catalyst timing at page 12
- B-story structural function
- Fun and Games as structural heart
- All Is Lost and Dark Night placement
- Finale structural payoff system

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic structure:
- Monomyth circular structure pattern
- Departure, initiation, return framework
- 17 stages of the journey structure
- Structural universality across cultures
- Myth as structural template
- Sacred and profane structural division

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive structure analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different structural aspects
- Provide specific structural analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified structural diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major structure concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on screenplay structure theory with decades of academic and practical experience."},
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

        print("   ⚡ Processamento intensivo de teoria estrutural...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"structure_ultra_synthesis_{timestamp}.txt"

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

    # Análise de qualidade estrutural
    structure_terms = [
        'three-act', 'plot point', 'inciting incident', 'climax', 'resolution',
        'midpoint', 'catalyst', 'setup', 'confrontation', 'paradigm', 'beat', 'sequence'
    ]

    text_lower = response_text.lower()
    structure_score = sum(text_lower.count(term) for term in structure_terms)

    print(f"   🏗️ Score estrutural específico: {structure_score}")

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
        "structure_score": structure_score,
        "theories": theories,
        "file": filename,
        "time": end_time - start_time
    }

def main():
    print("=" * 60)
    print("🏗️ TESTE STRUCTURE ULTRA SYNTHESIS")
    print("Aplicando técnica vencedora do THEME para STRUCTURE")
    print("=" * 60)
    print()

    result = test_structure_ultra_synthesis()

    if result:
        print("\n" + "=" * 60)
        print("📊 COMPARAÇÃO COM TOP 5 MÉTODOS")
        print("=" * 60)
        print()
        print("🥇 THEME (campeão): 35 citações, 757 palavras")
        print("🥈 PACING: 32 citações, 847 palavras")
        print("🥉 ACTION: 28 citações, 661 palavras")
        print("4️⃣ CHARACTER: 17-25 citações, 608-725 palavras")
        print("5️⃣ DIALOGUE: 7-8 citações, 491-625 palavras")
        print(f"🏗️ STRUCTURE (novo): {result['total_theories']} citações, {result['words']} palavras")
        print()

        # Análise de posição
        if result['total_theories'] >= 35:
            print("🏆 STRUCTURE: POTENCIAL NOVO CAMPEÃO! Igualou/Superou THEME!")
        elif result['total_theories'] >= 32:
            print("🥈 STRUCTURE: EXCELENTE! Top 2 com PACING")
        elif result['total_theories'] >= 28:
            print("🥉 STRUCTURE: MUITO BOM! Top 3 com ACTION")
        elif result['total_theories'] >= 25:
            print("📈 STRUCTURE: BOM! Top 4 com CHARACTER")
        elif result['total_theories'] >= 17:
            print("📊 STRUCTURE: Razoável, nível médio")
        else:
            print("⚠️ STRUCTURE: Precisa melhorias significativas")

        print(f"\n🏗️ Score estrutural específico: {result['structure_score']}")
        print(f"⏱️ Tempo de processamento: {result['time']:.1f}s")

        # Save results
        results_data = {
            "test": "Structure Ultra Synthesis Test",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": "STRUCTURE Ultra Synthesis (THEME technique)",
            "results": result,
            "ranking": {
                "theme": {"theories": 35, "words": 757, "position": 1},
                "pacing": {"theories": 32, "words": 847, "position": 2},
                "action": {"theories": 28, "words": 661, "position": 3},
                "structure": {"theories": result['total_theories'], "words": result['words'], "position": "TBD"}
            }
        }

        results_filename = f"structure_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Relatório detalhado: {results_filename}")

if __name__ == "__main__":
    main()