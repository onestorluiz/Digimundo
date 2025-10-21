# 🔥🔥🔥 SCRIPTUREMON - MASTER INDEX 🔥🔥🔥

**Data:** 2025-10-05 (Atualizado: 05/10/2025 08:12)
**Versão:** 2.1 (Atualizado com 4 livros de estrutura + DrStructure completo)
**Localização Projeto:** `/Users/clubproducoes/Digimundo/scripturemon-clean`
**📍 Localização DESTE Arquivo:** `/Users/clubproducoes/Digimundo/claude_code/🔥🔥🔥SCRIPTUREMON_MASTER_INDEX🔥🔥🔥.md`

---

## 🔥 ÚLTIMOS AVANÇOS - VERSÃO 2.1 (05/10/2025)

### ✅ DrStructure com 4 Livros de Teoria (2x Mais Contexto!)

**Antes:** Estrutura usava apenas 2 livros (Save the Cat + Story)
**Agora:** Estrutura usa 4 livros top-ranked por relevância:

1. **Making a Good Script Great (Seger)** - 732 menções estruturais (turning point: 103, act two: 95, catalyst: 68)
2. **Story (McKee)** - 626 menções (climax: 211, inciting incident: 121)
3. **Screenplay (Field)** - 419 menções (paradigm: 35, structure: 73)
4. **Save the Cat (Snyder)** - 391 menções (beats: 79, midpoint: 46)

**Impacto:**
- 📚 Chunks: 439 → 874 (+99%)
- 📖 Palavras: 196,919 → 392,240 (+99%)
- 🤖 LLM Insights: 2,907 → 4,063 chars (+40%)
- 📑 Citações: 3 autores (Seger, McKee, Field)

**Arquivos modificados:**
- 📍 `/Users/clubproducoes/Digimundo/scripturemon-clean/core/theory_indexer.py`
  - Linha 691: Primary mapping → `'structure': 'making-a-good-script-great'`
  - Linhas 853-858: Multi-book array com 4 livros
  - Linhas 708-710, 879-881: Author mappings (seger, field, snyder)

**Validação:**
- ✅ Test: `/Users/clubproducoes/Digimundo/claude_code/MEMORY/conhecimentos/🔥🔥🔥test_integration_complete🔥🔥🔥.py`
- ✅ Output: `Test_structure_20251005_080955.html`
- ✅ Resultados: 4 books loaded, 874 chunks, 392K palavras

---

## 🎯 SEÇÃO 1: O QUE É SCRIPTUREMON?

### Definição

**Scripturemon** é um sistema profissional de análise de roteiros que combina:
- **Análise Python objetiva** (métricas quantitativas)
- **Insights de teoria clássica** (13 livros de screenwriting)
- **Análise LLM qualitativa** (interpretação profunda via IA)

### Para Que Serve

**Objetivo:** Fornecer feedback profissional detalhado sobre roteiros
**Usuário:** Roteiristas que querem melhorar seus scripts
**Output:** Relatórios HTML/Markdown com score, problemas, soluções e exemplos

### O Que Ele Faz

```
INPUT: Roteiro (.txt, .pdf, .fountain)
  ↓
ANÁLISE: 22 especialistas Python + 13 livros de teoria + LLM
  ↓
OUTPUT: Relatório profissional com:
  - Overall Score (0-100)
  - Breakdown por dimensão (dialogue, structure, character, etc)
  - Problemas identificados (com severity)
  - Soluções práticas
  - Exemplos de roteiros mestres
```

### Diferenciais

✅ **Análise Multi-Perspectiva:** 13 autores de teoria (McKee, Truby, Campbell, etc)
✅ **Bilíngue:** Suporta roteiros em inglês e português
✅ **Deep Context:** Carrega livro completo (~128k tokens) para análise profunda
✅ **Tradução Automática:** HTMLs em inglês traduzidos para português via LLM
✅ **Organizado:** Estrutura de pastas numeradas automáticas

---

## 🏗️ SEÇÃO 2: COMPONENTES PRINCIPAIS

### Arquitetura Visual

