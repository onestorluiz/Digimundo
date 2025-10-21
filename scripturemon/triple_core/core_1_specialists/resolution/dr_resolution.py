"""
Script Doctor Omegamon - Resolution and Closure Specialist
A Script Doctor™ in Digimon form specializing in endings and narrative closure.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class PlotThread:
    """Represents a plot thread to be resolved."""
    thread_id: str
    description: str
    introduced_page: int
    resolved: bool
    resolved_page: int
    resolution_quality: float  # 0-1
    thread_type: str  # main, subplot, character, relationship, mystery


@dataclass
class ResolutionElement:
    """Key element in resolution/denouement."""
    name: str
    present: bool
    effectiveness: float  # 0-1
    page_location: int
    notes: str


class DrResolution:
    """
    Script Doctor Omegamon - The Resolution and Closure Specialist
    
    A Script Doctor™ in Digimon form, specializing in analyzing endings,
    denouement, ensuring all threads are resolved, and emotional closure.
    
    Identity: Script Doctor first, Digimon resolution specialist second.
    """
    
    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Omegamon with rules and configuration."""
        self.name = "Script Doctor Omegamon"
        self.digimon_name = "Omegamon"
        self.title = "Script Doctor - Resolution and Closure Specialist"
        self.specialty = "Endings, denouement, loose threads, emotional closure"
        self.identity = "I am Script Doctor Omegamon, a professional Script Doctor™ specializing in resolution and closure"
        
        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "resolution_rules.yaml"
        
        self.rules = self._load_rules()
        
        # Resolution markers
        self.resolution_markers = [
            "the end", "fade out", "epilogue", "years later", "finally",
            "and so", "in the end", "conclusion", "resolution", "denouement"
        ]
        
        # Thread type patterns
        self.thread_patterns = {
            "mystery": ["who", "what", "where", "secret", "truth", "reveal"],
            "relationship": ["love", "friendship", "family", "together", "apart"],
            "quest": ["find", "search", "mission", "goal", "objective"],
            "conflict": ["versus", "fight", "enemy", "opponent", "rival"]
        }
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file."""
        try:
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules from {self.rules_path}: {e}")
            return {"rules": [], "resolution_checklist": {}}
    
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Perform complete resolution analysis of screenplay.
        
        Args:
            screenplay_text: The full screenplay text
        
        Returns:
            Complete resolution diagnostic report
        """
        lines = screenplay_text.split('\n')
        total_pages = len(lines) // 55 or 1
        
        # Locate resolution section
        resolution_location = self._locate_resolution(screenplay_text, total_pages)
        resolution_text = self._extract_resolution_text(screenplay_text, resolution_location)
        
        # Track plot threads
        plot_threads = self._track_plot_threads(screenplay_text)
        
        # Analyze resolution elements
        resolution_elements = self._analyze_resolution_elements(resolution_text, screenplay_text)
        
        # Check emotional satisfaction
        emotional_satisfaction = self._analyze_emotional_satisfaction(resolution_text, screenplay_text)
        
        # Analyze character arc completion
        character_arcs = self._analyze_character_arcs(screenplay_text, resolution_text)
        
        # Check theme resolution
        theme_resolved = self._check_theme_resolution(resolution_text, screenplay_text)
        
        # Analyze final image
        final_image = self._analyze_final_image(resolution_text, screenplay_text)
        
        # Check for new world order
        new_world = self._check_new_world_order(resolution_text)
        
        # Detect multiple endings
        multiple_endings = self._detect_multiple_endings(resolution_text)
        
        # Check against rules
        rule_violations = self._check_resolution_rules(
            resolution_text, plot_threads, resolution_elements,
            emotional_satisfaction, character_arcs, theme_resolved
        )
        
        # Calculate score
        score = self._calculate_resolution_score(
            plot_threads, resolution_elements, emotional_satisfaction,
            character_arcs, rule_violations
        )
        
        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, plot_threads, resolution_elements,
            emotional_satisfaction, rule_violations
        )
        
        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "resolution_location": {
                "page_start": resolution_location["start"],
                "page_end": resolution_location["end"],
                "duration_pages": resolution_location["end"] - resolution_location["start"],
                "percentage_of_script": ((resolution_location["end"] - resolution_location["start"]) / total_pages) * 100
            },
            "plot_threads": self._threads_to_dict(plot_threads),
            "threads_resolved_percentage": self._calculate_thread_resolution_rate(plot_threads),
            "resolution_elements": self._elements_to_dict(resolution_elements),
            "emotional_satisfaction_score": emotional_satisfaction,
            "character_arcs_completed": character_arcs["completion_rate"],
            "theme_resolved": theme_resolved,
            "final_image_strength": final_image["strength"],
            "final_image_mirrors_opening": final_image["mirrors_opening"],
            "new_world_established": new_world,
            "has_multiple_endings": multiple_endings,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, plot_threads, resolution_elements
            ),
            "signature": f"Diagnosed by {self.name}™"
        }
    
    def _locate_resolution(self, screenplay: str, total_pages: int) -> Dict[str, Any]:
        """Locate the resolution/denouement section."""
        lines = screenplay.split('\n')
        
        # Resolution typically starts after 90% mark
        expected_start = int(total_pages * 0.90)
        
        # Search for resolution markers
        resolution_found = False
        resolution_start = expected_start
        
        for i, line in enumerate(lines):
            current_page = (i // 55) + 1
            if current_page >= expected_start:
                for marker in self.resolution_markers:
                    if marker in line.lower():
                        resolution_start = current_page
                        resolution_found = True
                        break
            if resolution_found:
                break
        
        # If not found, assume last 10% is resolution
        if not resolution_found:
            resolution_start = expected_start
        
        return {
            "start": resolution_start,
            "end": total_pages,
            "found_by_marker": resolution_found
        }
    
    def _extract_resolution_text(self, screenplay: str, location: Dict) -> str:
        """Extract resolution portion of screenplay."""
        lines = screenplay.split('\n')
        start_line = (location["start"] - 1) * 55
        
        return '\n'.join(lines[start_line:])
    
    def _track_plot_threads(self, screenplay: str) -> List[PlotThread]:
        """Track all plot threads throughout screenplay."""
        threads = []
        lines = screenplay.split('\n')
        
        # Track various thread types
        potential_threads = defaultdict(dict)
        
        for i, line in enumerate(lines):
            current_page = (i // 55) + 1
            line_lower = line.lower()
            
            # Look for thread introductions (first 75% of script)
            if current_page < len(lines) // 55 * 0.75:
                # Mystery threads
                if any(word in line_lower for word in ["mystery", "secret", "hidden", "discover"]):
                    thread_id = f"mystery_{current_page}"
                    potential_threads[thread_id] = {
                        "type": "mystery",
                        "description": line.strip()[:50],
                        "introduced_page": current_page,
                        "resolved": False
                    }
                
                # Relationship threads
                if any(word in line_lower for word in ["love", "relationship", "marry", "together"]):
                    thread_id = f"relationship_{current_page}"
                    potential_threads[thread_id] = {
                        "type": "relationship",
                        "description": line.strip()[:50],
                        "introduced_page": current_page,
                        "resolved": False
                    }
                
                # Goal/quest threads
                if any(word in line_lower for word in ["must find", "need to", "have to", "mission"]):
                    thread_id = f"quest_{current_page}"
                    potential_threads[thread_id] = {
                        "type": "quest",
                        "description": line.strip()[:50],
                        "introduced_page": current_page,
                        "resolved": False
                    }
        
        # Check for resolutions in last 25%
        resolution_start = len(lines) // 55 * 0.75
        for i, line in enumerate(lines):
            current_page = (i // 55) + 1
            if current_page >= resolution_start:
                line_lower = line.lower()
                
                # Look for resolution keywords
                if any(word in line_lower for word in ["resolved", "solved", "found", "together", "finally"]):
                    # Mark relevant threads as resolved
                    for thread_id, thread_data in potential_threads.items():
                        if not thread_data["resolved"]:
                            # Simple heuristic - would be more sophisticated in production
                            if thread_data["type"] in line_lower or "finally" in line_lower:
                                thread_data["resolved"] = True
                                thread_data["resolved_page"] = current_page
        
        # Convert to PlotThread objects
        for thread_id, data in potential_threads.items():
            threads.append(PlotThread(
                thread_id=thread_id,
                description=data["description"],
                introduced_page=data["introduced_page"],
                resolved=data["resolved"],
                resolved_page=data.get("resolved_page", 0),
                resolution_quality=0.8 if data["resolved"] else 0.0,
                thread_type=data["type"]
            ))
        
        return threads[:10]  # Limit to 10 most important threads
    
    def _analyze_resolution_elements(self, resolution_text: str, full_screenplay: str) -> Dict[str, ResolutionElement]:
        """Analyze key elements in resolution."""
        elements = {}
        
        # Plot closure
        elements["plot_closure"] = ResolutionElement(
            name="Plot Closure",
            present=self._detect_plot_closure(resolution_text),
            effectiveness=0.7 if self._detect_plot_closure(resolution_text) else 0.2,
            page_location=0,
            notes="Main plot threads resolved"
        )
        
        # Emotional catharsis
        elements["emotional_catharsis"] = ResolutionElement(
            name="Emotional Catharsis",
            present=self._detect_emotional_catharsis(resolution_text),
            effectiveness=0.8 if self._detect_emotional_catharsis(resolution_text) else 0.3,
            page_location=0,
            notes="Emotional release/satisfaction"
        )
        
        # Character transformation shown
        elements["character_transformation"] = ResolutionElement(
            name="Character Transformation",
            present=self._detect_transformation(resolution_text, full_screenplay),
            effectiveness=0.8 if self._detect_transformation(resolution_text, full_screenplay) else 0.2,
            page_location=0,
            notes="Protagonist change demonstrated"
        )
        
        # Thematic statement
        elements["thematic_statement"] = ResolutionElement(
            name="Thematic Statement",
            present=self._detect_thematic_statement(resolution_text),
            effectiveness=0.7 if self._detect_thematic_statement(resolution_text) else 0.3,
            page_location=0,
            notes="Theme expressed through resolution"
        )
        
        # New equilibrium
        elements["new_equilibrium"] = ResolutionElement(
            name="New Equilibrium",
            present=self._detect_new_equilibrium(resolution_text),
            effectiveness=0.7 if self._detect_new_equilibrium(resolution_text) else 0.3,
            page_location=0,
            notes="New status quo established"
        )
        
        # Final image
        elements["final_image"] = ResolutionElement(
            name="Final Image",
            present="fade out" in resolution_text.lower() or "the end" in resolution_text.lower(),
            effectiveness=0.8 if "fade out" in resolution_text.lower() else 0.5,
            page_location=0,
            notes="Memorable closing image"
        )
        
        return elements
    
    def _analyze_emotional_satisfaction(self, resolution_text: str, full_screenplay: str) -> float:
        """Analyze emotional satisfaction level of resolution."""
        satisfaction_markers = [
            "happy", "joy", "peace", "content", "fulfilled", "complete",
            "together", "home", "safe", "free", "love", "smile", "laugh"
        ]
        
        bittersweet_markers = [
            "but", "although", "sacrifice", "lost", "gone", "memory",
            "remember", "never forget", "price", "cost"
        ]
        
        resolution_lower = resolution_text.lower()
        
        # Count emotional markers
        positive_count = sum(1 for marker in satisfaction_markers if marker in resolution_lower)
        bittersweet_count = sum(1 for marker in bittersweet_markers if marker in resolution_lower)
        
        # Calculate satisfaction score
        if positive_count > 5:
            base_score = 0.9
        elif positive_count > 3:
            base_score = 0.7
        elif positive_count > 1:
            base_score = 0.5
        else:
            base_score = 0.3
        
        # Adjust for complexity
        if bittersweet_count > 0:
            base_score = min(1.0, base_score + 0.1)  # Bittersweet can be more satisfying
        
        return base_score
    
    def _analyze_character_arcs(self, screenplay: str, resolution_text: str) -> Dict[str, Any]:
        """Analyze character arc completion."""
        # Simple heuristic - look for character names and their resolution
        character_names = self._extract_character_names(screenplay)
        
        completed_arcs = 0
        total_arcs = len(character_names)
        
        for character in character_names[:5]:  # Check top 5 characters
            if character.lower() in resolution_text.lower():
                completed_arcs += 1
        
        completion_rate = completed_arcs / max(1, total_arcs)
        
        return {
            "completion_rate": completion_rate,
            "completed": completed_arcs,
            "total": total_arcs
        }
    
    def _extract_character_names(self, screenplay: str) -> List[str]:
        """Extract character names from screenplay."""
        # Simple pattern: lines that are all caps and not scene headings
        lines = screenplay.split('\n')
        character_names = []
        
        for line in lines:
            line = line.strip()
            if line.isupper() and len(line.split()) <= 3:
                if not any(marker in line for marker in ["INT.", "EXT.", "FADE", "CUT TO"]):
                    character_names.append(line)
        
        # Get unique names
        unique_names = list(set(character_names))
        return unique_names[:10]  # Limit to 10 main characters
    
    def _check_theme_resolution(self, resolution_text: str, full_screenplay: str) -> bool:
        """Check if theme is resolved."""
        theme_markers = [
            "learned", "realized", "understood", "truth", "meaning",
            "what matters", "important", "lesson", "moral", "message"
        ]
        
        resolution_lower = resolution_text.lower()
        theme_count = sum(1 for marker in theme_markers if marker in resolution_lower)
        
        return theme_count >= 2
    
    def _analyze_final_image(self, resolution_text: str, full_screenplay: str) -> Dict[str, Any]:
        """Analyze the final image of the screenplay."""
        # Get first and last meaningful content
        opening_lines = '\n'.join(full_screenplay.split('\n')[:100])
        closing_lines = resolution_text.split('\n')[-50:]
        closing_text = '\n'.join(closing_lines)
        
        # Check for mirroring
        mirrors_opening = self._check_mirroring(opening_lines, closing_text)
        
        # Evaluate strength
        strength = 0.5  # Base strength
        
        if "fade out" in closing_text.lower():
            strength += 0.2
        if mirrors_opening:
            strength += 0.3
        
        return {
            "mirrors_opening": mirrors_opening,
            "strength": min(1.0, strength)
        }
    
    def _check_mirroring(self, opening: str, closing: str) -> bool:
        """Check if closing mirrors or contrasts opening."""
        # Simple check for shared keywords/themes
        opening_words = set(opening.lower().split())
        closing_words = set(closing.lower().split())
        
        # Check for significant overlap
        overlap = opening_words.intersection(closing_words)
        
        # Remove common words
        common = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for"}
        meaningful_overlap = overlap - common
        
        return len(meaningful_overlap) > 10
    
    def _check_new_world_order(self, resolution_text: str) -> bool:
        """Check if new world order is established."""
        new_world_markers = [
            "now", "new", "different", "changed", "transformed",
            "never be the same", "from now on", "beginning", "fresh start"
        ]
        
        resolution_lower = resolution_text.lower()
        marker_count = sum(1 for marker in new_world_markers if marker in resolution_lower)
        
        return marker_count >= 2
    
    def _detect_multiple_endings(self, resolution_text: str) -> bool:
        """Detect if there are multiple false endings."""
        ending_markers = ["the end", "fade out", "fade to black", "cut to black"]
        
        resolution_lower = resolution_text.lower()
        lines = resolution_lower.split('\n')
        
        ending_count = 0
        last_ending_line = -10
        
        for i, line in enumerate(lines):
            for marker in ending_markers:
                if marker in line:
                    # Check if this is far enough from last ending
                    if i - last_ending_line > 5:
                        ending_count += 1
                        last_ending_line = i
        
        return ending_count > 1
    
    def _detect_plot_closure(self, text: str) -> bool:
        """Detect if plot is closed."""
        closure_markers = ["resolved", "solved", "finished", "complete", "over", "done"]
        text_lower = text.lower()
        return any(marker in text_lower for marker in closure_markers)
    
    def _detect_emotional_catharsis(self, text: str) -> bool:
        """Detect emotional catharsis."""
        catharsis_markers = [
            "tears", "joy", "relief", "peace", "free", "weight lifted",
            "finally", "at last", "home", "complete"
        ]
        text_lower = text.lower()
        return sum(1 for marker in catharsis_markers if marker in text_lower) >= 2
    
    def _detect_transformation(self, resolution_text: str, full_screenplay: str) -> bool:
        """Detect if transformation is shown."""
        transformation_markers = [
            "changed", "different", "not the same", "transformed",
            "learned", "grew", "became", "no longer"
        ]
        resolution_lower = resolution_text.lower()
        return any(marker in resolution_lower for marker in transformation_markers)
    
    def _detect_thematic_statement(self, text: str) -> bool:
        """Detect thematic statement."""
        theme_markers = [
            "meaning", "truth", "lesson", "learned", "realized",
            "what matters", "important", "understand"
        ]
        text_lower = text.lower()
        return sum(1 for marker in theme_markers if marker in text_lower) >= 2
    
    def _detect_new_equilibrium(self, text: str) -> bool:
        """Detect new equilibrium establishment."""
        equilibrium_markers = [
            "new normal", "now", "from this day", "going forward",
            "life goes on", "continues", "begins"
        ]
        text_lower = text.lower()
        return any(marker in text_lower for marker in equilibrium_markers)
    
    def _calculate_thread_resolution_rate(self, threads: List[PlotThread]) -> float:
        """Calculate percentage of threads resolved."""
        if not threads:
            return 100.0
        
        resolved = sum(1 for t in threads if t.resolved)
        return (resolved / len(threads)) * 100
    
    def _check_resolution_rules(self, resolution_text: str, threads: List,
                               elements: Dict, emotional_satisfaction: float,
                               character_arcs: Dict, theme_resolved: bool) -> List[Dict]:
        """Check resolution against rules."""
        violations = []
        
        for rule in self.rules.get("rules", []):
            if rule["id"] == "OMEGA.R001":
                # Narrative closure
                unresolved = [t for t in threads if not t.resolved]
                if len(unresolved) > 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{len(unresolved)} unresolved plot threads",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "OMEGA.R002":
                # Emotional satisfaction
                if emotional_satisfaction < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low emotional satisfaction: {emotional_satisfaction:.0%}",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "OMEGA.R003":
                # Character arc completion
                if character_arcs["completion_rate"] < 0.6:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Only {character_arcs['completion_rate']:.0%} of arcs completed",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "OMEGA.R004":
                # Theme resolution
                if not theme_resolved:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Theme not addressed in resolution",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "OMEGA.R008":
                # Final image
                if not elements.get("final_image", ResolutionElement("", False, 0, 0, "")).present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Weak or missing final image",
                        "fix": rule["fix"]
                    })
        
        return violations
    
    def _calculate_resolution_score(self, threads: List, elements: Dict,
                                   emotional_satisfaction: float,
                                   character_arcs: Dict, violations: List) -> float:
        """Calculate overall resolution score."""
        score = 90.0
        
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
        
        # Factor in thread resolution
        thread_rate = self._calculate_thread_resolution_rate(threads) / 100
        score = score * 0.7 + (thread_rate * 100) * 0.1
        
        # Factor in emotional satisfaction
        score = score * 0.8 + (emotional_satisfaction * 100) * 0.1
        
        # Factor in character arc completion
        score = score * 0.9 + (character_arcs["completion_rate"] * 100) * 0.1
        
        return max(5.0, min(95.0, round(score, 1)))
    
    def _threads_to_dict(self, threads: List[PlotThread]) -> List[Dict]:
        """Convert threads to dictionary format."""
        return [
            {
                "thread_id": t.thread_id,
                "description": t.description,
                "introduced_page": t.introduced_page,
                "resolved": t.resolved,
                "resolved_page": t.resolved_page,
                "resolution_quality": round(t.resolution_quality, 2),
                "thread_type": t.thread_type
            }
            for t in threads[:5]  # Limit to 5 for readability
        ]
    
    def _elements_to_dict(self, elements: Dict[str, ResolutionElement]) -> Dict:
        """Convert elements to dictionary format."""
        result = {}
        for key, element in elements.items():
            result[key] = {
                "present": element.present,
                "effectiveness": round(element.effectiveness, 2),
                "notes": element.notes
            }
        return result
    
    def _generate_diagnosis(self, score: float, threads: List,
                          elements: Dict, emotional_satisfaction: float,
                          violations: List) -> str:
        """Generate narrative resolution diagnosis."""
        diagnosis = f"Resolution Analysis Score: {score}/100\n\n"
        
        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent resolution! All threads tied up with emotional satisfaction. "
        elif score >= 70:
            diagnosis += "Good resolution with minor loose threads or pacing issues. "
        elif score >= 50:
            diagnosis += "Resolution needs work - multiple unresolved elements. "
        else:
            diagnosis += "Major resolution problems - unsatisfying conclusion. "
        
        # Thread analysis
        unresolved = [t for t in threads if not t.resolved]
        if unresolved:
            diagnosis += f"{len(unresolved)} plot threads left hanging. "
        
        # Emotional analysis
        if emotional_satisfaction < 0.5:
            diagnosis += "Lacks emotional catharsis - feels incomplete. "
        elif emotional_satisfaction > 0.8:
            diagnosis += "Strong emotional payoff achieved. "
        
        # Missing elements
        missing = [name for name, elem in elements.items() if not elem.present]
        if missing:
            diagnosis += f"Missing: {', '.join(missing[:3])}. "
        
        # Critical issues
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical issues: {', '.join([v['title'] for v in critical])}."
        
        return diagnosis
    
    def _generate_recommendations(self, score: float, violations: List,
                                 threads: List, elements: Dict) -> List[str]:
        """Generate specific resolution recommendations."""
        recommendations = []
        
        # Top violations
        for violation in sorted(violations,
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 3:
                break
        
        # Unresolved threads
        unresolved = [t for t in threads if not t.resolved]
        if unresolved:
            recommendations.append(f"Resolve {len(unresolved)} open plot threads")
        
        # Missing elements
        if not elements.get("emotional_catharsis", ResolutionElement("", False, 0, 0, "")).present:
            recommendations.append("Add emotional catharsis moment")
        if not elements.get("new_equilibrium", ResolutionElement("", False, 0, 0, "")).present:
            recommendations.append("Show new world order after story events")
        
        # General advice
        if score < 70:
            recommendations.append("Study endings of similar successful films")
            recommendations.append("Ensure denouement is 3-5 pages, not rushed")
        
        return recommendations[:5]  # Limit to 5