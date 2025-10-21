#!/usr/bin/env python3
"""
SISTEMA DE SUPER ESPECIALISTAS V2 - COM PROFUNDIDADE GARANTIDA
===============================================================
Melhorias:
1. Força output mínimo via parâmetros Ollama
2. Validação de qualidade
3. Re-prompt automático se superficial
"""

import os
import json
import subprocess
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

class SuperSpecialistSystemV2:
    """Sistema melhorado com garantia de profundidade"""

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

        quality_score["passed"] = (
            word_count >= 800 and
            page_refs >= 5 and
            quotes >= 3 and
            comparisons >= 3 and
            theory_refs >= 5
        )

        return quality_score

    def _build_enhanced_prompt(self,
                              specialist: SuperSpecialist,
                              screenplay: str,
                              attempt: int = 1) -> str:
        """Constrói prompt melhorado com instruções mais assertivas"""

        # Se é uma re-tentativa, adiciona instruções extras
        retry_instruction = ""
        if attempt > 1:
            retry_instruction = """
⚠️ YOUR PREVIOUS ANALYSIS WAS TOO SUPERFICIAL!
Requirements NOT met. This time:
- MINIMUM 800 words (not tokens, WORDS)
- At least 10 specific page references
- At least 5 direct quotes
- At least 5 theoretical framework citations
- At least 3 comparisons with reference scripts

DEPTH IS MANDATORY. SUPERFICIAL ANALYSIS WILL BE REJECTED.
"""

        mega_prompt = f"""
# SUPER SPECIALIST: {specialist.name}
# ATTEMPT: {attempt}

{retry_instruction}

## CRITICAL INSTRUCTIONS - READ CAREFULLY

You are the world's leading expert in {specialist.domain}.
You have been given 100,000+ tokens of context to analyze deeply.
Your output MUST be between {specialist.min_output} and {specialist.max_output} WORDS.

THIS IS NOT A SUGGESTION - IT IS A REQUIREMENT.

## YOUR EXPERTISE INCLUDES:

### Theoretical Mastery:
{', '.join(specialist.theoretical_framework)}

### Reference Scripts You Know Intimately:
{', '.join(specialist.reference_scripts)}

## THE SCREENPLAY TO ANALYZE:

{screenplay}

## MANDATORY ANALYSIS STRUCTURE:

### 1. DEEP PATTERN RECOGNITION (300+ words)
Identify patterns that others miss. Use your theoretical knowledge.
Quote specific pages. Compare with reference scripts.

### 2. EVIDENCE-BASED INSIGHTS (400+ words)
Every claim needs proof:
- "On page X, we see..."
- "This mirrors [Reference Script] when..."
- "As [Theorist] argues in [Work]..."

### 3. CONTRADICTIONS & COMPLEXITIES (300+ words)
What doesn't fit the standard model?
What contradicts theory?
What's psychologically complex?

### 4. UNIQUE EXPERT PERSPECTIVE (300+ words)
What would other analysts miss?
What does YOUR specific expertise reveal?
How does this challenge conventional readings?

## DEPTH REQUIREMENTS:
- Minimum 10 page references (p.XX)
- Minimum 5 direct quotes from screenplay
- Minimum 5 theoretical framework citations
- Minimum 3 detailed comparisons with reference scripts
- Minimum 800 WORDS total

## OUTPUT FORMAT:

Start with: "EXPERT ANALYSIS: {specialist.name}"

Then provide your analysis in clear sections with headers.

Remember: You are THE expert. Your reputation depends on depth and specificity.
Superficial analysis is career-ending. Make every word count.

BEGIN YOUR EXPERT ANALYSIS NOW:
"""
        return mega_prompt

    def analyze_with_specialist_v2(self,
                                  specialist: SuperSpecialist,
                                  screenplay: str,
                                  max_attempts: int = 3) -> Dict[str, Any]:
        """Executa análise com validação de profundidade"""

        logger.info(f"🔬 Starting {specialist.name} analysis V2")

        for attempt in range(1, max_attempts + 1):
            logger.info(f"   Attempt {attempt}/{max_attempts}")

            # Build prompt
            prompt = self._build_enhanced_prompt(specialist, screenplay, attempt)

            start_time = time.time()

            try:
                # Execute with JSON API for better control
                api_url = "http://localhost:11434/api/generate"

                payload = {
                    "model": self.base_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 3000,      # Force more tokens
                        "temperature": 0.8,        # More creative
                        "top_p": 0.95,            # Wider sampling
                        "repeat_penalty": 1.0,     # Allow repetition for depth
                        "num_ctx": 131072          # Max context
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

                if quality["passed"]:
                    logger.info(f"   ✅ Quality check PASSED")

                    # Save result
                    result_data = {
                        "specialist": specialist.name,
                        "domain": specialist.domain,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "processing_time": elapsed,
                        "attempt": attempt,
                        "quality_metrics": quality,
                        "analysis": output,
                        "frameworks_used": specialist.theoretical_framework,
                        "references_used": specialist.reference_scripts
                    }

                    # Save to file
                    result_file = self.results_dir / f"{specialist.id}_{specialist.name}_v2_{int(time.time())}.json"
                    with open(result_file, 'w', encoding='utf-8') as f:
                        json.dump(result_data, f, indent=2, ensure_ascii=False)

                    logger.info(f"   📁 Saved to {result_file.name}")

                    return result_data
                else:
                    logger.warning(f"   ⚠️ Quality check FAILED, retrying...")

            except Exception as e:
                logger.error(f"   ❌ Error: {e}")

        logger.error(f"   ❌ Failed after {max_attempts} attempts")
        return {"error": "quality_failed", "specialist": specialist.name}

    def test_character_arc_v2(self, screenplay_sample: str):
        """Testa Character Arc com sistema V2"""

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
                "Casablanca - Rick Blaine",
                "The Godfather - Michael Corleone",
                "Breaking Bad - Walter White",
                "Parasite - Kim Ki-taek",
                "Joker - Arthur Fleck"
            ]
        )

        return self.analyze_with_specialist_v2(character_arc, screenplay_sample)

