"""
Comparison Visualizer - Visualizações de Comparação de Scripts
Fase 4.A - Gráficos Específicos para Comparação Multi-Dimensional
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional, Tuple
import logging
from .charts import ChartGenerator
logger = logging.getLogger(__name__)

class ComparisonVisualizer:
    """
    Visualizador especializado em comparação de roteiros
    """

    def __init__(self):
        self.chart_generator = ChartGenerator()
        self.comparison_colors = {'script_a': '#007bff', 'script_b': '#28a745', 'similarity': '#ffc107', 'difference': '#dc3545'}
        self.dimension_labels = {'structure': 'Estrutura', 'characters': 'Personagens', 'dialogue': 'Diálogos', 'pacing': 'Ritmo', 'sentiment': 'Sentimentos', 'style': 'Estilo', 'themes': 'Temas'}

    def create_similarity_radar(self, script_a_data: Dict[str, float], script_b_data: Dict[str, float], script_a_name: str='Script A', script_b_name: str='Script B', title: str='Comparação Multi-Dimensional') -> str:
        """
        Cria radar chart comparando dois scripts em múltiplas dimensões
        """
        try:
            dimensions = list(set(script_a_data.keys()) & set(script_b_data.keys()))
            if not dimensions:
                return self.chart_generator._error_chart('Dados de comparação não disponíveis')
            labels = [self.dimension_labels.get(dim, dim.title()) for dim in dimensions]
            values_a = [script_a_data.get(dim, 0) * 100 for dim in dimensions]
            values_b = [script_b_data.get(dim, 0) * 100 for dim in dimensions]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values_a, theta=labels, fill='toself', fillcolor='rgba(0, 123, 255, 0.2)', line=dict(color=self.comparison_colors['script_a'], width=3), name=script_a_name, marker=dict(size=8, symbol='circle')))
            fig.add_trace(go.Scatterpolar(r=values_b, theta=labels, fill='toself', fillcolor='rgba(40, 167, 69, 0.2)', line=dict(color=self.comparison_colors['script_b'], width=3), name=script_b_name, marker=dict(size=8, symbol='diamond')))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%')), title=title, height=600, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando radar comparação: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_similarity_heatmap(self, similarity_matrix: Dict[str, Dict[str, float]], title: str='Matriz de Similaridade') -> str:
        """
        Cria heatmap de similaridade entre dimensões
        """
        try:
            if not similarity_matrix:
                return self.chart_generator._error_chart('Matriz de similaridade não disponível')
            dimensions = list(similarity_matrix.keys())
            labels = [self.dimension_labels.get(dim, dim.title()) for dim in dimensions]
            z = []
            for dim1 in dimensions:
                row = []
                for dim2 in dimensions:
                    similarity = similarity_matrix.get(dim1, {}).get(dim2, 0) * 100
                    row.append(similarity)
                z.append(row)
            fig = go.Figure(go.Heatmap(z=z, x=labels, y=labels, colorscale='RdYlGn', showscale=True, colorbar=dict(title='Similaridade (%)')))
            for i in range(len(dimensions)):
                for j in range(len(dimensions)):
                    value = z[i][j]
                    fig.add_annotation(x=j, y=i, text=f'{value:.1f}%', showarrow=False, font=dict(color='white' if value < 50 else 'black', size=10))
            fig.update_layout(title=title, height=400 + len(dimensions) * 30, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando heatmap similaridade: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_side_by_side_bars(self, script_a_data: Dict[str, float], script_b_data: Dict[str, float], script_a_name: str='Script A', script_b_name: str='Script B', title: str='Comparação Lado a Lado') -> str:
        """
        Cria gráfico de barras lado a lado
        """
        try:
            dimensions = list(set(script_a_data.keys()) & set(script_b_data.keys()))
            if not dimensions:
                return self.chart_generator._error_chart('Dados de comparação não disponíveis')
            labels = [self.dimension_labels.get(dim, dim.title()) for dim in dimensions]
            values_a = [script_a_data.get(dim, 0) * 100 for dim in dimensions]
            values_b = [script_b_data.get(dim, 0) * 100 for dim in dimensions]
            fig = go.Figure()
            fig.add_trace(go.Bar(name=script_a_name, x=labels, y=values_a, marker_color=self.comparison_colors['script_a'], text=[f'{v:.1f}%' for v in values_a], textposition='outside'))
            fig.add_trace(go.Bar(name=script_b_name, x=labels, y=values_b, marker_color=self.comparison_colors['script_b'], text=[f'{v:.1f}%' for v in values_b], textposition='outside'))
            fig.update_layout(title=title, xaxis_title='Dimensões', yaxis_title='Score (%)', barmode='group', height=500, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando barras lado a lado: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_difference_waterfall(self, differences: Dict[str, float], title: str='Análise de Diferenças') -> str:
        """
        Cria gráfico waterfall mostrando diferenças entre scripts
        """
        try:
            if not differences:
                return self.chart_generator._error_chart('Dados de diferenças não disponíveis')
            dimensions = list(differences.keys())
            labels = [self.dimension_labels.get(dim, dim.title()) for dim in dimensions]
            values = [differences[dim] * 100 for dim in dimensions]
            colors = [self.comparison_colors['script_a'] if v >= 0 else self.comparison_colors['script_b'] for v in values]
            fig = go.Figure(go.Waterfall(name='Diferenças', orientation='v', measure=['relative'] * len(labels), x=labels, textposition='outside', text=[f'{v:+.1f}%' for v in values], y=values, connector={'line': {'color': 'rgb(63, 63, 63)'}}, decreasing={'marker': {'color': self.comparison_colors['script_b']}}, increasing={'marker': {'color': self.comparison_colors['script_a']}}))
            fig.update_layout(title=title, xaxis_title='Dimensões', yaxis_title='Diferença (%)', height=500, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando waterfall diferenças: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_similarity_gauge(self, overall_similarity: float, title: str='Similaridade Geral') -> str:
        """
        Cria gauge de similaridade geral
        """
        try:
            similarity_percent = overall_similarity * 100
            fig = go.Figure(go.Indicator(mode='gauge+number+delta', value=similarity_percent, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': title}, delta={'reference': 70}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': self._get_similarity_color(similarity_percent)}, 'steps': [{'range': [0, 30], 'color': '#ffcccc'}, {'range': [30, 70], 'color': '#ffffcc'}, {'range': [70, 100], 'color': '#ccffcc'}], 'threshold': {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': 90}}))
            interpretation = self._get_similarity_interpretation(similarity_percent)
            fig.add_annotation(text=interpretation, x=0.5, y=0.2, xref='paper', yref='paper', showarrow=False, font=dict(size=14))
            fig.update_layout(height=400, font={'size': 14}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando gauge similaridade: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_comparison_summary_dashboard(self, comparison_data: Dict[str, Any], script_a_name: str='Script A', script_b_name: str='Script B', title: str='Dashboard de Comparação') -> str:
        """
        Cria dashboard completo de comparação
        """
        try:
            fig = make_subplots(rows=2, cols=2, subplot_titles=('Similaridade Geral', 'Comparação por Dimensão', 'Matriz de Correlação', 'Principais Diferenças'), specs=[[{'type': 'indicator'}, {'type': 'bar'}], [{'type': 'scatter'}, {'type': 'bar'}]])
            overall_sim = comparison_data.get('overall_similarity', 0) * 100
            fig.add_trace(go.Indicator(mode='gauge+number', value=overall_sim, title={'text': 'Similaridade %'}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': self._get_similarity_color(overall_sim)}, 'steps': [{'range': [0, 30], 'color': '#ffcccc'}, {'range': [30, 70], 'color': '#ffffcc'}, {'range': [70, 100], 'color': '#ccffcc'}]}), row=1, col=1)
            dimensions_data = comparison_data.get('dimensions', [])
            if dimensions_data:
                dim_names = [d.get('name', '') for d in dimensions_data]
                similarities = [d.get('similarity', 0) * 100 for d in dimensions_data]
                fig.add_trace(go.Bar(x=dim_names, y=similarities, name='Similaridade por Dimensão', marker_color=self.comparison_colors['similarity']), row=1, col=2)
            if len(dimensions_data) > 1:
                x_values = [d.get('script_a_score', 0) * 100 for d in dimensions_data]
                y_values = [d.get('script_b_score', 0) * 100 for d in dimensions_data]
                fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers+text', text=[d.get('name', '') for d in dimensions_data], textposition='top center', marker=dict(size=10, color=self.comparison_colors['script_a']), name='Correlação Scores'), row=2, col=1)
            differences = comparison_data.get('key_differences', [])
            if differences:
                diff_labels = [d[:20] + '...' if len(d) > 20 else d for d in differences[:5]]
                diff_values = list(range(len(diff_labels), 0, -1))
                fig.add_trace(go.Bar(x=diff_values, y=diff_labels, orientation='h', name='Principais Diferenças', marker_color=self.comparison_colors['difference']), row=2, col=2)
            fig.update_layout(title_text=title, height=800, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando dashboard comparação: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def _get_similarity_color(self, similarity_percent: float) -> str:
        """Retorna cor baseada no percentual de similaridade"""
        if similarity_percent >= 80:
            return '#28a745'
        elif similarity_percent >= 60:
            return '#ffc107'
        elif similarity_percent >= 40:
            return '#fd7e14'
        else:
            return '#dc3545'

    def _get_similarity_interpretation(self, similarity_percent: float) -> str:
        """Retorna interpretação textual da similaridade"""
        if similarity_percent >= 80:
            return 'Muito Similar'
        elif similarity_percent >= 60:
            return 'Moderadamente Similar'
        elif similarity_percent >= 40:
            return 'Pouco Similar'
        else:
            return 'Muito Diferente'
_comparison_visualizer = None

def get_comparison_visualizer() -> ComparisonVisualizer:
    """Retorna instância singleton do visualizador de comparação"""
    global _comparison_visualizer
    if _comparison_visualizer is None:
        _comparison_visualizer = ComparisonVisualizer()
    return _comparison_visualizer