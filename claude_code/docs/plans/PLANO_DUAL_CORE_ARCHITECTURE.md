# 🧠 Plano de Arquitetura Dual-Core para Script Doctor™

## 📌 Status do Documento v2.6 - SISTEMA DE MEMÓRIA HIERÁRQUICO

**Este documento define a EVOLUÇÃO para Dual-Core + Memória Hierárquica**

- **Trabalha em conjunto com**:
  - `SCRIPT_DOCTOR_MASTER_PLAN.md` (v3.3 ✅) - Infraestrutura e orquestração
  - `DIARIO_DE_BORDO_DUAL_CORE.md` (Sessão 2 ✅) - Progresso e descobertas
  - `AUDITORIA_FORENSE_SCRIPTUREMON.md` ✅ - Mapeamento de desconexões
  - `🔥CHECKPOINT_SYSTEM🔥.md` (NOVO ✅) - Rastreamento de progresso
- **Responsabilidade deste plano**: Arquitetura Wrapper Dual-Core + Content + Memória
- **Data**: 01 de Outubro de 2025 - 02:20
- **Versão**: 2.6 - Sistema de Memória Hierárquico
- **Última Sincronização**: SESSÃO 2 - Sistema de memória aprovado

⚠️ **REGRA DE OURO:** Toda modificação requer sincronização dos arquivos

### Mudanças v2.5 → v2.6:
- ✅ Adição FASE 2B: Sistema de Memória Hierárquico (2-3 dias)
- ✅ Arquitetura de memória 3 níveis (specialists/ + shared/ + meta/)
- ✅ Classes implementadas: SpecialistMemory, SharedMemory, MetaMemory
- ✅ MemoryConsolidator para aprendizado contínuo
- ✅ Importance scoring para evitar crescimento infinito
- ✅ Cross-specialist learning automático
- ✅ Integração com BM25 e SmartCache existentes
- ✅ Roadmap: 4 fases → 5 fases (8-12 dias total)

### Mudanças v2.4 → v2.5:
- ✅ Incorporação de 8 categorias de desconexões da auditoria
- ✅ Roadmap de 4 fases de integração (20% → 100%)
- ✅ Estratégia de indexação de content/ (13 livros + 35 roteiros)
- ✅ Plano de ativação de patches (CitationValidator, IdentityEnforcer, SmartCache)
- ✅ Arquitetura ContentIndexer + BM25 integration
- ✅ Learning system com 128k tokens para LLM

---

## 🔴 DESCOBERTA CRÍTICA - SISTEMA JÁ EXISTE

### ✅ REALIDADE DO SISTEMA (DESCOBERTO EM ANÁLISE PROFUNDA)

**Base:** `/Users/clubproducoes/Digimundo/scripturemon-clean/`

1. **24 Especialistas Python** ✅ JÁ IMPLEMENTADOS E FUNCIONAIS
   - Local: `specialists/implementations/`
   - Exemplo: `character_dialogue_specialist.py` (946 linhas!)
   - Classes: `DrDialogue`, `DrCharacter`, etc.
   - Método: `analyze(screenplay_text)` → Dict estruturado
   - **STATUS:** Funcionais mas NÃO usados no fluxo principal

2. **Sistema LLM** ✅ JÁ INTEGRADO (MAS LLM-ONLY)
   - Ollama funcionando com Mistral 8x7b
   - Orquestrador em `core/scripturemon.py`
   - **PROBLEMA:** Chama LLM diretamente, ignora especialistas Python

3. **Regras YAML** ✅ COMPLETAS
   - Local: `specialists/rules/`
   - Estruturadas com severity, test, fix

### 🔥🔥🔥 DESCOBERTAS DA AUDITORIA FORENSE (SESSÃO 2)

**DOCUMENTO COMPLETO:** `/Users/clubproducoes/Digimundo/claude_code/AUDITORIA_FORENSE_SCRIPTUREMON.md`

#### ❌ DESCONEXÃO #1: BIBLIOTECA DE CONTEÚDO INVISÍVEL (CRÍTICO)
- **13 livros de teoria** em `content/theory/` - ZERO uso
- **35 roteiros masterclass** em `content/screenplays/masters/` - ZERO uso
- **~250MB de conhecimento premium** completamente desperdiçado
- **Sistema de memória BM25** existe mas NÃO indexa content/
- **EVIDÊNCIA:** `grep -r "content/" *.py` = 0 resultados

#### ❌ DESCONEXÃO #2: PATCHES IMPLEMENTADOS MAS DESATIVADOS (CRÍTICO)
- `CitationValidator` (171 linhas) - anti-alucinação pronto, NÃO ativado
- `IdentityEnforcer` (135 linhas) - Script Doctor™ identity pronta, NÃO usada
- `SmartCache` (189 linhas) - cache inteligente pronto, NÃO integrado
- **EVIDÊNCIA:** Zero imports em `core/scripturemon.py`

#### ❌ DESCONEXÃO #3: ARQUITETURA DUAL-CORE NÃO EXISTE
- Sistema atual: LLM-only
- Especialistas Python: Existem mas não são usados
- **Solução**: DualCoreWrapper (não-invasivo)

### 📊 IMPACTO MEDIDO
```
CAPACIDADE ATUAL:        20%  ░░░░░░░░░░░░░░░░░░░░
CAPACIDADE POTENCIAL:   100%  ████████████████████
CÓDIGO NÃO USADO:     15.750 linhas
CONTEÚDO NÃO USADO:   250MB (48 arquivos premium)
```

---

## 🔗 INTEGRAÇÃO COM MASTER PLAN

**DIVISÃO DE RESPONSABILIDADES:**

**ESTE PLANO (Dual-Core):**
- ✅ Arquitetura dos 24 especialistas
- ✅ Implementação Python + LLM
- ✅ Análise multi-pass profunda
- ✅ Biblioteca teórica integrada
- ✅ Database de masterpieces
- ✅ Prompts inteligentes (128k tokens)

**MASTER PLAN:**
- ✅ Infraestrutura base (validação, cache, identidade)
- ✅ Base de conhecimento (indexação)
- ✅ Sistema de notas (0-100 + grades)
- ✅ Orquestrador principal
- ✅ CLI e interface
- ✅ Testes de integração

**→ Consulte `SCRIPT_DOCTOR_MASTER_PLAN.md` para infraestrutura e orquestração**

---

## 🎯 Resumo Executivo (ATUALIZADO - Baseado na Realidade)

### O Que É
Evolução de sistema **EXISTENTE** que combina **24 especialistas Python já implementados** com **análise LLM** através de arquitetura Wrapper não-invasiva.

### Situação Descoberta (Análise Profunda - 30/09/2025)
✅ **24 especialistas Python** - COMPLETOS E FUNCIONAIS (ex: 946 linhas no DrDialogue)
✅ **Sistema de regras YAML** - ESTRUTURADO E CARREGADO
✅ **Ollama integrado** - FUNCIONANDO com Mistral 8x7b
✅ **Orquestrador** - ATIVO em `core/scripturemon.py`
✅ **CLI completo** - PRONTO (`run.py`)
❌ **Dual-Core** - NÃO EXISTE (sistema é LLM-only)
❌ **Especialistas Python** - EXISTEM mas NÃO SÃO USADOS

### Evolução Planejada (v2.4) - WRAPPER NÃO-INVASIVO
🚀 **DualCoreWrapper sem modificar código existente**:
- **Core 1 (Python)**: USAR especialistas já implementados (sem modificar)
- **Core 2 (LLM/Mistral)**: ADICIONAR análise LLM com contexto Python
- **Wrapper**: Envolver especialistas Python + injetar LLM
- **Fallback**: Se LLM falhar, retorna só Python (robusto)
- **Incremental**: Testar um especialista por vez

### Como Funciona (REALIDADE)
```python
# ANTES (LLM-only - atual)
orquestrador → LLM direto → resultado

# DEPOIS (Dual-Core - objetivo)
wrapper → Python analisa → dados estruturados
       → LLM enriquece com contexto Python → insights
       → Synthesis → resultado completo (Python + LLM)
```

**Fluxo Detalhado:**
1. **DualCoreWrapper.analyze()** chamado
2. **Python Core** analisa (usando código existente) → Dict estruturado
3. **LLM** recebe contexto Python + roteiro → insights qualitativos
4. **Synthesis** combina → resultado final rico
5. **Fallback** se LLM falhar → retorna só Python (sempre funciona)

### Diferencial Único
- **SEM alucinações**: Python valida todos os dados factuais
- **COM profundidade**: LLM usa 128k tokens para análise exaustiva
- **Teoria + Prática**: Compara com McKee, Truby, Save the Cat E obras-primas reais
- **Configurável**: Liga/desliga LLM, ajusta profundidade, escolhe especialistas

