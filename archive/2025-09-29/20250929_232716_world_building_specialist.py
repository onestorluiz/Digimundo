#!/usr/bin/env python3
"""
Script Doctor Worldmon - World Building Specialist
Analyzes world creation, universe consistency, environmental storytelling, and setting authenticity.
"""

import re
import yaml
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict, Counter


@dataclass
class WorldElement:
    """Represents an element of the world."""
    element_type: str  # location, technology, culture, etc.
    name: str
    description: str
    scene_num: int
    consistency_score: float
    line_num: int


@dataclass
class Location:
    """Represents a location in the world."""
    name: str
    location_type: str  # interior, exterior, specific place
    appearances: List[int]  # scene numbers
    descriptions: List[str]
    consistency: float
    atmosphere: str


@dataclass
class WorldRule:
    """Represents a rule or law of the world."""
    rule_type: str  # physical, social, technological, magical
    description: str
    established_scene: int
    violations: List[Tuple[int, str]]  # scene_num, violation description
    consistency: float


@dataclass
class CulturalElement:
    """Represents a cultural element."""
    element_type: str  # custom, tradition, belief, social norm
    description: str
    scenes: List[int]
    depth_score: float


@dataclass
class WorldAnalysis:
    """Complete world building analysis."""
    world_type: str
    establishment_quality: float
    consistency_score: float
    detail_richness: float
    cultural_depth: float
    geographic_clarity: float
    temporal_consistency: float
    technological_consistency: float
    atmospheric_coherence: float
    world_story_integration: float


@dataclass
class WorldBuildingResult:
    """Result from world building analysis."""
    specialist: Dict[str, str]
    score: int
    world_analysis: WorldAnalysis
    world_elements: List[WorldElement]
    locations: List[Location]
    world_rules: List[WorldRule]
    cultural_elements: List[CulturalElement]
    world_map: Dict[str, Any]  # Visual representation of world
    timeline: List[Dict[str, Any]]  # World timeline
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]

    # Additional analysis
    immersion_score: float = 0.0
    believability_score: float = 0.0
    uniqueness_score: float = 0.0
    world_depth_layers: Dict[str, float] = field(default_factory=dict)


