#!/usr/bin/env python3
"""
MemBridge Module - Ponte de Memória Avançada (Stub para Fase 1.C)
Sistema complexo de gerenciamento de memória
"""

import time
import json
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from collections import deque

class MemoryType(Enum):
    """Tipos de memória no sistema"""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"

class ImportanceLevel(Enum):
    """Níveis de importância para memórias"""
    TRIVIAL = 0.1
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    CRITICAL = 0.9
    ETERNAL = 1.0

# Estado global do sistema de memória
_memory_state = {
    "short_term": deque(maxlen=100),
    "long_term": [],
    "episodic": [],
    "semantic": {},
    "procedural": {},
    "total_memories": 0,
    "promoted_count": 0,
    "forgotten_count": 0,
    "consolidation_runs": 0
}

def promote(memory: Dict[str, Any], importance: float = 0.5) -> bool:
    """
    Promove memória entre níveis
    Sistema complexo de promoção baseado em importância
    """
    # Enriquecer memória com metadados
    enriched = {
        **memory,
        "timestamp": time.time(),
        "importance": importance,
        "access_count": 0,
        "last_accessed": time.time(),
        "memory_id": f"mem_{_memory_state['total_memories']}",
        "consolidation_level": 0
    }
    
    _memory_state["total_memories"] += 1
    
    # Decisão complexa de onde armazenar
    if importance >= ImportanceLevel.HIGH.value:
        # Memórias importantes vão direto para long-term
        _memory_state["long_term"].append(enriched)
        _memory_state["promoted_count"] += 1
        
        # Também adicionar ao episódico se for experiência
        if memory.get("kind") == "experience":
            _memory_state["episodic"].append(enriched)
    
    elif importance >= ImportanceLevel.MEDIUM.value:
        # Médias vão para short-term primeiro
        _memory_state["short_term"].append(enriched)
        
    else:
        # Baixa importância: avaliar se vale armazenar
        if len(_memory_state["short_term"]) < 50:
            _memory_state["short_term"].append(enriched)
        else:
            _memory_state["forgotten_count"] += 1
            return False
    
    # Trigger consolidação se necessário
    if _memory_state["total_memories"] % 50 == 0:
        _consolidate_memories()
    
    return True

def counts() -> Dict[str, int]:
    """
    Retorna contagens detalhadas de memórias
    """
    return {
        "short_term": len(_memory_state["short_term"]),
        "long_term": len(_memory_state["long_term"]),
        "episodic": len(_memory_state["episodic"]),
        "semantic": len(_memory_state["semantic"]),
        "procedural": len(_memory_state["procedural"]),
        "total": _memory_state["total_memories"],
        "promoted": _memory_state["promoted_count"],
        "forgotten": _memory_state["forgotten_count"],
        "consolidations": _memory_state["consolidation_runs"]
    }

def retrieve(query: str, memory_type: Optional[MemoryType] = None) -> List[Dict[str, Any]]:
    """
    Recupera memórias baseado em query
    Sistema complexo de busca
    """
    results = []
    
    # Buscar em diferentes tipos de memória
    if memory_type == MemoryType.SHORT_TERM or memory_type is None:
        for mem in _memory_state["short_term"]:
            if _matches_query(mem, query):
                mem["access_count"] += 1
                mem["last_accessed"] = time.time()
                results.append(mem)
    
    if memory_type == MemoryType.LONG_TERM or memory_type is None:
        for mem in _memory_state["long_term"]:
            if _matches_query(mem, query):
                mem["access_count"] += 1
                mem["last_accessed"] = time.time()
                results.append(mem)
    
    # Ordenar por relevância (importância + acessos)
    results.sort(key=lambda x: x.get("importance", 0) + (x.get("access_count", 0) * 0.01), reverse=True)
    
    return results[:10]  # Máximo 10 resultados

def consolidate() -> Dict[str, Any]:
    """
    Força consolidação de memórias
    Processo complexo de otimização
    """
    return _consolidate_memories()

def _consolidate_memories() -> Dict[str, Any]:
    """
    Consolidação interna de memórias
    Move memórias importantes de short para long-term
    """
    _memory_state["consolidation_runs"] += 1
    
    promoted = 0
    forgotten = 0
    
    # Avaliar memórias short-term
    current_short = list(_memory_state["short_term"])
    _memory_state["short_term"].clear()
    
    for mem in current_short:
        # Calcular score de consolidação
        age = time.time() - mem.get("timestamp", time.time())
        importance = mem.get("importance", 0.5)
        access_count = mem.get("access_count", 0)
        
        consolidation_score = importance + (access_count * 0.1) - (age / 86400)  # age em dias
        
        if consolidation_score > 0.6:
            # Promover para long-term
            mem["consolidation_level"] += 1
            _memory_state["long_term"].append(mem)
            promoted += 1
        elif consolidation_score > 0.3:
            # Manter em short-term
            _memory_state["short_term"].append(mem)
        else:
            # Esquecer
            forgotten += 1
    
    _memory_state["promoted_count"] += promoted
    _memory_state["forgotten_count"] += forgotten
    
    return {
        "consolidated": promoted,
        "forgotten": forgotten,
        "retained": len(_memory_state["short_term"]),
        "timestamp": time.time()
    }

def _matches_query(memory: Dict[str, Any], query: str) -> bool:
    """
    Verifica se memória corresponde à query
    """
    query_lower = query.lower()
    
    # Buscar em todos os campos string da memória
    for key, value in memory.items():
        if isinstance(value, str) and query_lower in value.lower():
            return True
        elif isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, str) and query_lower in v.lower():
                    return True
    
    return False

def get_statistics() -> Dict[str, Any]:
    """
    Retorna estatísticas avançadas do sistema
    """
    total_size = 0
    oldest_memory = None
    newest_memory = None
    most_accessed = None
    
    all_memories = (
        list(_memory_state["short_term"]) + 
        _memory_state["long_term"] + 
        _memory_state["episodic"]
    )
    
    if all_memories:
        oldest_memory = min(all_memories, key=lambda x: x.get("timestamp", float('inf')))
        newest_memory = max(all_memories, key=lambda x: x.get("timestamp", 0))
        most_accessed = max(all_memories, key=lambda x: x.get("access_count", 0))
        
        # Estimar tamanho
        for mem in all_memories:
            total_size += len(json.dumps(mem))
    
    return {
        "total_memories": _memory_state["total_memories"],
        "active_memories": len(all_memories),
        "memory_usage_bytes": total_size,
        "oldest_timestamp": oldest_memory.get("timestamp") if oldest_memory else None,
        "newest_timestamp": newest_memory.get("timestamp") if newest_memory else None,
        "most_accessed_id": most_accessed.get("memory_id") if most_accessed else None,
        "consolidation_runs": _memory_state["consolidation_runs"],
        "promotion_rate": _memory_state["promoted_count"] / max(1, _memory_state["total_memories"]),
        "forget_rate": _memory_state["forgotten_count"] / max(1, _memory_state["total_memories"])
    }

__all__ = [
    "promote", "counts", "retrieve", "consolidate",
    "get_statistics", "MemoryType", "ImportanceLevel"
]