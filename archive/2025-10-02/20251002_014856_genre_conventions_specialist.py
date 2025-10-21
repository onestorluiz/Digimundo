#!/usr/bin/env python3
"""
Script Doctor Genremon - Genre Conventions Specialist
Analyzes genre conventions, tropes, expectations, and cross-genre blending.
"""

import re
import yaml
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict, Counter


@dataclass
class GenreMarker:
    """Represents a genre marker in the screenplay."""
    genre: str
    marker_type: str  # convention, trope, tone, pacing, etc.
    text: str
    context: str  # dialogue, action, scene
    scene_num: int
    strength: float  # 0.0 to 1.0
    line_num: int


@dataclass
class GenreConvention:
    """Represents a genre convention."""
    name: str
    genre: str
    type: str  # essential, common, optional
    present: bool
    occurrences: List[int] = field(default_factory=list)
    strength: float = 0.0


@dataclass
class Trope:
    """Represents a genre trope."""
    name: str
    genre: str
    usage: str  # played_straight, subverted, deconstructed, avoided
    occurrences: List[Tuple[int, str]] = field(default_factory=list)
    effectiveness: float = 0.0


@dataclass
class GenreAnalysis:
    """Complete genre analysis results."""
    primary_genre: str
    secondary_genres: List[str]
    genre_purity: float
    conventions_met: int
    conventions_missing: int
    tropes_used: int
    tropes_subverted: int
    expectations_met: float
    pacing_alignment: float
    tone_alignment: float
    hybrid_balance: float


@dataclass
class GenreConventionsResult:
    """Result from genre conventions analysis."""
    specialist: Dict[str, str]
    score: int
    genre_analysis: GenreAnalysis
    genre_markers: List[GenreMarker]
    conventions: List[GenreConvention]
    tropes: List[Trope]
    genre_distribution: Dict[str, float]
    scene_genres: Dict[int, Dict[str, float]]
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]

    # Additional analysis
    genre_confidence: float = 0.0
    audience_satisfaction: float = 0.0
    originality_score: float = 0.0
    genre_evolution: List[Dict[str, Any]] = field(default_factory=list)