```
┌────────────────────────────────────────────────────────────────┐
│                      SCRIPTUREMON SYSTEM                        │
└────────────────────────────────────────────────────────────────┘

INPUT: screenplay.txt
  │
  ├─────────────────────────────────────────────────────────────┐
  │                                                               │
  ▼                                                               ▼
┌──────────────────────┐                            ┌──────────────────────┐
│   CORE 1: PYTHON     │                            │  ANÁLISE COMPLETA    │
│   (Objetivo)         │                            │  (22 Specialists)    │
│                      │                            │                      │
│ - DrDialogue         │                            │ ScreenplayAnalyzer   │
│ - DrStructure        │                            │   ├─ Dialogue        │
│ - DrPacing           │                            │   ├─ Structure       │
│ - ... (22 total)     │                            │   ├─ Pacing          │
│                      │                            │   ├─ Character       │
│ Output: Métricas     │                            │   └─ ... (22 total)  │
│         Violations   │                            │                      │
│         Score        │                            │ Output: Overall      │
└──────────┬───────────┘                            │         Report       │
           │                                        └──────────────────────┘
           │
           ▼
┌──────────────────────┐
│  DUAL-CORE WRAPPER   │
│  (Integrador)        │
│                      │
│ 1. Recebe Python     │
│ 2. Carrega teoria    │◄────────┐
│ 3. Chama LLM         │         │
│ 4. Sintetiza         │         │
│ 5. Exporta HTML      │         │
└──────────┬───────────┘         │
           │                     │
           ▼                     │
┌──────────────────────┐         │
│   CORE 2: LLM        │         │
│   (Qualitativo)      │         │
│                      │         │
│ - Ollama CLI         │         │
│ - Model: optimized   │         │
│ - Deep context       │         │
│ - Timeout: 900s      │         │
│                      │         │
│ Output: Insights     │         │
│         Patterns     │         │
│         Solutions    │         │
└──────────┬───────────┘         │
           │                     │
           ▼                     │
┌──────────────────────┐         │
│  FORMATTED EXPORTER  │         │
│  (HTML/TXT)          │         │
│                      │         │
│ - CSS Profissional   │         │
│ - 3 partes:          │         │
│   1. Python          │         │
│   2. LLM             │         │
│   3. Síntese         │         │
└──────────┬───────────┘         │
           │                     │
           ▼                     │
   ┌───────────────┐             │
   │ ANALYSIS.HTML │             │
   └───────────────┘             │
                                 │
        ┌────────────────────────┘
        │
        │  TEORIA (13 livros)
        │
        ▼
┌──────────────────────┐
│  THEORY INDEXER      │
│  (Carregador)        │
│                      │
│ Path: content/theory/│
│                      │
│ 13 livros TXT:       │
│ - McKee (Story)      │
│ - McKee (Dialogue)   │
│ - McKee (Character)  │
│ - Truby              │
│ - Campbell           │
│ - Vogler             │
│ - Field              │
│ - Seger              │
│ - Egri               │
│ - Snyder             │
│ - Cowgill            │
│ - Aristotle          │
│ - Weiland            │
│                      │
│ Total: 1.2M palavras │
│ Chunks: ~2,700       │
│                      │
│ Modos:               │
│ - SHALLOW (BM25)     │
│ - DEEP (livro full)  │
└──────────────────────┘
```

### Componentes Detalhados

#### 1. **CORE 1: Python Specialists (22 especialistas)**

**O que faz:** Análise objetiva e quantitativa do roteiro

**Especialistas disponíveis:**
```
NARRATIVE (6):
  - Structure: 3-act, plot points, proportions
  - Pacing: Ritmo, beats, timing
  - Opening: Hook, setup, inciting incident
  - Climax: Stakes, agency, payoff
  - Resolution: Closure, satisfaction
  - Transitions: Scene flow, continuity

CHARACTER (3):
  - Psychology: Depth, consistency, believability
  - Arcs: Transformation, growth
  - Relationships: Dynamics, conflicts

DIALOGUE (3):
  - Dialogue: Authenticity, purpose
  - Voice: Distinctiveness, consistency
  - Subtext: Layers, implication

TECHNICAL (2):
  - Formatting: Industry standards
  - Action: Visual storytelling

DEPTH (5):
  - Symbolism: Metaphors, imagery
  - Theme: Consistency, exploration
  - Tone: Mood, atmosphere
  - Visual Motifs: Recurring elements
  - (Subtext também aqui)

CRAFT (2):
  - Genre: Conventions, expectations
  - World Building: Setting, rules

MARKET (2):
  - Originality: Fresh perspectives
  - Market Potential: Comercial viability
```

