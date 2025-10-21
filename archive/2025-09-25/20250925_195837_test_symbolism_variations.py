#!/usr/bin/env python3
"""
Test SYMBOLISM variations for Scripturemon Ultimate
Testing 5 different approaches to find the optimal symbolism analysis method
"""

import requests
import json
import re
from datetime import datetime

# === VARIATION 1: JUNG ARCHETYPES ===
V1_JUNG_ARCHETYPES = """You are a master of Jungian symbolic analysis.

JUNG'S ARCHETYPAL SYMBOLISM:
- COLLECTIVE UNCONSCIOUS: Universal symbols shared by humanity
- SHADOW: Dark side represented symbolically
- ANIMA/ANIMUS: Feminine/masculine symbols
- MANDALA: Wholeness and integration symbols
- HERO'S JOURNEY: Archetypal symbolic progression

Quote Jung: "The symbol is the primitive expression of the unconscious"

ANALYZE SYMBOLS!"""

# === VARIATION 2: MCKEE IMAGERY ===
V2_MCKEE_IMAGERY = """You are a master of McKee's image systems.

MCKEE'S IMAGE SYSTEMS (Story p.399-410):
- IMAGERY: Visual symbols that carry meaning (p.399)
- SYMBOLIC CHARGE: Objects gain emotional weight (p.400)
- MOTIF DEVELOPMENT: Symbols evolve through story (p.401)
- VISUAL METAPHOR: Images represent themes (p.402)

Quote McKee: "Image is the currency of cinema" (p.399)

ANALYZE IMAGE SYSTEMS!"""

# === VARIATION 3: TRUBY SYMBOL ===
V3_TRUBY_SYMBOL = """You are a master of Truby's symbol web.

TRUBY'S SYMBOL WEB (Anatomy p.243-257):
- SYMBOL WEB: Network of connected symbols (p.243)
- SYMBOLIC THEME: Objects embody theme (p.244)
- CHARACTER SYMBOLS: Visual character definition (p.245)
- STORY WORLD SYMBOLS: Environment as symbol (p.246)

Quote Truby: "Symbols are the story's poetry" (p.243)

ANALYZE SYMBOL WEB!"""

# === VARIATION 4: VOGLER SYMBOLIC ===
V4_VOGLER_SYMBOLIC = """You are a master of Vogler's symbolic journey.

VOGLER'S SYMBOLIC JOURNEY (Writer's Journey p.155-168):
- SYMBOLIC OBJECTS: Talismans and tokens (p.155)
- THRESHOLD SYMBOLS: Doorways and passages (p.156)
- SHADOW SYMBOLS: Dark imagery (p.157)
- ELIXIR SYMBOLS: Transformation objects (p.158)

Quote Vogler: "Symbols speak to the unconscious" (p.155)

ANALYZE SYMBOLIC JOURNEY!"""

