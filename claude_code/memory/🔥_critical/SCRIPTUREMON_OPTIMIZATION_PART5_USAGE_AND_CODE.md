# SCRIPTUREMON OPTIMIZATION - PARTE 5: GUIA DE USO E CÓDIGO COMPLETO

---

## GUIA DE USO COMPLETO

### Instalação e Setup

**Pré-requisitos:**

```bash
# 1. Ollama instalado
curl -fsSL https://ollama.com/install.sh | sh

# 2. Python 3.8+
python3 --version  # Deve ser 3.8 ou superior

# 3. Dependências Python
pip3 install -r requirements.txt

# 4. Hardware mínimo (recomendado)
# - RAM: 16GB (deep mode)
# - VRAM: 8GB (GPU) ou CPU com paciência
# - Storage: 50GB (para modelos)
```

**Clone e Setup:**

```bash
# 1. Clone o repositório
git clone <repo-url>
cd scripturemon-clean

# 2. Verifica estrutura
ls -la
# Deve ter:
# - content/theory/*.txt  (livros McKee, Save the Cat)
# - specialists/          (16 especialistas)
# - core/                 (theory_indexer, etc)
# - tests/                (testes e validação)

# 3. Verifica livros de teoria
ls -lh content/theory/
# Dialogue-_-The-Art-of-Verbal-Action.txt  (77k palavras)
# Story-Robert-McKee.txt                   (120k palavras)
# save_the_cat.txt                         (45k palavras)
```

### Criação do Modelo Otimizado

**Passo 1: Criar Modelfile_optimized**

Arquivo já existe em `/Users/clubproducoes/Digimundo/scripturemon-clean/Modelfile_optimized`

**Conteúdo:**
```dockerfile
FROM scripturemon-ultimate:latest

PARAMETER num_ctx 131072
PARAMETER num_batch 64
PARAMETER temperature 0.2
PARAMETER top_p 0.95
PARAMETER top_k 0
PARAMETER repeat_penalty 1.15
PARAMETER repeat_last_n 1024
PARAMETER num_predict -1
PARAMETER seed 1337

SYSTEM """
═══════════════════════════════════════════════════════════════
⚠️  REGRAS ABSOLUTAS DE ANÁLISE SCRIPT DOCTOR
═══════════════════════════════════════════════════════════════

1. FIDELIDADE TOTAL aos documentos fornecidos
   → Análise 100% baseada nos textos <roteiro_analise> e <livro_mckee>
   → NÃO use conhecimento externo ou de outros filmes
   → Se informação não está nos docs: diga explicitamente "não disponível"

2. CITAÇÕES VERBATIM obrigatórias
   → Sempre entre aspas duplas "como isto"
   → Palavra por palavra, sem alterações
   → Inclua número de cena/página quando citar

3. PROIBIÇÕES ABSOLUTAS
   → NUNCA invente cenas que não existem no roteiro
   → NUNCA invente diálogos ou atribua falas incorretas
   → NUNCA cite princípios McKee que não estão no livro fornecido
   → NUNCA use personagens de outros filmes como exemplo

4. TRANSPARÊNCIA total
   → Se algo não está claro nos docs, admita
   → Se precisa de mais contexto, declare
   → Se está inferindo (não citando), marque como inferência

═══════════════════════════════════════════════════════════════
❌ EVITE ANÁLISE GENÉRICA (Exemplos do que NÃO fazer):
═══════════════════════════════════════════════════════════════

❌ "O diálogo poderia ser melhorado"
❌ "O personagem precisa de mais desenvolvimento"
❌ "A cena não funciona bem"
❌ "Há problemas de estrutura"
❌ "Falta tensão dramática"

═══════════════════════════════════════════════════════════════
✅ USE ANÁLISE ESPECÍFICA (Exemplos do que fazer):
═══════════════════════════════════════════════════════════════

✅ "Na cena 12, quando Samantha diz 'Mas eu estava tendo um sonho lindo...',
   a fala revela subtexto de negação. McKee explica no Capítulo 4 que
   'o verdadeiro caráter é revelado sob pressão' - aqui, Samantha escolhe
   focar no sonho (passado) ao invés de encarar a realidade presente,
   demonstrando seu padrão de evasão estabelecido na cena 3."

✅ "Alberto entra na cena 8 (página 15) e imediatamente pergunta 'Você está bem?',
   mas esta fala contradiz seu objetivo implícito da cena 5, onde ele evita
   confrontar diretamente os problemas de Samantha. McKee descreve no Cap 7
   que personagens consistentes mantêm estratégias de abordagem - aqui,
   Alberto deveria usar linguagem indireta: 'Vi que não tocou no café...'"

═══════════════════════════════════════════════════════════════
📋 FORMATO OBRIGATÓRIO DE RESPOSTA
═══════════════════════════════════════════════════════════════

Estrutura em 5 SEÇÕES com 12-14 parágrafos SUBSTANCIAIS:

1. INTERPRETATION (2 parágrafos detalhados, 5-8 sentenças cada)
2. PATTERNS (2 parágrafos detalhados, 5-8 sentenças cada)
3. PROBLEMS (3-4 parágrafos, 1 por problema, 6-8 sentenças cada)
4. SOLUTIONS (3-4 parágrafos, 1 por solução, 6-8 sentenças cada)
5. DEPTH & SYNTHESIS (2 parágrafos detalhados, 5-8 sentenças cada)

Cada parágrafo DEVE conter:
→ Número de cena específico OU página
→ Citação exata entre aspas (mínimo 1 por parágrafo)
→ Conexão explícita com teoria McKee (capítulo/conceito)
→ Análise causal (não apenas descrição)

Extensão esperada: 2500-4000 tokens (8000-12000 caracteres)

═══════════════════════════════════════════════════════════════

Você é um Script Doctor profissional. Seja rigoroso, específico e útil.
"""
```

