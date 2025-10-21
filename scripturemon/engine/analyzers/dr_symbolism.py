"""
Script Doctor Symbolismon - Symbolism and Metaphor Analysis Specialist
A Script Doctor™ in Digimon form specializing in symbolism, metaphor, motif, visual imagery, thematic resonance, avoid heavy-handed symbolism.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class SymbolismProfile:
    """Overall symbolism analysis."""
    symbolism_present: bool  # Visual metaphors/symbols exist
    symbol_clarity: bool  # Audience understands meaning
    symbol_consistency: bool  # Used throughout, not random
    motif_presence: bool  # Recurring visual/thematic element
    visual_metaphor_quality: bool  # Shows abstract through concrete
    color_symbolism: bool  # Colors carry meaning
    object_symbolism: bool  # Props/objects represent ideas
    setting_symbolism: bool  # Location reflects theme
    character_symbolism: bool  # Character represents idea/concept
    title_symbolism: bool  # Title reflects theme/meaning
    thematic_resonance: bool  # Symbols support theme
    symbol_subtlety: bool  # Not heavy-handed
    heavy_handed_detected: bool  # PENALTY (too obvious, preachy)
    confused_symbolism_detected: bool  # PENALTY (unclear meaning)
    inconsistent_symbols_detected: bool  # PENALTY (symbol changes meaning)
    overall_symbolism_quality: float


@dataclass
class SymbolismAnalysisResults:
    """Complete symbolism analysis results."""
    symbolism_profile: SymbolismProfile
    symbol_list: List[str]  # Identified symbols
    motif_list: List[str]  # Recurring motifs
    visual_metaphor_list: List[str]  # Visual metaphors
    color_symbolism_list: List[str]  # Color symbolism instances
    object_symbolism_list: List[str]  # Object symbolism
    setting_symbolism_list: List[str]  # Setting symbolism
    character_symbolism_list: List[str]  # Character as symbol
    heavy_handed_list: List[str]  # Heavy-handed symbolism (PENALTY)
    confused_symbols_list: List[str]  # Confused symbolism (PENALTY)
    score: float
    diagnosis: str
    recommendations: List[str]


class DrSymbolism:
    """
    Script Doctor Symbolismon - The Symbolism and Metaphor Analysis Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing symbolism,
    metaphor, motif, visual imagery, thematic resonance, avoid heavy-handed symbolism.

    Identity: Script Doctor first, Digimon symbolism specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Symbolismon with rules and configuration."""
        self.name = "Script Doctor Symbolismon"
        self.digimon_name = "Symbolismon"
        self.title = "Script Doctor - Symbolism and Metaphor Analysis Specialist"
        self.specialty = "Symbolism, metaphor, motif, visual imagery, thematic resonance, avoid heavy-handed symbolism"
        self.identity = "I am Script Doctor Symbolismon, a professional Script Doctor™ specializing in symbolism and metaphor analysis"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "symbolism_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - SYMBOLISM SPECIFIC
        self.deep_context_queries = [
            "McKee Story symbolism visual metaphor imagery",
            "McKee Story symbol motif recurring element",
            "McKee Story visual storytelling show abstract",
            "McKee Story symbol thematic resonance meaning",
            "McKee Story metaphor concrete represents abstract",
            "McKee Story symbol consistency throughout story",
            "McKee Story avoid heavy-handed symbolism subtle",
            "McKee Story symbol clarity audience understands",
            "McKee Story visual symbol reinforce theme",
            "McKee Story object symbolism props meaning",
            # McKee Story - SYMBOLISM & METAPHOR (ultra-specific from symbolism/metaphor sections)
            "McKee Story screenwriting art making mental physical visual correlatives inner conflict images",
            "McKee Story great work living metaphor says life like this poetic lucidity",
            "McKee Story archetypal image hunter prey mountaintop great things happen places symbols",
            "McKee Story symbolic progression character transformation waitress goddess lifts above genre",
            "Syd Field Screenplay visual imagery symbol",
            "Field visual storytelling metaphor cinematography",
            "Field symbol motif recurring visual element",
            "Field setting symbolism location reflects theme",
            "Field visual metaphor show don't tell",
            "Blake Snyder Save the Cat visual symbol",
            "Snyder symbol title reflects theme meaning",
            "Snyder visual metaphor concrete abstract",
            "Snyder symbol motif recurring element pattern",
            "Snyder avoid on-the-nose symbolism subtle",
            "John Truby Anatomy symbol thematic design",
            "Truby symbol web thematic network connections",
            "Truby symbol motif recurring pattern builds",
            "Truby symbol character represents idea archetype",
            "Truby visual symbol strategic placement design",
            "Truby avoid heavy-handed symbolism nuanced",
            "Christopher Vogler Writer's Journey symbol archetype",
            "Vogler mythic symbol collective unconscious",
            "Vogler symbol motif recurring archetype pattern",
            "Vogler character symbol represents idea journey",
            "Vogler visual symbol mythic resonance universal",
            "Joseph Campbell Hero 1000 Faces symbol myth",
            "Campbell universal symbols archetypal imagery",
            "Campbell symbol motif recurring mythic pattern",
            "Campbell character symbol god hero archetype",
            "Campbell visual symbol collective unconscious meaning",
            "Aristotle Poetics metaphor representation mimesis",
            "Aristotle metaphor shows through concrete imagery",
            "Aristotle metaphor clarity obscurity balance",
            "Aristotle visual representation symbolic meaning",
            "Aristotle metaphor elevates language through imagery",
            "Linda Seger Making Good Script Great visual symbol",
            "Seger visual metaphor cinematographic symbol",
            "Seger symbol motif recurring visual element",
            "Seger symbol clarity audience comprehension",
            "Seger avoid heavy-handed symbolism subtle nuance",
            "Seger symbol thematic resonance supports theme",
            "Lajos Egri Art Dramatic Writing symbol premise",
            "Egri symbol supports premise theme unity",
            "Egri visual symbol character reflects idea",
            "William Goldman Adventures Screen Trade visual storytelling",
            "Goldman visual symbol metaphor cinematography",
            "Shonda Rhimes visual symbol television imagery",
            "David Mamet visual metaphor dramatic symbol",
            "Alexander Mackendrick visual storytelling symbol image",
            "Mackendrick visual metaphor show abstract concrete",
            "K.M. Weiland Creating Character Arcs symbol transformation",
            "Weiland symbol motif character arc resonance",
            "Weiland visual symbol lie truth theme",
            "symbolism visual metaphor motif imagery",
            "symbol clarity audience understands meaning",
            "symbol consistency recurring throughout story",
            "motif recurring visual thematic element pattern",
            "visual metaphor show abstract through concrete",
            "color symbolism meaning red blue white black",
            "object symbolism props carry thematic meaning",
            "setting symbolism location reflects theme mood",
            "character symbolism represents idea archetype concept",
            "title symbolism reflects theme central meaning",
            "thematic resonance symbols support theme unity",
            "symbol subtlety nuanced not heavy-handed obvious",
            "avoid heavy-handed symbolism preachy obvious penalty",
            "avoid confused symbolism unclear meaning penalty",
            "avoid inconsistent symbols meaning changes penalty"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story image system category motif repeats with variation subtle",
        "McKee Story symbolic ascension build imagery from specific to universal",
        "McKee Story external imagery preexisting symbol imported same meaning",
        "McKee Story internal imagery invented meaning unique to this film",
        "McKee Story symbolism subliminal invisible avoid pointing at symbol",

        # Campbell Hero 1000 Faces - GPT-5 (12 Oct 2025)
        "Campbell Hero axis mundi world navel center temple pillar,",
        "Campbell Hero world tree tree of life branches roots,",
        "Campbell Hero cosmic egg cracking emergence creation emanations,",
        "Campbell Hero belly whale womb tomb incubation transformation,",
        "Campbell Hero labyrinth minotaur ariadne thread center exit,",
        "Campbell Hero dragon hoard treasure gold fire shadow,",
        "Campbell Hero river crossing boat oar ferryman passage,",

        # Truby Anatomy 22 Steps - GPT-5 (12 Oct 2025)
        "Truby Anatomy symbol web network refer repeat resonance compressed meaning",
        "Truby Anatomy story symbol title organizing metaphor structure twist encapsulation",
        "Truby Anatomy symbol line connecting main symbols across subsystems coherence",
        "Truby Anatomy symbolic character god father king goddess shadow translation",
        "Truby Anatomy symbolic character animal wolf bat serpent centaur modern myth",
        "Truby Anatomy symbolic character machine robot replicant tin man human reversal",
        "Truby Anatomy symbolic theme single image expresses moral sequence opposition",
        "Truby Anatomy symbol for story world natural setting magical force field charge",
        "Truby Anatomy symbolic actions miniatures gestural meaning thematic crystallization",
        "Truby Anatomy symbolic objects web cluster tied to designing principle selection",
        "Truby Anatomy reverse symbol web undercut genre twist expectation inversion",
        "Truby Anatomy taglines key words repeated cumulative echo thematic payoff",
        "Truby Anatomy naming symbolic names Dickensian sound image value encoding",
        "Truby Anatomy symbol connected to character change setup payoff framing",
        "Truby Anatomy story movement symbol mapping raft river road tree mountain",
        "Truby Anatomy audience pattern recognition repetition variation leitmotif",
        "Truby Anatomy moral symbol scarlet letter public conformity true love tension",
        "Truby Anatomy city symbol network matrix web entrapment control system",
        "Truby Anatomy death symbols graveyard undertow abyss tolling bell foreshadow",
        "Truby Anatomy house symbols nest cradle armor branch attic basement plotting",

        # Field Screenplay Paradigm - GPT-5 (12 Oct 2025)
        "Field Screenplay visual storytelling story told with pictures not exposition",
        "Field Screenplay visual image metaphor recurring motif cinematic sign",
        "Field Screenplay bookend opening closing mirror image resonance",
        "Field Screenplay montage imagery compress time convey idea",
        "Field Screenplay insert close shot detail object symbolic emphasis",
        "Field Screenplay POV reverse angle perception subjectivity meaning",
        "Field Screenplay movement blocking staging behavioral symbolism",
        "Field Screenplay master shot composition environment relationship",
        "Field Screenplay action is character symbolic choices on screen",
        "Field Screenplay show don’t tell subtext beneath image",
        "Field Screenplay last image final picture thematic echo closure",
        "Field Screenplay recurring prop color texture motif supports theme",
        "Field Screenplay cutaway reaction shot visual punctuation meaning",
        "Field Screenplay silence music sound contrast emphasize image",
        "Field Screenplay transitions dissolves fades bookend framing device",
        "Field Screenplay visual metaphor context content glass water analogy",
        "Field Screenplay tag image coda after solution lingering symbol",
        "Field Screenplay establishing shot orient world symbolic geography",
        "Field Screenplay beat change on picture not words emphasis",
        "Field Screenplay image system designed across acts visual cohesion",

        # Vogler Writer's Journey - GPT-5 (12 Oct 2025)
        "Vogler Journey sword magic weapon will focus light-saber",
        "Vogler Journey grail ultimate boon cup heals wounded land",
        "Vogler Journey elixir healing potion knowledge experience wisdom",
        "Vogler Journey ariadne’s thread clew apron strings connection home",
        "Vogler Journey belly of the whale engulfment crushing trashmasher",
        "Vogler Journey sacred marriage ring altar union inner balance",
        "Vogler Journey apotheosis halo light beam divine approval",
        "Vogler Journey baptism immersion drowning resurrection cleansing",
        "Vogler Journey puppet hand godfather logo control marionette metaphor",
        "Vogler Journey ruby slippers mentor gift yellow brick road",
        "Vogler Journey horse of a different color color change omen",
        "Vogler Journey poppies sleep enchantment blanket of snow rescue",
        "Vogler Journey angel on shoulder devil conscience debate",
        "Vogler Journey sword-bridge narrow crossing peril final misstep",
        "Vogler Journey magic flight comb scarf river forest barrier",
        "Vogler Journey mirror insight seeing clearly clairvoyance revelation",
        "Vogler Journey labyrinth minotaur thread guidance return path",
        "Vogler Journey tentpole act breaks points of tension sag",
        "Vogler Journey stained glass prologue mythic backstory illustration",
        "Vogler Journey campfire storytelling healing song boasting feast",

            # McKee Character - GPT-5 (12 Oct 2025)
            "McKee Character symbolic character metaphor for humanity becoming",
            "McKee Character archetypal character mother warrior trickster time power",
            "McKee Character allegorical character risks reduction balance dimensionality",
            "McKee Character metaphorical protagonist animal cartoon object free will",
            "McKee Character Center of Good symbolic light within darkness",
            "McKee Character cast mirrors society reflective metaphor world",
            "McKee Character theme embodied in value-charged character actions",
            "McKee Character epiphany image symbolic gesture seals meaning",
            "McKee Character name costume totem objects symbolic extensions identity",
            "McKee Character setting as symbol charged landscape moral field",
            "McKee Character foil symbolic counterpoint clarifies protagonist essence",
            "McKee Character obsession emblem comic identity blind spot",
            "McKee Character transformation symbolic rite passage completed character",
            "McKee Character freedom versus fate symbolized by recurrent motif",
            "McKee Character moral imagination selects symbols vital not trivial",
            "McKee Character narration stance frames mythic or ironic distance",
            "McKee Character unreliable narrator symbolizes fallible memory identity",
            "McKee Character dramatic irony godlike audience perspective mythic",
            "McKee Character controlling value personified as archetypal pressure",
            "McKee Character resolution closing image carries symbolic resonance",

            # Seger Script Great - GPT-5 (12 Oct 2025)
            "Seger Script cinematic metaphors visual ideas carry meaning",
            "Seger Script recurring motifs plant payoff unify theme",
            "Seger Script repetition and contrast pattern images echo",
            "Seger Script foreshadowing images promise later payoffs",
            "Seger Script symbolic objects props accrue significance",
            "Seger Script final image bookend symbolic resonance",
            "Seger Script subtext via image not dialogue overtelling",
            "Seger Script scene sequence builds thematic imagery progression",
            "Seger Script balancing images and dialogue trust visuals",
            "Seger Script implied meaning through composition framing rhythm",
            "Seger Script descriptive language suggests metaphor for collaborators",
            "Seger Script motif placement around turning points reinforce",
            "Seger Script transformation shown through evolving visual motif",
            "Seger Script atmosphere color texture support symbolic intent",
            "Seger Script opening image thematic metaphor seed",
            "Seger Script payoff image at climax resolves metaphor",
            "Seger Script avoid mixed metaphors maintain clarity consistency",
            "Seger Script POV affects symbolic reveal timing",
            "Seger Script montage juxtaposition create metaphor without words",
            "Seger Script props from setup to resolution deliver theme",

            # Cowgill Short Films - GPT-5 (12 Oct 2025)
            "Cowgill Short visual storytelling images tell story more",
            "Cowgill Short power of images audience processes quickly",
            "Cowgill Short nonverbal language reactions gestures carry meaning",
            "Cowgill Short business object handling reveals inner life",
            "Cowgill Short INSERT highlight significant letter insignia detail",
            "Cowgill Short atmosphere mirrors emotion rain night shadow",
            "Cowgill Short recurring props motifs underscore theme subtly",
            "Cowgill Short action over description symbolic behavior choices",
            "Cowgill Short show don’t tell subtext beneath images",
            "Cowgill Short a picture worth a thousand words renewed",
            "Cowgill Short object focus flower sand owl creek example",
            "Cowgill Short sound and image reinforce narrative meaning",
            "Cowgill Short opening image signals tone arena theme",
            "Cowgill Short visual reveal withhold then pay off",
            "Cowgill Short minimal dialogue let imagery communicate",
            "Cowgill Short mise en scene arrangement expresses conflict",
            "Cowgill Short props barriers boombox basketball speak character",
            "Cowgill Short symbolic act choice at climax defines",
            "Cowgill Short edit juxtaposition past present storyteller viewpoint",
            "Cowgill Short end image last line linger thematic",

            # Aristotle Poetics - GPT-5 (12 Oct 2025)
            "Aristotle Poetics: How do I deploy symbols as semeia that clarify causal truth at recognition rather than as free-floating motifs?",
            "Aristotle Poetics: Which images can bear double meanings pre/post anagnorisis without feeling planted (e.g., a lock, a scar, a lullaby)?",
            "Aristotle Poetics: How to ensure a recurring image is ‘oikeion’ to the action—its reappearance must compel or evidence a necessary act?",
            "Aristotle Poetics: How to foreshadow peripeteia with visual antithesis that flips identity/function at the hinge?",
            "Aristotle Poetics: How to bind a symbol to kinship (rings, cradles, graves) to intensify tragic pathos within necessity?",
            "Aristotle Poetics: How to prevent symbol-driven scenes from creating a second action—each symbol scene must change what must happen next?",
            "Aristotle Poetics: How to convert a theme-statement into a symbolic deed (burning a letter, crossing a threshold) that argues by action?",
            "Aristotle Poetics: How to use costume color or emblem as mistaken identity proof early and true identity proof later?",
            "Aristotle Poetics: How to design a prop-chain (gift→pawn→return) that evidences necessity rather than coincidence?",
            "Aristotle Poetics: How to ensure the final image symbolizes the clarified structure (katharsis) rather than a moral takeaway?",
            "Aristotle Poetics: How to avoid allegory that replaces action—symbols must be subordinate to mythos, not a parallel lecture?",
            "Aristotle Poetics: How to time symbolic revelation so it coincides with cognitive recognition (seeing is knowing)?",
            "Aristotle Poetics: How to link setting symbols (doorways, thresholds) to act breaks (beginning/middle/end) as structural markers?",
            "Aristotle Poetics: How to embed a sonic motif (melos) that functions like a token of identity to trigger recognition?",
            "Aristotle Poetics: How to track the symbol’s causal role across drafts—if it does not cause or evidence a necessity, cut it?",
            "Aristotle Poetics: How to balance subtlety/clarity—ensure spectators can ‘see the necessity’ without verbal explanation?",
            "Aristotle Poetics: How to mirror a symbol’s meaning across protagonist/antagonist to show reversal in values?",
            "Aristotle Poetics: How to keep symbols from becoming opsis-first spectacle—use them at decision points, not in tableaux?",
            "Aristotle Poetics: How to make a symbolic gesture (kneeling, washing hands) carry a reclassified meaning at lysis?",
            "Aristotle Poetics: How to leverage negative symbols (absences, omissions) as proof of truth in the recognition scene?",

            # Snyder Save the Cat - GPT-5 (12 Oct 2025)
            "Snyder Cat: Is your Opening Image/Final Image pair a clear symbolic inversion (e.g., alone vs. together, dark vs. light) that encodes the arc?",
            "Snyder Cat: Do you plant an object/color motif in Act One that appears in All Is Lost as a ‘whiff of death’ symbol of the old self’s collapse?",
            "Snyder Cat: Is the Save the Cat act mirrored symbolically in the Finale (same gesture/object reframed as true strength)?",
            "Snyder Cat: Are theme motifs (e.g., locks/keys for autonomy vs. control) placed across BS2 zones to guide audience subconscious?",
            "Snyder Cat: Do your set pieces carry symbolic stakes (not just physical), aligning imagery with internal conflict?",
            "Snyder Cat: Is there a recurring line/image that evolves meaning (ironic at first usage, sincere by Final Image)?",
            "Snyder Cat: Does the antagonist carry a counter-motif (color/object) that the hero rejects or transforms by the end?",
            "Snyder Cat: In Dark Night of the Soul, do you use silent symbolism (rainfall, extinguished light, discarded token) over monologue?",
            "Snyder Cat: Are location choices symbolic (house/bridge/mirror room) at major turns (25/55/75/85), not just convenient?",
            "Snyder Cat: Does your title ‘say what it is’ and carry symbolic resonance (Legally Blonde), echoed in key dialogue/images?",
            "Snyder Cat: Do callbacks resolve symbolically in Act Three (broken object repaired, empty seat filled), proving transformation?",
            "Snyder Cat: Is the Midpoint symbolically the ‘zenith/nadir’ (sunset/noon, high/low vantage) matching false win/loss?",
            "Snyder Cat: Are props that convey backstory (photo, trophy) used in action beats rather than static ‘holds,’ to keep symbols alive?",
            "Snyder Cat: Do you avoid discordant symbols that suggest a different genre or theme than your logline promises?",
            "Snyder Cat: Is the ‘house’ in Monster in the House chosen for symbolic meaning (family, institution) beyond containment?",
            "Snyder Cat: Does the B-Story carry its own motif that merges with the A-Story motif at Break into Three (visual synthesis)?",
            "Snyder Cat: Is the whiff of death symbol referenced in the Finale as an overcome image (flower replanted, light rekindled)?",
            "Snyder Cat: Do you ensure motif density peaks at Midpoint and Finale, providing subconscious cohesion?",
            "Snyder Cat: Are costume/wardrobe shifts used as symbolic markers of inner change (color palette move, uniform shed)?",
            "Snyder Cat: Could your story’s core transformation be understood by a caveman via images alone, without words?",

            # Weiland Character Arcs - GPT-5 (12 Oct 2025)
            "Weiland Arcs Death motif at Third Plot Point symbolic demise",
            "Weiland Arcs Mirror moment Midpoint self-recognition thematic reflection",
            "Weiland Arcs Pandora’s box First Plot Point irreversible opening",
            "Weiland Arcs Before and After mirror scenes contrasted visuals",
            "Weiland Arcs Locked door doorway between worlds commitment symbolism",
            "Weiland Arcs Centerpiece Midpoint big scene anchors transformation",
            "Weiland Arcs Faux climax preliminary victory deceptive lull",
            "Weiland Arcs Blatantly demonstrate the Truth emblematic gesture token",
            "Weiland Arcs Normal World objects symbolize Lie enabling comforts",
            "Weiland Arcs Adventure world artifacts represent emerging Truth",
            "Weiland Arcs Costuming posture props show internal change nonverbal",
            "Weiland Arcs Weather light darkness track arc emotional beats",
            "Weiland Arcs Wound scar Ghost visual callbacks during revelations",
            "Weiland Arcs Sacrifice objectized relinquish Want tangible loss",
            "Weiland Arcs Threshold crossings physical spaces mark structural turns",
            "Weiland Arcs Renewed attack imagery echoes earlier temptations amplified",
            "Weiland Arcs Climax emblem choice icon of Truth held",
            "Weiland Arcs Resolution closing image encapsulates Lie to Truth",
            "Weiland Arcs Antagonist totems embody world’s Lie oppressive presence",
            "Weiland Arcs Series recurring symbols evolve with each arc beat",











        ]

        # Symbolism analysis patterns (bilingual: EN + PT) - 150-170+ markers

        # Symbolism present markers (visual metaphors/symbols)
        self.symbolism_present_markers = [
            # English
            "symbol", "symbolism", "symbolic", "symbolizes", "represents",
            "metaphor", "metaphorical", "imagery", "visual metaphor",
            "stands for", "embodies", "signifies", "conveys meaning",
            "visual symbol", "recurring image", "motif", "pattern",
            "thematic imagery", "visual theme", "symbolic meaning",
            "represents idea", "embodies concept", "visual representation",
            # Portuguese
            "símbolo", "simbolismo", "simbólico", "simboliza", "representa",
            "metáfora", "metafórico", "imagética", "metáfora visual",
            "significa", "incorpora", "expressa significado", "transmite sentido",
            "símbolo visual", "imagem recorrente", "motivo", "padrão",
            "imagética temática", "tema visual", "significado simbólico",
            "representa ideia", "incorpora conceito", "representação visual"
        ]

        # Symbol clarity markers (audience understands meaning)
        self.symbol_clarity_markers = [
            # English
            "clear symbol", "obvious meaning", "audience understands",
            "meaning is clear", "symbolism evident", "transparent symbolism",
            "easily grasped", "comprehensible symbol", "readable symbolism",
            "meaning accessible", "clear imagery", "understandable metaphor",
            # Portuguese
            "símbolo claro", "significado óbvio", "audiência entende",
            "significado é claro", "simbolismo evidente", "simbolismo transparente",
            "facilmente compreendido", "símbolo compreensível", "simbolismo legível",
            "significado acessível", "imagética clara", "metáfora compreensível"
        ]

        # Symbol consistency markers (used throughout, not random)
        self.symbol_consistency_markers = [
            # English
            "recurring symbol", "consistent symbolism", "throughout story",
            "pattern repeats", "motif returns", "symbol recurs",
            "established symbol", "maintained symbolism", "unified imagery",
            "symbolic consistency", "repeated motif", "pattern consistency",
            # Portuguese
            "símbolo recorrente", "simbolismo consistente", "ao longo da história",
            "padrão se repete", "motivo retorna", "símbolo recorre",
            "símbolo estabelecido", "simbolismo mantido", "imagética unificada",
            "consistência simbólica", "motivo repetido", "consistência de padrão"
        ]

        # Motif presence markers (recurring visual/thematic element)
        self.motif_presence_markers = [
            # English
            "motif", "recurring motif", "visual motif", "thematic motif",
            "pattern", "recurring pattern", "visual pattern", "leitmotif",
            "repeated element", "recurring element", "symbolic pattern",
            "visual leitmotif", "thematic pattern", "recurring imagery",
            # Portuguese
            "motivo", "motivo recorrente", "motivo visual", "motivo temático",
            "padrão", "padrão recorrente", "padrão visual", "leitmotiv",
            "elemento repetido", "elemento recorrente", "padrão simbólico",
            "leitmotiv visual", "padrão temático", "imagética recorrente"
        ]

        # Visual metaphor markers (shows abstract through concrete)
        self.visual_metaphor_markers = [
            # English
            "visual metaphor", "shows through imagery", "concrete visual",
            "abstract becomes concrete", "visual representation",
            "shows not tells", "visual storytelling", "imagery conveys",
            "metaphorical imagery", "symbolic visual", "visual symbol",
            "image represents", "visual embodies", "cinematic metaphor",
            # Portuguese
            "metáfora visual", "mostra através de imagens", "visual concreto",
            "abstrato torna-se concreto", "representação visual",
            "mostra não conta", "narrativa visual", "imagética transmite",
            "imagética metafórica", "visual simbólico", "símbolo visual",
            "imagem representa", "visual incorpora", "metáfora cinematográfica"
        ]

        # Color symbolism markers
        self.color_symbolism_markers = [
            # English
            "color symbolism", "red symbolizes", "blue represents",
            "white signifies", "black embodies", "color meaning",
            "symbolic color", "color motif", "color palette meaning",
            "red imagery", "blue motif", "white symbol", "black metaphor",
            # Portuguese
            "simbolismo de cor", "vermelho simboliza", "azul representa",
            "branco significa", "preto incorpora", "significado de cor",
            "cor simbólica", "motivo de cor", "paleta de cores significado",
            "imagética vermelha", "motivo azul", "símbolo branco", "metáfora preta"
        ]

        # Object symbolism markers (props carry meaning)
        self.object_symbolism_markers = [
            # English
            "object symbolism", "prop symbolizes", "item represents",
            "symbolic object", "meaningful prop", "object metaphor",
            "item carries meaning", "symbolic prop", "object embodies",
            "prop represents idea", "meaningful item", "symbolic artifact",
            # Portuguese
            "simbolismo de objeto", "objeto de cena simboliza", "item representa",
            "objeto simbólico", "objeto de cena significativo", "metáfora de objeto",
            "item carrega significado", "objeto de cena simbólico", "objeto incorpora",
            "objeto de cena representa ideia", "item significativo", "artefato simbólico"
        ]

        # Setting symbolism markers (location reflects theme)
        self.setting_symbolism_markers = [
            # English
            "setting symbolism", "location symbolizes", "place represents",
            "symbolic setting", "meaningful location", "environment embodies",
            "setting reflects theme", "location metaphor", "place carries meaning",
            "symbolic environment", "setting mirrors", "location embodies",
            # Portuguese
            "simbolismo de cenário", "localização simboliza", "lugar representa",
            "cenário simbólico", "localização significativa", "ambiente incorpora",
            "cenário reflete tema", "metáfora de localização", "lugar carrega significado",
            "ambiente simbólico", "cenário espelha", "localização incorpora"
        ]

        # Character symbolism markers (character represents idea/concept)
        self.character_symbolism_markers = [
            # English
            "character symbolism", "character represents", "symbolic character",
            "character embodies idea", "allegorical character", "character metaphor",
            "represents concept", "character stands for", "symbolic figure",
            "character personifies", "allegorical figure", "archetype embodies",
            # Portuguese
            "simbolismo de personagem", "personagem representa", "personagem simbólico",
            "personagem incorpora ideia", "personagem alegórico", "metáfora de personagem",
            "representa conceito", "personagem significa", "figura simbólica",
            "personagem personifica", "figura alegórica", "arquétipo incorpora"
        ]

        # Title symbolism markers
        self.title_symbolism_markers = [
            # English
            "title symbolism", "title represents", "symbolic title",
            "title embodies theme", "title metaphor", "title meaning",
            "title reflects", "title signifies", "meaningful title",
            # Portuguese
            "simbolismo de título", "título representa", "título simbólico",
            "título incorpora tema", "metáfora de título", "significado de título",
            "título reflete", "título significa", "título significativo"
        ]

        # Thematic resonance markers (symbols support theme)
        self.thematic_resonance_markers = [
            # English
            "thematic resonance", "supports theme", "reinforces theme",
            "theme and symbol unified", "symbolic unity", "thematic coherence",
            "symbol serves theme", "thematic integration", "unified symbolism",
            "symbol echoes theme", "thematic harmony", "symbol amplifies theme",
            # Portuguese
            "ressonância temática", "apoia tema", "reforça tema",
            "tema e símbolo unificados", "unidade simbólica", "coerência temática",
            "símbolo serve tema", "integração temática", "simbolismo unificado",
            "símbolo ecoa tema", "harmonia temática", "símbolo amplifica tema"
        ]

        # Symbol subtlety markers (not heavy-handed)
        self.symbol_subtlety_markers = [
            # English
            "subtle symbolism", "nuanced symbol", "understated metaphor",
            "delicate imagery", "layered symbolism", "sophisticated symbol",
            "implicit meaning", "indirect symbolism", "suggestive imagery",
            "refined symbolism", "elegant metaphor", "tasteful symbolism",
            # Portuguese
            "simbolismo sutil", "símbolo nuançado", "metáfora discreta",
            "imagética delicada", "simbolismo em camadas", "símbolo sofisticado",
            "significado implícito", "simbolismo indireto", "imagética sugestiva",
            "simbolismo refinado", "metáfora elegante", "simbolismo de bom gosto"
        ]

        # Heavy-handed symbolism markers (PENALTY - too obvious, preachy)
        self.heavy_handed_markers = [
            # English
            "heavy-handed symbolism", "obvious symbolism", "on-the-nose symbol",
            "preachy symbolism", "sledgehammer symbolism", "too obvious",
            "blatant symbolism", "clumsy metaphor", "forced symbolism",
            "ham-fisted symbol", "overwrought symbolism", "unsubtle symbolism",
            "beating audience over head", "painfully obvious", "lacking subtlety",
            # Portuguese
            "simbolismo pesado", "simbolismo óbvio", "símbolo direto demais",
            "simbolismo pregador", "simbolismo martelado", "óbvio demais",
            "simbolismo flagrante", "metáfora desajeitada", "simbolismo forçado",
            "símbolo desajeitado", "simbolismo exagerado", "simbolismo sem sutileza",
            "batendo na cabeça da audiência", "dolorosamente óbvio", "falta de sutileza"
        ]

        # Confused symbolism markers (PENALTY - unclear meaning)
        self.confused_symbolism_markers = [
            # English
            "confused symbolism", "unclear symbol", "ambiguous meaning",
            "muddled metaphor", "obscure symbolism", "incomprehensible symbol",
            "symbol doesn't work", "failed metaphor", "unclear imagery",
            "confusing symbolism", "vague symbol", "indecipherable metaphor",
            # Portuguese
            "simbolismo confuso", "símbolo pouco claro", "significado ambíguo",
            "metáfora confusa", "simbolismo obscuro", "símbolo incompreensível",
            "símbolo não funciona", "metáfora fracassada", "imagética pouco clara",
            "simbolismo confundidor", "símbolo vago", "metáfora indecifrável"
        ]

        # Inconsistent symbols markers (PENALTY - symbol changes meaning)
        self.inconsistent_symbols_markers = [
            # English
            "inconsistent symbolism", "symbol changes meaning", "shifting symbolism",
            "contradictory symbol", "symbol loses meaning", "muddled symbol",
            "symbol confusion", "symbol contradicts", "unstable symbolism",
            "symbol undermines itself", "incoherent symbolism", "symbol breaks down",
            # Portuguese
            "simbolismo inconsistente", "símbolo muda significado", "simbolismo mutante",
            "símbolo contraditório", "símbolo perde significado", "símbolo confuso",
            "confusão de símbolo", "símbolo contradiz", "simbolismo instável",
            "símbolo se sabota", "simbolismo incoerente", "símbolo se desfaz"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze symbolism and metaphor in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete symbolism diagnostic report
        """
        # Extract page count and scenes
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)

        # Extract Act 1, 2, 3 for pattern analysis
        act1_text = self._extract_pages(screenplay_text, 0, int(page_count * 0.25))
        act2_text = self._extract_pages(screenplay_text, int(page_count * 0.25), int(page_count * 0.75))
        act3_text = self._extract_pages(screenplay_text, int(page_count * 0.75), page_count)

        # Analyze symbolism present (visual metaphors/symbols)
        symbolism_present = self._analyze_symbolism_present(screenplay_text)

        # Analyze symbol clarity (audience understands meaning)
        symbol_clarity = self._analyze_symbol_clarity(screenplay_text)

        # Analyze symbol consistency (used throughout, not random)
        symbol_consistency = self._analyze_symbol_consistency(screenplay_text, act1_text, act2_text, act3_text)

        # Analyze motif presence (recurring visual/thematic element)
        motif_presence = self._analyze_motif_presence(screenplay_text)

        # Analyze visual metaphor quality (shows abstract through concrete)
        visual_metaphor = self._analyze_visual_metaphor(screenplay_text)

        # Analyze color symbolism
        color_symbolism = self._analyze_color_symbolism(screenplay_text)

        # Analyze object symbolism (props carry meaning)
        object_symbolism = self._analyze_object_symbolism(screenplay_text)

        # Analyze setting symbolism (location reflects theme)
        setting_symbolism = self._analyze_setting_symbolism(screenplay_text)

        # Analyze character symbolism (character represents idea)
        character_symbolism = self._analyze_character_symbolism(screenplay_text)

        # Analyze title symbolism
        title_symbolism = self._analyze_title_symbolism(screenplay_text)

        # Analyze thematic resonance (symbols support theme)
        thematic_resonance = self._analyze_thematic_resonance(screenplay_text)

        # Analyze symbol subtlety (not heavy-handed)
        symbol_subtlety = self._analyze_symbol_subtlety(screenplay_text)

        # Detect heavy-handed symbolism (PENALTY - too obvious, preachy)
        heavy_handed = self._detect_heavy_handed(screenplay_text)

        # Detect confused symbolism (PENALTY - unclear meaning)
        confused_symbolism = self._detect_confused_symbolism(screenplay_text)

        # Detect inconsistent symbols (PENALTY - symbol changes meaning)
        inconsistent_symbols = self._detect_inconsistent_symbols(screenplay_text)

        # Build symbolism profile
        symbolism_profile = SymbolismProfile(
            symbolism_present=symbolism_present["present"],
            symbol_clarity=symbol_clarity["clear"],
            symbol_consistency=symbol_consistency["consistent"],
            motif_presence=motif_presence["present"],
            visual_metaphor_quality=visual_metaphor["high_quality"],
            color_symbolism=color_symbolism["present"],
            object_symbolism=object_symbolism["present"],
            setting_symbolism=setting_symbolism["present"],
            character_symbolism=character_symbolism["present"],
            title_symbolism=title_symbolism["present"],
            thematic_resonance=thematic_resonance["present"],
            symbol_subtlety=symbol_subtlety["subtle"],
            heavy_handed_detected=heavy_handed["detected"],
            confused_symbolism_detected=confused_symbolism["detected"],
            inconsistent_symbols_detected=inconsistent_symbols["detected"],
            overall_symbolism_quality=0.0  # calculated below
        )

        # Calculate overall symbolism quality
        symbolism_profile.overall_symbolism_quality = self._calculate_overall_symbolism_quality(symbolism_profile)

        # Check against rules
        rule_violations = self._check_symbolism_rules(
            symbolism_profile, symbolism_present, symbol_clarity, symbol_consistency,
            motif_presence, visual_metaphor, color_symbolism, object_symbolism,
            setting_symbolism, character_symbolism, title_symbolism,
            thematic_resonance, symbol_subtlety, heavy_handed,
            confused_symbolism, inconsistent_symbols
        )

        # Calculate score
        score = self._calculate_symbolism_score(symbolism_profile, rule_violations)

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, symbolism_profile, rule_violations)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "symbolism_present": {
                "present": symbolism_present["present"],
                "count": symbolism_present["count"],
                "list": symbolism_present["list"][:10]
            },
            "symbol_clarity": {
                "clear": symbol_clarity["clear"],
                "count": symbol_clarity["count"]
            },
            "symbol_consistency": {
                "consistent": symbol_consistency["consistent"],
                "count": symbol_consistency["count"],
                "act_distribution": symbol_consistency["act_distribution"]
            },
            "motif_presence": {
                "present": motif_presence["present"],
                "count": motif_presence["count"],
                "list": motif_presence["list"][:10]
            },
            "visual_metaphor": {
                "high_quality": visual_metaphor["high_quality"],
                "count": visual_metaphor["count"],
                "list": visual_metaphor["list"][:10]
            },
            "color_symbolism": {
                "present": color_symbolism["present"],
                "count": color_symbolism["count"],
                "list": color_symbolism["list"][:10]
            },
            "object_symbolism": {
                "present": object_symbolism["present"],
                "count": object_symbolism["count"],
                "list": object_symbolism["list"][:10]
            },
            "setting_symbolism": {
                "present": setting_symbolism["present"],
                "count": setting_symbolism["count"],
                "list": setting_symbolism["list"][:5]
            },
            "character_symbolism": {
                "present": character_symbolism["present"],
                "count": character_symbolism["count"],
                "list": character_symbolism["list"][:5]
            },
            "title_symbolism": {
                "present": title_symbolism["present"],
                "count": title_symbolism["count"]
            },
            "thematic_resonance": {
                "present": thematic_resonance["present"],
                "count": thematic_resonance["count"]
            },
            "symbol_subtlety": {
                "subtle": symbol_subtlety["subtle"],
                "count": symbol_subtlety["count"]
            },
            "heavy_handed": {
                "detected": heavy_handed["detected"],
                "penalty": heavy_handed.get("penalty", False),
                "count": heavy_handed["count"],
                "list": heavy_handed["list"][:5]
            },
            "confused_symbolism": {
                "detected": confused_symbolism["detected"],
                "penalty": confused_symbolism.get("penalty", False),
                "count": confused_symbolism["count"],
                "list": confused_symbolism["list"][:5]
            },
            "inconsistent_symbols": {
                "detected": inconsistent_symbols["detected"],
                "penalty": inconsistent_symbols.get("penalty", False),
                "count": inconsistent_symbols["count"],
                "list": inconsistent_symbols["list"][:5]
            },
            "overall_symbolism_quality": symbolism_profile.overall_symbolism_quality,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, symbolism_profile
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

    def _analyze_symbolism_present(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze symbolism present (visual metaphors/symbols exist).

        McKee: "Visual symbols and metaphors - show abstract ideas through concrete imagery."
        Truby: "Symbol web - interconnected symbols create thematic network, resonance."
        """
        present = False
        symbol_list = []

        # Check for symbolism markers
        count = 0
        for marker in self.symbolism_present_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract symbolism instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        symbol_list.append(line.strip()[:100])
                        if len(symbol_list) >= 20:
                            break

        if count >= 5:
            present = True
        elif count >= 3:
            present = True

        return {
            "present": present,
            "count": count,
            "list": symbol_list
        }

    def _analyze_symbol_clarity(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze symbol clarity (audience understands meaning).

        McKee: "Symbol must be clear - audience grasps meaning without confusion."
        Aristotle: "Metaphor clarity - balance between obscurity and obviousness."
        """
        clear = False

        # Check for clarity markers
        count = 0
        for marker in self.symbol_clarity_markers:
            count += screenplay.lower().count(marker)

        if count >= 3:
            clear = True
        elif count >= 2:
            clear = True

        return {
            "clear": clear,
            "count": count
        }

    def _analyze_symbol_consistency(self, screenplay: str, act1_text: str, act2_text: str, act3_text: str) -> Dict[str, Any]:
        """
        Analyze symbol consistency (used throughout, not random).

        McKee: "Symbol consistency - recurring throughout story, not random appearance."
        Truby: "Symbol web - symbols recur, build, deepen meaning across story."
        """
        consistent = False

        # Check for consistency markers
        count = 0
        for marker in self.symbol_consistency_markers:
            count += screenplay.lower().count(marker)

        # Check distribution across acts
        act1_count = sum(act1_text.lower().count(m) for m in self.symbol_consistency_markers[:10])
        act2_count = sum(act2_text.lower().count(m) for m in self.symbol_consistency_markers[:10])
        act3_count = sum(act3_text.lower().count(m) for m in self.symbol_consistency_markers[:10])

        # Consistency requires presence across multiple acts
        acts_with_symbols = sum([act1_count > 0, act2_count > 0, act3_count > 0])

        if acts_with_symbols >= 2:
            consistent = True
        elif count >= 4:
            consistent = True

        return {
            "consistent": consistent,
            "count": count,
            "act_distribution": {
                "act1": act1_count,
                "act2": act2_count,
                "act3": act3_count,
                "acts_with_symbols": acts_with_symbols
            }
        }

    def _analyze_motif_presence(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze motif presence (recurring visual/thematic element).

        McKee: "Motif - recurring visual or thematic element reinforces meaning."
        Vogler: "Recurring archetypal motifs - visual patterns echo mythic resonance."
        """
        present = False
        motif_list = []

        # Check for motif markers
        count = 0
        for marker in self.motif_presence_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract motif instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        motif_list.append(line.strip()[:100])
                        if len(motif_list) >= 20:
                            break

        if count >= 4:
            present = True
        elif count >= 2:
            present = True

        return {
            "present": present,
            "count": count,
            "list": motif_list
        }

    def _analyze_visual_metaphor(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze visual metaphor quality (shows abstract through concrete).

        McKee: "Visual metaphor - show abstract ideas through concrete visual imagery."
        Seger: "Visual storytelling - metaphors make abstract concepts visible, tangible."
        """
        high_quality = False
        visual_metaphor_list = []

        # Check for visual metaphor markers
        count = 0
        for marker in self.visual_metaphor_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract visual metaphor instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        visual_metaphor_list.append(line.strip()[:100])
                        if len(visual_metaphor_list) >= 20:
                            break

        if count >= 5:
            high_quality = True
        elif count >= 3:
            high_quality = True

        return {
            "high_quality": high_quality,
            "count": count,
            "list": visual_metaphor_list
        }

    def _analyze_color_symbolism(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze color symbolism (colors carry meaning).

        Seger: "Color symbolism - colors reinforce theme, emotion, character state."
        Mackendrick: "Visual design - color palette carries symbolic weight, meaning."
        """
        present = False
        color_list = []

        # Check for color symbolism markers
        count = 0
        for marker in self.color_symbolism_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract color symbolism instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        color_list.append(line.strip()[:100])
                        if len(color_list) >= 20:
                            break

        if count >= 3:
            present = True
        elif count >= 2:
            present = True

        return {
            "present": present,
            "count": count,
            "list": color_list
        }

    def _analyze_object_symbolism(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze object symbolism (props carry meaning).

        McKee: "Object symbolism - props carry thematic weight, represent ideas."
        Seger: "Meaningful objects - props with symbolic significance support theme."
        """
        present = False
        object_list = []

        # Check for object symbolism markers
        count = 0
        for marker in self.object_symbolism_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract object symbolism instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        object_list.append(line.strip()[:100])
                        if len(object_list) >= 20:
                            break

        if count >= 3:
            present = True
        elif count >= 2:
            present = True

        return {
            "present": present,
            "count": count,
            "list": object_list
        }

    def _analyze_setting_symbolism(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze setting symbolism (location reflects theme).

        McKee: "Setting symbolism - location embodies theme, reflects character state."
        Truby: "Symbolic setting - environment carries thematic meaning, resonance."
        """
        present = False
        setting_list = []

        # Check for setting symbolism markers
        count = 0
        for marker in self.setting_symbolism_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract setting symbolism instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        setting_list.append(line.strip()[:100])
                        if len(setting_list) >= 20:
                            break

        if count >= 3:
            present = True
        elif count >= 2:
            present = True

        return {
            "present": present,
            "count": count,
            "list": setting_list
        }

    def _analyze_character_symbolism(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze character symbolism (character represents idea/concept).

        Truby: "Symbolic character - character embodies idea, represents concept allegorically."
        Vogler: "Archetypal character - character represents universal idea, mythic concept."
        """
        present = False
        character_list = []

        # Check for character symbolism markers
        count = 0
        for marker in self.character_symbolism_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract character symbolism instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        character_list.append(line.strip()[:100])
                        if len(character_list) >= 20:
                            break

        if count >= 3:
            present = True
        elif count >= 2:
            present = True

        return {
            "present": present,
            "count": count,
            "list": character_list
        }

    def _analyze_title_symbolism(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze title symbolism (title reflects theme/meaning).

        Snyder: "Title symbolism - title embodies central theme, symbolic meaning."
        McKee: "Meaningful title - reflects core idea, thematic resonance."
        """
        present = False

        # Check for title symbolism markers
        count = 0
        for marker in self.title_symbolism_markers:
            count += screenplay.lower().count(marker)

        if count >= 2:
            present = True
        elif count >= 1:
            present = True

        return {
            "present": present,
            "count": count
        }

    def _analyze_thematic_resonance(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze thematic resonance (symbols support theme).

        McKee: "Thematic resonance - symbols reinforce theme, create unity."
        Truby: "Symbol web - interconnected symbols support thematic unity."
        """
        present = False

        # Check for thematic resonance markers
        count = 0
        for marker in self.thematic_resonance_markers:
            count += screenplay.lower().count(marker)

        if count >= 4:
            present = True
        elif count >= 2:
            present = True

        return {
            "present": present,
            "count": count
        }

    def _analyze_symbol_subtlety(self, screenplay: str) -> Dict[str, Any]:
        """
        Analyze symbol subtlety (not heavy-handed).

        McKee: "Symbol subtlety - nuanced, layered, sophisticated - not obvious."
        Truby: "Avoid heavy-handed symbolism - subtle, implicit, suggestive."
        """
        subtle = False

        # Check for subtlety markers
        count = 0
        for marker in self.symbol_subtlety_markers:
            count += screenplay.lower().count(marker)

        if count >= 3:
            subtle = True
        elif count >= 2:
            subtle = True

        return {
            "subtle": subtle,
            "count": count
        }

    def _detect_heavy_handed(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect heavy-handed symbolism (PENALTY - too obvious, preachy).

        McKee: "Heavy-handed symbolism - too obvious, preachy, lacks subtlety - worst flaw."
        Seger: "Avoid sledgehammer symbolism - audience feels insulted, patronized."
        """
        detected = False
        penalty = False
        heavy_list = []

        # Check for heavy-handed markers
        count = 0
        for marker in self.heavy_handed_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract heavy-handed instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        heavy_list.append(line.strip()[:100])
                        if len(heavy_list) >= 10:
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
            "list": heavy_list
        }

    def _detect_confused_symbolism(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect confused symbolism (PENALTY - unclear meaning).

        McKee: "Confused symbolism - unclear meaning, audience doesn't understand."
        Aristotle: "Metaphor must have clarity - obscurity without meaning fails."
        """
        detected = False
        penalty = False
        confused_list = []

        # Check for confused symbolism markers
        count = 0
        for marker in self.confused_symbolism_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract confused symbolism instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        confused_list.append(line.strip()[:100])
                        if len(confused_list) >= 10:
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
            "list": confused_list
        }

    def _detect_inconsistent_symbols(self, screenplay: str) -> Dict[str, Any]:
        """
        Detect inconsistent symbols (PENALTY - symbol changes meaning).

        McKee: "Symbol consistency - meaning must remain stable, not shift randomly."
        Truby: "Inconsistent symbol undermines thematic unity, confuses audience."
        """
        detected = False
        penalty = False
        inconsistent_list = []

        # Check for inconsistent symbol markers
        count = 0
        for marker in self.inconsistent_symbols_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract inconsistent symbol instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        inconsistent_list.append(line.strip()[:100])
                        if len(inconsistent_list) >= 10:
                            break

        if count >= 2:
            detected = True
            penalty = True

        return {
            "detected": detected,
            "penalty": penalty,
            "count": count,
            "list": inconsistent_list
        }

    def _calculate_overall_symbolism_quality(self, profile: SymbolismProfile) -> float:
        """Calculate overall symbolism quality score."""
        scores = [
            1.0 if profile.symbolism_present else 0.5,  # Important (enriches story)
            1.0 if profile.symbol_clarity else 0.6,  # Important (audience must understand)
            1.0 if profile.symbol_consistency else 0.5,  # Important (recurring throughout)
            1.0 if profile.motif_presence else 0.7,  # Important (recurring element)
            1.0 if profile.visual_metaphor_quality else 0.6,  # Important (show abstract)
            1.0 if profile.color_symbolism else 0.8,  # Nice to have (sophisticated)
            1.0 if profile.object_symbolism else 0.8,  # Nice to have (props meaning)
            1.0 if profile.setting_symbolism else 0.8,  # Nice to have (environment meaning)
            1.0 if profile.character_symbolism else 0.8,  # Nice to have (allegorical)
            1.0 if profile.title_symbolism else 0.9,  # Nice to have (title meaning)
            1.0 if profile.thematic_resonance else 0.5,  # Critical (symbols support theme)
            1.0 if profile.symbol_subtlety else 0.6,  # Important (not heavy-handed)
            0.0 if profile.heavy_handed_detected else 1.0,  # PENALTY (critical violation)
            0.0 if profile.confused_symbolism_detected else 1.0,  # PENALTY (clarity issue)
            0.0 if profile.inconsistent_symbols_detected else 1.0  # PENALTY (consistency issue)
        ]

        # Average
        overall = sum(scores) / len(scores)

        return max(0.0, min(1.0, overall))

    def _check_symbolism_rules(self, profile: SymbolismProfile, symbolism_present: Dict,
                               symbol_clarity: Dict, symbol_consistency: Dict,
                               motif_presence: Dict, visual_metaphor: Dict,
                               color_symbolism: Dict, object_symbolism: Dict,
                               setting_symbolism: Dict, character_symbolism: Dict,
                               title_symbolism: Dict, thematic_resonance: Dict,
                               symbol_subtlety: Dict, heavy_handed: Dict,
                               confused_symbolism: Dict, inconsistent_symbols: Dict) -> List[Dict]:
        """Check symbolism against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "SYMBOLISM.R001":
                # Symbolism Present
                if not profile.symbolism_present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Symbolism weak - limited visual metaphors/symbols detected",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R002":
                # Symbol Clarity
                if not profile.symbol_clarity:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Symbol clarity weak - audience may not understand meaning",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R003":
                # Symbol Consistency
                if not profile.symbol_consistency:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Symbol consistency weak - not recurring throughout story",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R004":
                # Motif Presence
                if not profile.motif_presence:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Motif missing - no recurring visual/thematic element",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R005":
                # Visual Metaphor Quality
                if not profile.visual_metaphor_quality:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Visual metaphor weak - not showing abstract through concrete",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R006":
                # Color Symbolism
                if not profile.color_symbolism:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Color symbolism missing - colors not carrying meaning",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R007":
                # Object Symbolism
                if not profile.object_symbolism:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Object symbolism missing - props not carrying thematic meaning",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R008":
                # Setting Symbolism
                if not profile.setting_symbolism:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Setting symbolism missing - location not reflecting theme",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R009":
                # Character Symbolism
                if not profile.character_symbolism:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Character symbolism missing - characters not representing ideas",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R010":
                # Title Symbolism
                if not profile.title_symbolism:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Title symbolism missing - title not reflecting theme/meaning",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R011":
                # Thematic Resonance
                if not profile.thematic_resonance:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Thematic resonance weak - symbols not supporting theme",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R012":
                # Symbol Subtlety
                if not profile.symbol_subtlety:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Symbol subtlety weak - symbolism not nuanced/layered",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R013":
                # Avoid Heavy-Handed Symbolism
                if profile.heavy_handed_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Heavy-handed symbolism detected - too obvious, preachy, lacks subtlety",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R014":
                # Avoid Confused Symbolism
                if profile.confused_symbolism_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Confused symbolism detected - unclear meaning, audience doesn't understand",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "SYMBOLISM.R015":
                # Avoid Inconsistent Symbols
                if profile.inconsistent_symbols_detected:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Inconsistent symbols detected - symbol meaning shifts/contradicts",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_symbolism_score(self, profile: SymbolismProfile, violations: List) -> float:
        """Calculate overall symbolism score."""
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
        if profile.heavy_handed_detected:
            score -= 25  # Critical penalty (worst violation)
        if profile.confused_symbolism_detected:
            score -= 20  # High penalty (clarity failure)
        if profile.inconsistent_symbols_detected:
            score -= 15  # High penalty (consistency failure)

        # Bonus for excellence
        if profile.overall_symbolism_quality > 0.85:
            score += 5
        elif profile.overall_symbolism_quality > 0.75:
            score += 3

        if profile.symbolism_present and profile.thematic_resonance:
            score += 5  # McKee's excellence (symbols support theme)

        if profile.symbol_subtlety and not profile.heavy_handed_detected:
            score += 3  # Sophisticated symbolism

        if profile.motif_presence and profile.symbol_consistency:
            score += 3  # Recurring motif (sophisticated)

        if profile.visual_metaphor_quality:
            score += 2  # Shows abstract through concrete

        if profile.symbol_clarity and not profile.confused_symbolism_detected:
            score += 2  # Clear symbols

        # Cap at 95
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profile: SymbolismProfile,
                           violations: List) -> str:
        """Generate symbolism diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Symbolism sophisticated with clear visual metaphors, thematic resonance, and subtlety"
        elif score >= 60:
            level = "GOOD"
            summary = "Symbolism present but could be more sophisticated or consistent"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Symbolism problems - heavy-handed, unclear, or inconsistent"
        else:
            level = "POOR"
            summary = "Major symbolism problems - heavy-handed, confused, or lacking"

        diagnosis = f"SYMBOLISM {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if not profile.symbolism_present:
            issues.append("limited symbolism")
        if not profile.symbol_clarity:
            issues.append("unclear symbols")
        if not profile.symbol_consistency:
            issues.append("inconsistent symbols")
        if profile.heavy_handed_detected:
            issues.append("heavy-handed")
        if profile.confused_symbolism_detected:
            issues.append("confused symbolism")
        if not profile.thematic_resonance:
            issues.append("weak thematic resonance")
        if not profile.motif_presence:
            issues.append("no motif")
        if not profile.symbol_subtlety:
            issues.append("lacks subtlety")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _generate_recommendations(self, score: float, violations: List,
                                  profile: SymbolismProfile) -> List[str]:
        """Generate specific symbolism recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if not profile.symbolism_present:
            recommendations.append("Add visual symbolism - McKee: 'Visual symbols and metaphors show abstract ideas through concrete imagery'")

        if not profile.symbol_clarity:
            recommendations.append("Improve symbol clarity - Aristotle: 'Metaphor must balance clarity and subtlety - audience must understand'")

        if not profile.symbol_consistency:
            recommendations.append("Strengthen symbol consistency - Truby: 'Symbol web - symbols recur, build, deepen meaning across story'")

        if profile.heavy_handed_detected:
            recommendations.append("Eliminate heavy-handed symbolism - McKee: 'Avoid sledgehammer symbolism - subtle, nuanced, layered symbols resonate'")

        if profile.confused_symbolism_detected:
            recommendations.append("Clarify confused symbolism - Aristotle: 'Metaphor without clarity fails - audience must grasp meaning'")

        if profile.inconsistent_symbols_detected:
            recommendations.append("Fix inconsistent symbols - McKee: 'Symbol meaning must remain stable throughout - inconsistency confuses'")

        if not profile.thematic_resonance:
            recommendations.append("Strengthen thematic resonance - Truby: 'Symbol web - interconnected symbols support thematic unity'")

        if not profile.motif_presence:
            recommendations.append("Add recurring motif - McKee: 'Motif - recurring visual/thematic element reinforces meaning, creates resonance'")

        if not profile.visual_metaphor_quality:
            recommendations.append("Improve visual metaphor - Seger: 'Visual storytelling - metaphors make abstract concepts visible, tangible'")

        if not profile.symbol_subtlety:
            recommendations.append("Increase symbol subtlety - McKee: 'Symbol subtlety - nuanced, layered, sophisticated - not obvious'")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study McKee's Story - symbolism and visual metaphor principles essential")
            recommendations.append("Study Truby's Anatomy - symbol web and thematic network design")

        return recommendations[:5]

    def export_symbolism_features(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Export symbolism features for correlation/analysis.

        Returns structured data with symbolism metrics.
        """
        symbolism_present = self._analyze_symbolism_present(screenplay_text)
        symbol_clarity = self._analyze_symbol_clarity(screenplay_text)
        motif_presence = self._analyze_motif_presence(screenplay_text)
        thematic_resonance = self._analyze_thematic_resonance(screenplay_text)

        return {
            "symbolism": {
                "symbolism_present": symbolism_present["present"],
                "symbol_clarity": symbol_clarity["clear"],
                "motif_presence": motif_presence["present"],
                "thematic_resonance": thematic_resonance["present"]
            },
            "meta": {
                "source": "DrSymbolism",
                "focus": "Symbolism and metaphor analysis"
            }
        }


# Compatibility class for testing framework
class DrSymbolismAnalysis(DrSymbolism):
    """Alias for compatibility with test framework."""
    pass
