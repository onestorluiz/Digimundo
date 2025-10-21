#!/usr/bin/env python3
"""
SISTEMA DE SUPER ESPECIALISTAS COM CONTEXTO LIMPO
==================================================
Cada especialista:
1. Carrega 100K tokens de contexto (roteiro + teoria + referências)
2. Processa profundamente
3. Sintetiza em 800-1500 tokens de output denso
4. LIMPA contexto antes do próximo
"""

import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SuperSpecialist:
    """Super Especialista com contexto massivo"""
    id: str
    name: str
    domain: str
    theoretical_framework: List[str]  # McKee, Truby, etc
    reference_scripts: List[str]      # Filmes para comparar
    min_output: int = 800
    max_output: int = 1500
    context_size: int = 131072

class SuperSpecialistSystem:
    """Sistema de análise com especialistas de contexto limpo"""

    def __init__(self, base_model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.base_model = base_model
        self.knowledge_base = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/knowledge_packs")
        self.reference_scripts = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/reference_scripts")
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/analysis_results")
        self.results_dir.mkdir(exist_ok=True)

    def _load_theoretical_framework(self, frameworks: List[str]) -> str:
        """Carrega frameworks teóricos (McKee, Truby, etc)"""
        content = []
        for framework in frameworks:
            framework_file = self.knowledge_base / f"{framework.lower()}.md"
            if framework_file.exists():
                with open(framework_file, 'r', encoding='utf-8') as f:
                    content.append(f"=== {framework} FRAMEWORK ===\n{f.read()}\n")
        return "\n".join(content)

    def _load_reference_scripts(self, script_names: List[str]) -> str:
        """Carrega trechos relevantes de roteiros de referência"""
        content = []
        for script in script_names:
            script_file = self.reference_scripts / f"{script.lower().replace(' ', '_')}.txt"
            if script_file.exists():
                with open(script_file, 'r', encoding='utf-8') as f:
                    # Pega apenas trechos relevantes (primeiras 5000 palavras)
                    text = f.read()[:30000]
                    content.append(f"=== REFERENCE: {script} ===\n{text}\n")
        return "\n".join(content)

    def _build_specialist_prompt(self,
                                specialist: SuperSpecialist,
                                screenplay: str,
                                specialist_prompt: str) -> str:
        """Constrói prompt com 100K+ tokens de contexto"""

        # 1. Carrega frameworks teóricos (30K tokens)
        theory = self._load_theoretical_framework(specialist.theoretical_framework)

        # 2. Carrega roteiros de referência (40K tokens)
        references = self._load_reference_scripts(specialist.reference_scripts)

        # 3. Monta o mega-prompt
        mega_prompt = f"""
# SUPER SPECIALIST: {specialist.name}

## YOUR MISSION
You are the {specialist.name} specialist. Your domain is {specialist.domain}.
You have access to complete theoretical frameworks and reference scripts.
Your analysis must be DEEP, SPECIFIC, and EVIDENCE-BASED.

## THEORETICAL FRAMEWORK (Study these deeply)
{theory}

## REFERENCE SCRIPTS (Compare and contrast)
{references}

## SCREENPLAY TO ANALYZE
{screenplay}

## YOUR SPECIALIST INSTRUCTIONS
{specialist_prompt}

## OUTPUT REQUIREMENTS
- MINIMUM: {specialist.min_output} tokens
- MAXIMUM: {specialist.max_output} tokens
- Every claim needs page/time evidence
- Compare with at least 3 reference scripts
- Quote theoretical sources
- Identify patterns others might miss

## DEPTH REQUIREMENT
You have 100,000+ tokens of context. USE THEM.
- Cross-reference theory with script
- Find parallels in reference scripts
- Identify contradictions
- Map micro-patterns
- Challenge conventional readings

REMEMBER: Your {specialist.max_output} token output is the DISTILLATION
of 100,000 tokens of deep analysis. Make every word count.

Now provide your EXPERT ANALYSIS:
"""
        return mega_prompt

    def analyze_with_specialist(self,
                               specialist: SuperSpecialist,
                               screenplay: str,
                               specialist_prompt: str) -> Dict[str, Any]:
        """Executa análise com um super especialista"""

        logger.info(f"🔬 Starting {specialist.name} analysis")
        logger.info(f"   Domain: {specialist.domain}")
        logger.info(f"   Frameworks: {', '.join(specialist.theoretical_framework)}")
        logger.info(f"   References: {', '.join(specialist.reference_scripts[:3])}...")

        # Build massive context
        prompt = self._build_specialist_prompt(specialist, screenplay, specialist_prompt)
        prompt_size = len(prompt.encode('utf-8'))
        logger.info(f"   Prompt size: {prompt_size:,} bytes (~{prompt_size//4:,} tokens)")

        start_time = time.time()

        try:
            # Execute with full context
            result = subprocess.run(
                [
                    'ollama', 'run',
                    self.base_model,
                    '--verbose'
                ],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes per specialist
            )

            elapsed = time.time() - start_time
            logger.info(f"   ✅ Completed in {elapsed:.1f} seconds")

            # Parse output
            output = result.stdout.strip()
            output_tokens = len(output.split())

            logger.info(f"   Output: {output_tokens} tokens")

            if output_tokens < specialist.min_output:
                logger.warning(f"   ⚠️ Output below minimum ({output_tokens} < {specialist.min_output})")

            # Save result
            result_data = {
                "specialist": specialist.name,
                "domain": specialist.domain,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "processing_time": elapsed,
                "prompt_size": prompt_size,
                "output_tokens": output_tokens,
                "analysis": output,
                "frameworks_used": specialist.theoretical_framework,
                "references_used": specialist.reference_scripts
            }

            # Save to file
            result_file = self.results_dir / f"{specialist.id}_{specialist.name}_{int(time.time())}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            logger.info(f"   📁 Saved to {result_file.name}")

            return result_data

        except subprocess.TimeoutExpired:
            logger.error(f"   ❌ Timeout after 10 minutes")
            return {"error": "timeout", "specialist": specialist.name}
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            return {"error": str(e), "specialist": specialist.name}

    def test_character_arc_specialist(self, screenplay_sample: str):
        """Testa o Character Arc Super Specialist"""

        # Define o super especialista
        character_arc = SuperSpecialist(
            id="02",
            name="character-arc-super",
            domain="Character Transformation & Psychology",
            theoretical_framework=[
                "McKee - Character True Character",
                "Truby - Character Web & Moral Argument",
                "Vogler - Hero's Journey",
                "Seger - Transformational Arc",
                "Egri - Orchestration"
            ],
            reference_scripts=[
                "Casablanca - Rick's Transformation",
                "The Godfather - Michael's Descent",
                "Parasite - Class Consciousness",
                "Breaking Bad - Walter's Corruption",
                "Joker - Psychological Breakdown"
            ]
        )

        # Prompt específico do especialista
        specialist_prompt = """
## CHARACTER ARC DEEP ANALYSIS

Map the protagonist's transformation with surgical precision:

1. PSYCHOLOGICAL ARCHITECTURE (250 tokens)
   - Initial belief system & lie
   - Defense mechanisms
   - Shadow/Wound origin
   - Coping strategies

2. TRANSFORMATION TIMELINE (400 tokens)
   - Every micro-change with page number
   - Resistance moments
   - Regression patterns
   - False changes vs real changes

3. COMPARATIVE ANALYSIS (300 tokens)
   - Compare with Rick (Casablanca)
   - Compare with Michael (Godfather)
   - Identify unique patterns

4. PSYCHOLOGICAL MECHANISMS (250 tokens)
   - Projection patterns
   - Denial structures
   - Rationalization methods
   - Breakthrough moments

5. VERDICT ON CHANGE (300 tokens)
   - Is it earned or given?
   - Psychological credibility
   - Permanence assessment
   - What others might miss

Focus on EVIDENCE. Every claim needs proof.
"""

        return self.analyze_with_specialist(character_arc, screenplay_sample, specialist_prompt)

# Teste
if __name__ == "__main__":
    # Sample screenplay (você colocaria um roteiro real aqui)
    sample_screenplay = """
    FADE IN:

    INT. APARTMENT - DAY

    JOHN (35), unshaven, stares at a photo of a woman. His hands shake.

    JOHN
    (to photo)
    I don't need anyone. Never did.

    He throws the photo in the trash. Then immediately retrieves it.

    [... resto do roteiro ...]
    """

    system = SuperSpecialistSystem()

    logger.info("=" * 60)
    logger.info("🚀 TESTING SUPER SPECIALIST SYSTEM")
    logger.info("=" * 60)

    result = system.test_character_arc_specialist(sample_screenplay)

    if "error" not in result:
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULT")
        print("=" * 60)
        print(result["analysis"][:2000] + "...")  # Primeiros 2000 chars

        print("\n📈 QUALITY METRICS:")
        print(f"   Output tokens: {result['output_tokens']}")
        print(f"   Processing time: {result['processing_time']:.1f}s")
        print(f"   Frameworks used: {', '.join(result['frameworks_used'])}")