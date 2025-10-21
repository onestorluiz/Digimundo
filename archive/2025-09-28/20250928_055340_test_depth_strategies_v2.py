#!/usr/bin/env python3
"""
SISTEMA DE TESTE DE PROFUNDIDADE V2 - 10 ESTRATÉGIAS
======================================================
Testa 10 estratégias diferentes para encontrar a combinação perfeita
de volume, profundidade e especificidade.
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
    """Analisador de profundidade de texto aprimorado"""

    def __init__(self):
        self.theorists = ['McKee', 'Truby', 'Vogler', 'Seger', 'Field', 'Egri', 'Campbell', 'Snyder', 'Hauge', 'Yorke']
        self.technical_terms = [
            'protagonist', 'antagonist', 'inciting incident', 'climax', 'denouement',
            'character arc', 'transformation', 'wound', 'ghost', 'belief system',
            'defense mechanism', 'projection', 'sublimation', 'catharsis', 'anagnorisis',
            'peripeteia', 'hamartia', 'hubris', 'nemesis', 'deus ex machina',
            'three-act structure', 'midpoint', 'plot point', 'reversal', 'recognition'
        ]
        self.psychological_terms = [
            'ego', 'id', 'superego', 'unconscious', 'repression', 'denial',
            'rationalization', 'displacement', 'transference', 'shadow', 'persona',
            'archetype', 'complex', 'neurosis', 'psychosis', 'trauma', 'PTSD',
            'cognitive dissonance', 'attachment', 'avoidance', 'grief stages'
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
        film_comparisons = len(re.findall(r'similar to|like in|unlike|compared to|mirrors|echoes|parallels|reminiscent of', text, re.I))
        unique_insights = len(re.findall(r'what .+ miss|overlooked|subtle|nuanced|hidden|deeper meaning|underlying', text, re.I))
        contradictions = len(re.findall(r'however|but|yet|paradox|contradiction|ironic|despite|although', text, re.I))

        # Estrutura argumentativa
        cause_effect = len(re.findall(r'because|therefore|thus|consequently|as a result|leads to|causes|triggers', text, re.I))
        psych_mechanisms = sum(1 for term in self.psychological_terms if term.lower() in text.lower())
        transformation_beats = len(re.findall(r'shift|change|transform|evolve|growth|regression|breakthrough|turning point', text, re.I))

        # Calcular scores compostos AJUSTADOS
        depth_score = (
            (page_refs * 3) +
            (direct_quotes * 2) +
            (theory_citations * 4) +
            (framework_apps * 3) +
            (technical_terms * 2)
        ) / 10

        richness_score = (
            (min(word_count / 100, 15)) +  # Cap at 1500 words
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

        overall_score = (depth_score * 0.4 + richness_score * 0.3 + specificity_score * 0.3)

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

class StrategyTesterV2:
    """Testador aprimorado com 10 estratégias diferentes"""

    def __init__(self, model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M"):
        self.model = model
        self.analyzer = DepthAnalyzer()
        self.results_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/strategy_tests_v2")
        self.results_dir.mkdir(exist_ok=True)

    def strategy_1_hybrid_masterclass(self, screenplay: str) -> str:
        """Estratégia 1: Híbrida Masterclass + Academic"""
        return f"""
You're teaching an ADVANCED MASTERCLASS with academic rigor to PhD students.

PART 1: EVIDENCE EXCAVATION (minimum 300 words)
Start with: "Let's begin our deep analysis by examining the evidence..."

Like a detective, uncover:
- Quote EXACT dialogue from at least 5 different pages
- Note PRECISE page numbers for every claim
- Identify 3 patterns others would miss
- Find 2 contradictions or paradoxes

PART 2: THEORETICAL FRAMEWORK (minimum 300 words)
Continue with: "Now applying our theoretical lens..."

Apply these frameworks WITH SPECIFIC EXAMPLES:
- McKee's gap between expectation and result (cite page)
- Truby's need vs desire (with character quotes)
- Vogler's journey stages (identify at least 3)
- Include proper academic citations

