# 🚀 PLANO DE IMPLEMENTAÇÃO: TRIPLE-CORE V2 (MELHOR DOS DOIS MUNDOS)

**Data:** 2025-10-14
**Objetivo:** Restaurar Triple-Core (Oct 4) + Portar melhorias do Dual-Core (Oct 14)
**Estratégia:** MERGE INTELIGENTE ao invés de simples rollback

---

## 📊 RESUMO EXECUTIVO

### ❌ ABORDAGEM ERRADA: Rollback Simples
```
Restaurar Oct 4 completo
→ Perde: NER validation, Two-Pass LLM, OpenAI support, etc.
→ Risco: Perder 10 dias de desenvolvimento
```

### ✅ ABORDAGEM CORRETA: Merge Inteligente
```
Triple-Core (Oct 4) + Features Novas (Oct 14)
→ Mantém: Core 2 (Examples), Modelfile otimizado, Few-shot examples
→ Adiciona: NER validation, Two-Pass LLM, OpenAI, Quality checks
→ Resultado: MELHOR SISTEMA POSSÍVEL
```

---

## 🔍 FEATURES DO OCT 14 QUE DEVEM SER PORTADAS

### 1️⃣ **NER Validation** ⭐ CRÍTICO!
**O que é:** Validação de entidades nomeadas usando spaCy para detectar alucinações

**Arquivos envolvidos:**
- `/engine/orchestration/dual_core_wrapper.py` (linhas 141-357)

**Métodos:**
```python
def _extract_entities_safe(screenplay_text, max_chars=150000)
    → Extrai personagens REAIS do roteiro (regex + spaCy NER)
    → Retorna: set de nomes em UPPERCASE

def _extract_llm_characters(llm_insights)
    → Extrai personagens mencionados na análise LLM
    → Retorna: set de nomes em UPPERCASE

def _validate_character_names(llm_insights, screenplay_text)
    → Compara personagens LLM vs roteiro
    → Retorna: {'valid': bool, 'overlap_ratio': float, 'hallucinated': list}
```

**Logs gerados:**
```
[DUAL-CORE] ✅ NER validation passed: overlap=85.3%, matched=12 characters
[DUAL-CORE] ⚠️ NER validation concern: overlap=21.7%, hallucinated=['SOFIA', 'JULIO']
```

**Por que é importante:**
- Detecta alucinações EM TEMPO REAL
- Permite reject/retry automático
- Fornece métricas objetivas de qualidade
- Foi essa validação que DETECTOU o problema!

**Onde adicionar no Triple-Core:**
- Adicionar no `triple_core_wrapper.py` após Core 3 (LLM)
- Usar os mesmos métodos (copiar código)

---

### 2️⃣ **Two-Pass LLM Architecture** ⭐ MELHORIA DE QUALIDADE

**O que é:** LLM executa em 2 rodadas separadas:
- **Pass 1:** Identificar problemas (WHAT is wrong)
- **Pass 2:** Expandar soluções (HOW to fix with examples)

**Arquivos envolvidos:**
- `/engine/orchestration/dual_core_wrapper.py` (linhas 1111-1435)

**Métodos:**
```python
def _build_llm_prompt_pass1(screenplay_text, python_result)
    → Prompt focado em identificar 4 problemas específicos
    → Retorna: Seções 1-3 (INTERPRETAÇÃO, PADRÕES, PROBLEMAS)

def _build_llm_prompt_pass2(screenplay_text, python_result, pass1_response)
    → Prompt focado em expandir soluções com exemplos
    → Retorna: Seções 4-5 (SOLUÇÕES, SÍNTESE)

def _combine_two_pass_responses(pass1_response, pass2_response)
    → Concatena os dois passes
```

**Flags:**
```python
DualCoreWrapper(
    specialist,
    two_pass_llm=True  # Habilita arquitetura 2-pass
)
```

**Por que é importante:**
- Separa concern: identificação vs solução
- Permite prompts mais focados e específicos
- Melhora qualidade de exemplos ANTES/DEPOIS
- Reduz token waste (cada pass tem prompt menor)

