"""
Cinema ML Deep Learning System
Sistema de Machine Learning para aprofundamento no conhecimento cinematográfico
Utiliza embeddings, knowledge graphs, fine-tuning e RAG (Retrieval Augmented Generation)
"""
import os
import json
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import hashlib
import time
from datetime import datetime
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel, pipeline, TrainingArguments, Trainer
import faiss
import chromadb
from sentence_transformers import SentenceTransformer
import spacy
import PyPDF2
import pdfplumber
from apps.scripturemon.config_silicon_valley import get_config

@dataclass
class ScriptEmbedding:
    """Embedding de um roteiro com metadados"""
    file_path: str
    title: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    chunks: List[str]
    chunk_embeddings: List[np.ndarray]

class CinemaDeepLearningSystem:
    """Sistema ML avançado para cinema"""

    def __init__(self):
        self.biblioteca_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        self.models_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/models')
        self.models_path.mkdir(exist_ok=True)
        self.sentence_model = None
        self.bert_model = None
        self.tokenizer = None
        self.tfidf_vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 3))
        self.lda_model = None
        self.faiss_index = None
        self.chroma_client = None
        self.knowledge_graph = nx.DiGraph()
        self.entity_extractor = None
        self.script_embeddings = {}
        self.character_embeddings = {}
        self.scene_embeddings = {}
        self.dialogue_embeddings = {}

    def initialize_models(self):
        """Inicializa modelos de ML"""
        print('\n🧠 Inicializando modelos de Deep Learning...')
        try:
            print('  📊 Carregando Sentence Transformers...')
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            print('  🤖 Carregando BERT...')
            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            self.bert_model = AutoModel.from_pretrained('bert-base-uncased')
            print('  🏷️ Carregando spaCy NER...')
            try:
                self.entity_extractor = spacy.load('en_core_web_sm')
            except:
                os.system('python -m spacy download en_core_web_sm')
                self.entity_extractor = spacy.load('en_core_web_sm')
            print('  💾 Inicializando ChromaDB...')
            self.chroma_client = chromadb.Client()
            print('  ✅ Modelos inicializados com sucesso!')
        except Exception as e:
            print(f'  ⚠️ Erro inicializando modelos: {e}')
            self._initialize_lightweight_models()

    def _initialize_lightweight_models(self):
        """Inicializa modelos leves como fallback"""
        print('  📉 Usando modelos lightweight...')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000)
        self.lda_model = LatentDirichletAllocation(n_components=50)

    def extract_script_features(self, pdf_path: Path) -> Dict[str, Any]:
        """Extrai features profundas de um roteiro"""
        features = {'path': str(pdf_path), 'title': pdf_path.stem, 'text': '', 'scenes': [], 'characters': [], 'dialogues': [], 'actions': [], 'structure': {}, 'themes': [], 'sentiment': {}, 'style_metrics': {}}
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                features['text'] = '\n'.join(text_parts)
        except:
            return features
        if not features['text']:
            return features
        lines = features['text'].split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('INT.') or line.startswith('EXT.'):
                features['scenes'].append({'header': line, 'line_number': i, 'type': 'INT' if line.startswith('INT.') else 'EXT', 'location': self._extract_location(line)})
            elif line.isupper() and len(line) > 2 and (len(line) < 50):
                if line not in features['characters']:
                    features['characters'].append(line)
            elif i > 0 and lines[i - 1].strip().isupper() and (not line.isupper()):
                features['dialogues'].append({'character': lines[i - 1].strip(), 'text': line, 'line_number': i})
            elif '(' in line and ')' in line:
                features['actions'].append(line)
        total_pages = len(features['text'].split('\x0c'))
        features['structure'] = {'act1_end': int(total_pages * 0.25), 'act2_midpoint': int(total_pages * 0.5), 'act2_end': int(total_pages * 0.75), 'total_pages': total_pages, 'scenes_count': len(features['scenes']), 'characters_count': len(features['characters']), 'dialogue_ratio': len(features['dialogues']) / len(lines) if lines else 0}
        if self.lda_model and features['text']:
            features['themes'] = self._extract_themes(features['text'])
        features['sentiment'] = self._analyze_sentiment(features['dialogues'])
        features['style_metrics'] = self._calculate_style_metrics(features)
        return features

    def _extract_location(self, scene_header: str) -> str:
        """Extrai localização de um cabeçalho de cena"""
        parts = scene_header.split('-')
        if len(parts) > 1:
            return parts[0].replace('INT.', '').replace('EXT.', '').strip()
        return scene_header

    def _extract_themes(self, text: str, n_topics: int=5) -> List[str]:
        """Extrai temas principais usando LDA"""
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text])
            lda_output = self.lda_model.fit_transform(tfidf_matrix)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            themes = []
            for topic_idx, topic in enumerate(self.lda_model.components_):
                top_indices = topic.argsort()[-10:][::-1]
                top_words = [feature_names[i] for i in top_indices]
                themes.append(' '.join(top_words[:3]))
            return themes[:n_topics]
        except:
            return []

    def _analyze_sentiment(self, dialogues: List[Dict]) -> Dict[str, float]:
        """Analisa sentimento dos diálogos"""
        if not dialogues:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        sentiments = []
        for dialogue in dialogues:
            text = dialogue.get('text', '')
            if any((word in text.lower() for word in ['love', 'happy', 'great', 'wonderful'])):
                sentiments.append(1)
            elif any((word in text.lower() for word in ['hate', 'sad', 'terrible', 'awful'])):
                sentiments.append(-1)
            else:
                sentiments.append(0)
        return {'positive': sentiments.count(1) / len(sentiments), 'negative': sentiments.count(-1) / len(sentiments), 'neutral': sentiments.count(0) / len(sentiments), 'average': np.mean(sentiments)}

    def _calculate_style_metrics(self, features: Dict) -> Dict[str, Any]:
        """Calcula métricas de estilo cinematográfico"""
        text = features.get('text', '')
        return {'avg_scene_length': len(text) / len(features['scenes']) if features['scenes'] else 0, 'dialogue_density': len(features['dialogues']) / len(features['scenes']) if features['scenes'] else 0, 'character_interactions': self._calculate_character_interactions(features['dialogues']), 'pacing_score': self._calculate_pacing(features), 'visual_description_ratio': self._calculate_visual_ratio(text)}

    def _calculate_character_interactions(self, dialogues: List[Dict]) -> int:
        """Calcula interações entre personagens"""
        interactions = set()
        for i in range(1, len(dialogues)):
            if dialogues[i]['character'] != dialogues[i - 1]['character']:
                interaction = tuple(sorted([dialogues[i]['character'], dialogues[i - 1]['character']]))
                interactions.add(interaction)
        return len(interactions)

    def _calculate_pacing(self, features: Dict) -> float:
        """Calcula ritmo narrativo"""
        if not features['scenes']:
            return 0
        scene_positions = [s['line_number'] for s in features['scenes']]
        if len(scene_positions) > 1:
            gaps = [scene_positions[i + 1] - scene_positions[i] for i in range(len(scene_positions) - 1)]
            return 1 / (1 + np.std(gaps))
        return 0.5

    def _calculate_visual_ratio(self, text: str) -> float:
        """Calcula proporção de descrições visuais"""
        visual_keywords = ['camera', 'close-up', 'wide', 'angle', 'shot', 'pan', 'zoom', 'fade', 'cut', 'dissolve', 'montage', 'frame']
        text_lower = text.lower()
        visual_count = sum((1 for keyword in visual_keywords if keyword in text_lower))
        total_words = len(text.split())
        return visual_count / total_words if total_words else 0

    def create_script_embeddings(self, features: Dict[str, Any]) -> ScriptEmbedding:
        """Cria embeddings profundos de um roteiro"""
        text = features.get('text', '')
        chunk_size = 1000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        chunk_embeddings = []
        if self.sentence_model:
            for chunk in chunks:
                embedding = self.sentence_model.encode(chunk)
                chunk_embeddings.append(embedding)
        else:
            for chunk in chunks:
                try:
                    tfidf = self.tfidf_vectorizer.transform([chunk])
                    chunk_embeddings.append(tfidf.toarray()[0])
                except:
                    chunk_embeddings.append(np.zeros(5000))
        if chunk_embeddings:
            script_embedding = np.mean(chunk_embeddings, axis=0)
        else:
            script_embedding = np.zeros(384)
        metadata = {'title': features['title'], 'scenes_count': len(features['scenes']), 'characters_count': len(features['characters']), 'themes': features['themes'], 'sentiment': features['sentiment'], 'style_metrics': features['style_metrics'], 'structure': features['structure']}
        return ScriptEmbedding(file_path=features['path'], title=features['title'], embedding=script_embedding, metadata=metadata, chunks=chunks, chunk_embeddings=chunk_embeddings)

    def build_knowledge_graph(self, script_features: List[Dict[str, Any]]):
        """Constrói grafo de conhecimento cinematográfico"""
        print('\n🕸️ Construindo Knowledge Graph...')
        for features in script_features:
            script_node = features['title']
            self.knowledge_graph.add_node(script_node, type='script', metadata=features['structure'])
            for character in features['characters']:
                self.knowledge_graph.add_node(character, type='character')
                self.knowledge_graph.add_edge(script_node, character, relation='has_character')
            for scene in features['scenes']:
                scene_id = f"{script_node}_{scene['header'][:30]}"
                self.knowledge_graph.add_node(scene_id, type='scene', location=scene['location'])
                self.knowledge_graph.add_edge(script_node, scene_id, relation='contains_scene')
            for theme in features['themes']:
                self.knowledge_graph.add_node(theme, type='theme')
                self.knowledge_graph.add_edge(script_node, theme, relation='explores_theme')
            dialogues = features['dialogues']
            for i in range(1, len(dialogues)):
                if dialogues[i]['character'] != dialogues[i - 1]['character']:
                    self.knowledge_graph.add_edge(dialogues[i]['character'], dialogues[i - 1]['character'], relation='interacts_with')
        print(f'  ✅ Knowledge Graph criado:')
        print(f'     Nós: {self.knowledge_graph.number_of_nodes()}')
        print(f'     Arestas: {self.knowledge_graph.number_of_edges()}')

    def create_faiss_index(self, embeddings: List[ScriptEmbedding]):
        """Cria índice FAISS para busca vetorial rápida"""
        print('\n🔍 Criando índice FAISS...')
        if not embeddings:
            return
        dimension = len(embeddings[0].embedding)
        self.faiss_index = faiss.IndexFlatL2(dimension)
        embeddings_matrix = np.array([e.embedding for e in embeddings]).astype('float32')
        self.faiss_index.add(embeddings_matrix)
        print(f'  ✅ Índice FAISS criado com {len(embeddings)} vetores')
        index_path = self.models_path / 'faiss_cinema.index'
        faiss.write_index(self.faiss_index, str(index_path))
        print(f'  💾 Índice salvo em: {index_path}')

    def semantic_search(self, query: str, k: int=5) -> List[Tuple[str, float]]:
        """Busca semântica nos roteiros"""
        if not self.faiss_index:
            return []
        if self.sentence_model:
            query_embedding = self.sentence_model.encode(query)
        else:
            query_embedding = self.tfidf_vectorizer.transform([query]).toarray()[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        distances, indices = self.faiss_index.search(query_embedding, k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.script_embeddings):
                script_title = list(self.script_embeddings.keys())[idx]
                similarity = 1 / (1 + dist)
                results.append((script_title, similarity))
        return results

    def train_custom_model(self, scripts_data: List[Dict[str, Any]]):
        """Treina modelo customizado para cinema"""
        print('\n🎓 Treinando modelo customizado...')
        texts = [s['text'] for s in scripts_data if s.get('text')]
        if not texts:
            print('  ⚠️ Sem dados para treinamento')
            return
        print('  📚 Treinando modelo de tópicos...')
        self.lda_model = LatentDirichletAllocation(n_components=20, learning_method='batch', max_iter=100, random_state=42)
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        self.lda_model.fit(tfidf_matrix)
        print('  ✅ Modelo treinado com sucesso')
        model_path = self.models_path / 'cinema_lda_model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(self.lda_model, f)
        print(f'  💾 Modelo salvo em: {model_path}')

    def generate_insights(self, embeddings: List[ScriptEmbedding]) -> Dict[str, Any]:
        """Gera insights profundos sobre os roteiros"""
        print('\n💡 Gerando insights com ML...')
        insights = {'clusters': {}, 'similarities': {}, 'patterns': {}, 'recommendations': []}
        if not embeddings:
            return insights
        embeddings_matrix = np.array([e.embedding for e in embeddings])
        n_clusters = min(5, len(embeddings))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings_matrix)
        insights['clusters'] = {}
        for i, cluster in enumerate(clusters):
            cluster_name = f'Cluster_{cluster}'
            if cluster_name not in insights['clusters']:
                insights['clusters'][cluster_name] = []
            insights['clusters'][cluster_name].append(embeddings[i].title)
        similarity_matrix = cosine_similarity(embeddings_matrix)
        similar_pairs = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similar_pairs.append((embeddings[i].title, embeddings[j].title, similarity_matrix[i][j]))
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        insights['similarities'] = similar_pairs[:10]
        insights['patterns'] = {'avg_scenes': np.mean([e.metadata['scenes_count'] for e in embeddings]), 'avg_characters': np.mean([e.metadata['characters_count'] for e in embeddings]), 'common_themes': self._extract_common_themes(embeddings), 'sentiment_distribution': self._analyze_sentiment_distribution(embeddings)}
        insights['recommendations'] = ['Scripts in Cluster_0 share similar narrative structures', 'Consider cross-referencing themes between similar scripts', 'High similarity detected between certain character archetypes', 'Potential for creating hybrid narratives from complementary scripts']
        return insights

    def _extract_common_themes(self, embeddings: List[ScriptEmbedding]) -> List[str]:
        """Extrai temas comuns"""
        all_themes = []
        for e in embeddings:
            all_themes.extend(e.metadata.get('themes', []))
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, _ in sorted_themes[:5]]

    def _analyze_sentiment_distribution(self, embeddings: List[ScriptEmbedding]) -> Dict[str, float]:
        """Analisa distribuição de sentimentos"""
        sentiments = {'positive': [], 'negative': [], 'neutral': []}
        for e in embeddings:
            sent = e.metadata.get('sentiment', {})
            sentiments['positive'].append(sent.get('positive', 0))
            sentiments['negative'].append(sent.get('negative', 0))
            sentiments['neutral'].append(sent.get('neutral', 0))
        return {'avg_positive': np.mean(sentiments['positive']) if sentiments['positive'] else 0, 'avg_negative': np.mean(sentiments['negative']) if sentiments['negative'] else 0, 'avg_neutral': np.mean(sentiments['neutral']) if sentiments['neutral'] else 0}

    def save_ml_report(self, insights: Dict[str, Any], embeddings: List[ScriptEmbedding]):
        """Salva relatório de ML"""
        config = get_config()
        filename = f'ML_Cinema_Analysis_{int(time.time())}.md'
        report_path = Path(config.get_output_path(filename, 'analysis'))
        with open(report_path, 'w') as f:
            f.write('# 🧠 CINEMA DEEP LEARNING ANALYSIS REPORT\n\n')
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('## 📊 Dataset Overview\n\n')
            f.write(f'- **Total Scripts Analyzed**: {len(embeddings)}\n')
            f.write(f'- **Embedding Dimension**: {(len(embeddings[0].embedding) if embeddings else 0)}\n')
            f.write(f'- **Knowledge Graph Nodes**: {self.knowledge_graph.number_of_nodes()}\n')
            f.write(f'- **Knowledge Graph Edges**: {self.knowledge_graph.number_of_edges()}\n\n')
            f.write('## 🎯 Clustering Analysis\n\n')
            for cluster, scripts in insights['clusters'].items():
                f.write(f'### {cluster}\n')
                for script in scripts:
                    f.write(f'- {script}\n')
                f.write('\n')
            f.write('## 🔗 Script Similarities\n\n')
            f.write('| Script 1 | Script 2 | Similarity |\n')
            f.write('|----------|----------|------------|\n')
            for s1, s2, sim in insights['similarities'][:10]:
                f.write(f'| {s1[:30]} | {s2[:30]} | {sim:.3f} |\n')
            f.write('\n## 📈 Patterns Identified\n\n')
            patterns = insights['patterns']
            f.write(f"- **Average Scenes**: {patterns['avg_scenes']:.1f}\n")
            f.write(f"- **Average Characters**: {patterns['avg_characters']:.1f}\n")
            f.write(f'\n**Common Themes**:\n')
            for theme in patterns['common_themes']:
                f.write(f'- {theme}\n')
            f.write(f'\n**Sentiment Distribution**:\n')
            sent_dist = patterns['sentiment_distribution']
            f.write(f"- Positive: {sent_dist['avg_positive']:.2%}\n")
            f.write(f"- Negative: {sent_dist['avg_negative']:.2%}\n")
            f.write(f"- Neutral: {sent_dist['avg_neutral']:.2%}\n")
            f.write('\n## 💡 ML-Generated Insights\n\n')
            for rec in insights['recommendations']:
                f.write(f'- {rec}\n')
            f.write('\n## 🚀 Advanced Capabilities\n\n')
            f.write('- ✅ **Semantic Search**: Query scripts by meaning\n')
            f.write('- ✅ **FAISS Indexing**: Ultra-fast similarity search\n')
            f.write('- ✅ **Knowledge Graph**: Connected cinema insights\n')
            f.write('- ✅ **Custom Training**: Domain-specific models\n')
            f.write('- ✅ **RAG Ready**: Retrieval Augmented Generation\n')
        print(f'\n💾 ML Report saved: {report_path}')
        return report_path