**Output típico:**
```python
{
    'score': 85.0,  # 0-100
    'rule_violations': [
        {'id': 'DIAL.R003', 'severity': 'high', 'message': '...'},
        ...
    ],
    'recommendations': ['Fix X', 'Improve Y', ...],
    'data': {
        # Métricas específicas do specialist
        'authenticity_score': 0.82,
        'voice_profiles': [...],
        ...
    }
}
```

---

#### 2. **DUAL-CORE WRAPPER (Integrador)**

**O que faz:** Transforma análise Python em análise Dual-Core (Python + LLM)

**Path:** `triple_core/orchestrators/dual_core_wrapper.py`

**Fluxo:**
```
1. Recebe specialist Python (ex: DrDialogue)
2. Executa análise Python → score + violations
3. Carrega teoria relevante via theory_indexer
4. Constrói prompt LLM com Python result + teoria
5. Chama Ollama subprocess
6. Sintetiza Python + LLM em resultado unificado
7. Exporta HTML formatado
```

**Parâmetros críticos:**
```python
DualCoreWrapper(
    python_specialist=DrDialogue(),  # Qual specialist usar
    specialist_type='dialogue',       # Qual teoria carregar
    deep_context=True,                # Livro completo ou chunks?
    use_theory=True,                  # Carregar teoria?
    llm_model='scripturemon-optimized',
    llm_timeout=900                   # 15min para deep context
)
```

---

#### 3. **THEORY INDEXER (Carregador de Teoria)**

**O que faz:** Indexa e busca nos 13 livros de screenwriting theory

**Path:** `core/theory_indexer.py`
**Livros Path:** `content/theory/*.txt`

**13 Livros Indexados:**

| Autor | Livro | Palavras | Chunks | Usado Por |
|-------|-------|----------|--------|-----------|
| McKee | Story | 135k | 302 | 'mckee', 'dialogue' |
| McKee | Dialogue | 77k | 173 | 'mckee_dialogue', 'dialogue' |
| McKee | Character | 93k | 209 | 'mckee_character' |
| Truby | Anatomy of Story | 126k | 282 | 'truby', 'dialogue' |
| Campbell | Hero's Journey | 127k | 285 | 'campbell' |
| Vogler | Writer's Journey | 100k | 224 | 'vogler' |
| Field | Screenplay | 112k | 251 | 'field', 'dialogue' |
| Seger | Making Script Great | 82k | 184 | 'seger', 'dialogue' |
| Egri | Dramatic Writing | 96k | 214 | 'egri', 'dialogue' |
| Snyder | Save the Cat | 61k | 112 | 'snyder' |
| Cowgill | Short Films | 75k | 169 | 'cowgill', 'dialogue' |
| Aristotle | Poetics | 67k | 151 | 'aristotle' |
| Weiland | Character Arcs | 51k | 114 | 'weiland' |

**Mapeamento ENRIQUECIDO:**
```python
# NOVIDADE: 'dialogue' carrega 7 livros (vs 1 antes)
'dialogue': [
    McKee Dialogue (100.0 score, 1031 menções),
    Cowgill (69.3 score, 524 menções),
    Truby (59.0 score, 748 menções),
    Field (35.4 score),
    Seger (31.2 score),
    McKee Story (26.3 score),
    Egri (21.6 score)
]
# Total: 1,575 chunks (810% increase!)
```

**Modos de busca:**

**SHALLOW Mode (padrão):**
```python
indexer.search_for_problems(problems_list)
# - BM25 search nos chunks
# - Retorna top N mais relevantes (~15-20 chunks)
# - Rápido (~2-5s)
# - Consome menos tokens (~10-20k)
```

**DEEP Mode (multi-autor):**
```python
indexer.get_full_book_context(specialist_type)
# - Retorna livro completo
# - ~128k tokens
# - Lento (~4-5min por autor no LLM)
# - Análise mais profunda
```