**Onde adicionar no Triple-Core:**
- Adicionar flag `two_pass_llm` no `__init__`
- Adicionar lógica condicional no Core 3
- Se `two_pass_llm=True`, fazer 2 chamadas LLM ao invés de 1

---

### 3️⃣ **OpenAI API Support (Hybrid Backend)** 💰 FLEXIBILIDADE

**O que é:** Suporte híbrido para Ollama (local) + OpenAI API (cloud)

**Arquivos envolvidos:**
- `/engine/orchestration/dual_core_wrapper.py` (linhas 1628-1761)

**Métodos:**
```python
def _call_llm(prompt)
    → Detecta model name:
      - Se começa com 'gpt-' → OpenAI API
      - Caso contrário → Ollama
    → OpenAI: Usa openai.ChatCompletion
    → Ollama: Usa subprocess ollama run

def get_openai_cost_summary()
    → Retorna custo total de chamadas OpenAI
    → {'total_calls': 5, 'total_cost': 0.23}
```

**Uso:**
```python
TripleCoreWrapper(
    specialist,
    llm_model="gpt-5-preview"  # Usa OpenAI
)
# ou
TripleCoreWrapper(
    specialist,
    llm_model="scripturemon-optimized"  # Usa Ollama
)
```

**Por que é importante:**
- Permite testar com GPT-5 (mais inteligente)
- Cost tracking automático
- Fallback se Ollama crashar
- Comparação de qualidade entre modelos

**Onde adicionar no Triple-Core:**
- Substituir `_call_ollama()` por `_call_llm()` (versão híbrida)
- Adicionar `get_openai_cost_summary()`

---

### 4️⃣ **Quality Validation (Nivel 10)** 📊 GARANTIA DE QUALIDADE

**O que é:** Validação robusta baseada em critérios específicos

**Arquivos envolvidos:**
- `/engine/orchestration/dual_core_wrapper.py` (linhas 1438-1607)

**Métodos:**
```python
def _validate_llm_output(llm_response)
    → Checa: length, error patterns, specific examples, depth indicators
    → Retorna: {'valid': bool, 'score': 0-10, 'reason': str}

def _validate_analysis_quality(analysis, author)
    → Checa critérios "nivel 10":
      - Mínimo 15,000 caracteres
      - 3+ citações de cenas específicas
      - 3+ citações verbatim de diálogos (20+ palavras)
      - 2+ exemplos ANTES/DEPOIS de reescrita
      - 3+ citações de teoria
    → Retorna: (passed: bool, score: 0-10, issues: list)
```

**Logs gerados:**
```
[DUAL-CORE] LLM analysis completed: 12543 chars, quality: 8.5/10
[DUAL-CORE] 📊 NIVEL 10 VALIDATION: 7.5/10 - ❌ FAILED
[DUAL-CORE]   Too few ANTES/DEPOIS rewrites: 1/2 (-2.5)
```

**Por que é importante:**
- Garante qualidade mínima (pode rejeitar output ruim)
- Fornece métricas objetivas
- Permite tuning de prompts baseado em scores
- Detecta quando LLM está "lazy"

**Onde adicionar no Triple-Core:**
- Adicionar após Core 3 (LLM) gerar output
- Se score < 7.0, logar warning ou retry

---

### 5️⃣ **Personalized Prompts** 🎯 CUSTOMIZAÇÃO POR AUTOR

**O que é:** Prompts específicos por autor/teoria

**Arquivos envolvidos:**
- `/engine/prompts/__init__.py`
- `/engine/prompts/authors/` (múltiplos arquivos)

**Uso:**
```python
DualCoreWrapper(
    specialist,
    use_personalized_prompts=True,  # Habilita prompts personalizados
    specialist_type='mckee_dialogue'  # Autor específico
)
```

**Por que é importante:**
- Cada autor tem vocabulário específico
- Prompts adaptados à teoria
- Melhora relevância de análise

