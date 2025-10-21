#!/usr/bin/env python3
import ollama
import json
import time
from datetime import datetime

# Script de teste para análise de tensão
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

def test_tension_ultra_synthesis():
    """Test TENSION using THEME's winning method"""

    print("⚡ TENSION ULTRA SYNTHESIS - Aplicando técnica THEME vencedora")

    # Usar EXATA estrutura que funcionou para THEME (35 citações)
    prompt = """
You are the world's leading expert on narrative tension and suspense theory with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP TENSION ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Tension through fear and pity arousal
- Suspense in recognition and reversal
- Building tension toward catharsis
- Dramatic irony creating audience tension
- Quote multiple passages from Poetics about tension mechanics
- Unity of time intensifying tension

**ROBERT MCKEE'S STORY** - Deep dive required:
- Tension through the gap between expectation and result
- Progressive complications building tension
- Turning points as tension releases and rebuilds
- "Tension is created by desire meeting obstacle"
- Dramatic tension vs narrative drive
- Subtext creating underlying tension
- Quote extensively from Story about tension dynamics

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- Tension through dramatic question
- Desire line maintaining narrative tension
- Reveals and reversals as tension tools
- Opponent escalation increasing tension
- Moral dilemma creating internal tension
- Subplot weaving for tension layering
- Drive, mystery, and suspense techniques

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Tension building through act structure
- Plot points as tension pivots
- Rising action and tension curves
- Setup creating tension expectations
- Midpoint shifting tension dynamics
- Climax as maximum tension point
- Page-by-page tension management

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Tension journey analysis:
- Tension in crossing thresholds
- Tests creating escalating tension
- Approach to inmost cave building dread
- Ordeal as tension climax
- Death and rebirth tension patterns
- Road back maintaining tension
- Suspense through archetypal patterns

**BLAKE SNYDER'S SAVE THE CAT** - Tension beat analysis:
- Promise of the premise creating expectations
- B-story providing tension relief
- Fun and Games establishing tension baseline
- Midpoint raising tension stakes
- Bad guys close in escalation
- All is lost false defeat tension
- Dark night maintaining emotional tension

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic tension:
- Belly of the whale tension
- Road of trials building tension
- Meeting with goddess/temptress tension
- Atonement tension with authority
- Apotheosis release and rebuild
- Return threshold final tensions
- Master of two worlds resolution

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive tension analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different tension aspects
- Provide specific tension analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified tension diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major tension concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on narrative tension and suspense theory with decades of academic and practical experience."},
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

        print("   ⚡ Processamento intensivo de teoria de tensão...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"tension_ultra_synthesis_{timestamp}.txt"

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

    # Análise de qualidade de tensão
    tension_terms = [
        'tension', 'suspense', 'dread', 'anticipation', 'escalation',
        'stakes', 'pressure', 'buildup', 'climax', 'release', 'relief', 'anxiety'
    ]

    text_lower = response_text.lower()
    tension_score = sum(text_lower.count(term) for term in tension_terms)

    print(f"   ⚡ Score de tensão específico: {tension_score}")

    # Comparação com TOP performers
    if total_theories >= 35:
        print("   🏆 EXCELÊNCIA! Igualou THEME (35+ citações)")
    elif total_theories >= 32:
        print("   ✅ SUCESSO! Nível PACING alcançado (32+ citações)")
    elif total_theories >= 28:
        print("   ✅ MUITO BOM! Nível ACTION alcançado (28+ citações)")
    elif total_theories >= 25:
        print("   ⚠️  BOM! Padrão alto alcançado (25+ citações)")
    else:
        print(f"   ❌ INSUFICIENTE. Faltam: {25 - total_theories} citações")

    print(f"   📁 Análise salva: {filename}")

    return {
        "words": words,
        "total_theories": total_theories,
        "tension_score": tension_score,
        "theories": theories,
        "file": filename,
        "time": end_time - start_time
    }

def main():
    print("=" * 60)
    print("⚡ TESTE TENSION ULTRA SYNTHESIS")
    print("Aplicando técnica vencedora do THEME para TENSION")
    print("=" * 60)
    print()

    result = test_tension_ultra_synthesis()

    if result:
        print("\n" + "=" * 60)
        print("📊 COMPARAÇÃO COM TOP 7 MÉTODOS")
        print("=" * 60)
        print()
        print("🥇 THEME: 35 citações, 757 palavras")
        print("🥈 PACING: 32 citações, 847 palavras")
        print("🥉 ACTION: 28 citações, 661 palavras")
        print("4️⃣ STRUCTURE: 25 citações, 868 palavras")
        print("5️⃣ CHARACTER: 17-25 citações, 608-725 palavras")
        print("5️⃣ CONFLICT: 17 citações, 977 palavras")
        print("6️⃣ DIALOGUE: 7-8 citações, 491-625 palavras")
        print(f"⚡ TENSION (novo): {result['total_theories']} citações, {result['words']} palavras")
        print()

        # Análise de posição
        if result['total_theories'] >= 35:
            print("🏆 TENSION: POTENCIAL NOVO CAMPEÃO! Igualou/Superou THEME!")
        elif result['total_theories'] >= 32:
            print("🥈 TENSION: EXCELENTE! Top 2 com PACING")
        elif result['total_theories'] >= 28:
            print("🥉 TENSION: MUITO BOM! Top 3 com ACTION")
        elif result['total_theories'] >= 25:
            print("📈 TENSION: BOM! Top 4 performance")
        elif result['total_theories'] >= 17:
            print("📊 TENSION: Razoável, nível médio")
        else:
            print("⚠️ TENSION: Precisa melhorias significativas")

        print(f"\n⚡ Score de tensão específico: {result['tension_score']}")
        print(f"⏱️ Tempo de processamento: {result['time']:.1f}s")

        # Save results
        results_data = {
            "test": "Tension Ultra Synthesis Test",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": "TENSION Ultra Synthesis (THEME technique)",
            "results": result,
            "ranking": {
                "theme": {"theories": 35, "words": 757, "position": 1},
                "pacing": {"theories": 32, "words": 847, "position": 2},
                "action": {"theories": 28, "words": 661, "position": 3},
                "structure": {"theories": 25, "words": 868, "position": 4},
                "tension": {"theories": result['total_theories'], "words": result['words'], "position": "TBD"}
            }
        }

        results_filename = f"tension_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Relatório detalhado: {results_filename}")

if __name__ == "__main__":
    main()