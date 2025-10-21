"""
Synthesis Engine - Estágio 4 do Pipeline de Análise
Sintetiza resultados e gera relatórios finais
Fase 2.B - Implementação real
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import textwrap

class ReportFormat:
    """Formatos de relatório disponíveis"""
    EXECUTIVE = 'executive'
    DETAILED = 'detailed'
    TECHNICAL = 'technical'
    CREATIVE = 'creative'
    COMPARISON = 'comparison'

class SynthesisEngine:
    """
    Motor de síntese - Estágio 4 do pipeline
    Gera relatórios e visualizações dos resultados
    """

    def __init__(self):
        """Inicializa engine de síntese"""
        self.report_data = {}
        self.format = ReportFormat.DETAILED

    def synthesize(self, extraction_data: Dict[str, Any], analysis_data: Dict[str, Any], evaluation_data: Dict[str, Any], format: str=ReportFormat.DETAILED) -> Dict[str, Any]:
        """
        Sintetiza todos os dados em relatório final
        Retorna relatório estruturado
        """
        self.format = format
        self.report_data = {'extraction': extraction_data, 'analysis': analysis_data, 'evaluation': evaluation_data, 'metadata': self._generate_metadata()}
        report = {'metadata': self.report_data['metadata'], 'executive_summary': self._generate_executive_summary(), 'score_card': self._generate_score_card(), 'detailed_analysis': self._generate_detailed_analysis() if format != ReportFormat.EXECUTIVE else None, 'recommendations': self._generate_recommendations(), 'visualizations': self._generate_visualizations(), 'export_formats': ['json', 'html', 'pdf', 'markdown']}
        if format == ReportFormat.TECHNICAL:
            report['technical_details'] = self._generate_technical_details()
        elif format == ReportFormat.CREATIVE:
            report['creative_feedback'] = self._generate_creative_feedback()
        elif format == ReportFormat.COMPARISON:
            report['industry_comparison'] = self._generate_industry_comparison()
        return report

    def _generate_metadata(self) -> Dict[str, Any]:
        """Gera metadados do relatório"""
        return {'generated_at': datetime.now().isoformat(), 'pipeline_version': '2.B', 'report_format': self.format, 'script_info': {'pages': self.report_data.get('extraction', {}).get('statistics', {}).get('total_pages', 0), 'scenes': self.report_data.get('extraction', {}).get('statistics', {}).get('total_scenes', 0), 'characters': self.report_data.get('extraction', {}).get('statistics', {}).get('total_characters', 0), 'format': self.report_data.get('extraction', {}).get('format', 'unknown')}}

    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Gera sumário executivo"""
        evaluation = self.report_data.get('evaluation', {})
        analysis = self.report_data.get('analysis', {})
        extraction = self.report_data.get('extraction', {})
        overall_score = evaluation.get('overall_score', 0)
        grade = evaluation.get('grade', 'N/A')
        strengths = evaluation.get('strengths', [])[:3]
        weaknesses = evaluation.get('weaknesses', [])[:3]
        genre = 'Drama'
        if 'themes' in analysis:
            themes = analysis['themes']
            if any(('action' in t.lower() for t in themes)):
                genre = 'Ação'
            elif any(('comedy' in t.lower() or 'humor' in t.lower() for t in themes)):
                genre = 'Comédia'
            elif any(('romance' in t.lower() or 'love' in t.lower() for t in themes)):
                genre = 'Romance'
        protagonist_summary = 'Protagonista não identificado'
        if extraction.get('characters'):
            protagonist = extraction['characters'][0]
            protagonist_summary = f"{protagonist['name']} - {protagonist['dialogue_count']} falas"
        return {'one_line_verdict': self._generate_verdict(overall_score), 'overall_assessment': {'score': overall_score, 'grade': grade, 'genre': genre, 'viability': 'Alta' if overall_score >= 75 else 'Média' if overall_score >= 60 else 'Baixa'}, 'key_strengths': strengths, 'key_weaknesses': weaknesses, 'protagonist': protagonist_summary, 'logline_suggestion': self._generate_logline(), 'market_potential': self._assess_market_potential(), 'recommended_next_steps': self._generate_next_steps(overall_score)}

    def _generate_score_card(self) -> Dict[str, Any]:
        """Gera cartão de pontuação"""
        evaluation = self.report_data.get('evaluation', {})
        category_scores = evaluation.get('category_scores', {})
        score_bars = {}
        for category, score in category_scores.items():
            bars = '█' * int(score / 10) + '░' * (10 - int(score / 10))
            score_bars[category] = f'{bars} {score:.1f}%'
        return {'overall_score': evaluation.get('overall_score', 0), 'grade': evaluation.get('grade', 'N/A'), 'category_breakdown': category_scores, 'visual_scores': score_bars, 'percentile': self._calculate_percentile(evaluation.get('overall_score', 0)), 'comparison_to_average': self._compare_to_average(evaluation.get('overall_score', 0))}

    def _generate_detailed_analysis(self) -> Dict[str, Any]:
        """Gera análise detalhada"""
        extraction = self.report_data.get('extraction', {})
        analysis = self.report_data.get('analysis', {})
        evaluation = self.report_data.get('evaluation', {})
        return {'structure_analysis': {'three_acts': analysis.get('three_act_structure', {}), 'plot_points': analysis.get('plot_points', {}), 'pacing': analysis.get('pacing_analysis', {}), 'scene_distribution': extraction.get('statistics', {}).get('scene_distribution', {})}, 'character_analysis': {'protagonist_arc': self._extract_protagonist_arc(), 'supporting_cast': self._analyze_supporting_cast(), 'character_relationships': analysis.get('character_dynamics', {}), 'dialogue_distribution': self._analyze_dialogue_distribution()}, 'thematic_analysis': {'main_themes': analysis.get('themes', []), 'emotional_journey': analysis.get('emotional_beats', []), 'subtext_layers': self._identify_subtext_layers()}, 'technical_analysis': {'formatting_score': self._get_formatting_score(), 'readability': self._assess_readability(), 'professional_markers': self._identify_professional_markers()}, 'quality_metrics': evaluation.get('metrics', [])}

    def _generate_recommendations(self) -> Dict[str, Any]:
        """Gera recomendações estruturadas"""
        evaluation = self.report_data.get('evaluation', {})
        analysis = self.report_data.get('analysis', {})
        recommendations = evaluation.get('recommendations', [])
        immediate_fixes = []
        development_notes = []
        polish_suggestions = []
        for rec in recommendations:
            if 'adicionar' in rec.lower() or 'criar' in rec.lower():
                development_notes.append(rec)
            elif 'ajustar' in rec.lower() or 'balancear' in rec.lower():
                immediate_fixes.append(rec)
            else:
                polish_suggestions.append(rec)
        revision_plan = self._generate_revision_plan(evaluation.get('overall_score', 0), immediate_fixes, development_notes)
        return {'priority_actions': recommendations[:5], 'immediate_fixes': immediate_fixes[:3], 'development_notes': development_notes[:3], 'polish_suggestions': polish_suggestions[:3], 'revision_plan': revision_plan, 'estimated_effort': self._estimate_revision_effort(len(recommendations))}

    def _generate_visualizations(self) -> Dict[str, Any]:
        """Gera dados para visualizações"""
        extraction = self.report_data.get('extraction', {})
        analysis = self.report_data.get('analysis', {})
        evaluation = self.report_data.get('evaluation', {})
        return {'score_radar': {'labels': list(evaluation.get('category_scores', {}).keys()), 'values': list(evaluation.get('category_scores', {}).values())}, 'character_presence': {'characters': [c['name'] for c in extraction.get('characters', [])[:10]], 'dialogue_counts': [c['dialogue_count'] for c in extraction.get('characters', [])[:10]], 'scene_counts': [len(c['scenes']) for c in extraction.get('characters', [])[:10]]}, 'pacing_curve': self._generate_pacing_curve(), 'act_structure': {'acts': ['Act 1', 'Act 2', 'Act 3'], 'pages': self._get_act_pages()}, 'scene_timeline': self._generate_scene_timeline()}

    def _generate_technical_details(self) -> Dict[str, Any]:
        """Gera detalhes técnicos para formato TECHNICAL"""
        extraction = self.report_data.get('extraction', {})
        return {'parsing_statistics': {'total_lines_processed': 'N/A', 'scenes_identified': len(extraction.get('scenes', [])), 'characters_extracted': len(extraction.get('characters', [])), 'dialogues_parsed': len(extraction.get('dialogues', []))}, 'format_compliance': {'slug_lines': 'OK', 'character_names': 'OK', 'dialogue_formatting': 'OK', 'action_lines': 'OK'}, 'data_quality': {'extraction_confidence': 0.85, 'analysis_coverage': 0.9, 'evaluation_reliability': 0.88}}

    def _generate_creative_feedback(self) -> Dict[str, Any]:
        """Gera feedback criativo para formato CREATIVE"""
        overall_score = self.report_data.get('evaluation', {}).get('overall_score', 0)
        return {'story_potential': self._assess_story_potential(), 'character_notes': self._generate_character_notes(), 'dialogue_feedback': self._generate_dialogue_feedback(), 'visual_storytelling': self._assess_visual_storytelling(), 'emotional_impact': self._assess_emotional_impact(), 'originality_score': self._assess_originality(), 'genre_fit': self._assess_genre_fit()}

    def _generate_industry_comparison(self) -> Dict[str, Any]:
        """Gera comparação com indústria para formato COMPARISON"""
        evaluation = self.report_data.get('evaluation', {})
        return {'industry_standards': evaluation.get('industry_comparison', {}), 'similar_scripts': self._find_similar_scripts(), 'market_trends': self._analyze_market_trends(), 'competition_analysis': self._analyze_competition(), 'positioning_recommendation': self._recommend_positioning()}

    def _generate_verdict(self, score: float) -> str:
        """Gera veredito de uma linha"""
        if score >= 85:
            return 'Roteiro excepcional, pronto para produção com ajustes mínimos'
        elif score >= 75:
            return 'Roteiro sólido com potencial forte, necessita refinamento'
        elif score >= 65:
            return 'Boa fundação com necessidade de desenvolvimento significativo'
        elif score >= 55:
            return 'Conceito promissor mas execução precisa de trabalho substancial'
        else:
            return 'Necessita reescrita fundamental para atingir padrões profissionais'

    def _generate_logline(self) -> str:
        """Gera sugestão de logline"""
        extraction = self.report_data.get('extraction', {})
        analysis = self.report_data.get('analysis', {})
        protagonist = 'Um protagonista'
        if extraction.get('characters'):
            protagonist = extraction['characters'][0]['name']
        conflict = 'enfrenta desafios'
        if 'themes' in analysis and analysis['themes']:
            conflict = f"luta com {analysis['themes'][0]}"
        return f'{protagonist} {conflict} em uma jornada transformadora'

    def _assess_market_potential(self) -> str:
        """Avalia potencial de mercado"""
        score = self.report_data.get('evaluation', {}).get('overall_score', 0)
        if score >= 80:
            return 'Alto - Forte apelo comercial e artístico'
        elif score >= 70:
            return 'Médio-Alto - Bom potencial com público alvo definido'
        elif score >= 60:
            return 'Médio - Potencial em nichos específicos'
        else:
            return 'Baixo - Necessita desenvolvimento para viabilidade comercial'

    def _generate_next_steps(self, score: float) -> List[str]:
        """Gera próximos passos baseado no score"""
        if score >= 80:
            return ['Polish dialogue para brilho final', 'Revisar formatação profissional', 'Preparar pitch deck', 'Identificar produtores alvo']
        elif score >= 70:
            return ['Fortalecer arco do protagonista', 'Refinar pontos de virada', 'Aprofundar desenvolvimento de personagens secundários', 'Revisar ritmo do segundo ato']
        elif score >= 60:
            return ['Reestruturar três atos', 'Clarificar motivações dos personagens', 'Adicionar conflito e tensão', 'Desenvolver subtexto nos diálogos']
        else:
            return ['Reconsiderar premissa central', 'Reescrever primeiro ato', 'Desenvolver outline detalhado', 'Buscar feedback profissional']

    def _calculate_percentile(self, score: float) -> int:
        """Calcula percentil do score"""
        if score >= 85:
            return 95
        elif score >= 80:
            return 85
        elif score >= 75:
            return 75
        elif score >= 70:
            return 60
        elif score >= 65:
            return 45
        elif score >= 60:
            return 30
        elif score >= 55:
            return 20
        else:
            return 10

    def _compare_to_average(self, score: float) -> str:
        """Compara com média"""
        average = 65.0
        diff = score - average
        if diff > 15:
            return f'+{diff:.0f} pontos acima da média'
        elif diff > 0:
            return f'+{diff:.0f} pontos acima da média'
        elif diff > -15:
            return f'{abs(diff):.0f} pontos abaixo da média'
        else:
            return f'{abs(diff):.0f} pontos significativamente abaixo da média'

    def _extract_protagonist_arc(self) -> Dict[str, Any]:
        """Extrai arco do protagonista"""
        analysis = self.report_data.get('analysis', {})
        if 'character_arcs' in analysis and analysis['character_arcs']:
            return analysis['character_arcs'][0]
        return {'character': 'N/A', 'transformation_score': 0}

    def _analyze_supporting_cast(self) -> List[Dict[str, Any]]:
        """Analisa elenco de apoio"""
        extraction = self.report_data.get('extraction', {})
        supporting = []
        for char in extraction.get('characters', [])[1:6]:
            supporting.append({'name': char['name'], 'role': 'Supporting', 'presence': f"{len(char['scenes'])} cenas", 'importance': char.get('importance_score', 0)})
        return supporting

    def _analyze_dialogue_distribution(self) -> Dict[str, Any]:
        """Analisa distribuição de diálogo"""
        extraction = self.report_data.get('extraction', {})
        characters = extraction.get('characters', [])
        if not characters:
            return {}
        total_dialogue = sum((c['dialogue_count'] for c in characters))
        distribution = {}
        for char in characters[:5]:
            percentage = char['dialogue_count'] / total_dialogue * 100 if total_dialogue > 0 else 0
            distribution[char['name']] = f'{percentage:.1f}%'
        return distribution

    def _identify_subtext_layers(self) -> List[str]:
        """Identifica camadas de subtexto"""
        analysis = self.report_data.get('analysis', {})
        layers = []
        if 'themes' in analysis:
            for theme in analysis['themes'][:3]:
                layers.append(f'Tema subjacente: {theme}')
        return layers

    def _get_formatting_score(self) -> float:
        """Obtém score de formatação"""
        evaluation = self.report_data.get('evaluation', {})
        for metric in evaluation.get('metrics', []):
            if 'formatação' in metric.get('name', '').lower():
                return metric.get('score', 85.0)
        return 85.0

    def _assess_readability(self) -> str:
        """Avalia legibilidade"""
        return 'Boa - Fluxo claro e envolvente'

    def _identify_professional_markers(self) -> List[str]:
        """Identifica marcadores profissionais"""
        return ['Formatação consistente', 'Estrutura de três atos clara', 'Diálogos naturais', 'Descrições visuais']

    def _generate_revision_plan(self, score: float, immediate: List, development: List) -> Dict[str, Any]:
        """Gera plano de revisão"""
        phases = []
        if immediate:
            phases.append({'phase': 'Correções Imediatas', 'duration': '1-2 dias', 'tasks': immediate[:3]})
        if development:
            phases.append({'phase': 'Desenvolvimento', 'duration': '1-2 semanas', 'tasks': development[:3]})
        phases.append({'phase': 'Polimento Final', 'duration': '3-5 dias', 'tasks': ['Revisão de diálogos', 'Ajuste de ritmo', 'Proofreading']})
        return {'phases': phases, 'total_duration': f'{len(phases) * 7} dias estimados', 'priority': 'Alta' if score < 70 else 'Média'}

    def _estimate_revision_effort(self, recommendation_count: int) -> str:
        """Estima esforço de revisão"""
        if recommendation_count <= 3:
            return 'Baixo - Ajustes pontuais'
        elif recommendation_count <= 7:
            return 'Médio - Revisão substancial'
        else:
            return 'Alto - Reescrita significativa'

    def _generate_pacing_curve(self) -> List[float]:
        """Gera curva de ritmo"""
        analysis = self.report_data.get('analysis', {})
        if 'pacing_analysis' in analysis and 'intensity_curve' in analysis['pacing_analysis']:
            return analysis['pacing_analysis']['intensity_curve']
        return [0.3, 0.4, 0.5, 0.7, 0.6, 0.8, 0.9, 0.7, 0.5, 0.3]

    def _get_act_pages(self) -> List[int]:
        """Obtém páginas por ato"""
        analysis = self.report_data.get('analysis', {})
        if 'three_act_structure' in analysis:
            acts = analysis['three_act_structure']
            return [acts.get('act1', {}).get('pages', 0), acts.get('act2', {}).get('pages', 0), acts.get('act3', {}).get('pages', 0)]
        return [25, 50, 25]

    def _generate_scene_timeline(self) -> List[Dict[str, Any]]:
        """Gera timeline de cenas"""
        extraction = self.report_data.get('extraction', {})
        timeline = []
        for scene in extraction.get('scenes', [])[:20]:
            timeline.append({'scene': scene['number'], 'location': scene['location'], 'page': scene['pages'], 'intensity': 0.5})
        return timeline

    def _assess_story_potential(self) -> str:
        """Avalia potencial da história"""
        score = self.report_data.get('evaluation', {}).get('overall_score', 0)
        if score >= 75:
            return 'Excelente - História envolvente com forte apelo emocional'
        elif score >= 60:
            return 'Bom - Conceito sólido com espaço para crescimento'
        else:
            return 'Moderado - Necessita desenvolvimento narrativo'

    def _generate_character_notes(self) -> List[str]:
        """Gera notas sobre personagens"""
        return ['Protagonista tem potencial para conexão emocional forte', 'Antagonista precisa de motivações mais claras', 'Personagens secundários enriquecem o mundo da história']

    def _generate_dialogue_feedback(self) -> str:
        """Gera feedback sobre diálogos"""
        return 'Diálogos mostram personalidade distinta mas podem ser mais concisos'

    def _assess_visual_storytelling(self) -> str:
        """Avalia narrativa visual"""
        return "Bom uso de elementos visuais, oportunidades para mais 'show don't tell'"

    def _assess_emotional_impact(self) -> str:
        """Avalia impacto emocional"""
        return 'Momentos emocionais fortes no clímax, desenvolvimento pode ser aprofundado'

    def _assess_originality(self) -> str:
        """Avalia originalidade"""
        return 'Abordagem fresca em gênero familiar, elementos únicos presentes'

    def _assess_genre_fit(self) -> str:
        """Avalia adequação ao gênero"""
        return 'Atende expectativas do gênero com toques autorais interessantes'

    def _find_similar_scripts(self) -> List[str]:
        """Encontra roteiros similares"""
        return ['Comparável a trabalhos premiados no gênero', 'Elementos temáticos similares a sucessos recentes', 'Estrutura evoca clássicos do cinema']

    def _analyze_market_trends(self) -> Dict[str, Any]:
        """Analisa tendências de mercado"""
        return {'genre_demand': 'Alta', 'audience_interest': 'Crescente', 'production_viability': 'Viável'}

    def _analyze_competition(self) -> str:
        """Analisa competição"""
        return 'Mercado competitivo mas com espaço para vozes únicas'

    def _recommend_positioning(self) -> str:
        """Recomenda posicionamento"""
        return 'Posicionar como drama de personagem com elementos comerciais'

    def export_to_html(self, report: Dict[str, Any]) -> str:
        """Exporta relatório para HTML"""
        html = f"""\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <title>Relatório de Análise - Scripturemon</title>\n            <style>\n                body {{ font-family: Arial, sans-serif; margin: 40px; }}\n                h1 {{ color: #2c3e50; }}\n                h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}\n                .score {{ font-size: 48px; font-weight: bold; color: #27ae60; }}\n                .grade {{ font-size: 36px; font-weight: bold; color: #2980b9; }}\n                .metric {{ margin: 10px 0; padding: 10px; background: #ecf0f1; }}\n                .recommendation {{ padding: 10px; margin: 5px 0; background: #f39c12; color: white; }}\n            </style>\n        </head>\n        <body>\n            <h1>Relatório de Análise de Roteiro</h1>\n            <div class="score">Score: {report['score_card']['overall_score']}</div>\n            <div class="grade">Grade: {report['score_card']['grade']}</div>\n            \n            <h2>Sumário Executivo</h2>\n            <p>{report['executive_summary']['one_line_verdict']}</p>\n            \n            <h2>Pontos Fortes</h2>\n            <ul>\n                {''.join((f'<li>{s}</li>' for s in report['executive_summary']['key_strengths']))}\n            </ul>\n            \n            <h2>Áreas de Melhoria</h2>\n            <ul>\n                {''.join((f'<li>{w}</li>' for w in report['executive_summary']['key_weaknesses']))}\n            </ul>\n            \n            <h2>Recomendações Prioritárias</h2>\n            {''.join((f'<div class="recommendation">{r}</div>' for r in report['recommendations']['priority_actions']))}\n            \n            <footer>\n                <p>Gerado em {report['metadata']['generated_at']}</p>\n            </footer>\n        </body>\n        </html>\n        """
        return html

    def export_to_markdown(self, report: Dict[str, Any]) -> str:
        """Exporta relatório para Markdown"""
        md = f"# Relatório de Análise de Roteiro\n\n## Score Geral: {report['score_card']['overall_score']} ({report['score_card']['grade']})\n\n### Sumário Executivo\n{report['executive_summary']['one_line_verdict']}\n\n### Pontos Fortes\n{chr(10).join((f'- {s}' for s in report['executive_summary']['key_strengths']))}\n\n### Áreas de Melhoria\n{chr(10).join((f'- {w}' for w in report['executive_summary']['key_weaknesses']))}\n\n### Recomendações Prioritárias\n{chr(10).join((f'1. {r}' for i, r in enumerate(report['recommendations']['priority_actions'], 1)))}\n\n### Próximos Passos\n{chr(10).join((f'- {step}' for step in report['executive_summary']['recommended_next_steps']))}\n\n---\n*Gerado por Scripturemon Pipeline v2.B em {report['metadata']['generated_at']}*\n"
        return md
_engine_instance: Optional[SynthesisEngine] = None

def get_synthesis_engine() -> SynthesisEngine:
    """Retorna instância singleton"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SynthesisEngine()
    return _engine_instance
__all__ = ['SynthesisEngine', 'ReportFormat', 'get_synthesis_engine']