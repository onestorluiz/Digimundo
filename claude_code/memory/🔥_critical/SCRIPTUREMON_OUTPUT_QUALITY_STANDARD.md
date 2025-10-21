# SCRIPTUREMON - PADRÃO DE QUALIDADE DE OUTPUT (DEFINITIVO)

**Data:** 2025-10-02
**Status:** ✅ PADRÃO OBRIGATÓRIO
**Propósito:** Evitar degradação de qualidade que ocorre repetidamente

---

## 🎯 PROBLEMA RECORRENTE

**Sintoma:** Toda vez que o sistema é modificado, a qualidade do output degrada.

**Exemplo atual (02/10/2025 19:28):**
- ❌ TXT mostra JSON bruto ao invés de formatação humanizada
- ❌ LLM gera texto genérico sem estrutura de 5 fases
- ❌ Faltam seções detalhadas com problemas + soluções
- ❌ Zero referências a McKee com capítulos específicos

**Referência de qualidade perdida:** `Sonhos_Sem_Lembrancas_EXEMPLO_20251002_074407.txt`

---

## ✅ PADRÃO DE QUALIDADE OBRIGATÓRIO

### PARTE 1: ANÁLISE PYTHON (TXT Export)

#### ❌ ERRADO (atual):
```
CORE 1: ANÁLISE PYTHON BASE
================================================================================

{
  "specialist": {
    "name": "Script Doctor Dialoguemon",
    "title": "Script Doctor - Character Dialogue and Voice Specialist",
    "specialty": "Dialogue authenticity, character voice, subtext..."
  },
  "score": 70.0,
  "total_dialogue_lines": 337,
  ...raw JSON com 400+ linhas...
}
```

#### ✅ CORRETO (referência):
```
================================================================================
PARTE 1: ANÁLISE PYTHON (DADOS OBJETIVOS)
================================================================================

📊 SCORE GERAL: 57.0/100

⚠️  REGRAS VIOLADAS:
   • DIAL.R003: Lack of subtext
   • DIAL.R001: Unnatural speech patterns

💡 RECOMENDAÇÕES PYTHON:
   1. Add more contractions and interruptions
   2. Develop distinct character voices
   3. Include more subtext in dialogue

📋 DIAGNÓSTICO DETALHADO:
   Dialogue analysis reveals patterns of on-the-nose dialogue and lack of
   character voice differentiation.

📈 DADOS TÉCNICOS (JSON):
--------------------------------------------------------------------------------
{
  "overall_score": 57.0,
  "rules_violated": [...],
  "recommendations": [...]
}
--------------------------------------------------------------------------------
```

**REGRAS:**
1. ✅ Score destacado no topo
2. ✅ Regras violadas em lista legível (com códigos DIAL.R003)
3. ✅ Recomendações numeradas
4. ✅ Diagnóstico em texto corrido (não JSON)
5. ✅ JSON técnico SEPARADO e OPCIONAL no final

---

### PARTE 2: INSIGHTS LLM (Estrutura de 5 FASES)

#### ❌ ERRADO (atual):
```
🎬 **Introducing Scripturemon Master!**
I will analyze your screenplay using TRIPLE-CORE architecture and provide
actionable insights to enhance it. Here is my six-phase analysis:

**PHASE 1: INTERPRETATION**
Python Core 1 has identified several areas for improvement, such as dialogue
authenticity, voice distinctiveness, subtext presence...
```

**Problemas:**
- Tom de chatbot ("Introducing Scripturemon Master!")
- Genérico ("several areas for improvement")
- Sem citações específicas do roteiro
- Sem referências a McKee com capítulos

