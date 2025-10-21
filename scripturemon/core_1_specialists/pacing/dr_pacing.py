"""
Script Doctor Pacingmon - Rhythm and Tempo Specialist
A Script Doctor™ in Digimon form specializing in screenplay pacing and rhythm.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class SceneMetrics:
    """Metrics for individual scene pacing."""
    scene_number: int
    page_start: int
    page_end: int
    length: float  # in pages
    tempo: str  # slow/medium/fast
    dialogue_ratio: float
    has_conflict: bool
    transition_type: str  # cut to/fade/dissolve/etc


class DrPacing:
    """
    Script Doctor Pacingmon - The Rhythm and Tempo Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing screenplay
    pacing, rhythm, tempo changes, and narrative flow.

    Identity: Script Doctor first, Digimon rhythm specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Pacingmon with rules and configuration."""
        self.name = "Script Doctor Pacingmon"
        self.digimon_name = "Pacingmon"
        self.title = "Script Doctor - Rhythm and Tempo Specialist"
        self.specialty = "Scene tempo, narrative flow, pacing dynamics"
        self.identity = "I am Script Doctor Pacingmon, a professional Script Doctor™ specializing in screenplay rhythm and pacing"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "pacing_rules.yaml"

        self.rules = self._load_rules()

        # Tempo word markers from rules (bilingual: EN + PT)
        self.tempo_markers = self.rules.get("pacing_metrics", {}).get("tempo_markers", {
            "slow": [
                # English
                "establishing", "contemplates", "waits", "silence", "slowly", "carefully",
                # Portuguese
                "estabelecendo", "contempla", "espera", "silêncio", "devagar", "cuidadosamente",
                "pausa", "observa", "reflete"
            ],
            "medium": [
                # English
                "walks", "talks", "drives", "discusses",
                # Portuguese
                "caminha", "fala", "dirige", "discute", "conversa", "anda"
            ],
            "fast": [
                # English
                "runs", "fights", "chases", "explodes", "crashes", "jumps", "attacks",
                # Portuguese
                "corre", "luta", "persegue", "explode", "bate", "pula", "ataca",
                "foge", "dispara", "arromba"
            ]
        })

    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file."""
        try:
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules from {self.rules_path}: {e}")
            return {"rules": [], "pacing_metrics": {}}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Perform complete pacing analysis of screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete pacing diagnostic report
        """
        lines = screenplay_text.split('\n')

        # Extract scenes
        scenes = self._extract_scenes(screenplay_text)

        # Calculate metrics
        page_count = len(lines) // 55 or 1
        dialogue_ratio = self._calculate_dialogue_ratio(screenplay_text)
        white_space_score = self._analyze_white_space(lines)

        # Analyze pacing dynamics
        pacing_curve = self._analyze_pacing_curve(scenes)
        tempo_distribution = self._analyze_tempo_distribution(scenes)

        # Check against rules
        rule_violations = self._check_pacing_rules(
            screenplay_text, scenes, page_count, dialogue_ratio, white_space_score
        )

        # Calculate score
        score = self._calculate_pacing_score(
            scenes, rule_violations, white_space_score, pacing_curve
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, scenes, pacing_curve, tempo_distribution, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "page_count": page_count,
            "scene_count": len(scenes),
            "average_scene_length": sum(s.length for s in scenes) / len(scenes) if scenes else 0,
            "dialogue_ratio": dialogue_ratio,
            "white_space_score": white_space_score,
            "pacing_curve": pacing_curve,
            "tempo_distribution": tempo_distribution,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(score, rule_violations, scenes),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _extract_scenes(self, screenplay: str) -> List[SceneMetrics]:
        """Extract and analyze individual scenes."""
        scenes = []
        lines = screenplay.split('\n')

        current_scene = None
        scene_number = 0
        current_page = 1
        line_count = 0

        scene_pattern = re.compile(r'^(INT\.|EXT\.|INT/EXT\.)', re.IGNORECASE)

        for i, line in enumerate(lines):
            # Track pages (55 lines per page)
            line_count += 1
            if line_count >= 55:
                current_page += 1
                line_count = 0

            # Detect scene headers
            if scene_pattern.match(line.strip()):
                # Save previous scene if exists
                if current_scene:
                    current_scene.page_end = current_page
                    current_scene.length = current_scene.page_end - current_scene.page_start
                    scenes.append(current_scene)

                # Start new scene
                scene_number += 1
                current_scene = SceneMetrics(
                    scene_number=scene_number,
                    page_start=current_page,
                    page_end=current_page,
                    length=0,
                    tempo="medium",
                    dialogue_ratio=0,
                    has_conflict=False,
                    transition_type="CUT TO:"
                )

                # Analyze scene content for tempo
                scene_text = self._get_scene_text(lines, i)
                current_scene.tempo = self._determine_tempo(scene_text)
                current_scene.dialogue_ratio = self._scene_dialogue_ratio(scene_text)
                current_scene.has_conflict = self._detect_conflict(scene_text)

        # Don't forget last scene
        if current_scene:
            current_scene.page_end = current_page
            current_scene.length = max(0.5, current_scene.page_end - current_scene.page_start)
            scenes.append(current_scene)

        return scenes

    def _get_scene_text(self, lines: List[str], start_idx: int) -> str:
        """Extract text for a single scene."""
        scene_text = []
        scene_pattern = re.compile(r'^(INT\.|EXT\.|INT/EXT\.)', re.IGNORECASE)

        for i in range(start_idx + 1, len(lines)):
            if scene_pattern.match(lines[i].strip()):
                break
            scene_text.append(lines[i])

        return '\n'.join(scene_text)

    def _determine_tempo(self, scene_text: str) -> str:
        """Determine scene tempo based on content."""
        text_lower = scene_text.lower()

        # Count tempo markers
        tempo_scores = {"slow": 0, "medium": 0, "fast": 0}

        for tempo, markers in self.tempo_markers.items():
            for marker in markers:
                tempo_scores[tempo] += text_lower.count(marker)

        # Return tempo with highest score
        if tempo_scores["fast"] > tempo_scores["medium"] and tempo_scores["fast"] > tempo_scores["slow"]:
            return "fast"
        elif tempo_scores["slow"] > tempo_scores["medium"]:
            return "slow"
        else:
            return "medium"

    def _scene_dialogue_ratio(self, scene_text: str) -> float:
        """Calculate dialogue ratio for a scene."""
        lines = scene_text.split('\n')
        dialogue_lines = 0
        total_lines = 0

        for line in lines:
            if line.strip():
                total_lines += 1
                # Simple heuristic: character names are in CAPS, dialogue follows
                if line.strip().isupper() and len(line.strip().split()) <= 3:
                    dialogue_lines += 1
                elif line.startswith('  '):  # Indented lines often dialogue
                    dialogue_lines += 1

        return dialogue_lines / total_lines if total_lines > 0 else 0

    def _detect_conflict(self, scene_text: str) -> bool:
        """Detect if scene contains conflict."""
        conflict_markers = [
            "argue", "fight", "disagree", "confronts", "challenges",
            "opposes", "refuses", "denies", "attacks", "threatens",
            "!", "?!", "no!", "never", "won't", "can't"
        ]

        text_lower = scene_text.lower()
        return any(marker in text_lower for marker in conflict_markers)

    def _calculate_dialogue_ratio(self, screenplay: str) -> float:
        """Calculate overall dialogue to action ratio."""
        lines = screenplay.split('\n')
        dialogue_lines = 0
        action_lines = 0

        for line in lines:
            if line.strip():
                if line.strip().isupper() and len(line.strip().split()) <= 3:
                    # Character name
                    dialogue_lines += 1
                elif line.startswith('  '):
                    # Dialogue (indented)
                    dialogue_lines += 1
                elif not line.strip().startswith('('):
                    # Action (not parenthetical)
                    action_lines += 1

        total = dialogue_lines + action_lines
        return dialogue_lines / total if total > 0 else 0.5

    def _analyze_white_space(self, lines: List[str]) -> float:
        """Analyze white space usage for readability."""
        blank_lines = sum(1 for line in lines if not line.strip())
        total_lines = len(lines)

        white_space_ratio = blank_lines / total_lines if total_lines > 0 else 0

        # Score: ideal is around 20-30% white space
        if 0.20 <= white_space_ratio <= 0.30:
            return 100
        elif 0.15 <= white_space_ratio <= 0.35:
            return 80
        elif 0.10 <= white_space_ratio <= 0.40:
            return 60
        else:
            return 40

    def _analyze_pacing_curve(self, scenes: List[SceneMetrics]) -> Dict[str, Any]:
        """Analyze the pacing curve throughout the screenplay."""
        if not scenes:
            return {"type": "flat", "score": 0}

        # Divide into acts (rough approximation)
        act1_scenes = scenes[:len(scenes)//4]
        act2_scenes = scenes[len(scenes)//4:3*len(scenes)//4]
        act3_scenes = scenes[3*len(scenes)//4:]

        # Calculate average tempo per act
        def avg_tempo_score(scene_list):
            if not scene_list:
                return 0
            scores = {"slow": 1, "medium": 2, "fast": 3}
            return sum(scores[s.tempo] for s in scene_list) / len(scene_list)

        act1_tempo = avg_tempo_score(act1_scenes)
        act2_tempo = avg_tempo_score(act2_scenes)
        act3_tempo = avg_tempo_score(act3_scenes)

        # Ideal curve: builds momentum
        if act1_tempo < act2_tempo < act3_tempo:
            return {"type": "escalating", "score": 100, "trajectory": [act1_tempo, act2_tempo, act3_tempo]}
        elif act3_tempo > act1_tempo:
            return {"type": "building", "score": 80, "trajectory": [act1_tempo, act2_tempo, act3_tempo]}
        elif act1_tempo == act2_tempo == act3_tempo:
            return {"type": "flat", "score": 40, "trajectory": [act1_tempo, act2_tempo, act3_tempo]}
        else:
            return {"type": "declining", "score": 20, "trajectory": [act1_tempo, act2_tempo, act3_tempo]}

    def _analyze_tempo_distribution(self, scenes: List[SceneMetrics]) -> Dict[str, int]:
        """Analyze distribution of scene tempos."""
        if not scenes:
            return {"slow": 0, "medium": 0, "fast": 0}

        tempo_count = Counter(s.tempo for s in scenes)
        return dict(tempo_count)

    def _check_pacing_rules(self, screenplay: str, scenes: List[SceneMetrics],
                           page_count: int, dialogue_ratio: float,
                           white_space_score: float) -> List[Dict[str, Any]]:
        """Check screenplay against pacing rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "PACE.R001":
                # Scene length balance
                if scenes:
                    avg_length = sum(s.length for s in scenes) / len(scenes)
                    if avg_length > 3 or avg_length < 1:
                        violations.append({
                            "rule_id": rule["id"],
                            "title": rule["title"],
                            "severity": rule["severity"],
                            "message": f"Average scene length: {avg_length:.1f} pages",
                            "fix": rule["fix"]
                        })

            elif rule["id"] == "PACE.R002":
                # Page per minute rule
                if page_count < 80 or page_count > 130:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Script is {page_count} pages",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R003":
                # Dialogue ratio
                if dialogue_ratio < 0.3 or dialogue_ratio > 0.7:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Dialogue ratio: {dialogue_ratio*100:.0f}%",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R004":
                # White space
                if white_space_score < 60:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Insufficient white space for readability",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_pacing_score(self, scenes: List[SceneMetrics], violations: List,
                               white_space_score: float, pacing_curve: Dict) -> float:
        """Calculate overall pacing score."""
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

        # Factor in white space
        score = score * 0.7 + white_space_score * 0.1

        # Factor in pacing curve
        score = score * 0.8 + pacing_curve.get("score", 50) * 0.2

        return max(5.0, min(95.0, round(score, 1)))

    def _generate_diagnosis(self, score: float, scenes: List[SceneMetrics],
                          pacing_curve: Dict, tempo_distribution: Dict,
                          violations: List) -> str:
        """Generate narrative pacing diagnosis."""
        diagnosis = f"Pacing Analysis Score: {score}/100\n\n"

        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent pacing! Your screenplay has professional rhythm with dynamic tempo changes. "
        elif score >= 70:
            diagnosis += "Good pacing foundation with some areas needing refinement. "
        elif score >= 50:
            diagnosis += "Pacing issues are impacting the screenplay's effectiveness. "
        else:
            diagnosis += "Significant pacing problems that will affect audience engagement. "

        # Pacing curve analysis
        curve_type = pacing_curve.get("type", "unknown")
        if curve_type == "escalating":
            diagnosis += "Perfect momentum building toward climax. "
        elif curve_type == "flat":
            diagnosis += "Pacing lacks variation - feels monotonous. "
        elif curve_type == "declining":
            diagnosis += "WARNING: Pacing decreases when it should accelerate. "

        # Scene length
        if scenes:
            avg_length = sum(s.length for s in scenes) / len(scenes)
            if avg_length > 3:
                diagnosis += f"Scenes too long (avg {avg_length:.1f} pages). "
            elif avg_length < 1:
                diagnosis += f"Scenes too short (avg {avg_length:.1f} pages). "

        # Critical issues
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical pacing issues: {', '.join([v['title'] for v in critical])}."

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 scenes: List[SceneMetrics]) -> List[str]:
        """Generate specific pacing recommendations."""
        recommendations = []

        # Top violations
        for violation in sorted(violations,
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 3:
                break

        # Scene-specific
        if scenes:
            long_scenes = [s for s in scenes if s.length > 4]
            if long_scenes:
                recommendations.append(f"Break up {len(long_scenes)} overly long scenes (4+ pages)")

            # Check tempo variety
            tempo_dist = Counter(s.tempo for s in scenes)
            if len(tempo_dist) == 1:
                recommendations.append("Add tempo variety - all scenes have same pace")

        # General advice
        if score < 70:
            recommendations.append("Study pacing in similar genre films")
            recommendations.append("Read screenplay aloud to feel rhythm")

        return recommendations[:5]  # Limit to 5 recommendations