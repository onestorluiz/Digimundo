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

                    # Voice-specific mappings (specific → general)
                    # These must come BEFORE the generic VOICE pattern to avoid early matching
                    if ('distinct voice' in rec.lower() or 'voice distinctiveness' in rec.lower() or
                          'unique voice' in rec.lower() or ('character voice' in rec.lower() and 'distinct' in rec.lower())):
                        problems.append({
                            'rule_id': 'VOICE_DISTINCTIVENESS',
                            'title': 'Create distinct character voices',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('interchangeable' in rec.lower() or 'same voice' in rec.lower() or
                          'sound the same' in rec.lower() or 'indistinguishable' in rec.lower()):
                        problems.append({
                            'rule_id': 'INTERCHANGEABLE_DIALOGUE',
                            'title': 'Avoid interchangeable dialogue',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('voice consistency' in rec.lower() or 'inconsistent voice' in rec.lower() or
                          ('character consistency' in rec.lower() and 'voice' in rec.lower())):
                        problems.append({
                            'rule_id': 'VOICE_CONSISTENCY',
                            'title': 'Maintain voice consistency',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('vocabulary' in rec.lower() and 'character' in rec.lower()) or
                          'word choice' in rec.lower() or ('diction' in rec.lower() and 'character' in rec.lower())):
                        problems.append({
                            'rule_id': 'VOCABULARY_CHOICE',
                            'title': 'Vary vocabulary by character',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('sentence structure' in rec.lower() or ('syntax' in rec.lower() and 'character' in rec.lower()) or
                          ('sentence length' in rec.lower() and 'character' in rec.lower())):
                        problems.append({
                            'rule_id': 'SENTENCE_STRUCTURE',
                            'title': 'Vary sentence structure by character',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('verbal tics' in rec.lower() or 'speech patterns' in rec.lower() or
                          'mannerisms' in rec.lower() or 'catchphrase' in rec.lower()):
                        problems.append({
                            'rule_id': 'VERBAL_TICS',
                            'title': 'Add verbal tics and speech patterns',
                            'severity': 'low',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('formality' in rec.lower() or 'formal vs informal' in rec.lower() or
                          ('register' in rec.lower() and 'speech' in rec.lower())):
                        problems.append({
                            'rule_id': 'FORMALITY_LEVELS',
                            'title': 'Vary formality levels between characters',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('voice authenticity' in rec.lower() or 'authentic voice' in rec.lower() or
                          'believable voice' in rec.lower() or ('realistic' in rec.lower() and 'voice' in rec.lower())):
                        problems.append({
                            'rule_id': 'VOICE_AUTHENTICITY',
                            'title': 'Ensure authentic character voices',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })

                    # World building-specific mappings (specific → general)
                    elif ('world establishment' in rec.lower() or 'world defined' in rec.lower() or
                          'world parameters' in rec.lower() or ('establish' in rec.lower() and 'world' in rec.lower())):
                        problems.append({
                            'rule_id': 'WORLD_ESTABLISHMENT',
                            'title': 'Establish world clearly',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('world consistency' in rec.lower() or 'world rules' in rec.lower() or
                          'internal consistency' in rec.lower() or ('world' in rec.lower() and 'contradict' in rec.lower())):
                        problems.append({
                            'rule_id': 'WORLD_CONSISTENCY',
                            'title': 'Maintain world consistency',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('environmental detail' in rec.lower() or 'environment lacks' in rec.lower() or
                          'sensory detail' in rec.lower() or ('environment' in rec.lower() and 'detail' in rec.lower())):
                        problems.append({
                            'rule_id': 'ENVIRONMENTAL_DETAIL',
                            'title': 'Add environmental details',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('cultural depth' in rec.lower() or 'culture feels shallow' in rec.lower() or
                          'cultural elements' in rec.lower() or ('culture' in rec.lower() and ('shallow' in rec.lower() or 'generic' in rec.lower()))):
                        problems.append({
                            'rule_id': 'CULTURAL_DEPTH',
                            'title': 'Develop cultural depth',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('geography' in rec.lower() or 'geographic' in rec.lower() or
                          'spatial relationships' in rec.lower() or 'location clarity' in rec.lower()):
                        problems.append({
                            'rule_id': 'GEOGRAPHIC_CLARITY',
                            'title': 'Clarify geography and spatial relationships',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('time period' in rec.lower() or 'temporal' in rec.lower() or
                          ('anachronism' in rec.lower() and 'world' in rec.lower())):
                        problems.append({
                            'rule_id': 'TEMPORAL_CONSISTENCY',
                            'title': 'Maintain temporal consistency',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('technology' in rec.lower() or 'tech level' in rec.lower() or
                          'technological consistency' in rec.lower()):
                        problems.append({
                            'rule_id': 'TECHNOLOGY_CONSISTENCY',
                            'title': 'Maintain technology level consistency',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('world integration' in rec.lower() or ('world' in rec.lower() and 'story' in rec.lower() and 'integration' in rec.lower()) or
                          'world feels like backdrop' in rec.lower() or ('world' in rec.lower() and 'backdrop' in rec.lower())):
                        problems.append({
                            'rule_id': 'WORLD_INTEGRATION',
                            'title': 'Integrate world with story',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })

                    # Symbolism-specific mappings (specific → general)
                    elif ('purposeful symbol' in rec.lower() or 'symbolic purpose' in rec.lower() or
                          'meaningful symbol' in rec.lower() or ('symbol' in rec.lower() and ('arbitrary' in rec.lower() or 'decorative' in rec.lower()))):
                        problems.append({
                            'rule_id': 'PURPOSEFUL_SYMBOLISM',
                            'title': 'Create purposeful symbols',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('symbol consistency' in rec.lower() or 'symbolic consistency' in rec.lower() or
                          ('symbol' in rec.lower() and ('inconsistent' in rec.lower() or 'changes meaning' in rec.lower()))):
                        problems.append({
                            'rule_id': 'SYMBOL_CONSISTENCY',
                            'title': 'Maintain symbol consistency',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('visual symbol' in rec.lower() or 'visual symbolism' in rec.lower() or
                          'recurring visual' in rec.lower() or ('visual' in rec.lower() and 'symbolic' in rec.lower())):
                        problems.append({
                            'rule_id': 'VISUAL_SYMBOLISM',
                            'title': 'Establish visual symbols',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('metaphor clarity' in rec.lower() or ('metaphor' in rec.lower() and ('unclear' in rec.lower() or 'obscure' in rec.lower() or 'obvious' in rec.lower()))):
                        problems.append({
                            'rule_id': 'METAPHOR_CLARITY',
                            'title': 'Balance metaphor clarity',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('symbol payoff' in rec.lower() or 'symbols not resolved' in rec.lower() or
                          'symbolic resolution' in rec.lower() or ('symbol' in rec.lower() and 'payoff' in rec.lower())):
                        problems.append({
                            'rule_id': 'SYMBOL_PAYOFF',
                            'title': 'Ensure symbolic payoff',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('over-symbolic' in rec.lower() or 'too many symbols' in rec.lower() or
                          'symbol overwhelm' in rec.lower() or 'oversymbol' in rec.lower()):
                        problems.append({
                            'rule_id': 'OVER_SYMBOLISM',
                            'title': 'Reduce excessive symbolism',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character symbol' in rec.lower() or 'character symbolism' in rec.lower() or
                          'symbolic association' in rec.lower() or ('character' in rec.lower() and 'symbolic dimension' in rec.lower())):
                        problems.append({
                            'rule_id': 'CHARACTER_SYMBOLISM',
                            'title': 'Add character symbolism',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('setting symbolic' in rec.lower() or 'environmental symbolism' in rec.lower() or
                          'location symbolism' in rec.lower() or ('setting' in rec.lower() and 'symbolic' in rec.lower())):
                        problems.append({
                            'rule_id': 'ENVIRONMENTAL_SYMBOLISM',
                            'title': 'Use setting symbolically',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Visual motifs-specific mappings (specific → general)
                    elif ('motif establishment' in rec.lower() or 'establish motif' in rec.lower() or
                          'motifs established' in rec.lower() or ('motif' in rec.lower() and 'not established' in rec.lower())):
                        problems.append({
                            'rule_id': 'MOTIF_ESTABLISHMENT',
                            'title': 'Establish visual motifs clearly',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('motif recurrence' in rec.lower() or 'motif reappear' in rec.lower() or
                          'recurring motif' in rec.lower() or ('motif' in rec.lower() and ('once' in rec.lower() or 'disappear' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MOTIF_RECURRENCE',
                            'title': 'Create recurring motifs',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('motif consistency' in rec.lower() or 'visual consistency' in rec.lower() or
                          ('motif' in rec.lower() and ('inconsistent' in rec.lower() or 'varies' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MOTIF_CONSISTENCY',
                            'title': 'Maintain motif consistency',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('thematic motif' in rec.lower() or 'motif theme' in rec.lower() or
                          ('motif' in rec.lower() and ('decorative' in rec.lower() or 'thematic' in rec.lower()))):
                        problems.append({
                            'rule_id': 'THEMATIC_MOTIFS',
                            'title': 'Connect motifs to theme',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('cinematic motif' in rec.lower() or 'motif impact' in rec.lower() or
                          'visual impact' in rec.lower() or ('motif' in rec.lower() and 'cinematic' in rec.lower())):
                        problems.append({
                            'rule_id': 'CINEMATIC_MOTIFS',
                            'title': 'Create cinematically compelling motifs',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('motif clarity' in rec.lower() or ('motif' in rec.lower() and ('subtle' in rec.lower() or 'obvious' in rec.lower() or 'confusing' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MOTIF_CLARITY',
                            'title': 'Balance motif clarity',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('motif payoff' in rec.lower() or 'visual payoff' in rec.lower() or
                          ('motif' in rec.lower() and ('resolution' in rec.lower() or 'payoff' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MOTIF_PAYOFF',
                            'title': 'Ensure motif payoff',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('motif density' in rec.lower() or ('motif' in rec.lower() and ('too many' in rec.lower() or 'too few' in rec.lower() or 'frequency' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MOTIF_DENSITY',
                            'title': 'Balance motif density',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Genre-specific mappings (specific → general)
                    elif ('genre identity' in rec.lower() or 'genre unclear' in rec.lower() or
                          ('genre' in rec.lower() and ('confusing' in rec.lower() or 'mixed' in rec.lower()))):
                        problems.append({
                            'rule_id': 'GENRE_CLARITY',
                            'title': 'Clarify genre identity',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('missing convention' in rec.lower() or 'essential convention' in rec.lower() or
                          ('convention' in rec.lower() and ('absent' in rec.lower() or 'lacking' in rec.lower()))):
                        problems.append({
                            'rule_id': 'GENRE_CONVENTIONS',
                            'title': 'Meet genre conventions',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('trope' in rec.lower() and ('missing' in rec.lower() or 'absent' in rec.lower() or 'use' in rec.lower())):
                        problems.append({
                            'rule_id': 'GENRE_TROPES',
                            'title': 'Use genre tropes appropriately',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('genre expectation' in rec.lower() or 'audience expectation' in rec.lower() or
                          ('expectation' in rec.lower() and ('unmet' in rec.lower() or 'not met' in rec.lower()))):
                        problems.append({
                            'rule_id': 'GENRE_EXPECTATIONS',
                            'title': 'Meet audience expectations',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('hybrid genre' in rec.lower() or 'genre blend' in rec.lower() or
                          ('genre' in rec.lower() and ('balance' in rec.lower() or 'unbalanced' in rec.lower()))):
                        problems.append({
                            'rule_id': 'GENRE_HYBRID',
                            'title': 'Balance hybrid genres',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('genre pacing' in rec.lower() or ('pacing' in rec.lower() and 'genre' in rec.lower())):
                        problems.append({
                            'rule_id': 'GENRE_PACING',
                            'title': 'Align pacing with genre',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('genre tone' in rec.lower() or ('tone' in rec.lower() and 'genre' in rec.lower())):
                        problems.append({
                            'rule_id': 'GENRE_TONE',
                            'title': 'Align tone with genre',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('trope subversion' in rec.lower() or 'subvert trope' in rec.lower() or
                          ('trope' in rec.lower() and ('predictable' in rec.lower() or 'cliché' in rec.lower()))):
                        problems.append({
                            'rule_id': 'TROPE_SUBVERSION',
                            'title': 'Subvert predictable tropes',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Character psychology-specific mappings (specific → general)
                    elif ('internal conflict' in rec.lower() or ('conflict' in rec.lower() and 'internal' in rec.lower()) or
                          'inner conflict' in rec.lower() or ('character' in rec.lower() and 'conflicted' in rec.lower())):
                        problems.append({
                            'rule_id': 'INTERNAL_CONFLICT',
                            'title': 'Develop internal conflict',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('want vs need' in rec.lower() or 'want and need' in rec.lower() or
                          ('want' in rec.lower() and 'need' in rec.lower()) or 'want/need' in rec.lower()):
                        problems.append({
                            'rule_id': 'WANT_VS_NEED',
                            'title': 'Clarify want vs need',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character depth' in rec.lower() or 'psychological depth' in rec.lower() or
                          ('character' in rec.lower() and ('shallow' in rec.lower() or 'superficial' in rec.lower()))):
                        problems.append({
                            'rule_id': 'CHARACTER_DEPTH',
                            'title': 'Add character depth',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('emotional authenticity' in rec.lower() or ('emotion' in rec.lower() and ('fake' in rec.lower() or 'inauthentic' in rec.lower())) or
                          'emotional truth' in rec.lower() or ('feeling' in rec.lower() and 'manufactured' in rec.lower())):
                        problems.append({
                            'rule_id': 'EMOTIONAL_AUTHENTICITY',
                            'title': 'Increase emotional authenticity',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character consistency' in rec.lower() or 'psychological consistency' in rec.lower() or
                          ('character' in rec.lower() and ('inconsistent' in rec.lower() or 'contradicts' in rec.lower()))):
                        problems.append({
                            'rule_id': 'CHARACTER_CONSISTENCY',
                            'title': 'Maintain character consistency',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('vulnerability' in rec.lower() or 'vulnerable' in rec.lower() or
                          ('character' in rec.lower() and ('invulnerable' in rec.lower() or 'weakness' in rec.lower()))) and
                          'relationship' not in rec.lower()):
                        problems.append({
                            'rule_id': 'VULNERABILITY',
                            'title': 'Show character vulnerability',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('character growth' in rec.lower() or 'character stagnates' in rec.lower() or 'stagnant character' in rec.lower()) and
                          'arc' not in rec.lower() and 'transformation' not in rec.lower() and
                          'catalyst' not in rec.lower() and 'flat arc' not in rec.lower()):
                        problems.append({
                            'rule_id': 'CHARACTER_GROWTH',
                            'title': 'Develop character growth',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('defense mechanism' in rec.lower() or 'psychological defense' in rec.lower() or
                          ('character' in rec.lower() and ('deny' in rec.lower() or 'deflect' in rec.lower() or 'rationalize' in rec.lower()))):
                        problems.append({
                            'rule_id': 'PSYCHOLOGICAL_DEFENSE',
                            'title': 'Show psychological defenses',
                            'severity': 'low',
                            'message': rec,
                            'fix': rec
                        })

                    # Character arcs-specific mappings (specific → general)
                    elif ('arc establishment' in rec.lower() or 'establish arc' in rec.lower() or
                          ('arc' in rec.lower() and ('not established' in rec.lower() or 'unclear' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ARC_ESTABLISHMENT',
                            'title': 'Establish character arc',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('earned' in rec.lower() and ('transformation' in rec.lower() or 'change' in rec.lower()) or
                          'unearned change' in rec.lower() or 'sudden transformation' in rec.lower()):
                        problems.append({
                            'rule_id': 'ARC_EARNED',
                            'title': 'Earn the transformation',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('transformation' in rec.lower() or ('character' in rec.lower() and ('unchanged' in rec.lower() or 'no change' in rec.lower())) or
                          'character arc transformation' in rec.lower()):
                        problems.append({
                            'rule_id': 'ARC_TRANSFORMATION',
                            'title': 'Show character transformation',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('catalyst' in rec.lower() or 'inciting incident' in rec.lower() or
                          ('trigger' in rec.lower() and 'change' in rec.lower())):
                        problems.append({
                            'rule_id': 'ARC_CATALYST',
                            'title': 'Add transformation catalyst',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('resistance to change' in rec.lower() or ('resistance' in rec.lower() and 'arc' in rec.lower()) or
                          'character resists' in rec.lower() or 'pushback' in rec.lower()):
                        problems.append({
                            'rule_id': 'ARC_RESISTANCE',
                            'title': 'Show resistance to change',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('cost of change' in rec.lower() or 'sacrifice' in rec.lower() or
                          ('change' in rec.lower() and ('cost' in rec.lower() or 'price' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ARC_COST',
                            'title': 'Show cost of transformation',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('arc incomplete' in rec.lower() or 'arc unfinished' in rec.lower() or
                          ('arc' in rec.lower() and ('incomplete' in rec.lower() or 'unresolved' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ARC_COMPLETION',
                            'title': 'Complete the character arc',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('flat arc' in rec.lower() or 'static character' in rec.lower() or
                          ('character' in rec.lower() and 'doesn\'t change' in rec.lower())):
                        problems.append({
                            'rule_id': 'FLAT_ARC',
                            'title': 'Consider flat arc appropriateness',
                            'severity': 'low',
                            'message': rec,
                            'fix': rec
                        })

                    # Character relationships-specific mappings (specific → general)
                    elif ('central relationship' in rec.lower() or 'main relationship' in rec.lower() or
                          ('relationship' in rec.lower() and ('unclear' in rec.lower() or 'no clear' in rec.lower()))):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_CENTRAL',
                            'title': 'Define central relationship',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('chemistry' in rec.lower() or ('relationship' in rec.lower() and 'flat' in rec.lower()) or
                          'connection lacking' in rec.lower()):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_CHEMISTRY',
                            'title': 'Develop relationship chemistry',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('relationship conflict' in rec.lower() or 'conflict in relationship' in rec.lower()) and
                          'internal conflict' not in rec.lower()):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_CONFLICT',
                            'title': 'Add relationship conflict',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('relationship evolution' in rec.lower() or 'relationship static' in rec.lower() or
                          ('relationship' in rec.lower() and ('doesn\'t evolve' in rec.lower() or 'stagnant' in rec.lower()))):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_EVOLUTION',
                            'title': 'Show relationship evolution',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('relationship stakes' in rec.lower() or 'stakes in relationship' in rec.lower() or
                          ('relationship' in rec.lower() and 'low stakes' in rec.lower())):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_STAKES',
                            'title': 'Raise relationship stakes',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('relationship variety' in rec.lower() or 'relationship types' in rec.lower() or
                          'only one type of relationship' in rec.lower()):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_VARIETY',
                            'title': 'Add relationship variety',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('vulnerability in relationship' in rec.lower() or 'relationship vulnerability' in rec.lower() or
                          ('vulnerability' in rec.lower() and 'relationship' in rec.lower()) or
                          ('no vulnerability shown' in rec.lower() and 'relationship' in rec.lower())):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_VULNERABILITY',
                            'title': 'Show relationship vulnerability',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('relationship subtext' in rec.lower() or 'subtext in relationship' in rec.lower()) and
                          'dialogue subtext' not in rec.lower()):
                        problems.append({
                            'rule_id': 'RELATIONSHIP_SUBTEXT',
                            'title': 'Add relationship subtext',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Originality-specific mappings (specific → general)
                    elif ('concept originality' in rec.lower() or 'original concept' in rec.lower() or
                          ('concept' in rec.lower() and ('derivative' in rec.lower() or 'unoriginal' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ORIGINALITY_CONCEPT',
                            'title': 'Develop original concept',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('plot innovation' in rec.lower() or 'innovative plot' in rec.lower() or
                          ('plot' in rec.lower() and ('predictable' in rec.lower() or 'generic' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ORIGINALITY_PLOT',
                            'title': 'Innovate plot structure',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character originality' in rec.lower() or 'original characters' in rec.lower() or
                          ('characters' in rec.lower() and ('stereotypical' in rec.lower() or 'stock' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ORIGINALITY_CHARACTERS',
                            'title': 'Create original characters',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('dialogue freshness' in rec.lower() or 'fresh dialogue' in rec.lower() or
                          ('dialogue' in rec.lower() and ('cliché' in rec.lower() or 'overused' in rec.lower()))):
                        problems.append({
                            'rule_id': 'ORIGINALITY_DIALOGUE',
                            'title': 'Write fresh dialogue',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('derivative elements' in rec.lower() or 'too derivative' in rec.lower() or
                          'heavily derivative' in rec.lower()):
                        problems.append({
                            'rule_id': 'ORIGINALITY_DERIVATIVE',
                            'title': 'Reduce derivative elements',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('trope usage' in rec.lower() or 'tropes played straight' in rec.lower()) and
                          'genre' not in rec.lower() and 'subvert' not in rec.lower()):
                        problems.append({
                            'rule_id': 'ORIGINALITY_TROPES',
                            'title': 'Subvert or avoid tropes',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('innovation points' in rec.lower() or 'lack innovation' in rec.lower() or
                          'no innovation' in rec.lower()):
                        problems.append({
                            'rule_id': 'ORIGINALITY_INNOVATION',
                            'title': 'Add innovation points',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('unique elements' in rec.lower() or 'uniqueness low' in rec.lower() or
                          ('unique' in rec.lower() and 'lacking' in rec.lower())):
                        problems.append({
                            'rule_id': 'ORIGINALITY_UNIQUE',
                            'title': 'Increase unique elements',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })

                    # Market potential-specific mappings (specific → general)
                    elif ('market potential' in rec.lower() or 'commercial viability' in rec.lower() or
                          ('market' in rec.lower() and 'weak' in rec.lower() and 'genre' not in rec.lower())):
                        problems.append({
                            'rule_id': 'MARKET_VIABILITY',
                            'title': 'Improve market viability',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('audience appeal' in rec.lower() or 'audience size' in rec.lower() or
                          ('audience' in rec.lower() and ('limited' in rec.lower() or 'narrow' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MARKET_AUDIENCE',
                            'title': 'Broaden audience appeal',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('hook' in rec.lower() and ('market' in rec.lower() or 'commercial' in rec.lower() or
                          'marketable' in rec.lower() or 'strong hook' in rec.lower() or 'hook strength' in rec.lower())):
                        problems.append({
                            'rule_id': 'MARKET_HOOK',
                            'title': 'Strengthen commercial hook',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('genre marketability' in rec.lower() or 'genre appeal' in rec.lower() or
                          ('genre' in rec.lower() and 'unmarketable' in rec.lower())):
                        problems.append({
                            'rule_id': 'MARKET_GENRE',
                            'title': 'Improve genre marketability',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('commercial elements' in rec.lower() or 'marketable elements' in rec.lower() or
                          'lacks commercial appeal' in rec.lower()):
                        problems.append({
                            'rule_id': 'MARKET_ELEMENTS',
                            'title': 'Add commercial elements',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('market risks' in rec.lower() or 'commercial risks' in rec.lower() or
                          ('risk' in rec.lower() and 'market' in rec.lower())):
                        problems.append({
                            'rule_id': 'MARKET_RISKS',
                            'title': 'Mitigate market risks',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('revenue potential' in rec.lower() or 'revenue projection' in rec.lower() or
                          ('revenue' in rec.lower() and 'low' in rec.lower())):
                        problems.append({
                            'rule_id': 'MARKET_REVENUE',
                            'title': 'Increase revenue potential',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('global potential' in rec.lower() or 'international appeal' in rec.lower() or
                          ('global' in rec.lower() and ('limited' in rec.lower() or 'weak' in rec.lower()))):
                        problems.append({
                            'rule_id': 'MARKET_GLOBAL',
                            'title': 'Expand global potential',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Generic dialogue patterns (fallback for non-specific voice issues)
                    elif (('voice' in rec.lower() or 'distinct' in rec.lower()) and
                        'character intro' not in rec.lower() and
                        'visual description' not in rec.lower() and
                        'active voice' not in rec.lower() and
                        'passive voice' not in rec.lower()):  # Exclude action-related voice
                        problems.append({
                            'rule_id': 'VOICE',
                            'title': 'Lacking distinct character voices',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('subtext' in rec.lower() or 'talk around' in rec.lower() or
                          'stating' in rec.lower() or 'directly' in rec.lower() or
                          'hide' in rec.lower() or 'layers' in rec.lower()) and
                          'theme' not in rec.lower()):  # Exclude theme-related subtext
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
                    elif (('conflict in dialogue' in rec.lower() or 'tension' in rec.lower()) and
                          'climax' not in rec.lower() and 'confrontation' not in rec.lower()):  # Exclude climax-related
                        problems.append({
                            'rule_id': 'CONFLICT',
                            'title': 'Missing conflict in dialogue',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    # Structure-specific mappings (most specific → most general)
                    # Order matters: specific beats before generic structure
                    # Note: Climax and Resolution mappings come BEFORE this to prevent cross-contamination
                    elif (('inciting incident' in rec.lower() or
                          ('climax' in rec.lower() and 'weak' not in rec.lower() and 'final' not in rec.lower() and
                           'payoff' not in rec.lower() and 'stakes' not in rec.lower() and 'timing' not in rec.lower() and
                           'emotional' not in rec.lower() and 'clarity' not in rec.lower() and 'anticlimax' not in rec.lower() and
                           'confrontation' not in rec.lower() and 'battle' not in rec.lower() and 'showdown' not in rec.lower() and
                           'tension' not in rec.lower() and 'placement' not in rec.lower() and 'satisfying' not in rec.lower() and
                           'dragging' not in rec.lower() and 'ending' not in rec.lower() and 'long' not in rec.lower()) or
                          ('resolution' in rec.lower() and 'climax' not in rec.lower() and 'rushed' not in rec.lower() and
                           'loose' not in rec.lower() and 'ending' not in rec.lower() and 'denouement' not in rec.lower() and
                           'closure' not in rec.lower() and 'dragging' not in rec.lower() and 'overlong' not in rec.lower() and
                           'abrupt' not in rec.lower() and 'incomplete' not in rec.lower() and 'character arc' not in rec.lower() and
                           'secondary' not in rec.lower() and 'long' not in rec.lower() and 'satisfying' not in rec.lower() and
                           'emotional' not in rec.lower() and 'thematic' not in rec.lower())) and 'theme' not in rec.lower() and
                          'opening' not in rec.lower() and 'first' not in rec.lower() and
                          'underwhelming' not in rec.lower()):  # Exclude opening/climax/resolution-specific
                        problems.append({
                            'rule_id': 'BEATS',
                            'title': 'Structural beats clarity or timing',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif 'midpoint' in rec.lower() or 'reversal' in rec.lower():
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
                    elif (('pacing' in rec.lower() or 'pace' in rec.lower() or
                          'variations' in rec.lower() or 'slow' in rec.lower()) and
                          'opening' not in rec.lower() and 'first' not in rec.lower()):  # Exclude opening-specific
                        problems.append({
                            'rule_id': 'PACING',
                            'title': 'Pacing and rhythm issues',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('dramatic intensity' in rec.lower() or 'intensity' in rec.lower() or
                          'stakes' in rec.lower()):
                        problems.append({
                            'rule_id': 'INTENSITY',
                            'title': 'Dramatic intensity and stakes',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('complications' in rec.lower() or 'obstacles' in rec.lower() or
                          'progressive' in rec.lower()):
                        problems.append({
                            'rule_id': 'COMPLICATIONS',
                            'title': 'Progressive complications and obstacles',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('beat' in rec.lower() or 'confidence' in rec.lower()):
                        problems.append({
                            'rule_id': 'BEATS',
                            'title': 'Structural beats clarity or timing',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    # Pacing-specific mappings (specific → general)
                    elif ('scene length' in rec.lower() or 'vary scene' in rec.lower() or
                          'scene balance' in rec.lower() or 'monotonous' in rec.lower()):
                        problems.append({
                            'rule_id': 'SCENE_LENGTH',
                            'title': 'Scene length balance and variation',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('white space' in rec.lower() or 'dense blocks' in rec.lower() or
                          'break up paragraphs' in rec.lower() or 'readability' in rec.lower()):
                        problems.append({
                            'rule_id': 'WHITE_SPACE',
                            'title': 'White space and readability',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('momentum' in rec.lower() or 'building urgency' in rec.lower() or
                          'accelerate' in rec.lower() or 'flat pacing' in rec.lower()):
                        problems.append({
                            'rule_id': 'MOMENTUM',
                            'title': 'Momentum building and acceleration',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('breathing room' in rec.lower() or 'quiet moments' in rec.lower() or
                          'fatigue' in rec.lower() or 'relentless' in rec.lower()):
                        problems.append({
                            'rule_id': 'BREATHING_ROOM',
                            'title': 'Breathing room and pacing rhythm',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('opening' in rec.lower() and ('slow' in rec.lower() or 'first 10' in rec.lower() or
                          'tighten' in rec.lower())):
                        problems.append({
                            'rule_id': 'OPENING_PACE',
                            'title': 'Opening pace and hook',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('act 2' in rec.lower() or 'second act' in rec.lower() or
                          'midpoint' in rec.lower() and 'sag' in rec.lower()):
                        problems.append({
                            'rule_id': 'ACT2_SAG',
                            'title': 'Act 2 momentum and midpoint',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('transition' in rec.lower() or 'flow' in rec.lower() or
                          'match cut' in rec.lower() or 'sluggish' in rec.lower()):
                        problems.append({
                            'rule_id': 'TRANSITIONS',
                            'title': 'Transition speed and flow',
                            'severity': 'low',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('dialogue ratio' in rec.lower() or 'action-to-dialogue' in rec.lower() or
                          'dialogue-heavy' in rec.lower() or 'action-heavy' in rec.lower()):
                        problems.append({
                            'rule_id': 'DIALOGUE_RATIO',
                            'title': 'Action-to-dialogue balance',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Theme-specific mappings (specific → general)
                    elif ('central theme' in rec.lower() or 'clear theme' in rec.lower() or
                          'thematic anchor' in rec.lower() or 'unified theme' in rec.lower()):
                        problems.append({
                            'rule_id': 'CENTRAL_THEME',
                            'title': 'Clear central theme',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('theme consistency' in rec.lower() or 'thematic consistency' in rec.lower() or
                          'theme shifts' in rec.lower() or 'theme contradicts' in rec.lower() or
                          'thematic unity' in rec.lower()):
                        problems.append({
                            'rule_id': 'THEME_CONSISTENCY',
                            'title': 'Thematic consistency throughout',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('theme through action' in rec.lower() or 'show theme' in rec.lower() or
                          'theme stated' in rec.lower() or 'express theme' in rec.lower()):
                        problems.append({
                            'rule_id': 'SHOW_NOT_TELL',
                            'title': 'Theme expressed through action',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('heavy-handed' in rec.lower() or 'preachy' in rec.lower() or
                          'sermon' in rec.lower() or ('subtle' in rec.lower() and 'theme' in rec.lower())):
                        problems.append({
                            'rule_id': 'HEAVY_HANDED',
                            'title': 'Avoid heavy-handed thematic messaging',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('thematic depth' in rec.lower() or 'supporting themes' in rec.lower() or
                          'thematic layers' in rec.lower() or 'single theme' in rec.lower()):
                        problems.append({
                            'rule_id': 'THEMATIC_DEPTH',
                            'title': 'Multiple theme layers and depth',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('theme resolved' in rec.lower() or 'thematic resolution' in rec.lower() or
                          'thematic closure' in rec.lower() or 'theme payoff' in rec.lower() or
                          ('resolution' in rec.lower() and 'theme' in rec.lower())):
                        problems.append({
                            'rule_id': 'THEME_RESOLUTION',
                            'title': 'Theme resolution and closure',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('opposing viewpoints' in rec.lower() or 'counterargument' in rec.lower() or
                          'thematic complexity' in rec.lower() or 'one-sided' in rec.lower()):
                        problems.append({
                            'rule_id': 'OPPOSING_VIEWS',
                            'title': 'Opposing thematic viewpoints',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('thematic stakes' in rec.lower() or 'theme matters' in rec.lower() or
                          'thematic consequences' in rec.lower()):
                        problems.append({
                            'rule_id': 'THEME_STAKES',
                            'title': 'Theme stakes and consequences',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    # Tone-specific mappings (specific → general)
                    elif (('tone consistency' in rec.lower() or 'tonal consistency' in rec.lower() or
                          'tone shifts' in rec.lower() or 'jarring' in rec.lower()) and
                          'theme' not in rec.lower()):
                        problems.append({
                            'rule_id': 'TONE_CONSISTENCY',
                            'title': 'Tonal consistency and unity',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('establish' in rec.lower() and 'tone' in rec.lower()) or 'tone established' in rec.lower():
                        problems.append({
                            'rule_id': 'TONE_ESTABLISHMENT',
                            'title': 'Establish clear tone early',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('tonal transition' in rec.lower() or 'tone transition' in rec.lower() or
                          'smooth transition' in rec.lower() or 'abrupt shift' in rec.lower()):
                        problems.append({
                            'rule_id': 'TONE_TRANSITIONS',
                            'title': 'Smooth tonal transitions',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('genre' in rec.lower() and 'tone' in rec.lower()) or
                          'genre alignment' in rec.lower() or 'tone match' in rec.lower()):
                        problems.append({
                            'rule_id': 'GENRE_TONE',
                            'title': 'Genre-appropriate tone',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('emotional tone' in rec.lower() or 'emotional range' in rec.lower() or
                          'monotonous' in rec.lower()):
                        problems.append({
                            'rule_id': 'EMOTIONAL_RANGE',
                            'title': 'Emotional tone variation',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('atmospheric' in rec.lower() or 'atmosphere' in rec.lower()) and 'tone' not in rec.lower():
                        problems.append({
                            'rule_id': 'ATMOSPHERE',
                            'title': 'Atmospheric consistency',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('comic relief' in rec.lower() or ('humor' in rec.lower() and 'balance' in rec.lower())):
                        problems.append({
                            'rule_id': 'COMIC_RELIEF',
                            'title': 'Comic relief balance',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('climax' in rec.lower() and 'tone' in rec.lower()) or
                          'intensify tone' in rec.lower() or 'tonal climax' in rec.lower()):
                        problems.append({
                            'rule_id': 'TONAL_CLIMAX',
                            'title': 'Tonal climax intensity',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    # Subtext-specific mappings (specific → general)
                    elif ('on-the-nose' in rec.lower() or 'on the nose' in rec.lower() or
                          'stating emotions' in rec.lower() or 'tell feelings' in rec.lower()):
                        problems.append({
                            'rule_id': 'ON_THE_NOSE',
                            'title': 'On-the-nose dialogue lacks subtext',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('subtext' in rec.lower() or 'implicit' in rec.lower() or
                          'layers' in rec.lower() or 'beneath' in rec.lower()) and
                          'theme' not in rec.lower()):
                        problems.append({
                            'rule_id': 'SUBTEXT_DEPTH',
                            'title': 'Lacking subtext and implicit meaning',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('contradiction' in rec.lower() or 'say one thing mean another' in rec.lower() or
                          'words actions' in rec.lower()):
                        problems.append({
                            'rule_id': 'CONTRADICTIONS',
                            'title': 'Missing contradictions and subtext layers',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('power dynamic' in rec.lower() or 'relationship dynamic' in rec.lower() or
                          'dominance' in rec.lower() or 'status' in rec.lower()):
                        problems.append({
                            'rule_id': 'POWER_DYNAMICS',
                            'title': 'Power dynamics and subtext',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('hidden agenda' in rec.lower() or 'ulterior motive' in rec.lower() or
                          'secret intention' in rec.lower()):
                        problems.append({
                            'rule_id': 'HIDDEN_AGENDAS',
                            'title': 'Hidden agendas and motivations',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('silence' in rec.lower() or 'pause' in rec.lower() or 'beat' in rec.lower() or
                          'what not said' in rec.lower()):
                        problems.append({
                            'rule_id': 'MEANINGFUL_SILENCE',
                            'title': 'Meaningful silences and pauses',
                            'severity': 'low',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('avoidance' in rec.lower() or 'deflection' in rec.lower() or
                          'changing subject' in rec.lower() or 'evasion' in rec.lower()):
                        problems.append({
                            'rule_id': 'AVOIDANCE_PATTERNS',
                            'title': 'Avoidance patterns in dialogue',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('irony' in rec.lower() or 'double meaning' in rec.lower() or
                          'sarcasm' in rec.lower() or 'two levels' in rec.lower()):
                        problems.append({
                            'rule_id': 'DOUBLE_MEANINGS',
                            'title': 'Irony and double meanings',
                            'severity': 'low',
                            'message': rec,
                            'fix': rec
                        })
                    elif (('act' in rec.lower() or 'structure' in rec.lower() or 'proportion' in rec.lower()) and
                          'theme' not in rec.lower() and 'tone' not in rec.lower() and
                          'action' not in rec.lower() and 'active' not in rec.lower() and
                          'opening' not in rec.lower() and 'first' not in rec.lower() and 'hook' not in rec.lower()):  # Exclude theme/tone/action/opening-related
                        problems.append({
                            'rule_id': 'STRUCTURE',
                            'title': 'Three-act structure problems',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })

                    # Action-specific mappings (specific → general)
                    elif ('show don\'t tell' in rec.lower() or 'telling not showing' in rec.lower() or
                          'internal state' in rec.lower() or 'show not tell' in rec.lower()):
                        problems.append({
                            'rule_id': 'SHOW_NOT_TELL',
                            'title': 'Show don\'t tell - visualize internal states',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('present tense' in rec.lower() or 'tense issues' in rec.lower() or
                          'past tense' in rec.lower() or 'convert to present' in rec.lower()):
                        problems.append({
                            'rule_id': 'PRESENT_TENSE',
                            'title': 'Present tense in action lines',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('active voice' in rec.lower() or 'passive voice' in rec.lower() or
                          'voice issues' in rec.lower()):
                        problems.append({
                            'rule_id': 'ACTIVE_VOICE',
                            'title': 'Active voice in action description',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('visual clarity' in rec.lower() or 'vague description' in rec.lower() or
                          'specific visual' in rec.lower() or 'concrete details' in rec.lower()):
                        problems.append({
                            'rule_id': 'VISUAL_CLARITY',
                            'title': 'Visual clarity and concrete imagery',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('unfilmable' in rec.lower() or 'internal thought' in rec.lower() or
                          'camera cannot see' in rec.lower() or 'remembers' in rec.lower() or
                          'thinks' in rec.lower() or 'realizes' in rec.lower()):
                        problems.append({
                            'rule_id': 'UNFILMABLE',
                            'title': 'Avoid unfilmable elements',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('vivid verbs' in rec.lower() or 'weak verbs' in rec.lower() or
                          'strong verbs' in rec.lower() or 'action verbs' in rec.lower()):
                        problems.append({
                            'rule_id': 'VIVID_VERBS',
                            'title': 'Use vivid, specific verbs',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('concise action' in rec.lower() or 'paragraph length' in rec.lower() or
                          'action blocks' in rec.lower() or 'overlong' in rec.lower()):
                        problems.append({
                            'rule_id': 'CONCISE_ACTION',
                            'title': 'Keep action paragraphs concise',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character introduction' in rec.lower() or 'introduce character' in rec.lower() or
                          'first appearance' in rec.lower() or 'character intro' in rec.lower()):
                        problems.append({
                            'rule_id': 'CHARACTER_INTRO',
                            'title': 'Strong character introductions',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Formatting-specific mappings (specific → general)
                    elif ('scene heading' in rec.lower() or 'slugline' in rec.lower() or
                          'INT.' in rec or 'EXT.' in rec or 'scene format' in rec.lower()):
                        problems.append({
                            'rule_id': 'SCENE_HEADINGS',
                            'title': 'Proper scene heading format',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('page count' in rec.lower() or 'too long' in rec.lower() or
                          'too short' in rec.lower() or 'length' in rec.lower() and 'screenplay' in rec.lower()):
                        problems.append({
                            'rule_id': 'PAGE_COUNT',
                            'title': 'Appropriate screenplay length',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('white space' in rec.lower() or 'readability' in rec.lower() or
                          'dense' in rec.lower() or 'wall of text' in rec.lower()):
                        problems.append({
                            'rule_id': 'WHITE_SPACE',
                            'title': 'Proper white space and readability',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character name' in rec.lower() and 'format' in rec.lower() or
                          'all caps' in rec.lower() and 'character' in rec.lower()):
                        problems.append({
                            'rule_id': 'CHARACTER_NAMES',
                            'title': 'Proper character name formatting',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('dialogue format' in rec.lower() or 'parenthetical' in rec.lower() or
                          'dialogue block' in rec.lower()):
                        problems.append({
                            'rule_id': 'DIALOGUE_FORMAT',
                            'title': 'Proper dialogue formatting',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('camera direction' in rec.lower() or 'camera angle' in rec.lower() or
                          'CLOSE ON' in rec or 'ANGLE ON' in rec or 'POV' in rec):
                        problems.append({
                            'rule_id': 'CAMERA_DIRECTIONS',
                            'title': 'Avoid camera directions in spec scripts',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('we see' in rec.lower() or 'we hear' in rec.lower() or
                          'we watch' in rec.lower() or 'we notice' in rec.lower()):
                        problems.append({
                            'rule_id': 'WE_SEE_HEAR',
                            'title': 'Avoid "we see/hear" construction',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('transition' in rec.lower() and ('excessive' in rec.lower() or 'overuse' in rec.lower() or
                          'CUT TO' in rec or 'FADE' in rec) and
                          'flow' not in rec.lower() and 'jarring' not in rec.lower()):  # Exclude flow-related transitions
                        problems.append({
                            'rule_id': 'TRANSITIONS',
                            'title': 'Minimize transition usage',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Transitions/Flow-specific mappings (specific → general)
                    elif ('jarring' in rec.lower() or 'abrupt' in rec.lower() or
                          'sudden shift' in rec.lower() or 'disconnected' in rec.lower() and 'scene' in rec.lower()):
                        problems.append({
                            'rule_id': 'JARRING_TRANSITIONS',
                            'title': 'Avoid jarring scene transitions',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('smooth flow' in rec.lower() or 'seamless' in rec.lower() or
                          'natural connection' in rec.lower() or 'flow between' in rec.lower()):
                        problems.append({
                            'rule_id': 'SMOOTH_FLOW',
                            'title': 'Create smooth narrative flow',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('momentum' in rec.lower() and ('loses' in rec.lower() or 'loss' in rec.lower() or
                          'stalls' in rec.lower() or 'drag' in rec.lower())):
                        problems.append({
                            'rule_id': 'MOMENTUM_LOSS',
                            'title': 'Maintain momentum between scenes',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('match cut' in rec.lower() or 'visual connection' in rec.lower() or
                          'mirror' in rec.lower() and 'scene' in rec.lower() or
                          'parallel scene' in rec.lower()):
                        problems.append({
                            'rule_id': 'MATCH_CUT',
                            'title': 'Use visual connections and match cuts',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('cause and effect' in rec.lower() or 'consequence' in rec.lower() or
                          'results from' in rec.lower() or 'leads to' in rec.lower() and 'scene' in rec.lower()):
                        problems.append({
                            'rule_id': 'CAUSE_EFFECT',
                            'title': 'Establish cause-effect scene connections',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('temporal' in rec.lower() or 'timeline' in rec.lower() or
                          'time jump' in rec.lower() or 'when unclear' in rec.lower()):
                        problems.append({
                            'rule_id': 'TEMPORAL_CLARITY',
                            'title': 'Ensure temporal clarity between scenes',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('scene connection' in rec.lower() or 'connective tissue' in rec.lower() or
                          'link between scenes' in rec.lower() or 'connect scenes' in rec.lower()):
                        problems.append({
                            'rule_id': 'SCENE_CONNECTIONS',
                            'title': 'Strengthen scene-to-scene connections',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('flow rhythm' in rec.lower() or 'transition pacing' in rec.lower() or
                          'rhythm between scenes' in rec.lower()):
                        problems.append({
                            'rule_id': 'FLOW_RHYTHM',
                            'title': 'Improve flow and rhythm',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Opening-specific mappings (specific → general)
                    elif (('hook' in rec.lower() or 'grab attention' in rec.lower() or
                          'first impression' in rec.lower() or 'opening hook' in rec.lower()) and
                          'market' not in rec.lower() and 'commercial' not in rec.lower() and 'marketable' not in rec.lower()):
                        problems.append({
                            'rule_id': 'HOOK',
                            'title': 'Strong hook to grab attention',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('first 10 pages' in rec.lower() or 'first ten pages' in rec.lower() or
                          'opening pages' in rec.lower() or 'first pages' in rec.lower()):
                        problems.append({
                            'rule_id': 'FIRST_TEN_PAGES',
                            'title': 'Strengthen first 10 pages',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('inciting incident' in rec.lower() or 'catalyst' in rec.lower() or
                          'call to action' in rec.lower() or 'call to adventure' in rec.lower()):
                        problems.append({
                            'rule_id': 'INCITING_INCIDENT',
                            'title': 'Clarify inciting incident',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('establish world' in rec.lower() or 'world building' in rec.lower() and 'opening' in rec.lower() or
                          'introduce world' in rec.lower() or 'setting' in rec.lower() and 'opening' in rec.lower()):
                        problems.append({
                            'rule_id': 'WORLD_ESTABLISHMENT',
                            'title': 'Establish world and setting in opening',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('introduce protagonist' in rec.lower() or 'introduce character' in rec.lower() and 'opening' in rec.lower() or
                          'main character introduction' in rec.lower()):
                        problems.append({
                            'rule_id': 'OPENING_CHARACTER_INTRO',
                            'title': 'Introduce protagonist effectively',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('establish tone' in rec.lower() and 'opening' in rec.lower() or
                          'set tone' in rec.lower() and 'opening' in rec.lower() or
                          'tone in opening' in rec.lower()):
                        problems.append({
                            'rule_id': 'TONE_SETTING',
                            'title': 'Establish tone in opening',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('establish stakes' in rec.lower() or 'set up stakes' in rec.lower() or
                          "what's at stake" in rec.lower() or 'stakes unclear' in rec.lower()):
                        problems.append({
                            'rule_id': 'STAKES_ESTABLISHMENT',
                            'title': 'Establish stakes early',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('slow start' in rec.lower() or 'weak opening' in rec.lower() or
                          'drag in opening' in rec.lower() or 'opening drags' in rec.lower()):
                        problems.append({
                            'rule_id': 'SLOW_START',
                            'title': 'Avoid slow starts',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })

                    # Climax-specific mappings (specific → general)
                    elif ('final confrontation' in rec.lower() or 'climactic battle' in rec.lower() or
                          'ultimate showdown' in rec.lower() or 'final battle' in rec.lower()):
                        problems.append({
                            'rule_id': 'FINAL_CONFRONTATION',
                            'title': 'Strengthen final confrontation',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('climax stakes' in rec.lower() or 'everything at stake' in rec.lower() or
                          'maximum tension' in rec.lower() and 'climax' in rec.lower() or
                          'stakes' in rec.lower() and 'climax' in rec.lower()):
                        problems.append({
                            'rule_id': 'CLIMAX_STAKES',
                            'title': 'Raise stakes at climax',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('climax payoff' in rec.lower() or 'setup payoff' in rec.lower() and 'climax' in rec.lower() or
                          'satisfying climax' in rec.lower() or 'payoff' in rec.lower() and 'climax' in rec.lower()):
                        problems.append({
                            'rule_id': 'CLIMAX_PAYOFF',
                            'title': 'Deliver satisfying climax payoff',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('climax timing' in rec.lower() or 'climax too early' in rec.lower() or
                          'climax too late' in rec.lower() or 'climax placement' in rec.lower()):
                        problems.append({
                            'rule_id': 'CLIMAX_TIMING',
                            'title': 'Improve climax timing and placement',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('emotional peak' in rec.lower() or 'emotional climax' in rec.lower() or
                          'cathartic moment' in rec.lower() or 'emotional release' in rec.lower()):
                        problems.append({
                            'rule_id': 'EMOTIONAL_PEAK',
                            'title': 'Create emotional peak at climax',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('weak climax' in rec.lower() or 'anticlimax' in rec.lower() or
                          'underwhelming climax' in rec.lower() or 'climax falls flat' in rec.lower()):
                        problems.append({
                            'rule_id': 'WEAK_CLIMAX',
                            'title': 'Strengthen weak climax',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('climax clarity' in rec.lower() or 'confusing climax' in rec.lower() or
                          'unclear climax' in rec.lower() or 'climax' in rec.lower() and 'confusing' in rec.lower()):
                        problems.append({
                            'rule_id': 'CLIMAX_CLARITY',
                            'title': 'Clarify climax action and stakes',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('climax resolution' in rec.lower() or 'climax leads to resolution' in rec.lower() or
                          'resolve climax' in rec.lower() or 'climax to resolution' in rec.lower()):
                        problems.append({
                            'rule_id': 'CLIMAX_RESOLUTION',
                            'title': 'Connect climax to resolution',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })

                    # Resolution-specific mappings (specific → general)
                    elif ('rushed resolution' in rec.lower() or 'too quick ending' in rec.lower() or
                          'abrupt ending' in rec.lower() or 'rushed ending' in rec.lower()):
                        problems.append({
                            'rule_id': 'RUSHED_RESOLUTION',
                            'title': 'Avoid rushed resolution',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('loose ends' in rec.lower() or 'unresolved threads' in rec.lower() or
                          'incomplete resolution' in rec.lower() or 'unresolved' in rec.lower() and 'plot' in rec.lower()):
                        problems.append({
                            'rule_id': 'LOOSE_ENDS',
                            'title': 'Resolve loose ends and plot threads',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('emotional resolution' in rec.lower() or 'emotional closure' in rec.lower() or
                          'catharsis' in rec.lower() or 'emotional satisfaction' in rec.lower()):
                        problems.append({
                            'rule_id': 'EMOTIONAL_CLOSURE',
                            'title': 'Provide emotional closure',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('thematic resolution' in rec.lower() or 'thematic closure' in rec.lower() or
                          'theme payoff' in rec.lower() and 'resolution' in rec.lower() or
                          'theme' in rec.lower() and 'ending' in rec.lower()):
                        problems.append({
                            'rule_id': 'THEMATIC_CLOSURE',
                            'title': 'Deliver thematic resolution',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('character arc' in rec.lower() and 'resolution' in rec.lower() or
                          'character transformation' in rec.lower() and 'complete' in rec.lower() or
                          'arc closure' in rec.lower()):
                        problems.append({
                            'rule_id': 'CHARACTER_ARC_CLOSURE',
                            'title': 'Complete character arc in resolution',
                            'severity': 'high',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('denouement' in rec.lower() or 'falling action' in rec.lower() or
                          'resolution pacing' in rec.lower() or 'pace' in rec.lower() and 'ending' in rec.lower()):
                        problems.append({
                            'rule_id': 'DENOUEMENT_PACING',
                            'title': 'Improve denouement pacing',
                            'severity': 'medium',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('satisfying ending' in rec.lower() or 'satisfying conclusion' in rec.lower() or
                          'resolution payoff' in rec.lower() or 'unsatisfying' in rec.lower() and 'ending' in rec.lower()):
                        problems.append({
                            'rule_id': 'SATISFYING_ENDING',
                            'title': 'Create satisfying ending',
                            'severity': 'critical',
                            'message': rec,
                            'fix': rec
                        })
                    elif ('ending too long' in rec.lower() or 'dragging ending' in rec.lower() or
                          'overlong resolution' in rec.lower() or 'ending drags' in rec.lower()):
                        problems.append({
                            'rule_id': 'TOO_LONG_ENDING',
                            'title': 'Tighten overlong ending',
                            'severity': 'medium',
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
