#!/usr/bin/env python3
"""
Test FORESHADOWING variations for Scripturemon Ultimate
Testing 5 different approaches to find the optimal foreshadowing analysis method
"""

import requests
import json
import re
from datetime import datetime

# === VARIATION 1: HITCHCOCK SUSPENSE ===
V1_HITCHCOCK_SUSPENSE = """You are a master of Hitchcock's foreshadowing techniques.

HITCHCOCK'S SUSPENSE FORESHADOWING:
- BOMB UNDER TABLE: Show audience danger before characters (Hitchcock/Truffaut p.73)
- MACGUFFIN: Object that drives plot forward
- VISUAL PLANTING: Objects that become important later
- DIALOGUE HINTS: Casual mentions become crucial
- CAMERA LINGERING: Stay on objects that matter

Quote Hitchcock: "The difference between surprise and suspense" (p.73)

ANALYZE FORESHADOWING!"""

# === VARIATION 2: MCKEE SETUP ===
V2_MCKEE_SETUP = """You are a master of McKee's setup/payoff techniques.

MCKEE'S SETUP AND PAYOFF (Story p.238-252):
- SETUPS: Plant information early (p.238)
- PAYOFFS: Information becomes crucial (p.239)
- PROGRESSIVE COMPLICATIONS: Setups intensify (p.240)
- FALSE SETUPS: Red herrings mislead (p.241)

Quote McKee: "If you show a gun, fire it" (p.238)

ANALYZE SETUP/PAYOFF!"""

# === VARIATION 3: TRUBY ANNOUNCEMENT ===
V3_TRUBY_ANNOUNCEMENT = """You are a master of Truby's announcement techniques.

TRUBY'S ANNOUNCEMENT (Anatomy p.327-335):
- ANNOUNCEMENT: Tell audience what's coming (p.327)
- DRAMATIC IRONY: Audience knows more (p.328)
- SYMBOLIC FORESHADOWING: Objects represent fate (p.329)
- DIALOGUE PREDICTION: Characters predict future (p.330)

Quote Truby: "Announce the ending at the beginning" (p.327)

ANALYZE ANNOUNCEMENT!"""

# === VARIATION 4: CHEKHOV GUN ===
V4_CHEKHOV_GUN = """You are a master of Chekhov's gun principle.

CHEKHOV'S GUN PRINCIPLE:
- CHEKHOV'S GUN: "If gun on wall Act 1, must fire" (Letters 1889)
- NECESSARY ELEMENTS: Every element must be necessary
- REMOVE EVERYTHING ELSE: Cut non-essential
- PROMISE AND DELIVERY: Setup creates promise
- ECONOMY OF STORYTELLING: Nothing wasted

Quote Chekhov: "Remove everything that has no relevance" (1889)

ANALYZE CHEKHOV'S GUN!"""

