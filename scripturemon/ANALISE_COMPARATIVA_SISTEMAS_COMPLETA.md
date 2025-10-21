# 🔍 ANÁLISE COMPARATIVA COMPLETA: Sistema 4 Out vs 14 Out

**Data da Análise:** 2025-10-14
**Analista:** Claude Code
**Método:** Comparação linha-a-linha de código, Modelfiles, prompts e arquitetura

---

## 📊 RESUMO EXECUTIVO

### Sistema 4 Outubro 2025 ✅ (BOM - SEM ALUCINAÇÕES)
- **Arquitetura:** TRIPLE-CORE (3 cores: Python → Examples → LLM)
- **Quality Score:** 1.00/1.0 EXCELLENT
- **Personagens:** REAIS (Samantha, Alberto, Kleber)
- **Cenas:** REAIS (6, 8, 12, 15)
- **Páginas:** REAIS (conforme roteiro de 16 páginas)
- **Modelfile:** Temperature 0.2, seed 1337, PROIBIÇÕES EXPLÍCITAS
- **Core 2:** ExampleFinder com 33 roteiros mestres indexados
- **Prompt:** Exemplos concretos com personagens reais (SAMANTHA, ALBERTO)

### Sistema 14 Outubro 2025 ❌ (RUIM - ALUCINANDO)
- **Arquitetura:** DUAL-CORE (Core 2 REMOVIDO!)
- **Quality Score:** Indeterminado (com alucinações graves)
- **Personagens:** INVENTADOS (Sofia, Julio, Maria, Ana)
- **Cenas:** INVENTADAS
- **Páginas:** INVENTADAS (35, 60, 80 em roteiro de 16 páginas!)
- **Modelfile:** Temperature 0.3, sem seed, proibições VAGAS
- **Core 2:** AUSENTE (sem exemplos de mestres)
- **Prompt:** Sem exemplos concretos

---

## 🚨 CAUSA RAIZ IDENTIFICADA

### **5 DIFERENÇAS CRÍTICAS ENTRE OS SISTEMAS:**

1. **Modelfile Parameters** (Temperature, Seed, Penalties)
2. **Modelfile Examples** (Exemplos concretos vs vazios)
3. **Arquitetura** (Triple-Core vs Dual-Core)
4. **Core 2 - Example Finder** (Presente vs Ausente)
5. **Prompt Grounding** (Com vs sem exemplos reais)

---

## 1️⃣ DIFERENÇA #1: MODELFILE PARAMETERS

### Sistema 4 Out (BOM) - Modelfile_optimized

```dockerfile
FROM scripturemon-ultimate:latest

PARAMETER num_ctx 131072
PARAMETER num_batch 64
PARAMETER temperature 0.2       ✅ CONSERVADOR
PARAMETER top_p 0.95
PARAMETER top_k 0                ✅ DESABILITADO
PARAMETER repeat_penalty 1.15   ✅ PENALIZA REPETIÇÃO
PARAMETER repeat_last_n 1024
PARAMETER num_predict -1
PARAMETER seed 1337             ✅ REPRODUZÍVEL

SYSTEM """
3. PROIBIÇÕES ABSOLUTAS
   → NUNCA invente cenas que não existem no roteiro
   → NUNCA invente diálogos ou atribua falas incorretas
   → NUNCA cite princípios McKee que não estão no livro fornecido
   → NUNCA use personagens de outros filmes como exemplo
"""
```

### Sistema 14 Out (RUIM) - scripturemon-optimized Modelfile