---

#### 4. **LLM CORE (Ollama)**

**O que faz:** Análise qualitativa usando teoria + exemplo Python

**Modelo:** `scripturemon-optimized` (customizado)
**Engine:** Ollama CLI via subprocess
**Timeout:** 900s (15min) para deep context

**Prompt Structure:**
```xml
<contexto>
  Você é crítico profissional de roteiros.
  Analise baseando-se em teoria de screenwriting.
</contexto>

<documento_fonte id="livro_dialogue">
  [Livro completo ou chunks relevantes]
</documento_fonte>

<screenplay_excerpt>
  [Trecho do roteiro]
</screenplay_excerpt>

<python_analysis>
  Score: 85.0
  Violations: [...]
  Recommendations: [...]
</python_analysis>

<instrucoes>
1. INTERPRETAÇÃO: O que a análise Python revela?
2. PADRÕES: Que padrões você vê?
3. PROBLEMAS: Identifique issues além do Python
4. SOLUÇÕES: Como resolver usando teoria?
5. PROFUNDIDADE: Insights únicos da teoria
</instrucoes>
```

**Output Esperado:**
```
1. INTERPRETAÇÃO
[Análise interpretativa dos dados Python]

2. PADRÕES
[Padrões identificados no roteiro]

3. PROBLEMAS
[Problemas além dos detectados por Python]

4. SOLUÇÕES
[Soluções baseadas na teoria carregada]

5. PROFUNDIDADE & SÍNTESE
[Insights únicos conectando teoria + prática]
```

---

#### 5. **FORMATTED EXPORTER (Gerador HTML/TXT)**

**O que faz:** Gera relatórios profissionais formatados

**Path:** `triple_core/exporters/formatted_exporter.py`

**Formatos:**
- **HTML:** CSS moderno, gradients, interativo
- **TXT:** 80 colunas, plain text para LLMs

