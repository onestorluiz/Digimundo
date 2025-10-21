#!/usr/bin/env python3
"""
Script Doctor Tonemon - Tone Consistency Specialist
Analyzes tonal consistency, mood management, and atmospheric unity in screenplays.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import re
import yaml
from pathlib import Path
from collections import Counter
import statistics


@dataclass
class ToneMarker:
    """Represents a tonal element in the screenplay."""
    tone_type: str  # dramatic, comedic, suspenseful, etc.
    intensity: float  # 0.0 to 1.0
    scene_num: int
    context: str  # dialogue, action, scene_heading
    text: str
    line_num: int
    

@dataclass
class ToneAnalysis:
    """Results from tone consistency analysis."""
    dominant_tone: Optional[str] = None
    secondary_tones: List[str] = field(default_factory=list)
    tone_consistency_score: float = 0.0
    tone_established: bool = False
    tone_shifts: int = 0
    smooth_transitions: int = 0
    jarring_transitions: int = 0
    emotional_range_score: float = 0.0
    genre_alignment_score: float = 0.0
    dialogue_tone_match: float = 0.0
    action_tone_match: float = 0.0
    atmospheric_consistency: float = 0.0
    climax_intensity: float = 0.0
    resolution_satisfaction: float = 0.0
    pacing_tone_alignment: float = 0.0
    

@dataclass
class ToneResult:
    """Complete tone consistency analysis result."""
    score: int
    specialist: Dict[str, str]
    tone_analysis: ToneAnalysis
    tone_markers: List[ToneMarker]
    scene_tones: Dict[int, Dict[str, float]]  # scene -> tone types & intensities
    tone_progression: List[Dict[str, Any]]  # How tone evolves
    tone_transitions: List[Dict[str, Any]]  # Transitions between tones
    emotional_arc: Dict[str, Any]  # Emotional journey
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]
    tone_map: Dict[str, float]  # Overall tone distribution
    

class DrTone:
    """Script Doctor Tonemon - Tone Consistency Specialist."""

    def __init__(self):
        """Initialize the tone consistency specialist."""
        self.name = "Script Doctor Tonemon"
        self.specialty = "Tone Consistency"
        self.load_rules()
        
        # Tone indicators by type
        self.tone_indicators = {
            'dramatic': {
                'words': ['serious', 'tense', 'grave', 'intense', 'heavy', 'solemn', 'profound'],
                'actions': ['stares', 'freezes', 'trembles', 'collapses', 'confronts'],
                'dialogue': ['truth', 'consequences', 'fate', 'destiny', 'sacrifice']
            },
            'comedic': {
                'words': ['laughs', 'chuckles', 'giggles', 'funny', 'absurd', 'ridiculous', 'hilarious'],
                'actions': ['trips', 'stumbles', 'bumbles', 'pratfall', 'slapstick'],
                'dialogue': ['joke', 'kidding', 'hilarious', 'funny', 'laugh']
            },
            'suspenseful': {
                'words': ['creeps', 'lurks', 'shadows', 'mysterious', 'ominous', 'eerie', 'unsettling'],
                'actions': ['prowls', 'stalks', 'hides', 'watches', 'waits'],
                'dialogue': ['careful', 'danger', 'watch out', 'something\'s wrong', 'too quiet']
            },
            'romantic': {
                'words': ['love', 'passion', 'tender', 'gentle', 'soft', 'warm', 'intimate'],
                'actions': ['embraces', 'kisses', 'caresses', 'holds', 'gazes'],
                'dialogue': ['love', 'heart', 'forever', 'always', 'soul']
            },
            'action': {
                'words': ['explosive', 'crashes', 'speeds', 'races', 'fights', 'battles', 'adrenaline'],
                'actions': ['jumps', 'dives', 'rolls', 'punches', 'kicks', 'shoots'],
                'dialogue': ['move', 'go', 'now', 'run', 'get down']
            },
            'horror': {
                'words': ['terrifying', 'horror', 'nightmare', 'blood', 'scream', 'monster', 'evil'],
                'actions': ['screams', 'flees', 'hides', 'shudders', 'gasps'],
                'dialogue': ['help', 'no', 'please', 'god', 'monster']
            },
            'melancholic': {
                'words': ['sad', 'lonely', 'lost', 'empty', 'hollow', 'grief', 'sorrow'],
                'actions': ['sighs', 'weeps', 'slumps', 'stares', 'withdraws'],
                'dialogue': ['miss', 'gone', 'lost', 'remember', 'used to']
            },
            'lighthearted': {
                'words': ['bright', 'cheerful', 'playful', 'breezy', 'carefree', 'sunny', 'upbeat'],
                'actions': ['skips', 'bounces', 'dances', 'whistles', 'hums'],
                'dialogue': ['great', 'wonderful', 'perfect', 'fun', 'awesome']
            }
        }
        
        # Genre expectations
        self.genre_tones = {
            'drama': ['dramatic', 'melancholic', 'serious'],
            'comedy': ['comedic', 'lighthearted'],
            'thriller': ['suspenseful', 'dramatic', 'action'],
            'horror': ['horror', 'suspenseful', 'dramatic'],
            'romance': ['romantic', 'dramatic', 'lighthearted'],
            'action': ['action', 'dramatic', 'suspenseful']
        }
        
    def load_rules(self):
        """Load rules from YAML configuration."""
        rules_path = Path(__file__).parent.parent / 'rules' / 'tone_consistency_rules.yaml'
        try:
            with open(rules_path, 'r') as f:
                self.rules_config = yaml.safe_load(f)
                self.rules = self.rules_config.get('rules', [])
        except FileNotFoundError:
            self.rules = []
            self.rules_config = {}
            
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """Analyze screenplay for tone consistency."""
        lines = screenplay_text.split('\n')
        
        # Extract structural elements
        scenes = self._extract_scenes(lines)
        dialogue = self._extract_dialogue(lines)
        action_lines = self._extract_action_lines(lines)
        
        # Identify tone markers
        tone_markers = self._identify_tone_markers(scenes, dialogue, action_lines)
        
        # Analyze scene tones
        scene_tones = self._analyze_scene_tones(tone_markers, scenes)
        
        # Analyze tone progression
        tone_progression = self._analyze_tone_progression(scene_tones, scenes)
        
        # Analyze tone transitions
        tone_transitions = self._analyze_transitions(scene_tones, scenes)
        
        # Analyze emotional arc
        emotional_arc = self._analyze_emotional_arc(tone_markers, scenes)
        
        # Create tone map
        tone_map = self._create_tone_map(tone_markers)
        
        # Perform tone analysis
        tone_analysis = self._perform_tone_analysis(
            tone_markers, scene_tones, tone_transitions, emotional_arc, scenes
        )
        
        # Check rules
        violations = self._check_rule_violations(
            tone_analysis, tone_transitions, emotional_arc
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            tone_analysis, violations, tone_transitions
        )
        
        # Calculate score
        score = self._calculate_score(tone_analysis, violations)
        
        return {
            "score": score,
            "specialist": {
                "name": self.name,
                "specialty": self.specialty,
                "identity": "Script Doctor™ first, Digimon tone specialist second"
            },
            "tone_analysis": tone_analysis,
            "tone_markers": tone_markers,
            "scene_tones": scene_tones,
            "tone_progression": tone_progression,
            "tone_transitions": tone_transitions,
            "emotional_arc": emotional_arc,
            "recommendations": recommendations,
            "rule_violations": violations,
            "tone_map": tone_map,
            "diagnosis": self._generate_diagnosis(tone_analysis, violations, tone_map)
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
        
    def _extract_dialogue(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract dialogue from screenplay."""
        dialogue_blocks = []
        current_character = None
        current_dialogue = []
        dialogue_start = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Character name
            if stripped and stripped.isupper() and not any(
                keyword in stripped for keyword in ['INT.', 'EXT.', 'FADE', 'CUT']
            ):
                if current_character and current_dialogue:
                    dialogue_blocks.append({
                        'character': current_character,
                        'dialogue': ' '.join(current_dialogue),
                        'line_num': dialogue_start
                    })
                current_character = stripped.split('(')[0].strip()
                current_dialogue = []
                dialogue_start = i + 1
                
            # Dialogue line
            elif current_character and stripped and not stripped.startswith('('):
                current_dialogue.append(stripped)
                
            # End of dialogue
            elif not stripped and current_character and current_dialogue:
                dialogue_blocks.append({
                    'character': current_character,
                    'dialogue': ' '.join(current_dialogue),
                    'line_num': dialogue_start
                })
                current_character = None
                current_dialogue = []
                
        # Don't forget last dialogue
        if current_character and current_dialogue:
            dialogue_blocks.append({
                'character': current_character,
                'dialogue': ' '.join(current_dialogue),
                'line_num': dialogue_start
            })
            
        return dialogue_blocks
        
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
                
            # Skip character names and parentheticals
            if (stripped and stripped.isupper() and len(stripped.split()) <= 3) or \
               (stripped.startswith('(') and stripped.endswith(')')):
                if in_action and current_action:
                    action_lines.append({
                        'text': ' '.join(current_action),
                        'line_num': action_start
                    })
                in_action = False
                current_action = []
                continue
                
            # This is action
            if stripped and not in_action:
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
        
    def _identify_tone_markers(self,
                               scenes: List[Dict[str, Any]],
                               dialogue: List[Dict[str, Any]],
                               action_lines: List[Dict[str, Any]]) -> List[ToneMarker]:
        """Identify tone markers throughout the screenplay."""
        markers = []
        
        # Analyze action lines for tone
        for action in action_lines:
            text_lower = action['text'].lower()
            scene_num = self._find_scene_for_line(action['line_num'], scenes)
            
            for tone_type, indicators in self.tone_indicators.items():
                intensity = 0.0
                
                # Check words
                for word in indicators['words']:
                    if word in text_lower:
                        intensity += 0.2
                        
                # Check actions
                for action_word in indicators['actions']:
                    if action_word in text_lower:
                        intensity += 0.3
                        
                if intensity > 0:
                    markers.append(ToneMarker(
                        tone_type=tone_type,
                        intensity=min(intensity, 1.0),
                        scene_num=scene_num,
                        context='action',
                        text=action['text'][:100],
                        line_num=action['line_num']
                    ))
                    
        # Analyze dialogue for tone
        for dial in dialogue:
            text_lower = dial['dialogue'].lower()
            scene_num = self._find_scene_for_line(dial['line_num'], scenes)
            
            for tone_type, indicators in self.tone_indicators.items():
                intensity = 0.0
                
                # Check dialogue keywords
                for word in indicators['dialogue']:
                    if word in text_lower:
                        intensity += 0.25
                        
                # Check general words too
                for word in indicators['words']:
                    if word in text_lower:
                        intensity += 0.15
                        
                if intensity > 0:
                    markers.append(ToneMarker(
                        tone_type=tone_type,
                        intensity=min(intensity, 1.0),
                        scene_num=scene_num,
                        context='dialogue',
                        text=dial['dialogue'][:100],
                        line_num=dial['line_num']
                    ))
                    
        # Analyze scene headings for atmospheric tone
        for scene in scenes:
            heading_lower = scene['heading'].lower()
            
            # Night scenes tend toward dramatic/suspenseful
            if 'night' in heading_lower:
                markers.append(ToneMarker(
                    tone_type='dramatic',
                    intensity=0.3,
                    scene_num=scene['scene_num'],
                    context='scene_heading',
                    text=scene['heading'],
                    line_num=scene['line_start']
                ))
                
            # Specific locations suggest tones
            if 'cemetery' in heading_lower or 'graveyard' in heading_lower:
                markers.append(ToneMarker(
                    tone_type='melancholic',
                    intensity=0.4,
                    scene_num=scene['scene_num'],
                    context='scene_heading',
                    text=scene['heading'],
                    line_num=scene['line_start']
                ))
                
        return markers
        
    def _find_scene_for_line(self, line_num: int, scenes: List[Dict[str, Any]]) -> int:
        """Find which scene a line belongs to."""
        for scene in scenes:
            if scene['line_start'] <= line_num <= scene['line_end']:
                return scene['scene_num']
        return 0
        
    def _analyze_scene_tones(self,
                            tone_markers: List[ToneMarker],
                            scenes: List[Dict[str, Any]]) -> Dict[int, Dict[str, float]]:
        """Analyze the tone of each scene."""
        scene_tones = {}
        
        for scene in scenes:
            scene_num = scene['scene_num']
            scene_tones[scene_num] = {}
            
            # Aggregate tone markers for this scene
            scene_markers = [m for m in tone_markers if m.scene_num == scene_num]
            
            for marker in scene_markers:
                if marker.tone_type not in scene_tones[scene_num]:
                    scene_tones[scene_num][marker.tone_type] = 0.0
                scene_tones[scene_num][marker.tone_type] += marker.intensity
                
            # Normalize intensities
            total_intensity = sum(scene_tones[scene_num].values())
            if total_intensity > 0:
                for tone_type in scene_tones[scene_num]:
                    scene_tones[scene_num][tone_type] /= total_intensity
                    
        return scene_tones
        
    def _analyze_tone_progression(self,
                                 scene_tones: Dict[int, Dict[str, float]],
                                 scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze how tone progresses through the screenplay."""
        progression = []
        
        for scene in scenes:
            scene_num = scene['scene_num']
            tones = scene_tones.get(scene_num, {})
            
            if tones:
                dominant = max(tones.items(), key=lambda x: x[1])
                progression.append({
                    'scene': scene_num,
                    'dominant_tone': dominant[0],
                    'intensity': dominant[1],
                    'all_tones': tones
                })
            else:
                progression.append({
                    'scene': scene_num,
                    'dominant_tone': 'neutral',
                    'intensity': 0.0,
                    'all_tones': {}
                })
                
        return progression
        
    def _analyze_transitions(self,
                            scene_tones: Dict[int, Dict[str, float]],
                            scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze transitions between different tones."""
        transitions = []
        
        for i in range(len(scenes) - 1):
            current_scene = scenes[i]['scene_num']
            next_scene = scenes[i + 1]['scene_num']
            
            current_tones = scene_tones.get(current_scene, {})
            next_tones = scene_tones.get(next_scene, {})
            
            if current_tones and next_tones:
                current_dominant = max(current_tones.items(), key=lambda x: x[1])[0] if current_tones else 'neutral'
                next_dominant = max(next_tones.items(), key=lambda x: x[1])[0] if next_tones else 'neutral'
                
                if current_dominant != next_dominant:
                    # Calculate transition smoothness
                    smoothness = self._calculate_transition_smoothness(
                        current_dominant, next_dominant, current_tones, next_tones
                    )
                    
                    transitions.append({
                        'from_scene': current_scene,
                        'to_scene': next_scene,
                        'from_tone': current_dominant,
                        'to_tone': next_dominant,
                        'smoothness': smoothness,
                        'type': 'smooth' if smoothness > 0.5 else 'jarring'
                    })
                    
        return transitions
        
    def _calculate_transition_smoothness(self,
                                        from_tone: str,
                                        to_tone: str,
                                        from_tones: Dict[str, float],
                                        to_tones: Dict[str, float]) -> float:
        """Calculate how smooth a tone transition is."""
        # Compatible tone pairs
        compatible = {
            'dramatic': ['suspenseful', 'melancholic', 'action'],
            'comedic': ['lighthearted', 'romantic'],
            'suspenseful': ['dramatic', 'horror', 'action'],
            'romantic': ['dramatic', 'lighthearted', 'melancholic'],
            'action': ['suspenseful', 'dramatic'],
            'horror': ['suspenseful', 'dramatic'],
            'melancholic': ['dramatic', 'romantic'],
            'lighthearted': ['comedic', 'romantic']
        }
        
        # Check compatibility
        if to_tone in compatible.get(from_tone, []):
            smoothness = 0.7
        elif from_tone in compatible.get(to_tone, []):
            smoothness = 0.7
        else:
            smoothness = 0.3
            
        # Check if there's overlap in secondary tones
        overlap = set(from_tones.keys()) & set(to_tones.keys())
        if overlap:
            smoothness += 0.2
            
        return min(smoothness, 1.0)
        
    def _analyze_emotional_arc(self,
                              tone_markers: List[ToneMarker],
                              scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the emotional arc of the screenplay."""
        if not scenes:
            return {'type': 'flat', 'intensity_curve': []}
            
        # Calculate emotional intensity per scene
        intensity_curve = []
        
        for scene in scenes:
            scene_markers = [m for m in tone_markers if m.scene_num == scene['scene_num']]
            
            # Calculate average intensity
            if scene_markers:
                avg_intensity = statistics.mean([m.intensity for m in scene_markers])
            else:
                avg_intensity = 0.0
                
            intensity_curve.append(avg_intensity)
            
        # Determine arc type
        if not intensity_curve:
            arc_type = 'flat'
        else:
            first_third = statistics.mean(intensity_curve[:len(intensity_curve)//3] or [0])
            middle_third = statistics.mean(intensity_curve[len(intensity_curve)//3:2*len(intensity_curve)//3] or [0])
            final_third = statistics.mean(intensity_curve[2*len(intensity_curve)//3:] or [0])
            
            if final_third > middle_third > first_third:
                arc_type = 'rising'
            elif first_third > middle_third > final_third:
                arc_type = 'falling'
            elif middle_third > first_third and middle_third > final_third:
                arc_type = 'peaked'
            else:
                arc_type = 'variable'
                
        return {
            'type': arc_type,
            'intensity_curve': intensity_curve,
            'first_third': first_third if 'first_third' in locals() else 0,
            'middle_third': middle_third if 'middle_third' in locals() else 0,
            'final_third': final_third if 'final_third' in locals() else 0
        }
        
    def _create_tone_map(self, tone_markers: List[ToneMarker]) -> Dict[str, float]:
        """Create overall tone distribution map."""
        tone_map = {}
        
        for marker in tone_markers:
            if marker.tone_type not in tone_map:
                tone_map[marker.tone_type] = 0.0
            tone_map[marker.tone_type] += marker.intensity
            
        # Normalize
        total = sum(tone_map.values())
        if total > 0:
            for tone_type in tone_map:
                tone_map[tone_type] /= total
                
        return tone_map
        
    def _perform_tone_analysis(self,
                              tone_markers: List[ToneMarker],
                              scene_tones: Dict[int, Dict[str, float]],
                              tone_transitions: List[Dict[str, Any]],
                              emotional_arc: Dict[str, Any],
                              scenes: List[Dict[str, Any]]) -> ToneAnalysis:
        """Perform comprehensive tone analysis."""
        analysis = ToneAnalysis()
        
        # Determine dominant tone
        tone_map = self._create_tone_map(tone_markers)
        if tone_map:
            analysis.dominant_tone = max(tone_map.items(), key=lambda x: x[1])[0]
            analysis.secondary_tones = [t for t, v in tone_map.items() 
                                       if t != analysis.dominant_tone and v > 0.1]
            
        # Check if tone is established early
        early_scenes = list(scene_tones.keys())[:3]
        if early_scenes:
            early_tones = []
            for scene_num in early_scenes:
                if scene_tones[scene_num]:
                    dominant = max(scene_tones[scene_num].items(), key=lambda x: x[1])[0]
                    early_tones.append(dominant)
            if early_tones and early_tones.count(analysis.dominant_tone) >= 2:
                analysis.tone_established = True
                
        # Calculate consistency
        if scene_tones:
            scene_dominant_tones = []
            for scene_num, tones in scene_tones.items():
                if tones:
                    dominant = max(tones.items(), key=lambda x: x[1])[0]
                    scene_dominant_tones.append(dominant)
                    
            if scene_dominant_tones and analysis.dominant_tone:
                consistency = scene_dominant_tones.count(analysis.dominant_tone) / len(scene_dominant_tones)
                analysis.tone_consistency_score = consistency
                
        # Count tone shifts
        analysis.tone_shifts = len(tone_transitions)
        analysis.smooth_transitions = sum(1 for t in tone_transitions if t['smoothness'] > 0.5)
        analysis.jarring_transitions = analysis.tone_shifts - analysis.smooth_transitions
        
        # Calculate emotional range
        if emotional_arc['intensity_curve']:
            intensities = emotional_arc['intensity_curve']
            if max(intensities) > 0:
                analysis.emotional_range_score = (max(intensities) - min(intensities)) / max(intensities)
                
        # Calculate climax intensity (last quarter)
        if emotional_arc['intensity_curve']:
            last_quarter = emotional_arc['intensity_curve'][-(len(emotional_arc['intensity_curve'])//4):]
            if last_quarter:
                analysis.climax_intensity = statistics.mean(last_quarter)
                
        # Resolution satisfaction (based on arc type)
        if emotional_arc['type'] in ['rising', 'peaked']:
            analysis.resolution_satisfaction = 0.7
        elif emotional_arc['type'] == 'variable':
            analysis.resolution_satisfaction = 0.5
        else:
            analysis.resolution_satisfaction = 0.3
            
        # These would need more sophisticated analysis
        analysis.genre_alignment_score = 0.6  # Simplified
        analysis.dialogue_tone_match = 0.7  # Simplified
        analysis.action_tone_match = 0.7  # Simplified
        analysis.atmospheric_consistency = analysis.tone_consistency_score
        analysis.pacing_tone_alignment = 0.6  # Simplified
        
        return analysis
        
    def _check_rule_violations(self,
                              analysis: ToneAnalysis,
                              transitions: List[Dict[str, Any]],
                              emotional_arc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for rule violations."""
        violations = []
        
        for rule in self.rules:
            if self._evaluate_rule(rule, analysis, transitions, emotional_arc):
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
                      analysis: ToneAnalysis,
                      transitions: List[Dict[str, Any]],
                      emotional_arc: Dict[str, Any]) -> bool:
        """Evaluate if a rule is violated."""
        rule_id = rule['id']
        
        # Established Tone
        if rule_id == 'TON.R001':
            return not analysis.tone_established
            
        # Tone Consistency
        elif rule_id == 'TON.R002':
            return analysis.tone_consistency_score < 0.5
            
        # Genre-Appropriate Tone
        elif rule_id == 'TON.R003':
            return analysis.genre_alignment_score < 0.5
            
        # Tonal Transitions
        elif rule_id == 'TON.R004':
            return analysis.jarring_transitions > analysis.smooth_transitions
            
        # Dialogue Tone Match
        elif rule_id == 'TON.R005':
            return analysis.dialogue_tone_match < 0.5
            
        # Action Tone Match
        elif rule_id == 'TON.R006':
            return analysis.action_tone_match < 0.5
            
        # Emotional Tone Range
        elif rule_id == 'TON.R007':
            return analysis.emotional_range_score < 0.2
            
        # Comic Relief Balance
        elif rule_id == 'TON.R008':
            # Check if comedy undermines drama
            if analysis.dominant_tone == 'dramatic' and 'comedic' in analysis.secondary_tones:
                return len([t for t in transitions if t['to_tone'] == 'comedic']) > 3
            return False
            
        # Tonal Stakes
        elif rule_id == 'TON.R009':
            # Check if tone matches stakes (simplified)
            return analysis.climax_intensity < 0.5
            
        # Atmospheric Consistency
        elif rule_id == 'TON.R010':
            return analysis.atmospheric_consistency < 0.5
            
        # Tonal Climax
        elif rule_id == 'TON.R011':
            return analysis.climax_intensity < 0.6
            
        # Resolution Tone
        elif rule_id == 'TON.R012':
            return analysis.resolution_satisfaction < 0.4
            
        # Subgenre Tone Mix
        elif rule_id == 'TON.R013':
            # Check for incompatible tone combinations
            if 'horror' in analysis.secondary_tones and 'comedic' in analysis.secondary_tones:
                return True
            return False
            
        # Visual Tone Cues
        elif rule_id == 'TON.R014':
            # This would need visual analysis
            return False
            
        # Pacing Supports Tone
        elif rule_id == 'TON.R015':
            return analysis.pacing_tone_alignment < 0.5
            
        return False
        
    def _generate_recommendations(self,
                                 analysis: ToneAnalysis,
                                 violations: List[Dict[str, Any]],
                                 transitions: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Address critical violations first
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        for violation in critical_violations[:2]:
            recommendations.append(f"CRITICAL: {violation['fix']}")
            
        # Check establishment
        if not analysis.tone_established:
            recommendations.append(
                "Establish the dominant tone clearly in opening scenes"
            )
            
        # Check consistency
        if analysis.tone_consistency_score < 0.5:
            recommendations.append(
                "Improve tonal consistency throughout the screenplay"
            )
            
        # Check transitions
        if analysis.jarring_transitions > analysis.smooth_transitions:
            recommendations.append(
                "Smooth jarring tonal transitions with bridging elements"
            )
            
        # Check emotional range
        if analysis.emotional_range_score < 0.2:
            recommendations.append(
                "Vary emotional intensity to avoid monotonous tone"
            )
            
        # Check climax
        if analysis.climax_intensity < 0.6:
            recommendations.append(
                "Intensify tone approaching climax for greater impact"
            )
            
        # Check resolution
        if analysis.resolution_satisfaction < 0.4:
            recommendations.append(
                "Ensure resolution tone satisfies story promises"
            )
            
        # Check for too many tone shifts
        if analysis.tone_shifts > len(transitions) * 0.7:
            recommendations.append(
                "Reduce frequent tone shifts for better coherence"
            )
            
        return recommendations[:7]  # Limit to 7 recommendations
        
    def _calculate_score(self,
                        analysis: ToneAnalysis,
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
            
        # Bonus for good tone management
        if analysis.tone_established:
            base_score += 5
            
        if analysis.tone_consistency_score > 0.7:
            base_score += 5
            
        if analysis.smooth_transitions > analysis.jarring_transitions:
            base_score += 5
            
        if analysis.emotional_range_score > 0.5:
            base_score += 3
            
        if analysis.climax_intensity > 0.7:
            base_score += 5
            
        if analysis.resolution_satisfaction > 0.6:
            base_score += 3
            
        # Penalty for too many tone shifts
        if analysis.tone_shifts > 10:
            base_score -= 5

        return max(5, min(95, base_score))

    def _generate_diagnosis(self, tone_analysis: ToneAnalysis,
                          violations: List[Dict[str, Any]],
                          tone_map: Dict[str, float]) -> str:
        """Generate narrative tone diagnosis."""
        score = self._calculate_score(tone_analysis, violations)
        diagnosis = f"Tone Analysis Score: {score}/100\n\n"

        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent tonal consistency! Your screenplay maintains a unified, professional tone. "
        elif score >= 70:
            diagnosis += "Good tonal foundation with some areas needing refinement. "
        elif score >= 50:
            diagnosis += "Tone issues are impacting the screenplay's coherence. "
        else:
            diagnosis += "Significant tonal problems that will affect audience immersion. "

        # Dominant tone
        if tone_analysis.dominant_tone:
            diagnosis += f"Dominant tone: {tone_analysis.dominant_tone}. "
        else:
            diagnosis += "WARNING: No clear dominant tone - screenplay lacks tonal identity. "

        # Establishment
        if not tone_analysis.tone_established:
            diagnosis += "Tone not clearly established in opening. "

        # Consistency
        if tone_analysis.tone_consistency_score >= 0.8:
            diagnosis += "Excellent tonal consistency throughout. "
        elif tone_analysis.tone_consistency_score >= 0.6:
            diagnosis += "Moderate consistency - some tonal variations. "
        else:
            diagnosis += "Inconsistent tone - shifts undermine narrative unity. "

        # Transitions
        if tone_analysis.jarring_transitions > 0:
            diagnosis += f"WARNING: {tone_analysis.jarring_transitions} jarring tonal shifts. "
        elif tone_analysis.smooth_transitions > 5:
            diagnosis += "Smooth tonal transitions maintain flow. "

        # Genre alignment
        if tone_analysis.genre_alignment_score >= 0.7:
            diagnosis += "Tone well-aligned with genre expectations. "
        elif tone_analysis.genre_alignment_score < 0.5:
            diagnosis += "Tone misaligned with genre - adjust to match conventions. "

        # Emotional range
        if tone_analysis.emotional_range_score < 0.3:
            diagnosis += "Monotonous emotional tone - add variation within framework. "
        elif tone_analysis.emotional_range_score > 0.7:
            diagnosis += "Good emotional range creates dynamic experience. "

        # Climax intensity
        if tone_analysis.climax_intensity < 0.5:
            diagnosis += "WARNING: Tone flat through climax - needs intensification. "

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            diagnosis += f"\n\nCRITICAL ISSUES ({len(critical_violations)}): "
            for v in critical_violations[:2]:
                diagnosis += f"{v['title']}. "

        return diagnosis.strip()
