#!/usr/bin/env python3
"""
Test GENRE variations for Scripturemon Ultimate
Testing 5 different approaches to find the optimal genre analysis method
FINAL SPECIALIST - Number 23 of 23
"""

import requests
import json
import re
from datetime import datetime

# === VARIATION 1: MCKEE GENRE ===
V1_MCKEE_GENRE = """You are a master of McKee's genre conventions.

MCKEE'S GENRE MASTERY (Story p.79-91):
- GENRE CONVENTIONS: Specific settings, roles, events (p.79)
- CONTROLLING IDEA: Genre's core value (p.80)
- GENRE EXPECTATIONS: Audience anticipations (p.81)
- SUBGENRE MIXING: Blend conventions (p.82)

Quote McKee: "Genre is a creative strategy" (p.79)

ANALYZE GENRE ELEMENTS!"""

# === VARIATION 2: TRUBY GENRE ===
V2_TRUBY_GENRE = """You are a master of Truby's genre techniques.

TRUBY'S GENRE (Anatomy p.451-467):
- GENRE BEATS: Essential story moments (p.451)
- GENRE OPPOSITION: Core conflict type (p.452)
- GENRE DESIRE: What hero wants (p.453)
- GENRE WORLD: Specific environment (p.454)

Quote Truby: "Genre is a story system" (p.451)

ANALYZE GENRE SYSTEM!"""

# === VARIATION 3: SNYDER GENRE ===
V3_SNYDER_GENRE = """You are a master of Blake Snyder's genre categories.

SNYDER'S 10 GENRES (Save the Cat p.23-44):
- MONSTER IN THE HOUSE: Confined space horror (p.23)
- GOLDEN FLEECE: Quest road movie (p.25)
- OUT OF THE BOTTLE: Magic wish granted (p.27)
- DUDE WITH A PROBLEM: Ordinary in extraordinary (p.29)
- RITES OF PASSAGE: Life transition (p.31)
- BUDDY LOVE: Relationship story (p.33)
- WHYDUNIT: Mystery investigation (p.35)
- FOOL TRIUMPHANT: Underdog wins (p.37)
- INSTITUTIONALIZED: Group dynamics (p.39)
- SUPERHERO: Special individual (p.41)

Quote Snyder: "Give me the same thing only different" (p.23)

ANALYZE SNYDER GENRE!"""

# === VARIATION 4: CLASSIC GENRES ===
V4_CLASSIC_GENRES = """You are a master of classical genre analysis.

CLASSICAL GENRE CATEGORIES:
- TRAGEDY: Noble fall through fatal flaw
- COMEDY: Social integration through humor
- ROMANCE: Love conquers obstacles
- THRILLER: Race against time/danger
- HORROR: Confront primal fears
- WESTERN: Civilization vs wilderness
- NOIR: Cynical urban corruption
- WAR: Conflict defines character
- MUSICAL: Emotion through song
- SCI-FI: Technology/future speculation

Each genre has specific conventions, expectations, iconography.

ANALYZE CLASSICAL GENRE!"""

