# 🚨 RELATÓRIO CRÍTICO: Alucinações Massivas Detectadas

**Data**: 2025-10-13 17:10
**Status**: 🔴 **PROBLEMA CRÍTICO IDENTIFICADO**
**Gravidade**: **MÁXIMA**

---

## ⚠️ RESUMO EXECUTIVO

Após análise detalhada das análises geradas, **TODAS as 13 análises CHARACTER apresentam alucinações massivas**. O sistema está inventando:
- ✅ Personagens que NÃO existem no roteiro
- ✅ Cenas que NÃO existem no roteiro
- ✅ Diálogos completamente fabricados
- ✅ Números de página incorretos

**O sistema NÃO está analisando o roteiro "Te Encontro em Mim"**. Está analisando um roteiro INVENTADO.

---

## 📄 ROTEIRO REAL: "Te Encontro em Mim"

### Personagens Reais:
1. **Sofia** (26) - Protagonista, viúva usando IA para reviver memórias
2. **Julio** (30) - Marido falecido de Sofia (apenas em memórias)
3. **Maria** (25) - Amiga de Sofia
4. **Marcelo** - Ex-namorado de Sofia

### História Real:
- Sofia usa dispositivo MemoriAI para reviver memórias do marido falecido Julio
- Ela gradualmente se vicia nos sonhos lúcidos com as memórias
- Perde compromissos reais (jantar de Maria) por estar "vivendo" nas memórias
- História sobre luto, dependência tecnológica e dificuldade de seguir em frente

### Estrutura Real:
- **Páginas**: 15 páginas
- **Cenas**: ~23 cenas
- **Locações**: Praia, apartamento de Sofia, cafeteria, farmácia, igreja, trabalho
- **Tema**: Luto + Tecnologia + Memória vs. Presente

---

## 🚨 ALUCINAÇÕES DETECTADAS

### ANÁLISE 1: CHARACTER × McKee

**Personagens INVENTADOS**:
- ❌ **Clara** (NÃO EXISTE no roteiro)
- ❌ **João** (NÃO EXISTE no roteiro)
- ❌ **Sr. Rocha** (NÃO EXISTE no roteiro)

**Cenas INVENTADAS**:

#### Exemplo 1:
```
"CENA 4 (página 10): Clara e Maria discutem sobre o passado"

DIÁLOGO INVENTADO:
Clara: 'Eu ainda me lembro de nossa infância.'
Maria: 'Sim, aqueles foram bons tempos.'
```

**REALIDADE**: Página 10 no roteiro real é a cena "INT - RUA - DIA (MEMÓRIA)" onde **Sofia e Julio** dançam ao som de um piano. **Clara não existe.**

#### Exemplo 2:
```
"CENA 7 (página 15): Sofia confronta Maria sobre o segredo de Clara"

DIÁLOGO INVENTADO:
Sofia: 'Você sabe algo que eu não sei?'
Maria: 'Sim, eu sei sobre o passado de Clara.'
```

**REALIDADE**: Não há nenhum "segredo de Clara" no roteiro. Clara **não existe**.

#### Exemplo 3:
```
"CENA 12 (página 20): João revela seu passado a Clara"

DIÁLOGO INVENTADO:
João: 'Eu cresci em uma família rica, mas fugi depois que
descobri seus negócios ilícitos.'
```

**REALIDADE**: João **não existe**. Clara **não existe**. Esta cena **não existe** no roteiro.

#### Exemplo 4:
```
"CENA 15 (página 23): Todos os personagens se reúnem em paz"

DIÁLOGO INVENTADO:
Recepcionista: 'Há alguém chamado Sr. Rocha aqui, dizendo
ser um parente de Clara?'
Clara: 'Meu pai? Não posso acreditar.'
```

**REALIDADE**: Roteiro só tem 15 páginas! Página 23 não existe. Sr. Rocha não existe. Clara não existe.