**Estrutura HTML:**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* CSS profissional: gradients, shadows, hover */
    body { font-family: -apple-system; }
    .metric { font-size: 2em; color: #2563eb; }
    .llm-insights { background: linear-gradient(...); }
  </style>
</head>
<body>
  <h1>SCRIPTUREMON - ANÁLISE DUAL-CORE</h1>

  <!-- PARTE 1: ANÁLISE PYTHON -->
  <div class="python-core">
    <h2>CORE 1: ANÁLISE PYTHON (OBJETIVA)</h2>
    <div class="metric">Score: 85.0/100</div>
    <div class="violations">
      <h3>⚠️ REGRAS VIOLADAS</h3>
      [Lista de violations com severity]
    </div>
    <div class="recommendations">
      <h3>💡 RECOMENDAÇÕES</h3>
      [Lista de fixes práticos]
    </div>
  </div>

  <!-- PARTE 2: INSIGHTS LLM -->
  <div class="llm-insights">
    <h2>CORE 2: INSIGHTS LLM (QUALITATIVA)</h2>
    <div class="section">
      <div class="insight-header">1. INTERPRETAÇÃO</div>
      <p>[Análise interpretativa]</p>
    </div>
    <div class="section">
      <div class="insight-header">2. PADRÕES</div>
      <p>[Padrões identificados]</p>
    </div>
    <div class="section">
      <div class="insight-header">3. PROBLEMAS</div>
      <p>[Problemas detectados]</p>
    </div>
    <div class="section">
      <div class="insight-header">4. SOLUÇÕES</div>
      <p>[Soluções propostas]</p>
    </div>
    <div class="section">
      <div class="insight-header">5. PROFUNDIDADE & SÍNTESE</div>
      <p>[Insights únicos]</p>
    </div>
  </div>

  <!-- PARTE 3: SÍNTESE -->
  <div class="synthesis">
    <h2>SÍNTESE (PYTHON + LLM)</h2>
    <p>[Resumo executivo combinando ambos]</p>
  </div>
</body>
</html>
```

**Feature especial:** Remove códigos técnicos (DIAL.R003, STRUCT.R001) do HTML para leitura humana, mas mantém no TXT para processamento por outras IAs.

---

## 🎬 SEÇÃO 3: CASOS DE USO

### CASO 1: Análise Multi-Autor (13 perspectivas)

**Quando usar:** Quer feedback de múltiplos autores de teoria

**Script:** `analyze_sonhos_multi_author.py`

**Como rodar:**
```bash
python3 analyze_sonhos_multi_author.py
```

**O que faz:**
```
1. Cria pasta organizada: ROTEIRO_dialogue_0001/
   ├── 1_individuais/  (13 HTMLs, 1 por autor)
   ├── 2_logs/         (execution logs)
   └── 3_consolidados/ (1 HTML traduzido)

2. Para cada autor (13 total):
   - DrDialogue analisa roteiro (Python)
   - DualCoreWrapper carrega livro do autor (~128k tokens)
   - Ollama LLM analisa com deep context (4-5min)
   - Exporta HTML individual

3. Consolida 13 HTMLs em 1:
   - Detecta análises em inglês
   - Traduz via LLM para português
   - Gera HTML final consolidado

4. Output:
   - 13 análises individuais (nativas)
   - 1 análise consolidada (PT traduzida)
   - Logs de execução
   - README explicativo
```

**Tempo:** ~57 minutos (13 × 4.4min)
**Output:** ~67KB HTML consolidado

**Configuração:**
```python
AUTHORS = [
    'aristotle', 'campbell', 'cowgill', 'dialogue',
    'egri', 'field', 'mckee', 'mckee_character',
    'mckee_dialogue', 'seger', 'snyder', 'truby', 'vogler'
]

# Para cada autor:
wrapper = DualCoreWrapper(
    python_specialist=DrDialogue(),
    specialist_type=AUTOR,  # Define qual livro carregar
    deep_context=True,      # Livro completo!
    llm_timeout=900
)
```

---

### CASO 2: Análise Completa (22 Specialists)

**Quando usar:** Quer análise profissional completa do roteiro

**Script:** `ScreenplayAnalyzer`

**Como rodar:**
```python
from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer

analyzer = ScreenplayAnalyzer(
    llm_model='scripturemon-optimized',
    deep_context=False  # Usa SHALLOW para velocidade
)

result = analyzer.analyze_screenplay(
    screenplay_path='path/to/screenplay.txt',
    output_dir='workspace/outputs/analysis'
)

print(f"Overall Score: {result['overall_score']}/100")
print(f"Level: {result['overall_level']}")  # amateur, developing, competent, good, excellent, masterful
```

**O que faz:**
```
1. Executa TODOS os 22 specialists:
   - Dialogue, Structure, Pacing, Character, etc
   - Cada um gera análise Dual-Core (Python + LLM)

2. Agrega resultados:
   - Overall Score (0-100)
   - 7 dimensões (narrative, character, dialogue, technical, depth, craft, market)
   - Strengths/Weaknesses
   - Recommendations priorizadas

3. Gera relatórios:
   - HTML report (visual, interativo)
   - Markdown report (técnico, detalhado)
   - Executive summary (decisores)
```

**Tempo:** ~26 minutos (22 × ~70s)
**Output:** Relatório completo multi-dimensional

---

### CASO 3: Análise Single Specialist

**Quando usar:** Quer feedback específico (ex: só dialogue)

**Como rodar:**
```python
from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

# Criar specialist
specialist = DrDialogue()

# Criar wrapper
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    specialist_type='dialogue',  # Carrega 7 livros!
    deep_context=True,           # ou False para velocidade
    llm_model='scripturemon-optimized'
)

# Analisar
result = wrapper.analyze(screenplay_text)

