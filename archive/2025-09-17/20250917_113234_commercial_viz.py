"""
Commercial Visualizer - Visualizações de Predição Comercial
Fase 4.A - Gráficos Específicos para Análise de Mercado
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional, Tuple
import logging
from .charts import ChartGenerator
logger = logging.getLogger(__name__)

class CommercialVisualizer:
    """
    Visualizador especializado em predição comercial
    """

    def __init__(self):
        self.chart_generator = ChartGenerator()
        self.commercial_colors = {'high_potential': '#28a745', 'medium_potential': '#ffc107', 'low_potential': '#dc3545', 'market_factors': '#17a2b8', 'risk_low': '#28a745', 'risk_medium': '#ffc107', 'risk_high': '#dc3545'}
        self.market_categories = {'mainstream': 'Mainstream', 'niche': 'Nicho', 'art_house': 'Arte/Autor', 'commercial': 'Comercial', 'independent': 'Independente'}

    def create_commercial_score_gauge(self, commercial_score: float, confidence: float, title: str='Potencial Comercial') -> str:
        """
        Cria gauge de potencial comercial
        """
        try:
            score_percent = commercial_score * 100
            fig = go.Figure(go.Indicator(mode='gauge+number+delta', value=score_percent, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': title}, delta={'reference': 60}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': self._get_commercial_color(score_percent)}, 'steps': [{'range': [0, 30], 'color': '#ffdddd'}, {'range': [30, 60], 'color': '#ffffdd'}, {'range': [60, 80], 'color': '#ddffdd'}, {'range': [80, 100], 'color': '#ddffdd'}], 'threshold': {'line': {'color': 'gold', 'width': 4}, 'thickness': 0.75, 'value': 85}}))
            fig.add_annotation(text=f'Confiança: {confidence * 100:.1f}%', x=0.5, y=0.15, xref='paper', yref='paper', showarrow=False, font=dict(size=12))
            fig.update_layout(height=400, font={'size': 14}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando gauge comercial: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_market_factors_radar(self, market_factors: List[Dict[str, Any]], title: str='Fatores de Mercado') -> str:
        """
        Cria radar chart para fatores de mercado
        """
        try:
            if not market_factors:
                return self.chart_generator._error_chart('Fatores de mercado não disponíveis')
            factor_names = []
            factor_weights = []
            factor_scores = []
            for factor in market_factors:
                name = factor.get('name', 'N/A')
                weight = factor.get('weight', 0)
                score = factor.get('score', 0)
                factor_names.append(name)
                factor_weights.append(weight * 100)
                factor_scores.append(score * 100)
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=factor_weights, theta=factor_names, fill='toself', fillcolor='rgba(23, 162, 184, 0.2)', line=dict(color=self.commercial_colors['market_factors'], width=2), name='Peso no Mercado'))
            fig.add_trace(go.Scatterpolar(r=factor_scores, theta=factor_names, fill='toself', fillcolor='rgba(40, 167, 69, 0.2)', line=dict(color=self.commercial_colors['high_potential'], width=2), name='Performance'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%')), title=title, height=600, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando radar fatores: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_risk_assessment_chart(self, risk_level: str, risk_factors: Dict[str, float], title: str='Análise de Risco') -> str:
        """
        Cria gráfico de avaliação de risco
        """
        try:
            if not risk_factors:
                return self.chart_generator._error_chart('Fatores de risco não disponíveis')
            factors = list(risk_factors.keys())
            values = [risk_factors[factor] * 100 for factor in factors]
            risk_color = self.commercial_colors.get(f'risk_{risk_level.lower()}', '#6c757d')
            colors = [risk_color] * len(values)
            fig = go.Figure(go.Bar(x=factors, y=values, marker_color=colors, text=[f'{v:.1f}%' for v in values], textposition='outside'))
            fig.add_hline(y=50, line_dash='dash', line_color='gray', annotation_text='Limite de Risco')
            fig.update_layout(title=f'{title} - Nível: {risk_level.upper()}', xaxis_title='Fatores de Risco', yaxis_title='Impacto (%)', height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando avaliação risco: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_target_audience_pie(self, target_audience: List[str], audience_weights: Optional[Dict[str, float]]=None, title: str='Público-Alvo') -> str:
        """
        Cria gráfico de pizza para público-alvo
        """
        try:
            if not target_audience:
                return self.chart_generator._error_chart('Dados de público-alvo não disponíveis')
            if audience_weights is None:
                weights = [1] * len(target_audience)
            else:
                weights = [audience_weights.get(audience, 1) for audience in target_audience]
            fig = go.Figure(go.Pie(labels=target_audience, values=weights, hole=0.3, textinfo='label+percent', textposition='auto', marker_colors=self.chart_generator.default_colors[:len(target_audience)]))
            fig.update_layout(title=title, height=500, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando pizza público: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_genre_multiplier_chart(self, genre_data: Dict[str, float], base_score: float, title: str='Multiplicadores por Gênero') -> str:
        """
        Cria gráfico mostrando impacto dos multiplicadores de gênero
        """
        try:
            if not genre_data:
                return self.chart_generator._error_chart('Dados de gênero não disponíveis')
            genres = list(genre_data.keys())
            multipliers = list(genre_data.values())
            adjusted_scores = [base_score * mult for mult in multipliers]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Score Base', x=genres, y=[base_score] * len(genres), marker_color='lightgray', opacity=0.6))
            colors = [self._get_commercial_color(score * 100) for score in adjusted_scores]
            fig.add_trace(go.Bar(name='Score Ajustado', x=genres, y=adjusted_scores, marker_color=colors, text=[f'{score:.2f}' for score in adjusted_scores], textposition='outside'))
            fig.update_layout(title=title, xaxis_title='Gêneros', yaxis_title='Score Comercial', barmode='overlay', height=400, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando multiplicadores gênero: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_roi_projection_chart(self, budget_ranges: List[str], roi_projections: List[float], confidence_intervals: Optional[List[Tuple[float, float]]]=None, title: str='Projeção de ROI') -> str:
        """
        Cria gráfico de projeção de ROI por faixa orçamentária
        """
        try:
            if not budget_ranges or not roi_projections:
                return self.chart_generator._error_chart('Dados de ROI não disponíveis')
            fig = go.Figure()
            fig.add_trace(go.Bar(name='ROI Projetado', x=budget_ranges, y=roi_projections, marker_color=[self._get_roi_color(roi) for roi in roi_projections], text=[f'{roi:.1f}x' for roi in roi_projections], textposition='outside'))
            if confidence_intervals:
                error_y = dict(type='data', array=[ci[1] - roi for roi, ci in zip(roi_projections, confidence_intervals)], arrayminus=[roi - ci[0] for roi, ci in zip(roi_projections, confidence_intervals)], visible=True)
                fig.data[0].error_y = error_y
            fig.add_hline(y=1.0, line_dash='dash', line_color='red', annotation_text='Break-even')
            fig.update_layout(title=title, xaxis_title='Faixas Orçamentárias', yaxis_title='ROI (Retorno sobre Investimento)', height=400, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando projeção ROI: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_commercial_dashboard(self, commercial_prediction: Dict[str, Any], title: str='Dashboard Comercial') -> str:
        """
        Cria dashboard completo de predição comercial
        """
        try:
            fig = make_subplots(rows=2, cols=2, subplot_titles=('Score Comercial Geral', 'Fatores de Mercado', 'Análise de Risco', 'Público-Alvo'), specs=[[{'type': 'indicator'}, {'type': 'bar'}], [{'type': 'bar'}, {'type': 'pie'}]])
            overall_score = commercial_prediction.get('overall_score', 0) * 100
            fig.add_trace(go.Indicator(mode='gauge+number', value=overall_score, title={'text': 'Potencial %'}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': self._get_commercial_color(overall_score)}, 'steps': [{'range': [0, 30], 'color': '#ffdddd'}, {'range': [30, 60], 'color': '#ffffdd'}, {'range': [60, 100], 'color': '#ddffdd'}]}), row=1, col=1)
            market_factors = commercial_prediction.get('market_factors', [])[:5]
            if market_factors:
                factor_names = [f['name'][:15] + '...' if len(f['name']) > 15 else f['name'] for f in market_factors]
                factor_scores = [f.get('score', 0) * 100 for f in market_factors]
                fig.add_trace(go.Bar(x=factor_names, y=factor_scores, name='Fatores', marker_color=self.commercial_colors['market_factors']), row=1, col=2)
            risk_factors = commercial_prediction.get('risk_factors', {})
            if risk_factors:
                risk_names = list(risk_factors.keys())[:5]
                risk_values = [risk_factors[name] * 100 for name in risk_names]
                fig.add_trace(go.Bar(x=risk_names, y=risk_values, name='Riscos', marker_color=self.commercial_colors['medium_potential']), row=2, col=1)
            target_audience = commercial_prediction.get('target_audience', [])
            if target_audience:
                fig.add_trace(go.Pie(labels=target_audience, values=[1] * len(target_audience), name='Público'), row=2, col=2)
            fig.update_layout(title_text=title, height=800, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando dashboard comercial: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def _get_commercial_color(self, score_percent: float) -> str:
        """Retorna cor baseada no score comercial"""
        if score_percent >= 75:
            return self.commercial_colors['high_potential']
        elif score_percent >= 50:
            return self.commercial_colors['medium_potential']
        else:
            return self.commercial_colors['low_potential']

    def _get_roi_color(self, roi: float) -> str:
        """Retorna cor baseada no ROI"""
        if roi >= 3.0:
            return self.commercial_colors['high_potential']
        elif roi >= 1.5:
            return self.commercial_colors['medium_potential']
        else:
            return self.commercial_colors['low_potential']
_commercial_visualizer = None

def get_commercial_visualizer() -> CommercialVisualizer:
    """Retorna instância singleton do visualizador comercial"""
    global _commercial_visualizer
    if _commercial_visualizer is None:
        _commercial_visualizer = CommercialVisualizer()
    return _commercial_visualizer