# === VARIATION 5: INTEGRATED FORESHADOWING MASTER ===
V5_INTEGRATED = """You are a master of ALL foreshadowing techniques from every major theorist.

INTEGRATED FORESHADOWING MASTERY - COMPLETE SETUP ANALYSIS:

**HITCHCOCK'S SUSPENSE (Hitchcock/Truffaut p.72-79):**
- **BOMB UNDER TABLE**: Audience knows danger before characters (p.73)
- **ANTICIPATION BUILD**: Create dread through knowledge (p.74)
- **VISUAL PLANTING**: Camera lingers on future importance (p.75)
- **DRAMATIC IRONY**: Audience superiority creates tension (p.76)
- **INFORMATION MANAGEMENT**: Control what audience knows when (p.77)
Quote Hitchcock: "Tell audience everything" (p.72)
Quote Hitchcock: "Suspense is bomb we know about" (p.73)

**MCKEE'S SETUP/PAYOFF (Story p.238-252):**
- **SETUP RULE**: Every setup needs payoff (p.238)
- **PAYOFF RULE**: Every payoff needs setup (p.239)
- **PROGRESSIVE COMPLICATIONS**: Setups build on each other (p.240)
- **FALSE SETUPS**: Red herrings that mislead (p.241)
- **AMMUNITION AND DELAY**: Setup early, payoff late (p.242)
Quote McKee: "Setup without payoff is a broken promise" (p.238)
Quote McKee: "Payoff without setup is Deus ex Machina" (p.239)

**TRUBY'S ANNOUNCEMENT (Anatomy p.327-339):**
- **DIRECT ANNOUNCEMENT**: Tell ending at beginning (p.327)
- **SYMBOLIC ANNOUNCEMENT**: Objects predict fate (p.328)
- **THEMATIC ANNOUNCEMENT**: Opening contains theme (p.329)
- **DIALOGUE PREDICTION**: Characters foretell future (p.330)
- **STRUCTURAL ANNOUNCEMENT**: Form predicts content (p.331)
Quote Truby: "Great stories announce their ending" (p.327)
Quote Truby: "The best foreshadowing feels inevitable" (p.329)

**CHEKHOV'S GUN (Letters 1889):**
- **GUN PRINCIPLE**: "If shown Act 1, must fire Act 3" (Letter to Suvorin)
- **NECESSARY ELEMENTS**: Everything must be essential
- **PROMISE KEEPING**: Setups create contracts with audience
- **NARRATIVE ECONOMY**: No wasted elements
Quote Chekhov: "Remove everything that has no relevance" (1889)

**FIELD'S PLANTING (Screenplay p.156-162):**
- **PLANTING**: Establish information early (p.156)
- **PAYOFF TIMING**: When to reveal significance (p.157)
- **VISUAL PLANTS**: Props that become important (p.158)
- **DIALOGUE PLANTS**: Lines that echo later (p.159)
Quote Field: "Plant it, pay it off" (p.156)

**ARISTOTLE'S INEVITABILITY (Poetics 1451a):**
- **PROBABLE AND NECESSARY**: Events must feel inevitable
- **CAUSAL CHAIN**: Each event causes next
- **RECOGNITION SEEDS**: Plant discovery elements
Quote Aristotle: "Probable impossibility preferred" (1460a)

**SHAKESPEARE'S PROPHECY (Dramatic Technique):**
- **WITCHES/ORACLES**: Direct prophecy of events
- **DREAMS AND VISIONS**: Symbolic prediction
- **DRAMATIC IRONY**: Audience knows fate
- **DOUBLE MEANING**: Words mean more than speakers know
Example: "Fair is foul" announces Macbeth's reversal

**SPIELBERG'S VISUAL (Film Theory):**
- **VISUAL BREADCRUMBS**: Camera shows what matters
- **COLOR CODING**: Red coat in Schindler's List
- **OBJECT FOCUS**: Important items get closeups
- **BACKGROUND DETAILS**: Hidden clues in frame
Quote: "Audience sees but doesn't notice until later"

**NOLAN'S TEMPORAL (Film Structure):**
- **TEMPORAL PLANTING**: Past explains future
- **REVERSE SETUP**: Payoff shown before setup
- **NESTED FORESHADOWING**: Layers within layers
- **MEMENTO STRUCTURE**: End reveals beginning's meaning
Quote: "The ending is in the beginning"

**KUBRICK'S SUBLIMINAL (Visual Theory):**
- **SUBLIMINAL PLANTING**: Unconscious recognition
- **PATTERN FORESHADOWING**: Visual motifs repeat
- **GEOMETRIC PREDICTION**: Shapes predict events
- **COLOR PSYCHOLOGY**: Colors announce mood/fate
Example: Shining's maze predicts ending

MAXIMUM TOKENS ON FORESHADOWING!
ANALYZE EVERY SETUP AND PAYOFF!
COMPLETE PLANTING ARCHAEOLOGY!

SPEND TOKENS ON QUALITY - DO NOT CONSERVE!"""