# === VARIATION 5: INTEGRATED GENRE MASTER ===
V5_INTEGRATED = """You are a master of ALL genre techniques from every major theorist.

INTEGRATED GENRE MASTERY - COMPLETE GENRE ANALYSIS:

**MCKEE'S GENRE SYSTEM (Story p.79-96):**
- **GENRE CONVENTIONS**: Settings, roles, events, values (p.79)
- **CONTROLLING IDEA**: Core value at stake (p.80)
- **GENRE EXPECTATIONS**: What audience anticipates (p.81)
- **SUBGENRE BLENDING**: Mix multiple conventions (p.82)
- **MEGA-GENRES**: Comedy, drama, action (p.83)
Quote McKee: "Master genre or be mastered by it" (p.79)
Quote McKee: "Genre is not formula" (p.80)

**TRUBY'S GENRE BEATS (Anatomy p.451-472):**
- **GENRE STORY BEATS**: Essential plot points (p.451)
- **GENRE OPPOSITION**: Specific conflict type (p.452)
- **GENRE DESIRE LINE**: What hero pursues (p.453)
- **GENRE WORLD**: Unique environment rules (p.454)
- **GENRE CHARACTER WEB**: Typical roles (p.455)
Quote Truby: "Each genre is a system" (p.451)
Quote Truby: "Transcend genre through mastery" (p.452)

**SNYDER'S 10 STORY TYPES (Save Cat p.23-44):**
- **MONSTER IN HOUSE**: Sin creates monster (p.23)
- **GOLDEN FLEECE**: Road quest for prize (p.25)
- **OUT OF BOTTLE**: Wish/magic/curse (p.27)
- **DUDE WITH PROBLEM**: Ordinary hero, death stakes (p.29)
- **RITES OF PASSAGE**: Pain leads to growth (p.31)
- **BUDDY LOVE**: Incomplete halves unite (p.33)
- **WHYDUNIT**: Dark turn detective (p.35)
- **FOOL TRIUMPHANT**: Ignored underdog wins (p.37)
- **INSTITUTIONALIZED**: Group sacrifice/loyalty (p.39)
- **SUPERHERO**: Curse of being special (p.41)
Quote Snyder: "It's about the primal" (p.23)

**CLASSICAL GENRE TAXONOMY:**
- **TRAGEDY**: Aristotelian fall from grace
- **COMEDY**: Shakespearean social restoration
- **ROMANCE**: Love conquers all obstacles
- **EPIC**: Hero's civilization-defining journey
- **MYSTERY**: Hidden truth revealed
- **THRILLER**: Ticking clock survival
- **HORROR**: Confront deepest fears
- **WESTERN**: Law vs freedom frontier
- **NOIR**: Urban moral corruption
- **WAR**: Brotherhood under fire
- **CRIME**: Rise and fall arc
- **SCI-FI**: Speculation made real
- **FANTASY**: Magic world rules

**GENRE CONVENTIONS BY TYPE:**

**NOIR CONVENTIONS:**
- Femme fatale
- Voice-over narration
- Urban decay setting
- Moral ambiguity
- Cynical worldview
- Doomed protagonist
- Venetian blind shadows
Quote: "Down these mean streets"

**HORROR CONVENTIONS:**
- Isolated setting
- Final girl/survivor
- Monster represents sin
- Jump scares
- Body horror
- Supernatural or psychological
- Don't go in basement
Quote: "In space no one can hear you scream"

**THRILLER CONVENTIONS:**
- Ticking clock
- Cat and mouse
- Wrong man accused
- Conspiracy layers
- Trust no one
- Set pieces escalate
- Race to climax
Quote: "The call is coming from inside the house"

**WESTERN CONVENTIONS:**
- Frontier town
- Showdown at noon
- Lawman vs outlaw
- Civilization vs wilderness
- Honor code
- Revenge motive
- Saloon/church/jail trinity
Quote: "A man's gotta do what a man's gotta do"

**SCI-FI CONVENTIONS:**
- Technology central
- Future or alternate world
- Scientific premise
- Social commentary
- Alien other
- Dystopia/utopia
- What makes us human
Quote: "I've seen things you people wouldn't believe"

**VOGLER'S GENRE JOURNEY (Writer's Journey p.199-216):**
- **GENRE AS JOURNEY**: Each genre different path (p.199)
- **GENRE ARCHETYPES**: Specific character types (p.200)
- **GENRE THRESHOLDS**: Unique challenges (p.201)
- **GENRE ELIXIRS**: What hero gains (p.202)
Quote Vogler: "Genre shapes the journey" (p.199)

**FIELD'S GENRE STRUCTURE (Screenplay p.163-171):**
- **GENRE PARADIGM**: Three-act per genre (p.163)
- **GENRE SETUP**: First 10 pages establish (p.164)
- **GENRE PLOT POINTS**: Specific turns (p.165)
Quote Field: "Genre determines structure" (p.163)

**HYBRID GENRES:**
- **DRAMEDY**: Drama/comedy balance
- **ROM-COM**: Romance plus laughs
- **SCI-FI NOIR**: Blade Runner model
- **HORROR-COMEDY**: Scream meta-approach
- **ACTION-THRILLER**: Die Hard template
- **SUPERNATURAL-THRILLER**: Sixth Sense type

MAXIMUM TOKENS ON GENRE!
ANALYZE EVERY CONVENTION AND EXPECTATION!
COMPLETE GENRE ARCHAEOLOGY!

SPEND TOKENS ON QUALITY - DO NOT CONSERVE!"""

