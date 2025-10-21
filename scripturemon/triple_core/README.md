# 🎬 TRIPLE-CORE ARCHITECTURE

Sistema de análise profissional de roteiros com **3 cores independentes**.

---

## 📊 ARQUITETURA

```
INPUT: Screenplay Text
  ↓
┌─────────────────────────────────────────┐
│ CORE 1: Python Technical Analysis       │
│ - 24 especialistas Dr* (Python puro)    │
│ - Métricas objetivas, scores            │
│ - Tempo: ~0.0s                          │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ CORE 2: Master Examples Finder          │
│ - Busca em 33 roteiros mestres          │
│ - Exemplos concretos de soluções        │
│ - Tempo: ~0.0s                          │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ CORE 3: LLM Theory Enrichment           │
│ - Model: scripturemon-optimized         │
│ - Context: McKee full book (77k words)  │
│ - Tempo: ~5-7 minutos                   │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ ORCHESTRATOR: Synthesis                 │
│ - Combina os 3 cores                    │
│ - Gera TXT + HTML humanizados           │
└─────────────────────────────────────────┘
  ↓
OUTPUT: Formatted Reports (TXT + HTML)
```

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
triple_core/
├── __init__.py                    # Imports principais
│
├── core_1_specialists/            # 🔧 PYTHON CORE 1
│   ├── __init__.py
│   ├── base/                      # Classes base
│   ├── dialogue/                  # DrDialogue
│   ├── structure/                 # DrStructure
│   ├── character/                 # DrPsychology, DrArcs, DrRelationships
│   ├── theme/                     # Temas e subtexto
│   ├── style/                     # Tom, voz
│   ├── formatting/                # Formatação técnica
│   └── quality/                   # Qualidade geral
│
├── core_2_examples/               # 📚 PYTHON CORE 2
│   ├── __init__.py
│   ├── example_finder.py          # ExampleFinderCore
│   ├── example_formatter.py       # Formatação de exemplos
│   └── masters_index.py           # Indexação dos 33 roteiros
│
├── core_3_llm/                    # 🤖 LLM CORE 3
│   ├── __init__.py
│   ├── prompt_builder.py          # Prompt de 260 linhas
│   ├── theory_loader.py           # McKee book loader
│   ├── llm_caller.py              # Subprocess Ollama
│   └── response_parser.py         # Parse da resposta
│
├── orchestrators/                 # 🎯 WRAPPERS
│   ├── __init__.py
│   ├── dual_core_wrapper.py       # 2 cores (Python + LLM)
│   └── triple_core_wrapper.py     # 3 cores (Python + Examples + LLM)
│
└── exporters/                     # 📄 OUTPUT
    ├── __init__.py
    └── formatted_exporter.py      # TXT + HTML export
```

---

## 🚀 QUICK START

### Uso Básico (Triple-Core)

```python
from triple_core import TripleCoreWrapper
from triple_core.core_1_specialists.dialogue import DrDialogue

# 1. Criar especialista Python (Core 1)
specialist = DrDialogue()

# 2. Criar wrapper Triple-Core
wrapper = TripleCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-optimized",
    deep_context=True  # OBRIGATÓRIO para qualidade
)

# 3. Analisar roteiro
with open("screenplay.txt") as f:
    screenplay_text = f.read()

result = wrapper.analyze(screenplay_text)

# 4. Exportar resultados
wrapper.export_formatted(result, "My Screenplay", format="txt")
wrapper.export_formatted(result, "My Screenplay", format="html")
```

### Uso de Core Individual

```python
# CORE 1: Apenas Python (análise técnica)
from triple_core.core_1_specialists.dialogue import DrDialogue

specialist = DrDialogue()
python_result = specialist.analyze(screenplay_text)
# Output: Dict com scores, violations, recommendations

# CORE 2: Apenas Examples (busca em mestres)
from triple_core.core_2_examples import ExampleFinderCore

finder = ExampleFinderCore()
examples = finder.analyze(
    base_analysis=python_result,
    screenplay_text=screenplay_text
)
# Output: 6 exemplos de 33 roteiros mestres

