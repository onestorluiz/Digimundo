"""
🎬 SCREENPLAY COMPARISON SYSTEM SUPREME
Compare multiple screenplays, find similarities, track evolution
"""
import asyncio
import json
import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import re
from collections import defaultdict, Counter
import numpy as np
from enum import Enum

class ComparisonType(Enum):
    STRUCTURE = 'structure'
    CHARACTERS = 'characters'
    THEMES = 'themes'
    DIALOGUE = 'dialogue'
    TECHNICAL = 'technical'
    EVOLUTION = 'evolution'
    SIMILARITY = 'similarity'
    PLAGIARISM = 'plagiarism'

@dataclass
class ScreenplayMetadata:
    title: str
    author: str = 'Unknown'
    draft: str = '1'
    date: str = ''
    pages: int = 0
    genre: List[str] = field(default_factory=list)
    logline: str = ''
    file_hash: str = ''

@dataclass
class CharacterProfile:
    name: str
    lines_count: int = 0
    words_count: int = 0
    scenes_count: int = 0
    avg_line_length: float = 0
    vocabulary_size: int = 0
    emotional_arc: List[float] = field(default_factory=list)
    relationships: Dict[str, int] = field(default_factory=dict)
    signature_phrases: List[str] = field(default_factory=list)

@dataclass
class StructuralElement:
    element_type: str
    page_start: int
    page_end: int
    duration: int
    description: str = ''
    tension_level: float = 0
    characters_present: List[str] = field(default_factory=list)

@dataclass
class ComparisonResult:
    screenplay_a: str
    screenplay_b: str
    overall_similarity: float = 0
    structure_similarity: float = 0
    character_similarity: float = 0
    dialogue_similarity: float = 0
    theme_similarity: float = 0
    unique_to_a: Dict[str, Any] = field(default_factory=dict)
    unique_to_b: Dict[str, Any] = field(default_factory=dict)
    shared_elements: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

