"""
Script Doctor Alphamon - First Impressions Specialist
A Script Doctor™ in Digimon form specializing in opening hooks and first 10 pages.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class OpeningElement:
    """Key element in screenplay opening."""
    name: str
    found: bool
    page_found: int
    quality_score: float  # 0-1
    notes: str


@dataclass
class PageAnalysis:
    """Analysis of a specific page."""
    page_number: int
    has_conflict: bool
    has_character: bool
    has_action: bool
    has_dialogue: bool
    hook_strength: float
    word_count: int


class DrOpening:
    """
    Script Doctor Alphamon - The First Impressions Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing screenplay
    openings, first impressions, hooks, and the critical first 10 pages.

    Identity: Script Doctor first, Digimon opening specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Alphamon with rules and configuration."""
        self.name = "Script Doctor Alphamon"
        self.digimon_name = "Alphamon"
        self.title = "Script Doctor - First Impressions Specialist"
        self.specialty = "Opening hooks, first 10 pages, initial engagement"
        self.identity = "I am Script Doctor Alphamon, a professional Script Doctor™ specializing in powerful openings"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "opening_rules.yaml"

        self.rules = self._load_rules()

        # Cliché openings to detect
        self.cliche_patterns = [
            r"alarm\s+clock",
            r"wak(es?|ing)\s+up",
            r"it\s+was\s+all\s+a\s+dream",
            r"looking\s+in\s+(the\s+)?mirror",
            r"weather\s+report",
            r"driving\s+to\s+work",
            r"morning\s+routine",
            r"breakfast\s+scene"
        ]

        # Hook patterns
        self.hook_patterns = {
            "action": [r"explod", r"crash", r"fight", r"run", r"chase", r"shoot"],
            "mystery": [r"dead", r"missing", r"strange", r"mysterious", r"unknown"],
            "conflict": [r"argument", r"confrontation", r"threat", r"danger", r"attack"],
            "surprise": [r"suddenly", r"without warning", r"unexpected", r"shocked"]
        }

    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file."""
        try:
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules from {self.rules_path}: {e}")
            return {"rules": []}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Perform complete opening analysis of screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete opening diagnostic report
        """
        lines = screenplay_text.split('\n')

        # Extract first 10 pages (approximately 550 lines)
        first_ten_pages_lines = lines[:550]
        first_ten_pages = '\n'.join(first_ten_pages_lines)

        # Analyze key elements
        opening_elements = self._analyze_opening_elements(first_ten_pages)
        page_by_page = self._analyze_page_by_page(first_ten_pages_lines)

        # Check specific metrics
        hook_strength = self._evaluate_hook_strength(lines[:55])  # First page
        cliche_score = self._check_for_cliches(first_ten_pages)
        protagonist_intro = self._find_protagonist_introduction(first_ten_pages)
        genre_clarity = self._assess_genre_clarity(first_ten_pages)

        # Check against rules
        rule_violations = self._check_opening_rules(
            first_ten_pages, opening_elements, page_by_page,
            hook_strength, cliche_score, protagonist_intro
        )

        # Calculate score
        score = self._calculate_opening_score(
            opening_elements, rule_violations, hook_strength,
            cliche_score, protagonist_intro
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, opening_elements, hook_strength,
            cliche_score, protagonist_intro, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "opening_elements": self._elements_to_dict(opening_elements),
            "hook_strength": hook_strength,  # Main field for hook strength
            "first_page_impact": hook_strength,  # Alias for compatibility
            "opening_type": self._determine_opening_type(screenplay_text),
            "cliche_score": cliche_score,
            "cliches_found": self._get_cliches_list(screenplay_text),
            "protagonist_introduction": protagonist_intro,
            "protagonist_intro_page": protagonist_intro.get("page_introduced", "N/A"),
            "protagonist_intro_quality": protagonist_intro.get("quality", "N/A"),
            "genre_clarity": genre_clarity,
            "genre_signals": self._detect_genre_signals(screenplay_text),
            "genre_clarity_score": genre_clarity * 100 if isinstance(genre_clarity, (int, float)) else 0,
            "world_clarity_score": self._get_world_clarity_score(opening_elements),
            "time_period_established": self._is_time_established(opening_elements),
            "location_established": self._is_location_established(opening_elements),
            "tone_established": self._is_tone_established(opening_elements),
            "premise_promised": self._is_premise_promised(opening_elements),
            "central_conflict_hinted": self._is_conflict_hinted(opening_elements),
            "stakes_indicated": self._are_stakes_indicated(opening_elements),
            "page_analysis": self._pages_to_dict(page_by_page),
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, opening_elements, hook_strength
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _analyze_opening_elements(self, first_ten_pages: str) -> Dict[str, OpeningElement]:
        """Analyze key opening elements."""
        elements = {}
        lines = first_ten_pages.split('\n')

        # Opening image
        opening_image = OpeningElement(
            name="Opening Image",
            found=False,
            page_found=0,
            quality_score=0,
            notes=""
        )

        # Look for first visual description
        for i, line in enumerate(lines[:110]):  # First 2 pages
            if any(word in line.upper() for word in ["EXT.", "INT.", "FADE IN"]):
                opening_image.found = True
                opening_image.page_found = i // 55 + 1
                # Check quality based on description length and vividness
                next_lines = '\n'.join(lines[i:i+10])
                if len(next_lines) > 100:
                    opening_image.quality_score = 0.7
                if any(word in next_lines.lower() for word in ["beautiful", "dark", "mysterious", "perfect"]):
                    opening_image.quality_score += 0.2
                opening_image.notes = "Visual opening found"
                break

        elements["opening_image"] = opening_image

        # Character introduction
        character_intro = OpeningElement(
            name="Character Introduction",
            found=False,
            page_found=0,
            quality_score=0,
            notes=""
        )

        # Look for character names in CAPS
        for i, line in enumerate(lines[:275]):  # First 5 pages
            if re.match(r'^[A-Z][A-Z\s]+(\(\d+s?\))?$', line.strip()) and len(line.strip()) > 2:
                character_intro.found = True
                character_intro.page_found = i // 55 + 1
                # Check if character does something interesting
                next_lines = '\n'.join(lines[i:i+20])
                if any(word in next_lines.lower() for word in ["runs", "fights", "discovers", "confronts"]):
                    character_intro.quality_score = 0.8
                else:
                    character_intro.quality_score = 0.5
                character_intro.notes = f"Character introduced on page {character_intro.page_found}"
                break

        elements["character_introduction"] = character_intro

        # World establishment
        world_setup = OpeningElement(
            name="World Establishment",
            found=False,
            page_found=0,
            quality_score=0,
            notes=""
        )

        # Check for setting descriptions
        setting_words = ["city", "town", "house", "office", "street", "year", "future", "past"]
        for i, line in enumerate(lines[:275]):  # First 5 pages
            if any(word in line.lower() for word in setting_words):
                world_setup.found = True
                world_setup.page_found = i // 55 + 1
                world_setup.quality_score = 0.6
                world_setup.notes = "World/setting established"
                break

        elements["world_establishment"] = world_setup

        # Inciting incident hint
        incident_hint = OpeningElement(
            name="Conflict/Mystery Hint",
            found=False,
            page_found=0,
            quality_score=0,
            notes=""
        )

        conflict_words = ["problem", "wrong", "dead", "missing", "strange", "help", "danger"]
        for i, line in enumerate(lines[:550]):  # First 10 pages
            if any(word in line.lower() for word in conflict_words):
                incident_hint.found = True
                incident_hint.page_found = i // 55 + 1
                incident_hint.quality_score = 0.7
                incident_hint.notes = f"Conflict hinted on page {incident_hint.page_found}"
                break

        elements["conflict_hint"] = incident_hint

        return elements

    def _analyze_page_by_page(self, lines: List[str]) -> List[PageAnalysis]:
        """Analyze each page of the opening."""
        pages = []

        for page_num in range(1, 11):  # First 10 pages
            start_line = (page_num - 1) * 55
            end_line = min(page_num * 55, len(lines))
            page_lines = lines[start_line:end_line]
            page_text = '\n'.join(page_lines)

            page_analysis = PageAnalysis(
                page_number=page_num,
                has_conflict=self._detect_conflict(page_text),
                has_character=self._detect_character(page_text),
                has_action=self._detect_action(page_text),
                has_dialogue=self._detect_dialogue(page_text),
                hook_strength=self._evaluate_hook_strength(page_lines),
                word_count=len(page_text.split())
            )

            pages.append(page_analysis)

        return pages

    def _evaluate_hook_strength(self, lines: List[str]) -> float:
        """Evaluate the hook strength of given lines."""
        text = '\n'.join(lines).lower()
        hook_score = 0.0

        # Check for different hook types
        for hook_type, patterns in self.hook_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    hook_score += 0.2

        # Check for immediate conflict
        if any(word in text for word in ["no", "don't", "stop", "help", "!"]):
            hook_score += 0.2

        # Check for intriguing opening line
        first_line = lines[0] if lines else ""
        if len(first_line) > 20 and not first_line.upper().startswith("FADE"):
            hook_score += 0.1

        return min(1.0, hook_score)

    def _check_for_cliches(self, text: str) -> float:
        """Check for cliché openings (lower is better)."""
        cliche_count = 0
        text_lower = text.lower()

        for pattern in self.cliche_patterns:
            if re.search(pattern, text_lower):
                cliche_count += 1

        # Return inverse score (0 = many clichés, 1 = no clichés)
        if cliche_count == 0:
            return 1.0
        elif cliche_count == 1:
            return 0.7
        elif cliche_count == 2:
            return 0.4
        else:
            return 0.2

    def _find_protagonist_introduction(self, text: str) -> Dict[str, Any]:
        """Find and analyze protagonist introduction."""
        lines = text.split('\n')

        for i, line in enumerate(lines):
            # Look for character introduction pattern
            if re.match(r'^[A-Z][A-Z\s]+(\(\d+s?\))?$', line.strip()) and len(line.strip()) > 2:
                page = i // 55 + 1

                # Check how they're introduced
                intro_quality = "basic"
                next_lines = '\n'.join(lines[i:i+10]).lower()

                if any(word in next_lines for word in ["saves", "helps", "rescues"]):
                    intro_quality = "heroic"
                elif any(word in next_lines for word in ["struggles", "fails", "tries"]):
                    intro_quality = "sympathetic"
                elif any(word in next_lines for word in ["mysterious", "dangerous", "powerful"]):
                    intro_quality = "intriguing"

                return {
                    "found": True,
                    "page": page,
                    "quality": intro_quality,
                    "character_name": line.strip().split('(')[0].strip()
                }

        return {
            "found": False,
            "page": 0,
            "quality": "missing",
            "character_name": None
        }

    def _assess_genre_clarity(self, text: str) -> float:
        """Assess how clearly genre is established."""
        genre_markers = {
            "thriller": ["gun", "chase", "danger", "threat", "kill"],
            "comedy": ["laugh", "funny", "joke", "ridiculous", "awkward"],
            "horror": ["blood", "scream", "dark", "creepy", "dead"],
            "romance": ["love", "kiss", "beautiful", "heart", "romantic"],
            "scifi": ["space", "alien", "future", "technology", "robot"],
            "action": ["explosion", "fight", "chase", "weapon", "battle"]
        }

        text_lower = text.lower()
        genre_scores = {}

        for genre, markers in genre_markers.items():
            score = sum(1 for marker in markers if marker in text_lower)
            if score > 0:
                genre_scores[genre] = score

        # Clear genre if one dominates
        if genre_scores:
            max_score = max(genre_scores.values())
            if max_score >= 3:
                return 1.0
            elif max_score >= 2:
                return 0.7
            else:
                return 0.4
        return 0.2

    def _detect_conflict(self, text: str) -> bool:
        """Detect if text contains conflict."""
        conflict_indicators = [
            "no", "don't", "can't", "won't", "stop",
            "argue", "fight", "disagree", "oppose",
            "!", "?!"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in conflict_indicators)

    def _detect_character(self, text: str) -> bool:
        """Detect if text contains character."""
        return bool(re.search(r'^[A-Z][A-Z\s]+(\(\d+s?\))?$', text, re.MULTILINE))

    def _detect_action(self, text: str) -> bool:
        """Detect if text contains action."""
        action_words = ["runs", "jumps", "fights", "grabs", "throws", "shoots", "drives"]
        text_lower = text.lower()
        return any(word in text_lower for word in action_words)

    def _detect_dialogue(self, text: str) -> bool:
        """Detect if text contains dialogue."""
        # Simple heuristic: indented lines after character names
        lines = text.split('\n')
        for i, line in enumerate(lines[:-1]):
            if re.match(r'^[A-Z][A-Z\s]+(\(\d+s?\))?$', line.strip()):
                if i + 1 < len(lines) and lines[i + 1].startswith(' '):
                    return True
        return False

    def _check_opening_rules(self, text: str, elements: Dict, pages: List,
                            hook_strength: float, cliche_score: float,
                            protagonist: Dict) -> List[Dict[str, Any]]:
        """Check against opening rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "OPEN.R001":
                # Page one hook
                if hook_strength < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Hook strength only {hook_strength*100:.0f}%",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "OPEN.R002":
                # Opening image
                if not elements["opening_image"].found or elements["opening_image"].quality_score < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": rule["fail_msg"],
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "OPEN.R003":
                # Character introduction
                if not protagonist["found"] or protagonist["page"] > 10:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Protagonist introduced on page {protagonist['page']}" if protagonist["found"] else "No clear protagonist",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "OPEN.R008":
                # Clichés
                if cliche_score < 0.7:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Cliché opening detected",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_opening_score(self, elements: Dict, violations: List,
                                hook_strength: float, cliche_score: float,
                                protagonist: Dict) -> float:
        """Calculate overall opening score."""
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

        # Factor in hook strength (very important)
        score = score * 0.7 + (hook_strength * 100) * 0.3

        # Factor in cliché avoidance
        if cliche_score < 0.5:
            score -= 10

        # Protagonist introduction
        if not protagonist["found"]:
            score -= 15
        elif protagonist["page"] > 5:
            score -= 5

        return max(0, min(100, round(score, 1)))

    def _elements_to_dict(self, elements: Dict[str, OpeningElement]) -> Dict:
        """Convert elements to dictionary."""
        result = {}
        for key, element in elements.items():
            result[key] = {
                "name": element.name,
                "found": element.found,
                "page_found": element.page_found,
                "quality_score": element.quality_score,
                "notes": element.notes
            }
        return result

    def _pages_to_dict(self, pages: List[PageAnalysis]) -> List[Dict]:
        """Convert page analyses to dictionary."""
        return [
            {
                "page": p.page_number,
                "has_conflict": p.has_conflict,
                "has_character": p.has_character,
                "has_action": p.has_action,
                "has_dialogue": p.has_dialogue,
                "hook_strength": p.hook_strength,
                "word_count": p.word_count
            }
            for p in pages
        ]

    def _generate_diagnosis(self, score: float, elements: Dict,
                          hook_strength: float, cliche_score: float,
                          protagonist: Dict, violations: List) -> str:
        """Generate narrative diagnosis."""
        diagnosis = f"Opening Analysis Score: {score}/100\n\n"

        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent opening! You grab attention immediately and sustain interest. "
        elif score >= 70:
            diagnosis += "Good opening with solid hooks, but room for improvement. "
        elif score >= 50:
            diagnosis += "Opening needs work to meet professional standards. "
        else:
            diagnosis += "Major opening issues that will cause readers to stop. "

        # Hook analysis
        if hook_strength < 0.5:
            diagnosis += f"Page one hook is weak ({hook_strength*100:.0f}%). "
        elif hook_strength > 0.8:
            diagnosis += "Strong page one hook! "

        # Protagonist
        if not protagonist["found"]:
            diagnosis += "No clear protagonist introduction. "
        elif protagonist["page"] > 5:
            diagnosis += f"Protagonist introduced too late (page {protagonist['page']}). "

        # Clichés
        if cliche_score < 0.5:
            diagnosis += "Opening uses tired clichés. "

        # Critical issues
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical issues: {', '.join([v['title'] for v in critical])}."

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 elements: Dict, hook_strength: float) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Priority fixes
        for violation in sorted(violations,
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 3:
                break

        # Hook specific
        if hook_strength < 0.5:
            recommendations.append("Start with immediate conflict or intriguing mystery")

        # Character specific
        if not elements["character_introduction"].found:
            recommendations.append("Introduce protagonist with defining action by page 5")

        # General advice
        if score < 70:
            recommendations.append("Study opening pages of produced scripts in your genre")

        return recommendations[:5]

    def _determine_opening_type(self, screenplay: str) -> str:
        """Determine the type of opening."""
        # Get approximately first page (55 lines)
        lines = screenplay.split('\n')[:55]
        first_page = '\n'.join(lines)
        lower = first_page.lower()

        if any(word in lower for word in ["explosion", "chase", "fight", "crash", "fire"]):
            return "action"
        elif any(word in lower for word in ["mystery", "dead", "murder", "strange"]):
            return "mystery"
        elif "dream" in lower or "wakes up" in lower:
            return "dream/wake"
        elif "flashback" in lower or "earlier" in lower:
            return "flashback"
        elif "establishing" in lower:
            return "establishing"
        else:
            return "character"

    def _get_cliches_list(self, screenplay: str) -> List[str]:
        """Get list of clichés found in opening."""
        cliches = []
        # Get first 10 pages (approximately 550 lines)
        lines = screenplay.split('\n')[:550]
        first_ten = '\n'.join(lines)
        lower = first_ten.lower()

        if "alarm clock" in lower or "alarm beeps" in lower:
            cliches.append("Alarm clock wake-up")
        if "it was all a dream" in lower or "wakes up" in lower:
            cliches.append("Dream sequence opening")
        if "once upon a time" in lower:
            cliches.append("Once upon a time")
        if "dark and stormy night" in lower:
            cliches.append("Dark and stormy night")
        if "in the beginning" in lower:
            cliches.append("In the beginning")
        if "looks in the mirror" in lower or "looks in mirror" in lower:
            cliches.append("Character describing self in mirror")

        return cliches

    def _detect_genre_signals(self, screenplay: str) -> str:
        """Detect genre from opening pages."""
        # Get first 10 pages (approximately 550 lines)
        lines = screenplay.split('\n')[:550]
        first_ten = '\n'.join(lines)
        lower = first_ten.lower()

        genre_markers = {
            "action/thriller": ["explosion", "gun", "chase", "fight", "bomb", "terrorist"],
            "horror": ["blood", "scream", "monster", "dark", "creepy", "haunted"],
            "comedy": ["laugh", "joke", "funny", "awkward", "embarrassing"],
            "drama": ["tears", "emotion", "relationship", "family", "loss"],
            "sci-fi": ["space", "alien", "future", "technology", "robot", "year 2"]
        }

        scores = {}
        for genre, markers in genre_markers.items():
            scores[genre] = sum(1 for marker in markers if marker in lower)

        if scores:
            return max(scores, key=scores.get)
        return "unclear"

    def _get_world_clarity_score(self, elements: Dict[str, 'OpeningElement']) -> int:
        """Get world establishment score."""
        if "world_establishment" in elements:
            return int(elements["world_establishment"].quality_score * 100)
        return 0

    def _is_time_established(self, elements: Dict[str, 'OpeningElement']) -> bool:
        """Check if time period is established."""
        if "world_establishment" in elements:
            return elements["world_establishment"].found
        return False

    def _is_location_established(self, elements: Dict[str, 'OpeningElement']) -> bool:
        """Check if location is established."""
        if "world_establishment" in elements:
            return elements["world_establishment"].found
        return False

    def _is_tone_established(self, elements: Dict[str, 'OpeningElement']) -> bool:
        """Check if tone is established."""
        if "voice_and_tone" in elements:
            return elements["voice_and_tone"].found
        return False

    def _is_premise_promised(self, elements: Dict[str, 'OpeningElement']) -> bool:
        """Check if premise is promised."""
        if "promise_of_premise" in elements:
            return elements["promise_of_premise"].found
        return False

    def _is_conflict_hinted(self, elements: Dict[str, 'OpeningElement']) -> bool:
        """Check if central conflict is hinted."""
        if "forward_momentum" in elements:
            return elements["forward_momentum"].quality_score > 0.5
        return False

    def _are_stakes_indicated(self, elements: Dict[str, 'OpeningElement']) -> bool:
        """Check if stakes are indicated."""
        if "stakes_indication" in elements:
            return elements["stakes_indication"].found
        return False