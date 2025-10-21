"""
Script Doctor Relatemon - Character Relationships and Dynamics Specialist
A Script Doctor™ in Digimon form specializing in relationship dynamics and interpersonal connections.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import math


@dataclass
class RelationshipDynamic:
    """Analysis of a relationship between two characters."""
    character_a: str
    character_b: str
    relationship_type: str  # romantic, friendship, family, rival, etc.
    interaction_count: int
    chemistry_score: float  # 0-1
    conflict_present: bool
    evolution_tracked: bool
    power_balance: str  # equal, a_dominant, b_dominant, shifting
    emotional_depth: float  # 0-1
    stakes_level: str  # high, medium, low
    obstacles: List[str]
    vulnerability_shown: bool
    subtext_present: bool
    resolution_status: str  # resolved, unresolved, open


@dataclass
class InteractionMoment:
    """A specific interaction between characters."""
    characters: Tuple[str, str]
    page: int
    interaction_type: str  # dialogue, action, conflict, intimate
    emotional_tone: str
    advances_relationship: bool
    reveals_character: bool
    has_subtext: bool


class DrRelationships:
    """
    Script Doctor Relatemon - The Character Relationships and Dynamics Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing relationship dynamics,
    interpersonal conflicts, and emotional connections between characters.

    Identity: Script Doctor first, Digimon relationship specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Relatemon with rules and configuration."""
        self.name = "Script Doctor Relatemon"
        self.digimon_name = "Relatemon"
        self.title = "Script Doctor - Character Relationships and Dynamics Specialist"
        self.specialty = "Relationship dynamics, interpersonal conflict, emotional connections, character chemistry"
        self.identity = "I am Script Doctor Relatemon, a professional Script Doctor™ specializing in relationships"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "character_relationships_rules.yaml"

        self.rules = self._load_rules()

        # Relationship markers
        self.chemistry_words = [
            "smile", "laugh", "touch", "look", "eyes meet", "connection",
            "understand", "know", "feel", "together", "close"
        ]

        self.conflict_words = [
            "argue", "fight", "disagree", "clash", "oppose", "challenge",
            "confront", "tension", "struggle", "conflict", "versus"
        ]

        self.vulnerability_words = [
            "truth", "honest", "admit", "confess", "reveal", "expose",
            "open", "share", "trust", "fear", "weakness", "need"
        ]

        self.relationship_types = {
            "romantic": ["love", "kiss", "embrace", "desire", "passion"],
            "friendship": ["friend", "buddy", "pal", "trust", "loyalty"],
            "family": ["father", "mother", "son", "daughter", "brother", "sister"],
            "rival": ["compete", "rival", "enemy", "oppose", "challenge"],
            "mentor": ["teach", "learn", "guide", "wisdom", "student"]
        }

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze character relationships and dynamics in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete relationship diagnostic report
        """
        # Extract characters
        characters = self._extract_main_characters(screenplay_text)

        # Map all interactions
        interactions = self._map_interactions(screenplay_text, characters)

        # Analyze relationship dynamics
        relationships = self._analyze_relationships(screenplay_text, characters, interactions)

        # Identify central relationship
        central_relationship = self._identify_central_relationship(relationships)

        # Analyze relationship evolution
        evolution_analysis = self._analyze_evolution(relationships, interactions)

        # Check for conflict in relationships
        conflict_analysis = self._analyze_relationship_conflicts(relationships)

        # Analyze chemistry
        chemistry_analysis = self._analyze_chemistry(relationships)

        # Check power dynamics
        power_dynamics = self._analyze_power_dynamics(relationships)

        # Analyze obstacles
        obstacle_analysis = self._analyze_obstacles(relationships)

        # Check vulnerability
        vulnerability_analysis = self._analyze_vulnerability(relationships, interactions)

        # Analyze subtext
        subtext_analysis = self._analyze_subtext(interactions)

        # Check relationship variety
        variety_analysis = self._analyze_relationship_variety(relationships)

        # Analyze resolution
        resolution_analysis = self._analyze_resolutions(screenplay_text, relationships)

        # Check against rules
        rule_violations = self._check_relationship_rules(
            relationships, central_relationship, evolution_analysis,
            conflict_analysis, chemistry_analysis
        )

        # Calculate score
        score = self._calculate_relationship_score(
            relationships, central_relationship, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, relationships, central_relationship, rule_violations
        )

        # Prepare relationship summaries
        relationship_summaries = self._create_relationship_summaries(relationships)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "character_count": len(characters),
            "relationship_count": len(relationships),
            "total_interactions": len(interactions),
            "central_relationship": self._format_relationship_name(central_relationship) if central_relationship else "None",
            "central_relationship_defined": central_relationship is not None,
            "relationships_with_stakes": sum(1 for r in relationships if r.stakes_level in ["high", "medium"]),
            "evolving_relationships": evolution_analysis["evolving_count"],
            "static_relationships": evolution_analysis["static_count"],
            "relationships_with_conflict": conflict_analysis["with_conflict"],
            "conflict_percentage": conflict_analysis["percentage"],
            "average_chemistry_score": chemistry_analysis["average_score"],
            "high_chemistry_pairs": chemistry_analysis["high_chemistry_pairs"],
            "power_dynamics_clear": power_dynamics["clear_dynamics"],
            "shifting_power_count": power_dynamics["shifting_count"],
            "relationships_with_obstacles": obstacle_analysis["with_obstacles"],
            "obstacle_types": obstacle_analysis["types"],
            "vulnerability_present": vulnerability_analysis["present"],
            "vulnerability_moments": vulnerability_analysis["moment_count"],
            "subtext_percentage": subtext_analysis["percentage"],
            "relationship_variety_score": variety_analysis["variety_score"],
            "relationship_types_present": variety_analysis["types_present"],
            "resolved_relationships": resolution_analysis["resolved_count"],
            "unresolved_relationships": resolution_analysis["unresolved_count"],
            "relationship_summaries": relationship_summaries,
            "key_interactions": self._get_key_interactions(interactions),
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, relationships, central_relationship
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _extract_main_characters(self, screenplay: str) -> List[str]:
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

        # Return characters that appear more than 5 times
        main_characters = [char for char, count in character_counts.items() if count > 5]
        return sorted(main_characters, key=lambda x: character_counts[x], reverse=True)[:8]

    def _map_interactions(self, screenplay: str, characters: List[str]) -> List[InteractionMoment]:
        """Map all interactions between characters."""
        lines = screenplay.split('\n')
        interactions = []

        # Track when characters appear close to each other
        for i in range(len(lines)):
            # Check 10-line windows for character proximity
            window_start = max(0, i - 5)
            window_end = min(len(lines), i + 5)
            window_lines = lines[window_start:window_end]
            window_text = ' '.join(window_lines)

            # Check each character pair
            for j, char_a in enumerate(characters):
                for char_b in characters[j+1:]:
                    if char_a in window_text and char_b in window_text:
                        # Characters appear near each other
                        page = i // 55  # Approximate page

                        # Determine interaction type
                        interaction_type = self._determine_interaction_type(window_text)
                        emotional_tone = self._determine_emotional_tone(window_text)

                        # Check if advances relationship
                        advances = self._check_advances_relationship(window_text)

                        # Check for character revelation
                        reveals = self._check_reveals_character(window_text)

                        # Check for subtext
                        has_subtext = self._check_for_subtext(window_text)

                        interactions.append(InteractionMoment(
                            characters=(char_a, char_b),
                            page=page,
                            interaction_type=interaction_type,
                            emotional_tone=emotional_tone,
                            advances_relationship=advances,
                            reveals_character=reveals,
                            has_subtext=has_subtext
                        ))

                        # Skip ahead to avoid duplicate detection
                        i += 5
                        break

        return interactions

    def _determine_interaction_type(self, text: str) -> str:
        """Determine the type of interaction."""
        text_lower = text.lower()

        if any(word in text_lower for word in self.conflict_words):
            return "conflict"
        elif any(word in text_lower for word in ["kiss", "embrace", "hold", "touch"]):
            return "intimate"
        elif "?" in text and "!" in text:
            return "dialogue"
        else:
            return "action"

    def _determine_emotional_tone(self, text: str) -> str:
        """Determine emotional tone of interaction."""
        text_lower = text.lower()

        if any(word in text_lower for word in ["love", "care", "tender"]):
            return "loving"
        elif any(word in text_lower for word in ["angry", "furious", "rage"]):
            return "angry"
        elif any(word in text_lower for word in ["sad", "cry", "tears"]):
            return "sad"
        elif any(word in text_lower for word in ["laugh", "smile", "joy"]):
            return "joyful"
        elif any(word in text_lower for word in ["tense", "nervous", "awkward"]):
            return "tense"
        else:
            return "neutral"

    def _check_advances_relationship(self, text: str) -> bool:
        """Check if interaction advances the relationship."""
        text_lower = text.lower()
        advance_markers = [
            "closer", "understand", "realize", "forgive", "trust",
            "admit", "confess", "change", "different", "new"
        ]
        return any(marker in text_lower for marker in advance_markers)

    def _check_reveals_character(self, text: str) -> bool:
        """Check if interaction reveals character."""
        text_lower = text.lower()
        reveal_markers = [
            "truth", "really", "actually", "never knew", "didn't know",
            "secret", "confession", "admit", "reveal"
        ]
        return any(marker in text_lower for marker in reveal_markers)

    def _check_for_subtext(self, text: str) -> bool:
        """Check if interaction has subtext."""
        # Simple heuristic: conflicting verbal and non-verbal
        has_positive_words = any(word in text.lower() for word in ["fine", "okay", "good"])
        has_negative_action = any(word in text.lower() for word in ["turns away", "looks away", "silence"])

        return has_positive_words and has_negative_action

    def _analyze_relationships(self, screenplay: str, characters: List[str],
                             interactions: List[InteractionMoment]) -> List[RelationshipDynamic]:
        """Analyze dynamics of each relationship."""
        relationships = []

        # Group interactions by character pair
        pair_interactions = defaultdict(list)
        for interaction in interactions:
            pair_interactions[interaction.characters].append(interaction)

        # Analyze each character pair
        for (char_a, char_b), pair_inters in pair_interactions.items():
            if len(pair_inters) < 2:
                continue  # Need multiple interactions for relationship

            # Determine relationship type
            rel_type = self._determine_relationship_type(screenplay, char_a, char_b)

            # Calculate chemistry score
            chemistry = self._calculate_chemistry(pair_inters)

            # Check for conflict
            has_conflict = any(i.interaction_type == "conflict" for i in pair_inters)

            # Check evolution
            has_evolution = self._check_relationship_evolution(pair_inters)

            # Determine power balance
            power = self._determine_power_balance(screenplay, char_a, char_b, pair_inters)

            # Calculate emotional depth
            depth = self._calculate_emotional_depth(pair_inters)

            # Determine stakes
            stakes = self._determine_stakes(screenplay, char_a, char_b)

            # Find obstacles
            obstacles = self._find_obstacles(screenplay, char_a, char_b)

            # Check vulnerability
            has_vulnerability = any(self._check_vulnerability_in_text(
                screenplay[i.page*55:(i.page+1)*55]) for i in pair_inters)

            # Check subtext
            has_subtext = any(i.has_subtext for i in pair_inters)

            # Determine resolution status
            resolution = self._determine_resolution_status(screenplay, char_a, char_b)

            relationships.append(RelationshipDynamic(
                character_a=char_a,
                character_b=char_b,
                relationship_type=rel_type,
                interaction_count=len(pair_inters),
                chemistry_score=chemistry,
                conflict_present=has_conflict,
                evolution_tracked=has_evolution,
                power_balance=power,
                emotional_depth=depth,
                stakes_level=stakes,
                obstacles=obstacles,
                vulnerability_shown=has_vulnerability,
                subtext_present=has_subtext,
                resolution_status=resolution
            ))

        return relationships

    def _determine_relationship_type(self, screenplay: str, char_a: str, char_b: str) -> str:
        """Determine the type of relationship between characters."""
        # Get all text where both characters appear
        lines = screenplay.split('\n')
        relevant_text = []

        for i in range(len(lines)):
            if char_a in lines[i] or char_b in lines[i]:
                # Get surrounding context
                start = max(0, i - 3)
                end = min(len(lines), i + 3)
                relevant_text.extend(lines[start:end])

        combined_text = ' '.join(relevant_text).lower()

        # Check relationship type markers
        for rel_type, markers in self.relationship_types.items():
            if any(marker in combined_text for marker in markers):
                return rel_type

        return "undefined"

    def _calculate_chemistry(self, interactions: List[InteractionMoment]) -> float:
        """Calculate chemistry score between characters."""
        if not interactions:
            return 0.0

        score = 0.0

        # Positive emotional tones add to chemistry
        positive_tones = ["loving", "joyful", "playful"]
        score += sum(0.1 for i in interactions if i.emotional_tone in positive_tones)

        # Intimate interactions add to chemistry
        score += sum(0.2 for i in interactions if i.interaction_type == "intimate")

        # Advancement adds to chemistry
        score += sum(0.05 for i in interactions if i.advances_relationship)

        # Subtext can indicate chemistry
        score += sum(0.05 for i in interactions if i.has_subtext)

        return min(1.0, score)

    def _check_relationship_evolution(self, interactions: List[InteractionMoment]) -> bool:
        """Check if relationship evolves over time."""
        if len(interactions) < 3:
            return False

        # Check if emotional tones change
        tones = [i.emotional_tone for i in interactions]
        unique_tones = len(set(tones))

        # Check if relationship advances
        advances = sum(1 for i in interactions if i.advances_relationship)

        return unique_tones > 1 and advances > 0

    def _determine_power_balance(self, screenplay: str, char_a: str, char_b: str,
                                interactions: List[InteractionMoment]) -> str:
        """Determine power balance in relationship."""
        # Simple heuristic based on who initiates more
        a_initiates = 0
        b_initiates = 0

        lines = screenplay.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == char_a:
                # Check if addressing char_b
                for j in range(i+1, min(i+5, len(lines))):
                    if char_b in lines[j]:
                        a_initiates += 1
                        break
            elif line.strip() == char_b:
                # Check if addressing char_a
                for j in range(i+1, min(i+5, len(lines))):
                    if char_a in lines[j]:
                        b_initiates += 1
                        break

        if a_initiates > b_initiates * 1.5:
            return "a_dominant"
        elif b_initiates > a_initiates * 1.5:
            return "b_dominant"
        elif len(interactions) > 5:
            return "shifting"
        else:
            return "equal"

    def _calculate_emotional_depth(self, interactions: List[InteractionMoment]) -> float:
        """Calculate emotional depth of relationship."""
        if not interactions:
            return 0.0

        depth = 0.3  # Base depth

        # Variety of emotional tones adds depth
        unique_tones = len(set(i.emotional_tone for i in interactions))
        depth += unique_tones * 0.1

        # Character revelation adds depth
        depth += sum(0.05 for i in interactions if i.reveals_character)

        # Subtext adds depth
        depth += sum(0.05 for i in interactions if i.has_subtext)

        return min(1.0, depth)

    def _determine_stakes(self, screenplay: str, char_a: str, char_b: str) -> str:
        """Determine stakes level of relationship."""
        # Look for high-stakes keywords near both characters
        lines = screenplay.split('\n')
        high_stakes_words = ["life", "death", "save", "lose", "everything", "never"]
        medium_stakes_words = ["important", "matter", "need", "must", "promise"]

        stakes_score = 0
        for i, line in enumerate(lines):
            if char_a in line or char_b in line:
                window = ' '.join(lines[max(0, i-2):min(len(lines), i+3)]).lower()
                if any(word in window for word in high_stakes_words):
                    stakes_score += 2
                elif any(word in window for word in medium_stakes_words):
                    stakes_score += 1

        if stakes_score > 10:
            return "high"
        elif stakes_score > 5:
            return "medium"
        else:
            return "low"

    def _find_obstacles(self, screenplay: str, char_a: str, char_b: str) -> List[str]:
        """Find obstacles to relationship."""
        obstacles = []
        text_lower = screenplay.lower()

        # Common obstacle patterns
        if "can't be together" in text_lower or "forbidden" in text_lower:
            obstacles.append("external prohibition")
        if "different worlds" in text_lower or "don't belong" in text_lower:
            obstacles.append("social differences")
        if "trust" in text_lower and "can't" in text_lower:
            obstacles.append("trust issues")
        if "secret" in text_lower or "truth" in text_lower:
            obstacles.append("secrets/lies")

        return obstacles[:3]  # Max 3 obstacles

    def _check_vulnerability_in_text(self, text: str) -> bool:
        """Check if text contains vulnerability."""
        text_lower = text.lower()
        return any(word in text_lower for word in self.vulnerability_words)

    def _determine_resolution_status(self, screenplay: str, char_a: str, char_b: str) -> str:
        """Determine if relationship is resolved."""
        lines = screenplay.split('\n')

        # Check last 20% of screenplay
        last_section_start = int(len(lines) * 0.8)
        last_section = ' '.join(lines[last_section_start:]).lower()

        # Look for resolution markers
        if (char_a.lower() in last_section and char_b.lower() in last_section):
            if any(word in last_section for word in ["together", "forgive", "love", "peace"]):
                return "resolved"
            elif any(word in last_section for word in ["goodbye", "leave", "over"]):
                return "resolved"

        return "unresolved"

    def _identify_central_relationship(self, relationships: List[RelationshipDynamic]) -> Optional[RelationshipDynamic]:
        """Identify the central relationship driving the story."""
        if not relationships:
            return None

        # Score each relationship
        scored = []
        for rel in relationships:
            score = 0
            score += rel.interaction_count * 2
            score += rel.chemistry_score * 10
            score += 5 if rel.conflict_present else 0
            score += 5 if rel.evolution_tracked else 0
            score += 10 if rel.stakes_level == "high" else 5 if rel.stakes_level == "medium" else 0
            score += rel.emotional_depth * 10

            scored.append((score, rel))

        # Return highest scoring relationship
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else None

    def _analyze_evolution(self, relationships: List[RelationshipDynamic],
                          interactions: List[InteractionMoment]) -> Dict[str, Any]:
        """Analyze relationship evolution."""
        evolving = sum(1 for r in relationships if r.evolution_tracked)
        static = len(relationships) - evolving

        return {
            "evolving_count": evolving,
            "static_count": static,
            "percentage_evolving": (evolving / max(len(relationships), 1)) * 100
        }

    def _analyze_relationship_conflicts(self, relationships: List[RelationshipDynamic]) -> Dict[str, Any]:
        """Analyze conflicts in relationships."""
        with_conflict = sum(1 for r in relationships if r.conflict_present)

        return {
            "with_conflict": with_conflict,
            "without_conflict": len(relationships) - with_conflict,
            "percentage": (with_conflict / max(len(relationships), 1)) * 100
        }

    def _analyze_chemistry(self, relationships: List[RelationshipDynamic]) -> Dict[str, Any]:
        """Analyze chemistry across relationships."""
        if not relationships:
            return {"average_score": 0, "high_chemistry_pairs": []}

        scores = [r.chemistry_score for r in relationships]
        avg = sum(scores) / len(scores)

        high_chemistry = [(r.character_a, r.character_b)
                         for r in relationships if r.chemistry_score > 0.7]

        return {
            "average_score": avg,
            "high_chemistry_pairs": high_chemistry
        }

    def _analyze_power_dynamics(self, relationships: List[RelationshipDynamic]) -> Dict[str, Any]:
        """Analyze power dynamics in relationships."""
        clear = sum(1 for r in relationships if r.power_balance != "undefined")
        shifting = sum(1 for r in relationships if r.power_balance == "shifting")

        return {
            "clear_dynamics": clear == len(relationships),
            "shifting_count": shifting,
            "static_count": len(relationships) - shifting
        }

    def _analyze_obstacles(self, relationships: List[RelationshipDynamic]) -> Dict[str, Any]:
        """Analyze obstacles in relationships."""
        with_obstacles = sum(1 for r in relationships if r.obstacles)

        all_obstacles = []
        for r in relationships:
            all_obstacles.extend(r.obstacles)

        unique_types = list(set(all_obstacles))

        return {
            "with_obstacles": with_obstacles,
            "types": unique_types[:5]  # Top 5 types
        }

    def _analyze_vulnerability(self, relationships: List[RelationshipDynamic],
                              interactions: List[InteractionMoment]) -> Dict[str, Any]:
        """Analyze vulnerability in relationships."""
        with_vulnerability = sum(1 for r in relationships if r.vulnerability_shown)

        vulnerable_moments = sum(1 for i in interactions
                               if i.reveals_character or i.emotional_tone in ["sad", "fearful"])

        return {
            "present": with_vulnerability > 0,
            "relationship_count": with_vulnerability,
            "moment_count": vulnerable_moments
        }

    def _analyze_subtext(self, interactions: List[InteractionMoment]) -> Dict[str, Any]:
        """Analyze subtext in interactions."""
        with_subtext = sum(1 for i in interactions if i.has_subtext)

        return {
            "count": with_subtext,
            "percentage": (with_subtext / max(len(interactions), 1)) * 100
        }

    def _analyze_relationship_variety(self, relationships: List[RelationshipDynamic]) -> Dict[str, Any]:
        """Analyze variety of relationship types."""
        types = [r.relationship_type for r in relationships]
        unique_types = list(set(types))

        variety_score = min(1.0, len(unique_types) * 0.2)

        return {
            "variety_score": variety_score,
            "types_present": unique_types,
            "type_count": len(unique_types)
        }

    def _analyze_resolutions(self, screenplay: str,
                            relationships: List[RelationshipDynamic]) -> Dict[str, Any]:
        """Analyze relationship resolutions."""
        resolved = sum(1 for r in relationships if r.resolution_status == "resolved")
        unresolved = sum(1 for r in relationships if r.resolution_status == "unresolved")

        return {
            "resolved_count": resolved,
            "unresolved_count": unresolved,
            "open_count": len(relationships) - resolved - unresolved
        }

    def _format_relationship_name(self, rel: Optional[RelationshipDynamic]) -> str:
        """Format relationship name for display."""
        if not rel:
            return "None"
        return f"{rel.character_a}-{rel.character_b}"

    def _get_key_interactions(self, interactions: List[InteractionMoment]) -> List[Dict]:
        """Get key interaction moments."""
        key_moments = []

        # Find most impactful interactions
        for i in interactions[:10]:  # Top 10
            if i.advances_relationship or i.reveals_character:
                key_moments.append({
                    "characters": f"{i.characters[0]}-{i.characters[1]}",
                    "page": i.page,
                    "type": i.interaction_type,
                    "impact": "advances" if i.advances_relationship else "reveals"
                })

        return key_moments[:5]  # Top 5

    def _check_relationship_rules(self, relationships: List[RelationshipDynamic],
                                 central: Optional[RelationshipDynamic],
                                 evolution: Dict, conflict: Dict,
                                 chemistry: Dict) -> List[Dict]:
        """Check relationships against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "REL.R001":
                # Defined relationships
                undefined = sum(1 for r in relationships if r.relationship_type == "undefined")
                if undefined > len(relationships) * 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{undefined} undefined relationships",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "REL.R002":
                # Relationship stakes
                low_stakes = sum(1 for r in relationships if r.stakes_level == "low")
                if low_stakes > len(relationships) * 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Most relationships have low stakes",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "REL.R003":
                # Dynamic evolution
                if evolution["percentage_evolving"] < 50:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Only {evolution['percentage_evolving']:.0f}% of relationships evolve",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "REL.R004":
                # Conflict in relationships
                if conflict["percentage"] < 30:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Too little conflict in relationships",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "REL.R006":
                # Chemistry present
                if chemistry["average_score"] < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Low chemistry between characters",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "REL.R012":
                # Central relationship clear
                if not central:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No clear central relationship",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_relationship_score(self, relationships: List[RelationshipDynamic],
                                     central: Optional[RelationshipDynamic],
                                     violations: List) -> float:
        """Calculate overall relationship score."""
        score = 100.0

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
        if central:
            score += 5

        # Bonus for high-quality relationships
        high_quality = sum(1 for r in relationships
                          if r.chemistry_score > 0.7 and r.emotional_depth > 0.7)
        score += min(high_quality * 2, 10)

        return max(0.0, min(100.0, score))

    def _generate_diagnosis(self, score: float, relationships: List[RelationshipDynamic],
                          central: Optional[RelationshipDynamic], violations: List) -> str:
        """Generate diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Strong, dynamic relationships driving the story"
        elif score >= 60:
            level = "GOOD"
            summary = "Solid relationships but could be deeper"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Relationship issues affecting engagement"
        else:
            level = "POOR"
            summary = "Major relationship problems throughout"

        diagnosis = f"RELATIONSHIPS {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if not central:
            issues.append("no central relationship")
        if len(relationships) < 3:
            issues.append("too few relationships")
        if all(not r.conflict_present for r in relationships):
            issues.append("no conflict")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _create_relationship_summaries(self, relationships: List[RelationshipDynamic]) -> List[Dict]:
        """Create summaries of all relationships."""
        summaries = []

        for rel in relationships:
            summaries.append({
                "characters": f"{rel.character_a}-{rel.character_b}",
                "type": rel.relationship_type,
                "interactions": rel.interaction_count,
                "chemistry": f"{rel.chemistry_score*100:.0f}%",
                "has_conflict": rel.conflict_present,
                "evolves": rel.evolution_tracked,
                "stakes": rel.stakes_level,
                "status": rel.resolution_status
            })

        return summaries

    def _generate_recommendations(self, score: float, violations: List,
                                 relationships: List[RelationshipDynamic],
                                 central: Optional[RelationshipDynamic]) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:  # Top 3 violations
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if not central:
            recommendations.append("Establish a clear central relationship to drive the story")

        static_rels = [r for r in relationships if not r.evolution_tracked]
        if static_rels:
            names = [f"{r.character_a}-{r.character_b}" for r in static_rels[:2]]
            recommendations.append(f"Add evolution to: {', '.join(names)}")

        low_chemistry = [r for r in relationships if r.chemistry_score < 0.3]
        if low_chemistry:
            recommendations.append("Build chemistry through specific character moments")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study relationship dynamics in acclaimed screenplays")

        return recommendations[:5]  # Return top 5