# Enhanced test
if __name__ == "__main__":

    # Amostra maior de roteiro para teste
    sample_screenplay = """
    FADE IN:

    INT. APARTMENT - DAY (PAGE 1)

    JOHN (35), unshaven, hollow eyes, stares at a framed photo
    of SARAH (30s, radiant smile). His hands shake.

    JOHN
    (to photo)
    I don't need anyone. Never did.

    He throws the photo in the trash. Beat. His jaw clenches.
    He retrieves it immediately, wiping dust off the glass.

    JOHN (CONT'D)
    (whispered)
    Liar.

    INT. OFFICE - DAY (PAGE 15)

    John sits alone in a conference room. COLLEAGUES chat and
    laugh outside the glass walls. He doesn't look up.

    MANAGER (O.S.)
    John, you joining us for drinks?

    JOHN
    (not looking up)
    Got work.

    The manager leaves. John's screen shows a blank document.

    INT. APARTMENT - NIGHT (PAGE 23)

    John watches old videos on his phone. Sarah's voice echoes.

    SARAH (ON VIDEO)
    You can't push everyone away forever.

    John throws the phone across the room. It cracks but keeps
    playing. Sarah's laughter fills the silence.

    [Continue with more pages...]
    """

    system = SuperSpecialistSystemV2()

    logger.info("=" * 60)
    logger.info("🚀 TESTING SUPER SPECIALIST SYSTEM V2")
    logger.info("=" * 60)

    result = system.test_character_arc_v2(sample_screenplay)

    if "error" not in result:
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULT")
        print("=" * 60)
        print(f"\nQuality Metrics:")
        for key, value in result["quality_metrics"].items():
            print(f"   {key}: {value}")

        print(f"\n📝 Analysis Preview (first 1000 chars):")
        print(result["analysis"][:1000] + "...")
    else:
        print(f"\n❌ Analysis failed: {result['error']}")