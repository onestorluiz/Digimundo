"""
Sentiment Visualizer - Visualizações de Análise Emocional
Fase 4.A - Gráficos Específicos para Análise de Sentimentos
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional, Tuple
import logging
from .charts import ChartGenerator
logger = logging.getLogger(__name__)

class SentimentVisualizer:
    """
    Visualizador especializado em análise de sentimentos
    """

    def __init__(self):
        self.chart_generator = ChartGenerator()
        self.sentiment_colors = {'positive': '#28a745', 'negative': '#dc3545', 'neutral': '#6c757d', 'joy': '#ffc107', 'fear': '#6f42c1', 'anger': '#dc3545', 'sadness': '#17a2b8', 'surprise': '#fd7e14', 'love': '#e83e8c'}

    def create_sentiment_distribution(self, sentiment_data: Dict[str, float], title: str='Distribuição de Sentimentos') -> str:
        """
        Cria gráfico de distribuição de sentimentos
        """
        try:
            data = {'Positivo': sentiment_data.get('positive', 0) * 100, 'Negativo': sentiment_data.get('negative', 0) * 100, 'Neutro': sentiment_data.get('neutral', 0) * 100}
            colors = [self.sentiment_colors['positive'], self.sentiment_colors['negative'], self.sentiment_colors['neutral']]
            fig = go.Figure(go.Pie(labels=list(data.keys()), values=list(data.values()), hole=0.4, marker_colors=colors, textinfo='label+percent', textposition='auto'))
            compound = sentiment_data.get('compound', 0)
            fig.add_annotation(text=f'<b>Score Geral</b><br>{compound:.2f}', x=0.5, y=0.5, font_size=16, showarrow=False)
            fig.update_layout(title=title, height=500, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando distribuição sentimentos: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_emotion_radar(self, emotions: Dict[str, float], title: str='Análise de Emoções') -> str:
        """
        Cria radar chart para emoções específicas
        """
        try:
            labels = []
            values = []
            emotion_labels = {'joy': 'Alegria', 'fear': 'Medo', 'anger': 'Raiva', 'sadness': 'Tristeza', 'surprise': 'Surpresa', 'love': 'Amor'}
            for emotion, value in emotions.items():
                if emotion in emotion_labels:
                    labels.append(emotion_labels[emotion])
                    values.append(value * 100)
            if not labels:
                return self.chart_generator._error_chart('Dados de emoções não disponíveis')
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', fillcolor='rgba(255, 193, 7, 0.3)', line_color='rgba(255, 193, 7, 1)', line_width=3, marker_size=8, name='Intensidade Emocional'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%')), title=title, height=500, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando radar emoções: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_character_sentiment_heatmap(self, character_sentiments: Dict[str, Dict[str, float]], title: str='Sentimentos por Personagem') -> str:
        """
        Cria heatmap de sentimentos por personagem
        """
        try:
            if not character_sentiments:
                return self.chart_generator._error_chart('Dados de personagens não disponíveis')
            characters = list(character_sentiments.keys())
            sentiment_types = ['positive', 'negative', 'neutral']
            sentiment_labels = ['Positivo', 'Negativo', 'Neutro']
            z = []
            for sentiment_type in sentiment_types:
                row = []
                for character in characters:
                    value = character_sentiments[character].get(sentiment_type, 0) * 100
                    row.append(value)
                z.append(row)
            fig = go.Figure(go.Heatmap(z=z, x=characters, y=sentiment_labels, colorscale='RdYlGn', showscale=True, colorbar_title='Intensidade (%)'))
            for i, sentiment_type in enumerate(sentiment_types):
                for j, character in enumerate(characters):
                    value = z[i][j]
                    fig.add_annotation(x=j, y=i, text=f'{value:.1f}%', showarrow=False, font_color='white' if value < 50 else 'black')
            fig.update_layout(title=title, height=300 + len(sentiment_types) * 50, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando heatmap personagens: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_sentiment_timeline(self, timeline_data: List[Tuple[str, Dict[str, float]]], title: str='Evolução Emocional') -> str:
        """
        Cria gráfico temporal da evolução dos sentimentos
        """
        try:
            if not timeline_data:
                return self.chart_generator._error_chart('Dados temporais não disponíveis')
            scenes = [item[0] for item in timeline_data]
            positive_values = [item[1].get('positive', 0) * 100 for item in timeline_data]
            negative_values = [item[1].get('negative', 0) * 100 for item in timeline_data]
            compound_values = [item[1].get('compound', 0) * 50 + 50 for item in timeline_data]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=scenes, y=positive_values, mode='lines+markers', name='Positivo', line=dict(color=self.sentiment_colors['positive'], width=2), marker=dict(size=6)))
            fig.add_trace(go.Scatter(x=scenes, y=negative_values, mode='lines+markers', name='Negativo', line=dict(color=self.sentiment_colors['negative'], width=2), marker=dict(size=6)))
            fig.add_trace(go.Scatter(x=scenes, y=compound_values, mode='lines+markers', name='Score Geral', line=dict(color='#007bff', width=3, dash='dot'), marker=dict(size=8)))
            fig.update_layout(title=title, xaxis_title='Cenas/Momentos', yaxis_title='Intensidade (%)', height=400, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando timeline sentimentos: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_dialogue_intensity_chart(self, dialogue_data: List[Tuple[str, str, float]], title: str='Intensidade dos Diálogos') -> str:
        """
        Cria gráfico de intensidade emocional dos diálogos
        """
        try:
            if not dialogue_data:
                return self.chart_generator._error_chart('Dados de diálogos não disponíveis')
            characters = [item[0] for item in dialogue_data]
            texts = [item[1][:50] + '...' if len(item[1]) > 50 else item[1] for item in dialogue_data]
            intensities = [item[2] * 100 for item in dialogue_data]
            colors = [self.chart_generator._get_score_color(intensity) for intensity in intensities]
            fig = go.Figure(go.Bar(x=characters, y=intensities, text=texts, textposition='outside', marker_color=colors, hovertemplate='<b>%{x}</b><br>Intensidade: %{y:.1f}%<br>Texto: %{text}<extra></extra>'))
            fig.update_layout(title=title, xaxis_title='Personagens', yaxis_title='Intensidade Emocional (%)', height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando intensidade diálogos: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')

    def create_sentiment_summary_dashboard(self, sentiment_analysis: Dict[str, Any], title: str='Dashboard de Sentimentos') -> str:
        """
        Cria dashboard completo de análise de sentimentos
        """
        try:
            fig = make_subplots(rows=2, cols=2, subplot_titles=('Distribuição Geral', 'Emoções Específicas', 'Intensidade por Cena', 'Resumo Estatístico'), specs=[[{'type': 'pie'}, {'type': 'polar'}], [{'type': 'scatter'}, {'type': 'bar'}]])
            sentiment_data = sentiment_analysis.get('overall_sentiment', {})
            fig.add_trace(go.Pie(labels=['Positivo', 'Negativo', 'Neutro'], values=[sentiment_data.get('positive', 0) * 100, sentiment_data.get('negative', 0) * 100, sentiment_data.get('neutral', 0) * 100], marker_colors=[self.sentiment_colors['positive'], self.sentiment_colors['negative'], self.sentiment_colors['neutral']]), row=1, col=1)
            emotions = sentiment_analysis.get('emotions', {})
            if emotions:
                fig.add_trace(go.Scatterpolar(r=[emotions.get(emotion, 0) * 100 for emotion in ['joy', 'fear', 'anger', 'sadness', 'surprise', 'love']], theta=['Alegria', 'Medo', 'Raiva', 'Tristeza', 'Surpresa', 'Amor'], fill='toself', name='Emoções'), row=1, col=2)
            timeline = sentiment_analysis.get('timeline', [])
            if timeline:
                scenes = [f'Cena {i + 1}' for i in range(len(timeline))]
                compounds = [item.get('compound', 0) * 50 + 50 for item in timeline]
                fig.add_trace(go.Scatter(x=scenes, y=compounds, mode='lines+markers', name='Evolução Emocional'), row=2, col=1)
            stats = sentiment_analysis.get('statistics', {})
            if stats:
                fig.add_trace(go.Bar(x=['Média', 'Mediana', 'Máximo', 'Mínimo'], y=[stats.get('mean', 0) * 100, stats.get('median', 0) * 100, stats.get('max', 0) * 100, stats.get('min', 0) * 100], name='Estatísticas'), row=2, col=2)
            fig.update_layout(title_text=title, height=800, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            return fig.to_json()
        except Exception as e:
            logger.error(f'Erro criando dashboard sentimentos: {e}')
            return self.chart_generator._error_chart(f'Erro: {str(e)}')
_sentiment_visualizer = None

def get_sentiment_visualizer() -> SentimentVisualizer:
    """Retorna instância singleton do visualizador de sentimentos"""
    global _sentiment_visualizer
    if _sentiment_visualizer is None:
        _sentiment_visualizer = SentimentVisualizer()
    return _sentiment_visualizer