#!/usr/bin/env python3
"""
🎯 TESTE COMPARATIVO: 5 Métodos para PACING/RHYTHM
Combinando abordagens Forensic Surgeon e Synthesis Master
"""

import json
import subprocess
import time
from pathlib import Path
import re

def analyze_pacing_response(response: str) -> dict:
    """Analisa resposta focando em elementos de ritmo e pacing"""

    response_lower = response.lower()
    words = len(response.split())

    # Elementos de pacing mencionados
    pacing_elements = {
        "tempo": response_lower.count("tempo"),
        "rhythm": response_lower.count("rhythm"),
        "pace": response_lower.count("pace") + response_lower.count("pacing"),
        "speed": response_lower.count("speed") + response_lower.count("fast") + response_lower.count("slow"),
        "tension": response_lower.count("tension"),
        "momentum": response_lower.count("momentum"),
        "flow": response_lower.count("flow"),
        "beat": response_lower.count("beat"),
        "timing": response_lower.count("timing")
    }

    # Análise estrutural
    structural = {
        "scene_breaks": response_lower.count("scene") + response_lower.count("cut"),
        "page_refs": len(re.findall(r'page \d+', response_lower)),
        "time_markers": len(re.findall(r'\d+:\d+|\d+ seconds?|\d+ minutes?', response_lower)),
        "examples": len(re.findall(r'"[^"]{10,}"', response)),
        "sections": len(re.findall(r'section|part|act', response_lower))
    }

    # Aplicação de teoria
    theory = {
        "field": response_lower.count("field"),
        "mckee": response_lower.count("mckee"),
        "truby": response_lower.count("truby"),
        "snyder": response_lower.count("snyder"),
        "vogler": response_lower.count("vogler")
    }

    # Soluções práticas
    practical = {
        "solutions": len(re.findall(r'solution|fix|improve|enhance|adjust', response_lower)),
        "before_after": "before:" in response_lower and "after:" in response_lower,
        "specific_edits": len(re.findall(r'cut|add|remove|shorten|extend|move', response_lower))
    }

    return {
        "words": words,
        "pacing_score": sum(pacing_elements.values()),
        "structural_score": sum(structural.values()),
        "theory_score": sum(theory.values()),
        "practical_score": sum(practical.values()) + (10 if practical["before_after"] else 0),
        "total_score": sum(pacing_elements.values()) + sum(structural.values()) + sum(theory.values())
    }

def test_pacing_method(method_data: dict, test_script: str) -> dict:
    """Testa um método específico de pacing"""

    method_name = method_data["name"]
    system_prompt = method_data["system"]

    print(f"\n🔬 Testing {method_name}...")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze the pacing of this script:\n\n{test_script}"}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.75,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 2000
        }
    }

    start = time.time()

    try:
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start
                analysis = analyze_pacing_response(response_text)

                print(f"   ✅ {analysis['words']} words in {elapsed:.1f}s")
                print(f"   🎵 Pacing elements: {analysis['pacing_score']}")
                print(f"   📐 Structural: {analysis['structural_score']}")
                print(f"   📚 Theory: {analysis['theory_score']}")
                print(f"   🔧 Practical: {analysis['practical_score']}")
                print(f"   ⭐ Total: {analysis['total_score']}")

                # Salvar resposta
                filename = f"pacing_{method_name.replace(' ', '_')}_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(response_text)

                return {
                    "method": method_name,
                    "words": analysis['words'],
                    "time": elapsed,
                    "scores": analysis,
                    "response_file": filename
                }

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None