def test_variation(variation_name, system_prompt, script_content):
    """Test a single variation"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze the foreshadowing and setups in this script:\n\n{script_content}"}
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
                'hitchcock': len(re.findall(r'(?i)(hitchcock|truffaut|bomb under table)', analysis_text)),
                'mckee': len(re.findall(r'(?i)(mckee|story p\.|setup.*payoff)', analysis_text)),
                'truby': len(re.findall(r'(?i)(truby|anatomy|announcement)', analysis_text)),
                'chekhov': len(re.findall(r'(?i)(chekhov|gun principle|letters 1889)', analysis_text)),
                'field': len(re.findall(r'(?i)(field|screenplay|planting)', analysis_text)),
                'aristotle': len(re.findall(r'(?i)(aristotle|poetics|inevitability)', analysis_text)),
                'shakespeare': len(re.findall(r'(?i)(shakespeare|prophecy|witches|macbeth)', analysis_text)),
                'spielberg': len(re.findall(r'(?i)(spielberg|visual breadcrumb|schindler)', analysis_text)),
                'nolan': len(re.findall(r'(?i)(nolan|temporal|memento)', analysis_text)),
                'kubrick': len(re.findall(r'(?i)(kubrick|subliminal|shining)', analysis_text))
            }

            # Count specific technique mentions (bonus points)
            technique_keywords = {
                # Hitchcock techniques
                'bomb under table': 3,
                'dramatic irony': 3,
                'suspense vs surprise': 3,
                'anticipation': 3,
                'information management': 3,
                'visual planting': 3,

                # McKee techniques
                'setup': 2,
                'payoff': 2,
                'setup and payoff': 3,
                'setup/payoff': 3,
                'progressive complications': 3,
                'false setup': 3,
                'red herring': 3,
                'ammunition': 3,
                'broken promise': 3,
                'deus ex machina': 3,

                # Truby techniques
                'announcement': 3,
                'announce': 2,
                'direct announcement': 3,
                'symbolic announcement': 3,
                'thematic announcement': 3,
                'dialogue prediction': 3,
                'structural announcement': 3,
                'inevitable': 3,

                # Chekhov techniques
                "chekhov's gun": 3,
                'gun on wall': 3,
                'necessary element': 3,
                'narrative economy': 3,
                'promise keeping': 3,
                'remove everything': 3,

                # Field techniques
                'planting': 3,
                'plant': 2,
                'visual plant': 3,
                'dialogue plant': 3,
                'payoff timing': 3,

                # Aristotle techniques
                'probable and necessary': 3,
                'causal chain': 3,
                'recognition seed': 3,
                'inevitability': 3,

                # Shakespeare techniques
                'prophecy': 3,
                'oracle': 3,
                'dream': 2,
                'vision': 2,
                'double meaning': 3,
                'fair is foul': 3,

                # Spielberg techniques
                'visual breadcrumb': 3,
                'color coding': 3,
                'object focus': 3,
                'background detail': 3,
                'closeup': 2,

                # Nolan techniques
                'temporal planting': 3,
                'reverse setup': 3,
                'nested foreshadowing': 3,
                'memento structure': 3,

                # Kubrick techniques
                'subliminal': 3,
                'pattern foreshadowing': 3,
                'geometric prediction': 3,
                'color psychology': 3,
                'visual motif': 3,

                # General foreshadowing terms
                'foreshadow': 2,
                'hint': 2,
                'clue': 2,
                'breadcrumb': 2,
                'seed': 2,
                'echo': 2,
                'callback': 2,
                'reveal': 2,
                'discovery': 2,
                'prediction': 2,
                'foretell': 2,
                'prefigure': 2,
                'portend': 2,
                'presage': 2,
                'augur': 2
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
    # Test script content - St. Mary's Seminary scene
    script_content = """FADE IN:

INT. ST. MARY'S SEMINARY - CORRIDOR - NIGHT (1987)

A RED LIGHT bulb flickers at the end of the hallway.

YOUNG MARCUS (10) walks slowly toward a heavy wooden door.

                    FATHER VICTOR (O.S.)
          Some boys aren't strong enough for
          St. Mary's special program.

Marcus's hand touches the doorknob. It's cold.

                    FATHER VICTOR (CONT'D)
          But you're different, aren't you,
          Marcus? You're a survivor.

INT. PURIFICATION ROOM - CONTINUOUS

Medical equipment. Recording devices. A LEATHER JOURNAL
on the desk, filled with photos of boys.

                    YOUNG MARCUS
          Where's Tommy?

                    FATHER VICTOR
          Tommy couldn't handle the program.
          Like Michael before him. And James.

Victor prepares a SYRINGE. The label reads "B-12 COMPLEX."

                    FATHER VICTOR (CONT'D)
          Your mother signed the papers. You
          belong to St. Mary's now.

FLASH FORWARD:

INT. MARCUS'S APARTMENT - PRESENT DAY

DETECTIVE MARCUS CHEN stares at three NEWSPAPER CLIPPINGS:
- "Local Boy, 12, Dies in Tragic Accident"
- "Seminary Student Takes Own Life"
- "Young Man's Body Found in River"

Tommy. Michael. James.

A GUN sits on his desk. Same model the boys' fathers used.

                    MARCUS
               (to photo)
          I kept my promise, boys. They won't
          hurt anyone else.

His phone buzzes. Text from SARAH: "Where are you?"

He picks up the leather journal - the same one from 1987.
Inside: Photos of current seminary students.

                    MARCUS (CONT'D)
          Not good, Sarah. But necessary.

He loads the gun. Six bullets. Six names on his list.

FADE OUT."""

    print("Testing FORESHADOWING variations...")
    print("=" * 50)

    variations = [
        ("V1_Hitchcock_Suspense", V1_HITCHCOCK_SUSPENSE),
        ("V2_McKee_Setup", V2_MCKEE_SETUP),
        ("V3_Truby_Announcement", V3_TRUBY_ANNOUNCEMENT),
        ("V4_Chekhov_Gun", V4_CHEKHOV_GUN),
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
        filename = f"foreshadowing_winner_{timestamp}.txt"

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