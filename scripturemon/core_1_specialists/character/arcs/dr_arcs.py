"""
Script Doctor Arcmon - Character Arc and Transformation Specialist
A Script Doctor™ in Digimon form specializing in character transformation and growth arcs.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ArcStage:
    """A stage in a character's arc."""
    stage_name: str
    page_range: Tuple[int, int]
    description: str
    character_state: str
    evidence: List[str]  # Lines/actions showing this stage


@dataclass
class CharacterArc:
    """Complete arc analysis for a character."""
    character_name: str
    arc_type: str  # positive, negative, flat, dual
    has_clear_arc: bool
    starting_state: str
    ending_state: str
    catalyst_present: bool
    catalyst_description: str
    transformation_earned: bool
    stages: List[ArcStage]
    resistance_shown: bool
    cost_of_change: str
    point_of_no_return_page: int
    arc_completion_score: float  # 0-1
    thematic_alignment: float  # 0-1


class DrCharacterArcs:
    """
    Script Doctor Arcmon - The Character Arc and Transformation Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing character arcs,
    transformations, and growth trajectories throughout the screenplay.

    Identity: Script Doctor first, Digimon arc specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Arcmon with rules and configuration."""
        self.name = "Script Doctor Arcmon"
        self.digimon_name = "Arcmon"
        self.title = "Script Doctor - Character Arc and Transformation Specialist"
        self.specialty = "Character transformation, growth arcs, change progression, earned evolution"
        self.identity = "I am Script Doctor Arcmon, a professional Script Doctor™ specializing in character arcs"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "rules" / "character_arcs_rules.yaml"

        self.rules = self._load_rules()

        # Arc markers
        self.change_markers = [
            "realize", "understand", "learn", "discover", "change",
            "transform", "become", "evolve", "grow", "accept"
        ]

        self.resistance_markers = [
            "can't", "won't", "never", "refuse", "deny",
            "impossible", "no way", "not me", "i don't"
        ]

        self.catalyst_markers = [
            "everything changed", "that's when", "after that",
            "from that moment", "never the same", "turned upside down"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze character arcs and transformations in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete arc diagnostic report
        """
        # Extract characters and their journeys
        characters = self._extract_characters(screenplay_text)

        # Analyze each character's arc
        character_arcs = {}
        for character in characters:
            arc = self._analyze_character_arc(screenplay_text, character)
            if arc:
                character_arcs[character] = arc

        # Identify protagonist
        protagonist = self._identify_protagonist(character_arcs)
        protagonist_arc = character_arcs.get(protagonist) if protagonist else None

        # Analyze arc relationships
        arc_relationships = self._analyze_arc_relationships(character_arcs)

        # Check progressive transformation
        progression_analysis = self._analyze_progression(protagonist_arc) if protagonist_arc else {}

        # Analyze thematic alignment
        thematic_alignment = self._calculate_thematic_alignment(character_arcs)

        # Check for false victories/defeats
        complexity_analysis = self._analyze_arc_complexity(protagonist_arc) if protagonist_arc else {}

        # Analyze transformation demonstration
        demonstration_analysis = self._analyze_transformation_demonstration(
            screenplay_text, protagonist_arc
        ) if protagonist_arc else {}

        # Calculate arc timeline believability
        timeline_analysis = self._analyze_timeline(protagonist_arc) if protagonist_arc else {}

        # Check against rules
        rule_violations = self._check_arc_rules(
            protagonist_arc, character_arcs, progression_analysis,
            demonstration_analysis
        )

        # Calculate score
        score = self._calculate_arc_score(
            protagonist_arc, character_arcs, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, protagonist_arc, character_arcs, rule_violations
        )

        # Prepare arc summaries
        arc_summaries = self._create_arc_summaries(character_arcs)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "characters_analyzed": len(character_arcs),
            "protagonist": protagonist if protagonist else "Unknown",
            "protagonist_arc_type": protagonist_arc.arc_type if protagonist_arc else "none",
            "protagonist_has_clear_arc": protagonist_arc.has_clear_arc if protagonist_arc else False,
            "protagonist_starting_state": protagonist_arc.starting_state if protagonist_arc else "undefined",
            "protagonist_ending_state": protagonist_arc.ending_state if protagonist_arc else "undefined",
            "catalyst_present": protagonist_arc.catalyst_present if protagonist_arc else False,
            "catalyst_description": protagonist_arc.catalyst_description if protagonist_arc else "none",
            "transformation_earned": protagonist_arc.transformation_earned if protagonist_arc else False,
            "resistance_shown": protagonist_arc.resistance_shown if protagonist_arc else False,
            "point_of_no_return": protagonist_arc.point_of_no_return_page if protagonist_arc else 0,
            "cost_of_change": protagonist_arc.cost_of_change if protagonist_arc else "none",
            "arc_stages": len(protagonist_arc.stages) if protagonist_arc else 0,
            "progression_score": progression_analysis.get("score", 0),
            "progressive_steps": progression_analysis.get("steps", []),
            "arc_relationships": arc_relationships,
            "mirror_arcs": arc_relationships.get("mirrors", []),
            "contrast_arcs": arc_relationships.get("contrasts", []),
            "supporting_arcs_count": len([a for a in character_arcs.values() if a.has_clear_arc]) - 1,
            "thematic_alignment": thematic_alignment,
            "complexity_score": complexity_analysis.get("score", 0),
            "false_moments": complexity_analysis.get("false_moments", []),
            "transformation_demonstrated": demonstration_analysis.get("demonstrated", False),
            "demonstration_examples": demonstration_analysis.get("examples", []),
            "timeline_believability": timeline_analysis.get("believable", False),
            "timeline_score": timeline_analysis.get("score", 0),
            "arc_summaries": arc_summaries,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, protagonist_arc, character_arcs
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _extract_characters(self, screenplay: str) -> List[str]:
        """Extract main characters from screenplay."""
        lines = screenplay.split('\n')
        character_counts = defaultdict(int)

        for line in lines:
            line = line.strip()
            # Character name line: all caps, not scene heading
            if (line.isupper() and
                len(line.split()) <= 3 and
                not any(marker in line for marker in ['INT.', 'EXT.', 'FADE', 'CUT'])):

                character = line.split('(')[0].strip()  # Remove parentheticals
                if character:
                    character_counts[character] += 1

        # Return characters that appear more than 5 times (main characters)
        main_characters = [char for char, count in character_counts.items() if count > 5]
        return sorted(main_characters, key=lambda x: character_counts[x], reverse=True)[:5]

    def _analyze_character_arc(self, screenplay: str, character: str) -> Optional[CharacterArc]:
        """Analyze a single character's arc."""
        lines = screenplay.split('\n')

        # Find character's first and last substantial appearances
        appearances = self._find_character_appearances(lines, character)
        if len(appearances) < 3:
            return None  # Not enough to determine arc

        # Analyze starting state
        starting_state = self._analyze_character_state(
            lines, character, appearances[:3]
        )

        # Analyze ending state
        ending_state = self._analyze_character_state(
            lines, character, appearances[-3:]
        )

        # Determine arc type
        arc_type = self._determine_arc_type(starting_state, ending_state)

        # Find catalyst
        catalyst = self._find_catalyst(lines, character, appearances)

        # Check for resistance
        resistance = self._find_resistance(lines, character, appearances)

        # Find point of no return
        point_of_no_return = self._find_point_of_no_return(
            lines, character, appearances
        )

        # Analyze transformation stages
        stages = self._analyze_arc_stages(lines, character, appearances)

        # Determine if transformation is earned
        earned = self._is_transformation_earned(stages, catalyst["present"])

        # Find cost of change
        cost = self._find_cost_of_change(lines, character, appearances)

        # Calculate completion score
        completion_score = self._calculate_completion_score(
            stages, catalyst["present"], earned, cost
        )

        # Estimate thematic alignment
        thematic = self._estimate_thematic_alignment(arc_type, stages)

        return CharacterArc(
            character_name=character,
            arc_type=arc_type,
            has_clear_arc=(starting_state != ending_state),
            starting_state=starting_state,
            ending_state=ending_state,
            catalyst_present=catalyst["present"],
            catalyst_description=catalyst["description"],
            transformation_earned=earned,
            stages=stages,
            resistance_shown=resistance,
            cost_of_change=cost,
            point_of_no_return_page=point_of_no_return,
            arc_completion_score=completion_score,
            thematic_alignment=thematic
        )

    def _find_character_appearances(self, lines: List[str], character: str) -> List[int]:
        """Find all line numbers where character appears."""
        appearances = []

        for i, line in enumerate(lines):
            if line.strip() == character:
                # Character is speaking
                appearances.append(i)
            elif character in line:
                # Character mentioned in action/description
                appearances.append(i)

        return appearances

    def _analyze_character_state(self, lines: List[str], character: str,
                                 appearance_indices: List[int]) -> str:
        """Analyze character's state based on their appearances."""
        if not appearance_indices:
            return "undefined"

        # Collect relevant text around appearances
        context_lines = []
        for idx in appearance_indices:
            # Get surrounding context
            start = max(0, idx - 2)
            end = min(len(lines), idx + 10)
            context_lines.extend(lines[start:end])

        context_text = ' '.join(context_lines).lower()

        # Analyze emotional/psychological state
        if any(word in context_text for word in ["confident", "strong", "sure", "determined"]):
            return "confident"
        elif any(word in context_text for word in ["afraid", "scared", "nervous", "uncertain"]):
            return "fearful"
        elif any(word in context_text for word in ["angry", "furious", "rage", "hate"]):
            return "angry"
        elif any(word in context_text for word in ["sad", "depressed", "lonely", "lost"]):
            return "sad"
        elif any(word in context_text for word in ["happy", "joy", "content", "peace"]):
            return "content"
        elif any(word in context_text for word in ["confused", "torn", "conflicted"]):
            return "conflicted"
        else:
            return "neutral"

    def _determine_arc_type(self, starting: str, ending: str) -> str:
        """Determine the type of character arc."""
        positive_changes = [
            ("fearful", "confident"),
            ("sad", "content"),
            ("angry", "peaceful"),
            ("conflicted", "resolved"),
            ("selfish", "selfless")
        ]

        negative_changes = [
            ("confident", "fearful"),
            ("content", "sad"),
            ("innocent", "corrupted"),
            ("hopeful", "cynical")
        ]

        if starting == ending:
            return "flat"

        for start, end in positive_changes:
            if starting == start and ending == end:
                return "positive"

        for start, end in negative_changes:
            if starting == start and ending == end:
                return "negative"

        # Default: if different, call it positive
        return "positive" if starting != ending else "flat"

    def _find_catalyst(self, lines: List[str], character: str,
                      appearances: List[int]) -> Dict[str, Any]:
        """Find the catalyst for character change."""
        if len(appearances) < 2:
            return {"present": False, "description": "none"}

        # Look for catalyst in first third of appearances
        first_third_idx = len(appearances) // 3
        search_appearances = appearances[:first_third_idx + 1]

        for app_idx in search_appearances:
            # Check surrounding lines for catalyst markers
            start = max(0, app_idx - 5)
            end = min(len(lines), app_idx + 5)
            context = ' '.join(lines[start:end]).lower()

            if any(marker in context for marker in self.catalyst_markers):
                return {
                    "present": True,
                    "description": "Major event triggers change"
                }

        # Check for dramatic events early in screenplay
        early_lines = ' '.join(lines[:100]).lower()
        if any(word in early_lines for word in ["dies", "killed", "accident", "fired", "divorced"]):
            return {
                "present": True,
                "description": "Traumatic event catalyzes transformation"
            }

        return {"present": False, "description": "No clear catalyst"}

    def _find_resistance(self, lines: List[str], character: str,
                        appearances: List[int]) -> bool:
        """Find if character shows resistance to change."""
        if not appearances:
            return False

        # Look in middle third of appearances
        start_idx = len(appearances) // 3
        end_idx = 2 * len(appearances) // 3

        for app_idx in appearances[start_idx:end_idx]:
            # Check character's dialogue for resistance
            if app_idx < len(lines) - 1:
                next_lines = []
                for i in range(app_idx + 1, min(app_idx + 5, len(lines))):
                    if lines[i].strip() and not lines[i].strip().isupper():
                        next_lines.append(lines[i].lower())

                dialogue = ' '.join(next_lines)
                if any(marker in dialogue for marker in self.resistance_markers):
                    return True

        return False

    def _find_point_of_no_return(self, lines: List[str], character: str,
                                 appearances: List[int]) -> int:
        """Find the page where character reaches point of no return."""
        if not appearances:
            return 0

        # Usually in last third
        last_third_start = 2 * len(appearances) // 3

        for app_idx in appearances[last_third_start:]:
            # Look for decisive action or declaration
            context_start = max(0, app_idx - 3)
            context_end = min(len(lines), app_idx + 10)
            context = ' '.join(lines[context_start:context_end]).lower()

            if any(word in context for word in ["no turning back", "decided", "choose", "must", "will"]):
                # Estimate page number (assuming ~55 lines per page)
                return app_idx // 55

        # Default to 2/3 through screenplay
        return (len(lines) * 2) // (3 * 55)

    def _analyze_arc_stages(self, lines: List[str], character: str,
                           appearances: List[int]) -> List[ArcStage]:
        """Analyze the stages of character's arc."""
        if not appearances:
            return []

        stages = []
        total_pages = len(lines) // 55  # Approximate

        # Stage 1: Setup (first 20%)
        setup_apps = [a for a in appearances if a < len(lines) * 0.2]
        if setup_apps:
            stages.append(ArcStage(
                stage_name="Setup",
                page_range=(1, total_pages // 5),
                description="Character in ordinary world",
                character_state=self._analyze_character_state(lines, character, setup_apps[:3]),
                evidence=self._extract_evidence(lines, setup_apps[:2])
            ))

        # Stage 2: Catalyst (20-30%)
        catalyst_apps = [a for a in appearances if len(lines) * 0.2 <= a < len(lines) * 0.3]
        if catalyst_apps:
            stages.append(ArcStage(
                stage_name="Catalyst",
                page_range=(total_pages // 5, total_pages * 3 // 10),
                description="Inciting incident forces change",
                character_state="disrupted",
                evidence=self._extract_evidence(lines, catalyst_apps[:2])
            ))

        # Stage 3: Resistance (30-50%)
        resist_apps = [a for a in appearances if len(lines) * 0.3 <= a < len(lines) * 0.5]
        if resist_apps:
            stages.append(ArcStage(
                stage_name="Resistance",
                page_range=(total_pages * 3 // 10, total_pages // 2),
                description="Character resists change",
                character_state="conflicted",
                evidence=self._extract_evidence(lines, resist_apps[:2])
            ))

        # Stage 4: Transformation (50-80%)
        transform_apps = [a for a in appearances if len(lines) * 0.5 <= a < len(lines) * 0.8]
        if transform_apps:
            stages.append(ArcStage(
                stage_name="Transformation",
                page_range=(total_pages // 2, total_pages * 4 // 5),
                description="Character undergoes change",
                character_state="evolving",
                evidence=self._extract_evidence(lines, transform_apps[:2])
            ))

        # Stage 5: Resolution (80-100%)
        resolution_apps = [a for a in appearances if a >= len(lines) * 0.8]
        if resolution_apps:
            stages.append(ArcStage(
                stage_name="Resolution",
                page_range=(total_pages * 4 // 5, total_pages),
                description="New equilibrium reached",
                character_state=self._analyze_character_state(lines, character, resolution_apps[-3:]),
                evidence=self._extract_evidence(lines, resolution_apps[:2])
            ))

        return stages

    def _extract_evidence(self, lines: List[str], appearance_indices: List[int]) -> List[str]:
        """Extract evidence lines for a stage."""
        evidence = []

        for idx in appearance_indices[:2]:  # First 2 appearances
            if idx < len(lines):
                # Get the character's dialogue or action
                if lines[idx].strip().isupper():
                    # Character name - get their dialogue
                    for i in range(idx + 1, min(idx + 5, len(lines))):
                        if lines[i].strip() and not lines[i].strip().isupper():
                            evidence.append(lines[i].strip()[:80])
                            break
                else:
                    # Action line mentioning character
                    evidence.append(lines[idx].strip()[:80])

        return evidence[:3]  # Max 3 pieces of evidence

    def _is_transformation_earned(self, stages: List[ArcStage], catalyst: bool) -> bool:
        """Determine if transformation is earned."""
        # Must have catalyst and at least 3 stages
        if not catalyst or len(stages) < 3:
            return False

        # Must have progression through stages
        required_stages = ["Setup", "Transformation"]
        stage_names = [s.stage_name for s in stages]

        return all(req in stage_names for req in required_stages)

    def _find_cost_of_change(self, lines: List[str], character: str,
                            appearances: List[int]) -> str:
        """Find what the character loses in their transformation."""
        if not appearances:
            return "none"

        # Look in last half of appearances
        last_half = appearances[len(appearances) // 2:]

        loss_words = ["lost", "sacrifice", "give up", "leave behind", "goodbye", "never again"]

        for app_idx in last_half:
            context = ' '.join(lines[max(0, app_idx - 5):min(len(lines), app_idx + 5)]).lower()

            for loss_word in loss_words:
                if loss_word in context:
                    if "friend" in context:
                        return "relationships"
                    elif "home" in context or "place" in context:
                        return "security"
                    elif "dream" in context or "hope" in context:
                        return "innocence"
                    elif "self" in context or "who i" in context:
                        return "identity"
                    else:
                        return "sacrifice made"

        return "minimal cost"

    def _calculate_completion_score(self, stages: List[ArcStage], catalyst: bool,
                                   earned: bool, cost: str) -> float:
        """Calculate how complete the arc is."""
        score = 0.0

        # Points for stages
        score += min(len(stages) * 0.15, 0.6)  # Max 0.6 for stages

        # Points for catalyst
        if catalyst:
            score += 0.15

        # Points for earned transformation
        if earned:
            score += 0.15

        # Points for cost
        if cost != "none" and cost != "minimal cost":
            score += 0.1

        return min(1.0, score)

    def _estimate_thematic_alignment(self, arc_type: str, stages: List[ArcStage]) -> float:
        """Estimate how well arc aligns with typical themes."""
        if arc_type == "positive" and len(stages) >= 4:
            return 0.8
        elif arc_type == "negative" and len(stages) >= 3:
            return 0.7
        elif arc_type == "flat":
            return 0.5  # Flat arcs can be thematically strong too
        else:
            return 0.3

    def _identify_protagonist(self, arcs: Dict[str, CharacterArc]) -> Optional[str]:
        """Identify the protagonist based on arc prominence."""
        if not arcs:
            return None

        # Score each character
        scores = {}
        for name, arc in arcs.items():
            score = 0
            if arc.has_clear_arc:
                score += 3
            if arc.catalyst_present:
                score += 2
            if arc.transformation_earned:
                score += 2
            score += arc.arc_completion_score * 3

            scores[name] = score

        # Return highest scoring character
        if scores:
            return max(scores, key=scores.get)

        return None

    def _calculate_thematic_alignment(self, arcs: Dict[str, CharacterArc]) -> float:
        """Calculate overall thematic alignment of character arcs."""
        if not arcs:
            return 0.0

        alignment_scores = []
        for arc in arcs.values():
            alignment_scores.append(arc.thematic_alignment)

        return sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.0

    def _analyze_arc_relationships(self, arcs: Dict[str, CharacterArc]) -> Dict[str, Any]:
        """Analyze relationships between character arcs."""
        relationships = {
            "mirrors": [],
            "contrasts": [],
            "parallels": []
        }

        if len(arcs) < 2:
            return relationships

        arc_list = list(arcs.values())

        for i in range(len(arc_list)):
            for j in range(i + 1, len(arc_list)):
                arc1, arc2 = arc_list[i], arc_list[j]

                # Mirror arcs: similar transformations
                if arc1.arc_type == arc2.arc_type and arc1.arc_type != "flat":
                    relationships["mirrors"].append(
                        (arc1.character_name, arc2.character_name)
                    )

                # Contrast arcs: opposite transformations
                elif (arc1.arc_type == "positive" and arc2.arc_type == "negative") or \
                     (arc1.arc_type == "negative" and arc2.arc_type == "positive"):
                    relationships["contrasts"].append(
                        (arc1.character_name, arc2.character_name)
                    )

                # Parallel arcs: same catalyst
                if arc1.catalyst_description == arc2.catalyst_description and \
                   arc1.catalyst_present and arc2.catalyst_present:
                    relationships["parallels"].append(
                        (arc1.character_name, arc2.character_name)
                    )

        return relationships

    def _analyze_progression(self, arc: Optional[CharacterArc]) -> Dict[str, Any]:
        """Analyze progression of transformation."""
        if not arc or not arc.stages:
            return {"score": 0, "steps": []}

        steps = []
        for stage in arc.stages:
            steps.append({
                "stage": stage.stage_name,
                "state": stage.character_state,
                "pages": f"{stage.page_range[0]}-{stage.page_range[1]}"
            })

        # Score based on number and clarity of steps
        score = min(len(steps) * 0.2, 1.0)

        return {
            "score": score,
            "steps": steps
        }

    def _analyze_arc_complexity(self, arc: Optional[CharacterArc]) -> Dict[str, Any]:
        """Analyze complexity of arc (false victories/defeats)."""
        if not arc:
            return {"score": 0, "false_moments": []}

        # Look for reversals in stages
        false_moments = []
        complexity_score = 0.3  # Base score

        if len(arc.stages) > 3:
            # Check for state reversals
            for i in range(len(arc.stages) - 1):
                if arc.stages[i].character_state != arc.stages[i + 1].character_state:
                    false_moments.append(f"Stage {i + 1}: State reversal")
                    complexity_score += 0.2

        return {
            "score": min(1.0, complexity_score),
            "false_moments": false_moments[:3]  # Top 3
        }

    def _analyze_transformation_demonstration(self, screenplay: str,
                                             arc: Optional[CharacterArc]) -> Dict[str, Any]:
        """Analyze if transformation is demonstrated through action."""
        if not arc or not arc.has_clear_arc:
            return {"demonstrated": False, "examples": []}

        lines = screenplay.split('\n')
        examples = []

        # Look for action demonstrating change in final third
        final_third_start = 2 * len(lines) // 3

        for i in range(final_third_start, len(lines)):
            if arc.character_name in lines[i]:
                # Check for action verbs showing change
                for j in range(i, min(i + 5, len(lines))):
                    line_lower = lines[j].lower()
                    if any(word in line_lower for word in self.change_markers):
                        examples.append(lines[j].strip()[:80])
                        break

        demonstrated = len(examples) > 0

        return {
            "demonstrated": demonstrated,
            "examples": examples[:3]  # Top 3
        }

    def _analyze_timeline(self, arc: Optional[CharacterArc]) -> Dict[str, Any]:
        """Analyze if transformation timeline is believable."""
        if not arc:
            return {"believable": False, "score": 0}

        # Check if arc has enough stages
        if len(arc.stages) < 3:
            return {"believable": False, "score": 0.3}

        # Check if transformation is too quick
        if arc.point_of_no_return_page < 50:
            return {"believable": False, "score": 0.4}

        # Good timeline if stages are well distributed
        score = min(len(arc.stages) * 0.2, 0.8)

        if arc.resistance_shown:
            score += 0.2

        return {
            "believable": score > 0.6,
            "score": min(1.0, score)
        }

    def _check_arc_rules(self, protagonist_arc: Optional[CharacterArc],
                        all_arcs: Dict[str, CharacterArc],
                        progression: Dict, demonstration: Dict) -> List[Dict]:
        """Check character arcs against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "ARC.R001":
                # Clear arc trajectory
                if not protagonist_arc or not protagonist_arc.has_clear_arc:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Protagonist lacks clear character arc",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ARC.R002":
                # Earned transformation
                if protagonist_arc and not protagonist_arc.transformation_earned:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Character change feels unearned",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ARC.R004":
                # Catalyst for change
                if protagonist_arc and not protagonist_arc.catalyst_present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No clear catalyst for transformation",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ARC.R005":
                # Resistance to change
                if protagonist_arc and not protagonist_arc.resistance_shown:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Character accepts change too easily",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ARC.R006":
                # Progressive steps
                if progression.get("score", 0) < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Transformation lacks progressive steps",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "ARC.R013":
                # Transformation demonstration
                if not demonstration.get("demonstrated", False):
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Change not demonstrated through action",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_arc_score(self, protagonist_arc: Optional[CharacterArc],
                            all_arcs: Dict[str, CharacterArc],
                            violations: List) -> float:
        """Calculate overall arc score."""
        score = 90.0

        # Deduct for violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 20
            elif violation["severity"] == "high":
                score -= 15
            elif violation["severity"] == "medium":
                score -= 8
            elif violation["severity"] == "low":
                score -= 5

        # Bonus for excellence
        if protagonist_arc:
            if protagonist_arc.has_clear_arc:
                score += 5
            if protagonist_arc.transformation_earned:
                score += 5
            if protagonist_arc.arc_completion_score > 0.8:
                score += 5

        # Bonus for supporting arcs
        supporting_arcs = len([a for a in all_arcs.values() if a.has_clear_arc]) - 1
        if supporting_arcs > 0:
            score += min(supporting_arcs * 2, 10)

        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, protagonist_arc: Optional[CharacterArc],
                          all_arcs: Dict[str, CharacterArc], violations: List) -> str:
        """Generate diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Strong character arcs with earned transformations"
        elif score >= 60:
            level = "GOOD"
            summary = "Clear arcs but could be strengthened"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Arc issues affecting character development"
        else:
            level = "POOR"
            summary = "Major arc problems throughout"

        diagnosis = f"CHARACTER ARCS {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if not protagonist_arc or not protagonist_arc.has_clear_arc:
            issues.append("unclear protagonist arc")
        if protagonist_arc and not protagonist_arc.catalyst_present:
            issues.append("missing catalyst")
        if protagonist_arc and not protagonist_arc.transformation_earned:
            issues.append("unearned change")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _create_arc_summaries(self, arcs: Dict[str, CharacterArc]) -> List[Dict]:
        """Create summaries of all character arcs."""
        summaries = []

        for name, arc in arcs.items():
            summaries.append({
                "character": name,
                "arc_type": arc.arc_type,
                "has_arc": arc.has_clear_arc,
                "start": arc.starting_state,
                "end": arc.ending_state,
                "completion": f"{arc.arc_completion_score*100:.0f}%"
            })

        return summaries

    def _generate_recommendations(self, score: float, violations: List,
                                 protagonist_arc: Optional[CharacterArc],
                                 all_arcs: Dict[str, CharacterArc]) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:  # Top 3 violations
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if not protagonist_arc or not protagonist_arc.has_clear_arc:
            recommendations.append("Define clear beginning, middle, and end states for protagonist")

        if protagonist_arc and not protagonist_arc.catalyst_present:
            recommendations.append("Add inciting incident that forces protagonist to change")

        if protagonist_arc and not protagonist_arc.resistance_shown:
            recommendations.append("Show protagonist resisting change before accepting it")

        if protagonist_arc and protagonist_arc.cost_of_change in ["none", "minimal cost"]:
            recommendations.append("Make transformation cost the character something meaningful")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study character arcs in acclaimed screenplays")

        return recommendations[:5]  # Return top 5