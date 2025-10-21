# 🚀 PROPOSTA FASE 4 - Prompts Verdadeiramente Personalizados

**Data**: 10 de Outubro 2025
**Versão**: 1.0
**Status**: 📝 PROPOSTA (Aguardando Aprovação)

---

## 🎯 OBJETIVO FASE 4

Elevar o sistema de **FASE 3** (scores reais 15.5-18.0/10) para **excelência absoluta** (18.0-20.0/10) através de prompts **verdadeiramente personalizados** baseados em análise completa de cada livro de teoria.

### Diferença: FASE 2 vs FASE 4

#### FASE 2 (Atual - "Prompts Personalizados")
❌ **Realidade**: Prompts **melhorados** mas ainda genéricos
- Baseados em conhecimento geral de cada autor
- Mesma estrutura básica para todos os 13 autores
- Instruções adaptadas manualmente
- **Resultado**: Elevou média de 5.8 → 7.5/10 (sistema), real 16.3/10

#### FASE 4 (Proposta - "Prompts Verdadeiramente Personalizados")
✅ **Conceito**: Prompts **únicos** por autor, gerados via LLM
- Baseados em análise COMPLETA de cada livro (~128k tokens)
- Estrutura única adaptada à metodologia específica do autor
- Conexões profundas entre conceitos do livro
- **Resultado Esperado**: Elevar de 16.3/10 → 18.0-20.0/10 real

---

## 📊 PROBLEMA ATUAL (FASE 3)

### Análise do Sistema Atual

**Pontos Fortes**:
- ✅ Deep context (livros completos carregados)
- ✅ Two-Pass LLM (identificar + expandir)
- ✅ Prompts "personalizados" FASE 2
- ✅ Nivel 10 validation
- ✅ Scores reais 15.5-18.0/10 (excelente)

**Limitação Identificada**:
❌ **Prompts FASE 2 são "melhores genéricos", não "verdadeiramente personalizados"**

#### Evidência da Limitação

**Exemplo EGRI - Prompt FASE 2 (Atual)**:
```
EGRI'S METHOD:
1. Core Premise: "X leads to Y"
   - Identify screenplay's premise
   - Cite 3+ scenes

2. Character Premise Alignment
   - Characters embody premise?

3. Premise Through Action
   - Show, don't tell

4. Premise Clarity
   - Is premise clear?
```

**Análise**:
- ✅ Menciona conceitos corretos de Egri
- ❌ Mas são conceitos **genéricos** que qualquer pessoa familiarizada com Egri conhece
- ❌ Não reflete a **profundidade** do livro "The Art of Dramatic Writing"
- ❌ Não faz **conexões específicas** entre capítulos
- ❌ Não usa **exemplos concretos** do livro

---

## 🔬 METODOLOGIA FASE 4

### Processo de Criação de Prompts Verdadeiramente Personalizados

#### ETAPA 1: Análise Completa do Livro (Por Autor)

**Input**:
- Livro completo de teoria (~128k tokens)
- Nome do autor
- Especialidade (dialogue, structure, character, etc.)

**Processo** (via LLM):
```python
prompt_analysis = f"""
Você receberá o livro completo de {autor} sobre {especialidade}.

SUA MISSÃO:
1. Ler o livro INTEIRO
2. Identificar os 10-15 conceitos PRINCIPAIS do autor
3. Mapear as CONEXÕES entre esses conceitos
4. Extrair EXEMPLOS CONCRETOS usados pelo autor
5. Identificar o VOCABULÁRIO ÚNICO do autor
6. Mapear a ESTRUTURA ARGUMENTATIVA do autor

OUTPUT:
- Conceitos principais (lista de 10-15)
- Conexões entre conceitos (grafo)
- Exemplos do livro (5-10 casos)
- Termos técnicos únicos (glossário)
- Estrutura de raciocínio do autor

Livro completo:
{book_full_text}
"""
```

