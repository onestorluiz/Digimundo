# 🔍 ANÁLISE COMPARATIVA: Sistema 4 Out (BOM) vs Sistema Atual (ALUCINANDO)

**Data da Análise:** 2025-10-14
**Objetivo:** Identificar exatamente o que causou a perda de qualidade e alucinações

---

## 📊 RESUMO EXECUTIVO

### Sistema Antigo (4 outubro 2025)
- ✅ **Qualidade:** 1.00/1.0 EXCELLENT
- ✅ **Arquitetura:** TRIPLE-CORE
- ✅ **Citações:** Específicas, reais, verificáveis
- ✅ **Exemplos:** 6 de 33 roteiros mestres indexados
- ✅ **Anti-Alucinação:** Modelfile com proibições explícitas

### Sistema Atual (14 outubro 2025)
- ❌ **Qualidade:** Alucinando
- ❌ **Arquitetura:** DUAL-CORE (Core 2 removido!)
- ❌ **Citações:** Inventando cenas que não existem
- ❌ **Exemplos:** Zero (Core 2 não existe)
- ❌ **Anti-Alucinação:** Modelfile sem as regras críticas

---

## 🏗️ COMPARAÇÃO DE ARQUITETURA

### SISTEMA ANTIGO (4 out) - TRIPLE-CORE

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
│ CORE 2: Master Examples Finder ✅        │
│ - Busca em 33 roteiros mestres          │
│ - Exemplos REAIS de soluções            │
│ - Personagens, diálogos REAIS           │
│ - Tempo: ~0.0s                          │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ CORE 3: LLM Theory Enrichment           │
│ - Model: scripturemon-optimized         │
│ - Context: McKee full book (77k words)  │
│ - Prompt com EXEMPLOS REAIS do Core 2   │
│ - Tempo: ~5-7 minutos                   │
└─────────────────────────────────────────┘
  ↓
OUTPUT: Análise baseada em DADOS REAIS
```

**Pasta:** `/triple_core/`
**Arquivos-chave:**
- `triple_core/core_1_specialists/` - 24 especialistas Python
- `triple_core/core_2_examples/` - **Busca em roteiros mestres**
- `triple_core/core_3_llm/` - LLM caller
- `triple_core/orchestrators/triple_core_wrapper.py`

---

### SISTEMA ATUAL (14 out) - DUAL-CORE

```
INPUT: Screenplay Text
  ↓
┌─────────────────────────────────────────┐
│ CORE 1: Python Analysis                 │
│ - engine/analyzers/ (24 analisadores)   │
│ - Métricas objetivas                    │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ ❌ CORE 2: REMOVIDO! ❌                  │
│ - Sem exemplos de roteiros mestres      │
│ - Sem referências concretas             │
│ - LLM precisa INVENTAR exemplos         │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ CORE 3: LLM                             │
│ - Modelo: scripturemon-optimized        │
│ - Sem exemplos REAIS para basear        │
│ - ALUCINA personagens e cenas           │
└─────────────────────────────────────────┘
  ↓
OUTPUT: Análise COM ALUCINAÇÕES
```

**Pasta:** `/engine/`
**Arquivos-chave:**
- `engine/analyzers/` - 24 analisadores
- `engine/orchestration/dual_core_wrapper.py` - **SEM Core 2!**

---

## 📂 COMPARAÇÃO DE ESTRUTURA

### Diretórios Presentes no Sistema Antigo (AUSENTES no Atual)

```diff
SISTEMA ANTIGO (4 out):
+ /triple_core/                    ← PASTA CRÍTICA REMOVIDA!
+   /core_1_specialists/           ← Python analysis
+   /core_2_examples/              ← 33 ROTEIROS MESTRES
+     example_finder.py            ← Busca exemplos REAIS
+     example_formatter.py         ← Formata exemplos
+     masters_index.py             ← Index de 33 roteiros
+   /core_3_llm/                   ← LLM integration
+   /orchestrators/
+     triple_core_wrapper.py       ← Combina os 3 cores
+ /specialists/dual_core/
+ /content/screenplays/            ← 33 roteiros mestres

