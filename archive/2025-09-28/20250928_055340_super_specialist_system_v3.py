#!/usr/bin/env python3
"""
SISTEMA DE SUPER ESPECIALISTAS V3 - FORÇA BRUTA DE PROFUNDIDADE
================================================================
Estratégia V3:
1. Usa Chain of Thought para forçar expansão
2. Quebra análise em seções obrigatórias
3. Força mínimo por seção
4. Salva todas as tentativas para análise
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
import re
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SuperSpecialist:
    """Super Especialista com contexto massivo"""
    id: str
    name: str
    domain: str
    theoretical_framework: List[str]
    reference_scripts: List[str]
    min_output: int = 800
    max_output: int = 1500
    context_size: int = 131072

class SuperSpecialistSystemV3:
    """Sistema V3 com força bruta para garantir profundidade"""

    def __init__(self, base_model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.base_model = base_model
        self.knowledge_base = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/knowledge_packs")
        self.reference_scripts = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/reference_scripts")
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/analysis_results")
        self.results_dir.mkdir(exist_ok=True)

    def _validate_depth(self, output: str) -> Dict[str, Any]:
        """Valida se a análise tem profundidade suficiente"""

        # Conta elementos de qualidade
        page_refs = len(re.findall(r'p\.\s*\d+|page\s+\d+', output, re.I))
        quotes = len(re.findall(r'"[^"]{20,}"', output))
        comparisons = len(re.findall(r'similar to|unlike|compared to|contrast with', output, re.I))
        theory_refs = len(re.findall(r'McKee|Truby|Vogler|Seger|Field|Egri', output))

        word_count = len(output.split())

        quality_score = {
            "word_count": word_count,
            "page_references": page_refs,
            "direct_quotes": quotes,
            "comparisons": comparisons,
            "theory_references": theory_refs,
            "depth_score": (page_refs * 2 + quotes * 3 + comparisons * 2 + theory_refs) / 10
        }

        # Critérios ajustados - prioridade em palavras e profundidade
        quality_score["passed"] = (
            word_count >= 1000 or  # Se tem 1000+ palavras, aprova
            (
                word_count >= 800 and  # Ou se tem 800+ E boa profundidade
                page_refs >= 5 and
                quotes >= 3 and
                (comparisons >= 2 or theory_refs >= 10)  # Flexibilizado
            )
        )

        return quality_score

    def _build_chain_of_thought_prompt(self,
                                      specialist: SuperSpecialist,
                                      screenplay: str,
                                      attempt: int = 1) -> str:
        """Constrói prompt com Chain of Thought para forçar expansão"""

        # Instruções extra para re-tentativas
        retry_instruction = ""
        if attempt > 1:
            retry_instruction = """
🔴🔴🔴 CRITICAL WARNING 🔴🔴🔴
Your previous analysis was REJECTED for being too superficial!

MINIMUM REQUIREMENTS (NON-NEGOTIABLE):
✅ 800+ WORDS (not tokens - WORDS!)
✅ 10+ specific page references (p.XX)
✅ 5+ direct quotes from screenplay
✅ 5+ citations of theoretical frameworks
✅ 3+ comparisons with reference scripts

FAILURE TO MEET THESE = REJECTION
🔴🔴🔴 THIS IS YOUR FINAL CHANCE 🔴🔴🔴
"""

        mega_prompt = f"""
# SUPER SPECIALIST ANALYSIS SYSTEM V3
# SPECIALIST: {specialist.name}
# ATTEMPT: {attempt}/3

{retry_instruction}

## YOUR IDENTITY
You are THE world authority on {specialist.domain}.
You have studied every major work on the subject.
You must demonstrate this expertise through DEPTH and SPECIFICITY.

## CRITICAL REQUIREMENT
Your analysis MUST be AT LEAST 800 WORDS.
This is not a suggestion - it's a REQUIREMENT.
Analyses under 800 words will be REJECTED.

## THE SCREENPLAY TO ANALYZE

{screenplay}

## MANDATORY ANALYSIS STRUCTURE

You MUST complete ALL sections below.
Each section has a MINIMUM word count.
SKIP NO SECTIONS.

### SECTION 1: PATTERN RECOGNITION (minimum 200 words)
Start with: "In analyzing this screenplay's character arc, several critical patterns emerge..."

Identify AT LEAST 3 patterns. For each:
- Quote the specific page (p.XX)
- Quote the exact dialogue or action
- Explain what this reveals about the character
- Connect to theoretical framework

### SECTION 2: PSYCHOLOGICAL ARCHITECTURE (minimum 200 words)
Continue with: "The protagonist's psychological architecture reveals..."

Map the character's:
- Initial belief system (with page evidence)
- Defense mechanisms (with specific examples)
- Wound/Ghost (origin and manifestation)
- The lie they believe vs truth they need

### SECTION 3: TRANSFORMATION TIMELINE (minimum 200 words)
Continue with: "Tracking the transformation beat by beat..."

Document AT LEAST 5 key moments:
- Page number
- What happens
- Internal shift
- Resistance or acceptance
- Compare to similar moment in reference scripts

