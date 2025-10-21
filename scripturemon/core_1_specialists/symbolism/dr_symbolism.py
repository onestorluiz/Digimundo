#!/usr/bin/env python3
"""
Script Doctor Symbolmon - Symbolism and Metaphor Specialist
Analyzes symbolic elements, metaphors, and allegorical meaning in screenplays.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import re
import yaml
from pathlib import Path
from collections import Counter


@dataclass
class Symbol:
    """Represents a symbolic element."""
    symbol_type: str  # visual, object, color, setting, character
    name: str
    occurrences: List[Dict[str, Any]] = field(default_factory=list)
    meaning: str = ""
    consistency_score: float = 0.0
    payoff: bool = False
    evolution: List[str] = field(default_factory=list)
    

@dataclass
class Metaphor:
    """Represents a metaphorical element."""
    text: str
    location: Dict[str, Any]
    vehicle: str  # What is used for comparison
    tenor: str  # What is being compared
    clarity_score: float = 0.0
    integration_score: float = 0.0
    

@dataclass
class SymbolismAnalysis:
    """Results from symbolism analysis."""
    total_symbols: int = 0
    purposeful_symbols: int = 0
    visual_symbols: int = 0
    object_symbols: int = 0
    color_symbols: int = 0
    setting_symbols: int = 0
    character_symbols: int = 0
    symbol_consistency_score: float = 0.0
    symbol_density: float = 0.0  # Symbols per scene
    metaphor_count: int = 0
    metaphor_clarity_average: float = 0.0
    symbolic_payoff_ratio: float = 0.0
    emotional_resonance_score: float = 0.0
    

@dataclass
class SymbolismResult:
    """Complete symbolism analysis result."""
    score: int
    specialist: Dict[str, str]
    symbolism_analysis: SymbolismAnalysis
    symbols: List[Symbol]
    metaphors: List[Metaphor]
    symbol_network: Dict[str, List[str]]  # Symbol connections
    scene_symbolism: Dict[str, List[str]]  # Symbols per scene
    symbolic_arcs: List[Dict[str, Any]]  # How symbols evolve
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]
    symbolic_patterns: Dict[str, Any]
    

class DrSymbolism:
    """Script Doctor Symbolmon - Symbolism and Metaphor Specialist."""
    
    def __init__(self):
        """Initialize the symbolism specialist."""
        self.name = "Script Doctor Symbolmon"
        self.specialty = "Symbolism and Metaphor"
        self.load_rules()
        
        # Common symbolic elements to look for
        self.visual_symbols = [
            'mirror', 'window', 'door', 'bridge', 'wall', 'fence',
            'light', 'shadow', 'darkness', 'sun', 'moon', 'stars',
            'fire', 'water', 'earth', 'wind', 'storm', 'rain'
        ]
        
        self.object_symbols = [
            'key', 'lock', 'chain', 'rope', 'knife', 'gun',
            'flower', 'ring', 'watch', 'clock', 'photo', 'letter',
            'book', 'map', 'compass', 'mask', 'crown', 'cross'
        ]
        
        self.color_keywords = [
            'red', 'blue', 'green', 'yellow', 'black', 'white',
            'gray', 'grey', 'gold', 'silver', 'purple', 'orange'
        ]
        
        self.metaphor_indicators = [
            'like', 'as if', 'as though', 'seems', 'appears',
            'reminds', 'resembles', 'similar to', 'kind of'
        ]
        
        # Symbolic settings
        self.symbolic_settings = {
            'prison': 'confinement/limitation',
            'hospital': 'healing/vulnerability', 
            'church': 'faith/morality',
            'graveyard': 'death/past',
            'bridge': 'transition/connection',
            'crossroads': 'choice/decision',
            'mountain': 'challenge/achievement',
            'ocean': 'unconscious/emotion',
            'forest': 'unknown/nature',
            'desert': 'isolation/trial'
        }
        
    def load_rules(self):
        """Load rules from YAML configuration."""
        rules_path = Path(__file__).parent.parent / 'rules' / 'symbolism_metaphor_rules.yaml'
        try:
            with open(rules_path, 'r') as f:
                self.rules_config = yaml.safe_load(f)
                self.rules = self.rules_config.get('rules', [])
        except FileNotFoundError:
            self.rules = []
            self.rules_config = {}
            
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """Analyze screenplay for symbolism and metaphor."""
        lines = screenplay_text.split('\n')
        
        # Extract structural elements
        scenes = self._extract_scenes(lines)
        action_lines = self._extract_action_lines(lines)
        dialogue = self._extract_dialogue(lines)
        
        # Identify symbolic elements
        symbols = self._identify_symbols(scenes, action_lines, dialogue)
        
        # Identify metaphors
        metaphors = self._identify_metaphors(action_lines, dialogue)
        
        # Analyze symbolism
        symbolism_analysis = self._analyze_symbolism(
            symbols, metaphors, scenes
        )
        
        # Build symbol network
        symbol_network = self._build_symbol_network(symbols, scenes)
        
        # Map symbols to scenes
        scene_symbolism = self._map_scene_symbolism(symbols, scenes)
        
        # Analyze symbolic arcs
        symbolic_arcs = self._analyze_symbolic_arcs(symbols, scenes)
        
        # Identify patterns
        symbolic_patterns = self._identify_symbolic_patterns(symbols, metaphors)
        
        # Check rules
        violations = self._check_rule_violations(
            symbolism_analysis, symbols, metaphors, symbolic_arcs
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            symbolism_analysis, violations, symbols
        )
        
        # Calculate score
        score = self._calculate_score(symbolism_analysis, violations)

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, symbolism_analysis, len(symbols), len(metaphors), violations
        )

        # Convert dataclasses to dicts
        symbols_dict = [
            {
                'symbol_type': sym.symbol_type,
                'name': sym.name,
                'occurrences': sym.occurrences,
                'meaning': sym.meaning,
                'consistency_score': sym.consistency_score,
                'payoff': sym.payoff,
                'evolution': sym.evolution
            } for sym in symbols
        ]

        metaphors_dict = [
            {
                'text': met.text,
                'location': met.location,
                'vehicle': met.vehicle,
                'tenor': met.tenor,
                'clarity_score': met.clarity_score,
                'integration_score': met.integration_score
            } for met in metaphors
        ]

        return {
            'score': score,
            'specialist': {
                "name": self.name,
                "specialty": self.specialty,
                "identity": "Script Doctor™ first, Digimon symbolism specialist second"
            },
            'total_symbols': symbolism_analysis.total_symbols,
            'purposeful_symbols': symbolism_analysis.purposeful_symbols,
            'visual_symbols': symbolism_analysis.visual_symbols,
            'object_symbols': symbolism_analysis.object_symbols,
            'color_symbols': symbolism_analysis.color_symbols,
            'setting_symbols': symbolism_analysis.setting_symbols,
            'character_symbols': symbolism_analysis.character_symbols,
            'symbol_consistency_score': symbolism_analysis.symbol_consistency_score,
            'symbol_density': symbolism_analysis.symbol_density,
            'metaphor_count': symbolism_analysis.metaphor_count,
            'metaphor_clarity_average': symbolism_analysis.metaphor_clarity_average,
            'symbolic_payoff_ratio': symbolism_analysis.symbolic_payoff_ratio,
            'emotional_resonance_score': symbolism_analysis.emotional_resonance_score,
            'symbols': symbols_dict,
            'metaphors': metaphors_dict,
            'symbol_network': symbol_network,
            'scene_symbolism': scene_symbolism,
            'symbolic_arcs': symbolic_arcs,
            'recommendations': recommendations,
            'rule_violations': violations,
            'symbolic_patterns': symbolic_patterns,
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
                        'content': scene_content,
                        'line_num': current_scene_line,
                        'scene_num': scene_num
                    })
                    scene_num += 1
                current_scene = line.strip()
                current_scene_line = i
                scene_content = []
            elif current_scene:
                scene_content.append(line)
                
        # Don't forget last scene
        if current_scene:
            scenes.append({
                'heading': current_scene,
                'content': scene_content,
                'line_num': current_scene_line,
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
                
            # Skip parentheticals
            if stripped.startswith('(') and stripped.endswith(')'):
                continue
                
            # This looks like action
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
                if current_character and current_dialogue:
                    dialogue_blocks.append({
                        'character': current_character,
                        'text': ' '.join(current_dialogue),
                        'line_num': i
                    })
                current_character = stripped.split('(')[0].strip()
                current_dialogue = []
                
            # Dialogue line
            elif current_character and stripped and not stripped.startswith('('):
                current_dialogue.append(stripped)
                
            # End of dialogue
            elif not stripped and current_character and current_dialogue:
                dialogue_blocks.append({
                    'character': current_character,
                    'text': ' '.join(current_dialogue),
                    'line_num': i
                })
                current_character = None
                current_dialogue = []
                
        # Don't forget last dialogue
        if current_character and current_dialogue:
            dialogue_blocks.append({
                'character': current_character,
                'text': ' '.join(current_dialogue),
                'line_num': len(lines)
            })
            
        return dialogue_blocks
        
    def _identify_symbols(self, 
                         scenes: List[Dict[str, Any]],
                         action_lines: List[Dict[str, Any]],
                         dialogue: List[Dict[str, Any]]) -> List[Symbol]:
        """Identify symbolic elements in screenplay."""
        symbols = []
        
        # Look for visual symbols in action lines
        for action in action_lines:
            text_lower = action['text'].lower()
            for visual_symbol in self.visual_symbols:
                if visual_symbol in text_lower:
                    symbol = self._find_or_create_symbol(
                        symbols, 'visual', visual_symbol
                    )
                    symbol.occurrences.append({
                        'type': 'action',
                        'text': action['text'][:100],
                        'line_num': action['line_num']
                    })
                    
        # Look for object symbols
        for action in action_lines:
            text_lower = action['text'].lower()
            for object_symbol in self.object_symbols:
                if object_symbol in text_lower:
                    symbol = self._find_or_create_symbol(
                        symbols, 'object', object_symbol
                    )
                    symbol.occurrences.append({
                        'type': 'action',
                        'text': action['text'][:100],
                        'line_num': action['line_num']
                    })
                    
        # Look for color symbols
        for action in action_lines:
            text_lower = action['text'].lower()
            for color in self.color_keywords:
                if color in text_lower:
                    symbol = self._find_or_create_symbol(
                        symbols, 'color', color
                    )
                    symbol.occurrences.append({
                        'type': 'action',
                        'text': action['text'][:100],
                        'line_num': action['line_num']
                    })
                    
        # Look for symbolic settings
        for scene in scenes:
            heading_lower = scene['heading'].lower()
            for setting, meaning in self.symbolic_settings.items():
                if setting in heading_lower:
                    symbol = self._find_or_create_symbol(
                        symbols, 'setting', setting
                    )
                    symbol.meaning = meaning
                    symbol.occurrences.append({
                        'type': 'setting',
                        'text': scene['heading'],
                        'scene_num': scene['scene_num']
                    })
                    
        # Calculate consistency for each symbol
        for symbol in symbols:
            symbol.consistency_score = self._calculate_symbol_consistency(symbol, scenes)
            
        return symbols
        
    def _find_or_create_symbol(self, 
                               symbols: List[Symbol], 
                               symbol_type: str, 
                               name: str) -> Symbol:
        """Find existing symbol or create new one."""
        for symbol in symbols:
            if symbol.symbol_type == symbol_type and symbol.name == name:
                return symbol
                
        new_symbol = Symbol(symbol_type=symbol_type, name=name)
        symbols.append(new_symbol)
        return new_symbol
        
    def _calculate_symbol_consistency(self, symbol: Symbol, scenes: List[Dict[str, Any]]) -> float:
        """Calculate how consistently a symbol is used."""
        if len(symbol.occurrences) < 2:
            return 1.0  # Single occurrence is consistent by default
            
        # Check distribution across screenplay
        scene_nums = []
        for occ in symbol.occurrences:
            if 'scene_num' in occ:
                scene_nums.append(occ['scene_num'])
                
        if not scene_nums:
            return 0.5
            
        # Calculate spread
        if len(scenes) > 0:
            first_occurrence = min(scene_nums)
            last_occurrence = max(scene_nums)
            spread = (last_occurrence - first_occurrence) / len(scenes)
            
            # Good consistency if symbol appears throughout
            if spread > 0.5:  # Appears across more than half the screenplay
                return 0.8
            elif spread > 0.25:  # Appears across a quarter
                return 0.6
            else:
                return 0.4
        
        return 0.5
        
    def _identify_metaphors(self,
                           action_lines: List[Dict[str, Any]],
                           dialogue: List[Dict[str, Any]]) -> List[Metaphor]:
        """Identify metaphorical language."""
        metaphors = []
        
        # Look in action lines
        for action in action_lines:
            text = action['text']
            text_lower = text.lower()
            
            # Check for simile indicators
            for indicator in self.metaphor_indicators:
                if indicator in text_lower:
                    # Extract the comparison
                    pattern = rf'{indicator}\s+([^.!?]+)[.!?]?'
                    matches = re.findall(pattern, text_lower)
                    
                    for match in matches:
                        metaphor = Metaphor(
                            text=match[:100],
                            location={'type': 'action', 'line_num': action['line_num']},
                            vehicle=self._extract_vehicle(match),
                            tenor=self._extract_tenor(text, match),
                            clarity_score=self._calculate_metaphor_clarity(match),
                            integration_score=0.7  # Action metaphors usually well integrated
                        )
                        metaphors.append(metaphor)
                        
        # Look in dialogue
        for dial in dialogue:
            text = dial['text']
            text_lower = text.lower()
            
            for indicator in self.metaphor_indicators:
                if indicator in text_lower:
                    pattern = rf'{indicator}\s+([^.!?]+)[.!?]?'
                    matches = re.findall(pattern, text_lower)
                    
                    for match in matches:
                        metaphor = Metaphor(
                            text=match[:100],
                            location={
                                'type': 'dialogue',
                                'character': dial['character'],
                                'line_num': dial['line_num']
                            },
                            vehicle=self._extract_vehicle(match),
                            tenor=self._extract_tenor(text, match),
                            clarity_score=self._calculate_metaphor_clarity(match),
                            integration_score=self._calculate_integration(match, dial['character'])
                        )
                        metaphors.append(metaphor)
                        
        return metaphors
        
    def _extract_vehicle(self, metaphor_text: str) -> str:
        """Extract what is being used for comparison."""
        # Simple extraction - get last few words
        words = metaphor_text.split()
        if len(words) > 2:
            return ' '.join(words[-3:])
        return metaphor_text
        
    def _extract_tenor(self, full_text: str, metaphor_text: str) -> str:
        """Extract what is being compared."""
        # Get context before the metaphor
        index = full_text.lower().find(metaphor_text.lower())
        if index > 0:
            before = full_text[:index].split()[-3:]
            return ' '.join(before)
        return "unknown"
        
    def _calculate_metaphor_clarity(self, metaphor_text: str) -> float:
        """Calculate how clear the metaphor is."""
        # Simple clarity based on length and common words
        words = metaphor_text.split()
        
        if len(words) < 3:
            return 0.3  # Too short
        elif len(words) > 10:
            return 0.5  # Too long
        else:
            return 0.8  # Just right
            
    def _calculate_integration(self, metaphor_text: str, character: str) -> float:
        """Calculate how well integrated the metaphor is."""
        # Basic integration score
        # Could be enhanced with character voice analysis
        return 0.6
        
    def _analyze_symbolism(self,
                          symbols: List[Symbol],
                          metaphors: List[Metaphor],
                          scenes: List[Dict[str, Any]]) -> SymbolismAnalysis:
        """Analyze overall symbolism."""
        analysis = SymbolismAnalysis()
        
        analysis.total_symbols = len(symbols)
        
        # Count symbol types
        for symbol in symbols:
            if symbol.symbol_type == 'visual':
                analysis.visual_symbols += 1
            elif symbol.symbol_type == 'object':
                analysis.object_symbols += 1
            elif symbol.symbol_type == 'color':
                analysis.color_symbols += 1
            elif symbol.symbol_type == 'setting':
                analysis.setting_symbols += 1
            elif symbol.symbol_type == 'character':
                analysis.character_symbols += 1
                
        # Calculate purposeful symbols (those with multiple occurrences)
        analysis.purposeful_symbols = sum(
            1 for s in symbols if len(s.occurrences) > 1
        )
        
        # Calculate consistency
        if symbols:
            consistencies = [s.consistency_score for s in symbols]
            analysis.symbol_consistency_score = sum(consistencies) / len(consistencies)
        
        # Calculate density
        if scenes:
            analysis.symbol_density = len(symbols) / len(scenes)
            
        # Analyze metaphors
        analysis.metaphor_count = len(metaphors)
        if metaphors:
            clarities = [m.clarity_score for m in metaphors]
            analysis.metaphor_clarity_average = sum(clarities) / len(clarities)
            
        # Calculate payoff ratio
        symbols_with_payoff = sum(1 for s in symbols if s.payoff)
        if symbols:
            analysis.symbolic_payoff_ratio = symbols_with_payoff / len(symbols)
            
        # Calculate emotional resonance (simplified)
        emotional_symbols = ['heart', 'tears', 'blood', 'fire', 'storm', 'sun', 'moon']
        emotional_count = sum(
            1 for s in symbols 
            if any(em in s.name for em in emotional_symbols)
        )
        if symbols:
            analysis.emotional_resonance_score = min(emotional_count / len(symbols) * 2, 1.0)
            
        return analysis
        
    def _build_symbol_network(self,
                             symbols: List[Symbol],
                             scenes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Build network of symbol connections."""
        network = {}
        
        # Connect symbols that appear in same scenes
        for scene in scenes:
            scene_symbols = []
            
            for symbol in symbols:
                for occ in symbol.occurrences:
                    if occ.get('scene_num') == scene['scene_num']:
                        scene_symbols.append(symbol.name)
                        break
                        
            # Create connections
            for i, sym1 in enumerate(scene_symbols):
                if sym1 not in network:
                    network[sym1] = []
                for sym2 in scene_symbols[i+1:]:
                    if sym2 not in network[sym1]:
                        network[sym1].append(sym2)
                        
        return network
        
    def _map_scene_symbolism(self,
                            symbols: List[Symbol],
                            scenes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Map symbols to scenes."""
        scene_symbolism = {}
        
        for scene in scenes:
            scene_key = f"Scene {scene['scene_num']}: {scene['heading']}"
            scene_symbols = []
            
            for symbol in symbols:
                for occ in symbol.occurrences:
                    if occ.get('scene_num') == scene['scene_num']:
                        scene_symbols.append(f"{symbol.name} ({symbol.symbol_type})")
                        
            scene_symbolism[scene_key] = scene_symbols
            
        return scene_symbolism
        
    def _analyze_symbolic_arcs(self,
                              symbols: List[Symbol],
                              scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze how symbols evolve through story."""
        arcs = []
        
        for symbol in symbols:
            if len(symbol.occurrences) > 2:  # Need multiple occurrences for arc
                arc = {
                    'symbol': symbol.name,
                    'type': symbol.symbol_type,
                    'appearances': len(symbol.occurrences),
                    'evolution': []
                }
                
                # Track evolution through occurrences
                for i, occ in enumerate(symbol.occurrences):
                    if i == 0:
                        arc['evolution'].append('Introduction')
                    elif i == len(symbol.occurrences) - 1:
                        arc['evolution'].append('Resolution')
                        symbol.payoff = True  # Mark as having payoff
                    else:
                        arc['evolution'].append('Development')
                        
                arcs.append(arc)
                
        return arcs
        
    def _identify_symbolic_patterns(self,
                                   symbols: List[Symbol],
                                   metaphors: List[Metaphor]) -> Dict[str, Any]:
        """Identify patterns in symbolism."""
        patterns = {
            'dominant_type': None,
            'recurring_symbols': [],
            'metaphor_style': None,
            'symbolic_density': None
        }
        
        # Find dominant symbol type
        if symbols:
            type_counts = Counter(s.symbol_type for s in symbols)
            patterns['dominant_type'] = type_counts.most_common(1)[0][0]
            
        # Find recurring symbols
        patterns['recurring_symbols'] = [
            s.name for s in symbols if len(s.occurrences) > 2
        ]
        
        # Analyze metaphor style
        if metaphors:
            if len(metaphors) > 5:
                patterns['metaphor_style'] = 'metaphor-rich'
            elif len(metaphors) > 2:
                patterns['metaphor_style'] = 'moderate-metaphor'
            else:
                patterns['metaphor_style'] = 'literal'
                
        # Symbolic density
        total_symbolic_elements = len(symbols) + len(metaphors)
        if total_symbolic_elements > 20:
            patterns['symbolic_density'] = 'dense'
        elif total_symbolic_elements > 10:
            patterns['symbolic_density'] = 'moderate'
        else:
            patterns['symbolic_density'] = 'sparse'
            
        return patterns
        
    def _check_rule_violations(self,
                              analysis: SymbolismAnalysis,
                              symbols: List[Symbol],
                              metaphors: List[Metaphor],
                              symbolic_arcs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for rule violations."""
        violations = []
        
        for rule in self.rules:
            if self._evaluate_rule(rule, analysis, symbols, metaphors, symbolic_arcs):
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
                      analysis: SymbolismAnalysis,
                      symbols: List[Symbol],
                      metaphors: List[Metaphor],
                      symbolic_arcs: List[Dict[str, Any]]) -> bool:
        """Evaluate if a rule is violated."""
        rule_id = rule['id']
        
        # Purposeful Symbolism
        if rule_id == 'SYM.R001':
            return analysis.purposeful_symbols < analysis.total_symbols / 2
            
        # Symbol Consistency  
        elif rule_id == 'SYM.R002':
            return analysis.symbol_consistency_score < 0.5
            
        # Visual Symbolism
        elif rule_id == 'SYM.R003':
            return analysis.visual_symbols == 0
            
        # Metaphor Clarity
        elif rule_id == 'SYM.R004':
            return analysis.metaphor_clarity_average < 0.4 or \
                   analysis.metaphor_clarity_average > 0.9
            
        # Symbol Payoff
        elif rule_id == 'SYM.R005':
            return analysis.symbolic_payoff_ratio < 0.3
            
        # Avoid Over-Symbolism
        elif rule_id == 'SYM.R006':
            return analysis.symbol_density > 2.0  # More than 2 symbols per scene
            
        # Character Symbols
        elif rule_id == 'SYM.R007':
            return analysis.character_symbols == 0 and len(symbols) > 5
            
        # Environmental Symbols
        elif rule_id == 'SYM.R008':
            return analysis.setting_symbols == 0
            
        # Color Symbolism
        elif rule_id == 'SYM.R009':
            return analysis.color_symbols == 0 and len(symbols) > 3
            
        # Object Symbolism
        elif rule_id == 'SYM.R010':
            return analysis.object_symbols == 0
            
        # Metaphor Integration
        elif rule_id == 'SYM.R011':
            if metaphors:
                avg_integration = sum(m.integration_score for m in metaphors) / len(metaphors)
                return avg_integration < 0.5
            return False
            
        # Symbol Evolution
        elif rule_id == 'SYM.R012':
            return len(symbolic_arcs) == 0 and len(symbols) > 3
            
        # Universal vs Specific
        elif rule_id == 'SYM.R013':
            # This would need cultural analysis
            return False
            
        # Foreshadowing Symbols
        elif rule_id == 'SYM.R014':
            # Check if early symbols pay off
            early_symbols = [s for s in symbols if s.occurrences and 
                           s.occurrences[0].get('scene_num', 999) < 3]
            if early_symbols:
                return not any(s.payoff for s in early_symbols)
            return False
            
        # Emotional Symbols
        elif rule_id == 'SYM.R015':
            return analysis.emotional_resonance_score < 0.2
            
        return False
        
    def _generate_recommendations(self,
                                 analysis: SymbolismAnalysis,
                                 violations: List[Dict[str, Any]],
                                 symbols: List[Symbol]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Address critical violations first
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        for violation in critical_violations[:2]:
            recommendations.append(f"CRITICAL: {violation['fix']}")
            
        # Check symbol purposefulness
        if analysis.purposeful_symbols < analysis.total_symbols / 2:
            recommendations.append(
                "Make symbols more purposeful - ensure they recur and evolve"
            )
            
        # Check consistency
        if analysis.symbol_consistency_score < 0.5:
            recommendations.append(
                "Improve symbol consistency throughout screenplay"
            )
            
        # Check visual symbols
        if analysis.visual_symbols == 0:
            recommendations.append(
                "Add visual symbols to create cinematic imagery"
            )
            
        # Check payoff
        if analysis.symbolic_payoff_ratio < 0.3:
            recommendations.append(
                "Ensure symbols have meaningful payoff in resolution"
            )
            
        # Check density
        if analysis.symbol_density > 2.0:
            recommendations.append(
                "Reduce symbol density - focus on essential symbols"
            )
        elif analysis.symbol_density < 0.3:
            recommendations.append(
                "Consider adding symbolic elements to enrich narrative"
            )
            
        # Check metaphors
        if analysis.metaphor_count == 0:
            recommendations.append(
                "Add metaphorical language to deepen meaning"
            )
        elif analysis.metaphor_clarity_average < 0.5:
            recommendations.append(
                "Clarify metaphors without making them obvious"
            )
            
        return recommendations[:7]  # Limit to 7 recommendations
        
    def _calculate_score(self,
                        analysis: SymbolismAnalysis,
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
            
        # Bonus for good symbolism
        if analysis.purposeful_symbols > analysis.total_symbols * 0.6:
            base_score += 5
            
        if analysis.symbol_consistency_score > 0.7:
            base_score += 5
            
        if analysis.symbolic_payoff_ratio > 0.5:
            base_score += 5
            
        if analysis.emotional_resonance_score > 0.5:
            base_score += 3
            
        # Penalty for over-symbolism
        if analysis.symbol_density > 2.0:
            base_score -= 10
            
        # Bonus for metaphor quality
        if analysis.metaphor_clarity_average > 0.6 and analysis.metaphor_count > 3:
            base_score += 5

        return max(5, min(95, base_score))

    def _generate_diagnosis(self, score: int, analysis: SymbolismAnalysis,
                           num_symbols: int, num_metaphors: int,
                           violations: List[Dict]) -> str:
        """Generate diagnosis based on symbolism analysis."""
        diagnosis_parts = []

        # Overall assessment
        if score >= 85:
            diagnosis_parts.append("✅ EXCELLENT symbolic depth and meaningful metaphors.")
        elif score >= 70:
            diagnosis_parts.append("👍 GOOD symbolism with room for deeper layers.")
        elif score >= 50:
            diagnosis_parts.append("⚠️  MODERATE symbolism - needs more intentional symbolic elements.")
        else:
            diagnosis_parts.append("❌ CRITICAL lack of symbolism - story feels literal and flat.")

        # Symbol count
        diagnosis_parts.append(f"Found {num_symbols} symbols ({analysis.purposeful_symbols} purposeful), {num_metaphors} metaphors.")

        # Symbol consistency
        if analysis.symbol_consistency_score < 0.5:
            diagnosis_parts.append(f"Symbol consistency is low ({analysis.symbol_consistency_score:.2f}) - symbols used inconsistently.")
        elif analysis.symbol_consistency_score > 0.8:
            diagnosis_parts.append(f"Excellent symbol consistency ({analysis.symbol_consistency_score:.2f})!")

        # Symbolic payoff
        if analysis.symbolic_payoff_ratio < 0.3:
            diagnosis_parts.append(f"Low payoff ratio ({analysis.symbolic_payoff_ratio:.2f}) - symbols not resolved.")
        elif analysis.symbolic_payoff_ratio > 0.7:
            diagnosis_parts.append(f"Great symbolic payoff ({analysis.symbolic_payoff_ratio:.2f})!")

        # Symbol density
        if analysis.symbol_density > 2.0:
            diagnosis_parts.append(f"⚠️  Over-symbolic ({analysis.symbol_density:.1f} symbols/scene) - may feel heavy-handed.")
        elif analysis.symbol_density < 0.3:
            diagnosis_parts.append(f"Low symbol density ({analysis.symbol_density:.1f}) - could use more layers.")

        # Metaphor quality
        if num_metaphors > 0:
            if analysis.metaphor_clarity_average > 0.7:
                diagnosis_parts.append(f"Clear, effective metaphors (avg {analysis.metaphor_clarity_average:.2f}).")
            elif analysis.metaphor_clarity_average < 0.4:
                diagnosis_parts.append(f"Metaphors unclear (avg {analysis.metaphor_clarity_average:.2f}) - may confuse readers.")

        # Violations
        if violations:
            critical_violations = [v for v in violations if v['severity'] == 'critical']
            if critical_violations:
                diagnosis_parts.append(f"⚠️  {len(critical_violations)} critical symbolic issues detected.")

        return " ".join(diagnosis_parts)
