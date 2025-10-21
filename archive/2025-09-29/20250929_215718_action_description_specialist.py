"""
Script Doctor Actionmon - Action Description and Visual Prose Specialist
A Script Doctor™ in Digimon form specializing in action lines and visual storytelling.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter


@dataclass
class ActionLine:
    """Analysis of a single action line or paragraph."""
    line_number: int
    text: str
    word_count: int
    verb_strength: float  # 0-1
    visual_clarity: float  # 0-1
    has_unfilmables: bool
    tense_issues: bool
    voice_issues: bool
    shows_not_tells: bool
    emotional_context: bool


@dataclass
class CharacterIntroduction:
    """Analysis of a character introduction."""
    character_name: str
    line_number: int
    has_age_range: bool
    has_visual_description: bool
    description_quality: float  # 0-1
    introduction_text: str


class DrActionDescription:
    """
    Script Doctor Actionmon - The Action Description and Visual Prose Specialist

    A Script Doctor™ in Digimon form, specializing in action lines,
    visual storytelling, and cinematic prose.

    Identity: Script Doctor first, Digimon action specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Actionmon with rules and configuration."""
        self.name = "Script Doctor Actionmon"
        self.digimon_name = "Actionmon"
        self.title = "Script Doctor - Action Description and Visual Prose Specialist"
        self.specialty = "Action lines, visual storytelling, descriptive prose, cinematic writing"
        self.identity = "I am Script Doctor Actionmon, a professional Script Doctor™ specializing in action"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "action_description_rules.yaml"

        self.rules = self._load_rules()

        # Language patterns
        self.weak_verbs = [
            'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'has', 'have', 'had', 'do', 'does', 'did',
            'go', 'goes', 'went', 'walk', 'walks', 'walked',
            'move', 'moves', 'moved', 'look', 'looks', 'looked'
        ]

        self.strong_verbs = [
            'sprint', 'dash', 'leap', 'plunge', 'slam', 'crash',
            'explode', 'shatter', 'pierce', 'slice', 'thrust',
            'glide', 'swagger', 'stumble', 'creep', 'lunge'
        ]

        self.telling_phrases = [
            'feels', 'thinks', 'remembers', 'realizes', 'knows',
            'wants', 'needs', 'hopes', 'wishes', 'believes',
            'seems', 'appears to be', 'looks like'
        ]

        self.unfilmable_words = [
            'remembers', 'thinks', 'realizes', 'knows', 'believes',
            'used to', 'would often', 'has always', 'never before'
        ]

        self.camera_directions = [
            'ANGLE ON', 'CLOSE ON', 'PAN', 'ZOOM', 'TRACK',
            'DOLLY', 'CRANE', 'POV', 'ECU', 'CU', 'WIDE SHOT'
        ]

        self.passive_indicators = [
            'is being', 'was being', 'are being', 'were being',
            'has been', 'have been', 'had been', 'will be'
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze action description and visual prose in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete action diagnostic report
        """
        lines = screenplay_text.split('\n')

        # Extract action lines
        action_lines = self._extract_action_lines(lines)

        # Analyze each action line
        analyzed_actions = [self._analyze_action_line(i, line)
                          for i, line in action_lines]

        # Check character introductions
        character_intros = self._analyze_character_introductions(lines)

        # Analyze show vs tell
        show_tell_analysis = self._analyze_show_vs_tell(analyzed_actions)

        # Check tense and voice
        grammar_analysis = self._analyze_grammar(analyzed_actions)

        # Analyze visual clarity
        visual_analysis = self._analyze_visual_clarity(analyzed_actions)

        # Check for unfilmables
        unfilmable_analysis = self._check_unfilmables(analyzed_actions)

        # Analyze verb usage
        verb_analysis = self._analyze_verbs(analyzed_actions)

        # Check paragraph length
        paragraph_analysis = self._analyze_paragraph_length(lines)

        # Analyze cinematic quality
        cinematic_analysis = self._analyze_cinematic_quality(analyzed_actions)

        # Check spatial clarity
        spatial_analysis = self._analyze_spatial_clarity(action_lines)

        # Analyze emotional context
        emotional_analysis = self._analyze_emotional_context(analyzed_actions)

        # Check for camera directions
        camera_analysis = self._check_camera_directions(action_lines)

        # Check against rules
        rule_violations = self._check_action_rules(
            show_tell_analysis, grammar_analysis, visual_analysis,
            unfilmable_analysis, paragraph_analysis, character_intros
        )

        # Calculate score
        score = self._calculate_action_score(
            analyzed_actions, rule_violations, show_tell_analysis,
            grammar_analysis, visual_analysis
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, analyzed_actions, rule_violations
        )

        # Get problematic lines
        problem_lines = self._get_problem_lines(analyzed_actions)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "total_action_lines": len(action_lines),
            "show_vs_tell_ratio": show_tell_analysis["show_ratio"],
            "telling_instances": show_tell_analysis["telling_count"],
            "present_tense_percentage": grammar_analysis["present_tense_percentage"],
            "active_voice_percentage": grammar_analysis["active_voice_percentage"],
            "tense_issues_count": grammar_analysis["tense_issues"],
            "voice_issues_count": grammar_analysis["voice_issues"],
            "visual_clarity_score": visual_analysis["clarity_score"],
            "highly_visual_lines": visual_analysis["highly_visual_count"],
            "unfilmable_count": unfilmable_analysis["count"],
            "unfilmable_examples": unfilmable_analysis["examples"],
            "weak_verb_percentage": verb_analysis["weak_verb_percentage"],
            "strong_verb_count": verb_analysis["strong_verb_count"],
            "vivid_verb_examples": verb_analysis["vivid_examples"],
            "average_paragraph_length": paragraph_analysis["average_length"],
            "overlong_paragraphs": paragraph_analysis["overlong_count"],
            "cinematic_score": cinematic_analysis["score"],
            "reads_like_movie": cinematic_analysis["reads_like_movie"],
            "spatial_clarity_score": spatial_analysis["score"],
            "emotional_context_present": emotional_analysis["present"],
            "emotional_moments": emotional_analysis["moment_count"],
            "camera_directions_found": camera_analysis["count"],
            "character_intro_count": len(character_intros),
            "well_introduced_characters": sum(1 for c in character_intros
                                            if c.description_quality > 0.7),
            "problem_lines": problem_lines,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, analyzed_actions,
                show_tell_analysis, grammar_analysis
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _extract_action_lines(self, lines: List[str]) -> List[Tuple[int, str]]:
        """Extract action lines from screenplay."""
        action_lines = []
        in_dialogue = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                in_dialogue = False
                continue

            # Skip scene headings
            if any(stripped.startswith(x) for x in ['INT.', 'EXT.', 'INT/', 'EXT/']):
                in_dialogue = False
                continue

            # Skip transitions
            if any(stripped.endswith(x) for x in [':', 'TO:', 'OUT.', 'IN.']):
                in_dialogue = False
                continue

            # Character name (dialogue starts)
            if stripped.isupper() and len(stripped.split()) <= 3:
                in_dialogue = True
                continue

            # Skip dialogue and parentheticals
            if in_dialogue:
                continue

            # Skip parentheticals even outside dialogue
            if stripped.startswith('(') and stripped.endswith(')'):
                continue

            # This is an action line
            action_lines.append((i, stripped))

        return action_lines

    def _analyze_action_line(self, line_number: int, text: str) -> ActionLine:
        """Analyze a single action line."""
        words = text.split()
        word_count = len(words)

        # Check verb strength
        verb_strength = self._calculate_verb_strength(text)

        # Check visual clarity
        visual_clarity = self._calculate_visual_clarity(text)

        # Check for unfilmables
        has_unfilmables = any(word in text.lower() for word in self.unfilmable_words)

        # Check tense
        tense_issues = self._has_tense_issues(text)

        # Check voice
        voice_issues = self._has_voice_issues(text)

        # Check show vs tell
        shows_not_tells = not any(phrase in text.lower() for phrase in self.telling_phrases)

        # Check emotional context
        emotional_context = self._has_emotional_context(text)

        return ActionLine(
            line_number=line_number,
            text=text,
            word_count=word_count,
            verb_strength=verb_strength,
            visual_clarity=visual_clarity,
            has_unfilmables=has_unfilmables,
            tense_issues=tense_issues,
            voice_issues=voice_issues,
            shows_not_tells=shows_not_tells,
            emotional_context=emotional_context
        )

    def _calculate_verb_strength(self, text: str) -> float:
        """Calculate strength of verbs used."""
        words = text.lower().split()

        weak_count = sum(1 for word in words if word in self.weak_verbs)
        strong_count = sum(1 for word in words if word in self.strong_verbs)

        if weak_count + strong_count == 0:
            return 0.5

        strength = strong_count / (weak_count + strong_count)
        return min(1.0, strength * 1.5)  # Boost a bit

    def _calculate_visual_clarity(self, text: str) -> float:
        """Calculate visual clarity of description."""
        score = 0.5  # Base score

        # Specific visual words increase clarity
        visual_words = ['color', 'shape', 'size', 'texture', 'light', 'shadow',
                       'red', 'blue', 'green', 'dark', 'bright', 'tall', 'small']

        text_lower = text.lower()
        for word in visual_words:
            if word in text_lower:
                score += 0.1

        # Action verbs increase clarity
        action_verbs = ['runs', 'jumps', 'falls', 'crashes', 'explodes', 'breaks']
        for verb in action_verbs:
            if verb in text_lower:
                score += 0.1

        # Vague words decrease clarity
        vague_words = ['something', 'somehow', 'somewhere', 'thing', 'stuff']
        for word in vague_words:
            if word in text_lower:
                score -= 0.1

        return max(0.0, min(1.0, score))

    def _has_tense_issues(self, text: str) -> bool:
        """Check if text has tense issues."""
        past_tense_markers = ['was', 'were', 'had', 'did', 'went', 'came', 'saw']
        text_lower = text.lower()

        return any(f' {marker} ' in f' {text_lower} ' for marker in past_tense_markers)

    def _has_voice_issues(self, text: str) -> bool:
        """Check if text has passive voice issues."""
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in self.passive_indicators)

    def _has_emotional_context(self, text: str) -> bool:
        """Check if action conveys emotion."""
        emotion_words = [
            'angry', 'sad', 'happy', 'afraid', 'nervous', 'excited',
            'tears', 'smile', 'frown', 'tense', 'relaxed', 'shaking'
        ]

        text_lower = text.lower()
        return any(word in text_lower for word in emotion_words)

    def _analyze_character_introductions(self, lines: List[str]) -> List[CharacterIntroduction]:
        """Analyze how characters are introduced."""
        introductions = []
        introduced = set()

        for i, line in enumerate(lines):
            # Look for character names in action lines
            if not line.strip() or line.strip().isupper():
                continue

            # Check for capitalized names (character intros)
            words = line.split()
            for word in words:
                # Check if it's a name (capitalized, not first word)
                if (word.isupper() and
                    len(word) > 2 and
                    word not in introduced and
                    not word.endswith('.')):

                    introduced.add(word)

                    # Check quality of introduction
                    has_age = any(x in line.lower() for x in ['20s', '30s', '40s', '50s', 'young', 'old', 'teen'])
                    has_visual = len(line) > 20  # Simple heuristic

                    quality = 0.3
                    if has_age:
                        quality += 0.35
                    if has_visual:
                        quality += 0.35

                    introductions.append(CharacterIntroduction(
                        character_name=word,
                        line_number=i,
                        has_age_range=has_age,
                        has_visual_description=has_visual,
                        description_quality=quality,
                        introduction_text=line[:100]
                    ))

        return introductions

    def _analyze_show_vs_tell(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Analyze show vs tell ratio."""
        showing = sum(1 for a in actions if a.shows_not_tells)
        telling = len(actions) - showing

        return {
            "showing_count": showing,
            "telling_count": telling,
            "show_ratio": showing / max(len(actions), 1),
            "examples": [a.text[:50] for a in actions if not a.shows_not_tells][:3]
        }

    def _analyze_grammar(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Analyze grammar issues."""
        tense_issues = sum(1 for a in actions if a.tense_issues)
        voice_issues = sum(1 for a in actions if a.voice_issues)

        total = max(len(actions), 1)

        return {
            "tense_issues": tense_issues,
            "voice_issues": voice_issues,
            "present_tense_percentage": ((total - tense_issues) / total) * 100,
            "active_voice_percentage": ((total - voice_issues) / total) * 100
        }

    def _analyze_visual_clarity(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Analyze visual clarity of action lines."""
        if not actions:
            return {"clarity_score": 0, "highly_visual_count": 0}

        clarity_scores = [a.visual_clarity for a in actions]
        avg_clarity = sum(clarity_scores) / len(clarity_scores)

        return {
            "clarity_score": avg_clarity,
            "highly_visual_count": sum(1 for s in clarity_scores if s > 0.7),
            "low_clarity_count": sum(1 for s in clarity_scores if s < 0.3)
        }

    def _check_unfilmables(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Check for unfilmable elements."""
        unfilmable_lines = [a for a in actions if a.has_unfilmables]

        return {
            "count": len(unfilmable_lines),
            "percentage": (len(unfilmable_lines) / max(len(actions), 1)) * 100,
            "examples": [a.text[:50] for a in unfilmable_lines][:3]
        }

    def _analyze_verbs(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Analyze verb usage in action lines."""
        all_verbs = []
        weak_count = 0
        strong_count = 0

        for action in actions:
            words = action.text.lower().split()
            for word in words:
                if word in self.weak_verbs:
                    weak_count += 1
                    all_verbs.append(word)
                elif word in self.strong_verbs:
                    strong_count += 1
                    all_verbs.append(word)

        total_verbs = max(weak_count + strong_count, 1)

        return {
            "weak_verb_count": weak_count,
            "strong_verb_count": strong_count,
            "weak_verb_percentage": (weak_count / total_verbs) * 100,
            "vivid_examples": [v for v in all_verbs if v in self.strong_verbs][:5]
        }

    def _analyze_paragraph_length(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze action paragraph lengths."""
        paragraphs = []
        current = []

        for line in lines:
            stripped = line.strip()

            # Skip dialogue and scene headings
            if (not stripped or
                stripped.isupper() or
                any(stripped.startswith(x) for x in ['INT.', 'EXT.'])):

                if current:
                    paragraphs.append(len(current))
                    current = []
                continue

            current.append(line)

        if current:
            paragraphs.append(len(current))

        if not paragraphs:
            return {"average_length": 0, "overlong_count": 0}

        avg_length = sum(paragraphs) / len(paragraphs)
        overlong = sum(1 for p in paragraphs if p > 4)

        return {
            "average_length": avg_length,
            "overlong_count": overlong,
            "paragraph_count": len(paragraphs)
        }

    def _analyze_cinematic_quality(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Analyze if prose reads cinematically."""
        if not actions:
            return {"score": 0, "reads_like_movie": False}

        # Factors that make it cinematic
        cinematic_score = 0.5  # Base

        # Visual clarity adds to cinematic quality
        avg_visual = sum(a.visual_clarity for a in actions) / len(actions)
        cinematic_score += avg_visual * 0.2

        # Present tense adds to cinematic quality
        present_tense_ratio = sum(1 for a in actions if not a.tense_issues) / len(actions)
        cinematic_score += present_tense_ratio * 0.15

        # Strong verbs add to cinematic quality
        strong_verb_ratio = sum(a.verb_strength for a in actions) / len(actions)
        cinematic_score += strong_verb_ratio * 0.15

        return {
            "score": min(1.0, cinematic_score),
            "reads_like_movie": cinematic_score > 0.7
        }

    def _analyze_spatial_clarity(self, action_lines: List[Tuple[int, str]]) -> Dict[str, Any]:
        """Analyze spatial clarity in action."""
        spatial_words = [
            'left', 'right', 'above', 'below', 'behind', 'front',
            'across', 'between', 'near', 'far', 'center', 'corner'
        ]

        lines_with_spatial = 0
        for _, text in action_lines:
            if any(word in text.lower() for word in spatial_words):
                lines_with_spatial += 1

        score = min(1.0, lines_with_spatial / max(len(action_lines), 1) * 3)

        return {
            "score": score,
            "has_clear_geography": score > 0.5
        }

    def _analyze_emotional_context(self, actions: List[ActionLine]) -> Dict[str, Any]:
        """Analyze emotional context in action."""
        emotional_actions = [a for a in actions if a.emotional_context]

        return {
            "present": len(emotional_actions) > 0,
            "moment_count": len(emotional_actions),
            "percentage": (len(emotional_actions) / max(len(actions), 1)) * 100
        }

    def _check_camera_directions(self, action_lines: List[Tuple[int, str]]) -> Dict[str, Any]:
        """Check for camera directions in action."""
        found_directions = []

        for line_num, text in action_lines:
            text_upper = text.upper()
            for direction in self.camera_directions:
                if direction in text_upper:
                    found_directions.append((line_num, direction))
                    break

        return {
            "count": len(found_directions),
            "examples": found_directions[:3]
        }

    def _get_problem_lines(self, actions: List[ActionLine]) -> List[Dict]:
        """Get most problematic action lines."""
        problems = []

        for action in actions:
            score = 0
            issues = []

            if action.has_unfilmables:
                score += 3
                issues.append("unfilmable")
            if action.tense_issues:
                score += 2
                issues.append("tense")
            if action.voice_issues:
                score += 2
                issues.append("passive")
            if not action.shows_not_tells:
                score += 1
                issues.append("telling")
            if action.visual_clarity < 0.3:
                score += 1
                issues.append("unclear")

            if score > 0:
                problems.append({
                    "line": action.line_number,
                    "text": action.text[:50],
                    "issues": issues,
                    "severity": score
                })

        # Sort by severity and return top 10
        problems.sort(key=lambda x: x["severity"], reverse=True)
        return problems[:10]

    def _check_action_rules(self, show_tell: Dict, grammar: Dict, visual: Dict,
                           unfilmable: Dict, paragraphs: Dict,
                           intros: List[CharacterIntroduction]) -> List[Dict]:
        """Check action against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "ACT.R001":
                # Show don't tell
                if show_tell["show_ratio"] < 0.7:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Only {show_tell['show_ratio']*100:.0f}% showing",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ACT.R002":
                # Present tense active voice
                if grammar["present_tense_percentage"] < 80:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{grammar['tense_issues']} tense issues found",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ACT.R003":
                # Concise and clear
                if visual["clarity_score"] < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Low visual clarity in action",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ACT.R006":
                # Avoid unfilmables
                if unfilmable["count"] > 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{unfilmable['count']} unfilmable elements",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ACT.R007":
                # Character introduction
                poor_intros = sum(1 for i in intros if i.description_quality < 0.5)
                if poor_intros > len(intros) * 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Poor character introductions",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ACT.R008":
                # Action paragraphs short
                if paragraphs["overlong_count"] > 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{paragraphs['overlong_count']} overlong paragraphs",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_action_score(self, actions: List[ActionLine], violations: List,
                               show_tell: Dict, grammar: Dict, visual: Dict) -> float:
        """Calculate overall action score."""
        score = 100.0

        # Deduct for violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 15
            elif violation["severity"] == "high":
                score -= 10
            elif violation["severity"] == "medium":
                score -= 5
            elif violation["severity"] == "low":
                score -= 3

        # Bonus for excellence
        if show_tell["show_ratio"] > 0.9:
            score += 5
        if grammar["present_tense_percentage"] > 95:
            score += 5
        if visual["clarity_score"] > 0.8:
            score += 5

        return max(0.0, min(100.0, score))

    def _generate_diagnosis(self, score: float, actions: List[ActionLine],
                          violations: List) -> str:
        """Generate diagnosis summary."""
        if score >= 85:
            level = "EXCELLENT"
            summary = "Highly visual and cinematic action"
        elif score >= 70:
            level = "GOOD"
            summary = "Generally strong action with minor issues"
        elif score >= 55:
            level = "NEEDS WORK"
            summary = "Action issues affecting readability"
        else:
            level = "POOR"
            summary = "Major action problems throughout"

        diagnosis = f"ACTION {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if any(a.has_unfilmables for a in actions):
            issues.append("unfilmables")
        if any(a.tense_issues for a in actions):
            issues.append("tense problems")
        if any(not a.shows_not_tells for a in actions):
            issues.append("telling not showing")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues[:3])}"

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 actions: List[ActionLine], show_tell: Dict,
                                 grammar: Dict) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:  # Top 3 violations
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if grammar["tense_issues"] > 10:
            recommendations.append("Review all action and convert to present tense")

        if show_tell["telling_count"] > 10:
            recommendations.append("Convert internal states to observable actions")

        weak_verbs = sum(1 for a in actions if a.verb_strength < 0.3)
        if weak_verbs > len(actions) * 0.3:
            recommendations.append("Replace weak verbs with vivid, specific verbs")

        # General excellence recommendations
        if score < 55:
            recommendations.append("Study action writing in produced screenplays")

        return recommendations[:5]  # Return top 5