**Output Esperado** (Exemplo EGRI):
```json
{
  "author": "EGRI",
  "specialty": "premise",
  "core_concepts": [
    {
      "concept": "Premise como força motriz",
      "definition": "Uma premissa deve ser provável, não apenas possível",
      "chapter": 1,
      "examples": ["Romeu e Julieta: Grande amor desafia obstáculos leva a tragédia"],
      "connections": ["→ Character needs", "→ Conflict escalation"]
    },
    {
      "concept": "Três-dimensionalidade de personagem",
      "definition": "Fisiologia, Sociologia, Psicologia",
      "chapter": 4,
      "examples": ["Nora (Casa de Bonecas): evolução psicológica"]
    },
    // ... mais 8-13 conceitos
  ],
  "concept_graph": {
    "Premise": ["Character", "Conflict", "Dialogue"],
    "Character": ["Orchestration", "Growth"],
    "Conflict": ["Premise", "Escalation", "Climax"]
  },
  "vocabulary": {
    "Premise": "Uma tese demonstrada através da ação",
    "Orchestration": "Contraste entre personagens para revelar premise",
    "Unity of Opposites": "Conflito entre forças que gera drama"
  },
  "argument_structure": {
    "type": "dedutivo",
    "flow": "Premise → Character → Conflict → Dialogue → Resolution",
    "key_chapters": [1, 4, 6, 8]
  }
}
```

---

#### ETAPA 2: Geração de Prompt Personalizado

**Input**:
- Análise completa do livro (JSON acima)
- Template base de análise

**Processo** (via LLM):
```python
prompt_generation = f"""
Você receberá:
1. Análise completa do livro de {autor}
2. Template base de análise de roteiro

SUA MISSÃO:
Criar um PROMPT ÚNICO para análise de roteiros usando EXCLUSIVAMENTE
a metodologia de {autor} conforme mapeada na análise do livro.

REQUISITOS:
1. Use os 10-15 conceitos principais identificados
2. Mantenha o VOCABULÁRIO ÚNICO do autor
3. Siga a ESTRUTURA ARGUMENTATIVA do autor
4. Faça CONEXÕES entre conceitos (conforme grafo)
5. Use EXEMPLOS CONCRETOS do livro
6. Adapte a ESTRUTURA do prompt à metodologia

NÃO:
- Não use conceitos genéricos
- Não misture metodologias de outros autores
- Não invente conceitos não presentes no livro

Análise do livro:
{book_analysis_json}

Template base:
{base_template}
"""
```

