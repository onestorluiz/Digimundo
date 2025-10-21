#!/usr/bin/env python3
"""
Script Doctor Thememon - Theme Consistency Specialist
Analyzes thematic unity, development, and expression throughout the screenplay.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import re
import yaml
from pathlib import Path
from collections import Counter


@dataclass
class ThematicElement:
    """Represents a thematic element in the screenplay."""
    theme: str
    occurrences: List[Dict[str, Any]] = field(default_factory=list)
    strength: float = 0.0
    consistency: float = 0.0
    

@dataclass 
class ThemeAnalysis:
    """Results from theme consistency analysis."""
    central_theme: Optional[str] = None
    central_theme_strength: float = 0.0
    supporting_themes: List[str] = field(default_factory=list)
    theme_consistency_score: float = 0.0
    thematic_depth: int = 0
    theme_expression_methods: Dict[str, int] = field(default_factory=dict)
    theme_plot_alignment: float = 0.0
    theme_character_alignment: float = 0.0
    opposing_viewpoints_present: bool = False
    theme_resolved: bool = False
    heavy_handed_score: float = 0.0  # 0 = subtle, 1 = preachy
    

@dataclass
class ThemeResult:
    """Complete theme consistency analysis result."""
    score: int
    specialist: Dict[str, str]
    theme_analysis: ThemeAnalysis
    thematic_elements: List[ThematicElement]
    act_themes: Dict[str, List[str]]
    character_themes: Dict[str, List[str]]
    scene_theme_density: Dict[str, float]
    thematic_conflicts: List[Dict[str, Any]]
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]
    theme_progression: Dict[str, Any]
    

class DrTheme:
    """Script Doctor Thememon - Theme Consistency Specialist."""

    def __init__(self):
        """Initialize the theme consistency specialist."""
        self.name = "Script Doctor Thememon"
        self.specialty = "Theme Consistency"
        self.load_rules()
        
        # Common themes and related keywords
        self.theme_keywords = {
            'redemption': ['forgive', 'redeem', 'second chance', 'atone', 'mistake', 'past'],
            'love': ['love', 'heart', 'together', 'care', 'devotion', 'romance'],
            'power': ['control', 'power', 'authority', 'dominance', 'strength', 'rule'],
            'identity': ['who', 'self', 'identity', 'become', 'true', 'real'],
            'family': ['family', 'father', 'mother', 'son', 'daughter', 'home'],
            'sacrifice': ['sacrifice', 'give up', 'cost', 'price', 'lose', 'choice'],
            'justice': ['justice', 'right', 'wrong', 'fair', 'law', 'truth'],
            'freedom': ['free', 'freedom', 'liberty', 'escape', 'prison', 'chains'],
            'revenge': ['revenge', 'vengeance', 'payback', 'retribution', 'even'],
            'survival': ['survive', 'live', 'death', 'danger', 'threat', 'fight'],
            'ambition': ['ambition', 'success', 'achieve', 'goal', 'dream', 'win'],
            'corruption': ['corrupt', 'greed', 'betray', 'lie', 'cheat', 'steal'],
            'loyalty': ['loyal', 'faithful', 'trust', 'betray', 'stand by', 'true'],
            'courage': ['brave', 'courage', 'fear', 'stand up', 'fight', 'face'],
            'truth': ['truth', 'lie', 'honest', 'secret', 'reveal', 'hidden']
        }
        
        # Heavy-handed indicators
        self.preachy_indicators = [
            'the moral is', 'the lesson is', 'what this means is',
            'the point is', 'you see,', 'obviously', 'clearly',
            'as you know', 'remember that', 'never forget',
            'always remember', 'the truth is', 'in conclusion'
        ]
        
    def load_rules(self):
        """Load rules from YAML configuration."""
        rules_path = Path(__file__).parent.parent / 'rules' / 'theme_consistency_rules.yaml'
        try:
            with open(rules_path, 'r') as f:
                self.rules_config = yaml.safe_load(f)
                self.rules = self.rules_config.get('rules', [])
        except FileNotFoundError:
            self.rules = []
            self.rules_config = {}
            
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """Analyze screenplay for theme consistency."""
        lines = screenplay_text.split('\n')
        
        # Extract structural elements
        scenes = self._extract_scenes(lines)
        dialogue = self._extract_dialogue(lines)
        characters = self._extract_characters(lines)
        acts = self._identify_acts(scenes)
        
        # Identify themes
        thematic_elements = self._identify_themes(screenplay_text, scenes, dialogue)
        
        # Perform theme analysis
        theme_analysis = self._analyze_themes(
            thematic_elements, scenes, dialogue, characters
        )
        
        # Analyze theme distribution
        act_themes = self._analyze_act_themes(acts, thematic_elements)
        character_themes = self._analyze_character_themes(characters, dialogue, thematic_elements)
        scene_density = self._calculate_scene_theme_density(scenes, thematic_elements)
        
        # Find thematic conflicts
        thematic_conflicts = self._identify_thematic_conflicts(thematic_elements, dialogue)
        
        # Analyze theme progression
        theme_progression = self._analyze_theme_progression(thematic_elements, scenes)
        
        # Check rules
        violations = self._check_rule_violations(
            theme_analysis, thematic_elements, act_themes, theme_progression
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            theme_analysis, violations, thematic_elements
        )
        
        # Calculate score
        score = self._calculate_score(theme_analysis, violations)
        
        return {
            "score": score,
            "specialist": {
                "name": self.name,
                "specialty": self.specialty,
                "identity": "Script Doctor™ first, Digimon theme specialist second"
            },
            "theme_analysis": theme_analysis,
            "thematic_elements": thematic_elements,
            "act_themes": act_themes,
            "character_themes": character_themes,
            "scene_theme_density": scene_density,
            "thematic_conflicts": thematic_conflicts,
            "recommendations": recommendations,
            "rule_violations": violations,
            "theme_progression": theme_progression,
            "diagnosis": self._generate_diagnosis(theme_analysis, violations)
        }
        
    def _extract_scenes(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract scenes from screenplay."""
        scenes = []
        current_scene = None
        scene_lines = []
        scene_num = 0
        
        for i, line in enumerate(lines):
            if any(line.strip().startswith(prefix) for prefix in ['INT.', 'EXT.']):
                if current_scene:
                    scenes.append({
                        'heading': current_scene,
                        'content': '\n'.join(scene_lines),
                        'line_start': current_scene_start,
                        'line_end': i - 1,
                        'scene_num': scene_num
                    })
                    scene_num += 1
                current_scene = line.strip()
                current_scene_start = i
                scene_lines = []
            elif current_scene:
                scene_lines.append(line)
                
        # Don't forget last scene
        if current_scene:
            scenes.append({
                'heading': current_scene,
                'content': '\n'.join(scene_lines),
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
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Character name
            if stripped and stripped.isupper() and not any(
                keyword in stripped for keyword in ['INT.', 'EXT.', 'FADE', 'CUT']
            ):
                # Save previous dialogue
                if current_character and current_dialogue:
                    dialogue_blocks.append({
                        'character': current_character,
                        'dialogue': ' '.join(current_dialogue),
                        'line_num': i
                    })
                    
                current_character = stripped.split('(')[0].strip()
                current_dialogue = []
                
            # Dialogue line
            elif current_character and stripped and not stripped.startswith('('):
                current_dialogue.append(stripped)
                
        # Don't forget last dialogue
        if current_character and current_dialogue:
            dialogue_blocks.append({
                'character': current_character,
                'dialogue': ' '.join(current_dialogue),
                'line_num': len(lines)
            })
            
        return dialogue_blocks
        
    def _extract_characters(self, lines: List[str]) -> Set[str]:
        """Extract unique character names."""
        characters = set()
        
        for line in lines:
            stripped = line.strip()
            if stripped and stripped.isupper() and not any(
                keyword in stripped for keyword in ['INT.', 'EXT.', 'FADE', 'CUT']
            ):
                character = stripped.split('(')[0].strip()
                characters.add(character)
                
        return characters
        
    def _identify_acts(self, scenes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Identify act structure based on scenes."""
        if not scenes:
            return {}
            
        total_scenes = len(scenes)
        
        # Simple three-act structure estimation
        act1_end = total_scenes // 4
        act2_end = (total_scenes * 3) // 4
        
        acts = {
            'act1': scenes[:act1_end],
            'act2': scenes[act1_end:act2_end],
            'act3': scenes[act2_end:]
        }
        
        return acts
        
    def _identify_themes(self, 
                        screenplay_text: str,
                        scenes: List[Dict[str, Any]],
                        dialogue: List[Dict[str, Any]]) -> List[ThematicElement]:
        """Identify thematic elements in the screenplay."""
        thematic_elements = []
        text_lower = screenplay_text.lower()
        
        # Check for each known theme
        for theme, keywords in self.theme_keywords.items():
            occurrences = []
            
            # Count keyword occurrences
            keyword_count = 0
            for keyword in keywords:
                keyword_count += text_lower.count(keyword.lower())
                
                # Find specific occurrences in dialogue
                for d in dialogue:
                    if keyword.lower() in d['dialogue'].lower():
                        occurrences.append({
                            'type': 'dialogue',
                            'character': d['character'],
                            'text': d['dialogue'][:100],
                            'keyword': keyword
                        })
                        
            if keyword_count > 2:  # Threshold for theme presence
                element = ThematicElement(
                    theme=theme,
                    occurrences=occurrences[:10],  # Limit occurrences
                    strength=min(keyword_count / 20, 1.0),  # Normalize strength
                    consistency=self._calculate_theme_consistency(occurrences, scenes)
                )
                thematic_elements.append(element)
                
        # Sort by strength
        thematic_elements.sort(key=lambda x: x.strength, reverse=True)
        
        return thematic_elements
        
    def _calculate_theme_consistency(self, 
                                     occurrences: List[Dict[str, Any]], 
                                     scenes: List[Dict[str, Any]]) -> float:
        """Calculate how consistently a theme appears."""
        if not occurrences or not scenes:
            return 0.0
            
        # Check distribution across screenplay
        scene_count = len(scenes)
        scenes_with_theme = len(set(occ.get('scene_num', 0) 
                                   for occ in occurrences 
                                   if 'scene_num' in occ))
        
        if scene_count > 0:
            distribution = scenes_with_theme / scene_count
        else:
            distribution = 0.0
            
        return min(distribution * 2, 1.0)  # Scale up but cap at 1.0
        
    def _analyze_themes(self,
                       thematic_elements: List[ThematicElement],
                       scenes: List[Dict[str, Any]],
                       dialogue: List[Dict[str, Any]],
                       characters: Set[str]) -> ThemeAnalysis:
        """Analyze overall thematic structure."""
        analysis = ThemeAnalysis()
        
        if not thematic_elements:
            return analysis
            
        # Identify central theme (strongest)
        analysis.central_theme = thematic_elements[0].theme
        analysis.central_theme_strength = thematic_elements[0].strength
        
        # Supporting themes
        if len(thematic_elements) > 1:
            analysis.supporting_themes = [el.theme for el in thematic_elements[1:4]]
            
        # Calculate consistency
        consistencies = [el.consistency for el in thematic_elements]
        if consistencies:
            analysis.theme_consistency_score = sum(consistencies) / len(consistencies)
            
        # Thematic depth (number of layered themes)
        analysis.thematic_depth = min(len(thematic_elements), 5)
        
        # Analyze expression methods
        analysis.theme_expression_methods = self._analyze_expression_methods(
            thematic_elements, scenes, dialogue
        )
        
        # Check alignments
        analysis.theme_plot_alignment = self._calculate_plot_alignment(
            thematic_elements, scenes
        )
        analysis.theme_character_alignment = self._calculate_character_alignment(
            thematic_elements, characters, dialogue
        )
        
        # Check for opposing viewpoints
        analysis.opposing_viewpoints_present = self._check_opposing_viewpoints(
            thematic_elements, dialogue
        )
        
        # Check if theme is resolved
        analysis.theme_resolved = self._check_theme_resolution(
            thematic_elements, scenes
        )
        
        # Calculate heavy-handedness
        analysis.heavy_handed_score = self._calculate_heavy_handedness(
            dialogue, thematic_elements
        )
        
        return analysis
        
    def _analyze_expression_methods(self,
                                    thematic_elements: List[ThematicElement],
                                    scenes: List[Dict[str, Any]],
                                    dialogue: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze how themes are expressed."""
        methods = {
            'dialogue': 0,
            'action': 0,
            'symbolism': 0,
            'conflict': 0,
            'character_choice': 0
        }
        
        for element in thematic_elements:
            for occ in element.occurrences:
                if occ.get('type') == 'dialogue':
                    methods['dialogue'] += 1
                elif occ.get('type') == 'action':
                    methods['action'] += 1
                elif occ.get('type') == 'symbol':
                    methods['symbolism'] += 1
                    
        # Look for thematic conflicts
        conflict_keywords = ['but', 'however', 'fight', 'argue', 'conflict', 'versus']
        for scene in scenes:
            if any(keyword in scene['content'].lower() for keyword in conflict_keywords):
                methods['conflict'] += 1
                
        # Look for character choices
        choice_keywords = ['choose', 'decide', 'choice', 'must', 'have to']
        for d in dialogue:
            if any(keyword in d['dialogue'].lower() for keyword in choice_keywords):
                methods['character_choice'] += 1
                
        return methods
        
    def _calculate_plot_alignment(self,
                                  thematic_elements: List[ThematicElement],
                                  scenes: List[Dict[str, Any]]) -> float:
        """Calculate how well plot aligns with themes."""
        if not thematic_elements or not scenes:
            return 0.0
            
        # Check if major plot points involve thematic elements
        major_scene_indices = [
            0,  # Opening
            len(scenes) // 4,  # Act 1 break
            len(scenes) // 2,  # Midpoint
            (len(scenes) * 3) // 4,  # Act 2 break
            len(scenes) - 1  # Ending
        ]
        
        theme_in_major_scenes = 0
        for idx in major_scene_indices:
            if idx < len(scenes):
                scene_content = scenes[idx]['content'].lower()
                for element in thematic_elements[:3]:  # Check top 3 themes
                    theme_keywords = self.theme_keywords.get(element.theme, [])
                    if any(kw.lower() in scene_content for kw in theme_keywords):
                        theme_in_major_scenes += 1
                        break
                        
        alignment = theme_in_major_scenes / len(major_scene_indices)
        return alignment
        
    def _calculate_character_alignment(self,
                                       thematic_elements: List[ThematicElement],
                                       characters: Set[str],
                                       dialogue: List[Dict[str, Any]]) -> float:
        """Calculate how well characters embody themes."""
        if not thematic_elements or not characters:
            return 0.0
            
        # Check how many characters engage with themes
        characters_with_themes = set()
        
        for element in thematic_elements:
            for occ in element.occurrences:
                if 'character' in occ:
                    characters_with_themes.add(occ['character'])
                    
        if len(characters) > 0:
            alignment = len(characters_with_themes) / len(characters)
        else:
            alignment = 0.0
            
        return min(alignment * 1.5, 1.0)  # Scale up but cap at 1.0
        
    def _check_opposing_viewpoints(self,
                                   thematic_elements: List[ThematicElement],
                                   dialogue: List[Dict[str, Any]]) -> bool:
        """Check if opposing thematic viewpoints are presented."""
        # Look for contradictory statements about themes
        opposition_keywords = ['but', 'however', 'disagree', 'wrong', 'no', "don't"]
        
        theme_discussions = 0
        opposing_discussions = 0
        
        for d in dialogue:
            dialogue_lower = d['dialogue'].lower()
            
            # Check if dialogue discusses themes
            for element in thematic_elements[:3]:  # Top 3 themes
                theme_keywords = self.theme_keywords.get(element.theme, [])
                if any(kw.lower() in dialogue_lower for kw in theme_keywords):
                    theme_discussions += 1
                    
                    # Check for opposition
                    if any(opp in dialogue_lower for opp in opposition_keywords):
                        opposing_discussions += 1
                    break
                    
        # If more than 20% of theme discussions include opposition
        if theme_discussions > 0:
            return (opposing_discussions / theme_discussions) > 0.2
        return False
        
    def _check_theme_resolution(self,
                                thematic_elements: List[ThematicElement],
                                scenes: List[Dict[str, Any]]) -> bool:
        """Check if theme is resolved by the end."""
        if not thematic_elements or not scenes:
            return False
            
        # Check last 10% of screenplay for theme resolution
        last_scenes = scenes[-(len(scenes) // 10):]
        
        if not last_scenes:
            return False
            
        # Look for resolution keywords with theme
        resolution_keywords = [
            'finally', 'realize', 'understand', 'accept', 'peace',
            'resolve', 'complete', 'fulfill', 'achieve', 'learn'
        ]
        
        for scene in last_scenes:
            scene_lower = scene['content'].lower()
            
            # Check if central theme appears with resolution
            if thematic_elements:
                central_theme = thematic_elements[0].theme
                theme_keywords = self.theme_keywords.get(central_theme, [])
                
                theme_present = any(kw.lower() in scene_lower for kw in theme_keywords)
                resolution_present = any(kw in scene_lower for kw in resolution_keywords)
                
                if theme_present and resolution_present:
                    return True
                    
        return False
        
    def _calculate_heavy_handedness(self,
                                    dialogue: List[Dict[str, Any]],
                                    thematic_elements: List[ThematicElement]) -> float:
        """Calculate how preachy/heavy-handed the theme delivery is."""
        if not dialogue:
            return 0.0
            
        preachy_count = 0
        theme_dialogue_count = 0
        
        for d in dialogue:
            dialogue_lower = d['dialogue'].lower()
            
            # Check if dialogue discusses themes
            is_thematic = False
            for element in thematic_elements[:3]:
                theme_keywords = self.theme_keywords.get(element.theme, [])
                if any(kw.lower() in dialogue_lower for kw in theme_keywords):
                    is_thematic = True
                    theme_dialogue_count += 1
                    break
                    
            # Check for preachy indicators
            if is_thematic:
                for indicator in self.preachy_indicators:
                    if indicator in dialogue_lower:
                        preachy_count += 1
                        break
                        
        if theme_dialogue_count > 0:
            return preachy_count / theme_dialogue_count
        return 0.0
        
    def _analyze_act_themes(self,
                           acts: Dict[str, List[Dict[str, Any]]],
                           thematic_elements: List[ThematicElement]) -> Dict[str, List[str]]:
        """Analyze theme distribution across acts."""
        act_themes = {}
        
        for act_name, act_scenes in acts.items():
            themes_in_act = []
            
            # Combine all act content
            act_content = ' '.join(scene['content'] for scene in act_scenes).lower()
            
            # Check each theme's presence
            for element in thematic_elements:
                theme_keywords = self.theme_keywords.get(element.theme, [])
                keyword_count = sum(act_content.count(kw.lower()) for kw in theme_keywords)
                
                if keyword_count > 2:  # Threshold for presence
                    themes_in_act.append(element.theme)
                    
            act_themes[act_name] = themes_in_act
            
        return act_themes
        
    def _analyze_character_themes(self,
                                  characters: Set[str],
                                  dialogue: List[Dict[str, Any]],
                                  thematic_elements: List[ThematicElement]) -> Dict[str, List[str]]:
        """Analyze which themes each character engages with."""
        character_themes = {}
        
        for character in characters:
            themes = []
            
            # Get all dialogue for this character
            char_dialogue = [d['dialogue'] for d in dialogue if d['character'] == character]
            char_text = ' '.join(char_dialogue).lower()
            
            # Check each theme
            for element in thematic_elements:
                theme_keywords = self.theme_keywords.get(element.theme, [])
                if any(kw.lower() in char_text for kw in theme_keywords):
                    themes.append(element.theme)
                    
            character_themes[character] = themes
            
        return character_themes
        
    def _calculate_scene_theme_density(self,
                                       scenes: List[Dict[str, Any]],
                                       thematic_elements: List[ThematicElement]) -> Dict[str, float]:
        """Calculate thematic density for each scene."""
        scene_density = {}
        
        for scene in scenes:
            theme_count = 0
            scene_lower = scene['content'].lower()
            word_count = len(scene['content'].split())
            
            # Count theme keywords
            for element in thematic_elements:
                theme_keywords = self.theme_keywords.get(element.theme, [])
                theme_count += sum(scene_lower.count(kw.lower()) for kw in theme_keywords)
                
            # Calculate density
            if word_count > 0:
                density = theme_count / word_count
            else:
                density = 0.0
                
            scene_density[scene['heading']] = min(density * 10, 1.0)  # Scale and cap
            
        return scene_density
        
    def _identify_thematic_conflicts(self,
                                     thematic_elements: List[ThematicElement],
                                     dialogue: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify conflicts between themes."""
        conflicts = []
        
        # Look for opposing themes
        opposing_pairs = [
            ('freedom', 'control'),
            ('love', 'revenge'),
            ('truth', 'corruption'),
            ('loyalty', 'ambition'),
            ('justice', 'revenge')
        ]
        
        present_themes = [el.theme for el in thematic_elements]
        
        for theme1, theme2 in opposing_pairs:
            if theme1 in present_themes and theme2 in present_themes:
                conflicts.append({
                    'theme1': theme1,
                    'theme2': theme2,
                    'type': 'opposing_themes',
                    'description': f'{theme1.title()} vs {theme2.title()} creates thematic tension'
                })
                
        return conflicts
        
    def _analyze_theme_progression(self,
                                   thematic_elements: List[ThematicElement],
                                   scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how themes develop through the story."""
        if not thematic_elements or not scenes:
            return {'progression': 'none'}
            
        central_theme = thematic_elements[0].theme
        theme_keywords = self.theme_keywords.get(central_theme, [])
        
        # Divide screenplay into quarters
        quarter_size = len(scenes) // 4
        quarters = [
            scenes[:quarter_size],
            scenes[quarter_size:quarter_size*2],
            scenes[quarter_size*2:quarter_size*3],
            scenes[quarter_size*3:]
        ]
        
        # Count theme presence in each quarter
        quarter_counts = []
        for quarter in quarters:
            quarter_text = ' '.join(s['content'] for s in quarter).lower()
            count = sum(quarter_text.count(kw.lower()) for kw in theme_keywords)
            quarter_counts.append(count)
            
        # Analyze progression pattern
        if quarter_counts[3] > quarter_counts[0]:  # More at end than beginning
            progression = 'escalating'
        elif quarter_counts[0] > quarter_counts[3]:  # More at beginning
            progression = 'diminishing'
        elif max(quarter_counts) == quarter_counts[1] or max(quarter_counts) == quarter_counts[2]:
            progression = 'midpoint_peak'
        else:
            progression = 'steady'
            
        return {
            'progression': progression,
            'quarter_counts': quarter_counts,
            'central_theme': central_theme
        }
        
    def _check_rule_violations(self,
                               theme_analysis: ThemeAnalysis,
                               thematic_elements: List[ThematicElement],
                               act_themes: Dict[str, List[str]],
                               theme_progression: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for rule violations."""
        violations = []
        
        for rule in self.rules:
            if self._evaluate_rule(rule, theme_analysis, thematic_elements, 
                                  act_themes, theme_progression):
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
                      theme_analysis: ThemeAnalysis,
                      thematic_elements: List[ThematicElement],
                      act_themes: Dict[str, List[str]],
                      theme_progression: Dict[str, Any]) -> bool:
        """Evaluate if a rule is violated."""
        rule_id = rule['id']
        
        # Clear Central Theme
        if rule_id == 'THE.R001':
            return theme_analysis.central_theme is None or \
                   theme_analysis.central_theme_strength < 0.3
            
        # Theme Consistency
        elif rule_id == 'THE.R002':
            return theme_analysis.theme_consistency_score < 0.5
            
        # Theme Expressed Through Action
        elif rule_id == 'THE.R003':
            methods = theme_analysis.theme_expression_methods
            return methods.get('action', 0) < methods.get('dialogue', 0) / 2
            
        # Character Arcs Support Theme
        elif rule_id == 'THE.R004':
            return theme_analysis.theme_character_alignment < 0.4
            
        # Plot Serves Theme
        elif rule_id == 'THE.R005':
            return theme_analysis.theme_plot_alignment < 0.4
            
        # Avoid Heavy-Handed Messaging
        elif rule_id == 'THE.R006':
            return theme_analysis.heavy_handed_score > 0.3
            
        # Multiple Theme Layers
        elif rule_id == 'THE.R007':
            return theme_analysis.thematic_depth < 2
            
        # Theme-Dialogue Balance
        elif rule_id == 'THE.R008':
            return theme_analysis.heavy_handed_score > 0.2
            
        # Visual Theme Reinforcement
        elif rule_id == 'THE.R009':
            methods = theme_analysis.theme_expression_methods
            return methods.get('symbolism', 0) == 0
            
        # Theme Resolution
        elif rule_id == 'THE.R010':
            return not theme_analysis.theme_resolved
            
        # Opposing Viewpoints
        elif rule_id == 'THE.R011':
            return not theme_analysis.opposing_viewpoints_present
            
        # Universal vs Specific
        elif rule_id == 'THE.R012':
            # Check if theme is too generic (high strength but low depth)
            return theme_analysis.central_theme_strength > 0.7 and \
                   theme_analysis.thematic_depth < 2
            
        # Theme Stakes
        elif rule_id == 'THE.R013':
            methods = theme_analysis.theme_expression_methods
            return methods.get('character_choice', 0) < 2
            
        # Opening Establishes Theme
        elif rule_id == 'THE.R014':
            if 'act1' in act_themes:
                return theme_analysis.central_theme not in act_themes.get('act1', [])
            return True
            
        # Theme Evolution
        elif rule_id == 'THE.R015':
            return theme_progression.get('progression') == 'none'
            
        return False
        
    def _generate_recommendations(self,
                                 theme_analysis: ThemeAnalysis,
                                 violations: List[Dict[str, Any]],
                                 thematic_elements: List[ThematicElement]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Address critical violations first
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        for violation in critical_violations[:2]:
            recommendations.append(f"CRITICAL: {violation['fix']}")
            
        # Check for missing central theme
        if not theme_analysis.central_theme:
            recommendations.append(
                "Establish a clear central theme to unify the story"
            )
            
        # Check consistency
        if theme_analysis.theme_consistency_score < 0.5:
            recommendations.append(
                "Strengthen thematic consistency throughout all acts"
            )
            
        # Check heavy-handedness
        if theme_analysis.heavy_handed_score > 0.3:
            recommendations.append(
                "Express themes more subtly through action and subtext"
            )
            
        # Check depth
        if theme_analysis.thematic_depth < 2:
            recommendations.append(
                "Add supporting themes to create thematic depth"
            )
            
        # Check resolution
        if not theme_analysis.theme_resolved:
            recommendations.append(
                "Provide clearer thematic resolution in the final act"
            )
            
        # Check opposition
        if not theme_analysis.opposing_viewpoints_present:
            recommendations.append(
                "Include opposing viewpoints to create thematic complexity"
            )
            
        # Check expression methods
        methods = theme_analysis.theme_expression_methods
        if methods.get('action', 0) < methods.get('dialogue', 0) / 2:
            recommendations.append(
                "Show theme through character actions, not just dialogue"
            )
            
        return recommendations[:7]  # Limit to 7 recommendations
        
    def _calculate_score(self,
                        theme_analysis: ThemeAnalysis,
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
            
        # Bonus for good thematic structure
        if theme_analysis.central_theme:
            base_score += 5
            
        if theme_analysis.theme_consistency_score > 0.7:
            base_score += 5
            
        if theme_analysis.opposing_viewpoints_present:
            base_score += 3
            
        if theme_analysis.theme_resolved:
            base_score += 5
            
        # Penalty for heavy-handedness
        if theme_analysis.heavy_handed_score > 0.3:
            base_score -= 10
            
        # Bonus for depth
        base_score += min(theme_analysis.thematic_depth * 2, 10)
        
        return max(5, min(95, base_score))

    def _generate_diagnosis(self, theme_analysis: ThemeAnalysis,
                          violations: List[Dict[str, Any]]) -> str:
        """Generate narrative theme diagnosis."""
        score = self._calculate_score(theme_analysis, violations)
        diagnosis = f"Theme Analysis Score: {score}/100\n\n"

        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent thematic unity! Your screenplay has clear, consistent themes that resonate throughout. "
        elif score >= 70:
            diagnosis += "Good thematic foundation with some areas needing refinement. "
        elif score >= 50:
            diagnosis += "Theme issues are impacting the screenplay's coherence. "
        else:
            diagnosis += "Significant thematic problems that will affect story impact. "

        # Central theme
        if theme_analysis.central_theme:
            diagnosis += f"Central theme identified: {theme_analysis.central_theme}. "
        else:
            diagnosis += "WARNING: No clear central theme - story lacks thematic anchor. "

        # Consistency
        if theme_analysis.theme_consistency_score >= 0.7:
            diagnosis += "Theme maintains strong consistency across all acts. "
        elif theme_analysis.theme_consistency_score >= 0.5:
            diagnosis += "Theme consistency is moderate - some acts deviate. "
        else:
            diagnosis += "Theme lacks consistency - shifts or contradicts itself. "

        # Heavy-handedness check
        if theme_analysis.heavy_handed_score > 0.3:
            diagnosis += "WARNING: Theme delivery is preachy - needs subtlety. "
        elif theme_analysis.heavy_handed_score < 0.1:
            diagnosis += "Theme is expressed with excellent subtlety. "

        # Depth
        if theme_analysis.thematic_depth >= 3:
            diagnosis += "Rich thematic layers create depth and complexity. "
        elif theme_analysis.thematic_depth == 0:
            diagnosis += "Single-dimensional theme - add supporting themes. "

        # Opposition
        if theme_analysis.opposing_viewpoints_present:
            diagnosis += "Good thematic complexity with opposing viewpoints. "
        else:
            diagnosis += "Add counterarguments for thematic richness. "

        # Resolution
        if theme_analysis.theme_resolved:
            diagnosis += "Theme reaches satisfying resolution. "
        else:
            diagnosis += "Theme needs clearer resolution in final act. "

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            diagnosis += f"\n\nCRITICAL ISSUES ({len(critical_violations)}): "
            for v in critical_violations[:2]:
                diagnosis += f"{v['title']}. "

        return diagnosis.strip()
