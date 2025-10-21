"""
Author-Specific Prompts for Scripturemon v12.0

Each screenplay theory author (McKee, Truby, Field, etc.) gets personalized
prompts that emphasize their specific methodology and ensure high-quality
analysis (15K+ chars, 3+ scenes, 3+ quotes, 2+ ANTES/DEPOIS).

Based on reverse engineering from MCKEE_DIALOGUE (8/10) and CAMPBELL (7/10).

Author: Scripturemon Team
Date: 2025-10-10
Version: 12.0
"""

from typing import Dict, Any


# ============================================================================
# AUTHOR-SPECIFIC REQUIREMENTS
# ============================================================================

AUTHOR_SPECIFIC_REQUIREMENTS = {
    'dialogue': {
        'focus': 'DIALOGUE ANALYSIS (Multi-Theory Approach)',
        'theory_book': 'Multiple dialogue theory books',
        'instructions': """
FOCUS: Comprehensive dialogue analysis using 7 theory books

MUST ANALYZE:
1. **Subtexto** (McKee): Identify on-the-nose vs. subtext dialogue
   - Cite 3+ scenes where dialogue lacks subtext
   - Quote 3+ examples of on-the-nose dialogue
   - Provide ANTES/DEPOIS rewrites showing subtextual alternatives

2. **Voz Única** (Egri): Each character's distinctive voice
   - Cite scenes where characters sound too similar
   - Quote dialogue showing voice confusion
   - Rewrite to give each character unique patterns

3. **Conflito** (Truby): Dialogue revealing character conflict
   - Cite scenes with weak conflict
   - Quote passive/agreeable dialogue
   - Rewrite to add tension and opposition

4. **Economia** (Cowgill): Every word must count
   - Cite verbose dialogue moments
   - Quote unnecessarily long speeches
   - Rewrite to be concise yet powerful

MANDATORY FORMAT FOR EACH PROBLEM:
"PROBLEMA X: [Type] ([Theory Citation])
CENA [number] (página [number]): [Context]
DIÁLOGO ATUAL: '[Quote verbatim from screenplay]'
ANÁLISE: [Why this is problematic using theory]

SOLUÇÃO:
ANTES: '[Current dialogue]'
DEPOIS: '[Improved dialogue]'
RESULTADO ESPERADO: [What this achieves]"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['McKee', 'Egri', 'Truby', 'Cowgill', 'Field', 'Seger', 'Yorke']
    },

    'egri': {
        'focus': 'PREMISE (Lajos Egri - The Art of Dramatic Writing)',
        'theory_book': 'The Art of Dramatic Writing',
        'instructions': """
FOCUS: Identify and strengthen screenplay's PREMISE

EGRI'S METHOD:
1. **Core Premise**: "X leads to Y" (ex: "Ruthless ambition leads to destruction")
   - Identify screenplay's premise in one sentence
   - Cite 3+ scenes demonstrating this premise
   - Quote 3+ key dialogues that reveal/support premise

2. **Character Premise Alignment**: Do characters embody the premise?
   - Cite scenes where characters act against premise
   - Quote dialogue contradicting premise
   - Rewrite to align character actions/words with premise

3. **Premise Through Action**: Show, don't tell
   - Identify exposition-heavy dialogue
   - Quote dialogue that TELLS premise instead of SHOWING
   - Rewrite to show premise through character behavior

4. **Premise Clarity**: Is premise clear throughout?
   - Cite scenes where premise gets muddy
   - Quote confusing/contradictory dialogue
   - Rewrite to reinforce premise

MANDATORY EXAMPLE:
"PREMISE IDENTIFICADA: 'Medo de vulnerabilidade leva ao isolamento'

CENA 5 (página 12): Sofia evita intimidade com Julio
DIÁLOGO ATUAL: 'Eu tenho medo de me abrir' (on-the-nose)
ANÁLISE: Egri diria que personagem DECLARA premissa ao invés de VIVER

SOLUÇÃO:
ANTES: 'Eu tenho medo de me abrir'
DEPOIS: [Sofia desvia olhar] 'Vamos falar de outra coisa?'
RESULTADO: Ação demonstra medo sem declarar (Egri, Cap. 4: Premise)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Egri']
    },

    'field': {
        'focus': 'THREE-ACT STRUCTURE (Syd Field - Screenplay)',
        'theory_book': 'Screenplay: The Foundations of Screenwriting',
        'instructions': """
FOCUS: Analyze THREE-ACT STRUCTURE through dialogue

FIELD'S PARADIGM:
1. **Plot Point 1** (end of Act 1, ~page 25-30)
   - Cite EXACT PAGE where protagonist makes key decision
   - Quote DIALOGUE at this turning point
   - Rewrite if turning point is weak/unclear

2. **Midpoint** (middle of Act 2, ~page 60)
   - Cite scene where stakes raise/direction shifts
   - Quote dialogue marking this shift
   - Rewrite to make midpoint more dramatic

3. **Plot Point 2** (end of Act 2, ~page 85-90)
   - Cite page where all seems lost/final push begins
   - Quote dialogue at this low/high point
   - Rewrite to strengthen transition to Act 3

4. **Dialogue Marking Structure**: How dialogue reveals acts
   - Cite dialogue that foreshadows turning points
   - Quote setup/payoff dialogues across acts
   - Rewrite to make structure clearer through dialogue

MANDATORY EXAMPLE:
"PLOT POINT 1 (página 28): Sofia decide deixar Pedro e ir para SP

DIÁLOGO ATUAL:
Pedro: 'Você não vai mesmo?'
Sofia: 'Não. Eu vou.' (weak, on-the-nose)

ANÁLISE: Field enfatiza que Plot Point 1 deve VIRAR a história em nova direção.
Este diálogo é passivo, não marca virada clara.

SOLUÇÃO:
ANTES: 'Não. Eu vou.'
DEPOIS: [Sofia põe aliança na mesa] 'A passagem já está comprada.'
RESULTADO: Ação física + diálogo concreto = virada clara (Field, Paradigm)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Field']
    },

    'mckee': {
        'focus': 'STORY DESIGN PRINCIPLES (Robert McKee - Story)',
        'theory_book': 'Story: Substance, Structure, Style and the Principles of Screenwriting',
        'instructions': """
FOCUS: McKee's STORY DESIGN through dialogue

McKEE'S PRINCIPLES:
1. **Scene Design**: Every scene must turn (value change)
   - Cite 3+ scenes without clear value turn
   - Quote dialogue that fails to advance story
   - Rewrite to create turning points through dialogue

2. **Gap Between Expectation & Result**: Surprise through dialogue
   - Cite predictable dialogue moments
   - Quote exchanges where outcome is obvious
   - Rewrite to create gap (subtext, reversal, irony)

3. **Show Don't Tell**: Action over exposition
   - Cite exposition-heavy dialogue
   - Quote telling vs showing moments
   - Rewrite to show through behavior/subtext

4. **True Character**: Pressure reveals character
   - Cite dialogue under no pressure
   - Quote safe/comfortable exchanges
   - Rewrite to add pressure revealing true nature

MANDATORY EXAMPLE:
"PROBLEMA: Cena sem turning point (McKee, Cap. 17: Scene Design)

CENA 8 (página 22): Maria confronta Sofia sobre decisão

DIÁLOGO ATUAL:
Maria: 'Você tem certeza disso?'
Sofia: 'Sim, tenho.'
[fim da cena - sem mudança]

ANÁLISE: McKee: 'Cena sem turning point é cena morta'. Valores começam
e terminam iguais (Sofia: decidida → decidida).

SOLUÇÃO:
ANTES: 'Sim, tenho.'
DEPOIS: Sofia: 'Sim... [pausa] Você acha que estou errada?'
         Maria: [silêncio]
         Sofia: 'Maria?'

RESULTADO: Valor vira de 'certeza' para 'dúvida' (McKee turning point)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['McKee']
    },

    'truby': {
        'focus': '22 STEPS TO STORY (John Truby - The Anatomy of Story)',
        'theory_book': 'The Anatomy of Story: 22 Steps to Becoming a Master Storyteller',
        'instructions': """
FOCUS: Map screenplay to Truby's 22 BUILDING BLOCKS

TRUBY'S 22 STEPS (focus on key ones):
1. **Self-Revelation (Step 1)**: Character's deep need
   - Cite scenes revealing protagonist's need
   - Quote dialogue hinting at need
   - Rewrite to make need clearer

2. **Ghost/Wound (Step 2)**: Past trauma
   - Cite scenes where ghost is revealed
   - Quote dialogue referencing past
   - Rewrite to deepen wound through subtext

3. **Desire (Step 3)**: What character wants
   - Cite where desire is stated
   - Quote dialogue expressing want
   - Rewrite to show want through action/dialogue

4. **Opponent (Step 8-10)**: Character blocking desire
   - Cite confrontation scenes
   - Quote dialogue showing opposition
   - Rewrite to sharpen conflict

5. **Battle (Step 19)**: Final confrontation
   - Cite climax dialogue
   - Quote key exchange in battle
   - Rewrite to heighten stakes

MANDATORY EXAMPLE:
"STEP 2: GHOST/WOUND - MISSING in current screenplay

DEVERIA APARECER: Cena 3 (página 7) - Sofia conhece Julio

ADICIONAR DIÁLOGO:
Julio: 'Você parece tensa. Tudo bem?'
Sofia: [forçando sorriso] 'Só... última vez que senti isso não acabou bem.'
Julio: 'Sentiu o quê?'
Sofia: [muda de assunto] 'Nada. Você quer café?'

RESULTADO: Estabelece ghost/wound sem expor demais (Truby, Step 2: Ghost)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Truby']
    },

    'snyder': {
        'focus': '15 SAVE THE CAT BEATS (Blake Snyder - Save the Cat)',
        'theory_book': 'Save the Cat: The Last Book on Screenwriting You\'ll Ever Need',
        'instructions': """
FOCUS: Identify Snyder's 15 BEATS through dialogue

BLAKE SNYDER'S 15 BEATS:
1. **Opening Image** (page 1): Establish world/character
   - Quote FIRST dialogue of screenplay
   - Analyze what it establishes
   - Rewrite if weak opening

2. **Catalyst** (page 12): Inciting incident
   - Cite page where life changes
   - Quote dialogue at catalyst moment
   - Rewrite to make catalyst clearer

3. **Break into Two** (page 25): Commit to journey
   - Cite EXACT page of commitment
   - Quote dialogue showing decision
   - Rewrite to mark beat clearly

4. **B Story** (page 30): Relationship/theme
   - Cite where B story character appears
   - Quote dialogue establishing relationship
   - Rewrite to deepen B story connection

5. **Midpoint** (page 60): False victory/defeat
   - Cite midpoint scene
   - Quote dialogue at this peak/valley
   - Rewrite to heighten midpoint

6. **All Is Lost** (page 75): Lowest point
   - Cite where hope dies
   - Quote dialogue of despair
   - Rewrite to deepen darkness

MANDATORY EXAMPLE:
"BEAT 3: BREAK INTO TWO (página 26)

ATUAL: Sofia decide ir para São Paulo (implícito, sem diálogo claro)

PROBLEMA: Snyder diz Beat 3 deve ser MOMENTO CLARO de decisão.
Aqui está vago.

SOLUÇÃO - ADICIONAR DIÁLOGO:
INT. CASA MARIA - NOITE
Maria: 'Então você vai mesmo?'
Sofia: [respira fundo, liga laptop, compra passagem]
Sofia: 'Pronto. Não tem mais volta.'

RESULTADO: Ação + diálogo = break into two claro (Snyder, Beat 3)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Snyder']
    },

    'vogler': {
        'focus': "HERO'S JOURNEY (Christopher Vogler - The Writer's Journey)",
        'theory_book': "The Writer's Journey: Mythic Structure for Writers",
        'instructions': """
FOCUS: Map screenplay to 12 STAGES of Hero's Journey

VOGLER'S 12 STAGES:
1. **Ordinary World** (Act 1 opening)
   - Cite scenes establishing normal life
   - Quote dialogue showing ordinary world
   - Rewrite to contrast with special world

2. **Call to Adventure** (Act 1, ~page 10)
   - Cite scene where call comes
   - Quote dialogue delivering call
   - Rewrite to make call more compelling

3. **Refusal of Call** (Act 1, ~page 15)
   - Cite where hero resists
   - Quote dialogue of refusal/doubt
   - Rewrite to deepen fear/resistance

4. **Meeting Mentor** (Act 1, ~page 20)
   - Cite mentor introduction scene
   - Quote advice/wisdom given
   - Rewrite to make mentor more impactful

5. **Crossing Threshold** (Act 2 opening, ~page 25-30)
   - Cite threshold crossing scene
   - Quote dialogue marking entrance to special world
   - Rewrite to heighten commitment

6. **Tests, Allies, Enemies** (Act 2a)
   - Cite scenes establishing relationships
   - Quote dialogue showing alliances/conflicts
   - Rewrite to clarify relationships

MANDATORY EXAMPLE:
"STAGE 3: REFUSAL OF CALL (página 15)

CENA: Julio convida Sofia para trabalho em SP

DIÁLOGO ATUAL:
Julio: 'Vem para São Paulo comigo.'
Sofia: 'Não sei... tenho medo.'

ANÁLISE: Vogler diz Refusal deve mostrar RAZÃO profunda do medo,
geralmente ligada ao wound.

SOLUÇÃO:
ANTES: 'Não sei... tenho medo.'
DEPOIS:
Sofia: [desvia olhar] 'Última pessoa que me pediu para largar tudo...'
Julio: 'O que aconteceu?'
Sofia: [levanta] 'Desculpa, preciso ir.'

RESULTADO: Refusal com ghost/wound, mais profundo (Vogler, Stage 3)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Vogler', 'Campbell']
    },

    'campbell': {
        'focus': "HERO'S JOURNEY (Joseph Campbell - The Hero with a Thousand Faces)",
        'theory_book': 'The Hero with a Thousand Faces',
        'instructions': """
FOCUS: Archetypal patterns in dialogue (Campbell's Monomyth)

CAMPBELL'S MONOMYTH STAGES:
1. **Departure** (Separation from ordinary world)
   - Cite dialogue showing resistance to leaving
   - Quote exchanges revealing attachment to old world
   - Rewrite to deepen departure tension

2. **Initiation** (Trials and transformation)
   - Cite dialogue during trials
   - Quote moments of doubt/growth
   - Rewrite to show transformation through dialogue

3. **Return** (Bringing gift back)
   - Cite dialogue showing wisdom gained
   - Quote how hero shares knowledge
   - Rewrite to make return gift clearer

4. **Archetypal Characters**: Mentor, Threshold Guardian, Shadow
   - Cite scenes with archetypal figures
   - Quote dialogue revealing archetype
   - Rewrite to strengthen archetypal function

MANDATORY EXAMPLE:
"ARQUÉTIPO: MENTOR (Campbell, Part 1: Departure)

CENA 4 (página 10): Maria aconselha Sofia sobre mudança

DIÁLOGO ATUAL:
Maria: 'Você deveria ir. É uma boa oportunidade.'

ANÁLISE: Campbell diz Mentor deve dar DÁDIVA (gift/tool) ao herói.
Aqui é apenas conselho genérico.

SOLUÇÃO:
ANTES: 'Você deveria ir. É uma boa oportunidade.'
DEPOIS:
Maria: [pega foto antiga] 'Quando eu tinha sua idade, também tive medo.'
Maria: 'Sabe o que aprendi? Arrepender do que fez dói menos que arrepender do que não fez.'
Maria: [dá foto] 'Essa sou eu em Paris. Sozinha. Melhor decisão da minha vida.'

RESULTADO: Mentor dá DÁDIVA concreta (sabedoria + símbolo) (Campbell, Mentor)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Campbell']
    },

    'seger': {
        'focus': 'SCRIPT PROBLEMS & SOLUTIONS (Linda Seger - Making a Good Script Great)',
        'theory_book': 'Making a Good Script Great',
        'instructions': """
FOCUS: Identify common script problems Seger addresses

SEGER'S COMMON PROBLEMS:
1. **On-the-Nose Dialogue**: Characters say exactly what they mean
   - Cite 3+ on-the-nose moments
   - Quote direct/obvious dialogue
   - Rewrite with subtext/indirection

2. **Weak Obstacles**: No opposition/conflict
   - Cite scenes where characters agree too easily
   - Quote passive dialogue
   - Rewrite to add obstacles/resistance

3. **Unclear Motivation**: Why character acts
   - Cite actions without clear motivation
   - Quote dialogue that doesn't reveal why
   - Rewrite to show motivation through dialogue

4. **Predictable Dialogue**: No surprises
   - Cite predictable exchanges
   - Quote expected responses
   - Rewrite with unexpected turns/reversals

MANDATORY EXAMPLE:
"PROBLEMA 1: ON-THE-NOSE DIALOGUE (Seger, Cap. 5: Dialogue)

CENA 7 (página 18): Sofia revela sentimentos

DIÁLOGO ATUAL:
Sofia: 'Eu gosto muito de você, Julio. Tenho medo de me machucar.'

ANÁLISE: Seger: 'Good dialogue has subtext'. Aqui Sofia DECLARA tudo
explicitamente. Sem camadas, sem subtexto.

SOLUÇÃO:
ANTES: 'Eu gosto muito de você, Julio. Tenho medo de me machucar.'
DEPOIS:
Sofia: [mexe no colar nervosamente] 'Você... você sempre é assim?'
Julio: 'Como assim?'
Sofia: 'Tão... [procura palavra] ...presente.'
Julio: [se aproxima] 'Isso é ruim?'
Sofia: [recua] 'Não sei ainda.'

RESULTADO: Sentimentos revelados através de AÇÃO + SUBTEXTO (Seger)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Seger']
    },

    'cowgill': {
        'focus': 'SHORT FILM STRUCTURE (Linda J. Cowgill - Writing Short Films)',
        'theory_book': 'Writing Short Films: Structure and Content for Screenwriters',
        'instructions': """
FOCUS: Economy and compression in dialogue

COWGILL'S SHORT FILM PRINCIPLES:
1. **Economy of Words**: Every word must count
   - Cite verbose dialogue moments
   - Quote unnecessarily long speeches
   - Rewrite to be concise yet impactful

2. **Visual Storytelling**: Show, don't say
   - Cite dialogue that could be action
   - Quote telling vs showing
   - Rewrite to replace dialogue with action

3. **Character Essence**: Reveal quickly
   - Cite slow character reveals
   - Quote exposition-heavy introductions
   - Rewrite to show character essence immediately

4. **Compression**: Full story in less space
   - Cite scenes that could be combined
   - Quote redundant dialogue
   - Rewrite to compress without losing meaning

MANDATORY EXAMPLE:
"PROBLEMA: EXCESSO DE PALAVRAS (Cowgill, Cap. 3: Dialogue Economy)

CENA 5 (página 12): Sofia explica seu passado

DIÁLOGO ATUAL (78 palavras):
Sofia: 'Quando eu tinha vinte anos, me apaixonei por um cara. Ele era
incrível, sabe? Mas depois de seis meses ele simplesmente desapareceu.
Não atendeu mais minhas ligações, não respondeu mensagens. Foi como se
eu nunca tivesse existido. Desde então eu tenho dificuldade de confiar.'

ANÁLISE: Cowgill: 'In short films, one word must do work of three'.
Aqui temos 78 palavras fazendo trabalho de 15.

SOLUÇÃO:
ANTES: [78 palavras acima]
DEPOIS (12 palavras):
Sofia: [olha foto antiga] 'Última vez que confiei... [rasga foto] ...não acabou bem.'

RESULTADO: Mesma informação em 85% menos palavras + ação física (Cowgill)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Cowgill']
    },

    'aristotle': {
        'focus': 'POETICS (Aristotle - Poética)',
        'theory_book': 'Poetics',
        'instructions': """
FOCUS: Aristotelian dramatic principles in dialogue

ARISTOTLE'S PRINCIPLES:
1. **Mimesis** (Imitation of life): Show don't tell
   - Cite dialogue that tells instead of shows
   - Quote expositional speeches
   - Rewrite to show through action/behavior

2. **Catharsis** (Emotional purging): Build to emotional peak
   - Cite scenes building to catharsis
   - Quote dialogue at emotional climax
   - Rewrite to heighten emotional impact

3. **Hamartia** (Tragic flaw): Character's fatal flaw
   - Cite dialogue revealing flaw
   - Quote moments where flaw appears
   - Rewrite to make flaw clearer through dialogue

4. **Peripeteia** (Reversal): Sudden change of fortune
   - Cite reversal scenes
   - Quote dialogue at reversal moment
   - Rewrite to sharpen reversal through dialogue

5. **Anagnorisis** (Recognition): Moment of revelation
   - Cite recognition scenes
   - Quote dialogue of realization
   - Rewrite to deepen discovery

MANDATORY EXAMPLE:
"PRINCÍPIO: PERIPETEIA (Reversão) - Aristóteles, Poética Cap. 11

CENA 10 (página 28): Sofia descobre verdade sobre Julio

DIÁLOGO ATUAL:
Maria: 'Sofia, preciso te contar algo. O Julio está noivo.'
Sofia: 'O quê?! Não acredito!'

ANÁLISE: Aristóteles diz Peripeteia deve vir de DENTRO da ação, não
exposição externa. Aqui é notícia entregue, não revelação dramática.

SOLUÇÃO:
ANTES: Exposição direta por Maria
DEPOIS:
[Sofia mexe no celular de Julio]
Sofia: [voz congela] 'Amor, que horas você chega? Saudades. Ana.'
[Julio entra]
Julio: 'Encontrou o que procurava?'
[Silêncio]

RESULTADO: Peripeteia através de DESCOBERTA, não exposição (Aristóteles)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['Aristotle']
    },

    'mckee_dialogue': {
        'focus': 'DIALOGUE AS ACTION (Robert McKee - Dialogue)',
        'theory_book': 'Dialogue: The Art of Verbal Action for Page, Stage, and Screen',
        'instructions': """
FOCUS: McKee's complete dialogue methodology

McKEE DIALOGUE PRINCIPLES:
1. **Dialogue as Action**: Words DO things, not just say
   - Cite passive dialogue (mere talk)
   - Quote dialogue that doesn't advance story
   - Rewrite to make dialogue ACT (persuade, attack, seduce, etc)

2. **Subtext**: What's unsaid > what's said
   - Cite on-the-nose dialogue
   - Quote explicit statements of feeling
   - Rewrite with subtext/indirection

3. **Orchestration**: Each character unique voice
   - Cite characters sounding similar
   - Quote interchangeable dialogue
   - Rewrite to give distinct voices

4. **Exposition**: Hide information in conflict
   - Cite exposition dumps
   - Quote info-delivery dialogue
   - Rewrite to weave info into conflict

5. **Monologue**: When to use, how to use
   - Cite unjustified monologues
   - Quote speeches that could be action
   - Rewrite to justify/replace monologues

MANDATORY EXAMPLE:
"PRINCÍPIO: DIALOGUE AS ACTION (McKee 'Dialogue', Cap. 2)

CENA 3 (página 8): Sofia tenta convencer Maria

DIÁLOGO ATUAL (diálogo como TALK, não ACTION):
Sofia: 'Maria, eu realmente acho que deveria tentar. É uma boa oportunidade.'
Maria: 'Eu não sei, tenho dúvidas.'
Sofia: 'Mas você sempre quis isso.'

ANÁLISE: McKee: 'Dialogue is ACTION'. Aqui Sofia está FALANDO sobre
convencer, não CONVENCENDO através do diálogo.

SOLUÇÃO - Diálogo como AÇÃO:
ANTES: Diálogo passivo acima
DEPOIS:
Sofia: [mostra anúncio] 'Salário: R$8.000. Benefícios. Home office.'
Maria: 'Sofia—'
Sofia: 'Sua faculdade fica a 10 minutos.'
Maria: 'Eu sei, mas—'
Sofia: [aponta foto no anúncio] 'Esse é o escritório. Vidro, vista pro mar.'
Maria: [pega anúncio] '...Deixa eu pensar.'

RESULTADO: Diálogo ATUA (bombardeia com facts) ao invés de FALAR (McKee)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['McKee']
    },

    'mckee_character': {
        'focus': 'CHARACTER DESIGN (Robert McKee - Character)',
        'theory_book': 'Character: The Art of Role and Cast Design for Page, Stage, and Screen',
        'instructions': """
FOCUS: Character revelation through dialogue (McKee Character)

McKEE CHARACTER PRINCIPLES:
1. **Deep Character**: Contradiction between dimensions
   - Cite one-dimensional characters
   - Quote dialogue showing only surface
   - Rewrite to reveal deeper contradictions

2. **Characterization vs Character**: Actions reveal truth
   - Cite dialogue that tells character traits
   - Quote self-description
   - Rewrite to show traits through behavior

3. **Character Arc**: Transformation through pressure
   - Cite static characters
   - Quote dialogue showing no change
   - Rewrite to show evolution

4. **Cast Design**: Each character's unique function
   - Cite redundant characters
   - Quote similar character voices
   - Rewrite to differentiate functions

MANDATORY EXAMPLE:
"PRINCÍPIO: DEEP CHARACTER (McKee 'Character', Cap. 3: Dimensions)

CENA 6 (página 15): Sofia mostra contradição

DIÁLOGO ATUAL (unidimensional - só superfície):
Sofia: 'Eu sou uma pessoa organizada. Gosto de planejar tudo.'

ANÁLISE: McKee: 'Deep character has contradictions'. Aqui Sofia é
apenas 'organizada' (uma dimensão). Precisa mostrar CONTRADIÇÃO.

SOLUÇÃO - Adicionar profundidade:
ANTES: Diálogo acima (unidimensional)
DEPOIS:
[Apartamento impecável de Sofia]
Julio: 'Você é... organizada.'
Sofia: [ri] 'Obsessiva é a palavra. Tudo tem lugar.'
[Abre armário - roupas caem, caos total]
Sofia: [fecha rápido] 'Exceto o armário. Armário não conta.'

RESULTADO: Contradição = Deep Character (organizada vs caótica) (McKee)"
        """,
        'min_chars': 15000,
        'min_scenes': 3,
        'min_quotes': 3,
        'min_rewrites': 2,
        'theory_citations': ['McKee']
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_author_specific_requirements(author: str) -> Dict[str, Any]:
    """
    Get specific requirements for an author.

    Args:
        author: Author name (dialogue, egri, field, etc.)

    Returns:
        Dict with author's specific requirements
    """
    return AUTHOR_SPECIFIC_REQUIREMENTS.get(
        author.lower(),
        AUTHOR_SPECIFIC_REQUIREMENTS['dialogue']  # Default to dialogue
    )


def build_personalized_prompt_pass1(author: str, screenplay_context: str,
                                    python_metrics: str) -> str:
    """
    Build Pass 1 prompt (IDENTIFY PROBLEMS) personalized for author.

    Args:
        author: Author name
        screenplay_context: Screenplay text or excerpt
        python_metrics: Python analysis metrics

    Returns:
        Personalized prompt for Pass 1
    """
    author_config = get_author_specific_requirements(author)

    prompt = f"""
# SCRIPTUREMON FORENSIC ANALYSIS - PASS 1: IDENTIFY PROBLEMS

## AUTHOR: {author.upper()}
## FOCUS: {author_config['focus']}
## THEORY BOOK: {author_config['theory_book']}

---

## YOUR MISSION (PASS 1):

Você é um Script Doctor especializado em **{author.upper()}**.

Analise o roteiro abaixo e identifique **EXATAMENTE 4 PROBLEMAS TÉCNICOS**
usando a metodologia de {author.upper()}.

{author_config['instructions']}

---

## CRITICAL REQUIREMENTS FOR PASS 1:

✅ **MUST IDENTIFY**: Exactly 4 technical problems
✅ **MUST CITE**: 3+ specific scene numbers
✅ **MUST CITE**: 3+ specific page numbers
✅ **MUST QUOTE**: 3+ dialogues verbatim (20+ words each)
✅ **MUST REFERENCE**: Theory from {author_config['theory_book']}
✅ **MINIMUM LENGTH**: {author_config['min_chars']//2} characters

---

## FORMAT REQUIRED:

Para cada um dos 4 problemas, use EXATAMENTE este formato:

```
PROBLEMA [número]: [Tipo do problema] ([Autor], '[Livro]', Cap. [X])

CENA [número] (página [número]): [Contexto da cena]

DIÁLOGO ATUAL:
"[Quote VERBATIM do roteiro - mínimo 20 palavras]"

ANÁLISE:
[Explicação do problema usando teoria específica do autor]
[Mínimo 3-4 frases detalhadas]
```

---

## PYTHON METRICS (Use as reference):

{python_metrics}

---

## SCREENPLAY TO ANALYZE:

{screenplay_context}

---

## OUTPUT STRUCTURE (PASS 1 ONLY):

Generate **ONLY** these 3 sections:

### 1. INTERPRETAÇÃO (2 paragraphs)
- Interprete as métricas Python
- Conecte com teoria de {author.upper()}

### 2. PADRÕES (2 paragraphs)
- Identifique padrões recorrentes
- Conecte padrões com teoria

### 3. PROBLEMAS (4 problems - use format above)
- PROBLEMA 1: [...]
- PROBLEMA 2: [...]
- PROBLEMA 3: [...]
- PROBLEMA 4: [...]

**DO NOT generate sections 4 or 5 - they will come in Pass 2.**

---

BEGIN ANALYSIS:
"""

    return prompt


def build_personalized_prompt_pass2(author: str, screenplay_context: str,
                                    python_metrics: str, pass1_result: str) -> str:
    """
    Build Pass 2 prompt (EXPAND SOLUTIONS) personalized for author.

    Args:
        author: Author name
        screenplay_context: Screenplay text or excerpt
        python_metrics: Python analysis metrics
        pass1_result: Results from Pass 1 (problems identified)

    Returns:
        Personalized prompt for Pass 2
    """
    author_config = get_author_specific_requirements(author)

    prompt = f"""
# SCRIPTUREMON FORENSIC ANALYSIS - PASS 2: EXPAND SOLUTIONS

## AUTHOR: {author.upper()}
## FOCUS: {author_config['focus']}

---

## YOUR MISSION (PASS 2):

Você recebeu análise Pass 1 com 4 problemas identificados.

Agora, forneça **SOLUÇÕES CONCRETAS** com exemplos **ANTES/DEPOIS**
para cada problema, usando metodologia de {author.upper()}.

---

## CRITICAL REQUIREMENTS FOR PASS 2:

✅ **MUST PROVIDE**: Solutions for ALL 4 problems from Pass 1
✅ **MUST INCLUDE**: 2+ complete ANTES/DEPOIS dialogue rewrites
✅ **MUST SHOW**: Line-by-line improvements
✅ **MUST EXPLAIN**: Why rewrite is better (theory-based)
✅ **MINIMUM LENGTH**: {author_config['min_chars']//2} characters

---

## FORMAT REQUIRED FOR EACH SOLUTION:

```
SOLUÇÃO PARA PROBLEMA [número]: [Tipo]

FUNDAMENTAÇÃO TEÓRICA:
[Explicar solução usando teoria de {author.upper()}]

EXEMPLO CONCRETO:

CENA [número] (página [número]): [Contexto]

ANTES (Atual):
"[Diálogo atual do roteiro]"

DEPOIS (Melhorado):
"[Diálogo reescrito aplicando teoria]"

RESULTADO ESPERADO:
[O que esta mudança alcança - 2-3 frases]
```

---

## PASS 1 RESULTS (Problems identified):

{pass1_result}

---

## PYTHON METRICS (Reference):

{python_metrics}

---

## SCREENPLAY (For rewrite examples):

{screenplay_context}

---

## OUTPUT STRUCTURE (PASS 2 ONLY):

Generate **ONLY** these 2 sections:

### 4. SOLUÇÕES (4 solutions - use format above)

Para cada um dos 4 problemas identificados em Pass 1:
- Fundamentação teórica
- Exemplo concreto ANTES/DEPOIS
- Resultado esperado

### 5. DEPTH & SYNTHESIS (2 detailed paragraphs)

Parágrafo 1: Interconexões
- Como os 4 problemas se relacionam?
- Qual padrão geral emerge?
- Como teoria de {author.upper()} explica?

Parágrafo 2: Recomendações de leitura
- Capítulos específicos de {author_config['theory_book']}
- Outras obras de {author.upper()} relevantes
- Como aprofundar nestes conceitos

---

BEGIN PASS 2:
"""

    return prompt