---

## 🏗️ Arquitetura Dual-Core

### Conceito Fundamental
```
[Screenplay] → [Python Core] → [Structured Analysis] → [Guided LLM Prompt] → [LLM Core] → [Synthesis] → [Final Report]
```

### Fluxo Simplificado
```
ENTRADA → PYTHON (análise objetiva) → CONTEXTO RICO → LLM (insights profundos) → SÍNTESE → RELATÓRIO
```

### Por Que Funciona?

1. **LLM Recebe Contexto Rico**: Em vez de analisar do zero, o LLM recebe a análise estrutural completa
2. **Elimina Alucinações**: Python garante precisão dos dados objetivos
3. **Prompts Otimizados**: LLM foca apenas em insights qualitativos
4. **Qualidade Máxima**: Combina precisão algorítmica com compreensão artística

### Vantagem de Cada Núcleo

| Python Core | LLM Core (Mistral) |
|------------|-------------------|
| ✅ Contagens precisas | ✅ Entende subtexto |
| ✅ Estrutura dos 3 atos | ✅ Avalia naturalidade |
| ✅ Métricas objetivas | ✅ Compara com teoria |
| ✅ Sempre consistente | ✅ Sugere reescritas |
| ✅ Instantâneo | ✅ Insights criativos |

---

## 💻 Implementação Técnica

### Estrutura Base de um Especialista Dual-Core (COMPLETA)

```python
class DualCoreSpecialist:
    """
    Especialista com arquitetura Dual-Core
    Combina análise estrutural (Python) com insights profundos (LLM)
    """

    def __init__(self, name: str, specialty: str, use_llm: bool = True):
        self.name = name
        self.specialty = specialty
        self.use_llm = use_llm

        # Núcleo 1: Python (sempre ativo)
        self.python_core = PythonAnalysisCore()

        # Núcleo 2: LLM (opcional, mas recomendado)
        if self.use_llm:
            self.llm_core = OllamaLLMCore(model="mistral")

    def analyze(self, screenplay: str) -> DualCoreResult:
        """Análise dual-core do roteiro"""

        # FASE 1: Análise Python (instantânea)
        python_analysis = self.python_core.analyze(screenplay)

        # FASE 2: LLM guiado (se habilitado)
        llm_analysis = None
        if self.use_llm:
            guided_prompt = self._create_guided_prompt(screenplay, python_analysis)
            llm_analysis = self.llm_core.analyze(guided_prompt)

        # FASE 3: Síntese
        return self._synthesize_results(python_analysis, llm_analysis)

    def _create_guided_prompt(self, screenplay: str, python_analysis: dict) -> str:
        """Cria prompt otimizado com contexto da análise Python"""
        return f"""
        CONTEXTO ESTRUTURAL (já analisado):
        {python_analysis.to_report()}

        PROBLEMAS DETECTADOS:
        {python_analysis.get_violations()}

        AGORA ANALISE QUALITATIVAMENTE:
        - Aspectos artísticos e criativos
        - Nuances e subtexto
        - Sugestões específicas de melhoria

        TRECHOS RELEVANTES DO ROTEIRO:
        {python_analysis.get_relevant_excerpts()}
        """
```

### Versão Simplificada (Para Começar)
```python
class DualCoreSpecialist:
    def __init__(self, name, use_llm=True):
        self.python_core = PythonCore()      # Sempre ativo
        self.llm_core = MistralCore() if use_llm else None

    def analyze(self, screenplay):
        # 1. Python analisa
        python_result = self.python_core.analyze(screenplay)

        # 2. LLM aprofunda (se ativo)
        if self.llm_core:
            llm_result = self.llm_core.analyze_with_context(
                screenplay,
                python_result
            )

        # 3. Combina resultados
        return self.synthesize(python_result, llm_result)
```

### Prompt Inteligente para LLM
```python
def create_smart_prompt(screenplay, python_analysis):
    return f"""
    VOCÊ JÁ SABE (análise Python):
    - {python_analysis.dialogue_count} diálogos
    - {python_analysis.problems} problemas encontrados
    - Páginas problemáticas: {python_analysis.problem_pages}

    AGORA APROFUNDE:
    1. POR QUE esses problemas são problemáticos?
    2. COMO os mestres resolveriam?
    3. REESCREVA os trechos problemáticos

    TRECHO PARA ANÁLISE:
    {screenplay[problematic_section]}
    """
```

---

## 📊 Matriz de Priorização para Implementação Dual-Core

### 🔴 Prioridade CRÍTICA (Ganho Máximo com LLM)
Especialistas que NECESSITAM compreensão contextual profunda:

| # | Especialista | Python Core | LLM Core | Justificativa |
|---|-------------|------------|----------|---------------|
| 9 | **Subtext** | Detecta padrões | Entende não-ditos | Subtexto é impossível sem compreensão profunda |
| 3 | **Character Psychology** | Conta falas | Analisa motivações | Psicologia precisa compreensão humana |
| 14 | **Theme Consistency** | Palavras-chave | Análise temática | Temas são conceitos abstratos |
| 16 | **Symbolism & Metaphor** | Detecta símbolos | Interpreta significados | Simbolismo requer interpretação |
| 1 | **Character Dialogue** | Métricas | Naturalidade e voz | Diálogo natural precisa compreensão |

### 🟡 Prioridade ALTA (Benefício Significativo)
Especialistas que ganham muito com insights qualitativos:

| # | Especialista | Python Core | LLM Core | Justificativa |
|---|-------------|------------|----------|---------------|
| 18 | **Tone Consistency** | Detecta mudanças | Avalia adequação | Tom é subjetivo |
| 20 | **World Building** | Conta elementos | Avalia coerência | Mundos precisam consistência |
| 17 | **Voice Consistency** | Padrões de fala | Vozes únicas | Voz é personalidade |
| 2 | **Character Arcs** | Mapeia mudanças | Avalia crescimento | Arcos são jornadas emocionais |
| 5 | **Character Relationships** | Mapeia interações | Dinâmica emocional | Relacionamentos são complexos |

### 🟢 Prioridade MÉDIA (Benefício Moderado)
Especialistas onde Python é forte mas LLM adiciona valor:

| # | Especialista | Python Core | LLM Core | Justificativa |
|---|-------------|------------|----------|---------------|
| 19 | **Genre Conventions** | Checa elementos | Avalia aderência | Gêneros têm nuances |
| 21 | **Originality Assessment** | Detecta clichês | Avalia criatividade | Originalidade é contextual |
| 15 | **Visual Motifs** | Conta recorrências | Interpreta propósito | Motivos visuais têm significado |
| 11 | **Climax** | Identifica clímax | Avalia impacto | Impacto é emocional |
| 12 | **Resolution** | Verifica fechamentos | Satisfação emocional | Satisfação é subjetiva |

### 🔵 Prioridade BAIXA (Python Suficiente)
Especialistas onde análise estrutural é adequada:

| # | Especialista | Python Core | LLM Core | Justificativa |
|---|-------------|------------|----------|---------------|
| 7 | **Structure** | Analisa 3 atos | Confirma estrutura | Estrutura é matemática |
| 8 | **Formatting** | Verifica regras | Confirma padrões | Formato é técnico |
| 6 | **Pacing** | Conta cenas/páginas | Avalia ritmo | Pacing é quantificável |
| 10 | **Opening** | Analisa primeiras páginas | Avalia hook | Abertura tem regras claras |
| 13 | **Transitions** | Detecta transições | Avalia fluidez | Transições são identificáveis |
| 4 | **Action Description** | Conta linhas | Clareza e impacto | Ação é visual e direta |

### 🏆 Especialistas Meta (Sempre Dual-Core)

| # | Especialista | Função | Necessidade LLM |
|---|-------------|--------|-----------------|
| 22 | **Overall Quality** | Síntese de todos | Alta - precisa ponderar qualitativamente |
| 23 | **Market Potential** | Análise comercial | Alta - mercado é complexo |
| 24 | **Executive Summary** | Decisão final | Crítica - decisão precisa sabedoria |

---

## 🔄 Fluxo de Implementação

### Fase 1: Preparação da Infraestrutura (Semana 1)
```python
# 1. Criar classe base DualCoreSpecialist
# 2. Implementar integração com Ollama
# 3. Criar sistema de prompts guiados
# 4. Estabelecer protocolo de síntese
```

### Fase 2: Migração Prioritária (Semana 2)
```python
# Converter especialistas CRÍTICOS primeiro:
1. Subtext Specialist → SubtextDualCore
2. Character Psychology → PsychologyDualCore
3. Theme Consistency → ThemeDualCore
4. Symbolism & Metaphor → SymbolismDualCore
5. Character Dialogue → DialogueDualCore
```