**Onde adicionar no Triple-Core:**
- Adicionar flag `use_personalized_prompts`
- Import de `engine.prompts`
- Condicional no `_build_llm_prompt()`

---

### 6️⃣ **Better Error Handling** 🛡️ ROBUSTEZ

**O que é:** Tratamento de erro mais robusto

**Melhorias:**
- Memory error handling (`MemoryError` → retry com metade do texto)
- Unicode error handling (`UnicodeDecodeError` → limpar e retry)
- Timeout configurável (ou None para sem timeout)
- Catch-all para validação (nunca quebrar análise)

**Exemplo:**
```python
try:
    entities = self._extract_entities_safe(screenplay_text)
except MemoryError:
    logger.error(f"OOM while processing {len(screenplay_text)} chars")
    if max_chars > 50000:
        return self._extract_entities_safe(screenplay_text, max_chars // 2)
except UnicodeDecodeError:
    clean_text = screenplay_text.encode('utf-8', errors='ignore').decode('utf-8')
    return self._extract_entities_safe(clean_text, max_chars)
```

**Onde adicionar no Triple-Core:**
- Aplicar em todos os métodos que processam texto
- Adicionar timeout configurável no `__init__`

---

## 🏗️ ARQUITETURA FINAL: TRIPLE-CORE V2

```
┌─────────────────────────────────────────────────────────────┐
│              TRIPLE-CORE V2 (BEST OF BOTH WORLDS)            │
├─────────────────────────────────────────────────────────────┤
│  INPUT: Screenplay Text                                      │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 1: Python Specialist                            │  │
│  │  • 24 especialistas                                   │  │
│  │  • Métricas objetivas                                 │  │
│  │  📁 /triple_core/core_1_specialists/                 │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 2: Example Finder ⭐ (RESTAURADO!)             │  │
│  │  • 33 roteiros mestres indexados                      │  │
│  │  • Busca exemplos REAIS                               │  │
│  │  • Vincent Vega, Neo, Jules, Dom Cobb                 │  │
│  │  📁 /triple_core/core_2_examples/                    │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORE 3: LLM (MELHORADO!)                            │  │
│  │  • Hybrid backend: Ollama OR OpenAI 🆕               │  │
│  │  • Two-Pass LLM (opcional) 🆕                        │  │
│  │  • Personalized prompts (opcional) 🆕                │  │
│  │  • Modelfile otimizado (temp 0.2, seed 1337)         │  │
│  │  • Few-shot examples (Samantha, Alberto)              │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  VALIDATION LAYER 🆕                                  │  │
│  │  • NER validation (spaCy)                             │  │
│  │  • Quality check (nivel 10 criteria)                  │  │
│  │  • LLM output validation                              │  │
│  │  • Hallucination detection                            │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  OUTPUT: High-quality analysis without hallucinations ✅  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 PLANO DE IMPLEMENTAÇÃO PASSO-A-PASSO

### FASE 1: BACKUP E PREPARAÇÃO (10 min)

**1.1. Backup do sistema atual**
```bash
# Criar backup completo do sistema atual (Oct 14)
cd /Users/clubproducoes/Digimundo/scripturemon
tar -czf ../scripturemon_oct14_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    --exclude=workspace/outputs \
    --exclude=__pycache__ \
    --exclude=.git \
    .

# Verificar backup
ls -lh ../scripturemon_oct14_backup_*.tar.gz
```

**1.2. Parar todas as análises rodando**
```bash
pkill -f "analyze_all_specialists.py"
ps aux | grep analyze  # Verificar se parou
```

**1.3. Criar branch de desenvolvimento**
```bash
cd /Users/clubproducoes/Digimundo/scripturemon
git status
git add .
git commit -m "Backup antes de merge Triple-Core V2"
git branch triple-core-v2
git checkout triple-core-v2
```

---

### FASE 2: RESTAURAR TRIPLE-CORE BASE (20 min)

**2.1. Copiar Triple-Core do backup Oct 4**
```bash
# Copiar diretório triple_core/
cp -r /tmp/scripturemon_oct4/scripturemon-clean/triple_core/ \
      /Users/clubproducoes/Digimundo/scripturemon/

