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

def test_theme_ultra_synthesis():
    """Test THEME using exact PACING method"""

    print("🎯 THEME ULTRA SYNTHESIS - Replicando método PACING vencedor")

    # EXATO mesmo prompt estrutural que funcionou para PACING
    prompt = """
You are the world's leading expert on screenwriting theme theory with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP THEME ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Moral philosophy and thematic purpose in tragedy
- Theme serving catharsis and audience enlightenment
- Universal truths revealed through specific stories
- Quote multiple passages from Poetics and explain thematic implications
- Discuss relationship between theme and dramatic action

**ROBERT MCKEE'S STORY** - Deep dive required:
- Controlling idea and theme integration: "Theme is meaning"
- Value systems and moral arguments in storytelling
- Theme expressed through action, not dialogue
- Premise and thematic statement development
- "Theme must be earned through story" - demonstrate understanding
- Quote extensively from Story and show thematic mastery

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- Moral argument as story's backbone
- Theme woven through character arcs and plot
- Opposition of values creating thematic tension
- Moral premise and its expression through structure
- Theme serving the 22-step story progression
- Character philosophy conflicts revealing theme

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Theme established in setup and explored throughout
- Thematic development through three-act structure
- Character growth serving thematic purpose
- Theme as story's central organizing principle
- Conflict serving thematic exploration

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Thematic journey analysis:
- Universal themes in monomyth structure
- Theme serving hero's transformation
- Archetypal themes across cultures
- Wisdom acquisition as thematic element
- Theme revealed through hero's trials and growth

**BLAKE SNYDER'S SAVE THE CAT** - Thematic beat analysis:
- Theme stated early and explored throughout
- Character decisions reflecting thematic choices
- Theme serving each story beat
- Thematic resolution in final image
- Genre expectations and thematic conventions

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic theme:
- Universal human themes across mythologies
- Theme as collective unconscious expression
- Spiritual transformation and thematic meaning
- Cultural wisdom transmission through theme
- Archetypal themes in human storytelling

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive theme analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different thematic aspects
- Provide specific thematic analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified thematic diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major theme concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on screenwriting theme theory with decades of academic and practical experience."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    start_time = time.time()

    try:
        # EXATAS mesmas configurações que funcionaram para PACING
        data = {
            "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.75,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_predict": 4000,    # Mesmo valor do PACING
                "num_ctx": 8192         # Mesmo valor do PACING
            }
        }

        print("   ⚡ Processamento intensivo de teoria temática...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"theme_ultra_synthesis_{timestamp}.txt"

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

    # Análise de qualidade temática
    theme_terms = [
        'moral', 'justice', 'faith', 'redemption', 'forgiveness', 'ethics',
        'divine', 'human nature', 'responsibility', 'guilt', 'conscience'
    ]

    text_lower = response_text.lower()
    theme_score = sum(text_lower.count(term) for term in theme_terms)

    print(f"   🎭 Score temático específico: {theme_score}")

    # Comparação com PACING
    if total_theories >= 32:
        print("   🏆 EXCELÊNCIA! Superou PACING (32 citações)")
    elif total_theories >= 25:
        print("   ✅ SUCESSO! Padrão alto alcançado (25+ citações)")
    elif total_theories >= 17:
        print("   ⚠️  BOM! Nível CHARACTER alcançado (17+ citações)")
    else:
        print(f"   ❌ INSUFICIENTE. Faltam: {17 - total_theories} citações")

    print(f"   📁 Análise salva: {filename}")

    return {
        "words": words,
        "total_theories": total_theories,
        "theme_score": theme_score,
        "theories": theories,
        "file": filename,
        "time": end_time - start_time
    }

def main():
    print("=" * 60)
    print("🎭 TESTE THEME ULTRA SYNTHESIS")
    print("Aplicando técnica vencedora do PACING para THEME")
    print("=" * 60)
    print()

    result = test_theme_ultra_synthesis()

    if result:
        print("\n" + "=" * 60)
        print("📊 COMPARAÇÃO COM OUTROS MÉTODOS")
        print("=" * 60)
        print()
        print("🎯 PACING (método original): 32 citações, 847 palavras")
        print("🎯 CHARACTER (replicação): 17 citações, 608 palavras")
        print("🎯 DIALOGUE (replicação): 7 citações, 491 palavras")
        print(f"🎯 THEME (novo): {result['total_theories']} citações, {result['words']} palavras")
        print()

        # Análise de posição
        if result['total_theories'] >= 32:
            print("🥇 THEME: NOVO CAMPEÃO! Superou PACING!")
        elif result['total_theories'] >= 25:
            print("🥈 THEME: EXCELENTE! Segundo lugar após PACING")
        elif result['total_theories'] >= 17:
            print("🥉 THEME: BOM! Mesmo nível do CHARACTER")
        else:
            print("📈 THEME: Precisa melhorias para competir")

        print(f"\n🎭 Score temático específico: {result['theme_score']}")
        print(f"⏱️ Tempo de processamento: {result['time']:.1f}s")

        # Save results
        results_data = {
            "test": "Theme Ultra Synthesis Test",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": "THEME Ultra Synthesis (PACING technique)",
            "results": result,
            "comparison": {
                "pacing": {"theories": 32, "words": 847},
                "character": {"theories": 17, "words": 608},
                "dialogue": {"theories": 7, "words": 491},
                "theme": {"theories": result['total_theories'], "words": result['words']}
            }
        }

        results_filename = f"theme_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Relatório detalhado: {results_filename}")

if __name__ == "__main__":
    main()