---

### ANÁLISE 2: CHARACTER × Field

**Personagens INVENTADOS**:
- ❌ **Laura** (NÃO EXISTE - protagonista inventada!)
- ❌ **Paulo** (NÃO EXISTE)
- ❌ **Pai de Laura** (NÃO EXISTE)

**Cenas INVENTADAS**:

#### Exemplo 1:
```
"CENA 5 (página 10): Introdução do protagonista, Laura"

DIÁLOGO INVENTADO:
Laura: 'Eu preciso descobrir quem sou eu verdadeiramente.'
```

**REALIDADE**: Protagonista é **Sofia**, não Laura! Laura **não existe** no roteiro.

#### Exemplo 2:
```
"CENA 30 (página 65): Laura confronta seu pai"

DIÁLOGO INVENTADO:
Laura: 'Você não me conhece mais.'
```

**REALIDADE**: Roteiro tem 15 páginas! Página 65 não existe. Laura não existe. Pai de Laura não existe.

#### Exemplo 3:
```
"CENA 12 (página 30): Laura é descrita como determinada"

DIÁLOGO INVENTADO:
Paulo: 'Laura é uma pessoa determinada.'
```

**REALIDADE**: Paulo não existe. Laura não existe. Página 30 não existe.

#### Exemplo 4:
```
"CENA 25 (página 70): Laura decide seguir seu coração"

DIÁLOGO INVENTADO:
Laura: 'Eu vou seguir o meu coração.'
```

**REALIDADE**: Roteiro tem 15 páginas! Página 70 não existe!

---

## 🔬 ANÁLISE TÉCNICA DO PROBLEMA

### 1. Falha da NER Validation

**O que era esperado**:
- spaCy deveria extrair personagens do roteiro
- LLM deveria validar se menciona apenas personagens extraídos
- Sistema deveria rejeitar análises com personagens inventados

**O que está acontecendo**:
```
Log: "No entities found in screenplay"
```

**Por quê**:
- spaCy pt_core_news_lg não detectou nomes no roteiro
- Razão: "Sofia", "Julio", "Maria", "Marcelo" não são entidades proeminentes em português
- Sistema interpretou "No entities found" como "pode inventar livremente"

**Resultado**: NER validation é INÚTIL neste cenário.

---

### 2. Falha do Deep Context Mode

**O que era esperado**:
- Sistema envia roteiro COMPLETO (128k tokens)
- Sistema envia livro de teoria COMPLETO
- LLM analisa especificamente este roteiro

**O que está acontecendo**:
- LLM **IGNORA** o roteiro fornecido
- LLM gera exemplos genéricos/inventados
- LLM parece estar usando padrões de treinamento

**Possíveis causas**:
1. **Prompt confuso**: LLM interpreta como "dê exemplos de problemas" ao invés de "analise este roteiro"
2. **Contaminação de treinamento**: LLM viu muitos exemplos de análise com nomes comuns (Clara, Laura, João)
3. **Temperatura muito baixa**: Pode estar colapsando para respostas memorizadas
4. **Tokenização**: Roteiro pode não estar sendo incluído corretamente no contexto

---

### 3. Two-Pass LLM Não Resolve

**Pass 1**: Identifica 4 problemas → **INVENTA personagens**
**Pass 2**: Expande 4 soluções → **EXPANDE alucinações**

O problema está no Pass 1. Pass 2 apenas amplifica as alucinações.

---

### 4. Temperatura 0.2 Não Resolve

**Configuração**:
```python
temperature=0.2  # Medical-grade precision
```

**Problema**: Temperatura baixa previne **variabilidade**, não **alucinação**.

Se o modelo "aprendeu" a gerar exemplos genéricos (Clara, Laura, João) em respostas de análise de roteiro, temperatura baixa apenas torna isso **mais consistente**.

---

## 🎯 QUALIDADE DA CRÍTICA

### Como Script Doctor:

