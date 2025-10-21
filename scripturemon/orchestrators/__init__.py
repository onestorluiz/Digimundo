"""
🎯 ORCHESTRATORS: Triple-Core Wrappers

Wrappers que combinam os 3 cores em análises completas.

DualCoreWrapper (Base):
- Combina Core 1 (Python) + Core 3 (LLM)
- Prompt completo de 260 linhas
- Theory indexer com Deep Dive mode
- Synthesis Python + LLM

TripleCoreWrapper (Triple-Core):
- Herda de DualCoreWrapper
- Adiciona Core 2 (Examples Finder)
- Combina 3 cores independentes
- Output final: TXT + HTML

Usage:
    from triple_core.orchestrators import TripleCoreWrapper
    from triple_core.core_1_specialists.dialogue import DrDialogue

    wrapper = TripleCoreWrapper(
        python_specialist=DrDialogue(),
        llm_model="scripturemon-optimized",
        deep_context=True
    )
    result = wrapper.analyze(screenplay_text)
"""

__orchestrators__ = ["DualCoreWrapper", "TripleCoreWrapper"]

from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

__all__ = ["DualCoreWrapper", "TripleCoreWrapper"]
