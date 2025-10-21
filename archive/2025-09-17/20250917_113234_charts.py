"""
Chart Generator - Base para Visualizações
Fase 4.A - Sistema de Gráficos com Plotly
"""
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging
logger = logging.getLogger(__name__)

@dataclass
class ChartConfig:
    """Configuração base para gráficos"""
    title: str
    width: int = 800
    height: int = 600
    theme: str = 'plotly_white'
    show_legend: bool = True
    responsive: bool = True

class ChartGenerator:
    """
    Gerador base de gráficos usando Plotly
    """

    def __init__(self):
        self.default_colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1', '#e83e8c', '#fd7e14']

    def create_score_gauge(self, score: float, title: str='Score', max_value: float=100.0) -> str:
        """
        Cria gráfico gauge para scores
        """
        try:
            fig = go.Figure(go.Indicator(mode='gauge+number+delta', value=score, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': title}, delta={'reference': max_value * 0.7}, gauge={'axis': {'range': [None, max_value]}, 'bar': {'color': self._get_score_color(score, max_value)}, 'steps': [{'range': [0, max_value * 0.6], 'color': 'lightgray'}, {'range': [max_value * 0.6, max_value * 0.8], 'color': 'gray'}], 'threshold': {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': max_value * 0.9}}))
            fig.update_layout(height=400, font={'size': 14}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando gauge: {e}')
            return self._error_chart(f'Erro: {str(e)}')

    def create_category_radar(self, categories: Dict[str, float], title: str='Análise por Categoria') -> str:
        """
        Cria gráfico radar para categorias
        """
        try:
            labels = list(categories.keys())
            values = list(categories.values())
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', fillcolor='rgba(0, 123, 255, 0.2)', line_color='rgba(0, 123, 255, 1)', line_width=2, name=title))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title=title, height=500, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando radar: {e}')
            return self._error_chart(f'Erro: {str(e)}')

    def create_progress_bars(self, data: Dict[str, float], title: str='Métricas', horizontal: bool=True) -> str:
        """
        Cria gráfico de barras de progresso
        """
        try:
            labels = list(data.keys())
            values = list(data.values())
            colors = [self._get_score_color(v, 100) for v in values]
            if horizontal:
                fig = go.Figure(go.Bar(x=values, y=labels, orientation='h', marker_color=colors, text=[f'{v:.1f}' for v in values], textposition='inside'))
                fig.update_layout(xaxis_title='Score', height=300 + len(labels) * 30)
            else:
                fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors, text=[f'{v:.1f}' for v in values], textposition='outside'))
                fig.update_layout(yaxis_title='Score', height=400)
            fig.update_layout(title=title, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando barras: {e}')
            return self._error_chart(f'Erro: {str(e)}')

    def create_pie_chart(self, data: Dict[str, float], title: str='Distribuição', show_percentages: bool=True) -> str:
        """
        Cria gráfico de pizza
        """
        try:
            labels = list(data.keys())
            values = list(data.values())
            fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.3, textinfo='label+percent' if show_percentages else 'label', textposition='auto', marker_colors=self.default_colors[:len(labels)]))
            fig.update_layout(title=title, height=500, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando pizza: {e}')
            return self._error_chart(f'Erro: {str(e)}')

    def create_timeline_chart(self, data: List[Tuple[str, float, str]], title: str='Timeline', y_title: str='Valor') -> str:
        """
        Cria gráfico de linha temporal
        """
        try:
            timestamps = [item[0] for item in data]
            values = [item[1] for item in data]
            labels = [item[2] if len(item) > 2 else '' for item in data]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines+markers', line=dict(color=self.default_colors[0], width=2), marker=dict(size=8, color=self.default_colors[0]), text=labels, textposition='top center', name=title))
            fig.update_layout(title=title, xaxis_title='Tempo', yaxis_title=y_title, height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando timeline: {e}')
            return self._error_chart(f'Erro: {str(e)}')

    def create_heatmap(self, data: List[List[float]], x_labels: List[str], y_labels: List[str], title: str='Heatmap') -> str:
        """
        Cria heatmap
        """
        try:
            fig = go.Figure(go.Heatmap(z=data, x=x_labels, y=y_labels, colorscale='RdYlBu', reversescale=True, showscale=True))
            fig.update_layout(title=title, height=400 + len(y_labels) * 20, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando heatmap: {e}')
            return self._error_chart(f'Erro: {str(e)}')

    def _get_score_color(self, score: float, max_value: float=100.0) -> str:
        """Retorna cor baseada no score"""
        percentage = score / max_value * 100
        if percentage >= 80:
            return '#28a745'
        elif percentage >= 70:
            return '#17a2b8'
        elif percentage >= 60:
            return '#ffc107'
        else:
            return '#dc3545'

    def _error_chart(self, message: str) -> str:
        """Cria gráfico de erro"""
        fig = go.Figure()
        fig.add_annotation(text=message, xref='paper', yref='paper', x=0.5, y=0.5, xanchor='center', yanchor='middle', showarrow=False, font=dict(size=16, color='red'))
        fig.update_layout(title='Erro na Visualização', height=300, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False))
        return fig.to_json()
_chart_generator = None

def get_chart_generator() -> ChartGenerator:
    """Retorna instância singleton do gerador de gráficos"""
    global _chart_generator
    if _chart_generator is None:
        _chart_generator = ChartGenerator()
    return _chart_generator