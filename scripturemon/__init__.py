"""
🎬 SCRIPTUREMON TRIPLE-CORE ARCHITECTURE

Arquitetura de 3 cores para análise profissional de roteiros:

CORE 1 - Python Technical Analysis (core_1_specialists/)
    └─ 24 especialistas Dr* (DrDialogue, DrStructure, etc)
    └─ Análise técnica objetiva: métricas, scores, violations
    └─ Tempo: ~0.0s (instantâneo)

CORE 2 - Master Examples Finder (core_2_examples/)
    └─ Busca em 33 roteiros mestres
    └─ Encontra exemplos concretos de soluções
    └─ Tempo: ~0.0s (pré-indexado)

CORE 3 - LLM Theory Enrichment (core_3_llm/)
    └─ Model: scripturemon-optimized (Ollama)
    └─ Context: McKee full book (77k words)
    └─ Tempo: ~5-7 minutos (Deep Dive)

ORCHESTRATORS (orchestrators/)
    └─ DualCoreWrapper: Python + LLM (2 cores)
    └─ TripleCoreWrapper: Python + Examples + LLM (3 cores)

Usage:
    from triple_core.core_1_specialists.dialogue import DrDialogue
    from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

    specialist = DrDialogue()
    wrapper = TripleCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-optimized",
        deep_context=True
    )
    result = wrapper.analyze(screenplay_text)
"""

__version__ = "1.0.0"
__architecture__ = "triple-core"

# Facilitar imports
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

__all__ = [
    "TripleCoreWrapper",
    "DualCoreWrapper",
]