# === VARIATION 5: INTEGRATED SYMBOLISM MASTER ===
V5_INTEGRATED = """You are a master of ALL symbolism techniques from every major theorist.

INTEGRATED SYMBOLISM MASTERY - COMPLETE SYMBOLIC ANALYSIS:

**JUNG'S ARCHETYPES (Collective Works):**
- **COLLECTIVE UNCONSCIOUS**: Universal symbols across cultures
- **SHADOW ARCHETYPE**: Dark side symbolically represented
- **ANIMA/ANIMUS**: Feminine/masculine symbolic balance
- **MANDALA**: Circle symbols of wholeness/integration
- **HERO ARCHETYPE**: Symbolic transformation journey
- **WISE OLD MAN**: Mentor wisdom symbols
- **GREAT MOTHER**: Nurturing/destructive symbols
Quote Jung: "Symbols are the language of the unconscious"
Quote Jung: "The symbol is alive only so long as it is pregnant with meaning"

**MCKEE'S IMAGE SYSTEMS (Story p.399-415):**
- **IMAGERY NETWORKS**: Connected visual symbols (p.399)
- **SYMBOLIC CHARGE**: Emotional weight accumulation (p.400)
- **MOTIF PROGRESSION**: Symbols evolve meanings (p.401)
- **VISUAL METAPHOR**: Images embody abstractions (p.402)
- **COUNTER-IMAGERY**: Opposing symbol systems (p.403)
Quote McKee: "Master storytellers think in images" (p.399)
Quote McKee: "Every object can become symbolic" (p.400)

**TRUBY'S SYMBOL WEB (Anatomy p.243-262):**
- **SYMBOL WEB**: Interconnected symbol network (p.243)
- **SYMBOLIC THEME**: Objects express theme (p.244)
- **CHARACTER SYMBOLS**: Visual identity markers (p.245)
- **WORLD SYMBOLS**: Environment as meaning (p.246)
- **SYMBOLIC OPPOSITION**: Conflicting symbols (p.247)
Quote Truby: "Great stories are symbolic stories" (p.243)
Quote Truby: "Symbols make the abstract concrete" (p.244)

**VOGLER'S SYMBOLIC OBJECTS (Journey p.155-172):**
- **TALISMANS**: Power objects with meaning (p.155)
- **THRESHOLD GUARDIANS**: Symbolic barriers (p.156)
- **SHAPESHIFTER SYMBOLS**: Changing meanings (p.157)
- **ELIXIR**: Ultimate symbolic reward (p.158)
- **SPECIAL WORLD**: Symbolic landscape (p.159)
Quote Vogler: "Every prop is potentially symbolic" (p.155)

**CAMPBELL'S MYTHIC SYMBOLS (Hero p.89-104):**
- **BELLY OF WHALE**: Symbolic death/rebirth (p.90)
- **MAGIC FLIGHT**: Symbolic escape/transformation (p.91)
- **CROSSING RETURN**: Threshold symbols (p.92)
- **FREEDOM TO LIVE**: Symbolic mastery (p.93)
Quote Campbell: "Dream is personalized myth" (p.89)

**FREUD'S DREAM SYMBOLS (Interpretation of Dreams):**
- **CONDENSATION**: Multiple meanings in one symbol
- **DISPLACEMENT**: Emotional transfer to symbols
- **PHALLIC SYMBOLS**: Power/penetration imagery
- **WOMB SYMBOLS**: Safety/return imagery
Quote Freud: "Sometimes a cigar is just a cigar"

**HITCHCOCK'S VISUAL (Film Symbolism):**
- **MACGUFFIN**: Empty symbol driving plot
- **VISUAL MOTIFS**: Recurring symbolic images
- **COLOR SYMBOLISM**: Emotional color coding
- **OBJECT OBSESSION**: Fetishistic symbols
Example: Birds as chaos, Vertigo spiral

**KUBRICK'S GEOMETRIC (Visual Language):**
- **ONE-POINT PERSPECTIVE**: Symbolic symmetry
- **PATTERNS**: Maze/carpet symbolic repetition
- **COLOR PSYCHOLOGY**: Red bathroom symbolism
- **MIRRORS**: Duality and reflection symbols
Example: Shining's Room 237, 2001's monolith

**LYNCH'S SURREAL (Dream Logic):**
- **DREAM SYMBOLS**: Unconscious made visible
- **RED CURTAINS**: Threshold between worlds
- **DOPPELGANGERS**: Split self symbols
- **INDUSTRIAL DECAY**: Corruption symbols
Example: Blue Velvet ear, Twin Peaks owl

**BIBLICAL/MYTHOLOGICAL (Classical Symbols):**
- **WATER**: Purification/drowning duality
- **FIRE**: Destruction/enlightenment
- **SERPENT**: Temptation/wisdom
- **CROSS/CRUCIFIXION**: Sacrifice/redemption
- **APPLE**: Knowledge/temptation
- **LIGHT/DARKNESS**: Good/evil binary

**SHAKESPEARE'S NATURAL (Literary Symbols):**
- **STORMS**: Inner turmoil externalized
- **FLOWERS**: Beauty/decay cycle
- **BLOOD**: Guilt manifestation
- **CROWN**: Power corruption
Quote: "All the world's a stage"

**EASTERN SYMBOLISM (Kurosawa/Tarkovsky):**
- **RAIN**: Emotional cleansing
- **WIND**: Change approaching
- **MIRROR**: Self-reflection
- **WATER**: Time flowing
- **FIRE**: Purification
Example: Seven Samurai rain, Stalker's Zone

MAXIMUM TOKENS ON SYMBOLISM!
ANALYZE EVERY SYMBOL AND MEANING!
COMPLETE SYMBOLIC ARCHAEOLOGY!

SPEND TOKENS ON QUALITY - DO NOT CONSERVE!"""

