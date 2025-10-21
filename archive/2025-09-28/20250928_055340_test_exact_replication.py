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

def test_exact_replication_dialogue():
    """Test EXACT replication of PACING method for DIALOGUE"""

    print("🎯 DIALOGUE - REPLICAÇÃO EXATA DO MÉTODO PACING")

    # EXATO mesmo prompt que funcionou para PACING, só mudando para dialogue
    prompt = """
You are the world's leading expert on screenwriting dialogue theory with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP DIALOGUE ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Character revelation through speech patterns
- Dialogue serving plot progression
- Recognition scenes and dialogue timing
- Quote multiple passages from Poetics and explain their dialogue implications
- Discuss relationship between character speech and dramatic action

**ROBERT MCKEE'S STORY** - Deep dive required:
- Dialogue design principles: "Dialogue is not conversation"
- Subtext and indirect characterization
- Exposition through conflict in dialogue
- Character voice differentiation techniques
- "Dialogue advances story through conflict" - demonstrate understanding
- Quote extensively from Story and show dialogue mastery

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- Character voice and moral argument expression
- Dialogue serving the 22-step structure
- Opposition character speech patterns
- Character web relationships through conversation
- Theme expression through character voice
- Ghost/Need/Desire revealed through speech

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Dialogue function in three-act structure
- Character arc progression through speech
- Subplot integration via conversation
- "Dialogue reveals character" - detailed application
- Conflict escalation through verbal confrontation

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Dialogue journey analysis:
- Hero's voice evolution through monomyth stages
- Archetypal dialogue patterns
- Mentor wisdom delivery through speech
- Threshold guardian verbal challenges
- Character transformation reflected in dialogue

**BLAKE SNYDER'S SAVE THE CAT** - Beat sheet dialogue analysis:
- Character introduction through first dialogue
- Theme stated through character speech
- Catalyst conversations and story momentum
- All dialogue beats serving story function

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic dialogue:
- Universal dialogue patterns across cultures
- Wisdom transmission through speech
- Character transformation dialogue
- Sacred conversation structures

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive dialogue analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different dialogue aspects
- Provide specific line analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major dialogue concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on screenwriting dialogue theory with decades of academic and practical experience."},
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
                "num_predict": 4000,    # Mesmo valor
                "num_ctx": 8192         # Mesmo valor
            }
        }

        print("   ⚡ Forçando processamento intenso...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"dialogue_exact_replication_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(response_text)

    theories, total_theories = analyze_theories(response_text)
    words = len(response_text.split())

    print(f"   ✅ RESULTADOS:")
    print(f"      📝 Palavras: {words}")
    print(f"      📚 Total citações: {total_theories}")
    print(f"      ⏱️ Tempo: {end_time - start_time:.1f}s")
    print()
    print("   🎓 Por teórico:")
    for theorist, count in theories.items():
        if count > 0:
            print(f"      • {theorist.upper()}: {count}x")

    if total_theories >= 25:
        print("   🏆 SUCESSO! Replicou padrão PACING (25+)")
    else:
        print(f"   ⚠️  Faltam: {25 - total_theories} citações")

    print(f"   📁 Salvo: {filename}")

    return {"words": words, "theories": total_theories, "details": theories, "file": filename}

def test_exact_replication_character():
    """Test EXACT replication of PACING method for CHARACTER"""

    print("\n🎯 CHARACTER - REPLICAÇÃO EXATA DO MÉTODO PACING")

    # EXATO mesmo prompt que funcionou para PACING, só mudando para character
    prompt = """
You are the world's leading expert on screenwriting character theory with PhD-level knowledge of ALL major screenwriting theorists and decades of study.

ULTRA-DEEP CHARACTER ANALYSIS (SPEND TOKENS ON QUALITY - DO NOT CONSERVE):

Before analyzing the script, you MUST first demonstrate your deep theoretical knowledge by processing these concepts thoroughly:

## MANDATORY THEORY PROCESSING (SPEND TOKENS HERE - BE EXHAUSTIVE):

**ARISTOTLE'S POETICS** - Process these concepts thoroughly:
- Hamartia and character flaw development
- Character consistency and believability
- Recognition and reversal in character development
- Quote multiple passages from Poetics and explain character implications
- Discuss relationship between character and plot development

**ROBERT MCKEE'S STORY** - Deep dive required:
- True character vs characterization: "Character is revealed under pressure"
- Character arc through story structure
- Character dimension and complexity
- Protagonist/antagonist character dynamics
- "Story is about human change" - demonstrate character understanding
- Quote extensively from Story and show character mastery