SISTEMA ATUAL (14 out):
- (triple_core/ NÃO EXISTE)
- (content/screenplays/ NÃO EXISTE)
+ /engine/
+   /analyzers/                    ← Dr* classes
+   /orchestration/
+     dual_core_wrapper.py         ← Só 2 cores (sem examples)
```

---

## 🔧 COMPARAÇÃO DE MODELFILES

### Modelfile Antigo (4 out) - COM Anti-Alucinação

**Arquivo:** `/tmp/scripturemon_oct4/scripturemon-clean/config/Modelfile_optimized`

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

3. PROIBIÇÕES ABSOLUTAS ← ✅ CRÍTICO!
   → NUNCA invente cenas que não existem no roteiro
   → NUNCA invente diálogos ou atribua falas incorretas
   → NUNCA cite princípios McKee que não estão no livro fornecido
   → NUNCA use personagens de outros filmes como exemplo

4. TRANSPARÊNCIA total
   → Se algo não está claro nos docs, admita
   → Se precisa de mais contexto, declare
   → Se está inferindo (não citando), marque como inferência
"""
```

**Características:**
- ✅ Proibições EXPLÍCITAS contra invenções
- ✅ Exigência de citações verbatim
- ✅ Transparência obrigatória
- ✅ Seed fixo (1337) para reprodutibilidade
- ✅ Temperature baixo (0.2)

---

### Modelfile Atual - Estado Desconhecido

**Localização:** No Ollama como `scripturemon-optimized`

**PROBLEMA:** Precisamos verificar se este Modelfile:
1. Tem as **PROIBIÇÕES ABSOLUTAS** contra alucinações?
2. Foi modificado/simplificado em algum momento?
3. Ainda tem as regras anti-invenção?

**Comando para investigar:**
```bash
ollama show scripturemon-optimized --modelfile
```

---

## 🔍 COMPARAÇÃO DO CORE 2 (MASTER EXAMPLES)

### Sistema Antigo - Core 2 ATIVO

**Arquivo:** `/triple_core/core_2_examples/example_finder.py`

**Função:** Buscar exemplos CONCRETOS em 33 roteiros clássicos

**Roteiros Indexados:**
1. Pulp Fiction (Tarantino)
2. Inception (Nolan)
3. The Dark Knight (Nolan)
4. Gladiator
5. American Beauty
6. Star Wars IV
7. The Matrix
8. ... e mais 26 roteiros clássicos

**Output Exemplo:**
```python
{
    'total_examples': 6,
    'screenplays_searched': 33,
    'examples_found': [
        {
            'problem_addressed': 'Lacking distinct character voices',
            'screenplay': 'Pulp Fiction',
            'character': 'JULES',  # ← PERSONAGEM REAL!
            'dialogue': 'The path of the righteous man...',  # ← DIÁLOGO REAL!
            'context': 'Opening apartment scene',  # ← CENA REAL!
            'why_good': 'Biblical cadence creates unique voice',
            'lesson': 'Give each character unique rhythm and vocabulary'
        },
        ...
    ]
}
```

**Como Funcionava:**
1. Core 1 (Python) identifica problema técnico
2. Core 2 busca em 33 roteiros mestres exemplos de como resolver
3. Core 3 (LLM) recebe os EXEMPLOS REAIS no prompt
4. LLM analisa baseado em DADOS CONCRETOS, não inventando

---

### Sistema Atual - Core 2 REMOVIDO

**Status:** ❌ NÃO EXISTE

**Consequência:**
- LLM não recebe exemplos concretos
- LLM precisa "adivinhar" como resolver problemas
- LLM INVENTA personagens, cenas, diálogos

**Evidência da Alucinação:**

Roteiro "Te Encontro em Mim" (16 páginas):
```
❌ LLM citou: "CENA 6 (página 15): Sofia mostra contradição"
❌ LLM citou: "CENA 10 (página 35): Julio descreve Sofia"
❌ LLM citou: "CENA 18 (página 60): Sofia não mostra transformação"
❌ LLM citou: "CENA 25 (página 80): Personagens secundários"
```

