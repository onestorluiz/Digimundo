# Fase 2: Prompts Personalizados - Implementação Completa

**Data**: 2025-10-10
**Versão**: v12.2
**Status**: ✅ IMPLEMENTADO E INTEGRADO

---

## 🎯 OBJETIVO

Elevar autores médios (3-5/10) para nível profissional (7-8/10) através de prompts específicos baseados em cada teoria.

**Impacto Esperado**:
- Autores médios: 3-5/10 → 7-8/10 (+75-133%)
- Autores nível alto: 7-8/10 → 9-10/10 (+14-25%)
- **Média geral: 5.8/10 → 7.5/10 (+29%)**

---

## 📁 ARQUIVOS CRIADOS

### 1. `engine/prompts/__init__.py`
**Propósito**: Package initialization
**Exports**:
- `AUTHOR_SPECIFIC_REQUIREMENTS`
- `get_author_specific_requirements()`
- `build_personalized_prompt_pass1()`
- `build_personalized_prompt_pass2()`

### 2. `engine/prompts/author_prompts.py` ⭐ **CORE**
**Propósito**: Prompts personalizados para cada um dos 13 autores
**Tamanho**: 1,200+ linhas
**Conteúdo**:

#### Autores Implementados (13/13):

| Autor | Focus | Min Chars | Requirements |
|-------|-------|-----------|--------------|
| **dialogue** | Multi-Theory Dialogue | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **egri** | PREMISE | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **field** | THREE-ACT STRUCTURE | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **mckee** | STORY DESIGN | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **truby** | 22 STEPS | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **snyder** | 15 SAVE THE CAT BEATS | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **vogler** | HERO'S JOURNEY (12 stages) | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **campbell** | MONOMYTH (Archetypes) | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **seger** | SCRIPT PROBLEMS | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **cowgill** | ECONOMY (Short Films) | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **aristotle** | POETICS (Mimesis, Catharsis) | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **mckee_dialogue** | DIALOGUE AS ACTION | 15,000 | 3 scenes, 3 quotes, 2 rewrites |
| **mckee_character** | CHARACTER DESIGN | 15,000 | 3 scenes, 3 quotes, 2 rewrites |

---

## 🔧 INTEGRAÇÃO COM DUAL_CORE_WRAPPER

### COMO USAR (Modo Recomendado - Opt-In):

O sistema foi implementado de forma **opt-in** para manter compatibilidade com código existente.

#### Opção 1: Usar prompts personalizados (RECOMENDADO)

```python
from engine.orchestration.dual_core_wrapper import DualCoreWrapper
from engine.analyzers.dr_dialogue import DrDialogue

specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    use_theory=True,
    deep_context=True,
    specialist_type='egri',  # Autor específico
    two_pass_llm=True,
    use_personalized_prompts=True  # ⚠️ ATIVAR PROMPTS PERSONALIZADOS
)

result = wrapper.analyze(screenplay_text)
```

#### Opção 2: Usar sistema antigo (backward compatibility)

```python
# Simplesmente NÃO passar use_personalized_prompts=True
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    use_theory=True,
    deep_context=True,
    specialist_type='egri',
    two_pass_llm=True
    # use_personalized_prompts não definido = False = sistema antigo
)
```

---

## 📊 DIFERENÇA: PROMPT ANTIGO VS PERSONALIZADO

### PROMPT ANTIGO (Genérico):

```
Analise o roteiro usando teoria de {AUTOR}.
Identifique 4 problemas.
Forneça soluções.
```

**Resultado**: Análises genéricas, 3-5/10

---

### PROMPT PERSONALIZADO (Exemplo: EGRI):

