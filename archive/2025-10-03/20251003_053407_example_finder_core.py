"""
ExampleFinderCore - Python Core 2 do Triple-Core

Analisa o resultado do Python Core 1 (especialista base) e busca:
1. Exemplos de soluções similares nos roteiros mestres
2. Exemplos de boa execução onde o usuário errou
3. Referências concretas de como mestres resolveram problemas similares

Fluxo:
- Recebe análise do Python Core 1
- Identifica problemas/violações
- Busca exemplos nos masters que resolvem esses problemas
- Retorna exemplos concretos com contexto
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from core.master_script_indexer import get_master_indexer, ScriptExample


@dataclass
class MasterExample:
    """Exemplo de um roteiro mestre que resolve um problema"""
    problem: str  # Problema que este exemplo resolve
    screenplay: str  # Nome do roteiro
    scene_context: str  # Contexto da cena
    character: str
    dialogue: str
    why_good: str  # Por que este exemplo é bom
    lesson: str  # Lição a ser aprendida


class ExampleFinderCore:
    """
    Python Core 2: Busca exemplos nos roteiros mestres.

    Este é o SEGUNDO CORE PYTHON no Triple-Core:
    1. Python Core 1 (Specialist) → Análise técnica objetiva
    2. Python Core 2 (ExampleFinder) → Exemplos de mestres  ← VOCÊ ESTÁ AQUI
    3. LLM Core → Enriquecimento com teoria

    O ExampleFinder analisa os problemas encontrados pelo Core 1
    e busca exemplos reais de como mestres (Tarantino, Nolan, etc)
    resolveram problemas similares.
    """

    def __init__(self):
        self.indexer = get_master_indexer()

    def analyze(self,
                base_analysis: Dict[str, Any],
                screenplay_text: str,
                max_examples_per_problem: int = 7) -> Dict[str, Any]:
        """
        Analisa os problemas do Core 1 e busca exemplos de soluções.

        Args:
            base_analysis: Resultado do Python Core 1 (especialista)
            screenplay_text: Texto do roteiro analisado
            max_examples_per_problem: Máximo de exemplos por problema

        Returns:
            Dicionário com exemplos de mestres organizados por problema
        """
        result = {
            'core': 'example_finder',
            'examples_found': [],
            'master_screenplays': self.indexer.list_available_screenplays(),
            'screenplays_searched': len(self.indexer.list_available_screenplays()),
            'problems_analyzed': []
        }

        # Extrair problemas/violações do Core 1
        problems = self._extract_problems(base_analysis)
        result['problems_analyzed'] = [p['title'] for p in problems]

        # Para cada problema, buscar exemplos
        for problem in problems:
            examples = self._find_examples_for_problem(
                problem,
                max_examples=max_examples_per_problem
            )
            result['examples_found'].extend(examples)

        # Estatísticas
        result['total_examples'] = len(result['examples_found'])
        result['coverage'] = len(result['examples_found']) / max(len(problems), 1)

        return result

    def _extract_problems(self, base_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai lista de problemas da análise do Core 1.

        Procura em:
        - rules_violated
        - rule_violations
        - recommendations (implied problems)
        """
        problems = []

        # Violações diretas
        if 'rule_violations' in base_analysis:
            for violation in base_analysis['rule_violations']:
                problems.append({
                    'rule_id': violation.get('rule_id', 'UNKNOWN'),
                    'title': violation.get('title', 'Unknown Problem'),
                    'severity': violation.get('severity', 'medium'),
                    'message': violation.get('message', ''),
                    'fix': violation.get('fix', '')
                })

        # Violações em formato string
        if 'rules_violated' in base_analysis:
            violations = base_analysis['rules_violated']
            if isinstance(violations, list):
                for v in violations:
                    if isinstance(v, str):
                        problems.append({
                            'rule_id': 'GENERIC',
                            'title': v,
                            'severity': 'medium',
                            'message': v,
                            'fix': ''
                        })

        # Recomendações (implied problems)
        if 'recommendations' in base_analysis:
            recommendations = base_analysis['recommendations']
            if isinstance(recommendations, list):
                for rec in recommendations[:15]:  # Máximo 15 recomendações (otimizado para cobertura)
                    # Inferir problema da recomendação
                    if 'voice' in rec.lower() or 'distinct' in rec.lower():
                        problems.append({
                            'rule_id': 'VOICE',
                            'title': 'Lacking distinct character voices',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('subtext' in rec.lower() or 'talk around' in rec.lower() or
                          'stating' in rec.lower() or 'directly' in rec.lower() or
                          'hide' in rec.lower() or 'layers' in rec.lower()):
                        problems.append({
                            'rule_id': 'SUBTEXT',
                            'title': 'Lacking subtext in dialogue',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'on-the-nose' in rec.lower() or 'on the nose' in rec.lower():
                        problems.append({
                            'rule_id': 'ON_THE_NOSE',
                            'title': 'On-the-nose dialogue',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'exposition' in rec.lower() or 'explaining' in rec.lower():
                        problems.append({
                            'rule_id': 'EXPOSITION',
                            'title': 'Exposition dumps in dialogue',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'rhythm' in rec.lower() or 'natural' in rec.lower() or 'speech pattern' in rec.lower():
                        problems.append({
                            'rule_id': 'RHYTHM',
                            'title': 'Unnatural speech rhythm',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'conflict in dialogue' in rec.lower() or 'tension' in rec.lower():
                        problems.append({
                            'rule_id': 'CONFLICT',
                            'title': 'Missing conflict in dialogue',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    # Structure-specific mappings
                    elif 'act' in rec.lower() or 'structure' in rec.lower() or 'proportion' in rec.lower():
                        problems.append({
                            'rule_id': 'STRUCTURE',
                            'title': 'Three-act structure problems',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'midpoint' in rec.lower():
                        problems.append({
                            'rule_id': 'MIDPOINT',
                            'title': 'Midpoint timing or strength issues',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'plot point' in rec.lower() or 'turning point' in rec.lower():
                        problems.append({
                            'rule_id': 'PLOT_POINT',
                            'title': 'Plot point placement problems',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })

        return problems

    def _find_examples_for_problem(self,
                                     problem: Dict[str, Any],
                                     max_examples: int = 7) -> List[Dict[str, Any]]:
        """
        Busca exemplos de roteiros mestres que resolvem este problema.

        Args:
            problem: Dicionário com info do problema
            max_examples: Máximo de exemplos a retornar

        Returns:
            Lista de exemplos formatados
        """
        # Keywords para busca baseadas no problema
        search_query = problem['title'] + ' ' + problem.get('message', '')

        # Buscar no indexer
        raw_examples: List[ScriptExample] = self.indexer.find_examples_by_problem(
            search_query,
            max_results=max_examples
        )

        # Formatar exemplos
        formatted_examples = []
        for example in raw_examples:
            formatted = {
                'problem_addressed': problem['title'],
                'screenplay': example.screenplay,
                'character': example.character,
                'dialogue': example.dialogue,
                'context': example.context,
                'scene_number': example.scene_number,
                'why_good': self._explain_why_good(example, problem),
                'lesson': self._extract_lesson(example, problem)
            }
            formatted_examples.append(formatted)

        return formatted_examples

    def _explain_why_good(self, example: ScriptExample, problem: Dict[str, Any]) -> str:
        """
        Explica por que este exemplo é uma boa solução para o problema.

        Análise heurística baseada no tipo de problema.
        """
        problem_title = problem['title'].lower()

        if 'subtext' in problem_title:
            return (f"This dialogue from {example.screenplay} shows subtext: "
                   f"the character says one thing but means another, creating layers.")

        elif 'voice' in problem_title or 'distinct' in problem_title:
            return (f"{example.character} in {example.screenplay} has a unique voice: "
                   f"distinctive word choice and rhythm that sets them apart.")

        elif 'exposition' in problem_title:
            return (f"This scene from {example.screenplay} conveys information "
                   f"naturally through action/conflict instead of explaining directly.")

        elif 'conflict' in problem_title:
            return (f"Notice how {example.screenplay} creates tension: "
                   f"characters have opposing goals creating natural conflict.")

        # Structure-specific explanations
        elif 'structure' in problem_title or 'act' in problem_title:
            return (f"{example.screenplay} demonstrates strong three-act structure: "
                   f"clear setup, confrontation, and resolution with proper pacing.")

        elif 'midpoint' in problem_title:
            return (f"The midpoint in {example.screenplay} shifts the story: "
                   f"a major revelation or reversal that changes the protagonist's approach.")

        elif 'plot point' in problem_title or 'turning point' in problem_title:
            return (f"{example.screenplay} places plot points effectively: "
                   f"major story turns occur at optimal moments for maximum impact.")

        else:
            return (f"This example from {example.screenplay} demonstrates "
                   f"professional-level execution of dialogue craft.")

    def _extract_lesson(self, example: ScriptExample, problem: Dict[str, Any]) -> str:
        """
        Extrai a lição principal que o escritor deve aprender deste exemplo.
        """
        problem_title = problem['title'].lower()

        if 'subtext' in problem_title:
            return "Let characters hide their true feelings. What they say ≠ what they mean."

        elif 'voice' in problem_title:
            return "Give each character unique vocabulary, rhythm, and speech patterns."

        elif 'exposition' in problem_title:
            return "Show information through behavior and conflict, not explanation."

        elif 'conflict' in problem_title:
            return "Every scene needs tension. Characters should want opposing things."

        # Structure-specific lessons
        elif 'structure' in problem_title or 'act' in problem_title:
            return "Follow the 25/50/25 rule: Setup (Act 1), Confrontation (Act 2), Resolution (Act 3)."

        elif 'midpoint' in problem_title:
            return "Place a major reversal at page 50-60. The hero must change strategy after this."

        elif 'plot point' in problem_title or 'turning point' in problem_title:
            return "Major turns at pages 25-30 (Plot Point 1) and 85-90 (Plot Point 2) create momentum."

        else:
            return f"Study how {example.screenplay} handles this - apply similar techniques."

    def get_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Gera resumo executivo dos exemplos encontrados.

        Args:
            analysis_result: Resultado do analyze()

        Returns:
            String com resumo
        """
        total = analysis_result['total_examples']
        problems = len(analysis_result['problems_analyzed'])
        screenplays = set(ex['screenplay'] for ex in analysis_result['examples_found'])

        summary = f"Found {total} examples from {len(screenplays)} master screenplays "
        summary += f"addressing {problems} problems identified in your script.\n\n"

        summary += "Master screenplays referenced:\n"
        for screenplay in sorted(screenplays):
            count = sum(1 for ex in analysis_result['examples_found']
                       if ex['screenplay'] == screenplay)
            summary += f"  • {screenplay} ({count} examples)\n"

        return summary
