#!/usr/bin/env python3
"""
🎯 TESTE: 5 OTIMIZAÇÕES DO V3_BALANCED
Meta: 700 palavras com quality score > 0.30
Foco: Encontrar o sweet spot perfeito
"""

import json
import logging
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """Métricas de qualidade da resposta"""
    word_count: int
    insight_depth: int  # 0-10: profundidade dos insights
    evidence_count: int  # número de exemplos concretos
    theory_applications: int  # frameworks teóricos aplicados
    unique_observations: int  # observações não óbvias
    actionable_items: int  # sugestões práticas
    coherence_score: float  # 0-1: coerência estrutural
    quality_score: float  # score geral calculado

    def calculate_quality_score(self) -> float:
        """Calcula score geral de qualidade"""
        weights = {
            'insight_depth': 0.25,
            'evidence_count': 0.20,
            'theory_applications': 0.15,
            'unique_observations': 0.20,
            'actionable_items': 0.10,
            'coherence_score': 0.10
        }

        # Normalizar valores
        normalized = {
            'insight_depth': min(self.insight_depth / 10, 1),
            'evidence_count': min(self.evidence_count / 10, 1),
            'theory_applications': min(self.theory_applications / 5, 1),
            'unique_observations': min(self.unique_observations / 8, 1),
            'actionable_items': min(self.actionable_items / 5, 1),
            'coherence_score': self.coherence_score
        }

        score = sum(normalized[k] * w for k, w in weights.items())
        return round(score, 2)

def analyze_response_quality(response: str) -> QualityMetrics:
    """Analisa qualidade da resposta com métricas detalhadas"""

    # Contagem de palavras
    word_count = len(response.split())

    # Análise de insights (procura por padrões de profundidade)
    insight_patterns = [
        r'fundamentally',
        r'crucial',
        r'the real',
        r'deeper',
        r'beneath',
        r'core issue',
        r'root cause',
        r'hidden',
        r'subtle'
    ]
    insight_depth = sum(1 for p in insight_patterns if re.search(p, response, re.I))

    # Contagem de evidências (citações, exemplos, referências)
    evidence_patterns = [
        r'"[^"]+"',  # citações
        r'page \d+',  # referências de página
        r'line \d+',  # referências de linha
        r'for example',
        r'for instance',
        r'specifically',
        r'scene where',
        r'when \w+ says'
    ]
    evidence_count = sum(1 for p in evidence_patterns if re.search(p, response, re.I))

    # Aplicações teóricas
    theory_patterns = [
        r'McKee',
        r'Field',
        r'Snyder',
        r'Campbell',
        r'Vogler',
        r'Truby',
        r'three.act',
        r'save.the.cat',
        r'hero.s journey'
    ]
    theory_applications = sum(1 for p in theory_patterns if re.search(p, response, re.I))

    # Observações únicas (procura por análises não óbvias)
    unique_patterns = [
        r'notice how',
        r'interestingly',
        r'paradox',
        r'contrast',
        r'unexpected',
        r'rarely seen',
        r'unique to',
        r'stands out'
    ]
    unique_observations = sum(1 for p in unique_patterns if re.search(p, response, re.I))

    # Items acionáveis
    action_patterns = [
        r'should',
        r'could',
        r'needs? to',
        r'must',
        r'consider',
        r'try',
        r'rewrite',
        r'revise'
    ]
    actionable_items = sum(1 for p in action_patterns if re.search(p, response, re.I))

    # Coerência (baseada em estrutura e transições)
    transition_words = [
        r'however',
        r'moreover',
        r'furthermore',
        r'therefore',
        r'thus',
        r'consequently',
        r'first',
        r'second',
        r'finally'
    ]
    transitions = sum(1 for p in transition_words if re.search(p, response, re.I))
    coherence_score = min(transitions / 5, 1.0)  # normalizado para max 1.0

    metrics = QualityMetrics(
        word_count=word_count,
        insight_depth=insight_depth,
        evidence_count=evidence_count,
        theory_applications=theory_applications,
        unique_observations=unique_observations,
        actionable_items=actionable_items,
        coherence_score=coherence_score,
        quality_score=0  # será calculado
    )

    metrics.quality_score = metrics.calculate_quality_score()
    return metrics