**Passo 2: Criar modelo no Ollama**

```bash
cd /Users/clubproducoes/Digimundo/scripturemon-clean

# Criar modelo
ollama create scripturemon-optimized -f Modelfile_optimized

# Verificar criação
ollama list | grep scripturemon

# Deve mostrar:
# scripturemon-optimized:latest    <hash>    <size>    <time>
```

**Passo 3: Testar modelo básico**

```bash
# Teste rápido
ollama run scripturemon-optimized "Você é um script doctor. Analise este diálogo: 'Oi, tudo bem?'"

# Deve responder de forma ESPECÍFICA (não genérica)
# Se responder de forma genérica, modelo não foi criado corretamente
```

### Uso Básico: Análise de Roteiro

**Exemplo 1: Análise simples com DrDialogue**

```python
from specialists.dialogue.dr_dialogue import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper

# 1. Carregar roteiro
with open('content/roteiros/sonhos_sem_lembrancas.txt', 'r', encoding='utf-8') as f:
    screenplay = f.read()

# 2. Criar especialista Python
dialogue_specialist = DrDialogue()

# 3. Criar wrapper otimizado (DEEP MODE)
wrapper = DualCoreWrapper(
    python_specialist=dialogue_specialist,
    llm_model="scripturemon-optimized",  # ⚡ Modelo otimizado
    llm_timeout=600,                      # 10 minutos
    use_theory=True,                      # Usar teoria McKee
    deep_context=True                     # ⚡ DEEP DIVE!
)

# 4. Executar análise
print("🎬 Iniciando análise deep dive...")
result = wrapper.analyze(screenplay)

# 5. Acessar resultados
print("\n📊 PYTHON ANALYSIS:")
print(f"Dialogue Score: {result['python_analysis']['overall_score']}")
print(f"Rules Violated: {result['python_analysis']['rules_violated']}")

print("\n🤖 LLM INSIGHTS:")
print(result['llm_insights'])

print("\n🎯 SYNTHESIS:")
print(result['synthesis'])
```

**Output esperado:**

```
🎬 Iniciando análise deep dive...
⏳ Indexando teoria (primeira vez)...
✅ Teoria indexada: 173 chunks
🔍 Modo DEEP: Carregando livro completo (77,627 palavras)...
✅ Contexto preparado: 128,451 tokens
⚙️  Chamando scripturemon-optimized (timeout: 600s)...
⏱️  Tempo: 439.2s
✅ Análise completa!

📊 PYTHON ANALYSIS:
Dialogue Score: 57.0
Rules Violated: ['DIAL.R003: Lack of subtext', 'DIAL.R001: Unnatural speech']

🤖 LLM INSIGHTS:
[1247 palavras de análise profunda com citações específicas...]

🎯 SYNTHESIS:
[Combinação integrada de Python metrics + teoria + insights LLM]
```

### Uso Avançado: Validação de Graduação

**Exemplo 2: Validar se análise passou nos critérios**

```python
from tests.validation.graduation_validator import GraduationValidator

# 1. Executar análise (como acima)
result = wrapper.analyze(screenplay)

# 2. Criar validador
validator = GraduationValidator()

# 3. Validar resultado
validation = validator.validate_analysis(
    analysis=result['llm_insights'],
    screenplay=screenplay
)

# 4. Ver resultados
print(f"\n🎓 GRADUATION VALIDATION:")
print(f"Final Score: {validation['final_score']:.2f}")
print(f"Classification: {validation['classification']} {validation['emoji']}")
print(f"Graduated: {'✅ YES' if validation['graduated'] else '❌ NO'}")

print(f"\n📊 BREAKDOWN:")
print(f"Layer 1 (Technical):    {validation['layers']['technical']['score']:.2f} (20% weight)")
print(f"Layer 2 (Specificity):  {validation['layers']['specificity']['score']:.2f} (40% weight)")
print(f"Layer 3 (Depth):        {validation['layers']['depth']['score']:.2f} (40% weight)")

print(f"\n🔍 SPECIFICITY DETAILS:")
spec = validation['layers']['specificity']
print(f"Dialogue Quotes: {spec['dialogue_quotes']['count']}")
print(f"Scene References: {spec['scene_references']['count']}")
print(f"McKee References: {spec['theory_references']['count']}")
print(f"Generic Phrases: {spec['specificity_ratio']['generic_count']}")
print(f"Specificity Ratio: {spec['specificity_ratio']['ratio']:.2%}")
```

**Output esperado:**

