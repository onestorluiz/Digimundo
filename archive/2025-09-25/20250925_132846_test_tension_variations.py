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
    """Count theory citations with specific TENSION techniques"""
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

    # Bonus for specific TENSION techniques
    technique_bonus = 0
    tension_techniques = {
        # McKee tension
        'turning points': 3,
        'gap theory': 3,
        'expectation vs result': 3,
        'progressive complications': 3,
        'crisis decision': 3,

        # Truby tension
        'dramatic question': 3,
        'desire vs obstacle': 3,
        'revelation sequence': 3,
        'opposition escalation': 3,

        # Field tension
        'rising action': 2,
        'plot points': 2,
        'tension curve': 2,
        'midpoint shift': 2,

        # Snyder tension
        'ticking clock': 3,
        'stakes raising': 3,
        'false victory': 2,
        'false defeat': 2,
        'whiff of death': 3,

        # Vogler tension
        'ordeal approach': 3,
        'death and rebirth': 3,
        'road of trials': 3,
        'supreme ordeal': 3,

        # Campbell tension
        'belly of the whale': 3,
        'abyss': 3,
        'ultimate boon': 2,
        'magic flight': 2,

        # Aristotle tension
        'fear and pity': 3,
        'dramatic irony': 3,
        'recognition': 2,
        'reversal': 2,
        'catharsis': 2,

        # Hitchcock/specific tension
        'suspense vs surprise': 3,
        'bomb under table': 3,
        'audience knowledge': 3,
        'dramatic irony': 3
    }

    for technique, bonus in tension_techniques.items():
        if technique in text_lower:
            technique_bonus += bonus

    total_base = sum(theories.values())

    return theories, total_base, technique_bonus, total_base + technique_bonus