**Output Esperado** (Exemplo EGRI - FASE 4):
```
# ANÁLISE DE ROTEIRO - METODOLOGIA EGRI

## OBJETIVO
Analisar roteiro através da metodologia completa de Lajos Egri
conforme estabelecida em "The Art of Dramatic Writing".

## ESTRUTURA DE ANÁLISE (Adaptada de Egri, Cap. 1-12)

### 1. IDENTIFICAÇÃO DA PREMISE (Egri, Cap. 1: Premise)

A premise é a TESE que o roteiro demonstra através da AÇÃO.
Egri: "Uma premise deve ser provável, não apenas possível."

TAREFA:
- Identifique a premise em formato: "[Qualidade/Ação] leva a [Resultado]"
  Exemplo (Romeu e Julieta): "Grande amor desafia obstáculos leva a tragédia"

- Analise se a premise é PROVÁVEL (fundamentada em natureza humana)
- Verifique se TODA A AÇÃO deriva da premise

PROBLEMAS COMUNS:
- Premise vaga ou múltipla
- Premise apenas possível, não provável
- Ações não derivam da premise

---

### 2. ORCHESTRATION (Egri, Cap. 4: Orchestration)

Egri define orchestration como "o contraste entre personagens que
revela a premise através de conflito".

TAREFA:
- Mapear a ORCHESTRA de personagens
- Cada personagem deve representar um POLO da premise
- Analisar se há "Unity of Opposites" (força e contra-força)

PERSONAGENS EM ORCHESTRATION:
- Protagonista: Encarna qual polo?
- Antagonista: Encarna polo oposto?
- Secundários: Que variações da premise representam?

VERIFICAR (Egri, Cap. 4):
- Cada personagem tem 3 dimensões? (Fisiologia, Sociologia, Psicologia)
- Há contraste suficiente? (Egri: "sem contraste, não há orchestration")
- Personagens crescem? (Egri: "personagem estático é personagem morto")

PROBLEMAS COMUNS:
- Personagens unidimensionais
- Falta de contraste/orchestration
- Crescimento não derivado da premise

---

### 3. CONFLICT & ESCALATION (Egri, Cap. 6: Conflict)

Egri: "Não há drama sem conflito. Conflito nasce da premise."

TAREFA:
- Mapear TODOS os níveis de conflito:
  * Conflito Externo (forças físicas/sociais)
  * Conflito Interno (psicológico)
  * Conflito Interpessoal (entre personagens da orchestra)

- Verificar ESCALATION (Egri: "conflito deve intensificar até climax")
- Analisar se conflito deriva da PREMISE

VERIFICAR ESCALATION POINT (Egri, Cap. 7):
- Crise → Clímax → Resolução
- Cada turning point deriva da premise?
- Há "Unity of Opposites" em cada confronto?

PROBLEMAS COMUNS:
- Conflito não deriva da premise
- Falta de escalation (conflito constante)
- Resolução não prova a premise

---

### 4. DIALOGUE AS PROOF OF PREMISE (Egri, Cap. 10: Dialogue)

Egri: "Diálogo deve provar a premise através de ação verbal."

TAREFA:
- Analisar se diálogo PROVA a premise (não apenas declara)
- Verificar se diálogo revela 3 dimensões do personagem
- Confirmar que diálogo tem SUBTEXTO (Egri: "people seldom say what they mean")

PROBLEMAS COMUNS (Egri, Cap. 10):
- "On-the-nose": personagem diz exatamente o que sente
  → Solução: Usar subtexto, ação reveladora

- Diálogo não deriva da premise
  → Solução: Alinhar fala com polo do personagem na orchestra

- Diálogo expositivo (dump de informação)
  → Solução: Entregar info através de conflito

---

## OUTPUT REQUIREMENTS (FASE 4)

Para CADA problema identificado, fornecer:

1. **IDENTIFICAÇÃO** (formato Egri):
   ```
   PROBLEMA: [Nome] - Violação de [Conceito Egri]
   CENA: [Número] (página [X])
   EVIDÊNCIA: [Quote do roteiro]
   ```

2. **ANÁLISE TEÓRICA** (vocabulário Egri):
   ```
   ANÁLISE:
   Egri em [Capítulo], [Conceito específico] estabelece que:
   "[Quote do livro se possível]"

   No roteiro, isso se manifesta como:
   [Explicação específica usando conceitos de Egri]

   Conexão com PREMISE:
   [Como isso afeta a demonstração da premise]
   ```

3. **SOLUÇÃO CONCRETA** (metodologia Egri):
   ```
   SOLUÇÃO:
   Aplicando [Conceito Egri específico]:

   ANTES: [Diálogo/cena atual]
   DEPOIS: [Reescrita aplicando conceito]

   JUSTIFICATIVA (Egri):
   [Por que essa solução alinha com metodologia]
   [Como fortalece a premise]
   [Como melhora orchestration]
   ```

---

## VOCABULARY ÚNICO DE EGRI (Use esses termos)

- **Premise**: Tese demonstrada através da ação
- **Orchestration**: Contraste entre personagens revelando premise
- **Unity of Opposites**: Forças opostas gerando conflito
- **Three-Dimensional Character**: Fisiologia + Sociologia + Psicologia
- **Growth/Transition**: Mudança de polo na premise
- **Escalation Point**: Momento onde conflito intensifica
- **Static Character**: Personagem sem crescimento (erro)
- **Jumping Character**: Mudança não motivada (erro)

---

## STRUCTURE (Follow Egri's Argument Flow)

1. PREMISE (fundação)
   ↓
2. CHARACTER (quem prova a premise?)
   ↓
3. ORCHESTRATION (contraste entre personagens)
   ↓
4. CONFLICT (unity of opposites)
   ↓
5. ESCALATION (intensificação até climax)
   ↓
6. RESOLUTION (premise demonstrada)

Cada análise deve seguir ESSA sequência lógica (Egri, estrutura do livro).

---

## EXEMPLOS DO PRÓPRIO EGRI (Use como referência)

### Exemplo 1: Ibsen, "A Doll's House" (Egri, Cap. 2)
- Premise: "Egoísmo leva à perda de amor"
- Orchestration: Nora (crescimento) vs Torvald (estático)
- Growth: Nora evolui de submissa para independente

### Exemplo 2: Shakespeare, "Romeo and Juliet" (Egri, Cap. 1)
- Premise: "Grande amor desafia obstáculos leva a tragédia"
- Unity of Opposites: Amor vs Ódio familiar
- Escalation: Encontro → Casamento → Morte

### Exemplo 3: Shakespeare, "Othello" (Egri, Cap. 6)
- Premise: "Ciúme leva à destruição"
- Character: Othello (three-dimensional: warrior, outsider, lover)
- Conflict: Interno (insegurança) + Externo (Iago)

---

## CRITICAL REMINDERS

1. **Sempre derivar da PREMISE**: Toda análise começa e termina na premise
2. **Usar vocabulário Egri**: Não inventar termos, usar os do livro
3. **Seguir estrutura lógica**: Premise → Character → Conflict → Resolution
4. **Citar capítulos específicos**: "Egri, Cap. 4: Orchestration"
5. **Exemplos concretos**: Use casos do livro (Ibsen, Shakespeare, etc)
6. **Three-dimensional analysis**: Sempre analisar Fisiologia, Sociologia, Psicologia
7. **Orchestration é chave**: Contraste entre personagens revela premise

---

BEGIN ANALYSIS FOLLOWING EGRI'S COMPLETE METHODOLOGY.
```

