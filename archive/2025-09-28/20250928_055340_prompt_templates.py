"""
Templates de prompts específicos para análise de roteiros
Criado para resolver o problema de insights genéricos
"""

# Template para análise estrutural específica
SPECIFIC_STRUCTURE_PROMPT = """
Analyze this screenplay excerpt and provide SPECIFIC details:

1. STRUCTURE (cite exact page numbers):
   - Inciting incident: page ___ (describe the exact scene)
   - Plot Point 1: page ___ (what exactly happens)
   - Midpoint: page ___ (false victory or defeat?)
   - Plot Point 2: page ___ (the turning point)
   - Climax: page ___ (final confrontation)

2. TECHNIQUES (name specific methods used):
   - Save The Cat beats present (with page numbers)
   - Hero's Journey stages identified (with examples)
   - Three-act proportions (calculate percentages)

3. DIALOGUE EXAMPLES:
   - Quote memorable lines with page numbers
   - Identify subtext examples
   - Character voice distinctions

4. COMPARISONS:
   - Similar to [specific film] because [specific reason]
   - Different from [specific film] in [specific way]

Be EXTREMELY SPECIFIC. Generic answers will be rejected.
Output as JSON with these exact fields.

Screenplay excerpt:
{screenplay_excerpt}

Theory to apply:
{theory_excerpt}
"""

# Template para análise de personagens
CHARACTER_ANALYSIS_PROMPT = """
Analyze the character development in this screenplay:

1. PROTAGONIST ARC:
   - Starting point (page ___): describe character state
   - First change (page ___): what triggers it
   - Midpoint shift (page ___): internal realization
   - Final state (page ___): how they've changed

2. SUPPORTING CHARACTERS:
   - Name each major character
   - Their function in the story
   - Key scene for each (with page number)

3. DIALOGUE PATTERNS:
   - Vocabulary level for each character
   - Speech patterns (formal/casual/slang)
   - Catchphrases or recurring elements

Provide SPECIFIC examples with page numbers.

Screenplay: {screenplay_excerpt}
"""

# Template para análise de temas
THEME_ANALYSIS_PROMPT = """
Identify the themes in this screenplay with CONCRETE evidence:

1. MAIN THEME:
   - First introduced (page ___): how
   - Developed through (list specific scenes)
   - Resolution (page ___): final statement

2. SUBTHEMES:
   - List each with page number of first appearance
   - How they support main theme

3. SYMBOLIC ELEMENTS:
   - Objects/locations that recur
   - Their meaning with examples

NO generic statements. Every point needs page number and quote.

Screenplay: {screenplay_excerpt}
"""

# Template para análise de ritmo
PACING_ANALYSIS_PROMPT = """
Analyze the pacing and rhythm:

1. SCENE LENGTHS:
   - Average pages per scene: ___
   - Longest scene: page ___ (___ pages)
   - Shortest scene: page ___ (___ pages)

2. TENSION CURVE:
   - Low points: pages ___
   - High points: pages ___
   - Build-up patterns identified

3. DIALOGUE/ACTION RATIO:
   - Act 1: ___% dialogue, ___% action
   - Act 2: ___% dialogue, ___% action
   - Act 3: ___% dialogue, ___% action

Provide exact measurements, not estimates.

Screenplay: {screenplay_excerpt}
"""

# Template de fallback melhorado (quando outros falham)
ENHANCED_FALLBACK_PROMPT = """
You are analyzing a screenplay. Even if you cannot identify specific page numbers,
provide the MOST SPECIFIC analysis possible:

1. Story structure elements you can identify
2. Writing techniques observed
3. Character development patterns
4. Dialogue characteristics
5. Similar films and WHY they're similar

Avoid saying:
- "The screenplay follows classic structure"
- "Characters are well-developed"
- "Dialogue is realistic"

Instead say:
- "The inciting incident appears to be [specific event]"
- "[Character name] changes from [trait] to [trait]"
- "Dialogue uses [specific technique] seen in [example]"

Screenplay: {screenplay_excerpt}
"""

# Função para selecionar o melhor template
def get_prompt_for_analysis(analysis_type="structure", screenplay_excerpt="", theory_excerpt=""):
    """
    Retorna o prompt apropriado para o tipo de análise

    Args:
        analysis_type: "structure", "character", "theme", "pacing", ou "general"
        screenplay_excerpt: Trecho do roteiro para análise
        theory_excerpt: Teoria para aplicar (opcional)

    Returns:
        String com o prompt formatado
    """
    templates = {
        "structure": SPECIFIC_STRUCTURE_PROMPT,
        "character": CHARACTER_ANALYSIS_PROMPT,
        "theme": THEME_ANALYSIS_PROMPT,
        "pacing": PACING_ANALYSIS_PROMPT,
        "general": ENHANCED_FALLBACK_PROMPT
    }

    template = templates.get(analysis_type, ENHANCED_FALLBACK_PROMPT)

    # Formatar o template com os excertos
    if "{screenplay_excerpt}" in template:
        template = template.replace("{screenplay_excerpt}", screenplay_excerpt[:5000])
    if "{theory_excerpt}" in template and theory_excerpt:
        template = template.replace("{theory_excerpt}", theory_excerpt[:2000])

    return template

# Sistema de validação de qualidade
def score_analysis_quality(analysis_text):
    """
    Avalia a qualidade de uma análise baseada em critérios específicos

    Returns:
        Float entre 0 e 1 indicando qualidade
    """
    score = 0.0

    # Checa menções a páginas específicas
    import re
    page_mentions = len(re.findall(r'page \d+', analysis_text.lower()))
    score += min(page_mentions * 0.1, 0.3)  # Max 0.3 pontos

    # Checa citações diretas
    quotes = len(re.findall(r'"[^"]{10,}"', analysis_text))
    score += min(quotes * 0.1, 0.2)  # Max 0.2 pontos

    # Checa menções a técnicas específicas
    techniques = [
        'save the cat', 'inciting incident', 'plot point',
        'midpoint', 'dark night', 'finale', 'catalyst',
        'three-act', "hero's journey", 'campbell'
    ]
    technique_count = sum(1 for t in techniques if t in analysis_text.lower())
    score += min(technique_count * 0.05, 0.2)  # Max 0.2 pontos

    # Checa tamanho adequado (não muito curto nem muito longo)
    word_count = len(analysis_text.split())
    if 200 <= word_count <= 1000:
        score += 0.2
    elif 100 <= word_count < 200:
        score += 0.1

    # Checa se tem estrutura JSON ou formatação
    if '{' in analysis_text and '}' in analysis_text:
        score += 0.1

    return min(score, 1.0)  # Garante que não passa de 1.0

# Função para decidir se precisa re-análise
def needs_reanalysis(analysis_text, min_quality=0.7):
    """
    Determina se uma análise precisa ser refeita

    Args:
        analysis_text: Texto da análise
        min_quality: Score mínimo aceitável (default 0.7)

    Returns:
        Boolean indicando se precisa refazer
    """
    score = score_analysis_quality(analysis_text)
    return score < min_quality, score