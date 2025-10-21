#!/usr/bin/env python3
"""
FUSÕES SIMBIÓTICAS - STORY DOCTOR + HYBRID MASTERCLASS
=======================================================
Combina os pontos fortes das duas melhores estratégias
em 5 variações diferentes para encontrar a perfeita.
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

class SymbioticStrategies:
    """5 Fusões diferentes de Story Doctor + Hybrid Masterclass"""

    def __init__(self, model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.model = model
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/symbiotic_tests")
        self.results_dir.mkdir(exist_ok=True)

    def fusion_1_medical_masterclass(self, screenplay: str) -> str:
        """Fusão 1: Estrutura médica com profundidade acadêmica"""
        return f"""
You are THE STORY DOCTOR teaching a MASTERCLASS to PhD students.
Combine clinical precision with academic depth.

=== MEDICAL MASTERCLASS PROTOCOL ===

📋 PART 1: PATIENT INTAKE & EVIDENCE EXCAVATION (350 words minimum)
"Class, let's begin with our patient's presenting symptoms..."

- Initial state (page 1): Quote "I don't need anyone. Never did."
- Chief complaint: What's the character's core problem?
- Symptom timeline: Track isolation pattern (pages 1, 15, 23, 45)
- Hidden symptoms: 3 things 99% of analysts would miss
- Quote EXACT dialogue from 5+ different moments
- Note contradictions (throws photo/retrieves it)

📊 PART 2: DIAGNOSTIC TESTS & THEORETICAL FRAMEWORK (350 words minimum)
"Now we run our diagnostic battery through multiple lenses..."

Run these diagnostic tests with page-specific results:
- McKee Test: Gap between "I don't need anyone" and retrieval action
- Truby Test: Want (isolation) vs Need (connection)
- Vogler Test: Which journey stage? (Refusal of call at page 1)
- Grief Stages Test: Where is John? (Denial → Anger → Bargaining)
- Field Test: Character = Action (throwing photo = internal chaos)

📉 PART 3: TREATMENT PLAN & COMPARATIVE ANALYSIS (350 words minimum)
"Based on our diagnosis, here's the treatment protocol..."

- What's working: Character consistency, authentic grief
- What needs treatment: Specify exact fixes with page numbers
- Medication (rewrites): Prescribe specific dialogue changes
- Compare to similar cases:
  * Rick (Casablanca): Similar isolation, different resolution
  * Michael (Godfather): Different type of loss response
  * Walter (Breaking Bad): Pride vs grief as motivator

📝 PART 4: PROGNOSIS & MASTERCLASS INSIGHTS (350 words minimum)
"The long-term outlook for this character arc..."

- Will the change last? Psychological evidence
- Risk factors for regression
- What makes this case unique in cinema history
- Hidden psychological mechanisms at play
- Your expert opinion that challenges conventional wisdom

REQUIREMENT: 1400+ words total. Each section 350+ words.
Be specific. Quote pages. Challenge assumptions.

Patient file:
{screenplay}

Begin medical masterclass:
"""

    def fusion_2_forensic_doctor(self, screenplay: str) -> str:
        """Fusão 2: Story Doctor com precisão forense"""
        return f"""
You are a FORENSIC STORY DOCTOR conducting an autopsy on this character arc.
Every cut reveals truth. Every observation is evidence.

=== FORENSIC CHARACTER AUTOPSY PROTOCOL ===

🔬 SECTION A: EXTERNAL EXAMINATION (400 words)
"Recording external observations of the subject..."

Surface presentation:
- Page 1: "I don't need anyone" - defensive posturing
- Physical state: unshaven, hollow eyes (markers of grief)
- Behavioral patterns: isolation, work avoidance (pages 15, 23)
- Quote 5 exact lines that reveal surface vs depth
- Time of death (emotional): "Three months" (page 45)
- Cause of death: "Car accident. My fault."

Evidence collection:
- Exhibit A: Photo throwing/retrieval (contradiction)
- Exhibit B: Blank screen for an hour (paralysis)
- Exhibit C: Cracked phone still playing (persistence of memory)

🧠 SECTION B: INTERNAL EXAMINATION (400 words)
"Making the Y-incision into the psyche..."

