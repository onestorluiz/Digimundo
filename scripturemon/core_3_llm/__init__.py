"""
🤖 CORE 3: LLM Theory Enrichment

Enriquecimento com teoria McKee via LLM otimizado.

Componentes:
- prompt_builder.py    → Constrói prompt de 260 linhas
- theory_loader.py     → Carrega livro McKee completo (77k words)
- llm_caller.py        → Subprocess Ollama
- response_parser.py   → Parse da resposta LLM

Prompt Structure:
1. Few-shot examples (análise BOA vs MÁ)
2. Task instructions (12-14 parágrafos)
3. Primacy/Recency mitigation
4. Deep context (livro completo)
5. Screenplay text
6. Core 1 metrics

Model: scripturemon-optimized (Ollama)
Context: 128k tokens (Deep Dive mode)
Output: 2500-4000 tokens de análise profunda
Tempo: ~5-7 minutos
"""

__core__ = "CORE_3_LLM_THEORY_ENRICHMENT"

# TODO: Modularizar componentes do DualCoreWrapper
# Para permitir uso independente do Core 3

__all__ = []
