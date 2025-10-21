"""
🔍 SEMANTIC SEARCH LIBRARY SUPREME
Deep semantic search across screenplay library with AI understanding
"""
import asyncio
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import re
import hashlib
from collections import defaultdict, Counter
import pickle
from enum import Enum

class SearchType(Enum):
    SEMANTIC = 'semantic'
    CHARACTER = 'character'
    DIALOGUE = 'dialogue'
    SCENE = 'scene'
    THEME = 'theme'
    EMOTION = 'emotion'
    STRUCTURE = 'structure'
    SIMILARITY = 'similarity'

@dataclass
class SearchResult:
    screenplay: str
    location: str
    content: str
    relevance_score: float
    context: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SemanticVector:
    """Semantic representation of text"""
    vector: np.ndarray
    text: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class SemanticSearchLibrary:

    def __init__(self):
        self.index_path = Path('output/semantic_index')
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.vectors: Dict[str, List[SemanticVector]] = {}
        self.embeddings_cache: Dict[str, np.ndarray] = {}
        self.screenplay_index: Dict[str, Dict] = {}
        self.load_index()
        self.initialize_semantic_models()

    def initialize_semantic_models(self):
        """Initialize semantic understanding models"""
        self.emotion_keywords = {'joy': ['happy', 'laugh', 'smile', 'celebrate', 'excited'], 'sadness': ['cry', 'tears', 'sad', 'mourn', 'grief'], 'anger': ['angry', 'rage', 'furious', 'mad', 'yell'], 'fear': ['scared', 'afraid', 'terror', 'panic', 'frighten'], 'love': ['love', 'kiss', 'embrace', 'passion', 'romantic'], 'surprise': ['shock', 'surprise', 'astonish', 'unexpected'], 'tension': ['tense', 'nervous', 'anxious', 'stress', 'pressure']}
        self.structural_markers = {'opening': ['FADE IN', 'OPENING', 'BEGIN'], 'inciting_incident': ['suddenly', 'everything changes', 'until'], 'turning_point': ['but then', 'however', 'reversal'], 'climax': ['final', 'showdown', 'confrontation', 'battle'], 'resolution': ['FADE OUT', 'THE END', 'finally']}
        self.theme_indicators = {'redemption': ['forgive', 'second chance', 'redeem', 'change'], 'identity': ['who am i', 'true self', 'identity', 'become'], 'sacrifice': ['give up', 'sacrifice', 'cost', 'price'], 'power': ['control', 'power', 'dominate', 'rule'], 'family': ['family', 'blood', 'legacy', 'inherit'], 'justice': ['justice', 'right', 'wrong', 'fair', 'law'], 'love': ['love', 'heart', 'soul', 'together'], 'betrayal': ['betray', 'trust', 'deceive', 'lie']}

    def load_index(self):
        """Load existing semantic index"""
        index_file = self.index_path / 'semantic_index.pkl'
        if index_file.exists():
            try:
                with open(index_file, 'rb') as f:
                    data = pickle.load(f)
                    self.vectors = data.get('vectors', {})
                    self.screenplay_index = data.get('screenplay_index', {})
                    self.embeddings_cache = data.get('embeddings_cache', {})
            except:
                pass

    def save_index(self):
        """Save semantic index"""
        index_file = self.index_path / 'semantic_index.pkl'
        with open(index_file, 'wb') as f:
            pickle.dump({'vectors': self.vectors, 'screenplay_index': self.screenplay_index, 'embeddings_cache': self.embeddings_cache, 'timestamp': datetime.now().isoformat()}, f)

    def index_screenplay(self, filepath: Path) -> Dict:
        """Index a screenplay for semantic search"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        screenplay_id = hashlib.md5(str(filepath).encode()).hexdigest()
        scenes = self.extract_scenes(content)
        dialogues = self.extract_dialogues(content)
        characters = self.extract_characters(content)
        vectors = []
        for scene in scenes:
            vector = self.create_semantic_vector(scene['text'], 'scene')
            vector.metadata = {'type': 'scene', 'location': scene['location'], 'page': scene.get('page', 0)}
            vectors.append(vector)
        for dialogue in dialogues:
            vector = self.create_semantic_vector(dialogue['text'], 'dialogue')
            vector.metadata = {'type': 'dialogue', 'character': dialogue['character'], 'page': dialogue.get('page', 0)}
            vectors.append(vector)
        themes = self.extract_themes(content)
        for theme, excerpts in themes.items():
            for excerpt in excerpts[:3]:
                vector = self.create_semantic_vector(excerpt, 'theme')
                vector.metadata = {'type': 'theme', 'theme': theme}
                vectors.append(vector)
        self.vectors[screenplay_id] = vectors
        self.screenplay_index[screenplay_id] = {'filepath': str(filepath), 'title': filepath.stem, 'indexed_date': datetime.now().isoformat(), 'scenes_count': len(scenes), 'dialogues_count': len(dialogues), 'characters': list(characters), 'themes': list(themes.keys()), 'vector_count': len(vectors)}
        self.save_index()
        return self.screenplay_index[screenplay_id]

    def extract_scenes(self, content: str) -> List[Dict]:
        """Extract scenes from screenplay"""
        scenes = []
        scene_pattern = re.compile('^(INT\\.|EXT\\.|I/E\\.)([^\\n]+)\\n((?:(?!INT\\.|EXT\\.|I/E\\.).)*)', re.MULTILINE | re.DOTALL)
        for match in scene_pattern.finditer(content):
            scene_heading = match.group(1) + match.group(2)
            scene_content = match.group(3)[:500]
            scenes.append({'location': scene_heading, 'text': scene_heading + '\n' + scene_content, 'page': content[:match.start()].count('\n') // 55})
        return scenes

    def extract_dialogues(self, content: str) -> List[Dict]:
        """Extract character dialogues"""
        dialogues = []
        dialogue_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n((?:(?!^[A-Z][A-Z\\s]+\\n).)+)', re.MULTILINE | re.DOTALL)
        for match in dialogue_pattern.finditer(content):
            character = match.group(1).strip()
            dialogue_text = match.group(2).strip()
            dialogues.append({'character': character, 'text': dialogue_text, 'page': content[:match.start()].count('\n') // 55})
        return dialogues

    def extract_characters(self, content: str) -> Set[str]:
        """Extract character names"""
        char_pattern = re.compile('^([A-Z][A-Z\\s]+)$', re.MULTILINE)
        return set(char_pattern.findall(content))

    def extract_themes(self, content: str) -> Dict[str, List[str]]:
        """Extract thematic content"""
        themes = defaultdict(list)
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            paragraph_lower = paragraph.lower()
            for theme, indicators in self.theme_indicators.items():
                if any((indicator in paragraph_lower for indicator in indicators)):
                    themes[theme].append(paragraph[:200])
        return dict(themes)

    def create_semantic_vector(self, text: str, vector_type: str) -> SemanticVector:
        """Create semantic vector from text"""
        cache_key = hashlib.md5(text.encode()).hexdigest()
        if cache_key in self.embeddings_cache:
            vector = self.embeddings_cache[cache_key]
        else:
            vector = self.create_text_embedding(text)
            self.embeddings_cache[cache_key] = vector
        return SemanticVector(vector=vector, text=text[:200], source=vector_type)

    def create_text_embedding(self, text: str) -> np.ndarray:
        """Create text embedding (simplified version)"""
        features = []
        text_lower = text.lower()
        features.append(len(text) / 1000)
        features.append(len(text.split()) / 100)
        for emotion, keywords in self.emotion_keywords.items():
            score = sum((1 for kw in keywords if kw in text_lower))
            features.append(score / len(keywords))
        for struct_type, markers in self.structural_markers.items():
            score = sum((1 for marker in markers if marker.lower() in text_lower))
            features.append(score / len(markers))
        for theme, indicators in self.theme_indicators.items():
            score = sum((1 for ind in indicators if ind in text_lower))
            features.append(score / len(indicators))
        while len(features) < 100:
            features.append(0)
        return np.array(features[:100])

    async def search(self, query: str, search_type: SearchType=SearchType.SEMANTIC, limit: int=10, screenplay_filter: Optional[List[str]]=None) -> List[SearchResult]:
        """Perform semantic search"""
        results = []
        if search_type == SearchType.SEMANTIC:
            results = await self.semantic_search(query, limit, screenplay_filter)
        elif search_type == SearchType.CHARACTER:
            results = await self.character_search(query, limit, screenplay_filter)
        elif search_type == SearchType.DIALOGUE:
            results = await self.dialogue_search(query, limit, screenplay_filter)
        elif search_type == SearchType.SCENE:
            results = await self.scene_search(query, limit, screenplay_filter)
        elif search_type == SearchType.THEME:
            results = await self.theme_search(query, limit, screenplay_filter)
        elif search_type == SearchType.EMOTION:
            results = await self.emotion_search(query, limit, screenplay_filter)
        elif search_type == SearchType.STRUCTURE:
            results = await self.structure_search(query, limit, screenplay_filter)
        elif search_type == SearchType.SIMILARITY:
            results = await self.similarity_search(query, limit, screenplay_filter)
        return results

    def semantic_search(self, query: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Perform semantic similarity search"""
        query_vector = self.create_text_embedding(query)
        all_results = []
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                similarity = self.cosine_similarity(query_vector, vector.vector)
                all_results.append(SearchResult(screenplay=screenplay_info['title'], location=f"Page {vector.metadata.get('page', '?')}", content=vector.text, relevance_score=similarity, context=vector.metadata.get('type', 'unknown'), metadata=vector.metadata))
        all_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return all_results[:limit]

    def character_search(self, query: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Search for character-specific content"""
        results = []
        character_name = query.upper()
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                if vector.metadata.get('type') == 'dialogue':
                    if vector.metadata.get('character') == character_name:
                        results.append(SearchResult(screenplay=screenplay_info['title'], location=f"Page {vector.metadata.get('page', '?')}", content=vector.text, relevance_score=1.0, context=f'Dialogue by {character_name}', metadata=vector.metadata))
        return results[:limit]

    def dialogue_search(self, query: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Search dialogue patterns"""
        results = []
        query_lower = query.lower()
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                if vector.metadata.get('type') == 'dialogue':
                    if query_lower in vector.text.lower():
                        relevance = vector.text.lower().count(query_lower) / len(vector.text.split())
                        results.append(SearchResult(screenplay=screenplay_info['title'], location=f"Page {vector.metadata.get('page', '?')}", content=vector.text, relevance_score=relevance, context=f"Dialogue by {vector.metadata.get('character', 'Unknown')}", metadata=vector.metadata))
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]

    def scene_search(self, query: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Search scene descriptions"""
        results = []
        query_lower = query.lower()
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                if vector.metadata.get('type') == 'scene':
                    if query_lower in vector.text.lower():
                        relevance = vector.text.lower().count(query_lower) / len(vector.text.split())
                        results.append(SearchResult(screenplay=screenplay_info['title'], location=vector.metadata.get('location', 'Unknown'), content=vector.text, relevance_score=relevance, context='Scene', metadata=vector.metadata))
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]

    def theme_search(self, theme: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Search for thematic content"""
        results = []
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                if vector.metadata.get('theme') == theme:
                    results.append(SearchResult(screenplay=screenplay_info['title'], location=f'Theme: {theme}', content=vector.text, relevance_score=1.0, context=f'Thematic content: {theme}', metadata=vector.metadata))
        return results[:limit]

    def emotion_search(self, emotion: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Search for emotional moments"""
        results = []
        keywords = self.emotion_keywords.get(emotion.lower(), [emotion.lower()])
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                text_lower = vector.text.lower()
                emotion_score = sum((1 for kw in keywords if kw in text_lower))
                if emotion_score > 0:
                    results.append(SearchResult(screenplay=screenplay_info['title'], location=f"Page {vector.metadata.get('page', '?')}", content=vector.text, relevance_score=emotion_score / len(keywords), context=f'Emotional moment: {emotion}', metadata={**vector.metadata, 'emotion': emotion}))
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]

    def structure_search(self, structure_element: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Search for structural elements"""
        results = []
        markers = self.structural_markers.get(structure_element.lower(), [structure_element])
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                text_lower = vector.text.lower()
                if any((marker.lower() in text_lower for marker in markers)):
                    results.append(SearchResult(screenplay=screenplay_info['title'], location=f"Page {vector.metadata.get('page', '?')}", content=vector.text, relevance_score=1.0, context=f'Structural element: {structure_element}', metadata={**vector.metadata, 'structure': structure_element}))
        return results[:limit]

    def similarity_search(self, reference_text: str, limit: int, screenplay_filter: Optional[List[str]]) -> List[SearchResult]:
        """Find similar scenes or passages"""
        ref_vector = self.create_text_embedding(reference_text)
        results = []
        for screenplay_id, vectors in self.vectors.items():
            if screenplay_filter:
                screenplay_title = self.screenplay_index[screenplay_id]['title']
                if screenplay_title not in screenplay_filter:
                    continue
            screenplay_info = self.screenplay_index[screenplay_id]
            for vector in vectors:
                similarity = self.cosine_similarity(ref_vector, vector.vector)
                if similarity > 0.7:
                    results.append(SearchResult(screenplay=screenplay_info['title'], location=f"Page {vector.metadata.get('page', '?')}", content=vector.text, relevance_score=similarity, context=f'Similar to reference ({similarity:.1%})', metadata=vector.metadata))
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def get_library_stats(self) -> Dict:
        """Get library statistics"""
        total_vectors = sum((len(vectors) for vectors in self.vectors.values()))
        stats = {'total_screenplays': len(self.screenplay_index), 'total_vectors': total_vectors, 'total_scenes': sum((info['scenes_count'] for info in self.screenplay_index.values())), 'total_dialogues': sum((info['dialogues_count'] for info in self.screenplay_index.values())), 'unique_characters': len(set((char for info in self.screenplay_index.values() for char in info['characters']))), 'themes_covered': len(set((theme for info in self.screenplay_index.values() for theme in info['themes']))), 'index_size_mb': self.index_path.stat().st_size / 1024 / 1024 if (self.index_path / 'semantic_index.pkl').exists() else 0}
        return stats

    def find_connections(self, screenplay_a: str, screenplay_b: str) -> Dict:
        """Find connections between screenplays"""
        id_a = None
        id_b = None
        for sid, info in self.screenplay_index.items():
            if info['title'] == screenplay_a:
                id_a = sid
            if info['title'] == screenplay_b:
                id_b = sid
        if not id_a or not id_b:
            return {'error': 'Screenplay not found'}
        connections = {'shared_themes': [], 'similar_scenes': [], 'character_parallels': [], 'dialogue_echoes': []}
        themes_a = set(self.screenplay_index[id_a]['themes'])
        themes_b = set(self.screenplay_index[id_b]['themes'])
        connections['shared_themes'] = list(themes_a & themes_b)
        vectors_a = self.vectors[id_a]
        vectors_b = self.vectors[id_b]
        for vec_a in vectors_a:
            if vec_a.metadata.get('type') == 'scene':
                for vec_b in vectors_b:
                    if vec_b.metadata.get('type') == 'scene':
                        similarity = self.cosine_similarity(vec_a.vector, vec_b.vector)
                        if similarity > 0.8:
                            connections['similar_scenes'].append({'scene_a': vec_a.metadata.get('location'), 'scene_b': vec_b.metadata.get('location'), 'similarity': similarity})
        return connections

async def main():
    """Test semantic search library"""
    library = SemanticSearchLibrary()
    test_screenplay = Path('test_screenplay.txt')
    with open(test_screenplay, 'w') as f:
        f.write("THE MATRIX\n\nFADE IN:\n\nINT. APARTMENT - NIGHT\n\nNEO, 30s, a computer hacker, sits at his computer. The screen glows green.\n\nNEO\nWhat is the Matrix?\n\nTRINITY appears behind him.\n\nTRINITY\nThe answer is out there, Neo. It's looking for you.\n\nEXT. CITY STREET - DAY\n\nNeo walks through the crowd, feeling disconnected from reality.\n\nMORPHEUS (V.O.)\nYou're living in a dream world, Neo.\n\nINT. CONSTRUCT - WHITE VOID\n\nMorpheus shows Neo the truth about reality.\n\nMORPHEUS\nWelcome to the real world.\n\nNeo looks shocked as he processes this revelation about identity and reality.\n\nFADE OUT.\n")
    print('Indexing screenplay...')
    index_info = await library.index_screenplay(test_screenplay)
    print(f'Indexed: {index_info}')
    print('\n' + '=' * 50)
    print('Testing Semantic Search')
    results = await library.search('searching for truth about reality', SearchType.SEMANTIC, limit=3)
    print(f"\nSemantic search results for 'searching for truth about reality':")
    for result in results:
        print(f'  [{result.relevance_score:.2f}] {result.screenplay} - {result.location}')
        print(f'    {result.content[:100]}...')
    results = await library.search('NEO', SearchType.CHARACTER, limit=2)
    print(f"\nCharacter search results for 'NEO':")
    for result in results:
        print(f'  {result.screenplay} - {result.context}')
        print(f'    {result.content[:100]}...')
    results = await library.search('identity', SearchType.THEME, limit=2)
    print(f"\nTheme search results for 'identity':")
    for result in results:
        print(f'  {result.screenplay} - {result.context}')
        print(f'    {result.content[:100]}...')
    results = await library.search('surprise', SearchType.EMOTION, limit=2)
    print(f"\nEmotion search results for 'surprise':")
    for result in results:
        print(f'  [{result.relevance_score:.2f}] {result.screenplay}')
        print(f'    {result.content[:100]}...')
    print('\n' + '=' * 50)
    print('Library Statistics:')
    stats = library.get_library_stats()
    for key, value in stats.items():
        print(f'  {key}: {value}')
if __name__ == '__main__':
    asyncio.run(main())