PART 3: PSYCHOLOGICAL EXCAVATION (minimum 300 words)
Continue with: "The psychological architecture reveals..."

Deep psychological analysis:
- Map ALL defense mechanisms with evidence
- Track unconscious patterns across pages
- Identify the wound/ghost origin
- Chart the complete transformation timeline

PART 4: COMPARATIVE ANALYSIS (minimum 300 words)
Continue with: "When we compare this to cinematic masterpieces..."

Compare with:
- Rick (Casablanca) - specific parallels
- Michael (Godfather) - key differences
- Walter (Breaking Bad) - shared patterns
- One unique comparison others wouldn't make

TOTAL REQUIREMENT: 1200+ words minimum

Screenplay to analyze:
{screenplay}

Begin your masterclass:
"""

    def strategy_2_forensic_analysis(self, screenplay: str) -> str:
        """Estratégia 2: Análise Forense Detalhada"""
        return f"""
You are a FORENSIC SCREENPLAY ANALYST preparing expert testimony.

Your analysis must be EXHAUSTIVELY DETAILED and EVIDENCE-BASED.

FORENSIC REPORT STRUCTURE:

SECTION A: CRIME SCENE (THE SETUP) - 400 words minimum
- Initial character state (p.1-15)
- Every piece of evidence about the character's psychology
- Quote exact dialogue with page numbers
- Identify what's hidden beneath the surface

SECTION B: INVESTIGATION (THE JOURNEY) - 400 words minimum
- Track every character beat chronologically
- Document each transformation moment
- Note resistance patterns
- Identify breakthrough points

SECTION C: EXPERT TESTIMONY (THEORETICAL ANALYSIS) - 400 words minimum
- Apply McKee, Truby, Vogler with precision
- Compare to 3 similar character arcs
- Explain psychological mechanisms
- Predict future behavior patterns

Use clinical precision. Every claim needs evidence.
Minimum 1200 words total.

Evidence:
{screenplay}

Begin forensic report:
"""

    def strategy_3_story_doctor(self, screenplay: str) -> str:
        """Estratégia 3: Story Doctor Diagnosis"""
        return f"""
You are THE STORY DOCTOR. This screenplay is your patient.

MEDICAL CHART - CHARACTER ANALYSIS