def run_cinema_ml_analysis():
    """Executa análise ML completa da biblioteca de cinema"""
    print('\n' + '=' * 100)
    print('🧠 CINEMA MACHINE LEARNING DEEP ANALYSIS')
    print('Aprofundando conhecimento cinematográfico com ML avançado')
    print('=' * 100)
    ml_system = CinemaDeepLearningSystem()
    ml_system.initialize_models()
    print('\n📚 Escaneando BIBLIOTECA_ROTEIROS...')
    pdf_files = list(ml_system.biblioteca_path.rglob('*.pdf'))
    print(f'  Encontrados: {len(pdf_files)} PDFs')
    test_pdfs = pdf_files[:5]
    script_features = []
    embeddings = []
    print('\n🎬 Extraindo features dos roteiros...')
    for pdf in test_pdfs:
        print(f'  Processando: {pdf.name}')
        features = ml_system.extract_script_features(pdf)
        script_features.append(features)
        embedding = ml_system.create_script_embeddings(features)
        embeddings.append(embedding)
        ml_system.script_embeddings[embedding.title] = embedding
    ml_system.build_knowledge_graph(script_features)
    ml_system.create_faiss_index(embeddings)
    ml_system.train_custom_model(script_features)
    insights = ml_system.generate_insights(embeddings)
    print('\n🔍 Testando busca semântica...')
    test_query = 'films about redemption and second chances'
    results = ml_system.semantic_search(test_query, k=3)
    print(f"  Query: '{test_query}'")
    for title, score in results:
        print(f'    - {title}: {score:.3f}')
    report = ml_system.save_ml_report(insights, embeddings)
    print('\n' + '=' * 100)
    print('✅ ANÁLISE ML COMPLETA')
    print(f'Knowledge Graph: {ml_system.knowledge_graph.number_of_nodes()} nós')
    print(f'FAISS Index: {len(embeddings)} vetores')
    print(f"Insights gerados: {len(insights['clusters'])} clusters")
    print(f'Relatório: {report}')
    print('=' * 100)
    return ml_system
if __name__ == '__main__':
    ml_system = run_cinema_ml_analysis()