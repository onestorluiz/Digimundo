#!/usr/bin/env python3
"""
Script Doctor Submon - Subtext and Layered Meaning Specialist
Analyzes implicit communication, unspoken emotions, and layered dialogue.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import re
import yaml
from pathlib import Path


@dataclass
class SubtextAnalysis:
    """Results from subtext analysis."""
    has_subtext: bool = False
    subtext_depth_score: float = 0.0
    on_the_nose_ratio: float = 0.0
    contradiction_count: int = 0
    emotional_layers: int = 0
    power_dynamics_present: bool = False
    hidden_agendas_detected: bool = False
    double_meanings_count: int = 0
    avoidance_patterns: List[str] = field(default_factory=list)
    meaningful_silences: int = 0
    ironic_moments: int = 0
    subtext_examples: List[Dict[str, Any]] = field(default_factory=list)
    payoff_potential: float = 0.0


@dataclass
class SubtextResult:
    """Complete subtext analysis result."""
    score: int
    specialist: Dict[str, str]
    subtext_analysis: SubtextAnalysis
    dialogue_layers: Dict[str, int]
    character_subtext: Dict[str, List[str]]
    scene_subtext_density: float
    most_layered_exchanges: List[Dict[str, Any]]
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]
    subtext_techniques_used: List[str]
    missing_opportunities: List[str]
    

class DrSubtext:
    """Script Doctor Submon - Subtext and Layered Meaning Specialist."""
    
    def __init__(self):
        """Initialize the subtext specialist."""
        self.name = "Script Doctor Submon"
        self.specialty = "Subtext and Layered Meaning"
        self.load_rules()
        
        # Subtext indicators
        self.on_the_nose_phrases = [
            r'\bI feel\b', r'\bI think\b', r'\bI am\b.{0,20}(angry|sad|happy|scared)',
            r'\bYou make me\b', r'\bThis makes me\b', r'\bI\'m feeling\b',
            r'\bThe truth is\b', r'\bTo be honest\b', r'\bActually\b',
            r'\bWhat I mean is\b', r'\bIn other words\b'
        ]
        
        self.avoidance_indicators = [
            r'\banyway\b', r'\bnevermind\b', r'\bforget it\b',
            r'\bnothing\b', r'\bit\'s fine\b', r'\bwhatever\b',
            r'\bdoesn\'t matter\b', r'\blet\'s just\b'
        ]
        
        self.contradiction_words = [
            'but', 'however', 'although', 'despite', 'yet', 'still',
            'nevertheless', 'nonetheless', 'except'
        ]
        
    def load_rules(self):
        """Load rules from YAML configuration."""
        rules_path = Path(__file__).parent.parent / 'rules' / 'subtext_rules.yaml'
        try:
            with open(rules_path, 'r') as f:
                self.rules_config = yaml.safe_load(f)
                self.rules = self.rules_config.get('rules', [])
        except FileNotFoundError:
            self.rules = []
            self.rules_config = {}
            
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """Analyze screenplay for subtext and layered meaning."""
        lines = screenplay_text.split('\n')
        
        # Extract components
        dialogue_blocks = self._extract_dialogue_blocks(lines)
        scenes = self._extract_scenes(lines)
        
        # Perform analysis
        subtext_analysis = self._analyze_subtext_depth(dialogue_blocks, scenes)
        dialogue_layers = self._analyze_dialogue_layers(dialogue_blocks)
        character_subtext = self._analyze_character_subtext(dialogue_blocks)
        scene_density = self._calculate_scene_subtext_density(scenes)
        layered_exchanges = self._find_most_layered_exchanges(dialogue_blocks)
        techniques_used = self._identify_techniques_used(dialogue_blocks, scenes)
        missing_ops = self._find_missing_opportunities(dialogue_blocks)
        
        # Check rules
        violations = self._check_rule_violations(
            subtext_analysis, dialogue_layers, techniques_used
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            subtext_analysis, violations, missing_ops
        )
        
        # Calculate score
        score = self._calculate_score(subtext_analysis, violations)
        
        return {
            "score": score,
            "specialist": {
                "name": self.name,
                "specialty": self.specialty,
                "identity": "Script Doctor™ first, Digimon subtext specialist second"
            },
            "subtext_analysis": subtext_analysis,
            "dialogue_layers": dialogue_layers,
            "character_subtext": character_subtext,
            "scene_subtext_density": scene_density,
            "most_layered_exchanges": layered_exchanges,
            "recommendations": recommendations,
            "rule_violations": violations,
            "subtext_techniques_used": techniques_used,
            "missing_opportunities": missing_ops,
            "diagnosis": self._generate_diagnosis(subtext_analysis, violations)
        }
        
    def _extract_dialogue_blocks(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract dialogue blocks with context."""
        dialogue_blocks = []
        current_character = None
        current_dialogue = []
        current_parenthetical = ""
        preceding_action = ""
        following_action = ""
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Character name (all caps, centered)
            if stripped and stripped.isupper() and not any(
                keyword in stripped for keyword in ['INT.', 'EXT.', 'FADE', 'CUT']
            ):
                # Save previous dialogue block
                if current_character and current_dialogue:
                    dialogue_blocks.append({
                        'character': current_character,
                        'dialogue': ' '.join(current_dialogue),
                        'parenthetical': current_parenthetical,
                        'preceding_action': preceding_action,
                        'following_action': following_action,
                        'line_number': i
                    })
                
                current_character = stripped
                current_dialogue = []
                current_parenthetical = ""
                preceding_action = self._get_preceding_action(lines, i)
                following_action = ""
                
            # Parenthetical
            elif stripped.startswith('(') and stripped.endswith(')'):
                current_parenthetical = stripped[1:-1]
                
            # Dialogue line
            elif current_character and stripped and not stripped.isupper():
                current_dialogue.append(stripped)
                
            # Action line after dialogue
            elif not current_character and stripped and not stripped.startswith((
                'INT.', 'EXT.', 'FADE', 'CUT'
            )):
                if dialogue_blocks:
                    dialogue_blocks[-1]['following_action'] = stripped
                    
        # Don't forget last dialogue block
        if current_character and current_dialogue:
            dialogue_blocks.append({
                'character': current_character,
                'dialogue': ' '.join(current_dialogue),
                'parenthetical': current_parenthetical,
                'preceding_action': preceding_action,
                'following_action': following_action,
                'line_number': len(lines)
            })
            
        return dialogue_blocks
        
    def _extract_scenes(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract scenes with their content."""
        scenes = []
        current_scene = None
        scene_content = []
        
        for line in lines:
            if any(line.strip().startswith(prefix) for prefix in ['INT.', 'EXT.']):
                if current_scene:
                    scenes.append({
                        'heading': current_scene,
                        'content': '\n'.join(scene_content)
                    })
                current_scene = line.strip()
                scene_content = []
            elif current_scene:
                scene_content.append(line)
                
        if current_scene:
            scenes.append({
                'heading': current_scene,
                'content': '\n'.join(scene_content)
            })
            
        return scenes
        
    def _get_preceding_action(self, lines: List[str], char_line: int) -> str:
        """Get action line preceding character name."""
        for i in range(char_line - 1, max(0, char_line - 5), -1):
            line = lines[i].strip()
            if line and not line.isupper() and not line.startswith((
                'INT.', 'EXT.', 'FADE', 'CUT', '('
            )):
                return line
        return ""
        
    def _analyze_subtext_depth(self, 
                               dialogue_blocks: List[Dict[str, Any]],
                               scenes: List[Dict[str, Any]]) -> SubtextAnalysis:
        """Analyze overall subtext depth."""
        analysis = SubtextAnalysis()
        
        if not dialogue_blocks:
            return analysis
            
        # Check for on-the-nose dialogue
        on_the_nose_count = 0
        for block in dialogue_blocks:
            dialogue = block['dialogue'].lower()
            if any(re.search(pattern, dialogue, re.I) 
                  for pattern in self.on_the_nose_phrases):
                on_the_nose_count += 1
                
        analysis.on_the_nose_ratio = on_the_nose_count / len(dialogue_blocks)
        
        # Check for contradictions between action and dialogue
        for block in dialogue_blocks:
            if self._has_contradiction(block):
                analysis.contradiction_count += 1
                
        # Check for avoidance patterns
        for block in dialogue_blocks:
            dialogue = block['dialogue'].lower()
            for pattern in self.avoidance_indicators:
                if re.search(pattern, dialogue, re.I):
                    analysis.avoidance_patterns.append(
                        f"{block['character']}: {pattern}"
                    )
                    
        # Check for meaningful silences (parentheticals indicating pauses)
        for block in dialogue_blocks:
            if 'beat' in block.get('parenthetical', '').lower() or \
               'pause' in block.get('parenthetical', '').lower():
                analysis.meaningful_silences += 1
                
        # Detect emotional layers
        analysis.emotional_layers = self._count_emotional_layers(dialogue_blocks)
        
        # Check for power dynamics
        analysis.power_dynamics_present = self._detect_power_dynamics(dialogue_blocks)
        
        # Check for hidden agendas
        analysis.hidden_agendas_detected = self._detect_hidden_agendas(dialogue_blocks)
        
        # Count double meanings
        analysis.double_meanings_count = self._count_double_meanings(dialogue_blocks)
        
        # Count ironic moments
        analysis.ironic_moments = self._count_ironic_moments(dialogue_blocks)
        
        # Calculate subtext depth score
        analysis.subtext_depth_score = self._calculate_subtext_depth_score(analysis)
        
        # Determine if subtext exists
        analysis.has_subtext = (
            analysis.subtext_depth_score > 0.3 or
            analysis.contradiction_count > 2 or
            len(analysis.avoidance_patterns) > 3
        )
        
        # Find examples
        analysis.subtext_examples = self._find_subtext_examples(dialogue_blocks)[:3]
        
        # Calculate payoff potential
        analysis.payoff_potential = self._calculate_payoff_potential(analysis)
        
        return analysis
        
    def _has_contradiction(self, block: Dict[str, Any]) -> bool:
        """Check if action contradicts dialogue."""
        dialogue = block['dialogue'].lower()
        action = (block.get('preceding_action', '') + ' ' + 
                 block.get('following_action', '')).lower()
                 
        # Simple contradiction patterns
        if 'fine' in dialogue or "okay" in dialogue or "great" in dialogue:
            if any(word in action for word in ['cry', 'tears', 'trembl', 'shak']):
                return True
                
        if 'don\'t care' in dialogue or 'doesn\'t matter' in dialogue:
            if any(word in action for word in ['stare', 'watch', 'focus', 'grip']):
                return True
                
        if 'hate' in dialogue:
            if any(word in action for word in ['smile', 'lean', 'touch']):
                return True
                
        return False
        
    def _count_emotional_layers(self, dialogue_blocks: List[Dict[str, Any]]) -> int:
        """Count emotional layers in dialogue."""
        layers = 0
        
        for block in dialogue_blocks:
            # Parenthetical adds layer
            if block.get('parenthetical'):
                layers += 1
                
            # Contradiction adds layer  
            if self._has_contradiction(block):
                layers += 1
                
            # Subtext indicators add layer
            dialogue = block['dialogue'].lower()
            if any(word in dialogue for word in self.contradiction_words):
                layers += 1
                
        return min(layers, 10)  # Cap at 10
        
    def _detect_power_dynamics(self, dialogue_blocks: List[Dict[str, Any]]) -> bool:
        """Detect if power dynamics are present in subtext."""
        power_indicators = [
            'sir', 'ma\'am', 'boss', 'please', 'sorry', 'excuse me',
            'if you don\'t mind', 'would you', 'could you', 'may I'
        ]
        
        dominance_indicators = [
            'listen', 'look', 'shut up', 'quiet', 'enough',
            'that\'s final', 'end of discussion', 'because I said so'
        ]
        
        for block in dialogue_blocks:
            dialogue = block['dialogue'].lower()
            if any(ind in dialogue for ind in power_indicators + dominance_indicators):
                return True
                
        return False
        
    def _detect_hidden_agendas(self, dialogue_blocks: List[Dict[str, Any]]) -> bool:
        """Detect if characters have hidden agendas."""
        agenda_indicators = [
            'by the way', 'speaking of', 'that reminds me',
            'while we\'re on the subject', 'incidentally',
            'before I forget', 'one more thing'
        ]
        
        deflection_count = 0
        for block in dialogue_blocks:
            dialogue = block['dialogue'].lower()
            if any(ind in dialogue for ind in agenda_indicators):
                deflection_count += 1
                
        return deflection_count >= 2
        
    def _count_double_meanings(self, dialogue_blocks: List[Dict[str, Any]]) -> int:
        """Count potential double meanings."""
        count = 0
        
        # Look for questions that aren't really questions
        for block in dialogue_blocks:
            dialogue = block['dialogue']
            if '?' in dialogue:
                # Rhetorical questions often have double meaning
                if any(word in dialogue.lower() for word in 
                      ['really', 'seriously', 'honestly', 'actually']):
                    count += 1
                    
        return count
        
    def _count_ironic_moments(self, dialogue_blocks: List[Dict[str, Any]]) -> int:
        """Count ironic moments in dialogue."""
        count = 0
        
        irony_indicators = [
            'perfect', 'great', 'wonderful', 'fantastic', 'brilliant',
            'just what I needed', 'exactly', 'of course', 'naturally'
        ]
        
        for block in dialogue_blocks:
            dialogue = block['dialogue'].lower()
            action = block.get('preceding_action', '').lower() + \
                    block.get('following_action', '').lower()
                    
            # Positive words with negative context suggest irony
            if any(word in dialogue for word in irony_indicators):
                if any(neg in action for neg in 
                      ['sigh', 'roll', 'shake', 'frown', 'glare']):
                    count += 1
                    
        return count
        
    def _calculate_subtext_depth_score(self, analysis: SubtextAnalysis) -> float:
        """Calculate overall subtext depth score."""
        score = 0.0
        
        # Penalize on-the-nose dialogue
        score += (1.0 - analysis.on_the_nose_ratio) * 0.3
        
        # Reward contradictions
        score += min(analysis.contradiction_count * 0.1, 0.2)
        
        # Reward avoidance patterns
        score += min(len(analysis.avoidance_patterns) * 0.05, 0.15)
        
        # Reward meaningful silences
        score += min(analysis.meaningful_silences * 0.05, 0.1)
        
        # Reward emotional layers
        score += (analysis.emotional_layers / 10.0) * 0.15
        
        # Bonus for advanced techniques
        if analysis.power_dynamics_present:
            score += 0.05
        if analysis.hidden_agendas_detected:
            score += 0.05
            
        return min(score, 1.0)
        
    def _find_subtext_examples(self, 
                               dialogue_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find best examples of subtext."""
        examples = []
        
        for block in dialogue_blocks:
            if self._has_contradiction(block):
                examples.append({
                    'type': 'contradiction',
                    'character': block['character'],
                    'dialogue': block['dialogue'][:100],
                    'action': block.get('following_action', '')[:100],
                    'explanation': 'Words and actions contradict'
                })
                
            # Check for deflection
            dialogue = block['dialogue'].lower()
            for pattern in self.avoidance_indicators:
                if re.search(pattern, dialogue, re.I):
                    examples.append({
                        'type': 'avoidance',
                        'character': block['character'],
                        'dialogue': block['dialogue'][:100],
                        'explanation': f'Character avoiding with "{pattern}"'
                    })
                    break
                    
        return examples[:5]  # Return top 5 examples
        
    def _calculate_payoff_potential(self, analysis: SubtextAnalysis) -> float:
        """Calculate potential for subtext payoff."""
        potential = 0.0
        
        # Hidden agendas have high payoff potential
        if analysis.hidden_agendas_detected:
            potential += 0.3
            
        # Power dynamics can lead to reversals
        if analysis.power_dynamics_present:
            potential += 0.2
            
        # Contradictions build tension
        if analysis.contradiction_count > 3:
            potential += 0.3
            
        # Avoidance suggests unresolved issues
        if len(analysis.avoidance_patterns) > 5:
            potential += 0.2
            
        return min(potential, 1.0)
        
    def _analyze_dialogue_layers(self, 
                                 dialogue_blocks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze layers of meaning in dialogue."""
        layers = {
            'surface_only': 0,
            'single_layer': 0,
            'double_layer': 0,
            'multi_layer': 0
        }
        
        for block in dialogue_blocks:
            layer_count = 0
            
            # Surface meaning always exists
            layer_count = 1
            
            # Parenthetical adds layer
            if block.get('parenthetical'):
                layer_count += 1
                
            # Contradiction adds layer
            if self._has_contradiction(block):
                layer_count += 1
                
            # Question marks might indicate another layer
            if '?' in block['dialogue'] and not block['dialogue'].strip().endswith('?'):
                layer_count += 1
                
            # Categorize
            if layer_count == 1:
                layers['surface_only'] += 1
            elif layer_count == 2:
                layers['single_layer'] += 1
            elif layer_count == 3:
                layers['double_layer'] += 1
            else:
                layers['multi_layer'] += 1
                
        return layers
        
    def _analyze_character_subtext(self, 
                                   dialogue_blocks: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Analyze subtext patterns by character."""
        character_patterns = {}
        
        for block in dialogue_blocks:
            char = block['character']
            if char not in character_patterns:
                character_patterns[char] = []
                
            # Check for patterns
            dialogue = block['dialogue'].lower()
            
            # Deflection
            if any(re.search(pat, dialogue, re.I) for pat in self.avoidance_indicators):
                character_patterns[char].append('deflection')
                
            # Contradiction
            if self._has_contradiction(block):
                character_patterns[char].append('contradiction')
                
            # Questions
            if '?' in dialogue:
                character_patterns[char].append('questioning')
                
            # Irony
            if any(word in dialogue for word in 
                  ['perfect', 'great', 'wonderful', 'fantastic']):
                if block.get('parenthetical'):
                    character_patterns[char].append('irony')
                    
        # Summarize patterns
        for char in character_patterns:
            patterns = character_patterns[char]
            unique_patterns = list(set(patterns))
            character_patterns[char] = unique_patterns
            
        return character_patterns
        
    def _calculate_scene_subtext_density(self, scenes: List[Dict[str, Any]]) -> float:
        """Calculate average subtext density across scenes."""
        if not scenes:
            return 0.0
            
        total_density = 0.0
        
        for scene in scenes:
            content = scene['content'].lower()
            density = 0.0
            
            # Check for subtext indicators
            for pattern in self.avoidance_indicators:
                if re.search(pattern, content, re.I):
                    density += 0.1
                    
            # Check for contradictory words
            for word in self.contradiction_words:
                density += content.count(word) * 0.05
                
            # Check for pauses/beats
            density += content.count('beat') * 0.1
            density += content.count('pause') * 0.1
            
            total_density += min(density, 1.0)
            
        return total_density / len(scenes)
        
    def _find_most_layered_exchanges(self, 
                                     dialogue_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find exchanges with most layers."""
        exchanges = []
        
        for i in range(len(dialogue_blocks) - 1):
            current = dialogue_blocks[i]
            next_block = dialogue_blocks[i + 1]
            
            # Check if it's an exchange (different characters)
            if current['character'] != next_block['character']:
                layers = 0
                
                # Count layers in exchange
                if self._has_contradiction(current):
                    layers += 1
                if self._has_contradiction(next_block):
                    layers += 1
                if current.get('parenthetical') or next_block.get('parenthetical'):
                    layers += 1
                    
                # Check for topic change (deflection)
                if any(ind in current['dialogue'].lower() + next_block['dialogue'].lower() 
                      for ind in ['anyway', 'speaking of', 'by the way']):
                    layers += 1
                    
                if layers > 0:
                    exchanges.append({
                        'characters': [current['character'], next_block['character']],
                        'first_line': current['dialogue'][:50],
                        'response': next_block['dialogue'][:50],
                        'layers': layers,
                        'techniques': self._identify_exchange_techniques(current, next_block)
                    })
                    
        # Sort by number of layers
        exchanges.sort(key=lambda x: x['layers'], reverse=True)
        
        return exchanges[:5]  # Return top 5
        
    def _identify_exchange_techniques(self, 
                                      block1: Dict[str, Any], 
                                      block2: Dict[str, Any]) -> List[str]:
        """Identify subtext techniques used in exchange."""
        techniques = []
        
        if self._has_contradiction(block1) or self._has_contradiction(block2):
            techniques.append('contradiction')
            
        if block1.get('parenthetical') or block2.get('parenthetical'):
            techniques.append('parenthetical_subtext')
            
        # Check for deflection
        combined = block1['dialogue'].lower() + block2['dialogue'].lower()
        if any(pat in combined for pat in ['anyway', 'nevermind', 'forget it']):
            techniques.append('deflection')
            
        # Check for questions
        if '?' in block1['dialogue'] or '?' in block2['dialogue']:
            techniques.append('loaded_questions')
            
        return techniques
        
    def _identify_techniques_used(self,
                                  dialogue_blocks: List[Dict[str, Any]],
                                  scenes: List[Dict[str, Any]]) -> List[str]:
        """Identify all subtext techniques used."""
        techniques = set()
        
        for block in dialogue_blocks:
            if self._has_contradiction(block):
                techniques.add('action_contradiction')
                
            if block.get('parenthetical'):
                techniques.add('parenthetical_meaning')
                
            dialogue = block['dialogue'].lower()
            
            if any(re.search(pat, dialogue, re.I) for pat in self.avoidance_indicators):
                techniques.add('deflection')
                
            if '?' in dialogue and not dialogue.strip().endswith('?'):
                techniques.add('buried_questions')
                
            if 'beat' in dialogue or 'pause' in dialogue:
                techniques.add('meaningful_silence')
                
            # Check for repetition
            words = dialogue.split()
            for word in set(words):
                if words.count(word) > 2 and len(word) > 3:
                    techniques.add('repetition_reveals')
                    break
                    
        return list(techniques)
        
    def _find_missing_opportunities(self, 
                                    dialogue_blocks: List[Dict[str, Any]]) -> List[str]:
        """Find missed opportunities for subtext."""
        opportunities = []
        
        for block in dialogue_blocks:
            dialogue = block['dialogue'].lower()
            
            # Direct emotional statements
            if any(phrase in dialogue for phrase in 
                  ['i love', 'i hate', 'i\'m angry', 'i\'m sad', 'i\'m happy']):
                opportunities.append(
                    f"Direct emotion from {block['character']} - could be shown through subtext"
                )
                
            # Exposition that could be subtext
            if 'because' in dialogue and len(dialogue) > 100:
                opportunities.append(
                    f"Explanation from {block['character']} - could be implied"
                )
                
            # Missing action contradictions
            if not block.get('preceding_action') and not block.get('following_action'):
                if any(word in dialogue for word in ['fine', 'okay', 'great']):
                    opportunities.append(
                        f"Potential for action contradiction with {block['character']}"
                    )
                    
        return opportunities[:5]  # Limit to 5
        
    def _check_rule_violations(self,
                               analysis: SubtextAnalysis,
                               dialogue_layers: Dict[str, int],
                               techniques: List[str]) -> List[Dict[str, Any]]:
        """Check for rule violations."""
        violations = []
        
        for rule in self.rules:
            if self._evaluate_rule(rule, analysis, dialogue_layers, techniques):
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
                      analysis: SubtextAnalysis,
                      dialogue_layers: Dict[str, int],
                      techniques: List[str]) -> bool:
        """Evaluate if a rule is violated."""
        rule_id = rule['id']
        
        # Subtext Present
        if rule_id == 'SUB.R001':
            return not analysis.has_subtext
            
        # Avoid On-the-Nose
        elif rule_id == 'SUB.R002':
            return analysis.on_the_nose_ratio > 0.5
            
        # Contradiction Creates Depth
        elif rule_id == 'SUB.R003':
            return analysis.contradiction_count == 0
            
        # Emotional Undercurrents
        elif rule_id == 'SUB.R004':
            return analysis.emotional_layers < 3
            
        # Power Games
        elif rule_id == 'SUB.R005':
            return not analysis.power_dynamics_present and len(techniques) > 2
            
        # Hidden Agendas
        elif rule_id == 'SUB.R006':
            return not analysis.hidden_agendas_detected and len(techniques) > 3
            
        # Double Meanings
        elif rule_id == 'SUB.R007':
            return analysis.double_meanings_count == 0 and dialogue_layers.get('multi_layer', 0) == 0
            
        # Avoidance Patterns
        elif rule_id == 'SUB.R008':
            return len(analysis.avoidance_patterns) == 0 and 'deflection' not in techniques
            
        # Context Changes Meaning
        elif rule_id == 'SUB.R009':
            return dialogue_layers.get('surface_only', 0) > dialogue_layers.get('multi_layer', 0) * 3
            
        # Silent Communication
        elif rule_id == 'SUB.R010':
            return analysis.meaningful_silences == 0 and 'meaningful_silence' not in techniques
            
        # Irony and Contradiction
        elif rule_id == 'SUB.R011':
            return analysis.ironic_moments == 0
            
        # Deflection Techniques
        elif rule_id == 'SUB.R012':
            return 'deflection' not in techniques and len(analysis.avoidance_patterns) == 0
            
        # Loaded Silences
        elif rule_id == 'SUB.R013':
            return analysis.meaningful_silences == 0
            
        # Repetition Reveals
        elif rule_id == 'SUB.R014':
            return 'repetition_reveals' not in techniques
            
        # Subtext Payoff
        elif rule_id == 'SUB.R015':
            return analysis.payoff_potential < 0.3
            
        return False
        
    def _generate_recommendations(self,
                                 analysis: SubtextAnalysis,
                                 violations: List[Dict[str, Any]],
                                 missing_ops: List[str]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Address critical violations first
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        for violation in critical_violations[:2]:
            recommendations.append(f"CRITICAL: {violation['fix']}")
            
        # Address on-the-nose dialogue
        if analysis.on_the_nose_ratio > 0.4:
            recommendations.append(
                "Reduce on-the-nose dialogue - characters state emotions too directly"
            )
            
        # Need more contradictions
        if analysis.contradiction_count < 2:
            recommendations.append(
                "Add contradictions between dialogue and action to create depth"
            )
            
        # Need more avoidance
        if len(analysis.avoidance_patterns) < 2:
            recommendations.append(
                "Have characters avoid difficult topics through deflection"
            )
            
        # Need meaningful pauses
        if analysis.meaningful_silences < 2:
            recommendations.append(
                "Use pauses and beats to create meaningful silences"
            )
            
        # Missing power dynamics
        if not analysis.power_dynamics_present:
            recommendations.append(
                "Consider adding power dynamics to relationships"
            )
            
        # Low payoff potential
        if analysis.payoff_potential < 0.3:
            recommendations.append(
                "Build subtext that pays off later in the story"
            )
            
        # Add missing opportunities
        if missing_ops:
            recommendations.append(
                f"Opportunity: {missing_ops[0]}"
            )
            
        return recommendations[:7]  # Limit to 7 recommendations
        
    def _calculate_score(self,
                        analysis: SubtextAnalysis,
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
            
        # Bonus for good subtext
        if analysis.has_subtext:
            base_score = min(base_score + 10, 100)
            
        # Bonus for depth
        base_score += int(analysis.subtext_depth_score * 10)
        
        # Penalty for too much on-the-nose
        if analysis.on_the_nose_ratio > 0.5:
            base_score -= 10
            
        # Bonus for advanced techniques
        if analysis.power_dynamics_present:
            base_score += 3
        if analysis.hidden_agendas_detected:
            base_score += 3
        if analysis.payoff_potential > 0.5:
            base_score += 5

        return max(5, min(95, base_score))

    def _generate_diagnosis(self, subtext_analysis: SubtextAnalysis,
                          violations: List[Dict[str, Any]]) -> str:
        """Generate narrative subtext diagnosis."""
        score = self._calculate_score(subtext_analysis, violations)
        diagnosis = f"Subtext Analysis Score: {score}/100\n\n"

        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent subtext! Your dialogue has rich layers of meaning. "
        elif score >= 70:
            diagnosis += "Good subtext foundation with some areas needing depth. "
        elif score >= 50:
            diagnosis += "Limited subtext - dialogue tends to be on-the-nose. "
        else:
            diagnosis += "Minimal subtext - characters state exactly what they mean. "

        # Subtext presence
        if not subtext_analysis.has_subtext:
            diagnosis += "WARNING: No subtext detected - dialogue lacks depth. "
        else:
            diagnosis += f"Subtext depth score: {subtext_analysis.subtext_depth_score:.2f}. "

        # On-the-nose ratio
        if subtext_analysis.on_the_nose_ratio > 0.6:
            diagnosis += "WARNING: Too much on-the-nose dialogue - characters state feelings directly. "
        elif subtext_analysis.on_the_nose_ratio < 0.3:
            diagnosis += "Good balance - characters communicate indirectly. "

        # Contradictions & layers
        if subtext_analysis.contradiction_count > 5:
            diagnosis += f"Good use of contradiction ({subtext_analysis.contradiction_count} instances). "
        elif subtext_analysis.contradiction_count == 0:
            diagnosis += "Add contradictions - characters saying one thing, meaning another. "

        # Power dynamics
        if not subtext_analysis.power_dynamics_present:
            diagnosis += "Missing power dynamics in relationships. "
        else:
            diagnosis += "Power dynamics create subtext richness. "

        # Hidden agendas
        if not subtext_analysis.hidden_agendas_detected:
            diagnosis += "Characters lack hidden agendas - add ulterior motives. "

        # Emotional layers
        if subtext_analysis.emotional_layers < 2:
            diagnosis += "Single-layer emotions - add complexity. "
        elif subtext_analysis.emotional_layers >= 4:
            diagnosis += "Rich emotional layers create depth. "

        # Meaningful silences
        if subtext_analysis.meaningful_silences < 3:
            diagnosis += "Add pauses and silences for subtext. "

        # Payoff potential
        if subtext_analysis.payoff_potential < 0.3:
            diagnosis += "Build subtext that pays off later. "

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            diagnosis += f"\n\nCRITICAL ISSUES ({len(critical_violations)}): "
            for v in critical_violations[:2]:
                diagnosis += f"{v['title']}. "

        return diagnosis.strip()
