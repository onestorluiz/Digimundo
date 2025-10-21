"""
Script Doctor Subtextmon - Subtext Analysis Specialist
A Script Doctor™ in Digimon form specializing in subtext, what's unsaid, implication, inference, reading between lines, layered meaning.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class SubtextMoment:
    """Individual subtext instance."""
    location: str  # scene/page
    surface_text: str  # what is said
    subtext: str  # what is meant
    technique: str  # how subtext is created (silence, action, irony, etc.)
    sophistication: float  # 0-1 (quality of subtext)
    notes: str


@dataclass
class SubtextProfile:
    """Overall subtext analysis."""
    subtext_moments_count: int
    on_the_nose_count: int  # PENALTY - explicit dialogue
    says_vs_means_ratio: float  # higher is better
    silence_pause_count: int
    action_contradiction_count: int
    visual_subtext_score: float
    hidden_agenda_count: int
    avoidance_deflection_count: int
    denial_suppression_count: int
    irony_sarcasm_count: int
    layered_meaning_score: float
    emotional_subtext_score: float
    power_dynamics_score: float
    subtext_sophistication: float  # 0-1
    subtext_consistency: float  # 0-1
    overall_subtext_quality: float
    reading_between_lines_score: float
    implication_inference_score: float
    surface_vs_depth_ratio: float
    subtext_richness: float


class DrSubtext:
    """
    Script Doctor Subtextmon - The Subtext Analysis Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing subtext,
    what's unsaid, implication, inference, reading between lines, layered meaning.

    Identity: Script Doctor first, Digimon subtext specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Subtextmon with rules and configuration."""
        self.name = "Script Doctor Subtextmon"
        self.digimon_name = "Subtextmon"
        self.title = "Script Doctor - Subtext Analysis Specialist"
        self.specialty = "Subtext, what's unsaid, implication, inference, reading between lines, layered meaning"
        self.identity = "I am Script Doctor Subtextmon, a professional Script Doctor™ specializing in subtext analysis"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "subtext_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - SUBTEXT SPECIFIC
        self.deep_context_queries = [
            # McKee Story - Subtext mastery as essence of dialogue
            "McKee Story subtext essence dialogue characters rarely say what mean gap truth",
            "McKee Story subtext what's unsaid more powerful than said silence pauses",
            "McKee Story text vs subtext surface meaning vs depth true meaning",
            "McKee Story dialogue subtext layered meaning multiple interpretations depth",
            "McKee Story on-the-nose dialogue vs subtext avoid explicit flat",
            "McKee Story subtext through action contradicting words behavior reveals truth",
            "McKee Dialogue Art of Verbal Action subtext as core sophisticated writing",
            "McKee Dialogue subtext implication inference reading between lines audience detective",

            # McKee Story - SUBTEXT DEPTH (ultra-specific manual reading)
            "McKee Story subtext unspoken truth beneath dialogue surface versus depth gap meaning",
            "McKee Story dialogue reveals character thought feeling beneath words true meaning hidden",
            "McKee Story action speaks louder words behavior reveals character truth versus claims",
            "McKee Story subtext gap words versus meaning what said versus what meant contradiction",
            "McKee Story on-the-nose dialogue flat stating obvious avoid subtext sophisticated depth",
            "McKee Story subtext through behavior action contradicts words truth revealed disparity",

            # McKee Story - TEXT vs SUBTEXT DUALITY (ultra-specific from TEXT AND SUBTEXT chapter)
            "McKee Story text sensory surface what see hear say do images soundtrack dialogue",
            "McKee Story subtext life under surface thoughts feelings known unknown hidden behavior",
            "McKee Story if scene about what scene about deep shit on-the-nose writing avoid",
            "McKee Story nothing what seems duplicity life everything exists two levels duality",
            "McKee Story veil truth living mask actual thoughts feelings behind saying doing",
            "McKee Story actor creates subtext not text inside out unspoken unconscious surface",
            "McKee Story storyteller guide beyond what seems what is depths unspoken unaware",

            # Truby Anatomy - Hidden motives and agendas
            "Truby Anatomy subtext hidden agenda ulterior motives character wants says different",
            "Truby Anatomy moral argument subtext ethical implications beneath surface dialogue",
            "Truby Anatomy character web subtext relationship dynamics unspoken tensions power",
            "Truby Anatomy wants vs needs subtext inner conflict external vs internal truth",
            "Truby Anatomy subtext strategic revelation what character hides why timing",
            "Truby Anatomy ghost subtext past wounds hidden driving behavior unspoken",
            "Truby Anatomy subtext thematic dialogue philosophy ideas beneath surface conversation",

            # Field Screenplay - Implication and reading between lines
            "Field Screenplay subtext implication suggestion rather than explicit statement sophisticated",
            "Field subtext reading between lines audience infers unstated meaning engagement",
            "Field subtext show don't tell visual behavioral rather than verbal exposition",
            "Field dialogue subtext says one thing means another gap words intent",
            "Field subtext through scene structure action sequence reveals character truth",
            "Field subtext character arc transformation inner change shown not stated",
            "Field subtext dramatic irony audience knows more than characters depth",

            # Snyder Save the Cat - Sophisticated subtext in beats
            "Snyder Save the Cat subtext double meaning layered dialogue depth sophistication",
            "Snyder primal subtext emotions beneath words universal human truth connection",
            "Snyder subtext in beats fun and games revealing character through action",
            "Snyder all is lost dark night soul subtext emotional truth vulnerability",
            "Snyder subtext Pope in Pool exposition disguised as action natural integration",
            "Snyder finale subtext synthesis transformation shown through behavior not words",

            # Vogler Writer's Journey - Shadow and unconscious meaning
            "Vogler Writer's Journey shadow subtext hidden self denied aspects unconscious",
            "Vogler archetypes subtext universal patterns beneath surface story mythic resonance",
            "Vogler mentor subtext wisdom teaching through action example not lecture",
            "Vogler threshold guardian subtext test challenge character forced reveal true self",
            "Vogler ordeal subtext death rebirth transformation shown through crisis behavior",
            "Vogler return subtext changed hero proof through action not proclamation",

            # Campbell Hero 1000 Faces - Mythic subtext and symbolic depth
            "Campbell Hero 1000 Faces mythic subtext symbolic meaning archetypal universal depth",
            "Campbell separation subtext leaving ordinary world reluctance fear shown not stated",
            "Campbell initiation subtext trials transformation inner change through action ordeal",
            "Campbell atonement father subtext confronting power source hidden truth revelation",
            "Campbell ultimate boon subtext wisdom gained shown through changed behavior",
            "Campbell return threshold subtext bringing wisdom home proof through action sacrifice",

            # Aristotle Poetics - Dianoia and thought beneath surface
            "Aristotle Poetics dianoia thought subtext ideas meaning beneath surface dialogue",
            "Aristotle necessity probability subtext logic cause effect implied not explained",
            "Aristotle recognition anagnorisis subtext realization dawning awareness shown process",
            "Aristotle catharsis subtext emotional truth pity fear audience inference engagement",
            "Aristotle unity action subtext thematic coherence meaning through structure pattern",

            # Egri Art Dramatic Writing - Characters hiding true feelings
            "Egri Art Dramatic Writing subtext characters hide true feelings masks defense",
            "Egri premise subtext thematic truth argued through action not dialogue sermon",
            "Egri orchestration subtext conflict through contrasting characters revealed interaction clash",
            "Egri growing subtext character change transformation shown not announced development",
            "Egri inner conflict subtext character torn desires fear shown behavior contradiction",

            # Seger Making Good Script Great - Show don't tell sophistication
            "Seger Making Good Script Great subtext show don't tell imply not state visual",
            "Seger subtext layered meaning depth sophisticated writing audience engagement detective",
            "Seger subtext through action behavior reveals character truth more than words",
            "Seger subtext exposition integration natural organic context not info dump",
            "Seger dialogue subtext says means different gap sophisticated screenwriting quality",
            "Seger subtext emotional truth feelings shown through behavior body language visual",
            "Seger subtext avoidance deflection what character won't discuss reveals truth",

            # Weiland Creating Character Arcs - Inner truth and change
            "Weiland Creating Character Arcs lie believes subtext inner truth denied hidden",
            "Weiland ghost wound subtext past trauma driving behavior unspoken influence",
            "Weiland want vs need subtext external goal vs inner truth character blind",
            "Weiland moment truth subtext realization acceptance inner change shown decision",
            "Weiland character arc subtext transformation gradual shown through choices behavior",
            "Weiland flat arc subtext character knows truth world changes around steadfast",

            # Goldman Adventures Screen Trade - What's really happening beneath surface
            "Goldman Adventures Screen Trade subtext what's really happening beneath apparent action",
            "Goldman subtext sophisticated screenwriting quality depth vs exposition pedestrian flat",
            "Goldman subtext character behavior reveals truth more than dialogue action speaks",
            "Goldman nobody knows anything subtext uncertainty fear hidden beneath confidence bravado",
            "Goldman subtext screenplay structure meaning through pattern not explicit statement",

            # Rhimes Year of Yes - Layered drama and emotional subtext
            "Rhimes Year of Yes subtext layered drama emotional depth beneath surface story",
            "Rhimes authentic voice subtext truth vulnerability real emotion shown not stated",
            "Rhimes subtext relationship dynamics power tension chemistry shown interaction behavior",
            "Rhimes subtext saying yes to truth fear denial avoidance character avoiding",

            # Mamet Three Uses of the Knife - Withholding and action speaks
            "Mamet Three Uses of the Knife subtext action speaks truth words lie behavior reveals",
            "Mamet subtext withholding information implication mystery audience engagement detective",
            "Mamet dramatic structure subtext meaning through pattern juxtaposition not explanation",
            "Mamet subtext essential task what character wants shown pursuit not proclamation",

            # Mackendrick On Film-Making - Visual subtext and showing
            "Mackendrick On Film-Making subtext visual storytelling image behavior reveals truth",
            "Mackendrick subtext body language facial expression gesture reveals hidden emotion",
            "Mackendrick subtext through editing juxtaposition meaning created visual pattern",
            "Mackendrick subtext image sequence story told visually not verbally sophisticated",

            # General subtext concepts - Comprehensive coverage
            "subtext what's unsaid more powerful than said silence pauses eloquent",
            "subtext says vs means gap words intent truth beneath surface dialogue",
            "subtext through action contradicting words behavior betrays reveals truth",
            "subtext layered meaning multiple interpretations depth sophisticated engagement",
            "subtext implication inference reading between lines audience detective active",
            "on-the-nose dialogue vs subtext avoid explicit flat expositional stating",
            "subtext hidden agenda ulterior motives character wants different from says",
            "subtext emotional truth feelings hidden masked denied beneath surface behavior",
            "subtext avoidance deflection changing subject what character won't discuss reveals",
            "subtext denial suppression what character refuses admit acknowledge inner conflict",
            "subtext visual body language expression gesture posture reveals hidden truth",
            "subtext irony sarcasm saying opposite meaning literal vs intended sophisticated",
            "subtext power dynamics unspoken hierarchy dominance submission control manipulation",
            "subtext dramatic irony audience understands character blind engaged active",
            "rich sophisticated subtext vs absent flat expositional dialogue quality writing"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story text surface words deeds subtext hidden thoughts feelings",
        "McKee Story living mask public persona conceals inner contradictions",
        "McKee Story inner monologue guides choices but unseen on screen",
        "McKee Story behavior beats convey subtext gesture posture business",

        # McKee DIALOGUE - GPT-5 extracted (12 Oct 2025)
        "McKee Dialogue subtext said unsaid unsayable layered spheres implication",
        "McKee Dialogue subtext action beneath words tactic intent desire concealed",
        "McKee Dialogue text subtext transparency audience reads mind insight",
        "McKee Dialogue subtext contradiction words versus behavior disparity irony",
        "McKee Dialogue subtext indirection trialogue third thing funnel conflict",
        "McKee Dialogue subtext covert antagonism polite speech injures indirectly",
        "McKee Dialogue subtext erase on-the-nose dialogue hollow falsity warning",
        "McKee Dialogue subtext through figurative language sensory metaphor resonance",
        "McKee Dialogue subtext created by pause silence cue audience inference",
        "McKee Dialogue subtext economy fewer words greater meaning density",
        "McKee Dialogue subtext from backstory secrets revealed dilemma pressure",
        "McKee Dialogue subtext exposition as ammunition facts used as weapons",
        "McKee Dialogue subtext inner life unsayable subconscious urges energies",
        "McKee Dialogue subtext within culture high-context unsaid exchanged implicit",
        "McKee Dialogue subtext reading through narration free indirect style cues",
        "McKee Dialogue subtext beat labeling gerunds uncover true actions",
        "McKee Dialogue subtext irony positive negative charges double meanings",
        "McKee Dialogue subtext reflexive conflict self listening silent self",
        "McKee Dialogue subtext point of view limits reveal through hints",
        "McKee Dialogue subtext minimal conflict confessions intimacy bar scene",
        "McKee Dialogue subtext Daisy snuffs candles hulking insult message Gatsby",
        "McKee Dialogue subtext Tony Soprano therapy avoidance confession denial",
        "McKee Dialogue subtext trialogue canary murders power marriage war",
        "McKee Dialogue subtext counterpoint narration undercut sentimentality distance",
        "McKee Dialogue subtext through paralanguage proxemics gaze posture tempo",
        "McKee Dialogue subtext masked by clichés neutral language drains depth",
        "McKee Dialogue subtext rhythm glide words well yeah hmm thought-space",
        "McKee Dialogue subtext inner monologue externalizes unsayable impulses",
        "McKee Dialogue subtext Magic If inhabit character sense unspoken truths",
        "McKee Dialogue subtext misshapen scenes inner motives misalign outer talk",


        ]

        # Subtext analysis patterns (bilingual: EN + PT)

        # General subtext markers
        self.subtext_markers = [
            # English
            "subtext", "implied", "unspoken", "between the lines", "layered meaning",
            "what's really meant", "deeper meaning", "hidden meaning", "underneath",
            "beneath the surface", "true meaning", "reading between",
            # Portuguese
            "subtexto", "implícito", "não dito", "nas entrelinhas", "significado em camadas",
            "o que realmente significa", "significado mais profundo", "significado oculto",
            "por baixo", "sob a superfície", "verdadeiro significado"
        ]

        # Says vs means markers
        self.says_vs_means_markers = [
            # English
            "says X but means Y", "words vs intent", "surface vs depth",
            "says one thing means another", "literal vs intended",
            "words don't match meaning", "double meaning", "layered",
            # Portuguese
            "diz X mas significa Y", "palavras vs intenção", "superfície vs profundidade",
            "diz uma coisa significa outra", "literal vs pretendido",
            "palavras não correspondem significado", "duplo significado", "em camadas"
        ]

        # Silence markers
        self.silence_markers = [
            # English
            "silence", "pause", "doesn't say", "avoids saying", "won't say",
            "quiet", "says nothing", "no response", "beat", "long pause",
            # Portuguese
            "silêncio", "pausa", "não diz", "evita dizer", "não vai dizer",
            "quieto", "não diz nada", "sem resposta", "batida", "pausa longa"
        ]

        # Action contradiction markers
        self.action_contradiction_markers = [
            # English
            "says X but does Y", "words contradict actions", "actions betray words",
            "body language contradicts", "does opposite of what says",
            # Portuguese
            "diz X mas faz Y", "palavras contradizem ações", "ações traem palavras",
            "linguagem corporal contradiz", "faz o oposto do que diz"
        ]

        # Visual subtext markers
        self.visual_subtext_markers = [
            # English
            "body language", "facial expression", "gesture reveals", "eyes show",
            "posture indicates", "look says", "expression betrays", "face reveals",
            # Portuguese
            "linguagem corporal", "expressão facial", "gesto revela", "olhos mostram",
            "postura indica", "olhar diz", "expressão trai", "rosto revela"
        ]

        # Hidden agenda markers
        self.hidden_agenda_markers = [
            # English
            "ulterior motive", "hidden agenda", "real reason", "true intention",
            "secret motive", "hidden purpose", "real agenda", "true goal",
            # Portuguese
            "motivo oculto", "agenda escondida", "razão real", "intenção verdadeira",
            "motivo secreto", "propósito oculto", "agenda real", "objetivo verdadeiro"
        ]

        # Avoidance markers
        self.avoidance_markers = [
            # English
            "deflects", "changes subject", "avoids topic", "sidesteps",
            "dodges question", "evades", "redirects", "won't discuss",
            # Portuguese
            "desvia", "muda de assunto", "evita tópico", "esquiva-se",
            "esquiva pergunta", "evade", "redireciona", "não vai discutir"
        ]

        # Denial markers
        self.denial_markers = [
            # English
            "denies", "suppresses", "won't admit", "refuses to acknowledge",
            "hides feeling", "buries emotion", "represses", "in denial",
            # Portuguese
            "nega", "suprime", "não admite", "recusa-se a reconhecer",
            "esconde sentimento", "enterra emoção", "reprime", "em negação"
        ]

        # Irony markers
        self.irony_markers = [
            # English
            "irony", "sarcasm", "says opposite", "ironic", "sarcastic",
            "tongue in cheek", "mock", "sardonic", "wry",
            # Portuguese
            "ironia", "sarcasmo", "diz o oposto", "irônico", "sarcástico",
            "língua na bochecha", "zomba", "sardônico", "mordaz"
        ]

        # On-the-nose markers (PENALTY)
        self.on_the_nose_markers = [
            # English
            "on-the-nose", "too explicit", "states obvious", "expositional",
            "tells instead of shows", "spells it out", "explains feelings",
            "I feel", "I think", "I believe", "I want", "I need",
            # Portuguese
            "explícito demais", "óbvio", "expositório", "conta ao invés de mostrar",
            "soletra", "explica sentimentos", "eu sinto", "eu penso",
            "eu acredito", "eu quero", "eu preciso"
        ]

        # Layered meaning markers
        self.layered_meaning_markers = [
            # English
            "multiple meanings", "layered", "levels of meaning", "depth",
            "surface and subtext", "rich meaning", "complex", "nuanced",
            # Portuguese
            "múltiplos significados", "em camadas", "níveis de significado", "profundidade",
            "superfície e subtexto", "significado rico", "complexo", "nuançado"
        ]

        # Implication markers
        self.implication_markers = [
            # English
            "implies", "suggests", "hints", "insinuates", "alludes",
            "intimates", "indicates", "infers", "implication", "inference",
            # Portuguese
            "implica", "sugere", "insinua", "alude", "intima",
            "indica", "infere", "implicação", "inferência"
        ]

        # Emotional subtext markers
        self.emotional_subtext_markers = [
            # English
            "hidden feelings", "true emotions", "beneath surface emotion",
            "masks feeling", "hides emotion", "emotional truth",
            # Portuguese
            "sentimentos ocultos", "emoções verdadeiras", "emoção sob superfície",
            "mascara sentimento", "esconde emoção", "verdade emocional"
        ]

        # Power dynamics markers
        self.power_dynamics_markers = [
            # English
            "power dynamic", "hierarchy", "dominance", "submission",
            "unspoken power", "subtle control", "manipulation",
            # Portuguese
            "dinâmica de poder", "hierarquia", "dominância", "submissão",
            "poder não dito", "controle sutil", "manipulação"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze subtext in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete subtext diagnostic report
        """
        # Extract page count and scenes
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)

        # Detect subtext moments
        subtext_moments = self._detect_subtext_moments(screenplay_text)

        # Detect on-the-nose dialogue (PENALTY)
        on_the_nose = self._detect_on_the_nose(screenplay_text)

        # Analyze says vs means
        says_vs_means = self._analyze_says_vs_means(screenplay_text)

        # Analyze silence and pauses
        silence_pauses = self._analyze_silence_pauses(screenplay_text)

        # Analyze action-word contradiction
        action_contradiction = self._analyze_action_word_contradiction(screenplay_text)

        # Analyze visual subtext
        visual_subtext = self._analyze_visual_subtext(screenplay_text)

        # Detect hidden agendas
        hidden_agendas = self._detect_hidden_agendas(screenplay_text)

        # Detect avoidance/deflection
        avoidance_deflection = self._detect_avoidance_deflection(screenplay_text)

        # Detect denial/suppression
        denial_suppression = self._detect_denial_suppression(screenplay_text)

        # Detect irony/sarcasm
        irony_sarcasm = self._detect_irony_sarcasm(screenplay_text)

        # Assess layered meaning
        layered_meaning = self._assess_layered_meaning(screenplay_text)

        # Analyze emotional subtext
        emotional_subtext = self._analyze_emotional_subtext(screenplay_text)

        # Analyze power dynamics
        power_dynamics = self._analyze_power_subtext(screenplay_text)

        # Assess subtext sophistication
        subtext_sophistication = self._assess_subtext_sophistication(screenplay_text)

        # Assess subtext consistency
        subtext_consistency = self._assess_subtext_consistency(screenplay_text, scenes)

        # Analyze reading between lines
        reading_between_lines = self._analyze_reading_between_lines(screenplay_text)

        # Analyze implication/inference
        implication_inference = self._analyze_implication_inference(screenplay_text)

        # Build subtext profile
        subtext_profile = SubtextProfile(
            subtext_moments_count=subtext_moments["count"],
            on_the_nose_count=on_the_nose["count"],
            says_vs_means_ratio=says_vs_means["ratio"],
            silence_pause_count=silence_pauses["count"],
            action_contradiction_count=action_contradiction["count"],
            visual_subtext_score=visual_subtext["score"],
            hidden_agenda_count=hidden_agendas["count"],
            avoidance_deflection_count=avoidance_deflection["count"],
            denial_suppression_count=denial_suppression["count"],
            irony_sarcasm_count=irony_sarcasm["count"],
            layered_meaning_score=layered_meaning["score"],
            emotional_subtext_score=emotional_subtext["score"],
            power_dynamics_score=power_dynamics["score"],
            subtext_sophistication=subtext_sophistication["sophistication"],
            subtext_consistency=subtext_consistency["consistency"],
            overall_subtext_quality=0.0,  # calculated below
            reading_between_lines_score=reading_between_lines["score"],
            implication_inference_score=implication_inference["score"],
            surface_vs_depth_ratio=says_vs_means["ratio"],
            subtext_richness=0.0  # calculated below
        )

        # Calculate overall subtext quality
        subtext_profile.overall_subtext_quality = self._calculate_overall_subtext_quality(subtext_profile)
        subtext_profile.subtext_richness = self._calculate_subtext_richness(subtext_profile)

        # Check against rules
        rule_violations = self._check_subtext_rules(
            subtext_profile, subtext_moments, on_the_nose,
            says_vs_means, layered_meaning, subtext_sophistication,
            subtext_consistency
        )

        # Calculate score
        score = self._calculate_subtext_score(
            subtext_profile, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, subtext_profile, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "subtext_moments": {
                "count": subtext_moments["count"],
                "present": subtext_moments.get("present", False),
                "quality": subtext_moments.get("quality", "medium"),
                "examples": subtext_moments.get("examples", [])[:3]
            },
            "on_the_nose": {
                "count": on_the_nose["count"],
                "penalty": on_the_nose.get("penalty", False),
                "examples": on_the_nose.get("examples", [])[:3]
            },
            "says_vs_means": {
                "ratio": says_vs_means["ratio"],
                "healthy": says_vs_means.get("healthy", False),
                "count": says_vs_means.get("count", 0)
            },
            "silence_pauses": {
                "count": silence_pauses["count"],
                "effective": silence_pauses.get("effective", False),
                "examples": silence_pauses.get("examples", [])[:2]
            },
            "action_contradiction": {
                "count": action_contradiction["count"],
                "present": action_contradiction["count"] > 0,
                "examples": action_contradiction.get("examples", [])[:2]
            },
            "visual_subtext": {
                "score": visual_subtext["score"],
                "present": visual_subtext.get("present", False),
                "examples": visual_subtext.get("examples", [])[:2]
            },
            "hidden_agendas": {
                "count": hidden_agendas["count"],
                "present": hidden_agendas["count"] > 0,
                "examples": hidden_agendas.get("examples", [])[:2]
            },
            "avoidance_deflection": {
                "count": avoidance_deflection["count"],
                "present": avoidance_deflection["count"] > 0
            },
            "denial_suppression": {
                "count": denial_suppression["count"],
                "present": denial_suppression["count"] > 0
            },
            "irony_sarcasm": {
                "count": irony_sarcasm["count"],
                "present": irony_sarcasm["count"] > 0,
                "examples": irony_sarcasm.get("examples", [])[:2]
            },
            "layered_meaning": {
                "score": layered_meaning["score"],
                "present": layered_meaning.get("present", False),
                "sophistication": layered_meaning.get("sophistication", "medium")
            },
            "emotional_subtext": {
                "score": emotional_subtext["score"],
                "present": emotional_subtext.get("present", False),
                "strong": emotional_subtext.get("strong", False)
            },
            "power_dynamics": {
                "score": power_dynamics["score"],
                "present": power_dynamics.get("present", False),
                "examples": power_dynamics.get("examples", [])[:2]
            },
            "subtext_sophistication": {
                "sophistication": subtext_sophistication["sophistication"],
                "level": subtext_sophistication.get("level", "medium"),
                "quality": subtext_sophistication.get("quality", "medium")
            },
            "subtext_consistency": {
                "consistency": subtext_consistency["consistency"],
                "sustained": subtext_consistency.get("sustained", False),
                "act_breakdown": subtext_consistency.get("by_act", {})
            },
            "reading_between_lines": {
                "score": reading_between_lines["score"],
                "present": reading_between_lines.get("present", False),
                "quality": reading_between_lines.get("quality", "medium")
            },
            "implication_inference": {
                "score": implication_inference["score"],
                "present": implication_inference.get("present", False),
                "count": implication_inference.get("count", 0)
            },
            "overall_subtext_quality": subtext_profile.overall_subtext_quality,
            "subtext_richness": subtext_profile.subtext_richness,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, subtext_profile
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

    def _detect_subtext_moments(self, screenplay: str) -> Dict[str, Any]:
        """
        Identify rich subtext moments.

        McKee: "The essence of dialogue is SUBTEXT - characters rarely say what they mean."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            # Check for subtext patterns
            for marker in self.subtext_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        present = count >= 3

        # Determine quality
        if count >= 10:
            quality = "excellent"
        elif count >= 6:
            quality = "good"
        elif count >= 3:
            quality = "adequate"
        else:
            quality = "poor"

        return {
            "count": count,
            "present": present,
            "quality": quality,
            "examples": examples
        }

    def _detect_on_the_nose(self, screenplay: str) -> Dict[str, Any]:
        """
        Flag explicit expositional dialogue (PENALTY).

        McKee: "On-the-nose dialogue is bad - characters stating emotions/intentions explicitly."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            # Check for on-the-nose patterns
            for marker in self.on_the_nose_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Penalty if excessive
        penalty = count >= 5

        return {
            "count": count,
            "penalty": penalty,
            "examples": examples
        }

    def _analyze_says_vs_means(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze words vs actual intent.

        McKee: "Best dialogue says one thing, means another."
        """
        # Count says vs means markers
        count = 0
        for marker in self.says_vs_means_markers:
            count += screenplay.lower().count(marker)

        # Calculate ratio (0-1, higher is better)
        ratio = min(1.0, count / 8.0)

        healthy = ratio >= 0.5

        return {
            "ratio": ratio,
            "healthy": healthy,
            "count": count
        }

    def _analyze_silence_pauses(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze what's not said.

        McKee: "Silence and pauses create subtext - what characters don't say is powerful."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.silence_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        effective = count >= 3

        return {
            "count": count,
            "effective": effective,
            "examples": examples
        }

    def _analyze_action_word_contradiction(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze actions that contradict words.

        McKee: "When actions contradict words, actions reveal truth - powerful subtext."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.action_contradiction_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        return {
            "count": count,
            "examples": examples
        }

    def _analyze_visual_subtext(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze body language and visual cues.

        Mackendrick: "Visual subtext - body language, expressions reveal truth."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.visual_subtext_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Calculate score (0-1)
        score = min(1.0, count / 10.0)

        present = count >= 3

        return {
            "score": score,
            "present": present,
            "count": count,
            "examples": examples
        }

    def _detect_hidden_agendas(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect ulterior motives.

        Truby: "Hidden agendas create subtext - character wants one thing, says another."
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.hidden_agenda_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        return {
            "count": count,
            "examples": examples
        }

    def _detect_avoidance_deflection(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect topic avoidance.

        Subtext through what character avoids discussing.
        """
        count = 0

        for marker in self.avoidance_markers:
            count += screenplay.lower().count(marker)

        return {
            "count": count
        }

    def _detect_denial_suppression(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect when character won't admit truth.

        Subtext through denial - what character refuses to acknowledge.
        """
        count = 0

        for marker in self.denial_markers:
            count += screenplay.lower().count(marker)

        return {
            "count": count
        }

    def _detect_irony_sarcasm(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect saying opposite of what's meant.

        Irony/sarcasm creates subtext - literal opposite of intended meaning.
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.irony_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        return {
            "count": count,
            "examples": examples
        }

    def _assess_layered_meaning(self, screenplay: str) -> Dict[str, Any]:
        """
        Assess multiple interpretation levels.

        Sophisticated subtext = multiple layers of meaning.
        """
        count = 0

        for marker in self.layered_meaning_markers:
            count += screenplay.lower().count(marker)

        # Calculate score (0-1)
        score = min(1.0, count / 8.0)

        present = count >= 3

        # Determine sophistication
        if score >= 0.7:
            sophistication = "excellent"
        elif score >= 0.5:
            sophistication = "good"
        elif score >= 0.3:
            sophistication = "adequate"
        else:
            sophistication = "poor"

        return {
            "score": score,
            "present": present,
            "sophistication": sophistication,
            "count": count
        }

    def _analyze_emotional_subtext(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze true feelings hidden beneath surface.

        Emotional subtext = feelings character hides or won't admit.
        """
        count = 0

        for marker in self.emotional_subtext_markers:
            count += screenplay.lower().count(marker)

        # Calculate score (0-1)
        score = min(1.0, count / 8.0)

        present = count >= 3
        strong = score >= 0.6

        return {
            "score": score,
            "present": present,
            "strong": strong,
            "count": count
        }

    def _analyze_power_subtext(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze unspoken hierarchy and power dynamics.

        Power subtext = unspoken dominance, submission, manipulation.
        """
        count = 0
        examples = []

        for line in screenplay.split('\n'):
            for marker in self.power_dynamics_markers:
                if marker in line.lower():
                    count += 1
                    if len(examples) < 5:
                        examples.append(line.strip()[:100])
                    break

        # Calculate score (0-1)
        score = min(1.0, count / 6.0)

        present = count >= 2

        return {
            "score": score,
            "present": present,
            "count": count,
            "examples": examples
        }

    def _assess_subtext_sophistication(self, screenplay: str) -> Dict[str, Any]:
        """
        Assess quality of subtext.

        Sophisticated subtext = layered, nuanced, rich with meaning.
        """
        # Count various subtext techniques
        subtext_count = sum(1 for marker in self.subtext_markers if marker in screenplay.lower())
        layered_count = sum(1 for marker in self.layered_meaning_markers if marker in screenplay.lower())
        implication_count = sum(1 for marker in self.implication_markers if marker in screenplay.lower())

        # Calculate sophistication (0-1)
        total = subtext_count + layered_count + implication_count
        sophistication = min(1.0, total / 20.0)

        # Determine level
        if sophistication >= 0.7:
            level = "excellent"
            quality = "sophisticated"
        elif sophistication >= 0.5:
            level = "good"
            quality = "solid"
        elif sophistication >= 0.3:
            level = "adequate"
            quality = "basic"
        else:
            level = "poor"
            quality = "weak"

        return {
            "sophistication": sophistication,
            "level": level,
            "quality": quality
        }

    def _assess_subtext_consistency(self, screenplay: str, scenes: List[Dict]) -> Dict[str, Any]:
        """
        Assess subtext throughout script.

        Subtext should be consistent across all acts - not sporadic.
        """
        if not scenes:
            return {
                "consistency": 0.0,
                "sustained": False,
                "by_act": {}
            }

        # Count subtext markers by act
        total_scenes = len(scenes)
        act1_end = total_scenes // 4
        act2_end = 3 * total_scenes // 4

        act1_subtext = 0
        act2_subtext = 0
        act3_subtext = 0

        for i, scene in enumerate(scenes):
            scene_text = '\n'.join(scene['content'])
            subtext_count = sum(1 for marker in self.subtext_markers if marker in scene_text.lower())

            if i < act1_end:
                act1_subtext += subtext_count
            elif i < act2_end:
                act2_subtext += subtext_count
            else:
                act3_subtext += subtext_count

        # Calculate average subtext per act
        act1_avg = act1_subtext / max(1, act1_end) if act1_end > 0 else 0
        act2_avg = act2_subtext / max(1, act2_end - act1_end) if (act2_end - act1_end) > 0 else 0
        act3_avg = act3_subtext / max(1, total_scenes - act2_end) if (total_scenes - act2_end) > 0 else 0

        # Overall average
        overall_avg = (act1_avg + act2_avg + act3_avg) / 3.0

        # Consistent if all acts have reasonable subtext
        sustained = act1_avg >= 0.5 and act2_avg >= 0.5 and act3_avg >= 0.5

        # Calculate consistency (0-1)
        consistency = min(1.0, overall_avg / 2.0)

        return {
            "consistency": consistency,
            "sustained": sustained,
            "by_act": {
                "act1": act1_avg,
                "act2": act2_avg,
                "act3": act3_avg
            }
        }

    def _analyze_reading_between_lines(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze how much audience must infer.

        Good subtext requires audience to read between lines.
        """
        # Count implication/inference markers
        count = 0
        for marker in self.implication_markers:
            count += screenplay.lower().count(marker)

        # Calculate score (0-1)
        score = min(1.0, count / 10.0)

        present = count >= 3

        # Determine quality
        if score >= 0.7:
            quality = "excellent"
        elif score >= 0.5:
            quality = "good"
        elif score >= 0.3:
            quality = "adequate"
        else:
            quality = "poor"

        return {
            "score": score,
            "present": present,
            "quality": quality,
            "count": count
        }

    def _analyze_implication_inference(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze use of implication rather than statement.

        Sophisticated writing implies rather than states explicitly.
        """
        count = 0

        for marker in self.implication_markers:
            count += screenplay.lower().count(marker)

        # Calculate score (0-1)
        score = min(1.0, count / 10.0)

        present = count >= 3

        return {
            "score": score,
            "present": present,
            "count": count
        }

    def _calculate_overall_subtext_quality(self, profile: SubtextProfile) -> float:
        """Calculate overall subtext quality score."""
        scores = [
            1.0 if profile.subtext_moments_count >= 3 else 0.0,
            max(0.0, 1.0 - (profile.on_the_nose_count / 10.0)),  # PENALTY for on-the-nose
            profile.says_vs_means_ratio,
            min(1.0, profile.silence_pause_count / 5.0),
            min(1.0, profile.action_contradiction_count / 3.0),
            profile.visual_subtext_score,
            min(1.0, profile.hidden_agenda_count / 4.0),
            min(1.0, profile.avoidance_deflection_count / 4.0),
            min(1.0, profile.irony_sarcasm_count / 3.0),
            profile.layered_meaning_score,
            profile.emotional_subtext_score,
            profile.subtext_sophistication,
            profile.subtext_consistency
        ]

        # Average
        overall = sum(scores) / len(scores)

        return max(0.0, min(1.0, overall))

    def _calculate_subtext_richness(self, profile: SubtextProfile) -> float:
        """Calculate subtext richness (variety of techniques used)."""
        techniques_used = 0

        if profile.subtext_moments_count >= 3:
            techniques_used += 1
        if profile.says_vs_means_ratio >= 0.3:
            techniques_used += 1
        if profile.silence_pause_count >= 2:
            techniques_used += 1
        if profile.action_contradiction_count >= 1:
            techniques_used += 1
        if profile.visual_subtext_score >= 0.3:
            techniques_used += 1
        if profile.hidden_agenda_count >= 1:
            techniques_used += 1
        if profile.avoidance_deflection_count >= 2:
            techniques_used += 1
        if profile.denial_suppression_count >= 2:
            techniques_used += 1
        if profile.irony_sarcasm_count >= 1:
            techniques_used += 1
        if profile.layered_meaning_score >= 0.3:
            techniques_used += 1
        if profile.emotional_subtext_score >= 0.3:
            techniques_used += 1
        if profile.power_dynamics_score >= 0.3:
            techniques_used += 1

        # Richness = variety of techniques (0-1)
        richness = techniques_used / 12.0

        return max(0.0, min(1.0, richness))

    def _check_subtext_rules(self, profile: SubtextProfile, subtext_moments: Dict,
                            on_the_nose: Dict, says_vs_means: Dict,
                            layered_meaning: Dict, subtext_sophistication: Dict,
                            subtext_consistency: Dict) -> List[Dict]:
        """Check subtext against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "SUBTEXT.R001":
                # Subtext Present
                if profile.subtext_moments_count < 3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Subtext weak or absent - flat dialogue",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R002":
                # Avoid On-The-Nose Dialogue
                if profile.on_the_nose_count >= 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"On-the-nose dialogue present ({profile.on_the_nose_count} instances) - too explicit",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R003":
                # Layered Meaning
                if profile.layered_meaning_score < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Layered meaning weak - single-level interpretation",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R004":
                # Says vs Means
                if profile.says_vs_means_ratio < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Says vs means weak - characters say exactly what they mean",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R005":
                # Action Contradicts Words
                if profile.action_contradiction_count < 1:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No action-word contradiction - missing powerful subtext technique",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R006":
                # Silence and Pauses
                if profile.silence_pause_count < 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Insufficient silence/pauses - what's NOT said creates subtext",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R007":
                # Visual Subtext
                if profile.visual_subtext_score < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Visual subtext weak - body language reveals truth",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R008":
                # Hidden Agenda/Motives
                if profile.hidden_agenda_count < 1:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No hidden agendas - characters too transparent",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R009":
                # Avoidance/Deflection
                if profile.avoidance_deflection_count < 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No avoidance/deflection - characters too direct",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R010":
                # Denial/Suppression
                if profile.denial_suppression_count < 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No denial/suppression - characters admit everything",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R011":
                # Irony/Sarcasm
                # Low priority - not required
                pass

            elif rule["id"] == "SUBTEXT.R012":
                # Reading Between Lines
                if profile.reading_between_lines_score < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Reading between lines weak - too literal",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R013":
                # Emotional Truth Beneath Surface
                if profile.emotional_subtext_score < 0.3:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Emotional subtext weak - surface emotions only",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R014":
                # Sophisticated Subtext
                if profile.subtext_sophistication < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Subtext sophistication low - basic or absent",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SUBTEXT.R015":
                # Subtext Consistency
                if profile.subtext_consistency < 0.4:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Subtext not sustained - sporadic or inconsistent",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_subtext_score(self, profile: SubtextProfile, violations: List) -> float:
        """Calculate overall subtext score."""
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

        # Extra penalty for on-the-nose dialogue
        if profile.on_the_nose_count >= 5:
            score -= (profile.on_the_nose_count - 4) * 2  # -2 per extra instance

        # Bonus for excellence
        if profile.overall_subtext_quality > 0.8:
            score += 5
        elif profile.overall_subtext_quality > 0.7:
            score += 3

        if profile.subtext_sophistication > 0.7:
            score += 3

        if profile.says_vs_means_ratio > 0.6:
            score += 3

        if profile.subtext_richness > 0.7:
            score += 2

        if profile.subtext_consistency > 0.6 and profile.subtext_moments_count >= 5:
            score += 2

        # Cap at 95
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profile: SubtextProfile,
                          violations: List) -> str:
        """Generate subtext diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Subtext is rich, layered, and sophisticated"
        elif score >= 60:
            level = "GOOD"
            summary = "Subtext present but could be richer"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Subtext weak or inconsistent"
        else:
            level = "POOR"
            summary = "Major subtext problems - flat, on-the-nose dialogue"

        diagnosis = f"SUBTEXT {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if profile.on_the_nose_count >= 5:
            issues.append(f"on-the-nose dialogue ({profile.on_the_nose_count})")
        if profile.says_vs_means_ratio < 0.3:
            issues.append("characters say exactly what they mean")
        if profile.subtext_moments_count < 3:
            issues.append("weak subtext")
        if profile.layered_meaning_score < 0.3:
            issues.append("no layered meaning")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 profile: SubtextProfile) -> List[str]:
        """Generate specific subtext recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if profile.on_the_nose_count >= 5:
            recommendations.append("Eliminate on-the-nose dialogue - McKee: 'Characters rarely say what they mean'")

        if profile.says_vs_means_ratio < 0.3:
            recommendations.append("Create gap between words and intent - McKee: 'Best dialogue says one thing, means another'")

        if profile.subtext_moments_count < 3:
            recommendations.append("Add rich subtext throughout - McKee Dialogue: 'The essence of dialogue is SUBTEXT'")

        if profile.silence_pause_count < 2:
            recommendations.append("Use silence and pauses - what's NOT said creates powerful subtext")

        if profile.visual_subtext_score < 0.3:
            recommendations.append("Add visual subtext - body language, expressions reveal truth (Mackendrick)")

        if profile.layered_meaning_score < 0.3:
            recommendations.append("Create layered meaning - multiple levels of interpretation")

        if profile.subtext_sophistication < 0.4:
            recommendations.append("Increase sophistication - rich subtext engages audience as detective")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study McKee's Dialogue - entire book dedicated to subtext as essence of dialogue")
            recommendations.append("Study McKee's Story - subtext is gap between what character says and truth")

        return recommendations[:5]

    def export_subtext_features(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Export subtext features for correlation/analysis.

        Returns structured data with subtext metrics.
        Useful for external indexing, correlation engines, or ML pipelines.

        Args:
            screenplay_text: Full screenplay text

        Returns:
            Dict with subtext metrics
        """
        subtext_moments = self._detect_subtext_moments(screenplay_text)
        on_the_nose = self._detect_on_the_nose(screenplay_text)
        says_vs_means = self._analyze_says_vs_means(screenplay_text)
        layered_meaning = self._assess_layered_meaning(screenplay_text)

        return {
            "subtext_moments": {
                "count": subtext_moments["count"],
                "present": subtext_moments.get("present", False)
            },
            "on_the_nose": {
                "count": on_the_nose["count"],
                "penalty": on_the_nose.get("penalty", False)
            },
            "says_vs_means": {
                "ratio": says_vs_means["ratio"],
                "healthy": says_vs_means.get("healthy", False)
            },
            "layered_meaning": {
                "score": layered_meaning["score"],
                "present": layered_meaning.get("present", False)
            },
            "meta": {
                "source": "DrSubtext",
                "focus": "Subtext and layered meaning"
            }
        }


# Compatibility class for testing framework
class DrSubtextAnalysis(DrSubtext):
    """Alias for compatibility with test framework."""
    pass
