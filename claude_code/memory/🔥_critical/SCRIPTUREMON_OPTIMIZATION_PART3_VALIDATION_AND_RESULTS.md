# SCRIPTUREMON OPTIMIZATION - PARTE 3: VALIDAÇÃO E RESULTADOS

---

## SISTEMA DE VALIDAÇÃO DE 3 CAMADAS

### Arquitetura de Validação

**Arquivo:** `tests/validation/graduation_validator.py`

**Classe:** `GraduationValidator`

**Filosofia:**
```
Aprovação técnica ≠ Qualidade real
100% pass técnico + 37.5% utilidade = PROBLEMA
```

**Solução: 3 camadas independentes**

```
LAYER 1: TECHNICAL VALIDATION (20% peso)
    ↓
    Verifica estrutura, formato, comprimento mínimo
    Passa/Falha binário
    ↓
LAYER 2: SPECIFICITY VALIDATION (40% peso)
    ↓
    Citações, referências, grounding
    Scoring 0-100
    ↓
LAYER 3: DEPTH VALIDATION (40% peso)
    ↓
    Insights, análise causal, síntese
    Scoring 0-100
    ↓
FINAL SCORE = (L1 × 0.2) + (L2 × 0.4) + (L3 × 0.4)
```

---

## LAYER 1: VALIDAÇÃO TÉCNICA (20%)

### Critérios Obrigatórios

**1. Estrutura de Seções**

```python
def validate_structure(self, analysis: str) -> Dict:
    """Valida presença de seções obrigatórias"""

    required_sections = [
        'INTERPRETATION',
        'PATTERNS',
        'PROBLEMS',
        'SOLUTIONS',
        'DEPTH'
    ]

    found_sections = []
    for section in required_sections:
        # Case-insensitive search
        if re.search(rf'\b{section}\b', analysis, re.IGNORECASE):
            found_sections.append(section)

    return {
        'score': len(found_sections) / len(required_sections),
        'found': found_sections,
        'missing': set(required_sections) - set(found_sections)
    }
```

**Threshold:** 4/5 seções (80%)

**Por quê importante:**
- Garante análise abrangente (não apenas um aspecto)
- Força cobertura de problemas E soluções
- Previne análises superficiais de 1 parágrafo

**2. Comprimento Mínimo**

```python
def validate_length(self, analysis: str) -> Dict:
    """Valida extensão da análise"""

    word_count = len(analysis.split())
    char_count = len(analysis)

    # Metas estabelecidas pelo system message
    min_words = 600      # ~2500 tokens mínimo
    target_words = 1000  # ~4000 tokens ideal

    if word_count < min_words:
        quality = 'TOO_SHORT'
        score = word_count / min_words
    elif word_count < target_words:
        quality = 'ACCEPTABLE'
        score = 0.7 + (0.3 * (word_count - min_words) / (target_words - min_words))
    else:
        quality = 'EXCELLENT'
        score = 1.0

    return {
        'score': score,
        'word_count': word_count,
        'char_count': char_count,
        'quality': quality,
        'meets_minimum': word_count >= min_words
    }
```

**Thresholds:**
- Mínimo: 600 palavras (score 0.5)
- Aceitável: 800 palavras (score 0.7)
- Excelente: 1000+ palavras (score 1.0)

**Por quê importante:**
- Análises curtas = genéricas
- Análises longas = detalhadas (quando bem estruturadas)
- Força modelo a desenvolver argumentos

**3. Formato de Parágrafos**

```python
def validate_paragraphs(self, analysis: str) -> Dict:
    """Valida estrutura de parágrafos"""

    # Split por linhas vazias
    paragraphs = [p.strip() for p in analysis.split('\n\n') if p.strip()]

    # Conta parágrafos substantivos (50+ palavras)
    substantial = [p for p in paragraphs if len(p.split()) >= 50]

    # Meta: 12-14 parágrafos substantivos (system message)
    min_paragraphs = 8
    target_paragraphs = 12

    count = len(substantial)

    if count < min_paragraphs:
        quality = 'INSUFFICIENT'
        score = count / min_paragraphs
    elif count < target_paragraphs:
        quality = 'GOOD'
        score = 0.7 + (0.3 * (count - min_paragraphs) / (target_paragraphs - min_paragraphs))
    else:
        quality = 'EXCELLENT'
        score = 1.0

    return {
        'score': score,
        'total_paragraphs': len(paragraphs),
        'substantial_paragraphs': count,
        'quality': quality
    }
```

**Thresholds:**
- Mínimo: 8 parágrafos substantivos
- Bom: 10 parágrafos
- Excelente: 12+ parágrafos