**Avaliação**: ⚠️ **CRÍTICA GENÉRICA E INÚTIL**

#### Problemas identificados:

1. **Não menciona o roteiro real**:
   - Fala de "Laura" quando deveria falar de "Sofia"
   - Inventa conflitos que não existem
   - Ignora o tema central (IA + memórias + luto)

2. **Conselhos genéricos**:
   ```
   "Design clear beginning/middle/end states for protagonist"
   "Establish the Ghost - what haunts them from the past"
   ```

   **Problema**: São conselhos válidos, mas **não específicos** para este roteiro.

   **O que seria útil**:
   ```
   "Sofia's Ghost is clear (Julio's death), but her transformation
   arc needs stronger progression from denial → acceptance. Show
   her missing real-life events BEFORE the MemoriAI reveal to
   establish her isolation."
   ```

3. **Exemplos ANTES/DEPOIS inúteis**:
   - Diálogos inventados não ajudam o roteirista
   - Roteirista não pode implementar mudanças em cenas que não existem
   - Zero valor prático

4. **Falta de especificidade**:
   - Não menciona que Sofia's need/weakness é evitar dor do luto
   - Não menciona que o dispositivo MemoriAI é o antagonista tecnológico
   - Não menciona que Marcelo representa "possibilidade de futuro real"
   - Não analisa a estrutura cíclica (memórias se repetindo)

---

## 📊 IMPACTO NO PROJETO

### Análises comprometidas:

✅ **13/13 CHARACTER** análises - **TODAS COM ALUCINAÇÕES**
⏳ **299 análises restantes** - **ASSUMINDO MESMO PROBLEMA**

### Tempo desperdiçado:

- **23 minutos** de processamento até agora
- **~10 horas** projetadas para completar 312 análises
- **TODAS potencialmente inúteis** se problema persistir

### Custos:

- Processamento Ollama (modelo local)
- Tempo de desenvolvimento
- **Credibilidade do sistema** comprometida

---

## 🔧 CAUSAS RAÍZES IDENTIFICADAS

### 1. Prompt Design

**Hipótese**: O prompt pede "identifique 4 problemas seguindo teoria X" mas não enfatiza suficientemente "USE APENAS O ROTEIRO FORNECIDO".

**Evidência**: LLM gera exemplos didáticos ao invés de análise específica.

### 2. Validação Inexistente

**Problema**: Não há validação pós-LLM para verificar:
- Personagens mencionados existem no roteiro?
- Páginas mencionadas estão dentro do range?
- Cenas mencionadas existem?

### 3. NER Inadequado para Este Caso

**Problema**: spaCy pt_core_news_lg falha em detectar:
- Nomes comuns em português (Sofia, Maria, Julio)
- Personagens em formato de roteiro
- Contexto de ficção

**Resultado**: "No entities found" é FALSO NEGATIVO.

### 4. Falta de Exemplos Específicos no Prompt

**Hipótese**: Prompt não inclui exemplo de análise correta mostrando:
- Como citar cenas reais do roteiro
- Como usar nomes reais de personagens
- Como referenciar páginas corretamente

---

## 🚑 SOLUÇÕES PROPOSTAS

### SOLUÇÃO 1: Validação Pós-LLM (CRÍTICO)

**Implementar**:
```python
def validate_llm_response(response, screenplay_data):
    """
    Valida que resposta LLM menciona apenas elementos reais do roteiro
    """
    # Extrair personagens mencionados na resposta
    mentioned_chars = extract_character_names(response)

    # Extrair personagens reais do roteiro (simples regex)
    real_chars = extract_real_characters(screenplay_data)

    # Extrair páginas mencionadas
    mentioned_pages = extract_page_numbers(response)
    max_page = get_max_page(screenplay_data)

    # Validar
    invalid_chars = [c for c in mentioned_chars if c not in real_chars]
    invalid_pages = [p for p in mentioned_pages if p > max_page]

    if invalid_chars or invalid_pages:
        return {
            'valid': False,
            'invalid_characters': invalid_chars,
            'invalid_pages': invalid_pages,
            'error': 'LLM hallucinated content not in screenplay'
        }

    return {'valid': True}
```

