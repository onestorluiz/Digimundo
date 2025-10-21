#!/usr/bin/env python3
"""
Script Doctor Motifmon - Visual Motifs Specialist
Analyzes recurring visual elements and patterns in screenplays.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import re
import yaml
from pathlib import Path
from collections import Counter
import statistics


@dataclass
class VisualMotif:
    """Represents a visual motif."""
    name: str
    motif_type: str  # object, color, lighting, weather, movement, etc.
    occurrences: List[Dict[str, Any]] = field(default_factory=list)
    first_appearance: Optional[int] = None
    last_appearance: Optional[int] = None
    frequency: float = 0.0
    consistency_score: float = 0.0
    evolution: List[str] = field(default_factory=list)
    thematic_connection: float = 0.0
    emotional_weight: float = 0.0
    cinematic_impact: float = 0.0
    

@dataclass
class MotifAnalysis:
    """Results from visual motif analysis."""
    total_motifs: int = 0
    established_motifs: int = 0
    recurring_motifs: int = 0
    object_motifs: int = 0
    color_motifs: int = 0
    lighting_motifs: int = 0
    weather_motifs: int = 0
    movement_motifs: int = 0
    motif_density: float = 0.0
    consistency_score: float = 0.0
    evolution_score: float = 0.0
    cinematic_potential: float = 0.0
    thematic_alignment: float = 0.0
    has_bookends: bool = False
    payoff_score: float = 0.0
    

@dataclass
class MotifResult:
    """Complete visual motif analysis result."""
    score: int
    specialist: Dict[str, str]
    motif_analysis: MotifAnalysis
    visual_motifs: List[VisualMotif]
    motif_patterns: Dict[str, List[int]]  # Motif name -> scene numbers
    character_motifs: Dict[str, List[str]]  # Character -> associated motifs
    scene_motifs: Dict[int, List[str]]  # Scene number -> motifs present
    motif_relationships: Dict[str, List[str]]  # Motif connections
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]
    motif_timeline: List[Dict[str, Any]]
    

class DrVisualMotifs:
    """Script Doctor Motifmon - Visual Motifs Specialist."""
    
    def __init__(self):
        """Initialize the visual motifs specialist."""
        self.name = "Script Doctor Motifmon"
        self.specialty = "Visual Motifs"
        self.load_rules()
        
        # Common visual motif patterns to look for
        self.object_patterns = [
            r'\b(mirror|window|door|clock|watch|key|lock|photograph|letter|book)s?\b',
            r'\b(ring|necklace|bracelet|pendant|jewelry)\b',
            r'\b(knife|gun|sword|weapon)s?\b',
            r'\b(flower|rose|tree|plant)s?\b',
            r'\b(mask|veil|hood|disguise)s?\b'
        ]
        
        self.color_patterns = [
            r'\b(red|crimson|scarlet|ruby)\b',
            r'\b(blue|azure|sapphire|navy)\b',
            r'\b(green|emerald|jade|forest)\b',
            r'\b(black|dark|shadow|ebony)\b',
            r'\b(white|pale|ivory|snow)\b',
            r'\b(gold|golden|amber|yellow)\b',
            r'\b(silver|gray|grey|steel)\b'
        ]
        
        self.lighting_patterns = [
            r'\b(light|lights|lighting|lit|illuminat\w+)\b',
            r'\b(dark|darkness|shadow|shadows|shade)\b',
            r'\b(bright|dim|glow|gleam|shine)\b',
            r'\b(candle|lamp|flashlight|torch)s?\b',
            r'\b(sun|sunlight|moonlight|starlight)\b'
        ]
        
        self.weather_patterns = [
            r'\b(rain|raining|rainy|downpour)\b',
            r'\b(snow|snowing|snowfall|blizzard)\b',
            r'\b(storm|thunder|lightning|tempest)\b',
            r'\b(fog|mist|haze|foggy|misty)\b',
            r'\b(wind|windy|breeze|gust)\b',
            r'\b(sun|sunny|sunshine|clear)\b'
        ]
        
        self.movement_patterns = [
            r'\b(circle|circular|circling|round)\b',
            r'\b(spiral|spiraling|spinning|whirl)\b',
            r'\b(ascend|ascending|rise|rising|climb)\b',
            r'\b(descend|descending|fall|falling|drop)\b',
            r'\b(forward|backward|advance|retreat)\b'
        ]
        
    def load_rules(self):
        """Load rules from YAML configuration."""
        rules_path = Path(__file__).parent.parent / 'rules' / 'visual_motifs_rules.yaml'
        try:
            with open(rules_path, 'r') as f:
                self.rules_config = yaml.safe_load(f)
                self.rules = self.rules_config.get('rules', [])
        except FileNotFoundError:
            self.rules = []
            self.rules_config = {}
            
    def _generate_diagnosis(self, score: int, analysis: MotifAnalysis,
                           num_motifs: int, violations: List[Dict]) -> str:
        """Generate diagnosis based on visual motifs analysis."""
        diagnosis_parts = []

        if score >= 85:
            diagnosis_parts.append("✅ EXCELLENT visual motifs - strong cinematic language.")
        elif score >= 70:
            diagnosis_parts.append("👍 GOOD visual motifs with room for enhancement.")
        elif score >= 50:
            diagnosis_parts.append("⚠️  ADEQUATE motifs but significant improvements needed.")
        else:
            diagnosis_parts.append("❌ WEAK visual motifs - lacking cinematic depth.")

        # Motif establishment
        if analysis.established_motifs < 3:
            diagnosis_parts.append(f"Only {analysis.established_motifs} established motifs (need 3+)")

        # Motif recurrence
        if analysis.recurring_motifs < 2:
            diagnosis_parts.append(f"Only {analysis.recurring_motifs} recurring motifs")

        # Motif density
        if analysis.motif_density < 0.5:
            diagnosis_parts.append(f"⚠️  Low motif density ({analysis.motif_density:.2f})")
        elif analysis.motif_density > 3.0:
            diagnosis_parts.append(f"⚠️  Over-saturated with motifs ({analysis.motif_density:.1f}/scene)")

        # Consistency
        if analysis.consistency_score < 0.6:
            diagnosis_parts.append(f"Motif consistency is low ({analysis.consistency_score:.2f})")

        # Evolution
        if analysis.evolution_score < 0.5:
            diagnosis_parts.append("Motifs are static - they don't evolve with story")

        # Cinematic potential
        if analysis.cinematic_potential < 0.6:
            diagnosis_parts.append(f"Cinematic impact is weak ({analysis.cinematic_potential:.2f})")

        # Thematic alignment
        if analysis.thematic_alignment < 0.5:
            diagnosis_parts.append("Motifs lack thematic connection")

        # Bookends
        if not analysis.has_bookends:
            diagnosis_parts.append("Missing visual bookends between opening and closing")

        # Payoff
        if analysis.payoff_score < 0.5:
            diagnosis_parts.append(f"Motif payoff is weak ({analysis.payoff_score:.2f})")

        # Critical violations
        critical_violations = [v for v in violations if v.get('severity') == 'critical']
        if critical_violations:
            diagnosis_parts.append(f"🚨 {len(critical_violations)} critical issues")

        return " ".join(diagnosis_parts)

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """Analyze screenplay for visual motifs."""
        lines = screenplay_text.split('\n')
        
        # Extract structural elements
        scenes = self._extract_scenes(lines)
        action_lines = self._extract_action_lines(lines)
        
        # Identify visual motifs
        visual_motifs = self._identify_visual_motifs(scenes, action_lines)
        
        # Analyze motif patterns
        motif_patterns = self._analyze_motif_patterns(visual_motifs, scenes)
        
        # Map character associations
        character_motifs = self._map_character_motifs(visual_motifs, scenes)
        
        # Map scene motifs
        scene_motifs = self._map_scene_motifs(visual_motifs, scenes)
        
        # Analyze motif relationships
        motif_relationships = self._analyze_motif_relationships(visual_motifs, scenes)
        
        # Create motif timeline
        motif_timeline = self._create_motif_timeline(visual_motifs, scenes)
        
        # Perform analysis
        motif_analysis = self._analyze_motifs(
            visual_motifs, scenes, motif_patterns
        )
        
        # Check rules
        violations = self._check_rule_violations(
            motif_analysis, visual_motifs, motif_patterns
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            motif_analysis, violations, visual_motifs
        )
        
        # Calculate score
        score = self._calculate_score(motif_analysis, violations)

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, motif_analysis, len(visual_motifs), violations
        )

        # Convert visual_motifs to dicts
        visual_motifs_dict = [
            {
                'name': motif.name,
                'motif_type': motif.motif_type,
                'occurrences': motif.occurrences,
                'first_appearance': motif.first_appearance,
                'last_appearance': motif.last_appearance,
                'frequency': motif.frequency,
                'consistency_score': motif.consistency_score,
                'evolution': motif.evolution,
                'thematic_connection': motif.thematic_connection,
                'emotional_weight': motif.emotional_weight,
                'cinematic_impact': motif.cinematic_impact
            } for motif in visual_motifs
        ]

        return {
            'score': score,
            'specialist': {
                "name": self.name,
                "specialty": self.specialty,
                "identity": "Script Doctor™ first, Digimon visual motifs specialist second"
            },
            # Flatten MotifAnalysis fields
            'total_motifs': motif_analysis.total_motifs,
            'established_motifs': motif_analysis.established_motifs,
            'recurring_motifs': motif_analysis.recurring_motifs,
            'object_motifs': motif_analysis.object_motifs,
            'color_motifs': motif_analysis.color_motifs,
            'lighting_motifs': motif_analysis.lighting_motifs,
            'weather_motifs': motif_analysis.weather_motifs,
            'movement_motifs': motif_analysis.movement_motifs,
            'motif_density': motif_analysis.motif_density,
            'consistency_score': motif_analysis.consistency_score,
            'evolution_score': motif_analysis.evolution_score,
            'cinematic_potential': motif_analysis.cinematic_potential,
            'thematic_alignment': motif_analysis.thematic_alignment,
            'has_bookends': motif_analysis.has_bookends,
            'payoff_score': motif_analysis.payoff_score,
            # Other fields
            'visual_motifs': visual_motifs_dict,
            'motif_patterns': motif_patterns,
            'character_motifs': character_motifs,
            'scene_motifs': scene_motifs,
            'motif_relationships': motif_relationships,
            'recommendations': recommendations,
            'rule_violations': violations,
            'motif_timeline': motif_timeline,
            'diagnosis': diagnosis
        }
        
    def _extract_scenes(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract scenes from screenplay."""
        scenes = []
        current_scene = None
        scene_content = []
        scene_num = 0
        
        for i, line in enumerate(lines):
            if any(line.strip().startswith(prefix) for prefix in ['INT.', 'EXT.']):
                if current_scene:
                    scenes.append({
                        'heading': current_scene,
                        'content': '\n'.join(scene_content),
                        'line_start': current_scene_start,
                        'line_end': i - 1,
                        'scene_num': scene_num
                    })
                    scene_num += 1
                current_scene = line.strip()
                current_scene_start = i
                scene_content = []
            elif current_scene:
                scene_content.append(line)
                
        # Don't forget last scene
        if current_scene:
            scenes.append({
                'heading': current_scene,
                'content': '\n'.join(scene_content),
                'line_start': current_scene_start,
                'line_end': len(lines) - 1,
                'scene_num': scene_num
            })
            
        return scenes
        
    def _extract_action_lines(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract action lines from screenplay."""
        action_lines = []
        in_action = False
        current_action = []
        action_start = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip scene headings and transitions
            if any(stripped.startswith(prefix) for prefix in 
                  ['INT.', 'EXT.', 'FADE', 'CUT']):
                if in_action and current_action:
                    action_lines.append({
                        'text': ' '.join(current_action),
                        'line_num': action_start
                    })
                in_action = False
                current_action = []
                continue
                
            # Skip character names and dialogue
            if stripped and stripped.isupper() and len(stripped.split()) <= 3:
                if in_action and current_action:
                    action_lines.append({
                        'text': ' '.join(current_action),
                        'line_num': action_start
                    })
                in_action = False
                current_action = []
                continue
                
            # Skip parentheticals and dialogue
            if stripped.startswith('(') or (current_action == [] and not in_action and stripped and not stripped[0].isupper()):
                continue
                
            # This looks like action
            if stripped and not in_action:
                # Check it's not dialogue (rough heuristic)
                is_dialogue = False
                for j in range(max(0, i-2), i):
                    if j < len(lines):
                        prev_line = lines[j].strip()
                        if prev_line.isupper() and len(prev_line.split()) <= 3:
                            is_dialogue = True
                            break

                if not is_dialogue:
                    in_action = True
                    action_start = i
                    current_action = [stripped]
            elif stripped and in_action:
                current_action.append(stripped)
            elif not stripped and in_action:
                if current_action:
                    action_lines.append({
                        'text': ' '.join(current_action),
                        'line_num': action_start
                    })
                in_action = False
                current_action = []
                
        # Don't forget last action
        if in_action and current_action:
            action_lines.append({
                'text': ' '.join(current_action),
                'line_num': action_start
            })
            
        return action_lines
        
    def _identify_visual_motifs(self,
                               scenes: List[Dict[str, Any]],
                               action_lines: List[Dict[str, Any]]) -> List[VisualMotif]:
        """Identify visual motifs in the screenplay."""
        motifs = []
        motif_candidates = {}
        
        # Search for object motifs
        for pattern in self.object_patterns:
            self._find_motif_pattern(pattern, 'object', scenes, action_lines, motif_candidates)
            
        # Search for color motifs
        for pattern in self.color_patterns:
            self._find_motif_pattern(pattern, 'color', scenes, action_lines, motif_candidates)
            
        # Search for lighting motifs
        for pattern in self.lighting_patterns:
            self._find_motif_pattern(pattern, 'lighting', scenes, action_lines, motif_candidates)
            
        # Search for weather motifs
        for pattern in self.weather_patterns:
            self._find_motif_pattern(pattern, 'weather', scenes, action_lines, motif_candidates)
            
        # Search for movement motifs
        for pattern in self.movement_patterns:
            self._find_motif_pattern(pattern, 'movement', scenes, action_lines, motif_candidates)
            
        # Convert candidates to motifs (only keep recurring ones)
        for key, occurrences in motif_candidates.items():
            if len(occurrences) >= 2:  # Must appear at least twice
                name, motif_type = key
                motif = VisualMotif(
                    name=name,
                    motif_type=motif_type,
                    occurrences=occurrences
                )
                
                # Calculate properties
                scene_nums = [occ['scene_num'] for occ in occurrences if 'scene_num' in occ]
                if scene_nums:
                    motif.first_appearance = min(scene_nums)
                    motif.last_appearance = max(scene_nums)
                    motif.frequency = len(occurrences) / len(scenes) if scenes else 0
                    
                # Calculate consistency
                motif.consistency_score = self._calculate_consistency(motif, scenes)
                
                # Analyze evolution
                motif.evolution = self._analyze_evolution(motif, scenes)
                
                # Calculate impact scores
                motif.cinematic_impact = self._calculate_cinematic_impact(motif)
                motif.emotional_weight = self._calculate_emotional_weight(motif)
                motif.thematic_connection = self._calculate_thematic_connection(motif)
                
                motifs.append(motif)
                
        return motifs
        
    def _find_motif_pattern(self,
                           pattern: str,
                           motif_type: str,
                           scenes: List[Dict[str, Any]],
                           action_lines: List[Dict[str, Any]],
                           candidates: Dict[Tuple[str, str], List[Dict[str, Any]]]):
        """Find occurrences of a motif pattern."""
        regex = re.compile(pattern, re.IGNORECASE)
        
        # Search in action lines
        for action in action_lines:
            matches = regex.findall(action['text'])
            for match in matches:
                # Normalize the match
                if isinstance(match, tuple):
                    match = match[0]
                match = match.lower()
                
                # Find which scene this belongs to
                scene_num = self._find_scene_for_line(action['line_num'], scenes)
                
                key = (match, motif_type)
                if key not in candidates:
                    candidates[key] = []
                    
                candidates[key].append({
                    'text': action['text'][:100],
                    'line_num': action['line_num'],
                    'scene_num': scene_num,
                    'context': 'action'
                })
                
        # Also search in scene headings for location motifs
        for scene in scenes:
            matches = regex.findall(scene['heading'])
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                match = match.lower()
                
                key = (match, motif_type)
                if key not in candidates:
                    candidates[key] = []
                    
                candidates[key].append({
                    'text': scene['heading'],
                    'scene_num': scene['scene_num'],
                    'context': 'heading'
                })
                
    def _find_scene_for_line(self, line_num: int, scenes: List[Dict[str, Any]]) -> Optional[int]:
        """Find which scene a line belongs to."""
        for scene in scenes:
            if scene['line_start'] <= line_num <= scene['line_end']:
                return scene['scene_num']
        return None
        
    def _calculate_consistency(self, motif: VisualMotif, scenes: List[Dict[str, Any]]) -> float:
        """Calculate how consistently a motif is used."""
        if len(motif.occurrences) < 2:
            return 0.0
            
        # Check distribution
        scene_nums = [occ['scene_num'] for occ in motif.occurrences if occ.get('scene_num') is not None]
        if not scene_nums or not scenes:
            return 0.0
            
        # Calculate spread
        spread = (max(scene_nums) - min(scene_nums)) / len(scenes)
        
        # Calculate regularity (standard deviation of gaps)
        if len(scene_nums) > 2:
            sorted_scenes = sorted(scene_nums)
            gaps = [sorted_scenes[i+1] - sorted_scenes[i] for i in range(len(sorted_scenes)-1)]
            if gaps:
                avg_gap = statistics.mean(gaps)
                if avg_gap > 0:
                    std_dev = statistics.stdev(gaps) if len(gaps) > 1 else 0
                    regularity = 1 - min(std_dev / avg_gap, 1)
                else:
                    regularity = 1.0
            else:
                regularity = 0.5
        else:
            regularity = 0.5
            
        # Combine spread and regularity
        consistency = (spread * 0.5) + (regularity * 0.5)
        return min(consistency, 1.0)
        
    def _analyze_evolution(self, motif: VisualMotif, scenes: List[Dict[str, Any]]) -> List[str]:
        """Analyze how a motif evolves through the story."""
        evolution = []
        
        if not motif.occurrences:
            return evolution
            
        total_scenes = len(scenes)
        for i, occ in enumerate(motif.occurrences):
            scene_num = occ.get('scene_num', 0)
            
            # Determine story position
            if scene_num < total_scenes * 0.25:
                position = "Setup"
            elif scene_num < total_scenes * 0.5:
                position = "Development"
            elif scene_num < total_scenes * 0.75:
                position = "Complication"
            else:
                position = "Resolution"
                
            if not evolution or evolution[-1] != position:
                evolution.append(position)
                
        return evolution
        
    def _calculate_cinematic_impact(self, motif: VisualMotif) -> float:
        """Calculate the cinematic impact of a motif."""
        impact = 0.5  # Base impact
        
        # Visual motifs have higher impact
        if motif.motif_type in ['object', 'color', 'lighting']:
            impact += 0.2
            
        # Weather and movement are very cinematic
        if motif.motif_type in ['weather', 'movement']:
            impact += 0.3
            
        # Frequency adds impact
        impact += min(motif.frequency * 2, 0.2)
        
        return min(impact, 1.0)
        
    def _calculate_emotional_weight(self, motif: VisualMotif) -> float:
        """Calculate emotional weight of a motif."""
        emotional_words = [
            'tear', 'cry', 'smile', 'laugh', 'scream', 'whisper',
            'heart', 'soul', 'love', 'hate', 'fear', 'hope',
            'dark', 'light', 'shadow', 'bright', 'cold', 'warm'
        ]
        
        weight = 0.0
        motif_text = ' '.join(occ.get('text', '') for occ in motif.occurrences).lower()
        
        for word in emotional_words:
            if word in motif_text or word in motif.name:
                weight += 0.1
                
        # Colors often carry emotional weight
        if motif.motif_type == 'color':
            weight += 0.2
            
        # Weather is emotional
        if motif.motif_type == 'weather':
            weight += 0.3
            
        return min(weight, 1.0)
        
    def _calculate_thematic_connection(self, motif: VisualMotif) -> float:
        """Calculate how well a motif connects to potential themes."""
        # This is simplified - would need theme analysis for accuracy
        connection = 0.5  # Base connection
        
        # Recurring motifs likely have thematic purpose
        if len(motif.occurrences) > 3:
            connection += 0.2
            
        # Motifs that evolve are often thematic
        if len(motif.evolution) > 2:
            connection += 0.2
            
        # High consistency suggests thematic purpose
        connection += motif.consistency_score * 0.1
        
        return min(connection, 1.0)
        
    def _analyze_motif_patterns(self,
                               motifs: List[VisualMotif],
                               scenes: List[Dict[str, Any]]) -> Dict[str, List[int]]:
        """Analyze patterns of motif appearances."""
        patterns = {}
        
        for motif in motifs:
            scene_nums = [
                occ['scene_num'] for occ in motif.occurrences 
                if occ.get('scene_num') is not None
            ]
            patterns[motif.name] = sorted(scene_nums)
            
        return patterns
        
    def _map_character_motifs(self,
                              motifs: List[VisualMotif],
                              scenes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Map motifs to characters (simplified)."""
        # This would need character extraction for full implementation
        character_motifs = {}
        
        # For now, return empty dict
        # Full implementation would analyze which motifs appear with which characters
        
        return character_motifs
        
    def _map_scene_motifs(self,
                         motifs: List[VisualMotif],
                         scenes: List[Dict[str, Any]]) -> Dict[int, List[str]]:
        """Map which motifs appear in each scene."""
        scene_motifs = {}
        
        for scene in scenes:
            scene_num = scene['scene_num']
            scene_motifs[scene_num] = []
            
            for motif in motifs:
                for occ in motif.occurrences:
                    if occ.get('scene_num') == scene_num:
                        if motif.name not in scene_motifs[scene_num]:
                            scene_motifs[scene_num].append(motif.name)
                            
        return scene_motifs
        
    def _analyze_motif_relationships(self,
                                    motifs: List[VisualMotif],
                                    scenes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Analyze relationships between motifs."""
        relationships = {}
        
        # Find motifs that appear together
        for i, motif1 in enumerate(motifs):
            relationships[motif1.name] = []
            
            for j, motif2 in enumerate(motifs):
                if i != j:
                    # Check if they appear in same scenes
                    scenes1 = set(occ['scene_num'] for occ in motif1.occurrences 
                                 if occ.get('scene_num') is not None)
                    scenes2 = set(occ['scene_num'] for occ in motif2.occurrences 
                                 if occ.get('scene_num') is not None)
                    
                    overlap = len(scenes1 & scenes2)
                    if overlap >= 2:  # Appear together at least twice
                        relationships[motif1.name].append(motif2.name)
                        
        return relationships
        
    def _create_motif_timeline(self,
                              motifs: List[VisualMotif],
                              scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create a timeline of motif appearances."""
        timeline = []
        
        for motif in motifs:
            for occ in motif.occurrences:
                if occ.get('scene_num') is not None:
                    timeline.append({
                        'scene': occ['scene_num'],
                        'motif': motif.name,
                        'type': motif.motif_type,
                        'context': occ.get('context', 'unknown')
                    })
                    
        # Sort by scene number
        timeline.sort(key=lambda x: x['scene'])
        
        return timeline
        
    def _analyze_motifs(self,
                       motifs: List[VisualMotif],
                       scenes: List[Dict[str, Any]],
                       patterns: Dict[str, List[int]]) -> MotifAnalysis:
        """Analyze overall motif usage."""
        analysis = MotifAnalysis()
        
        analysis.total_motifs = len(motifs)
        
        # Count established motifs (appear in first quarter)
        first_quarter = len(scenes) * 0.25
        analysis.established_motifs = sum(
            1 for m in motifs 
            if m.first_appearance is not None and m.first_appearance < first_quarter
        )
        
        # Count recurring motifs (3+ appearances)
        analysis.recurring_motifs = sum(1 for m in motifs if len(m.occurrences) >= 3)
        
        # Count by type
        for motif in motifs:
            if motif.motif_type == 'object':
                analysis.object_motifs += 1
            elif motif.motif_type == 'color':
                analysis.color_motifs += 1
            elif motif.motif_type == 'lighting':
                analysis.lighting_motifs += 1
            elif motif.motif_type == 'weather':
                analysis.weather_motifs += 1
            elif motif.motif_type == 'movement':
                analysis.movement_motifs += 1
                
        # Calculate density
        if scenes:
            analysis.motif_density = analysis.total_motifs / len(scenes)
            
        # Calculate average consistency
        if motifs:
            consistencies = [m.consistency_score for m in motifs]
            analysis.consistency_score = statistics.mean(consistencies)
            
        # Calculate evolution score
        evolving_motifs = sum(1 for m in motifs if len(m.evolution) > 2)
        if motifs:
            analysis.evolution_score = evolving_motifs / len(motifs)
            
        # Calculate cinematic potential
        if motifs:
            impacts = [m.cinematic_impact for m in motifs]
            analysis.cinematic_potential = statistics.mean(impacts)
            
        # Calculate thematic alignment
        if motifs:
            connections = [m.thematic_connection for m in motifs]
            analysis.thematic_alignment = statistics.mean(connections)
            
        # Check for bookends
        analysis.has_bookends = self._check_bookends(motifs, scenes)
        
        # Calculate payoff
        analysis.payoff_score = self._calculate_payoff(motifs, scenes)
        
        return analysis
        
    def _check_bookends(self, motifs: List[VisualMotif], scenes: List[Dict[str, Any]]) -> bool:
        """Check if there are visual bookends."""
        if not motifs or len(scenes) < 2:
            return False
            
        first_scene = 0
        last_scene = len(scenes) - 1
        
        for motif in motifs:
            scene_nums = [occ['scene_num'] for occ in motif.occurrences 
                         if occ.get('scene_num') is not None]
            if first_scene in scene_nums and last_scene in scene_nums:
                return True
                
        return False
        
    def _calculate_payoff(self, motifs: List[VisualMotif], scenes: List[Dict[str, Any]]) -> float:
        """Calculate if motifs have payoff in resolution."""
        if not motifs or not scenes:
            return 0.0
            
        last_quarter_start = len(scenes) * 0.75
        
        motifs_with_payoff = 0
        for motif in motifs:
            # Check if motif appears in last quarter
            final_appearances = [
                occ for occ in motif.occurrences 
                if occ.get('scene_num', 0) >= last_quarter_start
            ]
            if final_appearances:
                motifs_with_payoff += 1
                
        return motifs_with_payoff / len(motifs) if motifs else 0.0
        
    def _check_rule_violations(self,
                              analysis: MotifAnalysis,
                              motifs: List[VisualMotif],
                              patterns: Dict[str, List[int]]) -> List[Dict[str, Any]]:
        """Check for rule violations."""
        violations = []
        
        for rule in self.rules:
            if self._evaluate_rule(rule, analysis, motifs, patterns):
                violations.append({
                    'rule_id': rule['id'],
                    'title': rule['title'],
                    'severity': rule['severity'],
                    'message': rule.get('fail_msg', 'Rule violation'),
                    'fix': rule.get('fix', 'No fix available')
                })
                
        return violations
        
    def _evaluate_rule(self,
                      rule: Dict[str, Any],
                      analysis: MotifAnalysis,
                      motifs: List[VisualMotif],
                      patterns: Dict[str, List[int]]) -> bool:
        """Evaluate if a rule is violated."""
        rule_id = rule['id']
        
        # Established Visual Motifs
        if rule_id == 'MOT.R001':
            return analysis.established_motifs == 0 and analysis.total_motifs > 0
            
        # Motif Recurrence
        elif rule_id == 'MOT.R002':
            return analysis.recurring_motifs < analysis.total_motifs * 0.5
            
        # Visual Consistency
        elif rule_id == 'MOT.R003':
            return analysis.consistency_score < 0.5
            
        # Thematic Connection
        elif rule_id == 'MOT.R004':
            return analysis.thematic_alignment < 0.4
            
        # Character Motifs
        elif rule_id == 'MOT.R005':
            # Simplified - would need character analysis
            return False
            
        # Motif Evolution
        elif rule_id == 'MOT.R006':
            return analysis.evolution_score < 0.3
            
        # Visual Bookends
        elif rule_id == 'MOT.R007':
            return not analysis.has_bookends and analysis.total_motifs > 3
            
        # Motif Density Balance
        elif rule_id == 'MOT.R008':
            return analysis.motif_density > 2.0 or \
                   (analysis.motif_density < 0.2 and analysis.total_motifs > 0)
            
        # Cinematic Potential
        elif rule_id == 'MOT.R009':
            return analysis.cinematic_potential < 0.5
            
        # Motif Clarity
        elif rule_id == 'MOT.R010':
            # Would need more sophisticated clarity analysis
            return False
            
        # Emotional Motifs
        elif rule_id == 'MOT.R011':
            if motifs:
                emotional_weights = [m.emotional_weight for m in motifs]
                avg_weight = statistics.mean(emotional_weights)
                return avg_weight < 0.3
            return False
            
        # Transition Motifs
        elif rule_id == 'MOT.R012':
            # Would need transition analysis
            return False
            
        # Color Motifs
        elif rule_id == 'MOT.R013':
            return analysis.color_motifs == 0 and analysis.total_motifs > 3
            
        # Object Motifs
        elif rule_id == 'MOT.R014':
            return analysis.object_motifs == 0
            
        # Motif Payoff
        elif rule_id == 'MOT.R015':
            return analysis.payoff_score < 0.3
            
        return False
        
    def _generate_recommendations(self,
                                 analysis: MotifAnalysis,
                                 violations: List[Dict[str, Any]],
                                 motifs: List[VisualMotif]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Address critical violations first
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        for violation in critical_violations[:2]:
            recommendations.append(f"CRITICAL: {violation['fix']}")
            
        # Check establishment
        if analysis.established_motifs == 0 and analysis.total_motifs > 0:
            recommendations.append(
                "Establish key visual motifs in the opening scenes"
            )
            
        # Check recurrence
        if analysis.recurring_motifs < analysis.total_motifs * 0.5:
            recommendations.append(
                "Ensure visual motifs recur meaningfully throughout"
            )
            
        # Check consistency
        if analysis.consistency_score < 0.5:
            recommendations.append(
                "Improve consistency of motif presentation"
            )
            
        # Check evolution
        if analysis.evolution_score < 0.3:
            recommendations.append(
                "Let visual motifs evolve with the story"
            )
            
        # Check bookends
        if not analysis.has_bookends and analysis.total_motifs > 3:
            recommendations.append(
                "Create visual bookends by echoing opening motifs at the end"
            )
            
        # Check density
        if analysis.motif_density > 2.0:
            recommendations.append(
                "Reduce motif density - focus on fewer, stronger motifs"
            )
        elif analysis.motif_density < 0.2:
            recommendations.append(
                "Consider adding more visual motifs to enrich the narrative"
            )
            
        # Check payoff
        if analysis.payoff_score < 0.3:
            recommendations.append(
                "Ensure visual motifs have meaningful payoff in resolution"
            )
            
        return recommendations[:7]  # Limit to 7 recommendations
        
    def _calculate_score(self,
                        analysis: MotifAnalysis,
                        violations: List[Dict[str, Any]]) -> int:
        """Calculate overall score."""
        base_score = 90
        
        # Deduct for violations
        severity_penalties = {
            'critical': 15,
            'high': 10,
            'medium': 5,
            'low': 2
        }
        
        for violation in violations:
            base_score -= severity_penalties.get(violation['severity'], 0)
            
        # Bonus for good motif usage
        if analysis.established_motifs > 0:
            base_score += 3
            
        if analysis.recurring_motifs >= analysis.total_motifs * 0.6:
            base_score += 5
            
        if analysis.consistency_score > 0.7:
            base_score += 5
            
        if analysis.has_bookends:
            base_score += 5
            
        if analysis.payoff_score > 0.5:
            base_score += 5
            
        if analysis.cinematic_potential > 0.7:
            base_score += 5
            
        # Penalty for poor density
        if analysis.motif_density > 2.0 or analysis.motif_density < 0.1:
            base_score -= 5
            
        return max(5, min(95, base_score))