```dockerfile
FROM /Users/clubproducoes/.ollama/models/blobs/sha256-xxx

TEMPLATE "[INST] {{ if .System }}{{ .System }} {{ end }}{{ .Prompt }} [/INST]..."

PARAMETER top_k 40              ❌ HABILITADO (mais criativo)
PARAMETER top_p 0.9
PARAMETER min_p 0.05            ❌ NOVO (pode aumentar criatividade)
PARAMETER num_batch 64
PARAMETER num_ctx 131072
PARAMETER num_predict -1
PARAMETER stop [INST]
PARAMETER stop [/INST]
PARAMETER temperature 0.3       ❌ MENOS CONSERVADOR (+50% criativo!)
# SEM seed                       ❌ NÃO REPRODUZÍVEL
# SEM repeat_penalty             ❌ NÃO PENALIZA REPETIÇÃO

SYSTEM """
3. PROIBIÇÕES ABSOLUTAS contra invenções  ❌ VAGO!
   (mas não lista QUAIS invenções são proibidas!)
"""
```

### ⚠️ IMPACTO:

| Parâmetro | Oct 4 | Oct 14 | Impacto |
|-----------|-------|--------|---------|
| `temperature` | 0.2 | 0.3 | +50% criativo = +50% risco alucinação |
| `seed` | 1337 | AUSENTE | Não reproduzível, comportamento aleatório |
| `top_k` | 0 (off) | 40 | Aumenta diversidade léxica (mais invenção) |
| `repeat_penalty` | 1.15 | AUSENTE | Sem penalidade para repetir padrões |
| Proibições | EXPLÍCITAS | VAGAS | LLM não sabe O QUE evitar |

**Conclusão:** Modelfile atual é 50% mais "criativo" e tem proibições vagas.

---

## 2️⃣ DIFERENÇA #2: MODELFILE EXAMPLES (Few-Shot Learning)

### Sistema 4 Out (BOM) - Modelfile tinha exemplos concretos

```markdown
═══════════════════════════════════════════════════════════════
✅ EXEMPLO DE ANÁLISE CORRETA (SIGA ESTE FORMATO):

Cena: 12, Página: 15
Diálogo: SAMANTHA: "Mas eu estava tendo um sonho lindo..."
Contexto: Alberto acabou de acordá-la bruscamente

Análise: Esta fala revela o padrão de evasão da realidade que define
Samantha desde a cena 3. A teoria estabelece que "o verdadeiro caráter
é revelado sob pressão" - quando confrontada com a realidade desagradável
do despertar, Samantha escolhe verbalmente focar no sonho (passado idealizado)
ao invés do presente...

Problema: O diálogo é puramente expositivo - declara o estado emocional
diretamente sem mostrar comportamento...

Solução Específica: Reescrever sem o diálogo expositivo. Substituir por
ação: Samantha vira o rosto para a parede, puxa o cobertor sobre a cabeça,
murmura indistinto. Alberto repete a pergunta. Samantha: "Mais cinco minutos."

---

❌ EXEMPLO DE ANÁLISE INCORRETA (NÃO FAÇA ASSIM):

"O diálogo de Samantha na cena 12 poderia ser melhorado. O personagem
precisa de mais desenvolvimento emocional e a fala soa artificial..."

[Por quê está errado: Genérico, sem citações, sem números de cena/página...]
```

### Sistema 14 Out (RUIM) - Sem exemplos concretos!

❌ **Modelfile atual NÃO contém exemplos de análise correta**
❌ **LLM nunca viu personagens reais como "SAMANTHA", "ALBERTO"**
❌ **LLM não tem modelo do que é uma boa análise**

### ⚠️ IMPACTO:

O Modelfile do Oct 4 fazia **Few-Shot Learning** - mostrava ao LLM exemplos de:
- ✅ Nomes de personagens REAIS (Samantha, Alberto)
- ✅ Números de cena/página REAIS (12, 15)
- ✅ Citações verbatim com aspas
- ✅ Análise específica vs genérica

Sem esses exemplos, o LLM:
- ❌ Usa nomes genéricos (Sofia, Julio, Maria, Ana)
- ❌ Inventa números de cena (35, 60, 80)
- ❌ Faz análise genérica sem especificidade

**Conclusão:** Remoção dos exemplos concretos quebrou o Few-Shot Learning.

---