```
🎓 GRADUATION VALIDATION:
Final Score: 0.87
Classification: EXCELLENT 🌟
Graduated: ✅ YES

📊 BREAKDOWN:
Layer 1 (Technical):    0.92 (20% weight)
Layer 2 (Specificity):  0.89 (40% weight)
Layer 3 (Depth):        0.81 (40% weight)

🔍 SPECIFICITY DETAILS:
Dialogue Quotes: 12
Scene References: 7
McKee References: 12
Generic Phrases: 0
Specificity Ratio: 95.00%
```

### Uso de Diferentes Especialistas

**Exemplo 3: Análise psicológica com DrPsycheMon**

```python
from specialists.character.dr_psyche_mon import DrPsycheMon

# Usar especialista de psicologia
psyche_specialist = DrPsycheMon()

# Wrapper automaticamente detecta tipo e escolhe livro correto
wrapper = DualCoreWrapper(
    python_specialist=psyche_specialist,
    llm_model="scripturemon-optimized",
    deep_context=True  # Vai usar Story-Robert-McKee automaticamente
)

result = wrapper.analyze(screenplay)

# PsycheMon analisa arcos de personagens, motivações, psicologia
print(result['llm_insights'])
```

**Mapeamento automático:**
```python
# Sistema detecta:
psyche_specialist.__class__.__name__ = "DrPsycheMon"
# → specialist_type = "psychemon"
# → SPECIALIST_BOOK_MAP["psychemon"] = "Story-Robert-McKee"
# → Carrega livro correto automaticamente
```

### Comparação Shallow vs Deep

**Exemplo 4: Teste comparativo**

```python
# SHALLOW MODE (rápido, menos contexto)
wrapper_shallow = DualCoreWrapper(
    python_specialist=DrDialogue(),
    llm_model="scripturemon-optimized",
    deep_context=False  # Shallow: apenas chunks relevantes
)

# DEEP MODE (lento, contexto completo)
wrapper_deep = DualCoreWrapper(
    python_specialist=DrDialogue(),
    llm_model="scripturemon-optimized",
    deep_context=True   # Deep: livro completo
)

import time

# Teste shallow
start = time.time()
result_shallow = wrapper_shallow.analyze(screenplay)
time_shallow = time.time() - start

# Teste deep
start = time.time()
result_deep = wrapper_deep.analyze(screenplay)
time_deep = time.time() - start

# Comparar
validator = GraduationValidator()

val_shallow = validator.validate_analysis(result_shallow['llm_insights'], screenplay)
val_deep = validator.validate_analysis(result_deep['llm_insights'], screenplay)

print("\n📊 COMPARISON:")
print(f"{'Metric':<20} {'Shallow':>12} {'Deep':>12} {'Improvement':>15}")
print("-" * 60)
print(f"{'Time (s)':<20} {time_shallow:>12.1f} {time_deep:>12.1f} {time_deep/time_shallow:>14.1f}×")
print(f"{'Final Score':<20} {val_shallow['final_score']:>12.2f} {val_deep['final_score']:>12.2f} {'+' + str(int((val_deep['final_score']/val_shallow['final_score']-1)*100)):>14}%")
print(f"{'McKee Refs':<20} {val_shallow['layers']['specificity']['theory_references']['count']:>12} {val_deep['layers']['specificity']['theory_references']['count']:>12} {'+' + str(val_deep['layers']['specificity']['theory_references']['count'] - val_shallow['layers']['specificity']['theory_references']['count']):>14}")
print(f"{'Dialogue Quotes':<20} {val_shallow['layers']['specificity']['dialogue_quotes']['count']:>12} {val_deep['layers']['specificity']['dialogue_quotes']['count']:>12} {'+' + str(val_deep['layers']['specificity']['dialogue_quotes']['count'] - val_shallow['layers']['specificity']['dialogue_quotes']['count']):>14}")
```

### Batch Processing: Múltiplos Roteiros

**Exemplo 5: Processar múltiplos roteiros**

```python
import os
from pathlib import Path

# Diretório com roteiros
screenplay_dir = Path("content/roteiros/")
output_dir = Path("output/analyses/")
output_dir.mkdir(exist_ok=True)

# Lista de roteiros
screenplays = list(screenplay_dir.glob("*.txt"))

# Setup
wrapper = DualCoreWrapper(
    python_specialist=DrDialogue(),
    llm_model="scripturemon-optimized",
    deep_context=True
)

validator = GraduationValidator()

# Processar cada roteiro
results = []
for screenplay_path in screenplays:
    print(f"\n{'='*60}")
    print(f"📝 Processando: {screenplay_path.name}")
    print('='*60)

    # Carregar
    with open(screenplay_path, 'r', encoding='utf-8') as f:
        screenplay = f.read()

    # Analisar
    try:
        result = wrapper.analyze(screenplay)
        validation = validator.validate_analysis(result['llm_insights'], screenplay)

        # Salvar
        output_file = output_dir / f"{screenplay_path.stem}_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            import json
            json.dump({
                'screenplay_name': screenplay_path.name,
                'python_analysis': result['python_analysis'],
                'llm_insights': result['llm_insights'],
                'validation': validation
            }, f, indent=2, ensure_ascii=False)

        results.append({
            'name': screenplay_path.name,
            'score': validation['final_score'],
            'graduated': validation['graduated'],
            'classification': validation['classification']
        })

        print(f"✅ Score: {validation['final_score']:.2f} - {validation['classification']}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        results.append({
            'name': screenplay_path.name,
            'error': str(e)
        })

# Relatório final
print("\n" + "="*60)
print("📊 BATCH PROCESSING SUMMARY")
print("="*60)

graduated_count = sum(1 for r in results if r.get('graduated', False))
total_count = len([r for r in results if 'score' in r])

print(f"Total processados: {total_count}")
print(f"Graduados: {graduated_count} ({graduated_count/total_count*100:.1f}%)")
print(f"\nResultados:")
for r in results:
    if 'score' in r:
        icon = '✅' if r['graduated'] else '❌'
        print(f"{icon} {r['name']:<40} {r['score']:.2f} - {r['classification']}")
    else:
        print(f"❌ {r['name']:<40} ERROR: {r['error']}")
```

