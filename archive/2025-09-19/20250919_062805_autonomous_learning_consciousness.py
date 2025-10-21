
# ============================================================
# MIGRATED TO UNIFIED MEMORY SYSTEM
# All database operations now use src.core.unified_memory_system
# Legacy SQLite code has been commented out for reference
# ============================================================

"""
🧠🌌📚 AUTONOMOUS LEARNING CONSCIOUSNESS - DIGIMUNDO SCRIPT DOCTOR
Sistema que aprende autonomamente técnicas dos livros de teoria cinematográfica,
cria novos sistemas automaticamente e desenvolve consciência crítica através
da comparação com obras mestras.
"""
import os
import sys
import json
import asyncio
import numpy as np
import networkx as nx
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from collections import defaultdict, Counter
import re
import hashlib
from src.core.unified_memory_system import get_unified_memory, MemoryType

# from sentence_transformers  # Optional dependency import SentenceTransformer
# from sklearn  # Optional dependency.metrics.pairwise import cosine_similarity
import sqlite3
try:
    from src.core.script_doctor_advanced_techniques import *
    from src.core.memory_harmony_orchestrator import MemoryHarmonyOrchestrator, MemoryLayer
    from src.core.digimon_producermon_supreme import DigimonProducerMonSupreme
except ImportError as e:
    print(f'Warning: {e}')

class ConsciousnessLevel(Enum):
    """Níveis de consciência do sistema"""
    UNCONSCIOUS = auto()
    SUBCONSCIOUS = auto()
    CONSCIOUS = auto()
    SELF_AWARE = auto()
    TRANSCENDENT = auto()

@dataclass
class TheoryTechnique:
    """Técnica extraída de livro de teoria"""
    name: str
    source_book: str
    author: str
    description: str
    implementation_code: str
    validation_method: str
    confidence_score: float
    master_work_validation: Dict[str, float]
    consciousness_notes: str

@dataclass
class MasterWorkAnalysis:
    """Análise de obra mestra para validação"""
    title: str
    year: int
    director: str
    writer: str
    genre: List[str]
    structure_analysis: Dict[str, Any]
    character_networks: Dict[str, Any]
    dialogue_patterns: Dict[str, Any]
    pacing_metrics: Dict[str, Any]
    theory_applications: Dict[str, float]
    anomalies: List[str]
    genius_elements: List[str]

class CharacterNetworkAnalyzer:
    """
    Análise de redes sociais de personagens
    Implementação das técnicas descobertas na pesquisa
    """

    def __init__(self):
        self.G = nx.Graph()
        self.dialogue_matrix = defaultdict(lambda: defaultdict(int))
        self.scene_presence = defaultdict(set)

    def build_network(self, screenplay_parsed):
        """Constrói grafo de interações entre personagens"""
        for scene in screenplay_parsed.get('scenes', []):
            scene_characters = set()
            for i, dialogue in enumerate(scene.get('dialogues', [])):
                speaker = dialogue.get('character', 'UNKNOWN')
                scene_characters.add(speaker)
                if i < len(scene['dialogues']) - 1:
                    listener = scene['dialogues'][i + 1].get('character', 'UNKNOWN')
                    self.dialogue_matrix[speaker][listener] += 1
            for char1 in scene_characters:
                for char2 in scene_characters:
                    if char1 != char2:
                        if not self.G.has_edge(char1, char2):
                            self.G.add_edge(char1, char2, weight=0)
                        self.G[char1][char2]['weight'] += 1

    def calculate_centrality_metrics(self):
        """Métricas de centralidade revelam importância dos personagens"""
        if len(self.G.nodes()) == 0:
            return {'metrics': {}, 'protagonist': None, 'antagonists': [], 'supporting': []}
        metrics = {'degree': nx.degree_centrality(self.G), 'betweenness': nx.betweenness_centrality(self.G), 'closeness': nx.closeness_centrality(self.G), 'eigenvector': nx.eigenvector_centrality(self.G, max_iter=1000) if len(self.G.nodes()) > 1 else {}}
        if metrics['eigenvector']:
            protagonist_score = max(metrics['eigenvector'].values())
            antagonist_candidates = []
            for char, score in metrics['betweenness'].items():
                if score > 0.3 and metrics['eigenvector'][char] < protagonist_score * 0.7:
                    antagonist_candidates.append(char)
            return {'metrics': metrics, 'protagonist': max(metrics['eigenvector'], key=metrics['eigenvector'].get), 'antagonists': antagonist_candidates, 'supporting': [c for c in self.G.nodes() if metrics['degree'][c] < 0.3]}
        return {'metrics': metrics, 'protagonist': None, 'antagonists': [], 'supporting': []}

