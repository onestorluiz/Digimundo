#!/usr/bin/env python3
"""
Script Doctor Qualitymon - Overall Quality Specialist
Comprehensive quality assessment, holistic evaluation, excellence standards, professional polish.
"""

import re
import yaml
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import statistics


@dataclass
class QualityDimension:
    """Represents a dimension of screenplay quality."""
    dimension: str  # narrative, character, dialogue, etc.
    score: float  # 0.0 to 1.0
    strengths: List[str]
    weaknesses: List[str]
    specific_issues: List[Dict[str, Any]]


@dataclass
class QualityIndicator:
    """Represents a specific quality indicator."""
    category: str
    indicator: str
    present: bool
    strength: float
    location: List[int]  # scene numbers


@dataclass
class ProfessionalStandard:
    """Represents professional quality standards."""
    standard: str
    met: bool
    score: float
    details: str


@dataclass
class ExcellenceMarker:
    """Represents markers of excellence."""
    category: str
    description: str
    impact: float
    scenes: List[int]


@dataclass
class QualityAnalysis:
    """Complete quality analysis."""
    overall_quality: float
    quality_level: str  # amateur, developing, competent, professional, excellent, masterful
    narrative_quality: float
    character_quality: float
    dialogue_quality: float
    structural_quality: float
    emotional_quality: float
    visual_quality: float
    thematic_quality: float
    technical_quality: float
    entertainment_value: float
    production_viability: float


@dataclass
class OverallQualityResult:
    """Result from overall quality analysis."""
    specialist: Dict[str, str]
    score: int
    quality_analysis: QualityAnalysis
    quality_dimensions: List[QualityDimension]
    quality_indicators: List[QualityIndicator]
    professional_standards: List[ProfessionalStandard]
    excellence_markers: List[ExcellenceMarker]
    quality_map: Dict[str, float]  # Detailed quality breakdown
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]

    # Additional analysis
    readiness_score: float = 0.0  # Market readiness
    improvement_potential: float = 0.0
    standout_elements: List[str] = field(default_factory=list)
    critical_flaws: List[str] = field(default_factory=list)


