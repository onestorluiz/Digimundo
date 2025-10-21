"""
Script Doctor Transitionsmon - Transitions Analysis Specialist
A Script Doctor™ in Digimon form specializing in scene transitions, act transitions, time jumps, location changes, smooth flow, continuity.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class TransitionMoment:
    """Individual transition instance."""
    transition_number: int
    from_scene: str  # scene description
    to_scene: str
    transition_type: str  # "CUT", "DISSOLVE", "FADE", "SMASH CUT", "MONTAGE", etc.
    smoothness: float  # 0-1 (1=seamless)
    is_jarring: bool  # PENALTY
    clarity: float  # 0-1 (clear vs confusing)
    technique: str  # how transition is achieved
    notes: str


@dataclass
class TransitionsProfile:
    """Overall transitions analysis."""
    total_transitions: int
    scene_transitions: int
    act_transitions: int
    smooth_flow_score: float  # 0-1
    jarring_cuts_count: int  # PENALTY
    time_jumps_count: int
    time_jumps_clarity: float
    location_changes_count: int
    location_clarity: float
    pov_shifts_count: int
    parallel_action_count: int
    flashbacks_count: int
    montages_count: int
    continuity_score: float
    cliffhanger_count: int
    tone_shifts_count: int
    seamless_quality: float
    transition_consistency: float
    overall_transition_quality: float


class DrTransitions:
    """
    Script Doctor Transitionsmon - The Transitions Analysis Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing scene transitions,
    act transitions, time jumps, location changes, smooth flow, and continuity.

    Identity: Script Doctor first, Digimon transitions specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Transitionsmon with rules and configuration."""
        self.name = "Script Doctor Transitionsmon"
        self.digimon_name = "Transitionsmon"
        self.title = "Script Doctor - Transitions Analysis Specialist"
        self.specialty = "Scene transitions, act transitions, time jumps, location changes, smooth flow, continuity"
        self.identity = "I am Script Doctor Transitionsmon, a professional Script Doctor™ specializing in transitions analysis"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "transitions_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - TRANSITIONS SPECIFIC
        self.deep_context_queries = [
            # McKee Story - Scene flow and continuity
            "McKee Story scene transitions continuity smooth flow seamless storytelling",
            "McKee scene sequence structure cause effect chain logic progression",
            "McKee transitions between scenes momentum narrative drive forward",
            "McKee scene design beginning middle end microcosm structure complete",
            "McKee beat transitions within scene rhythm pacing progression escalation",
            "McKee progressive complications transitions escalating conflict mounting pressure",
            "McKee act transitions major turning crisis decision point no return",
            # McKee Story - PRINCIPLE OF TRANSITION (ultra-specific from transition section)
            "McKee Story without progression stumbles scene to scene little continuity nothing links events",
            "McKee Story third element links tail Scene A with head Scene B transition hinge",
            "McKee Story what scenes have common or opposition hinge transition connection",
            "McKee Story transition something held common two scenes or counterpointed between them",

            # Truby Anatomy - Story step transitions
            "Truby Anatomy 22 steps transitions flow between story beats sequence",
            "Truby scene transitions cause effect logic organic progression natural",
            "Truby opponent revelation transitions pressure mounting escalating conflict",
            "Truby desire line transitions obstacles complications mounting progressive",
            "Truby scene weaving multiple storylines parallel action intercutting crosscutting",
            "Truby battle sequence transitions confrontation escalation climax building",

            # Field Screenplay - Act structure transitions
            "Field Screenplay act transitions plot points major shifts turning crisis",
            "Field scene sequence transitions time location changes clarity orientation",
            "Field paradigm structure act breaks transitions page 25 85 major",
            "Field setup payoff transitions planted earlier harvested later callback",
            "Field scene transitions continuity smooth flow momentum uninterrupted forward",
            "Field midpoint transition major shift stakes raised escalation intensified",
            "Field montage sequence transitions time compression multiple events compressed",

            # Snyder Save the Cat - Beat transitions
            "Snyder Save the Cat beat sheet transitions flow between 15 beats",
            "Snyder catalyst to debate transition decision hesitation resistance choice",
            "Snyder break into two transition commitment departure journey begins",
            "Snyder fun games to bad guys close in transition shift escalation",
            "Snyder midpoint false victory defeat transition stakes raised shift",
            "Snyder all is lost to dark night soul transition lowest despair",
            "Snyder break into three transition solution discovered hope action final",
            "Snyder finale transitions five-point climax sequence resolution building",

            # Vogler Writer's Journey - Stage transitions
            "Vogler Writer's Journey threshold crossing transition departure commitment passage",
            "Vogler stage transitions 12-stage hero journey flow progression organic",
            "Vogler ordinary world to special world transition threshold passage crossing",
            "Vogler tests allies enemies to approach transition preparation mounting",
            "Vogler ordeal to reward transition death rebirth transformation revelation",
            "Vogler road back to resurrection transition return journey home final",
            "Vogler transitions through archetypal stages natural progression inevitable flow",

            # Campbell Hero 1000 Faces - Mythic transitions
            "Campbell Hero 1000 Faces departure initiation return transitions journey structure",
            "Campbell threshold crossing transition known to unknown familiar strange",
            "Campbell belly whale transition point no return commitment passage complete",
            "Campbell road trials transitions progressive tests mounting challenges escalating",
            "Campbell ultimate boon to return transition revelation brings back world",

            # Aristotle Poetics - Unity and continuity
            "Aristotle Poetics unity of action continuity beginning middle end organic",
            "Aristotle beginning follows nothing middle consequence beginning transitions necessary",
            "Aristotle end follows middle necessarily transitions inevitable logical progression",
            "Aristotle recognition reversal transitions peripeteia anagnorisis fortune shifts",
            "Aristotle cause effect chain continuity actions consequences logical inevitable",

            # Egri Art Dramatic Writing - Causal continuity
            "Egri Art Dramatic Writing cause and effect continuity transitions inevitable",
            "Egri premise drives transitions character conflict resolution progression organic",
            "Egri rising conflict transitions escalation intensification mounting pressure building",
            "Egri orchestration transitions between character storylines weaving intercutting",
            "Egri static to jumping character transitions growth transformation arc",

            # Seger Making Good Script Great - Transition techniques
            "Seger Making Good Script Great scene transitions techniques smooth seamless",
            "Seger smooth transitions avoid jarring cuts disorienting confusing audience",
            "Seger transition techniques dissolve cut match cut smash cut wipe",
            "Seger act transitions turning points major shifts plot progression escalation",
            "Seger parallel action crosscutting intercutting multiple storylines simultaneous weaving",
            "Seger montage sequences time compression transitions multiple events compressed",
            "Seger flashback transitions temporal shifts backstory revelation exposition organic",
            "Seger continuity clarity orientation audience always knows where when",

            # Weiland Creating Character Arcs - Arc transitions
            "Weiland Creating Character Arcs lie to truth transitions growth transformation",
            "Weiland normal world to adventure world transition threshold commitment",
            "Weiland first pinch point transition reminder opposition antagonist pressure",
            "Weiland midpoint transition shift no retreat stakes raised committed",
            "Weiland second pinch point transition opposition mounting pressure intensified",
            "Weiland third plot point transition all lost dark moment lowest",
            "Weiland climax transitions character arc completion lie rejected truth embraced",

            # Goldman Adventures Screen Trade - Film editing mastery
            "Goldman Adventures Screen Trade cutting transitions film editing invisible seamless",
            "Goldman scene transitions momentum forward drive compulsive page-turning engagement",
            "Goldman cut boring parts transitions enter late exit early economy",
            "Goldman transitions clarity audience orientation never confused always tracking",

            # Rhimes Year of Yes - Cliffhanger transitions
            "Rhimes Year of Yes cliffhanger transitions act breaks hook audience",
            "Rhimes beat ending transitions unanswered question suspense momentum forward",
            "Rhimes parallel storylines transitions weaving A B C stories intercutting",
            "Rhimes pacing transitions rhythm intensity peaks valleys balanced flow",

            # Mamet Three Uses of the Knife - Scene construction
            "Mamet Three Uses Knife scene construction beats transitions progression building",
            "Mamet transitions withholding information revelation strategic timing payoff",
            "Mamet cause effect chain transitions actions consequences inevitable logical",

            # Mackendrick On Film-Making - Cinematic transitions
            "Mackendrick On Film-Making cutting transitions montage editing cinematic techniques",
            "Mackendrick visual transitions match cut graphic match eyeline match spatial",
            "Mackendrick montage sequences transitions time space compression juxtaposition",

            # General transition concepts - comprehensive
            "scene transitions smooth seamless invisible craft flow uninterrupted momentum",
            "act transitions major shifts plot points turning crisis escalation",
            "time jumps time ellipsis clarity audience orientation temporal shifts",
            "location changes geography transitions clarity spatial orientation never confused",
            "POV shifts point of view transitions clarity whose perspective perception",
            "tone shifts mood transitions gradual organic justified emotional landscape shifts",
            "parallel action crosscutting intercutting multiple simultaneous storylines weaving",
            "montage sequences time compression multiple events compressed economical storytelling",
            "flashback transitions temporal shifts backstory revelation exposition organic justified",
            "smooth flow narrative continuity cause effect chain logical progression",
            "jarring cuts disorienting confusing audience loses orientation tracking confused",
            "transition techniques dissolve cut match cut smash cut wipe fade",
            "seamless transitions invisible craft audience unaware technique immersed story",
            "cliffhanger transitions act breaks hook audience suspense unanswered engaged",
            "continuity errors flow problems confusion disorientation audience loses tracking",
            "cause and effect continuity actions consequences logical inevitable chain",
            "narrative momentum uninterrupted forward drive compulsive engagement propulsion"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story transition third element hinge commonality opposition link scenes",
        "McKee Story transition link by word sound light object composition",
        "McKee Story transition invisible seam maintain momentum avoid stumble",

        ]

        # Transitions analysis patterns (bilingual: EN + PT)

        # Transition markers (technical)
        self.transition_markers = [
            # English
            "CUT TO", "DISSOLVE TO", "FADE TO", "FADE IN", "FADE OUT",
            "SMASH CUT", "MATCH CUT", "JUMP CUT", "WIPE TO",
            "transition", "cut to", "dissolve", "fade",
            # Portuguese
            "CORTA PARA", "DISSOLVE PARA", "FADE PARA", "FADE IN", "FADE OUT",
            "transição", "corta para", "dissolve"
        ]

        # Smooth flow markers
        self.smooth_markers = [
            # English
            "smooth", "seamless", "flows naturally", "continuous", "fluid",
            "invisible transition", "natural flow", "effortless",
            # Portuguese
            "suave", "sem costura", "flui naturalmente", "contínuo", "fluido",
            "transição invisível", "fluxo natural", "sem esforço"
        ]

        # Jarring cut markers (PENALTY)
        self.jarring_markers = [
            # English
            "jarring", "abrupt", "disorienting", "confusing cut", "awkward",
            "rough transition", "discontinuous", "breaks flow",
            # Portuguese
            "abrupto", "desorientador", "corte confuso", "desajeitado",
            "transição áspera", "descontínuo", "quebra o fluxo"
        ]

        # Time jump markers
        self.time_jump_markers = [
            # English
            "LATER", "NEXT DAY", "NEXT MORNING", "DAYS LATER", "WEEKS LATER",
            "MONTHS LATER", "YEARS LATER", "THE NEXT DAY", "ONE WEEK LATER",
            "time ellipsis", "time jump", "time passes",
            # Portuguese
            "DEPOIS", "DIA SEGUINTE", "MANHÃ SEGUINTE", "DIAS DEPOIS", "SEMANAS DEPOIS",
            "MESES DEPOIS", "ANOS DEPOIS", "NO DIA SEGUINTE", "UMA SEMANA DEPOIS",
            "elipse temporal", "salto temporal", "tempo passa"
        ]

        # Location change markers
        self.location_markers = [
            # English
            "INT.", "EXT.", "location change", "new setting", "different location",
            # Portuguese
            "INT.", "EXT.", "mudança de local", "novo cenário", "local diferente"
        ]

        # Parallel action markers
        self.parallel_markers = [
            # English
            "INTERCUT", "parallel action", "crosscut", "MEANWHILE",
            "SIMULTANEOUSLY", "AT THE SAME TIME",
            # Portuguese
            "INTERCORTAR", "ação paralela", "ENQUANTO ISSO",
            "SIMULTANEAMENTE", "AO MESMO TEMPO"
        ]

        # Flashback markers
        self.flashback_markers = [
            # English
            "FLASHBACK", "EARLIER", "YEARS AGO", "BEFORE", "IN THE PAST",
            # Portuguese
            "FLASHBACK", "ANTES", "ANOS ATRÁS", "NO PASSADO"
        ]

        # Montage markers
        self.montage_markers = [
            # English
            "MONTAGE", "SERIES OF SHOTS", "SEQUENCE", "TIME LAPSE",
            # Portuguese
            "MONTAGEM", "SÉRIE DE CENAS", "SEQUÊNCIA", "LAPSO TEMPORAL"
        ]

        # Act break markers
        self.act_break_markers = [
            # English
            "END OF ACT", "major shift", "plot point transition", "turning point",
            "ACT TWO", "ACT THREE", "major turning point",
            # Portuguese
            "FIM DO ATO", "mudança maior", "ponto de virada", "transição de ponto de trama",
            "ATO DOIS", "ATO TRÊS", "grande ponto de virada"
        ]

        # POV shift markers
        self.pov_shift_markers = [
            # English
            "POV shift", "point of view", "perspective change", "switches to",
            # Portuguese
            "mudança de POV", "ponto de vista", "mudança de perspectiva", "muda para"
        ]

        # Tone shift markers
        self.tone_shift_markers = [
            # English
            "tone shift", "mood change", "shifts from", "tonal change",
            # Portuguese
            "mudança de tom", "mudança de humor", "muda de", "mudança tonal"
        ]

        # Cliffhanger markers
        self.cliffhanger_markers = [
            # English
            "cliffhanger", "leaves audience hanging", "hook", "suspenseful cut",
            "cut at peak tension", "unresolved moment",
            # Portuguese
            "gancho", "deixa audiência suspensa", "corte suspense",
            "corta no pico de tensão", "momento não resolvido"
        ]

        # Continuity markers
        self.continuity_markers = [
            # English
            "continuity", "consistent", "flows logically", "cause and effect",
            "continuous", "unbroken flow",
            # Portuguese
            "continuidade", "consistente", "flui logicamente", "causa e efeito",
            "contínuo", "fluxo ininterrupto"
        ]

        # Seamless markers
        self.seamless_markers = [
            # English
            "seamless", "invisible", "unnoticeable", "effortless transition",
            "audience doesn't notice",
            # Portuguese
            "sem costura", "invisível", "imperceptível", "transição sem esforço",
            "audiência não percebe"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze transitions in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete transitions diagnostic report
        """
        # Extract page count and scenes
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)

        # Detect scene transitions
        scene_transitions = self._detect_scene_transitions(screenplay_text, scenes)

        # Analyze smooth flow
        smooth_flow = self._analyze_smooth_flow(screenplay_text, scenes)

        # Detect jarring cuts (PENALTY)
        jarring_cuts = self._detect_jarring_cuts(screenplay_text)

        # Analyze time jumps
        time_jumps = self._analyze_time_jumps(screenplay_text)

        # Analyze location changes
        location_changes = self._analyze_location_changes(screenplay_text, scenes)

        # Analyze act transitions
        act_transitions = self._analyze_act_transitions(screenplay_text, page_count)

        # Detect POV shifts
        pov_shifts = self._detect_pov_shifts(screenplay_text)

        # Detect parallel action
        parallel_action = self._detect_parallel_action(screenplay_text)

        # Detect flashbacks
        flashbacks = self._detect_flashbacks(screenplay_text)

        # Detect montages
        montages = self._detect_montages(screenplay_text)

        # Assess continuity
        continuity = self._assess_continuity(screenplay_text, scenes)

        # Detect cliffhangers
        cliffhangers = self._detect_cliffhangers(screenplay_text, scenes)

        # Analyze tone shifts
        tone_shifts = self._analyze_tone_shifts(screenplay_text)

        # Assess seamless quality
        seamless_quality = self._assess_seamless_quality(screenplay_text)

        # Assess transition consistency
        transition_consistency = self._assess_transition_consistency(
            scene_transitions, smooth_flow, jarring_cuts, continuity
        )

        # Build transitions profile
        transitions_profile = TransitionsProfile(
            total_transitions=scene_transitions["count"] + act_transitions["count"],
            scene_transitions=scene_transitions["count"],
            act_transitions=act_transitions["count"],
            smooth_flow_score=smooth_flow["score"],
            jarring_cuts_count=jarring_cuts["count"],
            time_jumps_count=time_jumps["count"],
            time_jumps_clarity=time_jumps["clarity"],
            location_changes_count=location_changes["count"],
            location_clarity=location_changes["clarity"],
            pov_shifts_count=pov_shifts["count"],
            parallel_action_count=parallel_action["count"],
            flashbacks_count=flashbacks["count"],
            montages_count=montages["count"],
            continuity_score=continuity["score"],
            cliffhanger_count=cliffhangers["count"],
            tone_shifts_count=tone_shifts["count"],
            seamless_quality=seamless_quality["score"],
            transition_consistency=transition_consistency["score"],
            overall_transition_quality=0.0  # calculated below
        )

        # Calculate overall transition quality
        transitions_profile.overall_transition_quality = self._calculate_overall_transition_quality(transitions_profile)

        # Check against rules
        rule_violations = self._check_transitions_rules(
            transitions_profile, scene_transitions, smooth_flow, jarring_cuts,
            time_jumps, location_changes, act_transitions, continuity,
            seamless_quality, transition_consistency
        )

        # Calculate score
        score = self._calculate_transitions_score(
            transitions_profile, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, transitions_profile, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "scene_transitions": {
                "count": scene_transitions["count"],
                "present": scene_transitions.get("present", False),
                "quality": scene_transitions.get("quality", "medium"),
                "examples": scene_transitions.get("examples", [])[:3]
            },
            "smooth_flow": {
                "score": smooth_flow["score"],
                "smooth": smooth_flow.get("smooth", False),
                "examples": smooth_flow.get("examples", [])[:2]
            },
            "jarring_cuts": {
                "count": jarring_cuts["count"],
                "penalty": jarring_cuts.get("penalty", False),
                "examples": jarring_cuts.get("examples", [])[:3]
            },
            "time_jumps": {
                "count": time_jumps["count"],
                "clarity": time_jumps["clarity"],
                "clear": time_jumps.get("clear", False),
                "examples": time_jumps.get("examples", [])[:2]
            },
            "location_changes": {
                "count": location_changes["count"],
                "clarity": location_changes["clarity"],
                "clear": location_changes.get("clear", False)
            },
            "act_transitions": {
                "count": act_transitions["count"],
                "strong": act_transitions.get("strong", False),
                "examples": act_transitions.get("examples", [])[:2]
            },
            "pov_shifts": {
                "count": pov_shifts["count"],
                "clear": pov_shifts.get("clear", False)
            },
            "parallel_action": {
                "count": parallel_action["count"],
                "effective": parallel_action.get("effective", False)
            },
            "flashbacks": {
                "count": flashbacks["count"],
                "smooth": flashbacks.get("smooth", False)
            },
            "montages": {
                "count": montages["count"],
                "appropriate": montages.get("appropriate", False)
            },
            "continuity": {
                "score": continuity["score"],
                "maintained": continuity.get("maintained", False)
            },
            "cliffhangers": {
                "count": cliffhangers["count"],
                "effective": cliffhangers.get("effective", False)
            },
            "tone_shifts": {
                "count": tone_shifts["count"],
                "smooth": tone_shifts.get("smooth", False)
            },
            "seamless_quality": {
                "score": seamless_quality["score"],
                "seamless": seamless_quality.get("seamless", False)
            },
            "transition_consistency": {
                "score": transition_consistency["score"],
                "consistent": transition_consistency.get("consistent", False)
            },
            "overall_transition_quality": transitions_profile.overall_transition_quality,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, transitions_profile
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

    def _detect_scene_transitions(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """
        Detect all scene transitions.

        Field/McKee: "Scene transitions fundamental to flow."
        """
        count = len(scenes) - 1 if len(scenes) > 1 else 0
        examples = []

        # Get examples of transitions
        for i in range(min(5, len(scenes) - 1)):
            from_scene = scenes[i]['heading']
            to_scene = scenes[i + 1]['heading']
            examples.append(f"{from_scene[:50]} → {to_scene[:50]}")

        present = count >= 5

        # Determine quality
        if count >= 30 and count <= 50:
            quality = "optimal"
        elif count >= 20 and count <= 60:
            quality = "good"
        elif count >= 10:
            quality = "adequate"
        else:
            quality = "insufficient"

        return {
            "count": count,
            "present": present,
            "quality": quality,
            "examples": examples
        }

    def _analyze_smooth_flow(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """
        Analyze flow smoothness.

        Seger: "Smooth transitions - audience doesn't notice transition."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.smooth_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Calculate score (0-1)
        score = min(1.0, count / 3.0)

        smooth = score >= 0.5 or count >= 2

        return {
            "score": score,
            "smooth": smooth,
            "count": count,
            "examples": examples
        }

    def _detect_jarring_cuts(self, screenplay: str) -> Dict[str, Any]:
        """
        Flag jarring/disorienting transitions (PENALTY).

        Seger: "Avoid jarring cuts - disorienting audience."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.jarring_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Penalty if present
        penalty = count >= 1

        return {
            "count": count,
            "penalty": penalty,
            "examples": examples
        }

    def _analyze_time_jumps(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze time ellipsis clarity.

        Field: "Time jumps must be clear - audience knows when/where."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.time_jump_markers:
                if marker in line.upper():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Assess clarity (0-1)
        # Presence of time jump markers = clear
        if count == 0:
            clarity = 1.0  # no time jumps = no confusion
        elif count <= 5:
            clarity = 0.9  # clear time jumps
        elif count <= 10:
            clarity = 0.7  # moderate
        else:
            clarity = 0.5  # many time jumps = potential confusion

        clear = clarity >= 0.6

        return {
            "count": count,
            "clarity": clarity,
            "clear": clear,
            "examples": examples
        }

    def _analyze_location_changes(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """
        Analyze geography transitions.

        Field: "Location changes must be clear - audience knows where they are."
        """
        count = 0

        # Count distinct location changes (scene headings)
        locations = set()
        for scene in scenes:
            # Extract location from heading
            heading = scene['heading']
            # Simple extraction: just use the heading as location
            locations.add(heading)

        count = len(locations)

        # Assess clarity (0-1)
        # More locations = need clarity
        if count <= 5:
            clarity = 1.0  # few locations = easy to track
        elif count <= 10:
            clarity = 0.8
        elif count <= 20:
            clarity = 0.6
        else:
            clarity = 0.4  # many locations = harder to track

        clear = clarity >= 0.6

        return {
            "count": count,
            "clarity": clarity,
            "clear": clear
        }

    def _analyze_act_transitions(self, screenplay: str, page_count: int) -> Dict[str, Any]:
        """
        Analyze major plot point transitions.

        Field: "Act transitions at plot points - major turning moments."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.act_break_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Also check for major transitions around expected plot points
        # Plot point 1 around page 25 (25% of script)
        # Midpoint around page 50-60 (50% of script)
        # Plot point 2 around page 75-90 (75% of script)
        # This is implicit - if count >= 2, likely has act transitions

        strong = count >= 2  # At least 2 major transitions

        return {
            "count": count,
            "strong": strong,
            "examples": examples
        }

    def _detect_pov_shifts(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect point of view changes.

        Vogler: "POV shifts must be clear - audience knows whose perspective."
        """
        count = 0

        for marker in self.pov_shift_markers:
            count += screenplay.lower().count(marker)

        clear = count == 0 or count <= 5  # Few POV shifts = clearer

        return {
            "count": count,
            "clear": clear
        }

    def _detect_parallel_action(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect crosscutting/intercutting.

        McKee: "Parallel action creates tension through intercutting."
        """
        count = 0

        for marker in self.parallel_markers:
            count += screenplay.upper().count(marker)

        effective = count >= 1 and count <= 5  # Present but not overused

        return {
            "count": count,
            "effective": effective
        }

    def _detect_flashbacks(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect temporal shifts to past.

        Seger: "Flashbacks can be jarring if not smooth."
        """
        count = 0

        for marker in self.flashback_markers:
            count += screenplay.upper().count(marker)

        # Smooth if few flashbacks (overuse = jarring)
        smooth = count <= 3

        return {
            "count": count,
            "smooth": smooth
        }

    def _detect_montages(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect montage sequences.

        Snyder: "Montages compress time effectively."
        """
        count = 0

        for marker in self.montage_markers:
            count += screenplay.upper().count(marker)

        # Appropriate if present but not overused
        appropriate = count >= 1 and count <= 3

        return {
            "count": count,
            "appropriate": appropriate
        }

    def _assess_continuity(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """
        Assess cause-and-effect continuity.

        Aristotle/Egri: "Unity of action - cause and effect continuity."
        """
        count = 0

        for marker in self.continuity_markers:
            count += screenplay.lower().count(marker)

        # Calculate score (0-1)
        score = min(1.0, count / 5.0)

        maintained = score >= 0.4 or count >= 2

        return {
            "score": score,
            "maintained": maintained,
            "count": count
        }

    def _detect_cliffhangers(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """
        Detect cliffhanger transitions.

        Rhimes: "Cliffhanger transitions hook audience."
        """
        count = 0

        for marker in self.cliffhanger_markers:
            count += screenplay.lower().count(marker)

        # Effective if present but not overused
        effective = count >= 1 and count <= 4

        return {
            "count": count,
            "effective": effective
        }

    def _analyze_tone_shifts(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze mood transitions.

        McKee: "Tone shifts must be smooth - jarring tone = disorienting."
        """
        count = 0

        for marker in self.tone_shift_markers:
            count += screenplay.lower().count(marker)

        # Smooth if few tone shifts (many = potentially jarring)
        smooth = count <= 3

        return {
            "count": count,
            "smooth": smooth
        }

    def _assess_seamless_quality(self, screenplay: str) -> Dict[str, Any]:
        """
        Assess invisible transitions.

        Ideal: "Audience doesn't notice transitions - seamless flow."
        """
        count = 0

        for marker in self.seamless_markers:
            count += screenplay.lower().count(marker)

        # Calculate score (0-1)
        score = min(1.0, count / 3.0)

        seamless = score >= 0.5 or count >= 2

        return {
            "score": score,
            "seamless": seamless,
            "count": count
        }

    def _assess_transition_consistency(self, scene_transitions: Dict,
                                      smooth_flow: Dict, jarring_cuts: Dict,
                                      continuity: Dict) -> Dict[str, Any]:
        """
        Assess overall transition quality consistency.

        Consistency = smooth flow + no jarring cuts + good continuity.
        """
        # Calculate consistency score
        scores = [
            1.0 if scene_transitions["count"] >= 10 else 0.5,
            smooth_flow["score"],
            max(0.0, 1.0 - (jarring_cuts["count"] * 0.2)),  # PENALTY for jarring
            continuity["score"]
        ]

        consistency_score = sum(scores) / len(scores)

        consistent = consistency_score >= 0.6

        return {
            "score": consistency_score,
            "consistent": consistent
        }

    def _calculate_overall_transition_quality(self, profile: TransitionsProfile) -> float:
        """Calculate overall transition quality score."""
        scores = [
            1.0 if profile.scene_transitions >= 10 else 0.5,
            profile.smooth_flow_score,
            max(0.0, 1.0 - (profile.jarring_cuts_count * 0.3)),  # PENALTY
            profile.time_jumps_clarity,
            profile.location_clarity,
            1.0 if profile.act_transitions >= 2 else 0.5,
            1.0 if profile.pov_shifts_count <= 5 else 0.6,
            profile.continuity_score,
            profile.seamless_quality,
            profile.transition_consistency
        ]

        # Average
        overall = sum(scores) / len(scores)

        return max(0.0, min(1.0, overall))

    def _check_transitions_rules(self, profile: TransitionsProfile,
                                 scene_transitions: Dict, smooth_flow: Dict,
                                 jarring_cuts: Dict, time_jumps: Dict,
                                 location_changes: Dict, act_transitions: Dict,
                                 continuity: Dict, seamless_quality: Dict,
                                 transition_consistency: Dict) -> List[Dict]:
        """Check transitions against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "TRANS.R001":
                # Transitions Present
                if profile.scene_transitions < 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Insufficient scene transitions - static story",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R002":
                # Smooth Flow
                if profile.smooth_flow_score < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Flow not smooth - transitions noticeable",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R003":
                # Avoid Jarring Cuts
                if profile.jarring_cuts_count >= 1:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Jarring cuts present ({profile.jarring_cuts_count}) - disorienting audience",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R004":
                # Time Jumps Clear
                if profile.time_jumps_clarity < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Time jumps unclear - audience disoriented",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R005":
                # Location Changes Clear
                if profile.location_clarity < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Location changes unclear - geography confusing",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R006":
                # Act Transitions Strong
                if profile.act_transitions < 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Weak act transitions - major shifts unclear",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R007":
                # POV Shifts Clear
                if profile.pov_shifts_count > 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Too many POV shifts ({profile.pov_shifts_count}) - perspective confusing",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R008":
                # Parallel Action Effective
                if profile.parallel_action_count > 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Parallel action overused - intercutting excessive",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R009":
                # Flashbacks Smooth
                if profile.flashbacks_count > 3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Too many flashbacks ({profile.flashbacks_count}) - temporal confusion",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R010":
                # Montages Appropriate
                if profile.montages_count > 3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Montages overused - technique loses impact",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R011":
                # Continuity Maintained
                if profile.continuity_score < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Continuity problems - cause-effect unclear",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R012":
                # Cliffhanger Transitions
                if profile.cliffhanger_count == 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No cliffhanger transitions - missing hook opportunities",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R013":
                # Tone Shifts Smooth
                if profile.tone_shifts_count > 3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Too many tone shifts - mood changes jarring",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R014":
                # Seamless Invisible
                if profile.seamless_quality < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Transitions not seamless - visible technique",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "TRANS.R015":
                # Transition Consistency
                if profile.transition_consistency < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Inconsistent transitions - quality varies",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_transitions_score(self, profile: TransitionsProfile, violations: List) -> float:
        """Calculate overall transitions score."""
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

        # Extra penalty for jarring cuts
        if profile.jarring_cuts_count >= 1:
            score -= profile.jarring_cuts_count * 10  # -10 per jarring cut

        # Bonus for excellence
        if profile.overall_transition_quality > 0.8:
            score += 5
        elif profile.overall_transition_quality > 0.7:
            score += 3

        if profile.smooth_flow_score > 0.7:
            score += 3

        if profile.seamless_quality > 0.6:
            score += 2

        if profile.continuity_score > 0.7:
            score += 2

        if profile.transition_consistency > 0.7:
            score += 2

        if profile.jarring_cuts_count == 0:
            score += 3  # Bonus for zero jarring cuts

        # Cap at 95
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profile: TransitionsProfile,
                          violations: List) -> str:
        """Generate transitions diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Transitions seamless and invisible - smooth flow throughout"
        elif score >= 60:
            level = "GOOD"
            summary = "Transitions generally smooth but some noticeable moments"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Transition problems - jarring cuts or unclear shifts"
        else:
            level = "POOR"
            summary = "Major transition problems - disorienting audience"

        diagnosis = f"TRANSITIONS {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if profile.jarring_cuts_count >= 1:
            issues.append(f"jarring cuts ({profile.jarring_cuts_count})")
        if profile.time_jumps_clarity < 0.5:
            issues.append("unclear time jumps")
        if profile.location_clarity < 0.5:
            issues.append("location confusion")
        if profile.continuity_score < 0.4:
            issues.append("continuity problems")
        if profile.seamless_quality < 0.4:
            issues.append("visible transitions")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 profile: TransitionsProfile) -> List[str]:
        """Generate specific transitions recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if profile.jarring_cuts_count >= 1:
            recommendations.append("Eliminate jarring cuts - Seger: 'Smooth transitions - audience doesn't notice' - make transitions seamless")

        if profile.smooth_flow_score < 0.4:
            recommendations.append("Improve flow smoothness - transitions should be invisible, natural - avoid abrupt changes")

        if profile.time_jumps_clarity < 0.5:
            recommendations.append("Clarify time jumps - Field: 'Audience must know when/where' - use clear time markers (LATER, NEXT DAY)")

        if profile.location_clarity < 0.5:
            recommendations.append("Clarify location changes - clear scene headings, avoid too many locations")

        if profile.act_transitions < 2:
            recommendations.append("Strengthen act transitions - Field: 'Plot points are major turning moments' - emphasize major shifts")

        if profile.continuity_score < 0.4:
            recommendations.append("Improve continuity - Aristotle/Egri: 'Unity of action - cause and effect' - maintain logical flow")

        if profile.seamless_quality < 0.4:
            recommendations.append("Make transitions seamless - best transitions are invisible, audience doesn't notice the craft")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study Field's Screenplay - scene transitions and act breaks fundamental to structure")
            recommendations.append("Study Seger's Making Good Script Great - transition techniques, smooth vs jarring")

        return recommendations[:5]

    def export_transitions_features(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Export transitions features for correlation/analysis.

        Returns structured data with transitions metrics.
        Useful for external indexing, correlation engines, or ML pipelines.

        Args:
            screenplay_text: Full screenplay text

        Returns:
            Dict with transitions metrics
        """
        scenes = self._extract_scenes(screenplay_text)
        scene_transitions = self._detect_scene_transitions(screenplay_text, scenes)
        smooth_flow = self._analyze_smooth_flow(screenplay_text, scenes)
        jarring_cuts = self._detect_jarring_cuts(screenplay_text)

        return {
            "scene_transitions": {
                "count": scene_transitions["count"],
                "present": scene_transitions.get("present", False)
            },
            "smooth_flow": {
                "score": smooth_flow["score"],
                "smooth": smooth_flow.get("smooth", False)
            },
            "jarring_cuts": {
                "count": jarring_cuts["count"],
                "penalty": jarring_cuts.get("penalty", False)
            },
            "meta": {
                "source": "DrTransitions",
                "focus": "Transitions quality and flow continuity"
            }
        }


# Compatibility class for testing framework
class DrTransitionsAnalysis(DrTransitions):
    """Alias for compatibility with test framework."""
    pass
