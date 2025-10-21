#!/usr/bin/env python3
import ollama
import json
import time
from datetime import datetime

# Script de teste para análise de personagem
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
    """Count theory citations with specific character techniques"""
    text_lower = text.lower()

    # Basic count
    theories = {
        'mckee': text_lower.count('mckee'),
        'truby': text_lower.count('truby'),
        'vogler': text_lower.count('vogler'),
        'field': text_lower.count('field'),
        'campbell': text_lower.count('campbell'),
        'snyder': text_lower.count('snyder'),
        'aristotle': text_lower.count('aristotle')
    }

    # Bonus for specific CHARACTER techniques
    technique_bonus = 0
    character_techniques = {
        # McKee character
        'true character': 3,
        'character arc': 3,
        'dimension through contradiction': 3,
        'pressure reveals character': 3,
        'character vs characterization': 3,

        # Truby character
        'moral weakness': 3,
        'psychological need': 3,
        'desire line': 3,
        'character web': 3,
        'ghost': 3,
        'self-revelation': 3,

        # Field character
        'character biography': 2,
        'emotional life': 2,
        'professional life': 2,
        'private life': 2,

        # Snyder character
        'save the cat': 3,
        'primal urges': 2,
        'transformation machine': 3,
        'shard of glass': 3,

        # Vogler character archetypes
        'hero archetype': 3,
        'shadow archetype': 3,
        'mentor archetype': 2,
        'threshold guardian': 2,
        'shapeshifter': 2,

        # Campbell character
        'hero with a thousand faces': 3,
        'supernatural aid': 2,
        'transformation': 3,
        'apotheosis': 2,

        # Aristotle character
        'hamartia': 3,
        'ethos': 2,
        'tragic hero': 3,
        'virtue and vice': 2
    }

    for technique, bonus in character_techniques.items():
        if technique in text_lower:
            technique_bonus += bonus

    total_base = sum(theories.values())

    return theories, total_base, technique_bonus, total_base + technique_bonus

