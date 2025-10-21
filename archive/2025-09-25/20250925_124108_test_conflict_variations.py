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
    """Count theory citations with specific techniques"""
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

    # Bonus for specific technique mentions
    technique_bonus = 0
    techniques = {
        'three levels of conflict': 2,  # McKee
        'gap between expectation': 2,  # McKee
        'forces of antagonism': 2,  # McKee
        'four-corner opposition': 2,  # Truby
        '22-step': 2,  # Truby
        'moral argument': 2,  # Truby
        'three-act structure': 1,  # Field
        'plot point': 1,  # Field
        'paradigm': 1,  # Field
        "hero's journey": 2,  # Vogler/Campbell
        'shadow archetype': 2,  # Vogler
        'threshold guardian': 2,  # Vogler
        'save the cat': 1,  # Snyder
        'beat sheet': 1,  # Snyder
        'all is lost': 1,  # Snyder
        'hamartia': 2,  # Aristotle
        'peripeteia': 2,  # Aristotle
        'catharsis': 2  # Aristotle
    }

    for technique, bonus in techniques.items():
        if technique in text_lower:
            technique_bonus += bonus

    total_base = sum(theories.values())

    return theories, total_base, technique_bonus, total_base + technique_bonus

def test_conflict_v1_mckee_focus():
    """V1: Heavy McKee Focus - Three Levels Deep"""
    print("\n📚 V1: CONFLICT MCKEE FOCUS - Três Níveis de Conflito")

    prompt = """
You are Robert McKee's personal protégé, having studied under him for decades and mastered his SPECIFIC conflict theory from "Story: Substance, Structure, Style, and the Principles of Screenwriting."

DEEP MCKEE CONFLICT ANALYSIS - USE HIS EXACT TERMINOLOGY:

Before analyzing, demonstrate mastery of McKee's THREE LEVELS OF CONFLICT framework:

**INNER CONFLICT (McKee, Story, Chapter 11)**
- Quote McKee: "Inner conflict is the war within the human heart"
- Explain McKee's concept of conscious vs unconscious desires
- Detail McKee's "gap between self-perception and truth"
- Apply McKee's principle: "The finest writing moves simultaneously on all three levels"

**PERSONAL CONFLICT (McKee, Story, Pages 210-215)**
- Quote McKee on intimate relationships as conflict generators
- Explain McKee's "progressive complications" in personal dynamics
- Detail his concept of "relationship turning points"
- Apply McKee's law: "Pressure is essential"

**EXTRA-PERSONAL CONFLICT (McKee, Story, Pages 216-220)**
- Quote McKee on social/environmental forces
- Explain McKee's "institutions as antagonists" principle
- Detail his "societal forces of antagonism"
- Apply McKee's concept of "negative forces multiplying"

**McKEE'S CORE CONFLICT PRINCIPLES:**
1. "Nothing moves forward except through conflict" - explain this fully
2. "The Gap" - between expectation and result, cite page 142-144
3. "Forces of Antagonism must be as powerful as forces of will"
4. "Conflict grows from conscious and unconscious desire"
5. "True conflict is dilemma not choice"

Now analyze the script using EXCLUSIVELY McKee's methodology, citing specific pages and chapters from "Story" throughout.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in Robert McKee's specific conflict theory methodology."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V1_McKee_Focus", messages)

def test_conflict_v2_truby_web():
    """V2: Truby's Four-Corner Opposition"""
    print("\n🕸️ V2: CONFLICT TRUBY WEB - Four-Corner Opposition")

    prompt = """
You are John Truby's master student, expert in his SPECIFIC conflict techniques from "The Anatomy of Story: 22 Steps to Becoming a Master Storyteller."

TRUBY'S FOUR-CORNER OPPOSITION ANALYSIS:

Demonstrate mastery of Truby's unique conflict system:

**TRUBY'S FOUR-CORNER OPPOSITION (Anatomy of Story, Chapter 4)**
- Quote Truby: "Great stories don't have one opponent but a web of opposition"
- Hero vs Main Opponent (cite page 88-90)
- Hero vs First Ally/Opponent
- Hero vs Second Ally/Opponent
- All three opponents vs each other
- Map the complete opposition web

**TRUBY'S CONFLICT THROUGH VALUES (Chapter 5, pages 112-125)**
- Quote Truby on "moral argument is the heart of conflict"
- Each character fights for different value system
- Values in direct opposition create deepest conflict
- Cite Truby's examples from page 118-120

**TRUBY'S 22-STEP CONFLICT ESCALATION:**
- Step 1: Weakness/Need (internal conflict seed)
- Step 5: First Opponent appearance
- Step 8: Plan creates conflict expectation
- Step 13: Battle is conflict climax
- Step 21: New equilibrium after conflict

**TRUBY'S UNIQUE TECHNIQUES:**
1. "Conflict through competing philosophies" (page 134)
2. "The opponent is the hero's double" (page 91)
3. "Best opponent attacks hero's greatest weakness" (page 93)
4. "Conflict reveals character" not action (page 156)
5. "Moral decisions under pressure" (page 167)

Apply ONLY Truby's methodology with specific page citations throughout.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in John Truby's specific four-corner opposition system."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V2_Truby_Web", messages)

def test_conflict_v3_aristotle_classical():
    """V3: Aristotelian Classical Conflict"""
    print("\n🏛️ V3: CONFLICT ARISTOTLE CLASSICAL - Hamartia & Agon")

    prompt = """