**PROBLEMA:**
- Roteiro só tem 16 páginas (não tem página 35, 60, 80!)
- Personagens "Sofia", "Julio", "Maria", "Ana" NÃO EXISTEM no roteiro
- LLM está INVENTANDO tudo

---

## 📝 COMPARAÇÃO DOS ORCHESTRATORS

### Sistema Antigo - TripleCoreWrapper

**Arquivo:** `/triple_core/orchestrators/triple_core_wrapper.py`

```python
class TripleCoreWrapper(DualCoreWrapper):
    """
    Herda DualCoreWrapper e ADICIONA Core 2 (Examples)

    Flow:
    1. Core 1 (Python) analisa → métricas técnicas
    2. Core 2 (Examples) busca → 6 exemplos de 33 roteiros
    3. Core 3 (LLM) recebe métricas + EXEMPLOS REAIS
    4. Synthesis combina tudo
    """

    def __init__(self, python_specialist, llm_model, deep_context=True):
        super().__init__(python_specialist, llm_model, deep_context)
        self.example_finder = ExampleFinderCore()  # ← CRÍTICO!

    def analyze(self, screenplay_text):
        # 1. Python analysis
        python_result = self.python_specialist.analyze(screenplay_text)

        # 2. Find REAL examples ← ✅ ESTE PASSO NÃO EXISTE NO ATUAL!
        examples = self.example_finder.analyze(
            base_analysis=python_result,
            screenplay_text=screenplay_text
        )

        # 3. LLM enrichment WITH REAL EXAMPLES
        llm_result = self._call_llm(
            screenplay_text,
            python_metrics=python_result,
            real_examples=examples  # ← LLM recebe EXEMPLOS REAIS!
        )

        return synthesis
```

---

### Sistema Atual - DualCoreWrapper

**Arquivo:** `/engine/orchestration/dual_core_wrapper.py`

```python
class DualCoreWrapper:
    """
    Apenas 2 cores: Python + LLM
    SEM Core 2 (Examples)
    """

    def __init__(self, python_specialist, llm_model, deep_context=True):
        self.python_specialist = python_specialist
        self.llm_model = llm_model
        # ❌ NÃO TEM: self.example_finder

    def analyze(self, screenplay_text):
        # 1. Python analysis
        python_result = self.python_specialist.analyze(screenplay_text)

        # 2. ❌ PASSO REMOVIDO: Buscar exemplos reais

        # 3. LLM enrichment WITHOUT EXAMPLES
        llm_result = self._call_llm(
            screenplay_text,
            python_metrics=python_result
            # ❌ NÃO TEM: real_examples
        )

        return synthesis
```

**Diferença Crítica:**
- Antigo: LLM recebe `real_examples` com personagens/diálogos REAIS
- Atual: LLM NÃO recebe exemplos → INVENTA

---

## 🎯 DIFERENÇAS CRÍTICAS IDENTIFICADAS

### 1. Arquitetura

| Aspecto | Sistema Antigo | Sistema Atual | Impacto |
|---------|---------------|---------------|---------|
| **Cores** | 3 (Python + Examples + LLM) | 2 (Python + LLM) | ❌ CRÍTICO |
| **Examples** | 6 de 33 roteiros mestres | 0 (não existe) | ❌ CRÍTICO |
| **Pasta** | `/triple_core/` | `/engine/` | ⚠️ Mudança |
| **Wrapper** | TripleCoreWrapper | DualCoreWrapper | ❌ CRÍTICO |

### 2. Modelfile

| Aspecto | Sistema Antigo | Sistema Atual | Status |
|---------|---------------|---------------|--------|
| **Proibições** | ✅ Explícitas (linhas 28-32) | ❓ Desconhecido | 🔍 Investigar |
| **Temperature** | 0.2 (conservador) | ❓ | 🔍 Investigar |
| **Seed** | 1337 (fixo) | ❓ | 🔍 Investigar |
| **System Prompt** | 96 linhas (detalhado) | ❓ | 🔍 Investigar |

