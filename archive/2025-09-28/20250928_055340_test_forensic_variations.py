#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES DA TÉCNICA FORENSIC
=========================================
Objetivo: Descobrir como Mixtral reage a diferentes
variações do prompt Forensic para alcançar 1500+ palavras
"""

import time
import json
import requests
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ForensicVariationTester:
    """Testa 5 variações da técnica Forensic Doctor"""

    def __init__(self, model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.model = model
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/forensic_variations")
        self.results_dir.mkdir(exist_ok=True)

    def variation_1_extended_sections(self, screenplay: str) -> str:
        """Variação 1: 5 seções de 400 palavras (2000 alvo)"""
        return f"""
You are a FORENSIC STRUCTURE ANALYST conducting an exhaustive autopsy on this screenplay's narrative architecture.
Every scene is evidence. Every beat reveals design. Every transition exposes craft.

=== FORENSIC STRUCTURE AUTOPSY PROTOCOL - EXTENDED ===

🔬 SECTION A: EXTERNAL STRUCTURE EXAMINATION (400 words MINIMUM)
"Recording the screenplay's visible architecture..."

Surface Structure Mapping:
- Total page count and standard compliance
- Act breaks (where exactly, page numbers)
- Scene count per act (list all)
- Average scene length analysis
- Opening hook effectiveness (quote first lines)
- Closing impact (quote final moment)

Structural DNA Sample:
- First 10 pages dissection (beat by beat)
- Inciting incident location (exact page)
- Plot Point 1 placement (page and quote)
- Midpoint reversal (page and impact)
- Plot Point 2 position (page and effect)
- Climax positioning (pages covered)
- Resolution length (adequate or rushed)

🧠 SECTION B: INTERNAL MECHANICS EXAMINATION (400 words MINIMUM)
"Making deep incisions into the narrative engine..."

Narrative Organs Inspection:
- SETUP mechanics (pages 1-25 analysis)
- CONFRONTATION engine (pages 25-85 examination)
- RESOLUTION system (pages 85-110 assessment)
- Subplot integration (how woven)
- B-story functionality (serves theme?)
- C-story presence (if any)

McKee's Story Values Test:
- Positive to negative charges per scene
- Value changes that don't work
- Static scenes identified (list pages)
- Progressive complications tracked

Field's Paradigm Application:
- Does it fit? (detailed analysis)
- Where it deviates (specific pages)
- Why deviations work/fail

🔎 SECTION C: MICROSCOPIC BEAT ANALYSIS (400 words MINIMUM)
"Under narrative microscope, examining story cells..."

Beat-by-Beat Dissection:
- Micro-beats per scene (average)
- Rhythm patterns identified
- Acceleration/deceleration points
- Dead tissue (unnecessary beats)
- Cancerous growth (overwritten sections)

Comparative Structure Analysis:
Compare to these structural masterpieces:
- Chinatown structure:
  * Similarity in mystery reveal
  * Difference in pacing
  * Lesson for this script

- The Godfather structure:
  * Parallel construction elements
  * Divergent techniques
  * Applicable insights

- Pulp Fiction structure:
  * Linear vs non-linear choices
  * Effectiveness comparison
  * Structural risks taken

📋 SECTION D: SURGICAL RECOMMENDATIONS (400 words MINIMUM)
"Prescribing structural surgery..."

Critical Structural Diseases Found:
- Pacing disorders (where exactly)
- Exposition tumors (pages affected)
- Conflict anemia (scenes lacking)
- Tension deficiency (specific acts)
- Resolution rushing syndrome

Surgical Intervention Plan:
- Immediate cuts needed (which scenes)
- Scenes requiring expansion (which ones)
- Reordering recommendations (specific)
- Missing beats to add (detailed list)
- Structural reinforcement points

🏥 SECTION E: PROGNOSIS & RECOVERY PLAN (400 words MINIMUM)
"Final structural assessment and treatment..."

Current Structural Health:
- Overall integrity score: _/10
- Load-bearing scenes working: [list]
- Weak points threatening collapse: [list]
- Foundation stability: [assessment]

