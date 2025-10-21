#!/usr/bin/env python3
"""
Test TONE variations for Scripturemon Ultimate
Testing 5 different approaches to find the optimal tone analysis method
"""

import requests
import json
import re
from datetime import datetime

# === VARIATION 1: MCKEE MOOD ===
V1_MCKEE_MOOD = """You are a master of McKee's mood and tone techniques.

MCKEE'S MOOD CONTROL (Story p.376-388):
- MOOD: Emotional atmosphere created (p.376)
- TONE: Attitude toward subject (p.377)
- GENRE CONVENTIONS: Tone expectations (p.378)
- IRONIC COUNTERPOINT: Tone against content (p.379)

Quote McKee: "Mood is the feeling within scene" (p.376)

ANALYZE TONE AND MOOD!"""

# === VARIATION 2: TRUBY TONE ===
V2_TRUBY_TONE = """You are a master of Truby's tone techniques.

TRUBY'S TONE (Anatomy p.418-427):
- STORY TONE: Overall emotional register (p.418)
- TONAL SHIFT: Changes mark turning points (p.419)
- GENRE TONE: Each genre has tone rules (p.420)
- COMIC/TRAGIC: Fundamental tone choice (p.421)

Quote Truby: "Tone is the story's attitude" (p.418)

ANALYZE STORY TONE!"""

# === VARIATION 3: GENRE TONE ===
V3_GENRE_TONE = """You are a master of genre-specific tone.

GENRE TONE MASTERY:
- NOIR: Cynical, fatalistic, dark
- THRILLER: Tense, paranoid, urgent
- HORROR: Dread, unease, shock
- DRAMA: Serious, emotional, realistic
- COMEDY: Light, ironic, playful

Each genre creates specific tonal expectations.

ANALYZE GENRE TONE!"""

# === VARIATION 4: CINEMATIC TONE ===
V4_CINEMATIC_TONE = """You are a master of cinematic tone creation.

CINEMATIC TONE TECHNIQUES:
- VISUAL TONE: Lighting, color, composition
- AUDIO TONE: Music, sound design, silence
- PERFORMANCE TONE: Acting style choices
- EDITORIAL TONE: Pacing, rhythm, cuts
- NARRATIVE TONE: Voice, perspective, distance

Film creates tone through all elements.

ANALYZE CINEMATIC TONE!"""

# === VARIATION 5: INTEGRATED TONE MASTER ===
V5_INTEGRATED = """You are a master of ALL tone techniques from every major theorist.

INTEGRATED TONE MASTERY - COMPLETE ATMOSPHERIC ANALYSIS:

**MCKEE'S MOOD/TONE (Story p.376-392):**
- **MOOD CREATION**: Feeling within scene atmosphere (p.376)
- **TONE DEFINITION**: Writer's attitude toward material (p.377)
- **GENRE CONVENTIONS**: Expected tonal registers (p.378)
- **IRONIC COUNTERPOINT**: Tone contradicts content (p.379)
- **COMIC CLIMAX**: Positive tone resolution (p.380)
- **TRAGIC CLIMAX**: Negative tone resolution (p.381)
Quote McKee: "Control mood or it controls you" (p.376)
Quote McKee: "Tone is invisible but felt" (p.377)

**TRUBY'S TONAL REGISTER (Anatomy p.418-432):**
- **STORY TONE**: Overall emotional atmosphere (p.418)
- **TONAL SHIFTS**: Mark story turning points (p.419)
- **GENRE TONE**: Each genre's tonal rules (p.420)
- **COMIC/TRAGIC**: Binary tonal choice (p.421)
- **IRONIC TONE**: Say one thing, mean another (p.422)
Quote Truby: "Tone is story's emotional DNA" (p.418)
Quote Truby: "Master tone or lose audience" (p.419)

**FIELD'S ATMOSPHERE (Screenplay p.189-196):**
- **ATMOSPHERIC SETUP**: Establish tone page one (p.189)
- **CONSISTENT TONE**: Maintain throughout (p.190)
- **TONAL MODULATION**: Controlled variations (p.191)
- **GENRE EXPECTATIONS**: Meet or subvert (p.192)
Quote Field: "First page sets tone" (p.189)

**GENRE-SPECIFIC TONES:**
- **NOIR**: Cynical, fatalistic, morally ambiguous
- **THRILLER**: Paranoid, urgent, breathless
- **HORROR**: Dread, unease, visceral fear
- **DRAMA**: Serious, emotional, realistic
- **COMEDY**: Light, playful, ironic
- **WESTERN**: Mythic, elegiac, violent
- **SCI-FI**: Wonder, speculation, alienation
- **ROMANCE**: Warm, hopeful, passionate

**HITCHCOCK'S SUSPENSE TONE (Film Theory):**
- **SUSTAINED DREAD**: Maintain unease throughout
- **ORDINARY MENACE**: Evil in everyday settings
- **WIT AMID TERROR**: Humor doesn't break tension
- **COOL OBSERVATION**: Detached camera eye
Quote: "Make audience suffer as much as possible"

**FINCHER'S DARK TONE (Visual Style):**
- **DESATURATED COLOR**: Drained of life
- **SHADOW DOMINANT**: Darkness overwhelms light
- **CLINICAL PRECISION**: Cold, methodical approach
- **DECAY AESTHETIC**: Everything deteriorating
Example: Se7en, Zodiac, Gone Girl atmosphere

**LYNCH'S SURREAL TONE (Dream Logic):**
- **UNCANNY VALLEY**: Familiar but wrong
- **AMBIENT DREAD**: Something always off
- **DREAM/NIGHTMARE**: Reality uncertain
- **SUBURBAN HORROR**: Evil beneath normal
Example: Blue Velvet, Mulholland Drive

**KUBRICK'S COLD TONE (Aesthetic Distance):**
- **EMOTIONAL DETACHMENT**: Observe don't feel
- **SYMMETRICAL COMPOSITION**: Inhuman perfection
- **IRONIC DISTANCE**: Commentary not empathy
- **DEHUMANIZATION**: People as objects
Example: 2001, Clockwork Orange, Shining

**COEN BROTHERS' IRONIC (Tonal Mixture):**
- **VIOLENCE AND HUMOR**: Death is absurd
- **REGIONAL SPECIFICITY**: Place determines tone
- **PHILOSOPHICAL COMEDY**: Existential jokes
- **CASUAL BRUTALITY**: Violence without weight
Example: Fargo, No Country, Burn After Reading

**TARKOVSKY'S SPIRITUAL (Contemplative Tone):**
- **TEMPORAL WEIGHT**: Time as character
- **NATURAL ELEMENTS**: Rain, wind, fire
- **SILENCE AND SPACE**: What's not said
- **METAPHYSICAL QUESTIONS**: Beyond material
Example: Stalker, Solaris, Mirror

**SCORSESE'S KINETIC (Energy Tone):**
- **NERVOUS ENERGY**: Constant movement
- **CATHOLIC GUILT**: Sin and redemption
- **VIOLENCE BALLET**: Choreographed chaos
- **MASCULINE ANXIETY**: Toxic masculinity
Example: Goodfellas, Taxi Driver, Raging Bull

**PTA'S INTENSE (Emotional Saturation):**
- **OVERWHELMING EMOTION**: Too much feeling
- **LONG TAKES**: Sustained intensity
- **EXPLOSIVE RELEASES**: Emotional volcanoes
- **FATHER ISSUES**: Paternal shadows
Example: There Will Be Blood, Magnolia

MAXIMUM TOKENS ON TONE!
ANALYZE EVERY ATMOSPHERIC ELEMENT!
COMPLETE TONAL ARCHAEOLOGY!

SPEND TOKENS ON QUALITY - DO NOT CONSERVE!"""