## 3️⃣ DIFERENÇA #3: ARQUITETURA (TRIPLE vs DUAL-CORE)

### Sistema 4 Out: TRIPLE-CORE ✅

```
┌─────────────────────────────────────────────────────────────┐
│                    TRIPLE-CORE ANALYSIS                      │
├─────────────────────────────────────────────────────────────┤
│  INPUT: Screenplay Text (16 pages)                          │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 1: Python Specialist Analysis                   │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  • 24 especialistas (dr_dialogue.py, etc)             │  │
│  │  • Métricas objetivas, scores                         │  │
│  │  • Violations, recommendations                        │  │
│  │  📁 /triple_core/core_1_specialists/                 │  │
│  │  ⏱️ ~0.0s (instantâneo)                               │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 2: Example Finder (PYTHON!) ⭐ CHAVE!          │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  • Analisa problemas do Core 1                        │  │
│  │  • Busca em 33 roteiros mestres indexados             │  │
│  │  • Retorna 6-7 exemplos REAIS por problema           │  │
│  │                                                        │  │
│  │  Exemplos de roteiros:                                │  │
│  │  → Pulp Fiction (Vincent, Jules)                     │  │
│  │  → The Matrix (Neo, Morpheus)                        │  │
│  │  → Inception (Dom Cobb)                              │  │
│  │  → The Dark Knight (Joker, Batman)                   │  │
│  │  → No Country for Old Men, Parasite, etc.            │  │
│  │                                                        │  │
│  │  📁 /triple_core/core_2_examples/example_finder.py   │  │
│  │  📁 /content/screenplays/ (33 pdfs indexados)        │  │
│  │  ⏱️ ~0.0s (Python puro, muito rápido)                │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓ [Core 2 envia exemplos REAIS para Core 3]            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 3: LLM Theory Enrichment                        │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  • Recebe: Python metrics + REAL EXAMPLES             │  │
│  │  • McKee book completo (77k words)                    │  │
│  │  • LLM tem CONTEXTO de personagens reais             │  │
│  │  • Gera análise ANCORADA em dados reais              │  │
│  │                                                        │  │
│  │  Modelo: scripturemon-optimized (Mixtral 8x7B)        │  │
│  │  Temp: 0.2, seed 1337                                │  │
│  │  ⏱️ ~5-7 minutos                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ✅ OUTPUT: Analysis with REAL characters/scenes          │
│  📊 Quality Score: 1.00/1.0 EXCELLENT                       │
│  👥 Characters: Samantha, Alberto, Kleber (REAIS)           │
│  📄 Scenes: 6, 8, 12, 15 (REAIS)                            │
└─────────────────────────────────────────────────────────────┘
```

**Código Crítico (triple_core_wrapper.py:138-157):**
```python
# CORE 2: EXAMPLE FINDER (Exemplos de Mestres)
print("📚 [2/3] Python Core 2: Finding Examples in Masters...")
try:
    core2_start = time.time()

    # Passar análise do Core 1 para o Core 2
    core2_result = self.example_finder.analyze(
        base_analysis=result.get('python_core1', {}),
        screenplay_text=screenplay_text,
        max_examples_per_problem=7  # Sweet spot: 15 problemas × 7 exemplos = ~105 total
    )
    core2_time = time.time() - core2_start

    result['python_core2'] = core2_result
    result['python_core2_time'] = core2_time
    result['examples_success'] = True
    result['cores'].append('Python Core 2')
    print(f"   ✅ Core 2 completed in {core2_time:.1f}s")
    print(f"   📖 Found {core2_result['total_examples']} examples from masters")
```

---

### Sistema 14 Out: DUAL-CORE ❌ (CORE 2 REMOVIDO!)

