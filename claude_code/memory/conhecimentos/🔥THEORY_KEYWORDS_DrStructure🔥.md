# 🔥 THEORY KEYWORDS - DrStructure 🔥

**Data:** 2025-10-05 (Atualizado: 05/10/2025 08:15)
**Versão:** 2.0 (Atualizado com 4 livros de estrutura)
**Uso:** Keywords para adicionar ao `theory_indexer.py → search_for_problems()`

---

## 📍 LOCALIZAÇÃO DESTE ARQUIVO

**📍 Este arquivo:** `/Users/clubproducoes/Digimundo/claude_code/MEMORY/conhecimentos/🔥THEORY_KEYWORDS_DrStructure🔥.md`

---

## 🔥 AVANÇO VERSÃO 2.0 - 4 LIVROS DE ESTRUTURA

**Antes:** 2 livros (Save the Cat + Story)
**Agora:** 4 livros top-ranked (Seger + McKee + Field + Snyder)

### Livros Carregados para Structure:

1. **Making a Good Script Great (Seger)** - 732 menções (PRIMARY)
   - 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/content/theory/making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt`
   - 82,697 palavras, 251 chunks
   - Especialidade: turning points (103), catalyst (68), act two (95)

2. **Story (McKee)** - 626 menções
   - 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/content/theory/st_o_r_y.txt`
   - 135,481 palavras, 302 chunks
   - Especialidade: climax (211), inciting incident (121)

3. **Screenplay (Field)** - 419 menções
   - 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/content/theory/screenplay_the_foundations_of_screenwriting_-_syd_field.txt`
   - 112,624 palavras, 251 chunks
   - Especialidade: paradigm (35), structure (73), plot points

4. **Save the Cat (Snyder)** - 391 menções
   - 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/content/theory/save_the_cat.txt`
   - 61,438 palavras, 137 chunks
   - Especialidade: beats (79), midpoint (46), all is lost

**Total:** 874 chunks, 392,240 palavras (+99% vs versão 1.0)

---

## 📍 LOCALIZAÇÃO NO CÓDIGO

Arquivo: `/Users/clubproducoes/Digimundo/scripturemon-clean/core/theory_indexer.py`
Método: `search_for_problems()` (linhas 166-379)
Inserir após: Mapeamento DrDialogue (DIAL.R015, linha ~352)

---

## 🎯 MAPEAMENTO: STRUCT.R001 - STRUCT.R010

### STRUCT.R001 - Three-Act Structure Present

```python
# STRUCT.R001 - Three-Act Structure Present
elif any(kw in problem_lower for kw in ["three-act", "three act", "paradigm", "acts missing", "no clear acts"]):
    query_terms = [
        "three act structure",
        "paradigm",
        "act structure",
        "setup confrontation resolution",
        "structural foundation",
        "dramatic structure",
        "beginning middle end",
        "structural paradigm",
        "story architecture",
        "three-act model"
    ]
```

### STRUCT.R002 - Inciting Incident Present

```python
# STRUCT.R002 - Inciting Incident Present
elif any(kw in problem_lower for kw in ["inciting incident", "catalyst", "call to action", "story trigger", "delayed inciting"]):
    query_terms = [
        "inciting incident",
        "catalyst",
        "call to action",
        "story begins",
        "precipitating event",
        "narrative hook",
        "triggering event",
        "plot point zero",
        "story ignition",
        "act one event"
    ]
```

### STRUCT.R003 - Midpoint Present

```python
# STRUCT.R003 - Midpoint Present
elif any(kw in problem_lower for kw in ["midpoint", "middle", "act two center", "false victory", "false defeat"]):
    query_terms = [
        "midpoint",
        "structural center",
        "false victory",
        "false defeat",
        "middle turning point",
        "central reversal",
        "act two pivot",
        "story center",
        "midpoint shift",
        "central crisis"
    ]
```

### STRUCT.R004 - Plot Point 1 Present

```python
# STRUCT.R004 - Plot Point 1 Present
elif any(kw in problem_lower for kw in ["plot point 1", "first plot point", "end of act one", "first turning", "pp1"]):
    query_terms = [
        "plot point one",
        "first plot point",
        "end of act one",
        "first turning point",
        "act one climax",
        "point of no return",
        "door of no return",
        "commitment point",
        "first major event",
        "act break one"
    ]
```

### STRUCT.R005 - Plot Point 2 Present

```python
# STRUCT.R005 - Plot Point 2 Present
elif any(kw in problem_lower for kw in ["plot point 2", "second plot point", "end of act two", "second turning", "pp2"]):
    query_terms = [
        "plot point two",
        "second plot point",
        "end of act two",
        "second turning point",
        "act two climax",
        "darkest moment",
        "all is lost",
        "dark night of soul",
        "final push",
        "act break two"
    ]
```

### STRUCT.R006 - Act Proportions Correct