class DrOverallQuality:
    """The Script Doctor™ Overall Quality Specialist."""

    def __init__(self):
        """Initialize the Overall Quality specialist."""
        self.name = "Script Doctor Qualitymon"
        self.specialty = "Comprehensive quality assessment, holistic evaluation, excellence standards, professional polish"

        # Load rules
        rules_path = Path(__file__).parent.parent / "rules" / "overall_quality_rules.yaml"
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)

        # Quality indicators
        self.quality_indicators = {
            'narrative': [
                'clear_premise', 'logical_progression', 'compelling_conflict',
                'satisfying_resolution', 'narrative_momentum', 'story_coherence'
            ],
            'character': [
                'distinct_voices', 'clear_motivations', 'character_arcs',
                'memorable_traits', 'authentic_behavior', 'emotional_depth'
            ],
            'dialogue': [
                'natural_flow', 'subtext', 'character_specific', 'advancing_plot',
                'revealing_character', 'memorable_lines'
            ],
            'structure': [
                'clear_acts', 'effective_setup', 'rising_action', 'climax_impact',
                'resolution_earned', 'scene_purpose'
            ],
            'technical': [
                'proper_format', 'clear_action', 'concise_description',
                'professional_presentation', 'readable_flow'
            ]
        }

        # Excellence markers
        self.excellence_indicators = {
            'memorable_opening': ['hooks', 'grabs', 'captivates', 'intrigues'],
            'powerful_climax': ['explosive', 'shocking', 'devastating', 'triumph'],
            'quotable_dialogue': ['iconic', 'memorable', 'brilliant', 'perfect'],
            'unforgettable_character': ['complex', 'layered', 'fascinating', 'unique'],
            'stunning_visual': ['breathtaking', 'spectacular', 'beautiful', 'striking'],
            'emotional_gutpunch': ['tears', 'devastating', 'heartbreaking', 'moving'],
            'brilliant_twist': ['unexpected', 'shocking', 'clever', 'brilliant']
        }

        # Quality thresholds
        self.quality_levels = {
            'masterful': 0.90,
            'excellent': 0.80,
            'professional': 0.70,
            'competent': 0.60,
            'developing': 0.50,
            'amateur': 0.0
        }

    def analyze(self, screenplay: str) -> OverallQualityResult:
        """Analyze overall quality of screenplay."""
        # Parse screenplay
        scenes = self._parse_scenes(screenplay)

        # Analyze quality dimensions
        quality_dimensions = self._analyze_quality_dimensions(scenes, screenplay)

        # Identify quality indicators
        quality_indicators = self._identify_quality_indicators(scenes)

        # Check professional standards
        professional_standards = self._check_professional_standards(
            scenes, screenplay, quality_dimensions
        )

        # Identify excellence markers
        excellence_markers = self._identify_excellence_markers(scenes)

        # Create quality map
        quality_map = self._create_quality_map(
            quality_dimensions, quality_indicators, professional_standards
        )

        # Calculate quality metrics
        quality_analysis = self._create_quality_analysis(
            quality_dimensions, quality_indicators, professional_standards,
            excellence_markers
        )

        # Identify standout elements and critical flaws
        standout_elements = self._identify_standout_elements(
            quality_dimensions, excellence_markers
        )
        critical_flaws = self._identify_critical_flaws(
            quality_dimensions, professional_standards
        )

        # Check rules
        rule_violations = self._check_rules(
            quality_analysis, quality_dimensions, professional_standards
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            quality_analysis, quality_dimensions, critical_flaws, rule_violations
        )

        # Calculate score
        score = self._calculate_score(quality_analysis, rule_violations)

        # Additional metrics
        readiness_score = self._calculate_readiness(quality_analysis, professional_standards)
        improvement_potential = self._calculate_improvement_potential(
            quality_analysis, quality_dimensions
        )

        return OverallQualityResult(
            specialist={
                'name': self.name,
                'specialty': self.specialty,
                'version': '1.0.0'
            },
            score=score,
            quality_analysis=quality_analysis,
            quality_dimensions=quality_dimensions,
            quality_indicators=quality_indicators,
            professional_standards=professional_standards,
            excellence_markers=excellence_markers,
            quality_map=quality_map,
            recommendations=recommendations,
            rule_violations=rule_violations,
            readiness_score=readiness_score,
            improvement_potential=improvement_potential,
            standout_elements=standout_elements,
            critical_flaws=critical_flaws
        )

    def _parse_scenes(self, screenplay: str) -> List[Dict[str, Any]]:
        """Parse screenplay into scenes."""
        scenes = []
        current_scene = None
        scene_num = 0

        for i, line in enumerate(screenplay.split('\n'), 1):
            line_stripped = line.strip()

            # Scene heading
            if re.match(r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)', line_stripped):
                if current_scene:
                    scenes.append(current_scene)
                scene_num += 1
                current_scene = {
                    'scene_num': scene_num,
                    'heading': line_stripped,
                    'dialogue': [],
                    'action': [],
                    'characters': set(),
                    'line_num': i,
                    'content_lines': 0
                }
            elif current_scene:
                # Character name (dialogue)
                if line_stripped.isupper() and len(line_stripped) > 0 and not line_stripped.startswith('('):
                    current_scene['characters'].add(line_stripped)
                    current_scene['dialogue'].append({
                        'character': line_stripped,
                        'line_num': i,
                        'text': ''
                    })
                # Dialogue
                elif current_scene['dialogue'] and not line_stripped.startswith('('):
                    if line_stripped:
                        current_scene['dialogue'][-1]['text'] += ' ' + line_stripped
                        current_scene['content_lines'] += 1
                # Action lines
                elif line_stripped and not line_stripped.startswith('('):
                    current_scene['action'].append({
                        'text': line_stripped,
                        'line_num': i
                    })
                    current_scene['content_lines'] += 1

        if current_scene:
            scenes.append(current_scene)

        return scenes

    def _analyze_quality_dimensions(self, scenes: List[Dict], screenplay: str) -> List[QualityDimension]:
        """Analyze different dimensions of quality."""
        dimensions = []

        # Narrative quality
        narrative_dim = self._assess_narrative_quality(scenes)
        dimensions.append(narrative_dim)

        # Character quality
        character_dim = self._assess_character_quality(scenes)
        dimensions.append(character_dim)

        # Dialogue quality
        dialogue_dim = self._assess_dialogue_quality(scenes)
        dimensions.append(dialogue_dim)

        # Structural quality
        structural_dim = self._assess_structural_quality(scenes)
        dimensions.append(structural_dim)

        # Emotional quality
        emotional_dim = self._assess_emotional_quality(scenes)
        dimensions.append(emotional_dim)

        # Visual quality
        visual_dim = self._assess_visual_quality(scenes)
        dimensions.append(visual_dim)

        # Thematic quality
        thematic_dim = self._assess_thematic_quality(scenes)
        dimensions.append(thematic_dim)

        # Technical quality
        technical_dim = self._assess_technical_quality(screenplay)
        dimensions.append(technical_dim)

        return dimensions

    def _assess_narrative_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess narrative quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5  # Base score

        # Check for clear setup (first 10% of scenes)
        setup_scenes = scenes[:max(1, len(scenes) // 10)]
        if setup_scenes:
            has_clear_setup = any(
                len(s['action']) > 3 or len(s['dialogue']) > 2
                for s in setup_scenes
            )
            if has_clear_setup:
                strengths.append("Clear story setup")
                score += 0.1
            else:
                weaknesses.append("Weak or unclear setup")
                issues.append({'issue': 'weak_setup', 'severity': 'high'})

        # Check for narrative momentum
        scene_lengths = [s['content_lines'] for s in scenes]
        if scene_lengths:
            avg_length = statistics.mean(scene_lengths)
            if 5 <= avg_length <= 20:
                strengths.append("Good narrative pacing")
                score += 0.15
            else:
                weaknesses.append("Pacing issues")
                issues.append({'issue': 'pacing_problems', 'severity': 'medium'})

        # Check for conflict presence
        conflict_scenes = 0
        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            if any(word in scene_text for word in
                  ['conflict', 'argue', 'fight', 'confront', 'challenge', 'oppose']):
                conflict_scenes += 1

        conflict_ratio = conflict_scenes / len(scenes) if scenes else 0
        if conflict_ratio >= 0.3:
            strengths.append("Strong conflict presence")
            score += 0.2
        else:
            weaknesses.append("Insufficient conflict")
            issues.append({'issue': 'weak_conflict', 'severity': 'high'})

        # Check for resolution
        if scenes:
            final_scenes = scenes[-max(1, len(scenes) // 10):]
            has_resolution = any(
                'resolve' in ' '.join(d['text'].lower() for d in s['dialogue'])
                or 'end' in s['heading'].lower()
                for s in final_scenes
            )
            if has_resolution or len(final_scenes[0]['action']) > 2:
                strengths.append("Clear resolution")
                score += 0.05
            else:
                weaknesses.append("Weak resolution")

        return QualityDimension(
            dimension='narrative',
            score=min(score, 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_character_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess character quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        # Count unique characters
        all_characters = set()
        for scene in scenes:
            all_characters.update(scene['characters'])

        if len(all_characters) >= 3:
            strengths.append(f"Good character variety ({len(all_characters)} characters)")
            score += 0.1
        else:
            weaknesses.append("Limited character variety")
            issues.append({'issue': 'few_characters', 'severity': 'medium'})

        # Check character presence distribution
        character_scenes = defaultdict(int)
        for scene in scenes:
            for char in scene['characters']:
                character_scenes[char] += 1

        # Check for protagonist (most present character)
        if character_scenes:
            protagonist = max(character_scenes.items(), key=lambda x: x[1])
            protagonist_presence = protagonist[1] / len(scenes)

            if protagonist_presence >= 0.5:
                strengths.append("Clear protagonist presence")
                score += 0.15
            else:
                weaknesses.append("Weak protagonist presence")
                issues.append({'issue': 'unclear_protagonist', 'severity': 'high'})

        # Check for character distinctiveness through dialogue
        character_dialogue = defaultdict(list)
        for scene in scenes:
            for dialogue in scene['dialogue']:
                character_dialogue[dialogue['character']].append(dialogue['text'])

        # Assess if characters have unique voices
        if len(character_dialogue) >= 2:
            dialogue_lengths = {
                char: statistics.mean([len(d.split()) for d in dialogues]) if dialogues else 0
                for char, dialogues in character_dialogue.items()
            }

            if dialogue_lengths:
                length_variance = statistics.variance(dialogue_lengths.values()) if len(dialogue_lengths) > 1 else 0
                if length_variance > 2:
                    strengths.append("Distinct character voices")
                    score += 0.2
                else:
                    weaknesses.append("Characters lack distinct voices")

        # Check for character development (dialogue evolution)
        for char, dialogues in character_dialogue.items():
            if len(dialogues) >= 3:
                # Simple check: does dialogue complexity change?
                early_dialogue = ' '.join(dialogues[:len(dialogues)//2])
                late_dialogue = ' '.join(dialogues[len(dialogues)//2:])

                if len(late_dialogue) > len(early_dialogue) * 1.2 or len(early_dialogue) > len(late_dialogue) * 1.2:
                    strengths.append("Character development evident")
                    score += 0.05
                    break

        return QualityDimension(
            dimension='character',
            score=min(score, 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_dialogue_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess dialogue quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        all_dialogue = []
        for scene in scenes:
            for dialogue in scene['dialogue']:
                if dialogue['text']:
                    all_dialogue.append(dialogue['text'])

        if not all_dialogue:
            weaknesses.append("Minimal dialogue")
            return QualityDimension(
                dimension='dialogue',
                score=0.3,
                strengths=strengths,
                weaknesses=weaknesses,
                specific_issues=[{'issue': 'no_dialogue', 'severity': 'high'}]
            )

        # Check dialogue length variety
        dialogue_lengths = [len(d.split()) for d in all_dialogue]
        if len(dialogue_lengths) > 1:
            length_variance = statistics.stdev(dialogue_lengths)
            if length_variance > 5:
                strengths.append("Good dialogue rhythm variety")
                score += 0.15
            else:
                weaknesses.append("Monotonous dialogue rhythm")

        # Check for subtext indicators
        subtext_indicators = ['...' , '—', 'pause', 'beat', 'silence']
        subtext_count = sum(1 for d in all_dialogue
                           if any(ind in d.lower() for ind in subtext_indicators))

        if subtext_count >= len(all_dialogue) * 0.1:
            strengths.append("Subtext and pauses present")
            score += 0.15

        # Check for natural speech patterns
        natural_patterns = ["I'm", "don't", "can't", "won't", "it's", "that's"]
        natural_count = sum(1 for d in all_dialogue
                           if any(pattern in d for pattern in natural_patterns))

        if natural_count >= len(all_dialogue) * 0.3:
            strengths.append("Natural speech patterns")
            score += 0.1
        else:
            weaknesses.append("Stilted or formal dialogue")
            issues.append({'issue': 'unnatural_dialogue', 'severity': 'medium'})

        # Check for overly long speeches
        long_speeches = [d for d in all_dialogue if len(d.split()) > 50]
        if len(long_speeches) > len(all_dialogue) * 0.2:
            weaknesses.append("Too many long speeches")
            issues.append({'issue': 'monologuing', 'severity': 'medium'})
            score -= 0.1

        # Check for memorable lines
        exclamations = sum(1 for d in all_dialogue if '!' in d or '?' in d)
        if exclamations >= len(all_dialogue) * 0.2:
            strengths.append("Dynamic dialogue with emotion")
            score += 0.1

        return QualityDimension(
            dimension='dialogue',
            score=min(max(score, 0), 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_structural_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess structural quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        if not scenes:
            return QualityDimension(
                dimension='structure',
                score=0.0,
                strengths=[],
                weaknesses=['No scenes'],
                specific_issues=[{'issue': 'no_structure', 'severity': 'critical'}]
            )

        # Check three-act structure
        total_scenes = len(scenes)
        act1_end = total_scenes // 4
        act2_end = (total_scenes * 3) // 4

        # Act 1 should establish
        act1_content = sum(s['content_lines'] for s in scenes[:act1_end])
        if act1_content > 0:
            strengths.append("Act 1 present")
            score += 0.15

        # Act 2 should develop
        if act2_end > act1_end:
            act2_content = sum(s['content_lines'] for s in scenes[act1_end:act2_end])
            if act2_content > act1_content:
                strengths.append("Strong Act 2 development")
                score += 0.2
            else:
                weaknesses.append("Weak second act")
                issues.append({'issue': 'weak_act2', 'severity': 'high'})

        # Act 3 should resolve
        act3_content = sum(s['content_lines'] for s in scenes[act2_end:])
        if act3_content > 0:
            strengths.append("Act 3 present")
            score += 0.15

        # Check scene progression
        scene_sizes = [s['content_lines'] for s in scenes]
        if len(scene_sizes) >= 3:
            # Check if scenes build
            first_third_avg = statistics.mean(scene_sizes[:len(scene_sizes)//3])
            last_third_avg = statistics.mean(scene_sizes[-len(scene_sizes)//3:])

            if last_third_avg > first_third_avg:
                strengths.append("Building momentum")
                score += 0.1

        # Check for scene variety
        location_variety = len(set(s['heading'].split('-')[0].strip() for s in scenes))
        if location_variety >= total_scenes * 0.3:
            strengths.append("Good location variety")
            score += 0.1
        else:
            weaknesses.append("Limited location variety")

        return QualityDimension(
            dimension='structure',
            score=min(score, 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_emotional_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess emotional quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        emotional_beats = 0
        emotion_words = ['love', 'hate', 'fear', 'anger', 'joy', 'sad', 'happy',
                        'tears', 'laugh', 'cry', 'heart', 'soul', 'pain', 'hope']

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            if any(word in scene_text for word in emotion_words):
                emotional_beats += 1

        emotional_density = emotional_beats / len(scenes) if scenes else 0

        if emotional_density >= 0.4:
            strengths.append("Strong emotional content")
            score += 0.3
        elif emotional_density >= 0.2:
            strengths.append("Adequate emotional content")
            score += 0.15
        else:
            weaknesses.append("Lacks emotional depth")
            issues.append({'issue': 'low_emotion', 'severity': 'medium'})

        # Check for emotional variety
        different_emotions = set()
        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            for emotion in ['love', 'fear', 'anger', 'joy', 'sadness']:
                if emotion in scene_text or any(related in scene_text
                                              for related in [emotion[:3], emotion + 's']):
                    different_emotions.add(emotion)

        if len(different_emotions) >= 3:
            strengths.append("Good emotional range")
            score += 0.2
        else:
            weaknesses.append("Limited emotional range")

        return QualityDimension(
            dimension='emotional',
            score=min(score, 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_visual_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess visual storytelling quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        visual_count = 0
        action_quality = 0

        for scene in scenes:
            # Check action line quality
            for action in scene['action']:
                text = action['text'].lower()

                # Visual verbs indicate good visual writing
                visual_verbs = ['sees', 'watches', 'reveals', 'discovers', 'appears',
                              'emerges', 'vanishes', 'transforms', 'explodes', 'crashes']

                if any(verb in text for verb in visual_verbs):
                    visual_count += 1

                # Check for specific visual details
                if len(text.split()) > 10 and any(word in text for word in ['color', 'light', 'shadow', 'dark']):
                    action_quality += 1

        if scenes:
            visual_density = visual_count / len(scenes)
            if visual_density >= 0.5:
                strengths.append("Strong visual storytelling")
                score += 0.25
            elif visual_density >= 0.25:
                strengths.append("Adequate visual elements")
                score += 0.15
            else:
                weaknesses.append("Weak visual storytelling")
                issues.append({'issue': 'lacks_visuals', 'severity': 'medium'})

        # Check for cinematic moments
        cinematic_words = ['slow motion', 'close-up', 'wide shot', 'reveal', 'pan', 'zoom']
        cinematic_moments = sum(1 for scene in scenes
                               for action in scene['action']
                               if any(word in action['text'].lower() for word in cinematic_words))

        if cinematic_moments >= 2:
            strengths.append("Cinematic awareness")
            score += 0.1

        # Balance of action vs dialogue
        total_action = sum(len(s['action']) for s in scenes)
        total_dialogue = sum(len(s['dialogue']) for s in scenes)

        if total_action + total_dialogue > 0:
            action_ratio = total_action / (total_action + total_dialogue)
            if 0.3 <= action_ratio <= 0.6:
                strengths.append("Good action/dialogue balance")
                score += 0.15
            else:
                weaknesses.append("Imbalanced action/dialogue ratio")

        return QualityDimension(
            dimension='visual',
            score=min(score, 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_thematic_quality(self, scenes: List[Dict]) -> QualityDimension:
        """Assess thematic quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        # Look for thematic keywords
        theme_categories = {
            'love': ['love', 'heart', 'romance', 'passion', 'affection'],
            'power': ['power', 'control', 'authority', 'dominate', 'rule'],
            'identity': ['identity', 'self', 'who am i', 'purpose', 'meaning'],
            'justice': ['justice', 'right', 'wrong', 'fair', 'moral'],
            'sacrifice': ['sacrifice', 'give up', 'cost', 'price', 'loss'],
            'redemption': ['redemption', 'forgive', 'second chance', 'atone'],
            'freedom': ['freedom', 'liberty', 'escape', 'prison', 'trapped']
        }

        themes_present = set()
        theme_depth = 0

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            for theme, keywords in theme_categories.items():
                if any(keyword in scene_text for keyword in keywords):
                    themes_present.add(theme)
                    theme_depth += 1

        if themes_present:
            if len(themes_present) == 1:
                strengths.append(f"Clear central theme: {list(themes_present)[0]}")
                score += 0.2
            elif len(themes_present) <= 3:
                strengths.append("Multiple complementary themes")
                score += 0.25
            else:
                weaknesses.append("Too many competing themes")
                issues.append({'issue': 'unfocused_themes', 'severity': 'medium'})

        if theme_depth >= len(scenes) * 0.3:
            strengths.append("Themes well-integrated")
            score += 0.25
        else:
            weaknesses.append("Themes underdeveloped")

        return QualityDimension(
            dimension='thematic',
            score=min(score, 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _assess_technical_quality(self, screenplay: str) -> QualityDimension:
        """Assess technical writing quality."""
        strengths = []
        weaknesses = []
        issues = []
        score = 0.5

        lines = screenplay.split('\n')

        # Check formatting
        has_fade_in = any('FADE IN' in line for line in lines[:5])
        has_fade_out = any('FADE OUT' in line for line in lines[-5:])

        if has_fade_in:
            strengths.append("Proper opening")
            score += 0.1
        else:
            weaknesses.append("Missing FADE IN")
            issues.append({'issue': 'missing_fade_in', 'severity': 'low'})

        if has_fade_out:
            strengths.append("Proper closing")
            score += 0.1
        else:
            weaknesses.append("Missing FADE OUT")
            issues.append({'issue': 'missing_fade_out', 'severity': 'low'})

        # Check scene heading format
        scene_headings = [line for line in lines
                         if re.match(r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)', line.strip())]

        if scene_headings:
            proper_headings = sum(1 for h in scene_headings
                                 if ' - ' in h and any(time in h.upper()
                                                      for time in ['DAY', 'NIGHT', 'MORNING', 'EVENING', 'CONTINUOUS']))
            if proper_headings >= len(scene_headings) * 0.8:
                strengths.append("Proper scene headings")
                score += 0.15
            else:
                weaknesses.append("Inconsistent scene headings")
                issues.append({'issue': 'formatting_issues', 'severity': 'medium'})

        # Check for overly long action blocks
        current_block = []
        long_blocks = 0
        for line in lines:
            if line.strip() and not line.strip().isupper():
                current_block.append(line)
            else:
                if len(current_block) > 4:
                    long_blocks += 1
                current_block = []

        if long_blocks > 3:
            weaknesses.append("Overly long action blocks")
            issues.append({'issue': 'dense_action_blocks', 'severity': 'medium'})
            score -= 0.1

        # Check line length
        long_lines = sum(1 for line in lines if len(line) > 80)
        if long_lines < len(lines) * 0.1:
            strengths.append("Good line length control")
            score += 0.1

        # Check for proper character name formatting
        character_names = [line.strip() for line in lines
                          if line.strip().isupper() and len(line.strip()) > 1
                          and not line.strip().startswith('(')]
        if character_names:
            strengths.append("Clear character names")
            score += 0.05

        return QualityDimension(
            dimension='technical',
            score=min(max(score, 0), 1.0),
            strengths=strengths,
            weaknesses=weaknesses,
            specific_issues=issues
        )

    def _identify_quality_indicators(self, scenes: List[Dict]) -> List[QualityIndicator]:
        """Identify specific quality indicators."""
        indicators = []

        for category, indicator_list in self.quality_indicators.items():
            for indicator_name in indicator_list:
                present, strength, locations = self._check_indicator(
                    scenes, category, indicator_name
                )

                if present:
                    indicators.append(QualityIndicator(
                        category=category,
                        indicator=indicator_name,
                        present=present,
                        strength=strength,
                        location=locations
                    ))

        return indicators

    def _check_indicator(self, scenes: List[Dict], category: str,
                        indicator: str) -> Tuple[bool, float, List[int]]:
        """Check for specific quality indicator."""
        locations = []
        strength = 0.0

        if category == 'narrative' and indicator == 'clear_premise':
            # Check first few scenes for premise establishment
            if scenes[:3]:
                setup_content = sum(s['content_lines'] for s in scenes[:3])
                if setup_content > 10:
                    return True, 0.8, [1, 2, 3]

        elif category == 'character' and indicator == 'distinct_voices':
            # Check for character voice variety
            character_dialogue = defaultdict(list)
            for scene in scenes:
                for dialogue in scene['dialogue']:
                    character_dialogue[dialogue['character']].append(dialogue['text'])

            if len(character_dialogue) >= 2:
                # Simple distinctiveness check
                avg_lengths = {char: statistics.mean([len(d.split()) for d in dialogues]) if dialogues else 0
                             for char, dialogues in character_dialogue.items()}
                if avg_lengths and max(avg_lengths.values()) > min(avg_lengths.values()) * 1.5:
                    return True, 0.7, list(range(1, min(6, len(scenes) + 1)))

        elif category == 'dialogue' and indicator == 'natural_flow':
            # Check for natural speech patterns
            natural_count = 0
            for i, scene in enumerate(scenes):
                for dialogue in scene['dialogue']:
                    if any(pattern in dialogue['text']
                          for pattern in ["I'm", "don't", "can't", "it's"]):
                        natural_count += 1
                        locations.append(i + 1)

            if natural_count >= 3:
                return True, min(natural_count * 0.15, 1.0), locations[:5]

        elif category == 'structure' and indicator == 'clear_acts':
            # Basic three-act check
            if len(scenes) >= 10:
                return True, 0.6, [1, len(scenes)//2, len(scenes)]

        return False, 0.0, []

    def _check_professional_standards(self, scenes: List[Dict], screenplay: str,
                                     quality_dimensions: List[QualityDimension]) -> List[ProfessionalStandard]:
        """Check against professional standards."""
        standards = []

        # Format standard
        format_quality = next((d.score for d in quality_dimensions if d.dimension == 'technical'), 0.5)
        standards.append(ProfessionalStandard(
            standard='Professional Formatting',
            met=format_quality >= 0.6,
            score=format_quality,
            details='Screenplay follows industry format standards'
        ))

        # Length standard (assuming proper page count)
        total_lines = len(screenplay.split('\n'))
        appropriate_length = 90 <= total_lines <= 3000  # Rough approximation
        standards.append(ProfessionalStandard(
            standard='Appropriate Length',
            met=appropriate_length,
            score=1.0 if appropriate_length else 0.3,
            details='Screenplay length within industry norms'
        ))

        # Dialogue standard
        dialogue_quality = next((d.score for d in quality_dimensions if d.dimension == 'dialogue'), 0.5)
        standards.append(ProfessionalStandard(
            standard='Professional Dialogue',
            met=dialogue_quality >= 0.6,
            score=dialogue_quality,
            details='Dialogue meets professional standards'
        ))

        # Structure standard
        structure_quality = next((d.score for d in quality_dimensions if d.dimension == 'structure'), 0.5)
        standards.append(ProfessionalStandard(
            standard='Sound Structure',
            met=structure_quality >= 0.6,
            score=structure_quality,
            details='Story structure professionally crafted'
        ))

        # Character standard
        character_quality = next((d.score for d in quality_dimensions if d.dimension == 'character'), 0.5)
        standards.append(ProfessionalStandard(
            standard='Compelling Characters',
            met=character_quality >= 0.6,
            score=character_quality,
            details='Characters meet professional standards'
        ))

        return standards

    def _identify_excellence_markers(self, scenes: List[Dict]) -> List[ExcellenceMarker]:
        """Identify markers of excellence."""
        markers = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            for marker_type, keywords in self.excellence_indicators.items():
                if any(keyword in scene_text for keyword in keywords):
                    markers.append(ExcellenceMarker(
                        category=marker_type,
                        description=f"Potential {marker_type.replace('_', ' ')} in scene {scene['scene_num']}",
                        impact=0.7,
                        scenes=[scene['scene_num']]
                    ))

        # Check for exceptional dialogue
        for scene in scenes:
            for dialogue in scene['dialogue']:
                if dialogue['text'] and (
                    '!' in dialogue['text'] and '?' in dialogue['text'] or
                    len(dialogue['text'].split()) > 30
                ):
                    markers.append(ExcellenceMarker(
                        category='memorable_dialogue',
                        description=f"Potentially memorable dialogue",
                        impact=0.6,
                        scenes=[scene['scene_num']]
                    ))
                    break

        return markers

    def _create_quality_map(self, dimensions: List[QualityDimension],
                           indicators: List[QualityIndicator],
                           standards: List[ProfessionalStandard]) -> Dict[str, float]:
        """Create detailed quality breakdown."""
        quality_map = {}

        # Add dimension scores
        for dim in dimensions:
            quality_map[f"{dim.dimension}_quality"] = dim.score

        # Add indicator strengths
        for ind in indicators:
            quality_map[f"{ind.category}_{ind.indicator}"] = ind.strength

        # Add standard scores
        for std in standards:
            quality_map[std.standard.lower().replace(' ', '_')] = std.score

        return quality_map

    def _create_quality_analysis(self, dimensions: List[QualityDimension],
                                indicators: List[QualityIndicator],
                                standards: List[ProfessionalStandard],
                                markers: List[ExcellenceMarker]) -> QualityAnalysis:
        """Create comprehensive quality analysis."""
        # Extract dimension scores
        dim_scores = {d.dimension: d.score for d in dimensions}

        # Calculate overall quality
        overall_quality = statistics.mean(dim_scores.values()) if dim_scores else 0.5

        # Adjust for excellence markers
        if markers:
            excellence_bonus = min(len(markers) * 0.02, 0.1)
            overall_quality = min(overall_quality + excellence_bonus, 1.0)

        # Determine quality level
        quality_level = 'amateur'
        for level, threshold in sorted(self.quality_levels.items(), key=lambda x: x[1], reverse=True):
            if overall_quality >= threshold:
                quality_level = level
                break

        # Calculate entertainment value
        entertainment_value = self._calculate_entertainment_value(dimensions, indicators)

        # Calculate production viability
        production_viability = self._calculate_production_viability(dimensions, standards)

        return QualityAnalysis(
            overall_quality=overall_quality,
            quality_level=quality_level,
            narrative_quality=dim_scores.get('narrative', 0.5),
            character_quality=dim_scores.get('character', 0.5),
            dialogue_quality=dim_scores.get('dialogue', 0.5),
            structural_quality=dim_scores.get('structure', 0.5),
            emotional_quality=dim_scores.get('emotional', 0.5),
            visual_quality=dim_scores.get('visual', 0.5),
            thematic_quality=dim_scores.get('thematic', 0.5),
            technical_quality=dim_scores.get('technical', 0.5),
            entertainment_value=entertainment_value,
            production_viability=production_viability
        )

    def _calculate_entertainment_value(self, dimensions: List[QualityDimension],
                                      indicators: List[QualityIndicator]) -> float:
        """Calculate entertainment value."""
        value = 0.5

        # Strong narrative adds entertainment
        narrative_dim = next((d for d in dimensions if d.dimension == 'narrative'), None)
        if narrative_dim:
            value += narrative_dim.score * 0.2

        # Emotional engagement
        emotional_dim = next((d for d in dimensions if d.dimension == 'emotional'), None)
        if emotional_dim:
            value += emotional_dim.score * 0.2

        # Visual excitement
        visual_dim = next((d for d in dimensions if d.dimension == 'visual'), None)
        if visual_dim:
            value += visual_dim.score * 0.1

        return min(value, 1.0)

    def _calculate_production_viability(self, dimensions: List[QualityDimension],
                                       standards: List[ProfessionalStandard]) -> float:
        """Calculate production viability."""
        viability = 0.5

        # Technical quality affects production
        technical_dim = next((d for d in dimensions if d.dimension == 'technical'), None)
        if technical_dim:
            viability += technical_dim.score * 0.2

        # Professional standards
        standards_met = sum(1 for s in standards if s.met)
        viability += (standards_met / len(standards)) * 0.3 if standards else 0

        return min(viability, 1.0)

    def _identify_standout_elements(self, dimensions: List[QualityDimension],
                                   markers: List[ExcellenceMarker]) -> List[str]:
        """Identify standout elements."""
        standouts = []

        # Check dimensions for strengths
        for dim in dimensions:
            if dim.score >= 0.8:
                standouts.append(f"Exceptional {dim.dimension} quality")
            elif dim.score >= 0.7 and dim.strengths:
                standouts.append(f"Strong {dim.dimension}: {dim.strengths[0]}")

        # Add excellence markers
        for marker in markers[:3]:  # Top 3
            standouts.append(marker.description)

        return standouts[:5]  # Return top 5

    def _identify_critical_flaws(self, dimensions: List[QualityDimension],
                                standards: List[ProfessionalStandard]) -> List[str]:
        """Identify critical flaws."""
        flaws = []

        # Check dimensions for critical weaknesses
        for dim in dimensions:
            if dim.score < 0.3:
                flaws.append(f"Critical weakness: {dim.dimension}")
            elif dim.score < 0.5 and dim.specific_issues:
                for issue in dim.specific_issues:
                    if issue.get('severity') in ['critical', 'high']:
                        flaws.append(f"{dim.dimension}: {issue['issue']}")

        # Check standards
        critical_standards = ['Professional Formatting', 'Sound Structure']
        for std in standards:
            if std.standard in critical_standards and not std.met:
                flaws.append(f"Fails {std.standard}")

        return flaws[:5]  # Return top 5

    def _check_rules(self, analysis: QualityAnalysis, dimensions: List[QualityDimension],
                    standards: List[ProfessionalStandard]) -> List[Dict[str, Any]]:
        """Check screenplay against quality rules."""
        violations = []

        for rule in self.rules_config['rules']:
            violation = self._check_single_rule(rule, analysis, dimensions, standards)
            if violation:
                violations.append(violation)

        return violations

    def _check_single_rule(self, rule: Dict, analysis: QualityAnalysis,
                          dimensions: List[QualityDimension],
                          standards: List[ProfessionalStandard]) -> Optional[Dict]:
        """Check a single rule."""
        passed = True
        details = ""

        rule_id = rule['id']

        if rule_id == 'QUA.R001':  # Professional Standard
            prof_standards_met = sum(1 for s in standards if s.met) / len(standards) if standards else 0
            passed = prof_standards_met >= 0.6
            details = f"Standards met: {prof_standards_met:.2f}"

        elif rule_id == 'QUA.R002':  # Narrative Coherence
            passed = analysis.narrative_quality >= 0.6
            details = f"Narrative quality: {analysis.narrative_quality:.2f}"

        elif rule_id == 'QUA.R003':  # Character Excellence
            passed = analysis.character_quality >= 0.6
            details = f"Character quality: {analysis.character_quality:.2f}"

        elif rule_id == 'QUA.R004':  # Dialogue Quality
            passed = analysis.dialogue_quality >= 0.6
            details = f"Dialogue quality: {analysis.dialogue_quality:.2f}"

        elif rule_id == 'QUA.R005':  # Pacing Excellence
            passed = analysis.structural_quality >= 0.6
            details = f"Structural quality: {analysis.structural_quality:.2f}"

        elif rule_id == 'QUA.R006':  # Emotional Impact
            passed = analysis.emotional_quality >= 0.6
            details = f"Emotional quality: {analysis.emotional_quality:.2f}"

        elif rule_id == 'QUA.R007':  # Visual Storytelling
            passed = analysis.visual_quality >= 0.5
            details = f"Visual quality: {analysis.visual_quality:.2f}"

        elif rule_id == 'QUA.R008':  # Thematic Depth
            passed = analysis.thematic_quality >= 0.5
            details = f"Thematic quality: {analysis.thematic_quality:.2f}"

        elif rule_id == 'QUA.R009':  # Technical Proficiency
            passed = analysis.technical_quality >= 0.6
            details = f"Technical quality: {analysis.technical_quality:.2f}"

        elif rule_id == 'QUA.R011':  # Entertainment Value
            passed = analysis.entertainment_value >= 0.6
            details = f"Entertainment value: {analysis.entertainment_value:.2f}"

        elif rule_id == 'QUA.R015':  # Overall Excellence
            passed = analysis.overall_quality >= 0.75
            details = f"Overall quality: {analysis.overall_quality:.2f}"

        if not passed:
            return {
                'rule_id': rule_id,
                'title': rule['title'],
                'severity': rule['severity'],
                'category': rule['category'],
                'message': rule['fail_msg'],
                'details': details,
                'fix': rule['fix']
            }

        return None

    def _generate_recommendations(self, analysis: QualityAnalysis,
                                 dimensions: List[QualityDimension],
                                 critical_flaws: List[str],
                                 violations: List[Dict]) -> List[str]:
        """Generate recommendations for quality improvement."""
        recommendations = []

        # Address critical flaws first
        if critical_flaws:
            recommendations.append(f"Priority: Fix {critical_flaws[0]}")

        # Address lowest scoring dimensions
        dim_scores = [(d.dimension, d.score) for d in dimensions]
        dim_scores.sort(key=lambda x: x[1])

        for dim, score in dim_scores[:2]:
            if score < 0.6:
                if dim == 'narrative':
                    recommendations.append("Strengthen story structure and conflict")
                elif dim == 'character':
                    recommendations.append("Develop more compelling characters with clear arcs")
                elif dim == 'dialogue':
                    recommendations.append("Polish dialogue for authenticity and impact")
                elif dim == 'structure':
                    recommendations.append("Refine pacing and structural progression")
                elif dim == 'emotional':
                    recommendations.append("Deepen emotional resonance and character connections")
                elif dim == 'visual':
                    recommendations.append("Enhance visual storytelling and cinematic moments")

        # Address quality level
        if analysis.quality_level in ['amateur', 'developing']:
            recommendations.append("Focus on fundamentals: clear story, strong characters, natural dialogue")
        elif analysis.quality_level == 'competent':
            recommendations.append("Polish for professional quality: refine all elements")
        elif analysis.quality_level == 'professional':
            recommendations.append("Add distinctive elements to elevate to excellence")

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            recommendations.append(f"Critical: {critical_violations[0]['fix']}")

        return recommendations[:6]  # Top 6 recommendations

    def _calculate_score(self, analysis: QualityAnalysis, violations: List[Dict]) -> int:
        """Calculate overall quality score."""
        # Base score from overall quality
        score = int(analysis.overall_quality * 100)

        # Deduct for violations
        severity_penalties = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 2
        }

        for violation in violations:
            score -= severity_penalties.get(violation['severity'], 5)

        # Bonus for excellence
        if analysis.quality_level == 'excellent':
            score += 5
        elif analysis.quality_level == 'masterful':
            score += 10

        return max(0, min(100, score))

    def _calculate_readiness(self, analysis: QualityAnalysis,
                           standards: List[ProfessionalStandard]) -> float:
        """Calculate market readiness."""
        readiness = 0.0

        # Base on overall quality
        readiness += analysis.overall_quality * 0.4

        # Professional standards
        standards_met = sum(1 for s in standards if s.met) / len(standards) if standards else 0
        readiness += standards_met * 0.3

        # Entertainment and production
        readiness += analysis.entertainment_value * 0.15
        readiness += analysis.production_viability * 0.15

        return min(readiness, 1.0)

    def _calculate_improvement_potential(self, analysis: QualityAnalysis,
                                        dimensions: List[QualityDimension]) -> float:
        """Calculate improvement potential."""
        # Lower quality = higher improvement potential
        base_potential = 1.0 - analysis.overall_quality

        # Check for specific weaknesses that can be improved
        improvable = 0
        for dim in dimensions:
            if 0.3 <= dim.score <= 0.6:  # In improvable range
                improvable += 1

        potential = base_potential * 0.5 + (improvable / len(dimensions)) * 0.5 if dimensions else base_potential

        return min(potential, 1.0)