Psychological organs examined:
- EGO: Shattered by guilt ("My fault")
- SUPEREGO: Punishing through isolation
- ID: Crying out through whispered "Liar"
- Defense mechanisms: [List all with evidence]
- Wound depth: Measure trauma penetration

Apply diagnostic frameworks:
- McKee's true character: Revealed under pressure
- Truby's need/desire: Mapped anatomically
- Vogler's journey: Current stage identified
- Attachment damage: Severity assessment

🔎 SECTION C: MICROSCOPIC ANALYSIS (400 words)
"Under high magnification, we observe..."

Cellular-level patterns:
- Micro-expressions of need (hand on door handle)
- Synaptic misfires (frozen at keyboard)
- Emotional DNA (what drives John fundamentally)
- Contamination from guilt pathogen
- Comparison with reference samples:
  * Rick Blaine tissue (Casablanca)
  * Michael Corleone cells (Godfather)
  * Walter White specimen (Breaking Bad)

📋 SECTION D: CAUSE OF CHARACTER DEATH & REBIRTH (400 words)
"Final determination and recommendations..."

Official cause: [Detailed explanation]
Manner of death: [Accident/Suicide/Natural]
Contributing factors: [List all]
Possibility of resurrection: [Treatment plan]
Time to full recovery: [Projection]
Risk of relapse: [Percentage with evidence]

REQUIREMENT: 1600+ words of forensic precision.
Every claim needs evidence. Every theory needs proof.

Begin autopsy:
{screenplay}
"""

    def fusion_3_academic_diagnosis(self, screenplay: str) -> str:
        """Fusão 3: Diagnóstico acadêmico com citações teóricas"""
        return f"""
You are a HARVARD STORY DOCTOR with 30 years of academic research.
Your diagnosis combines clinical expertise with scholarly rigor.

=== ACADEMIC CLINICAL REPORT ===

📚 CHAPTER 1: LITERATURE REVIEW & INTAKE (400 words)
"According to established narrative medicine theory..."

Begin with theoretical context:
- McKee (1997) argues: "True character emerges under pressure"
- Apply to page 1: John's pressure response
- Truby (2007) states: "Need vs desire drives all arcs"
- Evidence: "I don't need anyone" (desire) vs retrieval (need)
- Vogler (1992) maps: "The hero's journey stages"
- John's position: Refusing the call (page 1-23)

Patient presentation with academic framework:
- Cite 3 peer-reviewed sources on grief in narrative
- Quote 5 specific moments with theoretical analysis
- Compare to 3 canonical examples from film history

🔬 CHAPTER 2: DIAGNOSTIC METHODOLOGY (400 words)
"Our diagnostic approach employs multiple validated instruments..."

Diagnostic Battery:
1. The McKee Gap Analysis™
   - Expected: Self-sufficiency
   - Result: Desperate retrieval
   - Gap width: Severe (clinical significance)

2. The Truby Transformation Matrix™
   - Starting point: False belief system
   - Ending point: Truth acceptance potential
   - Journey mapping: [Specific beats]

3. The Seger Arc Validator™
   - Arc authenticity: Score 1-10
   - Earning index: How earned is change?
   - Permanence projection: Will it stick?

Include footnotes, citations, theoretical challenges

📐 CHAPTER 3: COMPARATIVE CASE STUDIES (400 words)
"When we examine similar cases in the literature..."

Case Study A: Rick Blaine Syndrome
- Similar presentation: Emotional isolation
- Different etiology: Lost love vs dead love
- Treatment variance: External vs internal resolution

Case Study B: Michael Corleone Complex
- Parallel: Family loss response
- Divergence: Embrace vs reject violence
- Prognostic implications

Case Study C: Walter White Paradigm
- Contrast: Pride vs grief as driver
- Similarity: Identity transformation
- Outcome predictions

📊 CHAPTER 4: TREATMENT RECOMMENDATIONS & PROGNOSIS (400 words)
"Based on our comprehensive analysis..."

Evidence-based interventions:
1. Dialogue therapy: Specific rewrites with rationale
2. Scene surgery: What to cut/add with justification
3. Arc chemotherapy: Intensive character development