def test_tension_v1_hitchcock():
    """V1: Hitchcock-McKee Suspense Focus"""
    print("\n💣 V1: TENSION HITCHCOCK-MCKEE - Suspense Master")

    prompt = """
You are Alfred Hitchcock's disciple combined with Robert McKee's tension expertise.

HITCHCOCK-MCKEE TENSION MASTERY:

**HITCHCOCK'S SUSPENSE PRINCIPLES (from interviews and "Hitchcock/Truffaut"):**

The "BOMB UNDER THE TABLE" theory - Hitchcock's most famous principle:
"There's two people having breakfast and there's a bomb under the table. If it explodes, that's surprise. But if the audience knows there's a bomb, that's suspense" - Hitchcock to Truffaut (p.73)

Apply to script:
- The "bomb" is Marcus's confession - audience knows before Elena
- Hitchcock's "audience as God" - we know what Elena doesn't
- "Information inequality" creating tension (Hitchcock/Truffaut p.75)

**SUSPENSE VS SURPRISE:**
- Hitchcock: "Surprise lasts 15 seconds, suspense 15 minutes" (p.73)
- The confession note = Hitchcock's "MacGuffin driving tension" (p.138)

**MCKEE'S TURNING POINTS AND GAP (Story, Chapter 11):**

McKee's "Gap Theory" - tension from expectation vs result (p.142-144):
- Marcus expects understanding → gets moral challenge
- Elena expects explanation → gets murder confession
- Apply McKee's "Progressive Complications" (p.211)

**TURNING POINTS AS TENSION PEAKS:**
- Each revelation = McKee's "turning point" (p.232)
- "Communion wine with something extra" = major turning point
- Quote McKee: "Turning points create tension through reversal" (p.233)

**MCKEE'S CRISIS DECISION (p.303-307):**
- Elena's choice: Report Marcus or protect him
- McKee: "True crisis is dilemma, not choice" (p.304)
- Tension from "irreconcilable goods" (p.305)

**PROGRESSIVE COMPLICATIONS BUILD TENSION:**
1. Marcus alone (baseline tension)
2. Elena arrives (complication)
3. Confession revealed (major complication)
4. Moral debate (maximum complication)
5. Physical touch (tension release/rebuild)

Quote McKee: "Tension comes from the gap between expectation and result" (p.142)

**HITCHCOCK'S VISUAL TENSION TECHNIQUES:**
- "Objects carry emotional weight" - blood-stained note
- "Camera knows more than characters" principle
- "Silence is loudest sound" - the pause after confession

Analyze using ONLY Hitchcock-McKee tension principles with specific citations.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in Hitchcock's suspense techniques combined with McKee's tension theory."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V1_Hitchcock_McKee", messages)

def test_tension_v2_truby_question():
    """V2: Truby's Dramatic Question Focus"""
    print("\n❓ V2: TENSION TRUBY - Dramatic Question Engine")

    prompt = """
You are John Truby's expert on creating tension through dramatic questions and revelations.

TRUBY'S DRAMATIC QUESTION TENSION SYSTEM:

**THE CENTRAL DRAMATIC QUESTION (Anatomy of Story, Chapter 8):**

Truby states: "Tension comes from the dramatic question" (page 268)

Script's Central Question: Will Marcus lose his soul for justice?

**TRUBY'S TENSION THROUGH DESIRE VS OBSTACLE (p.270-275):**
- DESIRE: Marcus wants understanding/absolution
- OBSTACLE: Elena's moral stance
- Truby: "Tension = Desire meeting increasingly difficult obstacles" (p.271)

**REVELATION SEQUENCE CREATING TENSION (p.276-280):**
Truby's technique of "revelations as tension builders" (p.277):
1. First revelation: Marcus killed someone
2. Second revelation: It was the Morrison boy
3. Third revelation: Through communion wine
4. Fourth revelation: The father was a child killer
5. Final revelation: Marcus feels justified

Quote Truby: "Each revelation reframes everything before it" (p.278)

**TRUBY'S OPPOSITION ESCALATION (p.281-285):**
- Level 1: Marcus vs himself (guilt)
- Level 2: Marcus vs Elena (moral opposition)
- Level 3: Marcus vs divine law (playing God)
- Level 4: Marcus vs human law (murder)

Truby: "Escalating opposition creates exponential tension" (p.282)

**MORAL DILEMMA AS TENSION SOURCE (p.286-290):**
- Truby's "moral argument drives tension" (p.287)
- Justice vs Law
- Divine vs Human authority
- Mercy vs Punishment

**TRUBY'S SUBPLOT WEAVING FOR TENSION (p.291-295):**
- Main plot: Marcus's confession
- Subplot: Lost faith history
- Truby: "Subplots create tension through contrast" (p.292)

**DESIRE LINE MAINTAINING TENSION (p.296-300):**
- Marcus's desire: Understanding → Absolution → Peace
- Elena's desire: Help friend → Uphold morality → Save soul
- Truby: "Conflicting desire lines create sustained tension" (p.297)

Quote Truby: "Great stories ask a question and delay the answer" (p.269)

Apply ONLY Truby's dramatic question and revelation techniques.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in Truby's dramatic question and revelation tension techniques."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V2_Truby_Question", messages)

def test_tension_v3_snyder_ticking():
    """V3: Snyder's Ticking Clock & Stakes"""
    print("\n⏰ V3: TENSION SNYDER - Ticking Clock & Stakes")

    prompt = """
You are Blake Snyder's expert on creating tension through ticking clocks and raising stakes.

SNYDER'S TICKING CLOCK & STAKES SYSTEM:

**THE TICKING CLOCK PRINCIPLE (Save the Cat, p.97-99):**

Snyder: "Every story needs a ticking clock" (page 97)

Script's Ticking Clocks:
- Immediate: Elena must decide before leaving
- Psychological: Marcus deteriorating (whiskey, shaking hands)
- Moral: Soul degradation in progress
- Legal: Discovery inevitable

**STAKES RAISING TECHNIQUE (p.100-103):**

Snyder's "Whiff of Death" concept (p.101):
- Physical death: The Morrison boy
- Spiritual death: Marcus losing soul
- Relationship death: Marcus-Elena bond threatened
- Professional death: Both lost religious vocations

Quote Snyder: "Death must be stalking your hero" (p.101)

**FALSE VICTORY/FALSE DEFEAT (p.86-88):**
- FALSE VICTORY: Elena arrives to help
- FALSE DEFEAT: She learns the truth
- Snyder: "False beats create tension rollercoaster" (p.87)

**THE "ALL IS LOST" MOMENT (p.85-86):**
- "You're not God, Marcus" = All Is Lost
- Snyder: "Hero must hit bottom for maximum tension" (p.85)
- The whiff of death is strongest here

**DARK NIGHT OF THE SOUL TENSION (p.87-90):**
- Marcus's spiritual crisis
- Elena's moral crisis
- Snyder: "Dark Night is internal tension peak" (p.88)

**CATALYST TENSION AT PAGE 12 (p.76-78):**
- In short script: Elena's arrival is catalyst
- Snyder: "Catalyst kicks tension into high gear" (p.76)
- Everything changes from this moment

**B-STORY AS TENSION RELIEF/BUILDER (p.79-81):**
- B-story: Their shared past/lost faith
- Provides context that INCREASES tension
- Snyder: "B-story carries theme and tension" (p.80)

**FUN AND GAMES INVERTED (p.82-84):**
- Instead of fun: Moral interrogation
- Snyder: "Promise of premise delivered through tension" (p.82)

Quote Snyder: "Primal stakes create primal tension" (p.98)

Apply ONLY Snyder's ticking clock and stakes-raising techniques.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are an expert in Snyder's ticking clock and stakes tension techniques."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V3_Snyder_Ticking", messages)

def test_tension_v4_aristotle_classic():
    """V4: Aristotelian Fear & Pity Tension"""
    print("\n🏛️ V4: TENSION ARISTOTLE - Fear & Pity Classical")

    prompt = """