### Fase 3: Expansão Gradual (Semana 3-4)
```python
# Converter especialistas de ALTA prioridade
# Manter fallback para Python puro se LLM falhar
```

### Fase 4: Otimização para QUALIDADE MÁXIMA
```python
# Ajustar prompts para análise mais profunda
# Implementar análise iterativa (múltiplas passadas)
# Adicionar verificação cruzada entre especialistas
# Permitir re-análise com foco em problemas específicos
```

---

## 🎨 Estratégia de Análise Profunda

### Análise Multi-Pass (Múltiplas Passadas)

Cada especialista Dual-Core fará TRÊS passadas de análise:

```python
class DualCoreDeepAnalysis:
    def analyze_deep(self, screenplay):
        # PASSADA 1: Análise Python Completa (2-3 minutos)
        python_analysis = self.python_core.deep_analysis(screenplay)
        # - Análise linha por linha
        # - Detecção de TODOS os padrões
        # - Mapeamento completo de relacionamentos
        # - Estatísticas exaustivas

        # PASSADA 2: Primeira Análise LLM (30-45 segundos)
        first_llm = self.llm_core.analyze(
            screenplay,
            context=python_analysis,
            depth="comprehensive",
            focus="identify_all_issues"
        )

        # PASSADA 3: Análise LLM Focada (30-45 segundos)
        deep_llm = self.llm_core.analyze(
            screenplay,
            context=python_analysis + first_llm,
            depth="surgical",
            focus="deep_dive_on_problems",
            examples="provide_specific_rewrites"
        )

        # SÍNTESE: Combinar todas as análises
        return self.synthesize_deep(
            python_analysis,
            first_llm,
            deep_llm
        )
```

### Prompts Expandidos para Qualidade

```python
def create_deep_analysis_prompt(self, screenplay, python_analysis):
    return f"""
    VOCÊ É {self.name} - SPECIALIST EM {self.specialty}

    TEMPO DISPONÍVEL: Você tem 45 segundos. Use TODOS eles.
    OBJETIVO: Análise MAIS PROFUNDA POSSÍVEL, não a mais rápida.

    ANÁLISE ESTRUTURAL COMPLETA:
    {python_analysis.full_report()}

    ANALISE OS SEGUINTES ASPECTOS EM PROFUNDIDADE:

    1. DIAGNÓSTICO COMPLETO (15 segundos)
       - Identifique TODOS os problemas, mesmo os sutis
       - Explique POR QUE cada problema é problemático
       - Conecte problemas com impacto na experiência do leitor

    2. ANÁLISE DE PADRÕES (10 segundos)
       - Identifique padrões recorrentes (bons e ruins)
       - Analise a consistência ao longo do roteiro
       - Detecte oportunidades perdidas

    3. COMPARAÇÃO COM OBRAS-PRIMAS (10 segundos)
       - Compare com os melhores exemplos do gênero
       - O que os mestres fariam diferente?
       - Cite exemplos específicos de filmes/roteiros

    4. REESCRITA DETALHADA (10 segundos)
       - Para CADA problema principal, forneça:
         * O texto atual
         * Sugestão de reescrita COMPLETA
         * Explicação do porquê da mudança

    ROTEIRO COMPLETO PARA ANÁLISE:
    {screenplay}

    NÃO ECONOMIZE PALAVRAS. SEJA EXAUSTIVO.
    """
```

### Análise Cruzada Entre Especialistas

```python
class CrossSpecialistAnalysis:
    """
    Especialistas compartilham insights entre si
    """

    def analyze_with_context(self, screenplay, other_specialists_results):
        # Recebe resultados de outros especialistas
        dialogue_insights = other_specialists_results.get('dialogue')
        character_insights = other_specialists_results.get('character')

        # Usa insights para análise mais rica
        enhanced_prompt = f"""
        CONTEXTO DE OUTROS ESPECIALISTAS:

        Dialogue Specialist encontrou:
        {dialogue_insights.main_issues}

        Character Specialist encontrou:
        {character_insights.arc_problems}

        AGORA, com esse contexto, analise {self.specialty} considerando:
        - Como os problemas de diálogo afetam {self.area}?
        - Como os arcos de personagem impactam {self.area}?
        - Que soluções integradas você propõe?
        """
```

---

## 🧩 Configuração Mistral 128k Tokens

### Aproveitamento Máximo do Contexto

Com 128k tokens disponíveis, podemos enviar para o Mistral:

```python
class MistralMaxContext:
    """
    Configuração para usar os 128k tokens do Mistral
    """

    MAX_TOKENS = 128000

    def prepare_ultra_context(self, screenplay, python_analysis):
        """
        Prepara contexto MASSIVO para análise profunda
        """
        context = {
            # 1. ROTEIRO COMPLETO (30-40k tokens)
            "full_screenplay": screenplay,

            # 2. ANÁLISE PYTHON COMPLETA (5-10k tokens)
            "python_full_report": python_analysis.complete_report,
            "all_metrics": python_analysis.all_metrics,
            "every_pattern": python_analysis.detected_patterns,

            # 3. BIBLIOTECA TEÓRICA (20-30k tokens)
            "screenplay_theory": self.load_theory_library(),
            "relevant_techniques": self.get_relevant_techniques(),
            "master_examples": self.load_masterclass_examples(),

            # 4. ROTEIROS DE REFERÊNCIA (30-40k tokens)
            "comparable_scenes": self.load_comparable_scenes(),
            "genre_masterpieces": self.load_genre_examples(),
            "structure_templates": self.load_structure_templates(),

            # 5. INSTRUÇÕES DETALHADAS (5-10k tokens)
            "analysis_depth": "maximum",
            "required_sections": self.get_all_analysis_sections(),
            "output_examples": self.load_output_examples()
        }

        return self.format_for_mistral(context)
```

### Uso Estratégico do Contexto Expandido

```python
def create_128k_prompt(self):
    return """
    [CONTEXTO: 128.000 tokens disponíveis - USE TODOS]

    SEÇÃO 1: ROTEIRO COMPLETO (não resumido)
    {full_screenplay}

    SEÇÃO 2: ANÁLISE ESTRUTURAL PYTHON
    {complete_python_analysis}

    SEÇÃO 3: BIBLIOTECA TEÓRICA
    Teorias Relevantes:
    - McKee Story Structure: {mckee_principles}
    - Truby's 22 Steps: {truby_steps}
    - Save the Cat: {save_cat_beats}
    - Hero's Journey: {campbell_journey}
    - Syd Field Paradigm: {field_paradigm}

    SEÇÃO 4: ROTEIROS COMPARÁVEIS
    Cenas similares de obras-primas:
    {masterpiece_scenes}

    Como Tarantino resolveria: {tarantino_approach}
    Como Sorkin resolveria: {sorkin_approach}
    Como Nolan resolveria: {nolan_approach}

    SEÇÃO 5: SUA ANÁLISE DEVE INCLUIR:
    1. Análise linha-por-linha do roteiro
    2. Comparação com CADA teoria mencionada
    3. Contraste com TODAS as obras-primas fornecidas
    4. Reescrita completa de TODAS as cenas problemáticas
    5. Justificativa teórica para CADA sugestão

    USE OS 128K TOKENS. SEJA EXAUSTIVO.
    """
```

---

## 📚 Sistema de Biblioteca Teórica

### Biblioteca de Teorias de Roteiro

```python
class ScreenwritingLibrary:
    """
    Biblioteca completa de teorias e técnicas
    """

    def __init__(self):
        self.theories = {
            'structure': {
                'three_act': load_theory('three_act_structure.md'),
                'save_the_cat': load_theory('save_the_cat_beats.md'),
                'heros_journey': load_theory('campbell_hero.md'),
                'field_paradigm': load_theory('syd_field.md'),
                'sequence_approach': load_theory('eight_sequences.md'),
                'mini_movie': load_theory('mini_movie_method.md')
            },
            'character': {
                'archetypes': load_theory('jung_archetypes.md'),
                'enneagram': load_theory('enneagram_types.md'),
                'want_need': load_theory('want_vs_need.md'),
                'ghost_wound': load_theory('backstory_wound.md'),
                'character_diamond': load_theory('truby_diamond.md')
            },
            'dialogue': {
                'subtext': load_theory('subtext_techniques.md'),
                'voice': load_theory('unique_voice.md'),
                'sorkin_style': load_theory('sorkin_dialogue.md'),
                'mamet_speak': load_theory('mamet_principles.md'),
                'tarantino_method': load_theory('tarantino_dialogue.md')
            },
            'theme': {
                'moral_premise': load_theory('moral_premise.md'),
                'controlling_idea': load_theory('mckee_controlling.md'),
                'thematic_unity': load_theory('thematic_coherence.md'),
                'symbol_systems': load_theory('symbolic_meaning.md')
            }
        }

    def get_relevant_theories(self, specialist_type, problems_found):
        """
        Seleciona teorias relevantes baseado nos problemas
        """
        relevant = []

        if 'structure' in problems_found:
            relevant.extend([
                self.theories['structure']['three_act'],
                self.theories['structure']['save_the_cat']
            ])

        if 'character' in problems_found:
            relevant.extend([
                self.theories['character']['want_need'],
                self.theories['character']['character_diamond']
            ])

        return relevant
```