Prognosis with confidence intervals:
- 75% chance of successful transformation (evidence-based)
- 25% risk of regression (specific triggers)
- Long-term monitoring required

Publication recommendations for further study

REQUIREMENT: 1600+ words. Academic tone. Heavy citations.
Footnote format. Challenge existing theory.

Patient dossier:
{screenplay}

Begin academic clinical report:
"""

    def fusion_4_detective_doctor(self, screenplay: str) -> str:
        """Fusão 4: Story Doctor como detetive de personagem"""
        return f"""
You are DETECTIVE STORY DOCTOR, solving the mystery of this character's transformation.
Every scene is a crime scene. Every line is a clue.

=== CASE FILE: CHARACTER INVESTIGATION ===

🔍 PART 1: CRIME SCENE ANALYSIS (350 words)
"Arriving at scene, 0800 hours. Subject: JOHN, 35..."

Initial observations:
- Victim: John's former self (emotionally murdered)
- Weapon: Guilt ("My fault" - page 45)
- Time of emotional death: 3 months ago
- Last seen alive: Before Sarah's accident

Evidence catalog:
- Exhibit A: "I don't need anyone" (false alibi)
- Exhibit B: Immediate photo retrieval (confession)
- Exhibit C: Whispered "Liar" (self-incrimination)
- Exhibit D: Blank screen (catatonic state)
- Exhibit E: Cracked phone (persistent attachment)

3 clues others missed: [Detail with page refs]

🔎 PART 2: INTERROGATION & TESTIMONY (350 words)
"Psychological interrogation of the suspect/victim..."