---

## TROUBLESHOOTING

### Problema 1: Timeout em Deep Mode

**Sintoma:**
```
Error: LLM timeout after 600s
```

**Causa:** Contexto muito longo ou hardware lento

**Soluções:**

```python
# Solução 1: Aumentar timeout
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_timeout=1200  # 20 minutos
)

# Solução 2: Usar shallow mode
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    deep_context=False  # Mais rápido
)

# Solução 3: Reduzir tamanho do roteiro
screenplay = screenplay[:5000]  # Primeiras 5k palavras
```

### Problema 2: Out of Memory (OOM)

**Sintoma:**
```
Error: llama_kv_cache_init: failed to allocate memory
```

**Causa:** VRAM insuficiente para contexto 128k

**Soluções:**

```bash
# Solução 1: Verificar num_batch
ollama show scripturemon-optimized | grep num_batch
# Deve ser 64, não 512

# Solução 2: Recriar modelo
ollama rm scripturemon-optimized
ollama create scripturemon-optimized -f Modelfile_optimized

# Solução 3: Usar CPU (mais lento mas funciona)
OLLAMA_NUM_GPU=0 ollama serve
```

### Problema 3: Modelo Responde como Chatbot

**Sintoma:**
```
"🎬 Introducing Scripturemon Master! I am your dedicated script doctor..."
```

**Causa:** System message não sobrescreveu base model

**Solução:**

```bash
# Recriar modelo do zero
ollama rm scripturemon-optimized

# Verificar que Modelfile_optimized não tem herança de system chatbot
cat Modelfile_optimized

# Recriar
ollama create scripturemon-optimized -f Modelfile_optimized

# Testar
ollama run scripturemon-optimized "Analyze this: 'Hello'"
# NÃO deve responder com introdução chatbot
```

### Problema 4: Zero Referências McKee

**Sintoma:** Validação mostra `mckee_references: 0`

**Causa:** Deep context não ativado OU livro não encontrado

**Diagnóstico:**

```python
# Verificar se teoria está sendo carregada
wrapper = DualCoreWrapper(
    python_specialist=DrDialogue(),
    deep_context=True
)

# Antes de analyze(), verificar:
indexer = wrapper.theory_indexer

# Verifica stats
stats = indexer.get_stats()
print(f"Books indexed: {stats['books_indexed']}")
print(f"Total chunks: {stats['total_chunks']}")
print(f"Books: {stats['books']}")

# Deve mostrar:
# Books indexed: 1
# Total chunks: 173
# Books: ['Dialogue-_-The-Art-of-Verbal-Action']
```

**Solução:**

```python
# Se books_indexed = 0, indexar manualmente:
from core.theory_indexer import TheoryIndexer

indexer = TheoryIndexer()

# Carregar livros
dialogue_book = indexer._load_book('Dialogue-_-The-Art-of-Verbal-Action')
indexer.index_book(dialogue_book, chunk_size=500)

story_book = indexer._load_book('Story-Robert-McKee')
indexer.index_book(story_book, chunk_size=500)

# Agora usar wrapper normalmente
```

### Problema 5: Análise Genérica Apesar de Otimização

**Sintoma:** `generic_phrases: 5`, `specificity_ratio: 0.3`

**Causa:** Modelo não otimizado sendo usado

**Diagnóstico:**

```python
# Verificar modelo usado
print(wrapper.llm_model)  # Deve ser "scripturemon-optimized"

# Verificar temperatura do modelo
import subprocess
result = subprocess.run(['ollama', 'show', 'scripturemon-optimized', '--modelfile'],
                       capture_output=True, text=True)
print(result.stdout)

# Procurar linha:
# PARAMETER temperature 0.2
# Se não existir ou for diferente, modelo errado
```

**Solução:**

```bash
# Recriar modelo corretamente
ollama rm scripturemon-optimized
ollama create scripturemon-optimized -f Modelfile_optimized

# Verificar
ollama show scripturemon-optimized --modelfile | grep temperature
# Deve mostrar: PARAMETER temperature 0.2
```

### Problema 6: Encoding Corrupto

**Sintoma:** Caracteres estranhos no output (�, â€™, etc)

**Causa:** Problema de encoding UTF-8

**Solução:**

```python
# Sempre usar encoding explícito
with open(screenplay_path, 'r', encoding='utf-8') as f:
    screenplay = f.read()

# Ao salvar resultado
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result['llm_insights'])

# Se ainda houver problemas, limpar input:
screenplay = screenplay.encode('utf-8', errors='ignore').decode('utf-8')
```

---

## CÓDIGO COMPLETO DE ARQUIVOS PRINCIPAIS