---

## 💡 VANTAGENS DA ABORDAGEM FASE 4

### Comparação Direta: FASE 2 vs FASE 4

| Aspecto | FASE 2 (Atual) | FASE 4 (Proposta) |
|---------|----------------|-------------------|
| **Base** | Conhecimento geral do autor | Análise completa do livro (~128k tokens) |
| **Profundidade** | Conceitos principais (3-5) | Conceitos completos (10-15) + Conexões |
| **Vocabulário** | Mistura de termos genéricos | Vocabulário único do autor |
| **Estrutura** | Template genérico adaptado | Estrutura única por metodologia |
| **Exemplos** | Inventados | Casos do próprio livro |
| **Conexões** | Superficiais | Grafo completo de inter-relações |
| **Tempo Criação** | Manual (~2h por autor) | LLM (~30 min por autor) |
| **Resultado Esperado** | 16.3/10 real | **18.0-20.0/10** ✨ |

---

## 🎯 RESULTADOS ESPERADOS

### Impacto Quantitativo

**FASE 3 (Atual)**:
- Score Real Médio: 16.3/10
- Top 5 autores: 18.0/10
- Autores médios: 15.5-16.0/10

**FASE 4 (Esperado)**:
- Score Real Médio: **17.5-18.0/10** (+1.5 pontos)
- Top autores: **19.0-20.0/10** (excelência absoluta)
- Autores médios: **17.0-18.0/10**

### Impacto Qualitativo

**Melhorias Esperadas**:
1. **Análises mais profundas**: Uso de 10-15 conceitos vs 3-5 atuais
2. **Conexões teóricas**: Explicações de COMO conceitos se relacionam
3. **Vocabulário preciso**: Termos exatos do autor, não aproximações
4. **Exemplos autênticos**: Casos do livro, não inventados
5. **Estrutura coerente**: Seguindo lógica específica do autor

---

## 🛠️ IMPLEMENTAÇÃO

### FASE 4A: Prova de Conceito (1 autor)

**Objetivo**: Validar metodologia com 1 autor antes de escalar