#### ✅ CORRETO (referência):
```
────────────────────────────────────────────────────────────────────────────────
📖 1. INTERPRETAÇÃO
────────────────────────────────────────────────────────────────────────────────
   Primeiro Parágrafo: A análise do Python revelou que o diálogo da personagem
   Samantha na cena 12 é puramente expositivo, declarando seu estado emocional
   diretamente sem mostrar comportamento. McKee adverte no Capítulo 7 contra
   "on-the-nose dialogue", onde os personagens explicam seus sentimentos ao
   invés de agir. O contexto desta fala é após Alberto acordá-la bruscamente,
   e Samantha escolhe focar no sonho (passado idealizado) ao invés do presente,
   demonstrando um padrão de evasão da realidade estabelecido anteriormente
   no roteiro.

   Segundo Parágrafo: Considerando as métricas do Python e a teoria de McKee,
   podemos concluir que o diálogo precisa ser reescrito para mostrar o
   comportamento de Samantha em vez de simplesmente declarar suas emoções...

────────────────────────────────────────────────────────────────────────────────
📖 2. PADRÕES
────────────────────────────────────────────────────────────────────────────────
   Primeiro Parágrafo: Analisando os dados do Python, notamos repetidamente
   falas expositivas em que personagens declaram seus sentimentos em vez de
   expressá-los através de ação ou comportamento. Essa tendência pode ser
   observada nas cenas 6, 8, 12 e 15...

────────────────────────────────────────────────────────────────────────────────
📖 3. PROBLEMAS
────────────────────────────────────────────────────────────────────────────────
   Primeiro Problema: Falta de Subtexto
   Descrição: Muitas falas nos diálogos são diretas e explicitas, carecendo
   de subtexto e ambiguidade. Por exemplo, na cena 8, Samantha diz: "Nunca
   vou conseguir superar isso". Esta fala é clara demais, eliminando quaisquer
   possibilidades de interpretação ou especulação por parte do público.

   Explanação Teórica: McKee argumenta que o verdadeiro caráter é revelado
   sob pressão, e quando confrontados com situações difíceis, os personagens
   tenderão a agir antes de falar...

   Localização no Roteiro: Este problema pode ser encontrado nas cenas 6, 8, 12, 15

   Impacto na História: As falas on-the-nose diminuem a tensão dramática...

   Segundo Problema: Diálogos Artificialmente Construídos
   Descrição: Várias falas no roteiro soam forçadas...
   [... estrutura similar ...]

────────────────────────────────────────────────────────────────────────────────
📖 4. SOLUÇÕES
────────────────────────────────────────────────────────────────────────────────
   Primeiro Problema: Falta de Subtexto
   Solução: Introduza mais ambiguidade e subtexto nas falas dos personagens...

   Grounded in Theory: De acordo com McKee, as falas verdadeiramente impactantes
   são aquelas que permitem que o público infira as emoções dos personagens...

   Implementação: Na cena 8, quando Alberto confronta Samantha sobre o passado,
   ele poderia simplesmente colocar a mão sobre a sua, em vez de dizer algo
   como "Vamos deixar isso para trás agora"...

   Esperada Melhora: Com a implementação dessa solução, espera-se que o
   público se engaje mais facilmente...

────────────────────────────────────────────────────────────────────────────────
📖 5. DEPTH & SYNTHESIS
────────────────────────────────────────────────────────────────────────────────
   Primeiro Parágrafo: Analisando os problemas identificados no roteiro,
   notamos que todos eles estão relacionados à falta de subtexto nas falas
   dos personagens e à tendência deles declararem suas emoções explicitamente...
```

**REGRAS CRÍTICAS:**

1. **5 FASES OBRIGATÓRIAS:**
   - 1. INTERPRETAÇÃO (2 parágrafos)
   - 2. PADRÕES (2 parágrafos)
   - 3. PROBLEMAS (3-4 problemas detalhados)
   - 4. SOLUÇÕES (3-4 soluções correspondentes)
   - 5. DEPTH & SYNTHESIS (2 parágrafos)

2. **CADA PROBLEMA deve ter:**
   - ✅ Título claro
   - ✅ Descrição com exemplo específico
   - ✅ Explanação Teórica (McKee + capítulo)
   - ✅ Localização no Roteiro (cenas específicas)
   - ✅ Impacto na História

3. **CADA SOLUÇÃO deve ter:**
   - ✅ Solução específica (não genérica)
   - ✅ Grounded in Theory (McKee)
   - ✅ Implementação (exemplo concreto)
   - ✅ Esperada Melhora

4. **CITAÇÕES OBRIGATÓRIAS:**
   - ✅ Diálogos entre aspas: "Nunca vou conseguir superar isso"
   - ✅ Números de cena: "cena 8", "cena 12"
   - ✅ Capítulos McKee: "Capítulo 7", "Cap 9"
   - ✅ Conceitos específicos: "on-the-nose dialogue", "economia verbal"