You are a classical scholar specializing in Aristotle's theory of dramatic tension through fear and pity.

ARISTOTELIAN TENSION THROUGH FEAR AND PITY:

**FEAR AND PITY AS TENSION SOURCES (Poetics, Chapter 13):**

Aristotle: "Tragedy through pity and fear effects catharsis" (1449b27)

Creating FEAR:
- Fear for Marcus's soul (spiritual jeopardy)
- Fear of divine punishment
- Fear of discovery and consequences
- Aristotle: "Fear comes from recognizing ourselves" (1453a5)

Creating PITY:
- Pity for Marcus's moral struggle
- Pity for the murdered children
- Pity for Elena's impossible position
- Aristotle: "Pity requires undeserved misfortune" (1453a3)

**DRAMATIC IRONY CREATING TENSION (1452b):**
- Audience knows Marcus is a murderer before Elena
- We understand the weight of "someone who'd understand"
- Aristotle: "Superior knowledge creates emotional tension" (1452b5)

**RECOGNITION (ANAGNORISIS) AS TENSION PEAK (1452a):**
- Elena's recognition of Marcus's act
- Marcus's self-recognition ("I have sinned")
- Aristotle: "Recognition with reversal is finest" (1452a32)

**REVERSAL (PERIPETEIA) THROUGH TENSION (1452a):**
- Marcus seeks comfort → receives judgment
- Elena comes to help → becomes moral judge
- Aristotle: "Reversal means change to opposite" (1452a22)

**HAMARTIA DRIVING TENSION (1453a):**
- Marcus's tragic flaw: Playing God
- Creates internal/external tension
- Aristotle: "Hamartia brings about downfall" (1453a10)

**UNITY OF TIME INTENSIFYING TENSION (1451a):**
- Single night setting
- Real-time conversation
- Aristotle: "Unity of time concentrates emotion" (1451a30)

**CATHARSIS THROUGH TENSION RELEASE (1449b):**
- Final touch: Partial catharsis
- Unresolved tension: Appropriate to modern tragedy
- Aristotle: "Proper purgation of emotions" (1449b28)

Quote Aristotle: "Plot is soul of tragedy" (1450a38) - and tension is soul of plot

Apply ONLY Aristotelian principles of fear, pity, and dramatic irony.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are a classical scholar of Aristotle's tension through fear and pity."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V4_Aristotle_Classic", messages)