**Etapas**:
1. Escolher 1 autor (sugestão: EGRI - já tem score alto)
2. Implementar Etapa 1 (análise completa do livro)
3. Implementar Etapa 2 (geração de prompt personalizado)
4. Testar com roteiro "Te Encontro em Mim"
5. Comparar resultado FASE 3 vs FASE 4 para EGRI
6. Validar se score melhorou

**Critérios de Sucesso**:
- ✅ Score EGRI FASE 4 > Score EGRI FASE 3
- ✅ Análise usa vocabulário único de Egri
- ✅ Análise segue estrutura do livro
- ✅ Prompt gerado automaticamente (não manual)

---

### FASE 4B: Escalar para 13 Autores

**Etapas** (após validação FASE 4A):
1. Repetir processo para todos os 13 autores
2. Gerar 13 prompts verdadeiramente personalizados
3. Substituir `engine/prompts/author_prompts.py`
4. Re-testar com roteiro validation
5. Comparar médias FASE 3 vs FASE 4

**Tempo Estimado**:
- Análise de livro (Etapa 1): ~30 min/autor via LLM
- Geração de prompt (Etapa 2): ~30 min/autor via LLM
- **Total**: ~13 horas para 13 autores
- **Ganho**: Automático via LLM (vs ~26h manual)

---

## 💰 CUSTO-BENEFÍCIO

### Custos

**Tempo Desenvolvimento**:
- FASE 4A (prova conceito): ~4-6 horas
- FASE 4B (escalar 13 autores): ~13 horas
- **Total**: ~20 horas desenvolvimento

**Custos Computacionais**:
- Análise de livro: ~128k tokens input + ~10k output = ~$0.50/autor
- Geração de prompt: ~10k tokens input + ~5k output = ~$0.10/autor
- **Total**: ~$0.60/autor × 13 = **~$8** (custo Ollama = $0)

### Benefícios

**Ganho em Qualidade**:
- Score médio: 16.3 → 18.0 (+1.7 pontos, +10%)
- Consistência: Todos autores 17.0+ (vs atual 15.5-18.0)
- **Resultado**: Sistema de excelência absoluta

**Ganho em Tempo Futuro**:
- Manutenção: Prompts auto-gerados (vs manual)
- Novos autores: ~1h/autor (vs ~2h manual)
- **ROI**: Positivo após 2-3 novos autores

---

## 🔮 ROADMAP

### Curto Prazo (Próximas 2 Semanas)

- [ ] **Semana 1**: Implementar FASE 4A (prova conceito com EGRI)
  - [ ] Dia 1-2: Implementar Etapa 1 (análise livro)
  - [ ] Dia 3-4: Implementar Etapa 2 (geração prompt)
  - [ ] Dia 5-6: Testar e validar resultados
  - [ ] Dia 7: Documentar findings e decidir go/no-go

- [ ] **Semana 2**: Se FASE 4A bem-sucedida, escalar (FASE 4B)
  - [ ] Dia 8-10: Análise completa dos 13 livros
  - [ ] Dia 11-12: Geração dos 13 prompts personalizados
  - [ ] Dia 13: Integração em `author_prompts.py`
  - [ ] Dia 14: Teste completo com 13 autores

### Médio Prazo (1 Mês)

- [ ] Validação com múltiplos roteiros (não apenas "Te Encontro em Mim")
- [ ] Ajustes finos baseados em feedback
- [ ] Documentação completa do sistema FASE 4
- [ ] Comparação estatística FASE 3 vs FASE 4

### Longo Prazo (3 Meses)

- [ ] Adicionar novos autores (ex: John Yorke, Christopher Booker)
- [ ] Sistema de auto-atualização (re-análise quando livro é atualizado)
- [ ] Métricas de impacto (antes/depois em produção real)

---

## 🚦 DECISÃO: GO / NO-GO

### Critérios para Aprovar FASE 4

**GO** se:
- ✅ FASE 4A (prova conceito) mostra melhoria clara vs FASE 3
- ✅ Score EGRI FASE 4 >= 18.0/10 (vs 15.5/10 atual)
- ✅ Análise usa vocabulário/estrutura únicos de Egri
- ✅ Custo-benefício positivo (ROI claro)