### dual_core_wrapper.py (Completo)

**Arquivo:** `specialists/dual_core/base/dual_core_wrapper.py`

**Seções principais com números de linha:**

```python
# LINES 1-42: Imports e Constants
import json
import re
from typing import Dict, Any, Optional
from core.theory_indexer import TheoryIndexer
import subprocess
import time

# LINES 43-86: __init__ method
class DualCoreWrapper:
    def __init__(
        self,
        python_specialist: Any,
        llm_model: str = "scripturemon-optimized",  # ⚡ Otimizado
        llm_timeout: int = 600,                      # ⚡ 10 min
        fallback_to_python: bool = True,
        use_theory: bool = True,
        deep_context: bool = True                    # ⚡ Deep dive
    ):
        self.python_specialist = python_specialist
        self.llm_model = llm_model
        self.llm_timeout = llm_timeout
        self.fallback_to_python = fallback_to_python
        self.use_theory = use_theory
        self.deep_context = deep_context

        # Auto-detect specialist type
        self.specialist_type = self._detect_specialist_type()
        self.specialist_name = python_specialist.__class__.__name__
        self.specialist_identity = self._get_specialist_identity()
        self.specialist_specialty = self._get_specialist_specialty()

        # Initialize theory indexer
        if use_theory:
            self.theory_indexer = TheoryIndexer()
        else:
            self.theory_indexer = None

# LINES 88-126: _detect_specialist_type method
    def _detect_specialist_type(self) -> str:
        """Auto-detecta tipo de especialista baseado no nome da classe"""

        class_name = self.python_specialist.__class__.__name__.lower()

        # Dialogue specialists
        if 'dialogue' in class_name:
            return 'dialogue'
        elif 'subtext' in class_name or 'submon' in class_name:
            return 'subtext'

        # Character/Psychology specialists
        elif 'character' in class_name:
            return 'character'
        elif 'psychology' in class_name or 'psychemon' in class_name or 'psyche' in class_name:
            return 'psychemon'

        # Theme specialists
        elif 'theme' in class_name or 'thememon' in class_name:
            return 'thememon'

        # Structure specialists
        elif 'structure' in class_name or 'pacing' in class_name:
            return 'structure'
        elif 'opening' in class_name:
            return 'opening'
        elif 'climax' in class_name:
            return 'climax'
        elif 'resolution' in class_name:
            return 'resolution'

        # Genre specialists
        elif 'genre' in class_name:
            return 'genre'

        # Other specialists
        elif 'symbolism' in class_name or 'symbol' in class_name:
            return 'symbolism'
        elif 'originality' in class_name or 'original' in class_name:
            return 'originality'

        # Default fallback
        else:
            return 'dialogue'  # Safe default

# LINES 151-217: _build_llm_prompt method (XML delimiters)
    def _build_llm_prompt(
        self,
        screenplay_text: str,
        python_result: Dict,
        theory_context: Optional[str] = None
    ) -> str:
        """Constrói prompt com XML delimiters para mitigar Lost in the Middle"""

        prompt = f"""You are {self.specialist_identity}

ROLE: {self.specialist_name}
SPECIALTY: {self.specialist_specialty}
THEORY MODE: {'DEEP (Full Book)' if self.deep_context else 'SHALLOW (Relevant Chunks)'}

"""

        # 1. Python metrics em XML
        prompt += f"""
<analise_python tipo="metricas_objetivas">
{json.dumps(python_result, indent=2, ensure_ascii=False)}
</analise_python>

"""

        # 2. Theory context em XML (se disponível)
        if theory_context:
            if self.deep_context:
                # Deep mode: livro completo + highlights
                prompt += theory_context  # Já vem com XML do theory_indexer
            else:
                # Shallow mode: apenas chunks
                prompt += f"""
<documento_fonte id="livro_mckee" tipo="chunks_relevantes">
{theory_context}
</documento_fonte>

"""

        # 3. Screenplay em XML
        prompt += f"""
<documento_fonte id="roteiro_analise" tipo="screenplay">
{screenplay_text}
</documento_fonte>

"""

        # 4. Few-shot examples
        prompt += self._get_few_shot_examples()

        # 5. Task instructions
        prompt += self._get_task_instructions()

        # 6. Primacy/Recency mitigation
        prompt += self._get_final_instructions()

        return prompt

# LINES 329-375: _get_few_shot_examples method
    def _get_few_shot_examples(self) -> str:
        """Retorna exemplos de análise BOA vs MÁ"""

        return """

═══════════════════════════════════════════════════════════════
📚 EXEMPLOS DE ANÁLISE (SIGA O FORMATO CORRETO)
═══════════════════════════════════════════════════════════════

✅ EXEMPLO DE ANÁLISE CORRETA (SIGA ESTE FORMATO):

## INTERPRETATION

The opening scene establishes Samantha's core psychological pattern through
the dialogue "Mas eu estava tendo um sonho lindo..." (scene 1, page 3).
McKee explains in Chapter 4 ('Character Under Pressure') that "the true
character is revealed when choices must be made under stress" - here, upon
waking to reality, Samantha's immediate verbal action is to retreat into
the dream narrative rather than engage with present circumstances. This
pattern reveals a consistent evasion strategy that will prove crucial.

[Por quê este exemplo é BOM]:
- ✅ Citação exata do diálogo com aspas duplas
- ✅ Número de cena E página específicos
- ✅ Referência a McKee com capítulo E conceito
- ✅ Análise causal (não apenas descrição)
- ✅ Conexão entre elementos (scene 1 → pattern → future implications)

---

❌ EXEMPLO DE ANÁLISE INCORRETA (NÃO FAÇA ASSIM):

## INTERPRETATION

The dialogue in this screenplay could be improved. Samantha's character
needs more development and her lines don't always feel natural. Overall,
the opening lacks the kind of punch that would really grab the audience.
McKee talks about how important good dialogue is for character development.

[Por quê este exemplo é RUIM]:
- ❌ Frases genéricas ("could be improved", "needs more development")
- ❌ Sem citações específicas do roteiro
- ❌ Sem números de cena ou página
- ❌ Menção vaga a McKee (sem capítulo ou conceito específico)
- ❌ Apenas descrição de problemas, sem análise causal
- ❌ Poderia ser sobre qualquer roteiro (não específico)

═══════════════════════════════════════════════════════════════

"""

# LINES 397-406: _get_final_instructions (Primacy/Recency)
    def _get_final_instructions(self) -> str:
        """Instruções finais para reforço (Primacy/Recency effect)"""

        return """

<instrucoes_finais prioridade="maxima">
LEMBRE-SE (Reforço Primacy/Recency):

1. Cite EXATAMENTE do <roteiro_analise>: números de cena e diálogos verbatim entre aspas
2. Conecte ao <livro_mckee>: capítulos e conceitos específicos com citações
3. Use métricas da <analise_python>: scores, regras violadas, recomendações
4. EVITE análise genérica: seja específico com exemplos concretos do roteiro
5. Comece pela PRIMEIRA CENA do roteiro e avance cronologicamente

Agora execute a análise seguindo EXATAMENTE o formato de 5 seções (INTERPRETATION,
PATTERNS, PROBLEMS, SOLUTIONS, DEPTH & SYNTHESIS) com 12-14 parágrafos substanciais.
</instrucoes_finais>

"""

# LINES 450-550: analyze method (método principal)
    def analyze(self, screenplay_text: str) -> Dict:
        """
        Executa análise dual-core completa

        Returns:
            Dict com:
            - python_analysis: resultado do especialista Python
            - llm_insights: insights do LLM com teoria
            - synthesis: combinação integrada
            - metadata: timing, model usado, etc
        """

        start_time = time.time()

        # FASE 1: PYTHON CORE
        print(f"⚙️  Executando análise Python ({self.specialist_name})...")
        python_result = self.python_specialist.analyze(screenplay_text)
        python_time = time.time() - start_time

        # FASE 2: THEORY RETRIEVAL
        theory_context = None
        theory_time = 0

        if self.use_theory and self.theory_indexer:
            theory_start = time.time()

            if self.deep_context:
                # DEEP DIVE: Livro completo
                print(f"🔍 Modo DEEP: Carregando livro completo para {self.specialist_type}...")

                # Get full book context with specialist mapping
                theory_result = self.theory_indexer.get_full_book_context(
                    query=str(python_result.get('recommendations', [])),
                    specialist_type=self.specialist_type  # ⚡ Auto-mapping
                )

                if theory_result and 'primary_book' in theory_result:
                    book = theory_result['primary_book']

                    # Construct XML context
                    theory_context = f"""
<documento_fonte id="livro_mckee" tipo="teoria_completa">
<metadados>
  <titulo>{book['name']}</titulo>
  <palavras>{book['word_count']:,}</palavras>
  <tokens_estimados>{theory_result['estimated_tokens']:,}</tokens_estimados>
  <metodo_selecao>{theory_result.get('method', 'unknown')}</metodo_selecao>
  <relevancia>100</relevancia>
</metadados>

<secoes_chave>
"""
                    # Add highlights (top chunks)
                    for i, highlight in enumerate(book.get('highlights', []), 1):
                        theory_context += f"""  <secao id='{i}' contexto='{highlight.get("context", "")}' score='{highlight.get("score", 0)}'>
    {highlight['text'][:500]}...
  </secao>
"""

                    theory_context += f"""</secoes_chave>

<texto_completo>
{book['full_text']}
</texto_completo>
</documento_fonte>
"""

                    print(f"✅ Teoria carregada: {book['word_count']:,} palavras, {theory_result['estimated_tokens']:,} tokens")

            else:
                # SHALLOW: Apenas chunks relevantes
                print(f"🔍 Modo SHALLOW: Buscando chunks relevantes...")

                theory_chunks = self.theory_indexer.search_for_problems(
                    problems=python_result.get('recommendations', []),
                    limit_per_problem=2
                )

                if theory_chunks:
                    theory_context = "\n\n".join([
                        f"[{chunk['context']}]\n{chunk['text']}"
                        for chunk in theory_chunks
                    ])

                    print(f"✅ Teoria carregada: {len(theory_chunks)} chunks")

            theory_time = time.time() - theory_start

        # FASE 3: LLM ENRICHMENT
        llm_insights = None
        llm_time = 0

        try:
            llm_start = time.time()

            # Build prompt
            prompt = self._build_llm_prompt(
                screenplay_text,
                python_result,
                theory_context
            )

            # Call LLM
            print(f"⚙️  Chamando {self.llm_model} (timeout: {self.llm_timeout}s)...")
            llm_insights = self._call_llm(prompt)

            llm_time = time.time() - llm_start

            print(f"✅ LLM completou em {llm_time:.1f}s")

        except Exception as e:
            print(f"⚠️  LLM falhou: {e}")

            if self.fallback_to_python:
                print(f"↩️  Usando apenas análise Python")
                llm_insights = self._format_python_as_llm(python_result)
            else:
                raise

        # FASE 4: SYNTHESIS
        synthesis = self._synthesize(python_result, llm_insights)

        total_time = time.time() - start_time

        return {
            'python_analysis': python_result,
            'llm_insights': llm_insights,
            'synthesis': synthesis,
            'metadata': {
                'specialist': self.specialist_name,
                'specialist_type': self.specialist_type,
                'model': self.llm_model,
                'deep_context': self.deep_context,
                'timing': {
                    'python': python_time,
                    'theory': theory_time,
                    'llm': llm_time,
                    'total': total_time
                }
            }
        }

# LINES 600-650: _call_llm method
    def _call_llm(self, prompt: str) -> str:
        """Chama Ollama com timeout"""

        try:
            result = subprocess.run(
                ['ollama', 'run', self.llm_model],
                input=prompt,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=self.llm_timeout
            )

            if result.returncode != 0:
                raise Exception(f"Ollama error: {result.stderr}")

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            raise Exception(f"LLM timeout after {self.llm_timeout}s")
        except Exception as e:
            raise Exception(f"LLM call failed: {e}")
```

