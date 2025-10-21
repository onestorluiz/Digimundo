#!/usr/bin/env python3
"""
Script Doctor Metamon - Originality Assessment Specialist
Analyzes creative uniqueness, fresh perspectives, innovation detection, and derivative analysis.
"""

import re
import yaml
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import hashlib


@dataclass
class OriginalElement:
    """Represents an original element in the screenplay."""
    element_type: str  # concept, plot, character, dialogue, etc.
    description: str
    uniqueness_score: float  # 0.0 to 1.0
    scene_num: int
    context: str
    line_num: int


@dataclass
class DerivativeElement:
    """Represents a potentially derivative element."""
    element_type: str
    description: str
    similarity_to: str  # what it's similar to
    derivative_score: float  # 0.0 to 1.0
    scene_num: int
    line_num: int


@dataclass
class InnovationPoint:
    """Represents a point of innovation."""
    innovation_type: str  # structural, narrative, character, etc.
    description: str
    impact_score: float
    scenes: List[int]


@dataclass
class TropeUsage:
    """Represents usage of a common trope."""
    trope_name: str
    usage_type: str  # played_straight, subverted, deconstructed, avoided
    occurrences: List[int]
    freshness_score: float


@dataclass
class OriginalityAnalysis:
    """Complete originality analysis."""
    overall_originality: float
    concept_uniqueness: float
    plot_innovation: float
    character_originality: float
    dialogue_freshness: float
    theme_innovation: float
    structural_innovation: float
    genre_subversion: float
    world_uniqueness: float
    resolution_surprise: float


@dataclass
class OriginalityAssessmentResult:
    """Result from originality assessment analysis."""
    specialist: Dict[str, str]
    score: int
    originality_analysis: OriginalityAnalysis
    original_elements: List[OriginalElement]
    derivative_elements: List[DerivativeElement]
    innovation_points: List[InnovationPoint]
    trope_usage: List[TropeUsage]
    uniqueness_map: Dict[str, float]  # scene-by-scene uniqueness
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]

    # Additional analysis
    creative_risk_score: float = 0.0
    commercial_viability: float = 0.0
    genre_innovation: float = 0.0
    fingerprint: str = ""  # Unique screenplay fingerprint


