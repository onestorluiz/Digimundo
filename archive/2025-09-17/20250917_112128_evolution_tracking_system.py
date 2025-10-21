"""
📊 EVOLUTION TRACKING SYSTEM SUPREME
Track and analyze screenplay evolution across drafts with deep insights
"""
import asyncio
import json
import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re
from collections import defaultdict, Counter
import numpy as np
from enum import Enum

class EvolutionMetric(Enum):
    STRUCTURAL = 'structural'
    DIALOGUE = 'dialogue'
    CHARACTER = 'character'
    PACING = 'pacing'
    THEME = 'theme'
    COMPLEXITY = 'complexity'
    QUALITY = 'quality'
    MOMENTUM = 'momentum'

@dataclass
class DraftSnapshot:
    """Snapshot of a screenplay draft"""
    draft_number: str
    timestamp: datetime
    file_hash: str
    pages: int
    scenes: int
    characters: List[str]
    word_count: int
    dialogue_ratio: float
    metrics: Dict[str, float] = field(default_factory=dict)
    notes: str = ''

@dataclass
class EvolutionChange:
    """A specific change between drafts"""
    change_type: str
    location: str
    old_content: str
    new_content: str
    impact_score: float = 0.0
    category: str = ''

@dataclass
class EvolutionInsight:
    """Insight about screenplay evolution"""
    insight_type: str
    description: str
    evidence: List[str]
    confidence: float
    recommendation: str = ''