Q: Why did you say "I don't need anyone"?
A: [Analyze John's psychological state]

Q: Why retrieve the photo immediately?
A: [Decode the contradiction]

Q: What does "Liar" reveal?
A: [Deep psychological meaning]

Cross-examination with theory:
- McKee witness: "True character under pressure..."
- Truby testimony: "Need versus desire..."
- Vogler evidence: "Hero's journey markers..."

Alibi check against similar cases:
- Rick (Casablanca): Different MO
- Michael (Godfather): Similar weapon (loss)
- Walter (Breaking Bad): Different motive

🗂️ PART 3: BUILDING THE CASE (350 words)
"Constructing the narrative of transformation..."

Timeline reconstruction:
- Pre-incident: John's life before
- Incident: Sarah's death
- Cover-up: 3 months of denial
- Discovery: Manager confrontation (page 15)
- Breakdown: Video watching (page 23)
- Confession: Therapist scene (page 45)

Motive analysis:
- Primary: Guilt-driven isolation
- Secondary: Fear of further loss
- Hidden: Self-punishment need

Psychological profile:
- Defense mechanisms: [List with evidence]
- Modus operandi: Push away before pushed
- Signature: The contradiction pattern

⚖️ PART 4: VERDICT & SENTENCING (350 words)
"Case conclusion and recommendations..."

Verdict on character arc:
- Guilty of: [Character flaws]
- Innocent of: [Undeserved blame]
- Sentence: [Transformation needed]

Rehabilitation plan:
- Phase 1: [Specific changes]
- Phase 2: [Development path]
- Phase 3: [Resolution]

Parole conditions:
- Must show genuine change
- No regression allowed
- Regular check-ins needed

Case closed assessment:
- Solved mysteries: [List]
- Remaining questions: [List]
- Cold case potential: [Areas to revisit]

REQUIREMENT: 1400+ words detective-style analysis.
Every deduction needs evidence. Build airtight case.

Case file:
{screenplay}

Begin investigation:
"""

    def fusion_5_surgical_masterclass(self, screenplay: str) -> str:
        """Fusão 5: Cirurgia narrativa com ensino masterclass"""
        return f"""
You are CHIEF SURGEON teaching a SURGICAL MASTERCLASS on character transformation.
This is a live operation. Every cut must be precise.

=== SURGICAL MASTERCLASS: CHARACTER TRANSFORMATION ===

⚕️ PROCEDURE 1: PRE-OP ASSESSMENT & PREP (350 words)
"Scrub in, everyone. Today's patient presents with severe emotional trauma..."

Patient: JOHN, 35, presenting with:
- Chief complaint: Acute grief disorder
- Onset: 3 months ago (Sarah's death)
- Symptoms: Isolation, guilt, work paralysis
- Vitals: Emotional flatline at page 1

Pre-op observations:
- "I don't need anyone" - protective scar tissue
- Photo throwing - involuntary spasm
- Immediate retrieval - healthy tissue fighting back
- "Liar" whisper - consciousness under anesthesia

Surgical plan with theoretical basis:
- McKee Incision: Cut between expectation/result
- Truby Suture: Stitch need to desire
- Vogler Graft: Transplant journey progression

Review similar surgeries:
- Rick Blaine procedure (successful)
- Michael Corleone operation (complicated)
- Walter White surgery (failed)

🔪 PROCEDURE 2: MAKING THE INCISION (350 words)
"First incision at page 1. Notice the resistance..."

Opening the character:
- Cut through defensive layer ("I don't need anyone")
- Expose the contradiction (throw/retrieve)
- Reveal the wound beneath (guilt/loss)
- Document bleeding points (emotional leaks)

Exploring the cavity:
- Page 15: Necrotic tissue (work paralysis)
- Page 23: Infection site (video watching)
- Page 45: Abscess location ("My fault")

Surgical technique notes:
- Gentle with fragile ego tissue
- Preserve healthy attachment fibers
- Remove only destructive patterns
- Cauterize self-harm tendencies

Teaching moment:
"Notice how the character tissue responds..."
[Detailed observations with theory]

🧵 PROCEDURE 3: RECONSTRUCTION & SUTURING (350 words)
"Now we rebuild the character architecture..."

Reconstruction steps:
1. Remove false belief system
2. Implant truth recognition
3. Reconnect emotional circuits
4. Restore relationship capacity

Suturing technique:
- Use McKee stitches for gap closure
- Apply Truby mesh for support
- Place Seger drains for healing
- Monitor for rejection signs

Checking the work:
- Test transformation stability
- Verify arc authenticity
- Confirm change permanence
- Look for complications

Critical teaching points:
"The key to successful character surgery is..."
[5 crucial insights with evidence]

🏥 PROCEDURE 4: POST-OP CARE & RECOVERY (350 words)
"Surgery complete. Now for recovery protocol..."

Immediate post-op:
- Character stable but fragile
- Monitor for regression
- Pain management (grief processing)
- Prevent infection (cynicism)

Recovery milestones:
- Day 1-30: Acute healing
- Day 31-90: Strengthening
- Day 91+: Integration

Discharge instructions:
- Continue therapy scenes
- Avoid isolation triggers
- Build support network
- Regular follow-ups needed

Surgical notes for publication:
- Technique innovations
- Unexpected findings
- Lessons learned
- Future improvements

Success metrics:
- Transformation achieved: [%]
- Complications: [List]
- Prognosis: [Detailed]

REQUIREMENT: 1400+ words surgical precision.
Every cut justified. Every stitch purposeful.

Patient on table:
{screenplay}

Begin surgery:
"""

    def test_strategy(self, strategy_name: str, prompt: str) -> Tuple[str, int, float]:
        """Testa uma estratégia e retorna output, word count e tempo"""

        logger.info(f"🧬 Testing {strategy_name}...")

        start_time = time.time()

        # Call Ollama API
        api_url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 5000,  # Máximo
                "temperature": 0.8,    # Sweet spot encontrado
                "top_p": 0.95,
                "num_ctx": 131072,
                "repeat_penalty": 1.0,
                "top_k": 100,
                "seed": 42
            }
        }

        try:
            response = requests.post(api_url, json=payload, timeout=300)

            if response.status_code == 200:
                result_json = response.json()
                output = result_json.get("response", "")

                elapsed = time.time() - start_time
                word_count = len(output.split())

                logger.info(f"   ✅ Complete: {word_count} words in {elapsed:.1f}s")

                # Save result
                result_file = self.results_dir / f"{strategy_name}_{int(time.time())}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "strategy": strategy_name,
                        "word_count": word_count,
                        "elapsed": elapsed,
                        "output": output
                    }, f, indent=2, ensure_ascii=False)

                return output, word_count, elapsed

            else:
                logger.error(f"API error: {response.status_code}")
                return "", 0, 0

        except Exception as e:
            logger.error(f"Exception: {e}")
            return "", 0, 0

    def run_all_fusions(self, screenplay: str) -> Dict[str, Any]:
        """Testa todas as 5 fusões simbióticas"""

        logger.info("=" * 60)
        logger.info("🧬 TESTE DE FUSÕES SIMBIÓTICAS")
        logger.info("=" * 60)

        strategies = {
            "fusion_1_medical_masterclass": self.fusion_1_medical_masterclass(screenplay),
            "fusion_2_forensic_doctor": self.fusion_2_forensic_doctor(screenplay),
            "fusion_3_academic_diagnosis": self.fusion_3_academic_diagnosis(screenplay),
            "fusion_4_detective_doctor": self.fusion_4_detective_doctor(screenplay),
            "fusion_5_surgical_masterclass": self.fusion_5_surgical_masterclass(screenplay)
        }

        results = {}

        for name, prompt in strategies.items():
            output, words, elapsed = self.test_strategy(name, prompt)

            results[name] = {
                "word_count": words,
                "elapsed": elapsed,
                "output": output[:500] + "..." if output else "FAILED"
            }

        # Rank by word count
        ranked = sorted(results.items(), key=lambda x: x[1]["word_count"], reverse=True)

        print("\n" + "=" * 60)
        print("🏆 RESULTADOS DAS FUSÕES")
        print("=" * 60)

        for i, (name, data) in enumerate(ranked, 1):
            print(f"\n{i}º {name}")
            print(f"   📝 Palavras: {data['word_count']}")
            print(f"   ⏱️ Tempo: {data['elapsed']:.1f}s")
            print(f"   ✅ Meta 1400: {'SIM' if data['word_count'] >= 1400 else 'NÃO'}")

        # Save final report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "winner": ranked[0][0],
            "rankings": ranked,
            "target_achieved": any(d["word_count"] >= 1400 for _, d in ranked)
        }

        report_file = self.results_dir / f"symbiotic_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

# Teste principal
if __name__ == "__main__":

    # Screenplay para teste
    test_screenplay = """
    FADE IN:

    INT. APARTMENT - DAY (PAGE 1)

    JOHN (35), unshaven, hollow eyes, stares at a framed photo
    of SARAH (30s, radiant smile). His hands shake.

    JOHN
    (to photo)
    I don't need anyone. Never did.

    He throws the photo in the trash. The glass SHATTERS.
    Beat. He immediately retrieves it, cutting his hand.

    JOHN (CONT'D)
    (whispered)
    Liar.

    INT. OFFICE - DAY (PAGE 15)

    John sits alone. MANAGER approaches.

    MANAGER
    John, you joining us for drinks?

    JOHN
    Got work.

    His screen has been blank for an hour.

    INT. APARTMENT - NIGHT (PAGE 23)

    John watches old videos. Sarah's voice echoes.

    SARAH (ON VIDEO)
    You can't push everyone away forever.

    John throws the phone. It cracks but keeps playing.

    INT. THERAPIST'S OFFICE - DAY (PAGE 45)

    THERAPIST
    Why did you come today?

    JOHN
    My manager made me.

    THERAPIST
    No one can make you be here.

    John's leg bounces. Hand on door handle.

    JOHN
    (barely audible)
    She's dead. Three months.
    Car accident. My fault.
    """

    tester = SymbioticStrategies()

    print("\n🧬 INICIANDO TESTE DE FUSÕES SIMBIÓTICAS")
    print("Combinando: STORY DOCTOR + HYBRID MASTERCLASS")
    print("Meta: 1400+ palavras com profundidade máxima")
    print("=" * 60)

    report = tester.run_all_fusions(test_screenplay)

    print(f"\n📁 Resultados salvos em: {tester.results_dir}")

    if report["target_achieved"]:
        print("\n🎉 SUCESSO! Pelo menos uma fusão alcançou 1400+ palavras!")
    else:
        print("\n⚠️ Nenhuma fusão alcançou 1400 palavras ainda")