def test_variation(variation_name, system_prompt, script_content):
    """Test a single variation"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze the tone and mood in this script:\n\n{script_content}"}
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
                'mckee': len(re.findall(r'(?i)(mckee|story p\.|mood|tone.*attitude)', analysis_text)),
                'truby': len(re.findall(r'(?i)(truby|anatomy|tonal.*register|story tone)', analysis_text)),
                'field': len(re.findall(r'(?i)(field|screenplay|atmosphere|first page)', analysis_text)),
                'hitchcock': len(re.findall(r'(?i)(hitchcock|suspense|dread|suffer)', analysis_text)),
                'fincher': len(re.findall(r'(?i)(fincher|se7en|zodiac|gone girl)', analysis_text)),
                'lynch': len(re.findall(r'(?i)(lynch|surreal|blue velvet|mulholland)', analysis_text)),
                'kubrick': len(re.findall(r'(?i)(kubrick|2001|clockwork|shining)', analysis_text)),
                'coen': len(re.findall(r'(?i)(coen|fargo|no country|burn after)', analysis_text)),
                'tarkovsky': len(re.findall(r'(?i)(tarkovsky|stalker|solaris|mirror)', analysis_text)),
                'scorsese': len(re.findall(r'(?i)(scorsese|goodfellas|taxi driver|raging bull)', analysis_text)),
                'pta': len(re.findall(r'(?i)(paul thomas anderson|pta|there will be blood|magnolia)', analysis_text))
            }

            # Count specific technique mentions (bonus points)
            technique_keywords = {
                # McKee techniques
                'mood': 2,
                'tone': 2,
                'atmosphere': 2,
                'emotional atmosphere': 3,
                'genre convention': 3,
                'ironic counterpoint': 3,
                'comic climax': 3,
                'tragic climax': 3,
                'attitude toward': 3,
                'feeling within': 3,

                # Truby techniques
                'tonal register': 3,
                'tonal shift': 3,
                'story tone': 3,
                'genre tone': 3,
                'comic/tragic': 3,
                'ironic tone': 3,
                'emotional dna': 3,
                'turning point': 2,

                # Field techniques
                'atmospheric setup': 3,
                'consistent tone': 3,
                'tonal modulation': 3,
                'genre expectation': 3,
                'first page': 2,

                # Genre tones
                'noir': 2,
                'cynical': 2,
                'fatalistic': 2,
                'thriller': 2,
                'paranoid': 2,
                'urgent': 2,
                'horror': 2,
                'dread': 2,
                'unease': 2,
                'drama': 2,
                'serious': 2,
                'comedy': 2,
                'light': 2,
                'playful': 2,
                'ironic': 2,
                'western': 2,
                'mythic': 2,
                'elegiac': 2,
                'sci-fi': 2,
                'wonder': 2,
                'romance': 2,
                'warm': 2,
                'hopeful': 2,

                # Hitchcock techniques
                'sustained dread': 3,
                'ordinary menace': 3,
                'wit amid terror': 3,
                'cool observation': 3,
                'detached': 2,
                'suspense': 2,

                # Fincher techniques
                'desaturated': 3,
                'shadow dominant': 3,
                'clinical precision': 3,
                'decay aesthetic': 3,
                'dark tone': 3,
                'cold': 2,
                'methodical': 2,

                # Lynch techniques
                'uncanny valley': 3,
                'ambient dread': 3,
                'dream/nightmare': 3,
                'dream logic': 3,
                'suburban horror': 3,
                'surreal': 2,

                # Kubrick techniques
                'emotional detachment': 3,
                'symmetrical': 2,
                'ironic distance': 3,
                'dehumanization': 3,
                'cold tone': 3,
                'aesthetic distance': 3,

                # Coen techniques
                'violence and humor': 3,
                'regional specificity': 3,
                'philosophical comedy': 3,
                'casual brutality': 3,
                'absurd': 2,

                # Tarkovsky techniques
                'temporal weight': 3,
                'natural elements': 3,
                'silence and space': 3,
                'metaphysical': 3,
                'contemplative': 2,
                'spiritual': 2,

                # Scorsese techniques
                'nervous energy': 3,
                'catholic guilt': 3,
                'violence ballet': 3,
                'masculine anxiety': 3,
                'kinetic': 2,

                # PTA techniques
                'overwhelming emotion': 3,
                'long takes': 3,
                'explosive release': 3,
                'father issues': 3,
                'emotional saturation': 3,

                # General tone terms
                'atmospheric': 2,
                'mood': 2,
                'tone': 2,
                'feeling': 2,
                'emotion': 2,
                'register': 2,
                'attitude': 2,
                'style': 2,
                'dark': 2,
                'heavy': 2,
                'oppressive': 2,
                'tense': 2,
                'ominous': 2,
                'foreboding': 2,
                'menacing': 2,
                'bleak': 2,
                'grim': 2,
                'disturbing': 2
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
    # Test script content - Dark tone scene
    script_content = """FADE IN:

