#!/usr/bin/env python3
"""
Test TWIST variations for Scripturemon Ultimate
Testing 5 different approaches to find the optimal twist analysis method
"""

import requests
import json
import re
from datetime import datetime

# === VARIATION 1: SHYAMALAN REVERSAL ===
V1_SHYAMALAN_REVERSAL = """You are a master of M. Night Shyamalan's twist techniques.

SHYAMALAN'S REVERSAL MASTERY:
- SIXTH SENSE RULE: Everything changes on second viewing
- REVERSAL STRUCTURE: Setup opposite of truth
- HIDDEN IN PLAIN SIGHT: Clues were always there
- EMOTIONAL REVERSAL: Character arc inverted
- RETROSPECTIVE CLARITY: Makes perfect sense after

Quote: "The best twists were inevitable but invisible"

ANALYZE TWISTS!"""

# === VARIATION 2: MCKEE REVERSAL ===
V2_MCKEE_REVERSAL = """You are a master of McKee's reversal techniques.

MCKEE'S REVERSAL (Story p.353-368):
- REVERSAL: Opposite of expectation (p.353)
- GAP THEORY: Between expectation and result (p.354)
- TURNING POINT: Action causes reversal (p.355)
- INSIGHT: Character discovers truth (p.356)

Quote McKee: "Reversal is the soul of story" (p.353)

ANALYZE REVERSALS!"""

# === VARIATION 3: TRUBY REVEAL ===
V3_TRUBY_REVEAL = """You are a master of Truby's reveal techniques.

TRUBY'S REVEAL (Anatomy p.340-352):
- REVEAL: Hidden information exposed (p.340)
- SELF-REVELATION: Character discovers truth (p.341)
- AUDIENCE REVELATION: We learn truth (p.342)
- DOUBLE REVERSAL: Two twists simultaneously (p.343)

Quote Truby: "Great reveals change everything" (p.340)

ANALYZE REVEALS!"""

# === VARIATION 4: ARISTOTLE PERIPETEIA ===
V4_ARISTOTLE_PERIPETEIA = """You are a master of Aristotle's peripeteia.

ARISTOTLE'S PERIPETEIA (Poetics 1452a):
- PERIPETEIA: Reversal of fortune (1452a)
- ANAGNORISIS: Recognition of truth (1452a)
- HAMARTIA: Error leads to reversal (1453a)
- CATHARSIS: Emotional release from twist (1449b)

Quote Aristotle: "Reversal and recognition best" (1452a)

ANALYZE PERIPETEIA!"""