### SECTION 4: THEORETICAL ANALYSIS (minimum 200 words)
Continue with: "Through the lens of established narrative theory..."

Apply AT LEAST 3 theories:
- McKee's gap between expectation and result
- Truby's need vs desire
- Vogler's hero's journey stages
- Field's character=action principle
- Seger's transformational arc

### SECTION 5: COMPARATIVE INSIGHTS (minimum 200 words)
Continue with: "When compared to masterful character arcs..."

Compare with AT LEAST 2 reference scripts:
- Specific similarities
- Key differences
- What this screenplay does uniquely
- What it could learn from references

### SECTION 6: EXPERT VERDICT (minimum 100 words)
Conclude with: "As an expert in {specialist.domain}, my assessment..."

- Is the change earned or given?
- Psychological credibility rating
- What 99% of analysts would miss
- Specific recommendations

## THEORETICAL FRAMEWORKS YOU MUST REFERENCE

{', '.join(specialist.theoretical_framework)}

## REFERENCE SCRIPTS YOU MUST COMPARE

{', '.join(specialist.reference_scripts)}

## FINAL REMINDERS

❌ DO NOT write less than 800 words
❌ DO NOT skip any section
❌ DO NOT be vague or general
✅ DO cite specific pages
✅ DO quote exact dialogue
✅ DO reference theory by name
✅ DO compare with named films

Your reputation as an expert depends on this analysis.
Superficial work is unacceptable.