INT. ABANDONED CHURCH - NIGHT

Rain hammers stained glass. Lightning illuminates broken
pews, scattered hymn books rotting in puddles.

MARCUS (40s) enters. Water drips from his coat. His footsteps
echo in the vast emptiness.

A DEAD RAT floats past his feet.

                    MARCUS
               (whispered)
          Forgive me, Father...

He walks toward the altar. Each step deliberate. Measured.
The floorboards groan under his weight.

AT THE ALTAR

A PRIEST kneels in prayer. Young. Innocent face. Clean collar.

                    PRIEST
          The church is closed, my son.

                    MARCUS
          I'm not your son.

The priest turns. Sees Marcus's face. Recognition. Terror.

                    PRIEST
          You... you were at St. Mary's.

                    MARCUS
          Room 237. Tuesday nights.

Thunder EXPLODES overhead. The priest backs against the altar.

                    PRIEST
          That was... that was forty years ago.
          I was just—

                    MARCUS
          —following orders?

Marcus pulls out a SYRINGE. Same kind they used on him.
The liquid inside is black as oil.

                    PRIEST
          Please. I've changed. I have a family now.

                    MARCUS
          So did Tommy. Before he hung himself
          at fourteen.

Lightning. The priest's face is skull-white. Shadows dance
on the walls like demons.

                    PRIEST
          I'll confess. To the police. Tonight.

Marcus steps closer. His shoes splash through bloody water.
Wait—when did it turn to blood?

                    MARCUS
          Too late for confession, Father.
          This is penance.

The priest SCREAMS. It echoes, distorts, becomes the scream
of a child. Marcus doesn't flinch.

                    MARCUS (CONT'D)
          Don't worry. It only hurts as much
          as you made us hurt.

He raises the syringe. Lightning freezes the moment—two men,
one kneeling, one standing, in a broken house of God.

                    MARCUS (CONT'D)
          Which means it's going to hurt
          quite a bit.

The stained glass SHATTERS inward. Rain and wind invade the
sanctuary. Candles extinguish. Darkness swallows everything.

A child's voice, singing:
          "Jesus loves me, this I know..."

Then silence. Just rain. And breathing in the dark.

FADE TO BLACK."""

    print("Testing TONE variations...")
    print("=" * 50)

    variations = [
        ("V1_McKee_Mood", V1_MCKEE_MOOD),
        ("V2_Truby_Tone", V2_TRUBY_TONE),
        ("V3_Genre_Tone", V3_GENRE_TONE),
        ("V4_Cinematic_Tone", V4_CINEMATIC_TONE),
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
        filename = f"tone_winner_{timestamp}.txt"

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