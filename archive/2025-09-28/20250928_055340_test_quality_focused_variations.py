#!/usr/bin/env python3
"""
TESTE DE VARIAÇÕES COM FOCO EM QUALIDADE VS VOLUME
===================================================
5 variações: 2 focadas em QUALIDADE máxima,
3 focadas em balancear qualidade e volume.
"""

import time
import json
import requests
import logging
import re
from pathlib import Path
from typing import Dict, Any, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """Métricas de qualidade além de contagem de palavras"""
    word_count: int
    insight_depth: int  # Profundidade dos insights
    evidence_count: int  # Citações e evidências
    theory_applications: int  # Aplicações teóricas
    unique_observations: int  # Observações únicas
    actionable_items: int  # Recomendações práticas
    coherence_score: float  # Coerência estrutural
    quality_score: float  # Score geral de qualidade

class QualityFocusedTester:
    """Testa variações com foco em qualidade vs volume"""

    def __init__(self, model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.model = model
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/quality_tests")
        self.results_dir.mkdir(exist_ok=True)

    def analyze_quality(self, text: str) -> QualityMetrics:
        """Analisa qualidade do output além de contar palavras"""

        word_count = len(text.split())

        # Contar elementos de qualidade
        insight_depth = len(re.findall(r'reveals|shows|demonstrates|indicates|suggests|implies', text, re.I))
        evidence_count = len(re.findall(r'page \d+|p\.\d+|"[^"]{20,}"', text))
        theory_applications = len(re.findall(r'McKee|Truby|Vogler|Field|Seger|Egri|Campbell|Snyder', text))
        unique_observations = len(re.findall(r'notice|observe|discover|find|detect|identify', text, re.I))
        actionable_items = len(re.findall(r'should|must|needs to|requires|recommend|suggest', text, re.I))

        # Coerência: verificar se tem estrutura clara
        has_sections = bool(re.findall(r'SECTION|PART|###|##', text))
        has_conclusion = bool(re.findall(r'conclusion|final|summary|verdict', text, re.I))
        has_intro = bool(re.findall(r'begin|start|first|initial', text, re.I))
        coherence_score = sum([has_sections, has_conclusion, has_intro]) / 3.0

        # Quality score composto
        quality_score = (
            (insight_depth * 0.2) +
            (evidence_count * 0.25) +
            (theory_applications * 0.15) +
            (unique_observations * 0.15) +
            (actionable_items * 0.15) +
            (coherence_score * 10 * 0.1)
        ) / 10

        return QualityMetrics(
            word_count=word_count,
            insight_depth=insight_depth,
            evidence_count=evidence_count,
            theory_applications=theory_applications,
            unique_observations=unique_observations,
            actionable_items=actionable_items,
            coherence_score=coherence_score,
            quality_score=quality_score
        )

    def variation_1_quality_max(self, screenplay: str) -> str:
        """Variação 1: QUALIDADE MÁXIMA - Profundidade sobre volume"""
        return f"""
You are the world's foremost expert on screenplay structure.
Your analysis must be INSIGHTFUL, PRECISE, and ACTIONABLE.

Quality over quantity. Depth over breadth. Insight over description.

=== EXPERT STRUCTURAL ANALYSIS ===

🎯 CORE STRUCTURAL DIAGNOSIS (Focus on quality)
"After careful examination, the fundamental structural reality is..."

Provide your DEEPEST INSIGHT about this structure.
Not what's obvious, but what only an expert would see.
Connect patterns others miss.
Reveal the hidden architecture.

Essential questions to answer with precision:
- What is the REAL organizing principle? (Not just "three acts")
- Where does the structure genuinely succeed?
- Where does it fundamentally fail?
- What single change would transform everything?

🔬 EVIDENCE-BASED OBSERVATIONS (Quality of proof)
"The evidence that supports my diagnosis..."

Cite ONLY the most revealing moments.
Quality quotes that prove your point.
Specific page references that matter.
Don't list everything - choose what's SIGNIFICANT.

📐 THEORETICAL FRAMEWORK (Depth of understanding)
"Applying advanced structural theory..."

Don't just name-drop McKee or Truby.
Show DEEP UNDERSTANDING of their principles.
Apply theory in ways that reveal new insights.
Connect multiple frameworks to show mastery.

💎 UNIQUE EXPERT INSIGHTS (What others miss)
"What 99% of readers won't notice..."

Share observations that require true expertise.
Point out subtle patterns.
Reveal unconscious structures.
Identify what the writer did without knowing.

🎬 MASTERCLASS COMPARISON (Selective and meaningful)
"This reminds me of one specific masterpiece..."

Choose ONE perfect comparison.
Explain WHY it's relevant.
Show what this script can learn.
Make the connection meaningful, not superficial.

✨ THE ONE ESSENTIAL PRESCRIPTION (Quality recommendation)
"If you change nothing else, change this..."

Give ONE transformative recommendation.
Explain WHY it will work.
Show HOW to implement it.
Predict the IMPACT.

REMEMBER: This is about QUALITY of analysis, not quantity of words.
Every sentence must add value. Every observation must matter.
Write less, but write BETTER.

Screenplay for expert analysis:
{screenplay}

Begin quality-focused analysis:
"""

    def variation_2_quality_precision(self, screenplay: str) -> str:
        """Variação 2: PRECISÃO CIRÚRGICA - Menos é mais"""
        return f"""
You are performing PRECISION STRUCTURAL SURGERY.
Every word must cut to the truth. No filler. No repetition. Pure insight.

=== PRECISION PROTOCOL ===

⚡ THE DIAGNOSIS (Get to the point)
The structural truth is: [Direct statement]
It works because: [Precise reason]
It fails because: [Exact problem]
The solution is: [Clear prescription]

🎯 THE EVIDENCE (Only what matters)
Critical evidence at page [X]: [Why it matters]
Revealing moment at page [Y]: [What it proves]
Turning point at page [Z]: [How it functions]

Do not describe. ANALYZE.
Do not summarize. INTERPRET.
Do not list. SYNTHESIZE.

🧬 THE PATTERN (What others miss)
The hidden pattern is: [Revelation]
It appears at: [Specific locations]
It means: [Interpretation]
It suggests: [Implication]

💊 THE PRESCRIPTION (Exactly what's needed)
Cut: [What and why]
Add: [What and where]
Restructure: [How and why]
Result: [Predicted outcome]

🏆 THE VERDICT (No padding)
Structural integrity: [Score]/10
Fatal flaw: [If any]
Hidden strength: [If any]
Success probability: [With/without changes]

PRECISION RULES:
- No throat-clearing
- No redundancy
- No obvious observations
- No unnecessary examples
- Every word earns its place

Screenplay requiring precision analysis:
{screenplay}

Begin surgical precision:
"""

    def variation_3_balanced_depth(self, screenplay: str) -> str:
        """Variação 3: PROFUNDIDADE BALANCEADA - Qualidade com volume adequado"""
        return f"""
You are a MASTER STRUCTURAL ANALYST balancing depth with comprehensive coverage.
Aim for substantial analysis (1000+ words) while maintaining exceptional quality.

=== BALANCED FORENSIC STRUCTURE ANALYSIS ===

📊 SECTION 1: STRUCTURAL FOUNDATION (300 words of quality analysis)
"Examining the architectural foundation..."

Begin with the most important structural observation.
Build from there with connected insights.
Layer evidence upon evidence.
Create a compelling analytical narrative.

The foundation reveals: [Deep insight about base structure]
This is evidenced by: [Multiple specific examples]
The implications are: [Connected observations]
This pattern continues through: [Trace the thread]

Remember: 300 words of QUALITY, not filler.

🔍 SECTION 2: HIDDEN MECHANISMS (300 words of revelations)
"Uncovering what drives the narrative..."

Dig beneath obvious structure.
Find the engine that really drives this story.
Identify unconscious patterns.
Reveal mathematical/musical structures.

The real mechanism is: [Surprising discovery]
It operates through: [Specific explanation]
Evidence includes: [Multiple proofs]
This creates: [Effect analysis]

Every sentence must reveal something non-obvious.

🎭 SECTION 3: COMPARATIVE MASTERY (300 words of expert comparison)
"Contextualizing within cinematic tradition..."

Select 2-3 PERFECT comparisons.
Explain precisely why they matter.
Show specific parallels and divergences.
Extract applicable lessons.

Compared to [Masterpiece 1]: [Detailed analysis]
Unlike [Masterpiece 2]: [Specific contrasts]
This suggests: [Synthesis of insights]

Make comparisons that illuminate, not just name-drop.

💡 SECTION 4: TRANSFORMATIVE PRESCRIPTION (300 words of solutions)
"Prescribing specific structural improvements..."

Provide 3-5 SPECIFIC, IMPLEMENTABLE changes.
Explain the theory behind each.
Predict the exact impact.
Show how they interconnect.

Priority 1: [Specific change with full reasoning]
Priority 2: [Another change with justification]
Priority 3: [Final change with explanation]
Synergy effect: [How changes work together]

Total target: 1200 words of pure quality.
No padding, but comprehensive coverage.

Screenplay for balanced analysis:
{screenplay}

Begin balanced quality analysis:
"""

    def variation_4_progressive_depth(self, screenplay: str) -> str:
        """Variação 4: PROFUNDIDADE PROGRESSIVA - Construção gradual"""
        return f"""
You are building a PROGRESSIVE STRUCTURAL ANALYSIS.
Start accessible, go deeper with each section, end with master-level insights.

=== PROGRESSIVE DEPTH PROTOCOL ===

🌊 LEVEL 1: SURFACE CLARITY (200 words)
"What any intelligent reader would notice..."

Start with clear, undeniable observations.
Build credibility with obvious truths.
Establish the baseline.

The structure appears to be: [Clear observation]
The genre signals include: [Obvious markers]
The basic framework follows: [Standard structure]

Set the stage for deeper analysis.

🌊🌊 LEVEL 2: PROFESSIONAL ANALYSIS (300 words)
"What a working screenwriter would observe..."

Apply professional frameworks.
Identify craft-level issues.
Spot technical problems and successes.

The professional assessment reveals: [Craft analysis]
Technical strengths include: [Specific elements]
Craft weaknesses appear in: [Problem areas]
Industry standards suggest: [Professional view]

Bridge from obvious to insightful.

🌊🌊🌊 LEVEL 3: EXPERT INSIGHTS (400 words)
"What a story expert would discover..."

Apply advanced theory.
Find hidden patterns.
Make non-obvious connections.
Reveal structural secrets.

The deeper analysis uncovers: [Hidden patterns]
Theoretical application shows: [Advanced insights]
Unconscious structures include: [Subtle discoveries]
Master-level observation: [Expert insight]

This is where real value emerges.

🌊🌊🌊🌊 LEVEL 4: VISIONARY SYNTHESIS (500 words)
"What transforms this from script to art..."

Synthesize all levels.
Provide transformative insights.
Connect to larger principles.
Offer visionary prescription.

The synthesis reveals: [Unified understanding]
The transformation requires: [Visionary changes]
The potential becomes: [What it could be]
The path forward: [Detailed roadmap]

End with insights that change everything.

Progressive total: 1400+ words of escalating quality.
Each level builds on the previous.
Depth increases systematically.

Screenplay for progressive analysis:
{screenplay}

Begin progressive deepening:
"""

    def variation_5_multi_expert_panel(self, screenplay: str) -> str:
        """Variação 5: PAINEL MULTI-EXPERT - Múltiplas perspectivas de qualidade"""
        return f"""
You are moderating a PANEL OF FIVE STRUCTURAL EXPERTS.
Each expert provides their unique, high-quality perspective.

=== EXPERT PANEL DISCUSSION ===

👤 EXPERT 1: THE CLASSICIST (Dr. Aristotle) (250 words)
"From a classical three-act perspective..."

Speaking as a structural purist:
The unity of action shows: [Classical analysis]
The dramatic necessity reveals: [Cause-effect chains]
The catharsis potential is: [Emotional journey]
My classical verdict: [Traditional assessment]

Apply Aristotelian principles with rigor.

👤 EXPERT 2: THE MODERNIST (Prof. McKee) (250 words)
"Looking at story values and turning points..."

From my decades of analysis:
The value progressions show: [McKee framework]
The gap between expectation/result: [Specific examples]
The controlling idea emerges as: [Theme extraction]
My modernist assessment: [Contemporary view]

Apply modern story theory precisely.

👤 EXPERT 3: THE MAVERICK (Ms. Kaufman) (250 words)
"Examining non-traditional structures..."

Forget conventional wisdom:
The real structure is: [Unconventional reading]
Traditional analysis misses: [What's overlooked]
The experimental potential: [Innovative possibilities]
My maverick suggestion: [Bold prescription]

Challenge assumptions productively.

👤 EXPERT 4: THE PSYCHOLOGIST (Dr. Jung) (250 words)
"Analyzing archetypal structures..."

The unconscious architecture reveals:
Archetypal patterns include: [Jungian analysis]
The collective unconscious echoes: [Universal themes]
The individuation journey shows: [Psychological arc]
My psychological prescription: [Deep structure fix]

Apply psychological frameworks meaningfully.

👤 EXPERT 5: THE SYNTHESIZER (You, the Moderator) (400 words)
"Synthesizing all perspectives..."

Having heard all experts:
The consensus points are: [Where they agree]
The revealing conflicts are: [Where they diverge]
The synthesis suggests: [Unified understanding]
The optimal path forward: [Integrated solution]

Weave together all perspectives.
Resolve contradictions.
Find the higher truth.
Provide unified prescription.

Total: 1400 words of multi-perspective quality.
Each expert adds unique value.
No redundancy between perspectives.

Screenplay for panel analysis:
{screenplay}

Begin expert panel discussion:
"""

    def test_variation(self, name: str, prompt: str) -> Dict[str, Any]:
        """Testa uma variação e analisa qualidade além de volume"""

        logger.info(f"🧪 Testing {name}...")

        start_time = time.time()

        # Call Ollama API
        api_url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 5000,
                "temperature": 0.8,  # Ajustado para qualidade
                "top_p": 0.95,
                "num_ctx": 131072,
                "repeat_penalty": 1.05,  # Ligeiramente penalizar repetição
                "top_k": 100,
                "seed": 42
            }
        }

        try:
            response = requests.post(api_url, json=payload, timeout=600)

            if response.status_code == 200:
                result_json = response.json()
                output = result_json.get("response", "")

                elapsed = time.time() - start_time

                # Análise de qualidade
                metrics = self.analyze_quality(output)

                result = {
                    "variation": name,
                    "word_count": metrics.word_count,
                    "quality_score": round(metrics.quality_score, 2),
                    "insight_depth": metrics.insight_depth,
                    "evidence_count": metrics.evidence_count,
                    "theory_applications": metrics.theory_applications,
                    "unique_observations": metrics.unique_observations,
                    "actionable_items": metrics.actionable_items,
                    "coherence_score": round(metrics.coherence_score, 2),
                    "elapsed": elapsed,
                    "words_per_quality": round(metrics.word_count / max(metrics.quality_score, 0.1), 1),
                    "output_preview": output[:500] + "..." if output else "FAILED"
                }

                logger.info(f"   📊 Words: {metrics.word_count}")
                logger.info(f"   ⭐ Quality Score: {metrics.quality_score:.2f}")
                logger.info(f"   💎 Insights: {metrics.insight_depth}")
                logger.info(f"   📍 Evidence: {metrics.evidence_count}")
                logger.info(f"   ⏱️ Time: {elapsed:.1f}s")

                # Save result
                result_file = self.results_dir / f"{name}_{int(time.time())}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump({**result, "full_output": output}, f, indent=2, ensure_ascii=False)

                return result

            else:
                logger.error(f"API error: {response.status_code}")
                return {"variation": name, "word_count": 0, "quality_score": 0, "error": "API error"}

        except Exception as e:
            logger.error(f"Exception: {e}")
            return {"variation": name, "word_count": 0, "quality_score": 0, "error": str(e)}

    def run_all_variations(self, screenplay: str) -> Dict[str, Any]:
        """Testa todas as 5 variações com foco em qualidade"""

        logger.info("=" * 60)
        logger.info("🎯 TESTANDO QUALIDADE VS VOLUME")
        logger.info("Foco: 2 em qualidade pura, 3 em balanço")
        logger.info("=" * 60)

        variations = {
            "V1_quality_max": self.variation_1_quality_max(screenplay),
            "V2_precision": self.variation_2_quality_precision(screenplay),
            "V3_balanced": self.variation_3_balanced_depth(screenplay),
            "V4_progressive": self.variation_4_progressive_depth(screenplay),
            "V5_multi_expert": self.variation_5_multi_expert_panel(screenplay)
        }

        results = []

        for name, prompt in variations.items():
            result = self.test_variation(name, prompt)
            results.append(result)

        # Rank by quality score
        results_by_quality = sorted(results, key=lambda x: x.get("quality_score", 0), reverse=True)

        # Rank by word count
        results_by_volume = sorted(results, key=lambda x: x.get("word_count", 0), reverse=True)

        # Print summary
        print("\n" + "=" * 60)
        print("🏆 RESULTADOS - QUALIDADE VS VOLUME")
        print("=" * 60)

        print("\n📊 RANKING POR QUALIDADE:")
        for i, result in enumerate(results_by_quality, 1):
            print(f"\n{i}º {result['variation']}")
            print(f"   ⭐ Quality Score: {result.get('quality_score', 0)}")
            print(f"   📝 Words: {result.get('word_count', 0)}")
            print(f"   💎 Insights: {result.get('insight_depth', 0)}")
            print(f"   📍 Evidence: {result.get('evidence_count', 0)}")
            print(f"   🎯 Words/Quality: {result.get('words_per_quality', 0)}")

        print("\n📊 RANKING POR VOLUME:")
        for i, result in enumerate(results_by_volume, 1):
            print(f"{i}º {result['variation']}: {result.get('word_count', 0)} palavras")

        # Identify sweet spot
        sweet_spot = None
        for result in results:
            if result.get("word_count", 0) > 800 and result.get("quality_score", 0) > 5:
                sweet_spot = result
                break

        if sweet_spot:
            print(f"\n🎯 SWEET SPOT ENCONTRADO:")
            print(f"   {sweet_spot['variation']}")
            print(f"   {sweet_spot['word_count']} palavras com quality score {sweet_spot['quality_score']}")

        # Save final report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "focus": "Quality vs Volume Balance",
            "results_by_quality": results_by_quality,
            "results_by_volume": results_by_volume,
            "sweet_spot": sweet_spot,
            "insights": {
                "best_quality": results_by_quality[0]["variation"] if results_by_quality else None,
                "best_volume": results_by_volume[0]["variation"] if results_by_volume else None,
                "best_balance": sweet_spot["variation"] if sweet_spot else None
            }
        }

        report_file = self.results_dir / f"quality_focus_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

# Teste principal
if __name__ == "__main__":

    # Screenplay para teste
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

    tester = QualityFocusedTester()

    print("\n🎯 EXPERIMENTO: QUALIDADE VS VOLUME")
    print("2 variações focadas em QUALIDADE pura")
    print("3 variações buscando BALANÇO qualidade/volume")
    print("=" * 60)

    report = tester.run_all_variations(test_screenplay)

    print(f"\n📁 Resultados salvos em: {tester.results_dir}")

    if report.get("sweet_spot"):
        print("\n✨ ENCONTRAMOS O EQUILÍBRIO IDEAL!")
    else:
        print("\n🔍 Continuando a buscar o equilíbrio ideal...")