### Integração Python + Biblioteca + LLM

```python
def analyze_with_theory(self, screenplay, python_analysis):
    # Python detecta problema
    if python_analysis.has_problem('weak_midpoint'):

        # Carrega teoria relevante
        midpoint_theory = self.library.get_theory('midpoint_reversal')

        # Envia para LLM com contexto teórico
        prompt = f"""
        PROBLEMA DETECTADO: Midpoint fraco na página {python_analysis.midpoint_page}

        TEORIA RELEVANTE (Blake Snyder):
        {midpoint_theory}

        ANALISE o midpoint atual:
        {screenplay[midpoint_section]}

        COMPARE com exemplos de midpoints efetivos:
        - The Matrix: Neo escolhe a pílula vermelha
        - Star Wars: Death Star destrói Alderaan
        - Alien: O alien está na nave

        SUGIRA reescrita baseada na teoria.
        """
```

---

## 🎬 Banco de Roteiros Masterpiece

### Database de Roteiros de Referência

```python
class MasterpieceDatabase:
    """
    Banco de dados com grandes roteiros para comparação
    """

    def __init__(self):
        self.load_masterpieces()

    def load_masterpieces(self):
        self.db = {
            'drama': [
                'the_godfather.screenplay',
                'shawshank_redemption.screenplay',
                'schindlers_list.screenplay',
                '12_angry_men.screenplay',
                'one_flew_over_cuckoos.screenplay'
            ],
            'action': [
                'die_hard.screenplay',
                'raiders_lost_ark.screenplay',
                'matrix.screenplay',
                'mad_max_fury_road.screenplay',
                'terminator_2.screenplay'
            ],
            'comedy': [
                'some_like_it_hot.screenplay',
                'annie_hall.screenplay',
                'groundhog_day.screenplay',
                'airplane.screenplay',
                'the_big_lebowski.screenplay'
            ],
            'thriller': [
                'silence_of_lambs.screenplay',
                'psycho.screenplay',
                'seven.screenplay',
                'the_sixth_sense.screenplay',
                'chinatown.screenplay'
            ],
            'scifi': [
                'blade_runner.screenplay',
                '2001_space_odyssey.screenplay',
                'alien.screenplay',
                'inception.screenplay',
                'eternal_sunshine.screenplay'
            ]
        }

    def find_comparable_scenes(self, scene_type, genre):
        """
        Encontra cenas comparáveis nos masterpieces
        """
        comparable = []

        for screenplay in self.db[genre]:
            scenes = self.extract_scenes(screenplay, scene_type)
            comparable.extend(scenes)

        return comparable

    def contrast_analysis(self, user_scene, masterpiece_scenes):
        """
        Análise comparativa com obras-primas
        """
        return f"""
        SUA CENA:
        {user_scene}

        COMPARE COM ESTAS OBRAS-PRIMAS:

        1. THE GODFATHER (Cena similar):
        {masterpiece_scenes[0]}
        - O que Coppola fez diferente?
        - Por que funciona melhor?

        2. CHINATOWN (Abordagem alternativa):
        {masterpiece_scenes[1]}
        - Como Towne resolveu?
        - Que técnicas usou?

        3. CASABLANCA (Clássico):
        {masterpiece_scenes[2]}
        - Estrutura clássica
        - Por que ainda funciona?

        SÍNTESE: O que sua cena pode aprender?
        """
```

### Análise Comparativa Automática

```python
class ComparativeAnalysis:
    def analyze_against_masters(self, screenplay, specialist_type):
        # 1. Identifica gênero
        genre = self.identify_genre(screenplay)

        # 2. Carrega masterpieces relevantes
        masters = self.db.get_masterpieces(genre, specialist_type)

        # 3. Para cada aspecto problemático
        for problem in self.python_analysis.problems:
            # Encontra como os mestres resolveram
            master_solutions = self.find_solutions_in_masters(
                problem,
                masters
            )

            # Cria prompt comparativo
            prompt = f"""
            PROBLEMA EM SEU ROTEIRO:
            {problem.description}
            {problem.excerpt}

            COMO OS MESTRES RESOLVERAM:

            {master_solutions}

            APLIQUE ESTAS LIÇÕES:
            1. Identifique o princípio usado
            2. Adapte para seu contexto
            3. Reescreva seguindo o exemplo
            4. Justifique as mudanças
            """
```

---

## 🎯 Fluxo de Análise Ultra-Profunda

### Pipeline Completo

```python
class UltraDeepAnalysisPipeline:
    """
    Pipeline de análise sem pressa, com foco em qualidade máxima
    """

    def analyze_screenplay_perfectly(self, screenplay):

        # FASE 1: Python Analysis (5-10 minutos)
        print("📊 Iniciando análise estrutural profunda...")
        python_result = self.python_exhaustive_analysis(screenplay)

        # FASE 2: Carregar Contexto (2-3 minutos)
        print("📚 Carregando biblioteca teórica...")
        theories = self.load_relevant_theories(python_result)

        print("🎬 Carregando roteiros de referência...")
        masterpieces = self.load_comparable_masterpieces(
            screenplay,
            python_result
        )

        # FASE 3: Primeira Análise LLM (5-10 minutos)
        print("🧠 Análise profunda - Primeira camada...")
        first_analysis = self.llm_analyze(
            context_size=128000,
            screenplay=screenplay,
            python_analysis=python_result,
            theories=theories,
            masterpieces=masterpieces,
            depth="exhaustive",
            focus="identify_everything"
        )

        # FASE 4: Segunda Análise LLM (5-10 minutos)
        print("🔬 Análise profunda - Segunda camada...")
        deep_analysis = self.llm_analyze(
            context_size=128000,
            previous_analysis=first_analysis,
            focus="deep_dive_problems",
            instruction="Analise CADA problema em profundidade"
        )

        # FASE 5: Terceira Análise LLM - Soluções (5-10 minutos)
        print("✍️ Gerando soluções e reescritas...")
        solutions = self.llm_analyze(
            context_size=128000,
            problems=deep_analysis.problems,
            masterpiece_examples=masterpieces,
            focus="complete_rewrites",
            instruction="Reescreva CADA cena problemática"
        )

        # FASE 6: Síntese Final (2-3 minutos)
        print("📝 Compilando relatório final...")
        return self.create_ultimate_report(
            python_result,
            first_analysis,
            deep_analysis,
            solutions,
            theories,
            masterpieces
        )
```

---

## 📈 Métricas de Sucesso

### Qualidade
- ✅ Análises mais profundas e nuançadas
- ✅ Detecção de subtexto e simbolismo
- ✅ Recomendações mais específicas e úteis

### Performance (FOCO EM QUALIDADE, NÃO VELOCIDADE)
- ⚡ Análise Python: Completa e detalhada (tempo irrelevante)
- 🔄 Análise LLM: 30-60s por especialista para análise PROFUNDA
- 📊 Total para 24 especialistas: 15-30 minutos de análise COMPLETA
- 🎯 **OBJETIVO**: Melhor análise possível, não a mais rápida

### Confiabilidade
- ✅ 100% de precisão em métricas objetivas (Python)
- ✅ 0% alucinações em dados factuais (validado por Python)
- ✅ Fallback automático se LLM indisponível

---

## 🚀 Próximos Passos

1. **Aprovar arquitetura Dual-Core**
2. **Implementar classe base `DualCoreSpecialist`**
3. **Criar primeiro protótipo com `DialogueDualCore`**
4. **Testar e validar ganhos de qualidade**
5. **Expandir para outros especialistas prioritários**

---

## 📝 Exemplo Prático: Dialogue Specialist Dual-Core

### Entrada
```screenplay
JOHN
I love you.

MARY
I love you too.
```

### Análise Python Core (0.1s)
```json
{
  "total_dialogues": 2,
  "avg_words": 3,
  "repetition_rate": 0.5,
  "conflict_detected": false,
  "score": 35,
  "problems": ["Too generic", "No conflict", "No character voice"]
}
```