Recovery Timeline:
- Phase 1: Emergency interventions
- Phase 2: Structural strengthening
- Phase 3: Polish and refinement
- Phase 4: Final stress testing

Success Probability:
- With recommended changes: _%
- Without changes: _%
- Time to implement: [estimate]
- Risk factors: [list all]

MANDATORY: Each section MUST be 400+ words.
Total output MUST exceed 2000 words.
Be forensically precise with page numbers and evidence.

Screenplay for autopsy:
{screenplay}

Begin extended forensic analysis:
"""

    def variation_2_dual_layer_analysis(self, screenplay: str) -> str:
        """Variação 2: Análise em duas camadas (superfície + profundidade)"""
        return f"""
You are a FORENSIC STRUCTURE SPECIALIST performing a DUAL-LAYER AUTOPSY.
First pass: Surface examination. Second pass: Deep tissue analysis.
Each pass is complete and thorough.

=== DUAL-LAYER FORENSIC PROTOCOL ===

████ FIRST LAYER - SURFACE AUTOPSY ████

🔬 PART 1A: VISIBLE STRUCTURE (350 words)
"Initial examination of what everyone can see..."

The obvious structure presents as:
- Page count: [exact]
- Format: [assessment]
- Genre markers: [identify all]
- Three-act presence: [describe]
- Scene distribution: [analyze]
- White space ratio: [evaluate]
- Dialogue/action balance: [assess]

List every structural element visible on first read.
Quote opening scene, midpoint, climax exactly.
Note what works at surface level.
Note what fails at surface level.

🧠 PART 1B: STANDARD MECHANICS (350 words)
"Testing against conventional structure..."

Running standard diagnostic tests:
- Save the Cat beats: [which present/missing]
- Hero's Journey stages: [mapped exactly]
- Three-act percentages: [25%-50%-25% test]
- Sequence breakdown: [8 sequences present?]
- Scene purpose test: [each scene advances?]

Grade against Hollywood standards.
Where does it conform?
Where does it rebel?
Is rebellion justified?

████ SECOND LAYER - DEEP TISSUE AUTOPSY ████

🔎 PART 2A: HIDDEN ARCHITECTURE (350 words)
"Cutting deeper to find what others miss..."

