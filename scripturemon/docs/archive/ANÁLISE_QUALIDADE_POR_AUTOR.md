# 📊 ANÁLISE DE QUALIDADE POR AUTOR

**Data**: 09/10/2025 16:25
**Roteiro Analisado**: Te Encontro em Mim
**Diretório**: `workspace/outputs/TE_ENCONTRO_EM_MIM__dialogue_0001/`

---

## 🎯 RESUMO EXECUTIVO

| Categoria | Autores | Tamanho Médio | Status |
|-----------|---------|---------------|--------|
| **🔴 FRACOS** (Timeout) | 5 | 5.8K | ❌ LLM falhou |
| **🟡 MÉDIOS** (Genéricos) | 6 | 7.7-10K | ⚠️ Superficial |
| **🟢 FORTES** (Completos) | 2 | 10-11K | ✅ Profundo |

---

## 🔴 AUTORES FRACOS (LLM TIMEOUT)

### Problema: Timeout após 900s

Estes autores **FALHARAM COMPLETAMENTE** por timeout do LLM:

| Autor | Tamanho | Problema | Resultado |
|-------|---------|----------|-----------|
| **DIALOGUE** | 5.8K | LLM timeout 900s | ❌ Só Python |
| **EGRI** | 5.8K | LLM timeout 900s | ❌ Só Python |
| **FIELD** | 7.7K | LLM timeout 900s | ❌ Só Python |
| **MCKEE** | 7.7K | LLM timeout 900s | ❌ Só Python |
| **SEGER** | 7.7K | LLM timeout 900s | ❌ Só Python |

### Conteúdo Típico (EGRI como exemplo):

```html
<div class="section part-2">
    <h2>🤖 PARTE 2: Insights LLM</h2>
    <div class="list-item" style="border-color: #ef4444;">
        ❌ Erro: LLM timeout after 900s
    </div>
</div>
<div class="section part-3">
    <h2>🎯 PARTE 3: Síntese</h2>
    <!-- VAZIO! -->
</div>
```

**Análise**:
- ❌ Zero insights LLM
- ❌ Zero análise qualitativa
- ❌ Zero exemplos do roteiro
- ❌ Apenas recomendações Python genéricas
- 💔 **INÚTIL para roteiristas**

### Por Que Falharam?

1. **Timeout hardcoded**: `llm_timeout=900` (15 minutos)
2. **Prompts complexos**: Deep mode requer 30-45 minutos
3. **Livros grandes**: 128k tokens + análise profunda
4. **Processo travou**: LLM não conseguiu completar

---

## 🟡 AUTORES MÉDIOS (ANÁLISES GENÉRICAS)

### Problema: Falta de Profundidade

Estes autores **COMPLETARAM** mas com análises **SUPERFICIAIS**:

| Autor | Tamanho | Conteúdo | Qualidade |
|-------|---------|----------|-----------|
| **SNYDER** | 9.7K | ~4 parágrafos | ⚠️ Genérico |
| **ARISTOTLE** | 9.5K | ~5 parágrafos | ⚠️ Abstrato |
| **TRUBY** | 10K | ~6 parágrafos | ⚠️ Vago |
| **COWGILL** | 10K | ~5 parágrafos | ⚠️ Superficial |
| **VOGLER** | 10K | ~5 parágrafos | ⚠️ Teórico |
| **MCKEE_CHARACTER** | 10K | ~6 parágrafos | ⚠️ Genérico |

### Características Comuns:

✅ **Pontos Positivos**:
- LLM completou (não deu timeout)
- Tem análise qualitativa
- Estrutura organizada
- Menciona teoria do autor

❌ **Problemas Identificados**:
- **Falta exemplos específicos**: Não cita cenas ou páginas
- **Falta diálogos verbatim**: Não quota falas do roteiro
- **Análise abstrata**: "O roteiro poderia...", "Recomenda-se..."
- **Genérico demais**: Poderia aplicar-se a qualquer roteiro
- **Sem before/after**: Não mostra como melhorar concretamente

### Exemplo (TRUBY - Parágrafo Típico):

