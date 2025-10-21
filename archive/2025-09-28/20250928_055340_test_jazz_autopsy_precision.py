#!/usr/bin/env python3
"""
🎯 TESTE ESPECÍFICO: Jazz Autopsy vs Forensic Puro
Verifica se a fusão realmente evita invenções do Jazz
"""

import json
import time
import subprocess
from pathlib import Path
import re

def analyze_for_inventions(response: str) -> dict:
    """Detecta invenções específicas do Jazz"""

    response_lower = response.lower()

    # Invenções típicas do Jazz
    jazz_inventions = {
        "bpm": bool(re.search(r'\d+ (?:bpm|beats per minute)', response_lower)),
        "musical_modes": bool(re.search(r'(?:dorian|lydian|phrygian|mixolydian) (?:mode|scale)', response_lower)),
        "trading_fours": "trading fours" in response_lower,
        "chord_progressions": bool(re.search(r'[A-G](?:#|b)? (?:major|minor)', response_lower)),
        "frequencies_hz": bool(re.search(r'\d+ (?:hz|hertz)', response_lower)),
        "measures": bool(re.search(r'measure \d+', response_lower)),
        "bars": bool(re.search(r'bar \d+', response_lower)),
        "verse_chorus": "verse-chorus" in response_lower or "verse and chorus" in response_lower,
    }

    # Elementos factuais do Forensic
    forensic_elements = {
        "evidence": response_lower.count("evidence"),
        "autopsy": response_lower.count("autopsy"),
        "forensic": response_lower.count("forensic"),
        "analysis": response_lower.count("analysis"),
        "examination": response_lower.count("examination"),
        "quotes": len(re.findall(r'"[^"]{10,}"', response)),  # Citações diretas
    }

    return {
        "inventions": jazz_inventions,
        "forensic": forensic_elements,
        "total_inventions": sum(jazz_inventions.values()),
        "has_quotes": forensic_elements["quotes"] > 0
    }

def test_method(prompt_system: str, method_name: str, test_script: str):
    """Testa um método específico"""

    print(f"\n🔬 Testing {method_name}...")

    messages = [
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": f"Analyze this dialogue:\n\n{test_script}"}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 2000
        }
    }

    try:
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                analysis = analyze_for_inventions(response_text)

                print(f"   📊 Total inventions: {analysis['total_inventions']}")
                print(f"   📝 Has quotes: {analysis['has_quotes']}")
                print(f"   🔬 Forensic elements: {sum(analysis['forensic'].values())}")

                # Detalhes das invenções
                if analysis['total_inventions'] > 0:
                    print("   ❌ INVENTIONS FOUND:")
                    for key, value in analysis['inventions'].items():
                        if value:
                            print(f"      - {key}: YES")
                else:
                    print("   ✅ NO INVENTIONS!")

                return analysis, response_text

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None, None