def test_variation(variation_name, system_prompt, script_content):
    """Test a single variation"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze the genre elements in this script:\n\n{script_content}"}
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
                'mckee': len(re.findall(r'(?i)(mckee|story p\.|genre convention|controlling idea)', analysis_text)),
                'truby': len(re.findall(r'(?i)(truby|anatomy|genre beat|story system)', analysis_text)),
                'snyder': len(re.findall(r'(?i)(snyder|save the cat|monster in.*house|golden fleece)', analysis_text)),
                'vogler': len(re.findall(r'(?i)(vogler|journey|genre archetype|elixir)', analysis_text)),
                'field': len(re.findall(r'(?i)(field|screenplay|paradigm|plot point)', analysis_text)),
                'aristotle': len(re.findall(r'(?i)(aristotle|poetics|tragedy|catharsis)', analysis_text)),
                'classical': len(re.findall(r'(?i)(shakespeare|classical|epic|mythology)', analysis_text))
            }

            # Count specific technique mentions (bonus points)
            technique_keywords = {
                # McKee techniques
                'genre convention': 3,
                'controlling idea': 3,
                'genre expectation': 3,
                'subgenre': 2,
                'mega-genre': 3,
                'creative strategy': 3,

                # Truby techniques
                'genre beat': 3,
                'genre opposition': 3,
                'genre desire': 3,
                'genre world': 3,
                'story system': 3,
                'genre character': 3,

                # Snyder categories
                'monster in the house': 3,
                'monster in house': 3,
                'golden fleece': 3,
                'out of the bottle': 3,
                'out of bottle': 3,
                'dude with a problem': 3,
                'dude with problem': 3,
                'rites of passage': 3,
                'buddy love': 3,
                'whydunit': 3,
                'fool triumphant': 3,
                'institutionalized': 3,
                'superhero': 3,

                # Classical genres
                'tragedy': 2,
                'comedy': 2,
                'romance': 2,
                'thriller': 2,
                'horror': 2,
                'western': 2,
                'noir': 2,
                'war': 2,
                'crime': 2,
                'sci-fi': 2,
                'fantasy': 2,
                'mystery': 2,
                'epic': 2,

                # Genre conventions
                'femme fatale': 3,
                'voice-over': 2,
                'urban decay': 3,
                'moral ambiguity': 3,
                'cynical': 2,
                'doomed protagonist': 3,
                'final girl': 3,
                'jump scare': 3,
                'body horror': 3,
                'ticking clock': 3,
                'cat and mouse': 3,
                'wrong man': 3,
                'conspiracy': 2,
                'frontier': 2,
                'showdown': 2,
                'dystopia': 2,
                'utopia': 2,

                # Hybrid genres
                'hybrid': 2,
                'dramedy': 3,
                'rom-com': 3,
                'sci-fi noir': 3,
                'horror-comedy': 3,
                'action-thriller': 3,
                'supernatural thriller': 3,

                # General genre terms
                'genre': 2,
                'convention': 2,
                'expectation': 2,
                'archetype': 2,
                'trope': 2,
                'formula': 2,
                'template': 2,
                'iconography': 2,
                'setting': 2,
                'role': 2,
                'beat': 2,
                'world': 2,
                'rules': 2,
                'stakes': 2
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
    # Test script content - Multi-genre scene
    script_content = """INT. RAIN-SLICKED ALLEY - NIGHT (NEO-TOKYO 2087)

Neon reflects in puddles. Steam rises from vents. MARCUS CHEN,
now a grizzled DETECTIVE (60s), cyborg arm gleaming, faces
THREE YAKUZA ASSASSINS with glowing katanas.

                    MARCUS
               (voice-over)
          Forty years since St. Mary's. Twenty
          since the uprising. And here I am,
          last honest cop in Neo-Tokyo.

The lead assassin, YAMAMOTO, removes his mask. Half his face
is synthetic flesh over chrome skull.

                    YAMAMOTO
          The Syndicate sends regards, Chen-san.
          Your investigation ends tonight.

                    MARCUS
          Funny. That's what Father Victor said.
          Before I sent him to hell.