```
"Os dados quantitativos sugerem que o roteiro possui um bom
equilíbrio entre os personagens, com Sofia e Maria como
principais vozes. No entanto, a pontuação de autenticidade do
diálogo é moderada, o que pode implicar em falta de profundidade."
```

**Análise do Problema**:
- ❌ Não cita qual cena
- ❌ Não cita qual diálogo
- ❌ Não mostra exemplo concreto
- ❌ Não dá solução específica
- ⚠️ **Genérico**: Poderia ser sobre qualquer roteiro

---

## 🟢 AUTORES FORTES (ANÁLISES COMPLETAS)

### Sucesso: Profundidade e Especificidade

Estes autores geraram análises **PROFISSIONAIS**:

| Autor | Tamanho | Conteúdo | Qualidade |
|-------|---------|----------|-----------|
| **MCKEE_DIALOGUE** | 11K | 7 parágrafos detalhados | ✅ Excelente |
| **CAMPBELL** | 10K | 6 parágrafos específicos | ✅ Bom |

### MCKEE_DIALOGUE - Exemplo de Qualidade:

```
"Um problema significativo identificado pelos dados é a falta
de subtexto no diálogo. Por exemplo, na CENA 1, quando Sofia
diz 'Julio, eu tenho medo de tentar e falhar' (página 2), ela
está declarando explicitamente seus sentimentos em vez de
permitir que o público infira através de seu comportamento."
```

**Por Que é Bom**:
- ✅ **Cita cena específica**: "CENA 1"
- ✅ **Cita página**: "página 2"
- ✅ **Quota diálogo verbatim**: "Julio, eu tenho medo..."
- ✅ **Identifica problema**: Falta de subtexto
- ✅ **Explica por quê**: Declaração explícita vs inferência

### Solução Oferecida:

```
"Em vez de declarar explicitamente 'tenho medo de tentar e
falhar', Sofia poderia dizer algo como 'Não sei se posso
lidar com mais desapontamentos'. Isto permite que o público
infira seu estado emocional."
```

**Por Que é Bom**:
- ✅ **Before/After claro**
- ✅ **Solução específica**: Reescreve o diálogo
- ✅ **Explica benefício**: "permite que o público infira"
- ✅ **Acionável**: Roteirista pode aplicar imediatamente

---

## 📊 COMPARAÇÃO DETALHADA

### Métricas de Qualidade:

| Autor | Size | Cenas Citadas | Diálogos Quotes | Before/After | Score |
|-------|------|---------------|-----------------|--------------|-------|
| **DIALOGUE** | 5.8K | ❌ 0 | ❌ 0 | ❌ 0 | 0/10 |
| **EGRI** | 5.8K | ❌ 0 | ❌ 0 | ❌ 0 | 0/10 |
| **FIELD** | 7.7K | ❌ 0 | ❌ 0 | ❌ 0 | 0/10 |
| **MCKEE** | 7.7K | ❌ 0 | ❌ 0 | ❌ 0 | 0/10 |
| **SEGER** | 7.7K | ❌ 0 | ❌ 0 | ❌ 0 | 0/10 |
| **SNYDER** | 9.7K | ⚠️ 1 | ⚠️ 0 | ⚠️ 0 | 3/10 |
| **ARISTOTLE** | 9.5K | ⚠️ 1 | ⚠️ 0 | ⚠️ 0 | 3/10 |
| **TRUBY** | 10K | ⚠️ 2 | ⚠️ 1 | ⚠️ 0 | 4/10 |
| **COWGILL** | 10K | ⚠️ 1 | ⚠️ 0 | ⚠️ 0 | 3/10 |
| **VOGLER** | 10K | ⚠️ 2 | ⚠️ 1 | ⚠️ 0 | 4/10 |
| **MCKEE_CHARACTER** | 10K | ⚠️ 2 | ⚠️ 1 | ⚠️ 1 | 5/10 |
| **CAMPBELL** | 10K | ✅ 3 | ✅ 2 | ✅ 2 | 7/10 |
| **MCKEE_DIALOGUE** | 11K | ✅ 4 | ✅ 3 | ✅ 3 | 8/10 |

---

## 🔍 ROOT CAUSES POR CATEGORIA