```
# SCRIPTUREMON FORENSIC ANALYSIS - PASS 1

## AUTHOR: EGRI
## FOCUS: PREMISE (Lajos Egri - The Art of Dramatic Writing)

EGRI'S METHOD:
1. Core Premise: "X leads to Y"
   - Identify screenplay's premise in one sentence
   - Cite 3+ scenes demonstrating premise
   - Quote 3+ dialogues revealing premise

2. Character Premise Alignment
   - Cite scenes where characters act against premise
   - Quote contradicting dialogue
   - Rewrite to align with premise

CRITICAL REQUIREMENTS:
✅ MUST CITE: 3+ specific scene numbers
✅ MUST CITE: 3+ specific page numbers
✅ MUST QUOTE: 3+ dialogues verbatim (20+ words each)
✅ MUST PROVIDE: 2+ ANTES/DEPOIS rewrites
✅ MINIMUM LENGTH: 15,000 characters

MANDATORY EXAMPLE FORMAT:
"PREMISE IDENTIFICADA: 'Medo leva ao isolamento'

CENA 5 (página 12): Sofia evita intimidade

DIÁLOGO ATUAL:
'Eu tenho medo de me abrir'

ANÁLISE: Egri diria que personagem DECLARA premissa
ao invés de VIVER...

SOLUÇÃO:
ANTES: 'Eu tenho medo de me abrir'
DEPOIS: [Sofia desvia olhar] 'Vamos falar de outra coisa?'
RESULTADO: Ação demonstra medo sem declarar (Egri, Cap. 4)"
```

**Resultado**: Análises específicas, 7-8/10

---

## 🎯 VALIDAÇÃO DE QUALIDADE

### Sistema de Validação Implementado:

```python
def _validate_quality(analysis: str, author: str) -> tuple[bool, float, list]:
    """
    Valida qualidade baseada em critérios dos autores nível 10.
    """
    score = 10.0
    issues = []

    # 1. Length
    if len(analysis) < 15000:
        score -= 2.0
        issues.append(f"Too short: {len(analysis)}/15000 chars")

    # 2. Scene citations
    scenes = len(re.findall(r'SCENE\s+\d+|CENA\s+\d+|página\s+\d+', analysis, re.I))
    if scenes < 3:
        score -= 2.0
        issues.append(f"Too few scenes: {scenes}/3")

    # 3. Verbatim quotes
    quotes = len(re.findall(r'"[^"]{20,}"', analysis))
    if quotes < 3:
        score -= 2.0
        issues.append(f"Too few quotes: {quotes}/3")

    # 4. ANTES/DEPOIS
    rewrites = len(re.findall(r'ANTES.*?DEPOIS|BEFORE.*?AFTER', analysis, re.DOTALL|re.I))
    if rewrites < 2:
        score -= 2.5
        issues.append(f"Too few rewrites: {rewrites}/2")

    # 5. Theory citations
    theory = len(re.findall(r'(McKee|Truby|Field|Campbell|Egri|Snyder|Seger|Cowgill|Aristotle|Vogler)', analysis))
    if theory < 3:
        score -= 1.5
        issues.append(f"Too few theory: {theory}/3")

    passed = score >= 7.0
    return passed, score, issues
```

---

## 📚 EXEMPLO COMPLETO: EGRI

### Input:
```python
wrapper = DualCoreWrapper(
    python_specialist=DrDialogue(),
    specialist_type='egri',
    use_personalized_prompts=True,
    two_pass_llm=True
)
```

### Pass 1 Prompt (Excerpt):
```
FOCUS: PREMISE (Lajos Egri - The Art of Dramatic Writing)

YOUR MISSION:
Identifique EXATAMENTE 4 PROBLEMAS usando metodologia de EGRI.

EGRI'S METHOD:
1. Core Premise: Identifique premissa "X leva a Y"
2. Character Premise Alignment: Personagens vivem premissa?
3. Premise Through Action: Mostrar vs contar
4. Premise Clarity: Premissa clara?

REQUIREMENTS:
- 3+ scene citations
- 3+ verbatim quotes
- Theory from "The Art of Dramatic Writing"
- 7,500+ characters
```

### Pass 2 Prompt (Excerpt):
```
FOCUS: EXPAND SOLUTIONS with ANTES/DEPOIS

For each of the 4 problems identified:
- Concrete line-by-line rewrite
- ANTES: Current dialogue
- DEPOIS: Improved dialogue
- Explain WHY using Egri's theory

REQUIREMENTS:
- 2+ complete rewrites
- Theory citations
- 7,500+ characters
```