# CORE 3: Usar via DualCoreWrapper
from triple_core.orchestrators import DualCoreWrapper

wrapper = DualCoreWrapper(
    python_specialist=specialist,
    deep_context=True
)
result = wrapper.analyze(screenplay_text)
# Output: Python + LLM synthesis
```

---

## 📊 CORES DETALHADOS

### CORE 1: Python Technical Analysis

**Função:** Análise objetiva e técnica do roteiro

**Especialistas disponíveis:**
- **dialogue/DrDialogue** - Diálogos e subtexto
- **structure/DrStructure** - Estrutura de 3 atos
- **character/DrPsychology** - Psicologia de personagens
- **character/DrArcs** - Arcos de personagem
- **character/DrRelationships** - Relacionamentos
- ...24 especialistas no total

**Output:**
```python
{
    'score': 70.0,
    'violations': 2,
    'recommendations': [
        "Strengthen character voices",
        "Add more subtext to dialogue"
    ],
    'rules_violated': ['DISTINCT_VOICES', 'SUBTEXT_DEPTH']
}
```

**Tempo:** ~0.0s (Python puro, instantâneo)

---

### CORE 2: Master Examples Finder

**Função:** Buscar exemplos concretos de soluções em roteiros mestres

**Masters indexados (33 roteiros):**
- Pulp Fiction (Tarantino)
- Inception (Nolan)
- The Dark Knight (Nolan)
- Gladiator
- American Beauty
- Star Wars IV
- The Matrix
- ...e mais 26 roteiros clássicos

**Output:**
```python
{
    'total_examples': 6,
    'screenplays_searched': 33,
    'examples_found': [
        {
            'problem_addressed': 'Lacking distinct character voices',
            'screenplay': 'Pulp Fiction',
            'character': 'JULES',
            'dialogue': 'The path of the righteous man...',
            'context': 'Opening apartment scene',
            'why_good': 'Biblical cadence creates unique voice',
            'lesson': 'Give each character unique rhythm and vocabulary'
        },
        ...
    ]
}
```

**Tempo:** ~0.0s (indexação pré-computada)

---

### CORE 3: LLM Theory Enrichment

**Função:** Análise profunda com teoria McKee

**Model:** scripturemon-optimized (Ollama)
**Context:** McKee full book (77k words)
**Prompt:** 260 linhas (few-shot + task instructions)

**Componentes do Prompt:**
1. Few-shot examples (análise BOA vs MÁ)
2. Task instructions (12-14 parágrafos)
3. Primacy/Recency mitigation
4. Deep context (livro McKee completo)
5. Screenplay text
6. Core 1 metrics

**Output:**
```
12-14 parágrafos detalhados:
- INTERPRETATION (2 parágrafos)
- PATTERNS (2 parágrafos)
- PROBLEMS (3-4 parágrafos)
- SOLUTIONS (3-4 parágrafos)
- DEPTH (2 parágrafos)

Total: 2500-4000 tokens
Referências: 8+ citações McKee
Citações: 4+ trechos do roteiro
```

**Tempo:** ~5-7 minutos (Deep Dive mode)

---

## ⚙️ ORCHESTRATORS

### DualCoreWrapper (Base)

Combina **Core 1 (Python) + Core 3 (LLM)**

```python
from triple_core.orchestrators import DualCoreWrapper

wrapper = DualCoreWrapper(
    python_specialist=DrDialogue(),
    llm_model="scripturemon-optimized",
    deep_context=True
)
```

**Output:** Python metrics + LLM insights + Synthesis

---

### TripleCoreWrapper (Triple-Core)

Combina **Core 1 (Python) + Core 2 (Examples) + Core 3 (LLM)**

```python
from triple_core import TripleCoreWrapper