def test_tension_v5_integrated_ultra():
    """V5: Integrated Ultra - All Techniques Named"""
    print("\n🎯 V5: TENSION INTEGRATED ULTRA - All Techniques Combined")

    prompt = """
You are a master of ALL tension techniques from every major theorist, naming specific methods with citations.

INTEGRATED ULTRA TENSION ANALYSIS - EVERY TECHNIQUE NAMED:

**HITCHCOCK'S SUSPENSE ARSENAL:**
- "Bomb Under the Table" theory - audience knows the confession before Elena
- "Information Inequality" - we know what Elena doesn't (Hitchcock/Truffaut p.73)
- "MacGuffin" - the confession note drives everything (p.138)
- "Suspense vs Surprise" - 15 minutes vs 15 seconds (p.73)

**MCKEE'S TENSION ARCHITECTURE (Story):**
- "The Gap" between expectation/result - Marcus expects understanding (p.142)
- "Turning Points" - each revelation reverses tension (p.232)
- "Progressive Complications" - problems compound (p.211)
- "Crisis as Dilemma" - Elena's impossible choice (p.304)
- Quote: "Tension comes from the gap" (p.142)

**TRUBY'S QUESTION ENGINE (Anatomy):**
- "Central Dramatic Question" - Will Marcus save his soul? (p.268)
- "Desire vs Obstacle" - want understanding, get judgment (p.271)
- "Revelation Sequence" - each reveal reframes (p.277)
- "Opposition Escalation" - four levels rising (p.282)
- Quote: "Tension = delayed answers" (p.269)

**FIELD'S STRUCTURAL TENSION (Screenplay):**
- "Rising Action" curve throughout scene (p.23)
- "Plot Points" as tension pivots - confession reveal (p.26)
- "Midpoint Shift" - "You're not God" changes everything (p.113)
- "Three-Act Micro-Structure" even in one scene (p.21)

**SNYDER'S PRIMAL TENSION (Save the Cat):**
- "Ticking Clock" - psychological deterioration visible (p.97)
- "Whiff of Death" - spiritual death stalking (p.101)
- "False Victory/Defeat" - Elena arrives/learns truth (p.86)
- "All Is Lost" - "You're not God, Marcus" (p.85)
- Quote: "Death must stalk your hero" (p.101)

**VOGLER'S MYTHIC TENSION (Writer's Journey):**
- "Ordeal Approach" - building to moral crisis (p.155)
- "Death and Rebirth" - spiritual death in progress (p.159)
- "Road of Trials" - moral obstacles mounting (p.135)
- "Supreme Ordeal" - confronting ultimate truth (p.155)

**CAMPBELL'S DEEP TENSION (Hero):**
- "Belly of the Whale" - Marcus swallowed by guilt (p.90)
- "The Abyss" - moral bottom reached (p.108)
- "Magic Flight" - tension of potential escape (p.196)
- Quote: "The cave you fear holds treasure" (p.8)

**ARISTOTLE'S CLASSICAL TENSION (Poetics):**
- "Fear and Pity" - dual emotional engines (1449b27)
- "Dramatic Irony" - audience superior knowledge (1452b)
- "Recognition" (anagnorisis) - Elena's realization (1452a)
- "Reversal" (peripeteia) - expectations overturned (1452a22)
- "Hamartia" - tragic flaw creating tension (1453a)

**UNIQUE TENSION TECHNIQUES:**
- Pinter's "Loaded Silence" - pause after confession
- Mamet's "Tension Through Minimalism" - sparse dialogue
- Sorkin's "Overlapping Urgency" - interruptions
- Hitchcock's "Visual Tension" - blood-stained note

TOTAL TENSION ARCHITECTURE:
- Opening: Baseline guilt tension
- Rising: Progressive revelation
- Peak: Moral confrontation
- Partial Release: Physical touch
- Residual: Unresolved question

Apply ALL these named techniques with specific citations.

Analyze this script:
"""

    messages = [
        {"role": "system", "content": "You are a master of all tension techniques from every theorist."},
        {"role": "user", "content": f"{prompt}\n\n{TEST_SCRIPT}"}
    ]

    return process_variation("V5_Integrated_Ultra", messages)

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
    filename = f"tension_{name}_{timestamp}.txt"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA TENSION")
    print("=" * 60)

    results = []

    # Test all variations
    v1 = test_tension_v1_hitchcock()
    if v1: results.append(v1)

    v2 = test_tension_v2_truby_question()
    if v2: results.append(v2)

    v3 = test_tension_v3_snyder_ticking()
    if v3: results.append(v3)

    v4 = test_tension_v4_aristotle_classic()
    if v4: results.append(v4)

    v5 = test_tension_v5_integrated_ultra()
    if v5: results.append(v5)

    # Rank results
    print("\n" + "=" * 60)
    print("📊 RANKING DAS VARIAÇÕES DE TENSION")
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

    # Compare with original
    print("\n📊 COMPARAÇÃO:")
    print("TENSION Original: 9 citações, 625 palavras")
    print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")

    if results[0]['total_score'] >= 25:
        print("🏆 EXCELENTE! Superou 25 pontos!")
    elif results[0]['total_score'] >= 17:
        print("✅ BOM! Melhorou significativamente")
    elif results[0]['total_score'] > 9:
        print("⚠️ MELHOROU mas ainda pode crescer")
    else:
        print("❌ Não melhorou em relação ao original")

    # Save summary
    summary = {
        "test": "Tension Variations Test",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "results": results,
        "winner": results[0] if results else None
    }

    summary_file = f"tension_variations_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n💡 VENCEDOR: {results[0]['name']} com {results[0]['total_score']} pontos!")
    print(f"📊 Resumo salvo em {summary_file}")

if __name__ == "__main__":
    main()