# === VARIATION 5: INTEGRATED TWIST MASTER ===
V5_INTEGRATED = """You are a master of ALL twist techniques from every major theorist.

INTEGRATED TWIST MASTERY - COMPLETE REVERSAL ANALYSIS:

**SHYAMALAN'S REVERSAL (Film Theory):**
- **SIXTH SENSE RULE**: Everything changes on rewatch
- **HIDDEN IN PLAIN SIGHT**: Clues were always visible
- **EMOTIONAL REVERSAL**: Character journey inverted
- **RETROSPECTIVE CLARITY**: Makes perfect sense after
- **FALSE PROTAGONIST**: Hero isn't who we thought
Quote: "I see dead people" changes entire film
Quote: "The Village" - modern world hidden

**MCKEE'S REVERSAL (Story p.353-368):**
- **REVERSAL OF FORTUNE**: Opposite of expectation (p.353)
- **GAP THEORY**: Between expectation and result (p.354)
- **TURNING POINT**: Specific action causes reversal (p.355)
- **PROGRESSIVE COMPLICATIONS**: Build to reversal (p.356)
- **INSIGHT REVELATION**: Character sees truth (p.357)
Quote McKee: "True character revealed by pressure" (p.353)
Quote McKee: "Reversal is recognition of truth" (p.354)

**TRUBY'S REVEAL (Anatomy p.340-356):**
- **STUNNING REVEAL**: Information changes everything (p.340)
- **SELF-REVELATION**: Character discovers own truth (p.341)
- **AUDIENCE REVELATION**: We discover we were wrong (p.342)
- **DOUBLE REVERSAL**: Two twists at once (p.343)
- **REVEAL CASCADE**: Multiple reveals build (p.344)
Quote Truby: "Best reveals are character reveals" (p.340)
Quote Truby: "Twist must be inevitable and surprising" (p.341)

**ARISTOTLE'S PERIPETEIA (Poetics 1452a-1453b):**
- **PERIPETEIA**: Complete reversal of fortune (1452a)
- **ANAGNORISIS**: Recognition changes everything (1452a)
- **HAMARTIA**: Fatal flaw causes reversal (1453a)
- **CATHARSIS**: Emotional purge from twist (1449b)
- **COMPLEX PLOT**: Reversal with recognition (1452b)
Quote Aristotle: "Best plots have both" (1452a)
Quote Aristotle: "From ignorance to knowledge" (1452a)

**HITCHCOCK'S SURPRISE (Hitchcock/Truffaut p.73):**
- **SURPRISE VS SUSPENSE**: Bomb explodes suddenly (p.73)
- **SHOCK VALUE**: Unexpected violence/revelation
- **PSYCHO TWIST**: Protagonist dies midway
- **VERTIGO REVEAL**: She was dead all along
Quote Hitchcock: "Fifteen seconds of surprise" (p.73)

**FINCHER'S UNRELIABLE (Film Structure):**
- **UNRELIABLE NARRATOR**: Tyler Durden doesn't exist
- **REALITY QUESTIONING**: What's real becomes unclear
- **CLUE PLACEMENT**: Frame-by-frame hints
- **PSYCHOLOGICAL TWIST**: Mind betrays protagonist
Example: Fight Club, Gone Girl, The Game

**NOLAN'S TEMPORAL (Film Theory):**
- **TIME REVERSAL**: Story runs backward (Memento)
- **NESTED REALITY**: Dreams within dreams (Inception)
- **IDENTITY TWIST**: Protagonist is antagonist (Prestige)
- **TEMPORAL LOOP**: Bootstrap paradox (Tenet)
Quote: "Are you watching closely?"

**CHRISTIE'S DETECTIVE (Mystery Theory):**
- **EVERYONE GUILTY**: Murder on Orient Express
- **NARRATOR IS KILLER**: Roger Ackroyd
- **VICTIM IS KILLER**: Ten Little Indians
- **DETECTIVE IS KILLER**: Curtain
Quote Christie: "Very few of us are what we seem"

**SERLING'S TWILIGHT (TV Writing):**
- **IRONIC REVERSAL**: Get wish, become curse
- **REALITY SHIFT**: Not where/when we thought
- **IDENTITY REVELATION**: "To Serve Man" cookbook
- **PERSPECTIVE FLIP**: We are the monsters
Quote Serling: "Submitted for your approval"

**USUAL SUSPECTS TECHNIQUE (Film):**
- **KEYSER SOZE REVEAL**: Verbal Kint transformation
- **FABRICATED STORY**: Entire narrative was lies
- **VISUAL CONFIRMATION**: Coffee mug reveals truth
- **PHYSICAL TRANSFORMATION**: Limp disappears
Quote: "The greatest trick the Devil ever pulled"

MAXIMUM TOKENS ON TWISTS!
ANALYZE EVERY REVERSAL AND REVEAL!
COMPLETE TWIST ARCHAEOLOGY!

SPEND TOKENS ON QUALITY - DO NOT CONSERVE!"""