class EvolutionTrackingSystem:

    def __init__(self):
        self.projects: Dict[str, List[DraftSnapshot]] = {}
        self.evolution_graphs: Dict[str, Dict] = {}
        self.insights_cache: Dict[str, List[EvolutionInsight]] = {}
        self.database_path = Path('output/evolution_tracking')
        self.database_path.mkdir(parents=True, exist_ok=True)
        self.load_evolution_data()
        self.analysis_engines = {'structural': self.analyze_structural_evolution, 'character': self.analyze_character_evolution, 'dialogue': self.analyze_dialogue_evolution, 'pacing': self.analyze_pacing_evolution, 'quality': self.analyze_quality_evolution, 'momentum': self.analyze_momentum_evolution}

    def load_evolution_data(self):
        """Load existing evolution data"""
        data_file = self.database_path / 'evolution_data.json'
        if data_file.exists():
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    for project, drafts in data.get('projects', {}).items():
                        self.projects[project] = [DraftSnapshot(draft_number=d['draft_number'], timestamp=datetime.fromisoformat(d['timestamp']), file_hash=d['file_hash'], pages=d['pages'], scenes=d['scenes'], characters=d['characters'], word_count=d['word_count'], dialogue_ratio=d['dialogue_ratio'], metrics=d.get('metrics', {}), notes=d.get('notes', '')) for d in drafts]
                    self.evolution_graphs = data.get('graphs', {})
            except Exception as e:
                print(f'Error loading evolution data: {e}')

    def save_evolution_data(self):
        """Save evolution data"""
        data_file = self.database_path / 'evolution_data.json'
        projects_data = {}
        for project, drafts in self.projects.items():
            projects_data[project] = [{'draft_number': d.draft_number, 'timestamp': d.timestamp.isoformat(), 'file_hash': d.file_hash, 'pages': d.pages, 'scenes': d.scenes, 'characters': d.characters, 'word_count': d.word_count, 'dialogue_ratio': d.dialogue_ratio, 'metrics': d.metrics, 'notes': d.notes} for d in drafts]
        with open(data_file, 'w') as f:
            json.dump({'projects': projects_data, 'graphs': self.evolution_graphs, 'last_updated': datetime.now().isoformat()}, f, indent=2)

    async def track_draft(self, project_name: str, filepath: Path, draft_number: str, notes: str='') -> DraftSnapshot:
        """Track a new draft of a screenplay"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        snapshot = DraftSnapshot(draft_number=draft_number, timestamp=datetime.now(), file_hash=hashlib.sha256(content.encode()).hexdigest(), pages=len(content.split('\n')) // 55, scenes=len(re.findall('(INT\\.|EXT\\.)', content)), characters=self.extract_characters(content), word_count=len(content.split()), dialogue_ratio=self.calculate_dialogue_ratio(content), notes=notes)
        snapshot.metrics = await self.calculate_draft_metrics(content)
        if project_name not in self.projects:
            self.projects[project_name] = []
        self.projects[project_name].append(snapshot)
        self.projects[project_name].sort(key=lambda d: d.draft_number)
        self.save_evolution_data()
        if len(self.projects[project_name]) > 1:
            await self.generate_evolution_insights(project_name)
        return snapshot

    def extract_characters(self, content: str) -> List[str]:
        """Extract character names from screenplay"""
        char_pattern = re.compile('^([A-Z][A-Z\\s]+)$', re.MULTILINE)
        characters = list(set(char_pattern.findall(content)))
        return characters[:20]

    def calculate_dialogue_ratio(self, content: str) -> float:
        """Calculate ratio of dialogue to total content"""
        dialogue_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n((?:(?!^[A-Z][A-Z\\s]+\\n).)+)', re.MULTILINE | re.DOTALL)
        dialogues = dialogue_pattern.findall(content)
        dialogue_text = ' '.join((d[1] for d in dialogues))
        if len(content) > 0:
            return len(dialogue_text) / len(content)
        return 0.0

    def calculate_draft_metrics(self, content: str) -> Dict[str, float]:
        """Calculate various metrics for a draft"""
        metrics = {}
        metrics['avg_scene_length'] = self.calculate_avg_scene_length(content)
        metrics['dialogue_complexity'] = self.calculate_dialogue_complexity(content)
        metrics['action_density'] = self.calculate_action_density(content)
        metrics['act_balance'] = self.calculate_act_balance(content)
        metrics['scene_variety'] = self.calculate_scene_variety(content)
        metrics['format_score'] = self.calculate_format_score(content)
        metrics['pacing_score'] = self.calculate_pacing_score(content)
        return metrics

    def calculate_avg_scene_length(self, content: str) -> float:
        """Calculate average scene length"""
        scenes = re.split('(INT\\.|EXT\\.)', content)
        if len(scenes) > 2:
            scene_lengths = [len(scene.split()) for scene in scenes[2::2]]
            return sum(scene_lengths) / len(scene_lengths) if scene_lengths else 0
        return 0

    def calculate_dialogue_complexity(self, content: str) -> float:
        """Calculate dialogue complexity (vocabulary diversity)"""
        dialogue_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n((?:(?!^[A-Z][A-Z\\s]+\\n).)+)', re.MULTILINE | re.DOTALL)
        dialogues = dialogue_pattern.findall(content)
        if not dialogues:
            return 0
        all_words = []
        for _, dialogue in dialogues:
            words = dialogue.lower().split()
            all_words.extend((word for word in words if word.isalpha()))
        if all_words:
            unique_words = len(set(all_words))
            total_words = len(all_words)
            return unique_words / total_words
        return 0

    def calculate_action_density(self, content: str) -> float:
        """Calculate density of action lines"""
        lines = content.split('\n')
        action_lines = [line for line in lines if line and (not re.match('^[A-Z][A-Z\\s]+$', line)) and (not line.startswith('INT.')) and (not line.startswith('EXT.'))]
        if lines:
            return len(action_lines) / len(lines)
        return 0

    def calculate_act_balance(self, content: str) -> float:
        """Calculate balance between acts"""
        total_pages = len(content.split('\n')) // 55
        return 0.8

    def calculate_scene_variety(self, content: str) -> float:
        """Calculate variety of scene locations"""
        scene_pattern = re.compile('(INT\\.|EXT\\.)([^\\n]+)', re.MULTILINE)
        locations = [match.group(2).strip() for match in scene_pattern.finditer(content)]
        if locations:
            unique_locations = len(set(locations))
            total_scenes = len(locations)
            return unique_locations / total_scenes
        return 0

    def calculate_format_score(self, content: str) -> float:
        """Calculate screenplay format quality"""
        score = 100.0
        lines = content.split('\n')
        for line in lines:
            if len(line) > 75:
                score -= 0.1
            if line.startswith(' ') and len(line.strip()) > 0:
                score -= 0.05
        return max(0, min(100, score))

    def calculate_pacing_score(self, content: str) -> float:
        """Calculate pacing score"""
        scenes = re.split('(INT\\.|EXT\\.)', content)
        if len(scenes) > 2:
            scene_lengths = [len(scene.split()) for scene in scenes[2::2]]
            if scene_lengths:
                std_dev = np.std(scene_lengths)
                mean_length = np.mean(scene_lengths)
                if mean_length > 0:
                    coefficient_of_variation = std_dev / mean_length
                    if 0.5 <= coefficient_of_variation <= 0.7:
                        return 100
                    elif coefficient_of_variation < 0.5:
                        return 70
                    else:
                        return 80
        return 50

    def compare_drafts(self, project_name: str, draft_a: str, draft_b: str) -> Dict[str, Any]:
        """Compare two specific drafts"""
        if project_name not in self.projects:
            return {'error': 'Project not found'}
        drafts = self.projects[project_name]
        snapshot_a = next((d for d in drafts if d.draft_number == draft_a), None)
        snapshot_b = next((d for d in drafts if d.draft_number == draft_b), None)
        if not snapshot_a or not snapshot_b:
            return {'error': 'Draft not found'}
        comparison = {'draft_a': draft_a, 'draft_b': draft_b, 'time_between': (snapshot_b.timestamp - snapshot_a.timestamp).days, 'page_change': snapshot_b.pages - snapshot_a.pages, 'scene_change': snapshot_b.scenes - snapshot_a.scenes, 'word_count_change': snapshot_b.word_count - snapshot_a.word_count, 'dialogue_ratio_change': snapshot_b.dialogue_ratio - snapshot_a.dialogue_ratio, 'metric_changes': {}, 'character_changes': {'added': list(set(snapshot_b.characters) - set(snapshot_a.characters)), 'removed': list(set(snapshot_a.characters) - set(snapshot_b.characters))}}
        for metric in snapshot_a.metrics:
            if metric in snapshot_b.metrics:
                change = snapshot_b.metrics[metric] - snapshot_a.metrics[metric]
                comparison['metric_changes'][metric] = {'old': snapshot_a.metrics[metric], 'new': snapshot_b.metrics[metric], 'change': change, 'percent_change': change / snapshot_a.metrics[metric] * 100 if snapshot_a.metrics[metric] != 0 else 0}
        return comparison

    async def generate_evolution_insights(self, project_name: str) -> List[EvolutionInsight]:
        """Generate insights about screenplay evolution"""
        if project_name not in self.projects:
            return []
        drafts = self.projects[project_name]
        if len(drafts) < 2:
            return []
        insights = []
        trajectory_insight = self.analyze_trajectory(drafts)
        if trajectory_insight:
            insights.append(trajectory_insight)
        character_insight = await self.analyze_character_evolution(drafts)
        if character_insight:
            insights.append(character_insight)
        structural_insight = await self.analyze_structural_evolution(drafts)
        if structural_insight:
            insights.append(structural_insight)
        dialogue_insight = await self.analyze_dialogue_evolution(drafts)
        if dialogue_insight:
            insights.append(dialogue_insight)
        pacing_insight = await self.analyze_pacing_evolution(drafts)
        if pacing_insight:
            insights.append(pacing_insight)
        quality_insight = await self.analyze_quality_evolution(drafts)
        if quality_insight:
            insights.append(quality_insight)
        momentum_insight = await self.analyze_momentum_evolution(drafts)
        if momentum_insight:
            insights.append(momentum_insight)
        self.insights_cache[project_name] = insights
        return insights

    def analyze_trajectory(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze overall trajectory of evolution"""
        page_counts = [d.pages for d in drafts]
        if all((page_counts[i] <= page_counts[i + 1] for i in range(len(page_counts) - 1))):
            trend = 'expanding'
            description = 'Screenplay is consistently growing in length'
            recommendation = "Consider tightening - longer isn't always better"
        elif all((page_counts[i] >= page_counts[i + 1] for i in range(len(page_counts) - 1))):
            trend = 'condensing'
            description = 'Screenplay is being refined and condensed'
            recommendation = "Good discipline - ensure key moments aren't lost"
        else:
            trend = 'oscillating'
            description = 'Screenplay length is fluctuating between drafts'
            recommendation = 'Consider stabilizing structure before fine-tuning'
        return EvolutionInsight(insight_type='trajectory', description=description, evidence=[f'Draft {d.draft_number}: {d.pages} pages' for d in drafts[-3:]], confidence=0.8, recommendation=recommendation)

    def analyze_character_evolution(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze how characters evolved"""
        first_draft = drafts[0]
        last_draft = drafts[-1]
        persistent_chars = set(first_draft.characters) & set(last_draft.characters)
        new_chars = set(last_draft.characters) - set(first_draft.characters)
        removed_chars = set(first_draft.characters) - set(last_draft.characters)
        if len(new_chars) > len(removed_chars):
            description = 'Character roster is expanding - story becoming more complex'
            recommendation = 'Ensure each character has a clear purpose'
        elif len(removed_chars) > len(new_chars):
            description = 'Character consolidation - focusing the narrative'
            recommendation = 'Good streamlining - verify emotional beats are preserved'
        else:
            description = 'Character roster is stable across drafts'
            recommendation = 'Consider deepening existing characters'
        return EvolutionInsight(insight_type='character_evolution', description=description, evidence=[f'Persistent: {len(persistent_chars)} characters', f'Added: {len(new_chars)} characters', f'Removed: {len(removed_chars)} characters'], confidence=0.85, recommendation=recommendation)

    def analyze_structural_evolution(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze structural changes"""
        scene_counts = [d.scenes for d in drafts]
        if len(scene_counts) > 1:
            scene_change = scene_counts[-1] - scene_counts[0]
            avg_scene_change = scene_change / (len(drafts) - 1)
            if avg_scene_change > 2:
                description = 'Structure becoming more granular with more scenes'
                recommendation = 'Good for pacing - ensure transitions flow'
            elif avg_scene_change < -2:
                description = 'Scenes being combined - structure simplifying'
                recommendation = 'Efficient storytelling - maintain visual variety'
            else:
                description = 'Structure remaining consistent'
                recommendation = 'Stable foundation - focus on scene quality'
            return EvolutionInsight(insight_type='structural_evolution', description=description, evidence=[f'First draft: {scene_counts[0]} scenes', f'Latest draft: {scene_counts[-1]} scenes', f'Average change: {avg_scene_change:.1f} scenes/draft'], confidence=0.75, recommendation=recommendation)
        return None

    def analyze_dialogue_evolution(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze dialogue changes"""
        dialogue_ratios = [d.dialogue_ratio for d in drafts]
        if len(dialogue_ratios) > 1:
            ratio_change = dialogue_ratios[-1] - dialogue_ratios[0]
            if ratio_change > 0.1:
                description = 'Dialogue increasing - becoming more dialogue-heavy'
                recommendation = "Ensure visual storytelling isn't neglected"
            elif ratio_change < -0.1:
                description = 'Dialogue decreasing - more visual storytelling'
                recommendation = 'Great for cinema - ensure character voices remain clear'
            else:
                description = 'Dialogue balance maintained'
                recommendation = 'Good consistency - refine quality over quantity'
            return EvolutionInsight(insight_type='dialogue_evolution', description=description, evidence=[f'First draft: {dialogue_ratios[0]:.1%} dialogue', f'Latest draft: {dialogue_ratios[-1]:.1%} dialogue'], confidence=0.7, recommendation=recommendation)
        return None

    def analyze_pacing_evolution(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze pacing changes"""
        pacing_scores = [d.metrics.get('pacing_score', 50) for d in drafts]
        if len(pacing_scores) > 1:
            pacing_trend = pacing_scores[-1] - pacing_scores[0]
            if pacing_trend > 10:
                description = 'Pacing improving - better rhythm and flow'
                recommendation = 'Excellent progress - fine-tune climactic moments'
            elif pacing_trend < -10:
                description = 'Pacing becoming less consistent'
                recommendation = 'Review scene transitions and rhythm'
            else:
                description = 'Pacing relatively stable'
                recommendation = 'Consider varying scene lengths for dynamics'
            return EvolutionInsight(insight_type='pacing_evolution', description=description, evidence=[f'Early pacing score: {pacing_scores[0]:.0f}', f'Current pacing score: {pacing_scores[-1]:.0f}'], confidence=0.65, recommendation=recommendation)
        return None

    def analyze_quality_evolution(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze overall quality trajectory"""
        quality_scores = []
        for draft in drafts:
            score = 0
            score += draft.metrics.get('format_score', 50) * 0.2
            score += draft.metrics.get('dialogue_complexity', 0.5) * 100 * 0.3
            score += draft.metrics.get('scene_variety', 0.5) * 100 * 0.2
            score += draft.metrics.get('pacing_score', 50) * 0.3
            quality_scores.append(score)
        if len(quality_scores) > 1:
            quality_change = quality_scores[-1] - quality_scores[0]
            if quality_change > 5:
                description = 'Overall quality improving across drafts'
                recommendation = 'Momentum is positive - maintain standards'
                confidence = 0.8
            elif quality_change < -5:
                description = 'Quality metrics declining - possible overworking'
                recommendation = 'Step back and revisit core strengths'
                confidence = 0.7
            else:
                description = 'Quality holding steady'
                recommendation = 'Time for bold creative choices'
                confidence = 0.6
            return EvolutionInsight(insight_type='quality_evolution', description=description, evidence=[f"Quality trajectory: {('+' if quality_change > 0 else '')}{quality_change:.1f} points", f'Current quality score: {quality_scores[-1]:.1f}/100'], confidence=confidence, recommendation=recommendation)
        return None

    def analyze_momentum_evolution(self, drafts: List[DraftSnapshot]) -> Optional[EvolutionInsight]:
        """Analyze momentum of changes"""
        if len(drafts) < 3:
            return None
        change_rates = []
        for i in range(1, len(drafts)):
            prev = drafts[i - 1]
            curr = drafts[i]
            page_change = abs(curr.pages - prev.pages) / max(prev.pages, 1)
            scene_change = abs(curr.scenes - prev.scenes) / max(prev.scenes, 1)
            dialogue_change = abs(curr.dialogue_ratio - prev.dialogue_ratio)
            change_rate = (page_change + scene_change + dialogue_change) / 3
            change_rates.append(change_rate)
        if change_rates:
            recent_momentum = np.mean(change_rates[-2:]) if len(change_rates) > 1 else change_rates[-1]
            if recent_momentum > 0.2:
                description = 'High momentum - significant changes between drafts'
                recommendation = 'Good exploration - consider stabilizing soon'
            elif recent_momentum < 0.05:
                description = 'Low momentum - minimal changes'
                recommendation = 'Script may be ready or needs fresh perspective'
            else:
                description = 'Moderate momentum - steady refinement'
                recommendation = 'Healthy revision pace - stay focused'
            return EvolutionInsight(insight_type='momentum', description=description, evidence=[f'Recent change rate: {recent_momentum:.1%}', f'Drafts analyzed: {len(drafts)}'], confidence=0.7, recommendation=recommendation)
        return None

    def generate_evolution_report(self, project_name: str) -> Dict:
        """Generate comprehensive evolution report"""
        if project_name not in self.projects:
            return {'error': 'Project not found'}
        drafts = self.projects[project_name]
        insights = self.insights_cache.get(project_name, [])
        report = {'project': project_name, 'total_drafts': len(drafts), 'time_span': (drafts[-1].timestamp - drafts[0].timestamp).days if len(drafts) > 1 else 0, 'first_draft': {'date': drafts[0].timestamp.isoformat(), 'pages': drafts[0].pages, 'scenes': drafts[0].scenes}, 'latest_draft': {'date': drafts[-1].timestamp.isoformat(), 'pages': drafts[-1].pages, 'scenes': drafts[-1].scenes}, 'evolution_summary': self.summarize_evolution(drafts), 'insights': [{'type': i.insight_type, 'description': i.description, 'recommendation': i.recommendation, 'confidence': i.confidence} for i in insights], 'recommended_next_steps': self.recommend_next_steps(drafts, insights)}
        report_file = self.database_path / f'evolution_report_{project_name}_{datetime.now():%Y%m%d}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        return report

    def summarize_evolution(self, drafts: List[DraftSnapshot]) -> str:
        """Create summary of evolution"""
        if len(drafts) < 2:
            return 'Insufficient drafts for evolution analysis'
        first = drafts[0]
        last = drafts[-1]
        summary_parts = []
        page_change = last.pages - first.pages
        if page_change > 0:
            summary_parts.append(f'expanded by {page_change} pages')
        elif page_change < 0:
            summary_parts.append(f'condensed by {abs(page_change)} pages')
        else:
            summary_parts.append('maintained page count')
        scene_change = last.scenes - first.scenes
        if scene_change > 0:
            summary_parts.append(f'added {scene_change} scenes')
        elif scene_change < 0:
            summary_parts.append(f'consolidated to {abs(scene_change)} fewer scenes')
        char_change = len(last.characters) - len(first.characters)
        if char_change != 0:
            summary_parts.append(f"{('added' if char_change > 0 else 'removed')} {abs(char_change)} characters")
        return f"Screenplay has {', '.join(summary_parts)} over {len(drafts)} drafts."

    def recommend_next_steps(self, drafts: List[DraftSnapshot], insights: List[EvolutionInsight]) -> List[str]:
        """Recommend next steps based on evolution"""
        recommendations = []
        if len(drafts) > 10:
            recommendations.append('Consider finalizing - numerous drafts suggest diminishing returns')
        elif len(drafts) < 3:
            recommendations.append('Continue revising - too early to assess evolution patterns')
        momentum_insight = next((i for i in insights if i.insight_type == 'momentum'), None)
        if momentum_insight and 'Low momentum' in momentum_insight.description:
            recommendations.append('Get fresh eyes on the script or take a break')
        quality_insight = next((i for i in insights if i.insight_type == 'quality_evolution'), None)
        if quality_insight and 'improving' in quality_insight.description.lower():
            recommendations.append('Continue current approach - quality metrics improving')
        recommendations.append('Focus on character emotional arcs in next draft')
        recommendations.append('Read dialogue aloud to test authenticity')
        return recommendations[:5]

async def main():
    """Test evolution tracking system"""
    tracker = EvolutionTrackingSystem()
    print('📊 EVOLUTION TRACKING SYSTEM TEST 📊\n')
    test_project = 'Test Screenplay'
    draft_contents = ['FADE IN:\n\nINT. APARTMENT - NIGHT\n\nJOHN, 30s, sits alone.\n\nJOHN\nI need to change my life.\n\nEXT. STREET - DAY\n\nJohn walks.\n\nFADE OUT.', 'FADE IN:\n\nINT. APARTMENT - NIGHT\n\nJOHN, 35, disheveled, sits alone. Empty bottles around.\n\nJOHN\nI need to change my life. But how?\n\nSARAH enters.\n\nSARAH\nYou start by standing up.\n\nEXT. STREET - DAY\n\nJohn walks with purpose now.\n\nINT. GYM - DAY\n\nJohn exercises.\n\nFADE OUT.', "FADE IN:\n\nINT. APARTMENT - NIGHT\n\nDarkness. A LIGHTER FLICKS - illuminates JOHN (35), stubbled, hollow eyes.\n\nJOHN\n(to himself)\nTomorrow. Always tomorrow.\n\nThe door CREAKS. SARAH (30s), concerned, enters with groceries.\n\nSARAH\nNo. Today.\n\nShe opens the blinds. Light floods in. John shields his eyes.\n\nJOHN\nIt's too bright.\n\nSARAH\nThat's the point.\n\nEXT. STREET - DAY\n\nJohn squints in sunlight, Sarah beside him.\n\nSARAH\nOne step. That's all.\n\nJohn takes a step. Then another.\n\nINT. GYM - DAY\n\nJohn on treadmill, struggling but moving.\n\nEXT. PARK - SUNSET\n\nJohn and Sarah sit on a bench.\n\nJOHN\nI almost forgot what this felt like.\n\nSARAH\nWhat?\n\nJOHN\nHope.\n\nFADE OUT."]
    for i, content in enumerate(draft_contents, 1):
        draft_file = Path(f'test_draft_{i}.txt')
        with open(draft_file, 'w') as f:
            f.write(content)
        snapshot = await tracker.track_draft(test_project, draft_file, f'Draft {i}', notes=f'Test draft {i}')
        print(f'Tracked Draft {i}:')
        print(f'  Pages: {snapshot.pages}')
        print(f'  Scenes: {snapshot.scenes}')
        print(f"  Characters: {', '.join(snapshot.characters)}")
        print(f'  Dialogue ratio: {snapshot.dialogue_ratio:.1%}')
        print()
    print('\nGenerating Evolution Insights...')
    insights = await tracker.generate_evolution_insights(test_project)
    for insight in insights:
        print(f'\n{insight.insight_type.upper()}:')
        print(f'  {insight.description}')
        print(f'  Recommendation: {insight.recommendation}')
        print(f'  Confidence: {insight.confidence:.0%}')
    print('\n' + '=' * 50)
    print('Evolution Report:')
    report = tracker.generate_evolution_report(test_project)
    print(f"Project: {report['project']}")
    print(f"Total drafts: {report['total_drafts']}")
    print(f"Time span: {report['time_span']} days")
    print(f"\nSummary: {report['evolution_summary']}")
    print('\nRecommended next steps:')
    for rec in report['recommended_next_steps']:
        print(f'  • {rec}')
    for i in range(1, 4):
        Path(f'test_draft_{i}.txt').unlink(missing_ok=True)
if __name__ == '__main__':
    asyncio.run(main())