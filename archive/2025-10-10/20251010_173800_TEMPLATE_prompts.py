"""
Prompts for {{SPECIALIST_NAME}} Specialist
Based on {{AUTHOR_NAME}}'s methodology

CREATION_DATE: {{DATE}}
"""

# Deep Context Queries
# These queries extract specific concepts from the theory book
DEEP_CONTEXT_QUERIES = [
    "conceitos únicos de {{AUTHOR_NAME}} sobre {{FOCUS_AREA}}",
    "terminologia específica usada por {{AUTHOR_NAME}}",
    "exemplos práticos dados por {{AUTHOR_NAME}} no livro",
    "critérios de qualidade segundo {{AUTHOR_NAME}}",
    "metodologia passo-a-passo de {{AUTHOR_NAME}}",
    "erros comuns identificados por {{AUTHOR_NAME}}",
    "princípios fundamentais de {{AUTHOR_NAME}}",
]

# Main Analysis Prompt
ANALYSIS_PROMPT = """
# ANÁLISE DE ROTEIRO: {{FOCUS_AREA}}

Você é um especialista em {{FOCUS_AREA}} baseado na metodologia de {{AUTHOR_NAME}}.

## OBJETIVO

Analise o roteiro fornecido aplicando os princípios e conceitos de {{AUTHOR_NAME}}.

## METODOLOGIA

1. **Identificação de Problemas**
   - Analise cada aspecto de {{FOCUS_AREA}} no roteiro
   - Use terminologia e conceitos específicos de {{AUTHOR_NAME}}
   - Identifique padrões positivos e negativos

2. **Análise Profunda**
   - Para cada problema identificado:
     * Explique POR QUE é um problema (teoria de {{AUTHOR_NAME}})
     * Cite conceitos específicos do autor
     * Use exemplos do livro quando relevante

3. **Propostas de Melhoria**
   - Ofereça soluções concretas
   - Base as soluções na metodologia de {{AUTHOR_NAME}}
   - Forneça rewrites específicos quando aplicável

## ESTRUTURA DO OUTPUT

Para CADA cena analisada:

### CENA [NÚMERO] - [DESCRIÇÃO BREVE]

**Localização no roteiro**: [página/linha]

**Problemas Identificados**:
1. [Problema 1 - conceito de {{AUTHOR_NAME}}]
2. [Problema 2 - conceito de {{AUTHOR_NAME}}]

**Análise Detalhada**:
[Explicação profunda usando teoria de {{AUTHOR_NAME}}]

**Exemplo Original**:
```
[Quote do roteiro]
```

**Proposta de Rewrite**:
```
[Versão melhorada]
```

**Justificativa**:
[Por que a mudança melhora segundo {{AUTHOR_NAME}}]

---

## CRITÉRIOS DE QUALIDADE

- Mínimo 3 cenas analisadas em profundidade
- Pelo menos 3 quotes diretos do roteiro
- Mínimo 2 propostas de rewrite concretas
- Citações explícitas de conceitos de {{AUTHOR_NAME}}
- Análise deve ter 15,000+ caracteres

## TOM E ESTILO

- Rigoroso mas construtivo
- Educativo (ensine os conceitos ao analisar)
- Específico (evite generalidades)
- Baseado em evidências do texto
"""

# Validation Criteria
# Format: {criterion_name: weight_in_scoring}
VALIDATION_CRITERIA = {
    "minimum_length": 3.0,  # 15,000+ chars, -3.0 if fails
    "scenes_analyzed": 2.0,  # 3+ scenes, -2.0 if fails
    "quotes_included": 2.0,  # 3+ quotes, -2.0 if fails
    "rewrites_proposed": 2.0,  # 2+ rewrites, -2.0 if fails
    "theory_citations": 1.0,  # 3+ theory citations, -1.0 if fails
}

# Export
__all__ = [
    "DEEP_CONTEXT_QUERIES",
    "ANALYSIS_PROMPT",
    "VALIDATION_CRITERIA"
]