**NO-GO** se:
- ❌ FASE 4A não mostra melhoria significativa
- ❌ Score FASE 4 <= Score FASE 3
- ❌ Complexidade implementação > benefício
- ❌ Custos computacionais inviáveis

---

## 📋 CHECKLIST DE APROVAÇÃO

### Antes de Iniciar FASE 4A

- [ ] Ler esta proposta completa
- [ ] Entender diferença FASE 2 vs FASE 4
- [ ] Validar que FASE 3 está estável (bug consolidador corrigido)
- [ ] Confirmar que vale a pena investir ~20h desenvolvimento
- [ ] Definir critérios claros de sucesso

### Durante FASE 4A (Prova Conceito)

- [ ] Implementar Etapa 1 (análise livro EGRI)
- [ ] Validar output da análise (10-15 conceitos + grafo)
- [ ] Implementar Etapa 2 (geração prompt EGRI)
- [ ] Validar prompt gerado (estrutura + vocabulário únicos)
- [ ] Testar com roteiro "Te Encontro em Mim"
- [ ] Comparar score FASE 3 vs FASE 4 (EGRI)
- [ ] Decidir: GO para FASE 4B ou NO-GO?

### Se GO para FASE 4B (Escalar)

- [ ] Análise completa dos 12 livros restantes
- [ ] Geração dos 12 prompts restantes
- [ ] Integração em `author_prompts.py`
- [ ] Teste com todos os 13 autores
- [ ] Validação de scores (média >= 17.5/10?)
- [ ] Documentação final FASE 4
- [ ] Deploy em produção

---

## 💬 PERGUNTAS & RESPOSTAS

### Q: Por que FASE 4 se FASE 3 já tem scores 15.5-18.0/10?

**A**: Porque queremos **excelência absoluta** (18.0-20.0/10), não apenas "bom". FASE 4 leva o sistema ao limite teórico de qualidade.

### Q: Qual a diferença real entre FASE 2 e FASE 4?

**A**: FASE 2 usa "conhecimento geral" sobre cada autor. FASE 4 usa "análise completa do livro" gerando prompts únicos por metodologia. É como a diferença entre "conhecer" um autor vs "estudar profundamente" o autor.

### Q: Vale a pena o investimento de ~20h?

**A**: Se o objetivo é ter o **melhor sistema de análise de roteiros do mundo**, sim. Se o objetivo é "bom o suficiente", FASE 3 já atende.

### Q: E se FASE 4A falhar (não melhorar scores)?

**A**: Investimos apenas ~6h na prova de conceito. Se falhar, abortamos e ficamos com FASE 3 (que já é excelente). Risco controlado.

### Q: Posso adicionar novos autores facilmente em FASE 4?

**A**: Sim! O processo é automatizado via LLM. Basta ter o livro de teoria em texto, rodar Etapa 1 + Etapa 2, e pronto (~1h por autor).

---

## 📊 RESUMO EXECUTIVO

**Situação Atual (FASE 3)**:
- Sistema excelente: scores reais 15.5-18.0/10
- Prompts "personalizados" FASE 2 são na verdade "melhorados genéricos"
- Limitação: Não usam análise profunda dos livros

**Proposta (FASE 4)**:
- Analisar cada livro completamente (~128k tokens)
- Gerar prompts verdadeiramente únicos por metodologia
- Elevar scores para 18.0-20.0/10 (excelência absoluta)

**Investimento**:
- Tempo: ~20h desenvolvimento
- Custo: ~$8 LLM (ou $0 com Ollama local)
- Risco: Baixo (prova conceito com 1 autor primeiro)

**Retorno Esperado**:
- Scores: 16.3 → 18.0 (+10%)
- Qualidade: Análises mais profundas, precisas, autênticas
- Futuro: Sistema escalável e de excelência mundial

**Recomendação**: **GO** para FASE 4A (prova conceito)

---

**Proposta Criada por**: Claude (Anthropic)
**Data**: 10 de Outubro 2025
**Versão**: 1.0
**Status**: 📝 Aguardando Aprovação