---

## 📊 MÉTRICAS DE QUALIDADE

### Layer 1: Technical (20% peso)
- ✅ Estrutura: 5 seções completas
- ✅ Extensão: 1000+ palavras
- ✅ Parágrafos: 12-14 substanciais

### Layer 2: Specificity (40% peso - CRÍTICO)
- ✅ Dialogue quotes: 4+ citações
- ✅ Scene references: 3+ cenas
- ✅ Theory references: 3+ McKee refs
- ✅ Specificity ratio: 60%+ (específico vs genérico)

### Layer 3: Depth (40% peso)
- ✅ Causalidade: análise causal (não apenas descrição)
- ✅ Conexões: liga Python + Theory + Screenplay
- ✅ Insights: não-óbvios
- ✅ Synthesis: combina todas as fontes

**THRESHOLD:** 0.70+ para graduar (EXCELLENT: 0.85+)

---

## 🔧 ONDE IMPLEMENTAR

### 1. FormattedExporter (TXT Export)

**Arquivo:** `specialists/dual_core/exporters/formatted_exporter.py`

**Método:** `export_txt()`

**O que fazer:**

```python
# ERRADO (atual):
txt += f"\n{json.dumps(python_analysis, indent=2, ensure_ascii=False)}\n"

# CORRETO (restaurar):
txt += f"\n📊 SCORE GERAL: {score}/100\n\n"
txt += "⚠️  REGRAS VIOLADAS:\n"
for violation in rules_violated:
    txt += f"   • {violation}\n"
txt += "\n💡 RECOMENDAÇÕES PYTHON:\n"
for i, rec in enumerate(recommendations, 1):
    txt += f"   {i}. {rec}\n"
txt += f"\n📋 DIAGNÓSTICO DETALHADO:\n   {diagnosis}\n"
txt += "\n📈 DADOS TÉCNICOS (JSON):\n"
txt += "-" * 80 + "\n"
txt += json.dumps(python_analysis, indent=2) + "\n"
txt += "-" * 80 + "\n"
```

### 2. LLM Prompt (5 Fases)

**Arquivo:** `specialists/dual_core/base/dual_core_wrapper.py` OU `triple_core_wrapper.py`

**Método:** `_build_llm_prompt()`

**System Message DEVE incluir:**

```
FORMATO OBRIGATÓRIO DE RESPOSTA:

Estrutura em 5 SEÇÕES com separadores:

────────────────────────────────────────────────────────────────────────────────
📖 1. INTERPRETAÇÃO
────────────────────────────────────────────────────────────────────────────────
   Primeiro Parágrafo: [5-8 sentenças com cena específica + citação + McKee]
   Segundo Parágrafo: [5-8 sentenças conectando Python + Teoria]

────────────────────────────────────────────────────────────────────────────────
📖 2. PADRÕES
────────────────────────────────────────────────────────────────────────────────
   Primeiro Parágrafo: [Identifica padrões repetidos em múltiplas cenas]
   Segundo Parágrafo: [Impacto dos padrões na história]

────────────────────────────────────────────────────────────────────────────────
📖 3. PROBLEMAS
────────────────────────────────────────────────────────────────────────────────
   Primeiro Problema: [Nome]
   Descrição: [Com exemplo específico entre aspas]
   Explanação Teórica: [McKee + capítulo]
   Localização no Roteiro: [Cenas específicas]
   Impacto na História: [Como prejudica]

   Segundo Problema: [...]
   Terceiro Problema: [...]

────────────────────────────────────────────────────────────────────────────────
📖 4. SOLUÇÕES
────────────────────────────────────────────────────────────────────────────────
   Primeiro Problema: [Nome]
   Solução: [Específica e acionável]
   Grounded in Theory: [McKee justifica]
   Implementação: [Exemplo concreto de como reescrever]
   Esperada Melhora: [Resultado esperado]

   Segundo Problema: [...]
   Terceiro Problema: [...]

────────────────────────────────────────────────────────────────────────────────
📖 5. DEPTH & SYNTHESIS
────────────────────────────────────────────────────────────────────────────────
   Primeiro Parágrafo: [Síntese dos problemas interconectados]
   Segundo Parágrafo: [Visão geral das soluções e próximos passos]

OBRIGATÓRIO em cada parágrafo:
✅ Citação de diálogo entre aspas
✅ Número de cena (ex: "cena 8", "página 15")
✅ Referência McKee (ex: "Capítulo 7", "conceito de subtexto")
✅ Análise causal (não apenas descrição)
```