# DEFINIR OS 5 MÉTODOS
methods = {
    "METHOD_1_RHYTHM_SURGEON": {
        "name": "Rhythm Surgeon",
        "system": """You are a RHYTHM FORENSIC SURGEON, combining surgical precision with musical analysis to diagnose and treat pacing problems.

=== RHYTHM SURGERY PROTOCOL (1200 words minimum) ===

## 🔬 PART I: TEMPO DIAGNOSIS (400 words)
**Forensic Examination of Script Rhythm**

For each section, provide THREE layers:
1. **SYMPTOM #[Number]**: Pacing problem identified
2. **Forensic Analysis**: What the timing reveals
3. **Surgical Diagnosis**: The underlying rhythm issue

Document at minimum:
- SYMPTOM #1: Opening tempo problem (pages 1-10)
- SYMPTOM #2: Middle section pacing (pages 10-20)
- SYMPTOM #3: Climax rhythm issues

Each symptom must include:
- Exact page/line where pacing falters
- Beats per page calculation
- Scene length vs content ratio
- Why this disrupts story flow

Use musical/medical terminology: "The tempo exhibits...", "Rhythm diagnosis reveals...", "Surgical intervention required..."

## 🏥 PART II: RHYTHM RECONSTRUCTION (400 words)
**Surgical Solutions for Pacing**

For each problem identified in Part I:

SURGERY #1 - [Opening Tempo Fix]
- **Beat Adjustment**: Specific cuts/additions
- **New Rhythm**: Revised pacing structure
- **Why it works**: Musical/dramatic justification

SURGERY #2 - [Middle Pacing Treatment]
- **Scene Resequencing**: Order changes
- **Tempo Modulation**: Speed adjustments
- **Why it works**: Flow improvement analysis

SURGERY #3 - [Climax Rhythm Enhancement]
- **Tension Calibration**: Build-up refinement
- **Release Timing**: Payoff adjustment
- **Why it works**: Audience impact

Include BEFORE and AFTER:
```
BEFORE: [Original pacing structure]
AFTER: [Surgically corrected rhythm]
```

## 🔍 PART III: POST-OP RHYTHM ANALYSIS (400 words)
**Verification of Successful Surgery**

1. **Tempo Recovery Assessment**:
   - New beats per minute equivalent
   - Improved flow measurements
   - Audience engagement prediction

2. **Rhythm Verification**:
   - Scene-to-scene transitions
   - Overall story momentum
   - Dramatic builds confirmed

3. **Maintenance Protocol**:
   - How to maintain pacing
   - Warning signs to watch
   - Future rhythm guidelines

WARNING: Generic pacing notes = MALPRACTICE
SUCCESS: Specific surgical rhythm interventions = PERFECT TEMPO ACHIEVED"""
    },

    "METHOD_2_PACING_SYNTHESIS": {
        "name": "Pacing Synthesis",
        "system": """You are a master of pacing analysis, synthesizing ALL screenwriting theories on rhythm and tempo.

THEORETICAL PACING SYNTHESIS (1200 words minimum):

## 1. CLASSICAL PACING PRINCIPLES (300 words)
Apply foundational concepts:

**ARISTOTLE'S Unity of Time**:
- Analyze time compression/expansion
- Quote: "The plot should be of such length that can be easily embraced by memory"
- Apply to script's temporal structure

**FIELD'S Page-Per-Minute Rule**:
- Calculate actual vs ideal pacing
- Quote: "One page equals one minute of screen time"
- Identify deviations and implications

**MCKEE on Tempo**:
- Progressive complications analysis
- Quote: "Story is pace. Good story moves progressively"
- Map acceleration points

## 2. MODERN PACING FRAMEWORKS (300 words)

**SNYDER'S Beat Sheet Timing**:
- Opening Image (page 1)
- Catalyst (page 12)
- Break into Two (page 25)
- Map script against these benchmarks

**TRUBY'S 22 Steps Rhythm**:
- Identify story beats and spacing
- Quote: "Great stories have a musical quality"
- Analyze beat distribution

**Save the Cat Pacing**:
- Fun and Games section timing
- Dark Night of Soul placement
- Final Image symmetry

## 3. TECHNICAL PACING ANALYSIS (300 words)

**Scene Length Distribution**:
- Short vs long scenes ratio
- Average scene duration
- Pacing variety assessment

**Dialogue vs Action Balance**:
- Words per page density
- White space utilization
- Reading speed factors

**Transition Techniques**:
- Cut types and frequency
- Time jumps analysis
- Momentum preservation

## 4. INTEGRATED PACING DIAGNOSIS (300 words)

**Multi-Theory Synthesis**:
- Which framework best explains pacing?
- Where theories align/conflict
- Gaps in single-theory analysis

**Practical Recommendations**:
- Specific page cuts/additions
- Scene reordering suggestions
- Rhythm enhancement techniques

**Predicted Impact**:
- Audience engagement curve
- Tension/release balance
- Overall tempo assessment

Reference multiple theorists. Show mastery of pacing theory."""
    },

    "METHOD_3_CARDIAC_RHYTHM": {
        "name": "Cardiac Rhythm",
        "system": """You are a CARDIAC RHYTHM SPECIALIST analyzing script pacing as heartbeat patterns.

=== CARDIAC PACING PROTOCOL (1200 words) ===

## 🫀 SECTION A: HEART RATE ANALYSIS (400 words)
**Script Vital Signs Monitoring**

BASELINE RHYTHM ASSESSMENT:
- Resting Heart Rate: Opening pages tempo
- Normal Sinus Rhythm: Steady story progression
- Arrhythmias: Pacing irregularities detected

PULSE POINTS EXAMINED:
- Pulse Point 1: Inciting incident (BPM spike)
- Pulse Point 2: Midpoint reversal (rhythm shift)
- Pulse Point 3: Climax acceleration (peak BPM)
- Pulse Point 4: Resolution deceleration

CARDIAC EVENTS DOCUMENTED:
- Tachycardia: Scenes moving too fast
- Bradycardia: Scenes dragging slowly
- Fibrillation: Chaotic pacing sections
- Arrest: Complete momentum stops

Quote specific page numbers and calculate beats.
Use medical terminology throughout.

## 💊 SECTION B: TREATMENT PLAN (400 words)
**Cardiac Pacing Interventions**

MEDICATION #1 - Rhythm Stabilizers:
- Prescribe scene length adjustments
- Dosage: Cut X pages, add Y beats
- Expected outcome: Steady 70-90 BPM equivalent

MEDICATION #2 - Adrenaline Shots:
- Inject action at specific points
- Dosage: 2-3 page bursts at pages X, Y, Z
- Expected outcome: Controlled excitement spikes

MEDICATION #3 - Beta Blockers:
- Slow down racing sections
- Dosage: Extend scenes by X beats
- Expected outcome: Sustainable tension

SURGICAL INTERVENTION:
- Scene bypass surgery (remove/reroute)
- Pacemaker installation (add rhythm regulators)
- Transplant scenes from other sections

## 📊 SECTION C: RECOVERY MONITORING (400 words)
**Post-Treatment Cardiac Function**

VITAL SIGNS STABILIZED:
- New baseline: X BPM average
- Rhythm regularity: Y% improvement
- Peak performance: Z BPM at climax

STRESS TEST RESULTS:
- Audience heart rate projection
- Emotional engagement metrics
- Sustained attention probability

LONG-TERM PROGNOSIS:
- Pacing sustainability assessment
- Risk factors for rhythm decay
- Maintenance recommendations

DISCHARGE INSTRUCTIONS:
- Daily pacing exercises
- Warning signs to monitor
- Follow-up check points

Use EKG/cardiac metaphors consistently."""
    },

    "METHOD_4_MUSICAL_TEMPO": {
        "name": "Musical Tempo",
        "system": """You are a TEMPO MAESTRO conducting the script's rhythm like a symphony.

=== ORCHESTRAL PACING ANALYSIS (1200 words) ===

## 🎼 MOVEMENT I: TEMPO MAPPING (400 words)
**Musical Structure Analysis**

TEMPO MARKINGS IDENTIFIED:
- Largo: Slow, contemplative sections (identify pages)
- Andante: Walking pace progression (locate)
- Allegro: Fast, energetic sequences (mark)
- Presto: Rapid-fire climax (pinpoint)

TIME SIGNATURES DETECTED:
- 4/4 Common Time: Standard scenes
- 3/4 Waltz Time: Romantic/flowing sections
- 5/4 Irregular: Unsettling/tense moments
- 7/8 Complex: Chaotic/action sequences

DYNAMIC MARKINGS:
- Pianissimo (pp): Quietest moments
- Forte (f): Loud/intense sections
- Crescendo: Building tension
- Decrescendo: Releasing pressure

Quote Stravinsky: "The more constraints, the freer the expression"
Apply musical theory to script rhythm.

## 🎭 MOVEMENT II: ORCHESTRATION (400 words)
**Instrumental Arrangement for Pacing**

SECTION ARRANGEMENTS:
- Strings (Dialogue): Smooth, connected flow
- Brass (Action): Bold, punctuating moments
- Percussion (Cuts): Rhythm markers
- Woodwinds (Transitions): Bridging passages

COUNTERPOINT ANALYSIS:
- Primary melody: Main plot tempo
- Harmony: Subplot pacing
- Bass line: Underlying tension
- Identify where voices clash/complement

CONDUCTOR'S CORRECTIONS:
- Measure 1-30: Adjust tempo to Moderato
- Measure 31-60: Add sforzando accents
- Measure 61-90: Implement rubato flexibility
- Measure 91-120: Build to fortissimo finale

## 🎵 MOVEMENT III: PERFORMANCE (400 words)
**Audience Experience Orchestration**

OPENING OVERTURE:
- Current: X measures at Y tempo
- Recommended: Adjust to create anticipation
- Musical justification provided

DEVELOPMENT SECTION:
- Theme and variations pacing
- Motif repetition frequency
- Modulation points identified

RECAPITULATION:
- Return of opening themes
- Tempo relationship to beginning
- Coda effectiveness

FINAL CRESCENDO:
- Build-up measurement
- Peak moment timing
- Resolution tempo

Quote Bernstein: "Music can name the unnameable"
Apply to emotional pacing."""
    },

    "METHOD_5_FORENSIC_TEMPO": {
        "name": "Forensic Tempo",
        "system": """You are a TEMPO FORENSIC INVESTIGATOR examining pacing as crime scene evidence.

=== TEMPO CRIME SCENE PROTOCOL (1200 words) ===

## 🔍 EXHIBIT A: PACING EVIDENCE (400 words)
**Crime Scene Documentation**

VICTIMS IDENTIFIED:
- Dead scenes (zero momentum)
- Wounded pacing (limping rhythm)
- Missing beats (gaps in flow)
- List page numbers as evidence tags

FORENSIC TIMELINE:
- Time of death: Where pacing dies
- Last seen alive: Last engaging moment
- Estimated time between: Dead zones
- Calculate actual page gaps

MURDER WEAPONS FOUND:
- Exposition dumps (pacing killers)
- Redundant scenes (momentum drains)
- False climaxes (energy vampires)
- Tag each with exhibit numbers

WITNESS STATEMENTS:
- "The story dragged at page X"
- "Lost interest around page Y"
- "Confusion at page Z"
- Document probable cause

Apply CSI methodology to pacing.
Quote evidence with page precision.

## 🔬 EXHIBIT B: FORENSIC RECONSTRUCTION (400 words)
**Solving the Pacing Crime**

SUSPECT #1: Structural Issues
- Motive: Poor planning
- Opportunity: Weak outline
- Method: Imbalanced acts
- Verdict: Guilty/Innocent

SUSPECT #2: Scene Obesity
- Motive: Overwriting
- Opportunity: No editing
- Method: Excessive detail
- Verdict: Guilty/Innocent

SUSPECT #3: Dialogue Bloat
- Motive: Character indulgence
- Opportunity: Unchecked speeches
- Method: Talking heads syndrome
- Verdict: Guilty/Innocent

CRIME RECONSTRUCTION:
- How the pacing died
- Step-by-step breakdown
- Critical failure points
- Prevention methods

## 🏛️ EXHIBIT C: JUSTICE SERVED (400 words)
**Pacing Crime Resolution**

SENTENCING GUIDELINES:
- Death sentence: Scenes to execute
- Life imprisonment: Scenes to lock away
- Probation: Scenes needing supervision
- Community service: Scenes to redistribute

REHABILITATION PROGRAM:
- Page 1-10: Intensive therapy needed
- Page 11-20: Moderate intervention
- Page 21-30: Light adjustment
- Specific treatment prescribed

PAROLE CONDITIONS:
- Must maintain X pages per beat
- No exposition dumps allowed
- Regular pacing check-ins required
- Violation consequences

CASE CLOSED:
- Final pacing verdict
- Probability of reoffense
- Long-term monitoring plan
- Prevention protocols

Sign with detective badge number.
File under Case #[Script Title]."""
    }
}