wrapper = TripleCoreWrapper(
    python_specialist=DrDialogue(),
    llm_model="scripturemon-optimized",
    deep_context=True
)
```

**Design Pattern:** Herança de DualCoreWrapper
- Herda prompt completo (260 linhas)
- Adiciona APENAS ExampleFinderCore
- Zero duplicação de código

**Output:** Python + Examples + LLM + Synthesis

---

## 📄 EXPORTERS

### FormattedExporter

Exporta resultados em formatos humanizados.

**TXT Format (5 fases):**
```
1. ANÁLISE TÉCNICA (Core 1)
2. EXEMPLOS DE MESTRES (Core 2)
3. TEORIA MCKEE (Core 3)
4. SÍNTESE
5. PLANO DE AÇÃO
```

**HTML Format (4 partes):**
- Análise Python (tabelas)
- Exemplos mestres (cards)
- Insights LLM (parágrafos)
- Síntese final (destaque)

**Output location:** `workspace/outputs/formatted/`

---

## 🎯 QUALITY METRICS

### Métricas Validadas (Score 1.00/1.0 EXCELLENT)

```python
QUALITY_METRICS = {
    'final_score': 1.00,              # 0.85+ = EXCELLENT
    'mckee_references': 8,            # 8+ citações com capítulos
    'dialogue_quotes': 4,             # 4+ trechos do roteiro
    'scene_references': 6,            # 6+ referências de cena
    'examples_found': 6,              # De 33 roteiros mestres
    'execution_time': 329,            # Segundos (Deep Dive)
    'graduated': True                 # Threshold: 0.70
}
```

### Comparação: Dual-Core vs Triple-Core

| Métrica | Dual | Triple | Δ |
|---------|------|--------|---|
| Análises | 2 | 3 | +50% |
| Exemplos | 0 | 6 | ∞ |
| Fases | 3 | 5 | +67% |
| Tempo | 7min | 5.5min | -21% |
| Score | 0.87 | 1.00 | +15% |

---

## 🔥 10 REGRAS CRÍTICAS

1. **NUNCA SIMPLIFICAR PROMPT** - 260 linhas obrigatórias
2. **CORE 2 NÃO VAI PARA LLM** - Apenas na síntese
3. **DEEP CONTEXT OBRIGATÓRIO** - `deep_context=True`
4. **MODEL FIXO** - `scripturemon-optimized`
5. **TIMEOUT MÍNIMO 600s** - Deep Dive demora
6. **HERANÇA OBRIGATÓRIA** - Triple herda Dual
7. **VALIDAR 6 MÉTRICAS** - Antes de graduar
8. **TXT HUMANIZADO** - 5 fases em português
9. **HTML ESTRUTURADO** - 4 partes coloridas
10. **BACKUP ANTES DE MODIFICAR** - Sistema crítico

---

## 🔄 EVOLUÇÕES FUTURAS

### V3: Quad-Core (Planejado)
```
+ CORE 4: Peer Review (outro especialista valida)
```

### V4: Penta-Core (Futuro)
```
+ CORE 5: Market Fit (análise mercado/público)
```

---

## 📚 DOCUMENTAÇÃO ADICIONAL

- **Guia Completo:** `/claude_code/MEMORY/🔥_critical/SCRIPTUREMON_TRIPLE_CORE_COMPLETE_GUIDE.md`
- **Integração Uchimon:** `/claude_code/MEMORY/conhecimentos/SCRIPTUREMON_TRIPLE_CORE_INTEGRATION.md`
- **Root Cause Analysis:** `/claude_code/MEMORY/🔥_critical/SCRIPTUREMON_QUALITY_FIX_20251002.md`

---

## ✅ COMPLIANCE

**Uchimon Laws:** 15/15 ✅
**Quality Score:** 1.00/1.0 EXCELLENT ✅
**Documentation:** 45KB ✅
**Git Commits:** Realizados ✅
**Status:** OPERATIONAL ✅

---

**🎬 TRIPLE-CORE ARCHITECTURE - READY FOR PRODUCTION 🎬**

**Version:** 1.0.0
**Date:** 03/10/2025
**Status:** ✅ OPERATIONAL

**DIGIMUNDO PRESENTE 🥷**
