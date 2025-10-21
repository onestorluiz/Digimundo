"""
Script Doctor Peakmon - Climax and Peak Moments Specialist
A Script Doctor™ in Digimon form specializing in climactic scenes and payoffs.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ClimaxElement:
    """Element of climactic sequence."""
    name: str
    present: bool
    intensity: float  # 0-1
    page_location: int
    effectiveness: float  # 0-1
    notes: str


@dataclass
class SetupPayoff:
    """Tracks setup and payoff pairs."""
    setup: str
    setup_page: int
    payoff: str
    payoff_page: int
    satisfied: bool
    impact: float  # 0-1


class DrClimax:
    """
    Script Doctor Peakmon - The Climax and Peak Moments Specialist
    
    A Script Doctor™ in Digimon form, specializing in analyzing climactic
    scenes, emotional peaks, and ensuring all setups have satisfying payoffs.
    
    Identity: Script Doctor first, Digimon climax specialist second.
    """
    
    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Peakmon with rules and configuration."""
        self.name = "Script Doctor Peakmon"
        self.digimon_name = "Peakmon"
        self.title = "Script Doctor - Climax and Peak Moments Specialist"
        self.specialty = "Climactic scenes, peak emotional moments, payoffs"
        self.identity = "I am Script Doctor Peakmon, a professional Script Doctor™ specializing in climactic moments and payoffs"
        
        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "climax_rules.yaml"
        
        self.rules = self._load_rules()
        
        # Climax indicators
        self.climax_markers = [
            "final battle", "final confrontation", "climax", "showdown",
            "all is lost", "darkest hour", "final stand", "last chance",
            "now or never", "point of no return", "do or die"
        ]
        
        # Intensity markers
        self.intensity_markers = {
            "high": ["explodes", "screams", "crashes", "shatters", "erupts", "devastating"],
            "medium": ["fights", "struggles", "confronts", "challenges", "faces"],
            "low": ["talks", "discusses", "considers", "thinks", "ponders"]
        }
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file."""
        try:
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules from {self.rules_path}: {e}")
            return {"rules": [], "climax_checklist": {}}
    
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Perform complete climax analysis of screenplay.
        
        Args:
            screenplay_text: The full screenplay text
        
        Returns:
            Complete climax diagnostic report
        """
        lines = screenplay_text.split('\n')
        total_pages = len(lines) // 55 or 1
        
        # Find and analyze climax
        climax_location = self._locate_climax(screenplay_text, total_pages)
        climax_text = self._extract_climax_text(screenplay_text, climax_location)
        
        # Analyze climax elements
        climax_elements = self._analyze_climax_elements(climax_text, climax_location)
        
        # Track setup/payoff
        setup_payoffs = self._analyze_setup_payoff(screenplay_text)
        
        # Calculate intensity
        intensity_score = self._calculate_intensity(climax_text)
        
        # Check protagonist agency
        protagonist_agency = self._check_protagonist_agency(climax_text)
        
        # Analyze emotional peak
        emotional_peak = self._analyze_emotional_peak(climax_text, screenplay_text)
        
        # Check for false victory/defeat
        false_moment = self._detect_false_victory_defeat(climax_text)
        
        # Verify theme expression
        theme_expression = self._check_theme_expression(climax_text)
        
        # Check against rules
        rule_violations = self._check_climax_rules(
            climax_text, climax_location, climax_elements,
            setup_payoffs, intensity_score, protagonist_agency
        )
        
        # Calculate score
        score = self._calculate_climax_score(
            climax_elements, setup_payoffs, intensity_score,
            protagonist_agency, rule_violations
        )
        
        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, climax_location, climax_elements,
            setup_payoffs, intensity_score, rule_violations
        )
        
        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "climax_location": {
                "page_start": climax_location["start"],
                "page_end": climax_location["end"],
                "percentage_point": climax_location["percentage"],
                "duration_pages": climax_location["end"] - climax_location["start"]
            },
            "intensity_score": intensity_score,
            "climax_elements": self._elements_to_dict(climax_elements),
            "setup_payoffs": self._payoffs_to_dict(setup_payoffs),
            "protagonist_agency": protagonist_agency,
            "emotional_peak_score": emotional_peak,
            "has_false_moment": false_moment["found"],
            "false_moment_type": false_moment.get("type", "none"),
            "theme_expressed": theme_expression,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, climax_elements, setup_payoffs
            ),
            "signature": f"Diagnosed by {self.name}™"
        }
    
    def _locate_climax(self, screenplay: str, total_pages: int) -> Dict[str, Any]:
        """Locate the climax in the screenplay."""
        lines = screenplay.split('\n')
        
        # Expected climax location (75-90% through script)
        expected_start = int(total_pages * 0.75)
        expected_end = int(total_pages * 0.90)
        
        # Search for climax markers
        climax_found = False
        climax_page = expected_start
        
        for i, line in enumerate(lines):
            current_page = (i // 55) + 1
            if expected_start <= current_page <= expected_end:
                for marker in self.climax_markers:
                    if marker in line.lower():
                        climax_page = current_page
                        climax_found = True
                        break
            if climax_found:
                break
        
        # If not found by markers, assume it's at 80%
        if not climax_found:
            climax_page = int(total_pages * 0.80)
        
        # Climax typically lasts 5-10% of script
        climax_duration = max(3, int(total_pages * 0.08))
        
        return {
            "start": climax_page,
            "end": min(climax_page + climax_duration, total_pages),
            "percentage": (climax_page / total_pages) * 100,
            "found_by_marker": climax_found
        }
    
    def _extract_climax_text(self, screenplay: str, location: Dict) -> str:
        """Extract the climax portion of screenplay."""
        lines = screenplay.split('\n')
        start_line = (location["start"] - 1) * 55
        end_line = location["end"] * 55
        
        return '\n'.join(lines[start_line:end_line])
    
    def _analyze_climax_elements(self, climax_text: str, location: Dict) -> Dict[str, ClimaxElement]:
        """Analyze key elements present in climax."""
        elements = {}
        text_lower = climax_text.lower()
        
        # Check for maximum conflict
        elements["maximum_conflict"] = ClimaxElement(
            name="Maximum Conflict",
            present=self._detect_conflict_level(climax_text) > 0.8,
            intensity=self._detect_conflict_level(climax_text),
            page_location=location["start"],
            effectiveness=self._detect_conflict_level(climax_text),
            notes="Highest level of conflict in story"
        )
        
        # Check for protagonist choice
        elements["protagonist_choice"] = ClimaxElement(
            name="Protagonist Choice",
            present=self._detect_choice(climax_text),
            intensity=0.9 if self._detect_choice(climax_text) else 0.2,
            page_location=location["start"],
            effectiveness=0.9 if self._detect_choice(climax_text) else 0.2,
            notes="Active protagonist decision"
        )
        
        # Check for time pressure
        elements["time_pressure"] = ClimaxElement(
            name="Time Pressure",
            present=self._detect_urgency(climax_text),
            intensity=0.8 if self._detect_urgency(climax_text) else 0.3,
            page_location=location["start"],
            effectiveness=0.8 if self._detect_urgency(climax_text) else 0.3,
            notes="Ticking clock or deadline"
        )
        
        # Check for visual action
        elements["visual_action"] = ClimaxElement(
            name="Visual Action",
            present=self._detect_visual_action(climax_text),
            intensity=self._calculate_action_density(climax_text),
            page_location=location["start"],
            effectiveness=self._calculate_action_density(climax_text),
            notes="Cinematic visual elements"
        )
        
        # Check for all is lost moment
        elements["all_is_lost"] = ClimaxElement(
            name="All Is Lost Moment",
            present="all is lost" in text_lower or "darkest hour" in text_lower,
            intensity=0.9 if "all is lost" in text_lower else 0.0,
            page_location=location["start"],
            effectiveness=0.9 if "all is lost" in text_lower else 0.0,
            notes="Protagonist at lowest point"
        )
        
        # Check for revelation
        elements["revelation"] = ClimaxElement(
            name="Revelation/Discovery",
            present=self._detect_revelation(climax_text),
            intensity=0.7 if self._detect_revelation(climax_text) else 0.0,
            page_location=location["start"],
            effectiveness=0.7 if self._detect_revelation(climax_text) else 0.0,
            notes="Key information revealed"
        )
        
        return elements
    
    def _analyze_setup_payoff(self, screenplay: str) -> List[SetupPayoff]:
        """Track setup and payoff throughout screenplay."""
        setup_payoffs = []
        lines = screenplay.split('\n')
        
        # Common setup/payoff patterns
        setup_patterns = [
            (r"plants?", r"uses?"),
            (r"hides?", r"reveals?"),
            (r"mentions?", r"returns?"),
            (r"promises?", r"delivers?"),
            (r"threatens?", r"executes?")
        ]
        
        # Track potential setups
        setups = {}
        
        for i, line in enumerate(lines):
            page = (i // 55) + 1
            
            # Look for setups in first 2/3 of script
            if page < len(lines) // 55 * 0.67:
                for setup_pattern, _ in setup_patterns:
                    if re.search(setup_pattern, line, re.I):
                        # Simple tracking - would be more sophisticated in production
                        key = f"{setup_pattern}_{page}"
                        setups[key] = {
                            "text": line.strip(),
                            "page": page,
                            "pattern": setup_pattern
                        }
        
        # Look for payoffs in last 1/3
        for i, line in enumerate(lines):
            page = (i // 55) + 1
            
            if page > len(lines) // 55 * 0.67:
                for setup_pattern, payoff_pattern in setup_patterns:
                    if re.search(payoff_pattern, line, re.I):
                        # Check if we have a matching setup
                        for key, setup in setups.items():
                            if setup["pattern"] == setup_pattern:
                                setup_payoffs.append(SetupPayoff(
                                    setup=setup["text"][:50],
                                    setup_page=setup["page"],
                                    payoff=line.strip()[:50],
                                    payoff_page=page,
                                    satisfied=True,
                                    impact=0.7  # Would calculate based on importance
                                ))
                                break
        
        return setup_payoffs
    
    def _calculate_intensity(self, climax_text: str) -> float:
        """Calculate intensity level of climax."""
        text_lower = climax_text.lower()
        words = text_lower.split()
        
        high_count = sum(1 for marker in self.intensity_markers["high"] 
                        if marker in text_lower)
        medium_count = sum(1 for marker in self.intensity_markers["medium"] 
                          if marker in text_lower)
        low_count = sum(1 for marker in self.intensity_markers["low"] 
                       if marker in text_lower)
        
        # Weight the scores
        intensity = (high_count * 1.0 + medium_count * 0.5 + low_count * 0.2)
        
        # Normalize to 0-1
        max_expected = 10  # Expected max intensity markers
        return min(1.0, intensity / max_expected)
    
    def _check_protagonist_agency(self, climax_text: str) -> Dict[str, Any]:
        """Check if protagonist is active in climax."""
        # Look for active verbs associated with main character
        active_verbs = [
            "decides", "chooses", "fights", "saves", "defeats",
            "destroys", "creates", "sacrifices", "confronts", "overcomes"
        ]
        
        passive_indicators = [
            "is saved", "is rescued", "watches", "waits", "hopes",
            "is helped", "gets lucky", "is given"
        ]
        
        text_lower = climax_text.lower()
        
        active_count = sum(1 for verb in active_verbs if verb in text_lower)
        passive_count = sum(1 for indicator in passive_indicators if indicator in text_lower)
        
        agency_score = (active_count - passive_count) / max(1, active_count + passive_count)
        
        return {
            "has_agency": agency_score > 0.3,
            "agency_score": max(0, min(1, (agency_score + 1) / 2)),  # Normalize to 0-1
            "active_actions": active_count,
            "passive_moments": passive_count
        }
    
    def _analyze_emotional_peak(self, climax_text: str, full_screenplay: str) -> float:
        """Analyze if climax is emotional peak."""
        # Emotional intensity markers
        emotion_markers = [
            "tears", "cries", "screams", "loves", "hates", "fears",
            "desperate", "heart", "soul", "everything", "nothing left",
            "final", "last chance", "goodbye", "forgive", "sorry"
        ]
        
        climax_emotion = sum(1 for marker in emotion_markers 
                           if marker in climax_text.lower())
        
        # Compare to rest of screenplay
        full_emotion = sum(1 for marker in emotion_markers 
                          if marker in full_screenplay.lower())
        
        # Climax should have high concentration of emotion
        climax_density = climax_emotion / max(1, len(climax_text.split()))
        full_density = full_emotion / max(1, len(full_screenplay.split()))
        
        # Score based on relative density
        if climax_density > full_density * 2:
            return 1.0
        elif climax_density > full_density * 1.5:
            return 0.8
        elif climax_density > full_density:
            return 0.6
        else:
            return 0.4
    
    def _detect_false_victory_defeat(self, climax_text: str) -> Dict[str, Any]:
        """Detect false victory or defeat before real climax."""
        victory_markers = ["wins", "succeeds", "triumphs", "defeats", "victory"]
        defeat_markers = ["loses", "fails", "defeated", "lost", "over"]
        reversal_markers = ["but", "however", "suddenly", "then", "until"]
        
        text_lower = climax_text.lower()
        lines = text_lower.split('\n')
        
        false_moment_found = False
        false_type = "none"
        
        for i, line in enumerate(lines[:-10]):  # Not in final lines
            # Check for victory followed by reversal
            if any(marker in line for marker in victory_markers):
                # Check next few lines for reversal
                next_lines = ' '.join(lines[i:i+5])
                if any(marker in next_lines for marker in reversal_markers):
                    false_moment_found = True
                    false_type = "false_victory"
                    break
            
            # Check for defeat followed by reversal
            if any(marker in line for marker in defeat_markers):
                next_lines = ' '.join(lines[i:i+5])
                if any(marker in next_lines for marker in reversal_markers):
                    false_moment_found = True
                    false_type = "false_defeat"
                    break
        
        return {
            "found": false_moment_found,
            "type": false_type
        }
    
    def _check_theme_expression(self, climax_text: str) -> bool:
        """Check if theme is expressed through climax."""
        # Look for thematic language
        theme_indicators = [
            "what really matters", "learned", "realized", "understood",
            "truth", "meaning", "purpose", "believe", "stand for",
            "fight for", "die for", "live for", "worth", "value"
        ]
        
        text_lower = climax_text.lower()
        theme_count = sum(1 for indicator in theme_indicators if indicator in text_lower)
        
        return theme_count >= 2  # At least 2 thematic elements
    
    def _detect_conflict_level(self, text: str) -> float:
        """Detect level of conflict in text."""
        conflict_markers = [
            "fight", "battle", "struggle", "confront", "clash", "oppose",
            "versus", "against", "conflict", "showdown", "face off", "duel"
        ]
        
        text_lower = text.lower()
        conflict_count = sum(1 for marker in conflict_markers if marker in text_lower)
        
        # Normalize
        return min(1.0, conflict_count / 5)  # 5 markers = max conflict
    
    def _detect_choice(self, text: str) -> bool:
        """Detect if protagonist makes a choice."""
        choice_markers = [
            "chooses", "decides", "must choose", "has to decide",
            "makes the choice", "picks", "selects", "opts", "elects"
        ]
        
        text_lower = text.lower()
        return any(marker in text_lower for marker in choice_markers)
    
    def _detect_urgency(self, text: str) -> bool:
        """Detect time pressure/urgency."""
        urgency_markers = [
            "time", "seconds", "minutes", "countdown", "before",
            "too late", "hurry", "quick", "fast", "now or never",
            "last chance", "running out", "deadline", "ticking"
        ]
        
        text_lower = text.lower()
        return sum(1 for marker in urgency_markers if marker in text_lower) >= 2
    
    def _detect_visual_action(self, text: str) -> bool:
        """Detect visual/cinematic action."""
        action_markers = [
            "runs", "jumps", "fights", "crashes", "explodes", "falls",
            "leaps", "dives", "shoots", "strikes", "hits", "dodges",
            "chases", "escapes", "climbs", "swings", "flies", "speeds"
        ]
        
        text_lower = text.lower()
        return sum(1 for marker in action_markers if marker in text_lower) >= 3
    
    def _calculate_action_density(self, text: str) -> float:
        """Calculate density of action in text."""
        action_words = self._detect_visual_action(text)
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        # Count action words
        action_markers = [
            "runs", "jumps", "fights", "crashes", "explodes", "falls",
            "leaps", "dives", "shoots", "strikes", "hits", "dodges"
        ]
        
        action_count = sum(1 for word in text.lower().split() 
                          if word in action_markers)
        
        density = action_count / word_count
        return min(1.0, density * 20)  # Scale up for visibility
    
    def _detect_revelation(self, text: str) -> bool:
        """Detect revelation or discovery."""
        revelation_markers = [
            "reveals", "discovers", "realizes", "understands", "sees",
            "truth", "secret", "hidden", "finally", "all along", "actually"
        ]
        
        text_lower = text.lower()
        return sum(1 for marker in revelation_markers if marker in text_lower) >= 2
    
    def _check_climax_rules(self, climax_text: str, location: Dict,
                           elements: Dict, payoffs: List,
                           intensity: float, agency: Dict) -> List[Dict]:
        """Check climax against rules."""
        violations = []
        
        for rule in self.rules.get("rules", []):
            if rule["id"] == "PEAK.R001":
                # Climax intensity
                if intensity < 0.7:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Climax intensity only {intensity*100:.0f}%",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PEAK.R002":
                # Setup payoff
                unpaid_setups = [p for p in payoffs if not p.satisfied]
                if len(unpaid_setups) > 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{len(unpaid_setups)} setups without payoffs",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PEAK.R003":
                # Protagonist agency
                if not agency["has_agency"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Protagonist passive in climax",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PEAK.R006":
                # Ticking clock
                if not elements.get("time_pressure", ClimaxElement("", False, 0, 0, 0, "")).present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No time pressure in climax",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PEAK.R015":
                # Climax duration
                duration = location["end"] - location["start"]
                total_pages = location["end"]  # Approximate
                percentage = (duration / total_pages) * 100 if total_pages > 0 else 0
                
                if percentage < 5 or percentage > 15:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Climax is {percentage:.0f}% of script (should be 5-15%)",
                        "fix": rule["fix"]
                    })
        
        return violations
    
    def _calculate_climax_score(self, elements: Dict, payoffs: List,
                               intensity: float, agency: Dict,
                               violations: List) -> float:
        """Calculate overall climax score."""
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
        
        # Factor in intensity
        score = score * 0.7 + (intensity * 100) * 0.1
        
        # Factor in protagonist agency
        score = score * 0.8 + (agency["agency_score"] * 100) * 0.1
        
        # Factor in essential elements
        essential_count = sum(1 for e in elements.values() if e.present)
        element_score = (essential_count / len(elements)) * 100 if elements else 0
        score = score * 0.9 + element_score * 0.1
        
        return max(0, min(100, round(score, 1)))
    
    def _elements_to_dict(self, elements: Dict[str, ClimaxElement]) -> Dict:
        """Convert elements to dictionary format."""
        result = {}
        for key, element in elements.items():
            result[key] = {
                "present": element.present,
                "intensity": round(element.intensity, 2),
                "effectiveness": round(element.effectiveness, 2),
                "notes": element.notes
            }
        return result
    
    def _payoffs_to_dict(self, payoffs: List[SetupPayoff]) -> List[Dict]:
        """Convert payoffs to dictionary format."""
        return [
            {
                "setup": p.setup,
                "setup_page": p.setup_page,
                "payoff": p.payoff,
                "payoff_page": p.payoff_page,
                "satisfied": p.satisfied,
                "impact": round(p.impact, 2)
            }
            for p in payoffs[:10]  # Limit to 10 for readability
        ]
    
    def _generate_diagnosis(self, score: float, location: Dict,
                          elements: Dict, payoffs: List,
                          intensity: float, violations: List) -> str:
        """Generate narrative climax diagnosis."""
        diagnosis = f"Climax Analysis Score: {score}/100\n\n"
        
        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent climax! Peak moment delivers maximum impact with strong payoffs. "
        elif score >= 70:
            diagnosis += "Good climax foundation but missing some essential elements. "
        elif score >= 50:
            diagnosis += "Climax needs significant strengthening to deliver satisfying peak. "
        else:
            diagnosis += "Major climax problems - not delivering the emotional/narrative peak needed. "
        
        # Location analysis
        if location["percentage"] < 70:
            diagnosis += f"Climax too early at {location['percentage']:.0f}% (should be 75-85%). "
        elif location["percentage"] > 90:
            diagnosis += f"Climax too late at {location['percentage']:.0f}% (should be 75-85%). "
        
        # Intensity analysis
        if intensity < 0.5:
            diagnosis += "Low intensity - climax feels flat and underpowered. "
        elif intensity > 0.8:
            diagnosis += "Excellent intensity - climax delivers maximum impact. "
        
        # Element analysis
        missing_elements = [name for name, elem in elements.items() if not elem.present]
        if missing_elements:
            diagnosis += f"Missing key elements: {', '.join(missing_elements[:3])}. "
        
        # Critical issues
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical issues: {', '.join([v['title'] for v in critical])}."
        
        return diagnosis
    
    def _generate_recommendations(self, score: float, violations: List,
                                 elements: Dict, payoffs: List) -> List[str]:
        """Generate specific climax recommendations."""
        recommendations = []
        
        # Top violations
        for violation in sorted(violations,
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 3:
                break
        
        # Missing elements
        missing_critical = []
        if not elements.get("protagonist_choice", ClimaxElement("", False, 0, 0, 0, "")).present:
            recommendations.append("Make protagonist actively choose the outcome")
        if not elements.get("time_pressure", ClimaxElement("", False, 0, 0, 0, "")).present:
            recommendations.append("Add ticking clock or deadline to climax")
        if not elements.get("all_is_lost", ClimaxElement("", False, 0, 0, 0, "")).present:
            recommendations.append("Add 'all is lost' moment before victory")
        
        # Setup/payoff issues
        unpaid = [p for p in payoffs if not p.satisfied]
        if len(unpaid) > 2:
            recommendations.append(f"Pay off {len(unpaid)} unresolved setups in climax")
        
        # General advice
        if score < 70:
            recommendations.append("Study climaxes in similar genre films")
            recommendations.append("Ensure climax is highest point of tension")
        
        return recommendations[:5]  # Limit to 5