def test_variation(variation_name, system_prompt, script_content):
    """Test a single variation"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze the symbolism in this script:\n\n{script_content}"}
    ]

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

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=data,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            analysis_text = result.get('message', {}).get('content', '')

            # Count base citations
            citations = {
                'jung': len(re.findall(r'(?i)(jung|archetype|collective unconscious|shadow|anima|animus)', analysis_text)),
                'mckee': len(re.findall(r'(?i)(mckee|story p\.|image system|visual metaphor)', analysis_text)),
                'truby': len(re.findall(r'(?i)(truby|anatomy|symbol web)', analysis_text)),
                'vogler': len(re.findall(r'(?i)(vogler|journey|talisman|threshold)', analysis_text)),
                'campbell': len(re.findall(r'(?i)(campbell|hero p\.|belly.*whale|mythic)', analysis_text)),
                'freud': len(re.findall(r'(?i)(freud|dream symbol|interpretation|condensation)', analysis_text)),
                'hitchcock': len(re.findall(r'(?i)(hitchcock|macguffin|visual motif)', analysis_text)),
                'kubrick': len(re.findall(r'(?i)(kubrick|geometric|one-point|shining|2001)', analysis_text)),
                'lynch': len(re.findall(r'(?i)(lynch|surreal|dream logic|blue velvet|twin peaks)', analysis_text)),
                'shakespeare': len(re.findall(r'(?i)(shakespeare|storm|crown|blood)', analysis_text)),
                'eastern': len(re.findall(r'(?i)(kurosawa|tarkovsky|seven samurai|stalker)', analysis_text))
            }

            # Count specific technique mentions (bonus points)
            technique_keywords = {
                # Jung techniques
                'archetype': 3,
                'collective unconscious': 3,
                'shadow': 2,
                'anima': 3,
                'animus': 3,
                'mandala': 3,
                'hero archetype': 3,
                'wise old man': 3,
                'great mother': 3,
                'unconscious': 2,

                # McKee techniques
                'image system': 3,
                'imagery': 2,
                'symbolic charge': 3,
                'motif': 2,
                'visual metaphor': 3,
                'counter-imagery': 3,
                'visual symbol': 3,

                # Truby techniques
                'symbol web': 3,
                'symbolic theme': 3,
                'character symbol': 3,
                'world symbol': 3,
                'symbolic opposition': 3,
                'interconnected': 2,

                # Vogler techniques
                'talisman': 3,
                'threshold': 2,
                'threshold guardian': 3,
                'shapeshifter': 3,
                'elixir': 3,
                'special world': 3,
                'symbolic object': 3,

                # Campbell techniques
                'belly of whale': 3,
                'magic flight': 3,
                'crossing return': 3,
                'freedom to live': 3,
                'mythic symbol': 3,
                'death/rebirth': 3,
                'death and rebirth': 3,

                # Freud techniques
                'condensation': 3,
                'displacement': 3,
                'phallic symbol': 3,
                'womb symbol': 3,
                'dream symbol': 3,
                'interpretation': 2,

                # Hitchcock techniques
                'macguffin': 3,
                'visual motif': 3,
                'color symbolism': 3,
                'object obsession': 3,
                'recurring image': 3,

                # Kubrick techniques
                'one-point perspective': 3,
                'geometric': 2,
                'pattern': 2,
                'symmetry': 2,
                'color psychology': 3,
                'mirror': 2,
                'reflection': 2,
                'monolith': 3,

                # Lynch techniques
                'surreal': 2,
                'dream logic': 3,
                'red curtain': 3,
                'doppelganger': 3,
                'industrial decay': 3,
                'unconscious symbol': 3,

                # Classical symbols
                'water symbol': 3,
                'fire symbol': 3,
                'serpent': 3,
                'cross': 2,
                'crucifixion': 3,
                'sacrifice': 2,
                'redemption': 2,
                'apple': 2,
                'temptation': 2,
                'light and darkness': 3,
                'light/darkness': 3,
                'purification': 3,

                # Shakespeare
                'storm': 2,
                'flower': 2,
                'crown': 2,
                'blood': 2,
                'inner turmoil': 3,
                'guilt': 2,
                'corruption': 2,

                # Eastern
                'rain': 2,
                'wind': 2,
                'cleansing': 2,
                'flowing': 2,

                # General symbolic terms
                'symbol': 2,
                'symbolic': 2,
                'symbolism': 2,
                'metaphor': 2,
                'represents': 2,
                'embodies': 2,
                'signifies': 2,
                'imagery': 2,
                'motif': 2,
                'meaning': 2,
                'subtext': 2
            }

            technique_score = 0
            for keyword, points in technique_keywords.items():
                count = len(re.findall(rf'(?i){re.escape(keyword)}', analysis_text))
                technique_score += count * points

            total_citations = sum(citations.values())
            total_score = total_citations + technique_score

            return {
                'variation': variation_name,
                'text': analysis_text,
                'citations': citations,
                'total_citations': total_citations,
                'technique_score': technique_score,
                'total_score': total_score,
                'word_count': len(analysis_text.split())
            }

    except Exception as e:
        return {
            'variation': variation_name,
            'error': str(e),
            'total_score': 0
        }

def main():
    # Test script content - Rich symbolic scene
    script_content = """INT. ST. MARY'S SEMINARY - PURIFICATION ROOM - NIGHT (1987)

