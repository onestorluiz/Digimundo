"""
Script Doctor Charactermon - Character Architecture and Development Specialist
A Script Doctor™ in Digimon form specializing in character depth, arc, and transformation.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class CharacterProfile:
    """Deep profile analysis for a character."""
    name: str
    total_scenes: int
    total_dialogue_lines: int
    total_actions: int
    dimension_score: float  # 0-1 (physical, psychological, social)
    arc_present: bool
    transformation_points: List[str]
    weakness_identified: bool
    desire_identified: bool
    internal_conflict: bool
    external_conflict: bool
    moral_choices: int
    relationship_count: int
    consistency_score: float  # 0-1
    archetype: str


@dataclass
class CharacterMoment:
    """A specific character development moment."""
    character: str
    scene_context: str
    moment_type: str  # weakness, desire, choice, transformation, revelation
    description: str
    act_position: str  # act1, act2, act3
    reveals_dimension: str  # physical, psychological, social


class DrCharacter:
    """
    Script Doctor Charactermon - The Character Architecture and Development Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing character depth,
    transformation arcs, true character revelation, and dimensional construction.

    Identity: Script Doctor first, Digimon character specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Charactermon with rules and configuration."""
        self.name = "Script Doctor Charactermon"
        self.digimon_name = "Charactermon"
        self.title = "Script Doctor - Character Architecture and Development Specialist"
        self.specialty = "Character depth, transformation arcs, true character, dimensional construction"
        self.identity = "I am Script Doctor Charactermon, a professional Script Doctor™ specializing in character architecture"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "character_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - CHARACTER SPECIFIC
        self.deep_context_queries = [
            # McKee Story - Character foundations
            "McKee Story true character revealed under pressure choices actions",
            "McKee Story character dimension layers complexity depth authenticity",
            "McKee Story character arc transformation change growth journey",
            "McKee Story character desire conscious goal vs unconscious need",
            "McKee Story character choices reveal true nature moral essence",
            "McKee Story character consistency authentic believable motivation",
            "McKee Story active protagonist drives story vs passive observer",
            "McKee Story character flaw weakness vulnerability humanity",
            "McKee Story character backstory ghost wound past trauma",
            "McKee Story supporting characters function serve protagonist journey",
            "McKee Story character revelation sequence progressive discovery",
            "McKee Story character contradiction complexity paradox realistic",

            # McKee Story - TRUE CHARACTER vs CHARACTERIZATION (ultra-specific manual reading)
            "McKee Story true character revealed pressure choices crisis decision under stress",
            "McKee Story characterization mask surface observable versus true character depth",
            "McKee Story character choices crisis moral reveal true nature essence core being",
            "McKee Story active protagonist drives story forward versus passive observer reactive",
            "McKee Story character arc death rebirth transformation change growth journey complete",
            "McKee Story character dimension three levels physical psychological social layers depth",
            "McKee Story character consistency authentic believable motivation organic natural behavior",

            # Truby Anatomy - Character architecture
            "Truby Anatomy character weakness psychological flaw need transformation",
            "Truby Anatomy character ghost past wound drives present behavior",
            "Truby Anatomy character moral argument worldview philosophy belief",
            "Truby Anatomy character desire line clear objective goal",
            "Truby Anatomy character web relationships network design opponents allies",
            "Truby Anatomy seven key character elements weakness need desire",
            "Truby Anatomy opponent character mirror reveals protagonist weakness",
            "Truby Anatomy ally character supports enables protagonist journey",
            "Truby Anatomy character revelation sequence planned design structure",
            "Truby Anatomy character self-revelation moment anagnorisis change",

            # Field Screenplay - Three-dimensional character
            "Field Screenplay three-dimensional character physical psychological social dimensions",
            "Field Screenplay character biography backstory history shapes present",
            "Field Screenplay character paradigm structure setup confrontation resolution",
            "Field Screenplay character growth obstacles conflict transformation",
            "Field Screenplay character point of view perspective worldview",
            "Field Screenplay inner character thoughts feelings vs outer behavior",
            "Field Screenplay character dramatic need drives story forward",
            "Field Screenplay character attitude defines behavior choices",

            # Snyder Save the Cat - Transformation mechanics
            "Snyder Save Cat save the cat moment likability empathy connection",
            "Snyder Save Cat transformation machine character arc A to B",
            "Snyder Save Cat character primal drives survival instincts universal",
            "Snyder Save Cat six things need fixing character flaws issues",
            "Snyder Save Cat dark night soul character lowest point crisis",
            "Snyder Save Cat character learns lesson theme stated internalized",
            "Snyder Save Cat stasis=death character must change or die",

            # Vogler Writer's Journey - Archetypal character
            "Vogler Writer's Journey hero archetype protagonist center journey",
            "Vogler Journey mentor archetype wisdom guidance supernatural aid",
            "Vogler Journey threshold guardian archetype tests hero commitment",
            "Vogler Journey herald archetype call adventure change catalyst",
            "Vogler Journey shapeshifter archetype doubt uncertainty ally/enemy",
            "Vogler Journey shadow archetype dark side villain antagonist",
            "Vogler Journey ally archetype companion support friendship",
            "Vogler Journey trickster archetype comic relief disruption chaos",
            "Vogler Journey hero transformation emotional inner journey stages",
            "Vogler Journey character faces inner demons shadow self",

            # Campbell Hero 1000 Faces - Mythic character journey
            "Campbell Hero 1000 Faces monomyth character separation initiation return",
            "Campbell Hero call adventure character ordinary world disrupted",
            "Campbell Hero refusal call character hesitation fear doubt",
            "Campbell Hero supernatural aid mentor magic helper appears",
            "Campbell Hero threshold crossing character commits journey",
            "Campbell Hero trials tests character proves worth courage",
            "Campbell Hero abyss ordeal character faces death rebirth",
            "Campbell Hero return elixir character brings wisdom home",
            "Campbell Hero character transformation death rebirth resurrection",

            # Aristotle Poetics - Character essence
            "Aristotle Poetics hamartia tragic flaw character fatal weakness",
            "Aristotle Poetics character consistency appropriate realistic believable",
            "Aristotle Poetics character moral choices ethical decisions reveal",
            "Aristotle Poetics character driven action vs plot driven",
            "Aristotle Poetics peripeteia reversal character fortune changes",
            "Aristotle Poetics anagnorisis recognition character realizes truth",
            "Aristotle Poetics character nobility stature tragic hero elevated",

            # Egri Art Dramatic Writing - Character construction
            "Egri Art Dramatic Writing character premise driven spine foundation",
            "Egri Art Dramatic Writing character dominant trait defining quality",
            "Egri Art Dramatic Writing tri-dimensional character physiology sociology psychology",
            "Egri Art Dramatic Writing character orchestration contrast conflict variety",
            "Egri Art Dramatic Writing character growth dialectical thesis antithesis synthesis",
            "Egri Art Dramatic Writing character unity opposites internal conflict",

            # Seger Making Good Script Great - Character craft
            "Seger Making Good Script Great character likability relatability empathy",
            "Seger character consistency believable authentic motivation",
            "Seger character transformation arc change growth journey",
            "Seger character backstory integration reveal show don't tell",
            "Seger character relationships dynamics reveal character nature",
            "Seger character attitude behavior reveals personality essence",

            # Weiland Creating Character Arcs - Arc structure
            "Weiland Creating Character Arcs positive change arc growth transformation",
            "Weiland Character Arcs negative change arc corruption fall tragedy",
            "Weiland Character Arcs flat arc character unchanging tests world",
            "Weiland Character lie vs truth character believes vs reality",
            "Weiland Character ghost wound past trauma drives behavior",
            "Weiland Character want vs need surface goal vs deep need",

            # Goldman Adventures Screen Trade - Character pragmatics
            "Goldman Adventures Screen Trade character behavior action reveals nature",
            "Goldman character active choices drive story forward momentum",
            "Goldman character interesting compelling watchable engaging audience",

            # Rhimes Year of Yes - Character authenticity
            "Rhimes Year of Yes character authentic voice distinctive unique real",
            "Rhimes character vulnerability humanity flawed relatable empathy",
            "Rhimes character emotional truth honest raw real feelings",

            # Mamet Writing/Three Uses - Character objectives
            "Mamet Writing character wants objective clear dramatic need",
            "Mamet character action pursuit objective drives every scene",
            "Mamet character obstacle opposition creates conflict drama",

            # Mackendrick On Film-making - Character behavior
            "Mackendrick On Film-making character behavior reveals show don't tell",
            "Mackendrick character visual external action reveals internal state"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story characterization surface traits mask desire behavior style speech",
        "McKee Story true character revealed through choice under pressure dilemma",
        "McKee Story choices action reaction under pressure reveal essential nature",
        "McKee Story character dimension contradiction within nature consistent complexity",
        "McKee Story contradiction between characterization deep character charming thief",
        "McKee Story center of good positive focus empathy audience bond",
        "McKee Story audience seeks center of good even among gangsters",
        "McKee Story empathy like me identification desire pursuit not sympathy",
        "McKee Story audience bond convert curiosity concern into identification",
        "McKee Story conscious desire unconscious desire object of desire spine",
        "McKee Story protagonist willful capacity pursue desire to end of line",
        "McKee Story comedy character blind obsession humour mania unseen by self",
        "McKee Story laugh at contradiction oblivious bigotry greed vanity",
        "McKee Story mind worm inciting incident tailored psyche forces quest",
        "McKee Story burrow psyche design event unique dilemma fulfill humanity",
        "McKee Story cast design orbit protagonist delineate dimensions through conflict",
        "McKee Story supporting roles provoke facets hero reacts different ways",

        # McKee DIALOGUE - GPT-5 extracted (12 Oct 2025)
        "McKee Dialogue true character revealed risk-filled choices under pressure",
        "McKee Dialogue characterization surface traits voice diction syntax idiom",
        "McKee Dialogue vocabulary names knowledge verbs specificity reveal intellect",
        "McKee Dialogue modifiers adjectives adverbs modals express personality attitudes",
        "McKee Dialogue character voice walking dictionary unique word hoard",
        "McKee Dialogue authenticity real versus realistic speech believable manner",
        "McKee Dialogue high-context culture economy unsaid shared experience dialogue",
        "McKee Dialogue low-context culture verbosity explicitness diversity gap",
        "McKee Dialogue comic character blind obsession monomania drives dialogue",
        "McKee Dialogue dramatic character awareness irony risk flexible thought",
        "McKee Dialogue idiolect dialect idiom without stereotype cliché authenticity",
        "McKee Dialogue dialogue originality begins vocabulary choices character-specific",

        # Campbell Hero 1000 Faces - GPT-5 (12 Oct 2025)
        "Campbell Hero archetype hero threshold guardian mentor herald trickster,",
        "Campbell Hero hero archetype reluctant willing antihero destined chosen,",
        "Campbell Hero shadow projection confrontation integration redemption,",
        "Campbell Hero shapeshifter ambiguity allure betrayal revelation trust,",
        "Campbell Hero mentor wisdom talisman initiation tests withdrawal,",
        "Campbell Hero herald summons intuition omen anomaly invitation,",
        "Campbell Hero trickster disruption comic relief sacred misrule,",
        "Campbell Hero woman temptress projection repression castration anxiety,",
        "Campbell Hero meeting goddess anima wholeness sacred marriage,",
        "Campbell Hero atonement father authority law superego reconciliation,",
        "Campbell Hero apotheosis self transcending ego illumination bliss,",
        "Campbell Hero master two worlds mediator translator diplomat,",
        "Campbell Hero freedom live present-centered fearlessness spontaneity,",
        "Campbell Hero refusal call neurosis fixation regression stasis,",
        "Campbell Hero belly whale regression incubation ego dissolution,",
        "Campbell Hero road trials resilience adaptability learning growth,",
        "Campbell Hero ultimate boon compassion service generosity sharing,",
        "Campbell Hero rescue without humility openness receptivity grace,",
        "Campbell Hero magic flight improvisation shapeshift deception escape,",
        "Campbell Hero return threshold humility reintegration service obligation,",
        "Campbell Hero tyrant king ego inflation possession shadow takeover,",
        "Campbell Hero redeemer emissary bodhisattva compassion vow,",
        "Campbell Hero martyrdom sacrifice crucifixion transformation meaning,",
        "Campbell Hero temptation pride hubris fall redemption insight,",
        "Campbell Hero transformation death rebirth identity shedding renewal,",
        "Campbell Hero tests difficult wit endurance courage mercy,",
        "Campbell Hero boon theft trickster demiurge igniting culture,",
        "Campbell Hero divine child prodigy wonder precocity destiny,",
        "Campbell Hero orphan exile outsider liminality perspective,",
        "Campbell Hero monster slayer dragon shadow integration treasure,",
        "Campbell Hero healer shaman underworld journey soul retrieval,",
        "Campbell Hero king priest judge lawgiver culture hero,",
        "Campbell Hero lover wooing ordeal union separation,",
        "Campbell Hero warrior conquest liberation overthrow ogre tyrant,",
        "Campbell Hero magician hermes mercurius guide psychopomp,",
        "Campbell Hero saint ascetic renunciation inwardness nonattachment,",
        "Campbell Hero trickster redeemer creative destruction renewal cycle,",
        "Campbell Hero herald crisis catalyst inciting signal omen,",
        "Campbell Hero guide woman spider grandmother wise helper,",
        "Campbell Hero helper animal bird serpent horse ally,",
        "Campbell Hero talisman amulet ring thread boon conduit,",
        "Campbell Hero sacrifice dismemberment offering restitution renewal,",
        "Campbell Hero return teacher transmitter law rite ritual,",
        "Campbell Hero bodhisattva compassion renunciation nirvana postponement,",
        "Campbell Hero sage silence inexpressible ineffable transmission,",
        "Campbell Hero prince pauper disguise humility revelation worthiness,",
        "Campbell Hero tests mercy sparing monster seed continuity,",
        "Campbell Hero boundary crosser liminal identity versatility,",
        "Campbell Hero wounded healer initiation scar mark,",
        "Campbell Hero descent facing fear annihilation acceptance,",
        "Campbell Hero ecstatic dance song poetry spell enchantment,",
        "Campbell Hero communion feast sharing elixir love,",
        "Campbell Hero elder return sponsor initiate succession,",
        "Campbell Hero mask persona divinity embodiment performance,",
        "Campbell Hero vow quest obligation promise destiny,",

        # Truby Anatomy 22 Steps - GPT-5 (12 Oct 2025)
        "Truby Anatomy character web function hero opponent ally fake-ally subplot comparison",
        "Truby Anatomy creating the hero weakness need moral psychological arc layered construction",
        "Truby Anatomy best character love to watch act think challenge fascination identification",
        "Truby Anatomy individualizing character theme opposition value set power status ability",
        "Truby Anatomy archetype king queen mentor warrior magician trickster lover rebel mapping",
        "Truby Anatomy shadow negative tendency archetype trap psychological pattern translation",
        "Truby Anatomy double technique hero opponent mirroring similarity contrast defining",
        "Truby Anatomy necessary opponent attacks great weakness relentless pressure growth",
        "Truby Anatomy fake-ally opponent deception dilemma torn loyalty structural surprise",
        "Truby Anatomy fake-opponent ally apparent conflict hidden friendship limited utility",
        "Truby Anatomy subplot character parallel line same problem different result comparison",
        "Truby Anatomy four-corner opposition hero main opponent secondary opponents box",
        "Truby Anatomy cutting extraneous characters function test story purpose elimination",
        "Truby Anatomy multiple heroes narrative drive techniques funnel cliffhanger coincidence",
        "Truby Anatomy requirements of a hero mystery empathy not sympathy moral need inclusion",
        "Truby Anatomy character change beliefs challenged new moral action range of change",
        "Truby Anatomy double reversal hero opponent mutual learning moral stereo insight",
        "Truby Anatomy metamorphosis extreme change symbol attachment beast human switch",
        "Truby Anatomy leader to tyrant arc power corruption moral fall structural indicators",
        "Truby Anatomy cynic to participant rejoining society recommitment service transformation",

        # Field Screenplay Paradigm - GPT-5 (12 Oct 2025)
        "Field Screenplay dramatic need wants win gain get achieve engine drives character",
        "Field Screenplay action is character behavior reveals who person is not what says",
        "Field Screenplay character arc transformation change beginning to end stages growth",
        "Field Screenplay point of view belief system world is as you see it",
        "Field Screenplay attitude manner opinion judgment right wrong optimistic pessimistic superior inferior",
        "Field Screenplay interior life from birth forms character biography creative research",
        "Field Screenplay exterior life reveals character professional personal private dimensions",
        "Field Screenplay professional life workplace boss coworkers job description relationships conflict",
        "Field Screenplay personal life marriage single divorced widowed commitments social circle",
        "Field Screenplay private life alone hobbies routines secrets habits reveal character",
        "Field Screenplay main character versus major character who story is about decisions",
        "Field Screenplay incident illuminates character Henry James determination of incident",
        "Field Screenplay character biography first ten years second ten years third ten years",
        "Field Screenplay forms character interior reveals character exterior diagram distinction",
        "Field Screenplay reluctant hero accepts destiny choice responsibility creative decisions",
        "Field Screenplay function of main character drives plot points moves story forward",
        "Field Screenplay character determines incident hub of wheel key event",
        "Field Screenplay internal versus external need emotional physical goal destination",
        "Field Screenplay writing from inside out character driving structure choices",
        "Field Screenplay protagonist active force causes things to happen not merely reacts",

        # Vogler Writer's Journey - GPT-5 (12 Oct 2025)
        "Vogler Journey hero archetype ego self sacrifice transformation audience identification",
        "Vogler Journey willing hero gung-ho committed no reluctance swift acceptance",
        "Vogler Journey reluctant hero fear hesitation obligations excuses threshold",
        "Vogler Journey anti-hero wounded cynical outlaw audience sympathy outsider",
        "Vogler Journey tragic hero hamartia hubris nemesis downfall cautionary",
        "Vogler Journey catalyst hero unchanged sparks transformation in others",
        "Vogler Journey group-oriented hero separation initiation return reintegration",
        "Vogler Journey loner hero outsider re-entry into group discomfort solitude",
        "Vogler Journey wounded hero psychic scars guilt trauma vulnerability",
        "Vogler Journey character flaws imperfection neuroses defenses growth arc",
        "Vogler Journey growth learning mentor lover villain teachers",
        "Vogler Journey apotheosis godlike awareness death of ego transcendence",
        "Vogler Journey sacred marriage inner balance anima animus integration",
        "Vogler Journey standing up to parent youth versus age generational conflict",
        "Vogler Journey demonization projecting shadow qualities onto enemy",
        "Vogler Journey shadow mask within villain as dark possibility of hero",
        "Vogler Journey shapeshifter love interest suspicion ambiguity doubt",
        "Vogler Journey trickster comic relief mischief cuts ego down change",
        "Vogler Journey mentor wise old man woman donor gifts training",
        "Vogler Journey herald messenger announces need for change challenge",

            # McKee Character - GPT-5 (12 Oct 2025)
            "McKee Character characterization outer traits versus true character inner core revealed",
            "McKee Character outer character social personal selves mask behaviors audience first impressions",
            "McKee Character inner character core self agent self hidden self interplay",
            "McKee Character true character revealed by choices under pressure crisis decision",
            "McKee Character dimensional character pattern of consistent contradictions creates complexity",
            "McKee Character complex character contradictions private versus public selves depth subtext",
            "McKee Character completed character revelation epiphany resolves inner contradiction becoming",
            "McKee Character Center of Good empathy attraction positive charge within protagonist",
            "McKee Character character versus person finished work in performance metaphor humanity",
            "McKee Character character depth subtext silent currents subconscious desires radiate",
            "McKee Character credibility anchored by characterization believable actions speech behaviors",
            "McKee Character intrigue unique characterization invites curiosity about true character",
            "McKee Character moral imagination values at stake sculpt character identity",
            "McKee Character character-driven causality inner motives choices drive major events",
            "McKee Character plot-driven causality external forces test and expose character",
            "McKee Character freedom versus fate viewpoint before after events shapes perception",
            "McKee Character revelation decision turning point swivels event and identity",
            "McKee Character character limits patterns of contradiction explored to breaking point",
            "McKee Character character focus masks invite puzzle solving psychological acumen",
            "McKee Character character and time arc of becoming beyond story climax",

            # Egri Dramatic Writing - GPT-5 (12 Oct 2025)
            "Egri Dramatic three dimensions physiology sociology psychology complete character foundation",
            "Egri Dramatic bone structure character outline heredity health environment psychology",
            "Egri Dramatic environment shapes character cause and effect continuous change",
            "Egri Dramatic dialectical approach thesis antithesis synthesis within character",
            "Egri Dramatic character growth evolution crisis climax revolution inevitable",
            "Egri Dramatic strength of will in a character stamina to conflict",
            "Egri Dramatic pivotal character forces conflict proves premise through action",
            "Egri Dramatic antagonist orchestrated opposition unity of opposites sustained",
            "Egri Dramatic characters plotting their own play necessity compels decisions",
            "Egri Dramatic static versus jumping character consistency of behavior warned",
            "Egri Dramatic orchestration contrasting types arranged for maximum conflict",
            "Egri Dramatic unity of opposites binds characters cannot separate stakes",
            "Egri Dramatic decision creates conflict decision evokes counterdecision escalation",
            "Egri Dramatic character necessity force of necessity motivates behavior",
            "Egri Dramatic cause and effect within character physiology to psychology",
            "Egri Dramatic seed within character contains future development consequences",
            "Egri Dramatic point of attack turning point in character life",
            "Egri Dramatic strength weakness contradictions internal external pressures collide",
            "Egri Dramatic character must change through series of conflicts",
            "Egri Dramatic character revelation through dialogue action not author commentary",

            # Seger Script Great - GPT-5 (12 Oct 2025)
            "Seger Script character consistency logic coherent behavior choices across script",
            "Seger Script creating multidimensional characters thinking acting feeling integrated",
            "Seger Script attitude stance toward life expressed through action not speeches",
            "Seger Script philosophy values stated briefly shown through decisions and actions",
            "Seger Script transformational arc beat-by-beat change beginning middle end",
            "Seger Script decision to act reveal character moment leads to action",
            "Seger Script emotional palette sad mad glad hurt scared broaden range",
            "Seger Script character’s spine from motivation to goal define throughline",
            "Seger Script motivation present versus backstory clarify what drives choices",
            "Seger Script contrasting character highlights protagonist traits expands texture",
            "Seger Script confidant reveal without talky exposition show not tell",
            "Seger Script catalyst character causes events pushes protagonist into action",
            "Seger Script love interest adds dimension transformation intersects plotline",
            "Seger Script antagonist opposes protagonist raises conflict throughout",
            "Seger Script mass-and-weight characters confer stature bodyguard assistant choices",
            "Seger Script balance character grounds theme protects against misinterpretation",
            "Seger Script voice of character embodies wisdom clarity compassion non-preachy",
            "Seger Script writer’s point-of-view character convey idea through action",
            "Seger Script audience point-of-view character skeptic to suspend disbelief",
            "Seger Script character functions audit cut combine clarify roles",

            # Cowgill Short Films - GPT-5 (12 Oct 2025)
            "Cowgill Short character and emotion who does what and why",
            "Cowgill Short protagonist want why need define driving action",
            "Cowgill Short one protagonist carries the story limited emphasis",
            "Cowgill Short character revealed in action under stress conflict",
            "Cowgill Short choices decisions commitments reveal true character",
            "Cowgill Short story revelation character revelation linked at climax",
            "Cowgill Short antagonist fully motivated opposes hero’s goal",
            "Cowgill Short catalyst confidant supporting characters purposeful",
            "Cowgill Short back-story specific events impinge on present behavior",
            "Cowgill Short emotion beneath behavior audience identification quick",
            "Cowgill Short attitudes beliefs values shown through actions",
            "Cowgill Short want pulls need pushes possible opposition",
            "Cowgill Short transformation pressure of conflict produces change",
            "Cowgill Short important characters defined by what they do",
            "Cowgill Short character biography physical sociology psychology targeted",
            "Cowgill Short fear as driver uncover need and stakes",
            "Cowgill Short minimal cast focus on main relationship conflict",
            "Cowgill Short business nonverbal moments reveal inner life",
            "Cowgill Short keep focused what does my protagonist really want",
            "Cowgill Short unsympathetic protagonist workable in short screen time",

            # Aristotle Poetics - GPT-5 (12 Oct 2025)
            "Aristotle Poetics: How do I engineer a ‘middling’ protagonist whose downfall is di’ hamartian (recognitive error) rather than di’ kakian, keeping moral vice out of the causal engine?",
            "Aristotle Poetics: What concrete tests show my protagonist’s ethos is ‘fitting’ (prepon) and ‘consistent’ (homalon) with the action’s necessities, not a free-floating psychology?",
            "Aristotle Poetics: How can I stage ethos so that character is inferred from deeds/choices under necessity (praxeis), rather than expository lexis about traits?",
            "Aristotle Poetics: Where should I place the decisive choice that reveals hamartia as agnoia (misrecognition), to prepare anagnorisis without telegraphing?",
            "Aristotle Poetics: How can I align supporting characters’ ethos as oikeia to the mythos, ensuring each speech/act is what ‘such a person would likely/necessarily do’?",
            "Aristotle Poetics: What constraints keep a ‘noble’ lead from becoming ‘disgusting’ (miaron) if he suffers undeserved prosperity-loss or vice-punishment scenarios Aristotle rejects?",
            "Aristotle Poetics: How do I make ethos secondary (material) to mythos (formal) while preserving vividness—i.e., choose choices that the plot requires, not actor showcases?",
            "Aristotle Poetics: What scene design reveals a change in ethos only as a function of recognition and reversal, not independent self-improvement arcs?",
            "Aristotle Poetics: How do I ensure virtues/vices are not the efficient causes of outcomes, but that outcomes arise from actions where ethos merely makes the action plausible?",
            "Aristotle Poetics: How do I encode ethos through conflict goals so motivations read as eikos/ananke rather than screenwriter intent (ha bouletai ho poietes)?",
            "Aristotle Poetics: How can I avoid episodic ‘one-person-centred’ (peri hena) structures by distributing character beats strictly along the action’s causal spine?",
            "Aristotle Poetics: What diagnostic distinguishes hamartia-as-error from a plot hole, and how do I rewrite to convert contrivance into plausible ignorance?",
            "Aristotle Poetics: How do I design a ‘better than average’ character whose fall still evokes pity/fear without relying on innocence or villainy?",
            "Aristotle Poetics: How can antagonists’ ethos be arranged so their necessary actions intensify the primary action rather than spawn a second plot?",
            "Aristotle Poetics: How do I reconcile contemporary ‘agency’ expectations with Aristotle’s action-primacy, keeping ethos subordinate yet compelling?",
            "Aristotle Poetics: What are practical lexis tactics (choice of words) to display dianoia through ethos—arguments and maxims that are fitting for ‘such a person’?",
            "Aristotle Poetics: How do I stage a recognition that ethically reclassifies the protagonist (from seeming just to actually errant) without imputing vice?",
            "Aristotle Poetics: How can I ensure backstory traits only exist insofar as they set potentials (dynameis) that the plot actualizes?",
            "Aristotle Poetics: What beat placement allows ethos to be judged by action outcomes (sumbainei), not authorial commentary or spectators’ morals?",
            "Aristotle Poetics: How do I keep pathos aimed at actions so the audience’s pity/fear attach to what happens, not to a character’s performative suffering alone?",

            # Snyder Save the Cat - GPT-5 (12 Oct 2025)
            "Snyder Cat: Does your logline include a vivid adjective for the hero and antagonist, and do those traits drive choices in every BS2 zone?",
            "Snyder Cat: Is there a genuine Save the Cat beat early that aligns with the hero’s flaw/need and later becomes a strength/weakness in Act Two?",
            "Snyder Cat: Is the hero proactive (leads) by page 25, making the Act Two choice and never being dragged by plot or other characters?",
            "Snyder Cat: Can you map the hero’s arc (Covenant of the Arc) with specific scene beats (belief → test → break → choice → new behavior)?",
            "Snyder Cat: Is the hero’s goal primal and stated by page 10 (survival, love, status, protection), not abstract (e.g., ‘find fulfillment’)?",
            "Snyder Cat: Does the Debate show reluctance rooted in the hero’s flaw (not mere delay), making the Break into Two a growth step?",
            "Snyder Cat: Is the B-Story relationship complementary/oppositional to the hero’s flaw and designed to pressure change?",
            "Snyder Cat: Does your casting archetype (e.g., ‘good girl tempted,’ ‘young man on the rise’) fit the genre and demographic sweet spot?",
            "Snyder Cat: Do supporting characters have distinct ‘limp and eyepatch’ hooks (speech/look/gesture) and micro-arcs, avoiding sameness?",
            "Snyder Cat: Are the hero and main antagonist two sides of the same coin (mirrors), differing in moral choice rather than capability?",
            "Snyder Cat: Does the hero fail in a way unique to their flaw at Midpoint/All Is Lost, making the eventual change necessary and earned?",
            "Snyder Cat: Is the hero the author of the Finale win (no ally solving), proving internal change through external action?",
            "Snyder Cat: Have you written the hero’s age/presentation to match market (youth-skewed leads unless ensemble/family four-quadrant)?",
            "Snyder Cat: Does the hero’s Save the Cat trait reappear as a ‘lockpick’ in the Finale, validating it as more than a likability gimmick?",
            "Snyder Cat: Do ensemble pieces still designate a clear hero (carrier of the theme), even if POV is shared across threads?",
            "Snyder Cat: Are there at least two moments where the hero rejects and later accepts the B-Story ally’s thematic advice?",
            "Snyder Cat: Do you avoid ‘talking the plot’ in the hero’s dialogue, revealing character via action and subtext under pressure?",
            "Snyder Cat: Are villain goals and methods understandable (even tempting), making the hero’s divergence a choice, not inevitability?",
            "Snyder Cat: Is the hero’s final choice costly (sacrifice), demonstrating transformation beyond mere competence gain?",
            "Snyder Cat: Do you chart how the hero’s initial coping strategy fails repeatedly until a theme-aligned strategy replaces it?",

            # Weiland Character Arcs - GPT-5 (12 Oct 2025)
            "Weiland Arcs Positive Change Arc The Lie Your Character Believes The Truth Want vs Need",
            "Weiland Arcs Flat Arc protagonist holds Truth transforms world Impact Character steadfast catalyst",
            "Weiland Arcs Negative Change Arc Disillusionment Arc Fall Arc Corruption Arc descent",
            "Weiland Arcs The Lie Your Character Believes symptoms fear guilt shame secrecy resistance",
            "Weiland Arcs The Truth personalized antidote to the Lie internal transformation empowerment",
            "Weiland Arcs The Thing Your Character Wants external plot goal pursuit surface cure",
            "Weiland Arcs The Thing Your Character Needs internal realization sacrifice Truth over Want",
            "Weiland Arcs Want versus Need silent war interior conflict fuels exterior plot",
            "Weiland Arcs Character Growth measured against arc structure beats Lie to Truth",
            "Weiland Arcs Impact Character introduces Truth opposes protagonist’s Lie catalyzes transformation",
            "Weiland Arcs Disillusionment Arc overcome Lie discover tragic Truth cynical awakening",
            "Weiland Arcs Fall Arc clings to Lie rejects Truth embraces worse Lie",
            "Weiland Arcs Corruption Arc begins with Truth seduced by Lie tragic choice",
            "Weiland Arcs Character resists change First Act entrenched in Lie initial denial",
            "Weiland Arcs Midpoint Moment of Truth accepts Truth subconsciously divided self",
            "Weiland Arcs Third Plot Point ultimate choice Want versus Need death of self",
            "Weiland Arcs Climax prove Truth learned reject the Lie decisive confrontation",
            "Weiland Arcs Resolution new Normal World reflects embraced Truth thematic closure",
            "Weiland Arcs Thing They Want vs Thing They Need harmony after transformation",
            "Weiland Arcs Characteristic Moment reveals strengths weaknesses hints Lie Truth trajectory",













        ]

        # Character analysis patterns (bilingual: EN + PT)

        # Weakness markers (Truby's Ghost/Need)
        self.weakness_markers = [
            # English
            "afraid", "fear", "can't", "unable", "failure", "failed",
            "weak", "coward", "scared", "terrified", "avoid", "hiding",
            "won't face", "running from", "escaping", "denial",
            # Portuguese
            "medo", "receio", "não consigo", "incapaz", "falha", "fracasso",
            "fraco", "covarde", "assustado", "apavorado", "evitar", "escondendo",
            "não enfrenta", "fugindo de", "escapando", "negação"
        ]

        # Desire/want markers
        self.desire_markers = [
            # English
            "I want", "I need", "must have", "have to get", "desire",
            "dream", "goal", "ambition", "seeking", "searching for",
            "my mission", "my purpose", "I will", "determined to",
            # Portuguese
            "eu quero", "eu preciso", "tenho que ter", "preciso conseguir",
            "desejo", "sonho", "objetivo", "ambição", "buscando", "procurando",
            "minha missão", "meu propósito", "eu vou", "determinado a"
        ]

        # Moral choice indicators
        self.moral_choice_markers = [
            # English
            "should I", "must I", "right thing", "wrong thing",
            "conscience", "guilt", "betray", "sacrifice", "choose between",
            "dilemma", "torn between", "what's right", "what's wrong",
            # Portuguese
            "devo", "tenho que", "coisa certa", "coisa errada",
            "consciência", "culpa", "trair", "sacrificar", "escolher entre",
            "dilema", "dividido entre", "o que é certo", "o que é errado"
        ]

        # Transformation indicators
        self.transformation_markers = [
            # English
            "changed", "different now", "not who I was", "became",
            "transformed", "learned", "realized", "understood",
            "new person", "no longer", "finally see", "awakened",
            # Portuguese
            "mudei", "diferente agora", "não sou quem era", "me tornei",
            "transformei", "aprendi", "percebi", "entendi",
            "nova pessoa", "não mais", "finalmente vejo", "despertei"
        ]

        # Internal conflict markers
        self.internal_conflict_markers = [
            # English
            "part of me", "conflicted", "torn", "don't know who I am",
            "war within", "fighting myself", "can't decide", "what am I",
            # Portuguese
            "parte de mim", "conflitado", "dividido", "não sei quem sou",
            "guerra interna", "lutando comigo", "não consigo decidir", "o que sou"
        ]

        # External conflict markers
        self.external_conflict_markers = [
            # English
            "against", "enemy", "opponent", "versus", "fighting",
            "stop", "destroy", "defeat", "battle", "war",
            # Portuguese
            "contra", "inimigo", "oponente", "versus", "lutando",
            "parar", "destruir", "derrotar", "batalha", "guerra"
        ]

        # Character archetype patterns (Vogler/Campbell)
        self.archetype_patterns = {
            "hero": ["journey", "quest", "chosen", "destiny", "save", "protect"],
            "mentor": ["teach", "guide", "wisdom", "training", "master", "sensei"],
            "threshold_guardian": ["test", "challenge", "prove", "guardian", "gatekeeper"],
            "herald": ["message", "news", "announce", "call", "summon"],
            "shapeshifter": ["betray", "deceive", "mysterious", "ambiguous", "unclear"],
            "shadow": ["dark", "evil", "villain", "antagonist", "enemy", "nemesis"],
            "ally": ["friend", "companion", "help", "support", "together", "team"],
            "trickster": ["joke", "fool", "comedy", "relief", "clown", "jester"]
        }

        # Save the cat moment patterns
        self.save_cat_markers = [
            "help", "save", "rescue", "protect", "defend", "kind",
            "compassion", "mercy", "gentle", "care for"
        ]

        # Hamartia (tragic flaw) patterns
        self.hamartia_markers = [
            "pride", "hubris", "arrogance", "blind", "obsession",
            "ambition", "jealousy", "greed", "lust", "wrath"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze character architecture and development in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete character diagnostic report
        """
        # Extract character data
        character_appearances = self._extract_character_data(screenplay_text)

        # Build character profiles
        character_profiles = self._build_character_profiles(character_appearances, screenplay_text)

        # Analyze character dimensions
        dimension_analysis = self._analyze_character_dimensions(character_profiles)

        # Detect character arcs
        arc_analysis = self._detect_character_arcs(character_profiles, screenplay_text)

        # Find transformation moments
        transformation_moments = self._find_transformation_moments(screenplay_text)

        # Analyze weakness/need (Truby)
        weakness_analysis = self._analyze_weakness_need(character_profiles, screenplay_text)

        # Analyze desire lines
        desire_analysis = self._analyze_desire_lines(character_profiles, screenplay_text)

        # Check moral choices
        moral_choices = self._analyze_moral_choices(screenplay_text)

        # Detect archetypes (Vogler/Campbell)
        archetype_analysis = self._detect_archetypes(character_profiles, screenplay_text)

        # Find save the cat moments
        save_cat_moments = self._find_save_cat_moments(screenplay_text)

        # Detect hamartia (tragic flaw)
        hamartia_analysis = self._detect_hamartia(character_profiles, screenplay_text)

        # Check character consistency
        consistency_analysis = self._analyze_character_consistency(character_profiles, screenplay_text)

        # Analyze internal vs external conflict
        conflict_analysis = self._analyze_character_conflicts(character_profiles, screenplay_text)

        # Check true character revelation (McKee)
        true_character = self._analyze_true_character_revelation(screenplay_text)

        # Analyze character relationships
        relationship_network = self._analyze_character_relationships(screenplay_text)

        # Check against rules
        rule_violations = self._check_character_rules(
            dimension_analysis, arc_analysis, weakness_analysis,
            desire_analysis, moral_choices, consistency_analysis
        )

        # Calculate score
        score = self._calculate_character_score(
            dimension_analysis, arc_analysis, weakness_analysis,
            desire_analysis, moral_choices, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, character_profiles, arc_analysis,
            weakness_analysis, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "total_characters": len(character_profiles),
            "main_characters": len([p for p in character_profiles.values() if p.total_scenes >= 3]),
            "character_profiles": self._profiles_to_dict(character_profiles),
            "dimensional_score": dimension_analysis["overall_score"],
            "three_dimensional_characters": dimension_analysis["fully_dimensional"],
            "flat_characters": dimension_analysis["flat_characters"],
            "character_arcs_present": arc_analysis["arcs_present"],
            "characters_with_arcs": arc_analysis["characters_with_arcs"],
            "transformation_moments": len(transformation_moments),
            "transformation_examples": transformation_moments[:3],  # Top 3
            "weakness_identified": weakness_analysis["total_with_weakness"],
            "desire_identified": desire_analysis["total_with_desire"],
            "moral_choices_count": len(moral_choices),
            "moral_choice_examples": moral_choices[:3],  # Top 3
            "archetypes_detected": archetype_analysis["archetypes_found"],
            "save_cat_moments": len(save_cat_moments),
            "hamartia_present": hamartia_analysis["present"],
            "consistency_score": consistency_analysis["overall_score"],
            "inconsistent_characters": consistency_analysis["inconsistent_list"],
            "internal_conflict_score": conflict_analysis["internal_score"],
            "external_conflict_score": conflict_analysis["external_score"],
            "true_character_revelations": true_character["revelation_count"],
            "relationship_network_size": len(relationship_network["relationships"]),
            "isolated_characters": relationship_network["isolated"],
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, character_profiles,
                arc_analysis, weakness_analysis
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _extract_character_data(self, screenplay: str) -> Dict[str, Dict]:
        """Extract all character appearances, dialogue, and actions."""
        lines = screenplay.split('\n')
        character_data = defaultdict(lambda: {
            "scenes": [],
            "dialogue_lines": [],
            "actions": [],
            "scene_contexts": []
        })

        current_scene = "SCENE_1"
        scene_counter = 1

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Detect scene headings
            if any(marker in line.upper() for marker in ['INT.', 'EXT.']):
                current_scene = f"SCENE_{scene_counter}"
                scene_counter += 1
                i += 1
                continue

            # Detect character dialogue
            if (line.isupper() and
                len(line.split()) <= 3 and
                not any(marker in line for marker in ['INT.', 'EXT.', 'FADE', 'CUT', 'DISSOLVE'])):

                character = line.split('(')[0].strip()

                # Add scene appearance
                if current_scene not in character_data[character]["scenes"]:
                    character_data[character]["scenes"].append(current_scene)

                # Collect dialogue
                i += 1
                dialogue_text = []

                while i < len(lines) and lines[i].strip():
                    next_line = lines[i].strip()

                    if next_line.isupper() and not next_line.startswith('('):
                        break

                    if not next_line.startswith('('):
                        dialogue_text.append(next_line)

                    i += 1

                if dialogue_text:
                    full_dialogue = ' '.join(dialogue_text)
                    character_data[character]["dialogue_lines"].append({
                        "scene": current_scene,
                        "text": full_dialogue
                    })

                continue

            # Detect action lines with character names
            if line and not line.isupper():
                for character in character_data.keys():
                    if character in line:
                        character_data[character]["actions"].append({
                            "scene": current_scene,
                            "action": line
                        })

            i += 1

        return dict(character_data)

    def _build_character_profiles(self, character_data: Dict, screenplay: str) -> Dict[str, CharacterProfile]:
        """Build deep profiles for each character."""
        profiles = {}

        for character, data in character_data.items():
            if len(data["scenes"]) < 1:  # Skip characters with no real presence
                continue

            total_scenes = len(data["scenes"])
            total_dialogue = len(data["dialogue_lines"])
            total_actions = len(data["actions"])

            # Calculate dimension score (physical, psychological, social)
            dimension_score = self._calculate_dimension_score(data, screenplay)

            # Check for character arc
            arc_present = self._has_character_arc(character, data, screenplay)

            # Find transformation points
            transformations = self._find_character_transformations(character, data, screenplay)

            # Check weakness identification
            weakness_identified = self._has_weakness(character, data)

            # Check desire identification
            desire_identified = self._has_desire(character, data)

            # Check internal conflict
            internal_conflict = self._has_internal_conflict(character, data)

            # Check external conflict
            external_conflict = self._has_external_conflict(character, data)

            # Count moral choices
            moral_choices = self._count_moral_choices(character, data)

            # Count relationships
            relationship_count = self._count_relationships(character, character_data)

            # Calculate consistency
            consistency_score = self._calculate_consistency(character, data)

            # Detect archetype
            archetype = self._detect_character_archetype(character, data, screenplay)

            profiles[character] = CharacterProfile(
                name=character,
                total_scenes=total_scenes,
                total_dialogue_lines=total_dialogue,
                total_actions=total_actions,
                dimension_score=dimension_score,
                arc_present=arc_present,
                transformation_points=transformations,
                weakness_identified=weakness_identified,
                desire_identified=desire_identified,
                internal_conflict=internal_conflict,
                external_conflict=external_conflict,
                moral_choices=moral_choices,
                relationship_count=relationship_count,
                consistency_score=consistency_score,
                archetype=archetype
            )

        return profiles

    def _calculate_dimension_score(self, character_data: Dict, screenplay: str) -> float:
        """Calculate three-dimensional character score (Field's Physical/Psychological/Social)."""
        score = 0.0

        # Physical dimension: actions, physical descriptions
        if len(character_data["actions"]) > 5:
            score += 0.33

        # Psychological dimension: internal thoughts, emotions in dialogue
        psychological_markers = ["feel", "think", "believe", "remember", "wish"]
        psych_count = 0
        for dialogue in character_data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in psychological_markers):
                psych_count += 1

        if psych_count > 3:
            score += 0.33

        # Social dimension: relationships, interactions
        if len(character_data["dialogue_lines"]) > 5:
            score += 0.34

        return min(1.0, score)

    def _has_character_arc(self, character: str, data: Dict, screenplay: str) -> bool:
        """Check if character has a transformation arc."""
        # Look for transformation markers in dialogue
        for dialogue in data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in self.transformation_markers):
                return True

        # Check if character appears in different act contexts with different behaviors
        if len(data["scenes"]) >= 5:  # Need enough presence to track arc
            return True

        return False

    def _find_character_transformations(self, character: str, data: Dict, screenplay: str) -> List[str]:
        """Find specific transformation moments for character."""
        transformations = []

        for dialogue in data["dialogue_lines"]:
            for marker in self.transformation_markers:
                if marker in dialogue["text"].lower():
                    transformations.append(f"{dialogue['scene']}: {dialogue['text'][:60]}...")
                    break

        return transformations[:3]  # Top 3

    def _has_weakness(self, character: str, data: Dict) -> bool:
        """Check if character's weakness/need is identified (Truby)."""
        for dialogue in data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in self.weakness_markers):
                return True
        return False

    def _has_desire(self, character: str, data: Dict) -> bool:
        """Check if character's desire/want is identified."""
        for dialogue in data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in self.desire_markers):
                return True
        return False

    def _has_internal_conflict(self, character: str, data: Dict) -> bool:
        """Check for internal conflict."""
        for dialogue in data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in self.internal_conflict_markers):
                return True
        return False

    def _has_external_conflict(self, character: str, data: Dict) -> bool:
        """Check for external conflict."""
        for dialogue in data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in self.external_conflict_markers):
                return True

        # Also check actions
        for action in data["actions"]:
            if any(marker in action["action"].lower() for marker in self.external_conflict_markers):
                return True

        return False

    def _count_moral_choices(self, character: str, data: Dict) -> int:
        """Count moral choice moments."""
        count = 0
        for dialogue in data["dialogue_lines"]:
            if any(marker in dialogue["text"].lower() for marker in self.moral_choice_markers):
                count += 1
        return count

    def _count_relationships(self, character: str, all_character_data: Dict) -> int:
        """Count relationships with other characters."""
        relationships = set()

        # Find other characters that appear in same scenes
        character_scenes = set(all_character_data[character]["scenes"])

        for other_char, other_data in all_character_data.items():
            if other_char == character:
                continue

            other_scenes = set(other_data["scenes"])
            if character_scenes & other_scenes:  # Intersection
                relationships.add(other_char)

        return len(relationships)

    def _calculate_consistency(self, character: str, data: Dict) -> float:
        """Calculate character consistency score."""
        if len(data["dialogue_lines"]) < 3:
            return 0.5  # Not enough data

        # Check for consistent voice patterns
        word_lengths = []
        for dialogue in data["dialogue_lines"]:
            words = dialogue["text"].split()
            if words:
                avg_len = sum(len(w) for w in words) / len(words)
                word_lengths.append(avg_len)

        if not word_lengths:
            return 0.5

        # Low variance = high consistency
        mean = sum(word_lengths) / len(word_lengths)
        variance = sum((x - mean) ** 2 for x in word_lengths) / len(word_lengths)

        # Convert variance to consistency score
        consistency = max(0.0, 1.0 - (variance / 10.0))

        return min(1.0, consistency)

    def _detect_character_archetype(self, character: str, data: Dict, screenplay: str) -> str:
        """Detect character archetype (Vogler/Campbell)."""
        scores = defaultdict(int)

        # Check dialogue and actions for archetype patterns
        all_text = []
        for dialogue in data["dialogue_lines"]:
            all_text.append(dialogue["text"].lower())
        for action in data["actions"]:
            all_text.append(action["action"].lower())

        combined_text = ' '.join(all_text)

        for archetype, patterns in self.archetype_patterns.items():
            for pattern in patterns:
                if pattern in combined_text:
                    scores[archetype] += 1

        if not scores:
            return "undefined"

        return max(scores.items(), key=lambda x: x[1])[0]

    def _analyze_character_dimensions(self, profiles: Dict[str, CharacterProfile]) -> Dict[str, Any]:
        """Analyze character dimensions (Field's three dimensions)."""
        if not profiles:
            return {
                "overall_score": 0.0,
                "fully_dimensional": [],
                "flat_characters": []
            }

        dimension_scores = [p.dimension_score for p in profiles.values()]
        overall = sum(dimension_scores) / len(dimension_scores)

        fully_dimensional = [p.name for p in profiles.values() if p.dimension_score >= 0.8]
        flat_characters = [p.name for p in profiles.values() if p.dimension_score < 0.4]

        return {
            "overall_score": overall,
            "fully_dimensional": fully_dimensional,
            "flat_characters": flat_characters
        }

    def _detect_character_arcs(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Detect character arcs and transformations."""
        characters_with_arcs = [p.name for p in profiles.values() if p.arc_present]

        return {
            "arcs_present": len(characters_with_arcs) > 0,
            "characters_with_arcs": characters_with_arcs,
            "arc_percentage": (len(characters_with_arcs) / max(len(profiles), 1)) * 100
        }

    def _find_transformation_moments(self, screenplay: str) -> List[Dict]:
        """Find specific transformation moments in screenplay."""
        moments = []
        lines = screenplay.split('\n')

        current_character = None

        for i, line in enumerate(lines):
            line = line.strip()

            # Track current character
            if line.isupper() and len(line.split()) <= 3:
                current_character = line.split('(')[0].strip()

            # Check for transformation markers
            for marker in self.transformation_markers:
                if marker in line.lower() and current_character:
                    moments.append({
                        "character": current_character,
                        "moment": line[:80] + "..." if len(line) > 80 else line,
                        "type": "transformation"
                    })
                    break

        return moments

    def _analyze_weakness_need(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Analyze character weakness/need (Truby's Ghost)."""
        with_weakness = [p.name for p in profiles.values() if p.weakness_identified]

        return {
            "total_with_weakness": len(with_weakness),
            "characters": with_weakness,
            "percentage": (len(with_weakness) / max(len(profiles), 1)) * 100
        }

    def _analyze_desire_lines(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Analyze character desire lines."""
        with_desire = [p.name for p in profiles.values() if p.desire_identified]

        return {
            "total_with_desire": len(with_desire),
            "characters": with_desire,
            "percentage": (len(with_desire) / max(len(profiles), 1)) * 100
        }

    def _analyze_moral_choices(self, screenplay: str) -> List[Dict]:
        """Find moral choice moments."""
        choices = []
        lines = screenplay.split('\n')

        current_character = None

        for line in lines:
            line = line.strip()

            if line.isupper() and len(line.split()) <= 3:
                current_character = line.split('(')[0].strip()

            for marker in self.moral_choice_markers:
                if marker in line.lower() and current_character:
                    choices.append({
                        "character": current_character,
                        "choice": line[:80] + "..." if len(line) > 80 else line
                    })
                    break

        return choices

    def _detect_archetypes(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Detect character archetypes (Vogler/Campbell)."""
        archetype_counts = Counter()

        for profile in profiles.values():
            if profile.archetype != "undefined":
                archetype_counts[profile.archetype] += 1

        return {
            "archetypes_found": dict(archetype_counts),
            "total_archetypes": len(archetype_counts)
        }

    def _find_save_cat_moments(self, screenplay: str) -> List[Dict]:
        """Find 'save the cat' moments (Snyder)."""
        moments = []
        lines = screenplay.split('\n')

        current_character = None

        for line in lines:
            line = line.strip()

            if line.isupper() and len(line.split()) <= 3:
                current_character = line.split('(')[0].strip()

            for marker in self.save_cat_markers:
                if marker in line.lower() and current_character:
                    moments.append({
                        "character": current_character,
                        "moment": line[:80] + "..." if len(line) > 80 else line
                    })
                    break

        return moments[:5]  # Top 5

    def _detect_hamartia(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Detect tragic flaw (Aristotle's hamartia)."""
        hamartia_found = []

        for line in screenplay.split('\n'):
            for marker in self.hamartia_markers:
                if marker in line.lower():
                    hamartia_found.append(marker)
                    break

        return {
            "present": len(hamartia_found) > 0,
            "flaws_detected": list(set(hamartia_found))
        }

    def _analyze_character_consistency(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Analyze character consistency."""
        if not profiles:
            return {
                "overall_score": 0.5,
                "inconsistent_list": []
            }

        consistency_scores = [p.consistency_score for p in profiles.values()]
        overall = sum(consistency_scores) / len(consistency_scores)

        inconsistent = [p.name for p in profiles.values() if p.consistency_score < 0.5]

        return {
            "overall_score": overall,
            "inconsistent_list": inconsistent
        }

    def _analyze_character_conflicts(self, profiles: Dict[str, CharacterProfile], screenplay: str) -> Dict[str, Any]:
        """Analyze internal vs external conflict balance."""
        if not profiles:
            return {
                "internal_score": 0.0,
                "external_score": 0.0
            }

        internal_count = sum(1 for p in profiles.values() if p.internal_conflict)
        external_count = sum(1 for p in profiles.values() if p.external_conflict)

        total = len(profiles)

        return {
            "internal_score": internal_count / max(total, 1),
            "external_score": external_count / max(total, 1),
            "both_present": internal_count > 0 and external_count > 0
        }

    def _analyze_true_character_revelation(self, screenplay: str) -> Dict[str, Any]:
        """Analyze true character revelation under pressure (McKee)."""
        pressure_markers = [
            "must choose", "forced to", "no choice", "pressure",
            "dilemma", "crisis", "breaking point", "pushed to"
        ]

        revelations = []

        for line in screenplay.split('\n'):
            for marker in pressure_markers:
                if marker in line.lower():
                    revelations.append(line[:80] + "..." if len(line) > 80 else line)
                    break

        return {
            "revelation_count": len(revelations),
            "examples": revelations[:3]
        }

    def _analyze_character_relationships(self, screenplay: str) -> Dict[str, Any]:
        """Analyze character relationship network (Truby's character web)."""
        # Extract character co-appearances
        scenes = screenplay.split('INT.') + screenplay.split('EXT.')
        relationships = []
        characters_seen = set()

        for scene in scenes:
            scene_characters = []
            for line in scene.split('\n'):
                if line.strip().isupper() and len(line.strip().split()) <= 3:
                    char = line.strip().split('(')[0].strip()
                    if char and not any(m in char for m in ['FADE', 'CUT', 'DISSOLVE']):
                        scene_characters.append(char)
                        characters_seen.add(char)

            # Create relationships
            for i in range(len(scene_characters)):
                for j in range(i + 1, len(scene_characters)):
                    relationships.append((scene_characters[i], scene_characters[j]))

        isolated = [c for c in characters_seen if not any(c in r for r in relationships)]

        return {
            "relationships": relationships[:20],  # Top 20
            "total_relationships": len(set(relationships)),
            "isolated": isolated
        }

    def _check_character_rules(self, dimension_analysis: Dict, arc_analysis: Dict,
                               weakness_analysis: Dict, desire_analysis: Dict,
                               moral_choices: List, consistency_analysis: Dict) -> List[Dict]:
        """Check character architecture against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "CHAR.R001":
                # Three-dimensional characters
                if dimension_analysis["overall_score"] < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low dimensional score: {dimension_analysis['overall_score']:.0%}",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "CHAR.R002":
                # Character arc required
                if not arc_analysis["arcs_present"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No character arcs detected",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "CHAR.R003":
                # Weakness/Need identified
                if weakness_analysis["percentage"] < 30:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Only {weakness_analysis['percentage']:.0f}% have weakness",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "CHAR.R004":
                # Desire line clear
                if desire_analysis["percentage"] < 30:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Only {desire_analysis['percentage']:.0f}% have desire",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "CHAR.R005":
                # Moral choices present
                if len(moral_choices) < 1:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No moral choices detected",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "CHAR.R006":
                # Character consistency
                if consistency_analysis["overall_score"] < 0.6:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low consistency: {consistency_analysis['overall_score']:.0%}",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_character_score(self, dimension_analysis: Dict, arc_analysis: Dict,
                                   weakness_analysis: Dict, desire_analysis: Dict,
                                   moral_choices: List, violations: List) -> float:
        """Calculate overall character architecture score."""
        # Start at 85 (not 100 - no character work is perfect)
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

        # Bonus for excellence (max +15, capped at 95)
        if dimension_analysis["overall_score"] > 0.9:
            score += 5
        elif dimension_analysis["overall_score"] > 0.7:
            score += 3

        if arc_analysis["arc_percentage"] > 80:
            score += 5
        elif arc_analysis["arc_percentage"] > 60:
            score += 3

        if len(moral_choices) > 3:
            score += 5
        elif len(moral_choices) > 1:
            score += 3

        # Cap at 95 (not 100 - always room for improvement)
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profiles: Dict, arc_analysis: Dict,
                          weakness_analysis: Dict, violations: List) -> str:
        """Generate character diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Characters are well-architected with clear dimensions and arcs"
        elif score >= 60:
            level = "GOOD"
            summary = "Characters work but could be more dimensional"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Character architecture issues affecting depth"
        else:
            level = "POOR"
            summary = "Major character construction problems throughout"

        diagnosis = f"CHARACTER {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if not arc_analysis["arcs_present"]:
            issues.append("no character arcs")
        if weakness_analysis["percentage"] < 30:
            issues.append("unclear weaknesses/needs")
        if len([p for p in profiles.values() if p.dimension_score < 0.5]) > len(profiles) / 2:
            issues.append("flat characters")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _profiles_to_dict(self, profiles: Dict[str, CharacterProfile]) -> List[Dict]:
        """Convert character profiles to dictionaries."""
        result = []
        for name, profile in profiles.items():
            result.append({
                "name": name,
                "scenes": profile.total_scenes,
                "dialogue_lines": profile.total_dialogue_lines,
                "dimension_score": profile.dimension_score,
                "has_arc": profile.arc_present,
                "transformations": len(profile.transformation_points),
                "has_weakness": profile.weakness_identified,
                "has_desire": profile.desire_identified,
                "internal_conflict": profile.internal_conflict,
                "external_conflict": profile.external_conflict,
                "moral_choices": profile.moral_choices,
                "consistency": profile.consistency_score,
                "archetype": profile.archetype
            })
        return result

    def _generate_recommendations(self, score: float, violations: List,
                                 profiles: Dict, arc_analysis: Dict,
                                 weakness_analysis: Dict) -> List[str]:
        """Generate specific character recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:  # Top 3 violations
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        flat_characters = [p.name for p in profiles.values() if p.dimension_score < 0.5]
        if flat_characters:
            recommendations.append(f"Add dimensions to: {', '.join(flat_characters[:3])}")

        if not arc_analysis["arcs_present"]:
            recommendations.append("Design transformation arcs showing character change")

        if weakness_analysis["percentage"] < 30:
            recommendations.append("Establish clear weakness/need for main characters (Truby's Ghost)")

        no_moral = [p.name for p in profiles.values() if p.moral_choices == 0]
        if len(no_moral) > 0:
            recommendations.append(f"Add moral choices for: {', '.join(no_moral[:3])}")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study character construction in acclaimed screenplays")
            recommendations.append("Apply McKee's True Character revelation under pressure")

        return recommendations[:5]  # Return top 5

    def export_character_features(self, screenplay_text: str) -> List[Dict]:
        """
        Export character features for correlation/analysis.

        Returns structured data with character metrics per character.
        Useful for external indexing, correlation engines, or ML pipelines.

        Args:
            screenplay_text: Full screenplay text

        Returns:
            List of dicts with keys:
                - character_name: Character identifier
                - dimensions: Physical/Psychological/Social scores
                - arc_data: Transformation points and arc structure
                - relationships: Character web connections
                - meta: Additional metadata
        """
        character_data = self._extract_character_data(screenplay_text)
        profiles = self._build_character_profiles(character_data, screenplay_text)

        features = []

        for character, profile in profiles.items():
            char_features = {
                "character_name": character,
                "dimensions": {
                    "overall_score": profile.dimension_score,
                    "has_physical": len(character_data[character]["actions"]) > 0,
                    "has_psychological": profile.internal_conflict,
                    "has_social": profile.relationship_count > 0
                },
                "arc_data": {
                    "has_arc": profile.arc_present,
                    "transformation_count": len(profile.transformation_points),
                    "transformations": profile.transformation_points
                },
                "character_traits": {
                    "weakness_identified": profile.weakness_identified,
                    "desire_identified": profile.desire_identified,
                    "moral_choices": profile.moral_choices,
                    "archetype": profile.archetype
                },
                "conflict_structure": {
                    "internal": profile.internal_conflict,
                    "external": profile.external_conflict
                },
                "relationships": {
                    "count": profile.relationship_count,
                    "scenes": profile.total_scenes
                },
                "consistency": {
                    "score": profile.consistency_score
                },
                "meta": {
                    "total_dialogue_lines": profile.total_dialogue_lines,
                    "total_actions": profile.total_actions,
                    "source": "DrCharacter"
                }
            }

            features.append(char_features)

        return features


# Compatibility class for testing framework
class DrCharacterArchitecture(DrCharacter):
    """Alias for compatibility with test framework."""
    pass