def create_v3_optimization_variations():
    """Cria 5 variações otimizadas do V3_balanced"""

    base_script = """FADE IN:

INT. THERAPIST'S OFFICE - DAY

SARAH (40s), tired eyes, sits across from DR. MARTINEZ.

SARAH
I need to tell someone what really
happened that night.

DR. MARTINEZ
Take your time.

SARAH
(long pause)
I killed my best friend. Not with a
gun or knife. With words.

FADE OUT.
"""

    variations = {
        "V3_opt1_evidence_focus": {
            "system": """You are a SCRIPT ANALYST focused on evidence-based analysis.

ANALYSIS FRAMEWORK (700 words target):

1. EVIDENCE GATHERING (200 words)
- Quote 5+ specific lines
- Reference 3+ page numbers
- Identify 3+ concrete scenes
- List measurable patterns

2. PATTERN RECOGNITION (200 words)
- Map recurring themes with examples
- Track character behavior changes
- Identify structural patterns
- Note dialogue rhythms

3. THEORETICAL APPLICATION (150 words)
- Apply 3+ screenwriting theories
- Compare to 2+ successful films
- Use established frameworks
- Reference expert opinions

4. PRACTICAL INSIGHTS (150 words)
- Provide 5+ actionable improvements
- Suggest specific rewrites
- Offer concrete solutions
- Include implementation steps

REQUIREMENTS:
- Every claim needs evidence
- Balance depth with brevity
- Target exactly 700 words
- Maximum insight density""",
            "user": f"Analyze this script:\n{base_script}"
        },

        "V3_opt2_insight_density": {
            "system": """You are a SCRIPT DOCTOR maximizing insight per word.

DENSE ANALYSIS PROTOCOL (700 words):

SECTION 1: CORE INSIGHTS (175 words)
Extract the 3 most profound observations.
Each insight must reveal hidden meaning.

SECTION 2: STRUCTURAL DIAGNOSIS (175 words)
Identify deep structural patterns.
Connect to universal storytelling principles.

SECTION 3: CHARACTER PSYCHOLOGY (175 words)
Decode subconscious motivations.
Reveal unspoken character truths.

SECTION 4: TRANSFORMATIVE FIXES (175 words)
Prescribe high-impact changes.
Each fix must transform the script.

RULES:
- No filler words
- Every sentence must deliver value
- Use precise, powerful language
- Compress maximum meaning into 700 words""",
            "user": f"Diagnose this script with maximum insight density:\n{base_script}"
        },

        "V3_opt3_structured_precision": {
            "system": """You are a FORENSIC SCRIPT EXAMINER using structured precision.

=== PRECISION PROTOCOL (700 words exact) ===

📍 EXTERNAL ANALYSIS (175 words)
• Surface elements catalog
• Visible patterns documentation
• Technical specifications
• Format compliance check

🔬 INTERNAL MECHANICS (175 words)
• Subtext excavation
• Emotional mechanics
• Psychological drivers
• Hidden connections

🎯 COMPARATIVE FORENSICS (175 words)
• Match against genre standards
• Compare to successful examples
• Identify deviations
• Measure effectiveness

💊 PRESCRIPTION (175 words)
• Targeted interventions
• Specific line rewrites
• Structural adjustments
• Priority fixes

MANDATE: Exactly 700 words. Maximum precision.""",
            "user": f"Perform forensic examination:\n{base_script}"
        },

        "V3_opt4_theory_practice_fusion": {
            "system": """SCRIPT OPTIMIZATION SPECIALIST combining theory with practice.

FUSION METHODOLOGY (700 words):

Part 1: THEORETICAL FRAMEWORK (200 words)
- Apply McKee's story principles
- Use Field's paradigm
- Include Save the Cat beats
- Reference Truby's anatomy

Part 2: PRACTICAL APPLICATION (200 words)
- Show exactly how theory applies
- Demonstrate with script examples
- Bridge concept to execution
- Prove theoretical points

Part 3: EVIDENCE-BASED CRITIQUE (150 words)
- Support every claim with proof
- Quote specific problematic lines
- Identify precise weaknesses
- Document pattern failures

Part 4: ACTIONABLE SOLUTIONS (150 words)
- Convert theory to practice
- Provide rewrite examples
- Suggest structural fixes
- Include implementation guide

Target: 700 words combining depth with practicality.""",
            "user": f"Analyze using theory-practice fusion:\n{base_script}"
        },

        "V3_opt5_golden_ratio": {
            "system": """SCRIPT ANALYST using Golden Ratio optimization.

GOLDEN RATIO ANALYSIS (700 words):

🔸 MACRO VIEW (40% - 280 words)
Big picture assessment:
- Overall story effectiveness
- Thematic coherence
- Structural integrity
- Genre fulfillment

🔹 MICRO VIEW (35% - 245 words)
Detailed examination:
- Line-by-line quality
- Dialogue authenticity
- Character consistency
- Scene mechanics

⚡ CRITICAL INSIGHTS (15% - 105 words)
Breakthrough observations:
- Hidden flaws
- Unrealized potential
- Subtle brilliance
- Core problems

✅ SOLUTIONS (10% - 70 words)
High-leverage fixes:
- Top 3 changes
- Quick wins
- Major improvements

Mathematical precision: 40/35/15/10 ratio.
Exactly 700 words total.""",
            "user": f"Apply golden ratio analysis:\n{base_script}"
        }
    }

    return variations

