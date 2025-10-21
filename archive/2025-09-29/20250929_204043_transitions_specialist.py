"""
Script Doctor Flowmon - Transitions and Flow Specialist
A Script Doctor™ in Digimon form specializing in scene transitions and narrative flow.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class SceneTransition:
    """Represents a transition between two scenes."""
    from_scene: int
    to_scene: int
    from_location: str
    to_location: str
    transition_type: str  # CUT TO, DISSOLVE TO, etc.
    connection_type: str  # cause_effect, temporal, thematic, etc.
    effectiveness: float  # 0-1
    momentum_maintained: bool
    notes: str


@dataclass
class FlowSegment:
    """A segment of narrative flow (group of connected scenes)."""
    scenes: List[int]
    flow_quality: float  # 0-1
    segment_type: str  # main_plot, subplot, sequence
    momentum_score: float
    has_clear_progression: bool


class DrTransitions:
    """
    Script Doctor Flowmon - The Transitions and Flow Specialist
    
    A Script Doctor™ in Digimon form, specializing in analyzing scene transitions,
    narrative flow, and ensuring seamless connectivity between scenes.
    
    Identity: Script Doctor first, Digimon flow specialist second.
    """
    
    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Flowmon with rules and configuration."""
        self.name = "Script Doctor Flowmon"
        self.digimon_name = "Flowmon"
        self.title = "Script Doctor - Transitions and Flow Specialist"
        self.specialty = "Scene transitions, narrative flow, connective tissue, seamless storytelling"
        self.identity = "I am Script Doctor Flowmon, a professional Script Doctor™ specializing in transitions and flow"
        
        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "transitions_rules.yaml"
        
        self.rules = self._load_rules()
        
        # Transition types
        self.transition_types = [
            "CUT TO:", "DISSOLVE TO:", "FADE TO:", "FADE IN:", "FADE OUT:",
            "MATCH CUT:", "SMASH CUT:", "IRIS OUT:", "WIPE TO:", "LATER",
            "CONTINUOUS", "INTERCUT", "CROSS FADE:"
        ]
        
        # Connection types
        self.connection_patterns = {
            "cause_effect": ["because", "therefore", "so", "thus", "causes", "leads to"],
            "temporal": ["later", "earlier", "meanwhile", "simultaneously", "then", "before", "after"],
            "thematic": ["similarly", "likewise", "contrast", "parallel", "echo"],
            "emotional": ["feels", "mood", "tension", "relief", "joy", "sorrow"],
            "visual": ["match", "similar", "same", "mirror", "reflects"]
        }
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file."""
        try:
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules from {self.rules_path}: {e}")
            return {"rules": [], "transition_checklist": {}}
    
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Perform complete transitions and flow analysis of screenplay.
        
        Args:
            screenplay_text: The full screenplay text
        
        Returns:
            Complete flow diagnostic report
        """
        # Extract scenes
        scenes = self._extract_scenes(screenplay_text)
        
        # Analyze transitions
        transitions = self._analyze_transitions(scenes)
        
        # Analyze flow segments
        flow_segments = self._identify_flow_segments(scenes, transitions)
        
        # Calculate momentum
        momentum_analysis = self._analyze_momentum(scenes, transitions)
        
        # Check time flow
        time_flow_clear = self._check_time_flow(scenes)
        
        # Analyze transition variety
        transition_variety = self._analyze_transition_variety(transitions)
        
        # Check subplot integration
        subplot_integration = self._analyze_subplot_integration(scenes, flow_segments)
        
        # Analyze enter late/leave early
        scene_efficiency = self._analyze_scene_efficiency(scenes)
        
        # Check geographic logic
        geographic_logic = self._check_geographic_logic(scenes)
        
        # Check against rules
        rule_violations = self._check_flow_rules(
            transitions, flow_segments, momentum_analysis,
            time_flow_clear, transition_variety, subplot_integration
        )
        
        # Calculate score
        score = self._calculate_flow_score(
            transitions, flow_segments, momentum_analysis,
            rule_violations, scene_efficiency
        )
        
        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, transitions, flow_segments,
            momentum_analysis, rule_violations
        )
        
        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "scene_count": len(scenes),
            "transition_count": len(transitions),
            "transitions": self._transitions_to_dict(transitions),
            "flow_segments": self._segments_to_dict(flow_segments),
            "momentum_score": momentum_analysis["overall_momentum"],
            "momentum_drops": momentum_analysis["momentum_drops"],
            "time_flow_clear": time_flow_clear,
            "transition_variety_score": transition_variety["variety_score"],
            "most_used_transition": transition_variety["most_common"],
            "subplot_integration_score": subplot_integration,
            "scene_efficiency_score": scene_efficiency["efficiency_score"],
            "scenes_starting_late": scene_efficiency["starting_late_percentage"],
            "geographic_logic_score": geographic_logic,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, transitions, momentum_analysis
            ),
            "signature": f"Diagnosed by {self.name}™"
        }
    
    def _extract_scenes(self, screenplay: str) -> List[Dict[str, Any]]:
        """Extract all scenes from screenplay."""
        scenes = []
        lines = screenplay.split('\n')
        
        scene_pattern = re.compile(r'^(INT\.|EXT\.|INT/EXT\.)\s+(.+?)\s*[-–]?\s*(DAY|NIGHT|DAWN|DUSK|CONTINUOUS)?', re.IGNORECASE)
        transition_pattern = re.compile(r'^(CUT TO:|DISSOLVE TO:|FADE TO:|MATCH CUT:|SMASH CUT:|FADE OUT|FADE IN)', re.IGNORECASE)
        
        current_scene = None
        scene_number = 0
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for scene heading
            scene_match = scene_pattern.match(line_stripped)
            if scene_match:
                # Save previous scene
                if current_scene:
                    current_scene["end_line"] = i - 1
                    current_scene["content"] = '\n'.join(lines[current_scene["start_line"]:i])
                    scenes.append(current_scene)
                
                # Start new scene
                scene_number += 1
                location_type = scene_match.group(1)
                location = scene_match.group(2) if scene_match.group(2) else ""
                time = scene_match.group(3) if scene_match.group(3) else "DAY"
                
                current_scene = {
                    "number": scene_number,
                    "heading": line_stripped,
                    "location_type": location_type,
                    "location": location,
                    "time": time,
                    "start_line": i,
                    "transition_in": "",
                    "transition_out": ""
                }
            
            # Check for transition
            elif transition_pattern.match(line_stripped) and current_scene:
                current_scene["transition_out"] = line_stripped
        
        # Don't forget last scene
        if current_scene:
            current_scene["end_line"] = len(lines) - 1
            current_scene["content"] = '\n'.join(lines[current_scene["start_line"]:])
            scenes.append(current_scene)
        
        return scenes
    
    def _analyze_transitions(self, scenes: List[Dict]) -> List[SceneTransition]:
        """Analyze transitions between scenes."""
        transitions = []
        
        for i in range(len(scenes) - 1):
            from_scene = scenes[i]
            to_scene = scenes[i + 1]
            
            # Determine transition type
            transition_type = from_scene.get("transition_out", "CUT TO:")
            if not transition_type:
                transition_type = "CUT TO:"  # Default
            
            # Determine connection type
            connection_type = self._determine_connection_type(from_scene, to_scene)
            
            # Evaluate effectiveness
            effectiveness = self._evaluate_transition_effectiveness(
                from_scene, to_scene, transition_type, connection_type
            )
            
            # Check momentum
            momentum_maintained = self._check_momentum(from_scene, to_scene)
            
            transitions.append(SceneTransition(
                from_scene=from_scene["number"],
                to_scene=to_scene["number"],
                from_location=from_scene["location"],
                to_location=to_scene["location"],
                transition_type=transition_type,
                connection_type=connection_type,
                effectiveness=effectiveness,
                momentum_maintained=momentum_maintained,
                notes=self._get_transition_notes(from_scene, to_scene)
            ))
        
        return transitions
    
    def _determine_connection_type(self, from_scene: Dict, to_scene: Dict) -> str:
        """Determine the type of connection between scenes."""
        from_content = from_scene.get("content", "").lower()
        to_content = to_scene.get("content", "").lower()
        
        # Check for cause-effect
        if any(word in to_content[:200] for word in ["because", "therefore", "so", "result"]):
            return "cause_effect"
        
        # Check for temporal
        if to_scene["time"] != from_scene["time"]:
            return "temporal"
        if any(word in to_scene["heading"].lower() for word in ["later", "earlier", "continuous"]):
            return "temporal"
        
        # Check for geographic
        if from_scene["location"] != to_scene["location"]:
            return "geographic"
        
        # Check for thematic
        # Simple heuristic - check for shared keywords
        from_words = set(from_content.split())
        to_words = set(to_content.split())
        overlap = from_words.intersection(to_words)
        if len(overlap) > 20:
            return "thematic"
        
        # Check for character continuity
        if self._has_character_continuity(from_scene, to_scene):
            return "character"
        
        return "standard"
    
    def _has_character_continuity(self, from_scene: Dict, to_scene: Dict) -> bool:
        """Check if same character appears in both scenes."""
        # Extract character names (lines in all caps)
        from_chars = re.findall(r'^([A-Z][A-Z\s]+)$', from_scene.get("content", ""), re.MULTILINE)
        to_chars = re.findall(r'^([A-Z][A-Z\s]+)$', to_scene.get("content", ""), re.MULTILINE)
        
        # Check for overlap
        from_set = set(from_chars)
        to_set = set(to_chars)
        
        return bool(from_set.intersection(to_set))
    
    def _evaluate_transition_effectiveness(self, from_scene: Dict, to_scene: Dict,
                                          transition_type: str, connection_type: str) -> float:
        """Evaluate how effective a transition is."""
        effectiveness = 0.5  # Base score
        
        # Bonus for clear connection
        if connection_type in ["cause_effect", "temporal", "character"]:
            effectiveness += 0.2
        
        # Bonus for appropriate transition type
        if transition_type != "CUT TO:":  # Using variety
            effectiveness += 0.1
        
        # Bonus for smooth location/time flow
        if from_scene["location"] == to_scene["location"]:
            effectiveness += 0.1
        elif from_scene["time"] == to_scene["time"]:
            effectiveness += 0.05
        
        # Check for jarring elements
        if self._is_jarring_transition(from_scene, to_scene):
            effectiveness -= 0.3
        
        return max(0, min(1, effectiveness))
    
    def _is_jarring_transition(self, from_scene: Dict, to_scene: Dict) -> bool:
        """Check if transition is jarring."""
        # Check for major time jump without indication
        time_change = from_scene["time"] != to_scene["time"]
        location_change = from_scene["location"] != to_scene["location"]
        
        # Both change without clear transition
        if time_change and location_change and "LATER" not in to_scene["heading"]:
            return True
        
        return False
    
    def _check_momentum(self, from_scene: Dict, to_scene: Dict) -> bool:
        """Check if momentum is maintained between scenes."""
        from_content = from_scene.get("content", "")
        to_content = to_scene.get("content", "")
        
        # Check if from_scene ends with question/conflict
        momentum_markers = ["?", "!", "...", "but", "however", "suddenly"]
        from_ending = from_content[-200:] if len(from_content) > 200 else from_content
        
        has_momentum_ending = any(marker in from_ending for marker in momentum_markers)
        
        # Check if to_scene starts with energy
        energy_starters = ["runs", "bursts", "crashes", "immediately", "suddenly"]
        to_beginning = to_content[:200] if len(to_content) > 200 else to_content
        
        has_energy_start = any(starter in to_beginning.lower() for starter in energy_starters)
        
        return has_momentum_ending or has_energy_start
    
    def _get_transition_notes(self, from_scene: Dict, to_scene: Dict) -> str:
        """Generate notes about the transition."""
        notes = []
        
        if from_scene["location"] == to_scene["location"]:
            notes.append("Same location")
        if from_scene["time"] != to_scene["time"]:
            notes.append(f"Time shift: {from_scene['time']} to {to_scene['time']}")
        
        return "; ".join(notes) if notes else "Standard transition"
    
    def _identify_flow_segments(self, scenes: List[Dict],
                               transitions: List[SceneTransition]) -> List[FlowSegment]:
        """Identify connected flow segments."""
        segments = []
        
        if not scenes:
            return segments
        
        current_segment_scenes = [1]
        
        for i, transition in enumerate(transitions):
            # Check if flow continues
            if transition.effectiveness > 0.6 and transition.momentum_maintained:
                current_segment_scenes.append(transition.to_scene)
            else:
                # End current segment
                if len(current_segment_scenes) > 1:
                    segment = self._create_flow_segment(current_segment_scenes, scenes, transitions)
                    segments.append(segment)
                
                # Start new segment
                current_segment_scenes = [transition.to_scene]
        
        # Don't forget last segment
        if len(current_segment_scenes) > 1:
            segment = self._create_flow_segment(current_segment_scenes, scenes, transitions)
            segments.append(segment)
        
        return segments
    
    def _create_flow_segment(self, scene_numbers: List[int],
                            scenes: List[Dict],
                            transitions: List[SceneTransition]) -> FlowSegment:
        """Create a flow segment from scene numbers."""
        # Calculate flow quality
        relevant_transitions = [
            t for t in transitions
            if t.from_scene in scene_numbers and t.to_scene in scene_numbers
        ]
        
        if relevant_transitions:
            avg_effectiveness = sum(t.effectiveness for t in relevant_transitions) / len(relevant_transitions)
            momentum_score = sum(1 for t in relevant_transitions if t.momentum_maintained) / len(relevant_transitions)
        else:
            avg_effectiveness = 0.5
            momentum_score = 0.5
        
        # Determine segment type
        if len(scene_numbers) > 5:
            segment_type = "sequence"
        elif len(scene_numbers) > 2:
            segment_type = "mini_sequence"
        else:
            segment_type = "scene_pair"
        
        return FlowSegment(
            scenes=scene_numbers,
            flow_quality=avg_effectiveness,
            segment_type=segment_type,
            momentum_score=momentum_score,
            has_clear_progression=momentum_score > 0.6
        )
    
    def _analyze_momentum(self, scenes: List[Dict],
                         transitions: List[SceneTransition]) -> Dict[str, Any]:
        """Analyze overall momentum throughout screenplay."""
        if not transitions:
            return {"overall_momentum": 0, "momentum_drops": []}
        
        momentum_maintained = sum(1 for t in transitions if t.momentum_maintained)
        overall_momentum = momentum_maintained / len(transitions)
        
        # Find momentum drops
        momentum_drops = []
        for i, transition in enumerate(transitions):
            if not transition.momentum_maintained and i > 0:
                if transitions[i-1].momentum_maintained:  # Was maintaining, now dropped
                    momentum_drops.append({
                        "scene": transition.from_scene,
                        "location": f"Scene {transition.from_scene} to {transition.to_scene}"
                    })
        
        return {
            "overall_momentum": overall_momentum,
            "momentum_drops": momentum_drops
        }
    
    def _check_time_flow(self, scenes: List[Dict]) -> bool:
        """Check if time progression is clear."""
        time_markers = ["LATER", "EARLIER", "CONTINUOUS", "MOMENTS LATER", "NEXT DAY"]
        
        time_clear_count = 0
        time_changes = 0
        
        for i in range(len(scenes) - 1):
            if scenes[i]["time"] != scenes[i+1]["time"]:
                time_changes += 1
                # Check if marked
                if any(marker in scenes[i+1]["heading"].upper() for marker in time_markers):
                    time_clear_count += 1
        
        if time_changes == 0:
            return True
        
        return (time_clear_count / time_changes) > 0.5
    
    def _analyze_transition_variety(self, transitions: List[SceneTransition]) -> Dict[str, Any]:
        """Analyze variety in transition types."""
        if not transitions:
            return {"variety_score": 0, "most_common": "None"}
        
        # Count transition types
        type_counts = defaultdict(int)
        for transition in transitions:
            type_counts[transition.transition_type] += 1
        
        # Calculate variety score
        unique_types = len(type_counts)
        total_transitions = len(transitions)
        
        variety_score = min(1.0, unique_types / 5)  # 5 different types = perfect variety
        
        # Find most common
        most_common = max(type_counts, key=type_counts.get)
        
        # Penalize if one type dominates
        if type_counts[most_common] / total_transitions > 0.8:
            variety_score *= 0.5
        
        return {
            "variety_score": variety_score,
            "most_common": most_common,
            "type_distribution": dict(type_counts)
        }
    
    def _analyze_subplot_integration(self, scenes: List[Dict],
                                    segments: List[FlowSegment]) -> float:
        """Analyze how well subplots are integrated."""
        # Simple heuristic - check for alternating pattern
        if len(segments) < 3:
            return 0.5
        
        # Check if segments alternate between different threads
        alternations = 0
        for i in range(len(segments) - 1):
            # Different segment types suggest different plot threads
            if segments[i].segment_type != segments[i+1].segment_type:
                alternations += 1
        
        integration_score = alternations / (len(segments) - 1) if len(segments) > 1 else 0
        
        return min(1.0, integration_score * 1.5)  # Scale up
    
    def _analyze_scene_efficiency(self, scenes: List[Dict]) -> Dict[str, Any]:
        """Analyze if scenes enter late and leave early."""
        efficient_scenes = 0
        
        for scene in scenes:
            content = scene.get("content", "")
            if not content:
                continue
            
            # Check for efficient start (action/dialogue early)
            lines = content.split('\n')
            non_empty_lines = [l for l in lines if l.strip()]
            
            if len(non_empty_lines) > 3:
                # Check if starts with action or dialogue (not description)
                first_content = non_empty_lines[1] if len(non_empty_lines) > 1 else ""
                if first_content.strip().isupper() or any(word in first_content.lower() 
                    for word in ["bursts", "runs", "enters", "grabs", "shoots"]):
                    efficient_scenes += 1
        
        efficiency_score = efficient_scenes / len(scenes) if scenes else 0
        
        return {
            "efficiency_score": efficiency_score,
            "starting_late_percentage": efficiency_score * 100
        }
    
    def _check_geographic_logic(self, scenes: List[Dict]) -> float:
        """Check if location changes make geographic sense."""
        illogical_jumps = 0
        
        for i in range(len(scenes) - 1):
            from_location = scenes[i]["location"]
            to_location = scenes[i+1]["location"]
            
            # Check for impossible geography
            if "NEW YORK" in from_location and "LOS ANGELES" in to_location:
                # Check if time passed
                if scenes[i]["time"] == scenes[i+1]["time"]:
                    illogical_jumps += 1
            
            # Add more geographic logic checks as needed
        
        logic_score = 1.0 - (illogical_jumps / max(1, len(scenes) - 1))
        return max(0, logic_score)
    
    def _check_flow_rules(self, transitions: List, segments: List,
                         momentum: Dict, time_clear: bool,
                         variety: Dict, subplot_integration: float) -> List[Dict]:
        """Check flow against rules."""
        violations = []
        
        for rule in self.rules.get("rules", []):
            if rule["id"] == "FLOW.R001":
                # Scene transition logic
                illogical = [t for t in transitions if t.effectiveness < 0.4]
                if len(illogical) > len(transitions) * 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{len(illogical)} illogical transitions",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "FLOW.R002":
                # Momentum maintenance
                if momentum["overall_momentum"] < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Momentum only {momentum['overall_momentum']*100:.0f}%",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "FLOW.R003":
                # Transition variety
                if variety["variety_score"] < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low variety: mostly {variety['most_common']}",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "FLOW.R004":
                # Time flow clarity
                if not time_clear:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Time progression unclear",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "FLOW.R007":
                # Subplot weaving
                if subplot_integration < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Subplots feel chunky, not woven",
                        "fix": rule["fix"]
                    })
        
        return violations
    
    def _calculate_flow_score(self, transitions: List, segments: List,
                             momentum: Dict, violations: List,
                             efficiency: Dict) -> float:
        """Calculate overall flow score."""
        score = 100.0
        
        # Deduct for violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 20
            elif violation["severity"] == "high":
                score -= 15
            elif violation["severity"] == "medium":
                score -= 8
            else:
                score -= 4
        
        # Factor in momentum
        score = score * 0.7 + (momentum["overall_momentum"] * 100) * 0.1
        
        # Factor in transition effectiveness
        if transitions:
            avg_effectiveness = sum(t.effectiveness for t in transitions) / len(transitions)
            score = score * 0.8 + (avg_effectiveness * 100) * 0.1
        
        # Factor in efficiency
        score = score * 0.9 + (efficiency["efficiency_score"] * 100) * 0.1
        
        return max(0, min(100, round(score, 1)))
    
    def _transitions_to_dict(self, transitions: List[SceneTransition]) -> List[Dict]:
        """Convert transitions to dictionary format."""
        return [
            {
                "from_scene": t.from_scene,
                "to_scene": t.to_scene,
                "type": t.transition_type,
                "connection": t.connection_type,
                "effectiveness": round(t.effectiveness, 2),
                "momentum_maintained": t.momentum_maintained,
                "notes": t.notes
            }
            for t in transitions[:10]  # Limit to 10 for readability
        ]
    
    def _segments_to_dict(self, segments: List[FlowSegment]) -> List[Dict]:
        """Convert flow segments to dictionary format."""
        return [
            {
                "scenes": s.scenes,
                "flow_quality": round(s.flow_quality, 2),
                "type": s.segment_type,
                "momentum_score": round(s.momentum_score, 2),
                "has_progression": s.has_clear_progression
            }
            for s in segments[:5]  # Limit to 5 for readability
        ]
    
    def _generate_diagnosis(self, score: float, transitions: List,
                          segments: List, momentum: Dict,
                          violations: List) -> str:
        """Generate narrative flow diagnosis."""
        diagnosis = f"Flow Analysis Score: {score}/100\n\n"
        
        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent flow! Seamless transitions with maintained momentum. "
        elif score >= 70:
            diagnosis += "Good flow with minor connectivity issues. "
        elif score >= 50:
            diagnosis += "Flow problems affecting narrative momentum. "
        else:
            diagnosis += "Major flow issues - screenplay feels disjointed. "
        
        # Momentum analysis
        if momentum["overall_momentum"] < 0.5:
            diagnosis += f"Low momentum ({momentum['overall_momentum']*100:.0f}%) - story drags. "
        
        # Transition analysis
        if transitions:
            poor_transitions = [t for t in transitions if t.effectiveness < 0.5]
            if poor_transitions:
                diagnosis += f"{len(poor_transitions)} weak transitions breaking flow. "
        
        # Segment analysis
        if segments:
            good_segments = [s for s in segments if s.flow_quality > 0.7]
            if len(good_segments) < len(segments) / 2:
                diagnosis += "Few sustained flow sequences. "
        
        # Critical issues
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical issues: {', '.join([v['title'] for v in critical])}."
        
        return diagnosis
    
    def _generate_recommendations(self, score: float, violations: List,
                                 transitions: List, momentum: Dict) -> List[str]:
        """Generate specific flow recommendations."""
        recommendations = []
        
        # Top violations
        for violation in sorted(violations,
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 3:
                break
        
        # Momentum issues
        if momentum["overall_momentum"] < 0.5:
            recommendations.append("Add questions/conflicts at scene ends to pull forward")
        
        if momentum["momentum_drops"]:
            recommendations.append(f"Fix momentum drops at scenes {', '.join([str(d['scene']) for d in momentum['momentum_drops'][:3]])}")
        
        # Transition issues
        weak_transitions = [t for t in transitions if t.effectiveness < 0.5]
        if len(weak_transitions) > 3:
            recommendations.append("Strengthen scene connections with clear cause-effect or time markers")
        
        # General advice
        if score < 70:
            recommendations.append("Study transitions in well-paced films")
            recommendations.append("Read script aloud to feel flow breaks")
        
        return recommendations[:5]  # Limit to 5