PATIENT INTAKE (300 words):
Presenting symptoms:
- What's wrong with this character?
- Initial diagnostic observations (with page refs)
- Chief complaints (character's problems)

DIAGNOSTIC TESTS (400 words):
Running these tests:
- McKee Test: Gap between mask and true character
- Truby Test: Need vs Desire alignment
- Vogler Test: Journey stage identification
- Field Test: Character = Action principle

Results for each test with specific evidence.

TREATMENT PLAN (300 words):
- What's working (strengths)
- What needs treatment (weaknesses)
- Prescribed changes (specific suggestions)
- Prognosis (will the arc work?)

CONSULTATION NOTES (200 words):
- Compare to similar cases (other films)
- Second opinion considerations
- Risk factors

Total: 1200+ words of detailed diagnosis

Patient file:
{screenplay}

Begin diagnosis:
"""

    def strategy_4_quantum_analysis(self, screenplay: str) -> str:
        """Estratégia 4: Análise Quântica Multi-dimensional"""
        return f"""
Perform a QUANTUM CHARACTER ANALYSIS - examining multiple dimensions simultaneously.

DIMENSION 1: SURFACE REALITY (300 words)
What the character shows the world:
- Public persona (pages 1-15)
- Stated beliefs (quote dialogue)
- Conscious choices (list 5)

DIMENSION 2: SHADOW REALM (300 words)
What lurks beneath:
- Repressed emotions (identify 3)
- Unconscious patterns (track across pages)
- Hidden motivations (decode 2)

DIMENSION 3: TRANSFORMATIONAL FIELD (300 words)
The change process:
- Quantum leaps (sudden shifts)
- Gradual evolution (incremental changes)
- Regression waves (backsliding moments)

DIMENSION 4: PARALLEL UNIVERSES (300 words)
Alternative interpretations:
- How would Freud read this?
- Jung's perspective?
- Modern trauma theory?
- Your unique interpretation?

Connect all dimensions. Show how they interact.
Minimum 1200 words.

Screenplay for quantum analysis:
{screenplay}

Begin multi-dimensional scan:
"""

    def strategy_5_archaeological_dig(self, screenplay: str) -> str:
        """Estratégia 5: Escavação Arqueológica"""
        return f"""
You're an ARCHAEOLOGICAL EXPERT excavating layers of character.

EXCAVATION REPORT:

SURFACE LAYER (300 words):
"At the surface level, we find..."
- Visible behavior patterns
- Obvious character traits
- Surface dialogue (quote 5 examples)

SEDIMENT LAYER (350 words):
"Digging deeper, we uncover..."
- Hidden patterns
- Buried emotions
- Subtext beneath dialogue
- Connect to page numbers

FOSSIL LAYER (350 words):
"At the deepest level, we discover..."
- Core wound/ghost
- Original trauma
- Fundamental belief system
- Primal needs

RECONSTRUCTION (300 words):
"Piecing together the findings..."
- How layers connect
- Complete character portrait
- Comparison with known archetypes
- Dating the trauma (when did wound occur?)

Total: 1300+ words
Use archaeological metaphors throughout.

Site to excavate:
{screenplay}

Begin excavation:
"""

    def strategy_6_musical_composition(self, screenplay: str) -> str:
        """Estratégia 6: Composição Musical do Arco"""
        return f"""
You're a MASTER COMPOSER analyzing the character arc as a musical piece.

THE CHARACTER SYMPHONY:

MOVEMENT I: EXPOSITION (Andante) - 300 words
"The character theme begins in a minor key..."
- Opening notes (page 1 state)
- Leitmotif (recurring patterns)
- Tempo (pacing of reveal)
- Dissonance (internal conflict)

MOVEMENT II: DEVELOPMENT (Allegro) - 300 words
"The theme develops through variations..."
- Key changes (transformation moments)
- Crescendos (emotional peaks)
- Diminuendos (moments of retreat)
- Counterpoint (conflicting desires)

MOVEMENT III: RECAPITULATION (Moderato) - 300 words
"The themes converge and transform..."
- Harmonic resolution (or lack thereof)
- Thematic callbacks
- New orchestration (how character changed)

MOVEMENT IV: CODA (Finale) - 300 words
"The final notes resonate with..."
- Resolution or suspension
- Echo of opening theme
- What lingers after

Use musical terminology. Reference specific pages.
Compare to symphonies in film.

Score to analyze:
{screenplay}

Begin composition analysis:
"""

    def strategy_7_surgical_precision(self, screenplay: str) -> str:
        """Estratégia 7: Precisão Cirúrgica"""
        return f"""
You are a NEUROSURGEON operating on the character's psyche.

SURGICAL REPORT:

PRE-OP ASSESSMENT (300 words):
Patient: [Character name]
Presenting condition:
- Psychological state (page 1)
- Symptoms (list 5 with evidence)
- Vital signs (core beliefs, desires, fears)

SURGICAL PROCEDURE (400 words):
"Making the first incision on page X..."
- Locate the wound precisely
- Identify damaged areas
- Track healing process
- Note complications

POST-OP ANALYSIS (300 words):
- Success of transformation
- Remaining scar tissue
- Recovery prognosis
- Follow-up needed

PEER REVIEW (300 words):
- Compare to similar cases (other films)
- Cite medical literature (film theory)
- Second opinion from colleagues

Use medical precision. Every cut matters.
1300+ words minimum.

Patient chart:
{screenplay}

Begin surgery:
"""

    def strategy_8_time_traveler(self, screenplay: str) -> str:
        """Estratégia 8: Viajante do Tempo"""
        return f"""
You're a TIME TRAVELER analyzing the character across temporal dimensions.

TEMPORAL ANALYSIS REPORT:

THE PAST (350 words):
"Traveling back to the character's origins..."
- The wound that started everything
- Formative moments (hypothesize pre-story)
- How past haunts present (page evidence)
- Ghosts that won't rest

THE PRESENT (350 words):
"In the story's now..."
- Moment-by-moment transformation
- Time stamps on each change (page numbers)
- Temporal loops (repeated patterns)
- Breaking free attempts

THE FUTURE (350 words):
"Projecting forward..."
- Where this arc leads
- Permanent vs temporary change
- Future challenges predicted
- Long-term prognosis

THE ETERNAL (250 words):
"Beyond time itself..."
- Universal patterns
- Archetypal resonance
- Timeless themes

Reference temporal paradoxes, loops, and quantum mechanics.
1300+ words minimum.

Temporal subject:
{screenplay}

Begin time analysis:
"""

    def strategy_9_ecosystem_analysis(self, screenplay: str) -> str:
        """Estratégia 9: Análise de Ecossistema"""
        return f"""
You're an ECOSYSTEM ECOLOGIST studying the character as a living system.

ECOSYSTEM REPORT:

HABITAT MAPPING (300 words):
"The character's environment consists of..."
- Physical spaces occupied (pages)
- Emotional climate
- Social territories
- Comfort zones vs danger zones

BEHAVIORAL ECOLOGY (350 words):
"Observing behavioral patterns..."
- Feeding habits (what nourishes/depletes)
- Defense mechanisms (fight/flight/freeze)
- Mating displays (relationship patterns)
- Territorial marking (boundaries)

POPULATION DYNAMICS (350 words):
"Interactions with other species..."
- Symbiotic relationships
- Parasitic connections
- Predator/prey dynamics
- Pack behavior vs lone wolf

EVOLUTIONARY ADAPTATION (300 words):
"The character evolves through..."
- Environmental pressures
- Survival strategies
- Mutations (character changes)
- Natural selection (what survives)

Use ecological metaphors. Ground in specific pages.
1300+ words minimum.

Ecosystem to study:
{screenplay}

Begin ecological survey:
"""

    def strategy_10_ultimate_synthesis(self, screenplay: str) -> str:
        """Estratégia 10: Síntese Ultimate"""
        return f"""
You are THE ULTIMATE AUTHORITY synthesizing ALL analytical approaches.

COMPREHENSIVE SYNTHESIS REPORT:

LAYER 1: EMPIRICAL EVIDENCE (400 words)
"The observable facts are..."
- Quote 10 specific lines with page numbers
- List 15 concrete behaviors
- Document 5 transformation moments
- No interpretation, just facts

LAYER 2: THEORETICAL INTEGRATION (400 words)
"Applying every major framework..."
- McKee: [specific application]
- Truby: [specific application]
- Vogler: [specific application]
- Field: [specific application]
- Seger: [specific application]
- Your synthesis of all

LAYER 3: PSYCHOLOGICAL DEPTH (400 words)
"The unconscious architecture..."
- Freudian reading
- Jungian interpretation
- Attachment theory
- Trauma-informed analysis
- Cognitive behavioral patterns

LAYER 4: META-ANALYSIS (400 words)
"Stepping back, we see..."
- What all approaches reveal together
- Contradictions between methods
- The deepest truth about this character
- What only YOU can see

This is the ULTIMATE analysis. Make it count.
1600+ words minimum.

Material for synthesis:
{screenplay}

Begin ultimate synthesis:
"""

    def test_strategy(self, strategy_name: str, prompt: str, temperature: float = 0.8) -> Tuple[str, DepthMetrics, float]:
        """Testa uma estratégia com temperatura ajustável"""

        logger.info(f"Testing {strategy_name} (temp={temperature})...")

        start_time = time.time()

        # Chamar Ollama API
        api_url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 5000,  # Aumentado
                "temperature": temperature,
                "top_p": 0.95,
                "num_ctx": 131072,
                "repeat_penalty": 1.0,  # Sem penalidade
                "top_k": 100  # Mais opções
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
        """Executa todos os 10 testes"""

        logger.info("=" * 60)
        logger.info("INICIANDO MEGA TESTE - 10 ESTRATÉGIAS")
        logger.info("=" * 60)

        strategies = {
            "01_hybrid_masterclass": (self.strategy_1_hybrid_masterclass(screenplay), 0.8),
            "02_forensic_analysis": (self.strategy_2_forensic_analysis(screenplay), 0.7),
            "03_story_doctor": (self.strategy_3_story_doctor(screenplay), 0.8),
            "04_quantum_analysis": (self.strategy_4_quantum_analysis(screenplay), 0.9),
            "05_archaeological": (self.strategy_5_archaeological_dig(screenplay), 0.8),
            "06_musical_composition": (self.strategy_6_musical_composition(screenplay), 0.85),
            "07_surgical_precision": (self.strategy_7_surgical_precision(screenplay), 0.75),
            "08_time_traveler": (self.strategy_8_time_traveler(screenplay), 0.9),
            "09_ecosystem": (self.strategy_9_ecosystem_analysis(screenplay), 0.85),
            "10_ultimate_synthesis": (self.strategy_10_ultimate_synthesis(screenplay), 0.8)
        }

        results = {}

        for name, (prompt, temp) in strategies.items():
            logger.info(f"\n🔬 Testando: {name}")
            output, metrics, elapsed = self.test_strategy(name, prompt, temp)

            results[name] = {
                "output": output,
                "metrics": metrics.__dict__,
                "elapsed": elapsed,
                "temperature": temp
            }

            # Log resumo
            logger.info(f"  📊 Palavras: {metrics.word_count}")
            logger.info(f"  ⭐ Score geral: {metrics.overall_score:.2f}")
            logger.info(f"  🎯 Profundidade: {metrics.depth_score:.2f}")
            logger.info(f"  💎 Riqueza: {metrics.richness_score:.2f}")
            logger.info(f"  📍 Especificidade: {metrics.specificity_score:.2f}")
            logger.info(f"  ⏱️ Tempo: {elapsed:.1f}s")

            # Salvar resultado individual
            result_file = self.results_dir / f"{name}_{int(time.time())}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(results[name], f, indent=2, ensure_ascii=False)

        # Análise comparativa
        comparison = self.compare_results(results)

        # Salvar comparação
        comparison_file = self.results_dir / f"mega_comparison_{int(time.time())}.json"
        with open(comparison_file, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)

        # Salvar relatório markdown
        self.save_markdown_report(comparison, results)

        return comparison

    def compare_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Compara e rankeia os 10 resultados"""

        comparison = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_strategies": 10,
            "rankings": {},
            "winner": None,
            "top_3": [],
            "detailed_scores": {},
            "insights": []
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
                "theory": metrics["theory_citations"],
                "temperature": data["temperature"]
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
        comparison["top_3"] = [name for name, _ in ranked[:3]]

        # Análise dos top 3
        for i, (name, scores) in enumerate(ranked[:3], 1):
            analysis = {
                "rank": i,
                "strategy": name,
                "strengths": [],
                "total_score": scores["overall"],
                "word_count": scores["words"]
            }

            # Identificar pontos fortes
            if scores["depth"] > 5:
                analysis["strengths"].append(f"Excelente profundidade ({scores['depth']:.1f})")
            if scores["words"] > 800:
                analysis["strengths"].append(f"Volume adequado ({scores['words']} palavras)")
            if scores["page_refs"] > 5:
                analysis["strengths"].append(f"Rica em referências ({scores['page_refs']} páginas)")
            if scores["theory"] > 3:
                analysis["strengths"].append(f"Bem fundamentada ({scores['theory']} teoristas)")

            comparison["insights"].append(analysis)

        return comparison

    def save_markdown_report(self, comparison: Dict, results: Dict):
        """Salva relatório detalhado em Markdown"""

        report = f"""# 📊 MEGA TESTE - 10 ESTRATÉGIAS DE PROFUNDIDADE

## 🗓️ Data: {comparison['timestamp']}

## 🏆 TOP 3 VENCEDORES

"""

        for insight in comparison["insights"]:
            scores = comparison["detailed_scores"][insight["strategy"]]
            report += f"""### {insight['rank']}º Lugar: {insight['strategy']}
- **Score Total**: {scores['overall']:.2f}
- **Palavras**: {scores['words']}
- **Profundidade**: {scores['depth']:.2f}
- **Riqueza**: {scores['richness']:.2f}
- **Especificidade**: {scores['specificity']:.2f}
- **Temperatura**: {scores['temperature']}
- **Pontos Fortes**: {', '.join(insight['strengths'])}

"""

        report += """## 📈 RANKING COMPLETO

| Rank | Estratégia | Score | Palavras | Depth | Rich | Spec | Temp |
|------|------------|-------|----------|-------|------|------|------|
"""

        for name, rank in sorted(comparison["rankings"].items(), key=lambda x: x[1]):
            s = comparison["detailed_scores"][name]
            report += f"| {rank} | {name} | {s['overall']:.2f} | {s['words']} | {s['depth']:.1f} | {s['richness']:.1f} | {s['specificity']:.1f} | {s['temperature']} |\n"

        report += "\n## 🔍 ANÁLISE DETALHADA\n\n"

        # Adicionar preview dos top 3
        for name in comparison["top_3"]:
            report += f"### {name}\n"
            report += f"**Preview (primeiras 500 caracteres):**\n```\n{results[name]['output'][:500]}...\n```\n\n"

        # Salvar
        report_file = self.results_dir / f"MEGA_REPORT_{int(time.time())}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"📄 Relatório salvo: {report_file}")

# Teste principal
if __name__ == "__main__":

    # Screenplay de teste expandido
    test_screenplay = """
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

    INT. APARTMENT - NIGHT (PAGE 23)

    John watches old videos on his phone. Sarah's voice echoes.

    SARAH (ON VIDEO)
    You can't push everyone away forever.
    One day you'll need someone and—

    John THROWS the phone. It cracks but keeps playing.

    INT. THERAPIST'S OFFICE - DAY (PAGE 45)

    THERAPIST (60s, patient) waits. John fidgets.

    THERAPIST
    Why did you come today?

    JOHN
    My manager made me.

    THERAPIST
    No one can make you be here.
    You chose to walk through that door.

    John's leg bounces. Hand on door handle.

    JOHN
    (barely audible)
    She's dead. Three months.
    Car accident. My fault.
    """

    tester = StrategyTesterV2()

    print("\n" + "=" * 60)
    print("🚀 MEGA TESTE DE PROFUNDIDADE - 10 ESTRATÉGIAS")
    print("=" * 60)

    comparison = tester.run_all_tests(test_screenplay)

    print("\n" + "=" * 60)
    print("📊 RESULTADOS FINAIS")
    print("=" * 60)

    print(f"\n🥇 VENCEDOR: {comparison['winner']}")
    scores = comparison["detailed_scores"][comparison["winner"]]
    print(f"   Score Total: {scores['overall']:.2f}")
    print(f"   Palavras: {scores['words']}")

    print("\n🏆 TOP 3:")
    for i, name in enumerate(comparison["top_3"], 1):
        s = comparison["detailed_scores"][name]
        print(f"{i}. {name}")
        print(f"   Score: {s['overall']:.2f} | Words: {s['words']} | Temp: {s['temperature']}")

    print(f"\n📁 Resultados salvos em: {tester.results_dir}")
    print(f"📄 Relatório completo: MEGA_REPORT_*.md")