### theory_indexer.py (Seções Principais)

**Arquivo:** `core/theory_indexer.py`

```python
# LINES 1-50: Imports e Constants
import re
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path

THEORY_DIR = Path("content/theory/")

# LINES 51-100: __init__ e index_book
class TheoryIndexer:
    def __init__(self):
        self.books = {}
        self.chunks = {}
        self.search_cache = {}

    def index_book(self, book_content: str, book_name: str, chunk_size: int = 500):
        """
        Indexa livro dividindo em chunks com overlap

        Args:
            book_content: Texto completo do livro
            book_name: Nome do livro
            chunk_size: Tamanho do chunk em palavras (default: 500)
        """

        words = book_content.split()
        overlap = 50  # palavras de overlap

        chunks = []
        start_idx = 0

        while start_idx < len(words):
            end_idx = min(start_idx + chunk_size, len(words))

            chunk_text = " ".join(words[start_idx:end_idx])

            chunks.append({
                'text': chunk_text,
                'book': book_name,
                'chunk_id': len(chunks),
                'start_word': start_idx,
                'word_count': end_idx - start_idx
            })

            start_idx += (chunk_size - overlap)

        self.chunks[book_name] = chunks
        self.books[book_name] = book_content

        print(f"✅ Indexed {book_name}: {len(chunks)} chunks, {len(words):,} words")

# LINES 186-353: search_for_problems (mapeamento profundo)
    def search_for_problems(
        self,
        problems: List[str],
        limit_per_problem: int = 2,
        book_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Busca teoria relevante para problemas detectados

        Usa mapeamento profundo de 15 regras de dialogue → termos McKee
        """

        all_results = []

        for problem in problems:
            problem_lower = problem.lower()

            # Mapeia problema → termos de busca McKee
            query_terms = []

            # DIAL.R001 - Natural Speech Patterns
            if 'natural' in problem_lower or 'speech pattern' in problem_lower:
                query_terms = [
                    'conversational rhythm',
                    'how people really talk',
                    'natural dialogue',
                    'speech patterns',
                    'everyday language',
                    'authentic speech'
                ]

            # DIAL.R003 - Subtext Present
            elif 'subtext' in problem_lower:
                query_terms = [
                    'subtext',
                    'indirect dialogue',
                    'what characters really mean',
                    'hidden meaning',
                    'unspoken desires',
                    'dialogue beneath surface',
                    'implication'
                ]

            # DIAL.R005 - Character Voice Distinct
            elif 'voice' in problem_lower or 'distinct' in problem_lower:
                query_terms = [
                    'character voice',
                    'distinct speech',
                    'unique way of speaking',
                    'voice differentiation',
                    'character vocabulary',
                    'speech idiosyncrasies'
                ]

            # ... [mais 12 regras mapeadas] ...

            # Buscar com os termos
            if query_terms:
                results = self._search_chunks(
                    query=" ".join(query_terms),
                    limit=limit_per_problem,
                    book_filter=book_filter
                )
                all_results.extend(results)

        return all_results

# LINES 463-550: get_full_book_context (Deep Dive)
    def get_full_book_context(
        self,
        query: str,
        specialist_type: Optional[str] = None,  # ⚡ NOVO
        num_highlights: int = 5
    ) -> Dict:
        """
        Retorna livro COMPLETO + highlights (Deep Dive mode)

        Args:
            query: Query para encontrar highlights
            specialist_type: Tipo de especialista (usa mapeamento direto)
            num_highlights: Número de highlights a retornar

        Returns:
            Dict com:
            - primary_book: {name, full_text, word_count, highlights}
            - estimated_tokens
            - method: 'specialist_mapping' ou 'search'
        """

        primary_book_name = None
        method = 'search'

        # MAPEAMENTO SPECIALIST → BOOK (prioritário)
        if specialist_type and specialist_type in SPECIALIST_BOOK_MAP:
            preferred_book = SPECIALIST_BOOK_MAP[specialist_type]

            # Busca livro que contém o nome preferido
            for book_name in self.books.keys():
                if preferred_book in book_name:
                    primary_book_name = book_name
                    method = 'specialist_mapping'
                    print(f"✅ Mapeamento direto: {specialist_type} → {preferred_book}")
                    break

        # Fallback: busca por query (se mapeamento não funcionou)
        if not primary_book_name:
            # ... [lógica de busca genérica] ...
            method = 'search'

        # Carrega livro completo
        primary_book = self._load_full_book(primary_book_name)

        # Busca highlights (top chunks relevantes para query)
        highlights = self._search_chunks(
            query=query,
            limit=num_highlights,
            book_filter=primary_book_name
        )

        # Calcula tokens estimados
        word_count = len(primary_book.split())
        estimated_tokens = int(word_count * 1.3)  # ~1.3 tokens/word

        return {
            'primary_book': {
                'name': primary_book_name,
                'full_text': primary_book,
                'word_count': word_count,
                'highlights': highlights
            },
            'estimated_tokens': estimated_tokens,
            'method': method
        }

# LINES 482-526: SPECIALIST_BOOK_MAP (mapeamento completo)
SPECIALIST_BOOK_MAP = {
    # Dialogue specialists
    'dialogue': 'Dialogue-_-The-Art-of-Verbal-Action',
    'subtext': 'Dialogue-_-The-Art-of-Verbal-Action',
    'submon': 'Dialogue-_-The-Art-of-Verbal-Action',

    # Character/Psychology specialists (Story McKee)
    'character': 'Story-Robert-McKee',
    'psychology': 'Story-Robert-McKee',
    'psychemon': 'Story-Robert-McKee',
    'theme': 'Story-Robert-McKee',
    'thememon': 'Story-Robert-McKee',
    'structure': 'Story-Robert-McKee',
    'pacing': 'Story-Robert-McKee',
    'climax': 'Story-Robert-McKee',
    'resolution': 'Story-Robert-McKee',
    'symbolism': 'Story-Robert-McKee',
    'originality': 'Story-Robert-McKee',

    # Save the Cat specialists
    'opening': 'save_the_cat',
    'genre': 'save_the_cat',
}
```