def test_variation(name: str, config: Dict, run_number: int) -> Tuple[str, QualityMetrics, float]:
    """Testa uma variação e retorna resultado"""

    logger.info(f"🧪 Testing {name} (Run {run_number})...")

    try:
        import requests
    except ImportError:
        # Fallback to subprocess if requests not available
        logger.warning("requests not available, using subprocess")

    api_url = "http://localhost:11434/api/chat"

    # Preparar mensagens
    messages = [
        {"role": "system", "content": config["system"]},
        {"role": "user", "content": config["user"]}
    ]

    # Configuração otimizada para Mixtral
    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",  # Modelo correto
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 2048,
            "stop": ["FADE OUT", "THE END", "[END]"]
        }
    }

    start_time = time.time()

    try:
        # Tentar com requests primeiro
        try:
            import requests
            response = requests.post(api_url, json=data, timeout=60)
            response.raise_for_status()
            response_data = response.json()
        except:
            # Fallback para curl
            cmd = ["curl", "-s", "-X", "POST", api_url,
                   "-H", "Content-Type: application/json",
                   "-d", json.dumps(data)]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                logger.error(f"Curl failed: {result.stderr}")
                return "", QualityMetrics(0,0,0,0,0,0,0,0), 0
            response_data = json.loads(result.stdout)

        response_text = response_data.get("message", {}).get("content", "")

        if not response_text:
            logger.error(f"Empty response for {name}")
            return "", QualityMetrics(0,0,0,0,0,0,0,0), 0

        elapsed = time.time() - start_time
        metrics = analyze_response_quality(response_text)

        logger.info(f"   📊 Words: {metrics.word_count}")
        logger.info(f"   ⭐ Quality Score: {metrics.quality_score}")
        logger.info(f"   💎 Insights: {metrics.insight_depth}")
        logger.info(f"   📍 Evidence: {metrics.evidence_count}")
        logger.info(f"   📚 Theories: {metrics.theory_applications}")
        logger.info(f"   🎯 Unique Observations: {metrics.unique_observations}")
        logger.info(f"   ⏱️ Time: {elapsed:.1f}s")

        return response_text, metrics, elapsed

    except Exception as e:
        logger.error(f"Error testing {name}: {e}")
        return "", QualityMetrics(0,0,0,0,0,0,0,0), 0

