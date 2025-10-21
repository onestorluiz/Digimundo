"""
AI Sentiment Analysis - Análise de Sentimento com NLP
Fase 3.C - Sistema de AI Avançada
"""
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from collections import Counter, defaultdict
import math
logger = logging.getLogger(__name__)

@dataclass
class SentimentScore:
    """Score de sentimento para um texto"""
    positive: float
    negative: float
    neutral: float
    compound: float
    confidence: float

@dataclass
class EmotionAnalysis:
    """Análise de emoções específicas"""
    joy: float
    fear: float
    anger: float
    sadness: float
    surprise: float
    love: float
    dominant_emotion: str

@dataclass
class DialogueSentiment:
    """Sentimento de um diálogo específico"""
    character: str
    text: str
    sentiment: SentimentScore
    emotions: EmotionAnalysis
    intensity: float

class SentimentLexicon:
    """Léxico de sentimentos otimizado para roteiros"""

    def __init__(self):
        """Inicializa com léxicos básicos em português e inglês"""
        self.positive_words = {'amor': 0.8, 'alegria': 0.7, 'feliz': 0.6, 'bom': 0.5, 'ótimo': 0.8, 'excelente': 0.9, 'maravilhoso': 0.8, 'perfeito': 0.7, 'sucesso': 0.6, 'vitória': 0.7, 'esperança': 0.6, 'sorrir': 0.5, 'conquistar': 0.6, 'realizar': 0.5, 'sonho': 0.6, 'paixão': 0.7, 'carinho': 0.6, 'gratidão': 0.7, 'paz': 0.6, 'harmonia': 0.6, 'liberdade': 0.7, 'love': 0.8, 'happy': 0.7, 'joy': 0.8, 'great': 0.6, 'amazing': 0.8, 'wonderful': 0.8, 'perfect': 0.7, 'success': 0.6, 'victory': 0.7, 'hope': 0.6, 'smile': 0.5, 'achieve': 0.6, 'dream': 0.6, 'passion': 0.7, 'freedom': 0.7, 'peace': 0.6, 'harmony': 0.6, 'brilliant': 0.8}
        self.negative_words = {'ódio': -0.8, 'raiva': -0.7, 'triste': -0.6, 'ruim': -0.5, 'péssimo': -0.8, 'terrível': -0.8, 'horrível': -0.8, 'fracasso': -0.7, 'derrota': -0.7, 'desespero': -0.8, 'medo': -0.6, 'chorar': -0.6, 'sofrer': -0.7, 'dor': -0.6, 'angústia': -0.7, 'solidão': -0.6, 'traição': -0.8, 'mentira': -0.6, 'culpa': -0.6, 'vergonha': -0.6, 'morte': -0.9, 'hate': -0.8, 'anger': -0.7, 'sad': -0.6, 'bad': -0.5, 'terrible': -0.8, 'horrible': -0.8, 'awful': -0.8, 'failure': -0.7, 'defeat': -0.7, 'despair': -0.8, 'fear': -0.6, 'cry': -0.6, 'suffer': -0.7, 'pain': -0.6, 'lonely': -0.6, 'betray': -0.8, 'lie': -0.6, 'guilt': -0.6, 'shame': -0.6, 'death': -0.9, 'disaster': -0.8}
        self.intensifiers = {'muito': 1.5, 'bem': 1.3, 'super': 1.7, 'mega': 1.8, 'ultra': 1.9, 'extremamente': 2.0, 'totalmente': 1.6, 'completamente': 1.8, 'absolutamente': 1.9, 'definitivamente': 1.5, 'realmente': 1.3, 'very': 1.5, 'really': 1.4, 'extremely': 2.0, 'absolutely': 1.9, 'totally': 1.6, 'completely': 1.8, 'definitely': 1.5, 'truly': 1.4, 'incredibly': 1.8, 'amazingly': 1.7, 'utterly': 1.9}
        self.negations = {'não', 'nunca', 'jamais', 'nada', 'nenhum', 'ninguém', 'nem', 'not', 'never', 'no', 'none', 'nobody', 'nothing', 'neither'}
        self.emotion_words = {'joy': {'português': ['alegria', 'felicidade', 'júbilo', 'euforia', 'contentamento'], 'english': ['joy', 'happiness', 'delight', 'euphoria', 'bliss', 'elation']}, 'fear': {'português': ['medo', 'terror', 'pavor', 'pânico', 'receio', 'apreensão'], 'english': ['fear', 'terror', 'horror', 'panic', 'anxiety', 'dread']}, 'anger': {'português': ['raiva', 'ira', 'fúria', 'irritação', 'ódio', 'rancor'], 'english': ['anger', 'rage', 'fury', 'wrath', 'irritation', 'hatred']}, 'sadness': {'português': ['tristeza', 'melancolia', 'depressão', 'luto', 'pesar'], 'english': ['sadness', 'melancholy', 'depression', 'grief', 'sorrow']}, 'surprise': {'português': ['surpresa', 'espanto', 'admiração', 'choque', 'pasmo'], 'english': ['surprise', 'amazement', 'astonishment', 'shock', 'wonder']}, 'love': {'português': ['amor', 'paixão', 'carinho', 'afeto', 'ternura', 'adoração'], 'english': ['love', 'passion', 'affection', 'adoration', 'tenderness']}}

    def get_word_sentiment(self, word: str) -> float:
        """
        Retorna o score de sentimento de uma palavra
        
        Args:
            word: Palavra para analisar
            
        Returns:
            Score entre -1.0 e 1.0
        """
        word = word.lower().strip()
        if word in self.positive_words:
            return self.positive_words[word]
        elif word in self.negative_words:
            return self.negative_words[word]
        else:
            return 0.0

    def is_intensifier(self, word: str) -> float:
        """Verifica se palavra é intensificador e retorna multiplicador"""
        word = word.lower().strip()
        return self.intensifiers.get(word, 1.0)

    def is_negation(self, word: str) -> bool:
        """Verifica se palavra é negação"""
        word = word.lower().strip()
        return word in self.negations

