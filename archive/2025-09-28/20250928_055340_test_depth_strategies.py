#!/usr/bin/env python3
"""
SISTEMA DE TESTE DE PROFUNDIDADE - COMPARAÇÃO DE ESTRATÉGIAS
=============================================================
Testa 5 estratégias diferentes de prompt para encontrar
a que produz análises mais profundas e ricas.
"""

import os
import json
import time
import re
import requests
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DepthMetrics:
    """Métricas detalhadas de profundidade"""
    # Contagens básicas
    word_count: int
    sentence_count: int
    paragraph_count: int

    # Evidências específicas
    page_references: int
    direct_quotes: int
    character_quotes: int

    # Análise teórica
    theory_citations: int
    framework_applications: int
    technical_terms: int

    # Comparações e insights
    film_comparisons: int
    unique_insights: int
    contradictions_noted: int

    # Estrutura argumentativa
    cause_effect_chains: int
    psychological_mechanisms: int
    transformation_beats: int

    # Score composto
    depth_score: float
    richness_score: float
    specificity_score: float
    overall_score: float

class DepthAnalyzer:
    """Analisador de profundidade de texto"""

    def __init__(self):
        self.theorists = ['McKee', 'Truby', 'Vogler', 'Seger', 'Field', 'Egri', 'Campbell', 'Snyder']
        self.technical_terms = [
            'protagonist', 'antagonist', 'inciting incident', 'climax', 'denouement',
            'character arc', 'transformation', 'wound', 'ghost', 'belief system',
            'defense mechanism', 'projection', 'sublimation', 'catharsis', 'anagnorisis',
            'peripeteia', 'hamartia', 'hubris', 'nemesis', 'deus ex machina'
        ]
        self.psychological_terms = [
            'ego', 'id', 'superego', 'unconscious', 'repression', 'denial',
            'rationalization', 'displacement', 'transference', 'shadow', 'persona',
            'archetype', 'complex', 'neurosis', 'psychosis', 'trauma', 'PTSD'
        ]

    def analyze_depth(self, text: str) -> DepthMetrics:
        """Analisa profundidade do texto com múltiplas métricas"""

        # Contagens básicas
        words = text.split()
        word_count = len(words)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraphs = text.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])

        # Evidências específicas
        page_refs = len(re.findall(r'\bp(?:age)?\s*\.?\s*\d+\b|\bpage\s+\d+\b', text, re.I))
        direct_quotes = len(re.findall(r'"[^"]{15,}"', text))
        character_quotes = len(re.findall(r'[A-Z][A-Z\s]+\n[^"\n]*"[^"]+"|[A-Z][a-z]+:\s*"[^"]+"', text))

        # Análise teórica
        theory_citations = sum(1 for t in self.theorists if t in text)
        framework_apps = len(re.findall(r'according to|as .+ argues|.+ framework|.+ theory|.+ principle', text, re.I))
        technical_terms = sum(1 for term in self.technical_terms if term.lower() in text.lower())

        # Comparações e insights
        film_comparisons = len(re.findall(r'similar to|like in|unlike|compared to|mirrors|echoes|parallels', text, re.I))
        unique_insights = len(re.findall(r'what .+ miss|overlooked|subtle|nuanced|hidden|deeper meaning', text, re.I))
        contradictions = len(re.findall(r'however|but|yet|paradox|contradiction|ironic|despite', text, re.I))

        # Estrutura argumentativa
        cause_effect = len(re.findall(r'because|therefore|thus|consequently|as a result|leads to|causes', text, re.I))
        psych_mechanisms = sum(1 for term in self.psychological_terms if term.lower() in text.lower())
        transformation_beats = len(re.findall(r'shift|change|transform|evolve|growth|regression|breakthrough', text, re.I))

        # Calcular scores compostos
        depth_score = (
            (page_refs * 3) +
            (direct_quotes * 2) +
            (theory_citations * 4) +
            (framework_apps * 3) +
            (technical_terms * 2)
        ) / 10

        richness_score = (
            (word_count / 100) +
            (paragraph_count * 2) +
            (film_comparisons * 3) +
            (unique_insights * 4) +
            (contradictions * 2)
        ) / 10

        specificity_score = (
            (page_refs * 4) +
            (direct_quotes * 3) +
            (character_quotes * 2) +
            (cause_effect * 2) +
            (transformation_beats * 3)
        ) / 10

        overall_score = (depth_score + richness_score + specificity_score) / 3

        return DepthMetrics(
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            page_references=page_refs,
            direct_quotes=direct_quotes,
            character_quotes=character_quotes,
            theory_citations=theory_citations,
            framework_applications=framework_apps,
            technical_terms=technical_terms,
            film_comparisons=film_comparisons,
            unique_insights=unique_insights,
            contradictions_noted=contradictions,
            cause_effect_chains=cause_effect,
            psychological_mechanisms=psych_mechanisms,
            transformation_beats=transformation_beats,
            depth_score=depth_score,
            richness_score=richness_score,
            specificity_score=specificity_score,
            overall_score=overall_score
        )

