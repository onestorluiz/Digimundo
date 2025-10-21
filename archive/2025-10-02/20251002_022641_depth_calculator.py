#!/usr/bin/env python3
"""
Depth Score Calculator
Calcula profundidade de análise Script Doctor
Valida expertise, aplicação de teoria, conexões e soluções acionáveis
"""

import re
from typing import Dict, List, Any


# Checklists de expertise por especialista
EXPERTISE_CHECKLISTS = {
    'dialogue': {
        'dialogue_functions': {
            'description': 'Identifica funções do diálogo',
            'indicators': ['exposition', 'characterization', 'subtext', 'conflict', 'voice', 'revelation'],
            'weight': 0.25
        },
        'dialogue_problems': {
            'description': 'Identifica problemas específicos',
            'indicators': ['on-the-nose', 'repetitive', 'unclear', 'unnatural', 'cliché', 'melodramatic'],
            'weight': 0.25
        },
        'character_voice': {
            'description': 'Analisa voz única',
            'indicators': ['distinct voice', 'character-specific', 'speech pattern', 'vocabulary', 'dialect'],
            'weight': 0.25
        },
        'theory': {
            'description': 'Aplica teoria McKee',
            'indicators': ['McKee', 'verbal action', 'beats', 'gap', 'turning point', 'dialogue design'],
            'weight': 0.25
        }
    },

    'structure': {
        'three_act': {
            'description': 'Analisa estrutura de 3 atos',
            'indicators': ['act 1', 'act 2', 'act 3', 'setup', 'confrontation', 'resolution', 'three-act'],
            'weight': 0.20
        },
        'plot_points': {
            'description': 'Identifica plot points',
            'indicators': ['inciting incident', 'turning point', 'midpoint', 'climax', 'crisis', 'plot point'],
            'weight': 0.20
        },
        'pacing': {
            'description': 'Analisa ritmo',
            'indicators': ['pacing', 'tempo', 'rhythm', 'momentum', 'beats', 'scene length'],
            'weight': 0.20
        },
        'arc': {
            'description': 'Examina arco narrativo',
            'indicators': ['arc', 'progression', 'escalation', 'payoff', 'setup', 'narrative'],
            'weight': 0.20
        },
        'innovation': {
            'description': 'Identifica inovações estruturais',
            'indicators': ['non-linear', 'parallel', 'flashback', 'temporal', 'timeline', 'structure'],
            'weight': 0.20
        }
    },

    'symbolism': {
        'visual_symbols': {
            'description': 'Identifica símbolos visuais',
            'indicators': ['symbol', 'metaphor', 'visual motif', 'imagery', 'recurring', 'symbolic'],
            'weight': 0.30
        },
        'meaning': {
            'description': 'Interpreta significado',
            'indicators': ['represents', 'symbolizes', 'meaning', 'significance', 'theme', 'stands for'],
            'weight': 0.25
        },
        'evolution': {
            'description': 'Traça evolução de símbolos',
            'indicators': ['evolves', 'transforms', 'payoff', 'foreshadowing', 'callback', 'arc'],
            'weight': 0.25
        },
        'network': {
            'description': 'Conecta símbolos',
            'indicators': ['connected', 'network', 'relationship', 'pattern', 'system', 'web'],
            'weight': 0.20
        }
    },

    'originality': {
        'unique_elements': {
            'description': 'Identifica originalidade',
            'indicators': ['original', 'unique', 'fresh', 'innovative', 'distinctive', 'novel'],
            'weight': 0.25
        },
        'derivative': {
            'description': 'Identifica derivações',
            'indicators': ['derivative', 'cliché', 'trope', 'similar to', 'reminiscent', 'borrowed'],
            'weight': 0.25
        },
        'comparison': {
            'description': 'Compara com outras obras',
            'indicators': ['compared to', 'similar', 'different from', 'like', 'unlike', 'references'],
            'weight': 0.25
        },
        'innovation': {
            'description': 'Avalia inovação',
            'indicators': ['subverts', 'deconstructs', 'reinvents', 'transforms', 'challenges', 'twist'],
            'weight': 0.25
        }
    },

    'psychemon': {
        'psychology': {
            'description': 'Analisa psicologia de personagem',
            'indicators': ['motivation', 'psychology', 'inner life', 'desire', 'fear', 'wound'],
            'weight': 0.30
        },
        'arc': {
            'description': 'Identifica arco psicológico',
            'indicators': ['transformation', 'growth', 'change', 'arc', 'development', 'evolution'],
            'weight': 0.25
        },
        'consistency': {
            'description': 'Avalia consistência',
            'indicators': ['consistent', 'believable', 'authentic', 'credible', 'realistic'],
            'weight': 0.25
        },
        'complexity': {
            'description': 'Avalia complexidade',
            'indicators': ['complex', 'nuanced', 'layered', 'multidimensional', 'depth', 'contradiction'],
            'weight': 0.20
        }
    },

    'submon': {
        'subtext_identification': {
            'description': 'Identifica subtexto',
            'indicators': ['subtext', 'underlying', 'implicit', 'unspoken', 'between the lines'],
            'weight': 0.30
        },
        'layers': {
            'description': 'Analisa camadas de significado',
            'indicators': ['layers', 'depth', 'meaning', 'surface', 'beneath', 'hidden'],
            'weight': 0.25
        },
        'gap_analysis': {
            'description': 'Analisa gap entre texto e subtexto',
            'indicators': ['gap', 'contrast', 'says vs means', 'contradiction', 'irony'],
            'weight': 0.25
        },
        'effectiveness': {
            'description': 'Avalia efetividade do subtexto',
            'indicators': ['effective', 'powerful', 'clear', 'obscure', 'balance', 'reveals'],
            'weight': 0.20
        }
    },

    'thememon': {
        'theme_identification': {
            'description': 'Identifica temas',
            'indicators': ['theme', 'central idea', 'message', 'meaning', 'explores', 'examines'],
            'weight': 0.30
        },
        'thematic_consistency': {
            'description': 'Avalia consistência temática',
            'indicators': ['consistent', 'unified', 'coherent', 'reinforces', 'supports'],
            'weight': 0.25
        },
        'integration': {
            'description': 'Analisa integração do tema',
            'indicators': ['integrated', 'woven', 'embedded', 'organic', 'natural', 'expressed'],
            'weight': 0.25
        },
        'depth': {
            'description': 'Avalia profundidade temática',
            'indicators': ['profound', 'deep', 'complex', 'nuanced', 'layered', 'universal'],
            'weight': 0.20
        }
    },

    'character_arcs': {
        'arc_structure': {
            'description': 'Analisa estrutura do arco',
            'indicators': ['arc', 'journey', 'transformation', 'change', 'growth', 'evolution'],
            'weight': 0.30
        },
        'motivation': {
            'description': 'Identifica motivação',
            'indicators': ['want', 'need', 'goal', 'desire', 'motivation', 'drive'],
            'weight': 0.25
        },
        'obstacles': {
            'description': 'Analisa obstáculos',
            'indicators': ['obstacle', 'conflict', 'challenge', 'opposition', 'struggle'],
            'weight': 0.25
        },
        'payoff': {
            'description': 'Avalia payoff do arco',
            'indicators': ['payoff', 'resolution', 'complete', 'satisfying', 'earned', 'culmination'],
            'weight': 0.20
        }
    },

    'relationships': {
        'dynamics': {
            'description': 'Analisa dinâmicas',
            'indicators': ['dynamic', 'relationship', 'interaction', 'chemistry', 'tension'],
            'weight': 0.30
        },
        'development': {
            'description': 'Avalia desenvolvimento',
            'indicators': ['develops', 'evolves', 'changes', 'grows', 'progression'],
            'weight': 0.25
        },
        'conflict': {
            'description': 'Analisa conflito relacional',
            'indicators': ['conflict', 'tension', 'opposition', 'clash', 'friction'],
            'weight': 0.25
        },
        'authenticity': {
            'description': 'Avalia autenticidade',
            'indicators': ['authentic', 'believable', 'realistic', 'genuine', 'credible'],
            'weight': 0.20
        }
    },

    'pacing': {
        'rhythm': {
            'description': 'Analisa ritmo',
            'indicators': ['rhythm', 'tempo', 'pace', 'speed', 'momentum'],
            'weight': 0.30
        },
        'variation': {
            'description': 'Avalia variação de ritmo',
            'indicators': ['varies', 'contrast', 'fast', 'slow', 'peaks', 'valleys'],
            'weight': 0.25
        },
        'scene_length': {
            'description': 'Analisa duração de cenas',
            'indicators': ['scene length', 'duration', 'beats', 'brevity', 'extended'],
            'weight': 0.25
        },
        'effectiveness': {
            'description': 'Avalia efetividade',
            'indicators': ['engaging', 'drags', 'rushed', 'balanced', 'maintains interest'],
            'weight': 0.20
        }
    },

    'tone_consistency': {
        'tone_identification': {
            'description': 'Identifica tom',
            'indicators': ['tone', 'mood', 'atmosphere', 'feel', 'emotional register'],
            'weight': 0.30
        },
        'consistency': {
            'description': 'Avalia consistência',
            'indicators': ['consistent', 'unified', 'coherent', 'stable', 'maintains'],
            'weight': 0.25
        },
        'shifts': {
            'description': 'Analisa mudanças de tom',
            'indicators': ['shifts', 'changes', 'transitions', 'tonal shift', 'contrast'],
            'weight': 0.25
        },
        'appropriateness': {
            'description': 'Avalia adequação',
            'indicators': ['appropriate', 'fits', 'matches', 'suits', 'genre'],
            'weight': 0.20
        }
    },

    'opening': {
        'hook': {
            'description': 'Analisa gancho inicial',
            'indicators': ['hook', 'opening', 'grabs attention', 'compelling', 'intrigue', 'first impression'],
            'weight': 0.30
        },
        'world_building': {
            'description': 'Avalia apresentação do mundo',
            'indicators': ['world', 'setting', 'establishes', 'introduces', 'context', 'foundation'],
            'weight': 0.25
        },
        'character_introduction': {
            'description': 'Analisa apresentação de personagens',
            'indicators': ['introduces', 'protagonist', 'character entry', 'first appearance', 'establishes character'],
            'weight': 0.25
        },
        'promise': {
            'description': 'Avalia promessa narrativa',
            'indicators': ['promise', 'genre expectation', 'tone', 'story question', 'direction', 'sets up'],
            'weight': 0.20
        }
    },

    'climax': {
        'crisis': {
            'description': 'Analisa momento de crise',
            'indicators': ['crisis', 'turning point', 'decision', 'dilemma', 'choice', 'critical moment'],
            'weight': 0.30
        },
        'escalation': {
            'description': 'Avalia escalação',
            'indicators': ['escalation', 'stakes', 'tension', 'intensity', 'peak', 'maximum'],
            'weight': 0.25
        },
        'payoff': {
            'description': 'Analisa payoff de setups',
            'indicators': ['payoff', 'resolution', 'callback', 'culmination', 'foreshadowing', 'fulfills'],
            'weight': 0.25
        },
        'impact': {
            'description': 'Avalia impacto emocional',
            'indicators': ['impact', 'emotional', 'cathartic', 'powerful', 'satisfying', 'resonant'],
            'weight': 0.20
        }
    },

    'resolution': {
        'closure': {
            'description': 'Analisa fechamento narrativo',
            'indicators': ['closure', 'resolution', 'resolves', 'concludes', 'wraps up', 'finale'],
            'weight': 0.30
        },
        'arc_completion': {
            'description': 'Avalia conclusão de arcos',
            'indicators': ['arc', 'character journey', 'transformation', 'completes', 'fulfills', 'destination'],
            'weight': 0.25
        },
        'emotional_satisfaction': {
            'description': 'Avalia satisfação emocional',
            'indicators': ['satisfying', 'earned', 'resonant', 'emotional payoff', 'fulfilling'],
            'weight': 0.25
        },
        'thematic_statement': {
            'description': 'Analisa afirmação temática',
            'indicators': ['theme', 'meaning', 'message', 'statement', 'point', 'what it means'],
            'weight': 0.20
        }
    },

    'action_description': {
        'clarity': {
            'description': 'Avalia claridade visual',
            'indicators': ['clear', 'visual', 'specific', 'concrete', 'vivid', 'precise'],
            'weight': 0.30
        },
        'economy': {
            'description': 'Analisa economia de linguagem',
            'indicators': ['concise', 'tight', 'efficient', 'brevity', 'streamlined', 'lean'],
            'weight': 0.25
        },
        'rhythm': {
            'description': 'Avalia ritmo da prosa',
            'indicators': ['rhythm', 'flow', 'pacing', 'sentence variety', 'beats', 'tempo'],
            'weight': 0.25
        },
        'filmability': {
            'description': 'Analisa tradutibilidade para tela',
            'indicators': ['filmable', 'shootable', 'visual storytelling', 'camera', 'cinematic', 'on screen'],
            'weight': 0.20
        }
    },

    'genre': {
        'conventions': {
            'description': 'Identifica convenções do gênero',
            'indicators': ['convention', 'trope', 'genre expectation', 'typical', 'standard', 'familiar'],
            'weight': 0.30
        },
        'subversion': {
            'description': 'Analisa subversões',
            'indicators': ['subverts', 'twist', 'unexpected', 'reinvents', 'challenges', 'defies'],
            'weight': 0.25
        },
        'tone_match': {
            'description': 'Avalia aderência ao tom do gênero',
            'indicators': ['tone', 'mood', 'atmosphere', 'genre appropriate', 'fits', 'matches'],
            'weight': 0.25
        },
        'audience_expectations': {
            'description': 'Analisa gestão de expectativas',
            'indicators': ['audience', 'expectation', 'delivers', 'satisfies', 'promise', 'genre contract'],
            'weight': 0.20
        }
    }
}