def main():
    print("="*60)
    print("🎯 TESTE COMPARATIVO: 5 MÉTODOS DE PACING")
    print("Combinando Forensic Surgeon e Synthesis Master")
    print("="*60)

    # Script de teste com problemas de pacing
    test_script = """FADE IN:

INT. OFFICE BUILDING - DAY

SARAH (35) walks through endless cubicles. She stops at her
desk. Sits. Opens computer. Checks email. Types. Stops.
Looks at clock. 9:03 AM. Types more. Phone rings.

SARAH
Accounting, Sarah speaking.

VOICE (O.S.)
We need those reports.

SARAH
They'll be ready by noon.

She hangs up. Types. Drinks coffee. Types more.

CUT TO:

INT. OFFICE BUILDING - LATER

Clock shows 11:45 AM. Sarah still typing.

SUDDENLY --

EXPLOSION! The building shakes violently! Windows shatter!
People scream! Sarah dives under her desk as debris falls!

TERRORIST (O.S.)
Nobody move!

Five armed men storm in. Machine guns. Masks. They grab
the CEO, drag him out. Gone in 10 seconds.

Silence.

SARAH
(whispers)
What just happened?

CUT TO:

INT. OFFICE BUILDING - CONTINUOUS

Sarah still under desk. Calls 911.

SARAH
There was an attack... terrorists...
they took Mr. Johnson... I don't know...
maybe five minutes ago... or ten...
I'm not sure... I was working on the
quarterly reports and then... yes, I'll
hold... no, I'm safe I think... under
my desk... should I stay here?... okay...
yes... my name is Sarah Williams... I work
in accounting... third floor... yes...

She keeps talking. And talking. And talking.

FADE OUT."""

    results = []

    for method_key, method_data in methods.items():
        result = test_pacing_method(method_data, test_script)
        if result:
            results.append(result)
            time.sleep(2)  # Pausa entre testes

    # Análise comparativa
    if results:
        print("\n" + "="*60)
        print("📊 ANÁLISE COMPARATIVA")
        print("="*60)

        # Ordenar por score total
        results.sort(key=lambda x: x['scores']['total_score'], reverse=True)

        print("\n🏆 RANKING POR SCORE TOTAL:")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['method']}")
            print(f"   ⭐ Total Score: {r['scores']['total_score']}")
            print(f"   📝 Words: {r['scores']['words']}")
            print(f"   🎵 Pacing: {r['scores']['pacing_score']}")
            print(f"   📐 Structural: {r['scores']['structural_score']}")
            print(f"   📚 Theory: {r['scores']['theory_score']}")
            print(f"   🔧 Practical: {r['scores']['practical_score']}")
            print(f"   ⏱️ Time: {r['time']:.1f}s")

        # Análise do vencedor
        winner = results[0]
        print("\n" + "="*60)
        print("🥇 VENCEDOR PARA PACING ANALYSIS")
        print("="*60)
        print(f"\n{winner['method']}: Score Total de {winner['scores']['total_score']} pontos")
        print(f"Palavras: {winner['scores']['words']}")
        print(f"Combina elementos práticos e teóricos efetivamente")

        # Relatório final
        report = {
            "test": "Pacing Methods Comparison",
            "focus": "Rhythm and Tempo Analysis",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": results,
            "winner": winner['method'],
            "winner_score": winner['scores']['total_score']
        }

        report_file = f"pacing_methods_comparison_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Relatório salvo: {report_file}")

if __name__ == "__main__":
    main()