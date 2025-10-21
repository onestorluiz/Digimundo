"""
📚 CORE 2: Master Examples Finder

Busca exemplos concretos de soluções em 33 roteiros mestres.

Masters incluem:
- Pulp Fiction, Inglourious Basterds (Tarantino)
- Inception, The Dark Knight (Nolan)
- Gladiator, American Beauty
- Star Wars, The Matrix
- E mais 25 roteiros clássicos

Fluxo:
1. Recebe problemas do Core 1
2. Busca em 33 roteiros indexados
3. Retorna 3-6 exemplos concretos
4. Para cada exemplo: screenplay, scene, dialogue, why_good, lesson

Output: Dict com examples_found, total_examples, screenplays_searched
Tempo: ~0.0s (indexação pré-computada)
"""

__core__ = "CORE_2_MASTER_EXAMPLES_FINDER"

from triple_core.core_2_examples.example_finder import ExampleFinderCore

__all__ = ["ExampleFinderCore"]