**Definição "substantivo":**
- 50+ palavras por parágrafo
- Não conta headers (## INTERPRETATION)
- Não conta listas de bullet points

**Por quê importante:**
- Previne "wall of text" (1 parágrafo gigante)
- Previne análise fragmentada (30 parágrafos de 1 linha)
- Força estruturação lógica de ideias

**4. Encoding e Caracteres Especiais**

```python
def validate_encoding(self, analysis: str) -> Dict:
    """Valida encoding e ausência de corrupção"""

    issues = []

    # Verifica caracteres corrompidos comuns
    corrupted_patterns = [
        r'\ufffd',           # Replacement character
        r'â€™',              # Encoding de '
        r'â€œ|â€',          # Encoding de " "
        r'Ã©|Ã¡|Ã§',       # Encoding de é á ç
    ]

    for pattern in corrupted_patterns:
        if re.search(pattern, analysis):
            issues.append(f'Corrupted encoding: {pattern}')

    # Verifica Unicode válido
    try:
        analysis.encode('utf-8')
        encoding_valid = True
    except UnicodeEncodeError as e:
        encoding_valid = False
        issues.append(f'Unicode error: {e}')

    return {
        'score': 1.0 if encoding_valid and not issues else 0.0,
        'encoding_valid': encoding_valid,
        'issues': issues
    }
```

**Threshold:** Must be 1.0 (sem erros)

**Por quê importante:**
- Corrupted text indica problema de processamento
- Pode indicar timeout truncado
- Afeta legibilidade

### Combinação Layer 1

```python
def technical_validation(self, analysis: str) -> Dict:
    """Executa todas validações técnicas"""

    structure = self.validate_structure(analysis)
    length = self.validate_length(analysis)
    paragraphs = self.validate_paragraphs(analysis)
    encoding = self.validate_encoding(analysis)

    # Score ponderado
    technical_score = (
        structure['score'] * 0.3 +
        length['score'] * 0.3 +
        paragraphs['score'] * 0.3 +
        encoding['score'] * 0.1
    )

    # MUST pass encoding (elimina corrupção)
    if encoding['score'] < 1.0:
        technical_score = 0.0

    return {
        'score': technical_score,
        'structure': structure,
        'length': length,
        'paragraphs': paragraphs,
        'encoding': encoding,
        'passed': technical_score >= 0.7
    }
```

**Threshold final Layer 1:** 0.7 (70%)

---

## LAYER 2: VALIDAÇÃO DE ESPECIFICIDADE (40%)

### Filosofia

**O problema central que causou a otimização:**
```
Análise genérica: "O diálogo poderia ser melhorado"
Análise específica: "Na cena 12, quando Samantha diz 'Mas eu estava
                    tendo um sonho lindo...', a fala revela..."
```

**Layer 2 mede exatamente isso.**

### Critérios de Especificidade

**1. Citações de Diálogo (Dialogue Quotes)**

```python
def count_dialogue_quotes(self, analysis: str) -> Dict:
    """Conta citações verbatim de diálogos do roteiro"""

    # Padrões de citação
    patterns = [
        r'["""]([^"""]{15,})["""]',     # Aspas curvas, min 15 chars
        r'"([^"]{15,})"',                # Aspas retas
        r"'([^']{30,})'"                 # Aspas simples (se longa)
    ]

    quotes = []
    for pattern in patterns:
        matches = re.finditer(pattern, analysis)
        for match in matches:
            quote_text = match.group(1)

            # Filtros de qualidade
            if self._is_dialogue_quote(quote_text):
                quotes.append({
                    'text': quote_text,
                    'length': len(quote_text),
                    'position': match.start()
                })

    # Scoring
    count = len(quotes)

    if count == 0:
        quality = 'NONE'
        score = 0.0
    elif count < 4:
        quality = 'INSUFFICIENT'
        score = count / 4 * 0.5  # Max 0.5 se menos de 4
    elif count < 8:
        quality = 'GOOD'
        score = 0.5 + ((count - 4) / 4 * 0.3)  # 0.5-0.8
    else:
        quality = 'EXCELLENT'
        score = 0.8 + min((count - 8) / 4 * 0.2, 0.2)  # 0.8-1.0

    return {
        'score': score,
        'count': count,
        'quotes': quotes,
        'quality': quality,
        'average_length': sum(q['length'] for q in quotes) / count if count > 0 else 0
    }

def _is_dialogue_quote(self, text: str) -> bool:
    """Verifica se texto é realmente diálogo (não teoria)"""

    # NÃO é diálogo se:

    # 1. Contém citação de teoria McKee
    theory_markers = ['mckee', 'capítulo', 'chapter', 'segundo o autor']
    if any(marker in text.lower() for marker in theory_markers):
        return False

    # 2. É muito longa (provavelmente descrição)
    if len(text) > 200:
        return False

    # 3. Não tem características de fala
    speech_markers = ['?', '!', '...', 'eu', 'você', 'mas', 'não']
    if not any(marker in text.lower() for marker in speech_markers):
        return False

    return True
```

**Thresholds:**
- 0 quotes = 0.0 (CRITICAL FAILURE)
- 1-3 quotes = 0.1-0.5 (INSUFFICIENT)
- 4-7 quotes = 0.5-0.8 (GOOD)
- 8+ quotes = 0.8-1.0 (EXCELLENT)

**Meta estabelecida:** 4-6 quotes (system message)

**Por quê importante:**
- Prova que modelo LEIOU o roteiro
- Prova grounding (não inventou)
- Citações verbatim = análise específica

**Exemplos reais do teste:**

✅ Quote válido:
```
"Mas eu estava tendo um sonho lindo..."
```

✅ Quote válido:
```
"Você está bem?"
```

❌ NÃO é quote (teoria):
```
"McKee explains that subtext is the unspoken meaning..."
```

**2. Referências a Cenas (Scene References)**

```python
def count_scene_references(self, analysis: str) -> Dict:
    """Conta referências específicas a cenas do roteiro"""

    # Padrões de referência
    patterns = [
        r'\bscene\s+(\d+)\b',           # "scene 12"
        r'\bcena\s+(\d+)\b',            # "cena 12"
        r'\bp[aá]gina\s+(\d+)\b',       # "página 15"
        r'\bpage\s+(\d+)\b',            # "page 15"
        r'\bline\s+(\d+)\b',            # "line 42"
        r'\blinha\s+(\d+)\b',           # "linha 42"
        r'in\s+scene\s+(\d+)',          # "in scene 3"
        r'na\s+cena\s+(\d+)',           # "na cena 3"
    ]

    references = set()  # Use set para evitar duplicatas

    for pattern in patterns:
        matches = re.finditer(pattern, analysis, re.IGNORECASE)
        for match in matches:
            ref_type = 'scene' if 'scene' in pattern or 'cena' in pattern else 'page'
            ref_number = match.group(1)

            references.add((ref_type, ref_number, match.group(0)))

    # Scoring
    count = len(references)

    if count == 0:
        quality = 'NONE'
        score = 0.0
    elif count < 3:
        quality = 'INSUFFICIENT'
        score = count / 3 * 0.5
    elif count < 7:
        quality = 'GOOD'
        score = 0.5 + ((count - 3) / 4 * 0.3)
    else:
        quality = 'EXCELLENT'
        score = 0.8 + min((count - 7) / 5 * 0.2, 0.2)

    return {
        'score': score,
        'count': count,
        'references': list(references),
        'quality': quality,
        'breakdown': self._breakdown_references(references)
    }

def _breakdown_references(self, references: set) -> Dict:
    """Analisa tipos de referências"""

    breakdown = {
        'scene_refs': 0,
        'page_refs': 0,
        'line_refs': 0
    }

    for ref_type, _, _ in references:
        if ref_type == 'scene':
            breakdown['scene_refs'] += 1
        elif ref_type == 'page':
            breakdown['page_refs'] += 1
        elif ref_type == 'line':
            breakdown['line_refs'] += 1

    return breakdown
```

**Thresholds:**
- 0 refs = 0.0 (CRITICAL)
- 1-2 refs = 0.1-0.5 (INSUFFICIENT)
- 3-6 refs = 0.5-0.8 (GOOD)
- 7+ refs = 0.8-1.0 (EXCELLENT)

**Meta estabelecida:** 5-8 scene refs

**Por quê importante:**
- Âncora análise em momentos específicos
- Previne generalização
- Permite verificação (usuário pode checar cena X)

**Exemplos reais do teste deep dive:**

✅ Valid references encontradas:
```
- "scene 1" (opening garden scene)
- "cena 12" (dream dialogue)
- "página 15" (Alberto's entrance)
- "scene 3" (pattern establishment)
- "in scene 8" (contradiction moment)
- "na cena 5" (avoidance behavior)
- "page 22" (redundancy example)
```

**3. Referências a Teoria McKee**

```python
def count_theory_references(self, analysis: str) -> Dict:
    """Conta referências específicas à teoria McKee"""

    # Padrões de citação teórica
    patterns = [
        r'\bmckee\b',                           # Menção ao autor
        r'\bcap[ií]tulo\s+\d+',                # "capítulo 4"
        r'\bchapter\s+\d+',                     # "chapter 4"
        r'(McKee|mckee)\s+(explains|states|argues|describes)',
        r'(segundo|conforme|como)\s+(McKee|mckee)',
        r'no\s+cap[ií]tulo\s+\d+',
        r'in\s+chapter\s+\d+',
    ]

    references = []

    for pattern in patterns:
        matches = re.finditer(pattern, analysis, re.IGNORECASE)
        for match in matches:
            # Extrai contexto (50 chars antes e depois)
            start = max(0, match.start() - 50)
            end = min(len(analysis), match.end() + 50)
            context = analysis[start:end]

            references.append({
                'match': match.group(0),
                'context': context,
                'position': match.start()
            })

    # Remove duplicatas próximas (mesmo parágrafo)
    unique_refs = self._deduplicate_nearby(references, distance=200)

    count = len(unique_refs)

    if count == 0:
        quality = 'NONE'
        score = 0.0
    elif count < 3:
        quality = 'INSUFFICIENT'
        score = count / 3 * 0.5
    elif count < 8:
        quality = 'GOOD'
        score = 0.5 + ((count - 3) / 5 * 0.3)
    else:
        quality = 'EXCELLENT'
        score = 0.8 + min((count - 8) / 4 * 0.2, 0.2)

    return {
        'score': score,
        'count': count,
        'references': unique_refs,
        'quality': quality
    }
```

**Thresholds:**
- 0 refs = 0.0 (não usou teoria!)
- 1-2 refs = 0.1-0.5 (uso superficial)
- 3-7 refs = 0.5-0.8 (bom uso)
- 8+ refs = 0.8-1.0 (profundo)

**Meta estabelecida:** 5-8 McKee refs

**Por quê importante:**
- Prova que modelo LEIOU o livro McKee
- Conecta análise prática → teoria
- Justifica recomendações com autoridade

**Exemplos do teste deep dive:**

✅ Valid theory references:
```
- "McKee explains in Chapter 4"
- "conforme McKee descreve"
- "no capítulo 7 sobre personagens"
- "McKee estabelece o princípio de"
- "segundo McKee, o verdadeiro caráter"
```

**4. Menções a Personagens**

```python
def count_character_mentions(self, analysis: str, screenplay_text: str) -> Dict:
    """Conta menções a personagens específicos do roteiro"""

    # Extrai personagens do roteiro
    character_names = self._extract_character_names(screenplay_text)

    mentions = {}
    total_count = 0

    for char_name in character_names:
        # Conta menções (case-insensitive)
        pattern = rf'\b{re.escape(char_name)}\b'
        matches = re.findall(pattern, analysis, re.IGNORECASE)

        count = len(matches)
        if count > 0:
            mentions[char_name] = count
            total_count += count

    unique_characters = len(mentions)

    # Scoring baseado em caracteres únicos mencionados
    if unique_characters == 0:
        quality = 'NONE'
        score = 0.0
    elif unique_characters < 3:
        quality = 'INSUFFICIENT'
        score = unique_characters / 3 * 0.5
    elif unique_characters < 5:
        quality = 'GOOD'
        score = 0.5 + ((unique_characters - 3) / 2 * 0.3)
    else:
        quality = 'EXCELLENT'
        score = 0.8 + min((unique_characters - 5) / 3 * 0.2, 0.2)

    return {
        'score': score,
        'total_mentions': total_count,
        'unique_characters': unique_characters,
        'breakdown': mentions,
        'quality': quality
    }

def _extract_character_names(self, screenplay: str) -> set:
    """Extrai nomes de personagens do roteiro"""

    # Padrão: nomes em CAPS seguidos de diálogo
    # EX: SAMANTHA
    #     Mas eu estava tendo...

    pattern = r'^([A-Z][A-Z\s]+)$'

    names = set()
    lines = screenplay.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()
        match = re.match(pattern, line)

        if match:
            name = match.group(1).strip()

            # Filtros: não é action line
            if len(name) > 2 and len(name.split()) <= 3:
                # Verifica se próxima linha é diálogo (não vazia, não caps)
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.isupper():
                        names.add(name)

    return names
```

**Thresholds:**
- 0 chars = 0.0
- 1-2 chars = 0.1-0.5
- 3-4 chars = 0.5-0.8
- 5+ chars = 0.8-1.0

**Por quê importante:**
- Análise focada em PERSONAGENS (não abstrata)
- Mostra atenção aos indivíduos
- Previne análise genérica de "a história"

**5. Ratio de Especificidade**

```python
def calculate_specificity_ratio(self, analysis: str) -> Dict:
    """Calcula ratio de frases específicas vs genéricas"""

    # Frases genéricas (red flags)
    generic_phrases = [
        r'poderia ser melhorado',
        r'precisa de trabalho',
        r'não funciona bem',
        r'tem problemas',
        r'falta desenvolvimento',
        r'carece de',
        r'deveria ter mais',
        r'é fraco',
        r'é forte',
        r'muito genérico',
        r'pouco desenvolvido',
        r'sem profundidade',
        r'superficial',
        r'in general',
        r'overall',
        r'basically',
        r'simply',
        r'just needs',
        r'could be better',
        r'needs work',
        r'lacks depth',
    ]

    # Frases específicas (green flags)
    specific_phrases = [
        r'na cena \d+',
        r'in scene \d+',
        r'quando .+ diz ["""]',
        r'mckee (explica|descreve|estabelece)',
        r'no capítulo \d+',
        r'página \d+',
        r'this dialogue: ["""]',
        r'este diálogo: ["""]',
        r'the line ["""]',
        r'a fala ["""]',
    ]

    generic_count = 0
    for pattern in generic_phrases:
        generic_count += len(re.findall(pattern, analysis, re.IGNORECASE))

    specific_count = 0
    for pattern in specific_phrases:
        specific_count += len(re.findall(pattern, analysis, re.IGNORECASE))

    # Calcula ratio
    total = generic_count + specific_count

    if total == 0:
        # Sem indicadores = assume neutro
        ratio = 0.5
        quality = 'NEUTRAL'
    else:
        ratio = specific_count / total

        if ratio < 0.3:
            quality = 'MOSTLY_GENERIC'
        elif ratio < 0.6:
            quality = 'MIXED'
        elif ratio < 0.8:
            quality = 'MOSTLY_SPECIFIC'
        else:
            quality = 'HIGHLY_SPECIFIC'

    # Score: penaliza genéricos pesadamente
    if generic_count > 3:
        score = 0.0  # FAIL se >3 frases genéricas
    else:
        score = ratio

    return {
        'score': score,
        'ratio': ratio,
        'generic_count': generic_count,
        'specific_count': specific_count,
        'quality': quality
    }
```

**Thresholds:**
- >3 generic phrases = 0.0 (FAIL)
- ratio < 0.6 = 0.0-0.6 (INSUFFICIENT)
- ratio 0.6-0.8 = 0.6-0.8 (GOOD)
- ratio > 0.8 = 0.8-1.0 (EXCELLENT)

**Meta:** Ratio > 0.8 (80% específico)

**Por quê é a métrica mais crítica:**
- Captura exatamente o problema original
- Uma frase genérica pode arruinar análise inteira
- Força modelo a ser concreto

### Combinação Layer 2

```python
def specificity_validation(self, analysis: str, screenplay: str) -> Dict:
    """Executa todas validações de especificidade"""

    dialogue = self.count_dialogue_quotes(analysis)
    scenes = self.count_scene_references(analysis)
    theory = self.count_theory_references(analysis)
    characters = self.count_character_mentions(analysis, screenplay)
    ratio = self.calculate_specificity_ratio(analysis)

    # Score ponderado
    specificity_score = (
        dialogue['score'] * 0.25 +      # 25% - Citações de diálogo
        scenes['score'] * 0.20 +         # 20% - Refs de cena
        theory['score'] * 0.20 +         # 20% - Refs McKee
        characters['score'] * 0.10 +     # 10% - Personagens
        ratio['score'] * 0.25            # 25% - Ratio específico/genérico
    )

    # CRITICAL: ratio é gate
    # Se muitas frases genéricas, falha tudo
    if ratio['generic_count'] > 5:
        specificity_score = min(specificity_score, 0.3)

    return {
        'score': specificity_score,
        'dialogue_quotes': dialogue,
        'scene_references': scenes,
        'theory_references': theory,
        'character_mentions': characters,
        'specificity_ratio': ratio,
        'passed': specificity_score >= 0.7
    }
```

**Threshold final Layer 2:** 0.7 (70%)

**Peso no score final:** 40% (maior peso individual)

---

## LAYER 3: VALIDAÇÃO DE PROFUNDIDADE (40%)

### Filosofia

**Diferença entre análise superficial e profunda:**

```
SUPERFICIAL:
"O diálogo de Samantha mostra que ela está triste."

PROFUNDA:
"O diálogo de Samantha na cena 12 'Mas eu estava tendo um sonho
lindo...' revela um padrão de evasão da realidade estabelecido
desde a cena 3, onde ela focou na beleza do jardim ao invés de
encarar o conflito com o pai. McKee descreve no Capítulo 4 que
'o verdadeiro caráter é revelado sob pressão' - aqui, Samantha
escolhe consistentemente focar no passado/imaginário (sonho) ao
invés da realidade presente (despertar), demonstrando sua estratégia
de coping através de dissociação que será crucial para o clímax."
```

**Layer 3 mede:**
- Análise causal (não apenas descrição)
- Conexões entre elementos
- Insights não-óbvios
- Síntese de múltiplas fontes

### Critérios de Profundidade

**1. Análise Causal vs Descritiva**

```python
def analyze_causality(self, analysis: str) -> Dict:
    """Mede uso de linguagem causal vs descritiva"""

    # Marcadores causais (profundidade)
    causal_markers = [
        r'\bporque\b',
        r'\bbecause\b',
        r'\bportanto\b',
        r'\btherefore\b',
        r'\bassim\b',
        r'\bthus\b',
        r'\bresulta em\b',
        r'\bresults in\b',
        r'\bleva a\b',
        r'\bleads to\b',
        r'\bcausa\b',
        r'\bcauses\b',
        r'\bdevido a\b',
        r'\bdue to\b',
        r'\b(como|since) consequência\b',
        r'\bas a consequence\b',
        r'\bisso significa que\b',
        r'\bthis means that\b',
        r'\brevelando\b',
        r'\brevealing\b',
        r'\bdemonstrand[oa]\b',
        r'\bdemonstrating\b',
    ]

    # Marcadores descritivos (superficialidade)
    descriptive_markers = [
        r'\bé\b',
        r'\bis\b',
        r'\bestá\b',
        r'\bhas\b',
        r'\btem\b',
        r'\bmostra\b',
        r'\bshows\b',
        r'\baparece\b',
        r'\bappears\b',
        r'\bparece\b',
        r'\bseems\b',
        r'\bexiste\b',
        r'\bexists\b',
    ]

    causal_count = 0
    for marker in causal_markers:
        causal_count += len(re.findall(marker, analysis, re.IGNORECASE))

    descriptive_count = 0
    for marker in descriptive_markers:
        descriptive_count += len(re.findall(marker, analysis, re.IGNORECASE))

    # Ratio causal/descritivo
    total = causal_count + descriptive_count
    if total == 0:
        ratio = 0.0
        quality = 'NO_ANALYSIS'
    else:
        ratio = causal_count / total

        if ratio < 0.2:
            quality = 'PURELY_DESCRIPTIVE'
        elif ratio < 0.4:
            quality = 'MOSTLY_DESCRIPTIVE'
        elif ratio < 0.6:
            quality = 'BALANCED'
        else:
            quality = 'CAUSAL_ANALYSIS'

    # Score: queremos ratio > 0.4
    if ratio < 0.3:
        score = ratio / 0.3 * 0.5
    elif ratio < 0.6:
        score = 0.5 + ((ratio - 0.3) / 0.3 * 0.3)
    else:
        score = 0.8 + min((ratio - 0.6) / 0.4 * 0.2, 0.2)

    return {
        'score': score,
        'causal_count': causal_count,
        'descriptive_count': descriptive_count,
        'ratio': ratio,
        'quality': quality
    }
```

**Thresholds:**
- Ratio < 0.3 = Descritivo (score < 0.5)
- Ratio 0.3-0.6 = Balanceado (score 0.5-0.8)
- Ratio > 0.6 = Causal (score 0.8-1.0)

**Por quê importante:**
- Descrição = superficial ("X existe")
- Causalidade = profundo ("X causa Y porque Z")
- Insights requerem explicação de mecanismos

**2. Conexões Entre Elementos**

```python
def analyze_connections(self, analysis: str) -> Dict:
    """Mede conexões entre cenas, personagens, teoria"""

    # Padrões de conexão
    connection_patterns = [
        # Temporal
        r'(desde|from) (a cena|scene) \d+',
        r'estabelecido (na|in) (cena|scene) \d+',
        r'(como visto|as seen) (na|in) (cena|scene) \d+',
        r'padrão (que|that) (começa|begins|started)',

        # Causal entre cenas
        r'(cena|scene) \d+.*?(resulta|results|leva|leads).*(cena|scene) \d+',
        r'(isto|this|isso).*(explica|explains).*(cena|scene) \d+',

        # Teoria + Prática
        r'mckee.*(descreve|describes).*(cena|scene|página|page)',
        r'(conforme|as) mckee.*(aqui|here|nesta|in this)',
        r'(princípio|principle|conceito|concept).*(aplicado|applied).*(cena|scene)',

        # Personagem + Padrão
        r'[A-Z][a-z]+.*(sempre|consistently|pattern|padrão)',
        r'[A-Z][a-z]+.*(estratégia|strategy|approach|método)',
        r'character.*(arc|desenvolvimento|development)',
    ]

    connections = []
    for pattern in connection_patterns:
        matches = re.finditer(pattern, analysis, re.IGNORECASE)
        for match in matches:
            connections.append({
                'type': 'connection',
                'pattern': pattern,
                'text': match.group(0),
                'position': match.start()
            })

    count = len(connections)

    if count == 0:
        quality = 'ISOLATED'
        score = 0.0
    elif count < 5:
        quality = 'FEW_CONNECTIONS'
        score = count / 5 * 0.5
    elif count < 10:
        quality = 'CONNECTED'
        score = 0.5 + ((count - 5) / 5 * 0.3)
    else:
        quality = 'HIGHLY_INTEGRATED'
        score = 0.8 + min((count - 10) / 10 * 0.2, 0.2)

    return {
        'score': score,
        'count': count,
        'connections': connections,
        'quality': quality
    }
```

**Thresholds:**
- 0 connections = Análise isolada (0.0)
- 1-4 connections = Poucas conexões (0.1-0.5)
- 5-9 connections = Conectada (0.5-0.8)
- 10+ connections = Integrada (0.8-1.0)

**Por quê importante:**
- Análise fragmentada = lista de observações
- Análise integrada = teia de relações
- Conexões = compreensão sistêmica

**Exemplo de conexão profunda:**

```
"O padrão de evasão de Samantha estabelecido na cena 3 (foco no
jardim) resulta no comportamento da cena 12 (foco no sonho), que
por sua vez explica sua incapacidade de confrontar o pai na cena
final. McKee descreve no Capítulo 7 que personagens consistentes
mantêm estratégias mesmo quando falham - aqui vemos essa consistência
destrutiva que precisará ser quebrada no clímax."
```

Essa frase conecta:
- 3 cenas diferentes
- 1 conceito McKee
- 1 padrão de personagem
- 1 implicação para clímax

**3. Insights Não-Óbvios**

```python
def detect_insights(self, analysis: str) -> Dict:
    """Detecta insights profundos vs observações óbvias"""

    # Marcadores de insight
    insight_markers = [
        r'\b(paradox|paradoxo)\b',
        r'\b(irony|ironia)\b',
        r'\b(contradição|contradiction)\b',
        r'\b(subtle|sutil)\b',
        r'\b(implica|implies|implicação|implication)\b',
        r'\b(subjacente|underlying)\b',
        r'\b(não óbvio|not obvious|escondido|hidden)\b',
        r'\b(revelador|revealing|revela que)\b',
        r'\b(unexpected|inesperado|surpreendente|surprising)\b',
        r'(apesar de|despite|embora|although)',
        r'(na superfície|on surface).*(na verdade|in reality)',
        r'(parece|seems).*(mas na verdade|but actually)',
    ]

    # Marcadores de obviedade
    obvious_markers = [
        r'\b(obviamente|obviously|claramente|clearly)\b',
        r'\b(é evidente|is evident|é óbvio)\b',
        r'\bsimple(s)?mente\b',
        r'\bbasica(lly|mente)\b',
        r'\bjust\b',
        r'\bmerely\b',
    ]

    insight_count = 0
    for marker in insight_markers:
        insight_count += len(re.findall(marker, analysis, re.IGNORECASE))

    obvious_count = 0
    for marker in obvious_markers:
        obvious_count += len(re.findall(marker, analysis, re.IGNORECASE))

    # Penaliza obviedade
    net_insights = max(0, insight_count - obvious_count)

    if net_insights == 0:
        quality = 'SURFACE_LEVEL'
        score = 0.3  # Não zero (pode ter insights sem markers)
    elif net_insights < 3:
        quality = 'SOME_DEPTH'
        score = 0.3 + (net_insights / 3 * 0.3)
    elif net_insights < 6:
        quality = 'INSIGHTFUL'
        score = 0.6 + ((net_insights - 3) / 3 * 0.2)
    else:
        quality = 'DEEPLY_INSIGHTFUL'
        score = 0.8 + min((net_insights - 6) / 4 * 0.2, 0.2)

    return {
        'score': score,
        'insight_markers': insight_count,
        'obvious_markers': obvious_count,
        'net_insights': net_insights,
        'quality': quality
    }
```

**Thresholds:**
- 0 net insights = Superficial (0.3)
- 1-2 insights = Alguma profundidade (0.3-0.6)
- 3-5 insights = Insightful (0.6-0.8)
- 6+ insights = Profundo (0.8-1.0)

**Por quê importante:**
- Insights = valor agregado
- Observações óbvias = qualquer um vê
- Profundidade = ver além da superfície

**4. Síntese de Múltiplas Fontes**

```python
def analyze_synthesis(self, analysis: str) -> Dict:
    """Mede integração de Python metrics + Theory + Screenplay"""

    # Marcadores de síntese
    synthesis_patterns = [
        # Python + Theory
        r'(métrica|metric|score).*(confirma|confirms|alinha|aligns).*(mckee|teoria|theory)',
        r'mckee.*(explicando|explaining).*(score|métrica)',

        # Theory + Screenplay
        r'mckee.*(cena|scene|diálogo|dialogue)',
        r'(cena|scene).*(mckee|capítulo|chapter)',
        r'(princípio|principle).*(aplicado|applied|exemplificado|exemplified)',

        # Python + Screenplay
        r'(score|métrica).*(cena|scene|diálogo|dialogue)',
        r'(análise objetiva|objective analysis).*(mostra|shows).*(cena|scene)',

        # Tripla síntese
        r'(score|métrica).*(confirma|aligns).*(cena|scene).*(mckee|teoria)',
    ]

    syntheses = []
    for pattern in synthesis_patterns:
        matches = re.finditer(pattern, analysis, re.IGNORECASE)
        syntheses.extend(matches)

    count = len(syntheses)

    # Verifica presença de seção SYNTHESIS/DEPTH explícita
    has_synthesis_section = bool(re.search(
        r'\b(SYNTHESIS|DEPTH|SÍNTESE|PROFUNDIDADE)\b',
        analysis,
        re.IGNORECASE
    ))

    if count == 0 and not has_synthesis_section:
        quality = 'SILOED'
        score = 0.2
    elif count < 3:
        quality = 'MINIMAL_SYNTHESIS'
        score = 0.2 + (count / 3 * 0.3)
    elif count < 6:
        quality = 'INTEGRATED'
        score = 0.5 + ((count - 3) / 3 * 0.3)
    else:
        quality = 'HIGHLY_SYNTHESIZED'
        score = 0.8 + min((count - 6) / 4 * 0.2, 0.2)

    # Bonus se tem seção dedicada
    if has_synthesis_section:
        score = min(1.0, score + 0.1)

    return {
        'score': score,
        'synthesis_count': count,
        'has_synthesis_section': has_synthesis_section,
        'quality': quality
    }
```

**Thresholds:**
- 0 syntheses = Isolada (0.2)
- 1-2 syntheses = Mínima (0.2-0.5)
- 3-5 syntheses = Integrada (0.5-0.8)
- 6+ syntheses = Sintetizada (0.8-1.0)

**Por quê é crítico:**
- Sistema Dual-Core só vale a pena SE houver síntese
- Sem síntese = apenas concatenação (Python + LLM separados)
- Com síntese = emergência (todo > partes)

**Exemplo de síntese:**

```
"A métrica Python detectou dialogue_score de 57.0 com violação
DIAL.R003 (falta de subtexto). Esta análise objetiva se alinha
com o princípio de McKee no Capítulo 4 sobre 'diálogo indireto'.
Examinando a cena 12, quando Samantha diz 'Mas eu estava tendo
um sonho lindo...', vemos exatamente essa falta: a fala é direta
demais, sem camadas. McKee argumenta que personagens raramente
dizem o que realmente querem - aqui Samantha deveria ter subtexto
(medo do pai? desejo de escapar?), não apenas nostalgia literal."
```

Esta síntese integra:
- Python metric (57.0, DIAL.R003)
- Theory (McKee Chapter 4, diálogo indireto)
- Screenplay (cena 12, quote exato)
- Análise (explicação de POR QUÊ é problema)

### Combinação Layer 3

```python
def depth_validation(self, analysis: str) -> Dict:
    """Executa todas validações de profundidade"""

    causality = self.analyze_causality(analysis)
    connections = self.analyze_connections(analysis)
    insights = self.detect_insights(analysis)
    synthesis = self.analyze_synthesis(analysis)

    # Score ponderado
    depth_score = (
        causality['score'] * 0.25 +     # 25% - Análise causal
        connections['score'] * 0.25 +    # 25% - Conexões
        insights['score'] * 0.25 +       # 25% - Insights
        synthesis['score'] * 0.25        # 25% - Síntese
    )

    return {
        'score': depth_score,
        'causality': causality,
        'connections': connections,
        'insights': insights,
        'synthesis': synthesis,
        'passed': depth_score >= 0.6
    }
```

**Threshold final Layer 3:** 0.6 (60%)

**Peso no score final:** 40%

---

## SCORE FINAL E CLASSIFICAÇÃO

### Cálculo do Score Final

```python
def validate_analysis(self, analysis: str, screenplay: str) -> Dict:
    """Validação completa de 3 camadas"""

    # Layer 1: Technical (20%)
    technical = self.technical_validation(analysis)

    # Layer 2: Specificity (40%)
    specificity = self.specificity_validation(analysis, screenplay)

    # Layer 3: Depth (40%)
    depth = self.depth_validation(analysis)

    # FINAL SCORE
    final_score = (
        technical['score'] * 0.20 +
        specificity['score'] * 0.40 +
        depth['score'] * 0.40
    )

    # CLASSIFICATION
    if final_score >= 0.85:
        classification = 'EXCELLENT'
        emoji = '🌟'
    elif final_score >= 0.75:
        classification = 'VERY_GOOD'
        emoji = '✅'
    elif final_score >= 0.65:
        classification = 'GOOD'
        emoji = '👍'
    elif final_score >= 0.50:
        classification = 'ACCEPTABLE'
        emoji = '⚠️'
    else:
        classification = 'INSUFFICIENT'
        emoji = '❌'

    # GRADUATION DECISION
    # Para graduar, precisa:
    # 1. Technical PASS (70%)
    # 2. Specificity PASS (70%)
    # 3. Depth ACCEPTABLE (60%)
    # 4. Final >= 0.70

    graduated = (
        technical['passed'] and
        specificity['passed'] and
        depth['passed'] and
        final_score >= 0.70
    )

    return {
        'final_score': final_score,
        'classification': classification,
        'emoji': emoji,
        'graduated': graduated,
        'layers': {
            'technical': technical,
            'specificity': specificity,
            'depth': depth
        },
        'breakdown': {
            'technical_contribution': technical['score'] * 0.20,
            'specificity_contribution': specificity['score'] * 0.40,
            'depth_contribution': depth['score'] * 0.40
        }
    }
```

### Classificações

**EXCELLENT (0.85-1.0)** 🌟
- Technical: 90%+
- Specificity: 85%+
- Depth: 80%+
- Característica: Análise profissional de script doctor real

**VERY_GOOD (0.75-0.85)** ✅
- Technical: 80%+
- Specificity: 75%+
- Depth: 70%+
- Característica: Análise útil, com pequenas imperfeições

**GOOD (0.65-0.75)** 👍
- Technical: 70%+
- Specificity: 70%+
- Depth: 60%+
- Característica: Análise aceitável, mas poderia ser mais profunda

**ACCEPTABLE (0.50-0.65)** ⚠️
- Technical: 60%+
- Specificity: 50%+
- Depth: 50%+
- Característica: Passa no básico, mas não gradua

**INSUFFICIENT (0.0-0.50)** ❌
- Qualquer layer abaixo do threshold
- Característica: Análise genérica, inútil

### Threshold de Graduação

**Para GRADUAR um especialista:**

```python
GRADUATION_REQUIREMENTS = {
    'technical_score': 0.70,      # 70% mínimo
    'specificity_score': 0.70,    # 70% mínimo
    'depth_score': 0.60,          # 60% mínimo
    'final_score': 0.70,          # 70% mínimo

    # Critérios adicionais
    'no_generic_phrases_limit': 3,  # Max 3 frases genéricas
    'min_dialogue_quotes': 4,       # Min 4 citações
    'min_scene_refs': 3,            # Min 3 refs de cena
    'min_theory_refs': 3,           # Min 3 refs McKee
}
```

**Por quê esses thresholds:**
- 70% = Maioria aprovada em testes educacionais
- Specificity 70% = CRÍTICO (foi o problema original)
- Depth 60% = Aceitável profundidade mínima
- Technical 70% = Estrutura sólida

---

CONTINUA EM PARTE 4...
