"""
Script Doctor Foreshadowingmon - Foreshadowing and Setup/Payoff Analysis Specialist
A Script Doctor™ in Digimon form specializing in foreshadowing, setup/payoff, Chekhov's gun, dramatic irony, plant/reveal technique.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class ForeshadowingProfile:
    """Overall foreshadowing analysis."""
    foreshadowing_present: bool  # Setup hints for future events
    setup_payoff_detected: bool  # Plants have payoffs (Chekhov's gun)
    plant_timing: bool  # Early setup for later payoff (Field)
    payoff_effectiveness: bool  # Satisfying reveal/resolution
    dramatic_irony_present: bool  # Audience knows more than characters
    visual_foreshadowing: bool  # Symbolic hints (visual storytelling)
    dialogue_foreshadowing: bool  # Verbal clues/hints
    misdirection_used: bool  # Hide clues in plain sight
    setup_distance: bool  # Adequate pages between plant and payoff
    inevitability_balance: bool  # Aristotle: surprise yet inevitable
    unfired_gun_detected: bool  # PENALTY (setup without payoff)
    deus_ex_machina_detected: bool  # PENALTY (payoff without setup)
    telegraphed_twist_detected: bool  # PENALTY (too obvious foreshadowing)
    overall_foreshadowing_quality: float


@dataclass
class ForeshadowingAnalysisResults:
    """Complete foreshadowing analysis results."""
    foreshadowing_profile: ForeshadowingProfile
    foreshadowing_moments: List[str]  # Moments of foreshadowing
    setup_list: List[str]  # Setup/plant moments
    payoff_list: List[str]  # Payoff/reveal moments
    dramatic_irony_list: List[str]  # Dramatic irony moments
    visual_foreshadowing_list: List[str]  # Visual hints
    misdirection_list: List[str]  # Misdirection moments
    unfired_guns: List[str]  # Setup without payoff (PENALTY)
    deus_ex_machina_list: List[str]  # Payoff without setup (PENALTY)
    score: float
    diagnosis: str
    recommendations: List[str]


class DrForeshadowing:
    """
    Script Doctor Foreshadowingmon - The Foreshadowing and Setup/Payoff Analysis Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing foreshadowing, setup/payoff,
    Chekhov's gun principle, dramatic irony, plant/reveal technique, avoid unfired guns and deus ex machina.

    Identity: Script Doctor first, Digimon foreshadowing specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Foreshadowingmon with rules and configuration."""
        self.name = "Script Doctor Foreshadowingmon"
        self.digimon_name = "Foreshadowingmon"
        self.title = "Script Doctor - Foreshadowing and Setup/Payoff Analysis Specialist"
        self.specialty = "Foreshadowing, setup/payoff, Chekhov's gun, dramatic irony, plant/reveal, avoid unfired guns and deus ex machina"
        self.identity = "I am Script Doctor Foreshadowingmon, a professional Script Doctor™ specializing in foreshadowing and setup/payoff analysis"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "foreshadowing_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - FORESHADOWING SPECIFIC
        self.deep_context_queries = [
            "McKee Story foreshadowing setup payoff",
            "McKee Story plant and reveal technique",
            "McKee Story setup early payoff later",
            "McKee Story dramatic irony audience knows",
            "McKee Story inevitability versus surprise",
            "McKee Story foreshadowing subtle hints",
            "McKee Story setup distance timing",
            "McKee Story payoff must be earned",
            "McKee Story foreshadowing through visual",
            "McKee Story Chekhov's gun principle",

            # McKee Story - FORESHADOWING & OBLIGATORY SCENE (ultra-specific manual reading)
            "McKee Story foreshadowing arrangement early events prepare later events",
            "McKee Story every choice genre setting character mood foreshadows",
            "McKee Story foreshadowing guide audience anticipate possibilities satisfy expectations",
            "McKee Story foreshadowing primary component projection obligatory scene crisis inciting incident",
            "McKee Story setup payoff planting information early harvesting later callback",

            "Syd Field Screenplay setup payoff structure",
            "Field plant early payoff later",
            "Field setup first act payoff third",
            "Field foreshadowing structural design",
            "Field setup distance between plant payoff",
            "Blake Snyder Save the Cat setup payoff",
            "Snyder plant in setup payoff climax",
            "Snyder foreshadowing beats structure",
            "Snyder save the cat plant reveal",
            "John Truby Anatomy foreshadowing revelation",
            "Truby revelation sequence building",
            "Truby foreshadowing strategic placement",
            "Truby setup payoff revelation design",
            "Truby dramatic irony character knowledge",
            "Truby inevitability foreshadowing design",
            "Christopher Vogler Writer's Journey foreshadowing",
            "Vogler foreshadowing mythic structure",
            "Vogler mentor's gift setup payoff",
            "Vogler ordeal foreshadowed preparation",
            "Joseph Campbell Hero 1000 Faces foreshadowing",
            "Campbell mythic foreshadowing prophecy",
            "Campbell hero journey foreshadowed stages",
            "Aristotle Poetics peripeteia reversal inevitable",
            "Aristotle anagnorisis recognition foreshadowed",
            "Aristotle inevitability versus surprise balance",
            "Aristotle foreshadowing necessary probable",
            "Linda Seger Making Good Script Great foreshadowing",
            "Seger setup payoff rewriting technique",
            "Seger plant reveal screenplay structure",
            "Seger foreshadowing subtle obvious",
            "Lajos Egri Art Dramatic Writing foreshadowing",
            "Egri premise foreshadows ending",
            "Egri inevitability dramatic structure",
            "William Goldman Adventures Screen Trade foreshadowing",
            "Goldman setup payoff screenplay craft",
            "Shonda Rhimes foreshadowing television storytelling",
            "David Mamet foreshadowing dramatic action",
            "Alexander Mackendrick foreshadowing visual storytelling",
            "K.M. Weiland Creating Character Arcs foreshadowing",
            "Weiland foreshadowing character transformation",
            "Weiland lie truth foreshadowed arc",
            "foreshadowing setup payoff Chekhov's gun",
            "plant early reveal later dramatic structure",
            "dramatic irony audience knows character doesn't",
            "inevitability surprise Aristotle reversal",
            "visual foreshadowing symbolic hints imagery",
            "misdirection hide clues plain sight",
            "unfired gun setup without payoff penalty",
            "deus ex machina payoff without setup penalty",
            "telegraphed twist too obvious foreshadowing"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story foreshadowing inciting incident projects obligatory scene image",
        "McKee Story setup payoff planted knowledge closes gap turning point",
        "McKee Story foreshadow image motif seed audience unconscious expectation",
        "McKee Story prepare ironic payoff plant contrary cues opposing charges",

        ]

        # Foreshadowing analysis patterns (bilingual: EN + PT) - 150-170+ markers

        # Foreshadowing present markers (hints of future events)
        self.foreshadowing_present_markers = [
            # English
            "will return", "this will matter", "you'll see", "mark my words", "remember this",
            "one day", "someday", "eventually", "in time", "later", "soon enough",
            "if only", "little did", "had no idea", "didn't know yet", "unaware that",
            "prophesy", "prophecy", "foretold", "predicted", "omen", "sign", "warning",
            "foreshadow", "hint", "clue", "suggestion", "portent",
            # Portuguese
            "vai voltar", "isso vai importar", "você vai ver", "marque minhas palavras", "lembre-se disso",
            "um dia", "algum dia", "eventualmente", "com o tempo", "mais tarde", "em breve",
            "se ao menos", "mal sabia", "não tinha ideia", "ainda não sabia", "sem saber que",
            "profecia", "profetizado", "previsto", "pressagiado", "presságio", "sinal", "aviso",
            "prenúncio", "pista", "indício", "sugestão", "augúrio"
        ]

        # Setup/plant markers (early establishment)
        self.setup_plant_markers = [
            # English
            "establishes", "introduces", "sets up", "plants", "places", "mentions",
            "shows", "reveals", "displays", "demonstrates", "presents",
            "notices", "observes", "sees", "finds", "discovers",
            "receives", "gets", "obtains", "acquires", "given",
            "learns", "told about", "hears about", "informed",
            # Portuguese
            "estabelece", "introduz", "prepara", "planta", "coloca", "menciona",
            "mostra", "revela", "exibe", "demonstra", "apresenta",
            "nota", "observa", "vê", "encontra", "descobre",
            "recebe", "consegue", "obtém", "adquire", "dado",
            "aprende", "contado sobre", "ouve sobre", "informado"
        ]

        # Payoff/reveal markers (later resolution)
        self.payoff_reveal_markers = [
            # English
            "pays off", "reveals", "comes back", "returns", "resurfaces",
            "was right", "as predicted", "as foretold", "as warned",
            "finally", "at last", "in the end", "ultimately",
            "realizes", "understands", "recognizes", "remembers",
            "the clue", "the hint", "the sign", "the warning",
            "makes sense now", "explains", "connects", "fits together",
            # Portuguese
            "retorna", "revela", "volta", "retorna", "ressurge",
            "estava certo", "como previsto", "como profetizado", "como avisado",
            "finalmente", "enfim", "no final", "no fim",
            "percebe", "entende", "reconhece", "lembra",
            "a pista", "o indício", "o sinal", "o aviso",
            "faz sentido agora", "explica", "conecta", "se encaixa"
        ]

        # Dramatic irony markers (audience knows, character doesn't)
        self.dramatic_irony_markers = [
            # English
            "unaware", "doesn't know", "has no idea", "oblivious",
            "if only knew", "little does know", "unknowingly",
            "audience knows", "we see but", "viewer knows",
            "secretly", "hidden from", "concealed", "behind back",
            "irony", "tragic irony", "dramatic irony",
            # Portuguese
            "desconhece", "não sabe", "não tem ideia", "alheio",
            "se ao menos soubesse", "mal sabe", "inconscientemente",
            "público sabe", "vemos mas", "espectador sabe",
            "secretamente", "escondido de", "oculto", "pelas costas",
            "ironia", "ironia trágica", "ironia dramática"
        ]

        # Visual foreshadowing markers (symbolic hints)
        self.visual_foreshadowing_markers = [
            # English
            "symbol", "symbolic", "imagery", "metaphor", "motif",
            "visual hint", "visual clue", "visual metaphor",
            "foreshadows visually", "visual parallel", "echoes",
            "mirror", "reflection", "shadow", "omen",
            "photograph", "portrait", "painting", "picture shows",
            "weapon", "gun", "knife", "tool", "object",
            # Portuguese
            "símbolo", "simbólico", "imagem", "metáfora", "motivo",
            "pista visual", "indício visual", "metáfora visual",
            "prenuncia visualmente", "paralelo visual", "ecos",
            "espelho", "reflexo", "sombra", "presságio",
            "fotografia", "retrato", "pintura", "imagem mostra",
            "arma", "pistola", "faca", "ferramenta", "objeto"
        ]

        # Dialogue foreshadowing markers (verbal clues)
        self.dialogue_foreshadowing_markers = [
            # English
            "says", "mentions", "warns", "predicts", "suggests",
            "tells", "prophesies", "foretells", "hints at",
            "dialogue foreshadows", "verbal hint", "spoken clue",
            "cryptic", "ambiguous", "double meaning",
            "joke that", "offhand comment", "casual remark",
            # Portuguese
            "diz", "menciona", "avisa", "prevê", "sugere",
            "conta", "profetiza", "prenúncia", "insinua",
            "diálogo prenúncia", "pista verbal", "indício falado",
            "críptico", "ambíguo", "duplo sentido",
            "piada que", "comentário casual", "observação casual"
        ]

        # Misdirection markers (hide clues in plain sight)
        self.misdirection_markers = [
            # English
            "misdirection", "red herring", "distraction", "misleading",
            "appears to be", "seems like", "looks like", "suggests",
            "hidden in plain sight", "overlooked", "dismissed",
            "fake clue", "false lead", "deception", "trick",
            # Portuguese
            "desvio", "pista falsa", "distração", "enganoso",
            "parece ser", "parece como", "parece", "sugere",
            "escondido à vista", "ignorado", "descartado",
            "pista falsa", "pista errada", "engano", "truque"
        ]

        # Setup distance markers (pages between plant and payoff)
        self.setup_distance_markers = [
            # English
            "earlier", "previously", "before", "back when",
            "from the beginning", "from act one", "from the start",
            "pages ago", "scenes ago", "acts ago",
            "established earlier", "set up before",
            # Portuguese
            "antes", "anteriormente", "previamente", "quando",
            "do início", "do ato um", "do começo",
            "páginas atrás", "cenas atrás", "atos atrás",
            "estabelecido antes", "preparado antes"
        ]

        # Inevitability markers (Aristotle: surprise yet inevitable)
        self.inevitability_markers = [
            # English
            "inevitable", "had to happen", "was bound to", "destined",
            "makes sense", "logical", "follows naturally",
            "surprise but inevitable", "unexpected but logical",
            "set in motion", "chain of events", "consequences",
            # Portuguese
            "inevitável", "tinha que acontecer", "estava destinado", "destinado",
            "faz sentido", "lógico", "segue naturalmente",
            "surpresa mas inevitável", "inesperado mas lógico",
            "colocado em movimento", "cadeia de eventos", "consequências"
        ]

        # Chekhov's gun markers (every element used)
        self.chekhovs_gun_markers = [
            # English
            "Chekhov", "gun on wall", "every element", "everything matters",
            "nothing wasted", "all connects", "comes back",
            "planted early used later", "setup pays off",
            # Portuguese
            "Chekhov", "arma na parede", "cada elemento", "tudo importa",
            "nada desperdiçado", "tudo conecta", "volta",
            "plantado cedo usado depois", "preparação retorna"
        ]

        # Unfired gun markers (PENALTY - setup without payoff)
        self.unfired_gun_markers = [
            # English
            "unfired gun", "Chekhov violation", "setup without payoff",
            "never used", "never returns", "forgotten", "abandoned",
            "loose end", "unresolved", "dropped thread",
            "mentioned but never", "shown but never", "established but never",
            # Portuguese
            "arma não disparada", "violação Chekhov", "preparação sem retorno",
            "nunca usado", "nunca volta", "esquecido", "abandonado",
            "ponta solta", "não resolvido", "fio abandonado",
            "mencionado mas nunca", "mostrado mas nunca", "estabelecido mas nunca"
        ]

        # Deus ex machina markers (PENALTY - payoff without setup)
        self.deus_ex_machina_markers = [
            # English
            "deus ex machina", "out of nowhere", "convenient", "contrived",
            "suddenly appears", "magically", "coincidentally",
            "unearned", "not setup", "no foreshadowing",
            "saves the day", "solves problem", "resolves conflict",
            "random", "unexplained", "unjustified",
            # Portuguese
            "deus ex machina", "do nada", "conveniente", "forçado",
            "aparece de repente", "magicamente", "coincidentemente",
            "não merecido", "sem preparação", "sem prenúncio",
            "salva o dia", "resolve problema", "resolve conflito",
            "aleatório", "inexplicado", "injustificado"
        ]

        # Telegraphed twist markers (PENALTY - too obvious foreshadowing)
        self.telegraphed_twist_markers = [
            # English
            "too obvious", "telegraphed", "predictable", "saw coming",
            "heavy-handed", "on the nose", "spelled out",
            "overtly foreshadowed", "excessively hinted",
            "audience ahead", "no surprise", "expected",
            # Portuguese
            "muito óbvio", "telegrafado", "previsível", "viu vindo",
            "pesado", "na cara", "explícito demais",
            "prenunciado demais", "insinuado em excesso",
            "público à frente", "sem surpresa", "esperado"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze foreshadowing and setup/payoff in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete foreshadowing diagnostic report
        """
        # Extract page count and scenes
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)

        # Extract Act 1 (first 25%) for setup/plant
        act1_text = self._extract_pages(screenplay_text, 0, int(page_count * 0.25))

        # Extract Act 2 (middle 50%) for development
        act2_text = self._extract_pages(screenplay_text, int(page_count * 0.25), int(page_count * 0.75))

        # Extract Act 3 (final 25%) for payoff/reveal
        act3_text = self._extract_pages(screenplay_text, int(page_count * 0.75), page_count)

        # Analyze foreshadowing present (hints of future events)
        foreshadowing_present = self._analyze_foreshadowing_present(screenplay_text)

        # Analyze setup/payoff (plants have payoffs - Chekhov's gun)
        setup_payoff = self._analyze_setup_payoff(screenplay_text, act1_text, act2_text, act3_text)

        # Analyze plant timing (early setup for later payoff - Field)
        plant_timing = self._analyze_plant_timing(screenplay_text, act1_text, act3_text)

        # Analyze payoff effectiveness (satisfying reveal)
        payoff_effectiveness = self._analyze_payoff_effectiveness(screenplay_text, act3_text)

        # Analyze dramatic irony (audience knows more than characters)
        dramatic_irony = self._analyze_dramatic_irony(screenplay_text)

        # Analyze visual foreshadowing (symbolic hints)
        visual_foreshadowing = self._analyze_visual_foreshadowing(screenplay_text)

        # Analyze dialogue foreshadowing (verbal clues)
        dialogue_foreshadowing = self._analyze_dialogue_foreshadowing(screenplay_text)

        # Analyze misdirection (hide clues in plain sight)
        misdirection = self._analyze_misdirection(screenplay_text)

        # Analyze setup distance (adequate pages between plant and payoff)
        setup_distance = self._analyze_setup_distance(screenplay_text, page_count)

        # Analyze inevitability balance (Aristotle: surprise yet inevitable)
        inevitability = self._analyze_inevitability_balance(screenplay_text)

        # Detect unfired gun (PENALTY - setup without payoff)
        unfired_gun = self._detect_unfired_gun(screenplay_text, setup_payoff)

        # Detect deus ex machina (PENALTY - payoff without setup)
        deus_ex_machina = self._detect_deus_ex_machina(screenplay_text, setup_payoff)

        # Detect telegraphed twist (PENALTY - too obvious foreshadowing)
        telegraphed_twist = self._detect_telegraphed_twist(screenplay_text)

        # Build foreshadowing profile
        foreshadowing_profile = ForeshadowingProfile(
            foreshadowing_present=foreshadowing_present["present"],
            setup_payoff_detected=setup_payoff["detected"],
            plant_timing=plant_timing["good_timing"],
            payoff_effectiveness=payoff_effectiveness["effective"],
            dramatic_irony_present=dramatic_irony["present"],
            visual_foreshadowing=visual_foreshadowing["present"],
            dialogue_foreshadowing=dialogue_foreshadowing["present"],
            misdirection_used=misdirection["used"],
            setup_distance=setup_distance["adequate"],
            inevitability_balance=inevitability["balanced"],
            unfired_gun_detected=unfired_gun["detected"],
            deus_ex_machina_detected=deus_ex_machina["detected"],
            telegraphed_twist_detected=telegraphed_twist["detected"],
            overall_foreshadowing_quality=0.0  # calculated below
        )

        # Calculate overall foreshadowing quality
        foreshadowing_profile.overall_foreshadowing_quality = self._calculate_overall_foreshadowing_quality(foreshadowing_profile)

        # Check against rules
        rule_violations = self._check_foreshadowing_rules(
            foreshadowing_profile, foreshadowing_present, setup_payoff, plant_timing,
            payoff_effectiveness, dramatic_irony, visual_foreshadowing, dialogue_foreshadowing,
            misdirection, setup_distance, inevitability, unfired_gun, deus_ex_machina,
            telegraphed_twist
        )

        # Calculate score
        score = self._calculate_foreshadowing_score(foreshadowing_profile, rule_violations)

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, foreshadowing_profile, rule_violations)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "foreshadowing_present": {
                "present": foreshadowing_present["present"],
                "count": foreshadowing_present["count"],
                "moments": foreshadowing_present["moments"][:10]
            },
            "setup_payoff": {
                "detected": setup_payoff["detected"],
                "setup_count": setup_payoff["setup_count"],
                "payoff_count": setup_payoff["payoff_count"],
                "setup_list": setup_payoff["setup_list"][:10],
                "payoff_list": setup_payoff["payoff_list"][:10]
            },
            "plant_timing": {
                "good_timing": plant_timing["good_timing"],
                "act1_plants": plant_timing["act1_plants"],
                "act3_payoffs": plant_timing["act3_payoffs"]
            },
            "payoff_effectiveness": {
                "effective": payoff_effectiveness["effective"],
                "count": payoff_effectiveness["count"]
            },
            "dramatic_irony": {
                "present": dramatic_irony["present"],
                "count": dramatic_irony["count"],
                "list": dramatic_irony["list"][:10]
            },
            "visual_foreshadowing": {
                "present": visual_foreshadowing["present"],
                "count": visual_foreshadowing["count"],
                "list": visual_foreshadowing["list"][:10]
            },
            "dialogue_foreshadowing": {
                "present": dialogue_foreshadowing["present"],
                "count": dialogue_foreshadowing["count"]
            },
            "misdirection": {
                "used": misdirection["used"],
                "count": misdirection["count"],
                "list": misdirection["list"][:10]
            },
            "setup_distance": {
                "adequate": setup_distance["adequate"],
                "average_distance": setup_distance.get("average_distance", 0)
            },
            "inevitability": {
                "balanced": inevitability["balanced"],
                "count": inevitability["count"]
            },
            "unfired_gun": {
                "detected": unfired_gun["detected"],
                "penalty": unfired_gun.get("penalty", False),
                "count": unfired_gun["count"],
                "list": unfired_gun["list"][:5]
            },
            "deus_ex_machina": {
                "detected": deus_ex_machina["detected"],
                "penalty": deus_ex_machina.get("penalty", False),
                "count": deus_ex_machina["count"],
                "list": deus_ex_machina["list"][:5]
            },
            "telegraphed_twist": {
                "detected": telegraphed_twist["detected"],
                "penalty": telegraphed_twist.get("penalty", False),
                "count": telegraphed_twist["count"]
            },
            "overall_foreshadowing_quality": foreshadowing_profile.overall_foreshadowing_quality,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, foreshadowing_profile
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

    def _extract_pages(self, screenplay: str, start_page: int, end_page: int) -> str:
        """Extract specific page range from screenplay."""
        lines = screenplay.split('\n')
        start_line = start_page * 55
        end_line = end_page * 55
        return '\n'.join(lines[start_line:end_line])

    def _analyze_foreshadowing_present(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze foreshadowing present (hints of future events).

        McKee: "Foreshadowing creates anticipation - plant hints that pay off later."
        Field: "Setup early, payoff later - essential structural principle."
        """
        present = False
        moments = []

        # Check for foreshadowing markers
        count = 0
        for marker in self.foreshadowing_present_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract foreshadowing moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        moments.append(line.strip()[:100])
                        if len(moments) >= 20:
                            break

        if count >= 8:
            present = True
        elif count >= 5:
            present = True

        return {
            "present": present,
            "count": count,
            "moments": moments
        }

    def _analyze_setup_payoff(self, screenplay: str, act1_text: str, act2_text: str, act3_text: str) -> Dict[str, Any]:
        """
        Analyze setup/payoff (plants have payoffs - Chekhov's gun).

        Chekhov: "If gun on wall in Act 1, must fire by Act 3 - every element must be used."
        McKee: "Setup/payoff - everything planted must pay off, no unfired guns."
        """
        detected = False
        setup_list = []
        payoff_list = []

        # Check for setup/plant markers
        setup_count = 0
        for marker in self.setup_plant_markers:
            marker_count = screenplay.lower().count(marker)
            setup_count += marker_count
            if marker_count > 0 and len(setup_list) < 20:
                # Extract setup moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        setup_list.append(line.strip()[:100])
                        if len(setup_list) >= 20:
                            break

        # Check for payoff/reveal markers
        payoff_count = 0
        for marker in self.payoff_reveal_markers:
            marker_count = screenplay.lower().count(marker)
            payoff_count += marker_count
            if marker_count > 0 and len(payoff_list) < 20:
                # Extract payoff moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        payoff_list.append(line.strip()[:100])
                        if len(payoff_list) >= 20:
                            break

        # Chekhov's gun: setup and payoff should be balanced
        if setup_count >= 5 and payoff_count >= 3:
            detected = True
        elif setup_count >= 3 and payoff_count >= 2:
            detected = True

        return {
            "detected": detected,
            "setup_count": setup_count,
            "payoff_count": payoff_count,
            "setup_list": setup_list,
            "payoff_list": payoff_list
        }

    def _analyze_plant_timing(self, screenplay: str, act1_text: str, act3_text: str) -> Dict[str, Any]:
        """
        Analyze plant timing (early setup for later payoff - Field).

        Field: "Plant in Act 1, pay off in Act 3 - structural principle of setup/payoff distance."
        McKee: "Setup must be early enough that payoff feels earned not convenient."
        """
        good_timing = False

        # Check for plants in Act 1
        act1_plants = 0
        for marker in self.setup_plant_markers:
            act1_plants += act1_text.lower().count(marker)

        # Check for payoffs in Act 3
        act3_payoffs = 0
        for marker in self.payoff_reveal_markers:
            act3_payoffs += act3_text.lower().count(marker)

        # Good timing: plants in Act 1, payoffs in Act 3
        if act1_plants >= 5 and act3_payoffs >= 3:
            good_timing = True
        elif act1_plants >= 3 and act3_payoffs >= 2:
            good_timing = True

        return {
            "good_timing": good_timing,
            "act1_plants": act1_plants,
            "act3_payoffs": act3_payoffs
        }

    def _analyze_payoff_effectiveness(self, screenplay: str, act3_text: str) -> Dict[str, Any]:
        """
        Analyze payoff effectiveness (satisfying reveal/resolution).

        McKee: "Payoff must be earned - setup creates anticipation, payoff delivers satisfaction."
        Truby: "Revelation sequence - each reveal builds to ultimate payoff at climax."
        """
        effective = False

        # Check for payoff markers
        count = 0
        for marker in self.payoff_reveal_markers:
            count += screenplay.lower().count(marker)

        # Check for satisfaction markers (makes sense, explains, etc.)
        satisfaction_markers = ["makes sense", "explains", "now I understand", "finally", "at last"]
        satisfaction_count = 0
        for marker in satisfaction_markers:
            satisfaction_count += screenplay.lower().count(marker)

        if count >= 5 and satisfaction_count >= 2:
            effective = True
        elif count >= 3:
            effective = True

        return {
            "effective": effective,
            "count": count,
            "satisfaction_count": satisfaction_count
        }

    def _analyze_dramatic_irony(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze dramatic irony (audience knows more than characters).

        McKee: "Dramatic irony - audience knows what character doesn't, creates tension."
        Aristotle: "Irony heightens tragic effect - audience sees disaster approaching."
        """
        present = False
        irony_list = []

        # Check for dramatic irony markers
        count = 0
        for marker in self.dramatic_irony_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract dramatic irony moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        irony_list.append(line.strip()[:100])
                        if len(irony_list) >= 20:
                            break

        if count >= 6:
            present = True
        elif count >= 4:
            present = True

        return {
            "present": present,
            "count": count,
            "list": irony_list
        }

    def _analyze_visual_foreshadowing(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze visual foreshadowing (symbolic hints through imagery).

        McKee: "Visual foreshadowing - symbols, motifs, imagery that hint at future events."
        Mackendrick: "Visual storytelling - images foreshadow through symbolic meaning."
        """
        present = False
        visual_list = []

        # Check for visual foreshadowing markers
        count = 0
        for marker in self.visual_foreshadowing_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0 and len(visual_list) < 20:
                # Extract visual foreshadowing moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        visual_list.append(line.strip()[:100])
                        if len(visual_list) >= 20:
                            break

        if count >= 6:
            present = True
        elif count >= 4:
            present = True

        return {
            "present": present,
            "count": count,
            "list": visual_list
        }

    def _analyze_dialogue_foreshadowing(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze dialogue foreshadowing (verbal clues/hints).

        McKee: "Dialogue can foreshadow - cryptic remarks, warnings, predictions hint at future."
        Truby: "Dialogue foreshadows through double meaning, ambiguity, prophetic statements."
        """
        present = False

        # Check for dialogue foreshadowing markers
        count = 0
        for marker in self.dialogue_foreshadowing_markers:
            count += screenplay.lower().count(marker)

        # Check for dialogue patterns (character names followed by dialogue)
        dialogue_lines = re.findall(r'^[A-Z][A-Z\s]+\n\s+(.+)', screenplay, re.MULTILINE)
        dialogue_foreshadowing_count = 0
        for line in dialogue_lines:
            for marker in self.foreshadowing_present_markers[:15]:  # Check key foreshadowing words
                if marker in line.lower():
                    dialogue_foreshadowing_count += 1

        if count >= 8 or dialogue_foreshadowing_count >= 5:
            present = True
        elif count >= 5 or dialogue_foreshadowing_count >= 3:
            present = True

        return {
            "present": present,
            "count": count,
            "dialogue_count": dialogue_foreshadowing_count
        }

    def _analyze_misdirection(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze misdirection (hide clues in plain sight).

        McKee: "Misdirection - plant clues audience misses, hide truth in plain sight."
        Truby: "Misdirection creates surprise - red herrings and false leads heighten revelation."
        """
        used = False
        misdirection_list = []

        # Check for misdirection markers
        count = 0
        for marker in self.misdirection_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract misdirection moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        misdirection_list.append(line.strip()[:100])
                        if len(misdirection_list) >= 20:
                            break

        if count >= 4:
            used = True
        elif count >= 2:
            used = True

        return {
            "used": used,
            "count": count,
            "list": misdirection_list
        }

    def _analyze_setup_distance(self, screenplay: str, page_count: int) -> Dict[str, Any]:
        """
        Analyze setup distance (adequate pages between plant and payoff).

        Field: "Setup/payoff distance - enough space between plant and reveal for impact."
        McKee: "Setup too close to payoff feels forced - need adequate dramatic distance."
        """
        adequate = False

        # Check for distance markers
        distance_count = 0
        for marker in self.setup_distance_markers:
            distance_count += screenplay.lower().count(marker)

        # Estimate average distance (rough heuristic)
        # If screenplay is 90+ pages and has distance markers, likely adequate
        if page_count >= 90 and distance_count >= 5:
            adequate = True
        elif page_count >= 60 and distance_count >= 3:
            adequate = True

        # Calculate approximate average distance (pages)
        average_distance = page_count / 3 if distance_count > 0 else 0

        return {
            "adequate": adequate,
            "distance_count": distance_count,
            "average_distance": average_distance
        }

    def _analyze_inevitability_balance(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze inevitability balance (Aristotle: surprise yet inevitable).

        Aristotle: "Best plots - surprise audience yet feel inevitable in hindsight."
        McKee: "Inevitability vs surprise - foreshadow enough to feel earned, not predictable."
        """
        balanced = False

        # Check for inevitability markers
        count = 0
        for marker in self.inevitability_markers:
            count += screenplay.lower().count(marker)

        # Balance: has foreshadowing but not telegraphed
        # If inevitability markers present and telegraphed markers low, balanced
        telegraphed_count = 0
        for marker in self.telegraphed_twist_markers[:10]:  # Check key telegraphed words
            telegraphed_count += screenplay.lower().count(marker)

        if count >= 5 and telegraphed_count <= 2:
            balanced = True
        elif count >= 3 and telegraphed_count <= 1:
            balanced = True

        return {
            "balanced": balanced,
            "count": count,
            "telegraphed_count": telegraphed_count
        }

    def _detect_unfired_gun(self, screenplay: str, setup_payoff_data: Dict) -> Dict[str, Any]:
        """
        Detect unfired gun (PENALTY - setup without payoff).

        Chekhov: "If gun on wall in Act 1, must fire by Act 3 - everything planted must pay off."
        McKee: "Unfired gun - setup without payoff frustrates audience, violates contract."
        """
        detected = False
        penalty = False
        unfired_list = []

        # Check for unfired gun markers
        count = 0
        for marker in self.unfired_gun_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract unfired gun moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        unfired_list.append(line.strip()[:100])
                        if len(unfired_list) >= 10:
                            break

        # Check setup/payoff ratio - if many setups but few payoffs, likely unfired guns
        setup_count = setup_payoff_data["setup_count"]
        payoff_count = setup_payoff_data["payoff_count"]

        if setup_count > 0:
            payoff_ratio = payoff_count / setup_count
            if payoff_ratio < 0.4:  # Less than 40% payoff rate = unfired guns
                detected = True
                penalty = True
            elif payoff_ratio < 0.6:
                detected = True

        if count >= 2:
            detected = True
            penalty = True

        return {
            "detected": detected,
            "penalty": penalty,
            "count": count,
            "list": unfired_list,
            "payoff_ratio": payoff_count / max(setup_count, 1)
        }

    def _detect_deus_ex_machina(self, screenplay: str, setup_payoff_data: Dict) -> Dict[str, Any]:
        """
        Detect deus ex machina (PENALTY - payoff without setup).

        Aristotle: "Deus ex machina - unearned resolution, god from machine, contrived ending."
        McKee: "Deus ex machina violation - payoff must be earned through setup, not magic."
        """
        detected = False
        penalty = False
        deus_list = []

        # Check for deus ex machina markers
        count = 0
        for marker in self.deus_ex_machina_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract deus ex machina moments
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        deus_list.append(line.strip()[:100])
                        if len(deus_list) >= 10:
                            break

        if count >= 3:
            detected = True
            penalty = True
        elif count >= 2:
            detected = True
            penalty = True

        return {
            "detected": detected,
            "penalty": penalty,
            "count": count,
            "list": deus_list
        }

    def _detect_telegraphed_twist(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect telegraphed twist (PENALTY - too obvious foreshadowing).

        McKee: "Telegraphed twist - foreshadowing too obvious, audience ahead of story."
        Truby: "Balance foreshadowing - enough to feel earned, not so much it's predictable."
        """
        detected = False
        penalty = False

        # Check for telegraphed twist markers
        count = 0
        for marker in self.telegraphed_twist_markers:
            count += screenplay.lower().count(marker)

        if count >= 4:
            detected = True
            penalty = True
        elif count >= 3:
            detected = True
            penalty = True

        return {
            "detected": detected,
            "penalty": penalty,
            "count": count
        }

    def _calculate_overall_foreshadowing_quality(self, profile: ForeshadowingProfile) -> float:
        """Calculate overall foreshadowing quality score."""
        scores = [
            1.0 if profile.foreshadowing_present else 0.5,  # Important
            1.0 if profile.setup_payoff_detected else 0.3,  # CRITICAL (Chekhov's gun)
            1.0 if profile.plant_timing else 0.5,  # Important (Field)
            1.0 if profile.payoff_effectiveness else 0.6,  # Important
            1.0 if profile.dramatic_irony_present else 0.7,  # Nice to have
            1.0 if profile.visual_foreshadowing else 0.7,  # Nice to have
            1.0 if profile.dialogue_foreshadowing else 0.7,  # Nice to have
            1.0 if profile.misdirection_used else 0.8,  # Nice to have (sophisticated)
            1.0 if profile.setup_distance else 0.6,  # Important
            1.0 if profile.inevitability_balance else 0.5,  # Important (Aristotle)
            0.0 if profile.unfired_gun_detected else 1.0,  # PENALTY (critical)
            0.0 if profile.deus_ex_machina_detected else 1.0,  # PENALTY (critical)
            0.0 if profile.telegraphed_twist_detected else 1.0  # PENALTY
        ]

        # Average
        overall = sum(scores) / len(scores)

        return max(0.0, min(1.0, overall))

    def _check_foreshadowing_rules(self, profile: ForeshadowingProfile, foreshadowing_present: Dict,
                                   setup_payoff: Dict, plant_timing: Dict,
                                   payoff_effectiveness: Dict, dramatic_irony: Dict,
                                   visual_foreshadowing: Dict, dialogue_foreshadowing: Dict,
                                   misdirection: Dict, setup_distance: Dict,
                                   inevitability: Dict, unfired_gun: Dict,
                                   deus_ex_machina: Dict, telegraphed_twist: Dict) -> List[Dict]:
        """Check foreshadowing against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "FORESHADOWING.R001":
                # Foreshadowing Present
                if not profile.foreshadowing_present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Foreshadowing weak - lacks hints/setup for future events",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R002":
                # Setup/Payoff Present (Chekhov's Gun)
                if not profile.setup_payoff_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Setup/payoff weak - Chekhov's gun principle violated",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R003":
                # Plant Timing
                if not profile.plant_timing:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Plant timing weak - setup not early enough for later payoff",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R004":
                # Payoff Effectiveness
                if not profile.payoff_effectiveness:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Payoff weak - reveals/resolutions not satisfying or earned",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R005":
                # Dramatic Irony
                if not profile.dramatic_irony_present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Dramatic irony missing - audience doesn't know more than characters",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R006":
                # Visual Foreshadowing
                if not profile.visual_foreshadowing:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Visual foreshadowing missing - lacks symbolic hints through imagery",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R007":
                # Dialogue Foreshadowing
                if not profile.dialogue_foreshadowing:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Dialogue foreshadowing weak - lacks verbal clues/hints",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R008":
                # Misdirection
                if not profile.misdirection_used:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Misdirection missing - clues too obvious, lacks red herrings",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R009":
                # Setup Distance
                if not profile.setup_distance:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Setup distance weak - insufficient pages between plant and payoff",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R010":
                # Inevitability Balance
                if not profile.inevitability_balance:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Inevitability balance weak - not surprising yet inevitable (Aristotle)",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R011":
                # Avoid Unfired Gun
                if profile.unfired_gun_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Unfired gun detected - setup without payoff violates Chekhov principle",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R012":
                # Avoid Deus Ex Machina
                if profile.deus_ex_machina_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Deus ex machina detected - payoff without setup, unearned resolution",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "FORESHADOWING.R013":
                # Avoid Telegraphed Twist
                if profile.telegraphed_twist_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Telegraphed twist detected - foreshadowing too obvious, predictable",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_foreshadowing_score(self, profile: ForeshadowingProfile, violations: List) -> float:
        """Calculate overall foreshadowing score."""
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

        # Extra penalty for major issues
        if profile.unfired_gun_detected:
            score -= 25  # critical penalty (Chekhov violation)
        if profile.deus_ex_machina_detected:
            score -= 30  # critical penalty (worst violation)
        if profile.telegraphed_twist_detected:
            score -= 15  # high penalty

        # Bonus for excellence
        if profile.overall_foreshadowing_quality > 0.85:
            score += 5
        elif profile.overall_foreshadowing_quality > 0.75:
            score += 3

        if profile.setup_payoff_detected and profile.plant_timing:
            score += 3  # McKee/Field's sophisticated structure

        if profile.dramatic_irony_present:
            score += 2  # Sophisticated storytelling

        if profile.misdirection_used:
            score += 2  # Advanced technique

        if profile.inevitability_balance:
            score += 3  # Aristotle's excellence

        if profile.setup_payoff_detected and not profile.unfired_gun_detected:
            score += 3  # Chekhov's gun properly executed

        # Cap at 95
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profile: ForeshadowingProfile,
                          violations: List) -> str:
        """Generate foreshadowing diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Foreshadowing sophisticated with effective setup/payoff and dramatic irony"
        elif score >= 60:
            level = "GOOD"
            summary = "Foreshadowing present but could be more strategic or better balanced"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Foreshadowing problems - unfired guns or weak setup/payoff detected"
        else:
            level = "POOR"
            summary = "Major foreshadowing problems - deus ex machina or telegraphed twists"

        diagnosis = f"FORESHADOWING {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if not profile.setup_payoff_detected:
            issues.append("weak setup/payoff")
        if not profile.plant_timing:
            issues.append("poor plant timing")
        if profile.unfired_gun_detected:
            issues.append("unfired guns")
        if profile.deus_ex_machina_detected:
            issues.append("deus ex machina")
        if profile.telegraphed_twist_detected:
            issues.append("telegraphed twists")
        if not profile.dramatic_irony_present:
            issues.append("no dramatic irony")
        if not profile.inevitability_balance:
            issues.append("poor inevitability balance")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                 profile: ForeshadowingProfile) -> List[str]:
        """Generate specific foreshadowing recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if not profile.setup_payoff_detected:
            recommendations.append("Strengthen setup/payoff - Chekhov: 'If gun on wall in Act 1, must fire by Act 3' - every element planted must pay off")

        if not profile.plant_timing:
            recommendations.append("Improve plant timing - Field: 'Plant in Act 1, pay off in Act 3' - early setup creates anticipation for later payoff")

        if profile.unfired_gun_detected:
            recommendations.append("Fix unfired guns - McKee: 'Everything planted must pay off, no unfired guns' - remove unused setups or add payoffs")

        if profile.deus_ex_machina_detected:
            recommendations.append("Eliminate deus ex machina - Aristotle: 'Payoff must be earned through setup' - plant solutions early, never magic endings")

        if profile.telegraphed_twist_detected:
            recommendations.append("Balance foreshadowing - McKee: 'Foreshadow enough to feel earned, not so much it's predictable' - add misdirection")

        if not profile.dramatic_irony_present:
            recommendations.append("Add dramatic irony - McKee: 'Audience knows what character doesn't, creates tension' - let audience see danger approaching")

        if not profile.inevitability_balance:
            recommendations.append("Balance inevitability - Aristotle: 'Best plots surprise audience yet feel inevitable in hindsight' - foreshadow subtly")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study McKee's Story - setup/payoff and foreshadowing principles essential")
            recommendations.append("Study Field's Screenplay - structural setup/payoff timing fundamental")

        return recommendations[:5]

    def export_foreshadowing_features(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Export foreshadowing features for correlation/analysis.

        Returns structured data with foreshadowing metrics.
        """
        foreshadowing_present = self._analyze_foreshadowing_present(screenplay_text)
        page_count = self._estimate_page_count(screenplay_text)
        act1_text = self._extract_pages(screenplay_text, 0, int(page_count * 0.25))
        act2_text = self._extract_pages(screenplay_text, int(page_count * 0.25), int(page_count * 0.75))
        act3_text = self._extract_pages(screenplay_text, int(page_count * 0.75), page_count)
        setup_payoff = self._analyze_setup_payoff(screenplay_text, act1_text, act2_text, act3_text)

        return {
            "foreshadowing": {
                "foreshadowing_present": foreshadowing_present["present"],
                "setup_payoff_detected": setup_payoff["detected"],
                "setup_count": setup_payoff["setup_count"],
                "payoff_count": setup_payoff["payoff_count"]
            },
            "meta": {
                "source": "DrForeshadowing",
                "focus": "Foreshadowing and setup/payoff analysis"
            }
        }


# Compatibility class for testing framework
class DrForeshadowingAnalysis(DrForeshadowing):
    """Alias for compatibility with test framework."""
    pass