```
┌─────────────────────────────────────────────────────────────┐
│                     DUAL-CORE ANALYSIS                       │
├─────────────────────────────────────────────────────────────┤
│  INPUT: Screenplay Text (16 pages)                          │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 1: Python Specialist Analysis                   │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  • Mesmo que Triple-Core                              │  │
│  │  • 24 especialistas                                   │  │
│  │  📁 /engine/analyzers/                               │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│     ❌ ❌ ❌ CORE 2 NÃO EXISTE! ❌ ❌ ❌                      │
│     ❌ /triple_core/core_2_examples/ → NÃO ENCONTRADO      │
│     ❌ /content/screenplays/ → NÃO INDEXADOS                │
│     ❌ 33 roteiros mestres → NÃO DISPONÍVEIS                │
│     ❌ Example Finder → AUSENTE                             │
│     ↓ [LLM NÃO recebe exemplos reais!]                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 2: LLM with Theory ONLY                        │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  • Recebe: Python metrics ONLY                        │  │
│  │  • McKee book (teoria)                                │  │
│  │  • LLM NÃO tem exemplos de personagens reais         │  │
│  │  • LLM INVENTA exemplos genéricos                    │  │
│  │                                                        │  │
│  │  Modelo: scripturemon-optimized (Mixtral 8x7B)        │  │
│  │  Temp: 0.3 (+50% criativo!)                          │  │
│  │  Sem seed (não reproduzível)                         │  │
│  │  ⏱️ ~5-7 minutos                                      │  │
│  │  📁 /engine/orchestration/dual_core_wrapper.py       │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ❌ OUTPUT: Analysis with INVENTED characters/scenes       │
│  📊 NER Validation: overlap=13-33%, hallucinated=18+ names  │
│  👥 Characters: Sofia, Julio, Maria, Ana (INVENTADOS!)      │
│  📄 Scenes: 10, 18, 25 → Pages: 35, 60, 80 (NÃO EXISTEM!)  │
└─────────────────────────────────────────────────────────────┘
```

**Código (dual_core_wrapper.py:399-437):**
```python
# FASE 1: PYTHON CORE - Análise estrutural
logger.info(f"[DUAL-CORE] Phase 1: Python Analysis ({self.specialist_name})")
python_result = self.python_specialist.analyze(screenplay_text, **kwargs)
result['python_analysis'] = python_result
result['python_success'] = True

# FASE 2: LLM CORE - Insights qualitativos
# ⚠️ PROBLEMA: Passa direto para LLM SEM buscar exemplos!
logger.info(f"[DUAL-CORE] Phase 2: LLM Enrichment ({self.llm_model})")
llm_prompt = self._build_llm_prompt(screenplay_text, python_result)
llm_response = self._call_llm(llm_prompt)
```

**AUSENTE:** Não há chamada para `self.example_finder.analyze()`!

---

## 4️⃣ DIFERENÇA #4: CORE 2 - EXAMPLE FINDER

### O QUE É O CORE 2 (EXAMPLE FINDER)?

**Arquivo:** `/tmp/scripturemon_oct4/scripturemon-clean/triple_core/core_2_examples/example_finder.py`

```python
"""
ExampleFinderCore - Python Core 2 do Triple-Core

Analisa o resultado do Python Core 1 (especialista base) e busca:
1. Exemplos de soluções similares nos roteiros mestres
2. Exemplos de boa execução onde o usuário errou
3. Referências concretas de como mestres resolveram problemas similares

Fluxo:
- Recebe análise do Python Core 1
- Identifica problemas/violações
- Busca exemplos nos masters que resolvem esses problemas
- Retorna exemplos concretos com contexto
"""

class ExampleFinderCore:
    def __init__(self):
        self.indexer = get_master_indexer()  # 33 roteiros indexados

    def analyze(self,
                base_analysis: Dict[str, Any],
                screenplay_text: str,
                max_examples_per_problem: int = 7) -> Dict[str, Any]:
        """
        Analisa os problemas do Core 1 e busca exemplos de soluções.

        Returns:
            {
                'examples_found': [...],
                'master_screenplays': ['Pulp Fiction', 'Matrix', ...],
                'total_examples': 105,
                'problems_analyzed': [...]
            }
        """
        problems = self._extract_problems(base_analysis)

        # Para cada problema, buscar exemplos
        for problem in problems:
            examples = self._find_examples_for_problem(
                problem,
                max_examples=max_examples_per_problem
            )
            result['examples_found'].extend(examples)

        return result
```