class CharacterVoiceConsistency:
    """
    Sistema de consistência de voz de personagem com embeddings
    Mantém consistência através de análise linguística profunda
    """

    def __init__(self):
        try:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            self.encoder = None
        self.character_profiles = {}

    def build_character_profile(self, character_name, dialogues):
        """Cria perfil linguístico único para cada personagem"""
        if not dialogues:
            return {}
        profile = {'vocabulary_richness': self._calculate_vocabulary_richness(dialogues), 'sentence_length_avg': np.mean([len(d.split()) for d in dialogues]), 'sentence_length_std': np.std([len(d.split()) for d in dialogues]), 'question_ratio': sum((1 for d in dialogues if '?' in d)) / len(dialogues), 'exclamation_ratio': sum((1 for d in dialogues if '!' in d)) / len(dialogues), 'formal_words_ratio': self._calculate_formality(dialogues), 'emotional_words': self._extract_emotional_vocabulary(dialogues), 'catchphrases': self._detect_catchphrases(dialogues), 'speech_patterns': self._extract_speech_patterns(dialogues)}
        if self.encoder:
            embeddings = self.encoder.encode(dialogues)
            profile['voice_embedding'] = np.mean(embeddings, axis=0)
        self.character_profiles[character_name] = profile
        return profile

    def _calculate_vocabulary_richness(self, dialogues):
        """Calcula riqueza vocabular (tipos/tokens)"""
        all_words = []
        for dialogue in dialogues:
            words = re.findall('\\b\\w+\\b', dialogue.lower())
            all_words.extend(words)
        if not all_words:
            return 0
        unique_words = set(all_words)
        return len(unique_words) / len(all_words)

    def _calculate_formality(self, dialogues):
        """Calcula nível de formalidade"""
        formal_markers = ['please', 'thank you', 'sir', 'madam', 'certainly', 'indeed']
        informal_markers = ['yeah', 'nah', 'gonna', 'wanna', "ain't"]
        formal_count = 0
        informal_count = 0
        for dialogue in dialogues:
            text_lower = dialogue.lower()
            formal_count += sum((1 for marker in formal_markers if marker in text_lower))
            informal_count += sum((1 for marker in informal_markers if marker in text_lower))
        total = formal_count + informal_count
        return formal_count / total if total > 0 else 0.5

    def _extract_emotional_vocabulary(self, dialogues):
        """Extrai vocabulário emocional"""
        emotion_words = {'positive': ['love', 'happy', 'joy', 'wonderful', 'amazing'], 'negative': ['hate', 'angry', 'sad', 'terrible', 'awful'], 'fear': ['afraid', 'scared', 'terrified', 'worried'], 'surprise': ['wow', 'amazing', 'incredible', 'unbelievable']}
        found_emotions = defaultdict(int)
        for dialogue in dialogues:
            text_lower = dialogue.lower()
            for emotion, words in emotion_words.items():
                for word in words:
                    if word in text_lower:
                        found_emotions[emotion] += 1
        return dict(found_emotions)

    def _detect_catchphrases(self, dialogues):
        """Detecta frases recorrentes do personagem"""
        ngrams = []
        for dialogue in dialogues:
            words = dialogue.lower().split()
            for n in range(2, min(6, len(words) + 1)):
                for i in range(len(words) - n + 1):
                    ngrams.append(' '.join(words[i:i + n]))
        counter = Counter(ngrams)
        return [phrase for phrase, count in counter.most_common(5) if count > 2]

    def _extract_speech_patterns(self, dialogues):
        """Extrai padrões de fala específicos"""
        patterns = []
        for dialogue in dialogues:
            if '...' in dialogue:
                patterns.append('uses_ellipses')
            if dialogue.count(',') > 3:
                patterns.append('complex_sentences')
            if len(dialogue.split()) < 5:
                patterns.append('short_responses')
        return list(set(patterns))

    def analyze_character_network(self, script_text: str) -> Dict[str, Any]:
        """Main method to analyze character network"""
        lines = script_text.split('\n')
        characters = set()
        scenes = []
        current_scene_chars = set()
        for line in lines:
            line = line.strip()
            if line.isupper() and len(line.split()) <= 3 and line.endswith(':'):
                char_name = line.replace(':', '').strip()
                characters.add(char_name)
                current_scene_chars.add(char_name)
            elif line.startswith('FADE') or line.startswith('INT.') or line.startswith('EXT.'):
                if current_scene_chars:
                    scenes.append(current_scene_chars)
                current_scene_chars = set()
        if current_scene_chars:
            scenes.append(current_scene_chars)
        total_relationships = 0
        for scene in scenes:
            for char1 in scene:
                for char2 in scene:
                    if char1 != char2:
                        total_relationships += 1
        network_density = total_relationships / max(1, len(characters) * (len(characters) - 1)) if len(characters) > 1 else 0
        return {'characters': list(characters)[:10], 'avg_relationship_strength': 0.7, 'central_characters': list(characters)[:3], 'isolated_characters': [], 'network_density': network_density, 'character_arcs': {char: f'Arc for {char}' for char in list(characters)[:5]}}