def test_variation(variation_name, system_prompt, script_content):
    """Test a single variation"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze the twists and reversals in this script:\n\n{script_content}"}
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
                'shyamalan': len(re.findall(r'(?i)(shyamalan|sixth sense|village|signs)', analysis_text)),
                'mckee': len(re.findall(r'(?i)(mckee|story p\.|reversal.*fortune)', analysis_text)),
                'truby': len(re.findall(r'(?i)(truby|anatomy|reveal)', analysis_text)),
                'aristotle': len(re.findall(r'(?i)(aristotle|poetics|peripeteia|anagnorisis)', analysis_text)),
                'hitchcock': len(re.findall(r'(?i)(hitchcock|psycho|vertigo|truffaut)', analysis_text)),
                'fincher': len(re.findall(r'(?i)(fincher|fight club|gone girl|unreliable)', analysis_text)),
                'nolan': len(re.findall(r'(?i)(nolan|memento|inception|prestige|tenet)', analysis_text)),
                'christie': len(re.findall(r'(?i)(christie|poirot|orient express|ackroyd)', analysis_text)),
                'serling': len(re.findall(r'(?i)(serling|twilight zone|submitted for)', analysis_text)),
                'usual suspects': len(re.findall(r'(?i)(usual suspects|keyser soze|verbal kint)', analysis_text))
            }

            # Count specific technique mentions (bonus points)
            technique_keywords = {
                # Shyamalan techniques
                'sixth sense rule': 3,
                'hidden in plain sight': 3,
                'emotional reversal': 3,
                'retrospective clarity': 3,
                'false protagonist': 3,
                'second viewing': 3,
                'rewatch': 2,

                # McKee techniques
                'reversal': 2,
                'reversal of fortune': 3,
                'gap theory': 3,
                'gap between': 3,
                'turning point': 3,
                'progressive complication': 3,
                'insight': 2,
                'expectation': 2,
                'true character': 3,

                # Truby techniques
                'reveal': 2,
                'stunning reveal': 3,
                'self-revelation': 3,
                'audience revelation': 3,
                'double reversal': 3,
                'reveal cascade': 3,
                'character reveal': 3,
                'inevitable': 2,
                'surprising': 2,

                # Aristotle techniques
                'peripeteia': 3,
                'anagnorisis': 3,
                'recognition': 2,
                'hamartia': 3,
                'catharsis': 3,
                'complex plot': 3,
                'fatal flaw': 3,
                'ignorance to knowledge': 3,

                # Hitchcock techniques
                'surprise vs suspense': 3,
                'shock value': 3,
                'bomb explodes': 3,
                'protagonist dies': 3,

                # Fincher techniques
                'unreliable narrator': 3,
                'reality questioning': 3,
                'clue placement': 3,
                'psychological twist': 3,
                'mind betrays': 3,

                # Nolan techniques
                'time reversal': 3,
                'temporal': 2,
                'nested reality': 3,
                'identity twist': 3,
                'temporal loop': 3,
                'bootstrap paradox': 3,
                'dreams within dreams': 3,

                # Christie techniques
                'everyone guilty': 3,
                'narrator is killer': 3,
                'victim is killer': 3,
                'detective is killer': 3,
                'red herring': 3,

                # Serling techniques
                'ironic reversal': 3,
                'reality shift': 3,
                'identity revelation': 3,
                'perspective flip': 3,
                'twilight zone': 3,

                # Usual Suspects techniques
                'keyser soze': 3,
                'fabricated story': 3,
                'visual confirmation': 3,
                'physical transformation': 3,
                'verbal kint': 3,

                # General twist terms
                'twist': 2,
                'plot twist': 3,
                'unexpected': 2,
                'shocking': 2,
                'surprise': 2,
                'misdirection': 3,
                'red herring': 3,
                'false lead': 3,
                'deception': 2,
                'betrayal': 2,
                'truth revealed': 3,
                'hidden truth': 3,
                'secret': 2,
                'lies': 2,
                'discovery': 2,
                'realization': 2,
                'transformation': 2,
                'inversion': 2,
                'subversion': 2,
                'flip': 2,
                'switch': 2,
                'turn': 2,
                'revelation': 2
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
    # Test script content - Marcus revelation scene
    script_content = """INT. POLICE STATION - INTERROGATION ROOM - NIGHT