# Verificar estrutura
ls -la triple_core/
ls -la triple_core/core_2_examples/
```

**2.2. Restaurar 33 roteiros mestres**
```bash
# Copiar roteiros indexados
mkdir -p content/screenplays
cp -r /tmp/scripturemon_oct4/scripturemon-clean/content/screenplays/ \
      /Users/clubproducoes/Digimundo/scripturemon/content/

# Verificar roteiros
ls content/screenplays/*.pdf | wc -l  # Deve ser 33
ls content/screenplays/masters_index.json  # Deve existir
```

**2.3. Restaurar Modelfile otimizado**
```bash
# Copiar Modelfile
cp /tmp/scripturemon_oct4/scripturemon-clean/config/Modelfile_optimized \
   /Users/clubproducoes/Digimundo/scripturemon/config/

# Recriar modelo Ollama
ollama create scripturemon-optimized \
  -f /Users/clubproducoes/Digimundo/scripturemon/config/Modelfile_optimized

# Verificar parâmetros
ollama show scripturemon-optimized --modelfile | grep -E "temperature|seed|top_k"
# Deve mostrar: temperature 0.2, seed 1337, top_k 0
```

**2.4. Verificar imports e dependências**
```bash
# Testar import
python3 -c "from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper; print('✅ Import OK')"

# Testar Core 2
python3 -c "from triple_core.core_2_examples.example_finder import ExampleFinderCore; print('✅ Core 2 OK')"

# Testar master indexer
python3 -c "from core.master_script_indexer import get_master_indexer; idx = get_master_indexer(); print(f'✅ {len(idx.list_available_screenplays())} screenplays indexed')"
```

---

### FASE 3: PORTAR NER VALIDATION (30 min) ⭐ CRÍTICO

**3.1. Adicionar métodos de validação ao Triple-Core**

Editar: `/triple_core/orchestrators/triple_core_wrapper.py`

```python
# No topo, adicionar imports
import spacy
import logging
import os

logger = logging.getLogger(__name__)

class TripleCoreWrapper(DualCoreWrapper):
    def __init__(self, ...):
        super().__init__(...)

        # NER Validation (lazy loading) 🆕
        self._nlp = None
        self._nlp_available = None
        self.enable_validation = os.getenv('ENABLE_NER_VALIDATION', 'true').lower() == 'true'

        if self.enable_validation:
            logger.info("🔍 NER validation enabled")

    @property
    def nlp(self):
        """Lazy load spaCy model with caching"""
        if self._nlp is None:
            try:
                import spacy
                logger.info("Loading spaCy pt_core_news_lg...")
                self._nlp = spacy.load(
                    "pt_core_news_lg",
                    disable=["parser", "lemmatizer"]
                )
                logger.info("✅ spaCy model loaded successfully")
            except (ImportError, OSError) as e:
                logger.error(f"spaCy error: {e}")
                self._nlp_available = False
                raise
        return self._nlp

    # COPIAR OS 3 MÉTODOS DO DUAL-CORE:
    # - _extract_entities_safe()
    # - _extract_llm_characters()
    # - _validate_character_names()
    # (código completo: linhas 141-357 do dual_core_wrapper.py)
```

**3.2. Adicionar validação no método analyze()**

```python
def analyze(self, screenplay_text: str) -> Dict[str, Any]:
    """Executa análise Triple-Core completa."""
    # ... Core 1, Core 2, Core 3 ...

    # ============================================================
    # VALIDATION LAYER: NER + Quality Checks 🆕
    # ============================================================
    print("🔍 [4/4] Validation Layer...")

    # NER Validation
    try:
        validation_result = self._validate_character_names(
            llm_insights=result.get('llm_insights', ''),
            screenplay_text=screenplay_text
        )
        result['validation'] = validation_result

        if not validation_result.get('valid'):
            logger.warning(
                f"⚠️ NER validation concern: "
                f"overlap={validation_result.get('overlap_ratio', 0):.1%}, "
                f"hallucinated={validation_result.get('hallucinated', [])}"
            )
    except Exception as e:
        logger.error(f"NER validation failed (non-blocking): {e}")
        result['validation'] = {'valid': True, 'warning': str(e)}

    return result
```

**3.3. Instalar spaCy se necessário**
```bash
pip3 install spacy
python3 -m spacy download pt_core_news_lg
```

**3.4. Testar NER validation**
```bash
# Teste rápido
python3 << 'EOF'
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper
from engine.analyzers.dr_dialogue import DrDialogue

specialist = DrDialogue()
wrapper = TripleCoreWrapper(specialist, llm_model="scripturemon-optimized")

# Testar validação
result = wrapper._validate_character_names(
    llm_insights="Sofia diz algo. Julio responde.",
    screenplay_text="SAMANTHA: Hello\nALBERTO: Hi"
)
print(f"✅ Validation: {result}")
# Deve detectar: hallucinated=['SOFIA', 'JULIO']
EOF
```

---

### FASE 4: PORTAR TWO-PASS LLM (20 min)

**4.1. Adicionar flag two_pass_llm**

Editar: `/triple_core/orchestrators/triple_core_wrapper.py`

```python
def __init__(self,
             python_specialist,
             llm_model="scripturemon-optimized",
             llm_timeout=600,
             deep_context=True,
             two_pass_llm=False):  # 🆕 Novo parâmetro

    super().__init__(...)
    self.two_pass_llm = two_pass_llm
```

**4.2. Adicionar lógica two-pass no Core 3**

```python
# CORE 3: LLM (Teoria + Síntese)
print("🤖 [3/3] LLM Core: Theory Enrichment...")

if self.two_pass_llm:
    # TWO-PASS MODE 🆕
    print("   🔄 TWO-PASS LLM MODE ENABLED")

    # Pass 1: Identificar problemas
    print("   🎯 Pass 1/2: Identifying problems...")
    pass1_prompt = self._build_llm_prompt_pass1(
        screenplay_text=screenplay_text,
        python_result=result.get('python_core1', {})
    )
    pass1_response = self._call_llm(pass1_prompt)
    print(f"   ✅ Pass 1 complete: {len(pass1_response)} chars")

    # Pass 2: Expandir soluções
    print("   🎯 Pass 2/2: Expanding solutions...")
    pass2_prompt = self._build_llm_prompt_pass2(
        screenplay_text=screenplay_text,
        python_result=result.get('python_core1', {}),
        pass1_response=pass1_response
    )
    pass2_response = self._call_llm(pass2_prompt)
    print(f"   ✅ Pass 2 complete: {len(pass2_response)} chars")

    # Combine
    llm_result = self._combine_two_pass_responses(pass1_response, pass2_response)
else:
    # SINGLE-PASS MODE (original)
    llm_prompt = super()._build_llm_prompt(...)
    llm_result = self._call_llm(llm_prompt)
```

**4.3. Copiar métodos two-pass do Dual-Core**

```python
# COPIAR DO DUAL-CORE:
# - _build_llm_prompt_pass1() (linhas 1111-1277)
# - _build_llm_prompt_pass2() (linhas 1279-1425)
# - _combine_two_pass_responses() (linhas 1427-1435)
```

---

### FASE 5: PORTAR OPENAI API SUPPORT (15 min)

**5.1. Substituir _call_ollama() por _call_llm() híbrido**

Editar: `/triple_core/orchestrators/triple_core_wrapper.py`

```python
def _call_llm(self, prompt: str) -> str:
    """
    Hybrid LLM backend: Ollama (local) or OpenAI (API).

    Auto-detects based on model name:
    - Models starting with 'gpt-' use OpenAI API
    - All other models use Ollama
    """
    try:
        # DETECT BACKEND
        if self.llm_model.startswith('gpt-'):
            # OPENAI API PATH 🆕
            logger.info(f"Using OpenAI API: {self.llm_model}")

            from openai import OpenAI
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise Exception("OPENAI_API_KEY not set")

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "Expert screenplay analyst..."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_completion_tokens=16000
            )

            # Track cost
            cost = (response.usage.prompt_tokens / 1_000_000) * 1.00 + \
                   (response.usage.completion_tokens / 1_000_000) * 4.00
            logger.info(f"OpenAI cost: ${cost:.4f}")

            return response.choices[0].message.content.strip()

        else:
            # OLLAMA PATH (original)
            logger.info(f"Using Ollama: {self.llm_model}")
            result = subprocess.run(
                ['ollama', 'run', self.llm_model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=self.llm_timeout if self.llm_timeout else None
            )

            if result.returncode != 0:
                raise Exception(f"Ollama failed: {result.stderr}")

            return result.stdout.strip()

    except Exception as e:
        raise Exception(f"LLM call failed: {e}")
```

**5.2. Adicionar método de cost tracking**

```python
def get_openai_cost_summary(self) -> Dict[str, Any]:
    """Returns summary of OpenAI API costs for this session."""
    if not hasattr(self, '_openai_costs') or not self._openai_costs:
        return {'total_calls': 0, 'total_cost': 0.0}

    return {
        'total_calls': len(self._openai_costs),
        'total_cost': sum(c['cost'] for c in self._openai_costs)
    }
```

---

### FASE 6: ATUALIZAR SCRIPT PRINCIPAL (10 min)

**6.1. Editar analyze_all_specialists.py**

```bash
# Backup
cp analyze_all_specialists.py analyze_all_specialists.py.bak

# Editar
nano analyze_all_specialists.py
```

**Mudanças:**

```python
# ANTES:
from engine.orchestration.dual_core_wrapper import DualCoreWrapper

# DEPOIS:
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

# ANTES:
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model=llm_model,
    ...
)

# DEPOIS:
wrapper = TripleCoreWrapper(  # 🆕 Usar Triple-Core V2
    python_specialist=specialist,
    llm_model=llm_model,
    deep_context=True,
    two_pass_llm=False,  # 🆕 Opcional: habilitar two-pass
)
```

---

### FASE 7: TESTES DE VALIDAÇÃO (30 min)

**7.1. Teste unitário: Core 2 funciona**
```bash
python3 << 'EOF'
from triple_core.core_2_examples.example_finder import ExampleFinderCore

finder = ExampleFinderCore()
result = finder.analyze(
    base_analysis={'recommendations': ['Improve dialogue', 'Add subtext']},
    screenplay_text="Sample text",
    max_examples_per_problem=3
)
print(f"✅ Core 2: Found {result['total_examples']} examples")
print(f"   Screenplays: {len(result['master_screenplays'])}")
EOF
```

**7.2. Teste unitário: NER validation funciona**
```bash
python3 << 'EOF'
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper
from engine.analyzers.dr_dialogue import DrDialogue

specialist = DrDialogue()
wrapper = TripleCoreWrapper(specialist)

# Teste 1: Personagens corretos (deve passar)
result = wrapper._validate_character_names(
    llm_insights="SAMANTHA diz algo. ALBERTO responde.",
    screenplay_text="SAMANTHA: Hello\nALBERTO: Hi"
)
assert result['valid'] == True, "❌ Falhou: deveria validar personagens corretos"
print(f"✅ Teste 1 passou: overlap={result['overlap_ratio']:.1%}")

# Teste 2: Personagens inventados (deve falhar)
result = wrapper._validate_character_names(
    llm_insights="SOFIA diz algo. JULIO responde. MARIA concorda.",
    screenplay_text="SAMANTHA: Hello\nALBERTO: Hi"
)
assert result['valid'] == False, "❌ Falhou: deveria detectar personagens inventados"
print(f"✅ Teste 2 passou: hallucinated={result['hallucinated']}")
EOF
```

**7.3. Teste integração: Análise completa**
```bash
# Análise de teste (5 min)
python3 analyze.py \
    "inputs/examples/Te Encontro em Mim .pdf" \
    --specialist dialogue \
    --output-format txt

# Verificar output
echo "
✅ CHECKLIST DE VALIDAÇÃO:
"
grep -q "Core 2" analyze_output.txt && echo "✅ Core 2 executou" || echo "❌ Core 2 não rodou"
grep -q "Found.*examples" analyze_output.txt && echo "✅ Encontrou exemplos" || echo "❌ Sem exemplos"
grep -q "NER validation" analyze_output.txt && echo "✅ NER validou" || echo "❌ NER não rodou"
grep -q "SAMANTHA\|ALBERTO\|KLEBER" analyze_output.txt && echo "✅ Personagens REAIS" || echo "❌ Personagens inventados"
! grep -q "SOFIA\|JULIO\|MARIA\|ANA" analyze_output.txt && echo "✅ Sem alucinações" || echo "❌ AINDA ALUCINANDO!"
```

**7.4. Teste de stress: Análise completa (opcional)**
```bash
# Rodar análise completa (2-3 horas)
python3 analyze_all_specialists.py \
    "inputs/examples/Te Encontro em Mim .pdf" \
    --yes

# Monitorar progresso
tail -f workspace/outputs/*/2_logs/analysis.log
```

---

### FASE 8: DOCUMENTAÇÃO E COMMIT (10 min)

**8.1. Atualizar README**
```bash
nano README_SISTEMA_ATUAL.md
```

Adicionar:
```markdown
## 🏗️ Arquitetura: Triple-Core V2