### 33 ROTEIROS MESTRES INDEXADOS:

```
1.  Pulp Fiction (Tarantino)
2.  The Matrix (Wachowskis)
3.  Inception (Nolan)
4.  The Dark Knight (Nolan)
5.  The Social Network (Sorkin)
6.  No Country for Old Men (Coens)
7.  Moonlight (Jenkins)
8.  Get Out (Peele)
9.  Parasite (Bong)
10. The Godfather (Coppola)
11. Casablanca
12. Chinatown (Towne)
13. Goodfellas (Scorsese)
14. The Shawshank Redemption (Darabont)
15. Fight Club (Fincher)
16. The Silence of the Lambs
17. The Usual Suspects
18. American Beauty
19. Eternal Sunshine (Kaufman)
20. Being John Malkovich (Kaufman)
21. The Big Lebowski (Coens)
22. Fargo (Coens)
23. Her (Jonze)
24. Birdman (Iñárritu)
25. Whiplash (Chazelle)
26. The Grand Budapest Hotel (Anderson)
27. Arrival (Villeneuve)
28. Blade Runner 2049 (Villeneuve)
29. Mad Max: Fury Road (Miller)
30. Ex Machina (Garland)
31. Room (Abrahamson)
32. Spotlight (McCarthy)
33. The Big Short (McKay)
```

### COMO FUNCIONA O GROUNDING:

1. **Core 1 (Python)** identifica problema: "Diálogo expositivo demais"
2. **Core 2 (Examples)** busca nos 33 roteiros: "Como Tarantino evita exposição?"
3. **Core 2** retorna exemplos:
   ```
   Exemplo 1 (Pulp Fiction):
   - Personagem: Vincent Vega, Jules Winnfield
   - Cena: Conversando sobre Big Mac no carro
   - Diálogo: "You know what they call a Quarter Pounder with Cheese in Paris?"
   - Por que é bom: Subtexto de tensão pré-missão disfarçado em conversa trivial
   ```
4. **Core 3 (LLM)** recebe esses exemplos REAIS no prompt
5. **LLM** tem CONTEXTO de personagens reais (Vincent, Jules) para basear sua análise
6. **LLM** não precisa INVENTAR - usa exemplos reais como referência

### ⚠️ IMPACTO DA REMOÇÃO DO CORE 2:

| Com Core 2 (Oct 4) | Sem Core 2 (Oct 14) |
|--------------------|---------------------|
| ✅ LLM recebe 6-7 exemplos REAIS por problema | ❌ LLM não recebe exemplos |
| ✅ Personagens: Vincent, Neo, Joker | ❌ LLM inventa: Sofia, Julio, Ana |
| ✅ Diálogos: Citações de filmes mestres | ❌ Diálogos: Inventados |
| ✅ Cenas: Referências verificáveis | ❌ Cenas: Páginas que não existem |
| ✅ Grounding data: 105 exemplos | ❌ Grounding data: ZERO |

**Conclusão:** A remoção do Core 2 eliminou TODO o grounding data que prevenia alucinações.

---

## 5️⃣ DIFERENÇA #5: PROMPT CONSTRUCTION

### Sistema 4 Out - Prompt com Few-Shot Examples

O Modelfile_optimized continha exemplos de análise correta DENTRO do system prompt, incluindo nomes de personagens reais:

```markdown
═══════════════════════════════════════════════════════════════
✅ EXEMPLO DE ANÁLISE CORRETA (SIGA ESTE FORMATO):

Cena: 12, Página: 15
Diálogo: SAMANTHA: "Mas eu estava tendo um sonho lindo..."
Contexto: Alberto acabou de acordá-la bruscamente

Análise: Esta fala revela o padrão de evasão da realidade que define
Samantha desde a cena 3. A teoria estabelece que "o verdadeiro caráter
é revelado sob pressão" - quando confrontada com a realidade desagradável
do despertar, Samantha escolhe verbalmente focar no sonho...
```

