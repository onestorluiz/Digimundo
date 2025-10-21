#!/usr/bin/env python3
"""
FASE 4: Shim de Compatibilidade - RAG BM25
Redireciona chamadas do sistema antigo para o novo BM25 do ChatGPT

Este arquivo substitui o rag_system.py original com uma interface
compatível que usa o BM25 superior implementado pelo ChatGPT.
"""

import sys
import os
from typing import List, Dict, Any, Optional
import logging

# Adiciona o sistema BM25 ao path
BM25_PATH = "/Users/clubproducoes/Digimundo/scripturemon-champion-refactored-bm25-tests 2/src"
if BM25_PATH not in sys.path:
    sys.path.insert(0, BM25_PATH)

# Importa o sistema BM25 do ChatGPT
try:
    from scripturemon_champion.rag import (
        index_document as bm25_index,
        search_documents as bm25_search,
        _INDEX as bm25_index_obj
    )
    BM25_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  BM25 não disponível, usando fallback: {e}")
    BM25_AVAILABLE = False

logger = logging.getLogger(__name__)

class RAGSystem:
    """
    Shim de compatibilidade para o RAG System original.
    Redireciona todas as operações para o BM25 do ChatGPT.
    """

    def __init__(self, db_path: Optional[str] = None, use_vector_search: bool = False):
        """
        Inicializa o sistema RAG (agora com BM25).

        Args:
            db_path: Ignorado (BM25 usa memória)
            use_vector_search: Ignorado (BM25 é superior)
        """
        self.documents_indexed = 0
        self.last_query = None
        self.last_results = []

        if not BM25_AVAILABLE:
            logger.warning("BM25 não disponível - modo degradado")
        else:
            logger.info("🚀 RAG System agora usa BM25 (10-100x melhor!)")

    def index_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """
        Indexa um documento no sistema BM25.

        Args:
            doc_id: ID único do documento
            content: Conteúdo textual
            metadata: Metadados opcionais

        Returns:
            True se sucesso
        """
        if not BM25_AVAILABLE:
            return False

        try:
            bm25_index(doc_id, content, metadata)
            self.documents_indexed += 1
            logger.debug(f"✅ Documento {doc_id} indexado com BM25")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao indexar {doc_id}: {e}")
            return False

    def add_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """Alias para index_document (compatibilidade)."""
        return self.index_document(doc_id, content, metadata)

    def search(self, query: str, top_k: int = 5, threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Busca documentos usando BM25.

        Args:
            query: Consulta de busca
            top_k: Número máximo de resultados
            threshold: Score mínimo (aplicado após busca)

        Returns:
            Lista de resultados com doc_id, score e metadata
        """
        if not BM25_AVAILABLE:
            return []

        try:
            results = bm25_search(query, top_k=top_k)

            # Aplica threshold se necessário
            if threshold > 0:
                results = [r for r in results if r.get('score', 0) >= threshold]

            self.last_query = query
            self.last_results = results

            logger.debug(f"🔍 BM25 retornou {len(results)} resultados para '{query}'")
            return results

        except Exception as e:
            logger.error(f"❌ Erro na busca BM25: {e}")
            return []

    def search_documents(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Alias para search (compatibilidade)."""
        return self.search(query, top_k=limit)

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera um documento específico.

        Args:
            doc_id: ID do documento

        Returns:
            Documento ou None
        """
        if not BM25_AVAILABLE:
            return None

        try:
            # Acessa diretamente o índice BM25
            if hasattr(bm25_index_obj, 'docs') and doc_id in bm25_index_obj.docs:
                doc = bm25_index_obj.docs[doc_id]
                return {
                    'doc_id': doc.doc_id,
                    'content': doc.text,
                    'metadata': doc.metadata
                }
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar {doc_id}: {e}")
            return None

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove um documento do índice.

        Args:
            doc_id: ID do documento

        Returns:
            True se sucesso
        """
        if not BM25_AVAILABLE:
            return False

        try:
            # BM25 tem método interno _remove_if_exists
            if hasattr(bm25_index_obj, '_remove_if_exists'):
                bm25_index_obj._remove_if_exists(doc_id)
                logger.debug(f"🗑️  Documento {doc_id} removido")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao remover {doc_id}: {e}")
            return False

    def clear_index(self) -> bool:
        """
        Limpa todo o índice BM25.

        Returns:
            True se sucesso
        """
        if not BM25_AVAILABLE:
            return False

        try:
            # Reinicializa o índice
            bm25_index_obj.docs.clear()
            bm25_index_obj.tf.clear()
            bm25_index_obj.df.clear()
            bm25_index_obj.doc_len.clear()
            bm25_index_obj.N = 0
            bm25_index_obj.avgdl = 0.0

            self.documents_indexed = 0
            logger.info("🧹 Índice BM25 limpo")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao limpar índice: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do sistema.

        Returns:
            Dicionário com estatísticas
        """
        stats = {
            'bm25_available': BM25_AVAILABLE,
            'documents_indexed': self.documents_indexed,
            'last_query': self.last_query,
            'last_results_count': len(self.last_results)
        }

        if BM25_AVAILABLE and hasattr(bm25_index_obj, 'N'):
            stats.update({
                'total_documents': bm25_index_obj.N,
                'avg_doc_length': bm25_index_obj.avgdl,
                'unique_terms': len(bm25_index_obj.df)
            })

        return stats

    def __repr__(self) -> str:
        """Representação do sistema."""
        if BM25_AVAILABLE:
            return f"<RAGSystem BM25 com {bm25_index_obj.N} docs>"
        return "<RAGSystem (BM25 indisponível)>"


# Compatibilidade com imports diretos
def create_rag_system(**kwargs):
    """Factory function para criar RAG System."""
    return RAGSystem(**kwargs)


# Se executado diretamente, mostra status
if __name__ == "__main__":
    print("="*60)
    print("RAG BM25 SHIM - Status de Compatibilidade")
    print("="*60)

    rag = RAGSystem()

    if BM25_AVAILABLE:
        print("✅ BM25 disponível e funcionando!")

        # Teste rápido
        print("\nTestando indexação e busca...")
        rag.index_document("test1", "O herói enfrenta o vilão na batalha final")
        rag.index_document("test2", "A jornada do herói começa com um chamado")

        results = rag.search("herói vilão", top_k=2)
        print(f"\nResultados para 'herói vilão':")
        for r in results:
            print(f"  - {r['doc_id']}: {r['score']:.2f}")

        print(f"\nEstatísticas: {rag.get_stats()}")
    else:
        print("❌ BM25 não disponível - instale o sistema ChatGPT")

    print("="*60)