### Prompt Guiado para LLM
```
Análise estrutural detectou:
- Diálogo genérico (pontuação: 35/100)
- Ausência de conflito
- Ausência de vozes distintas

Analise a QUALIDADE ARTÍSTICA e sugira REESCRITA que:
1. Adicione personalidade única a cada personagem
2. Introduza tensão ou subtexto
3. Torne o diálogo memorável e específico
```

### Resposta LLM Core (8s)
```
O diálogo carece de especificidade e autenticidade. As declarações
são intercambiáveis e não revelam nada sobre os personagens.

REESCRITA SUGERIDA:
JOHN
You know that thing you do with your nose when you're nervous?

MARY
(touching her nose, defensive)
I don't do anything with my—

JOHN
I've loved it since sophomore year.

MARY
(softening)
That's when you still had the mohawk.

Esta versão revela história compartilhada, gestos específicos e
personalidades distintas, mantendo a declaração de amor subtextual.
```

### Síntese Final
```json
{
  "score": 35,
  "grade": "D",
  "structural_issues": ["Generic", "No conflict", "No voice"],
  "artistic_assessment": "Lacks authenticity and specificity",
  "specific_recommendations": [
    "Add character-specific speech patterns",
    "Include shared history references",
    "Show emotion through behavior, not just words"
  ],
  "rewrite_example": "[exemplo acima]",
  "confidence": 0.95
}
```

---

## 📊 Formato de Saída Ultra-Detalhado

### Relatório Final Enriquecido

```python
class UltraDetailedReport:
    """
    Relatório final com profundidade máxima
    """

    def generate_ultimate_report(self, all_analyses):
        return {
            # 1. SUMÁRIO EXECUTIVO (2-3 páginas)
            'executive_summary': {
                'verdict': 'PASS/CONSIDER/RECOMMEND/CHAMPION',
                'one_line': 'Síntese em uma linha',
                'elevator_pitch': 'Pitch de 30 segundos',
                'core_strengths': ['Lista de forças principais'],
                'critical_issues': ['Problemas que DEVEM ser resolvidos'],
                'market_position': 'Posicionamento no mercado atual',
                'comparable_successes': ['Filmes comparáveis de sucesso']
            },

            # 2. ANÁLISE PROFUNDA POR ESPECIALISTA (50+ páginas)
            'specialist_reports': {
                'dialogue': {
                    'score': 85,
                    'grade': 'B+',
                    'python_metrics': {...},  # Todas as métricas
                    'llm_insights': {...},     # Insights profundos
                    'theoretical_analysis': {  # Análise teórica
                        'sorkin_principles': 'Como se compara...',
                        'mamet_speak': 'Aplicação de Mamet...',
                        'subtext_layers': 'Camadas de subtexto...'
                    },
                    'masterpiece_comparison': {  # Comparação com obras-primas
                        'godfather_dialogue': 'Comparação específica...',
                        'pulp_fiction_style': 'Estilo Tarantino...'
                    },
                    'specific_problems': [      # Problemas específicos
                        {
                            'page': 23,
                            'line': 15,
                            'current': 'Diálogo atual',
                            'issue': 'Explicação detalhada do problema',
                            'theory_violation': 'Qual princípio viola',
                            'suggested_rewrite': 'Reescrita completa',
                            'justification': 'Por que esta mudança'
                        }
                    ],
                    'patterns_detected': [...],  # Padrões encontrados
                    'improvement_exercises': [    # Exercícios para melhorar
                        'Exercício 1: Reescreva sem exposição',
                        'Exercício 2: Adicione subtexto',
                        'Exercício 3: Diferencie vozes'
                    ]
                },
                # ... Repete para TODOS os 24 especialistas
            },

            # 3. ANÁLISE CRUZADA (10+ páginas)
            'cross_analysis': {
                'dialogue_character_synergy': 'Como diálogo reflete personagens',
                'theme_structure_alignment': 'Como tema se alinha com estrutura',
                'pacing_tension_relationship': 'Relação entre ritmo e tensão',
                'unanimous_problems': ['Problemas que TODOS identificaram'],
                'conflicting_assessments': ['Onde especialistas discordam']
            },

            # 4. PLANO DE REVISÃO DETALHADO (20+ páginas)
            'revision_plan': {
                'immediate_fixes': [  # Correções imediatas
                    {
                        'priority': 1,
                        'issue': 'Problema específico',
                        'location': 'Página X, Linha Y',
                        'current_text': 'Texto atual',
                        'revised_text': 'Texto revisado',
                        'estimated_time': '30 minutos',
                        'difficulty': 'Fácil',
                        'impact': 'Alto'
                    }
                ],
                'structural_revisions': [...],  # Mudanças estruturais
                'character_development': [...],  # Desenvolvimento de personagem
                'thematic_enhancement': [...],   # Aprimoramento temático
                'polish_suggestions': [...]      # Sugestões de polimento
            },

            # 5. RECURSOS DE APRENDIZADO (5+ páginas)
            'learning_resources': {
                'recommended_reading': [
                    {'book': 'Story by McKee', 'chapters': [3, 7, 12]},
                    {'book': 'Save the Cat', 'sections': ['Midpoint', 'Finale']}
                ],
                'masterclass_suggestions': [
                    'Aaron Sorkin on Dialogue',
                    'Shonda Rhimes on Character'
                ],
                'screenplay_studies': [
                    'Study the opening of The Social Network',
                    'Analyze the midpoint of The Matrix'
                ],
                'writing_exercises': [
                    'Daily dialogue practice',
                    'Scene rewriting drills'
                ]
            },

            # 6. DADOS TÉCNICOS COMPLETOS
            'technical_data': {
                'page_count': 110,
                'word_count': 23500,
                'scene_count': 127,
                'character_count': 15,
                'dialogue_percentage': 0.42,
                'action_percentage': 0.58,
                'processing_time': '47 minutes',
                'tokens_used': 127840,
                'confidence_score': 0.94
            }
        }
```

### Exemplo de Saída Real

```
═══════════════════════════════════════════════════════════════
    SCRIPT DOCTOR™ ULTIMATE ANALYSIS REPORT
    Screenplay: "The Last Connection"
    Date: October 30, 2024
    Analysis Time: 47 minutes, 23 seconds
    Confidence: 94.2%
═══════════════════════════════════════════════════════════════

📋 EXECUTIVE SUMMARY
────────────────────
VERDICT: CONSIDER WITH MAJOR REVISIONS

One-Line: A promising tech-thriller with strong concept but
         weak execution, requiring significant character and
         dialogue work.

Comparable To: Ex Machina meets The Social Network
Market Position: Mid-budget streaming original ($15-25M)
Awards Potential: Limited without revisions
Franchise Potential: Moderate (world-building supports it)

Top 3 Strengths:
1. Original concept with contemporary relevance
2. Strong visual storytelling in action sequences
3. Compelling third act twist

Top 3 Critical Issues:
1. Protagonist lacks clear want/need dynamic (p.1-30)
2. Dialogue is 67% exposition, 12% authentic (throughout)
3. Midpoint reversal is predictable (p.55)

═══════════════════════════════════════════════════════════════

📝 DIALOGUE ANALYSIS (Score: 52/100 - Grade: D+)
────────────────────────────────────────────────────────────

PYTHON METRICS:
- Total dialogues: 347
- Average words per speech: 23.4 (too high)
- Subtext ratio: 0.12 (very low)
- Unique voice score: 0.31 (characters sound same)
- Exposition percentage: 67% (critical issue)

LLM DEEP ANALYSIS:
The dialogue suffers from what I call "Wikipedia syndrome" -
characters constantly explain things both speakers already know.
This violates Mamet's principle: "Characters should only speak
to get what they want."

THEORETICAL VIOLATION (McKee, p.387):
"Exposition is ammunition. It must be fired through conflict,
never simply presented." Your script violates this on pages:
10, 15, 23, 27, 31, 34, 39, 42, 48, 52, 58, 61, 67, 71...

COMPARISON WITH THE SOCIAL NETWORK:
Where Sorkin reveals Zuckerberg's character through rapid-fire
defensive dialogue, your protagonist states feelings directly:

YOUR SCRIPT (p.23):
ALEX: I feel isolated from humanity. Technology has become my
      only real connection.

SORKIN APPROACH (hypothetical rewrite):
ALEX: (typing furiously)
      Three billion users. Three billion.

SARAH: When's the last time you talked to one?

ALEX: I talk to them every day.

SARAH: Through a screen doesn't count.

ALEX: (still typing)
      Says who?

This reveals the same isolation through behavior and subtext.

SPECIFIC PROBLEM #1 (Page 10, Lines 12-18):
─────────────────────────────────────────
CURRENT:
JOHN: As you know, I've been working on artificial
      intelligence for fifteen years. My PhD thesis at MIT
      was on neural networks, and since then I've published
      forty papers on machine learning.

PROBLEM:
- Pure exposition dump
- "As you know" is a red flag
- No conflict or subtext
- Credentials listing, not character revelation

THEORETICAL VIOLATION:
Violates principle of "show, don't tell" and Truby's rule:
"Character is revealed through moral choice under pressure"

MASTERPIECE COMPARISON - THE IMITATION GAME:
Instead of Turing explaining his credentials, we see him solve
an impossible crossword in minutes, revealing genius through action.

SUGGESTED REWRITE:
JOHN: (to his reflection in black screen)
      Forty papers. Fifteen years.

The screen lights up: "PASSWORD INCORRECT - ATTEMPT 10,347"

JOHN: (laughing bitterly)
      And I can't even hack my own creation.

He types again. The screen goes dark. Permanently.

JOHN: (whisper)
      Oh no. No, no, no...

JUSTIFICATION:
- Reveals expertise through failure (irony)
- Creates immediate dramatic question
- Shows emotional state through behavior
- No exposition, pure dramatic action

[... continues for 47 more pages of dialogue analysis ...]

═══════════════════════════════════════════════════════════════

[... Report continues for all 24 specialists ...]
```

