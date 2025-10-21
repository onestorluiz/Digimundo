# SCRIPTUREMON V4.1 - SISTEMA COMPLETO DE OTIMIZAÇÃO

**Data:** 2025-10-02
**Status:** ✅ Fases 1 e 2 Completas - Sistema Produção
**Qualidade:** EXCELENTE (6/6 critérios, +600% especificidade)

---

## ÍNDICE

1. [Visão Geral do Sistema](#visão-geral)
2. [Arquitetura Dual-Core](#arquitetura-dual-core)
3. [Sistema RAG (Theory Indexer)](#sistema-rag)
4. [Modelo Otimizado](#modelo-otimizado)
5. [Prompt Engineering Avançado](#prompt-engineering)
6. [Validação de 3 Camadas](#validação)
7. [Resultados e Benchmarks](#resultados)
8. [Guia de Uso](#guia-de-uso)

---

## VISÃO GERAL

### O Problema Original

**Graduação de 16 especialistas V4.1:**
- ✅ 100% aprovação técnica (all passed technical criteria)
- ❌ Apenas 37.5% qualidade real (6/16 com análises úteis)

**Sintomas identificados:**
- Análises genéricas: "o diálogo poderia ser melhorado"
- Zero citações específicas do roteiro
- Inventava elementos não existentes
- Não usava teoria McKee apesar de ter acesso

**Causa raiz descoberta:**
1. Modelo sem parâmetros otimizados (temperature ~0.8 para análise factual!)
2. Prompt sem estrutura (texto corrido, sem delimitadores)
3. Ausência de grounding explícito
4. Fenômeno "Lost in the Middle" (contexto 100k+ tokens)

### A Solução Implementada

**Sistema de 3 otimizações integradas:**

1. **MODELO OTIMIZADO** (scripturemon-optimized)
   - temperature 0.2 (factual vs criativo 0.8)
   - num_batch 64 (evita OOM em contextos longos)
   - System message com regras absolutas

2. **PROMPT ENGINEERING AVANÇADO**
   - XML delimiters (mitiga Lost in the Middle)
   - Few-shot examples (análise BOA vs MÁ)
   - Primacy/Recency (reforço de instruções)

3. **RAG OTIMIZADO**
   - Deep Dive mode (livro completo 77k palavras)
   - Mapeamento specialist→book (seleção precisa)
   - Chunking inteligente com highlights

**Resultado:** +600% especificidade, 6/6 critérios, análises profissionais

---

## ARQUITETURA DUAL-CORE

### Conceito Fundamental

**Separação de responsabilidades:**

```
PYTHON CORE (Rápido, Objetivo)
    ↓
    Métricas estruturais
    Scores quantitativos
    Detecção de problemas
    ↓
THEORY RETRIEVAL (Python, Zero tokens LLM)
    ↓
    Busca teoria relevante
    Mapeia problemas → conceitos McKee
    Seleciona livro apropriado
    ↓
LLM CORE (Lento, Qualitativo)
    ↓
    Recebe: Python metrics + Teoria + Roteiro
    Gera: Insights qualitativos profundos
    ↓
SYNTHESIS (Combina ambos)
    ↓
    Resultado final rico
```

### Implementação

**Arquivo:** `specialists/dual_core/base/dual_core_wrapper.py`

**Classe:** `DualCoreWrapper`

**Parâmetros de inicialização:**
```python
DualCoreWrapper(
    python_specialist: Any,          # Instância do especialista (ex: DrDialogue)
    llm_model: str = "scripturemon-optimized",  # Modelo otimizado
    llm_timeout: int = 600,          # 10 min para deep context
    fallback_to_python: bool = True, # Se LLM falha, retorna só Python
    use_theory: bool = True,         # Ativa busca de teoria
    deep_context: bool = True        # DEEP DIVE: livro completo
)
```

**Fluxo de execução detalhado:**

```python
def analyze(self, screenplay_text: str) -> Dict:
    # FASE 1: PYTHON CORE
    python_result = self.python_specialist.analyze(screenplay_text)
    # → Retorna: scores, regras violadas, recomendações

    # FASE 2: THEORY RETRIEVAL (Python)
    if self.use_theory:
        if self.deep_context:
            # Deep Dive: livro completo (~77k palavras)
            theory = self.theory_indexer.get_full_book_context(
                query=problemas_detectados,
                specialist_type=self.specialist_type  # Auto-detectado
            )
        else:
            # Shallow: apenas chunks relevantes (~2k palavras)
            theory = self.theory_indexer.search_for_problems(
                problems=python_result['recommendations']
            )

    # FASE 3: LLM ENRICHMENT
    prompt = self._build_llm_prompt(
        screenplay_text,
        python_result,
        theory_context
    )
    llm_insights = self._call_llm(prompt)

    # FASE 4: SYNTHESIS
    return {
        'python_analysis': python_result,
        'llm_insights': llm_insights,
        'synthesis': self._synthesize(python_result, llm_insights)
    }
```

### Auto-Detecção de Especialista

**Método:** `_detect_specialist_type()` (linhas 88-126)

**Funcionamento:**
```python
class_name = specialist.__class__.__name__.lower()

if 'dialogue' in class_name:
    return 'dialogue'  # → Livro: Dialogue McKee
elif 'psychology' in class_name:
    return 'psychemon'  # → Livro: Story McKee
elif 'opening' in class_name:
    return 'opening'  # → Livro: Save the Cat
# ... 16 tipos mapeados
```

**Benefício:** Cada especialista automaticamente recebe o livro de teoria mais relevante.

---

## SISTEMA RAG (THEORY INDEXER)

### Descoberta Importante

**O sistema JÁ TINHA RAG implementado!**

Arquivo: `core/theory_indexer.py`

Classe: `TheoryIndexer`

**Não precisamos adicionar RAG - apenas OTIMIZAMOS o existente.**

### Funcionamento do RAG

**1. Indexação (executada uma vez ao iniciar):**

```python
indexer = TheoryIndexer()
indexer.index_book(dialogue_book, chunk_size=500)

# Processo:
# 1. Carrega livro (77,627 palavras)
# 2. Divide em chunks de 500 palavras
# 3. Overlap de 50 palavras entre chunks
# 4. Cria 173 chunks com metadados
# 5. Cache para buscas futuras
```

**Estrutura de um chunk:**
```python
{
    'text': 'texto do chunk (500 palavras)',
    'book': 'Dialogue-_-The-Art-of-Verbal-Action',
    'chunk_id': 42,
    'start_word': 21000,
    'word_count': 500
}
```

**2. Busca (modo SHALLOW):**

```python
# Buscar teoria para um problema específico
results = indexer.search_for_problems(
    problems=['unnatural speech', 'lack of subtext'],
    limit_per_problem=2
)

# Processo:
# 1. Mapeia problema → termos de busca McKee
#    'unnatural speech' → ['conversational rhythm',
#                          'speech patterns',
#                          'how people really talk']
#
# 2. Busca cada termo nos chunks
#    Score: query completa = +10pts
#           termo individual = +2pts
#
# 3. Retorna top chunks por problema
#    Resultado: ~2k palavras de teoria relevante
```

**Mapeamento profundo (15 regras dialogue → teoria):**

Arquivo: `theory_indexer.py` linhas 186-353

Exemplo:
```python
# DIAL.R003 - Subtext Present
if 'subtext' in problem_lower:
    query_terms = [
        'subtext',
        'indirect dialogue',
        'what characters really mean',
        'hidden meaning',
        'unspoken desires',
        'dialogue beneath surface',
        'implication'
    ]
```

**3. Deep Dive Mode (OTIMIZAÇÃO FASE 2):**

```python
deep_result = indexer.get_full_book_context(
    query='dialogue problems',
    specialist_type='dialogue'  # NOVO: mapeamento direto
)

# Processo otimizado:
# 1. Verifica specialist_type → 'dialogue'
# 2. Mapeia para livro: 'Dialogue-_-The-Art-of-Verbal-Action'
# 3. Carrega livro COMPLETO (77,627 palavras)
# 4. Busca 5 highlights (chunks mais relevantes para query)
# 5. Retorna: livro completo + highlights marcados

# Resultado:
{
    'primary_book': {
        'name': 'Dialogue-_-The-Art-of-Verbal-Action',
        'full_text': '... 77k palavras ...',
        'word_count': 77627,
        'highlights': [chunk1, chunk2, chunk3, chunk4, chunk5]
    },
    'estimated_tokens': 100915,  # ~1.3 tokens/palavra
    'method': 'specialist_mapping'  # Indica mapeamento direto
}
```

### Mapeamento Specialist → Book

**Implementação:** `theory_indexer.py` linhas 482-526

**Tabela completa:**
```python
SPECIALIST_BOOK_MAP = {
    # Dialogue specialists
    'dialogue': 'Dialogue-_-The-Art-of-Verbal-Action',
    'subtext': 'Dialogue-_-The-Art-of-Verbal-Action',
    'submon': 'Dialogue-_-The-Art-of-Verbal-Action',

    # Story structure specialists
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
    'genre': 'save_the_cat'
}
```

**Benefícios do mapeamento:**
1. ✅ Seleção instantânea (não precisa buscar)
2. ✅ Livro sempre correto para o especialista
3. ✅ Elimina ambiguidade (busca pode escolher errado)
4. ✅ Escalável (fácil adicionar novos livros/specialists)

### Estatísticas do Sistema RAG

```python
indexer.get_stats()

# Retorna:
{
    'books_indexed': 1,  # Dialogue McKee
    'total_chunks': 173,
    'total_words': 77627,
    'cache_size': 42,  # Buscas em cache
    'books': ['Dialogue-_-The-Art-of-Verbal-Action']
}
```

**Cache de buscas:**
- Primeira busca: processa chunks
- Buscas subsequentes: retorna do cache
- Cache key: `{query}_{limit}_{book_filter}`

---

CONTINUA EM PARTE 2...