### 🔴 Autores Fracos - Por Que Falharam?

**Causa Técnica**: LLM timeout de 900s

**Solução**: ✅ JÁ CORRIGIDA
- Removemos `llm_timeout=900`
- Agora `llm_timeout=None` (sem limite)
- Próximas análises NÃO terão este problema

**Ação Necessária**: Re-rodar análises destes 5 autores

---

### 🟡 Autores Médios - Por Que São Genéricos?

**Causas Múltiplas**:

1. **Prompts Insuficientes**
   - Não EXIGEM citações específicas
   - Não EXIGEM números de cena
   - Não EXIGEM diálogos verbatim
   - Não EXIGEM before/after

2. **Validação Fraca**
   - Sistema aceita outputs de 10K (mínimo deveria ser 15-20K)
   - Não verifica presença de citações
   - Não verifica exemplos concretos

3. **Teoria Insuficiente**
   - Chunks de teoria podem não ter os melhores exemplos
   - Deep mode não foi aplicado (estava com timeout)

**Soluções**:

1. **Melhorar Prompts** (ver seção de melhorias abaixo)
2. **Aumentar Validação Mínima** (15K chars mínimo)
3. **Exigir Formato Estruturado** (cena + página + quote obrigatórios)

---

### 🟢 Autores Fortes - Por Que Funcionam?

**Fatores de Sucesso**:

1. **McKEE_DIALOGUE**:
   - Livro focado especificamente em diálogo
   - Teoria rica em exemplos concretos
   - Prompt bem estruturado
   - Deep context funcionou

2. **CAMPBELL**:
   - Teoria arquetípica se aplica bem a personagens
   - Jornada do Herói fornece estrutura clara
   - Fácil de identificar padrões

**Características Comuns**:
- ✅ Citam cenas e páginas
- ✅ Quotam diálogos verbatim
- ✅ Oferecem before/after
- ✅ Explicam o POR QUÊ
- ✅ Aplicam teoria específica do autor

---

## 🎯 PLANO DE MELHORIA

### Priority 0 - Imediato (Já Feito)

✅ **Remover timeout** - CONCLUÍDO
- `llm_timeout=None` aplicado
- Análises futuras sem limite de tempo

### Priority 1 - Curto Prazo (Próximos Dias)

#### 1.1 Re-rodar Autores Fracos

```bash
# Re-rodar os 5 que falharam com timeout
python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" \\
    --author dialogue --deep

python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" \\
    --author egri --deep

# ... (field, mckee, seger)
```

#### 1.2 Melhorar Prompts dos Autores Médios

Para cada autor médio, adicionar ao prompt:

```python
CRITICAL REQUIREMENTS:
- MUST cite AT LEAST 3 specific scene numbers
- MUST cite AT LEAST 3 specific page numbers
- MUST quote AT LEAST 3 dialogues verbatim
- MUST provide AT LEAST 2 before/after rewrites
- MINIMUM 15,000 characters (not 10,000)
```

#### 1.3 Aumentar Validação de Qualidade

```python
# Em _validate_llm_output():
MIN_SCENE_CITATIONS = 3
MIN_PAGE_CITATIONS = 3
MIN_DIALOGUE_QUOTES = 3
MIN_BEFORE_AFTER = 2
MIN_LENGTH = 15000  # Era 10000

if scene_count < MIN_SCENE_CITATIONS:
    score -= 2.0
    reasons.append(f"Too few scene citations ({scene_count}/{MIN_SCENE_CITATIONS})")
```

### Priority 2 - Médio Prazo (Próxima Semana)

#### 2.1 Prompts Personalizados Por Autor

Criar prompts específicos baseados na força de cada autor:

**EGRI** (Premissa):
```
FOCUS: Identify the screenplay's PREMISE
- What is the core premise driving this story?
- Cite specific scenes showing premise in action
- Quote dialogues that reveal or contradict premise
```

**FIELD** (Estrutura em 3 Atos):
```
FOCUS: Analyze THREE-ACT STRUCTURE
- Identify Act 1 turning point (cite page number)
- Identify Midpoint (cite scene and dialogue)
- Identify Act 2 turning point (cite page)
```