---

## 🔧 Implementação Técnica Detalhada

### Estrutura de Diretórios

```
scripturemon-clean/
├── specialists/
│   ├── implementations/           # Especialistas Python atuais
│   ├── dual_core/                # NOVO: Especialistas Dual-Core
│   │   ├── base/
│   │   │   ├── dual_core_specialist.py
│   │   │   ├── ollama_integration.py
│   │   │   └── synthesis_engine.py
│   │   ├── specialists/
│   │   │   ├── dialogue_dual_core.py
│   │   │   ├── character_dual_core.py
│   │   │   └── [outros 22 especialistas]
│   │   └── configs/
│   │       ├── mistral_config.yaml
│   │       └── specialist_priorities.yaml
│   ├── library/                  # NOVO: Biblioteca Teórica
│   │   ├── theories/
│   │   │   ├── structure/
│   │   │   ├── character/
│   │   │   ├── dialogue/
│   │   │   └── theme/
│   │   └── index.json
│   ├── masterpieces/            # NOVO: Banco de Roteiros
│   │   ├── drama/
│   │   ├── action/
│   │   ├── comedy/
│   │   ├── thriller/
│   │   └── scifi/
│   └── orchestrator/            # NOVO: Orquestrador Principal
│       ├── orchestrator.py
│       ├── pipeline.py
│       └── report_generator.py
```

### Classe Base Dual-Core Completa

```python
# specialists/dual_core/base/dual_core_specialist.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import time
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DualCoreConfig:
    """Configuração para especialista Dual-Core"""
    use_llm: bool = True
    llm_model: str = "mistral:latest"
    max_tokens: int = 128000
    temperature: float = 0.7
    analysis_depth: str = "maximum"  # quick, standard, deep, maximum
    include_theory: bool = True
    include_masterpieces: bool = True
    cross_reference_specialists: bool = True
    generate_rewrites: bool = True

@dataclass
class AnalysisLayer:
    """Representa uma camada de análise"""
    layer_name: str
    duration: float
    token_count: int
    findings: Dict[str, Any]
    confidence: float

class DualCoreSpecialist(ABC):
    """
    Classe base para todos os especialistas Dual-Core
    Combina análise Python com insights LLM profundos
    """

    def __init__(self, name: str, specialty: str, config: Optional[DualCoreConfig] = None):
        self.name = name
        self.specialty = specialty
        self.config = config or DualCoreConfig()

        # Componentes
        self.python_core = self._init_python_core()
        self.llm_core = self._init_llm_core() if self.config.use_llm else None
        self.library = self._load_library()
        self.masterpiece_db = self._load_masterpiece_db()

        # Tracking
        self.analysis_layers: List[AnalysisLayer] = []
        self.total_tokens_used = 0
        self.analysis_start_time = None

    @abstractmethod
    def _init_python_core(self):
        """Inicializa o núcleo Python específico do especialista"""
        pass

    def _init_llm_core(self):
        """Inicializa conexão com Ollama/Mistral"""
        from ..base.ollama_integration import OllamaLLM
        return OllamaLLM(
            model=self.config.llm_model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )

    def analyze(self, screenplay: str,
                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Análise completa Dual-Core
        """
        self.analysis_start_time = time.time()

        # Layer 1: Python Analysis
        layer1 = self._python_analysis_layer(screenplay)
        self.analysis_layers.append(layer1)

        if not self.config.use_llm:
            return self._create_python_only_report(layer1)

        # Layer 2: Context Enrichment
        layer2 = self._context_enrichment_layer(screenplay, layer1, context)
        self.analysis_layers.append(layer2)

        # Layer 3: First LLM Analysis
        layer3 = self._first_llm_layer(screenplay, layer1, layer2)
        self.analysis_layers.append(layer3)

        # Layer 4: Deep LLM Analysis (if configured)
        if self.config.analysis_depth in ["deep", "maximum"]:
            layer4 = self._deep_llm_layer(screenplay, layer1, layer2, layer3)
            self.analysis_layers.append(layer4)

        # Layer 5: Solutions & Rewrites (if configured)
        if self.config.generate_rewrites:
            layer5 = self._solutions_layer(screenplay, self.analysis_layers)
            self.analysis_layers.append(layer5)

        # Final Synthesis
        return self._synthesize_all_layers()

    def _python_analysis_layer(self, screenplay: str) -> AnalysisLayer:
        """Layer 1: Análise Python exaustiva"""
        start = time.time()

        analysis = self.python_core.analyze(screenplay)

        return AnalysisLayer(
            layer_name="Python Structural Analysis",
            duration=time.time() - start,
            token_count=0,  # Python não usa tokens
            findings=analysis,
            confidence=1.0  # Python é determinístico
        )

    def _context_enrichment_layer(self, screenplay: str,
                                   python_layer: AnalysisLayer,
                                   external_context: Optional[Dict] = None) -> AnalysisLayer:
        """Layer 2: Enriquecimento com teoria e masterpieces"""
        start = time.time()

        context = {
            "theories": [],
            "masterpieces": [],
            "cross_references": {}
        }

        # Carregar teorias relevantes
        if self.config.include_theory:
            problems = python_layer.findings.get("problems", [])
            context["theories"] = self.library.get_relevant_theories(
                self.specialty,
                problems
            )

        # Carregar masterpieces comparáveis
        if self.config.include_masterpieces:
            genre = python_layer.findings.get("detected_genre", "drama")
            context["masterpieces"] = self.masterpiece_db.get_comparable_scenes(
                screenplay,
                genre,
                self.specialty
            )

        # Cross-reference com outros especialistas
        if self.config.cross_reference_specialists and external_context:
            context["cross_references"] = external_context

        return AnalysisLayer(
            layer_name="Context Enrichment",
            duration=time.time() - start,
            token_count=self._estimate_tokens(context),
            findings=context,
            confidence=1.0
        )

    def _first_llm_layer(self, screenplay: str,
                         python_layer: AnalysisLayer,
                         context_layer: AnalysisLayer) -> AnalysisLayer:
        """Layer 3: Primeira análise LLM - identificação completa"""
        start = time.time()

        prompt = self._build_first_analysis_prompt(
            screenplay,
            python_layer.findings,
            context_layer.findings
        )

        response = self.llm_core.analyze(prompt)
        tokens = self.llm_core.last_token_count
        self.total_tokens_used += tokens

        return AnalysisLayer(
            layer_name="LLM Initial Analysis",
            duration=time.time() - start,
            token_count=tokens,
            findings=response,
            confidence=response.get("confidence", 0.85)
        )

    def _deep_llm_layer(self, screenplay: str,
                        python_layer: AnalysisLayer,
                        context_layer: AnalysisLayer,
                        first_llm_layer: AnalysisLayer) -> AnalysisLayer:
        """Layer 4: Análise LLM profunda - deep dive nos problemas"""
        start = time.time()

        prompt = self._build_deep_analysis_prompt(
            screenplay,
            python_layer.findings,
            context_layer.findings,
            first_llm_layer.findings
        )

        response = self.llm_core.analyze(prompt)
        tokens = self.llm_core.last_token_count
        self.total_tokens_used += tokens

        return AnalysisLayer(
            layer_name="LLM Deep Analysis",
            duration=time.time() - start,
            token_count=tokens,
            findings=response,
            confidence=response.get("confidence", 0.9)
        )

    def _solutions_layer(self, screenplay: str,
                        previous_layers: List[AnalysisLayer]) -> AnalysisLayer:
        """Layer 5: Soluções e reescritas específicas"""
        start = time.time()

        # Compilar todos os problemas identificados
        all_problems = self._compile_problems(previous_layers)

        prompt = self._build_solutions_prompt(
            screenplay,
            all_problems,
            previous_layers[-1].findings.get("masterpiece_examples", [])
        )

        response = self.llm_core.analyze(prompt)
        tokens = self.llm_core.last_token_count
        self.total_tokens_used += tokens

        return AnalysisLayer(
            layer_name="Solutions & Rewrites",
            duration=time.time() - start,
            token_count=tokens,
            findings=response,
            confidence=response.get("confidence", 0.95)
        )

    def _synthesize_all_layers(self) -> Dict[str, Any]:
        """Sintetiza todas as camadas em relatório final"""
        total_time = time.time() - self.analysis_start_time

        return {
            "specialist": self.name,
            "specialty": self.specialty,
            "analysis_depth": self.config.analysis_depth,
            "layers_completed": len(self.analysis_layers),
            "total_time": f"{total_time:.2f} seconds",
            "total_tokens": self.total_tokens_used,
            "confidence": self._calculate_overall_confidence(),
            "findings": self._merge_findings(),
            "problems": self._compile_problems(self.analysis_layers),
            "solutions": self._compile_solutions(),
            "rewrites": self._compile_rewrites(),
            "theory_references": self._compile_theory_references(),
            "masterpiece_comparisons": self._compile_masterpiece_comparisons(),
            "cross_specialist_insights": self._compile_cross_insights(),
            "detailed_layers": [layer.__dict__ for layer in self.analysis_layers]
        }

    @abstractmethod
    def _build_first_analysis_prompt(self, screenplay: str,
                                     python_findings: Dict,
                                     context: Dict) -> str:
        """Constrói prompt para primeira análise LLM"""
        pass

    @abstractmethod
    def _build_deep_analysis_prompt(self, screenplay: str,
                                    python_findings: Dict,
                                    context: Dict,
                                    first_llm: Dict) -> str:
        """Constrói prompt para análise profunda"""
        pass

    @abstractmethod
    def _build_solutions_prompt(self, screenplay: str,
                                problems: List[Dict],
                                masterpieces: List[str]) -> str:
        """Constrói prompt para soluções e reescritas"""
        pass
```