class DrOriginalityAssessment:
    """The Script Doctor™ Originality Assessment Specialist."""

    def __init__(self):
        """Initialize the Originality Assessment specialist."""
        self.name = "Script Doctor Metamon"
        self.specialty = "Creative uniqueness, fresh perspectives, innovation detection, derivative analysis"

        # Load rules
        rules_path = Path(__file__).parent.parent / "rules" / "originality_assessment_rules.yaml"
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)

        # Common tropes database
        self.common_tropes = {
            'hero_journey': ['ordinary world', 'call to adventure', 'mentor', 'threshold'],
            'love_triangle': ['torn between', 'choose between', 'two suitors'],
            'chosen_one': ['prophecy', 'destiny', 'special powers', 'only one who can'],
            'redemption_arc': ['seeks redemption', 'atone', 'make amends', 'second chance'],
            'fish_out_water': ['new world', 'doesn\'t fit', 'culture clash', 'outsider'],
            'mentor_death': ['mentor dies', 'teacher sacrifices', 'guide killed'],
            'false_death': ['appears dead', 'thought dead', 'comes back', 'resurrects'],
            'macguffin': ['everyone wants', 'object of desire', 'mysterious item'],
            'ticking_clock': ['time running out', 'countdown', 'deadline', 'before it\'s too late'],
            'amnesia': ['lost memory', 'can\'t remember', 'forgotten past', 'amnesia']
        }

        # Cliché database
        self.cliches = {
            'dialogue': [
                'we\'re not so different',
                'this is just the beginning',
                'there\'s no time to explain',
                'it\'s quiet... too quiet',
                'we\'ve got company',
                'i\'ve got a bad feeling about this',
                'you just don\'t get it',
                'this time it\'s personal',
                'i\'m getting too old for this',
                'with great power'
            ],
            'plot': [
                'it was all a dream',
                'evil twin',
                'fake death',
                'chosen one prophecy',
                'love at first sight',
                'misunderstanding that could be solved with one conversation',
                'villain monologue',
                'hero walks away from explosion'
            ],
            'character': [
                'brooding antihero',
                'manic pixie dream girl',
                'wise old mentor',
                'comic relief sidekick',
                'evil for evil\'s sake villain',
                'perfect mary sue',
                'bumbling dad',
                'ice queen who needs to be melted'
            ]
        }

        # Innovation indicators
        self.innovation_markers = {
            'structural': ['non-linear', 'reverse chronology', 'parallel narratives',
                          'nested stories', 'unreliable narrator'],
            'narrative': ['subverted expectations', 'genre blend', 'meta-commentary',
                         'breaking fourth wall', 'ambiguous ending'],
            'character': ['complex morality', 'unconventional protagonist', 'role reversal',
                         'against type', 'unexpected alliance'],
            'thematic': ['fresh perspective', 'contemporary relevance', 'philosophical depth',
                        'social commentary', 'universal truth in new way'],
            'visual': ['unique imagery', 'symbolic visuals', 'innovative action',
                      'distinctive style', 'memorable set pieces']
        }

    def analyze(self, screenplay: str) -> Dict[str, Any]:
        """Analyze originality in screenplay."""
        # Parse screenplay
        scenes = self._parse_scenes(screenplay)

        # Identify original elements
        original_elements = self._identify_original_elements(scenes)

        # Identify derivative elements
        derivative_elements = self._identify_derivative_elements(scenes)

        # Detect innovation points
        innovation_points = self._detect_innovation_points(scenes)

        # Analyze trope usage
        trope_usage = self._analyze_trope_usage(scenes)

        # Create uniqueness map
        uniqueness_map = self._create_uniqueness_map(scenes, original_elements, derivative_elements)

        # Calculate originality metrics
        originality_analysis = self._create_originality_analysis(
            original_elements, derivative_elements, innovation_points,
            trope_usage, scenes
        )

        # Generate screenplay fingerprint
        fingerprint = self._generate_fingerprint(screenplay, originality_analysis)

        # Check rules
        rule_violations = self._check_rules(
            originality_analysis, original_elements, derivative_elements
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            originality_analysis, derivative_elements, trope_usage, rule_violations
        )

        # Calculate score
        score = self._calculate_score(originality_analysis, rule_violations)

        # Additional metrics
        creative_risk_score = self._calculate_creative_risk(
            innovation_points, originality_analysis
        )
        commercial_viability = self._calculate_commercial_viability(
            originality_analysis, trope_usage
        )
        genre_innovation = self._calculate_genre_innovation(
            innovation_points, trope_usage
        )

        # Convert nested dataclasses to dicts
        original_elements_dict = [
            {
                'element_type': elem.element_type,
                'description': elem.description,
                'uniqueness_score': elem.uniqueness_score,
                'scene_num': elem.scene_num,
                'context': elem.context,
                'line_num': elem.line_num
            } for elem in original_elements
        ]

        derivative_elements_dict = [
            {
                'element_type': elem.element_type,
                'description': elem.description,
                'similarity_to': elem.similarity_to,
                'derivative_score': elem.derivative_score,
                'scene_num': elem.scene_num,
                'line_num': elem.line_num
            } for elem in derivative_elements
        ]

        innovation_points_dict = [
            {
                'innovation_type': point.innovation_type,
                'description': point.description,
                'impact_score': point.impact_score,
                'scenes': point.scenes
            } for point in innovation_points
        ]

        trope_usage_dict = [
            {
                'trope_name': trope.trope_name,
                'usage_type': trope.usage_type,
                'occurrences': trope.occurrences,
                'freshness_score': trope.freshness_score
            } for trope in trope_usage
        ]

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, originality_analysis, original_elements, derivative_elements)

        # Return dict instead of dataclass
        return {
            'specialist': {
                'name': self.name,
                'specialty': self.specialty,
                'version': '1.0.0'
            },
            'score': score,
            # Flatten OriginalityAnalysis fields
            'overall_originality': originality_analysis.overall_originality,
            'concept_uniqueness': originality_analysis.concept_uniqueness,
            'plot_innovation': originality_analysis.plot_innovation,
            'character_originality': originality_analysis.character_originality,
            'dialogue_freshness': originality_analysis.dialogue_freshness,
            'theme_innovation': originality_analysis.theme_innovation,
            'structural_innovation': originality_analysis.structural_innovation,
            'genre_subversion': originality_analysis.genre_subversion,
            'world_uniqueness': originality_analysis.world_uniqueness,
            'resolution_surprise': originality_analysis.resolution_surprise,
            # Converted lists
            'original_elements': original_elements_dict,
            'derivative_elements': derivative_elements_dict,
            'innovation_points': innovation_points_dict,
            'trope_usage': trope_usage_dict,
            'uniqueness_map': uniqueness_map,
            'recommendations': recommendations,
            'rule_violations': rule_violations,
            'creative_risk_score': creative_risk_score,
            'commercial_viability': commercial_viability,
            'genre_innovation': genre_innovation,
            'fingerprint': fingerprint,
            'diagnosis': diagnosis,
            'signature': f"Diagnosed by {self.name}™"
        }

    def _generate_diagnosis(self, score: int, analysis: OriginalityAnalysis,
                          original_elements: List[OriginalElement],
                          derivative_elements: List[DerivativeElement]) -> str:
        """Generate diagnosis based on originality analysis."""
        diagnosis_parts = []

        if score >= 85:
            diagnosis_parts.append("✅ EXCELLENT originality - highly creative and fresh")
        elif score >= 70:
            diagnosis_parts.append("👍 GOOD originality with some unique elements")
        elif score >= 50:
            diagnosis_parts.append("⚠️  MODERATE originality - mix of fresh and familiar")
        else:
            diagnosis_parts.append("❌ LOW originality - heavily derivative")

        # Highlight strengths
        if analysis.concept_uniqueness > 0.7:
            diagnosis_parts.append(f"Strong concept uniqueness ({analysis.concept_uniqueness:.2f})")
        if analysis.plot_innovation > 0.7:
            diagnosis_parts.append(f"Innovative plot structure ({analysis.plot_innovation:.2f})")
        if analysis.character_originality > 0.7:
            diagnosis_parts.append(f"Original characters ({analysis.character_originality:.2f})")

        # Highlight weaknesses
        if analysis.overall_originality < 0.4:
            diagnosis_parts.append(f"Overall originality low ({analysis.overall_originality:.2f})")
        if len(derivative_elements) > 10:
            diagnosis_parts.append(f"{len(derivative_elements)} derivative elements detected")
        if len(original_elements) < 5:
            diagnosis_parts.append(f"Only {len(original_elements)} original elements found")

        return " ".join(diagnosis_parts)

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
                    'line_num': i
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
                # Action lines
                elif line_stripped and not line_stripped.startswith('('):
                    current_scene['action'].append({
                        'text': line_stripped,
                        'line_num': i
                    })

        if current_scene:
            scenes.append(current_scene)

        return scenes

    def _identify_original_elements(self, scenes: List[Dict]) -> List[OriginalElement]:
        """Identify original elements in screenplay."""
        original_elements = []

        for scene in scenes:
            # Check for unique dialogue patterns
            for dialogue in scene['dialogue']:
                uniqueness = self._assess_dialogue_uniqueness(dialogue['text'])
                if uniqueness > 0.6:
                    original_elements.append(OriginalElement(
                        element_type='dialogue',
                        description=dialogue['text'][:100],
                        uniqueness_score=uniqueness,
                        scene_num=scene['scene_num'],
                        context='character_voice',
                        line_num=dialogue['line_num']
                    ))

            # Check for unique action/visual elements
            for action in scene['action']:
                uniqueness = self._assess_action_uniqueness(action['text'])
                if uniqueness > 0.6:
                    original_elements.append(OriginalElement(
                        element_type='visual',
                        description=action['text'][:100],
                        uniqueness_score=uniqueness,
                        scene_num=scene['scene_num'],
                        context='action',
                        line_num=action['line_num']
                    ))

            # Check for unique scene concepts
            scene_uniqueness = self._assess_scene_uniqueness(scene)
            if scene_uniqueness > 0.7:
                original_elements.append(OriginalElement(
                    element_type='concept',
                    description=f"Scene concept: {scene['heading']}",
                    uniqueness_score=scene_uniqueness,
                    scene_num=scene['scene_num'],
                    context='scene',
                    line_num=scene['line_num']
                ))

        return original_elements

    def _assess_dialogue_uniqueness(self, text: str) -> float:
        """Assess uniqueness of dialogue."""
        if not text:
            return 0.0

        text_lower = text.lower()

        # Check against clichés
        cliche_count = sum(1 for cliche in self.cliches['dialogue']
                          if cliche in text_lower)

        if cliche_count > 0:
            return max(0.0, 0.5 - cliche_count * 0.2)

        # Check for unique phrasing
        unique_indicators = [
            len(text.split()) > 20,  # Longer, more complex dialogue
            '...' in text or '—' in text,  # Interrupted or trailing speech
            any(char in text for char in ['?', '!']) and len(text) > 10,  # Emotional complexity
            bool(re.search(r'[A-Z]{2,}', text)),  # Emphasis or shouting with nuance
        ]

        uniqueness = 0.5 + sum(unique_indicators) * 0.125
        return min(uniqueness, 1.0)

    def _assess_action_uniqueness(self, text: str) -> float:
        """Assess uniqueness of action lines."""
        if not text:
            return 0.0

        text_lower = text.lower()

        # Check for cliché actions
        cliche_actions = ['walks away from explosion', 'slow motion', 'rain at funeral',
                         'looking in mirror', 'wakes up screaming']

        if any(cliche in text_lower for cliche in cliche_actions):
            return 0.3

        # Check for unique descriptors
        unique_words = ['unusual', 'bizarre', 'surreal', 'unexpected', 'strange',
                       'peculiar', 'extraordinary', 'remarkable']

        unique_score = sum(1 for word in unique_words if word in text_lower) * 0.2

        # Check for specific, detailed description
        if len(text.split()) > 15 and ',' in text:
            unique_score += 0.3

        return min(0.5 + unique_score, 1.0)

    def _assess_scene_uniqueness(self, scene: Dict) -> float:
        """Assess overall scene uniqueness."""
        uniqueness = 0.5

        # Unique location
        common_locations = ['apartment', 'office', 'car', 'restaurant', 'bedroom',
                           'kitchen', 'street', 'park', 'bar', 'hospital']

        location = scene['heading'].lower()
        if not any(loc in location for loc in common_locations):
            uniqueness += 0.2

        # Unique character combination
        if len(scene['characters']) >= 4:  # Many character scene
            uniqueness += 0.1

        # Unique time setting
        if any(time in scene['heading'] for time in ['DAWN', 'DUSK', 'TWILIGHT']):
            uniqueness += 0.1

        # Unique scene length (very short or very long)
        total_content = len(scene['dialogue']) + len(scene['action'])
        if total_content < 3 or total_content > 20:
            uniqueness += 0.1

        return min(uniqueness, 1.0)

    def _identify_derivative_elements(self, scenes: List[Dict]) -> List[DerivativeElement]:
        """Identify potentially derivative elements."""
        derivative_elements = []

        for scene in scenes:
            # Check dialogue for clichés
            for dialogue in scene['dialogue']:
                text_lower = dialogue['text'].lower()
                for cliche in self.cliches['dialogue']:
                    if cliche in text_lower:
                        derivative_elements.append(DerivativeElement(
                            element_type='dialogue_cliche',
                            description=dialogue['text'][:100],
                            similarity_to=f"Common cliché: '{cliche}'",
                            derivative_score=0.8,
                            scene_num=scene['scene_num'],
                            line_num=dialogue['line_num']
                        ))

            # Check for plot clichés
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            for plot_cliche in self.cliches['plot']:
                if any(word in scene_text for word in plot_cliche.split()):
                    derivative_elements.append(DerivativeElement(
                        element_type='plot_cliche',
                        description=f"Scene contains: {plot_cliche}",
                        similarity_to=f"Common plot device: {plot_cliche}",
                        derivative_score=0.7,
                        scene_num=scene['scene_num'],
                        line_num=scene['line_num']
                    ))

            # Check for character stereotypes
            for character in scene['characters']:
                char_dialogue = ' '.join(d['text'].lower() for d in scene['dialogue']
                                       if d['character'] == character)

                for stereotype in self.cliches['character']:
                    if len(char_dialogue) > 50:  # Enough dialogue to assess
                        # Simplified stereotype detection
                        if 'mentor' in stereotype and 'wisdom' in char_dialogue:
                            derivative_elements.append(DerivativeElement(
                                element_type='character_stereotype',
                                description=f"{character} as {stereotype}",
                                similarity_to=f"Stock character: {stereotype}",
                                derivative_score=0.6,
                                scene_num=scene['scene_num'],
                                line_num=scene['line_num']
                            ))

        return derivative_elements

    def _detect_innovation_points(self, scenes: List[Dict]) -> List[InnovationPoint]:
        """Detect points of innovation in screenplay."""
        innovation_points = []

        # Check for structural innovations
        structural_innovation = self._check_structural_innovation(scenes)
        if structural_innovation:
            innovation_points.append(structural_innovation)

        # Check for narrative innovations
        for innovation_type, markers in self.innovation_markers.items():
            innovation_scenes = []

            for scene in scenes:
                scene_text = ' '.join(a['text'].lower() for a in scene['action'])

                for marker in markers:
                    if marker in scene_text:
                        innovation_scenes.append(scene['scene_num'])
                        break

            if innovation_scenes:
                innovation_points.append(InnovationPoint(
                    innovation_type=innovation_type,
                    description=f"{innovation_type.capitalize()} innovation detected",
                    impact_score=min(len(innovation_scenes) * 0.2, 1.0),
                    scenes=innovation_scenes
                ))

        # Check for character innovations
        character_innovation = self._check_character_innovation(scenes)
        if character_innovation:
            innovation_points.append(character_innovation)

        return innovation_points

    def _check_structural_innovation(self, scenes: List[Dict]) -> Optional[InnovationPoint]:
        """Check for structural innovations."""
        # Check for non-linear structure
        time_markers = []
        for scene in scenes:
            if 'FLASHBACK' in scene['heading'] or 'FLASH FORWARD' in scene['heading']:
                time_markers.append(scene['scene_num'])

            for action in scene['action']:
                if any(word in action['text'].lower()
                      for word in ['years earlier', 'years later', 'flashback', 'flash forward']):
                    time_markers.append(scene['scene_num'])

        if len(time_markers) >= 3:
            return InnovationPoint(
                innovation_type='structural',
                description='Non-linear narrative structure',
                impact_score=min(len(time_markers) * 0.15, 1.0),
                scenes=time_markers
            )

        return None

    def _check_character_innovation(self, scenes: List[Dict]) -> Optional[InnovationPoint]:
        """Check for character innovations."""
        all_characters = set()
        for scene in scenes:
            all_characters.update(scene['characters'])

        # Check for unusual protagonist (non-human, collective, etc.)
        unusual_names = [char for char in all_characters
                        if any(word in char.lower()
                              for word in ['robot', 'ai', 'computer', 'alien', 'creature'])]

        if unusual_names:
            return InnovationPoint(
                innovation_type='character',
                description='Unconventional protagonist type',
                impact_score=0.7,
                scenes=list(range(1, min(6, len(scenes) + 1)))  # First 5 scenes
            )

        return None

    def _analyze_trope_usage(self, scenes: List[Dict]) -> List[TropeUsage]:
        """Analyze how common tropes are used."""
        trope_usage = []

        for trope_name, trope_markers in self.common_tropes.items():
            occurrences = []
            usage_type = 'avoided'

            for scene in scenes:
                scene_text = ' '.join(a['text'].lower() for a in scene['action'])
                scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

                if any(marker in scene_text for marker in trope_markers):
                    occurrences.append(scene['scene_num'])

            if occurrences:
                # Determine usage type based on context
                usage_type = self._determine_trope_usage(trope_name, scenes, occurrences)
                freshness = self._calculate_trope_freshness(usage_type, len(occurrences))

                trope_usage.append(TropeUsage(
                    trope_name=trope_name,
                    usage_type=usage_type,
                    occurrences=occurrences,
                    freshness_score=freshness
                ))

        return trope_usage

    def _determine_trope_usage(self, trope_name: str, scenes: List[Dict],
                              occurrences: List[int]) -> str:
        """Determine how a trope is being used."""
        # Simplified determination
        if len(occurrences) == 1:
            return 'referenced'
        elif len(occurrences) >= 3:
            return 'played_straight'
        else:
            # Check for subversion indicators
            for scene_num in occurrences:
                scene = scenes[scene_num - 1]
                scene_text = ' '.join(a['text'].lower() for a in scene['action'])

                if any(word in scene_text
                      for word in ['but', 'however', 'instead', 'surprisingly', 'unexpectedly']):
                    return 'subverted'

            return 'played_straight'

    def _calculate_trope_freshness(self, usage_type: str, occurrence_count: int) -> float:
        """Calculate freshness of trope usage."""
        base_scores = {
            'avoided': 0.5,
            'referenced': 0.6,
            'subverted': 0.8,
            'deconstructed': 0.9,
            'played_straight': 0.3
        }

        freshness = base_scores.get(usage_type, 0.5)

        # Adjust for overuse
        if usage_type == 'played_straight' and occurrence_count > 3:
            freshness -= 0.1 * (occurrence_count - 3)

        return max(0.0, min(freshness, 1.0))

    def _create_uniqueness_map(self, scenes: List[Dict],
                              original_elements: List[OriginalElement],
                              derivative_elements: List[DerivativeElement]) -> Dict[str, float]:
        """Create scene-by-scene uniqueness map."""
        uniqueness_map = {}

        for scene in scenes:
            scene_num = scene['scene_num']

            # Count original elements in scene
            original_count = sum(1 for e in original_elements if e.scene_num == scene_num)
            original_score = sum(e.uniqueness_score for e in original_elements
                               if e.scene_num == scene_num)

            # Count derivative elements in scene
            derivative_count = sum(1 for e in derivative_elements if e.scene_num == scene_num)
            derivative_score = sum(e.derivative_score for e in derivative_elements
                                 if e.scene_num == scene_num)

            # Calculate scene uniqueness
            if original_count + derivative_count > 0:
                uniqueness = (original_score - derivative_score * 0.5) / (original_count + derivative_count)
            else:
                uniqueness = 0.5  # Neutral

            uniqueness_map[f"scene_{scene_num}"] = max(0.0, min(uniqueness, 1.0))

        return uniqueness_map

    def _create_originality_analysis(self, original_elements: List[OriginalElement],
                                    derivative_elements: List[DerivativeElement],
                                    innovation_points: List[InnovationPoint],
                                    trope_usage: List[TropeUsage],
                                    scenes: List[Dict]) -> OriginalityAnalysis:
        """Create comprehensive originality analysis."""
        # Overall originality
        if original_elements or derivative_elements:
            original_score = sum(e.uniqueness_score for e in original_elements)
            derivative_score = sum(e.derivative_score for e in derivative_elements)

            # Weight original elements more positively
            total_elements = max(1, len(original_elements) + len(derivative_elements))
            overall_originality = max(0.0, min(1.0,
                (original_score * 1.5 - derivative_score * 0.5) / total_elements))
        else:
            overall_originality = 0.5

        # Concept uniqueness
        concept_elements = [e for e in original_elements if e.element_type == 'concept']
        concept_uniqueness = (sum(e.uniqueness_score for e in concept_elements) / len(concept_elements)
                             if concept_elements else 0.5)

        # Plot innovation
        plot_innovations = [ip for ip in innovation_points if ip.innovation_type in ['narrative', 'structural']]
        plot_innovation = min(sum(ip.impact_score for ip in plot_innovations), 1.0)

        # Character originality
        character_elements = [e for e in original_elements if 'character' in e.context]
        character_stereotypes = [d for d in derivative_elements if d.element_type == 'character_stereotype']
        character_originality = max(0.0, min(1.0,
            0.5 + len(character_elements) * 0.1 - len(character_stereotypes) * 0.15))

        # Dialogue freshness
        dialogue_original = [e for e in original_elements if e.element_type == 'dialogue']
        dialogue_cliches = [d for d in derivative_elements if d.element_type == 'dialogue_cliche']
        dialogue_freshness = max(0.0, min(1.0,
            0.5 + len(dialogue_original) * 0.05 - len(dialogue_cliches) * 0.1))

        # Theme innovation
        theme_innovations = [ip for ip in innovation_points if ip.innovation_type == 'thematic']
        theme_innovation = min(sum(ip.impact_score for ip in theme_innovations) + 0.5, 1.0)

        # Structural innovation
        structural_innovations = [ip for ip in innovation_points if ip.innovation_type == 'structural']
        structural_innovation = min(sum(ip.impact_score for ip in structural_innovations) + 0.4, 1.0)

        # Genre subversion
        subverted_tropes = [t for t in trope_usage if t.usage_type in ['subverted', 'deconstructed']]
        genre_subversion = min(len(subverted_tropes) * 0.2 + 0.3, 1.0)

        # World uniqueness
        visual_elements = [e for e in original_elements if e.element_type == 'visual']
        world_uniqueness = min(len(visual_elements) * 0.1 + 0.4, 1.0)

        # Resolution surprise (simplified - would need full screenplay analysis)
        resolution_surprise = overall_originality * 0.8  # Approximation

        return OriginalityAnalysis(
            overall_originality=overall_originality,
            concept_uniqueness=concept_uniqueness,
            plot_innovation=plot_innovation,
            character_originality=character_originality,
            dialogue_freshness=dialogue_freshness,
            theme_innovation=theme_innovation,
            structural_innovation=structural_innovation,
            genre_subversion=genre_subversion,
            world_uniqueness=world_uniqueness,
            resolution_surprise=resolution_surprise
        )

    def _generate_fingerprint(self, screenplay: str, analysis: OriginalityAnalysis) -> str:
        """Generate unique fingerprint for screenplay."""
        # Create unique identifier based on content and originality
        content_hash = hashlib.md5(screenplay.encode()).hexdigest()[:8]

        originality_code = f"{int(analysis.overall_originality * 100):02d}"
        concept_code = f"{int(analysis.concept_uniqueness * 10)}"
        plot_code = f"{int(analysis.plot_innovation * 10)}"

        fingerprint = f"MET-{content_hash}-{originality_code}{concept_code}{plot_code}"
        return fingerprint

    def _check_rules(self, analysis: OriginalityAnalysis,
                    original_elements: List[OriginalElement],
                    derivative_elements: List[DerivativeElement]) -> List[Dict[str, Any]]:
        """Check screenplay against originality rules."""
        violations = []

        for rule in self.rules_config['rules']:
            violation = self._check_single_rule(rule, analysis, original_elements, derivative_elements)
            if violation:
                violations.append(violation)

        return violations

    def _check_single_rule(self, rule: Dict, analysis: OriginalityAnalysis,
                          original_elements: List[OriginalElement],
                          derivative_elements: List[DerivativeElement]) -> Optional[Dict]:
        """Check a single rule."""
        passed = True
        details = ""

        rule_id = rule['id']

        if rule_id == 'MET.R001':  # Concept Originality
            passed = analysis.concept_uniqueness >= 0.6
            details = f"Concept uniqueness: {analysis.concept_uniqueness:.2f}"

        elif rule_id == 'MET.R002':  # Plot Innovation
            passed = analysis.plot_innovation >= 0.5
            details = f"Plot innovation: {analysis.plot_innovation:.2f}"

        elif rule_id == 'MET.R003':  # Character Uniqueness
            passed = analysis.character_originality >= 0.5
            details = f"Character originality: {analysis.character_originality:.2f}"

        elif rule_id == 'MET.R004':  # Dialogue Freshness
            passed = analysis.dialogue_freshness >= 0.5
            details = f"Dialogue freshness: {analysis.dialogue_freshness:.2f}"

        elif rule_id == 'MET.R005':  # Theme Treatment
            passed = analysis.theme_innovation >= 0.4
            details = f"Theme innovation: {analysis.theme_innovation:.2f}"

        elif rule_id == 'MET.R007':  # Structure Innovation
            passed = analysis.structural_innovation >= 0.4
            details = f"Structural innovation: {analysis.structural_innovation:.2f}"

        elif rule_id == 'MET.R008':  # Genre Subversion
            passed = analysis.genre_subversion >= 0.4
            details = f"Genre subversion: {analysis.genre_subversion:.2f}"

        elif rule_id == 'MET.R010':  # Resolution Originality
            passed = analysis.resolution_surprise >= 0.5
            details = f"Resolution surprise: {analysis.resolution_surprise:.2f}"

        elif rule_id == 'MET.R011':  # World Uniqueness
            passed = analysis.world_uniqueness >= 0.5
            details = f"World uniqueness: {analysis.world_uniqueness:.2f}"

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

    def _generate_recommendations(self, analysis: OriginalityAnalysis,
                                 derivative_elements: List[DerivativeElement],
                                 trope_usage: List[TropeUsage],
                                 violations: List[Dict]) -> List[str]:
        """Generate recommendations for improving originality."""
        recommendations = []

        # Overall originality
        if analysis.overall_originality < 0.6:
            recommendations.append(
                "Inject more unique elements to distinguish screenplay from similar works"
            )

        # Concept
        if analysis.concept_uniqueness < 0.6:
            recommendations.append(
                "Develop a more distinctive core concept or add unique twist to familiar premise"
            )

        # Dialogue
        if analysis.dialogue_freshness < 0.5:
            cliche_count = len([d for d in derivative_elements if d.element_type == 'dialogue_cliche'])
            if cliche_count > 3:
                recommendations.append(
                    f"Replace {cliche_count} clichéd dialogue instances with fresh, character-specific lines"
                )

        # Plot
        if analysis.plot_innovation < 0.5:
            recommendations.append(
                "Add unexpected plot developments or structural innovations"
            )

        # Characters
        if analysis.character_originality < 0.5:
            recommendations.append(
                "Create more distinctive character traits and avoid stereotypes"
            )

        # Tropes
        played_straight = [t for t in trope_usage if t.usage_type == 'played_straight']
        if len(played_straight) > 3:
            recommendations.append(
                "Consider subverting or refreshing some conventional tropes"
            )

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            recommendations.append(
                f"Address critical originality issue: {critical_violations[0]['message']}"
            )

        return recommendations[:6]  # Top 6 recommendations

    def _calculate_score(self, analysis: OriginalityAnalysis, violations: List[Dict]) -> int:
        """Calculate overall originality score."""
        # Base score
        score = 90.0

        # Deduct for violations
        severity_penalties = {
            'critical': 20,
            'high': 15,
            'medium': 8,
            'low': 5
        }

        for violation in violations:
            score -= severity_penalties.get(violation['severity'], 5)

        # Bonuses graduais para originalidade excepcional (max +15 total)
        if analysis.overall_originality >= 0.8:
            score += 5
        elif analysis.overall_originality >= 0.6:
            score += 3

        if analysis.structural_innovation >= 0.8:
            score += 5
        elif analysis.structural_innovation >= 0.6:
            score += 3

        if analysis.genre_subversion >= 0.8:
            score += 5
        elif analysis.genre_subversion >= 0.6:
            score += 3

        return max(5, min(95, int(score)))

    def _calculate_creative_risk(self, innovation_points: List[InnovationPoint],
                                analysis: OriginalityAnalysis) -> float:
        """Calculate creative risk score."""
        risk = 0.0

        # High innovation = higher risk
        if innovation_points:
            risk += min(len(innovation_points) * 0.15, 0.5)

        # Very high originality = higher risk
        if analysis.overall_originality > 0.8:
            risk += 0.3

        # Structural innovation = risk
        risk += analysis.structural_innovation * 0.2

        return min(risk, 1.0)

    def _calculate_commercial_viability(self, analysis: OriginalityAnalysis,
                                       trope_usage: List[TropeUsage]) -> float:
        """Calculate commercial viability based on originality."""
        viability = 0.5  # Base

        # Sweet spot: some originality but not too much
        if 0.6 <= analysis.overall_originality <= 0.8:
            viability += 0.3
        elif analysis.overall_originality > 0.8:
            viability += 0.1  # Very original might be niche

        # Some familiar elements help
        if trope_usage:
            familiar_tropes = len([t for t in trope_usage if t.usage_type != 'avoided'])
            if 2 <= familiar_tropes <= 5:
                viability += 0.2

        return min(viability, 1.0)

    def _calculate_genre_innovation(self, innovation_points: List[InnovationPoint],
                                   trope_usage: List[TropeUsage]) -> float:
        """Calculate genre innovation score."""
        innovation = 0.5

        # Innovation points contribute
        if innovation_points:
            innovation += min(len(innovation_points) * 0.1, 0.3)

        # Subverted tropes contribute
        subverted = len([t for t in trope_usage if t.usage_type in ['subverted', 'deconstructed']])
        innovation += min(subverted * 0.1, 0.2)

        return min(innovation, 1.0)