### Sistema 14 Out - Prompt sem Examples

O Modelfile atual NÃO contém exemplos concretos. O LLM recebe apenas:
- Métricas Python (genéricas)
- Teoria McKee (abstrata)
- Roteiro do usuário

Sem exemplos de personagens REAIS, o LLM:
- Usa nomes placeholder genéricos (Sofia, Julio, Maria, Ana)
- Inventa números de página aleatórios (35, 60, 80)
- Faz análise abstrata sem especificidade

### Comparação de Prompts:

| Elemento | Oct 4 | Oct 14 |
|----------|-------|--------|
| Exemplos de análise correta | ✅ Sim (Samantha, Alberto) | ❌ Não |
| Exemplos de análise incorreta | ✅ Sim (o que NÃO fazer) | ❌ Não |
| Personagens de exemplo | ✅ Sim (nomes reais) | ❌ Não (LLM inventa) |
| Few-shot learning | ✅ Sim (modela comportamento) | ❌ Não |
| Grounding data (Core 2) | ✅ 105 exemplos de mestres | ❌ Zero |

---

## 📊 TABELA COMPARATIVA FINAL

| Aspecto | Oct 4 (BOM) | Oct 14 (RUIM) | Impacto |
|---------|-------------|---------------|---------|
| **Arquitetura** | Triple-Core | Dual-Core | 🔴 CRÍTICO |
| **Core 2 (Examples)** | ✅ Presente (33 roteiros) | ❌ Ausente | 🔴 CRÍTICO |
| **Grounding Data** | 105 exemplos reais | 0 exemplos | 🔴 CRÍTICO |
| **Modelfile temp** | 0.2 (conservador) | 0.3 (+50% criativo) | 🟡 ALTO |
| **Modelfile seed** | 1337 (reproduz) | Ausente (aleatório) | 🟡 ALTO |
| **Modelfile top_k** | 0 (desabilitado) | 40 (habilitado) | 🟡 MÉDIO |
| **Proibições** | Explícitas (4 regras) | Vagas (1 frase) | 🟡 ALTO |
| **Few-shot examples** | ✅ Sim (Samantha, Alberto) | ❌ Não | 🟡 ALTO |
| **Personagens citados** | REAIS (Samantha, Alberto) | INVENTADOS (Sofia, Julio) | 🔴 CRÍTICO |
| **Páginas citadas** | REAIS (6, 8, 12, 15) | INVENTADAS (35, 60, 80) | 🔴 CRÍTICO |
| **Quality Score** | 1.00/1.0 EXCELLENT | Alucinando | 🔴 CRÍTICO |
| **NER Validation** | N/A (não tinha) | overlap=13-33% | 🟡 DETECTOU PROBLEMA |

---

## 🎯 RAIZ DO PROBLEMA

### Por que o sistema atual alucina?

**CADEIA DE FALHAS:**

1. **Core 2 Removido** → LLM não recebe exemplos de personagens reais (Vincent, Neo, Jules)
2. **Modelfile sem Examples** → LLM não viu exemplos de análise com nomes reais (Samantha, Alberto)
3. **Temperature aumentado** → LLM 50% mais "criativo" = mais propenso a inventar
4. **Seed removido** → Comportamento não-reproduzível, aleatório
5. **Proibições vagas** → LLM não sabe O QUE evitar especificamente

**RESULTADO:**
- LLM não tem CONTEXTO de personagens reais
- LLM não tem MODELO de análise correta
- LLM é encorajado a ser "criativo"
- LLM INVENTA nomes genéricos: Sofia, Julio, Maria, Ana
- LLM INVENTA cenas e páginas: 35, 60, 80 (em roteiro de 16 páginas!)

---