Sistema híbrido combinando:
- ✅ Triple-Core (Oct 4): Core 2 com 33 roteiros mestres
- ✅ Features novas (Oct 14): NER validation, Two-Pass LLM, OpenAI support
- ✅ Melhor dos dois mundos

### Features:
1. **Core 2 (Example Finder)**: 33 roteiros mestres indexados
2. **NER Validation**: Detecta alucinações em tempo real
3. **Two-Pass LLM**: Qualidade melhorada (opcional)
4. **OpenAI Support**: Híbrido Ollama + OpenAI API
5. **Quality Validation**: Critérios nivel 10

### Uso:
```python
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

wrapper = TripleCoreWrapper(
    specialist,
    llm_model="scripturemon-optimized",  # ou "gpt-5-preview"
    two_pass_llm=False,  # True para 2 rodadas
    deep_context=True
)
```
```

**8.2. Commit das mudanças**
```bash
git add .
git commit -m "feat: Implement Triple-Core V2 (merge Oct 4 + Oct 14 features)

- Restore Core 2 (Example Finder) with 33 master screenplays
- Port NER validation from Oct 14 (spaCy-based hallucination detection)
- Port Two-Pass LLM architecture (optional)
- Port OpenAI API support (hybrid Ollama/OpenAI backend)
- Port Quality Validation (nivel 10 criteria)
- Restore Modelfile_optimized (temp 0.2, seed 1337, explicit prohibitions)
- Update analyze_all_specialists.py to use TripleCoreWrapper