class ScreenplayComparisonSystem:

    def __init__(self):
        self.screenplays_db: Dict[str, Dict] = {}
        self.comparison_cache: Dict[str, ComparisonResult] = {}
        self.evolution_tracking: Dict[str, List[Dict]] = {}
        self.similarity_threshold = 0.85
        self.database_path = Path('output/comparisons')
        self.database_path.mkdir(parents=True, exist_ok=True)
        self.load_comparison_history()

    def load_comparison_history(self):
        """Load previous comparisons"""
        history_file = self.database_path / 'comparison_history.json'
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.screenplays_db = data.get('screenplays', {})
                    self.evolution_tracking = data.get('evolution', {})
            except:
                pass

    def save_comparison_history(self):
        """Save comparison history"""
        history_file = self.database_path / 'comparison_history.json'
        with open(history_file, 'w') as f:
            json.dump({'screenplays': self.screenplays_db, 'evolution': self.evolution_tracking, 'timestamp': datetime.now().isoformat()}, f, indent=2, default=str)

    def analyze_screenplay(self, filepath: Path) -> Dict:
        """Deep analysis of a screenplay"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        file_hash = hashlib.sha256(content.encode()).hexdigest()
        metadata = self.extract_metadata(content)
        metadata.file_hash = file_hash
        structure = self.analyze_structure(content)
        characters = self.analyze_characters(content)
        themes = self.analyze_themes(content)
        dialogue_patterns = self.analyze_dialogue_patterns(content)
        technical = self.analyze_technical_aspects(content)
        analysis = {'filepath': str(filepath), 'metadata': metadata.__dict__, 'structure': structure, 'characters': {c.name: c.__dict__ for c in characters}, 'themes': themes, 'dialogue_patterns': dialogue_patterns, 'technical': technical, 'analysis_date': datetime.now().isoformat()}
        self.screenplays_db[file_hash] = analysis
        self.save_comparison_history()
        return analysis

    def extract_metadata(self, content: str) -> ScreenplayMetadata:
        """Extract screenplay metadata"""
        metadata = ScreenplayMetadata(title='Untitled', pages=len(content.split('\n')) // 55)
        title_match = re.search('(?:Title:|TITLE:)\\s*(.+)', content, re.IGNORECASE)
        if title_match:
            metadata.title = title_match.group(1).strip()
        else:
            first_lines = content.split('\n')[:5]
            for line in first_lines:
                if line.strip() and (not line.startswith('(')):
                    metadata.title = line.strip()
                    break
        author_match = re.search('(?:Written by|By|Author:)\\s*(.+)', content, re.IGNORECASE)
        if author_match:
            metadata.author = author_match.group(1).strip()
        draft_match = re.search('(?:Draft|DRAFT|Revision)\\s*([\\d.]+|\\w+)', content, re.IGNORECASE)
        if draft_match:
            metadata.draft = draft_match.group(1).strip()
        genre_keywords = {'Action': ['explosion', 'chase', 'fight', 'battle'], 'Comedy': ['laughs', 'joke', 'funny', 'humor'], 'Drama': ['tears', 'emotional', 'conflict', 'relationship'], 'Horror': ['scary', 'terror', 'blood', 'monster'], 'Sci-Fi': ['space', 'future', 'technology', 'alien'], 'Romance': ['love', 'kiss', 'heart', 'relationship']}
        content_lower = content.lower()
        for genre, keywords in genre_keywords.items():
            if any((kw in content_lower for kw in keywords)):
                metadata.genre.append(genre)
        return metadata

    def analyze_structure(self, content: str) -> List[StructuralElement]:
        """Analyze screenplay structure"""
        structure = []
        lines = content.split('\n')
        current_page = 1
        lines_per_page = 55
        act_pattern = re.compile('^(ACT\\s+\\w+|Act\\s+\\w+)', re.MULTILINE)
        acts = act_pattern.finditer(content)
        for match in acts:
            line_num = content[:match.start()].count('\n')
            page = line_num // lines_per_page + 1
            structure.append(StructuralElement(element_type='act', page_start=page, page_end=page, duration=1, description=match.group()))
        scene_pattern = re.compile('^(INT\\.|EXT\\.|I/E\\.).*', re.MULTILINE)
        scenes = scene_pattern.finditer(content)
        for i, match in enumerate(scenes):
            line_num = content[:match.start()].count('\n')
            page = line_num // lines_per_page + 1
            scene_end = content.find('\n\n', match.end())
            if scene_end == -1:
                scene_end = len(content)
            scene_content = content[match.start():scene_end]
            char_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n', re.MULTILINE)
            characters = list(set(char_pattern.findall(scene_content)))
            structure.append(StructuralElement(element_type='scene', page_start=page, page_end=page + (scene_end - match.start()) // (lines_per_page * 60), duration=(scene_end - match.start()) // (lines_per_page * 60) + 1, description=match.group()[:50], characters_present=characters))
        return structure

    def analyze_characters(self, content: str) -> List[CharacterProfile]:
        """Analyze character profiles"""
        characters = {}
        dialogue_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n((?:(?!^[A-Z][A-Z\\s]+\\n).)+)', re.MULTILINE | re.DOTALL)
        for match in dialogue_pattern.finditer(content):
            char_name = match.group(1).strip()
            dialogue = match.group(2).strip()
            if char_name not in characters:
                characters[char_name] = CharacterProfile(name=char_name)
            profile = characters[char_name]
            profile.lines_count += 1
            words = dialogue.split()
            profile.words_count += len(words)
            if not hasattr(profile, '_vocabulary'):
                profile._vocabulary = set()
            profile._vocabulary.update((word.lower() for word in words if word.isalpha()))
            profile.vocabulary_size = len(profile._vocabulary)
        for profile in characters.values():
            if profile.lines_count > 0:
                profile.avg_line_length = profile.words_count / profile.lines_count
        return list(characters.values())

    def analyze_themes(self, content: str) -> Dict[str, float]:
        """Analyze thematic elements"""
        themes = {}
        content_lower = content.lower()
        theme_keywords = {'redemption': ['forgive', 'redeem', 'second chance', 'atone'], 'love': ['love', 'heart', 'romance', 'passion', 'affection'], 'betrayal': ['betray', 'deceive', 'backstab', 'treachery'], 'power': ['power', 'control', 'dominate', 'authority'], 'sacrifice': ['sacrifice', 'give up', 'loss', 'selfless'], 'identity': ['identity', 'who am i', 'self', 'discover'], 'family': ['family', 'father', 'mother', 'sibling', 'parent'], 'justice': ['justice', 'fair', 'right', 'wrong', 'law'], 'survival': ['survive', 'alive', 'death', 'danger'], 'friendship': ['friend', 'buddy', 'companion', 'loyalty']}
        for theme, keywords in theme_keywords.items():
            count = sum((content_lower.count(kw) for kw in keywords))
            if count > 0:
                themes[theme] = count / (len(content) / 1000)
        return themes

    def analyze_dialogue_patterns(self, content: str) -> Dict[str, Any]:
        """Analyze dialogue patterns"""
        patterns = {'avg_line_length': 0, 'question_ratio': 0, 'exclamation_ratio': 0, 'profanity_count': 0, 'subtext_indicators': 0, 'common_phrases': [], 'dialogue_density': 0}
        dialogue_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n((?:(?!^[A-Z][A-Z\\s]+\\n).)+)', re.MULTILINE | re.DOTALL)
        dialogues = dialogue_pattern.findall(content)
        if dialogues:
            all_dialogue = ' '.join((d[1] for d in dialogues))
            dialogue_lines = [d[1].strip() for d in dialogues]
            patterns['avg_line_length'] = sum((len(line.split()) for line in dialogue_lines)) / len(dialogue_lines)
            patterns['question_ratio'] = sum((1 for line in dialogue_lines if '?' in line)) / len(dialogue_lines)
            patterns['exclamation_ratio'] = sum((1 for line in dialogue_lines if '!' in line)) / len(dialogue_lines)
            patterns['subtext_indicators'] = (all_dialogue.count('...') + all_dialogue.count('--') + all_dialogue.count('(')) / len(dialogue_lines)
            patterns['dialogue_density'] = len(all_dialogue) / len(content)
            words = all_dialogue.lower().split()
            phrases = []
            for i in range(len(words) - 2):
                phrase = ' '.join(words[i:i + 3])
                if all_dialogue.lower().count(phrase) > 2:
                    phrases.append(phrase)
            phrase_counter = Counter(phrases)
            patterns['common_phrases'] = phrase_counter.most_common(10)
        return patterns

    def analyze_technical_aspects(self, content: str) -> Dict[str, Any]:
        """Analyze technical screenplay aspects"""
        technical = {'format_score': 100, 'scene_headings': 0, 'action_lines': 0, 'parentheticals': 0, 'transitions': 0, 'camera_directions': 0, 'format_issues': [], 'avg_action_length': 0, 'white_space_ratio': 0}
        lines = content.split('\n')
        technical['scene_headings'] = len(re.findall('^(INT\\.|EXT\\.|I/E\\.)', content, re.MULTILINE))
        technical['parentheticals'] = content.count('(')
        technical['transitions'] = len(re.findall('^(CUT TO:|FADE IN:|FADE OUT:|DISSOLVE TO:)', content, re.MULTILINE))
        technical['camera_directions'] = len(re.findall('(CLOSE UP|WIDE SHOT|PAN|ZOOM|ANGLE ON|POV)', content, re.IGNORECASE))
        action_lines = []
        for i, line in enumerate(lines):
            if line and (not re.match('^[A-Z][A-Z\\s]+$', line)) and (len(line) > 75):
                technical['format_issues'].append(f'Line {i + 1}: Action line too long')
                technical['format_score'] -= 1
            if line and (not re.match('^[A-Z][A-Z\\s]+$', line)) and (not line.startswith('(')):
                action_lines.append(line)
        if action_lines:
            technical['avg_action_length'] = sum((len(line.split()) for line in action_lines)) / len(action_lines)
        empty_lines = sum((1 for line in lines if not line.strip()))
        technical['white_space_ratio'] = empty_lines / len(lines)
        if technical['camera_directions'] > technical['scene_headings'] * 0.5:
            technical['format_issues'].append('Excessive camera directions')
            technical['format_score'] -= 10
        return technical

    async def compare_screenplays(self, screenplay_a: Path, screenplay_b: Path, comparison_types: List[ComparisonType]=None) -> ComparisonResult:
        """Compare two screenplays"""
        if comparison_types is None:
            comparison_types = list(ComparisonType)
        analysis_a = await self.analyze_screenplay(screenplay_a)
        analysis_b = await self.analyze_screenplay(screenplay_b)
        result = ComparisonResult(screenplay_a=analysis_a['metadata']['title'], screenplay_b=analysis_b['metadata']['title'])
        if ComparisonType.STRUCTURE in comparison_types:
            result.structure_similarity = self.compare_structure(analysis_a['structure'], analysis_b['structure'])
        if ComparisonType.CHARACTERS in comparison_types:
            result.character_similarity = self.compare_characters(analysis_a['characters'], analysis_b['characters'])
        if ComparisonType.THEMES in comparison_types:
            result.theme_similarity = self.compare_themes(analysis_a['themes'], analysis_b['themes'])
        if ComparisonType.DIALOGUE in comparison_types:
            result.dialogue_similarity = self.compare_dialogue(analysis_a['dialogue_patterns'], analysis_b['dialogue_patterns'])
        similarities = [result.structure_similarity, result.character_similarity, result.theme_similarity, result.dialogue_similarity]
        result.overall_similarity = sum(similarities) / len(similarities)
        if result.overall_similarity > self.similarity_threshold:
            result.warnings.append(f'High similarity detected ({result.overall_similarity:.1%}). Consider reviewing for potential plagiarism.')
        result.unique_to_a = self.find_unique_elements(analysis_a, analysis_b)
        result.unique_to_b = self.find_unique_elements(analysis_b, analysis_a)
        result.suggestions = self.generate_comparison_suggestions(result)
        cache_key = f"{analysis_a['metadata']['file_hash']}_{analysis_b['metadata']['file_hash']}"
        self.comparison_cache[cache_key] = result
        self.save_comparison(result)
        return result

    def compare_structure(self, structure_a: List[Dict], structure_b: List[Dict]) -> float:
        """Compare structural elements"""
        if not structure_a or not structure_b:
            return 0.0
        scenes_a = [s for s in structure_a if s.get('element_type') == 'scene']
        scenes_b = [s for s in structure_b if s.get('element_type') == 'scene']
        scene_diff = abs(len(scenes_a) - len(scenes_b))
        scene_similarity = 1 - scene_diff / max(len(scenes_a), len(scenes_b))
        acts_a = [s for s in structure_a if s.get('element_type') == 'act']
        acts_b = [s for s in structure_b if s.get('element_type') == 'act']
        act_similarity = 1.0 if len(acts_a) == len(acts_b) else 0.5
        durations_a = [s.get('duration', 1) for s in scenes_a]
        durations_b = [s.get('duration', 1) for s in scenes_b]
        if durations_a and durations_b:
            avg_a = sum(durations_a) / len(durations_a)
            avg_b = sum(durations_b) / len(durations_b)
            pacing_similarity = 1 - abs(avg_a - avg_b) / max(avg_a, avg_b)
        else:
            pacing_similarity = 0
        return (scene_similarity + act_similarity + pacing_similarity) / 3

    def compare_characters(self, chars_a: Dict, chars_b: Dict) -> float:
        """Compare character profiles"""
        if not chars_a or not chars_b:
            return 0.0
        names_a = set(chars_a.keys())
        names_b = set(chars_b.keys())
        shared_names = names_a & names_b
        all_names = names_a | names_b
        name_similarity = len(shared_names) / len(all_names) if all_names else 0
        importance_similarity = 0
        if shared_names:
            for name in shared_names:
                lines_a = chars_a[name].get('lines_count', 0)
                lines_b = chars_b[name].get('lines_count', 0)
                if lines_a and lines_b:
                    importance_similarity += 1 - abs(lines_a - lines_b) / max(lines_a, lines_b)
            importance_similarity /= len(shared_names)
        return (name_similarity + importance_similarity) / 2

    def compare_themes(self, themes_a: Dict, themes_b: Dict) -> float:
        """Compare thematic elements"""
        if not themes_a or not themes_b:
            return 0.0
        all_themes = set(themes_a.keys()) | set(themes_b.keys())
        shared_themes = set(themes_a.keys()) & set(themes_b.keys())
        if not all_themes:
            return 0.0
        theme_overlap = len(shared_themes) / len(all_themes)
        weight_similarity = 0
        if shared_themes:
            for theme in shared_themes:
                weight_a = themes_a[theme]
                weight_b = themes_b[theme]
                weight_similarity += 1 - abs(weight_a - weight_b) / max(weight_a, weight_b)
            weight_similarity /= len(shared_themes)
        return (theme_overlap + weight_similarity) / 2

    def compare_dialogue(self, dialogue_a: Dict, dialogue_b: Dict) -> float:
        """Compare dialogue patterns"""
        if not dialogue_a or not dialogue_b:
            return 0.0
        similarities = []
        if dialogue_a.get('avg_line_length') and dialogue_b.get('avg_line_length'):
            diff = abs(dialogue_a['avg_line_length'] - dialogue_b['avg_line_length'])
            similarities.append(1 - diff / max(dialogue_a['avg_line_length'], dialogue_b['avg_line_length']))
        if 'question_ratio' in dialogue_a and 'question_ratio' in dialogue_b:
            diff = abs(dialogue_a['question_ratio'] - dialogue_b['question_ratio'])
            similarities.append(1 - diff)
        if 'dialogue_density' in dialogue_a and 'dialogue_density' in dialogue_b:
            diff = abs(dialogue_a['dialogue_density'] - dialogue_b['dialogue_density'])
            similarities.append(1 - diff)
        return sum(similarities) / len(similarities) if similarities else 0

    def find_unique_elements(self, analysis_a: Dict, analysis_b: Dict) -> Dict:
        """Find elements unique to screenplay A"""
        unique = {}
        chars_a = set(analysis_a.get('characters', {}).keys())
        chars_b = set(analysis_b.get('characters', {}).keys())
        unique['characters'] = list(chars_a - chars_b)
        themes_a = set(analysis_a.get('themes', {}).keys())
        themes_b = set(analysis_b.get('themes', {}).keys())
        unique['themes'] = list(themes_a - themes_b)
        tech_a = analysis_a.get('technical', {})
        tech_b = analysis_b.get('technical', {})
        if tech_a.get('camera_directions', 0) > tech_b.get('camera_directions', 0) * 2:
            unique['technical'] = 'Significantly more camera directions'
        return unique

    def generate_comparison_suggestions(self, result: ComparisonResult) -> List[str]:
        """Generate suggestions based on comparison"""
        suggestions = []
        if result.structure_similarity < 0.5:
            suggestions.append("The screenplays have very different structures. Consider if they're meant for the same format/medium.")
        if result.character_similarity < 0.3:
            suggestions.append('Character profiles are significantly different. This could indicate different storytelling approaches.')
        elif result.character_similarity > 0.9:
            suggestions.append('Characters are very similar. Consider differentiating character voices more.')
        if result.theme_similarity > 0.8:
            suggestions.append('Themes are very similar. Good thematic consistency if these are drafts of the same project.')
        if result.unique_to_a.get('characters'):
            suggestions.append(f"{result.screenplay_a} has unique characters: {', '.join(result.unique_to_a['characters'][:3])}")
        return suggestions

    async def track_evolution(self, project_name: str, screenplay_path: Path, draft_number: str) -> Dict:
        """Track screenplay evolution across drafts"""
        analysis = await self.analyze_screenplay(screenplay_path)
        analysis['draft_number'] = draft_number
        if project_name not in self.evolution_tracking:
            self.evolution_tracking[project_name] = []
        self.evolution_tracking[project_name].append(analysis)
        self.evolution_tracking[project_name].sort(key=lambda x: x.get('draft_number', '0'))
        evolution_report = self.generate_evolution_report(project_name)
        self.save_comparison_history()
        return evolution_report

    def generate_evolution_report(self, project_name: str) -> Dict:
        """Generate report on screenplay evolution"""
        if project_name not in self.evolution_tracking:
            return {'error': 'Project not found'}
        drafts = self.evolution_tracking[project_name]
        if len(drafts) < 2:
            return {'error': 'Need at least 2 drafts to compare'}
        report = {'project': project_name, 'total_drafts': len(drafts), 'evolution': [], 'trends': {}, 'improvements': [], 'concerns': []}
        for i in range(1, len(drafts)):
            prev = drafts[i - 1]
            curr = drafts[i]
            evolution = {'from_draft': prev.get('draft_number', 'unknown'), 'to_draft': curr.get('draft_number', 'unknown'), 'page_change': curr['metadata']['pages'] - prev['metadata']['pages'], 'character_changes': len(set(curr['characters'].keys()) - set(prev['characters'].keys())), 'new_themes': list(set(curr['themes'].keys()) - set(prev['themes'].keys()))}
            report['evolution'].append(evolution)
        page_counts = [d['metadata']['pages'] for d in drafts]
        if all((page_counts[i] <= page_counts[i + 1] for i in range(len(page_counts) - 1))):
            report['trends']['length'] = 'Increasing'
        elif all((page_counts[i] >= page_counts[i + 1] for i in range(len(page_counts) - 1))):
            report['trends']['length'] = 'Decreasing'
        else:
            report['trends']['length'] = 'Variable'
        first_chars = set(drafts[0]['characters'].keys())
        last_chars = set(drafts[-1]['characters'].keys())
        if len(last_chars) > len(first_chars):
            report['improvements'].append('Character roster expanded')
        first_dialogue = drafts[0]['dialogue_patterns'].get('avg_line_length', 0)
        last_dialogue = drafts[-1]['dialogue_patterns'].get('avg_line_length', 0)
        if 5 < last_dialogue < 15 and (first_dialogue < 5 or first_dialogue > 15):
            report['improvements'].append('Dialogue length normalized')
        if len(drafts) > 5:
            report['concerns'].append('Many drafts - consider finalizing')
        latest_format_score = drafts[-1]['technical'].get('format_score', 100)
        if latest_format_score < 80:
            report['concerns'].append('Format issues persist in latest draft')
        return report

    def save_comparison(self, result: ComparisonResult):
        """Save comparison result"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'comparison_{timestamp}.json'
        filepath = self.database_path / filename
        with open(filepath, 'w') as f:
            json.dump(result.__dict__, f, indent=2, default=str)

    async def find_similar_screenplays(self, screenplay_path: Path, threshold: float=0.7) -> List[Tuple[str, float]]:
        """Find similar screenplays in database"""
        target = await self.analyze_screenplay(screenplay_path)
        target_hash = target['metadata']['file_hash']
        similar = []
        for file_hash, screenplay in self.screenplays_db.items():
            if file_hash == target_hash:
                continue
            similarity = 0
            target_genres = set(target['metadata'].get('genre', []))
            other_genres = set(screenplay['metadata'].get('genre', []))
            if target_genres and other_genres:
                genre_sim = len(target_genres & other_genres) / len(target_genres | other_genres)
                similarity += genre_sim * 0.3
            target_themes = set(target['themes'].keys())
            other_themes = set(screenplay['themes'].keys())
            if target_themes and other_themes:
                theme_sim = len(target_themes & other_themes) / len(target_themes | other_themes)
                similarity += theme_sim * 0.4
            target_pages = target['metadata']['pages']
            other_pages = screenplay['metadata']['pages']
            if target_pages and other_pages:
                page_sim = 1 - abs(target_pages - other_pages) / max(target_pages, other_pages)
                similarity += page_sim * 0.3
            if similarity >= threshold:
                similar.append((screenplay['metadata']['title'], similarity))
        similar.sort(key=lambda x: x[1], reverse=True)
        return similar