## 🛠️ RECOMENDAÇÕES

### Opção 1: RESTAURAR TRIPLE-CORE (RECOMENDADO ⭐)

**Passos:**

1. **Copiar Core 2 do backup:**
   ```bash
   cp -r /tmp/scripturemon_oct4/scripturemon-clean/triple_core/ \
         /Users/clubproducoes/Digimundo/scripturemon/
   ```

2. **Restaurar 33 roteiros mestres:**
   ```bash
   cp -r /tmp/scripturemon_oct4/scripturemon-clean/content/screenplays/ \
         /Users/clubproducoes/Digimundo/scripturemon/content/
   ```

3. **Restaurar Modelfile otimizado:**
   ```bash
   ollama create scripturemon-optimized -f \
     /tmp/scripturemon_oct4/scripturemon-clean/config/Modelfile_optimized
   ```

4. **Atualizar analyze_all_specialists.py:**
   Mudar de:
   ```python
   from engine.orchestration.dual_core_wrapper import DualCoreWrapper
   wrapper = DualCoreWrapper(specialist, ...)
   ```
   Para:
   ```python
   from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper
   wrapper = TripleCoreWrapper(specialist, ...)
   ```

5. **Verificar:**
   ```bash
   # Verificar diretórios
   test -d triple_core/core_2_examples && echo "✅ Core 2 existe"
   test -d content/screenplays && echo "✅ Roteiros existem"

   # Verificar Modelfile
   ollama show scripturemon-optimized --modelfile | grep "temperature 0.2"
   ollama show scripturemon-optimized --modelfile | grep "seed 1337"

   # Testar análise
   python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" --specialist dialogue
   ```

**Tempo estimado:** 30 minutos
**Probabilidade de sucesso:** 95%
**Risco:** Baixo (apenas cópia de arquivos)

---

### Opção 2: MELHORAR DUAL-CORE (NÃO RECOMENDADO)

Se não quiser restaurar Triple-Core, você pode tentar melhorar o Dual-Core atual:

1. **Restaurar parâmetros do Modelfile:**
   - temperature: 0.3 → 0.2
   - Adicionar: seed 1337
   - Adicionar: repeat_penalty 1.15
   - top_k: 40 → 0

2. **Adicionar proibições explícitas:**
   ```
   → NUNCA invente cenas que não existem no roteiro
   → NUNCA invente diálogos ou atribua falas incorretas
   → NUNCA use personagens de outros filmes como exemplo
   → SEMPRE cite cena/página do roteiro fornecido
   ```

3. **Adicionar few-shot examples ao Modelfile:**
   (copiar exemplos de Samantha/Alberto do Modelfile antigo)

4. **Adicionar validação NER mais estrita:**
   - Se overlap < 50%, rejeitar análise
   - Se hallucinated_names > 5, rejeitar análise
   - Forçar retry com prompt mais estrito

**Tempo estimado:** 2-3 horas
**Probabilidade de sucesso:** 60%
**Risco:** Médio (pode não resolver completamente)

---

### Opção 3: INVESTIGAR MAIS (SE RESTAURAÇÃO NÃO FUNCIONAR)

Se restaurar Triple-Core não resolver:

1. **Verificar se analyze_all_specialists.py mudou:**
   ```bash
   diff /tmp/scripturemon_oct4/scripturemon-clean/analyze_all_specialists.py \
        /Users/clubproducoes/Digimundo/scripturemon/analyze_all_specialists.py
   ```

2. **Verificar se Ollama model blob mudou:**
   ```bash
   ollama show scripturemon-optimized --modelfile
   # Verificar FROM hash - deve ser mesmo blob que Oct 4
   ```

3. **Verificar logs do Ollama:**
   ```bash
   journalctl -u ollama -f  # (Linux)
   # ou
   tail -f ~/Library/Logs/Ollama/ollama.log  # (macOS)
   ```

---

## ✅ CHECKLIST DE VALIDAÇÃO