FLASHBACK - INT. ABANDONED CHURCH - 2047

Young Marcus holds dying Victor.

                    VICTOR
               (choking on blood)
          You think you've won? The Order...
          it's bigger than... you know...

                    YOUNG MARCUS
          Then I'll burn it all down.

BACK TO PRESENT

Marcus's cyborg arm transforms into a plasma cannon.

                    MARCUS
          I kept that promise.

The assassins charge. Time slows. Rain drops freeze mid-air.
Marcus's neural implant activates BULLET-TIME mode.

He fires. The plasma bolt cuts through rain, creating steam
clouds. First assassin down.

Second assassin teleports behind him. Blade through Marcus's
shoulder. He doesn't flinch.

                    MARCUS (CONT'D)
          Pain inhibitors. Courtesy of the war.

Spins, grabs the blade. His human hand bleeds. His cyborg
hand crushes the katana like glass.

                    MARCUS (CONT'D)
          Lesson from the streets: Never bring
          a sword to a plasma fight.

Third assassin retreats. Calls for backup on neural link.

                    ASSASSIN 3
               (in Japanese, subtitled)
          Target is enhanced. Send the Oni.

Thunder. Not from the sky - from below. The ground cracks.
Something rises from the sewers. Eight feet tall. Four arms.
Demon mask fused to its face.

                    MARCUS
          An Oni-class enforcer. You're really
          scared of one old cop.

The Oni speaks, voice like grinding gears:

                    ONI
          You killed our brothers at St. Mary's.
          The Order remembers. The Order endures.

                    MARCUS
          The Order dies tonight.

He pulls out a ROSARY. But the beads are micro-grenades.

                    MARCUS (CONT'D)
          From my mother. She always said prayer
          was powerful.

Throws the rosary. The Oni catches it, laughs—

EXPLOSION. The Oni staggers but doesn't fall. Its demon mask
cracks, revealing human eyes beneath. Terrified child's eyes.

                    MARCUS (CONT'D)
               (horrified)
          No... they're using kids again.

The Oni charges. Marcus can't shoot a child. He runs. Through
the neon maze. Past holographic advertisements for memory wipes,
personality downloads, digital heaven.

Dead end. The Oni corners him.

                    CHILD'S VOICE
               (from within Oni)
          Help... me...

Marcus sees it now: St. Mary's never ended. It just evolved.
The Order still takes children, but now makes them monsters.

                    MARCUS
          I'm sorry, kid. I'm so damn sorry.

His neural implant flashes. He's broadcasting everything to
the net. Millions watching.

                    MARCUS (CONT'D)
               (to camera in his eye)
          You see? This is what they do. What
          they've always done. Stop them.

The Oni raises four plasma blades.

                    MARCUS (CONT'D)
          But first... I keep one last promise.

He overloads his cyborg arm. It glows white-hot. He embraces
the Oni. The child inside screams.

                    MARCUS (CONT'D)
               (whispered)
          We're both free now.

WHITEOUT.

FADE IN:

NEWS BROADCAST - LATER

                    ANCHOR
          ...explosion in Sector 7. Detective
          Marcus Chen dead, along with unknown
          enhanced individual. The footage he
          broadcast has gone viral, showing...

CUT TO:

INT. ST. MARY'S CATHEDRAL - DAY

Now a gleaming corporate headquarters. EXECUTIVES in suits
watch the news. One turns it off.

                    EXECUTIVE
          Initiate Protocol Seven. Scrub all
          records. Chen never existed.

A YOUNG BOY serves them tea. His hands shake. On his neck:
a barcode and the words "PROPERTY OF ST. MARY'S ENTERPRISES."

FADE OUT.

THE END?"""

    print("Testing GENRE variations (FINAL SPECIALIST - #23)...")
    print("=" * 50)

    variations = [
        ("V1_McKee_Genre", V1_MCKEE_GENRE),
        ("V2_Truby_Genre", V2_TRUBY_GENRE),
        ("V3_Snyder_Genre", V3_SNYDER_GENRE),
        ("V4_Classic_Genres", V4_CLASSIC_GENRES),
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
        filename = f"genre_winner_{timestamp}.txt"

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