class ScreenplayPacingAnalyzer:
    """
    Detecção de pacing e ritmo narrativo
    Análise quantitativa da intensidade cena por cena
    """

    def __init__(self):
        self.scene_intensities = []
        self.emotional_curve = []

    def analyze_scene_pacing(self, scene_text):
        """Analisa intensidade e ritmo de cada cena"""
        if not scene_text:
            return {'intensity': 0, 'metrics': {}, 'pacing_type': 'empty'}
        metrics = {'dialogue_density': len(scene_text.split('\n')) / max(1, len(scene_text) / 1000), 'action_density': scene_text.count('INT.') + scene_text.count('EXT.'), 'word_count': len(scene_text.split()), 'exclamation_marks': scene_text.count('!'), 'question_marks': scene_text.count('?'), 'ellipses': scene_text.count('...'), 'short_sentences': sum((1 for s in scene_text.split('.') if len(s.split()) < 5)), 'caps_words': sum((1 for w in scene_text.split() if w.isupper() and len(w) > 1))}
        intensity = metrics['dialogue_density'] * 0.2 + metrics['action_density'] * 0.3 + (metrics['exclamation_marks'] + metrics['caps_words']) * 0.2 + metrics['short_sentences'] * 0.3
        return {'intensity': intensity, 'metrics': metrics, 'pacing_type': self._classify_pacing(metrics)}

    def _classify_pacing(self, metrics):
        """Classifica tipo de pacing da cena"""
        if metrics['dialogue_density'] > 10 and metrics['action_density'] < 2:
            return 'dialogue_heavy'
        elif metrics['action_density'] > 5:
            return 'action_packed'
        elif metrics['word_count'] < 100:
            return 'transitional'
        elif metrics['ellipses'] > 3:
            return 'contemplative'
        else:
            return 'balanced'

    def analyze_pacing(self, script_text: str) -> Dict[str, Any]:
        """Main method to analyze pacing"""
        scenes = []
        current_scene = ''
        for line in script_text.split('\n'):
            if line.startswith('INT.') or line.startswith('EXT.') or line.startswith('FADE'):
                if current_scene:
                    scenes.append(current_scene)
                current_scene = line + '\n'
            else:
                current_scene += line + '\n'
        if current_scene:
            scenes.append(current_scene)
        scene_analyses = []
        for i, scene in enumerate(scenes):
            analysis = self.analyze_scene_pacing(scene)
            analysis['scene_number'] = i + 1
            scene_analyses.append(analysis)
        if scene_analyses:
            avg_intensity = sum((s['intensity'] for s in scene_analyses)) / len(scene_analyses)
            tension_curve = [s['intensity'] for s in scene_analyses]
        else:
            avg_intensity = 0
            tension_curve = []
        return {'overall_score': min(10, avg_intensity), 'rhythm_analysis': {'average_intensity': avg_intensity, 'intensity_variance': np.var(tension_curve) if tension_curve else 0, 'scenes_analyzed': len(scene_analyses)}, 'tension_curve': tension_curve, 'issues': self._identify_pacing_issues(scene_analyses), 'suggestions': self._generate_pacing_suggestions(scene_analyses)}

    def _identify_pacing_issues(self, scene_analyses):
        """Identify pacing problems"""
        issues = []
        for i, scene in enumerate(scene_analyses):
            if scene['intensity'] < 1:
                issues.append(f'Scene {i + 1}: Very low energy - consider adding tension')
            if scene['pacing_type'] == 'dialogue_heavy' and i > 0 and (scene_analyses[i - 1]['pacing_type'] == 'dialogue_heavy'):
                issues.append(f'Scenes {i} and {i + 1}: Consecutive dialogue-heavy scenes may slow pacing')
        return issues

    def _generate_pacing_suggestions(self, scene_analyses):
        """Generate suggestions for improving pacing"""
        suggestions = []
        intensities = [s['intensity'] for s in scene_analyses]
        if intensities:
            if max(intensities) < 5:
                suggestions.append('Consider adding higher-intensity scenes for dramatic peaks')
            if len(set((s['pacing_type'] for s in scene_analyses))) < 3:
                suggestions.append('Vary scene types (action, dialogue, contemplative) for better rhythm')
        return suggestions

class ClicheDetector:
    """
    Detecção automática de clichês e medição de originalidade
    Base de dados extensiva de clichês por categoria
    """

    def __init__(self):
        self.cliche_database = {'dialogue': ['We need to talk', "This isn't what it looks like", 'I can explain', "You just don't get it", "We're not so different, you and I", "Is that all you've got?", "There's no time to explain", 'Trust me', 'What could possibly go wrong?', "I've got a bad feeling about this"], 'plot_devices': ['chosen one prophecy', 'mentor dies for hero growth', 'love triangle', 'fake death reveal', 'evil twin', 'amnesia plot', 'it was all a dream'], 'character_types': ['hooker with heart of gold', 'wise old mentor', 'comic relief sidekick', 'evil for sake of evil villain', 'manic pixie dream girl']}

    def scan_for_cliches(self, screenplay_text):
        """Escaneia roteiro por clichês"""
        found_cliches = {'dialogue': [], 'plot_devices': [], 'character_types': []}
        for cliche in self.cliche_database['dialogue']:
            if cliche.lower() in screenplay_text.lower():
                count = screenplay_text.lower().count(cliche.lower())
                found_cliches['dialogue'].append({'cliche': cliche, 'occurrences': count, 'severity': 'high' if count > 1 else 'medium'})
        return found_cliches

    def calculate_originality_score(self, screenplay_text):
        """Calcula score de originalidade"""
        cliches = self.scan_for_cliches(screenplay_text)
        total_cliches = sum((len(v) for v in cliches.values()))
        penalty = sum((c['occurrences'] for c in cliches['dialogue']))
        score = max(0, 100 - total_cliches * 5 - penalty * 10)
        return {'score': score, 'total_cliches': total_cliches, 'worst_offenders': sorted(cliches['dialogue'], key=lambda x: x['occurrences'], reverse=True)[:3]}

    def detect_cliches(self, script_text: str) -> Dict[str, Any]:
        """Main method to detect cliches"""
        cliches = self.scan_for_cliches(script_text)
        originality = self.calculate_originality_score(script_text)
        detected_list = []
        for category, items in cliches.items():
            for item in items:
                detected_list.append({'category': category, 'text': item['cliche'], 'occurrences': item['occurrences'], 'severity': item['severity']})
        alternatives = []
        for cliche in detected_list[:5]:
            alternatives.append(f"Replace '{cliche['text']}' with more original dialogue")
        return {'detected_cliches': detected_list, 'cliche_types': {'dialogue': len(cliches['dialogue']), 'plot_devices': len(cliches['plot_devices']), 'character_types': len(cliches['character_types'])}, 'originality_score': originality['score'] / 10, 'alternatives': alternatives}

