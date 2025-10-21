"""
HTML Report Generator - Gerador de Relatórios HTML Profissionais
Fase 4.A - Relatórios Interativos com Visualizações
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from jinja2 import Template, Environment, FileSystemLoader
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from apps.visualizations import ChartGenerator, SentimentVisualizer, ComparisonVisualizer, CommercialVisualizer
logger = logging.getLogger(__name__)

class HTMLReportGenerator:
    """
    Gerador de relatórios HTML profissionais
    """

    def __init__(self, template_dir: Optional[Path]=None):
        self.template_dir = template_dir or Path(__file__).parent / 'templates'
        self.chart_generator = ChartGenerator()
        self.sentiment_viz = SentimentVisualizer()
        self.comparison_viz = ComparisonVisualizer()
        self.commercial_viz = CommercialVisualizer()
        if self.template_dir.exists():
            self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        else:
            self.env = None

    def generate_executive_report(self, analysis_data: Dict[str, Any], output_path: Path, title: str='Relatório Executivo de Roteiro') -> bool:
        """
        Gera relatório executivo para produtores/investidores
        """
        try:
            report_data = {'title': title, 'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'), 'script_name': analysis_data.get('filename', 'Roteiro'), 'score': analysis_data.get('score', 0), 'grade': analysis_data.get('grade', 'N/A'), 'executive_summary': analysis_data.get('executive_summary', ''), 'strengths': analysis_data.get('strengths', []), 'weaknesses': analysis_data.get('weaknesses', []), 'recommendations': analysis_data.get('recommendations', []), 'commercial_prediction': self._prepare_commercial_data(analysis_data), 'visualizations': self._generate_executive_visualizations(analysis_data)}
            html_content = self._render_executive_template(report_data)
            output_path.write_text(html_content, encoding='utf-8')
            logger.info(f'Relatório executivo gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando relatório executivo: {e}')
            return False

    def generate_technical_report(self, analysis_data: Dict[str, Any], output_path: Path, title: str='Análise Técnica de Roteiro') -> bool:
        """
        Gera relatório técnico detalhado para roteiristas/diretores
        """
        try:
            report_data = {'title': title, 'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'), 'script_name': analysis_data.get('filename', 'Roteiro'), 'analysis': analysis_data.get('analysis', {}), 'deep_metrics': analysis_data.get('deep_metrics', {}), 'structure_analysis': analysis_data.get('structure_analysis', {}), 'character_analysis': analysis_data.get('character_analysis', {}), 'dialogue_analysis': analysis_data.get('dialogue_analysis', {}), 'sentiment_analysis': self._prepare_sentiment_data(analysis_data), 'recommendations': self._prepare_recommendations_data(analysis_data), 'visualizations': self._generate_technical_visualizations(analysis_data)}
            html_content = self._render_technical_template(report_data)
            output_path.write_text(html_content, encoding='utf-8')
            logger.info(f'Relatório técnico gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando relatório técnico: {e}')
            return False

    def generate_comparison_report(self, comparison_data: Dict[str, Any], output_path: Path, title: str='Análise Comparativa de Roteiros') -> bool:
        """
        Gera relatório de comparação entre roteiros
        """
        try:
            report_data = {'title': title, 'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'), 'script_a_name': comparison_data.get('script_a_name', 'Roteiro A'), 'script_b_name': comparison_data.get('script_b_name', 'Roteiro B'), 'overall_similarity': comparison_data.get('overall_similarity', 0), 'dimensions': comparison_data.get('dimensions', []), 'key_similarities': comparison_data.get('key_similarities', []), 'key_differences': comparison_data.get('key_differences', []), 'recommendation': comparison_data.get('recommendation', ''), 'visualizations': self._generate_comparison_visualizations(comparison_data)}
            html_content = self._render_comparison_template(report_data)
            output_path.write_text(html_content, encoding='utf-8')
            logger.info(f'Relatório comparativo gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando relatório comparativo: {e}')
            return False

    def generate_complete_report(self, analysis_data: Dict[str, Any], output_path: Path, title: str='Análise Completa de Roteiro') -> bool:
        """
        Gera relatório completo com todas as análises
        """
        try:
            report_data = {'title': title, 'generated_at': datetime.now().strftime('%d/%m/%Y %H:%M'), 'script_name': analysis_data.get('filename', 'Roteiro'), 'score': analysis_data.get('score', 0), 'grade': analysis_data.get('grade', 'N/A'), 'executive_summary': analysis_data.get('executive_summary', ''), 'full_analysis': analysis_data, 'visualizations': self._generate_all_visualizations(analysis_data)}
            html_content = self._render_complete_template(report_data)
            output_path.write_text(html_content, encoding='utf-8')
            logger.info(f'Relatório completo gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando relatório completo: {e}')
            return False

    def _generate_executive_visualizations(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Gera visualizações para relatório executivo"""
        visualizations = {}
        try:
            score = data.get('score', 0)
            visualizations['score_gauge'] = self.chart_generator.create_score_gauge(score, 'Score Geral')
            if 'commercial_prediction' in data:
                commercial = data['commercial_prediction']
                visualizations['commercial_gauge'] = self.commercial_viz.create_commercial_score_gauge(commercial.get('overall_score', 0), commercial.get('confidence', 0.8))
                if 'target_audience' in commercial:
                    visualizations['audience_pie'] = self.commercial_viz.create_target_audience_pie(commercial['target_audience'])
            if 'analysis' in data:
                categories = {'Estrutura': self._score_from_status(data['analysis'].get('structure')), 'Diálogos': self._score_from_status(data['analysis'].get('dialogue')), 'Ritmo': self._score_from_status(data['analysis'].get('pacing')), 'Personagens': self._score_from_status(data['analysis'].get('characters'))}
                visualizations['category_radar'] = self.chart_generator.create_category_radar(categories, 'Análise por Categoria')
        except Exception as e:
            logger.error(f'Erro gerando visualizações executivas: {e}')
        return visualizations

    def _generate_technical_visualizations(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Gera visualizações para relatório técnico"""
        visualizations = {}
        try:
            if 'sentiment_analysis' in data:
                sentiment = data['sentiment_analysis']
                visualizations['sentiment_dist'] = self.sentiment_viz.create_sentiment_distribution(sentiment.get('overall_sentiment', {}))
                if 'emotions' in sentiment:
                    visualizations['emotion_radar'] = self.sentiment_viz.create_emotion_radar(sentiment['emotions'])
                if 'character_sentiments' in sentiment:
                    visualizations['character_heatmap'] = self.sentiment_viz.create_character_sentiment_heatmap(sentiment['character_sentiments'])
            if 'structure_analysis' in data:
                structure = data['structure_analysis']
                metrics = {'Atos': structure.get('act_balance', 0), 'Cenas': structure.get('scene_distribution', 0), 'Pontos de Virada': structure.get('plot_points', 0), 'Arco Narrativo': structure.get('narrative_arc', 0)}
                visualizations['structure_bars'] = self.chart_generator.create_progress_bars(metrics, 'Métricas Estruturais')
        except Exception as e:
            logger.error(f'Erro gerando visualizações técnicas: {e}')
        return visualizations

    def _generate_comparison_visualizations(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Gera visualizações para relatório comparativo"""
        visualizations = {}
        try:
            similarity = data.get('overall_similarity', 0)
            visualizations['similarity_gauge'] = self.comparison_viz.create_similarity_gauge(similarity, 'Similaridade Geral')
            if 'dimensions' in data:
                dims = data['dimensions']
                script_a_data = {d['name']: d.get('script_a_score', 0) for d in dims}
                script_b_data = {d['name']: d.get('script_b_score', 0) for d in dims}
                visualizations['comparison_radar'] = self.comparison_viz.create_similarity_radar(script_a_data, script_b_data, data.get('script_a_name', 'Script A'), data.get('script_b_name', 'Script B'))
                visualizations['comparison_bars'] = self.comparison_viz.create_side_by_side_bars(script_a_data, script_b_data, data.get('script_a_name', 'Script A'), data.get('script_b_name', 'Script B'))
        except Exception as e:
            logger.error(f'Erro gerando visualizações comparativas: {e}')
        return visualizations

    def _generate_all_visualizations(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Gera todas as visualizações disponíveis"""
        visualizations = {}
        visualizations.update(self._generate_executive_visualizations(data))
        visualizations.update(self._generate_technical_visualizations(data))
        if 'sentiment_analysis' in data:
            visualizations['sentiment_dashboard'] = self.sentiment_viz.create_sentiment_summary_dashboard(data['sentiment_analysis'])
        if 'commercial_prediction' in data:
            visualizations['commercial_dashboard'] = self.commercial_viz.create_commercial_dashboard(data['commercial_prediction'])
        return visualizations

    def _render_executive_template(self, data: Dict[str, Any]) -> str:
        """Renderiza template executivo"""
        if self.env:
            template = self.env.get_template('executive_report.html')
            return template.render(**data)
        else:
            return self._generate_basic_html(data, 'executive')

    def _render_technical_template(self, data: Dict[str, Any]) -> str:
        """Renderiza template técnico"""
        if self.env:
            template = self.env.get_template('technical_report.html')
            return template.render(**data)
        else:
            return self._generate_basic_html(data, 'technical')

    def _render_comparison_template(self, data: Dict[str, Any]) -> str:
        """Renderiza template comparativo"""
        if self.env:
            template = self.env.get_template('comparison_report.html')
            return template.render(**data)
        else:
            return self._generate_basic_html(data, 'comparison')

    def _render_complete_template(self, data: Dict[str, Any]) -> str:
        """Renderiza template completo"""
        if self.env:
            template = self.env.get_template('complete_report.html')
            return template.render(**data)
        else:
            return self._generate_basic_html(data, 'complete')

    def _generate_basic_html(self, data: Dict[str, Any], report_type: str) -> str:
        """Gera HTML básico quando templates não estão disponíveis"""
        html = f"""\n<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{data.get('title', 'Relatório ScriptureMon')}</title>\n    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n    <style>\n        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}\n        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; }}\n        .score-badge {{ font-size: 3rem; font-weight: bold; }}\n        .visualization {{ margin: 2rem 0; min-height: 400px; }}\n        .section {{ margin: 3rem 0; }}\n        @media print {{ .no-print {{ display: none; }} }}\n    </style>\n</head>\n<body>\n    <div class="header text-center">\n        <h1>{data.get('title', 'Relatório ScriptureMon')}</h1>\n        <p>Gerado em {data.get('generated_at', '')}</p>\n    </div>\n    \n    <div class="container my-5">\n        {self._generate_report_content(data, report_type)}\n        \n        <div class="visualizations">\n            {self._generate_visualizations_html(data.get('visualizations', {}))}\n        </div>\n    </div>\n    \n    <script>\n        // Renderizar visualizações Plotly\n        {self._generate_plotly_scripts(data.get('visualizations', {}))}\n    </script>\n</body>\n</html>\n"""
        return html

    def _generate_report_content(self, data: Dict[str, Any], report_type: str) -> str:
        """Gera conteúdo do relatório baseado no tipo"""
        content = ''
        if report_type == 'executive':
            content = f"""\n            <div class="row section">\n                <div class="col-md-4 text-center">\n                    <div class="score-badge text-primary">{data.get('score', 0)}</div>\n                    <h3>Score Geral</h3>\n                    <span class="badge bg-primary fs-5">{data.get('grade', 'N/A')}</span>\n                </div>\n                <div class="col-md-8">\n                    <h3>Resumo Executivo</h3>\n                    <p class="lead">{data.get('executive_summary', '')}</p>\n                </div>\n            </div>\n            """
        elif report_type == 'technical':
            content = f"""\n            <div class="section">\n                <h2>Análise Técnica Detalhada</h2>\n                <div class="row">\n                    <div class="col-md-6">\n                        <h4>Estrutura</h4>\n                        <p>{data.get('structure_analysis', {})}</p>\n                    </div>\n                    <div class="col-md-6">\n                        <h4>Personagens</h4>\n                        <p>{data.get('character_analysis', {})}</p>\n                    </div>\n                </div>\n            </div>\n            """
        elif report_type == 'comparison':
            content = f"""\n            <div class="section">\n                <h2>Comparação: {data.get('script_a_name')} vs {data.get('script_b_name')}</h2>\n                <div class="text-center mb-4">\n                    <h3>Similaridade Geral: {data.get('overall_similarity', 0) * 100:.1f}%</h3>\n                </div>\n                <div class="row">\n                    <div class="col-md-6">\n                        <h4>Principais Semelhanças</h4>\n                        <ul>\n                            {''.join([f'<li>{s}</li>' for s in data.get('key_similarities', [])])}\n                        </ul>\n                    </div>\n                    <div class="col-md-6">\n                        <h4>Principais Diferenças</h4>\n                        <ul>\n                            {''.join([f'<li>{d}</li>' for d in data.get('key_differences', [])])}\n                        </ul>\n                    </div>\n                </div>\n            </div>\n            """
        return content

    def _generate_visualizations_html(self, visualizations: Dict[str, str]) -> str:
        """Gera HTML para visualizações"""
        html = ''
        for viz_id, viz_data in visualizations.items():
            html += f'<div id="{viz_id}" class="visualization"></div>\n'
        return html

    def _generate_plotly_scripts(self, visualizations: Dict[str, str]) -> str:
        """Gera scripts para renderizar visualizações Plotly"""
        scripts = ''
        for viz_id, viz_json in visualizations.items():
            scripts += f"\n            try {{\n                const {viz_id}_data = {viz_json};\n                Plotly.newPlot('{viz_id}', {viz_id}_data.data, {viz_id}_data.layout);\n            }} catch(e) {{\n                console.error('Erro renderizando {viz_id}:', e);\n            }}\n            "
        return scripts

    def _prepare_commercial_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara dados comerciais para o relatório"""
        commercial = data.get('commercial_prediction', {})
        return {'overall_score': commercial.get('overall_score', 0), 'confidence': commercial.get('confidence', 0), 'risk_level': commercial.get('risk_level', 'unknown'), 'market_category': commercial.get('market_category', 'unknown'), 'target_audience': commercial.get('target_audience', [])}

    def _prepare_sentiment_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara dados de sentimento para o relatório"""
        sentiment = data.get('sentiment_analysis', {})
        return {'overall_sentiment': sentiment.get('overall_sentiment', {}), 'emotions': sentiment.get('emotions', {}), 'character_sentiments': sentiment.get('character_sentiments', {}), 'timeline': sentiment.get('timeline', [])}

    def _prepare_recommendations_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepara recomendações para o relatório"""
        recs = data.get('recommendations', [])
        if isinstance(recs, dict):
            all_recs = []
            all_recs.extend(recs.get('quick_wins', []))
            all_recs.extend(recs.get('major_improvements', []))
            all_recs.extend(recs.get('advanced_techniques', []))
            return all_recs
        return recs

    def _score_from_status(self, status: str) -> float:
        """Converte status em score numérico"""
        status_scores = {'excellent': 90, 'good': 75, 'needs_improvement': 50, 'poor': 25}
        return status_scores.get(status, 0)
_html_generator = None

def get_html_generator() -> HTMLReportGenerator:
    """Retorna instância singleton do gerador HTML"""
    global _html_generator
    if _html_generator is None:
        _html_generator = HTMLReportGenerator()
    return _html_generator