class DrWorldBuilding:
    """The Script Doctor™ World Building Specialist."""

    def __init__(self):
        """Initialize the World Building specialist."""
        self.name = "Script Doctor Worldmon"
        self.specialty = "World creation, universe consistency, environmental storytelling, setting authenticity"

        # Load rules
        rules_path = Path(__file__).parent.parent / "rules" / "world_building_rules.yaml"
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)

        # World type indicators
        self.world_type_markers = {
            'contemporary_realistic': ['apartment', 'office', 'street', 'phone', 'car', 'computer'],
            'historical': ['castle', 'sword', 'horse', 'tavern', 'king', 'servant'],
            'fantasy': ['magic', 'dragon', 'spell', 'wizard', 'enchanted', 'mystical'],
            'sci_fi': ['spaceship', 'laser', 'android', 'hologram', 'portal', 'alien',
                      'cybernetic', 'neural', 'implant', 'drone', 'quantum', 'cyber',
                      'holo', 'tech', 'digital', 'synthetic', 'year 2'],
            'dystopian': ['surveillance', 'oppression', 'rebellion', 'wasteland', 'control',
                         'collective', 'resistance'],
            'post_apocalyptic': ['ruins', 'survivors', 'radiation', 'scavenger', 'bunker'],
            'western': ['saloon', 'sheriff', 'desert', 'gunslinger', 'horse', 'ranch'],
            'noir': ['alley', 'detective', 'rain', 'shadow', 'cigarette', 'neon']
        }

        # Environmental details
        self.environmental_categories = {
            'visual': ['color', 'light', 'shadow', 'texture', 'shape'],
            'auditory': ['sound', 'noise', 'echo', 'silence', 'music'],
            'tactile': ['rough', 'smooth', 'cold', 'warm', 'wet', 'dry'],
            'olfactory': ['smell', 'scent', 'odor', 'fragrance', 'stench'],
            'atmospheric': ['mood', 'tension', 'peaceful', 'chaotic', 'eerie']
        }

    def analyze(self, screenplay: str) -> WorldBuildingResult:
        """Analyze world building in screenplay."""
        # Parse screenplay
        scenes = self._parse_scenes(screenplay)

        # Identify world type
        world_type = self._identify_world_type(scenes)

        # Extract world elements
        world_elements = self._extract_world_elements(scenes)

        # Analyze locations
        locations = self._analyze_locations(scenes)

        # Extract world rules
        world_rules = self._extract_world_rules(scenes)

        # Analyze cultural elements
        cultural_elements = self._analyze_cultural_elements(scenes)

        # Create world map
        world_map = self._create_world_map(locations, scenes)

        # Build timeline
        timeline = self._build_world_timeline(scenes, world_elements)

        # Calculate metrics
        world_analysis = self._create_world_analysis(
            world_type, world_elements, locations, world_rules,
            cultural_elements, scenes
        )

        # Calculate depth layers
        world_depth_layers = self._analyze_depth_layers(
            world_elements, locations, cultural_elements
        )

        # Check rules
        rule_violations = self._check_rules(
            world_analysis, world_elements, locations, world_rules
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            world_analysis, world_elements, locations, rule_violations
        )

        # Calculate score
        score = self._calculate_score(world_analysis, rule_violations)

        # Additional metrics
        immersion_score = self._calculate_immersion(world_elements, locations)
        believability_score = self._calculate_believability(world_rules, world_analysis)
        uniqueness_score = self._calculate_uniqueness(world_elements, cultural_elements)

        return WorldBuildingResult(
            specialist={
                'name': self.name,
                'specialty': self.specialty,
                'version': '1.0.0'
            },
            score=score,
            world_analysis=world_analysis,
            world_elements=world_elements,
            locations=locations,
            world_rules=world_rules,
            cultural_elements=cultural_elements,
            world_map=world_map,
            timeline=timeline,
            recommendations=recommendations,
            rule_violations=rule_violations,
            immersion_score=immersion_score,
            believability_score=believability_score,
            uniqueness_score=uniqueness_score,
            world_depth_layers=world_depth_layers
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
                    'location': self._extract_location_from_heading(line_stripped),
                    'time': self._extract_time_from_heading(line_stripped),
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

    def _extract_location_from_heading(self, heading: str) -> str:
        """Extract location from scene heading."""
        # Remove INT./EXT./etc and time of day
        location = re.sub(r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)\s*', '', heading)
        location = re.sub(r'\s*-\s*(DAY|NIGHT|MORNING|EVENING|CONTINUOUS|LATER|MOMENTS LATER).*$', '', location)
        return location.strip()

    def _extract_time_from_heading(self, heading: str) -> str:
        """Extract time from scene heading."""
        time_match = re.search(r'-\s*(DAY|NIGHT|MORNING|EVENING|DAWN|DUSK|CONTINUOUS|LATER)', heading)
        return time_match.group(1) if time_match else 'UNSPECIFIED'

    def _identify_world_type(self, scenes: List[Dict]) -> str:
        """Identify the type of world."""
        type_scores = defaultdict(float)

        for scene in scenes:
            # Check scene headings and action
            scene_text = scene['heading'].lower()
            scene_text += ' '.join(a['text'].lower() for a in scene['action'])
            # Also check dialogue for world type markers
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            for world_type, markers in self.world_type_markers.items():
                for marker in markers:
                    if marker in scene_text:
                        type_scores[world_type] += 1

        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        return 'contemporary_realistic'  # Default

    def _extract_world_elements(self, scenes: List[Dict]) -> List[WorldElement]:
        """Extract world elements from scenes."""
        elements = []

        for scene in scenes:
            # Location elements
            if scene['location']:
                elements.append(WorldElement(
                    element_type='location',
                    name=scene['location'],
                    description=f"Scene location: {scene['heading']}",
                    scene_num=scene['scene_num'],
                    consistency_score=1.0,
                    line_num=scene['line_num']
                ))

            # Environmental details from action lines
            for action in scene['action']:
                elements.extend(self._extract_environmental_details(
                    action['text'], scene['scene_num'], action['line_num']
                ))

            # Technology mentions
            tech_words = ['computer', 'phone', 'weapon', 'vehicle', 'device', 'machine']
            for action in scene['action']:
                text_lower = action['text'].lower()
                for tech in tech_words:
                    if tech in text_lower:
                        elements.append(WorldElement(
                            element_type='technology',
                            name=tech,
                            description=action['text'],
                            scene_num=scene['scene_num'],
                            consistency_score=1.0,
                            line_num=action['line_num']
                        ))

        return elements

    def _extract_environmental_details(self, text: str, scene_num: int, line_num: int) -> List[WorldElement]:
        """Extract environmental details from text."""
        elements = []
        text_lower = text.lower()

        # Visual details
        visual_patterns = [
            r'(dim|bright|dark|shadowy|lit|glowing)',
            r'(red|blue|green|golden|silver|black|white)',
            r'(foggy|misty|clear|hazy|dusty)'
        ]

        for pattern in visual_patterns:
            if re.search(pattern, text_lower):
                elements.append(WorldElement(
                    element_type='environmental_visual',
                    name='visual_detail',
                    description=text,
                    scene_num=scene_num,
                    consistency_score=1.0,
                    line_num=line_num
                ))
                break

        # Atmospheric details
        atmosphere_words = ['tense', 'peaceful', 'chaotic', 'eerie', 'warm', 'cold']
        if any(word in text_lower for word in atmosphere_words):
            elements.append(WorldElement(
                element_type='atmospheric',
                name='atmosphere',
                description=text,
                scene_num=scene_num,
                consistency_score=1.0,
                line_num=line_num
            ))

        return elements

    def _analyze_locations(self, scenes: List[Dict]) -> List[Location]:
        """Analyze locations in the screenplay."""
        location_data = defaultdict(lambda: {
            'appearances': [],
            'descriptions': [],
            'types': []
        })

        for scene in scenes:
            if scene['location']:
                loc_name = scene['location']
                location_data[loc_name]['appearances'].append(scene['scene_num'])

                # Determine location type
                if scene['heading'].startswith('INT.'):
                    loc_type = 'interior'
                elif scene['heading'].startswith('EXT.'):
                    loc_type = 'exterior'
                else:
                    loc_type = 'mixed'
                location_data[loc_name]['types'].append(loc_type)

                # Collect descriptions
                for action in scene['action'][:3]:  # First 3 action lines
                    location_data[loc_name]['descriptions'].append(action['text'])

        # Create Location objects
        locations = []
        for name, data in location_data.items():
            # Check consistency
            type_consistency = len(set(data['types'])) == 1
            consistency = 1.0 if type_consistency else 0.5

            # Determine atmosphere
            atmosphere = self._determine_location_atmosphere(data['descriptions'])

            locations.append(Location(
                name=name,
                location_type=data['types'][0] if data['types'] else 'unknown',
                appearances=data['appearances'],
                descriptions=data['descriptions'],
                consistency=consistency,
                atmosphere=atmosphere
            ))

        return locations

    def _determine_location_atmosphere(self, descriptions: List[str]) -> str:
        """Determine atmosphere of a location from descriptions."""
        combined = ' '.join(descriptions).lower()

        atmosphere_keywords = {
            'tense': ['tense', 'nervous', 'anxious', 'stressed'],
            'peaceful': ['peaceful', 'calm', 'serene', 'quiet'],
            'chaotic': ['chaotic', 'frantic', 'wild', 'crazy'],
            'mysterious': ['mysterious', 'strange', 'eerie', 'weird'],
            'romantic': ['romantic', 'intimate', 'cozy', 'warm'],
            'dangerous': ['dangerous', 'threatening', 'deadly', 'risky']
        }

        for atmosphere, keywords in atmosphere_keywords.items():
            if any(keyword in combined for keyword in keywords):
                return atmosphere

        return 'neutral'

    def _extract_world_rules(self, scenes: List[Dict]) -> List[WorldRule]:
        """Extract implied world rules."""
        rules = []

        # Technology rules
        tech_mentions = defaultdict(list)
        for scene in scenes:
            for action in scene['action']:
                text_lower = action['text'].lower()
                # Check for technology
                if any(word in text_lower for word in ['computer', 'phone', 'car', 'gun']):
                    tech_mentions['modern_tech'].append(scene['scene_num'])
                if any(word in text_lower for word in ['spaceship', 'laser', 'hologram']):
                    tech_mentions['future_tech'].append(scene['scene_num'])
                if any(word in text_lower for word in ['sword', 'horse', 'torch']):
                    tech_mentions['historical_tech'].append(scene['scene_num'])

        # Determine technology rule
        if tech_mentions:
            dominant_tech = max(tech_mentions.items(), key=lambda x: len(x[1]))
            rules.append(WorldRule(
                rule_type='technological',
                description=f"World uses {dominant_tech[0].replace('_', ' ')}",
                established_scene=min(dominant_tech[1]) if dominant_tech[1] else 1,
                violations=[],
                consistency=1.0
            ))

        # Physical rules (gravity, physics)
        physics_normal = True
        for scene in scenes:
            for action in scene['action']:
                if any(word in action['text'].lower()
                      for word in ['floats', 'levitates', 'defies gravity']):
                    physics_normal = False
                    rules.append(WorldRule(
                        rule_type='physical',
                        description='Non-standard physics (anti-gravity or magic)',
                        established_scene=scene['scene_num'],
                        violations=[],
                        consistency=0.8
                    ))
                    break

        if physics_normal:
            rules.append(WorldRule(
                rule_type='physical',
                description='Standard Earth physics',
                established_scene=1,
                violations=[],
                consistency=1.0
            ))

        # Social rules
        social_indicators = {
            'formal': ['sir', 'madam', 'your majesty', 'lord', 'lady'],
            'casual': ['hey', 'dude', 'man', 'buddy'],
            'military': ['soldier', 'captain', 'general', 'sergeant']
        }

        for rule_name, indicators in social_indicators.items():
            for scene in scenes:
                for dialogue in scene['dialogue']:
                    if any(ind in dialogue['text'].lower() for ind in indicators):
                        rules.append(WorldRule(
                            rule_type='social',
                            description=f"{rule_name.capitalize()} social structure",
                            established_scene=scene['scene_num'],
                            violations=[],
                            consistency=0.9
                        ))
                        break

        return rules

    def _analyze_cultural_elements(self, scenes: List[Dict]) -> List[CulturalElement]:
        """Analyze cultural elements in the world."""
        cultural_elements = []

        # Customs and traditions
        custom_indicators = ['tradition', 'custom', 'ritual', 'ceremony', 'celebration']
        for scene in scenes:
            for action in scene['action']:
                text_lower = action['text'].lower()
                for indicator in custom_indicators:
                    if indicator in text_lower:
                        cultural_elements.append(CulturalElement(
                            element_type='custom',
                            description=action['text'],
                            scenes=[scene['scene_num']],
                            depth_score=0.7
                        ))

        # Beliefs and values
        belief_indicators = ['believe', 'faith', 'god', 'sacred', 'honor', 'duty']
        for scene in scenes:
            for dialogue in scene['dialogue']:
                text_lower = dialogue['text'].lower()
                for indicator in belief_indicators:
                    if indicator in text_lower:
                        cultural_elements.append(CulturalElement(
                            element_type='belief',
                            description=dialogue['text'],
                            scenes=[scene['scene_num']],
                            depth_score=0.8
                        ))

        # Food and cuisine
        food_mentions = []
        for scene in scenes:
            scene_text = ' '.join(a['text'] for a in scene['action'])
            if any(word in scene_text.lower()
                  for word in ['eat', 'drink', 'meal', 'food', 'restaurant', 'kitchen']):
                food_mentions.append(scene['scene_num'])

        if food_mentions:
            cultural_elements.append(CulturalElement(
                element_type='cuisine',
                description='Food/dining culture present',
                scenes=food_mentions,
                depth_score=0.5
            ))

        return cultural_elements

    def _create_world_map(self, locations: List[Location], scenes: List[Dict]) -> Dict[str, Any]:
        """Create a conceptual map of the world."""
        world_map = {
            'locations': {},
            'connections': [],
            'regions': []
        }

        # Map locations
        for location in locations:
            world_map['locations'][location.name] = {
                'type': location.location_type,
                'appearances': location.appearances,
                'atmosphere': location.atmosphere,
                'importance': len(location.appearances)
            }

        # Find connections (scenes that transition between locations)
        for i in range(len(scenes) - 1):
            current_loc = scenes[i]['location']
            next_loc = scenes[i + 1]['location']
            if current_loc and next_loc and current_loc != next_loc:
                world_map['connections'].append({
                    'from': current_loc,
                    'to': next_loc,
                    'scene_transition': f"{scenes[i]['scene_num']}->{scenes[i + 1]['scene_num']}"
                })

        # Group locations into regions (simplified)
        interior_locs = [l.name for l in locations if l.location_type == 'interior']
        exterior_locs = [l.name for l in locations if l.location_type == 'exterior']

        if interior_locs:
            world_map['regions'].append({
                'name': 'Interior Spaces',
                'locations': interior_locs
            })
        if exterior_locs:
            world_map['regions'].append({
                'name': 'Exterior Spaces',
                'locations': exterior_locs
            })

        return world_map

    def _build_world_timeline(self, scenes: List[Dict],
                             world_elements: List[WorldElement]) -> List[Dict[str, Any]]:
        """Build timeline of world revelation."""
        timeline = []

        for scene in scenes:
            scene_elements = [e for e in world_elements if e.scene_num == scene['scene_num']]

            if scene_elements:
                timeline.append({
                    'scene': scene['scene_num'],
                    'location': scene['location'],
                    'time': scene['time'],
                    'new_elements': len([e for e in scene_elements
                                       if e.element_type in ['location', 'technology']]),
                    'world_building': self._categorize_world_building(scene_elements)
                })

        return timeline

    def _categorize_world_building(self, elements: List[WorldElement]) -> str:
        """Categorize the type of world building in elements."""
        types = [e.element_type for e in elements]

        if 'location' in types:
            return 'spatial_expansion'
        elif 'technology' in types:
            return 'technological_reveal'
        elif 'environmental_visual' in types or 'atmospheric' in types:
            return 'atmospheric_deepening'
        else:
            return 'detail_enrichment'

    def _create_world_analysis(self, world_type: str, world_elements: List[WorldElement],
                              locations: List[Location], world_rules: List[WorldRule],
                              cultural_elements: List[CulturalElement],
                              scenes: List[Dict]) -> WorldAnalysis:
        """Create comprehensive world analysis."""
        # Establishment quality
        establishment_quality = self._calculate_establishment_quality(
            world_elements, scenes
        )

        # Consistency score
        consistency_score = self._calculate_consistency(
            locations, world_rules, world_elements
        )

        # Detail richness
        detail_richness = self._calculate_detail_richness(world_elements, scenes)

        # Cultural depth
        cultural_depth = min(len(cultural_elements) * 0.2, 1.0)

        # Geographic clarity
        geographic_clarity = self._calculate_geographic_clarity(locations)

        # Temporal consistency
        temporal_consistency = self._calculate_temporal_consistency(scenes)

        # Technological consistency
        technological_consistency = self._calculate_tech_consistency(world_rules)

        # Atmospheric coherence
        atmospheric_coherence = self._calculate_atmospheric_coherence(
            locations, world_elements
        )

        # World-story integration
        world_story_integration = self._calculate_story_integration(
            world_elements, scenes
        )

        return WorldAnalysis(
            world_type=world_type,
            establishment_quality=establishment_quality,
            consistency_score=consistency_score,
            detail_richness=detail_richness,
            cultural_depth=cultural_depth,
            geographic_clarity=geographic_clarity,
            temporal_consistency=temporal_consistency,
            technological_consistency=technological_consistency,
            atmospheric_coherence=atmospheric_coherence,
            world_story_integration=world_story_integration
        )

    def _calculate_establishment_quality(self, elements: List[WorldElement],
                                        scenes: List[Dict]) -> float:
        """Calculate how well the world is established."""
        if not scenes:
            return 0.0

        # Check if world is established early
        first_third = len(scenes) // 3
        early_elements = [e for e in elements if e.scene_num <= first_third]

        # Variety of element types
        element_types = set(e.element_type for e in early_elements)

        # Score based on early establishment and variety
        early_score = min(len(early_elements) * 0.1, 0.5)
        variety_score = min(len(element_types) * 0.1, 0.5)

        return early_score + variety_score

    def _calculate_consistency(self, locations: List[Location], rules: List[WorldRule],
                              elements: List[WorldElement]) -> float:
        """Calculate world consistency."""
        scores = []

        # Location consistency
        if locations:
            loc_consistency = sum(l.consistency for l in locations) / len(locations)
            scores.append(loc_consistency)

        # Rule consistency
        if rules:
            rule_consistency = sum(r.consistency for r in rules) / len(rules)
            scores.append(rule_consistency)

        # Element consistency
        if elements:
            elem_consistency = sum(e.consistency_score for e in elements) / len(elements)
            scores.append(elem_consistency)

        return sum(scores) / len(scores) if scores else 0.5

    def _calculate_detail_richness(self, elements: List[WorldElement],
                                  scenes: List[Dict]) -> float:
        """Calculate richness of world details."""
        if not scenes:
            return 0.0

        # Elements per scene
        elements_per_scene = len(elements) / len(scenes)

        # Variety of element types
        element_types = len(set(e.element_type for e in elements))

        # Environmental details
        environmental = sum(1 for e in elements
                          if 'environmental' in e.element_type or 'atmospheric' in e.element_type)

        # Calculate score
        density_score = min(elements_per_scene * 0.2, 0.4)
        variety_score = min(element_types * 0.1, 0.3)
        environmental_score = min(environmental * 0.05, 0.3)

        return density_score + variety_score + environmental_score

    def _calculate_geographic_clarity(self, locations: List[Location]) -> float:
        """Calculate geographic clarity."""
        if not locations:
            return 0.0

        # Check for repeated locations (helps establish geography)
        multi_appearance = sum(1 for l in locations if len(l.appearances) > 1)

        # Clear location types
        typed_locations = sum(1 for l in locations if l.location_type != 'unknown')

        # Score
        repeat_score = min(multi_appearance / len(locations), 0.5)
        type_score = typed_locations / len(locations) * 0.5

        return repeat_score + type_score

    def _calculate_temporal_consistency(self, scenes: List[Dict]) -> float:
        """Calculate temporal consistency."""
        if not scenes:
            return 0.0

        # Check time markers
        time_specified = sum(1 for s in scenes if s['time'] != 'UNSPECIFIED')

        # Check for time progression
        time_words = ['LATER', 'CONTINUOUS', 'MOMENTS LATER']
        progression_scenes = sum(1 for s in scenes
                               if any(word in s['time'] for word in time_words))

        # Score
        specification_score = time_specified / len(scenes) * 0.6
        progression_score = min(progression_scenes / len(scenes) * 2, 0.4)

        return specification_score + progression_score

    def _calculate_tech_consistency(self, rules: List[WorldRule]) -> float:
        """Calculate technological consistency."""
        tech_rules = [r for r in rules if r.rule_type == 'technological']

        if not tech_rules:
            return 0.7  # Neutral if no explicit tech rules

        # Check for violations
        total_violations = sum(len(r.violations) for r in tech_rules)

        if total_violations == 0:
            return 1.0
        else:
            return max(0.3, 1.0 - (total_violations * 0.2))

    def _calculate_atmospheric_coherence(self, locations: List[Location],
                                       elements: List[WorldElement]) -> float:
        """Calculate atmospheric coherence."""
        # Check location atmospheres
        if locations:
            atmosphere_types = set(l.atmosphere for l in locations if l.atmosphere != 'neutral')
            coherence = 1.0 if len(atmosphere_types) <= 2 else 0.5
        else:
            coherence = 0.5

        # Check atmospheric elements
        atmospheric_elements = [e for e in elements if e.element_type == 'atmospheric']
        if atmospheric_elements:
            coherence += min(len(atmospheric_elements) * 0.05, 0.5)

        return min(coherence, 1.0)

    def _calculate_story_integration(self, elements: List[WorldElement],
                                    scenes: List[Dict]) -> float:
        """Calculate world-story integration."""
        if not scenes or not elements:
            return 0.0

        # Check if world elements appear throughout story
        scene_coverage = len(set(e.scene_num for e in elements)) / len(scenes)

        # Check if world building serves narrative
        # (Simplified: more elements in dramatic scenes)
        dramatic_scenes = []
        for scene in scenes:
            if len(scene['dialogue']) > 3 or len(scene['action']) > 5:
                dramatic_scenes.append(scene['scene_num'])

        if dramatic_scenes:
            dramatic_elements = sum(1 for e in elements if e.scene_num in dramatic_scenes)
            narrative_integration = dramatic_elements / len(elements)
        else:
            narrative_integration = 0.5

        return scene_coverage * 0.5 + narrative_integration * 0.5

    def _analyze_depth_layers(self, elements: List[WorldElement], locations: List[Location],
                            cultural: List[CulturalElement]) -> Dict[str, float]:
        """Analyze different layers of world depth."""
        layers = {
            'physical': 0.0,
            'social': 0.0,
            'cultural': 0.0,
            'historical': 0.0,
            'atmospheric': 0.0
        }

        # Physical layer (locations, environment)
        if locations:
            layers['physical'] = min(len(locations) * 0.1, 1.0)

        # Social layer
        social_elements = [e for e in elements
                          if any(word in e.description.lower()
                                for word in ['people', 'crowd', 'society', 'community'])]
        layers['social'] = min(len(social_elements) * 0.2, 1.0)

        # Cultural layer
        layers['cultural'] = min(len(cultural) * 0.2, 1.0)

        # Historical layer (references to past)
        historical_refs = [e for e in elements
                          if any(word in e.description.lower()
                                for word in ['ancient', 'historical', 'past', 'tradition'])]
        layers['historical'] = min(len(historical_refs) * 0.3, 1.0)

        # Atmospheric layer
        atmospheric = [e for e in elements if 'atmospheric' in e.element_type]
        layers['atmospheric'] = min(len(atmospheric) * 0.15, 1.0)

        return layers

    def _check_rules(self, analysis: WorldAnalysis, elements: List[WorldElement],
                    locations: List[Location], rules: List[WorldRule]) -> List[Dict[str, Any]]:
        """Check screenplay against world building rules."""
        violations = []

        for rule in self.rules_config['rules']:
            violation = self._check_single_rule(rule, analysis, elements, locations, rules)
            if violation:
                violations.append(violation)

        return violations

    def _check_single_rule(self, rule: Dict, analysis: WorldAnalysis,
                          elements: List[WorldElement], locations: List[Location],
                          world_rules: List[WorldRule]) -> Optional[Dict]:
        """Check a single rule."""
        passed = True
        details = ""

        rule_id = rule['id']

        if rule_id == 'WOR.R001':  # World Establishment
            passed = analysis.establishment_quality >= 0.6
            details = f"Establishment quality: {analysis.establishment_quality:.2f}"

        elif rule_id == 'WOR.R002':  # Internal Consistency
            passed = analysis.consistency_score >= 0.7
            details = f"Consistency: {analysis.consistency_score:.2f}"

        elif rule_id == 'WOR.R003':  # Environmental Detail
            passed = analysis.detail_richness >= 0.5
            details = f"Detail richness: {analysis.detail_richness:.2f}"

        elif rule_id == 'WOR.R004':  # Cultural Depth
            passed = analysis.cultural_depth >= 0.3
            details = f"Cultural depth: {analysis.cultural_depth:.2f}"

        elif rule_id == 'WOR.R005':  # Geography Clarity
            passed = analysis.geographic_clarity >= 0.5
            details = f"Geographic clarity: {analysis.geographic_clarity:.2f}"

        elif rule_id == 'WOR.R006':  # Time Period Definition
            passed = analysis.temporal_consistency >= 0.6
            details = f"Temporal consistency: {analysis.temporal_consistency:.2f}"

        elif rule_id == 'WOR.R007':  # Technology Level
            passed = analysis.technological_consistency >= 0.7
            details = f"Tech consistency: {analysis.technological_consistency:.2f}"

        elif rule_id == 'WOR.R012':  # Atmospheric Coherence
            passed = analysis.atmospheric_coherence >= 0.6
            details = f"Atmospheric coherence: {analysis.atmospheric_coherence:.2f}"

        elif rule_id == 'WOR.R015':  # World-Story Integration
            passed = analysis.world_story_integration >= 0.5
            details = f"Story integration: {analysis.world_story_integration:.2f}"

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

    def _generate_recommendations(self, analysis: WorldAnalysis, elements: List[WorldElement],
                                 locations: List[Location],
                                 violations: List[Dict]) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []

        # Establishment
        if analysis.establishment_quality < 0.6:
            recommendations.append(
                "Establish world parameters more clearly in opening scenes"
            )

        # Consistency
        if analysis.consistency_score < 0.7:
            recommendations.append(
                "Ensure world rules remain consistent throughout screenplay"
            )

        # Detail richness
        if analysis.detail_richness < 0.5:
            recommendations.append(
                "Add more specific environmental and sensory details"
            )

        # Cultural depth
        if analysis.cultural_depth < 0.4:
            recommendations.append(
                "Develop unique cultural elements to enrich the world"
            )

        # Geographic clarity
        if analysis.geographic_clarity < 0.5:
            recommendations.append(
                "Clarify spatial relationships between locations"
            )

        # Atmospheric coherence
        if analysis.atmospheric_coherence < 0.6:
            recommendations.append(
                "Maintain consistent atmospheric tone across scenes"
            )

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            recommendations.append(
                f"Address critical world building issue: {critical_violations[0]['message']}"
            )

        return recommendations[:6]  # Top 6 recommendations

    def _calculate_score(self, analysis: WorldAnalysis, violations: List[Dict]) -> int:
        """Calculate overall world building score."""
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

        # Bonus for excellent world building
        if analysis.consistency_score >= 0.9:
            score += 5
        if analysis.detail_richness >= 0.8:
            score += 5
        if analysis.world_story_integration >= 0.8:
            score += 5

        return max(0, min(100, score))

    def _calculate_immersion(self, elements: List[WorldElement],
                           locations: List[Location]) -> float:
        """Calculate immersion score."""
        immersion = 0.0

        # Sensory details contribute to immersion
        sensory_elements = [e for e in elements
                           if any(sense in e.element_type
                                 for sense in ['visual', 'auditory', 'tactile', 'olfactory'])]
        immersion += min(len(sensory_elements) * 0.05, 0.4)

        # Atmospheric elements
        atmospheric = [e for e in elements if e.element_type == 'atmospheric']
        immersion += min(len(atmospheric) * 0.1, 0.3)

        # Recurring locations (familiarity)
        if locations:
            recurring = sum(1 for l in locations if len(l.appearances) > 1)
            immersion += min(recurring / len(locations) * 0.3, 0.3)

        return immersion

    def _calculate_believability(self, world_rules: List[WorldRule],
                               analysis: WorldAnalysis) -> float:
        """Calculate world believability."""
        believability = analysis.consistency_score * 0.5

        # Check rule violations
        if world_rules:
            total_violations = sum(len(r.violations) for r in world_rules)
            if total_violations == 0:
                believability += 0.3
            else:
                believability += max(0, 0.3 - total_violations * 0.1)

        # Logical coherence
        believability += analysis.technological_consistency * 0.2

        return min(believability, 1.0)

    def _calculate_uniqueness(self, elements: List[WorldElement],
                            cultural: List[CulturalElement]) -> float:
        """Calculate world uniqueness."""
        uniqueness = 0.5  # Base score

        # Unique element combinations
        element_types = set(e.element_type for e in elements)
        if len(element_types) >= 5:
            uniqueness += 0.2

        # Cultural elements add uniqueness
        if cultural:
            uniqueness += min(len(cultural) * 0.1, 0.3)

        return min(uniqueness, 1.0)