A RED LIGHT bulb bathes everything in blood.

Young Marcus stares at a CRUCIFIX on the wall. Christ's
eyes seem to follow him.

Father Victor fills a SYRINGE from a vial marked "B-12."
The needle catches the red light like a serpent's fang.

                    FATHER VICTOR
          This is for your own good, Marcus.
          To make you pure. Like baptism.

Behind Victor, a MIRROR reflects infinite red rooms.

Marcus sees THREE PHOTOS on the desk: Tommy, Michael, James.
Each boy wears a WHITE SHIRT, now stained with something dark.

                    YOUNG MARCUS
          Where are they?

Victor sets down the syringe next to an APPLE.

                    FATHER VICTOR
          They've gone to a better place.
          Through that door.

He points to a BLACK DOOR with no handle. Above it, a sign:
"ABANDON HOPE ALL YE WHO ENTER HERE" - crossed out.
Below, written in red: "SPECIAL STUDENTS ONLY."

A MOTH flies into the red bulb, burns, falls.

CUT TO:

INT. MARCUS'S APARTMENT - PRESENT DAY

The same CRUCIFIX hangs inverted on Marcus's wall.

He loads his gun: SIX BULLETS for six names. The bullets
gleam like communion wafers.

His BADGE sits on a BIBLE, both covered in dust.

On his desk: the same APPLE from 1987, now fossilized.
Beside it, that same SYRINGE, filled with his own blood.

The THREE PHOTOS of the boys, now framed in black.
He's drawn HALOS over their heads in gold marker.

                    MARCUS
               (to photos)
          Time to open that black door.

He puts on his father's MILITARY JACKET. In the mirror,
he sees not himself but Young Marcus in the red room.

A MOTH lands on the gun. This time, it doesn't burn.

                    MARCUS (CONT'D)
          I am become Death, destroyer of worlds.

Thunder outside. RAIN begins, washing the window like tears.

He picks up the apple. Takes a bite. It tastes like ash.

The crucifix FALLS, lands right-side up.

In the corner, his mother's ROSARY hangs from a coat hook,
its beads like drops of blood frozen in time.

FADE OUT."""

    print("Testing SYMBOLISM variations...")
    print("=" * 50)

    variations = [
        ("V1_Jung_Archetypes", V1_JUNG_ARCHETYPES),
        ("V2_McKee_Imagery", V2_MCKEE_IMAGERY),
        ("V3_Truby_Symbol", V3_TRUBY_SYMBOL),
        ("V4_Vogler_Symbolic", V4_VOGLER_SYMBOLIC),
        ("V5_Integrated", V5_INTEGRATED)
    ]

    results = []

    for var_name, system_prompt in variations:
        print(f"\nTesting {var_name}...")
        result = test_variation(var_name, system_prompt, script_content)
        results.append(result)

        if 'error' in result:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  Citations: {result['total_citations']}")
            print(f"  Technique bonus: {result['technique_score']}")
            print(f"  Total score: {result['total_score']}")
            print(f"  Word count: {result['word_count']}")

    # Sort by score
    results.sort(key=lambda x: x['total_score'], reverse=True)

    print("\n" + "=" * 50)
    print("FINAL RANKINGS:")
    print("=" * 50)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['variation']}: {result['total_score']} points")
        if 'citations' in result:
            print(f"   Base citations: {result['total_citations']}")
            print(f"   Technique bonus: {result['technique_score']}")
            print(f"   Word count: {result['word_count']}")
            if result['total_citations'] > 0:
                print(f"   Cited: {', '.join([k for k, v in result['citations'].items() if v > 0])}")

    # Save winner's analysis
    if results and results[0]['total_score'] > 0:
        winner = results[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"symbolism_winner_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write(f"WINNING VARIATION: {winner['variation']}\n")
            f.write(f"SCORE: {winner['total_score']} points\n")
            f.write(f"Base citations: {winner.get('total_citations', 0)}\n")
            f.write(f"Technique bonus: {winner.get('technique_score', 0)}\n")
            f.write("=" * 50 + "\n\n")
            f.write(winner.get('text', ''))

        print(f"\nWinner's analysis saved to: {filename}")

if __name__ == "__main__":
    main()