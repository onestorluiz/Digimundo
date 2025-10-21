"""
Script Doctor Pacingmon - Pacing Analysis Specialist
A Script Doctor™ in Digimon form specializing in scene pacing, rhythm, tempo, escalation timing, and momentum.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class ScenePacing:
    """Pacing analysis for individual scene."""
    scene_number: int
    page_start: int
    page_end: int
    duration_pages: float
    tempo: str  # "fast", "medium", "slow"
    momentum_score: float  # 0-1
    beat_density: float  # beats per page
    issues: List[str]


@dataclass
class PacingProfile:
    """Overall pacing analysis."""
    total_scenes: int
    avg_scene_duration: float
    tempo_variety_score: float
    escalation_present: bool
    momentum_maintained: bool
    sagging_middle_detected: bool
    climax_acceleration: bool
    breathing_room_score: float
    pacing_consistency: float
    overall_tempo: str
    rhythm_pattern: str
    beat_timing_score: float
    acceleration_points: List[Dict]
    deceleration_points: List[Dict]


class DrPacing:
    """
    Script Doctor Pacingmon - The Pacing Analysis Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing scene pacing,
    rhythm, tempo, escalation timing, beat timing, and narrative momentum.

    Identity: Script Doctor first, Digimon pacing specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Pacingmon with rules and configuration."""
        self.name = "Script Doctor Pacingmon"
        self.digimon_name = "Pacingmon"
        self.title = "Script Doctor - Pacing Analysis Specialist"
        self.specialty = "Scene pacing, rhythm, tempo, escalation timing, beat timing, momentum"
        self.identity = "I am Script Doctor Pacingmon, a professional Script Doctor™ specializing in pacing and rhythm"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "pacing_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - PACING SPECIFIC
        self.deep_context_queries = [
            # McKee Story - Pacing foundations
            "McKee Story pacing rhythm storytelling beats per scene tempo control",
            "McKee Story scene pacing duration length timing beats optimal",
            "McKee Story tempo control acceleration deceleration dramatic rhythm variation",
            "McKee Story progressive complications pacing escalation building momentum intensity",
            "McKee Story climax pacing acceleration peak moment timing crescendo",
            "McKee Story act pacing rhythm tempo balance across structure",
            "McKee Story sequence pacing mini-climaxes building tension rhythm",

            # McKee Story - BEAT RHYTHM & TIMING (ultra-specific manual reading)
            "McKee Story beat rhythm action reaction tempo exchange pattern",
            "McKee Story scene duration optimal beats number pacing control",
            "McKee Story sequence rhythm moderate climax pacing 3-5 scenes build",
            "McKee Story climax placement 75-85 percent through story timing optimal",

            # Field Screenplay - Scene tempo
            "Field Screenplay scene pacing tempo length duration timing optimal",
            "Field Screenplay scene construction pacing rhythm escalation momentum",
            "Field Screenplay act pacing balance tempo rhythm 25-50-25 structure",
            "Field Screenplay plot point timing pacing beats structural rhythm",
            "Field Screenplay pacing problems diagnosis fixes tempo issues",
            "Field Screenplay opening pacing first 10 pages hook tempo fast",
            "Field Screenplay climax pacing final 30 pages acceleration speed increase",

            # Snyder Save Cat - Beat timing precision
            "Snyder Save Cat beat sheet timing pacing 15 beats precise rhythm",
            "Snyder Save Cat page count timing beats specific pages rhythm",
            "Snyder Save Cat opening pacing pages 1-10 hook fast tempo",
            "Snyder Save Cat catalyst timing page 12 pacing beat precise",
            "Snyder Save Cat midpoint timing page 55 pacing beat crucial",
            "Snyder Save Cat all is lost timing page 75 pacing emotional low",
            "Snyder Save Cat finale pacing pages 85-110 acceleration climax speed",
            "Snyder Save Cat fun and games pacing promise premise delivered entertainment",
            "Snyder Save Cat bad guys close in pacing complications escalate pressure",

            # Truby Anatomy - 22-step rhythm
            "Truby Anatomy 22 step pacing rhythm progression timing sequence",
            "Truby Anatomy scene timing duration pacing escalation momentum building",
            "Truby Anatomy revelation sequence pacing progressive discovery timing",
            "Truby Anatomy battle pacing climax tempo acceleration peak moment",
            "Truby Anatomy opponent pacing complications obstacles timing escalation",

            # Vogler Writer's Journey - Mythic tempo
            "Vogler Writer's Journey 12 stages pacing rhythm mythic tempo",
            "Vogler Journey ordinary world pacing tempo establish rhythm opening",
            "Vogler Journey crossing threshold pacing timing momentum shift Act 2",
            "Vogler Journey tests allies enemies pacing tempo learning rhythm middle",
            "Vogler Journey ordeal pacing midpoint tempo crisis peak intensity",
            "Vogler Journey resurrection pacing finale tempo climax acceleration final",
            "Vogler Journey return pacing resolution tempo denouement closing rhythm",

            # Campbell Hero 1000 Faces - Mythic cycles
            "Campbell Hero 1000 Faces mythic rhythm pacing cycles tempo stages",
            "Campbell Hero monomyth timing rhythm pace 17 stages progression",
            "Campbell Hero departure pacing timing call refusal threshold tempo",
            "Campbell Hero initiation pacing rhythm trials ordeals tests tempo",
            "Campbell Hero return pacing timing resolution denouement closing rhythm",

            # Aristotle Poetics - Magnitude and tempo
            "Aristotle Poetics proper magnitude length pacing optimal duration timing",
            "Aristotle Poetics tempo unfolding action pacing unity time rhythm",
            "Aristotle Poetics complication unraveling pacing rhythm tying untying tempo",
            "Aristotle Poetics rising action pacing escalation build crisis climax",
            "Aristotle Poetics reversal recognition pacing timing peripeteia anagnorisis",

            # Seger Making Good Script Great - Pacing problems
            "Seger Making Good Script Great pacing chapters scene timing rhythm",
            "Seger restructuring pacing problems sagging middle momentum fixes",
            "Seger catalyst pacing timing inciting incident rhythm launch",
            "Seger turning points pacing timing beats reversals rhythm",
            "Seger act pacing tempo rhythm balance structure timing",
            "Seger climax pacing finale acceleration tempo speed increase",
            "Seger subplot pacing integration timing parallel stories rhythm",

            # Egri Art Dramatic Writing - Rising rhythm
            "Egri Art Dramatic Writing tempo orchestration rhythm pacing balance",
            "Egri Art rising conflict escalation pacing acceleration timing crisis",
            "Egri Art transition pacing timing scene connection flow rhythm",
            "Egri Art point of attack pacing where begin timing choice",
            "Egri Art crisis to crisis pacing escalation rhythm building tension",

            # Weiland Creating Character Arcs - Arc pacing
            "Weiland Creating Character Arcs pacing mirrors arc timing progression",
            "Weiland arc beat pacing timing lie truth journey rhythm",
            "Weiland midpoint pacing timing truth glimpse character shift tempo",
            "Weiland dark night soul pacing timing low point crisis rhythm",

            # Goldman/Rhimes/Mamet/Mackendrick - Practical pacing
            "Goldman Adventures Screen Trade pacing advice rhythm tempo craft",
            "Goldman pacing cutting tightening tempo faster rhythm lean",
            "Rhimes Year of Yes pacing storytelling rhythm television tempo commercial",
            "Rhimes TV act pacing tempo commercial breaks episodic rhythm",
            "Mamet Three Uses Knife rhythm tempo dramatic pacing beats",
            "Mamet scene pacing beats action want obstacle rhythm negotiation",
            "Mackendrick On Film-Making pacing control tempo rhythm visual timing",
            "Mackendrick montage pacing compression time passage rhythm editing tempo",

            # General pacing concepts
            "scene pacing acceleration deceleration techniques tempo control variation",
            "rhythm tempo narrative structure beat timing pattern pulse",
            "escalation timing momentum building progressive complications intensity increase",
            "beat timing scene duration optimal length pacing rhythm balance",
            "pacing consistency across acts tempo variation rhythm control",
            "sagging middle pacing issues Act 2 momentum maintain fixes",
            "climax pacing acceleration final act speed increase tempo fast",
            "opening pacing hook timing first 10 pages grab attention fast",
            "dialogue pacing speech rhythm conversation tempo natural flow",
            "action sequence pacing tempo speed rhythm choreography timing",
            "quiet moment pacing breathing room deceleration rest beats pause",
            "montage pacing compression time passage rhythm editing tempo cuts",
            "page count rhythm pacing 1 page 1 minute tempo target",
            "tension release pacing rhythm peaks valleys breathing pattern",
            "exposition pacing timing information revelation rhythm drip feed"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story rhythm swing between tension relaxation day life analogy",
        "McKee Story tempo level activity dialogue action cueing pattern",
        "McKee Story scene length average two three minutes avoid stuck record",
        "McKee Story accelerate rhythm shorten scenes then pause before climax",
        "McKee Story periodic sentence suspense last word cue actor reaction",

        ]

        # Pacing analysis patterns (bilingual: EN + PT)

        # General pacing markers
        self.pacing_markers = [
            # English - fast
            "fast-paced", "quick", "rapid", "swift", "hurried", "rushing",
            "breakneck", "frantic", "accelerates", "speeds up",
            # English - slow
            "slow", "gradual", "deliberate", "measured", "unhurried",
            "languid", "leisurely", "decelerates", "slows down",
            # English - rhythm
            "tempo", "rhythm", "momentum", "pace", "cadence", "beat",
            # Portuguese - fast
            "ritmo rápido", "rápido", "veloz", "acelerado", "apressado",
            "frenético", "acelera", "apressa",
            # Portuguese - slow
            "lento", "gradual", "deliberado", "medido", "calmo",
            "desacelera", "arrasta", "demora",
            # Portuguese - rhythm
            "ritmo", "cadência", "impulso", "batida", "tempo"
        ]

        # Acceleration markers
        self.acceleration_markers = [
            # English
            "speeds up", "accelerates", "quickens", "picks up pace",
            "gains momentum", "intensifies", "ramps up", "builds speed",
            "faster", "rapid-fire", "escalates quickly", "rushes forward",
            # Portuguese
            "acelera", "apressa", "intensifica", "ganha ritmo",
            "aumenta velocidade", "mais rápido", "dispara", "avança rápido"
        ]

        # Deceleration markers
        self.deceleration_markers = [
            # English
            "slows down", "decelerates", "drags", "lingers", "dwells",
            "loses momentum", "stalls", "grinds to halt", "crawls",
            "slower", "drawn out", "stretched", "prolonged",
            # Portuguese
            "desacelera", "arrasta", "demora", "perde ritmo",
            "para", "estanca", "mais lento", "prolongado", "esticado"
        ]

        # Rhythm markers
        self.rhythm_markers = [
            # English
            "rhythm", "beat", "pulse", "cadence", "pattern",
            "tempo", "meter", "syncopation", "flow", "pacing",
            "rhythmic", "measured", "steady", "regular", "irregular",
            # Portuguese
            "ritmo", "batida", "pulso", "cadência", "padrão",
            "compasso", "fluxo", "rítmico", "regular", "irregular"
        ]

        # Momentum markers
        self.momentum_markers = [
            # English
            "momentum", "drive", "energy", "propulsion", "force",
            "thrust", "push", "pull", "inertia", "velocity",
            "forward movement", "narrative drive", "unstoppable",
            # Portuguese
            "momentum", "impulso", "energia", "propulsão", "força",
            "empurrão", "movimento", "velocidade", "imparável"
        ]

        # Escalation markers
        self.escalation_markers = [
            # English
            "escalates", "builds", "intensifies", "grows", "increases",
            "mounts", "rises", "climbs", "heightens", "amplifies",
            "ratchets up", "raises stakes", "ups the ante",
            # Portuguese
            "aumenta", "constrói", "intensifica", "cresce", "eleva",
            "sobe", "amplifica", "levanta aposta", "aumenta tensão"
        ]

        # Timing markers
        self.timing_markers = [
            # English
            "timing", "duration", "length", "brevity", "brief",
            "long", "short", "extended", "compressed", "timed",
            "well-timed", "perfectly timed", "mistimed", "dragged out",
            # Portuguese
            "timing", "duração", "comprimento", "brevidade", "breve",
            "longo", "curto", "estendido", "comprimido", "cronometrado"
        ]

        # Scene duration indicators
        self.duration_indicators = {
            "very_short": ["quick cut", "flash", "glimpse", "instant", "moment"],
            "short": ["brief", "short", "compact", "tight"],
            "medium": ["standard", "regular", "normal"],
            "long": ["extended", "lengthy", "drawn-out", "prolonged"],
            "very_long": ["very long", "marathon", "epic", "exhaustive"]
        }

        # Beat timing indicators
        self.beat_timing_indicators = [
            # English
            "beat", "pause", "moment", "breath", "rest",
            "silence", "stillness", "lull", "interval", "gap",
            # Portuguese
            "batida", "pausa", "momento", "respiro", "descanso",
            "silêncio", "quietude", "intervalo", "lacuna"
        ]

        # Breathing room markers
        self.breathing_room_markers = [
            # English
            "breathing room", "quiet moment", "pause", "rest",
            "calm", "stillness", "reflection", "contemplation",
            "downtime", "respite", "breather", "lull",
            # Portuguese
            "respiro", "momento calmo", "pausa", "descanso",
            "calma", "quietude", "reflexão", "contemplação", "trégua"
        ]

        # Sagging middle markers
        self.sagging_markers = [
            # English
            "drags", "loses momentum", "stalls", "sags", "slows",
            "meandering", "aimless", "unfocused", "wandering",
            "boring", "dull", "tedious", "repetitive",
            # Portuguese
            "arrasta", "perde ritmo", "para", "desacelera",
            "sem rumo", "sem foco", "entediante", "monótono", "repetitivo"
        ]

        # Climax acceleration markers
        self.climax_acceleration_markers = [
            # English
            "racing toward", "building to climax", "accelerating",
            "mounting tension", "rapid succession", "breakneck finale",
            "explosive conclusion", "racing finale", "sprint to end",
            # Portuguese
            "correndo para", "construindo clímax", "acelerando",
            "tensão crescente", "sucessão rápida", "final explosivo"
        ]

        # Opening hook pacing markers
        self.opening_pacing_markers = [
            # English
            "grabs immediately", "instant hook", "cold open",
            "starts fast", "explosive opening", "immediate action",
            "in medias res", "hits the ground running",
            # Portuguese
            "gancho imediato", "começo explosivo", "ação imediata",
            "em plena ação", "começa rápido", "já correndo"
        ]

        # Dialogue pacing markers
        self.dialogue_pacing_markers = [
            # English
            "rapid-fire dialogue", "quick exchanges", "snappy",
            "slow conversation", "deliberate speech", "measured words",
            "overlapping dialogue", "interruptions", "clipped",
            # Portuguese
            "diálogo rápido", "trocas rápidas", "conversa lenta",
            "fala medida", "diálogo sobreposto", "interrupções"
        ]

        # Action sequence pacing markers
        self.action_pacing_markers = [
            # English
            "fast action", "frenetic", "choreographed", "intense",
            "rapid cuts", "quick succession", "relentless",
            "breakneck action", "nonstop", "continuous",
            # Portuguese
            "ação rápida", "frenético", "intenso", "cortes rápidos",
            "sucessão rápida", "implacável", "sem parar", "contínuo"
        ]

        # Tempo types
        self.tempo_types = {
            "allegro": ["fast", "quick", "rapid", "brisk", "swift"],
            "moderato": ["moderate", "medium", "steady", "balanced"],
            "adagio": ["slow", "deliberate", "measured", "careful"],
            "accelerando": ["speeding up", "accelerating", "quickening"],
            "ritardando": ["slowing down", "decelerating", "dragging"]
        }

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze pacing and rhythm in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete pacing diagnostic report
        """
        # Extract page count and scenes
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)

        # Analyze individual scene pacing
        scene_pacing_list = self._analyze_scene_durations(scenes)

        # Analyze beat timing
        beat_timing = self._analyze_beat_timing(screenplay_text, scenes)

        # Detect acceleration points
        acceleration_points = self._detect_acceleration(screenplay_text)

        # Detect deceleration points
        deceleration_points = self._detect_deceleration(screenplay_text)

        # Track momentum across acts
        momentum_tracking = self._track_momentum(screenplay_text, page_count)

        # Analyze escalation
        escalation_analysis = self._analyze_escalation(screenplay_text)

        # Detect rhythm patterns
        rhythm_patterns = self._detect_rhythm_patterns(scene_pacing_list)

        # Check for sagging middle
        sagging_middle = self._detect_sagging_middle(screenplay_text, page_count, momentum_tracking)

        # Verify climax acceleration
        climax_acceleration = self._verify_climax_acceleration(screenplay_text, page_count)

        # Analyze opening hook pacing
        opening_pacing = self._analyze_opening_pacing(screenplay_text)

        # Check breathing room
        breathing_room = self._analyze_breathing_room(screenplay_text, scene_pacing_list)

        # Analyze scene variety
        scene_variety = self._analyze_scene_variety(scene_pacing_list)

        # Calculate tempo consistency
        tempo_consistency = self._calculate_tempo_consistency(scene_pacing_list)

        # Pacing by act
        pacing_by_act = self._analyze_pacing_by_act(screenplay_text, page_count, scenes)

        # Overall tempo assessment
        overall_tempo = self._assess_overall_tempo(scene_pacing_list, rhythm_patterns)

        # Build pacing profile
        pacing_profile = PacingProfile(
            total_scenes=len(scenes),
            avg_scene_duration=sum(s.duration_pages for s in scene_pacing_list) / max(len(scene_pacing_list), 1),
            tempo_variety_score=scene_variety["variety_score"],
            escalation_present=escalation_analysis["present"],
            momentum_maintained=momentum_tracking["maintained"],
            sagging_middle_detected=sagging_middle["detected"],
            climax_acceleration=climax_acceleration["present"],
            breathing_room_score=breathing_room["score"],
            pacing_consistency=tempo_consistency,
            overall_tempo=overall_tempo,
            rhythm_pattern=rhythm_patterns["pattern_type"],
            beat_timing_score=beat_timing["timing_score"],
            acceleration_points=acceleration_points,
            deceleration_points=deceleration_points
        )

        # Check against rules
        rule_violations = self._check_pacing_rules(
            pacing_profile, sagging_middle, climax_acceleration,
            opening_pacing, breathing_room, escalation_analysis
        )

        # Calculate score
        score = self._calculate_pacing_score(
            pacing_profile, tempo_consistency, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, pacing_profile, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "total_pages": page_count,
            "total_scenes": len(scenes),
            "average_scene_duration": pacing_profile.avg_scene_duration,
            "overall_tempo": overall_tempo,
            "pacing_consistency": tempo_consistency,
            "rhythm_pattern": rhythm_patterns["pattern_type"],
            "tempo_variety": {
                "score": scene_variety["variety_score"],
                "fast_scenes": scene_variety["fast_count"],
                "medium_scenes": scene_variety["medium_count"],
                "slow_scenes": scene_variety["slow_count"]
            },
            "escalation": {
                "present": escalation_analysis["present"],
                "escalation_count": escalation_analysis["count"],
                "examples": escalation_analysis["examples"][:3]
            },
            "momentum": {
                "maintained": momentum_tracking["maintained"],
                "act1_momentum": momentum_tracking["act1_score"],
                "act2_momentum": momentum_tracking["act2_score"],
                "act3_momentum": momentum_tracking["act3_score"]
            },
            "sagging_middle": {
                "detected": sagging_middle["detected"],
                "severity": sagging_middle.get("severity", "none"),
                "description": sagging_middle.get("description", "")
            },
            "climax_acceleration": {
                "present": climax_acceleration["present"],
                "acceleration_detected": climax_acceleration.get("detected", False),
                "description": climax_acceleration.get("description", "")
            },
            "opening_pacing": {
                "appropriate": opening_pacing["appropriate"],
                "tempo": opening_pacing["tempo"],
                "hook_strength": opening_pacing.get("hook_strength", "medium")
            },
            "breathing_room": {
                "score": breathing_room["score"],
                "quiet_moments_count": breathing_room["count"],
                "sufficient": breathing_room["sufficient"]
            },
            "beat_timing": {
                "score": beat_timing["timing_score"],
                "avg_beats_per_page": beat_timing["avg_beats_per_page"],
                "consistency": beat_timing["consistency"]
            },
            "acceleration_points": {
                "count": len(acceleration_points),
                "examples": acceleration_points[:3]
            },
            "deceleration_points": {
                "count": len(deceleration_points),
                "examples": deceleration_points[:3]
            },
            "pacing_by_act": pacing_by_act,
            "scene_pacing_examples": [
                {
                    "scene": s.scene_number,
                    "pages": f"{s.page_start}-{s.page_end}",
                    "duration": s.duration_pages,
                    "tempo": s.tempo,
                    "momentum": s.momentum_score
                }
                for s in scene_pacing_list[:5]
            ],
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, pacing_profile, sagging_middle
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _estimate_page_count(self, screenplay: str) -> int:
        """Estimate page count from screenplay text."""
        lines = screenplay.split('\n')
        return max(1, len(lines) // 55)

    def _extract_scenes(self, screenplay: str) -> List[Dict]:
        """Extract all scenes from screenplay."""
        scenes = []
        lines = screenplay.split('\n')
        current_scene = None
        scene_number = 0

        for i, line in enumerate(lines):
            # Detect scene heading
            if re.match(r'^(INT\.|EXT\.)', line.strip()):
                # Save previous scene
                if current_scene:
                    current_scene['end_line'] = i - 1
                    current_scene['end_page'] = (i - 1) // 55
                    scenes.append(current_scene)

                # Start new scene
                scene_number += 1
                current_scene = {
                    'number': scene_number,
                    'heading': line.strip(),
                    'start_line': i,
                    'start_page': i // 55,
                    'content': []
                }
            elif current_scene:
                current_scene['content'].append(line)

        # Add last scene
        if current_scene:
            current_scene['end_line'] = len(lines) - 1
            current_scene['end_page'] = (len(lines) - 1) // 55
            scenes.append(current_scene)

        return scenes

    def _analyze_scene_durations(self, scenes: List[Dict]) -> List[ScenePacing]:
        """Analyze pacing for each individual scene."""
        scene_pacing_list = []

        for scene in scenes:
            duration = scene['end_page'] - scene['start_page']
            if duration < 0:
                duration = 0.5  # Minimum

            # Determine tempo based on duration
            if duration < 1:
                tempo = "fast"
            elif duration < 2.5:
                tempo = "medium"
            else:
                tempo = "slow"

            # Calculate momentum score (inversely related to duration for now)
            momentum_score = max(0.0, min(1.0, 1.0 - (duration / 5.0)))

            # Calculate beat density (rough estimate)
            content = '\n'.join(scene['content'])
            beats = sum(1 for marker in self.beat_timing_indicators if marker in content.lower())
            beat_density = beats / max(duration, 0.5)

            # Identify issues
            issues = []
            if duration > 5:
                issues.append("Scene too long - may drag")
            if duration < 0.3:
                issues.append("Scene too short - may feel rushed")
            if beat_density > 5:
                issues.append("Too many beats - overwhelming")
            if beat_density < 0.5 and duration > 2:
                issues.append("Too few beats - may feel flat")

            scene_pacing_list.append(ScenePacing(
                scene_number=scene['number'],
                page_start=scene['start_page'],
                page_end=scene['end_page'],
                duration_pages=duration,
                tempo=tempo,
                momentum_score=momentum_score,
                beat_density=beat_density,
                issues=issues
            ))

        return scene_pacing_list

    def _analyze_beat_timing(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """Analyze frequency and distribution of beats."""
        total_beats = 0
        beat_positions = []
        lines = screenplay.split('\n')

        for i, line in enumerate(lines):
            for marker in self.beat_timing_indicators:
                if marker in line.lower():
                    total_beats += 1
                    beat_positions.append(i // 55)  # Page number
                    break

        page_count = len(lines) // 55
        avg_beats_per_page = total_beats / max(page_count, 1)

        # Calculate consistency (variance in beat spacing)
        if len(beat_positions) > 1:
            spacings = [beat_positions[i+1] - beat_positions[i] for i in range(len(beat_positions) - 1)]
            mean_spacing = sum(spacings) / len(spacings)
            variance = sum((x - mean_spacing) ** 2 for x in spacings) / len(spacings)
            consistency = max(0.0, 1.0 - (variance / 10.0))
        else:
            consistency = 0.5

        # Timing score based on average and consistency
        if 1.0 <= avg_beats_per_page <= 3.0:
            beat_score = 0.8 + (consistency * 0.2)
        else:
            beat_score = 0.5 + (consistency * 0.2)

        return {
            "timing_score": beat_score,
            "total_beats": total_beats,
            "avg_beats_per_page": avg_beats_per_page,
            "consistency": consistency,
            "beat_positions": beat_positions[:10]
        }

    def _detect_acceleration(self, screenplay: str) -> List[Dict]:
        """Find moments of pacing acceleration."""
        acceleration_points = []
        lines = screenplay.split('\n')

        for i, line in enumerate(lines):
            for marker in self.acceleration_markers:
                if marker in line.lower():
                    acceleration_points.append({
                        "page": i // 55,
                        "description": line.strip()[:80] + "..." if len(line.strip()) > 80 else line.strip(),
                        "marker": marker
                    })
                    break

        return acceleration_points

    def _detect_deceleration(self, screenplay: str) -> List[Dict]:
        """Find moments of pacing deceleration."""
        deceleration_points = []
        lines = screenplay.split('\n')

        for i, line in enumerate(lines):
            for marker in self.deceleration_markers:
                if marker in line.lower():
                    deceleration_points.append({
                        "page": i // 55,
                        "description": line.strip()[:80] + "..." if len(line.strip()) > 80 else line.strip(),
                        "marker": marker
                    })
                    break

        return deceleration_points

    def _track_momentum(self, screenplay: str, page_count: int) -> Dict[str, Any]:
        """Track narrative momentum across acts."""
        lines = screenplay.split('\n')

        # Divide into acts (25/50/25)
        act1_end = int(len(lines) * 0.25)
        act2_end = int(len(lines) * 0.75)

        act1_text = '\n'.join(lines[:act1_end])
        act2_text = '\n'.join(lines[act1_end:act2_end])
        act3_text = '\n'.join(lines[act2_end:])

        # Calculate momentum for each act
        def calc_momentum(text):
            momentum_count = sum(1 for marker in self.momentum_markers if marker in text.lower())
            text_length = max(len(text), 1)
            return min(1.0, momentum_count / (text_length / 1000))

        act1_score = calc_momentum(act1_text)
        act2_score = calc_momentum(act2_text)
        act3_score = calc_momentum(act3_text)

        # Momentum is maintained if it doesn't drop significantly in Act 2
        maintained = act2_score >= (act1_score * 0.6)

        return {
            "maintained": maintained,
            "act1_score": act1_score,
            "act2_score": act2_score,
            "act3_score": act3_score,
            "overall_trend": "increasing" if act3_score > act1_score else "decreasing"
        }

    def _analyze_escalation(self, screenplay: str) -> Dict[str, Any]:
        """Verify progressive escalation."""
        escalation_count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.escalation_markers:
                if marker in line.lower():
                    escalation_count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:80] + "..." if len(line.strip()) > 80 else line.strip())
                    break

        return {
            "present": escalation_count > 0,
            "count": escalation_count,
            "examples": examples
        }

    def _detect_rhythm_patterns(self, scene_pacing_list: List[ScenePacing]) -> Dict[str, Any]:
        """Identify pacing rhythm patterns."""
        if not scene_pacing_list:
            return {"pattern_type": "none", "description": "No scenes detected"}

        # Analyze tempo sequence
        tempo_sequence = [s.tempo for s in scene_pacing_list]

        # Check for alternating pattern
        alternating = 0
        for i in range(len(tempo_sequence) - 1):
            if tempo_sequence[i] != tempo_sequence[i+1]:
                alternating += 1

        alternating_ratio = alternating / max(len(tempo_sequence) - 1, 1)

        if alternating_ratio > 0.7:
            pattern_type = "alternating"
            description = "Scene tempos alternate frequently"
        elif alternating_ratio < 0.3:
            pattern_type = "consistent"
            description = "Scene tempos remain relatively consistent"
        else:
            pattern_type = "mixed"
            description = "Mix of consistent and varying tempos"

        return {
            "pattern_type": pattern_type,
            "description": description,
            "alternating_ratio": alternating_ratio,
            "tempo_sequence": tempo_sequence[:10]
        }

    def _detect_sagging_middle(self, screenplay: str, page_count: int, momentum_tracking: Dict) -> Dict[str, Any]:
        """Check Act 2 for momentum loss (sagging middle)."""
        lines = screenplay.split('\n')

        # Act 2 is roughly middle 50%
        act2_start = int(len(lines) * 0.25)
        act2_end = int(len(lines) * 0.75)
        act2_text = '\n'.join(lines[act2_start:act2_end])

        # Count sagging markers
        sagging_count = sum(1 for marker in self.sagging_markers if marker in act2_text.lower())

        # Check momentum score
        act2_momentum = momentum_tracking["act2_score"]

        # Determine if sagging
        detected = (sagging_count > 2) or (act2_momentum < 0.3)

        if detected:
            if sagging_count > 5:
                severity = "high"
            elif sagging_count > 2:
                severity = "medium"
            else:
                severity = "low"

            description = f"Act 2 shows {sagging_count} sagging markers and momentum score of {act2_momentum:.2f}"
        else:
            severity = "none"
            description = "Act 2 maintains good momentum"

        return {
            "detected": detected,
            "severity": severity,
            "description": description,
            "sagging_markers_count": sagging_count,
            "act2_momentum": act2_momentum
        }

    def _verify_climax_acceleration(self, screenplay: str, page_count: int) -> Dict[str, Any]:
        """Verify final act accelerates into climax."""
        lines = screenplay.split('\n')

        # Final 25% should accelerate
        act3_start = int(len(lines) * 0.75)
        act3_text = '\n'.join(lines[act3_start:])

        # Count acceleration markers in Act 3
        acceleration_count = sum(1 for marker in self.climax_acceleration_markers if marker in act3_text.lower())
        general_acceleration = sum(1 for marker in self.acceleration_markers if marker in act3_text.lower())

        total_acceleration = acceleration_count + general_acceleration

        detected = total_acceleration >= 2

        if detected:
            description = f"Final act shows {total_acceleration} acceleration indicators"
        else:
            description = "Final act lacks clear acceleration into climax"

        return {
            "present": detected,
            "detected": detected,
            "acceleration_count": total_acceleration,
            "description": description
        }

    def _analyze_opening_pacing(self, screenplay: str) -> Dict[str, Any]:
        """Analyze pacing of first 10 pages."""
        lines = screenplay.split('\n')
        first_ten_pages = lines[:550]  # Roughly 10 pages
        opening_text = '\n'.join(first_ten_pages)

        # Check for fast opening
        fast_markers = sum(1 for marker in self.opening_pacing_markers if marker in opening_text.lower())

        # Check for action
        action_markers = sum(1 for marker in self.action_pacing_markers if marker in opening_text.lower())

        total_markers = fast_markers + action_markers

        if total_markers >= 3:
            tempo = "fast"
            hook_strength = "strong"
            appropriate = True
        elif total_markers >= 1:
            tempo = "medium"
            hook_strength = "medium"
            appropriate = True
        else:
            tempo = "slow"
            hook_strength = "weak"
            appropriate = False

        return {
            "appropriate": appropriate,
            "tempo": tempo,
            "hook_strength": hook_strength,
            "opening_markers": total_markers
        }

    def _analyze_breathing_room(self, screenplay: str, scene_pacing_list: List[ScenePacing]) -> Dict[str, Any]:
        """Check for quiet moments and breathing room."""
        # Count breathing room markers
        breathing_count = sum(1 for marker in self.breathing_room_markers if marker in screenplay.lower())

        # Count slow scenes
        slow_scenes = sum(1 for s in scene_pacing_list if s.tempo == "slow")

        total_quiet = breathing_count + slow_scenes
        total_scenes = len(scene_pacing_list)

        # Ideal: 15-25% quiet moments
        quiet_ratio = total_quiet / max(total_scenes, 1)

        if 0.15 <= quiet_ratio <= 0.25:
            score = 1.0
            sufficient = True
        elif 0.10 <= quiet_ratio <= 0.30:
            score = 0.7
            sufficient = True
        else:
            score = 0.4
            sufficient = False

        return {
            "score": score,
            "count": total_quiet,
            "sufficient": sufficient,
            "quiet_ratio": quiet_ratio
        }

    def _analyze_scene_variety(self, scene_pacing_list: List[ScenePacing]) -> Dict[str, Any]:
        """Analyze variety in scene durations."""
        if not scene_pacing_list:
            return {
                "variety_score": 0.0,
                "fast_count": 0,
                "medium_count": 0,
                "slow_count": 0
            }

        # Count tempo types
        fast_count = sum(1 for s in scene_pacing_list if s.tempo == "fast")
        medium_count = sum(1 for s in scene_pacing_list if s.tempo == "medium")
        slow_count = sum(1 for s in scene_pacing_list if s.tempo == "slow")

        total = len(scene_pacing_list)

        # Calculate variety score (higher when tempos are balanced)
        fast_ratio = fast_count / total
        medium_ratio = medium_count / total
        slow_ratio = slow_count / total

        # Ideal distribution: some of each (not all same)
        # Use entropy-like measure
        ratios = [fast_ratio, medium_ratio, slow_ratio]
        non_zero_ratios = [r for r in ratios if r > 0]

        if len(non_zero_ratios) >= 3:
            variety_score = 1.0
        elif len(non_zero_ratios) == 2:
            variety_score = 0.7
        else:
            variety_score = 0.3

        return {
            "variety_score": variety_score,
            "fast_count": fast_count,
            "medium_count": medium_count,
            "slow_count": slow_count
        }

    def _calculate_tempo_consistency(self, scene_pacing_list: List[ScenePacing]) -> float:
        """Calculate overall tempo consistency."""
        if not scene_pacing_list:
            return 0.5

        # Calculate variance in scene durations
        durations = [s.duration_pages for s in scene_pacing_list]
        mean_duration = sum(durations) / len(durations)
        variance = sum((d - mean_duration) ** 2 for d in durations) / len(durations)

        # Lower variance = more consistent
        # Normalize to 0-1 scale
        consistency = max(0.0, min(1.0, 1.0 - (variance / 5.0)))

        return consistency

    def _analyze_pacing_by_act(self, screenplay: str, page_count: int, scenes: List[Dict]) -> Dict[str, Any]:
        """Analyze pacing separately for each act."""
        lines = screenplay.split('\n')

        # Divide into acts
        act1_end_line = int(len(lines) * 0.25)
        act2_end_line = int(len(lines) * 0.75)

        # Categorize scenes by act
        act1_scenes = [s for s in scenes if s['end_line'] <= act1_end_line]
        act2_scenes = [s for s in scenes if act1_end_line < s['end_line'] <= act2_end_line]
        act3_scenes = [s for s in scenes if s['end_line'] > act2_end_line]

        def analyze_act_scenes(act_scenes):
            if not act_scenes:
                return {"scene_count": 0, "avg_duration": 0, "tempo": "unknown"}

            durations = [(s['end_page'] - s['start_page']) for s in act_scenes]
            avg_duration = sum(durations) / len(durations)

            if avg_duration < 1.5:
                tempo = "fast"
            elif avg_duration < 2.5:
                tempo = "medium"
            else:
                tempo = "slow"

            return {
                "scene_count": len(act_scenes),
                "avg_duration": avg_duration,
                "tempo": tempo
            }

        return {
            "act1": analyze_act_scenes(act1_scenes),
            "act2": analyze_act_scenes(act2_scenes),
            "act3": analyze_act_scenes(act3_scenes)
        }

    def _assess_overall_tempo(self, scene_pacing_list: List[ScenePacing], rhythm_patterns: Dict) -> str:
        """Assess overall screenplay tempo."""
        if not scene_pacing_list:
            return "unknown"

        # Count tempo types
        fast_count = sum(1 for s in scene_pacing_list if s.tempo == "fast")
        medium_count = sum(1 for s in scene_pacing_list if s.tempo == "medium")
        slow_count = sum(1 for s in scene_pacing_list if s.tempo == "slow")

        total = len(scene_pacing_list)

        # Determine dominant tempo
        if fast_count > (total * 0.5):
            return "fast"
        elif slow_count > (total * 0.5):
            return "slow"
        elif medium_count > (total * 0.5):
            return "medium"
        else:
            return "varied"

    def _check_pacing_rules(self, profile: PacingProfile, sagging_middle: Dict,
                           climax_acceleration: Dict, opening_pacing: Dict,
                           breathing_room: Dict, escalation: Dict) -> List[Dict]:
        """Check pacing against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "PACE.R001":
                # Consistent Pacing
                if profile.pacing_consistency < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Pacing inconsistent: {profile.pacing_consistency:.1%}",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R002":
                # Scene Duration Variety
                if profile.tempo_variety_score < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Insufficient scene duration variety",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R003":
                # Escalation Present
                if not profile.escalation_present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No escalation detected",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R006":
                # Momentum Maintained
                if not profile.momentum_maintained:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Momentum not maintained through Act 2",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R007":
                # Acceleration Into Climax
                if not profile.climax_acceleration:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Final act doesn't accelerate into climax",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R008":
                # Breathing Room Present
                if not breathing_room["sufficient"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Insufficient breathing room: {breathing_room['score']:.1%}",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R009":
                # Opening Hook Pacing
                if not opening_pacing["appropriate"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Opening pacing too slow",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R010":
                # Act 2 Momentum
                if sagging_middle["detected"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Sagging middle detected: {sagging_middle['severity']}",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "PACE.R015":
                # Overall Tempo Coherence
                if profile.pacing_consistency < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Overall tempo incoherent",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_pacing_score(self, profile: PacingProfile,
                                tempo_consistency: float,
                                violations: List) -> float:
        """Calculate overall pacing score."""
        # Start at 90
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
        if profile.pacing_consistency > 0.8:
            score += 5
        elif profile.pacing_consistency > 0.6:
            score += 3

        if profile.tempo_variety_score > 0.8:
            score += 3

        if profile.climax_acceleration and not profile.sagging_middle_detected:
            score += 2

        # Cap at 95
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profile: PacingProfile,
                          violations: List) -> str:
        """Generate pacing diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Pacing is well-controlled with good rhythm and tempo variation"
        elif score >= 60:
            level = "GOOD"
            summary = "Pacing works but could be more dynamic"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Pacing issues affecting narrative flow"
        else:
            level = "POOR"
            summary = "Major pacing problems throughout"

        diagnosis = f"PACING {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if profile.sagging_middle_detected:
            issues.append("sagging middle")
        if not profile.climax_acceleration:
            issues.append("no climax acceleration")
        if profile.pacing_consistency < 0.5:
            issues.append("inconsistent tempo")
        if profile.tempo_variety_score < 0.5:
            issues.append("low variety")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 profile: PacingProfile,
                                 sagging_middle: Dict) -> List[str]:
        """Generate specific pacing recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if profile.sagging_middle_detected:
            recommendations.append("Add complications and raises stakes in Act 2 to prevent sagging")

        if not profile.climax_acceleration:
            recommendations.append("Accelerate pacing in final act with shorter scenes and rising tension")

        if profile.tempo_variety_score < 0.5:
            recommendations.append("Vary scene durations - mix short, medium, and long scenes")

        if profile.pacing_consistency < 0.5:
            recommendations.append("Create more consistent rhythm while maintaining variety")

        if profile.breathing_room_score < 0.5:
            recommendations.append("Add quiet moments for audience to process and reflect")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study pacing in McKee's Story and Snyder's beat sheet")
            recommendations.append("Map scene durations and identify pacing dead zones")

        return recommendations[:5]

    def export_pacing_features(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Export pacing features for correlation/analysis.

        Returns structured data with pacing metrics.
        Useful for external indexing, correlation engines, or ML pipelines.

        Args:
            screenplay_text: Full screenplay text

        Returns:
            Dict with pacing metrics
        """
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)
        scene_pacing_list = self._analyze_scene_durations(scenes)
        momentum_tracking = self._track_momentum(screenplay_text, page_count)

        return {
            "page_metrics": {
                "total_pages": page_count,
                "total_scenes": len(scenes),
                "avg_scene_duration": sum(s.duration_pages for s in scene_pacing_list) / max(len(scene_pacing_list), 1)
            },
            "tempo_distribution": {
                "fast_scenes": sum(1 for s in scene_pacing_list if s.tempo == "fast"),
                "medium_scenes": sum(1 for s in scene_pacing_list if s.tempo == "medium"),
                "slow_scenes": sum(1 for s in scene_pacing_list if s.tempo == "slow")
            },
            "momentum": {
                "act1_score": momentum_tracking["act1_score"],
                "act2_score": momentum_tracking["act2_score"],
                "act3_score": momentum_tracking["act3_score"],
                "maintained": momentum_tracking["maintained"]
            },
            "pacing_consistency": self._calculate_tempo_consistency(scene_pacing_list),
            "meta": {
                "source": "DrPacing",
                "focus": "Scene pacing and narrative rhythm"
            }
        }


# Compatibility class for testing framework
class DrPacingAnalysis(DrPacing):
    """Alias for compatibility with test framework."""
    pass