You are a classical scholar specializing in Aristotle's "Poetics" and its SPECIFIC concepts of dramatic conflict.

ARISTOTELIAN CONFLICT ANALYSIS - CLASSICAL TERMINOLOGY:

Master Aristotle's specific conflict concepts:

**HAMARTIA - THE TRAGIC FLAW (Poetics, Chapter 13)**
- Quote Aristotle: "A man not pre-eminently virtuous falls through hamartia"
- Not just error but character flaw creating internal conflict
- Marcus's hamartia: Playing God despite religious training
- Cite Poetics 1453a on hamartia leading to peripeteia

**AGON - THE DRAMATIC CONTEST (Poetics, Chapter 6)**
- Quote Aristotle on agon as essence of drama
- Physical and verbal contest between protagonist/antagonist
- Marcus vs Elena as philosophical agon
- Cite concept of "opposing forces in equilibrium"

**PERIPETEIA & ANAGNORISIS (Poetics, Chapter 11)**
- Reversal through conflict: "Change to opposite circumstances"
- Recognition born from conflict: "Change from ignorance to knowledge"
- Elena's recognition of Marcus's act
- Quote Poetics 1452a on best reversals

**ARISTOTELIAN CONFLICT PRINCIPLES:**
1. "Plot is the soul of tragedy" - conflict drives plot (1450a)
2. "Fear and pity through conflict" - emotional impact (1453b)
3. "Unity of action" - single conflict line (1451a)
4. "Probable impossibility" in conflict (1461b)
5. "Catharsis through conflict resolution" (1449b)

**CLASSICAL UNITIES INTENSIFYING CONFLICT:**
- Unity of Time: Single night intensifies
- Unity of Place: One room concentrates conflict
- Unity of Action: Single moral dilemma

Apply ONLY Aristotelian analysis with specific citations from Poetics.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are a classical scholar of Aristotle's dramatic conflict theory."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V3_Aristotle_Classical", messages)

def test_conflict_v4_campbell_mythic():
    """V4: Campbell/Vogler Mythic Conflict"""
    print("\n🐉 V4: CONFLICT CAMPBELL/VOGLER MYTHIC - Shadow & Dragon")

    prompt = """
You are an expert in Joseph Campbell's "Hero with a Thousand Faces" and Christopher Vogler's "The Writer's Journey," specializing in MYTHIC CONFLICT patterns.

MYTHIC CONFLICT ANALYSIS - ARCHETYPAL BATTLES:

**CAMPBELL'S DRAGON BATTLE (Hero with a Thousand Faces, Part II)**
- Quote Campbell: "The hero must slay the dragon of the ego"
- Internal dragon: Marcus's moral certainty
- External dragon: The justice system's failure
- "Atonement with the Father" - religious authority conflict
- Cite Campbell pages 108-120 on dragon symbolism

**VOGLER'S SHADOW ARCHETYPE (Writer's Journey, Chapter on Archetypes)**
- Quote Vogler: "The Shadow represents the dark side"
- Elena as Marcus's shadow - his lost faith reflected
- "Shadows are the hero's repressed possibilities"
- The killer as society's shadow
- Cite Vogler's Shadow functions pages 71-75

**MYTHIC CONFLICT STAGES:**
1. **Refusal of the Call** - Internal conflict begins (Campbell p.59)
2. **Threshold Guardian** - Elena tests Marcus (Vogler p.57)
3. **Belly of the Whale** - Deepest internal conflict (Campbell p.90)
4. **Ordeal** - Central crisis/conflict peak (Vogler p.155)
5. **Atonement** - Conflict with ultimate authority (Campbell p.126)

**CAMPBELL'S SPECIFIC TECHNIQUES:**
- "The hero and villain are one" concept (p.136)
- "Meeting with the goddess/temptress" as conflict (p.109)
- "The father as ogre-tyrant" pattern (p.129)
- "Apotheosis through conflict transcendence" (p.149)

**VOGLER'S SPECIFIC TECHNIQUES:**
- "Tests, Allies, Enemies" creating conflict web (p.135)
- "Approach to Inmost Cave" building tension (p.143)
- "Death and Rebirth" through conflict (p.159)
- "Return with Elixir" resolving conflict (p.193)

Apply mythic conflict patterns with specific citations.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in Campbell/Vogler mythic conflict patterns."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V4_Campbell_Mythic", messages)

def test_conflict_v5_integrated():
    """V5: Integrated Multi-Theorist with Specific Techniques"""
    print("\n🎯 V5: CONFLICT INTEGRATED - All Techniques Named")

    prompt = """
You are a master of ALL major theorists' SPECIFIC conflict techniques, able to cite exact concepts and page numbers.