### 3. Dados de Treinamento/Contexto

| Aspecto | Sistema Antigo | Sistema Atual | Impacto |
|---------|---------------|---------------|---------|
| **Roteiros Mestres** | 33 indexados | 0 (não existe) | ❌ CRÍTICO |
| **Examples por Análise** | 6 concretos | 0 | ❌ CRÍTICO |
| **Personagens REAIS** | Sim (de 33 roteiros) | Não | ❌ CRÍTICO |
| **Diálogos REAIS** | Sim (citações exatas) | Não | ❌ CRÍTICO |

---

## 💡 CAUSA RAIZ DA ALUCINAÇÃO

### Por que o Sistema Atual Alucina?

**Sequência de Falha:**

1. **Core 2 foi removido**
   - `/triple_core/core_2_examples/` não existe no sistema atual
   - 33 roteiros mestres não estão mais indexados
   - ExampleFinderCore não é chamado

2. **LLM não recebe exemplos concretos**
   - Prompt do LLM NÃO inclui `real_examples`
   - LLM não tem REFERÊNCIAS de personagens/diálogos reais
   - LLM não sabe quais são os personagens do roteiro sendo analisado

3. **LLM preenche o vazio inventando**
   - Como precisa dar exemplos mas não tem dados reais
   - Inventa personagens genéricos (Sofia, Julio, Maria, Ana)
   - Inventa números de cena/página aleatórios (35, 60, 80)
   - Inventa diálogos que "soam plausíveis"

4. **Validação NER detecta mas não previne**
   - Logs mostram: `hallucinated=['SOFIA', 'JULIO', 'MARIA']`
   - Sistema DETECTA a alucinação
   - Mas não PARA a geração (só warning)

---

## 🔥 REGRA CRÍTICA VIOLADA

Do README do Triple-Core (linha 351):

> **2. CORE 2 NÃO VAI PARA LLM** - Apenas na síntese

**Interpretação INCORRETA que pode ter causado remoção:**

Alguém pode ter lido "Core 2 não vai para LLM" e pensado:
- ❌ "Então o Core 2 não é necessário"
- ❌ "Podemos remover o Core 2"

**Significado CORRETO:**

- ✅ Core 2 busca os exemplos
- ✅ Examples vão para o PROMPT do LLM (não como análise)
- ✅ LLM usa examples como GROUNDING
- ✅ Na síntese final, examples aparecem separadamente

**O Core 2 é FUNDAMENTAL para prevenir alucinações!**

---

## 📊 COMPARAÇÃO DE QUALIDADE

### Output do Sistema Antigo (4 out)

```
✅ ANÁLISE 1: CAMPBELL

1. INTERPRETAÇÃO
A análise do Python revelou que o diálogo da personagem Samantha
na cena 12 é puramente expositivo, declarando seu estado emocional
diretamente sem mostrar comportamento. McKee adverte no Capítulo 7
contra "on-the-nose dialogue", onde os personagens explicam seus
sentimentos ao invés de agir...

[Cita SAMANTHA REAL, CENA 12 REAL, DIÁLOGO REAL]
```

**Características:**
- ✅ Personagens do roteiro (Samantha, Alberto, Kleber)
- ✅ Cenas reais (6, 8, 12, 15)
- ✅ Diálogos citados corretamente
- ✅ Contexto verificável

---

### Output do Sistema Atual (14 out)

```
❌ PROBLEMA 1: Deep Character

CENA 6 (página 15): Sofia mostra contradição
DIÁLOGO ATUAL (unidimensional - só superfície):
"Eu sou uma pessoa organizada. Gosto de planejar tudo."

CENA 10 (página 35): Julio descreve Sofia
CENA 18 (página 60): Sofia não mostra transformação
CENA 25 (página 80): Personagens secundários (Maria e Ana)
```

**Características:**
- ❌ Personagens INVENTADOS (Sofia, Julio, Maria, Ana)
- ❌ Páginas IMPOSSÍVEIS (roteiro só tem 16 páginas!)
- ❌ Diálogos INVENTADOS
- ❌ Contexto FALSO