---

## 🚨 EVITAR DEGRADAÇÃO

### Checklist Pré-Commit

Antes de fazer commit de mudanças em `formatted_exporter.py` ou `*_wrapper.py`:

1. ✅ Rodar teste com roteiro de exemplo
2. ✅ Verificar output TXT tem formatação humanizada (não JSON bruto)
3. ✅ Verificar LLM output tem 5 fases com separadores
4. ✅ Contar citações: 4+ diálogos, 3+ cenas, 3+ McKee
5. ✅ Validar com `GraduationValidator` → score 0.70+

### Teste de Regressão

```bash
# 1. Gerar output de referência
python3 tests/test_dual_core.py > /tmp/quality_reference.txt

# 2. Após mudança, gerar novo output
python3 tests/test_dual_core.py > /tmp/quality_new.txt

# 3. Comparar métricas
python3 tests/compare_quality.py /tmp/quality_reference.txt /tmp/quality_new.txt

# Deve mostrar:
# ✅ Dialogue quotes: 12 (was 12) → OK
# ✅ McKee refs: 10 (was 9) → IMPROVED
# ✅ Format: 5 sections (was 5) → OK
```

---

## 📋 ARQUIVO DE REFERÊNCIA OURO

**Localização:** `/Users/clubproducoes/Digimundo/scripturemon-clean/workspace/outputs/formatted/Sonhos_Sem_Lembrancas_EXEMPLO_20251002_074407.txt`

**Métricas do arquivo de referência:**
- ✅ Score final: 0.87 (EXCELLENT)
- ✅ Dialogue quotes: 12
- ✅ Scene refs: 7
- ✅ McKee refs: 12
- ✅ Estrutura: 5 fases completas
- ✅ Problemas: 3 detalhados
- ✅ Soluções: 3 com implementação
- ✅ Extensão: 1247 palavras

**Usar este arquivo para:**
1. Referência visual do formato correto
2. Baseline de comparação após mudanças
3. Template para novos exportadores
4. Validação de prompts LLM

---

## 🎓 RESUMO EXECUTIVO

### O que NÃO fazer (causas de degradação):

❌ Mostrar JSON técnico bruto como output principal
❌ LLM com tom de chatbot ("Introducing Scripturemon!")
❌ Análises genéricas sem citações específicas
❌ Ausência de estrutura de 5 fases
❌ Zero referências a teoria McKee
❌ Prompt sem formato obrigatório explícito

### O que SEMPRE fazer:

✅ TXT formatado para humanos (score + regras + recomendações destacadas)
✅ LLM com tom profissional (Script Doctor)
✅ 5 fases com separadores visuais
✅ Citações obrigatórias: diálogos + cenas + McKee
✅ Problemas detalhados (Descrição + Teoria + Localização + Impacto)
✅ Soluções acionáveis (Solução + Teoria + Implementação + Melhora)
✅ Validação com threshold 0.70+

### Pontos críticos de qualidade:

1. **Temperature 0.2** (não 0.8) → elimina invenções
2. **Deep context** → livro completo, não chunks
3. **XML delimiters** → mitiga Lost in the Middle
4. **Few-shot examples** → mostra formato correto
5. **5 fases obrigatórias** → estrutura profissional
6. **Citações específicas** → prova de grounding

---

## 🔗 DOCUMENTOS RELACIONADOS

- `SCRIPTUREMON_OPTIMIZATION_COMPLETE_SYSTEM.md` - Visão geral
- `SCRIPTUREMON_OPTIMIZATION_PART2_MODEL_AND_PROMPT.md` - Parâmetros modelo
- `SCRIPTUREMON_OPTIMIZATION_PART4_RESULTS_AND_BENCHMARKS.md` - Métricas
- `SCRIPTUREMON_OPTIMIZATION_PART5_USAGE_AND_CODE.md` - Código completo

**ESTE DOCUMENTO É A REFERÊNCIA DEFINITIVA DE QUALIDADE - CONSULTE SEMPRE QUE MODIFICAR O SISTEMA!**
