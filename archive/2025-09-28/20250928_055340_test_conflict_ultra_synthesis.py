#!/usr/bin/env python3
import ollama
import json
import time
from datetime import datetime

# Script de teste para análise de conflito
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

def test_conflict_ultra_synthesis():
    """Test CONFLICT using THEME's winning method"""

    print("⚔️ CONFLICT ULTRA SYNTHESIS - Aplicando técnica THEME vencedora")

    # Usar EXATA estrutura que funcionou para THEME (35 citações)
    prompt = """
You are the world's leading expert on dramatic conflict theory with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP CONFLICT ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Hamartia and internal conflict origins
- Agon (conflict) as dramatic core
- Protagonist vs antagonist forces
- Internal vs external conflict in tragedy
- Quote multiple passages from Poetics about dramatic conflict
- Peripeteia (reversal) through conflict escalation

**ROBERT MCKEE'S STORY** - Deep dive required:
- Three levels of conflict: inner, personal, extra-personal
- Conflict as the substance of story
- Progressive complications through conflict
- "Nothing moves forward except through conflict"
- Gap between expectation and result
- Forces of antagonism principles
- Quote extensively from Story about conflict dynamics

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- Four-corner opposition system
- Conflict through competing values
- Weakness/need creating internal conflict
- Opponent as defining element
- Battle as conflict climax
- Moral argument through conflict
- Conflict webs in complex narratives

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Conflict driving three-act structure
- Internal and external conflicts interweaving
- Conflict escalation through plot points
- Obstacles and complications framework
- Character conflict vs situation conflict
- Conflict resolution in Act III

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Conflict journey analysis:
- Shadow as conflict embodiment
- Threshold guardians as conflict obstacles
- Internal conflict in hero's refusal
- Ordeal as maximum conflict point
- Enemies and allies in conflict web
- Inner and outer conflict convergence

**BLAKE SNYDER'S SAVE THE CAT** - Conflict beat analysis:
- Catalyst introducing conflict
- Debate as internal conflict
- Bad guys close in escalation
- All is lost as conflict peak
- Dark night of soul internal battle
- Finale conflict resolution

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic conflict:
- Dragon battle as universal conflict
- Internal dragons vs external dragons
- Conflict with father/authority figures
- Temptation as internal conflict
- Atonement through conflict resolution
- Conflict as transformation catalyst

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive conflict analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different conflict aspects
- Provide specific conflict analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified conflict diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major conflict concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on dramatic conflict theory with decades of academic and practical experience."},
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

        print("   ⚡ Processamento intensivo de teoria de conflito...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"conflict_ultra_synthesis_{timestamp}.txt"

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

    # Análise de qualidade de conflito
    conflict_terms = [
        'conflict', 'opposition', 'antagonist', 'struggle', 'tension',
        'obstacle', 'complication', 'dilemma', 'confrontation', 'clash', 'battle'
    ]

    text_lower = response_text.lower()
    conflict_score = sum(text_lower.count(term) for term in conflict_terms)

    print(f"   ⚔️ Score de conflito específico: {conflict_score}")

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
        "conflict_score": conflict_score,
        "theories": theories,
        "file": filename,
        "time": end_time - start_time
    }

def main():
    print("=" * 60)
    print("⚔️ TESTE CONFLICT ULTRA SYNTHESIS")
    print("Aplicando técnica vencedora do THEME para CONFLICT")
    print("=" * 60)
    print()

    result = test_conflict_ultra_synthesis()

    if result:
        print("\n" + "=" * 60)
        print("📊 COMPARAÇÃO COM TOP 6 MÉTODOS")
        print("=" * 60)
        print()
        print("🥇 THEME (campeão): 35 citações, 757 palavras")
        print("🥈 PACING: 32 citações, 847 palavras")
        print("🥉 ACTION: 28 citações, 661 palavras")
        print("4️⃣ STRUCTURE: 25 citações, 868 palavras")
        print("5️⃣ CHARACTER: 17-25 citações, 608-725 palavras")
        print("6️⃣ DIALOGUE: 7-8 citações, 491-625 palavras")
        print(f"⚔️ CONFLICT (novo): {result['total_theories']} citações, {result['words']} palavras")
        print()

        # Análise de posição
        if result['total_theories'] >= 35:
            print("🏆 CONFLICT: POTENCIAL NOVO CAMPEÃO! Igualou/Superou THEME!")
        elif result['total_theories'] >= 32:
            print("🥈 CONFLICT: EXCELENTE! Top 2 com PACING")
        elif result['total_theories'] >= 28:
            print("🥉 CONFLICT: MUITO BOM! Top 3 com ACTION")
        elif result['total_theories'] >= 25:
            print("📈 CONFLICT: BOM! Top 4-5 performance")
        elif result['total_theories'] >= 17:
            print("📊 CONFLICT: Razoável, nível médio")
        else:
            print("⚠️ CONFLICT: Precisa melhorias significativas")

        print(f"\n⚔️ Score de conflito específico: {result['conflict_score']}")
        print(f"⏱️ Tempo de processamento: {result['time']:.1f}s")

        # Save results
        results_data = {
            "test": "Conflict Ultra Synthesis Test",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": "CONFLICT Ultra Synthesis (THEME technique)",
            "results": result,
            "ranking": {
                "theme": {"theories": 35, "words": 757, "position": 1},
                "pacing": {"theories": 32, "words": 847, "position": 2},
                "action": {"theories": 28, "words": 661, "position": 3},
                "structure": {"theories": 25, "words": 868, "position": 4},
                "conflict": {"theories": result['total_theories'], "words": result['words'], "position": "TBD"}
            }
        }

        results_filename = f"conflict_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Relatório detalhado: {results_filename}")

if __name__ == "__main__":
    main()