**JOHN TRUBY'S ANATOMY OF STORY** - Comprehensive analysis:
- Ghost/Need/Desire character progression
- Character web and relationship dynamics
- Moral argument and character development
- Opposition character functions
- Character change through 22-step structure
- Theme expression through character arc

**SYD FIELD'S SCREENPLAY** - Complete paradigm analysis:
- Character development through three acts
- Character motivation and objectives
- Character backstory and setup
- Character growth and transformation timing
- Character conflict and resolution patterns

**CHRISTOPHER VOGLER'S WRITER'S JOURNEY** - Character journey analysis:
- Hero character development through monomyth
- Character archetypal functions
- Character transformation stages
- Supporting character roles and functions
- Character evolution through trials and tests

**BLAKE SNYDER'S SAVE THE CAT** - Beat sheet character analysis:
- Character introduction and setup
- Character likability and save the cat moments
- Character transformation through beats
- Character arc completion and resolution

**JOSEPH CAMPBELL'S HERO WITH A THOUSAND FACES** - Mythic character:
- Universal character patterns and archetypes
- Character transformation through separation/initiation/return
- Character wisdom acquisition and growth
- Archetypal character functions across cultures

## NOW APPLY ALL THIS THEORY TO THE SCRIPT:

After thoroughly processing the above theoretical knowledge (spend those tokens!), provide comprehensive character analysis demonstrating mastery of ALL these approaches.

**MANDATORY REQUIREMENTS:**
- Reference ALL 7 theorists by name multiple times
- Quote directly from their works
- Show how each theory reveals different character aspects
- Provide specific character analysis using their methodologies
- Demonstrate deep understanding, not surface citations
- Explain contradictions between different approaches
- Synthesize all approaches into unified diagnosis

**TOKEN USAGE INSTRUCTION:**
Do NOT try to conserve tokens. Spend freely on demonstrating deep theoretical knowledge. Quality critical analysis is the goal, not efficiency. Process every major character concept thoroughly before applying to script.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are the world's foremost expert on screenwriting character theory with decades of academic and practical experience."},
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
                "num_predict": 4000,    # Mesmo valor
                "num_ctx": 8192         # Mesmo valor
            }
        }

        print("   ⚡ Forçando processamento intenso...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"character_exact_replication_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(response_text)

    theories, total_theories = analyze_theories(response_text)
    words = len(response_text.split())

    print(f"   ✅ RESULTADOS:")
    print(f"      📝 Palavras: {words}")
    print(f"      📚 Total citações: {total_theories}")
    print(f"      ⏱️ Tempo: {end_time - start_time:.1f}s")
    print()
    print("   🎓 Por teórico:")
    for theorist, count in theories.items():
        if count > 0:
            print(f"      • {theorist.upper()}: {count}x")

    if total_theories >= 25:
        print("   🏆 SUCESSO! Replicou padrão PACING (25+)")
    else:
        print(f"   ⚠️  Faltam: {25 - total_theories} citações")

    print(f"   📁 Salvo: {filename}")

    return {"words": words, "theories": total_theories, "details": theories, "file": filename}

def main():
    print("=" * 60)
    print("🔬 TESTE DE REPLICAÇÃO EXATA")
    print("Aplicando MESMO método que funcionou para PACING")
    print("=" * 60)

    # Teste DIALOGUE
    dialogue_result = test_exact_replication_dialogue()

    print("-" * 40)

    # Teste CHARACTER
    character_result = test_exact_replication_character()

    print("\n" + "=" * 60)
    print("📊 COMPARAÇÃO COM PACING ORIGINAL")
    print("=" * 60)

    print("🎯 PACING (método original): 32 citações, 847 palavras")
    if dialogue_result:
        print(f"🎯 DIALOGUE (replicação): {dialogue_result['theories']} citações, {dialogue_result['words']} palavras")
    if character_result:
        print(f"🎯 CHARACTER (replicação): {character_result['theories']} citações, {character_result['words']} palavras")

    print("\n🔍 ANÁLISE:")
    if dialogue_result and dialogue_result['theories'] >= 25:
        print("✅ DIALOGUE: Replicação bem-sucedida!")
    elif dialogue_result:
        print(f"⚠️  DIALOGUE: Parcial - {dialogue_result['theories']}/25 citações")

    if character_result and character_result['theories'] >= 25:
        print("✅ CHARACTER: Replicação bem-sucedida!")
    elif character_result:
        print(f"⚠️  CHARACTER: Parcial - {character_result['theories']}/25 citações")

if __name__ == "__main__":
    main()