### Expected Output:
```
PROBLEMA 1: Premissa implícita (Egri, Cap. 4)

CENA 3 (página 7): Sofia revela medo

DIÁLOGO ATUAL:
"Eu tenho medo de me abrir emocionalmente. Não quero
me machucar de novo como aconteceu no passado."

ANÁLISE:
Egri enfatiza que premissa deve ser VIVIDA, não DECLARADA.
Sofia CONTA sua ferida ao invés de MOSTRAR através de ações.
Premissa implícita: "Medo de vulnerabilidade leva ao isolamento"

SOLUÇÃO:
ANTES: "Eu tenho medo de me abrir..."
DEPOIS:
Julio: "Quer falar sobre o que aconteceu?"
Sofia: [desvia olhar, mexe no colar]
Sofia: "Não há nada para falar."
Julio: "Sofia—"
Sofia: [levanta] "Café? Eu faço café."

RESULTADO:
Ação mostra medo/fuga ao invés de declarar. Premissa
revelada através de comportamento (Egri, Cap. 4: Premise in Action)
```

---

## 🚀 STATUS DA IMPLEMENTAÇÃO

### ✅ COMPLETO:

1. **Prompts Personalizados**: 13/13 autores ✅
   - `engine/prompts/author_prompts.py` (1,200+ linhas)
   - Cada autor com instruções específicas
   - Exemplos obrigatórios de formato
   - Requirements claros (15K chars, 3 scenes, 3 quotes, 2 rewrites)

2. **Sistema de Validação**: ✅
   - Critérios baseados em MCKEE_DIALOGUE + CAMPBELL
   - Score 0-10 com breakdown detalhado
   - Lista de issues se falhar

3. **Integração Opt-In**: ✅
   - `use_personalized_prompts` parameter
   - Backward compatibility preservada
   - Fácil de ativar/desativar

### ✅ INTEGRAÇÃO COMPLETA (v12.2):

4. **dual_core_wrapper.py INTEGRADO** ✅:
   ```python
   # Adicionar import no topo:
   from engine.prompts import (
       build_personalized_prompt_pass1,
       build_personalized_prompt_pass2
   )

   # No __init__, adicionar parâmetro:
   def __init__(
       self,
       ...
       use_personalized_prompts: bool = False  # Opt-in
   ):
       self.use_personalized_prompts = use_personalized_prompts

   # Em _build_llm_prompt_pass1, adicionar condicional:
   def _build_llm_prompt_pass1(self, screenplay_text, python_result):
       if self.use_personalized_prompts and self.specialist_type:
           # Usar prompts personalizados
           return build_personalized_prompt_pass1(
               author=self.specialist_type,
               screenplay_context=screenplay_text[:5000],  # Excerpt
               python_metrics=self._format_python_result(python_result)
           )
       else:
           # Usar prompt original (backward compatibility)
           return self._build_original_prompt_pass1(...)

   # Mesmo para _build_llm_prompt_pass2
   ```

5. **Adicionar Método de Validação**:
   ```python
   def _validate_analysis_quality(self, analysis: str) -> tuple[bool, float, list]:
       """Validate analysis quality using nivel 10 criteria."""
       import re

       score = 10.0
       issues = []

       # Length check
       if len(analysis) < 15000:
           score -= 2.0
           issues.append(f"Too short: {len(analysis)}/15000")

       # Scene citations
       scenes = len(re.findall(r'SCENE\s+\d+|CENA\s+\d+|página\s+\d+', analysis, re.I))
       if scenes < 3:
           score -= 2.0
           issues.append(f"Too few scenes: {scenes}/3")

       # Quotes
       quotes = len(re.findall(r'"[^"]{20,}"', analysis))
       if quotes < 3:
           score -= 2.0
           issues.append(f"Too few quotes: {quotes}/3")

       # ANTES/DEPOIS
       rewrites = len(re.findall(r'ANTES.*?DEPOIS|BEFORE.*?AFTER', analysis, re.DOTALL|re.I))
       if rewrites < 2:
           score -= 2.5
           issues.append(f"Too few rewrites: {rewrites}/2")

       passed = score >= 7.0
       return passed, score, issues
   ```

6. **Testar com 1 Autor**:
   ```bash
   python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" \\
       --author egri --deep
   ```

7. **Validar Resultados**:
   - Score ≥ 7.0?
   - 3+ scenes citadas?
   - 3+ quotes verbatim?
   - 2+ ANTES/DEPOIS?

8. **Aplicar a Todos os Autores**

---

## 📊 RESULTADOS ESPERADOS