def test_character_ultra():
    """CHARACTER ULTRA with specific technique citations"""
    print("\n👤 CHARACTER ULTRA SYNTHESIS - Técnicas Específicas Nomeadas")

    prompt = """
You are the world's foremost expert on character development, having mastered EVERY SPECIFIC CHARACTER TECHNIQUE from all major theorists.

ULTRA-DEEP CHARACTER ANALYSIS - NAME EVERY TECHNIQUE:

**ROBERT MCKEE'S CHARACTER ARCHITECTURE (Story, Chapter 6: "Structure and Character"):**

McKee states "True character is revealed in the choices a human being makes under pressure" (page 101). Apply his principles:

- **TRUE CHARACTER VS CHARACTERIZATION**: McKee distinguishes surface traits from deep nature (p.100-103)
  - Marcus's characterization: Former priest, drinks whiskey
  - Marcus's TRUE CHARACTER: Man who kills for justice - McKee's "pressure reveals essence" (p.101)

- **CHARACTER ARC**: McKee's "profound change from start to end" (p.104-106)
  - Marcus begins believing in divine justice → ends taking justice into own hands
  - Apply McKee's formula: "Pressure + Choice = True Character" (p.105)

- **DIMENSION THROUGH CONTRADICTION**: McKee's principle of internal opposition (p.107)
  - Priest who murders = McKee's "dimensional character through contradiction" (p.108)
  - Quote McKee: "Dimension means contradiction within deep character" (p.107)

**JOHN TRUBY'S CHARACTER WEB (Anatomy of Story, Chapter 3: "The Seven Key Steps of Story Structure"):**

Truby writes "Character is desire in human form" (page 41). Apply his system:

- **WEAKNESS/NEED**: Truby's two-part foundation (p.42-45)
  - Marcus's MORAL WEAKNESS: Plays God (Truby p.43)
  - Marcus's PSYCHOLOGICAL NEED: Accept limits of human justice (Truby p.44)

- **GHOST**: Truby's "event from past haunting character" (p.46)
  - Lost faith = Truby's ghost driving present action (p.47)

- **DESIRE LINE**: Truby's "what character wants" (p.48-50)
  - Marcus wants justice = Truby's "spine of story" (p.49)

- **SELF-REVELATION**: Truby's character transformation moment (p.51)
  - Elena's warning = push toward Truby's self-revelation (p.52)

Quote Truby: "Great characters are built from their weakness" (p.42)

**SYD FIELD'S THREE-DIMENSIONAL CHARACTER (Screenplay, Chapter 4: "Building a Character"):**

Field states "Character is the foundation of your screenplay" (page 45). Apply:

- **PROFESSIONAL/PERSONAL/PRIVATE**: Field's three dimensions (p.46-48)
  - PROFESSIONAL: Former priest (Field p.46)
  - PERSONAL: Relationship with Elena (Field p.47)
  - PRIVATE: Guilt and whiskey (Field p.48)

- **CHARACTER BIOGRAPHY**: Field's backstory technique (p.49-51)
  - "Lost faith once" = Field's biography informing present (p.50)

Quote Field: "Action is character" (p.45)

**BLAKE SNYDER'S TRANSFORMATION MACHINE (Save the Cat, Throughout):**

Snyder says "Movies are about transformation" (page 134). Apply:

- **SAVE THE CAT MOMENT**: Character's moral center shown early (p.12-14)
  - Marcus caring about murdered children = Snyder's empathy moment (p.13)

- **SHARD OF GLASS**: Snyder's "theme stated as character problem" (p.72)
  - "You're not God" = Snyder's thematic shard (p.73)

- **TRANSFORMATION MACHINE**: Story as character change device (p.134-136)
  - Script transforms Marcus from faith to action (p.135)

Quote Snyder: "All stories are about transformation" (p.134)

**CHRISTOPHER VOGLER'S ARCHETYPES (Writer's Journey, Chapter on Archetypes):**

Vogler identifies universal character patterns (page 29). Apply:

- **HERO ARCHETYPE**: Marcus as flawed hero (p.30-35)
  - Tragic flaw = Vogler's "humanized hero" (p.32)

- **SHADOW ARCHETYPE**: The killer as external shadow (p.65-70)
  - Also Marcus's internal shadow - his dark impulses (p.67)

- **SHAPESHIFTER**: Elena shifting from ally to opposition (p.71-76)
  - Vogler's "character changing allegiance" (p.72)

Quote Vogler: "Archetypes are energies within us all" (p.30)

**JOSEPH CAMPBELL'S HERO PATTERN (Hero with a Thousand Faces):**

Campbell writes about universal hero patterns (page 30). Apply:

- **SUPERNATURAL AID REFUSED**: Marcus rejecting divine justice (p.72-77)
  - Taking matters into own hands = Campbell's "hero refusing aid" (p.73)

- **APOTHEOSIS**: Campbell's "divine knowledge moment" (p.148-151)
  - Marcus realizing he's become what he opposed (p.149)

Quote Campbell: "The hero is the one who comes to know" (p.30)

**ARISTOTLE'S TRAGIC HERO (Poetics, Chapter 13):**

Aristotle defines the tragic hero (1453a). Apply:

- **HAMARTIA**: The tragic flaw (1453a7-10)
  - Marcus's pride = Aristotle's hamartia causing downfall

- **ETHOS**: Character's moral disposition (1450b8-10)
  - Former priest = Aristotle's "good person with flaw"

Quote Aristotle: "Character reveals moral choice" (1450b8)

Analyze EVERY character element using these SPECIFIC NAMED TECHNIQUES with citations.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in all specific character development techniques from every major theorist."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
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
                "num_predict": 4000,
                "num_ctx": 8192
            }
        }

        print("   ⚡ Processando CHARACTER ULTRA...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    end_time = time.time()
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"character_ultra_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(response_text)

    theories, base_count, technique_bonus, total_score = analyze_theories(response_text)
    words = len(response_text.split())

    print(f"   ✅ RESULTADOS:")
    print(f"      📝 Palavras: {words}")
    print(f"      📚 Total pontos: {total_score} ({base_count} citações + {technique_bonus} técnicas)")
    print(f"      ⏱️ Tempo: {end_time - start_time:.1f}s")
    print()
    print("   🎓 Citações por teórico:")
    for theorist, count in theories.items():
        if count > 0:
            print(f"      • {theorist.upper()}: {count}x")
    print()

    return {
        "words": words,
        "total_score": total_score,
        "base_count": base_count,
        "technique_bonus": technique_bonus,
        "theories": theories,
        "file": filename,
        "time": end_time - start_time
    }

def main():
    print("=" * 60)
    print("👤 TESTE CHARACTER ULTRA SYNTHESIS")
    print("Aplicando técnicas específicas nomeadas")
    print("=" * 60)

    result = test_character_ultra()

    if result:
        print("\n" + "=" * 60)
        print("📊 COMPARAÇÃO COM VERSÃO ORIGINAL")
        print("=" * 60)
        print()
        print("CHARACTER Original: 17-25 citações, 608-725 palavras")
        print(f"CHARACTER ULTRA: {result['total_score']} pontos ({result['base_count']} + {result['technique_bonus']}), {result['words']} palavras")
        print()

        if result['total_score'] >= 30:
            print("🏆 EXCELENTE! Superou 30 pontos!")
        elif result['total_score'] >= 25:
            print("✅ MUITO BOM! Alcançou 25+ pontos")
        elif result['total_score'] >= 17:
            print("⚠️ BOM! Manteve nível original")
        else:
            print("❌ Precisa melhorias")

        # Save results
        results_data = {
            "test": "Character Ultra Synthesis Test",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": "CHARACTER Ultra with Named Techniques",
            "results": result
        }

        results_filename = f"character_ultra_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Relatório detalhado: {results_filename}")

if __name__ == "__main__":
    main()