async def main():
    """Test the comparison system"""
    system = ScreenplayComparisonSystem()
    test_dir = Path('test_screenplays')
    if test_dir.exists():
        scripts = list(test_dir.glob('*.pdf')) + list(test_dir.glob('*.txt'))
        if len(scripts) >= 2:
            result = await system.compare_screenplays(scripts[0], scripts[1], [ComparisonType.STRUCTURE, ComparisonType.CHARACTERS, ComparisonType.THEMES])
            print(f'\nComparison: {result.screenplay_a} vs {result.screenplay_b}')
            print(f'Overall Similarity: {result.overall_similarity:.1%}')
            print(f'Structure: {result.structure_similarity:.1%}')
            print(f'Characters: {result.character_similarity:.1%}')
            print(f'Themes: {result.theme_similarity:.1%}')
            if result.warnings:
                print('\nWarnings:')
                for warning in result.warnings:
                    print(f'  - {warning}')
            if result.suggestions:
                print('\nSuggestions:')
                for suggestion in result.suggestions:
                    print(f'  - {suggestion}')
        if len(scripts) > 1:
            for i, script in enumerate(scripts):
                evolution = await system.track_evolution('TestProject', script, f'Draft {i + 1}')
            print('\nEvolution Report:')
            print(json.dumps(evolution, indent=2))
    else:
        print('No test screenplays found. Add PDFs or text files to test_screenplays/')
if __name__ == '__main__':
    asyncio.run(main())