def main():
    print("="*60)
    print("🎯 TESTE: Jazz Autopsy vs Forensic - Precisão")
    print("="*60)

    # Script de teste
    test_script = """FADE IN:

INT. OFFICE - NIGHT

DAVID (35) stares at his computer screen. His wife EMMA (33) enters.

EMMA
Still working?

DAVID
(not looking up)
Almost done.

EMMA
You said that three hours ago.

DAVID
This is important.

EMMA
(sitting beside him)
More important than us?

David finally looks at her. Sees the pain in her eyes.

DAVID
Emma, I...
(pause)
No. Nothing is.

He closes the laptop.

FADE OUT."""

    # Prompts dos métodos
    methods = {
        "Jazz_Autopsy": """You are a JAZZ PATHOLOGIST performing melodic forensics on dialogue.
Every conversation has rhythm, every silence has meaning. The dialogue is both music and evidence.

=== JAZZ FORENSIC AUTOPSY PROTOCOL (900 words) ===

🎺 SECTION 1: RHYTHMIC AUTOPSY (300 words)
**The Pulse of Death in Conversation**

Initial Cadence Examination:
Where does the beat begin?
What tempo drives the exchange?
Syncopation vs straight time.

Evidence Collection in 4/4:
- First measure: opening statement
- Second measure: response pattern
- Bridge sections: topic shifts
- Coda: how it ends

Temporal Forensics:
Time signatures of truth vs lies.
Rubato moments (freedom).
Accelerando of conflict.
Ritardando of resolution.

Jazz autopsy reveals the groove beneath words.
Each pause is forensically significant.
Swing ratio calculated precisely.

🔬 SECTION 2: IMPROVISATION EVIDENCE (300 words)
**Spontaneous Truth Under Microscope**

Call and Response Forensics:
Who leads, who follows?
Trading fours or trading blows?
The democracy of jazz dialogue.

Harmonic Evidence:
- Blue notes of sadness
- Flat fifths of tension
- Resolution to tonic (or not)

Bebop vs Cool Analysis:
Fast technical exchanges.
Or laid-back implications.
The style reveals intent.

Scat Evidence:
Non-verbal truth.
Sounds beyond words.
The primal under the polished.

Collecting final evidence.
Verdict on conversation.

🎯 SECTION 3: HARMONIC EVIDENCE (300 words)
**Proving Orchestral Crimes**

Dissonance Documentation:
Where harmony breaks down.
Augmented tensions.
Diminished relationships.

Resolution Forensics:
How conflicts resolve (or don't).
Authentic vs plagal cadences.
Deceptive resolutions.

Orchestration Violations:
- Instrumentation errors
- Balance problems
- Missing voices
- Overwhelming sections

REQUIREMENT: 900 words of orchestral forensic fusion.""",

        "Forensic_Pure": """You are a DIALOGUE FORENSIC SPECIALIST performing deep script analysis.
Your role is to examine dialogue with scientific precision, finding evidence and patterns.

=== DIALOGUE FORENSIC PROTOCOL (850 words required) ===

🔬 EVIDENCE COLLECTION (280 words)
**Initial Crime Scene Assessment**

Document every line of dialogue as evidence.
Note exact words, pauses, interruptions.
Catalog patterns of speech.
Identify verbal fingerprints.

Power dynamics through word choice.
Who questions, who answers.
Who deflects, who confronts.
The hierarchy in conversation.

Subtext examination:
What's unsaid but present.
The truth between lines.
Hidden meanings decoded.

🧪 PATTERN ANALYSIS (280 words)
**Behavioral Evidence**

Speech patterns reveal character.
Short sentences vs long.
Questions vs statements.
Active vs passive voice.

Emotional forensics:
Temperature of each exchange.
Escalation patterns.
De-escalation techniques.

Relationship dynamics:
History implied in familiarity.
Distance in formality.
Intimacy in silence.

🔍 FORENSIC RECONSTRUCTION (290 words)
**Building the Case**

Timeline of conversation.
Inciting incident.
Rising tensions.
Climax moment.
Resolution or lack thereof.

Character profiles from evidence:
What each person wants.
What they fear.
What they hide.

The verdict:
What this dialogue proves.
The truth it reveals.
The case it makes.

REQUIREMENT: Maintain forensic objectivity throughout.""",

        "Jazz_Pure": """You are a JAZZ DIALOGUE ANALYST seeing conversation as musical improvisation.
Every exchange is a jazz performance with rhythm, harmony, and spontaneity.

=== JAZZ DIALOGUE PROTOCOL (850 words) ===

🎺 RHYTHMIC ANALYSIS (280 words)
**The Beat of Conversation**

Identify the tempo: 120 BPM of normal talk, 140 BPM of argument, 80 BPM of intimacy.
Time signatures: 4/4 standard, 3/4 waltz of romance, 5/4 off-kilter tension.

Syncopation in interruptions.
Straight time in monologues.
Swing in playful banter.

The groove establishes mood.
Pocket players stay in rhythm.
Soloists break the pattern.

🎷 HARMONIC STRUCTURE (280 words)
**Chord Progressions of Dialogue**

Opening establishes key: Major for optimism, Minor for conflict.
Modulations show topic changes.
Blue notes reveal sadness.

ii-V-I progressions in resolution.
Suspended chords in uncertainty.
Diminished chords in tension.

Modal exploration:
Dorian mode for contemplation.
Mixolydian for playfulness.
Phrygian for darkness.

🎵 IMPROVISATION DYNAMICS (290 words)
**The Jazz of Spontaneity**

Call and response patterns.
Trading fours between speakers.
Comping behind the lead.

Solo moments of monologue.
Ensemble sections of agreement.
Free jazz chaos of argument.

The head: main theme stated.
The changes: variations explored.
The out: return or departure.

Jazz is conversation, conversation is jazz."""
    }

    # Testar cada método
    results = {}
    for name, prompt in methods.items():
        analysis, response = test_method(prompt, name, test_script)
        if analysis:
            results[name] = analysis

            # Salvar resposta para análise
            with open(f"{name}_test_response.txt", 'w') as f:
                f.write(response)

    # Comparação final
    print("\n" + "="*60)
    print("📊 COMPARAÇÃO FINAL")
    print("="*60)

    for name, analysis in results.items():
        print(f"\n{name}:")
        print(f"  Inventions: {analysis['total_inventions']}")
        print(f"  Has quotes: {analysis['has_quotes']}")
        print(f"  Forensic elements: {sum(analysis['forensic'].values())}")

        # Score de precisão
        precision_score = 0
        if analysis['total_inventions'] == 0:
            precision_score += 50
        if analysis['has_quotes']:
            precision_score += 25
        if sum(analysis['forensic'].values()) > 5:
            precision_score += 25

        print(f"  PRECISION SCORE: {precision_score}%")

    # Conclusão
    print("\n" + "="*60)
    print("🎯 CONCLUSÃO")
    print("="*60)

    if "Jazz_Autopsy" in results and "Forensic_Pure" in results:
        jazz_autopsy = results["Jazz_Autopsy"]
        forensic = results["Forensic_Pure"]

        print(f"\nJazz Autopsy tem {jazz_autopsy['total_inventions']} invenções")
        print(f"Forensic puro tem {forensic['total_inventions']} invenções")

        if jazz_autopsy['total_inventions'] < 3 and jazz_autopsy['has_quotes']:
            print("\n✅ Jazz Autopsy CONSEGUIU manter precisão!")
            print("A fusão funcionou - mantém criatividade sem inventar.")
        else:
            print("\n❌ Jazz Autopsy ainda tem problemas de invenção")
            print("Forensic puro continua mais preciso.")

if __name__ == "__main__":
    main()