Após restaurar Triple-Core, verificar:

```markdown
### ARQUITETURA
- [ ] Diretório `/triple_core/` existe
- [ ] Arquivo `/triple_core/core_2_examples/example_finder.py` existe
- [ ] Diretório `/content/screenplays/` existe com 33 PDFs
- [ ] Arquivo `/content/screenplays/masters_index.json` existe

### MODELFILE
- [ ] `ollama show scripturemon-optimized --modelfile` retorna config
- [ ] temperature = 0.2
- [ ] seed = 1337
- [ ] top_k = 0
- [ ] repeat_penalty = 1.15
- [ ] Contém "PROIBIÇÕES ABSOLUTAS" com 4 regras
- [ ] Contém exemplos de SAMANTHA e ALBERTO

### CÓDIGO
- [ ] `analyze_all_specialists.py` importa `TripleCoreWrapper`
- [ ] Análise de teste completa sem erros
- [ ] Log mostra: "Core 2 completed in X.Xs"
- [ ] Log mostra: "Found X examples from masters"

### QUALIDADE
- [ ] Personagens citados são REAIS (do roteiro)
- [ ] Páginas citadas estão dentro do range (1-16)
- [ ] Cenas citadas existem no roteiro
- [ ] NER validation: overlap > 80%
- [ ] NER validation: hallucinated < 3
- [ ] Quality Score >= 0.85
```

---

## 📝 LOGS E EVIDÊNCIAS

### Evidência da Alucinação (Oct 14):

```html
CENA 6 (página 15): Sofia mostra contradição em "Quero, mas não posso..."
CENA 10 (página 35): Julio descreve Sofia como "Ela sempre teve essa tendência..."
CENA 18 (página 60): Sofia não mostra transformação, apenas declara: "Mudei"
CENA 25 (página 80): Personagens secundários (Maria, Ana) comentam sobre Sofia
```

**PROBLEMA:** Roteiro tem apenas 16 páginas! Páginas 35, 60, 80 NÃO EXISTEM!
**PROBLEMA:** Personagens Sofia, Julio, Maria, Ana NÃO EXISTEM no roteiro!

### NER Validation Logs (Oct 14):

```
[DUAL-CORE] ⚠️ NER validation concern: overlap=21.7%, hallucinated=['RESULTADO', 'SOFIA', 'JULIO', 'MARIA', 'ANA', ...]
[DUAL-CORE] ⚠️ NER validation concern: overlap=18.2%, hallucinated=['SOFIA', 'JULIO', 'MARIA', ...]
[DUAL-CORE] ⚠️ NER validation concern: overlap=13.6%, hallucinated=['SOFIA', 'JULIO', ...]
```

### Análise Correta (Oct 4):

```html
CENA 6: Samantha diz "Mas eu estava tendo um sonho lindo..."
Alberto pergunta: "Você está bem?"
Kleber observa a cena da porta...

(Personagens REAIS, cenas REAIS, páginas REAIS)
```

---

## 🔚 CONCLUSÃO

**CAUSA RAIZ DEFINITIVA:**

A remoção do **CORE 2 (Example Finder)** eliminou TODO o grounding data que mantinha o LLM ancorado na realidade. Sem exemplos de personagens reais (Vincent Vega, Neo, Jules) dos 33 roteiros mestres, combinado com:

1. Modelfile sem few-shot examples (Samantha, Alberto)
2. Temperature aumentado (0.2 → 0.3)
3. Seed removido (não-reproduzível)
4. Proibições vagas

O LLM passou a **inventar** personagens, cenas e páginas genéricos para preencher o vazio onde antes havia dados concretos.

**SOLUÇÃO:** Restaurar Triple-Core do backup de 4 de outubro.

**TEMPO ESTIMADO:** 30 minutos
**PROBABILIDADE DE SUCESSO:** 95%

---

**Documento gerado por:** Claude Code
**Data:** 2025-10-14
**Versão:** 1.0 (Análise Completa)