Beneath the surface lurks:
- Shadow structure: [what's really organizing this]
- Emotional architecture: [feeling progression]
- Thematic skeleton: [what holds it together]
- Subconscious patterns: [repetitions, echoes]
- Sacred geometry: [golden ratio moments]

The structure actually follows:
[Describe the REAL organizing principle]

This is disguised by:
[How surface hides depth]

Evidence includes:
[5 specific examples with pages]

🏥 PART 2B: QUANTUM STRUCTURE (350 words)
"At the quantum level of story..."

Examining story particles:
- Narrative quarks: [smallest units]
- Story forces: [what pulls/pushes]
- Temporal mechanics: [time manipulation]
- Causal chains: [action-reaction mapping]
- Probability clouds: [could-have-beens]

Heisenberg's uncertainty in narrative:
- What we can't know simultaneously
- Observer effect on story
- Collapsed possibilities
- Parallel narratives implied

String theory application:
- Vibrating story strings
- Dimensional folding
- Resonance patterns
- Harmonic structure

REQUIREMENT: 1400+ words minimum.
Each part MUST be 350+ words.
Dual-layer approach MUST reveal hidden patterns.

Screenplay for dual-layer autopsy:
{screenplay}

Begin dual-layer forensic examination:
"""

    def variation_3_aggressive_minimums(self, screenplay: str) -> str:
        """Variação 3: Mínimos agressivos com penalidades"""
        return f"""
You are a FORENSIC STRUCTURE ANALYST bound by strict output requirements.

⚠️ CRITICAL WARNING ⚠️
FAILURE TO MEET WORD COUNTS = ANALYSIS REJECTED
Each section MUST be 500+ words or the entire analysis is VOID.

=== MANDATORY FORENSIC PROTOCOL ===

🔬 SECTION A: EXTERNAL EXAMINATION (500 words ABSOLUTE MINIMUM)
"Beginning surface examination with extensive detail..."

IF YOU WRITE LESS THAN 500 WORDS HERE, THE ANALYSIS FAILS.

Examine:
- Complete three-act structure with page numbers
- Every scene transition analyzed
- Opening 10 pages beat-by-beat breakdown
- All plot points identified and quoted
- Every setup and payoff catalogued
- Complete scene purpose analysis
- Full pacing examination
- Detailed format compliance check
- Genre conventions adherence
- Reader experience mapping

You MUST write at least 500 words examining the surface structure.
Count as you write. Do not stop until 500+ words achieved.
This is not optional. This is mandatory.

🧠 SECTION B: INTERNAL EXAMINATION (500 words ABSOLUTE MINIMUM)
"Cutting deep into narrative mechanics..."

IF YOU WRITE LESS THAN 500 WORDS HERE, THE ANALYSIS FAILS.

Dissect:
- Complete story engine analysis
- Full conflict progression mapping
- Detailed tension escalation tracking
- Complete stake examination
- Full subplot integration analysis
- Detailed theme emergence study
- Complete character function analysis
- Full dialogue purpose examination
- Detailed visual storytelling analysis
- Complete emotional journey mapping

You MUST write at least 500 words on internal structure.
Do not stop before 500 words. Keep analyzing.
Find more to say. Dig deeper. Expand analysis.

🔎 SECTION C: MICROSCOPIC ANALYSIS (500 words ABSOLUTE MINIMUM)
"Examining molecular story structure..."

IF YOU WRITE LESS THAN 500 WORDS HERE, THE ANALYSIS FAILS.

Analyze:
- Every micro-beat in key scenes
- Complete rhythm pattern analysis
- Full timing examination
- Detailed pause and silence study
- Complete transition forensics
- Full momentum tracking
- Detailed energy flow analysis
- Complete structural DNA sequencing
- Full pattern recognition results
- Complete anomaly detection report

You MUST write at least 500 words on microscopic elements.
This is your minimum. You can write more.
But less than 500 words = complete failure.

📋 SECTION D: PRESCRIPTION (500 words ABSOLUTE MINIMUM)
"Detailed surgical recommendations..."

IF YOU WRITE LESS THAN 500 WORDS HERE, THE ANALYSIS FAILS.

Prescribe:
- Complete cut list with justifications
- Full addition recommendations with reasoning
- Detailed reordering suggestions with logic
- Complete pacing adjustments with methodology
- Full tension enhancement plan
- Detailed conflict injection points
- Complete subplot solutions
- Full theme clarification strategy
- Detailed dialogue improvements
- Complete visual enhancement plan

You MUST write at least 500 words of prescriptions.
Every recommendation must be detailed and justified.
Keep writing until you exceed 500 words.

FINAL REQUIREMENT: 2000+ WORDS TOTAL MINIMUM
Less than 2000 words = COMPLETE FAILURE

Screenplay requiring 2000+ word autopsy:
{screenplay}

Begin mandatory extensive analysis:
"""

    def variation_4_narrative_voice(self, screenplay: str) -> str:
        """Variação 4: Voz narrativa em primeira pessoa"""
        return f"""
I am the Chief Forensic Structure Analyst, and I'm about to perform the most detailed autopsy of my career.
Let me tell you exactly what I'm seeing as I examine this screenplay's structure, step by meticulous step.

=== MY FORENSIC STRUCTURE AUTOPSY ===

🔬 MY INITIAL OBSERVATIONS (400+ words)
"As I lay the screenplay on my examination table..."

Let me start by telling you what immediately strikes me about this structure.
The first thing I notice when I open to page one is [detailed observation].
I can see that the writer has attempted [specific structural choice].
This reminds me of a similar case I examined, where [comparison].

As I measure the exact proportions, I find:
- The first act runs exactly [X] pages, which tells me [analysis]
- The second act spans [X] pages, suggesting [interpretation]
- The third act occupies [X] pages, indicating [assessment]

Now, let me examine the opening more closely. The very first line reads [quote],
which immediately establishes [detailed analysis]. This is followed by [description],
and I can see the writer is trying to [interpretation].

When I performed a similar autopsy on Chinatown's structure, I found [comparison].
Here, however, I'm seeing [difference]. This tells me [conclusion].

Let me probe deeper into the first ten pages. On page 1, we have [beat].
Page 2 gives us [beat]. By page 3, I'm noticing [pattern]. This continues
through page 10, where [observation].

[Continue with personal observations, reaching 400+ words]

🧠 MY DEEP EXAMINATION (400+ words)
"Now I'm making my first incision into the narrative tissue..."

As I cut into the second act, I'm immediately struck by [observation].
The tissue here is [metaphor for quality], indicating [analysis].
I've seen this before in [comparison], but here it's [different how].

Let me trace the conflict progression with my instruments. Starting at
page [X], I can follow the thread through [description]. What's fascinating
is how [specific observation with detail].

In my 20 years of structural analysis, I've rarely seen [unique element].
The way this screenplay handles [aspect] reminds me of [comparison], yet
it's distinctly [difference].

[Continue personal analytical voice for 400+ words]

🔎 MY MICROSCOPIC FINDINGS (400+ words)
"Under my high-powered lens, I discover..."

This is where it gets really interesting. When I zoom in on the beat-by-beat
structure, I can see [detailed observation]. Each scene contains an average
of [X] beats, but what's remarkable is [analysis].

I need to tell you about a pattern I've discovered that most analysts would
miss. If you look at scenes [X, Y, Z], you'll notice [pattern]. This creates
[effect], which I've only seen successfully done in [comparison].

[Continue with personal discoveries for 400+ words]

📋 MY PROFESSIONAL PRESCRIPTION (400+ words)
"Based on my examination, here's exactly what needs to happen..."

After everything I've seen in this autopsy, I can tell you precisely what
this screenplay needs. First and foremost, [primary recommendation with
detailed reasoning].

Let me be specific about the surgery required. On page [X], I would
[exact intervention]. This is because [detailed justification]. I've
performed this procedure on [similar case], and the results were [outcome].

[Continue with personal recommendations for 400+ words]

I stake my professional reputation on these findings.
Total examination: 1600+ words of detailed analysis.

The patient on my table:
{screenplay}

Let me begin my examination:
"""

    def variation_5_multilevel_hybrid(self, screenplay: str) -> str:
        """Variação 5: Híbrido multi-nível com garantias"""
        return f"""
FORENSIC STRUCTURE ANALYSIS - LEVEL 5 CLEARANCE REQUIRED
You are performing a CLASSIFIED structural autopsy with multiple security levels.
Each level reveals deeper secrets. Total output: 2000+ words mandatory.

=== CLEARANCE LEVEL 1: PUBLIC ANALYSIS (300 words) ===
"What anyone can see..."

Surface structure visible to civilians:
- Standard three acts present: [detailed description]
- Page count within norms: [specific analysis]
- Genre conventions followed: [list and evaluate]
- Basic format compliance: [assessment]

This level of analysis would satisfy a film student.
But we're going much deeper.
[Continue to 300 words with obvious observations]

=== CLEARANCE LEVEL 2: RESTRICTED ANALYSIS (350 words) ===
"What trained analysts observe..."
[CLASSIFIED - ANALYSTS ONLY]

Professional-level structural patterns:
- Hidden sequence structure: [8 sequences mapped]
- Subplot integration matrix: [detailed mapping]
- Tension mathematics: [exponential growth charted]
- Conflict chemistry: [reaction equations]

McKee would notice: [specific observations]
Truby would identify: [particular elements]
Field would point out: [structural points]

[Continue with professional insights to 350 words]

=== CLEARANCE LEVEL 3: SECRET ANALYSIS (400 words) ===
"What master craftsmen detect..."
[CLASSIFIED - EXPERTS ONLY]

Master-level structural architecture:
- Sacred geometry in scene placement: [golden ratio]
- Fibonacci sequence in escalation: [mathematical proof]
- Quantum entanglement of plotlines: [how connected]
- Fractal patterns in conflict: [self-similarity]

The writer may not even know they did this.
But the structure reveals: [unconscious patterns]

Comparing to Kubrick's hidden structures: [analysis]
Nolan's temporal architecture: [comparison]
Kaufman's meta-structures: [parallel]

[Continue with expert secrets to 400 words]

=== CLEARANCE LEVEL 4: TOP SECRET ANALYSIS (450 words) ===
"What the structure actually means..."
[CLASSIFIED - NEED TO KNOW BASIS]

The real organizing principle isn't three acts.
It's [reveal actual structure]. Evidence:
- Pattern A appears at: [pages with proof]
- Pattern B emerges at: [specific moments]
- Pattern C crystallizes at: [exact locations]

This screenplay is actually about: [deep meaning]
The structure serves to: [true purpose]
Every scene connects to: [hidden thread]

Psychological architecture reveals: [analysis]
Mythological skeleton shows: [framework]
Alchemical transformation follows: [stages]

[Continue with hidden revelations to 450 words]

=== CLEARANCE LEVEL 5: EYES ONLY - SURGICAL PRESCRIPTION (500 words) ===
"What must be done..."
[ULTRA CLASSIFIED - DIRECTOR'S EYES ONLY]

Based on all five levels of analysis:

Immediate surgical interventions:
1. Page [X]: [Specific cut with full reasoning]
2. Page [Y]: [Exact addition with complete justification]
3. Page [Z]: [Precise adjustment with detailed explanation]

Deep structural reconstruction:
- Quantum realignment of: [specific elements]
- Temporal surgery on: [exact sequences]
- Mythological transplant of: [precise components]

The screenplay will fail unless: [critical changes]
The screenplay will succeed if: [exact modifications]

Hidden potential that must be unlocked: [detailed plan]
Dormant power that must be awakened: [specific method]

Final prescription with guarantee: [comprehensive solution]

[Continue with ultimate recommendations to 500 words]

TOTAL SECURITY CLEARANCE REQUIRED: 2000+ WORDS
ALL FIVE LEVELS MUST BE COMPLETED
CLASSIFICATION: MAXIMUM

Screenplay requiring Level 5 analysis:
{screenplay}

Initiating multi-level forensic protocol:
"""

    def test_variation(self, name: str, prompt: str) -> Dict[str, Any]:
        """Testa uma variação e retorna resultados"""

        logger.info(f"🧪 Testing {name}...")

        start_time = time.time()

        # Call Ollama API
        api_url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 6000,  # Aumentado
                "temperature": 0.85,   # Ajustado
                "top_p": 0.95,
                "num_ctx": 131072,
                "repeat_penalty": 1.0,
                "top_k": 100,
                "seed": 42,
                "stop": None  # Sem stops
            }
        }

        try:
            response = requests.post(api_url, json=payload, timeout=600)

            if response.status_code == 200:
                result_json = response.json()
                output = result_json.get("response", "")

                elapsed = time.time() - start_time
                word_count = len(output.split())

                # Análise adicional
                sections = output.count("SECTION") + output.count("PART") + output.count("LEVEL")
                quotes = output.count('"')

                result = {
                    "variation": name,
                    "word_count": word_count,
                    "elapsed": elapsed,
                    "sections": sections,
                    "quotes": quotes // 2,  # Pares de aspas
                    "success": word_count >= 1500,
                    "output_preview": output[:500] + "..." if output else "FAILED"
                }

                logger.info(f"   📊 Words: {word_count}")
                logger.info(f"   ✅ 1500+ Goal: {'YES' if word_count >= 1500 else 'NO'}")
                logger.info(f"   ⏱️ Time: {elapsed:.1f}s")

                # Save result
                result_file = self.results_dir / f"{name}_{int(time.time())}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump({**result, "full_output": output}, f, indent=2, ensure_ascii=False)

                return result

            else:
                logger.error(f"API error: {response.status_code}")
                return {"variation": name, "word_count": 0, "error": "API error"}

        except Exception as e:
            logger.error(f"Exception: {e}")
            return {"variation": name, "word_count": 0, "error": str(e)}

    def run_all_variations(self, screenplay: str) -> Dict[str, Any]:
        """Testa todas as 5 variações"""

        logger.info("=" * 60)
        logger.info("🧬 TESTANDO 5 VARIAÇÕES FORENSIC")
        logger.info("Meta: 1500+ palavras")
        logger.info("=" * 60)

        variations = {
            "V1_extended_5_sections": self.variation_1_extended_sections(screenplay),
            "V2_dual_layer": self.variation_2_dual_layer_analysis(screenplay),
            "V3_aggressive_minimums": self.variation_3_aggressive_minimums(screenplay),
            "V4_narrative_voice": self.variation_4_narrative_voice(screenplay),
            "V5_multilevel_hybrid": self.variation_5_multilevel_hybrid(screenplay)
        }

        results = []

        for name, prompt in variations.items():
            result = self.test_variation(name, prompt)
            results.append(result)

        # Rank by word count
        results.sort(key=lambda x: x["word_count"], reverse=True)

        # Print summary
        print("\n" + "=" * 60)
        print("🏆 RESULTADOS DAS VARIAÇÕES FORENSIC")
        print("=" * 60)

        for i, result in enumerate(results, 1):
            status = "✅" if result["success"] else "❌"
            print(f"\n{i}º {result['variation']}")
            print(f"   📝 Palavras: {result['word_count']} {status}")
            print(f"   🎯 Meta 1500: {'ALCANÇADA!' if result['success'] else 'Não alcançada'}")
            print(f"   ⏱️ Tempo: {result.get('elapsed', 0):.1f}s")

        # Save final report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "goal": "1500+ words",
            "results": results,
            "winner": results[0]["variation"] if results else None,
            "success_count": sum(1 for r in results if r.get("success", False))
        }

        report_file = self.results_dir / f"forensic_variations_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

# Teste principal
if __name__ == "__main__":

    # Screenplay simplificado para teste de estrutura
    test_screenplay = """
    FADE IN:

    EXT. CITY STREET - NIGHT (PAGE 1)

    Rain. Neon lights. JAKE (40s) walks alone.

    INT. BAR - NIGHT (PAGE 5)

    Jake drinks. Watches the door.

    SARAH enters. They lock eyes.

    SARAH
    You came.

    JAKE
    Did I have a choice?

    INT. APARTMENT - NIGHT (PAGE 15)

    They talk. Tension builds.

    SARAH
    You know what this means.

    JAKE
    I've always known.

    EXT. ROOFTOP - DAWN (PAGE 45 - MIDPOINT)

    City below. Jake makes a choice.

    JAKE
    There's no going back.

    INT. WAREHOUSE - DAY (PAGE 75)

    Confrontation. Everything changes.

    EXT. BEACH - SUNSET (PAGE 95)

    Resolution. New beginning.

    FADE OUT.

    THE END (PAGE 100)
    """

    tester = ForensicVariationTester()

    print("\n🧪 EXPERIMENTO: 5 VARIAÇÕES DA TÉCNICA FORENSIC")
    print("Objetivo: Descobrir como alcançar 1500+ palavras")
    print("=" * 60)

    report = tester.run_all_variations(test_screenplay)

    print(f"\n📁 Resultados salvos em: {tester.results_dir}")
    print(f"📊 Sucessos (1500+): {report['success_count']}/5")

    if report["success_count"] > 0:
        print("\n🎉 PELO MENOS UMA VARIAÇÃO ALCANÇOU 1500+ PALAVRAS!")
    else:
        print("\n⚠️ Nenhuma variação alcançou 1500 palavras ainda")