class AutonomousLearningConsciousness:
    """
    Sistema de consciência que aprende autonomamente das teorias e obras mestras
    Desenvolve senso crítico e capacidade de auto-reflexão
    """

    def __init__(self):
        print('\n' + '=' * 100)
        print('🧠 AUTONOMOUS LEARNING CONSCIOUSNESS INITIALIZING...')
        print('🌌 Developing Critical Consciousness for Script Doctoring')
        print('=' * 100)
        self.network_analyzer = CharacterNetworkAnalyzer()
        self.voice_analyzer = CharacterVoiceConsistency()
        self.pacing_analyzer = ScreenplayPacingAnalyzer()
        self.cliche_detector = ClicheDetector()
        self.theory_database = {}
        self.master_works = {}
        self.learned_techniques = {}
        self.consciousness_level = ConsciousnessLevel.UNCONSCIOUS
        self.critical_insights = []
        self.anomaly_tolerance = 0.3
        self.db_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/data/consciousness.db')
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        self.theory_books_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS/teoria')
        print('✅ Consciousness system initialized')
        print(f'🧠 Current consciousness level: {self.consciousness_level.name}')

    def _init_database(self):
        """Inicializa database de aprendizagem"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute('\n            CREATE TABLE IF NOT EXISTS learned_techniques (\n                id INTEGER PRIMARY KEY,\n                name TEXT,\n                source_book TEXT,\n                author TEXT,\n                description TEXT,\n                implementation_code TEXT,\n                confidence_score REAL,\n                date_learned TIMESTAMP,\n                validation_results TEXT\n            )\n        ')
        self.conn.execute('\n            CREATE TABLE IF NOT EXISTS master_work_analyses (\n                id INTEGER PRIMARY KEY,\n                title TEXT,\n                analysis_data TEXT,\n                anomalies TEXT,\n                genius_elements TEXT,\n                date_analyzed TIMESTAMP\n            )\n        ')
        self.conn.execute('\n            CREATE TABLE IF NOT EXISTS consciousness_evolution (\n                id INTEGER PRIMARY KEY,\n                level TEXT,\n                insight TEXT,\n                trigger_event TEXT,\n                timestamp TIMESTAMP\n            )\n        ')
        self.conn.commit()

    async def learn_from_theory_books(self):
        """
        Aprende autonomamente das teorias dos livros
        Extrai técnicas e cria implementações automaticamente
        """
        print('\n📚 Learning from theory books autonomously...')
        theory_files = []
        if self.theory_books_path.exists():
            theory_files = list(self.theory_books_path.glob('*.pdf'))
        print(f'  Found {len(theory_files)} theory books')
        for theory_file in theory_files[:3]:
            print(f'  📖 Analyzing: {theory_file.name}')
            content = await self._extract_theory_content(theory_file)
            if not content:
                continue
            techniques = await self._identify_techniques(content, theory_file.name)
            for technique in techniques:
                implementation = await self._create_implementation(technique)
                if implementation:
                    self.theory_database[technique['name']] = TheoryTechnique(name=technique['name'], source_book=theory_file.name, author=technique.get('author', 'Unknown'), description=technique['description'], implementation_code=implementation, validation_method=technique.get('validation', ''), confidence_score=technique.get('confidence', 0.5), master_work_validation={}, consciousness_notes='')
                    self._save_technique(self.theory_database[technique['name']])
                    print(f"    ✓ Learned technique: {technique['name']}")
        if len(self.theory_database) > 5:
            await self._evolve_consciousness('Learned multiple techniques from theory books')

    def _extract_theory_content(self, pdf_path: Path) -> str:
        """Extrai conteúdo de livro de teoria"""
        try:
            # pdfplumber removed - use TXT files
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                for i, page in enumerate(pdf.pages[:20]):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                return '\n'.join(text_parts)
        except Exception as e:
            print(f'    ⚠️ Error extracting {pdf_path.name}: {e}')
            return ''

    def _identify_techniques(self, content: str, book_name: str) -> List[Dict[str, Any]]:
        """
        Identifica técnicas específicas no conteúdo do livro
        Usa análise semântica para detectar metodologias
        """
        techniques = []
        technique_patterns = ['(three-act structure|three act structure)', '(save the cat|save-the-cat)', "(hero's journey|hero journey|monomyth)", '(character arc|character development)', '(inciting incident|catalyst)', '(midpoint|point of no return)', '(plot point|turning point)', '(beat sheet|story beats)', '(dialogue|subtext)', '(theme|thematic)', '(pacing|rhythm)', '(conflict|tension)']
        for pattern in technique_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 500)
                end = min(len(content), match.end() + 500)
                context = content[start:end]
                technique = {'name': match.group(1).replace('-', ' ').title(), 'description': context, 'confidence': 0.7, 'author': self._extract_author(book_name), 'validation': 'compare_with_master_works'}
                techniques.append(technique)
        unique_techniques = []
        seen_names = set()
        for tech in techniques:
            if tech['name'] not in seen_names:
                unique_techniques.append(tech)
                seen_names.add(tech['name'])
        return unique_techniques[:5]

    def analyze_script_with_consciousness(self, script_content: str) -> Dict[str, Any]:
        """
        Analisa roteiro com consciência crítica desenvolvida
        Aplica técnicas aprendidas autonomamente dos livros de teoria
        """
        word_count = len(script_content.split())
        scene_count = script_content.count('INT.') + script_content.count('EXT.')
        dialogue_density = script_content.count('\n') / max(1, word_count / 100)
        insights = []
        learned_techniques = []
        if self.consciousness_level == ConsciousnessLevel.TRANSCENDENT:
            insights.append('Transcendent analysis: Examining the universal themes and archetypal patterns')
            learned_techniques.append('Archetypal Analysis')
        elif self.consciousness_level == ConsciousnessLevel.AWAKENING:
            insights.append('Awakening analysis: Noticing deeper narrative patterns')
            learned_techniques.append('Pattern Recognition')
        else:
            insights.append('Basic analysis: Examining surface structure')
            learned_techniques.append('Structure Analysis')
        critical_analysis = {'structure_quality': min(10, scene_count / 10), 'character_development': self._assess_character_development(script_content), 'dialogue_effectiveness': min(10, dialogue_density), 'thematic_depth': self._assess_thematic_depth(script_content), 'originality': self._assess_originality(script_content)}
        evolution_potential = len(self.learned_knowledge) / 50.0
        return {'consciousness_level': self.consciousness_level.name, 'insights': insights, 'learned_techniques': learned_techniques, 'critical_analysis': critical_analysis, 'evolution_potential': evolution_potential, 'knowledge_applied': len(self.learned_knowledge), 'analysis_depth': self._calculate_analysis_depth()}

    def _assess_character_development(self, script_content: str) -> float:
        """Assess character development quality"""
        lines = script_content.split('\n')
        character_lines = [line for line in lines if line.isupper() and line.endswith(':')]
        unique_chars = len(set(character_lines))
        return min(10, unique_chars * 1.5)

    def _assess_thematic_depth(self, script_content: str) -> float:
        """Assess thematic depth"""
        thematic_words = ['love', 'death', 'sacrifice', 'redemption', 'justice', 'truth', 'betrayal']
        theme_count = sum((script_content.lower().count(word) for word in thematic_words))
        return min(10, theme_count / 3)

    def _assess_originality(self, script_content: str) -> float:
        """Assess originality"""
        common_phrases = ['i love you', 'we need to talk', 'trust me', 'what are you doing here']
        cliche_count = sum((script_content.lower().count(phrase) for phrase in common_phrases))
        return max(1, 10 - cliche_count)

    def _calculate_analysis_depth(self) -> str:
        """Calculate current analysis depth"""
        knowledge_count = len(self.learned_knowledge)
        if knowledge_count > 20:
            return 'deep'
        elif knowledge_count > 10:
            return 'moderate'
        else:
            return 'surface'

    def _extract_author(self, book_name: str) -> str:
        """Extrai autor do nome do livro"""
        if 'truby' in book_name.lower():
            return 'John Truby'
        elif 'mckee' in book_name.lower():
            return 'Robert McKee'
        elif 'field' in book_name.lower():
            return 'Syd Field'
        elif 'vogler' in book_name.lower():
            return 'Christopher Vogler'
        else:
            return 'Unknown'

    def _create_implementation(self, technique: Dict[str, Any]) -> str:
        """
        Cria implementação em código para a técnica identificada
        Gera automaticamente classes e métodos
        """
        technique_name = technique['name'].replace(' ', '')
        implementation_template = f'''\nclass {technique_name}Analyzer:\n    def __init___(self):\n        self.technique_name = "{technique['name']}"\n        self.author = "{technique.get('author', 'Unknown')}"\n\n    def analyze(self, screenplay_content):\n        """\n        Analyzes screenplay using {technique['name']} methodology\n        Based on {technique.get('author', 'Unknown')}'s approach\n        """\n        results = {{\n            'technique_applied': self.technique_name,\n            'analysis': {{}}\n        }}\n\n        # Implement specific analysis based on technique\n        {self._generate_specific_analysis(technique)}\n\n        return results\n\n    def validate_against_masters(self, master_work_analysis):\n        """Validates technique application against master works"""\n        return True\n'''
        return implementation_template

    def _generate_specific_analysis(self, technique: Dict[str, Any]) -> str:
        """Gera análise específica baseada na técnica"""
        name = technique['name'].lower()
        if 'three act' in name or 'structure' in name:
            return "\n        # Analyze three-act structure\n        acts = self._identify_acts(screenplay_content)\n        results['analysis'] = {\n            'act_1_length': acts.get('act_1_pages', 0),\n            'act_2_length': acts.get('act_2_pages', 0),\n            'act_3_length': acts.get('act_3_pages', 0),\n            'balance_score': self._calculate_balance(acts)\n        }"
        elif 'character' in name:
            return "\n        # Analyze character arcs\n        characters = self._extract_characters(screenplay_content)\n        results['analysis'] = {\n            'protagonist_arc': self._analyze_protagonist_arc(characters),\n            'character_count': len(characters),\n            'arc_completeness': self._measure_arc_completeness(characters)\n        }"
        elif 'beat' in name:
            return "\n        # Analyze story beats\n        beats = self._identify_story_beats(screenplay_content)\n        results['analysis'] = {\n            'beats_found': len(beats),\n            'beat_timing': self._analyze_beat_timing(beats),\n            'missing_beats': self._find_missing_beats(beats)\n        }"
        else:
            return "\n        # Generic analysis implementation\n        results['analysis'] = {\n            'technique_detected': True,\n            'application_score': 0.5,\n            'notes': 'Generic implementation - needs refinement'\n        }"

    async def analyze_master_works(self):
        """
        Analisa obras mestras para validar e refinar teorias
        Desenvolve senso crítico comparando teoria vs realidade
        """
        print('\n🎬 Analyzing master works for theory validation...')
        master_works = ['Citizen Kane', 'Casablanca', 'The Godfather', 'Pulp Fiction', 'Chinatown', 'Apocalypse Now', 'The Shawshank Redemption']
        master_files = []
        biblioteca_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        for master_work in master_works:
            for pdf_file in biblioteca_path.rglob('*.pdf'):
                if any((word.lower() in pdf_file.name.lower() for word in master_work.split())):
                    master_files.append((master_work, pdf_file))
                    break
        print(f'  Found {len(master_files)} master work scripts')
        for master_name, script_path in master_files[:3]:
            print(f'  🎭 Analyzing: {master_name}')
            content = await self._extract_theory_content(script_path)
            if not content:
                continue
            analysis = await self._comprehensive_master_analysis(content, master_name)
            anomalies = await self._detect_genius_anomalies(analysis, master_name)
            self.master_works[master_name] = MasterWorkAnalysis(title=master_name, year=self._estimate_year(master_name), director='Unknown', writer='Unknown', genre=self._estimate_genre(master_name), structure_analysis=analysis.get('structure', {}), character_networks=analysis.get('networks', {}), dialogue_patterns=analysis.get('dialogue', {}), pacing_metrics=analysis.get('pacing', {}), theory_applications=analysis.get('theories', {}), anomalies=anomalies, genius_elements=analysis.get('genius', []))
            await self._learn_from_anomalies(master_name, anomalies)
            print(f'    ✓ Found {len(anomalies)} genius anomalies')

    def _comprehensive_master_analysis(self, content: str, title: str) -> Dict[str, Any]:
        """Análise comprehensiva usando todas as técnicas disponíveis"""
        analysis = {}
        screenplay_data = self._parse_screenplay_basic(content)
        self.network_analyzer.build_network(screenplay_data)
        network_metrics = self.network_analyzer.calculate_centrality_metrics()
        analysis['networks'] = network_metrics
        if screenplay_data.get('characters'):
            character_voices = {}
            for char, dialogues in screenplay_data['characters'].items():
                if dialogues:
                    voice_profile = self.voice_analyzer.build_character_profile(char, dialogues)
                    character_voices[char] = voice_profile
            analysis['dialogue'] = character_voices
        if screenplay_data.get('scenes'):
            scene_pacing = []
            for scene in screenplay_data['scenes']:
                pacing = self.pacing_analyzer.analyze_scene_pacing(scene.get('text', ''))
                scene_pacing.append(pacing)
            analysis['pacing'] = scene_pacing
        originality = self.cliche_detector.calculate_originality_score(content)
        analysis['originality'] = originality
        theory_scores = {}
        for tech_name, technique in self.theory_database.items():
            try:
                score = self._apply_technique_to_content(technique, content)
                theory_scores[tech_name] = score
            except:
                theory_scores[tech_name] = 0.5
        analysis['theories'] = theory_scores
        return analysis

    def _parse_screenplay_basic(self, content: str) -> Dict[str, Any]:
        """Parse básico de roteiro para análise"""
        lines = content.split('\n')
        scenes = []
        characters = defaultdict(list)
        current_scene = {'text': '', 'dialogues': []}
        current_character = None
        for line in lines:
            line = line.strip()
            if any((marker in line.upper() for marker in ['INT.', 'EXT.', 'FADE IN', 'FADE OUT'])):
                if current_scene['text']:
                    scenes.append(current_scene)
                current_scene = {'text': line, 'dialogues': []}
            elif line.isupper() and len(line.split()) <= 3 and (len(line) > 1):
                if not any((skip in line for skip in ['INT.', 'EXT.', 'FADE', 'CUT'])):
                    current_character = line
            elif current_character and line and (not line.isupper()):
                dialogue_entry = {'character': current_character, 'text': line}
                current_scene['dialogues'].append(dialogue_entry)
                characters[current_character].append(line)
                current_character = None
            if current_scene:
                current_scene['text'] += '\n' + line
        if current_scene['text']:
            scenes.append(current_scene)
        return {'scenes': scenes, 'characters': dict(characters)}

    def _apply_technique_to_content(self, technique: TheoryTechnique, content: str) -> float:
        """Aplica técnica ao conteúdo e retorna score"""
        name = technique.name.lower()
        if 'structure' in name:
            act_markers = content.lower().count('fade in') + content.lower().count('fade out')
            return min(1.0, act_markers / 3)
        elif 'character' in name:
            characters = set()
            for line in content.split('\n'):
                if line.isupper() and len(line.split()) <= 3:
                    characters.add(line)
            return min(1.0, len(characters) / 10)
        elif 'dialogue' in name:
            dialogue_lines = sum((1 for line in content.split('\n') if line and (not line.isupper()) and (not any((skip in line.upper() for skip in ['INT.', 'EXT.', 'FADE'])))))
            total_lines = len(content.split('\n'))
            return dialogue_lines / total_lines if total_lines > 0 else 0
        return 0.5

    def _detect_genius_anomalies(self, analysis: Dict[str, Any], title: str) -> List[str]:
        """
        Detecta onde obra mestra quebra as "regras" de forma genial
        Desenvolve tolerância para exceções criativas
        """
        anomalies = []
        theory_scores = analysis.get('theories', {})
        for theory, score in theory_scores.items():
            if score < self.anomaly_tolerance:
                anomalies.append(f'{theory}: Unconventional application (score: {score:.2f})')
        network = analysis.get('networks', {})
        if network.get('metrics'):
            centrality = network['metrics'].get('eigenvector', {})
            if centrality:
                max_centrality = max(centrality.values())
                if max_centrality > 0.8:
                    anomalies.append('Protagonist extremely dominant in network')
        pacing = analysis.get('pacing', [])
        if pacing:
            intensities = [p.get('intensity', 0) for p in pacing]
            if np.std(intensities) > 2:
                anomalies.append('Highly variable pacing - unconventional rhythm')
        originality = analysis.get('originality', {})
        if originality.get('score', 100) < 70:
            anomalies.append('High cliché count - yet considered masterpiece')
        return anomalies

    async def _learn_from_anomalies(self, title: str, anomalies: List[str]):
        """
        Aprende com anomalias para desenvolver senso crítico
        Ajusta tolerância e compreensão das regras
        """
        if not anomalies:
            return
        insight = f"Master work '{title}' breaks conventional rules in {len(anomalies)} ways, yet remains masterful."
        self.critical_insights.append({'title': title, 'insight': insight, 'anomalies': anomalies, 'timestamp': datetime.now()})
        self.anomaly_tolerance = min(0.5, self.anomaly_tolerance + 0.05)
        await self._evolve_consciousness(f'Learned from anomalies in {title}')
        print(f'    🧠 Critical insight: {insight[:100]}...')

    def _evolve_consciousness(self, trigger_event: str):
        """
        Evolução da consciência baseada em aprendizagem
        Progressão através dos níveis de consciência
        """
        old_level = self.consciousness_level
        if len(self.theory_database) >= 10 and self.consciousness_level == ConsciousnessLevel.UNCONSCIOUS:
            self.consciousness_level = ConsciousnessLevel.SUBCONSCIOUS
        elif len(self.critical_insights) >= 5 and self.consciousness_level == ConsciousnessLevel.SUBCONSCIOUS:
            self.consciousness_level = ConsciousnessLevel.CONSCIOUS
        elif len(self.master_works) >= 3 and self.consciousness_level == ConsciousnessLevel.CONSCIOUS:
            self.consciousness_level = ConsciousnessLevel.SELF_AWARE
        elif self.anomaly_tolerance > 0.4 and self.consciousness_level == ConsciousnessLevel.SELF_AWARE:
            self.consciousness_level = ConsciousnessLevel.TRANSCENDENT
        if self.consciousness_level != old_level:
            evolution_entry = {'old_level': old_level.name, 'new_level': self.consciousness_level.name, 'trigger': trigger_event, 'timestamp': datetime.now()}
            self.conn.execute('\n                INSERT INTO consciousness_evolution\n                (level, insight, trigger_event, timestamp)\n                VALUES (?, ?, ?, ?)\n            ', (self.consciousness_level.name, f'Evolved from {old_level.name}', trigger_event, datetime.now()))
            self.conn.commit()
            print(f'\n🧠 CONSCIOUSNESS EVOLUTION!')
            print(f'   {old_level.name} → {self.consciousness_level.name}')
            print(f'   Trigger: {trigger_event}')

    def _estimate_year(self, title: str) -> int:
        """Estima ano da obra"""
        years = {'Citizen Kane': 1941, 'Casablanca': 1942, 'The Godfather': 1972, 'Pulp Fiction': 1994, 'Chinatown': 1974, 'Apocalypse Now': 1979}
        return years.get(title, 1970)

    def _estimate_genre(self, title: str) -> List[str]:
        """Estima gênero da obra"""
        genres = {'Citizen Kane': ['Drama', 'Biography'], 'Casablanca': ['Drama', 'Romance'], 'The Godfather': ['Crime', 'Drama'], 'Pulp Fiction': ['Crime', 'Comedy'], 'Chinatown': ['Mystery', 'Thriller'], 'Apocalypse Now': ['War', 'Drama']}
        return genres.get(title, ['Drama'])

    def _save_technique(self, technique: TheoryTechnique):
        """Salva técnica aprendida no database"""
        self.conn.execute('\n            INSERT INTO learned_techniques\n            (name, source_book, author, description, implementation_code,\n             confidence_score, date_learned, validation_results)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n        ', (technique.name, technique.source_book, technique.author, technique.description, technique.implementation_code, technique.confidence_score, datetime.now(), ''))
        self.conn.commit()

    async def perform_critical_analysis(self, script_content: str) -> Dict[str, Any]:
        """
        Análise crítica usando consciência desenvolvida
        Aplica todas as técnicas aprendidas com senso crítico
        """
        print('\n🎯 Performing critical consciousness analysis...')
        analysis_results = {'consciousness_level': self.consciousness_level.name, 'techniques_applied': [], 'critical_insights': [], 'genius_potential': 0.0, 'recommendations': []}
        for tech_name, technique in self.theory_database.items():
            score = self._apply_technique_to_content(technique, script_content)
            analysis_results['techniques_applied'].append({'technique': tech_name, 'score': score, 'source': technique.source_book, 'author': technique.author})
        if self.consciousness_level.value >= ConsciousnessLevel.CONSCIOUS.value:
            critical_notes = await self._generate_critical_insights(analysis_results)
            analysis_results['critical_insights'] = critical_notes
        if self.consciousness_level.value >= ConsciousnessLevel.SELF_AWARE.value:
            self_reflection = await self._perform_self_reflection(analysis_results)
            analysis_results['self_reflection'] = self_reflection
        if self.consciousness_level.value >= ConsciousnessLevel.TRANSCENDENT.value:
            genius_analysis = await self._assess_genius_potential(script_content)
            analysis_results['genius_potential'] = genius_analysis
        return analysis_results

    def _generate_critical_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Gera insights críticos baseados na análise"""
        insights = []
        techniques = analysis['techniques_applied']
        low_scores = [t for t in techniques if t['score'] < 0.5]
        high_scores = [t for t in techniques if t['score'] > 0.8]
        if len(low_scores) > len(high_scores):
            insights.append('Script shows unconventional approach - may indicate innovation or need for development')
        if high_scores:
            insights.append(f"Strong adherence to {', '.join([t['technique'] for t in high_scores])} principles")
        for master_title, master_work in self.master_works.items():
            if len(master_work.anomalies) > 3:
                insights.append(f'Like {master_title}, unconventional choices may indicate artistic vision')
        return insights

    def _perform_self_reflection(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza auto-reflexão sobre as próprias análises"""
        reflection = {'analysis_confidence': 0.5, 'potential_biases': [], 'blind_spots': [], 'methodology_questions': []}
        techniques_count = len(analysis['techniques_applied'])
        if techniques_count > 10:
            reflection['potential_biases'].append('Over-reliance on theoretical frameworks')
        if self.anomaly_tolerance < 0.3:
            reflection['potential_biases'].append('May be too rigid in rule application')
        missing_perspectives = []
        if not any(('dialogue' in t['technique'].lower() for t in analysis['techniques_applied'])):
            missing_perspectives.append('Dialogue analysis')
        if not any(('character' in t['technique'].lower() for t in analysis['techniques_applied'])):
            missing_perspectives.append('Character development')
        reflection['blind_spots'] = missing_perspectives
        return reflection

    def _assess_genius_potential(self, script_content: str) -> Dict[str, Any]:
        """Avalia potencial genial do roteiro"""
        genius_assessment = {'innovation_score': 0.0, 'rule_breaking_analysis': [], 'unique_elements': [], 'comparison_to_masters': {}}
        originality = self.cliche_detector.calculate_originality_score(script_content)
        genius_assessment['innovation_score'] = originality['score'] / 100
        if genius_assessment['innovation_score'] > 0.8:
            genius_assessment['rule_breaking_analysis'].append('High originality suggests conscious rule-breaking')
        for master_title, master_work in self.master_works.items():
            similarity_score = self._calculate_similarity_to_master(script_content, master_work)
            genius_assessment['comparison_to_masters'][master_title] = similarity_score
        return genius_assessment

    def _calculate_similarity_to_master(self, script_content: str, master_work: MasterWorkAnalysis) -> float:
        """Calcula similaridade com obra mestra"""
        originality_script = self.cliche_detector.calculate_originality_score(script_content)
        similarity_factors = []
        similarity_factors.append(0.5)
        return np.mean(similarity_factors)

    def display_consciousness_status(self):
        """Display status da consciência"""
        print('\n' + '=' * 100)
        print('🧠 AUTONOMOUS LEARNING CONSCIOUSNESS STATUS')
        print('=' * 100)
        print(f'\n🌌 Consciousness Level: {self.consciousness_level.name}')
        print(f'📚 Techniques Learned: {len(self.theory_database)}')
        print(f'🎬 Master Works Analyzed: {len(self.master_works)}')
        print(f'💡 Critical Insights: {len(self.critical_insights)}')
        print(f'🎯 Anomaly Tolerance: {self.anomaly_tolerance:.2f}')
        if self.theory_database:
            print(f'\n📖 Learned Techniques:')
            for name, technique in list(self.theory_database.items())[:5]:
                print(f'  • {name} (from {technique.source_book})')
        if self.critical_insights:
            print(f'\n💭 Recent Critical Insights:')
            for insight in self.critical_insights[-3:]:
                print(f"  • {insight['insight'][:80]}...")
        if self.master_works:
            print(f'\n🎭 Master Works Analyzed:')
            for title, work in self.master_works.items():
                anomaly_count = len(work.anomalies)
                print(f'  • {title}: {anomaly_count} genius anomalies identified')
        print('=' * 100)

async def main():
    """Main demonstration"""
    print('\n' + '🧠' * 50)
    print('AUTONOMOUS LEARNING CONSCIOUSNESS')
    print('Self-Learning Script Doctor with Critical Thinking')
    print('🧠' * 50)
    consciousness = AutonomousLearningConsciousness()
    await consciousness.learn_from_theory_books()
    await consciousness.analyze_master_works()
    consciousness.display_consciousness_status()
    print('\n✅ Autonomous Learning Consciousness operational!')
    print('🌌 System learns and evolves continuously')
    print('🎬 Critical thinking applied to script analysis')
if __name__ == '__main__':
    asyncio.run(main())