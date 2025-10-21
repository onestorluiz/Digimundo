"""
Configuração Unificada - OMEGA-ASCENT v5.0 ULTRA-LEAN
Elimina redundância de 3 classes de config
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class UnifiedConfig:
    """Configuração unificada com modo adaptativo"""

    # Pesos base (comuns a todos os modos)
    w_beat: float = 0.44
    w_scene: float = 0.30
    w_act: float = 0.18
    w_global: float = 0.08

    # Parâmetros opcionais (ativados por modo)
    decay_base: Optional[float] = None
    proximity_gain: Optional[float] = None
    mmr_lambda: Optional[float] = None
    arc_boost: Optional[float] = None
    motif_boost: Optional[float] = None

    # Limites de busca
    k_beat: int = 6
    k_scene: int = 3
    k_act: int = 2
    k_global: int = 1

    # Modo de operação
    mode: str = "base"

    @classmethod
    def create(cls, mode: str = "base") -> "UnifiedConfig":
        """Factory method para diferentes modos"""
        configs = {
            "base": cls(),
            "plus": cls(
                decay_base=0.7,
                proximity_gain=0.6,
                mode="plus"
            ),
            "omega_plus": cls(
                decay_base=0.7,
                proximity_gain=0.6,
                mmr_lambda=0.72,
                arc_boost=0.20,
                motif_boost=0.15,
                mode="omega_plus"
            )
        }
        return configs.get(mode, configs["base"])

    def get_active_params(self) -> Dict[str, Any]:
        """Retorna apenas parâmetros ativos (não None)"""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __getitem__(self, key: str) -> Any:
        """Acesso dict-like para compatibilidade"""
        return getattr(self, key, None)