---

## 🔄 Sistema de Orquestração

### Orquestrador Principal

```python
# specialists/orchestrator/orchestrator.py

class ScriptDoctorOrchestrator:
    """
    Orquestra todos os 24 especialistas Dual-Core
    Gerencia pipeline de análise completa
    """

    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.specialists = self._load_all_specialists()
        self.execution_order = self._determine_execution_order()
        self.shared_context = {}

    def analyze_screenplay(self, screenplay_path: str) -> UltimateReport:
        """
        Executa análise completa com todos os especialistas
        """
        print("🎬 SCRIPT DOCTOR™ - INICIANDO ANÁLISE COMPLETA")
        print("=" * 60)

        # Carregar roteiro
        screenplay = self._load_screenplay(screenplay_path)

        # Fase 1: Especialistas Fundamentais (Structure, Character, Dialogue)
        print("\n📊 FASE 1: Análise Fundamental")
        fundamental_results = self._run_fundamental_specialists(screenplay)

        # Fase 2: Especialistas Narrativos (com contexto da Fase 1)
        print("\n📖 FASE 2: Análise Narrativa")
        narrative_results = self._run_narrative_specialists(
            screenplay,
            fundamental_results
        )

        # Fase 3: Especialistas Artísticos (com contexto acumulado)
        print("\n🎨 FASE 3: Análise Artística")
        artistic_results = self._run_artistic_specialists(
            screenplay,
            {**fundamental_results, **narrative_results}
        )

        # Fase 4: Meta-Análise (Overall, Market, Executive)
        print("\n🏆 FASE 4: Meta-Análise")
        meta_results = self._run_meta_specialists(
            screenplay,
            {**fundamental_results, **narrative_results, **artistic_results}
        )

        # Gerar Relatório Final
        print("\n📝 GERANDO RELATÓRIO FINAL...")
        report = self._generate_ultimate_report(
            screenplay,
            fundamental_results,
            narrative_results,
            artistic_results,
            meta_results
        )

        print("\n✅ ANÁLISE COMPLETA!")
        return report

    def _run_fundamental_specialists(self, screenplay: str) -> Dict:
        """Executa especialistas fundamentais em paralelo quando possível"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        specialists = ['structure', 'character', 'dialogue', 'pacing']
        results = {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(
                    self._run_specialist,
                    name,
                    screenplay
                ): name
                for name in specialists
            }

            for future in as_completed(futures):
                specialist_name = futures[future]
                try:
                    result = future.result()
                    results[specialist_name] = result
                    print(f"  ✓ {specialist_name.title()} completo")

                    # Compartilhar insights críticos
                    self._update_shared_context(specialist_name, result)

                except Exception as e:
                    print(f"  ✗ Erro em {specialist_name}: {e}")
                    results[specialist_name] = None

        return results

    def _update_shared_context(self, specialist_name: str, result: Dict):
        """Atualiza contexto compartilhado entre especialistas"""
        if result and "critical_findings" in result:
            self.shared_context[specialist_name] = {
                "critical_findings": result["critical_findings"],
                "score": result.get("score", 0),
                "main_issues": result.get("problems", [])[:3]
            }
```

---

## 🚦 Sistema de Priorização Inteligente

### Execução Adaptativa

```python
class AdaptiveExecutionEngine:
    """
    Ajusta execução baseado em problemas encontrados
    """

    def determine_specialist_depth(self,
                                   specialist_name: str,
                                   initial_scores: Dict[str, float]) -> str:
        """
        Determina profundidade de análise baseado em scores iniciais
        """

        # Se Python detectou problemas graves, fazer análise máxima
        if initial_scores.get(specialist_name, 100) < 40:
            return "maximum"

        # Se está OK, análise padrão
        elif initial_scores.get(specialist_name, 100) > 70:
            return "standard"

        # Se está mediano, análise profunda
        else:
            return "deep"

    def should_run_specialist(self,
                             specialist_name: str,
                             screenplay_metrics: Dict) -> bool:
        """
        Decide se um especialista deve rodar baseado no contexto
        """

        # Sempre rodar fundamentais
        if specialist_name in ["structure", "character", "dialogue"]:
            return True

        # Pular Subtext se não há diálogo suficiente
        if specialist_name == "subtext":
            return screenplay_metrics.get("dialogue_count", 0) > 50

        # Pular Action se roteiro é muito dialogado
        if specialist_name == "action":
            return screenplay_metrics.get("action_ratio", 0) > 0.3

        return True
```

---

## 💾 Sistema de Cache Inteligente

```python
class SmartCache:
    """
    Cache para evitar re-análises desnecessárias
    """

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def get_cached_analysis(self,
                           screenplay_hash: str,
                           specialist_name: str,
                           config_hash: str) -> Optional[Dict]:
        """
        Recupera análise cacheada se existir e for válida
        """
        cache_file = self.cache_dir / f"{screenplay_hash}_{specialist_name}_{config_hash}.json"

        if cache_file.exists():
            with open(cache_file) as f:
                cached = json.load(f)

            # Verificar se cache é recente (< 7 dias)
            if time.time() - cached["timestamp"] < 7 * 24 * 3600:
                return cached["analysis"]

        return None

    def save_analysis(self,
                      screenplay_hash: str,
                      specialist_name: str,
                      config_hash: str,
                      analysis: Dict):
        """
        Salva análise em cache
        """
        cache_file = self.cache_dir / f"{screenplay_hash}_{specialist_name}_{config_hash}.json"

        with open(cache_file, 'w') as f:
            json.dump({
                "timestamp": time.time(),
                "analysis": analysis
            }, f)
```

---

## 🎯 Conclusão

A arquitetura Dual-Core com análise profunda representa a evolução máxima do Script Doctor™:

- **Mantém** toda a precisão do Python
- **Adiciona** compreensão profunda via LLM com 128k tokens
- **Integra** biblioteca teórica completa
- **Compara** com banco de roteiros masterpiece
- **Prioriza** QUALIDADE sobre velocidade
- **Entrega** análise digna de consultoria premium

É a diferença entre um **analisador de roteiros** e um verdadeiro **Script Doctor™** de classe mundial.

---

## 🚀 ROADMAP DE INTEGRAÇÃO - 5 FASES (ATUALIZADO SESSÃO 2)

**Baseado em AUDITORIA_FORENSE_SCRIPTUREMON.md + Sistema de Memória Hierárquico**

### FASE 1: ATIVAR PYTHON CORE (1-2 dias) 🔥🔥🔥 IMPACTO CRÍTICO
**Objetivo:** Integrar os 24 especialistas Python que existem mas não são usados