class StrategyTester:
    """Testador de diferentes estratégias de prompt"""

    def __init__(self, model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.model = model
        self.analyzer = DepthAnalyzer()
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/strategy_tests")
        self.results_dir.mkdir(exist_ok=True)

    def strategy_1_academic(self, screenplay: str) -> str:
        """Estratégia 1: Abordagem Acadêmica Formal"""
        return f"""
You are a PhD professor in Film Studies at Harvard University.
Write a detailed academic analysis of this screenplay's character arc.

Requirements:
- Minimum 1000 words
- Use formal academic language
- Cite at least 10 theoretical sources
- Include footnotes and references
- Analyze with scholarly rigor

Screenplay:
{screenplay}

Begin your academic analysis:
"""

    def strategy_2_detective(self, screenplay: str) -> str:
        """Estratégia 2: Detetive de Personagem"""
        return f"""
You are a CHARACTER DETECTIVE - your job is to uncover EVERY hidden detail.

Your mission:
1. Find EVERY clue about the character's psychology
2. Uncover EVERY pattern others miss
3. Decode EVERY symbol and metaphor
4. Track EVERY micro-change in behavior
5. Expose EVERY contradiction

Be obsessively detailed. Leave no stone unturned.
Minimum 1000 words of investigation.

Evidence to analyze:
{screenplay}

Begin your investigation report:
"""

    def strategy_3_psychoanalyst(self, screenplay: str) -> str:
        """Estratégia 3: Psicanalista Profundo"""
        return f"""
You are the character's PSYCHOANALYST with 30 years experience.

Conduct a deep psychological analysis including:

CLINICAL ASSESSMENT (300 words):
- Initial psychological state
- Defense mechanisms catalog
- Trauma identification
- Attachment patterns

PSYCHODYNAMIC FORMULATION (400 words):
- Unconscious conflicts
- Transference patterns
- Resistance analysis
- Dream symbolism

THERAPEUTIC JOURNEY (300 words):
- Breakthrough moments
- Regression episodes
- Integration process
- Prognosis

Use clinical terminology. Be specific with page references.

Patient's story:
{screenplay}

Begin clinical assessment:
"""

    def strategy_4_masterclass(self, screenplay: str) -> str:
        """Estratégia 4: Masterclass com Exemplos"""
        return f"""
You're teaching a MASTERCLASS on character transformation.
This screenplay is your case study.

LESSON STRUCTURE:

OPENING (200 words):
"Class, today we examine a fascinating character arc..."
- Hook with the most interesting aspect

DEEP DIVE ANALYSIS (400 words):
"Notice on page X how the character..."
- Point out 10 specific moments
- Compare to Casablanca, Godfather, Breaking Bad
- Apply McKee, Truby, Vogler frameworks

WORKSHOP EXERCISE (300 words):
"If you were rewriting this character..."
- Identify missed opportunities
- Suggest specific improvements
- Demonstrate with rewritten scenes

MASTERCLASS CONCLUSION (200 words):
"The key takeaway for writers is..."

Screenplay for analysis:
{screenplay}

Begin your masterclass:
"""

    def strategy_5_comparative(self, screenplay: str) -> str:
        """Estratégia 5: Análise Comparativa Exaustiva"""
        return f"""
Conduct an EXHAUSTIVE COMPARATIVE ANALYSIS of this character arc.

PART 1 - THEORETICAL COMPARISON (350 words):
Compare with ALL these frameworks:
- McKee's Gap (expectation vs result)
- Truby's 22 Steps (identify which steps)
- Vogler's Journey (which stages present)
- Field's Paradigm (plot points)
- Seger's Tools (which tools used)
- Egri's Premise (what's being proved)

PART 2 - FILM COMPARISON (350 words):
Compare with these character arcs:
- Rick (Casablanca) - similarities/differences
- Michael (Godfather) - parallels/contrasts
- Walter (Breaking Bad) - shared patterns
- Provide page-specific evidence

PART 3 - PSYCHOLOGICAL COMPARISON (300 words):
Compare with psychological models:
- Freudian (id/ego/superego conflicts)
- Jungian (shadow integration)
- Attachment theory (patterns)
- Trauma response (fight/flight/freeze)

Total: 1000+ words of dense comparison

Screenplay:
{screenplay}

Begin comparative analysis:
"""

    def test_strategy(self, strategy_name: str, prompt: str) -> Tuple[str, DepthMetrics, float]:
        """Testa uma estratégia e retorna resultado com métricas"""

        logger.info(f"Testing {strategy_name}...")

        start_time = time.time()

        # Chamar Ollama API
        api_url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 3000,
                "temperature": 0.8,
                "top_p": 0.95,
                "num_ctx": 131072
            }
        }

        try:
            response = requests.post(api_url, json=payload, timeout=300)

            if response.status_code == 200:
                result_json = response.json()
                output = result_json.get("response", "")
            else:
                output = f"Error: {response.status_code}"

        except Exception as e:
            output = f"Exception: {str(e)}"

        elapsed = time.time() - start_time

        # Analisar profundidade
        metrics = self.analyzer.analyze_depth(output)

        return output, metrics, elapsed

    def run_all_tests(self, screenplay: str) -> Dict[str, Any]:
        """Executa todos os testes e compara resultados"""

        logger.info("=" * 60)
        logger.info("INICIANDO TESTES DE PROFUNDIDADE")
        logger.info("=" * 60)

        strategies = {
            "1_academic": self.strategy_1_academic(screenplay),
            "2_detective": self.strategy_2_detective(screenplay),
            "3_psychoanalyst": self.strategy_3_psychoanalyst(screenplay),
            "4_masterclass": self.strategy_4_masterclass(screenplay),
            "5_comparative": self.strategy_5_comparative(screenplay)
        }

        results = {}

        for name, prompt in strategies.items():
            logger.info(f"\nTestando estratégia: {name}")
            output, metrics, elapsed = self.test_strategy(name, prompt)

            results[name] = {
                "output": output,
                "metrics": metrics.__dict__,
                "elapsed": elapsed
            }

            # Log resumo
            logger.info(f"  Palavras: {metrics.word_count}")
            logger.info(f"  Score geral: {metrics.overall_score:.2f}")
            logger.info(f"  Profundidade: {metrics.depth_score:.2f}")
            logger.info(f"  Riqueza: {metrics.richness_score:.2f}")
            logger.info(f"  Especificidade: {metrics.specificity_score:.2f}")

            # Salvar resultado individual
            result_file = self.results_dir / f"{name}_{int(time.time())}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(results[name], f, indent=2, ensure_ascii=False)

        # Análise comparativa
        comparison = self.compare_results(results)

        # Salvar comparação
        comparison_file = self.results_dir / f"comparison_{int(time.time())}.json"
        with open(comparison_file, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)

        return comparison

    def compare_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Compara e rankeia os resultados"""

        comparison = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "rankings": {},
            "winner": None,
            "detailed_scores": {}
        }

        # Coletar scores
        for name, data in results.items():
            metrics = data["metrics"]
            comparison["detailed_scores"][name] = {
                "overall": metrics["overall_score"],
                "depth": metrics["depth_score"],
                "richness": metrics["richness_score"],
                "specificity": metrics["specificity_score"],
                "words": metrics["word_count"],
                "page_refs": metrics["page_references"],
                "quotes": metrics["direct_quotes"],
                "theory": metrics["theory_citations"]
            }

        # Rankear por score geral
        ranked = sorted(
            comparison["detailed_scores"].items(),
            key=lambda x: x[1]["overall"],
            reverse=True
        )

        comparison["rankings"] = {
            name: idx + 1
            for idx, (name, _) in enumerate(ranked)
        }

        comparison["winner"] = ranked[0][0]

        # Análise do vencedor
        winner_name = comparison["winner"]
        winner_metrics = results[winner_name]["metrics"]

        comparison["winner_analysis"] = {
            "strategy": winner_name,
            "strengths": [],
            "total_score": winner_metrics["overall_score"]
        }

        # Identificar pontos fortes
        if winner_metrics["depth_score"] > 10:
            comparison["winner_analysis"]["strengths"].append("Excelente profundidade teórica")
        if winner_metrics["richness_score"] > 10:
            comparison["winner_analysis"]["strengths"].append("Rica em insights e contradições")
        if winner_metrics["specificity_score"] > 10:
            comparison["winner_analysis"]["strengths"].append("Altamente específica com evidências")
        if winner_metrics["word_count"] > 1000:
            comparison["winner_analysis"]["strengths"].append("Volume substancial de análise")

        return comparison

# Teste principal
if __name__ == "__main__":

    # Screenplay de teste
    test_screenplay = """
    FADE IN:

    INT. APARTMENT - DAY (PAGE 1)

    JOHN (35), unshaven, hollow eyes, stares at a framed photo
    of SARAH (30s, radiant smile). His hands shake.

    JOHN
    (to photo)
    I don't need anyone. Never did.

    He throws the photo in the trash. Beat. Retrieves it.

    JOHN (CONT'D)
    (whispered)
    Liar.

    INT. OFFICE - DAY (PAGE 15)

    John sits alone. MANAGER approaches.

    MANAGER
    John, you joining us for drinks?

    JOHN
    Got work.

    His screen is blank. Has been for an hour.

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
    """

    tester = StrategyTester()

    print("\n" + "=" * 60)
    print("🔬 TESTANDO ESTRATÉGIAS DE PROFUNDIDADE")
    print("=" * 60)

    comparison = tester.run_all_tests(test_screenplay)

    print("\n" + "=" * 60)
    print("📊 RESULTADOS FINAIS")
    print("=" * 60)

    print(f"\n🏆 VENCEDOR: {comparison['winner']}")
    print(f"   Score Total: {comparison['winner_analysis']['total_score']:.2f}")

    print("\n📈 RANKING COMPLETO:")
    for strategy, rank in sorted(comparison["rankings"].items(), key=lambda x: x[1]):
        scores = comparison["detailed_scores"][strategy]
        print(f"{rank}. {strategy}")
        print(f"   Overall: {scores['overall']:.2f}")
        print(f"   Words: {scores['words']}")
        print(f"   Depth: {scores['depth']:.2f}")
        print(f"   Richness: {scores['richness']:.2f}")
        print(f"   Specificity: {scores['specificity']:.2f}")

    print("\n💪 PONTOS FORTES DO VENCEDOR:")
    for strength in comparison["winner_analysis"]["strengths"]:
        print(f"   ✓ {strength}")

    print("\n📁 Resultados salvos em:", tester.results_dir)