class DrGenreConventions:
    """The Script Doctor™ Genre Conventions Specialist."""

    def __init__(self):
        """Initialize the Genre Conventions specialist."""
        self.name = "Script Doctor Genremon"
        self.specialty = "Genre conventions, tropes, expectations, cross-genre blending"

        # Load rules
        rules_path = Path(__file__).parent.parent / "rules" / "genre_conventions_rules.yaml"
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)

        # Genre convention database
        self.genre_conventions = {
            'action': {
                'essential': ['hero_protagonist', 'clear_antagonist', 'physical_conflict',
                             'high_stakes', 'action_setpieces'],
                'common': ['chase_scene', 'fight_scene', 'explosion', 'weapon_use',
                          'ticking_clock'],
                'optional': ['one_liners', 'sacrificial_moment', 'training_montage']
            },
            'comedy': {
                'essential': ['humor', 'comedic_situations', 'laugh_moments',
                             'light_tone', 'happy_resolution'],
                'common': ['misunderstandings', 'physical_comedy', 'wordplay',
                          'comedic_timing', 'running_gags'],
                'optional': ['fourth_wall_break', 'callbacks', 'sight_gags']
            },
            'drama': {
                'essential': ['character_conflict', 'emotional_depth', 'realistic_dialogue',
                             'character_development', 'meaningful_stakes'],
                'common': ['relationship_dynamics', 'moral_dilemmas', 'internal_struggle',
                          'dramatic_confrontation', 'emotional_revelation'],
                'optional': ['symbolic_elements', 'parallel_storylines', 'thematic_depth']
            },
            'horror': {
                'essential': ['threat_presence', 'fear_moments', 'suspense_building',
                             'victim_characters', 'survival_stakes'],
                'common': ['jump_scares', 'gore_violence', 'isolation', 'darkness',
                          'monster_reveal'],
                'optional': ['final_girl', 'false_ending', 'backstory_reveal']
            },
            'thriller': {
                'essential': ['suspense', 'tension', 'mystery_element', 'danger',
                             'plot_twists'],
                'common': ['cat_and_mouse', 'red_herrings', 'time_pressure',
                          'betrayal', 'revelation'],
                'optional': ['unreliable_narrator', 'parallel_action', 'conspiracy']
            },
            'romance': {
                'essential': ['love_interest', 'romantic_tension', 'emotional_connection',
                             'relationship_development', 'romantic_resolution'],
                'common': ['meet_cute', 'obstacles_to_love', 'confession_scene',
                          'romantic_gestures', 'chemistry'],
                'optional': ['love_triangle', 'grand_gesture', 'reunion_scene']
            },
            'sci_fi': {
                'essential': ['futuristic_elements', 'technology', 'scientific_concepts',
                             'world_building', 'speculative_element'],
                'common': ['space_travel', 'aliens', 'time_travel', 'dystopia',
                          'advanced_weapons'],
                'optional': ['parallel_universe', 'cyberpunk', 'post_apocalyptic']
            },
            'fantasy': {
                'essential': ['magical_elements', 'fantastical_world', 'supernatural',
                             'quest_journey', 'good_vs_evil'],
                'common': ['prophecy', 'magical_creatures', 'chosen_one', 'mentor_figure',
                          'magical_artifact'],
                'optional': ['magical_school', 'portal_world', 'ancient_evil']
            }
        }

        # Genre markers
        self.genre_keywords = {
            'action': ['fight', 'chase', 'explosion', 'shoots', 'punches', 'kicks',
                      'battle', 'combat', 'weapon', 'escape', 'pursuit'],
            'comedy': ['laughs', 'jokes', 'funny', 'hilarious', 'gag', 'humor',
                      'witty', 'sarcastic', 'awkward', 'embarrassing'],
            'drama': ['tears', 'emotional', 'confronts', 'confesses', 'realizes',
                     'understands', 'forgives', 'regrets', 'struggles'],
            'horror': ['screams', 'terrified', 'blood', 'dark', 'creepy', 'shadow',
                      'monster', 'evil', 'possessed', 'haunted'],
            'thriller': ['tense', 'suspicious', 'mysterious', 'reveals', 'discovers',
                        'hidden', 'secret', 'dangerous', 'threat'],
            'romance': ['love', 'kiss', 'embrace', 'heart', 'romantic', 'passion',
                       'attraction', 'chemistry', 'feelings', 'relationship'],
            'sci_fi': ['spaceship', 'alien', 'robot', 'computer', 'technology',
                      'future', 'laser', 'portal', 'dimension', 'experiment'],
            'fantasy': ['magic', 'spell', 'wizard', 'dragon', 'sword', 'quest',
                       'prophecy', 'kingdom', 'mystical', 'enchanted']
        }

        # Pacing expectations by genre
        self.genre_pacing = {
            'action': {'tempo': 'fast', 'scene_length': 'short', 'dialogue_ratio': 0.3},
            'comedy': {'tempo': 'moderate', 'scene_length': 'medium', 'dialogue_ratio': 0.5},
            'drama': {'tempo': 'slow', 'scene_length': 'long', 'dialogue_ratio': 0.6},
            'horror': {'tempo': 'variable', 'scene_length': 'medium', 'dialogue_ratio': 0.4},
            'thriller': {'tempo': 'building', 'scene_length': 'medium', 'dialogue_ratio': 0.5},
            'romance': {'tempo': 'moderate', 'scene_length': 'medium', 'dialogue_ratio': 0.6},
            'sci_fi': {'tempo': 'moderate', 'scene_length': 'medium', 'dialogue_ratio': 0.5},
            'fantasy': {'tempo': 'moderate', 'scene_length': 'long', 'dialogue_ratio': 0.4}
        }

    def analyze(self, screenplay: str) -> GenreConventionsResult:
        """Analyze genre conventions in screenplay."""
        # Parse screenplay
        scenes = self._parse_scenes(screenplay)

        # Identify genres
        genre_markers = self._identify_genre_markers(scenes)
        genre_distribution = self._calculate_genre_distribution(genre_markers)
        primary_genre, secondary_genres = self._determine_genres(genre_distribution)

        # Analyze conventions
        conventions = self._analyze_conventions(scenes, primary_genre, secondary_genres)

        # Analyze tropes
        tropes = self._analyze_tropes(scenes, primary_genre, secondary_genres)

        # Calculate metrics
        genre_analysis = self._create_genre_analysis(
            primary_genre, secondary_genres, conventions, tropes,
            scenes, genre_markers
        )

        # Scene-by-scene genre
        scene_genres = self._analyze_scene_genres(scenes, genre_markers)

        # Track genre evolution
        genre_evolution = self._track_genre_evolution(scene_genres)

        # Check rules
        rule_violations = self._check_rules(genre_analysis, conventions, tropes)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            genre_analysis, conventions, tropes, rule_violations
        )

        # Calculate score
        score = self._calculate_score(genre_analysis, rule_violations)

        # Additional metrics
        genre_confidence = self._calculate_genre_confidence(
            genre_distribution, genre_markers
        )
        audience_satisfaction = self._estimate_audience_satisfaction(
            genre_analysis, conventions
        )
        originality_score = self._calculate_originality(tropes, conventions)

        return GenreConventionsResult(
            specialist={
                'name': self.name,
                'specialty': self.specialty,
                'version': '1.0.0'
            },
            score=score,
            genre_analysis=genre_analysis,
            genre_markers=genre_markers,
            conventions=conventions,
            tropes=tropes,
            genre_distribution=genre_distribution,
            scene_genres=scene_genres,
            recommendations=recommendations,
            rule_violations=rule_violations,
            genre_confidence=genre_confidence,
            audience_satisfaction=audience_satisfaction,
            originality_score=originality_score,
            genre_evolution=genre_evolution
        )

    def _parse_scenes(self, screenplay: str) -> List[Dict[str, Any]]:
        """Parse screenplay into scenes."""
        scenes = []
        current_scene = None
        scene_num = 0

        for i, line in enumerate(screenplay.split('\n'), 1):
            line = line.strip()

            # Scene heading
            if re.match(r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)', line):
                if current_scene:
                    scenes.append(current_scene)
                scene_num += 1
                current_scene = {
                    'scene_num': scene_num,
                    'heading': line,
                    'dialogue': [],
                    'action': [],
                    'characters': set(),
                    'line_num': i
                }
            elif current_scene:
                # Character name (dialogue)
                if line.isupper() and len(line) > 0 and not line.startswith('('):
                    current_scene['characters'].add(line)
                    current_scene['dialogue'].append({
                        'character': line,
                        'line_num': i,
                        'text': ''
                    })
                # Dialogue
                elif current_scene['dialogue'] and not line.startswith('('):
                    if line:
                        current_scene['dialogue'][-1]['text'] += ' ' + line
                # Action lines
                elif line and not line.startswith('('):
                    current_scene['action'].append({
                        'text': line,
                        'line_num': i
                    })

        if current_scene:
            scenes.append(current_scene)

        return scenes

    def _identify_genre_markers(self, scenes: List[Dict]) -> List[GenreMarker]:
        """Identify genre markers in scenes."""
        markers = []

        for scene in scenes:
            scene_num = scene['scene_num']

            # Check action lines
            for action in scene['action']:
                text_lower = action['text'].lower()
                for genre, keywords in self.genre_keywords.items():
                    for keyword in keywords:
                        if keyword in text_lower:
                            strength = self._calculate_marker_strength(
                                keyword, text_lower, 'action'
                            )
                            markers.append(GenreMarker(
                                genre=genre,
                                marker_type='keyword',
                                text=action['text'],
                                context='action',
                                scene_num=scene_num,
                                strength=strength,
                                line_num=action['line_num']
                            ))

            # Check dialogue
            for dialogue in scene['dialogue']:
                text_lower = dialogue['text'].lower()
                for genre, keywords in self.genre_keywords.items():
                    for keyword in keywords:
                        if keyword in text_lower:
                            strength = self._calculate_marker_strength(
                                keyword, text_lower, 'dialogue'
                            )
                            markers.append(GenreMarker(
                                genre=genre,
                                marker_type='keyword',
                                text=dialogue['text'],
                                context='dialogue',
                                scene_num=scene_num,
                                strength=strength,
                                line_num=dialogue['line_num']
                            ))

            # Scene-level markers
            markers.extend(self._identify_scene_level_markers(scene))

        return markers

    def _identify_scene_level_markers(self, scene: Dict) -> List[GenreMarker]:
        """Identify scene-level genre markers."""
        markers = []
        scene_num = scene['scene_num']

        # Check for action scene
        action_count = sum(1 for a in scene['action']
                          if any(word in a['text'].lower()
                                for word in ['fight', 'chase', 'explosion', 'shoots']))
        if action_count >= 2:
            markers.append(GenreMarker(
                genre='action',
                marker_type='scene_type',
                text='Action scene detected',
                context='scene',
                scene_num=scene_num,
                strength=min(action_count * 0.3, 1.0),
                line_num=scene['line_num']
            ))

        # Check for romantic scene
        romance_indicators = ['kiss', 'embrace', 'i love you', 'romantic']
        romance_count = sum(1 for d in scene['dialogue']
                           if any(ind in d['text'].lower() for ind in romance_indicators))
        if romance_count >= 1:
            markers.append(GenreMarker(
                genre='romance',
                marker_type='scene_type',
                text='Romantic scene detected',
                context='scene',
                scene_num=scene_num,
                strength=min(romance_count * 0.4, 1.0),
                line_num=scene['line_num']
            ))

        # Check for horror scene
        if 'dark' in scene['heading'].lower() or 'night' in scene['heading'].lower():
            horror_words = ['creep', 'shadow', 'blood', 'scream', 'terror']
            if any(word in ' '.join(a['text'].lower() for a in scene['action'])
                  for word in horror_words):
                markers.append(GenreMarker(
                    genre='horror',
                    marker_type='atmosphere',
                    text='Horror atmosphere detected',
                    context='scene',
                    scene_num=scene_num,
                    strength=0.6,
                    line_num=scene['line_num']
                ))

        return markers

    def _calculate_marker_strength(self, keyword: str, text: str, context: str) -> float:
        """Calculate strength of a genre marker."""
        base_strength = 0.5

        # Stronger if keyword appears multiple times
        count = text.lower().count(keyword)
        strength = base_strength + (count - 1) * 0.1

        # Context modifiers
        if context == 'action':
            strength *= 1.2  # Action lines are stronger indicators
        elif context == 'scene_heading':
            strength *= 1.3  # Scene headings are strong indicators

        return min(strength, 1.0)

    def _calculate_genre_distribution(self, markers: List[GenreMarker]) -> Dict[str, float]:
        """Calculate genre distribution from markers."""
        genre_weights = defaultdict(float)

        for marker in markers:
            genre_weights[marker.genre] += marker.strength

        # Normalize
        total = sum(genre_weights.values())
        if total > 0:
            return {genre: weight/total for genre, weight in genre_weights.items()}

        return {}

    def _determine_genres(self, distribution: Dict[str, float]) -> Tuple[str, List[str]]:
        """Determine primary and secondary genres."""
        if not distribution:
            return 'drama', []  # Default to drama

        sorted_genres = sorted(distribution.items(), key=lambda x: x[1], reverse=True)

        primary = sorted_genres[0][0]
        secondary = []

        # Secondary genres with significant presence (>15%)
        for genre, weight in sorted_genres[1:]:
            if weight >= 0.15:
                secondary.append(genre)
            else:
                break

        return primary, secondary[:2]  # Max 2 secondary genres

    def _analyze_conventions(self, scenes: List[Dict], primary_genre: str,
                            secondary_genres: List[str]) -> List[GenreConvention]:
        """Analyze genre conventions."""
        conventions = []

        # Check primary genre conventions
        if primary_genre in self.genre_conventions:
            for conv_type in ['essential', 'common', 'optional']:
                for convention_name in self.genre_conventions[primary_genre].get(conv_type, []):
                    convention = self._check_convention(
                        scenes, convention_name, primary_genre, conv_type
                    )
                    conventions.append(convention)

        # Check secondary genre conventions (only essential)
        for genre in secondary_genres:
            if genre in self.genre_conventions:
                for convention_name in self.genre_conventions[genre].get('essential', []):
                    convention = self._check_convention(
                        scenes, convention_name, genre, 'essential'
                    )
                    conventions.append(convention)

        return conventions

    def _check_convention(self, scenes: List[Dict], convention_name: str,
                         genre: str, conv_type: str) -> GenreConvention:
        """Check if a specific convention is present."""
        occurrences = []
        strength = 0.0

        # Map convention names to detection logic
        convention_checks = {
            'hero_protagonist': self._check_hero_protagonist,
            'clear_antagonist': self._check_clear_antagonist,
            'physical_conflict': self._check_physical_conflict,
            'high_stakes': self._check_high_stakes,
            'action_setpieces': self._check_action_setpieces,
            'humor': self._check_humor,
            'comedic_situations': self._check_comedic_situations,
            'character_conflict': self._check_character_conflict,
            'emotional_depth': self._check_emotional_depth,
            'threat_presence': self._check_threat_presence,
            'suspense': self._check_suspense,
            'love_interest': self._check_love_interest,
            'romantic_tension': self._check_romantic_tension,
            'magical_elements': self._check_magical_elements,
            'futuristic_elements': self._check_futuristic_elements,
        }

        # Use specific check if available, otherwise generic
        if convention_name in convention_checks:
            present, occurrences, strength = convention_checks[convention_name](scenes)
        else:
            present, occurrences, strength = self._generic_convention_check(
                scenes, convention_name
            )

        return GenreConvention(
            name=convention_name,
            genre=genre,
            type=conv_type,
            present=present,
            occurrences=occurrences,
            strength=strength
        )

    def _check_hero_protagonist(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for hero protagonist convention."""
        # Look for character who appears most and has heroic actions
        character_actions = defaultdict(list)

        for scene in scenes:
            for char in scene['characters']:
                for action in scene['action']:
                    if any(word in action['text'].lower()
                          for word in ['saves', 'rescues', 'fights', 'protects', 'stands up']):
                        character_actions[char].append(scene['scene_num'])

        if character_actions:
            hero = max(character_actions.items(), key=lambda x: len(x[1]))
            return True, hero[1], min(len(hero[1]) * 0.2, 1.0)

        return False, [], 0.0

    def _check_clear_antagonist(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for clear antagonist convention."""
        antagonist_indicators = ['threatens', 'attacks', 'evil', 'villain', 'enemy']
        occurrences = []

        for scene in scenes:
            for action in scene['action']:
                if any(ind in action['text'].lower() for ind in antagonist_indicators):
                    occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.3, 1.0)

        return present, occurrences, strength

    def _check_physical_conflict(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for physical conflict convention."""
        conflict_words = ['fight', 'battle', 'punch', 'kick', 'shoot', 'attack']
        occurrences = []

        for scene in scenes:
            for action in scene['action']:
                if any(word in action['text'].lower() for word in conflict_words):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 1
        strength = min(len(occurrences) * 0.25, 1.0)

        return present, occurrences, strength

    def _check_high_stakes(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for high stakes convention."""
        stakes_words = ['life', 'death', 'save', 'destroy', 'end', 'fate', 'survival']
        occurrences = []

        for scene in scenes:
            for dialogue in scene['dialogue']:
                if any(word in dialogue['text'].lower() for word in stakes_words):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.2, 1.0)

        return present, occurrences, strength

    def _check_action_setpieces(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for action setpieces convention."""
        setpiece_indicators = ['chase', 'explosion', 'crashes', 'battle', 'showdown']
        occurrences = []

        for scene in scenes:
            action_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(ind in action_text for ind in setpiece_indicators):
                if len(scene['action']) >= 5:  # Substantial action scene
                    occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 1
        strength = min(len(occurrences) * 0.4, 1.0)

        return present, occurrences, strength

    def _check_humor(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for humor convention."""
        humor_indicators = ['laughs', 'jokes', 'funny', 'hilarious', 'chuckles', 'grins']
        occurrences = []

        for scene in scenes:
            for action in scene['action']:
                if any(ind in action['text'].lower() for ind in humor_indicators):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 3
        strength = min(len(occurrences) * 0.15, 1.0)

        return present, occurrences, strength

    def _check_comedic_situations(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for comedic situations convention."""
        situation_words = ['awkward', 'embarrassing', 'mishap', 'confusion', 'mistake']
        occurrences = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(word in scene_text for word in situation_words):
                occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.25, 1.0)

        return present, occurrences, strength

    def _check_character_conflict(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for character conflict convention."""
        conflict_words = ['argues', 'confronts', 'disagrees', 'opposes', 'challenges']
        occurrences = []

        for scene in scenes:
            for action in scene['action']:
                if any(word in action['text'].lower() for word in conflict_words):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.3, 1.0)

        return present, occurrences, strength

    def _check_emotional_depth(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for emotional depth convention."""
        emotion_words = ['tears', 'cries', 'weeps', 'emotional', 'heartfelt', 'vulnerable']
        occurrences = []

        for scene in scenes:
            for action in scene['action']:
                if any(word in action['text'].lower() for word in emotion_words):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 1
        strength = min(len(occurrences) * 0.35, 1.0)

        return present, occurrences, strength

    def _check_threat_presence(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for threat presence convention."""
        threat_words = ['monster', 'killer', 'creature', 'evil', 'stalks', 'hunts']
        occurrences = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(word in scene_text for word in threat_words):
                occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.3, 1.0)

        return present, occurrences, strength

    def _check_suspense(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for suspense convention."""
        suspense_words = ['tense', 'nervous', 'holds breath', 'creeps', 'slowly']
        occurrences = []

        for scene in scenes:
            for action in scene['action']:
                if any(word in action['text'].lower() for word in suspense_words):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 3
        strength = min(len(occurrences) * 0.2, 1.0)

        return present, occurrences, strength

    def _check_love_interest(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for love interest convention."""
        love_words = ['love', 'attraction', 'feelings', 'heart', 'romantic']
        occurrences = []

        for scene in scenes:
            for dialogue in scene['dialogue']:
                if any(word in dialogue['text'].lower() for word in love_words):
                    occurrences.append(scene['scene_num'])
                    break

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.3, 1.0)

        return present, occurrences, strength

    def _check_romantic_tension(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for romantic tension convention."""
        tension_words = ['gazes', 'touches', 'close', 'chemistry', 'moment', 'eyes meet']
        occurrences = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(word in scene_text for word in tension_words):
                occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 2
        strength = min(len(occurrences) * 0.25, 1.0)

        return present, occurrences, strength

    def _check_magical_elements(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for magical elements convention."""
        magic_words = ['magic', 'spell', 'wizard', 'enchant', 'mystical', 'supernatural']
        occurrences = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(word in scene_text for word in magic_words):
                occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 1
        strength = min(len(occurrences) * 0.4, 1.0)

        return present, occurrences, strength

    def _check_futuristic_elements(self, scenes: List[Dict]) -> Tuple[bool, List[int], float]:
        """Check for futuristic elements convention."""
        future_words = ['spaceship', 'laser', 'robot', 'android', 'hologram', 'portal']
        occurrences = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(word in scene_text for word in future_words):
                occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 1
        strength = min(len(occurrences) * 0.4, 1.0)

        return present, occurrences, strength

    def _generic_convention_check(self, scenes: List[Dict],
                                 convention_name: str) -> Tuple[bool, List[int], float]:
        """Generic check for conventions not specifically implemented."""
        # Simple keyword-based check
        keywords = convention_name.replace('_', ' ').split()
        occurrences = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            if any(keyword in scene_text for keyword in keywords):
                occurrences.append(scene['scene_num'])

        present = len(occurrences) >= 1
        strength = min(len(occurrences) * 0.2, 1.0)

        return present, occurrences, strength

    def _analyze_tropes(self, scenes: List[Dict], primary_genre: str,
                       secondary_genres: List[str]) -> List[Trope]:
        """Analyze genre tropes."""
        tropes = []

        # Common tropes by genre
        genre_tropes = {
            'action': ['one_liner', 'explosion_walk', 'bad_guy_monologue'],
            'comedy': ['running_gag', 'callback', 'rule_of_three'],
            'drama': ['dark_secret', 'redemption_arc', 'sacrifice'],
            'horror': ['final_girl', 'jump_scare', 'false_death'],
            'thriller': ['red_herring', 'ticking_clock', 'double_cross'],
            'romance': ['meet_cute', 'love_triangle', 'grand_gesture'],
            'sci_fi': ['chosen_one', 'fish_out_of_water', 'prophecy'],
            'fantasy': ['mentor_death', 'magical_macguffin', 'prophecy']
        }

        # Check primary genre tropes
        if primary_genre in genre_tropes:
            for trope_name in genre_tropes[primary_genre]:
                trope = self._check_trope(scenes, trope_name, primary_genre)
                tropes.append(trope)

        return tropes

    def _check_trope(self, scenes: List[Dict], trope_name: str, genre: str) -> Trope:
        """Check for specific trope usage."""
        occurrences = []
        usage = 'avoided'
        effectiveness = 0.0

        # Specific trope detection
        if trope_name == 'one_liner':
            occurrences, usage = self._check_one_liner(scenes)
        elif trope_name == 'meet_cute':
            occurrences, usage = self._check_meet_cute(scenes)
        elif trope_name == 'jump_scare':
            occurrences, usage = self._check_jump_scare(scenes)
        # Add more specific trope checks as needed

        if occurrences:
            effectiveness = self._evaluate_trope_effectiveness(usage, len(occurrences))

        return Trope(
            name=trope_name,
            genre=genre,
            usage=usage,
            occurrences=occurrences,
            effectiveness=effectiveness
        )

    def _check_one_liner(self, scenes: List[Dict]) -> Tuple[List[Tuple[int, str]], str]:
        """Check for one-liner trope."""
        occurrences = []

        for scene in scenes:
            for dialogue in scene['dialogue']:
                text = dialogue['text'].strip()
                # Short, punchy dialogue after action
                if len(text) < 50 and any(end in text for end in ['!', '...', '.']):
                    if scene['scene_num'] > 1:  # Not in opening
                        occurrences.append((scene['scene_num'], text))

        if occurrences:
            return occurrences, 'played_straight'
        return [], 'avoided'

    def _check_meet_cute(self, scenes: List[Dict]) -> Tuple[List[Tuple[int, str]], str]:
        """Check for meet cute trope."""
        occurrences = []
        meet_words = ['bumps into', 'collides', 'spills', 'trips', 'awkward']

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            if any(word in scene_text for word in meet_words):
                if len(scene['characters']) >= 2:
                    occurrences.append((scene['scene_num'], 'Meet cute scene'))

        if occurrences:
            return occurrences, 'played_straight'
        return [], 'avoided'

    def _check_jump_scare(self, scenes: List[Dict]) -> Tuple[List[Tuple[int, str]], str]:
        """Check for jump scare trope."""
        occurrences = []
        scare_words = ['suddenly', 'jumps out', 'appears behind', 'screams']

        for scene in scenes:
            for action in scene['action']:
                if any(word in action['text'].lower() for word in scare_words):
                    occurrences.append((scene['scene_num'], action['text']))

        if occurrences:
            return occurrences, 'played_straight'
        return [], 'avoided'

    def _evaluate_trope_effectiveness(self, usage: str, count: int) -> float:
        """Evaluate how effectively a trope is used."""
        base_scores = {
            'subverted': 0.8,
            'deconstructed': 0.7,
            'played_straight': 0.5,
            'avoided': 0.3
        }

        score = base_scores.get(usage, 0.5)

        # Adjust for frequency
        if usage == 'played_straight' and count > 3:
            score -= 0.1  # Overused
        elif usage in ['subverted', 'deconstructed'] and count >= 1:
            score += 0.1  # Good use of subversion

        return min(max(score, 0.0), 1.0)

    def _create_genre_analysis(self, primary_genre: str, secondary_genres: List[str],
                              conventions: List[GenreConvention], tropes: List[Trope],
                              scenes: List[Dict], markers: List[GenreMarker]) -> GenreAnalysis:
        """Create comprehensive genre analysis."""
        # Convention metrics
        essential_conventions = [c for c in conventions
                                if c.type == 'essential' and c.genre == primary_genre]
        conventions_met = sum(1 for c in essential_conventions if c.present)
        conventions_missing = len(essential_conventions) - conventions_met

        # Trope metrics
        tropes_used = sum(1 for t in tropes if t.usage != 'avoided')
        tropes_subverted = sum(1 for t in tropes if t.usage in ['subverted', 'deconstructed'])

        # Calculate scores
        genre_purity = self._calculate_genre_purity(primary_genre, markers)
        expectations_met = conventions_met / len(essential_conventions) if essential_conventions else 0.5
        pacing_alignment = self._calculate_pacing_alignment(scenes, primary_genre)
        tone_alignment = self._calculate_tone_alignment(markers, primary_genre)
        hybrid_balance = self._calculate_hybrid_balance(primary_genre, secondary_genres, markers)

        return GenreAnalysis(
            primary_genre=primary_genre,
            secondary_genres=secondary_genres,
            genre_purity=genre_purity,
            conventions_met=conventions_met,
            conventions_missing=conventions_missing,
            tropes_used=tropes_used,
            tropes_subverted=tropes_subverted,
            expectations_met=expectations_met,
            pacing_alignment=pacing_alignment,
            tone_alignment=tone_alignment,
            hybrid_balance=hybrid_balance
        )

    def _calculate_genre_purity(self, primary_genre: str, markers: List[GenreMarker]) -> float:
        """Calculate how purely the screenplay adheres to primary genre."""
        if not markers:
            return 0.0

        primary_markers = [m for m in markers if m.genre == primary_genre]
        total_strength = sum(m.strength for m in markers)
        primary_strength = sum(m.strength for m in primary_markers)

        if total_strength > 0:
            return primary_strength / total_strength
        return 0.0

    def _calculate_pacing_alignment(self, scenes: List[Dict], genre: str) -> float:
        """Calculate how well pacing aligns with genre expectations."""
        if genre not in self.genre_pacing:
            return 0.5

        expected = self.genre_pacing[genre]

        # Calculate actual pacing metrics
        if not scenes:
            return 0.5

        total_elements = sum(len(s['action']) + len(s['dialogue']) for s in scenes)
        if total_elements == 0:
            return 0.5

        avg_scene_length = total_elements / len(scenes)
        dialogue_ratio = sum(len(s['dialogue']) for s in scenes) / total_elements

        # Compare to expectations
        score = 1.0

        # Scene length comparison
        if expected['scene_length'] == 'short' and avg_scene_length > 15:
            score -= 0.3
        elif expected['scene_length'] == 'long' and avg_scene_length < 8:
            score -= 0.3

        # Dialogue ratio comparison
        ratio_diff = abs(dialogue_ratio - expected['dialogue_ratio'])
        score -= ratio_diff

        return max(score, 0.0)

    def _calculate_tone_alignment(self, markers: List[GenreMarker], genre: str) -> float:
        """Calculate tone alignment with genre."""
        # Genre-appropriate tones
        genre_tones = {
            'action': ['intense', 'exciting', 'fast'],
            'comedy': ['light', 'funny', 'playful'],
            'drama': ['serious', 'emotional', 'thoughtful'],
            'horror': ['dark', 'tense', 'frightening'],
            'thriller': ['suspenseful', 'mysterious', 'tense'],
            'romance': ['warm', 'emotional', 'tender'],
            'sci_fi': ['thoughtful', 'mysterious', 'epic'],
            'fantasy': ['magical', 'adventurous', 'epic']
        }

        # Simple tone analysis based on markers
        if genre in genre_tones:
            genre_marker_count = sum(1 for m in markers if m.genre == genre)
            total_markers = len(markers)

            if total_markers > 0:
                return genre_marker_count / total_markers

        return 0.5

    def _calculate_hybrid_balance(self, primary: str, secondary: List[str],
                                 markers: List[GenreMarker]) -> float:
        """Calculate balance in hybrid genre screenplay."""
        if not secondary:
            return 1.0  # Not a hybrid

        # Calculate distribution
        genre_strengths = defaultdict(float)
        for marker in markers:
            genre_strengths[marker.genre] += marker.strength

        # Check if secondary genres are well-represented but not overwhelming
        primary_strength = genre_strengths[primary]
        secondary_strength = sum(genre_strengths[g] for g in secondary)

        if primary_strength == 0:
            return 0.0

        ratio = secondary_strength / primary_strength

        # Ideal ratio is between 0.3 and 0.7 (secondary present but not dominant)
        if 0.3 <= ratio <= 0.7:
            return 1.0
        elif ratio < 0.3:
            return ratio / 0.3  # Too little secondary
        else:
            return 0.7 / ratio  # Too much secondary

    def _analyze_scene_genres(self, scenes: List[Dict],
                             markers: List[GenreMarker]) -> Dict[int, Dict[str, float]]:
        """Analyze genre for each scene."""
        scene_genres = {}

        for scene in scenes:
            scene_num = scene['scene_num']
            scene_markers = [m for m in markers if m.scene_num == scene_num]

            genre_weights = defaultdict(float)
            for marker in scene_markers:
                genre_weights[marker.genre] += marker.strength

            # Normalize
            total = sum(genre_weights.values())
            if total > 0:
                scene_genres[scene_num] = {
                    genre: weight/total for genre, weight in genre_weights.items()
                }
            else:
                scene_genres[scene_num] = {}

        return scene_genres

    def _track_genre_evolution(self, scene_genres: Dict[int, Dict[str, float]]) -> List[Dict]:
        """Track how genre evolves through screenplay."""
        evolution = []

        for scene_num in sorted(scene_genres.keys()):
            if scene_genres[scene_num]:
                dominant = max(scene_genres[scene_num].items(), key=lambda x: x[1])
                evolution.append({
                    'scene': scene_num,
                    'dominant_genre': dominant[0],
                    'strength': dominant[1],
                    'genres': scene_genres[scene_num]
                })

        return evolution

    def _check_rules(self, analysis: GenreAnalysis, conventions: List[GenreConvention],
                    tropes: List[Trope]) -> List[Dict[str, Any]]:
        """Check screenplay against genre rules."""
        violations = []

        for rule in self.rules_config['rules']:
            violation = self._check_single_rule(rule, analysis, conventions, tropes)
            if violation:
                violations.append(violation)

        return violations

    def _check_single_rule(self, rule: Dict, analysis: GenreAnalysis,
                          conventions: List[GenreConvention],
                          tropes: List[Trope]) -> Optional[Dict]:
        """Check a single rule."""
        passed = True
        details = ""

        rule_id = rule['id']

        if rule_id == 'GEN.R001':  # Genre Identification
            passed = analysis.genre_purity >= 0.4
            details = f"Genre purity: {analysis.genre_purity:.2f}"

        elif rule_id == 'GEN.R002':  # Core Conventions
            passed = analysis.expectations_met >= 0.6
            details = f"Conventions met: {analysis.conventions_met}/{analysis.conventions_met + analysis.conventions_missing}"

        elif rule_id == 'GEN.R003':  # Audience Expectations
            passed = analysis.expectations_met >= 0.7
            details = f"Expectations met: {analysis.expectations_met:.2f}"

        elif rule_id == 'GEN.R004':  # Genre Tone Match
            passed = analysis.tone_alignment >= 0.5
            details = f"Tone alignment: {analysis.tone_alignment:.2f}"

        elif rule_id == 'GEN.R005':  # Trope Usage
            effectiveness = sum(t.effectiveness for t in tropes) / len(tropes) if tropes else 0
            passed = effectiveness >= 0.4
            details = f"Trope effectiveness: {effectiveness:.2f}"

        elif rule_id == 'GEN.R006':  # Genre Pacing
            passed = analysis.pacing_alignment >= 0.5
            details = f"Pacing alignment: {analysis.pacing_alignment:.2f}"

        elif rule_id == 'GEN.R008':  # Genre Hybridization
            passed = analysis.hybrid_balance >= 0.5
            details = f"Hybrid balance: {analysis.hybrid_balance:.2f}"

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

    def _generate_recommendations(self, analysis: GenreAnalysis,
                                 conventions: List[GenreConvention],
                                 tropes: List[Trope],
                                 violations: List[Dict]) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []

        # Genre clarity
        if analysis.genre_purity < 0.5:
            recommendations.append(
                f"Strengthen {analysis.primary_genre} genre identity through more consistent genre markers"
            )

        # Missing conventions
        missing_essential = [c for c in conventions
                           if c.type == 'essential' and not c.present]
        if missing_essential:
            conventions_list = ', '.join(c.name.replace('_', ' ') for c in missing_essential[:3])
            recommendations.append(
                f"Add missing {analysis.primary_genre} conventions: {conventions_list}"
            )

        # Pacing
        if analysis.pacing_alignment < 0.6:
            recommendations.append(
                f"Adjust pacing to better match {analysis.primary_genre} genre expectations"
            )

        # Tropes
        if analysis.tropes_subverted == 0 and analysis.tropes_used > 3:
            recommendations.append(
                "Consider subverting or refreshing some genre tropes for originality"
            )

        # Hybrid balance
        if analysis.secondary_genres and analysis.hybrid_balance < 0.6:
            recommendations.append(
                "Better balance primary and secondary genre elements"
            )

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            recommendations.append(
                f"Address critical genre issues: {critical_violations[0]['message']}"
            )

        return recommendations[:6]  # Top 6 recommendations

    def _calculate_score(self, analysis: GenreAnalysis, violations: List[Dict]) -> int:
        """Calculate overall genre score."""
        score = 100

        # Deduct for violations
        severity_penalties = {
            'critical': 15,
            'high': 10,
            'medium': 5,
            'low': 2
        }

        for violation in violations:
            score -= severity_penalties.get(violation['severity'], 5)

        # Bonus for good genre execution
        if analysis.genre_purity >= 0.7:
            score += 5
        if analysis.expectations_met >= 0.8:
            score += 5
        if analysis.tropes_subverted >= 2:
            score += 5

        return max(0, min(100, score))

    def _calculate_genre_confidence(self, distribution: Dict[str, float],
                                   markers: List[GenreMarker]) -> float:
        """Calculate confidence in genre identification."""
        if not distribution:
            return 0.0

        # Check if primary genre is clearly dominant
        sorted_genres = sorted(distribution.values(), reverse=True)
        if len(sorted_genres) >= 2:
            gap = sorted_genres[0] - sorted_genres[1]
            confidence = min(gap * 2, 1.0)
        else:
            confidence = sorted_genres[0] if sorted_genres else 0.0

        # Adjust for marker count
        if len(markers) < 10:
            confidence *= 0.7  # Less confident with fewer markers

        return confidence

    def _estimate_audience_satisfaction(self, analysis: GenreAnalysis,
                                       conventions: List[GenreConvention]) -> float:
        """Estimate audience satisfaction based on genre execution."""
        satisfaction = 0.0

        # Base on expectations met
        satisfaction += analysis.expectations_met * 0.4

        # Convention fulfillment
        essential_present = sum(1 for c in conventions
                              if c.type == 'essential' and c.present)
        essential_total = sum(1 for c in conventions if c.type == 'essential')
        if essential_total > 0:
            satisfaction += (essential_present / essential_total) * 0.3

        # Tone and pacing alignment
        satisfaction += analysis.tone_alignment * 0.15
        satisfaction += analysis.pacing_alignment * 0.15

        return min(satisfaction, 1.0)

    def _calculate_originality(self, tropes: List[Trope],
                              conventions: List[GenreConvention]) -> float:
        """Calculate originality score."""
        originality = 0.5  # Base score

        # Bonus for subverted tropes
        if tropes:
            subversion_rate = sum(1 for t in tropes
                                 if t.usage in ['subverted', 'deconstructed']) / len(tropes)
            originality += subversion_rate * 0.3

        # Bonus for unique convention combinations
        optional_present = sum(1 for c in conventions
                             if c.type == 'optional' and c.present)
        if optional_present >= 2:
            originality += 0.2

        return min(originality, 1.0)