def main():
    """Executa teste das 5 otimizações do V3"""

    print("\n" + "="*60)
    print("🎯 TESTE: OTIMIZAÇÕES DO V3_BALANCED")
    print("Meta: 700 palavras com quality score > 0.30")
    print("="*60 + "\n")

    # Criar diretório para salvar resultados
    output_dir = Path("v3_optimization_tests")
    output_dir.mkdir(exist_ok=True)

    variations = create_v3_optimization_variations()
    results = []

    # Testar cada variação
    for name, config in variations.items():
        response, metrics, elapsed = test_variation(name, config, 1)

        if metrics.word_count > 0:
            results.append({
                "name": name,
                "metrics": asdict(metrics),
                "time": elapsed,
                "response": response[:500] + "..."  # Primeiros 500 chars
            })

            # Salvar resposta completa
            with open(output_dir / f"{name}.txt", "w") as f:
                f.write(response)

    # Análise dos resultados
    print("\n" + "="*60)
    print("🏆 RESULTADOS - OTIMIZAÇÕES V3")
    print("="*60 + "\n")

    # Ranking por quality score
    quality_ranked = sorted(results, key=lambda x: x["metrics"]["quality_score"], reverse=True)

    print("📊 RANKING POR QUALIDADE:\n")
    for i, result in enumerate(quality_ranked, 1):
        m = result["metrics"]
        efficiency = m["word_count"] / m["quality_score"] if m["quality_score"] > 0 else float('inf')
        print(f"{i}º {result['name']}")
        print(f"   ⭐ Quality Score: {m['quality_score']}")
        print(f"   📝 Words: {m['word_count']}")
        print(f"   💎 Insights: {m['insight_depth']}")
        print(f"   📍 Evidence: {m['evidence_count']}")
        print(f"   🎯 Efficiency: {efficiency:.1f} words/quality")
        print()

    # Análise de proximidade à meta (700 palavras)
    print("🎯 PROXIMIDADE À META (700 palavras):")
    for result in results:
        m = result["metrics"]
        distance = abs(700 - m["word_count"])
        print(f"{result['name']}: {m['word_count']} palavras (Δ{distance})")

    # Identificar vencedor geral
    if results:
        print("\n" + "="*60)
        print("🏆 VENCEDOR GERAL")
        print("="*60 + "\n")

        # Calcular score composto: qualidade + proximidade a 700
        for result in results:
            m = result["metrics"]
            distance_penalty = abs(700 - m["word_count"]) / 700  # penalidade por distância
            composite_score = m["quality_score"] * (1 - distance_penalty * 0.5)
            result["composite_score"] = composite_score

        winner = max(results, key=lambda x: x.get("composite_score", 0))

        print(f"🥇 CAMPEÃO: {winner['name']}")
        print(f"   Quality Score: {winner['metrics']['quality_score']}")
        print(f"   Word Count: {winner['metrics']['word_count']}")
        print(f"   Composite Score: {winner['composite_score']:.3f}")
    else:
        print("\n⚠️ Nenhum resultado válido obtido. Verifique se o Ollama está rodando.")

    # Salvar relatório completo
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "meta": "700 palavras com quality score > 0.30",
        "results": results,
        "winner": winner["name"] if results else "None"
    }

    with open(output_dir / "optimization_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n📁 Resultados salvos em: {output_dir}")
    print("\n🔍 Missão: Encontrar o sweet spot perfeito!")

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("🎯 INICIANDO TESTE DE OTIMIZAÇÕES V3")
    logger.info("Meta: 700 palavras, score > 0.30")
    logger.info("="*60)
    main()