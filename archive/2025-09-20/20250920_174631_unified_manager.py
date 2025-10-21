"""
Unified Memory Manager - API única para todas as memórias do sistema.
Integra L1-L4 (SQLite), BM25, e vectorstore (Chroma) com rerank leve.
"""

import os
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import hashlib

from .sqlite_dao import MemoryDAO
from ..rag.adapter import RAGAdapter
import logging

# Configurar logger para memory manager
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UnifiedMemoryManager:
    """
    Gerenciador unificado de memórias.
    Combina múltiplas camadas de memória com diferentes características.
    """

    def __init__(self, settings_or_path):
        """
        Inicializa o gerenciador com configurações.

        Args:
            settings_or_path: Dicionário de configurações ou caminho para o diretório de dados
        """
        # Suportar ambos: dict de settings ou path string
        if isinstance(settings_or_path, str):
            # Path fornecido - criar settings mínimo
            self.settings = {
                'memory': {'time_weighted_retrieval': True, 'promote_on_hits': 5},
                'rag': {'enabled': False}
            }
            db_path = Path(settings_or_path) / 'mem.db'
        else:
            # Settings dict fornecido
            self.settings = settings_or_path
            db_path = Path(__file__).parent.parent.parent / 'data' / 'memory' / 'mem.db'

        logger.info("Inicializando UnifiedMemoryManager")

        # Usar DAO para persistência
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.dao = MemoryDAO(str(db_path))
        logger.info(f"DAO inicializado com banco: {db_path}")
        
        # Inicializar adaptador RAG
        rag_enabled = self.settings.get('rag', {}).get('enabled', False)
        if rag_enabled:
            logger.info("Inicializando adaptador RAG")
            self.rag_adapter = RAGAdapter(self.settings)
        else:
            logger.debug("RAG desabilitado nas configurações")
            self.rag_adapter = None
        
        # Componentes opcionais
        self.chroma_client = None
        self.bm25_index = None
        
        # Configurações de memória
        self.time_weight_enabled = self.settings.get('memory', {}).get('time_weighted_retrieval', True)
        self.promote_threshold = self.settings.get('memory', {}).get('promote_on_hits', 5)
        logger.debug(f"Configurações de memória: time_weight={self.time_weight_enabled}, promote_threshold={self.promote_threshold}")
        
        # Inicializar componentes se habilitados
        if rag_enabled:
            self._init_rag_components()
    
    
    def _init_rag_components(self):
        """Inicializa componentes RAG (BM25 + Vector) - STUB."""
        # STUB: Componentes RAG serão implementados posteriormente
        try:
            # Tentar importar BM25 existente
            from .bm25 import BM25Index
            self.bm25_index = BM25Index()
        except:
            # STUB: BM25 não disponível
            self.bm25_index = None
            
        # STUB: Chroma será conectado via attach_vectorstore()
        self.chroma_client = None
    
    def get_context(self, query: str, max_chunks: int = 12, **kwargs) -> List[Dict]:
        """
        Combina: L1–L4 (SQLite), BM25 (SQLite ou Whoosh), e vectorstore (Chroma) com rerank leve.
        Aplica time-weighted retrieval (recentes e importantes ganham score).
        
        Args:
            query: Query de busca
            max_chunks: Número máximo de chunks a retornar
            **kwargs: Argumentos adicionais (suporta max_memories para compatibilidade)
            
        Returns:
            Lista de trechos [{source, kind, score, text, meta}], já ordenada.
        """
        # Suportar max_memories para compatibilidade com harness
        if 'max_memories' in kwargs:
            max_chunks = kwargs['max_memories']
        
        logger.info(f"Buscando contexto para query: {query[:50]}... (max_chunks={max_chunks})")
        results = []
        
        # 1. Buscar em L1-L4 (SQLite) com matching melhorado
        sql_results = self._search_sql_memories(query, max_chunks * 2)
        for row in sql_results:
            # Calculate keyword matching score (simple BM25 approximation)
            content_lower = row['content'].lower()
            query_lower = query.lower()
            
            # Simple BM25-like score
            bm25_score = 0.0
            if query_lower in content_lower:
                bm25_score = 0.8  # Exact match
            else:
                # Word-level matching
                query_words = query_lower.split()
                matching_words = sum(1 for word in query_words if word in content_lower)
                if matching_words > 0:
                    bm25_score = (matching_words / len(query_words)) * 0.6
            
            # Calculate composite score
            final_score = self._calculate_score(row, semantic_score=0.0, bm25_score=bm25_score)
            
            results.append({
                'source': row['kind'],
                'kind': 'memory',
                'score': final_score,
                'text': row['content'],
                'meta': {
                    'id': row['id'],
                    'tags': row['tags'] if isinstance(row['tags'], list) else [],
                    'importance': row['importance'],
                    'hits': row['hits'],
                    'created_at': row['created_at']
                }
            })
        
        # 2. Buscar via BM25 se disponível
        if self.bm25_index:
            # STUB: BM25 search
            bm25_results = self._search_bm25(query, max_chunks)
            results.extend(bm25_results)
        
        # 3. Buscar via Chroma se disponível
        if self.chroma_client:
            # STUB: Vector search
            vector_results = self._search_vector(query, max_chunks)
            results.extend(vector_results)
        
        # 4. Buscar via RAG Adapter se disponível
        if self.rag_adapter:
            rag_results = self.rag_adapter.retrieve(query, max_chunks // 2)
            for rag_doc in rag_results:
                results.append({
                    'source': rag_doc.get('source', 'RAG'),
                    'kind': 'rag',
                    'score': rag_doc.get('score', 0.5),
                    'text': rag_doc.get('text', ''),
                    'meta': {
                        **rag_doc.get('meta', {}),
                        'citation': rag_doc.get('citation', ''),
                        'rank': rag_doc.get('rank', 0)
                    }
                })
        
        # 5. Ordenação melhorada - mais importante/recente primeiro
        # Sort by score (higher = better match + more recent/important)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Garantir que retornamos apenas o número solicitado
        return results[:max_chunks]
    
    def _search_sql_memories(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Busca memórias em L1-L4 via SQL usando DAO."""
        return self.dao.search_by_content(query, limit)
    
    def _calculate_score(self, row: Dict[str, Any], semantic_score: float = 0.0, bm25_score: float = 0.0) -> float:
        """
        Calcula score composto com pesos configuráveis.
        Formula: α*semantic + β*bm25 + γ*recency + δ*importance + ε*hits
        
        Args:
            row: Dados da memória
            semantic_score: Score semântico (0-1)
            bm25_score: Score BM25 (0-1)
            
        Returns:
            Score final normalizado (0-1)
        """
        # Pesos padrão (soma = 1.0)
        weights = self.settings.get('memory', {}).get('ranking_weights', {})
        alpha = weights.get('semantic', 0.35)
        beta = weights.get('bm25', 0.25)
        gamma = weights.get('recency', 0.20)
        delta = weights.get('importance', 0.15)
        epsilon = weights.get('hits', 0.05)
        
        # Componente 1: Score semântico
        comp_semantic = semantic_score * alpha
        
        # Componente 2: Score BM25
        comp_bm25 = bm25_score * beta
        
        # Componente 3: Recência
        recency_score = 0.0
        try:
            last_accessed_str = row.get('last_accessed', row.get('created_at', ''))
            if last_accessed_str:
                # Parse datetime
                if 'T' in last_accessed_str:
                    last_accessed = datetime.fromisoformat(last_accessed_str.replace('Z', '+00:00'))
                else:
                    last_accessed = datetime.fromisoformat(last_accessed_str)
                
                # Calculate recency score (exponential decay)
                age_hours = (datetime.now() - last_accessed.replace(tzinfo=None)).total_seconds() / 3600
                recency_score = max(0, 1.0 - (age_hours / 168))  # Decay over 1 week
                
        except (ValueError, TypeError) as e:
            logger.debug(f"Failed to parse date: {e}")
            
        comp_recency = recency_score * gamma
        
        # Componente 4: Importância
        importance = float(row.get('importance', 0.5))
        comp_importance = importance * delta
        
        # Componente 5: Hits (normalized)
        hits = int(row.get('hits', 0))
        hit_score = min(hits / 10, 1.0)  # Normalize to 0-1 (10+ hits = max)
        comp_hits = hit_score * epsilon
        
        # Score final
        final_score = comp_semantic + comp_bm25 + comp_recency + comp_importance + comp_hits
        
        # Normalizar para 0-1
        return min(max(final_score, 0.0), 1.0)
    
    def _search_bm25(self, query: str, limit: int) -> List[Dict]:
        """STUB: Busca BM25."""
        # STUB: Retorna lista vazia por enquanto
        return []
    
    def _search_vector(self, query: str, limit: int) -> List[Dict]:
        """STUB: Busca vetorial."""
        # STUB: Retorna lista vazia por enquanto
        return []
    
    def add_memory(self, content: str, timestamp: Optional[Any] = None,
                  importance: Optional[float] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Shim para compatibilidade com harness - delega para save_memory.
        
        Args:
            content: Conteúdo da memória
            timestamp: Timestamp (ignorado, usamos datetime.now())
            importance: Importância [0.0, 1.0]
            metadata: Metadados incluindo tags
            
        Returns:
            Dict com resultado da operação
        """
        tags = None
        if metadata and 'tags' in metadata:
            tags = metadata['tags']
        elif metadata and 'test_id' in metadata:
            # Para testes do harness
            tags = [metadata['test_id']]
        
        result = self.save_memory(content, tags, importance)
        return {'id': result, 'success': True}
    
    def get_memory_by_id(self, mem_id: str) -> Optional[Dict]:
        """
        Busca memória por ID.
        """
        try:
            return self.dao.get_memory(mem_id)
        except:
            return None
    
    def get_all_memories(self, limit: int = 10) -> List[Dict]:
        """
        Retorna todas as memórias (limitado).
        """
        try:
            # Usar DAO para buscar memórias recentes
            mems = self.dao.search_memories("", limit=limit)
            return [{'id': m[0], 'content': m[1], 'importance': m[4]} for m in mems]
        except:
            return []
    
    def record_hit(self, mem_id: str) -> None:
        """
        Registra hit em memória (para promoção).
        """
        try:
            # Incrementar importância (simulação)
            mem = self.dao.get_memory(mem_id)
            if mem and len(mem) > 4:
                new_importance = min(1.0, mem[4] + 0.1)
                # Não temos update direto, então apenas logamos
                logger.debug(f"Hit registrado para {mem_id}, importância: {new_importance}")
        except:
            pass
    
    def save_memory(self, content: str, tags: Optional[List[str]] = None, 
                   importance: Optional[float] = None) -> str:
        """
        Salva em L3; define importance pela heurística; retorna id.
        
        Args:
            content: Conteúdo da memória
            tags: Tags opcionais
            importance: Importância (0-1), calculada se None
            
        Returns:
            ID da memória salva
        """
        # Gerar ID único
        mem_id = hashlib.md5(f"{content}{time.time()}".encode()).hexdigest()[:12]
        
        # Calcular importância se não fornecida
        if importance is None:
            importance = self._calculate_importance(content, tags)
        
        # Usar DAO para salvar
        success = self.dao.create(
            id=mem_id,
            content=content,
            tags=tags,
            importance=importance,
            kind='L3'
        )
        
        return mem_id if success else None
    
    def _calculate_importance(self, content: str, tags: Optional[List[str]]) -> float:
        """Calcula importância heurística baseada no conteúdo."""
        importance = 0.5  # Base
        
        # Boost por tamanho (conteúdo mais longo pode ser mais importante)
        if len(content) > 500:
            importance += 0.1
        
        # Boost por tags específicas
        if tags:
            priority_tags = ['important', 'core', 'key', 'critical']
            if any(tag in priority_tags for tag in tags):
                importance += 0.2
        
        # Boost por palavras-chave
        keywords = ['error', 'fix', 'solution', 'important', 'remember']
        content_lower = content.lower()
        if any(kw in content_lower for kw in keywords):
            importance += 0.15
        
        return min(importance, 1.0)
    
    def promote_memory(self, mem_id: str) -> bool:
        """
        Promove L3->L2 conforme hits/importance.
        
        Args:
            mem_id: ID da memória
            
        Returns:
            True se promovida, False caso contrário
        """
        # Buscar memória usando DAO
        memory = self.dao.read(mem_id)
        
        if not memory:
            return False
        
        # Verificar se pode promover (L3 -> L2)
        if memory['kind'] != 'L3':
            return False
        
        # Verificar critérios de promoção
        can_promote = (
            memory['hits'] >= self.promote_threshold or
            memory['importance'] >= 0.8
        )
        
        if can_promote:
            return self.dao.promote(mem_id, 'L2')
        
        return False
    
    def record_hit(self, mem_id: str) -> None:
        """
        Incrementa hits e last_accessed; gatilha promoção quando cruzar limiar.
        
        Args:
            mem_id: ID da memória
        """
        # Incrementar hits usando DAO
        if self.dao.increment_hits(mem_id):
            # Verificar se deve promover
            memory = self.dao.read(mem_id)
            
            if memory and memory['hits'] >= self.promote_threshold and memory['kind'] == 'L3':
                self.promote_memory(mem_id)
    
    def attach_vectorstore(self, chroma_client_or_path: str) -> None:
        """
        Conecta/abre store semântica para memórias e para PDFs externos.
        
        Args:
            chroma_client_or_path: Cliente Chroma ou caminho para persistência
        """
        try:
            # STUB: Tentar importar Chroma
            import chromadb
            
            if isinstance(chroma_client_or_path, str):
                # Caminho fornecido - criar cliente persistente
                self.chroma_client = chromadb.PersistentClient(path=chroma_client_or_path)
            else:
                # Cliente já fornecido
                self.chroma_client = chroma_client_or_path
                
            # Criar/obter collection
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name="scripturemon_memories"
            )
            
        except ImportError:
            # STUB: Chroma não disponível
            print("AVISO: ChromaDB não disponível. Vectorstore não conectado.")
            self.chroma_client = None
    
    def close(self):
        """Fecha conexões e recursos."""
        if self.dao:
            self.dao.close()