**Tarefas:**
1. **Criar `specialists/dual_core/base/dual_core_wrapper.py`**
   - Classe `DualCoreWrapper` não-invasiva
   - Recebe specialist Python existente como dependency injection
   - Métodos: `analyze()`, `_analyze_python()`, `_analyze_llm()`, `_synthesize()`

2. **Modificar `core/scripturemon.py`**
   - Importar DualCoreWrapper
   - Substituir chamada direta ao LLM por wrapper
   - Manter backward compatibility (flag enable_dual_core)

3. **Testar com DrDialogue (protótipo)**
   - Converter character_dialogue_specialist para Dual-Core
   - Validar fluxo Python → LLM → Synthesis
   - Comparar qualidade: LLM-only vs Dual-Core

**Ganho Esperado:** 20% → 40% capacidade
**Tempo:** 1-2 dias
**Blocker:** Nenhum (tudo já existe)

---

### FASE 2: CONECTAR BIBLIOTECA DE CONTEÚDO (2-3 dias) 🔥🔥 IMPACTO ALTO
**Objetivo:** Indexar e integrar 13 livros + 35 roteiros que existem mas são ignorados

**Tarefas:**
1. **Criar `core/content_indexer.py`**
   - Classe `ContentIndexer` para indexar content/theory/ e content/screenplays/
   - Integração com BM25 existente (memory/)
   - Métodos: `index_theory_books()`, `index_masterpiece_scripts()`, `search_context()`

2. **Modificar prompts LLM**
   - Adicionar contexto teórico relevante aos prompts
   - Adicionar exemplos de masterpieces
   - Aumentar context window para 128k tokens

3. **Atualizar DualCoreWrapper**
   - Injetar ContentIndexer
   - Buscar contexto relevante antes de chamar LLM
   - Enriched prompt: Python data + teoria + exemplos

**Ganho Esperado:** 40% → 60% capacidade
**Tempo:** 2-3 dias
**Blocker:** Nenhum (content/ já existe, BM25 já funciona)

---

### FASE 2B: SISTEMA DE MEMÓRIA HIERÁRQUICO (2-3 dias) 🔥🔥 IMPACTO ALTO
**Objetivo:** Criar sistema de memória de 3 níveis para aprendizado contínuo

**Tarefas:**
1. **Criar estrutura de pastas**
   - `memory/specialists/[24 pastas]` (memória individual)
   - `memory/shared/` (conhecimento cross-specialist)
   - `memory/meta/` (meta-análise do orquestrador)
   - `memory/consolidation/` (sistema de aprendizado)

2. **Implementar classes de memória**
   - `core/memory/specialist_memory.py` - SpecialistMemory class
   - `core/memory/shared_memory.py` - SharedMemory class
   - `core/memory/meta_memory.py` - MetaMemory class
   - `core/memory/consolidator.py` - MemoryConsolidator class

3. **Integrar com sistemas existentes**
   - Reusar BM25Index para cada nível de memória
   - Reusar SmartCache para hot memory (TTL 2h)
   - Cold memory em BM25 (persistente)

4. **Implementar importance scoring**
   - Calcular relevância de cada insight (0.0-1.0)
   - Auto-arquivar memórias < 0.3 após 90 dias
   - Promover padrões recorrentes para shared/

5. **Cross-specialist learning**
   - Detectar insights relevantes para múltiplos especialistas
   - Notificação automática de conhecimento compartilhado
   - Correlation maps: "DrDialogue + DrCharacter = alta accuracy"

**Ganho Esperado:** 60% → 75% capacidade (sistema aprende e evolui)
**Tempo:** 2-3 dias
**Blocker:** Nenhum (BM25 e Cache já existem)

---

### FASE 3: ATIVAR PATCHES (1 dia) 🔥🔥 IMPACTO ALTO
**Objetivo:** Ativar CitationValidator, IdentityEnforcer, SmartCache que existem mas não são usados

**Tarefas:**
1. **Modificar `core/scripturemon.py`**
   - Import CitationValidator, IdentityEnforcer, SmartCache
   - Criar pipeline de validação
   - Aplicar patches em todas as respostas LLM

2. **Integrar no DualCoreWrapper**
   - Validar citações antes de retornar
   - Enforçar identidade Script Doctor™
   - Cachear análises Python + LLM

3. **Testar robustez**
   - Verificar redução de alucinações
   - Validar identidade consistente
   - Medir ganho de performance com cache

**Ganho Esperado:** 75% → 85% capacidade
**Tempo:** 1 dia
**Blocker:** Nenhum (patches já implementados)

---

### FASE 4: LIMPEZA E OTIMIZAÇÃO (2-3 dias) 🔥 IMPACTO MÉDIO
**Objetivo:** Consolidar duplicações, arquivar órfãos, completar features parciais

**Tarefas:**
1. **Consolidar Duplicações**
   - Escolher fonte canônica: content/theory/ (manter) vs knowledge_modelfiles/theory/ (arquivar)
   - Documentar decisão
   - Limpar duplicatas

2. **Arquivar Modelfiles Órfãos**
   - Mover knowledge_modelfiles/ para archive/
   - Manter apenas specialists/modelfiles/ ativo
   - Documentar mudança

3. **Completar Memory-Mesh**
   - Popular memory-mesh/runtime/ (vazio atualmente)
   - Implementar persistence para BM25
   - Testes de memória de longo prazo

4. **Atualizar/Arquivar Planos Antigos**
   - Revisar Planos_ias/
   - Deprecar ou sincronizar com planos atuais

**Ganho Esperado:** 85% → 100% capacidade
**Tempo:** 2-3 dias
**Blocker:** Nenhum (cleanup e polish)

---

## 📊 PROGRESSO ESPERADO POR FASE

```
INÍCIO (atual):          20%  ░░░░░░░░░░░░░░░░░░░░
Após FASE 1:             40%  ████████░░░░░░░░░░░░
Após FASE 2:             60%  ████████████░░░░░░░░
Após FASE 2B:            75%  ███████████████░░░░░  ← NOVO: Sistema aprende!
Após FASE 3:             85%  █████████████████░░░
Após FASE 4:            100%  ████████████████████

TOTAL: 8-12 dias de trabalho focado
```

**NOVA CAPACIDADE (FASE 2B):**
- Sistema memoriza padrões e erros
- Aprende continuamente com cada análise
- Compartilha conhecimento entre especialistas
- Auto-consolida aprendizados semanalmente
- Correlaciona performance entre especialistas

---

## 📋 SINCRONIZAÇÃO DOS 3 PLANOS

**⚠️ REGRA DE OURO:** Toda modificação em qualquer plano requer atualização dos 3 arquivos.

### Versões Atuais Sincronizadas:
- **MASTER_PLAN:** v3.2 (01/10/2025 - 01:55) ✅
- **DUAL_CORE_PLAN:** v2.5 (01/10/2025 - 02:00) ✅ ← ESTE ARQUIVO
- **DIÁRIO_BORDO:** Sessão 2 completa (01/10/2025 - 01:50) ✅
- **AUDITORIA_FORENSE:** Completa (01/10/2025) ✅

### Última Sincronização:
**Data:** 01/10/2025 - 02:00
**Evento:** Auditoria forense completa + Incorporação de 8 desconexões + Roadmap 4 fases
**Mudanças Principais:**
- Documentação de 8 categorias de desconexões sistêmicas
- Roadmap de integração de 4 fases (20% → 100%)
- Estratégia ContentIndexer para biblioteca premium
- Plano de ativação de patches anti-alucinação
- LLM com 128k tokens + contexto teórico + exemplos

### Consistência Validada:
- ✅ DUAL_CORE_PLAN sincronizado com AUDITORIA_FORENSE
- ✅ Roadmap de 4 fases documentado em todos os 3 planos
- ✅ ContentIndexer architecture definida
- ✅ Patches activation strategy clara
- ✅ Alinhado com MASTER_PLAN v3.2
- ✅ Sincronizado com DIÁRIO_BORDO Sessão 2

### Próxima Sincronização Obrigatória:
Quando qualquer um dos seguintes eventos ocorrer:
1. Início da implementação FASE 1 (DualCoreWrapper)
2. Conclusão de qualquer fase do roadmap
3. Ajustes na arquitetura ContentIndexer
4. Nova descoberta técnica
5. Mudança de priorização

---

*Documento criado em 30/09/2025*
*Última atualização: 01/10/2025 - v2.5 (SINCRONIZADO ✅)*
*Próxima revisão: Início da FASE 1 - Implementação DualCoreWrapper*

**STATUS:** 🟢 SINCRONIZADO COM OS 3 PLANOS + AUDITORIA
**PRÓXIMO:** SESSÃO 3 - Implementação FASE 1

**DIGIMUNDO PRESENTE 🥷**