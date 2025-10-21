"""
Dr. Yuki Tanaka - Narrative Architect
Specialist in three-act structure, plot points, and story architecture.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StructuralElement:
    """Represents a structural element in the screenplay."""
    name: str
    expected_page: int
    page_range: Tuple[int, int]  # (min, max) acceptable pages
    found_at: Optional[int] = None
    strength: float = 0.0  # 0-1 scale
    notes: str = ""


class DrStructure:
    """
    Script Doctor Structuremon - The Narrative Architecture Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing screenplay
    structure, ensuring proper three-act format, plot points, and pacing.

    Identity: Script Doctor first, Digimon specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Structuremon with rules and configuration."""
        self.name = "Script Doctor Structuremon"
        self.digimon_name = "Structuremon"
        self.title = "Script Doctor - Narrative Architecture Specialist"
        self.specialty = "Three-act structure, plot points, story architecture"
        self.identity = "I am Script Doctor Structuremon, a professional Script Doctor™ specializing in narrative structure"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "structure_rules.yaml"

        self.rules = self._load_rules()

        # Structural elements to track
        self.elements = {
            "opening_image": StructuralElement("Opening Image", 1, (1, 3)),
            "setup": StructuralElement("Setup/Ordinary World", 5, (1, 10)),
            "inciting_incident": StructuralElement("Inciting Incident", 12, (10, 15)),
            "debate": StructuralElement("Debate/Refusal", 17, (15, 20)),
            "plot_point_1": StructuralElement("Plot Point 1/Break into 2", 25, (23, 27)),
            "b_story": StructuralElement("B-Story Introduction", 30, (28, 35)),
            "fun_and_games": StructuralElement("Fun and Games", 40, (30, 50)),
            "midpoint": StructuralElement("Midpoint Reversal", 55, (50, 60)),
            "bad_guys_close": StructuralElement("Bad Guys Close In", 65, (60, 70)),
            "all_is_lost": StructuralElement("All Is Lost", 75, (73, 78)),
            "plot_point_2": StructuralElement("Plot Point 2/Break into 3", 80, (78, 82)),
            "finale": StructuralElement("Finale/Climax", 90, (85, 95)),
            "final_image": StructuralElement("Final Image", 110, (95, 120))
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
        Perform complete structural analysis of screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete diagnostic report
        """
        # Calculate basic metrics
        lines = screenplay_text.split('\n')
        page_count = self._estimate_page_count(lines)

        # Find structural elements
        self._identify_structural_elements(screenplay_text)

        # Analyze three-act structure
        act_analysis = self._analyze_acts(screenplay_text, page_count)

        # Check against rules
        rule_violations = self._check_rules(screenplay_text, page_count)

        # Calculate score
        score = self._calculate_structure_score()

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, act_analysis, rule_violations)

        # ✅ NOVO: Structure breakdown visual (padrão DrDialogue)
        structure_breakdown = {}
        for act_name, act_data in act_analysis.items():
            page_start = 1
            if act_name == "act2":
                page_start = int(act_analysis["act1"]["pages"]) + 1
            elif act_name == "act3":
                page_start = int(act_analysis["act1"]["pages"]) + int(act_analysis["act2"]["pages"]) + 1

            page_end = page_start + int(act_data["pages"]) - 1

            # Encontrar elementos neste ato
            act_elements = []
            for elem_name, elem_data in self._elements_to_dict().items():
                if elem_data["found_at"] and page_start <= elem_data["found_at"] <= page_end:
                    act_elements.append({
                        "name": elem_data["name"],
                        "page": elem_data["found_at"],
                        "strength": elem_data["strength"]
                    })

            structure_breakdown[act_name] = {
                "pages": f"{page_start}-{page_end}",
                "total_pages": int(act_data["pages"]),
                "percentage": round(act_data["percentage"], 1),
                "expected_percentage": act_data["expected"],
                "status": act_data["status"],
                "elements_found": act_elements,
                "issues": [] if act_data["status"] == "good" else [
                    f"Act is {abs(round(act_data['percentage'] - act_data['expected'], 1))}% {'longer' if act_data['percentage'] > act_data['expected'] else 'shorter'} than expected"
                ]
            }

        # ✅ NOVO: Beats detected com confidence
        beats_detected = []
        for elem_name, elem_data in self._elements_to_dict().items():
            if elem_data["found_at"]:
                beats_detected.append({
                    "name": elem_data["name"],
                    "page": elem_data["found_at"],
                    "confidence": elem_data["strength"],
                    "expected_page": elem_data["expected_page"]
                })

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "page_count": page_count,

            # ✅ BREAKDOWN VISUAL (padrão DrDialogue)
            "structure_breakdown": structure_breakdown,
            "beats_detected": sorted(beats_detected, key=lambda x: x["page"]),

            # Dados originais
            "act_analysis": act_analysis,
            "structural_elements": self._elements_to_dict(),
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(score, rule_violations),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _estimate_page_count(self, lines: List[str]) -> int:
        """
        Estimate screenplay page count.
        Industry standard: ~55 lines per page.
        """
        # Filter out blank lines for more accurate count
        non_blank = [l for l in lines if l.strip()]
        return max(1, len(non_blank) // 55)

    def _identify_structural_elements(self, screenplay: str):
        """Identify key structural elements in the screenplay."""
        lines = screenplay.split('\n')

        # Look for common structural markers
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            current_page = i // 55

            # Opening image (first visual description)
            if i < 100 and not self.elements["opening_image"].found_at:
                if "fade in" in line_lower or "ext." in line_lower or "int." in line_lower:
                    self.elements["opening_image"].found_at = current_page
                    self.elements["opening_image"].strength = 0.8

            # Inciting incident markers (bilingual: EN + PT)
            # Check from page 1 onwards, but penalize if too early/late
            if current_page >= 1:
                inciting_markers = [
                    # English
                    "suddenly", "but then", "everything changes", "until",
                    # Portuguese
                    "de repente", "mas então", "mas aí", "tudo muda", "até que",
                    "subitamente", "inesperadamente", "arromba", "afogando",
                    "inconsciente", "acidente", "ataque", "explosão"
                ]
                if any(word in line_lower for word in inciting_markers):
                    if not self.elements["inciting_incident"].found_at:
                        self.elements["inciting_incident"].found_at = current_page
                        # Ideal range: 10-15, adjust strength based on position
                        if 10 <= current_page <= 15:
                            self.elements["inciting_incident"].strength = 1.0  # Perfect
                        elif 5 <= current_page < 10:
                            self.elements["inciting_incident"].strength = 0.6  # Early
                        elif 15 < current_page <= 20:
                            self.elements["inciting_incident"].strength = 0.7  # Slightly late
                        else:
                            self.elements["inciting_incident"].strength = 0.4  # Too early or too late

            # Midpoint markers (bilingual: EN + PT)
            if 50 <= current_page <= 60:
                midpoint_markers = [
                    # English
                    "revelation", "discovers", "realizes", "truth",
                    # Portuguese
                    "revelação", "descobre", "percebe", "verdade", "compreende",
                    "entende", "descubro", "percebo"
                ]
                if any(word in line_lower for word in midpoint_markers):
                    if not self.elements["midpoint"].found_at:
                        self.elements["midpoint"].found_at = current_page
                        self.elements["midpoint"].strength = 0.7

            # All is lost markers (bilingual: EN + PT)
            if 73 <= current_page <= 78:
                lost_markers = [
                    # English
                    "dead", "lost", "over", "failed", "defeated",
                    # Portuguese
                    "morto", "morreu", "perdido", "acabou", "falhou", "derrotado",
                    "perdeu", "acabado", "fim"
                ]
                if any(word in line_lower for word in lost_markers):
                    if not self.elements["all_is_lost"].found_at:
                        self.elements["all_is_lost"].found_at = current_page
                        self.elements["all_is_lost"].strength = 0.6

            # Climax markers (bilingual: EN + PT)
            if 85 <= current_page <= 95:
                climax_markers = [
                    # English
                    "final", "confrontation", "showdown", "battle",
                    # Portuguese
                    "final", "confronto", "batalha", "luta final", "duelo",
                    "enfrentamento", "combate"
                ]
                if any(word in line_lower for word in climax_markers):
                    if not self.elements["finale"].found_at:
                        self.elements["finale"].found_at = current_page
                        self.elements["finale"].strength = 0.8

    def _analyze_acts(self, screenplay: str, page_count: int) -> Dict[str, Any]:
        """Analyze three-act structure."""
        # Standard proportions
        expected_act1 = page_count * 0.25
        expected_act2 = page_count * 0.50
        expected_act3 = page_count * 0.25

        # Try to detect act breaks
        act1_end = self.elements["plot_point_1"].found_at or int(expected_act1)
        act2_end = self.elements["plot_point_2"].found_at or int(expected_act1 + expected_act2)

        actual_act1 = act1_end
        actual_act2 = act2_end - act1_end
        actual_act3 = page_count - act2_end

        return {
            "act1": {
                "pages": actual_act1,
                "percentage": (actual_act1 / page_count * 100) if page_count > 0 else 0,
                "expected": 25,
                "status": self._evaluate_proportion(actual_act1 / page_count * 100, 25)
            },
            "act2": {
                "pages": actual_act2,
                "percentage": (actual_act2 / page_count * 100) if page_count > 0 else 0,
                "expected": 50,
                "status": self._evaluate_proportion(actual_act2 / page_count * 100, 50)
            },
            "act3": {
                "pages": actual_act3,
                "percentage": (actual_act3 / page_count * 100) if page_count > 0 else 0,
                "expected": 25,
                "status": self._evaluate_proportion(actual_act3 / page_count * 100, 25)
            }
        }

    def _evaluate_proportion(self, actual: float, expected: float) -> str:
        """Evaluate if proportion is acceptable."""
        diff = abs(actual - expected)
        if diff <= 5:
            return "good"
        elif diff <= 10:
            return "acceptable"
        else:
            return "problematic"

    def _check_rules(self, screenplay: str, page_count: int) -> List[Dict[str, Any]]:
        """Check screenplay against structural rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            # Check based on rule ID
            if rule["id"] == "STRU.R001":
                # Three-act structure check
                act_analysis = self._analyze_acts(screenplay, page_count)
                if any(act["status"] == "problematic" for act in act_analysis.values()):
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": rule["fail_msg"],
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "STRU.R002":
                # Inciting incident timing
                if self.elements["inciting_incident"].found_at:
                    if not (10 <= self.elements["inciting_incident"].found_at <= 15):
                        violations.append({
                            "rule_id": rule["id"],
                            "title": rule["title"],
                            "severity": rule["severity"],
                            "message": f"Inciting incident at page {self.elements['inciting_incident'].found_at}",
                            "fix": rule["fix"]
                        })
                else:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": "critical",
                        "message": "No clear inciting incident found",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "STRU.R004":
                # Midpoint check
                if not self.elements["midpoint"].found_at:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": rule["fail_msg"],
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_structure_score(self) -> float:
        """Calculate overall structure score - DrDialogue pattern."""
        score = 90.0
        found_count = 0
        missing_count = 0
        misplaced_count = 0

        # 1. Check cada elemento estrutural
        for element in self.elements.values():
            if element.found_at is None:
                missing_count += 1
            else:
                found_count += 1
                # ✅ RANGE FLEXÍVEL (não rígido)
                # Ideal range (expected -5 to +5)
                ideal_min = element.expected_page - 5
                ideal_max = element.expected_page + 5
                # Acceptable range (expected -10 to +10)
                accept_min = element.expected_page - 10
                accept_max = element.expected_page + 10

                if element.page_range[0] <= element.found_at <= element.page_range[1]:
                    # Dentro do range - OK
                    pass
                elif accept_min <= element.found_at <= accept_max:
                    # Fora do ideal mas aceitável
                    misplaced_count += 1
                else:
                    # Muito fora do range
                    misplaced_count += 1

        # 2. PENALTIES GRADUAIS (não brutais)
        score -= min(missing_count * 8, 25)      # Max -25 por elementos ausentes
        score -= min(misplaced_count * 3, 15)    # Max -15 por elementos fora do lugar

        # 3. VIOLATIONS (padrão DrDialogue 20/15/8/5)
        violations = self._check_rules("", 100)
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 20  # DrDialogue pattern
            elif violation["severity"] == "high":
                score -= 15
            elif violation["severity"] == "medium":
                score -= 8
            elif violation["severity"] == "low":
                score -= 5

        # 4. BONUSES (limitados como DrDialogue)
        if found_count >= 6:  # Todos os elementos principais
            score += 5
        elif found_count >= 4:  # Maioria dos elementos
            score += 3

        # 5. Minimum score: Se TEM estrutura básica, não vai abaixo de 15
        if found_count > 0 and score < 15:
            score = 15 + (found_count * 2)

        # 6. RANGE PADRÃO
        return round(max(5.0, min(95.0, score)), 1)

    def _elements_to_dict(self) -> Dict[str, Any]:
        """Convert structural elements to dictionary."""
        result = {}
        for key, element in self.elements.items():
            result[key] = {
                "name": element.name,
                "expected_page": element.expected_page,
                "found_at": element.found_at,
                "strength": element.strength,
                "status": "found" if element.found_at else "missing"
            }
        return result

    def _generate_diagnosis(self, score: float, act_analysis: Dict, violations: List) -> str:
        """Generate narrative diagnosis."""
        diagnosis = f"Structural Analysis Score: {score}/100\n\n"

        if score >= 85:
            diagnosis += "Excellent structure! Your screenplay follows professional standards with clear act breaks and well-placed plot points. "
        elif score >= 70:
            diagnosis += "Good structural foundation with some areas for improvement. "
        elif score >= 50:
            diagnosis += "Structure needs significant work to meet professional standards. "
        else:
            diagnosis += "Major structural issues detected that will impact the story's effectiveness. "

        # Act analysis
        problems = [k for k, v in act_analysis.items() if v["status"] == "problematic"]
        if problems:
            diagnosis += f"Act proportions need rebalancing ({', '.join(problems)}). "

        # Critical violations
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical issues: {', '.join([v['title'] for v in critical])}. "

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Priority fixes for violations
        for violation in sorted(violations, key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 5:  # Limit to top 5
                break

        # General recommendations based on score
        if score < 70:
            recommendations.append("Consider studying 'Save the Cat' beat sheet for structural guidance")

        if not self.elements["midpoint"].found_at:
            recommendations.append("Add a strong midpoint reversal around page 55")

        return recommendations