class SentimentAnalyzer:
    """Analisador principal de sentimento"""

    def __init__(self):
        """Inicializa analisador"""
        self.lexicon = SentimentLexicon()

    def preprocess_text(self, text: str) -> List[str]:
        """
        Pré-processa texto para análise
        
        Args:
            text: Texto a processar
            
        Returns:
            Lista de palavras processadas
        """
        text = re.sub('[^\\w\\s]', ' ', text.lower())
        text = re.sub('\\s+', ' ', text.strip())
        words = text.split()
        return words

    def analyze_sentiment(self, text: str) -> SentimentScore:
        """
        Analisa sentimento de um texto
        
        Args:
            text: Texto para analisar
            
        Returns:
            Score de sentimento
        """
        if not text or not text.strip():
            return SentimentScore(0.0, 0.0, 1.0, 0.0, 0.0)
        words = self.preprocess_text(text)
        if not words:
            return SentimentScore(0.0, 0.0, 1.0, 0.0, 0.0)
        scores = []
        i = 0
        while i < len(words):
            word = words[i]
            base_score = self.lexicon.get_word_sentiment(word)
            if base_score != 0.0:
                intensifier = 1.0
                if i > 0:
                    prev_word = words[i - 1]
                    intensifier = self.lexicon.is_intensifier(prev_word)
                negated = False
                for j in range(max(0, i - 3), i):
                    if self.lexicon.is_negation(words[j]):
                        negated = True
                        break
                final_score = base_score * intensifier
                if negated:
                    final_score = -final_score
                scores.append(final_score)
            i += 1
        if not scores:
            return SentimentScore(0.0, 0.0, 1.0, 0.0, 0.5)
        compound = sum(scores) / len(scores)
        compound = max(-1.0, min(1.0, compound))
        positive_scores = [s for s in scores if s > 0]
        negative_scores = [s for s in scores if s < 0]
        positive = sum(positive_scores) / len(scores) if positive_scores else 0.0
        negative = abs(sum(negative_scores)) / len(scores) if negative_scores else 0.0
        neutral = 1.0 - (positive + negative)
        total = positive + negative + neutral
        if total > 0:
            positive /= total
            negative /= total
            neutral /= total
        confidence = len(scores) / len(words)
        confidence = min(1.0, confidence * 1.5)
        return SentimentScore(positive=round(positive, 3), negative=round(negative, 3), neutral=round(neutral, 3), compound=round(compound, 3), confidence=round(confidence, 3))

    def analyze_emotions(self, text: str) -> EmotionAnalysis:
        """
        Analisa emoções específicas no texto
        
        Args:
            text: Texto para analisar
            
        Returns:
            Análise de emoções
        """
        words = self.preprocess_text(text)
        emotion_scores = {emotion: 0.0 for emotion in self.lexicon.emotion_words.keys()}
        for word in words:
            for emotion, word_lists in self.lexicon.emotion_words.items():
                for lang_words in word_lists.values():
                    if word in [w.lower() for w in lang_words]:
                        emotion_scores[emotion] += 1.0
                        break
        total_words = len(words)
        if total_words > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] = min(1.0, emotion_scores[emotion] / total_words * 10)
        dominant = max(emotion_scores.items(), key=lambda x: x[1])
        dominant_emotion = dominant[0] if dominant[1] > 0.1 else 'neutral'
        return EmotionAnalysis(joy=round(emotion_scores['joy'], 3), fear=round(emotion_scores['fear'], 3), anger=round(emotion_scores['anger'], 3), sadness=round(emotion_scores['sadness'], 3), surprise=round(emotion_scores['surprise'], 3), love=round(emotion_scores['love'], 3), dominant_emotion=dominant_emotion)

    def calculate_intensity(self, sentiment: SentimentScore, emotions: EmotionAnalysis) -> float:
        """
        Calcula intensidade emocional geral
        
        Args:
            sentiment: Score de sentimento
            emotions: Análise de emoções
            
        Returns:
            Intensidade entre 0.0 e 1.0
        """
        sentiment_intensity = abs(sentiment.compound)
        emotion_values = [emotions.joy, emotions.fear, emotions.anger, emotions.sadness, emotions.surprise, emotions.love]
        emotion_intensity = max(emotion_values)
        combined = sentiment_intensity * 0.6 + emotion_intensity * 0.4
        return round(combined, 3)