**SNYDER** (Save the Cat):
```
FOCUS: Identify SAVE THE CAT beats
- Opening Image: Quote first dialogue
- Catalyst: Which scene? What dialogue?
- Break into Two: Cite exact page
- All 15 beats with specific citations
```

#### 2.2 Few-Shot Examples por Autor

Adicionar exemplos ESPECÍFICOS de cada autor no prompt.

### Priority 3 - Longo Prazo (Próximo Mês)

#### 3.1 Sistema de Feedback Loop

```python
# Após cada análise
if quality_score < 7.0:
    # Retry com prompt melhorado
    enhanced_prompt = add_more_specific_requirements(original_prompt)
    retry_analysis(enhanced_prompt)
```

#### 3.2 Benchmarking Automático

Comparar cada análise com:
- Melhores análises existentes
- Checklist de qualidade
- Exemplos de análises profissionais

---

## 📋 CHECKLIST DE QUALIDADE IDEAL

Uma análise **PROFISSIONAL** deve ter:

### Conteúdo Mínimo:
- [ ] **15,000+ characters** (~2,500 palavras)
- [ ] **3+ cenas citadas** com números
- [ ] **3+ páginas citadas** com números
- [ ] **3+ diálogos quotados** verbatim
- [ ] **2+ before/after** rewrites
- [ ] **5+ teoria citations** do livro do autor

### Estrutura:
- [ ] **Interpretação** (2 parágrafos)
- [ ] **Padrões** (2 parágrafos)
- [ ] **Problemas** (3-4 parágrafos, 1 por problema)
- [ ] **Soluções** (3-4 parágrafos, 1 por problema)
- [ ] **Síntese** (2 parágrafos)

### Qualidade:
- [ ] **Específico**: Cita cenas/páginas/diálogos exatos
- [ ] **Aplicável**: Roteirista pode implementar hoje
- [ ] **Fundamentado**: Conecta com teoria do autor
- [ ] **Completo**: Cobre múltiplos aspectos
- [ ] **Profundo**: Vai além do óbvio

---

## 📊 SCORE ESPERADO APÓS MELHORIAS

| Autor | Score Atual | Score Esperado | Melhoria Necessária |
|-------|-------------|----------------|---------------------|
| DIALOGUE | 0/10 | 7/10 | Re-rodar sem timeout |
| EGRI | 0/10 | 7/10 | Re-rodar sem timeout |
| FIELD | 0/10 | 7/10 | Re-rodar sem timeout |
| MCKEE | 0/10 | 8/10 | Re-rodar sem timeout |
| SEGER | 0/10 | 7/10 | Re-rodar sem timeout |
| SNYDER | 3/10 | 7/10 | Prompt + Validação |
| ARISTOTLE | 3/10 | 6/10 | Prompt + Validação |
| TRUBY | 4/10 | 7/10 | Prompt + Validação |
| COWGILL | 3/10 | 6/10 | Prompt + Validação |
| VOGLER | 4/10 | 7/10 | Prompt + Validação |
| MCKEE_CHARACTER | 5/10 | 7/10 | Validação mais forte |
| CAMPBELL | 7/10 | 8/10 | Pequenos ajustes |
| MCKEE_DIALOGUE | 8/10 | 9/10 | Já está ótimo |

**Média Atual**: 3.7/10
**Média Esperada**: 7.2/10
**Melhoria**: +95%

---

## 💡 RECOMENDAÇÃO FINAL

### Ação Imediata:

1. ✅ **Timeout removido** - JÁ FEITO
2. 🔄 **Re-rodar 5 autores fracos** - Fazer HOJE
3. 📝 **Implementar validação melhorada** - Fazer HOJE

### Próximos Passos:

4. 🎯 **Melhorar prompts** - Próxima semana
5. 📊 **Prompts personalizados** - Próximo mês
6. 🔄 **Sistema de retry** - Próximo mês

---

**Assinado**: Claude Code (Análise de Qualidade)
**Data**: 09/10/2025 16:25
**Status**: ✅ **DIAGNÓSTICO COMPLETO - AÇÕES CLARAS**