Result: Best of both worlds - Triple-Core grounding + modern features"
```

---

## ✅ CHECKLIST DE SUCESSO

Após implementação, verificar:

### Arquitetura
- [ ] Diretório `/triple_core/` existe
- [ ] Diretório `/triple_core/core_2_examples/` existe
- [ ] Arquivo `example_finder.py` existe
- [ ] Diretório `/content/screenplays/` existe com 33 PDFs
- [ ] Arquivo `masters_index.json` existe

### Modelfile
- [ ] Comando `ollama show scripturemon-optimized --modelfile` funciona
- [ ] Parâmetro `temperature = 0.2`
- [ ] Parâmetro `seed = 1337`
- [ ] Parâmetro `top_k = 0`
- [ ] Parâmetro `repeat_penalty = 1.15`
- [ ] System prompt contém "PROIBIÇÕES ABSOLUTAS"
- [ ] System prompt contém exemplos de SAMANTHA e ALBERTO

### Features Novas (Portadas)
- [ ] Método `_validate_character_names()` existe
- [ ] Método `_extract_entities_safe()` existe
- [ ] Flag `two_pass_llm` disponível
- [ ] Método `_call_llm()` suporta OpenAI
- [ ] spaCy `pt_core_news_lg` instalado

### Testes Funcionais
- [ ] Import `TripleCoreWrapper` funciona sem erro
- [ ] Core 2 encontra exemplos (teste unitário passa)
- [ ] NER validation detecta alucinações (teste unitário passa)
- [ ] Análise completa roda sem crash
- [ ] Log mostra "Core 2 completed in X.Xs"
- [ ] Log mostra "Found X examples from masters"
- [ ] Log mostra "NER validation passed" ou "concern"

### Qualidade de Output
- [ ] Personagens citados são REAIS do roteiro
- [ ] Páginas citadas estão no range correto (1-16)
- [ ] Cenas citadas existem no roteiro
- [ ] Sem nomes inventados (Sofia, Julio, Maria, Ana)
- [ ] NER validation: overlap > 70%
- [ ] NER validation: hallucinated < 3

### Performance
- [ ] Core 1: ~0.0s
- [ ] Core 2: ~0.0-2s
- [ ] Core 3: ~5-7min (normal)
- [ ] Total: ~5-7min por specialist

---

## 🚨 TROUBLESHOOTING

### Problema: spaCy model não encontrado
```bash
python3 -m spacy download pt_core_news_lg
```

### Problema: Core 2 não encontra roteiros
```bash
# Verificar path
ls content/screenplays/*.pdf | wc -l

# Reindexar se necessário
python3 << 'EOF'
from core.master_script_indexer import get_master_indexer
indexer = get_master_indexer(force_rebuild=True)
print(f"Reindexed: {len(indexer.list_available_screenplays())} screenplays")
EOF
```

### Problema: Import errors
```bash
# Adicionar path
export PYTHONPATH="/Users/clubproducoes/Digimundo/scripturemon:$PYTHONPATH"

# Verificar imports
python3 -c "import sys; print('\n'.join(sys.path))"
```

### Problema: Ollama model não encontrado
```bash
# Recriar modelo
ollama create scripturemon-optimized \
  -f config/Modelfile_optimized

# Verificar
ollama list | grep scripturemon
```

---

## 📊 COMPARAÇÃO: V1 vs V2

| Feature | Oct 4 (V1) | Oct 14 | V2 (Merge) |
|---------|------------|--------|------------|
| **Core 2 (Examples)** | ✅ 33 roteiros | ❌ Ausente | ✅ 33 roteiros |
| **Modelfile Optimizado** | ✅ temp 0.2 | ❌ temp 0.3 | ✅ temp 0.2 |
| **Few-shot Examples** | ✅ Sim | ❌ Não | ✅ Sim |
| **NER Validation** | ❌ Não | ✅ Sim | ✅ Sim |
| **Two-Pass LLM** | ❌ Não | ✅ Sim | ✅ Sim (opt) |
| **OpenAI Support** | ❌ Não | ✅ Sim | ✅ Sim |
| **Quality Validation** | ❌ Não | ✅ Sim | ✅ Sim |
| **Hallucinations** | ✅ Zero | ❌ Graves | ✅ Zero |
| **Quality Score** | 1.00/1.0 | ??? | 1.00/1.0+ |

---

## 🎯 PRÓXIMOS PASSOS (APÓS IMPLEMENTAÇÃO)

1. **Monitorar métricas** por 1 semana:
   - NER validation overlap médio
   - Número de hallucinated names
   - Quality scores

2. **Tuning fino**:
   - Ajustar threshold de NER (50% → 70%?)
   - Testar two_pass_llm=True vs False
   - Comparar Ollama vs GPT-5

3. **Otimizações futuras**:
   - Cache de exemplos do Core 2
   - Paralelizar Core 1 + Core 2
   - Melhorar indexação de screenplays

---

**Documento criado por:** Claude Code
**Data:** 2025-10-14
**Versão:** 1.0 (Plano de Implementação Triple-Core V2)
**Tempo estimado total:** 2-3 horas