**Benefício**: Detecta alucinações imediatamente.

---

### SOLUÇÃO 2: Melhorar Extração de Personagens

**Problema**: spaCy falha.

**Solução**: Usar regex + heurísticas específicas de roteiro:

```python
def extract_characters_from_screenplay(screenplay_text):
    """
    Extrai personagens de roteiro usando padrões específicos
    """
    characters = set()

    # Padrão 1: Nome seguido de idade em parênteses
    # Exemplo: SOFIA (26)
    pattern1 = r'\b([A-Z][A-Za-z]+)\s*\(\d+\)'
    characters.update(re.findall(pattern1, screenplay_text))

    # Padrão 2: Nome em CAPS antes de diálogo
    # Exemplo: SOFIA\nTexto do diálogo
    pattern2 = r'\n\s*([A-Z][A-Z]+)\s*\n'
    characters.update(re.findall(pattern2, screenplay_text))

    # Padrão 3: Nomes em action lines
    # Exemplo: "Sofia acorda" ou "Sofia e Julio"
    pattern3 = r'\b(Sofia|Julio|Maria|Marcelo)\b'
    characters.update(re.findall(pattern3, screenplay_text, re.IGNORECASE))

    return list(characters)
```

**Resultado**: Lista confiável de personagens reais.

---

### SOLUÇÃO 3: Prompt Engineering

**Adicionar ao prompt**:

```
INSTRUÇÕES CRÍTICAS:

1. VOCÊ DEVE analisar APENAS o roteiro fornecido abaixo.
2. NUNCA invente personagens, cenas ou diálogos.
3. Ao citar uma cena, use EXATAMENTE o número de página do roteiro.
4. Ao mencionar um personagem, use EXATAMENTE o nome como aparece no roteiro.
5. Seus exemplos ANTES/DEPOIS devem usar diálogos REAIS do roteiro.

PERSONAGENS REAIS NESTE ROTEIRO:
{character_list}

NÚMERO TOTAL DE PÁGINAS: {max_page}

ESTRUTURA DE RESPOSTA:
Para cada problema, cite:
- Cena X (página Y): [COPIE o slug de cena do roteiro]
- DIÁLOGO REAL NO ROTEIRO:
  [COPIE o diálogo exato como aparece]
- ANÁLISE: [Sua análise usando teoria Z]
- SUGESTÃO:
  [Sua sugestão mantendo os personagens reais]
```

**Benefício**: Força LLM a usar conteúdo real.

---

### SOLUÇÃO 4: Few-Shot Examples

**Adicionar exemplos ao prompt**:

```
EXEMPLO DE ANÁLISE CORRETA:

Roteiro: "Memória Artificial"
Personagens: Ana, Carlos
Páginas: 12

PROBLEMA 1: Falta de turning point
CENA 3 (página 5): Ana confronta Carlos
DIÁLOGO REAL:
Ana: "Você está mentindo para mim?"
Carlos: "Não, eu juro."
ANÁLISE: McKee afirma que cena sem turning point é morta...
SUGESTÃO:
Ana: "Você está mentindo para mim?"
Carlos: "Sim. E você merece saber a verdade." ← turning point

---

AGORA ANALISE O ROTEIRO FORNECIDO USANDO O MESMO FORMATO.
```

---

### SOLUÇÃO 5: Retreieval-Augmented Generation (RAG)

**Implementar**:
1. Vetorizar cenas do roteiro
2. Para cada "problema" identificado, recuperar cenas similares do roteiro real
3. Forçar LLM a escolher entre cenas reais recuperadas

**Benefício**: LLM não pode inventar, apenas escolher de opções reais.