class ScriptSentimentAnalyzer:
    """Analisador de sentimento específico para roteiros"""

    def __init__(self):
        """Inicializa analisador"""
        self.analyzer = SentimentAnalyzer()

    def extract_dialogues(self, script_content: str) -> List[Dict[str, str]]:
        """
        Extrai diálogos do roteiro
        
        Args:
            script_content: Conteúdo do roteiro
            
        Returns:
            Lista de diálogos com personagem e texto
        """
        lines = script_content.split('\n')
        dialogues = []
        current_character = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.isupper() and len(line.split()) <= 3 and (not line.startswith(('INT.', 'EXT.'))):
                character = re.sub('\\s*\\([^)]*\\)', '', line).strip()
                if len(character) > 0 and len(character) < 50:
                    current_character = character
            elif current_character and (not line.startswith(('INT.', 'EXT.'))) and (not line.isupper()):
                dialogue_text = re.sub('\\([^)]*\\)', '', line).strip()
                if len(dialogue_text) > 10:
                    dialogues.append({'character': current_character, 'text': dialogue_text})
        return dialogues

    def analyze_script_sentiment(self, script_content: str) -> Dict[str, Any]:
        """
        Analisa sentimento completo de um roteiro
        
        Args:
            script_content: Conteúdo do roteiro
            
        Returns:
            Análise completa de sentimento
        """
        dialogues = self.extract_dialogues(script_content)
        if not dialogues:
            return {'status': 'error', 'message': 'Nenhum diálogo encontrado no roteiro', 'dialogue_count': 0}
        dialogue_sentiments = []
        for dialogue in dialogues:
            sentiment = self.analyzer.analyze_sentiment(dialogue['text'])
            emotions = self.analyzer.analyze_emotions(dialogue['text'])
            intensity = self.analyzer.calculate_intensity(sentiment, emotions)
            dialogue_sentiment = DialogueSentiment(character=dialogue['character'], text=dialogue['text'][:100] + '...' if len(dialogue['text']) > 100 else dialogue['text'], sentiment=sentiment, emotions=emotions, intensity=intensity)
            dialogue_sentiments.append(dialogue_sentiment)
        character_stats = defaultdict(list)
        for ds in dialogue_sentiments:
            character_stats[ds.character].append(ds)
        character_analysis = {}
        for character, dialogues in character_stats.items():
            avg_compound = sum((d.sentiment.compound for d in dialogues)) / len(dialogues)
            avg_intensity = sum((d.intensity for d in dialogues)) / len(dialogues)
            emotion_counts = Counter()
            for d in dialogues:
                emotion_counts[d.emotions.dominant_emotion] += 1
            character_analysis[character] = {'dialogue_count': len(dialogues), 'avg_sentiment': round(avg_compound, 3), 'avg_intensity': round(avg_intensity, 3), 'dominant_emotion': emotion_counts.most_common(1)[0][0] if emotion_counts else 'neutral', 'sentiment_range': {'min': round(min((d.sentiment.compound for d in dialogues)), 3), 'max': round(max((d.sentiment.compound for d in dialogues)), 3)}}
        all_compounds = [d.sentiment.compound for d in dialogue_sentiments]
        all_intensities = [d.intensity for d in dialogue_sentiments]
        overall_sentiment = sum(all_compounds) / len(all_compounds)
        overall_intensity = sum(all_intensities) / len(all_intensities)
        if overall_sentiment > 0.3:
            tone = 'positive'
        elif overall_sentiment < -0.3:
            tone = 'negative'
        else:
            tone = 'neutral'
        chunk_size = max(1, len(dialogue_sentiments) // 10)
        emotional_arc = []
        for i in range(0, len(dialogue_sentiments), chunk_size):
            chunk = dialogue_sentiments[i:i + chunk_size]
            chunk_sentiment = sum((d.sentiment.compound for d in chunk)) / len(chunk)
            emotional_arc.append(round(chunk_sentiment, 3))
        return {'status': 'success', 'dialogue_count': len(dialogues), 'character_count': len(character_stats), 'overall_analysis': {'sentiment': round(overall_sentiment, 3), 'intensity': round(overall_intensity, 3), 'tone': tone, 'emotional_range': {'min': round(min(all_compounds), 3), 'max': round(max(all_compounds), 3), 'variance': round(sum(((x - overall_sentiment) ** 2 for x in all_compounds)) / len(all_compounds), 3)}}, 'character_analysis': character_analysis, 'emotional_arc': emotional_arc, 'sample_dialogues': [asdict(d) for d in dialogue_sentiments[:5]], 'insights': self._generate_insights(character_analysis, overall_sentiment, overall_intensity, tone)}

    def _generate_insights(self, character_analysis: Dict, overall_sentiment: float, overall_intensity: float, tone: str) -> List[str]:
        """Gera insights automáticos da análise"""
        insights = []
        if tone == 'positive':
            insights.append(f'Roteiro tem tom predominantemente positivo (score: {overall_sentiment:.2f})')
        elif tone == 'negative':
            insights.append(f'Roteiro tem tom predominantemente negativo (score: {overall_sentiment:.2f})')
        else:
            insights.append(f'Roteiro mantém tom equilibrado/neutro (score: {overall_sentiment:.2f})')
        if overall_intensity > 0.7:
            insights.append('Alto nível de intensidade emocional - roteiro dramaticamente envolvente')
        elif overall_intensity < 0.3:
            insights.append('Baixa intensidade emocional - roteiro pode se beneficiar de mais drama')
        if len(character_analysis) > 0:
            most_positive = max(character_analysis.items(), key=lambda x: x[1]['avg_sentiment'])
            most_negative = min(character_analysis.items(), key=lambda x: x[1]['avg_sentiment'])
            if most_positive[1]['avg_sentiment'] > 0.3:
                insights.append(f'{most_positive[0]} é o personagem mais positivo/otimista')
            if most_negative[1]['avg_sentiment'] < -0.3:
                insights.append(f'{most_negative[0]} é o personagem mais negativo/conflituoso')
            most_talkative = max(character_analysis.items(), key=lambda x: x[1]['dialogue_count'])
            if most_talkative[1]['dialogue_count'] > len(character_analysis) * 2:
                insights.append(f"{most_talkative[0]} domina as falas ({most_talkative[1]['dialogue_count']} diálogos)")
        return insights
_sentiment_analyzer: Optional[ScriptSentimentAnalyzer] = None

def get_sentiment_analyzer() -> ScriptSentimentAnalyzer:
    """
    Retorna instância singleton do analisador
    
    Returns:
        ScriptSentimentAnalyzer configurado
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = ScriptSentimentAnalyzer()
    return _sentiment_analyzer

def analyze_script_sentiment(script_content: str) -> Dict[str, Any]:
    """Atalho para analisar sentimento de roteiro"""
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze_script_sentiment(script_content)

def analyze_text_sentiment(text: str) -> SentimentScore:
    """Atalho para analisar sentimento de texto"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_sentiment(text)
__all__ = ['SentimentScore', 'EmotionAnalysis', 'DialogueSentiment', 'ScriptSentimentAnalyzer', 'SentimentAnalyzer', 'get_sentiment_analyzer', 'analyze_script_sentiment', 'analyze_text_sentiment']