---

## 🛠️ PRÓXIMOS PASSOS RECOMENDADOS

### Opção 1: Restaurar Triple-Core (RECOMENDADO)

1. ✅ Copiar `/triple_core/` do backup de 4 out
2. ✅ Restaurar `/content/screenplays/` (33 roteiros mestres)
3. ✅ Verificar Modelfile tem proibições anti-alucinação
4. ✅ Atualizar `analyze_all_specialists.py` para usar TripleCoreWrapper
5. ✅ Re-executar análise com qualidade 1.00

**Tempo estimado:** 2-3 horas de trabalho

---

### Opção 2: Melhorar Dual-Core Atual

1. ⚠️ Adicionar regras anti-alucinação ao Modelfile
2. ⚠️ Implementar validação NER que PARA geração
3. ⚠️ Adicionar "character extraction" no Python Core
4. ⚠️ Passar lista de personagens reais para LLM

**Tempo estimado:** 5-8 horas de trabalho
**Risco:** Pode não atingir qualidade 1.00 do Triple-Core

---

### Opção 3: Investigação Adicional

Antes de qualquer mudança, investigar:

1. 🔍 `ollama show scripturemon-optimized --modelfile`
   - Verificar se tem as proibições anti-alucinação
   - Comparar parâmetros

2. 🔍 Verificar se `TripleCoreWrapper` ainda existe em algum lugar
   ```bash
   find /Users/clubproducoes/Digimundo -name "*triple*.py" 2>/dev/null
   ```

3. 🔍 Verificar git history
   ```bash
   git log --all --grep="triple" --oneline
   git log --all --grep="core.*2" --oneline
   ```

4. 🔍 Procurar nos backups
   ```bash
   find /Users/clubproducoes/Digimundo -name "*.zip" -newermt "2025-10-03" ! -newermt "2025-10-05"
   ```

---

## 📋 CHECKLIST DE VALIDAÇÃO

Após restaurar o sistema, validar:

- [ ] Diretório `/triple_core/` existe
- [ ] Pasta `/triple_core/core_2_examples/` existe
- [ ] Arquivo `example_finder.py` existe
- [ ] 33 roteiros em `/content/screenplays/` ou similar
- [ ] Modelfile tem "PROIBIÇÕES ABSOLUTAS" (linhas 28-32)
- [ ] `analyze_all_specialists.py` usa `TripleCoreWrapper`
- [ ] Teste com roteiro conhecido gera personagens REAIS
- [ ] Zero warnings de `hallucinated` no log
- [ ] Quality Score >= 0.85

---

## 📚 DOCUMENTOS RELACIONADOS

Do Sistema Antigo (4 out):
- `/triple_core/README.md` - Arquitetura completa
- `/docs/architecture/TRIPLE_CORE_DESIGN.md` - Design decisions
- `/results/v4.1_graduation/` - Testes de validação

Logs do Sistema Atual:
- `/analysis_progress_0015.log` - Mostra alucinações detectadas
- Checkpoint 0015 - 147/312 análises com alucinações

---

## ✅ CONCLUSÃO

**Causa Raiz Identificada:**

A remoção do **CORE 2 (Master Examples Finder)** causou as alucinações porque:

1. LLM não recebe mais exemplos REAIS de 33 roteiros mestres
2. LLM não sabe quais são os personagens do roteiro sendo analisado
3. LLM preenche o vazio inventando personagens/cenas/diálogos
4. Validação NER detecta mas não previne (só warning)

**Solução Recomendada:**

Restaurar arquitetura **TRIPLE-CORE** do backup de 4 de outubro, que tinha:
- ✅ Quality Score 1.00/1.0 EXCELLENT
- ✅ 6 exemplos REAIS por análise
- ✅ Zero alucinações
- ✅ Modelfile com proibições explícitas

**Status:** Aguardando decisão do usuário para próximos passos.

---

**Criado:** 2025-10-14
**Autor:** Claude (Análise Comparativa)
**Versão:** 1.0
