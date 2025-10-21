"""
Script Doctor Formatmon - Screenplay Formatting and Industry Standards Specialist
A Script Doctor™ in Digimon form specializing in script formatting and professional presentation.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class FormattingIssue:
    """A formatting issue found in the screenplay."""
    issue_type: str
    severity: str
    line_number: int
    line_text: str
    description: str
    fix_suggestion: str


@dataclass
class PageAnalysis:
    """Analysis of a screenplay page."""
    page_number: int
    line_count: int
    dialogue_percentage: float
    action_percentage: float
    white_space_percentage: float
    has_scene_heading: bool
    formatting_score: float


class DrFormatting:
    """
    Script Doctor Formatmon - The Screenplay Formatting and Industry Standards Specialist

    A Script Doctor™ in Digimon form, specializing in screenplay formatting,
    industry standards, and professional presentation.

    Identity: Script Doctor first, Digimon formatting specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Formatmon with rules and configuration."""
        self.name = "Script Doctor Formatmon"
        self.digimon_name = "Formatmon"
        self.title = "Script Doctor - Screenplay Formatting and Industry Standards Specialist"
        self.specialty = "Script formatting, industry standards, professional presentation, readability"
        self.identity = "I am Script Doctor Formatmon, a professional Script Doctor™ specializing in formatting"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "formatting_rules.yaml"

        self.rules = self._load_rules()

        # Formatting patterns
        self.scene_heading_pattern = r'^(INT\.|EXT\.|INT\./EXT\.|I/E\.)\s+[A-Z].*\s+-\s+(DAY|NIGHT|DAWN|DUSK|CONTINUOUS|LATER|MOMENTS LATER)'
        self.character_name_pattern = r'^[A-Z][A-Z\s]+(\([A-Z\.\s]+\))?$'
        self.parenthetical_pattern = r'^\([^)]+\)$'
        self.transition_pattern = r'^(FADE IN:|FADE OUT\.|FADE TO:|CUT TO:|DISSOLVE TO:|MATCH CUT TO:|SMASH CUT TO:|IRIS IN:|IRIS OUT:)$'

        # Camera direction patterns to avoid
        self.camera_directions = [
            'ANGLE ON', 'CLOSE ON', 'PAN TO', 'ZOOM IN', 'ZOOM OUT',
            'TRACK', 'DOLLY', 'CRANE', 'POV', 'INSERT', 'ECU', 'CU',
            'WIDE SHOT', 'MEDIUM SHOT', 'CLOSE UP', 'EXTREME CLOSE UP'
        ]

        # We see/hear patterns
        self.we_see_pattern = r'\b(we see|we hear|we watch|we notice)\b'

        # Past tense patterns
        self.past_tense_words = [
            'was', 'were', 'had', 'did', 'went', 'came', 'saw', 'made',
            'took', 'gave', 'found', 'told', 'asked', 'worked', 'called',
            'tried', 'became', 'left', 'felt', 'brought', 'began', 'kept'
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze screenplay formatting and industry standards compliance.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete formatting diagnostic report
        """
        lines = screenplay_text.split('\n')

        # Analyze structure
        structure_analysis = self._analyze_structure(lines)

        # Check scene headings
        scene_heading_issues = self._check_scene_headings(lines)

        # Check character formatting
        character_issues = self._check_character_formatting(lines)

        # Check dialogue formatting
        dialogue_issues = self._check_dialogue_formatting(lines)

        # Check action lines
        action_issues = self._check_action_lines(lines)

        # Check transitions
        transition_issues = self._check_transitions(lines)

        # Check camera directions
        camera_issues = self._check_camera_directions(lines)

        # Check tense usage
        tense_issues = self._check_tense(lines)

        # Check "we see/hear" usage
        we_see_issues = self._check_we_see_hear(lines)

        # Check parentheticals
        parenthetical_analysis = self._analyze_parentheticals(lines)

        # Analyze white space
        white_space_analysis = self._analyze_white_space(lines)

        # Estimate page count
        page_analysis = self._analyze_pages(lines)

        # Check for typos and grammar
        typo_analysis = self._check_typos_grammar(screenplay_text)

        # Compile all issues
        all_issues = (scene_heading_issues + character_issues + dialogue_issues +
                     action_issues + transition_issues + camera_issues +
                     tense_issues + we_see_issues)

        # Check against rules
        rule_violations = self._check_formatting_rules(
            all_issues, structure_analysis, page_analysis,
            parenthetical_analysis, white_space_analysis
        )

        # Calculate score
        score = self._calculate_formatting_score(
            all_issues, rule_violations, structure_analysis
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, all_issues, rule_violations
        )

        # Get top issues
        top_issues = self._get_top_issues(all_issues)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "total_lines": len(lines),
            "estimated_pages": page_analysis["estimated_pages"],
            "page_count_appropriate": page_analysis["appropriate_length"],
            "total_issues": len(all_issues),
            "critical_issues": sum(1 for i in all_issues if i.severity == "critical"),
            "high_issues": sum(1 for i in all_issues if i.severity == "high"),
            "medium_issues": sum(1 for i in all_issues if i.severity == "medium"),
            "low_issues": sum(1 for i in all_issues if i.severity == "low"),
            "scene_heading_issues": len(scene_heading_issues),
            "character_formatting_issues": len(character_issues),
            "dialogue_formatting_issues": len(dialogue_issues),
            "action_line_issues": len(action_issues),
            "transition_issues": len(transition_issues),
            "camera_direction_issues": len(camera_issues),
            "tense_issues": len(tense_issues),
            "we_see_hear_issues": len(we_see_issues),
            "parenthetical_overuse": parenthetical_analysis["overused"],
            "parenthetical_count": parenthetical_analysis["total_count"],
            "white_space_score": white_space_analysis["score"],
            "average_action_paragraph_length": white_space_analysis["avg_action_length"],
            "typos_found": typo_analysis["typo_count"],
            "scene_count": structure_analysis["scene_count"],
            "dialogue_percentage": structure_analysis["dialogue_percentage"],
            "action_percentage": structure_analysis["action_percentage"],
            "properly_formatted_percentage": structure_analysis["proper_format_percentage"],
            "top_issues": top_issues,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, all_issues, rule_violations, structure_analysis
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _analyze_structure(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze overall screenplay structure."""
        scene_count = 0
        dialogue_lines = 0
        action_lines = 0
        properly_formatted = 0
        total_content_lines = 0

        in_dialogue = False
        last_was_character = False

        for line in lines:
            line_stripped = line.strip()

            if not line_stripped:
                continue

            total_content_lines += 1

            # Check scene headings
            if re.match(self.scene_heading_pattern, line_stripped):
                scene_count += 1
                properly_formatted += 1
                action_lines += 1
                in_dialogue = False

            # Check character names
            elif re.match(self.character_name_pattern, line_stripped) and len(line_stripped.split()) <= 3:
                last_was_character = True
                in_dialogue = True
                properly_formatted += 1

            # Check dialogue
            elif in_dialogue and not line_stripped.isupper():
                dialogue_lines += 1
                if last_was_character or line_stripped.startswith('('):
                    properly_formatted += 1
                last_was_character = False

            # Check transitions
            elif re.match(self.transition_pattern, line_stripped):
                properly_formatted += 1
                in_dialogue = False

            # Action lines
            else:
                action_lines += 1
                in_dialogue = False
                last_was_character = False

        return {
            "scene_count": scene_count,
            "dialogue_lines": dialogue_lines,
            "action_lines": action_lines,
            "dialogue_percentage": (dialogue_lines / max(total_content_lines, 1)) * 100,
            "action_percentage": (action_lines / max(total_content_lines, 1)) * 100,
            "proper_format_percentage": (properly_formatted / max(total_content_lines, 1)) * 100
        }

    def _check_scene_headings(self, lines: List[str]) -> List[FormattingIssue]:
        """Check scene heading formatting."""
        issues = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Skip empty lines
            if not line_stripped:
                continue

            # Check if it looks like a scene heading
            if any(line_stripped.startswith(prefix) for prefix in ['INT.', 'EXT.', 'INT/', 'EXT/']):
                # Check proper format
                if not re.match(self.scene_heading_pattern, line_stripped):
                    issues.append(FormattingIssue(
                        issue_type="scene_heading",
                        severity="critical",
                        line_number=i + 1,
                        line_text=line_stripped[:50],
                        description="Incorrect scene heading format",
                        fix_suggestion="Use: INT./EXT. LOCATION - TIME OF DAY"
                    ))

        return issues

    def _check_character_formatting(self, lines: List[str]) -> List[FormattingIssue]:
        """Check character name formatting."""
        issues = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if not line_stripped:
                continue

            # Check if it's a character name (before dialogue)
            if (i < len(lines) - 1 and
                line_stripped and
                not any(line_stripped.startswith(p) for p in ['INT.', 'EXT.', 'FADE', 'CUT'])):

                next_line = lines[i + 1].strip() if i < len(lines) - 1 else ""

                # If next line looks like dialogue
                if next_line and not next_line.isupper() and not next_line.startswith('('):
                    # This should be a character name
                    if not line_stripped.isupper():
                        issues.append(FormattingIssue(
                            issue_type="character_name",
                            severity="critical",
                            line_number=i + 1,
                            line_text=line_stripped,
                            description="Character name not in ALL CAPS",
                            fix_suggestion="Character names must be ALL CAPS"
                        ))

        return issues

    def _check_dialogue_formatting(self, lines: List[str]) -> List[FormattingIssue]:
        """Check dialogue formatting."""
        issues = []

        in_dialogue = False
        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Character name starts dialogue
            if re.match(self.character_name_pattern, line_stripped) and len(line_stripped.split()) <= 3:
                in_dialogue = True

            # Empty line might end dialogue
            elif not line_stripped:
                in_dialogue = False

            # Scene heading ends dialogue
            elif any(line_stripped.startswith(p) for p in ['INT.', 'EXT.']):
                in_dialogue = False

        return issues

    def _check_action_lines(self, lines: List[str]) -> List[FormattingIssue]:
        """Check action line formatting."""
        issues = []

        current_paragraph = []
        in_action = False

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Skip if in dialogue or scene heading
            if (re.match(self.scene_heading_pattern, line_stripped) or
                re.match(self.character_name_pattern, line_stripped)):
                # Check accumulated paragraph
                if current_paragraph and len(current_paragraph) > 4:
                    issues.append(FormattingIssue(
                        issue_type="action_lines",
                        severity="high",
                        line_number=i - len(current_paragraph),
                        line_text=current_paragraph[0][:50],
                        description="Action paragraph too long (>4 lines)",
                        fix_suggestion="Break into 3-4 line paragraphs"
                    ))
                current_paragraph = []
                in_action = False
                continue

            # Empty line ends paragraph
            if not line_stripped:
                if current_paragraph and len(current_paragraph) > 4:
                    issues.append(FormattingIssue(
                        issue_type="action_lines",
                        severity="high",
                        line_number=i - len(current_paragraph),
                        line_text=current_paragraph[0][:50],
                        description="Action paragraph too long (>4 lines)",
                        fix_suggestion="Break into 3-4 line paragraphs"
                    ))
                current_paragraph = []
                continue

            # Action line
            if not line_stripped.isupper() and not line_stripped.startswith('('):
                current_paragraph.append(line_stripped)

        return issues

    def _check_transitions(self, lines: List[str]) -> List[FormattingIssue]:
        """Check transition usage."""
        issues = []
        transition_count = 0

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if re.match(self.transition_pattern, line_stripped):
                transition_count += 1

                # Check for overuse of CUT TO:
                if "CUT TO:" in line_stripped:
                    # CUT TO is often unnecessary
                    if transition_count > len(lines) / 100:  # More than 1 per 100 lines
                        issues.append(FormattingIssue(
                            issue_type="transitions",
                            severity="medium",
                            line_number=i + 1,
                            line_text=line_stripped,
                            description="Possible overuse of CUT TO:",
                            fix_suggestion="Use CUT TO: sparingly, only for emphasis"
                        ))

        return issues

    def _check_camera_directions(self, lines: List[str]) -> List[FormattingIssue]:
        """Check for camera directions."""
        issues = []

        for i, line in enumerate(lines):
            line_upper = line.strip().upper()

            for direction in self.camera_directions:
                if direction in line_upper:
                    issues.append(FormattingIssue(
                        issue_type="camera_directions",
                        severity="high",
                        line_number=i + 1,
                        line_text=line.strip()[:50],
                        description=f"Camera direction '{direction}' found",
                        fix_suggestion="Avoid camera directions in spec scripts"
                    ))
                    break

        return issues

    def _check_tense(self, lines: List[str]) -> List[FormattingIssue]:
        """Check for past tense in action lines."""
        issues = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Skip dialogue, character names, scene headings
            if (not line_stripped or
                line_stripped.isupper() or
                line_stripped.startswith('(') or
                re.match(self.scene_heading_pattern, line_stripped)):
                continue

            # Check for past tense in action lines
            words = line_stripped.lower().split()
            for word in self.past_tense_words:
                if word in words:
                    issues.append(FormattingIssue(
                        issue_type="tense",
                        severity="critical",
                        line_number=i + 1,
                        line_text=line_stripped[:50],
                        description=f"Past tense '{word}' in action line",
                        fix_suggestion="Use present tense in all action lines"
                    ))
                    break

        return issues[:20]  # Limit to 20 to avoid spam

    def _check_we_see_hear(self, lines: List[str]) -> List[FormattingIssue]:
        """Check for 'we see/we hear' usage."""
        issues = []

        for i, line in enumerate(lines):
            line_lower = line.strip().lower()

            if re.search(self.we_see_pattern, line_lower):
                issues.append(FormattingIssue(
                    issue_type="we_see_hear",
                    severity="medium",
                    line_number=i + 1,
                    line_text=line.strip()[:50],
                    description="'We see/we hear' phrase found",
                    fix_suggestion="Show directly without 'we see/we hear'"
                ))

        return issues

    def _analyze_parentheticals(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze parenthetical usage."""
        parenthetical_count = 0
        dialogue_count = 0

        in_dialogue = False
        for line in lines:
            line_stripped = line.strip()

            if re.match(self.character_name_pattern, line_stripped):
                in_dialogue = True
                dialogue_count += 1
            elif not line_stripped:
                in_dialogue = False
            elif in_dialogue and re.match(self.parenthetical_pattern, line_stripped):
                parenthetical_count += 1

        # More than 30% of dialogue with parentheticals is overuse
        overused = (parenthetical_count / max(dialogue_count, 1)) > 0.3

        return {
            "total_count": parenthetical_count,
            "dialogue_count": dialogue_count,
            "percentage": (parenthetical_count / max(dialogue_count, 1)) * 100,
            "overused": overused
        }

    def _analyze_white_space(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze white space and readability."""
        empty_lines = sum(1 for line in lines if not line.strip())
        total_lines = len(lines)

        white_space_percentage = (empty_lines / max(total_lines, 1)) * 100

        # Calculate average action paragraph length
        paragraph_lengths = []
        current_length = 0

        for line in lines:
            if line.strip() and not line.strip().isupper():
                current_length += 1
            elif current_length > 0:
                paragraph_lengths.append(current_length)
                current_length = 0

        avg_action_length = sum(paragraph_lengths) / max(len(paragraph_lengths), 1) if paragraph_lengths else 0

        # Good white space is 20-35%
        if 20 <= white_space_percentage <= 35:
            score = 1.0
        elif 15 <= white_space_percentage <= 40:
            score = 0.7
        else:
            score = 0.4

        return {
            "white_space_percentage": white_space_percentage,
            "score": score,
            "avg_action_length": avg_action_length
        }

    def _analyze_pages(self, lines: List[str]) -> Dict[str, Any]:
        """Estimate page count and check appropriateness."""
        # Rough estimate: 55 lines per page
        estimated_pages = len(lines) / 55

        # Feature film should be 90-120 pages
        appropriate_length = 90 <= estimated_pages <= 120

        return {
            "estimated_pages": int(estimated_pages),
            "appropriate_length": appropriate_length,
            "recommendation": self._get_length_recommendation(estimated_pages)
        }

    def _get_length_recommendation(self, pages: float) -> str:
        """Get recommendation based on page count."""
        if pages < 80:
            return "Too short for feature - expand story or consider short film"
        elif pages < 90:
            return "Slightly short - consider expanding key scenes"
        elif pages <= 120:
            return "Good length for feature film"
        elif pages <= 130:
            return "Slightly long - consider trimming"
        else:
            return "Too long - needs significant cutting"

    def _check_typos_grammar(self, screenplay: str) -> Dict[str, Any]:
        """Basic typo and grammar check."""
        # Very basic check for common issues
        typo_count = 0

        # Check for double spaces
        if "  " in screenplay:
            typo_count += screenplay.count("  ")

        # Check for common typos
        common_typos = [
            ("teh", "the"),
            ("adn", "and"),
            ("taht", "that"),
            ("recieve", "receive"),
            ("occured", "occurred")
        ]

        screenplay_lower = screenplay.lower()
        for typo, correct in common_typos:
            if typo in screenplay_lower:
                typo_count += screenplay_lower.count(typo)

        return {
            "typo_count": min(typo_count, 20),  # Cap at 20 to avoid spam
            "has_issues": typo_count > 0
        }

    def _get_top_issues(self, issues: List[FormattingIssue]) -> List[Dict]:
        """Get top formatting issues."""
        top_issues = []

        # Sort by severity
        sorted_issues = sorted(issues, key=lambda x: {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3
        }.get(x.severity, 4))

        for issue in sorted_issues[:10]:  # Top 10
            top_issues.append({
                "type": issue.issue_type,
                "severity": issue.severity,
                "line": issue.line_number,
                "description": issue.description,
                "fix": issue.fix_suggestion
            })

        return top_issues

    def _check_formatting_rules(self, issues: List[FormattingIssue],
                               structure: Dict, pages: Dict,
                               parentheticals: Dict, white_space: Dict) -> List[Dict]:
        """Check formatting against rules."""
        violations = []

        # Count issues by type
        issue_counts = defaultdict(int)
        for issue in issues:
            issue_counts[issue.issue_type] += 1

        for rule in self.rules.get("rules", []):
            if rule["id"] == "FMT.R001":
                # Scene heading format
                if issue_counts["scene_heading"] > 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{issue_counts['scene_heading']} scene heading issues",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R002":
                # Character name format
                if issue_counts["character_name"] > 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{issue_counts['character_name']} character name issues",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R003":
                # Action line length
                if issue_counts["action_lines"] > 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{issue_counts['action_lines']} action paragraphs too long",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R005":
                # Parentheticals usage
                if parentheticals["overused"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Parentheticals in {parentheticals['percentage']:.0f}% of dialogue",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R006":
                # Page count range
                if not pages["appropriate_length"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{pages['estimated_pages']} pages - {pages['recommendation']}",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R008":
                # Camera directions
                if issue_counts["camera_directions"] > 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{issue_counts['camera_directions']} camera directions found",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R009":
                # Present tense
                if issue_counts["tense"] > 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{issue_counts['tense']} past tense uses in action",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R010":
                # We see/hear
                if issue_counts["we_see_hear"] > 3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{issue_counts['we_see_hear']} uses of 'we see/we hear'",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FMT.R014":
                # White space balance
                if white_space["score"] < 0.7:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"White space: {white_space['white_space_percentage']:.0f}%",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_formatting_score(self, issues: List[FormattingIssue],
                                   violations: List, structure: Dict) -> float:
        """Calculate overall formatting score."""
        score = 100.0

        # Deduct for issues
        for issue in issues:
            if issue.severity == "critical":
                score -= 2
            elif issue.severity == "high":
                score -= 1
            elif issue.severity == "medium":
                score -= 0.5
            elif issue.severity == "low":
                score -= 0.25

        # Additional deductions for rule violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 5
            elif violation["severity"] == "high":
                score -= 3
            elif violation["severity"] == "medium":
                score -= 2
            elif violation["severity"] == "low":
                score -= 1

        # Bonus for good structure
        if structure["proper_format_percentage"] > 80:
            score += 5

        return max(0.0, min(100.0, score))

    def _generate_diagnosis(self, score: float, issues: List[FormattingIssue],
                          violations: List) -> str:
        """Generate diagnosis summary."""
        if score >= 90:
            level = "EXCELLENT"
            summary = "Professional formatting throughout"
        elif score >= 75:
            level = "GOOD"
            summary = "Generally well formatted with minor issues"
        elif score >= 60:
            level = "NEEDS WORK"
            summary = "Multiple formatting issues affecting readability"
        else:
            level = "POOR"
            summary = "Major formatting problems throughout"

        diagnosis = f"FORMATTING {level} ({score:.1f}/100): {summary}"

        # Add top issue types
        issue_types = set(i.issue_type for i in issues[:10])
        if issue_types:
            diagnosis += f". Key issues: {', '.join(list(issue_types)[:3])}"

        return diagnosis

    def _generate_recommendations(self, score: float, issues: List[FormattingIssue],
                                 violations: List, structure: Dict) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:  # Top 3 violations
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations based on issues
        issue_counts = defaultdict(int)
        for issue in issues:
            issue_counts[issue.issue_type] += 1

        if issue_counts["tense"] > 5:
            recommendations.append("Review all action lines and convert to present tense")

        if issue_counts["camera_directions"] > 3:
            recommendations.append("Remove camera directions - let director decide shots")

        if issue_counts["action_lines"] > 5:
            recommendations.append("Break up long action paragraphs for better readability")

        # General excellence recommendations
        if score < 60:
            recommendations.append("Consider using professional screenplay software")
            recommendations.append("Study professional screenplay format guides")

        return recommendations[:5]  # Return top 5