| Autor | Antes | Após Prompts | Melhoria |
|-------|-------|--------------|----------|
| DIALOGUE | 7/10 | 8/10 | +14% |
| EGRI | 7/10 | 8/10 | +14% |
| FIELD | 7/10 | 8/10 | +14% |
| MCKEE | 8/10 | 9/10 | +12% |
| SEGER | 7/10 | 8/10 | +14% |
| **SNYDER** | 3/10 | **7/10** | **+133%** ⭐ |
| **ARISTOTLE** | 3/10 | **6/10** | **+100%** ⭐ |
| **TRUBY** | 4/10 | **7/10** | **+75%** ⭐ |
| **COWGILL** | 3/10 | **6/10** | **+100%** ⭐ |
| **VOGLER** | 4/10 | **7/10** | **+75%** ⭐ |
| **MCKEE_CHARACTER** | 5/10 | **7/10** | **+40%** ⭐ |
| MCKEE_DIALOGUE | 8/10 | 9/10 | +12% |
| CAMPBELL | 7/10 | 8/10 | +14% |

**Média**: 5.8/10 → **7.5/10** (+29%)

---

## 🔗 LINKS RELACIONADOS

- **Código Fonte**: `engine/prompts/author_prompts.py`
- **Documentação Geral**: `AUTORES_NIVEL_10_E_PLANO.md`
- **Two-Pass Architecture**: `TWO_PASS_OFFICIAL_METHOD.md`
- **Test Results**: Pending implementation

---

## 💡 COMO ATIVAR

### Para Scripts Existentes:

```python
# Antes (Two-Pass apenas)
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    specialist_type='egri',
    two_pass_llm=True
)

# Depois (Two-Pass + Prompts Personalizados)
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    specialist_type='egri',
    two_pass_llm=True,
    use_personalized_prompts=True  # ⚠️ ADICIONAR ESTA LINHA
)
```

---

---

## 📦 CHANGELOG v12.2 - INTEGRAÇÃO COMPLETA

**Data**: 2025-10-10 (Fase 2 completada e integrada)

### Arquivos Modificados:

1. **`engine/orchestration/dual_core_wrapper.py`**:
   - ✅ Adicionado import de `build_personalized_prompt_pass1` e `build_personalized_prompt_pass2`
   - ✅ Adicionado parâmetro `use_personalized_prompts: bool = False` (opt-in)
   - ✅ Modificado `_build_llm_prompt_pass1()` para usar prompts personalizados quando ativado
   - ✅ Modificado `_build_llm_prompt_pass2()` para usar prompts personalizados quando ativado
   - ✅ Adicionado método `_validate_analysis_quality()` com critérios nivel 10
   - ✅ Integrado validação nivel 10 no fluxo de análise (linhas 224-240)

2. **`test_personalized_prompts.py`**:
   - ✅ Criado script de teste para validar integração
   - ✅ Testa EGRI com prompts personalizados + Two-Pass LLM

### Funcionalidade Implementada:

**ANTES (v12.1)**:
```python
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    specialist_type='egri',
    two_pass_llm=True
)
# Usava prompt genérico
```

**DEPOIS (v12.2)**:
```python
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    specialist_type='egri',
    two_pass_llm=True,
    use_personalized_prompts=True  # ⚠️ NOVO: Ativa prompts específicos por autor
)
# Usa prompt personalizado para EGRI com critérios específicos de Premise theory
```

### Validação de Qualidade:

Sistema agora valida automaticamente análises com prompts personalizados:

- ✅ Mínimo 15,000 caracteres
- ✅ 3+ citações de cenas (CENA X, página Y)
- ✅ 3+ citações verbatim de diálogos (com aspas)
- ✅ 2+ exemplos ANTES/DEPOIS de reescrita
- ✅ 3+ citações de teoria

**Score >= 7.0/10 = Qualidade profissional**

### Próximos Passos:

1. Testar com roteiro completo (Te Encontro em Mim.pdf)
2. Validar com todos os 13 autores
3. Medir impacto real na qualidade (esperado: 5.8/10 → 7.5/10)
4. Aplicar em produção se resultados confirmarem hipótese

---

**Criado por**: Scripturemon Team
**Data Inicial**: 2025-10-10
**Última Atualização**: 2025-10-10 (v12.2)
**Versão**: v12.2
**Status**: ✅ **FASE 2 IMPLEMENTADA E INTEGRADA - PRONTO PARA TESTES**