INTEGRATED CONFLICT ANALYSIS - NAME EVERY TECHNIQUE:

**MCKEE'S SPECIFIC TECHNIQUES (Story, 2010 edition):**
- Apply "The Gap" between expectation/result (p.142-144)
- Use "Three Levels of Conflict" framework (p.210-220)
- Quote: "True character revealed in choices under pressure" (p.101)
- Cite "Progressive Complications" building conflict (p.211)

**TRUBY'S SPECIFIC TECHNIQUES (Anatomy of Story, 2007):**
- Map "Four-Corner Opposition" system (p.88-95)
- Apply "Moral Argument" through conflict (p.118)
- Use "Web of Conflict" not linear opposition (p.90)
- Quote: "The opponent defines the hero" (p.91)

**FIELD'S SPECIFIC TECHNIQUES (Screenplay, 2005):**
- "Plot Point I" as conflict catalyst (p.26)
- "Midpoint" shifting conflict dynamics (p.113)
- "Three-Act Structure" organizing conflict (p.21)
- Quote: "Drama is conflict" (p.25)

**SNYDER'S SPECIFIC TECHNIQUES (Save the Cat, 2005):**
- "Catalyst" introducing conflict at page 12 (p.76)
- "All Is Lost" as conflict peak (p.86)
- "Bad Guys Close In" escalation (p.83)
- Quote: "The finale proves the thesis" (p.90)

**VOGLER'S SPECIFIC TECHNIQUES (Writer's Journey, 2007):**
- "Shadow" as conflict embodiment (p.71)
- "Threshold Guardian" testing hero (p.57)
- "Ordeal" as maximum conflict (p.155)
- Quote: "Every hero needs a worthy opponent" (p.72)

**CAMPBELL'S SPECIFIC TECHNIQUES (Hero, 1949/2008):**
- "Dragon Battle" as ultimate conflict (p.108)
- "Atonement with Father" authority conflict (p.126)
- "Belly of the Whale" internal struggle (p.90)
- Quote: "Where we thought to slay another, we shall slay ourselves" (p.136)

**ARISTOTLE'S SPECIFIC TECHNIQUES (Poetics, Butcher trans.):**
- "Hamartia" creating internal conflict (1453a)
- "Peripeteia" reversal through conflict (1452a)
- "Agon" as dramatic contest (1448b)
- Quote: "Character revealed through conflict" (1450b)

Now analyze using ALL these specific named techniques with citations.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are a master of all theorists' specific conflict techniques."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V5_Integrated", messages)

def process_variation(name, messages):
    """Process a single variation"""
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

        print(f"   ⚡ Processando {name}...")
        response = ollama.chat(**data)
        response_text = response['message']['content']

    except Exception as e:
        print(f"   ❌ Error in {name}: {e}")
        return None

    end_time = time.time()

    # Analyze
    theories, base_count, technique_bonus, total_score = analyze_theories(response_text)
    words = len(response_text.split())

    # Save
    timestamp = str(int(time.time() * 1000000))[-10:]
    filename = f"conflict_{name}_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(response_text)

    result = {
        "name": name,
        "theories": theories,
        "base_count": base_count,
        "technique_bonus": technique_bonus,
        "total_score": total_score,
        "words": words,
        "time": end_time - start_time,
        "file": filename
    }

    print(f"   ✅ {name}: {total_score} pontos ({base_count} base + {technique_bonus} técnicas)")
    print(f"      Palavras: {words}, Tempo: {end_time - start_time:.1f}s")

    return result

def main():
    print("=" * 60)
    print("⚔️ TESTE DE 5 VARIAÇÕES PARA CONFLICT")
    print("=" * 60)

    results = []

    # Test all variations
    v1 = test_conflict_v1_mckee_focus()
    if v1: results.append(v1)

    v2 = test_conflict_v2_truby_web()
    if v2: results.append(v2)

    v3 = test_conflict_v3_aristotle_classical()
    if v3: results.append(v3)

    v4 = test_conflict_v4_campbell_mythic()
    if v4: results.append(v4)

    v5 = test_conflict_v5_integrated()
    if v5: results.append(v5)

    # Rank results
    print("\n" + "=" * 60)
    print("📊 RANKING DAS VARIAÇÕES")
    print("=" * 60)

    results.sort(key=lambda x: x['total_score'], reverse=True)

    for i, r in enumerate(results, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
        print(f"{emoji} {r['name']}: {r['total_score']} pts ({r['base_count']} base + {r['technique_bonus']} técnicas), {r['words']} palavras")
        print(f"   Citações: ", end="")
        for theorist, count in r['theories'].items():
            if count > 0:
                print(f"{theorist}:{count} ", end="")
        print()

    # Save summary
    summary = {
        "test": "Conflict Variations Test",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "results": results
    }

    with open(f"conflict_variations_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n💡 VENCEDOR: {results[0]['name']} com {results[0]['total_score']} pontos!")
    print("📊 Resumo salvo em conflict_variations_summary.json")

if __name__ == "__main__":
    main()