"""
Sistema Hierárquico Unificado - Strategy Pattern
Elimina 3 implementações redundantes
"""

from typing import List, Dict, Tuple, Optional, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass

class SearchStrategy(Protocol):
    """Interface para estratégias de busca"""

    def enhance(self, results: List[Tuple], **kwargs) -> List[Tuple]:
        """Melhora resultados com lógica específica"""
        ...

class BaseStrategy:
    """Estratégia base com funcionalidade comum"""

    def apply_weights(self, results: List[Tuple], config: Dict) -> List[Tuple]:
        """Aplica pesos comuns a todos"""
        weighted = []
        for level, doc_id, score in results:
            if level == "beat":
                score *= config.get("w_beat", 0.44)
            elif level == "scene":
                score *= config.get("w_scene", 0.30)
            elif level == "act":
                score *= config.get("w_act", 0.18)
            elif level == "global":
                score *= config.get("w_global", 0.08)
            weighted.append((level, doc_id, score))
        return weighted

class StandardStrategy(BaseStrategy):
    """Estratégia padrão (hier_rag original)"""

    def enhance(self, results: List[Tuple], **kwargs) -> List[Tuple]:
        return self.apply_weights(results, kwargs.get("config", {}))

class PlusStrategy(BaseStrategy):
    """Estratégia Plus com decay"""

    def enhance(self, results: List[Tuple], **kwargs) -> List[Tuple]:
        weighted = self.apply_weights(results, kwargs.get("config", {}))

        # Aplica decay baseado em distância
        decay_base = kwargs.get("config", {}).get("decay_base", 0.7)
        focus_index = kwargs.get("focus_scene_index")

        if focus_index is not None:
            enhanced = []
            for level, doc_id, score in weighted:
                if "beat_" in doc_id:
                    # Extrair índice da cena
                    import re
                    match = re.search(r"beat_(?:dyn_)?(\d+)_", doc_id)
                    if match:
                        scene_idx = int(match.group(1))
                        dist = abs(scene_idx - focus_index)
                        decay_factor = decay_base ** dist
                        score *= (1.0 + 0.6 * decay_factor)
                enhanced.append((level, doc_id, score))
            return enhanced

        return weighted

class OmegaPlusStrategy(PlusStrategy):
    """Estratégia Omega Plus com arc boost e motif router"""

    def enhance(self, results: List[Tuple], **kwargs) -> List[Tuple]:
        # Primeiro aplica melhorias da Plus
        enhanced = super().enhance(results, **kwargs)

        config = kwargs.get("config", {})
        arc_scores = kwargs.get("arc_scores", {})
        motifs = kwargs.get("motifs", [])

        # Aplica arc boost
        arc_boost = config.get("arc_boost", 0.20)
        final_results = []

        for level, doc_id, score in enhanced:
            beat_key = doc_id.replace("beat_", "")
            if beat_key in arc_scores:
                arc_score = arc_scores[beat_key]
                if arc_score > 0:
                    score *= (1.0 + arc_boost * min(1.0, arc_score))

            # Aplica motif boost se houver motifs
            if motifs and level == "beat":
                # Simplificado - verificar presença de motifs
                score *= 1.15  # boost fixo por simplicidade

            final_results.append((level, doc_id, score))

        return sorted(final_results, key=lambda x: x[2], reverse=True)

class UnifiedHierarchicalSearcher:
    """Buscador hierárquico unificado"""

    def __init__(self, strategy_name: str = "omega_plus"):
        self.strategies = {
            "standard": StandardStrategy(),
            "plus": PlusStrategy(),
            "omega_plus": OmegaPlusStrategy()
        }
        self.strategy = self.strategies.get(strategy_name, StandardStrategy())

    def search(self,
               rag_service,
               queries: List[str],
               config: Dict,
               **kwargs) -> List[Tuple[str, str, float]]:
        """Busca unificada com estratégia plugável"""

        # Busca base comum a todas as estratégias (70% do código original)
        results = []

        # Busca em beats
        beat_hits = {}
        for query in queries:
            for doc_id, score in rag_service.search(query, ns="script_beat", k=20):
                beat_hits[doc_id] = max(beat_hits.get(doc_id, 0.0), score)

        k_beat = config.get("k_beat", 6)
        top_beats = sorted(beat_hits.items(), key=lambda x: x[1], reverse=True)[:k_beat]
        results.extend([("beat", doc_id, score) for doc_id, score in top_beats])

        # Busca em scenes
        scene_hits = {}
        for query in queries:
            for doc_id, score in rag_service.search(query, ns="script_scene", k=8):
                scene_hits[doc_id] = max(scene_hits.get(doc_id, 0.0), score)

        k_scene = config.get("k_scene", 3)
        top_scenes = sorted(scene_hits.items(), key=lambda x: x[1], reverse=True)[:k_scene]
        results.extend([("scene", doc_id, score) for doc_id, score in top_scenes])

        # Busca em acts
        act_hits = {}
        for query in queries:
            for doc_id, score in rag_service.search(query, ns="script_act", k=5):
                act_hits[doc_id] = max(act_hits.get(doc_id, 0.0), score)

        k_act = config.get("k_act", 2)
        top_acts = sorted(act_hits.items(), key=lambda x: x[1], reverse=True)[:k_act]
        results.extend([("act", doc_id, score) for doc_id, score in top_acts])

        # Busca global
        glob_hits = {}
        for query in queries:
            for doc_id, score in rag_service.search(query, ns="script_global", k=1):
                glob_hits[doc_id] = max(glob_hits.get(doc_id, 0.0), score)

        if glob_hits:
            k_global = config.get("k_global", 1)
            top_global = sorted(glob_hits.items(), key=lambda x: x[1], reverse=True)[:k_global]
            results.extend([("global", doc_id, score) for doc_id, score in top_global])

        # Aplicar estratégia específica (30% do código variável)
        enhanced_results = self.strategy.enhance(
            results,
            config=config,
            **kwargs
        )

        return enhanced_results

# Função de compatibilidade para migração fácil
def hierarchical_search(rag_service, queries, focus_scene_index, cfg, features,
                        arc_scores, progress_scores, index_map, motifs=None):
    """Wrapper de compatibilidade para código legado"""

    # Determinar estratégia baseado na config
    if hasattr(cfg, 'arc_boost'):
        strategy = 'omega_plus'
    elif hasattr(cfg, 'decay_base'):
        strategy = 'plus'
    else:
        strategy = 'standard'

    searcher = UnifiedHierarchicalSearcher(strategy)

    config_dict = cfg.__dict__ if hasattr(cfg, '__dict__') else cfg

    return searcher.search(
        rag_service,
        queries,
        config_dict,
        focus_scene_index=focus_scene_index,
        features=features,
        arc_scores=arc_scores,
        progress_scores=progress_scores,
        index_map=index_map,
        motifs=motifs
    )