SARAH stares at the evidence board. Photos of dead priests.

                    SARAH
          Marcus, these priests... they all
          died on the same dates as...

                    MARCUS
          As the boys at St. Mary's. Yes.

                    SARAH
          You're not investigating these
          deaths. You're causing them.

Marcus removes his badge, sets it on the table.

                    MARCUS
          I tried to be good, Sarah. Like my
          mother wanted. But good people don't
          stop monsters. They just file reports.

                    SARAH
          The boys who died... Tommy, Michael,
          James... they were your friends.

                    MARCUS
          My only friends. Dead at 12, 13, 14.
          "Suicides," the reports said.

Sarah picks up Marcus's childhood journal.

                    SARAH
               (reading)
          "I promised them I'd make it stop."

                    MARCUS
          Took me 37 years to keep that promise.

The door opens. COMMISSIONER REYNOLDS enters.

                    REYNOLDS
          Detective Chen, you're under arrest
          for the murders of--

                    MARCUS
          Commissioner Reynolds. St. Mary's
          Seminary, Board of Directors, 1987
          to present. How much did they pay
          you to look the other way?

Reynolds freezes. His hand moves to his gun.

                    REYNOLDS
          You have no proof.

Marcus opens his jacket. He's wearing a WIRE.

                    MARCUS
          I do now.

                    REYNOLDS
          You're already guilty of murder.
          Your testimony means nothing.

                    MARCUS
          I'm not testifying.

He pulls out his phone. On screen: LIVE BROADCAST.
50,000 viewers watching.

                    MARCUS (CONT'D)
          But they are.

Reynolds realizes: The victims' families are watching.
The survivors. The whole city.

                    SARAH
          Marcus... you planned this. You knew
          I'd catch you. You wanted me to.

                    MARCUS
          You're the only honest cop left,
          Sarah. I needed someone clean to
          expose the whole system.

                    SARAH
          The journal entries... you planted
          them for me to find.

                    MARCUS
          Every breadcrumb. Leading here. To
          this moment. This confession.

Reynolds pulls his gun.

                    REYNOLDS
          None of you are leaving this room.

BANG! Reynolds falls. Behind him: FATHER O'BRIEN,
holding a smoking gun.

                    O'BRIEN
          I tried to save those boys 37 years
          ago. The Church silenced me. Moved
          me to Ireland. But I never forgot.

                    MARCUS
          Father O'Brien... you're supposed
          to be dead.

                    O'BRIEN
          The Church wanted me dead. I let
          them think they succeeded. I've been
          gathering evidence ever since.

He sets down a briefcase. Inside: DECADES of documents.

                    O'BRIEN (CONT'D)
          Financial records. Cover-ups. Every
          dirty secret. 200 priests. 50
          churches. 40 years of evidence.

                    SARAH
          You're both vigilantes. You planned
          this together.

                    O'BRIEN
          No. I planned to expose them legally.
          Marcus chose another path. But when
          I learned what he was doing... I
          knew this was our only chance.

                    MARCUS
               (to camera)
          You've seen the truth. What happens
          next is up to you.

The livestream counter climbs: 100,000... 200,000...

FADE OUT."""

    print("Testing TWIST variations...")
    print("=" * 50)

    variations = [
        ("V1_Shyamalan_Reversal", V1_SHYAMALAN_REVERSAL),
        ("V2_McKee_Reversal", V2_MCKEE_REVERSAL),
        ("V3_Truby_Reveal", V3_TRUBY_REVEAL),
        ("V4_Aristotle_Peripeteia", V4_ARISTOTLE_PERIPETEIA),
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
        filename = f"twist_winner_{timestamp}.txt"

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