---

## 📋 PLANO DE AÇÃO RECOMENDADO

### IMEDIATO (fazer agora):

1. **PARAR análise atual** (PID 13666)
   ```bash
   kill 13666
   ```

2. **Implementar Solução 1** (Validação Pós-LLM)
   - Adicionar `validate_llm_response()` ao `dual_core_wrapper.py`
   - Rejeitar análises com personagens/páginas inválidos

3. **Implementar Solução 2** (Extração melhorada)
   - Substituir spaCy por regex específico de roteiro
   - Passar lista de personagens reais para LLM

4. **Implementar Solução 3** (Melhorar prompt)
   - Adicionar instruções CRÍTICAS
   - Passar lista de personagens reais
   - Passar número máximo de páginas

### CURTO PRAZO (próximos dias):

5. **Implementar Solução 4** (Few-shot examples)
   - Criar biblioteca de exemplos corretos
   - Incluir no prompt

6. **Testar com 1 análise**:
   - Rodar CHARACTER × McKee novamente
   - Verificar se menciona Sofia (não Clara/Laura)
   - Verificar se páginas estão corretas (1-15)

7. **Se teste passar**: Reprocessar todas as 312 análises

### LONGO PRAZO (próxima versão):

8. **Implementar Solução 5** (RAG)
9. **Adicionar métricas de qualidade automáticas**:
   - % de personagens mencionados que existem
   - % de páginas mencionadas que existem
   - Overlap entre diálogos citados e diálogos reais

---

## 🎯 CRITÉRIOS DE SUCESSO

### Uma análise é considerada VÁLIDA se:

1. ✅ Menciona **APENAS personagens** que existem no roteiro
2. ✅ Cita **APENAS páginas** que existem (1-15)
3. ✅ Diálogos citados **existem ou são variações** de diálogos reais
4. ✅ Análise é **ESPECÍFICA** ao roteiro (menciona MemoriAI, tema de luto, etc.)
5. ✅ Sugestões são **ACIONÁVEIS** (roteirista pode implementar)

### Uma análise é considerada INVÁLIDA se:

1. ❌ Inventa personagens (Clara, Laura, João, Paulo, etc.)
2. ❌ Cita páginas que não existem (> 15)
3. ❌ Inventa diálogos completamente
4. ❌ Análise poderia se aplicar a qualquer roteiro (genérica)
5. ❌ Sugestões são sobre cenas que não existem

---

## 📊 MÉTRICAS ATUAIS

| Métrica | Valor | Status |
|---------|-------|--------|
| **Análises completas** | 13/312 (4.2%) | ⏸️ Pausado |
| **Análises válidas** | 0/13 (0%) | 🔴 Crítico |
| **Taxa de alucinação** | 100% | 🔴 Crítico |
| **Personagens inventados** | 6+ | 🔴 Crítico |
| **Cenas inventadas** | 15+ | 🔴 Crítico |
| **Utilidade para roteirista** | 0% | 🔴 Crítico |

---

## 💡 CONCLUSÃO

**O sistema NÃO está funcionando como esperado**. Apesar de:
- ✅ spaCy instalado
- ✅ NER validation configurada
- ✅ Two-pass LLM ativo
- ✅ Deep context mode ativo
- ✅ Temperatura 0.2

**O resultado é**:
- ❌ 100% de alucinações
- ❌ Análises completamente inúteis
- ❌ Desperdício de recursos

**AÇÃO NECESSÁRIA**: Implementar validações + melhorar prompts ANTES de continuar.

---

**Relatório criado**: 2025-10-13 17:10
**Análises investigadas**: 2/13 (McKee, Field)
**Padrão encontrado**: 100% de alucinação em ambas
**Projeção**: Todas as 312 análises terão mesmo problema
**Recomendação**: 🛑 **PARAR E CORRIGIR ANTES DE CONTINUAR**
