"""
🔧 CORE 1: Python Technical Analysis

Especialistas Python que realizam análise técnica objetiva de roteiros.
Cada especialista (Dr*) é um Script Doctor focado em uma área específica.

Categorias:
- dialogue/     → Análise de diálogos (DrDialogue)
- structure/    → Estrutura de 3 atos (DrStructure)
- character/    → Personagens (DrPsychology, DrArcs, DrRelationships)
- theme/        → Temas e subtexto
- style/        → Tom, voz, estilo
- formatting/   → Formatação técnica
- quality/      → Qualidade geral e mercado

Output: Dict com scores, violations, recommendations
Tempo: ~0.0s (análise Python pura)
"""

__core__ = "CORE_1_PYTHON_TECHNICAL_ANALYSIS"

# Facilitar imports dos especialistas principais
try:
    from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
except ImportError:
    pass

try:
    from triple_core.core_1_specialists.structure.dr_structure import DrStructure
except ImportError:
    pass

try:
    from triple_core.core_1_specialists.character.dr_psychology import DrPsychology
    from triple_core.core_1_specialists.character.dr_arcs import DrArcs
    from triple_core.core_1_specialists.character.dr_relationships import DrRelationships
except ImportError:
    pass

__all__ = [
    "DrDialogue",
    "DrStructure",
    "DrPsychology",
    "DrArcs",
    "DrRelationships",
]