# Exportar
html_path = wrapper.export_formatted(
    result,
    screenplay_title="MEU_ROTEIRO",
    format="html"
)
```

**Tempo:** ~4-5 minutos (deep) ou ~1-2min (shallow)
**Output:** 1 HTML com análise Dual-Core

---

## 🔧 SEÇÃO 4: REFERÊNCIA RÁPIDA - DECISÕES COMUNS

### Decisão 1: Deep Context vs Shallow?

| Critério | SHALLOW | DEEP |
|----------|---------|------|
| **Velocidade** | ✅ Rápido (1-2min) | ❌ Lento (4-5min) |
| **Tokens LLM** | ✅ Poucos (~15k) | ❌ Muitos (~128k) |
| **Qualidade** | ⚠️ Boa | ✅ Excelente |
| **Quando usar** | Iteração rápida, feedback inicial | Análise final, multi-autor |
| **Custo** | ✅ Baixo | ❌ Alto |

**Recomendação:**
- **Desenvolvimento:** Shallow (iterar rápido)
- **Final:** Deep (máxima qualidade)
- **Multi-autor:** Sempre Deep (objetivo é profundidade)

---

### Decisão 2: Qual specialist_type usar?

| specialist_type | Livros Carregados | Quando Usar |
|-----------------|-------------------|-------------|
| `'dialogue'` | 7 livros (McKee, Cowgill, Truby, Field, Seger, Egri) | **Análise de diálogo enriquecida** |
| `'mckee_dialogue'` | 1 livro (McKee Dialogue) | Perspectiva única de McKee |
| `'truby'` | 1 livro (Truby) | Perspectiva única de Truby |
| `'aristotle'` | 1 livro (Poetics) | Perspectiva clássica |
| ... | ... | ... |

**Recomendação:**
- **Multi-perspectiva:** Use `'dialogue'` (7 livros!)
- **Autor específico:** Use `'mckee'`, `'truby'`, etc
- **Multi-autor:** Loop pelos 13 autores individuais

---

### Decisão 3: Single Specialist vs 22 Specialists?

| Aspecto | SINGLE | FULL (22) |
|---------|--------|-----------|
| **Tempo** | ~4-5min | ~26min |
| **Foco** | ✅ Específico (ex: só dialogue) | ✅ Completo (todas dimensões) |
| **Overall Score** | ❌ Não gera | ✅ Gera (0-100) |
| **Quando usar** | Feedback pontual, debug específico | Análise profissional completa |

**Recomendação:**
- **Debugging:** Single (ex: só dialogue está ruim)
- **Profissional:** Full 22 (cliente, produtor, pitch)

---

### Decisão 4: Tradução automática?

**Quando ativar:**
```python
consolidate_html_analyses(
    pattern='ANALISE_*.html',
    translate=True  # ← Ativar se quiser PT
)
```

**O que faz:**
1. Detecta HTMLs em inglês (30+ indicators)
2. Traduz via Ollama LLM
3. Preserva formatação HTML
4. Fallback para substituição simples se LLM falhar

**Quando usar:**
- ✅ Roteiros em PT para clientes BR
- ✅ Autores escrevem em inglês mas análise tem que ser PT
- ❌ Se análise já está em PT (não precisa)

---

## 📚 SEÇÃO 5: LINKS PARA DETALHES TÉCNICOS

### Documentação Completa

1. **📚 Catálogo Completo:** `/Users/clubproducoes/Digimundo/claude_code/📚CATALOGO_COMPLETO_ARQUITETURA.md`
   - Todos os 34 arquivos detalhados
   - Linhas de código, imports, métodos
   - Status de duplicação
   - Bug fixes aplicados

2. **🔥 Arquivos Análise Multi-Autor:** `/Users/clubproducoes/Digimundo/claude_code/MEMORY/conhecimentos/🔥🔥🔥ARQUIVOS_ANALISE_MULTI_AUTOR🔥🔥🔥.md`
   - 34 arquivos usados na análise
   - Fluxo completo end-to-end
   - Chain of execution
   - Estatísticas detalhadas

### Arquivos-Chave

**Scripts Principais:**
- `analyze_sonhos_multi_author.py` - Multi-autor orchestrator
- `consolidate_analyses.py` - Consolidador com tradução

**Componentes Core:**
- `triple_core/core_1_specialists/dialogue/dr_dialogue.py` - Specialist
- `triple_core/orchestrators/dual_core_wrapper.py` - Wrapper
- `core/theory_indexer.py` - Theory loader
- `triple_core/exporters/formatted_exporter.py` - HTML/TXT generator

**Regras:**
- `specialists/rules/character_dialogue_rules.yaml` - 15 regras dialogue

**Teoria:**
- `content/theory/*.txt` - 13 livros (1.2M palavras)

---

## 🚀 QUICK START - 3 COMANDOS

### 1. Análise Multi-Autor (13 perspectivas)
```bash
cd /Users/clubproducoes/Digimundo/scripturemon-clean
python3 analyze_sonhos_multi_author.py
# Tempo: ~57min
# Output: workspace/outputs/ROTEIRO_dialogue_0001/
```

### 2. Análise Completa (22 specialists)
```python
from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer

analyzer = ScreenplayAnalyzer()
result = analyzer.analyze_screenplay('screenplay.txt')
# Tempo: ~26min
# Output: HTML + Markdown reports
```

### 3. Análise Single (rápida)
```python
from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

wrapper = DualCoreWrapper(DrDialogue(), specialist_type='dialogue')
result = wrapper.analyze(screenplay_text)
wrapper.export_formatted(result, "TEST", "html")
# Tempo: ~4min (deep) ou ~1min (shallow)
```

---

## ⚠️ TROUBLESHOOTING COMUM

### Problema 1: "Ollama not found"
```bash
# Solução: Instalar Ollama
brew install ollama

# Verificar modelo
ollama list | grep scripturemon
```

### Problema 2: "Timeout error"
```python
# Solução: Aumentar timeout
wrapper = DualCoreWrapper(
    ...,
    llm_timeout=1200  # 20min em vez de 15min
)
```

### Problema 3: "Theory not found"
```python
# Solução: Verificar path
from pathlib import Path
theory_dir = Path('content/theory')
print(list(theory_dir.glob('*.txt')))  # Deve mostrar 13 arquivos
```

### Problema 4: "Score sempre 90.0"
```
# Causa: Nenhuma violation detectada (base score)
# Solução: Normal se roteiro está bom!
# Score varia: 5-95 (nunca 0 ou 100)
```

---

## 📊 GLOSSÁRIO

| Termo | Significado |
|-------|-------------|
| **Core 1** | Análise Python objetiva (métricas) |
| **Core 2** | Análise LLM qualitativa (insights) ou ExampleFinder |
| **Core 3** | LLM final (só em Triple-Core completo) |
| **Dual-Core** | Sistema Python + LLM (2 cores) |
| **Triple-Core** | Sistema Python + Examples + LLM (3 cores) |
| **Specialist** | Módulo Python que analisa 1 aspecto (ex: DrDialogue) |
| **Wrapper** | Componente que integra Specialist + LLM |
| **Deep Context** | Modo que carrega livro completo (~128k tokens) |
| **Shallow Context** | Modo que carrega só chunks relevantes (~15-20 chunks) |
| **Theory Indexer** | Componente que carrega livros de teoria |
| **specialist_type** | String que define qual livro carregar ('dialogue', 'truby', etc) |
| **Enriquecimento** | Mapping de 1 tipo para N livros (ex: 'dialogue' → 7 livros) |
| **BM25** | Algoritmo de busca textual (ranking) |
| **Violation** | Regra quebrada no roteiro |
| **Severity** | Gravidade (critical, high, medium, low) |
| **Chunk** | Pedaço de livro (~450 palavras) |

---

## 🎯 RESUMO: 1 MINUTO

**O QUE É:** Sistema de análise de roteiros com Python + Teoria + LLM

**COMPONENTES:**
- 22 Specialists Python (análise objetiva)
- 13 Livros de teoria (McKee, Truby, Campbell, etc)
- Ollama LLM (análise qualitativa)
- HTML/TXT formatado (output)

**CASOS DE USO:**
1. **Multi-Autor:** 13 perspectivas, deep context, 57min
2. **Completo:** 22 specialists, overall score, 26min
3. **Single:** 1 specialist, rápido, 4min

**DECISÕES-CHAVE:**
- Deep vs Shallow? → Deep = melhor, Shallow = rápido
- Single vs Full? → Single = debug, Full = profissional
- specialist_type? → 'dialogue' = 7 livros, outros = 1 livro

**OUTPUTS:**
- HTML profissional (CSS moderno)
- Markdown técnico
- Overall Score 0-100
- Problemas + Soluções

---

**ÚLTIMA ATUALIZAÇÃO:** 2025-10-05
**VERSÃO:** 2.0 (Master Index)
**PRÓXIMOS PASSOS:** Ver documentação completa nos links acima

**DIGIMUNDO PRESENTE 🥷**