BEGIN YOUR ANALYSIS NOW:
"""
        return mega_prompt

    def analyze_with_specialist_v3(self,
                                  specialist: SuperSpecialist,
                                  screenplay: str,
                                  max_attempts: int = 3) -> Dict[str, Any]:
        """Executa análise com validação de profundidade V3"""

        logger.info(f"🔬 Starting {specialist.name} analysis V3")
        logger.info(f"   Domain: {specialist.domain}")

        all_attempts = []

        for attempt in range(1, max_attempts + 1):
            logger.info(f"   Attempt {attempt}/{max_attempts}")

            # Build prompt with Chain of Thought
            prompt = self._build_chain_of_thought_prompt(specialist, screenplay, attempt)

            start_time = time.time()

            try:
                # Use Ollama API with aggressive parameters
                api_url = "http://localhost:11434/api/generate"

                payload = {
                    "model": self.base_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 4000,      # Even more tokens
                        "temperature": 0.9,        # Higher creativity
                        "top_p": 0.95,            # Wider sampling
                        "repeat_penalty": 1.0,     # Allow repetition
                        "num_ctx": 131072,         # Max context
                        "min_length": 3000         # Try to force minimum
                    }
                }

                response = requests.post(api_url, json=payload, timeout=600)

                if response.status_code == 200:
                    result_json = response.json()
                    output = result_json.get("response", "")
                else:
                    output = ""
                    logger.error(f"API error: {response.status_code}")

                elapsed = time.time() - start_time

                # Validate depth
                quality = self._validate_depth(output)
                logger.info(f"   Quality metrics:")
                logger.info(f"      Words: {quality['word_count']}")
                logger.info(f"      Page refs: {quality['page_references']}")
                logger.info(f"      Quotes: {quality['direct_quotes']}")
                logger.info(f"      Theory refs: {quality['theory_references']}")
                logger.info(f"      Depth score: {quality['depth_score']:.2f}")

                # Save attempt regardless of pass/fail
                attempt_data = {
                    "attempt": attempt,
                    "quality_metrics": quality,
                    "output": output,
                    "elapsed_time": elapsed
                }
                all_attempts.append(attempt_data)

                if quality["passed"]:
                    logger.info(f"   ✅ Quality check PASSED!")

                    # Save successful result
                    result_data = {
                        "specialist": specialist.name,
                        "domain": specialist.domain,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "processing_time": elapsed,
                        "attempt": attempt,
                        "quality_metrics": quality,
                        "analysis": output,
                        "frameworks_used": specialist.theoretical_framework,
                        "references_used": specialist.reference_scripts,
                        "all_attempts": all_attempts
                    }

                    # Save to file
                    result_file = self.results_dir / f"{specialist.id}_{specialist.name}_v3_{int(time.time())}.json"
                    with open(result_file, 'w', encoding='utf-8') as f:
                        json.dump(result_data, f, indent=2, ensure_ascii=False)

                    logger.info(f"   📁 Saved to {result_file.name}")

                    return result_data
                else:
                    logger.warning(f"   ⚠️ Quality check FAILED")
                    if attempt < max_attempts:
                        logger.info(f"   Retrying with more aggressive prompt...")

            except Exception as e:
                logger.error(f"   ❌ Error: {e}")

        # Save all failed attempts for analysis
        failed_file = self.results_dir / f"{specialist.id}_{specialist.name}_v3_FAILED_{int(time.time())}.json"
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump({
                "status": "FAILED",
                "specialist": specialist.name,
                "all_attempts": all_attempts
            }, f, indent=2, ensure_ascii=False)

        logger.error(f"   ❌ Failed after {max_attempts} attempts")
        logger.info(f"   📁 Failed attempts saved to {failed_file.name}")

        return {"error": "quality_failed", "specialist": specialist.name, "attempts": all_attempts}

    def test_character_arc_v3(self, screenplay_sample: str):
        """Testa Character Arc com sistema V3"""

        character_arc = SuperSpecialist(
            id="02",
            name="character-arc-super",
            domain="Character Transformation & Psychological Depth",
            theoretical_framework=[
                "McKee - True Character Under Pressure",
                "Truby - 22 Steps & Character Web",
                "Vogler - Hero's Journey Stages",
                "Seger - Making a Good Script Great",
                "Egri - Premise and Orchestration"
            ],
            reference_scripts=[
                "Casablanca - Rick Blaine's transformation",
                "The Godfather - Michael Corleone's descent",
                "Breaking Bad - Walter White's corruption",
                "Parasite - Kim Ki-taek's class awakening",
                "Joker - Arthur Fleck's psychological breakdown"
            ]
        )

        return self.analyze_with_specialist_v3(character_arc, screenplay_sample)

# Enhanced test with more screenplay content
if __name__ == "__main__":

    # More substantial screenplay sample
    sample_screenplay = """
    FADE IN:

    INT. APARTMENT - DAY (PAGE 1)

    JOHN (35), unshaven, hollow eyes, stares at a framed photo
    of SARAH (30s, radiant smile). His hands shake as he grips
    a coffee mug with "World's Best Husband" printed on it.

    JOHN
    (to photo)
    I don't need anyone. Never did.

    He THROWS the photo in the trash. The glass SHATTERS.

    Beat. His jaw clenches. He immediately retrieves it,
    cutting his hand on the broken glass. Blood drips.

    JOHN (CONT'D)
    (whispered)
    Liar.

    He carefully removes the photo from the broken frame,
    blood smearing the edges. Places it in his wallet.

    INT. OFFICE - DAY (PAGE 15)

    John sits alone in a glass conference room. COLLEAGUES
    chat and laugh outside. MANAGER (50s, concerned) enters.

    MANAGER
    John, you joining us for drinks?
    Team building, you know.

    JOHN
    (not looking up)
    Got work.

    MANAGER
    Your screen's been blank for an hour.

    John's fingers hover over the keyboard. Frozen.

    JOHN
    I'm thinking.

    MANAGER
    When's the last time you went home
    before midnight?

    JOHN
    When's the last time that mattered?

    Manager sighs, leaves. John stares at his reflection
    in the black screen. Doesn't recognize himself.

    INT. APARTMENT - NIGHT (PAGE 23)

    John watches old videos on his phone. Sarah's voice echoes.

    SARAH (ON VIDEO)
    You can't push everyone away forever.
    One day you'll need someone and—

    John THROWS the phone across the room. It hits the wall,
    screen cracking but still playing.

    SARAH (ON VIDEO) (CONT'D)
    —and I won't be there.

    The video loops. John covers his ears but can't block it out.

    JOHN
    (screaming)
    STOP!

    He grabs the phone, about to smash it completely, then
    sees Sarah's face frozen on the cracked screen. His rage
    dissolves into something else. Grief.

    INT. THERAPIST'S OFFICE - DAY (PAGE 45)

    John sits rigid across from THERAPIST (60s, patient).

    THERAPIST
    Why did you come today?

    JOHN
    My manager made me.

    THERAPIST
    No one can make you be here.
    You chose to walk through that door.

    JOHN
    I didn't have a choice.

    THERAPIST
    There's always a choice. Even now,
    you could leave.

    John's leg bounces. Hand on the door handle. Doesn't turn it.

    JOHN
    She said I push people away.

    THERAPIST
    Who?

    JOHN
    Doesn't matter. She's gone.

    THERAPIST
    Gone where?

    John's composure cracks for a microsecond.

    JOHN
    (barely audible)
    Dead. Car accident. Three months ago.

    [Continue with more scenes showing his journey...]
    """

    system = SuperSpecialistSystemV3()

    logger.info("=" * 60)
    logger.info("🚀 TESTING SUPER SPECIALIST SYSTEM V3")
    logger.info("=" * 60)

    result = system.test_character_arc_v3(sample_screenplay)

    if "error" not in result:
        print("\n" + "=" * 60)
        print("📊 ANALYSIS SUCCESSFUL!")
        print("=" * 60)
        print(f"\nQuality Metrics:")
        for key, value in result["quality_metrics"].items():
            print(f"   {key}: {value}")

        print(f"\n📝 Analysis Preview (first 500 chars):")
        print(result["analysis"][:500] + "...")

        print(f"\n✅ Full analysis saved to file")
        print(f"   Word count: {result['quality_metrics']['word_count']}")
        print(f"   Met minimum requirement: {result['quality_metrics']['word_count'] >= 800}")
    else:
        print(f"\n❌ Analysis failed after all attempts")
        print(f"Check failed attempts file for debugging")