"""
PDF Report Generator - Gerador de Relatórios PDF Profissionais
Fase 4.A - Relatórios PDF para Indústria Cinematográfica
"""
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether, Flowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    from reportlab.graphics import renderPDF
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
from .html_generator import HTMLReportGenerator
logger = logging.getLogger(__name__)

class PDFReportGenerator:
    """
    Gerador de relatórios PDF profissionais
    """

    def __init__(self):
        self.html_generator = HTMLReportGenerator()
        self.styles = None
        self.custom_styles = {}
        if REPORTLAB_AVAILABLE:
            self._setup_styles()

    def _setup_styles(self):
        """Configura estilos para o PDF"""
        self.styles = getSampleStyleSheet()
        self.custom_styles['Title'] = ParagraphStyle('CustomTitle', parent=self.styles['Title'], fontSize=24, textColor=colors.HexColor('#007bff'), spaceAfter=30, alignment=TA_CENTER)
        self.custom_styles['Heading1'] = ParagraphStyle('CustomHeading1', parent=self.styles['Heading1'], fontSize=18, textColor=colors.HexColor('#343a40'), spaceBefore=20, spaceAfter=10)
        self.custom_styles['Heading2'] = ParagraphStyle('CustomHeading2', parent=self.styles['Heading2'], fontSize=14, textColor=colors.HexColor('#495057'), spaceBefore=15, spaceAfter=8)
        self.custom_styles['BodyText'] = ParagraphStyle('CustomBody', parent=self.styles['BodyText'], fontSize=11, alignment=TA_JUSTIFY, spaceAfter=10)
        self.custom_styles['Score'] = ParagraphStyle('ScoreStyle', parent=self.styles['Title'], fontSize=36, textColor=colors.HexColor('#28a745'), alignment=TA_CENTER)

    def generate_executive_pdf(self, analysis_data: Dict[str, Any], output_path: Path, title: str='Relatório Executivo de Roteiro') -> bool:
        """
        Gera relatório executivo em PDF
        """
        if not REPORTLAB_AVAILABLE:
            return self._generate_pdf_via_html(analysis_data, output_path, title, 'executive')
        try:
            doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            story = []
            story.append(Paragraph(title, self.custom_styles['Title']))
            story.append(Spacer(1, 12))
            script_name = analysis_data.get('filename', 'Roteiro')
            story.append(Paragraph(f'<b>Roteiro:</b> {script_name}', self.styles['Normal']))
            story.append(Paragraph(f"<b>Data:</b> {datetime.now().strftime('%d/%m/%Y')}", self.styles['Normal']))
            story.append(Spacer(1, 20))
            score = analysis_data.get('score', 0)
            grade = analysis_data.get('grade', 'N/A')
            story.append(Paragraph(f'Score Geral', self.custom_styles['Heading1']))
            story.append(Paragraph(f'{score}/100', self.custom_styles['Score']))
            story.append(Paragraph(f'Grade: {grade}', self.styles['Normal']))
            story.append(Spacer(1, 20))
            story.append(Paragraph('Resumo Executivo', self.custom_styles['Heading1']))
            summary = analysis_data.get('executive_summary', 'Análise realizada com sucesso.')
            story.append(Paragraph(summary, self.custom_styles['BodyText']))
            story.append(Spacer(1, 20))
            story.append(self._create_strengths_weaknesses_section(analysis_data))
            if 'commercial_prediction' in analysis_data:
                story.append(PageBreak())
                story.append(self._create_commercial_section(analysis_data['commercial_prediction']))
            if 'recommendations' in analysis_data:
                story.append(self._create_recommendations_section(analysis_data['recommendations']))
            doc.build(story)
            logger.info(f'Relatório PDF executivo gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando PDF executivo: {e}')
            return False

    def generate_technical_pdf(self, analysis_data: Dict[str, Any], output_path: Path, title: str='Análise Técnica de Roteiro') -> bool:
        """
        Gera relatório técnico em PDF
        """
        if not REPORTLAB_AVAILABLE:
            return self._generate_pdf_via_html(analysis_data, output_path, title, 'technical')
        try:
            doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            story = []
            story.append(Paragraph(title, self.custom_styles['Title']))
            story.append(Spacer(1, 12))
            story.append(Paragraph('Análise por Categoria', self.custom_styles['Heading1']))
            story.append(self._create_category_analysis_table(analysis_data.get('analysis', {})))
            story.append(Spacer(1, 20))
            if 'structure_analysis' in analysis_data:
                story.append(Paragraph('Análise Estrutural', self.custom_styles['Heading1']))
                story.append(self._create_structure_analysis_section(analysis_data['structure_analysis']))
                story.append(Spacer(1, 20))
            if 'character_analysis' in analysis_data:
                story.append(PageBreak())
                story.append(Paragraph('Análise de Personagens', self.custom_styles['Heading1']))
                story.append(self._create_character_analysis_section(analysis_data['character_analysis']))
                story.append(Spacer(1, 20))
            if 'dialogue_analysis' in analysis_data:
                story.append(Paragraph('Análise de Diálogos', self.custom_styles['Heading1']))
                story.append(self._create_dialogue_analysis_section(analysis_data['dialogue_analysis']))
                story.append(Spacer(1, 20))
            if 'sentiment_analysis' in analysis_data:
                story.append(PageBreak())
                story.append(Paragraph('Análise de Sentimentos', self.custom_styles['Heading1']))
                story.append(self._create_sentiment_analysis_section(analysis_data['sentiment_analysis']))
            if 'recommendations' in analysis_data:
                story.append(PageBreak())
                story.append(self._create_technical_recommendations_section(analysis_data['recommendations']))
            doc.build(story)
            logger.info(f'Relatório PDF técnico gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando PDF técnico: {e}')
            return False

    def generate_comparison_pdf(self, comparison_data: Dict[str, Any], output_path: Path, title: str='Análise Comparativa de Roteiros') -> bool:
        """
        Gera relatório comparativo em PDF
        """
        if not REPORTLAB_AVAILABLE:
            return self._generate_pdf_via_html(comparison_data, output_path, title, 'comparison')
        try:
            doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            story = []
            story.append(Paragraph(title, self.custom_styles['Title']))
            story.append(Spacer(1, 12))
            script_a = comparison_data.get('script_a_name', 'Script A')
            script_b = comparison_data.get('script_b_name', 'Script B')
            story.append(Paragraph(f'<b>Comparando:</b> {script_a} vs {script_b}', self.styles['Normal']))
            story.append(Spacer(1, 20))
            similarity = comparison_data.get('overall_similarity', 0) * 100
            story.append(Paragraph('Similaridade Geral', self.custom_styles['Heading1']))
            story.append(Paragraph(f'{similarity:.1f}%', self.custom_styles['Score']))
            story.append(Spacer(1, 20))
            if 'dimensions' in comparison_data:
                story.append(Paragraph('Comparação por Dimensão', self.custom_styles['Heading1']))
                story.append(self._create_dimensions_comparison_table(comparison_data['dimensions']))
                story.append(Spacer(1, 20))
            if 'key_similarities' in comparison_data:
                story.append(Paragraph('Principais Semelhanças', self.custom_styles['Heading1']))
                for sim in comparison_data['key_similarities']:
                    story.append(Paragraph(f'• {sim}', self.styles['Normal']))
                story.append(Spacer(1, 20))
            if 'key_differences' in comparison_data:
                story.append(Paragraph('Principais Diferenças', self.custom_styles['Heading1']))
                for diff in comparison_data['key_differences']:
                    story.append(Paragraph(f'• {diff}', self.styles['Normal']))
                story.append(Spacer(1, 20))
            if 'recommendation' in comparison_data:
                story.append(Paragraph('Recomendação', self.custom_styles['Heading1']))
                story.append(Paragraph(comparison_data['recommendation'], self.custom_styles['BodyText']))
            doc.build(story)
            logger.info(f'Relatório PDF comparativo gerado: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Erro gerando PDF comparativo: {e}')
            return False

    def _create_strengths_weaknesses_section(self, data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de pontos fortes e fracos"""
        elements = []
        elements.append(Paragraph('Pontos Fortes e Fracos', self.custom_styles['Heading1']))
        table_data = [['Pontos Fortes', 'Pontos a Melhorar']]
        strengths = data.get('strengths', [])
        weaknesses = data.get('weaknesses', [])
        max_items = max(len(strengths), len(weaknesses))
        for i in range(max_items):
            strength = strengths[i] if i < len(strengths) else ''
            weakness = weaknesses[i] if i < len(weaknesses) else ''
            table_data.append([strength, weakness])
        table = Table(table_data, colWidths=[3.5 * inch, 3.5 * inch])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 12), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), colors.beige), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)
        return elements

    def _create_commercial_section(self, commercial_data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de predição comercial"""
        elements = []
        elements.append(Paragraph('Predição Comercial', self.custom_styles['Heading1']))
        score = commercial_data.get('overall_score', 0) * 100
        confidence = commercial_data.get('confidence', 0) * 100
        elements.append(Paragraph(f'<b>Potencial Comercial:</b> {score:.1f}%', self.styles['Normal']))
        elements.append(Paragraph(f'<b>Confiança:</b> {confidence:.1f}%', self.styles['Normal']))
        elements.append(Paragraph(f"<b>Nível de Risco:</b> {commercial_data.get('risk_level', 'N/A')}", self.styles['Normal']))
        elements.append(Paragraph(f"<b>Categoria de Mercado:</b> {commercial_data.get('market_category', 'N/A')}", self.styles['Normal']))
        if 'target_audience' in commercial_data:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph('<b>Público-Alvo:</b>', self.styles['Normal']))
            for audience in commercial_data['target_audience']:
                elements.append(Paragraph(f'• {audience}', self.styles['Normal']))
        return elements

    def _create_recommendations_section(self, recommendations: Any) -> List[Flowable]:
        """Cria seção de recomendações"""
        elements = []
        elements.append(Paragraph('Recomendações', self.custom_styles['Heading1']))
        if isinstance(recommendations, dict):
            if 'quick_wins' in recommendations:
                elements.append(Paragraph('Quick Wins', self.custom_styles['Heading2']))
                for rec in recommendations['quick_wins'][:3]:
                    elements.append(Paragraph(f"• {rec.get('title', rec)}", self.styles['Normal']))
                elements.append(Spacer(1, 10))
            if 'major_improvements' in recommendations:
                elements.append(Paragraph('Melhorias Principais', self.custom_styles['Heading2']))
                for rec in recommendations['major_improvements'][:3]:
                    elements.append(Paragraph(f"• {rec.get('title', rec)}", self.styles['Normal']))
        elif isinstance(recommendations, list):
            for rec in recommendations[:5]:
                if isinstance(rec, dict):
                    elements.append(Paragraph(f"• {rec.get('title', str(rec))}", self.styles['Normal']))
                else:
                    elements.append(Paragraph(f'• {rec}', self.styles['Normal']))
        return elements

    def _create_category_analysis_table(self, analysis: Dict[str, Any]) -> Table:
        """Cria tabela de análise por categoria"""
        table_data = [['Categoria', 'Status', 'Avaliação'], ['Estrutura', self._status_to_text(analysis.get('structure')), self._status_to_score(analysis.get('structure'))], ['Diálogos', self._status_to_text(analysis.get('dialogue')), self._status_to_score(analysis.get('dialogue'))], ['Ritmo', self._status_to_text(analysis.get('pacing')), self._status_to_score(analysis.get('pacing'))], ['Personagens', self._status_to_text(analysis.get('characters')), self._status_to_score(analysis.get('characters'))]]
        table = Table(table_data, colWidths=[2 * inch, 2 * inch, 1.5 * inch])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 12), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), colors.beige), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        return table

    def _create_structure_analysis_section(self, structure_data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de análise estrutural"""
        elements = []
        for key, value in structure_data.items():
            if isinstance(value, dict):
                elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b>", self.styles['Normal']))
                for sub_key, sub_value in value.items():
                    elements.append(Paragraph(f'  • {sub_key}: {sub_value}', self.styles['Normal']))
            else:
                elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", self.styles['Normal']))
        return elements

    def _create_character_analysis_section(self, character_data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de análise de personagens"""
        elements = []
        if isinstance(character_data, dict):
            for character, analysis in character_data.items():
                elements.append(Paragraph(f'<b>{character}:</b>', self.styles['Normal']))
                if isinstance(analysis, dict):
                    for key, value in analysis.items():
                        elements.append(Paragraph(f'  • {key}: {value}', self.styles['Normal']))
                else:
                    elements.append(Paragraph(f'  {analysis}', self.styles['Normal']))
                elements.append(Spacer(1, 5))
        return elements

    def _create_dialogue_analysis_section(self, dialogue_data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de análise de diálogos"""
        elements = []
        if isinstance(dialogue_data, dict):
            for key, value in dialogue_data.items():
                elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", self.styles['Normal']))
        return elements

    def _create_sentiment_analysis_section(self, sentiment_data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de análise de sentimentos"""
        elements = []
        if 'overall_sentiment' in sentiment_data:
            overall = sentiment_data['overall_sentiment']
            elements.append(Paragraph('<b>Sentimento Geral:</b>', self.styles['Normal']))
            elements.append(Paragraph(f"  • Positivo: {overall.get('positive', 0) * 100:.1f}%", self.styles['Normal']))
            elements.append(Paragraph(f"  • Negativo: {overall.get('negative', 0) * 100:.1f}%", self.styles['Normal']))
            elements.append(Paragraph(f"  • Neutro: {overall.get('neutral', 0) * 100:.1f}%", self.styles['Normal']))
            elements.append(Paragraph(f"  • Score Composto: {overall.get('compound', 0):.2f}", self.styles['Normal']))
            elements.append(Spacer(1, 10))
        if 'emotions' in sentiment_data:
            elements.append(Paragraph('<b>Análise de Emoções:</b>', self.styles['Normal']))
            emotions = sentiment_data['emotions']
            for emotion, value in emotions.items():
                elements.append(Paragraph(f'  • {emotion.title()}: {value * 100:.1f}%', self.styles['Normal']))
        return elements

    def _create_technical_recommendations_section(self, recommendations: Any) -> List[Flowable]:
        """Cria seção de recomendações técnicas detalhadas"""
        elements = []
        elements.append(Paragraph('Recomendações Técnicas Detalhadas', self.custom_styles['Heading1']))
        if isinstance(recommendations, dict):
            for category, items in recommendations.items():
                elements.append(Paragraph(category.replace('_', ' ').title(), self.custom_styles['Heading2']))
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            elements.append(Paragraph(f"<b>{item.get('title', 'Recomendação')}:</b>", self.styles['Normal']))
                            elements.append(Paragraph(item.get('description', ''), self.styles['Normal']))
                            if 'rationale' in item:
                                elements.append(Paragraph(f"<i>Justificativa: {item['rationale']}</i>", self.styles['Normal']))
                            elements.append(Spacer(1, 5))
                        else:
                            elements.append(Paragraph(f'• {item}', self.styles['Normal']))
                elements.append(Spacer(1, 10))
        return elements

    def _create_dimensions_comparison_table(self, dimensions: List[Dict[str, Any]]) -> Table:
        """Cria tabela de comparação por dimensões"""
        table_data = [['Dimensão', 'Script A', 'Script B', 'Similaridade']]
        for dim in dimensions:
            table_data.append([dim.get('name', 'N/A'), f"{dim.get('script_a_score', 0) * 100:.1f}%", f"{dim.get('script_b_score', 0) * 100:.1f}%", f"{dim.get('similarity', 0) * 100:.1f}%"])
        table = Table(table_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17a2b8')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 12), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), colors.beige), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        return table

    def _status_to_text(self, status: str) -> str:
        """Converte status em texto legível"""
        status_map = {'excellent': 'Excelente', 'good': 'Bom', 'needs_improvement': 'Precisa Melhorar', 'poor': 'Ruim'}
        return status_map.get(status, 'N/A')

    def _status_to_score(self, status: str) -> str:
        """Converte status em score"""
        status_scores = {'excellent': '90-100', 'good': '70-89', 'needs_improvement': '50-69', 'poor': '0-49'}
        return status_scores.get(status, 'N/A')

    def _generate_pdf_via_html(self, data: Dict[str, Any], output_path: Path, title: str, report_type: str) -> bool:
        """
        Gera PDF via HTML quando ReportLab não está disponível
        """
        try:
            html_path = output_path.with_suffix('.html')
            if report_type == 'executive':
                success = self.html_generator.generate_executive_report(data, html_path, title)
            elif report_type == 'technical':
                success = self.html_generator.generate_technical_report(data, html_path, title)
            elif report_type == 'comparison':
                success = self.html_generator.generate_comparison_report(data, html_path, title)
            else:
                success = self.html_generator.generate_complete_report(data, html_path, title)
            if success:
                logger.info(f'PDF não disponível, HTML gerado: {html_path}')
                return True
            return False
        except Exception as e:
            logger.error(f'Erro gerando PDF via HTML: {e}')
            return False
_pdf_generator = None

def get_pdf_generator() -> PDFReportGenerator:
    """Retorna instância singleton do gerador PDF"""
    global _pdf_generator
    if _pdf_generator is None:
        _pdf_generator = PDFReportGenerator()
    return _pdf_generator