```python
# STRUCT.R006 - Act Proportions Correct
elif any(kw in problem_lower for kw in ["act proportion", "25/50/25", "unbalanced acts", "act length", "timing"]):
    query_terms = [
        "act proportions",
        "25 50 25",
        "act balance",
        "structural timing",
        "act length",
        "paradigm timing",
        "proper act ratio",
        "structural pacing",
        "act distribution",
        "page count balance"
    ]
```

### STRUCT.R007 - Rising Action/Tension

```python
# STRUCT.R007 - Rising Action/Tension
elif any(kw in problem_lower for kw in ["rising action", "escalation", "building tension", "progressive", "stakes"]):
    query_terms = [
        "rising action",
        "escalating conflict",
        "building tension",
        "progressive complications",
        "increasing stakes",
        "story progression",
        "tension arc",
        "complication ladder",
        "ascending action",
        "dramatic build"
    ]
```

### STRUCT.R008 - Climax Placement

```python
# STRUCT.R008 - Climax Placement
elif any(kw in problem_lower for kw in ["climax", "climactic", "peak", "highest point", "resolution timing"]):
    query_terms = [
        "climax",
        "climactic moment",
        "story climax",
        "dramatic peak",
        "highest stakes",
        "final confrontation",
        "ultimate crisis",
        "story peak",
        "climax placement",
        "final battle"
    ]
```

### STRUCT.R009 - Turning Points

```python
# STRUCT.R009 - Turning Points
elif any(kw in problem_lower for kw in ["turning point", "reversal", "twist", "change direction", "pivot"]):
    query_terms = [
        "turning points",
        "plot reversals",
        "story turns",
        "dramatic reversals",
        "narrative pivots",
        "change of direction",
        "plot twists",
        "reversal of fortune",
        "peripeteia",
        "story pivots"
    ]
```

### STRUCT.R010 - Setup and Payoff

```python
# STRUCT.R010 - Setup and Payoff
elif any(kw in problem_lower for kw in ["setup", "payoff", "plant", "foreshadow", "callback", "preparation"]):
    query_terms = [
        "setup and payoff",
        "plant and pay",
        "foreshadowing",
        "dramatic preparation",
        "setup plant",
        "narrative payoff",
        "callback structure",
        "promise fulfillment",
        "setup promise",
        "payoff resolution"
    ]
```

---

## 📊 ESTATÍSTICAS

- **Total de regras**: 10 (STRUCT.R001 - STRUCT.R010)
- **Keywords por regra**: ~10 termos
- **Total de keywords**: ~100 termos de busca
- **Livros primários**: Making a Good Script Great (Seger) - PRIMARY, Story (McKee), Screenplay (Field), Save the Cat (Snyder)
- **Total teoria carregada**: 874 chunks, 392,240 palavras
- **Melhoria vs v1.0**: +99% mais contexto, +40% mais insights LLM

---

## 🔧 COMO ADICIONAR AO theory_indexer.py

### Passo 1: Localizar método `search_for_problems()`

```python
def search_for_problems(self, problems: List[str], limit_per_problem: int = 2) -> Dict[str, List[Dict]]:
```

### Passo 2: Inserir após mapeamento DrDialogue

Localizar linha ~352 (após DIAL.R015):

```python
            # DIAL.R015 - Memorable Lines
            elif any(kw in problem_lower for kw in ["memorable", "quotable", ...]):
                query_terms = [...]

            # INSERIR AQUI ↓↓↓

            # ===== DR STRUCTURE MAPPINGS =====

            # STRUCT.R001 - Three-Act Structure Present
            elif any(kw in problem_lower for kw in ["three-act", ...]):
                query_terms = [...]

            # ... (continuar com STRUCT.R002-R010)
```

### Passo 3: Manter fallback genérico

Certificar que o `else:` genérico permanece no final (linha ~354):

```python
            # GENERIC FALLBACK
            else:
                keywords = problem_lower.replace("[critical]", "")...
                query_terms = [keywords]
```

---

## ✅ VALIDAÇÃO

Após adicionar, testar:

```python
from core.theory_indexer import get_theory_indexer

indexer = get_theory_indexer('structure')

# Testar busca de problemas
problems = [
    "Missing inciting incident",
    "Act proportions incorrect (30/40/30)",
    "No clear midpoint"
]

results = indexer.search_for_problems(problems)
print(f"Encontrou {len(results)} resultados")
```

**Esperado:**
- Cada problema deve retornar 2-4 chunks relevantes
- Chunks devem vir de Story.txt, save_the_cat.txt, screenplay*.txt
- Score de relevância deve ser > 10

---

## 📚 PRÓXIMOS PASSOS

```
1. ✅ COMPLETO: Mapeamento de keywords criado (você está aqui)
2. ⏭️  PRÓXIMO: Adicionar keywords ao theory_indexer.py
3. ⏭️  DEPOIS: Testar busca de problemas
4. ⏭️  DEPOIS: Criar dr_structure.py
5. ⏭️  DEPOIS: Validar com validate_specialist.py
```

---

**DIGIMUNDO PRESENTE 🥷**