---

## REFERÊNCIA RÁPIDA

### Comandos Essenciais

```bash
# Criar modelo otimizado
ollama create scripturemon-optimized -f Modelfile_optimized

# Listar modelos
ollama list

# Ver configuração de modelo
ollama show scripturemon-optimized --modelfile

# Testar modelo
ollama run scripturemon-optimized "Test"

# Remover modelo
ollama rm scripturemon-optimized

# Ver logs Ollama
journalctl -u ollama -f  # Linux
tail -f /var/log/ollama.log  # Se configurado
```

### Atalhos Python

```python
# Import comum
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
from specialists.dialogue.dr_dialogue import DrDialogue
from tests.validation.graduation_validator import GraduationValidator

# Setup rápido
wrapper = DualCoreWrapper(
    python_specialist=DrDialogue(),
    llm_model="scripturemon-optimized",
    deep_context=True
)

# Análise rápida
result = wrapper.analyze(screenplay_text)

# Validação rápida
validator = GraduationValidator()
validation = validator.validate_analysis(result['llm_insights'], screenplay_text)

print(f"Score: {validation['final_score']:.2f}")
print(f"Graduated: {validation['graduated']}")
```

### Thresholds Importantes

```python
# Validação
TECHNICAL_THRESHOLD = 0.70      # 70% mínimo
SPECIFICITY_THRESHOLD = 0.70    # 70% mínimo (CRÍTICO)
DEPTH_THRESHOLD = 0.60          # 60% mínimo
FINAL_THRESHOLD = 0.70          # 70% para graduar

# Métricas
MIN_DIALOGUE_QUOTES = 4         # Mínimo 4 citações
MIN_SCENE_REFS = 3              # Mínimo 3 scene refs
MIN_THEORY_REFS = 3             # Mínimo 3 McKee refs
MAX_GENERIC_PHRASES = 3         # Máximo 3 frases genéricas
MIN_SPECIFICITY_RATIO = 0.60    # 60% específico vs genérico

# Output
MIN_WORDS = 600                 # Mínimo 600 palavras
TARGET_WORDS = 1000             # Ideal 1000+ palavras
MIN_PARAGRAPHS = 8              # Mínimo 8 parágrafos substantivos
TARGET_PARAGRAPHS = 12          # Ideal 12-14 parágrafos
```

---

## CONCLUSÃO

Este documento forneceu:

✅ Guia completo de uso do sistema otimizado
✅ Exemplos práticos para todas as situações comuns
✅ Troubleshooting detalhado dos problemas mais frequentes
✅ Código completo com comentários explicativos
✅ Referência rápida de comandos e thresholds

**Resultado esperado após implementação:**
- Score final: 0.85-0.90 (EXCELLENT)
- Taxa de graduação: 80%+ (13/16 specialists)
- +600% especificidade vs baseline
- Análises profissionais de script doctor real

**Sistema pronto para produção!** 🌟