class DepthScoreCalculator:
    """Calcula score de profundidade Script Doctor."""

    def __init__(self, specialist_type: str):
        """
        Inicializa calculadora.

        Args:
            specialist_type: Tipo do especialista (dialogue, structure, etc)
        """
        self.specialist_type = specialist_type
        self.expertise_checklist = EXPERTISE_CHECKLISTS.get(specialist_type, {})

        if not self.expertise_checklist:
            raise ValueError(f"Unknown specialist type: {specialist_type}")

    def calculate_expertise_score(self, analysis_text: str) -> Dict[str, Any]:
        """Calcula score de expertise do especialista."""
        component_scores = {}
        total_score = 0.0

        for component, config in self.expertise_checklist.items():
            indicators_found = 0
            total_indicators = len(config['indicators'])

            for indicator in config['indicators']:
                pattern = rf'\b{re.escape(indicator)}\b'
                if re.search(pattern, analysis_text, re.IGNORECASE):
                    indicators_found += 1

            # Score do componente
            component_score = indicators_found / total_indicators if total_indicators > 0 else 0
            component_scores[component] = {
                'score': component_score,
                'indicators_found': indicators_found,
                'total_indicators': total_indicators,
                'weight': config['weight'],
                'description': config['description']
            }

            # Adiciona ao total ponderado
            total_score += component_score * config['weight']

        return {
            'total_score': total_score,
            'components': component_scores,
            'threshold': 0.50,
            'passed': total_score >= 0.50
        }

    def assess_theory_application(self, analysis_text: str) -> Dict[str, Any]:
        """Avalia se teoria é aplicada ou apenas citada."""
        # Identifica citações de teoria
        theory_patterns = [
            r'according\s+to\s+\w+',
            r'\w+\s+argues',
            r'\w+\s+emphasizes',
            r'the\s+book\s+discusses',
            r'the\s+book\s+explains',
            r'theory\s+suggests',
            r'McKee\s+says',
            r'McKee\s+explains'
        ]

        theory_citations = 0
        for pattern in theory_patterns:
            theory_citations += len(re.findall(pattern, analysis_text, re.IGNORECASE))

        # Identifica aplicações de teoria
        application_patterns = [
            r'(according\s+to\s+\w+.*?)(scene\s+\d+|character|dialogue|example)',
            r'(\w+\s+emphasizes.*?)(for\s+example|in\s+this\s+case|specifically|scene)',
            r'(theory.*?)(demonstrates|shows|reveals|seen\s+in)',
            r'(McKee.*?)(in\s+scene|character|dialogue|this\s+screenplay)'
        ]

        theory_applications = 0
        for pattern in application_patterns:
            matches = re.findall(pattern, analysis_text, re.IGNORECASE | re.DOTALL)
            theory_applications += len(matches)

        # Score
        if theory_citations == 0:
            application_ratio = 0.0
        else:
            application_ratio = min(1.0, theory_applications / theory_citations)

        return {
            'theory_citations': theory_citations,
            'theory_applications': theory_applications,
            'application_ratio': application_ratio,
            'threshold': 0.50,
            'passed': application_ratio >= 0.50
        }

    def assess_problem_interconnections(self, analysis_text: str) -> Dict[str, Any]:
        """Avalia se análise conecta problemas entre si."""
        # Identifica seção de DEPTH & SYNTHESIS
        sections = analysis_text.split('\n\n')
        depth_section = None

        for i, section in enumerate(sections):
            if any(keyword in section.upper() for keyword in ['DEPTH', 'SYNTHESIS', '5.']):
                depth_section = '\n\n'.join(sections[i:])
                break

        if not depth_section:
            return {
                'has_depth_section': False,
                'connections_found': 0,
                'connection_score': 0.0,
                'passed': False
            }

        # Procura por conectores causais
        connection_indicators = [
            r'stems\s+from',
            r'leads\s+to',
            r'causes?',
            r'results?\s+in',
            r'contributes?\s+to',
            r'interconnected',
            r'related\s+to',
            r'because\s+of',
            r'due\s+to',
            r'consequently',
            r'therefore',
            r'thus',
            r'as\s+a\s+result'
        ]

        connections_found = 0
        for indicator in connection_indicators:
            connections_found += len(re.findall(indicator, depth_section, re.IGNORECASE))

        # Score baseado em densidade de conexões
        depth_length = len(depth_section)
        if depth_length == 0:
            connection_density = 0
        else:
            connection_density = connections_found / (depth_length / 500)

        connection_score = min(1.0, connection_density)

        return {
            'has_depth_section': True,
            'connections_found': connections_found,
            'connection_density': connection_density,
            'connection_score': connection_score,
            'threshold': 0.40,
            'passed': connection_score >= 0.40
        }

    def assess_solution_actionability(self, analysis_text: str) -> Dict[str, Any]:
        """Avalia se soluções são acionáveis."""
        # Identifica seção de SOLUTIONS
        sections = analysis_text.split('\n\n')
        solutions_section = None

        for i, section in enumerate(sections):
            if any(keyword in section.upper() for keyword in ['SOLUTION', '4.']):
                solutions_section = '\n\n'.join(sections[i:i+6])
                break

        if not solutions_section:
            return {
                'has_solutions_section': False,
                'actionable_solutions': 0,
                'actionability_score': 0.0,
                'passed': False
            }

        # Indicadores de ação específica
        action_indicators = [
            r'replace.*with',
            r'change.*to',
            r'rewrite.*as',
            r'cut\s+scene',
            r'add\s+a\s+scene',
            r'move\s+scene',
            r'instead\s+of.*use',
            r'rephrase.*to',
            r'condense.*into',
            r'split.*into',
            r'combine.*with'
        ]

        actionable_solutions = 0
        for indicator in action_indicators:
            actionable_solutions += len(re.findall(indicator, solutions_section, re.IGNORECASE))

        # Penaliza frases vagas
        vague_phrases = [
            r'improve\s+the',
            r'work\s+on',
            r'focus\s+on',
            r'consider\s+adding',
            r'should\s+be\s+better',
            r'needs\s+improvement',
            r'could\s+benefit'
        ]

        vague_count = 0
        for phrase in vague_phrases:
            vague_count += len(re.findall(phrase, solutions_section, re.IGNORECASE))

        # Score
        total_solution_statements = actionable_solutions + vague_count
        if total_solution_statements == 0:
            actionability_score = 0.0
        else:
            actionability_score = actionable_solutions / total_solution_statements

        return {
            'has_solutions_section': True,
            'actionable_solutions': actionable_solutions,
            'vague_solutions': vague_count,
            'actionability_score': actionability_score,
            'threshold': 0.60,
            'passed': actionability_score >= 0.60
        }

    def calculate(self, analysis_text: str) -> Dict[str, Any]:
        """
        Calcula score completo de profundidade.

        Args:
            analysis_text: Texto da análise LLM

        Returns:
            Dict com score final e componentes detalhados
        """
        # Componentes
        expertise = self.calculate_expertise_score(analysis_text)
        theory_app = self.assess_theory_application(analysis_text)
        interconnections = self.assess_problem_interconnections(analysis_text)
        actionability = self.assess_solution_actionability(analysis_text)

        # Score final (média ponderada)
        depth_score = (
            expertise['total_score'] * 0.35 +
            theory_app['application_ratio'] * 0.25 +
            interconnections['connection_score'] * 0.20 +
            actionability['actionability_score'] * 0.20
        )

        return {
            'final_score': depth_score,
            'percentage': depth_score * 100,
            'passed': depth_score >= 0.60,
            'threshold': 0.60,
            'components': {
                'expertise': expertise,
                'theory_application': theory_app,
                'interconnections': interconnections,
                'actionability': actionability
            },
            'weights': {
                'expertise': 0.35,
                'theory_application': 0.25,
                'interconnections': 0.20,
                'actionability': 0.20
            }
        }


def main():
    """Teste da calculadora."""
    analysis_good = """
    1. INTERPRETATION
    According to McKee, dialogue should reveal character. In scene 3,
    Samantha says "I can't remember" which shows her vulnerability.

    5. DEPTH & SYNTHESIS
    The memory problems stem from her trauma, which leads to relationship
    issues. This interconnected pattern reveals deeper themes.

    4. SOLUTIONS
    Replace the vague line with "I remember his hands, but not his face"
    to create more specific emotional resonance.
    """

    analysis_bad = """
    The screenplay could be improved. The writer should work on character
    development and focus on better dialogue.
    """

    calc = DepthScoreCalculator('dialogue')

    print("GOOD ANALYSIS:")
    result_good = calc.calculate(analysis_good)
    print(f"Score: {result_good['percentage']:.1f}%")
    print(f"Passed: {result_good['passed']}")

    print("\nBAD ANALYSIS:")
    result_bad = calc.calculate(analysis_bad)
    print(f"Score: {result_bad['percentage']:.1f}%")
    print(f"Passed: {result_bad['passed']}")


if __name__ == '__main__':
    main()
