"""
RAG Adapter - Interface unificada para sistemas RAG avançados.
Integra HyDE, RAPTOR, Self-RAG e outros em uma API padronizada.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.logging_setup import get_rag_logger

# Configurar logger para RAG
logger = get_rag_logger()

# Tentar importar módulos RAG existentes
try:
    from apps.scripturemon.rag_advanced import HyDE, RAPTOR, SelfRAG
    RAG_AVAILABLE = True
except ImportError:
    logger.warning("Módulos RAG avançados não disponíveis. Usando stubs.")
    RAG_AVAILABLE = False


class RAGAdapter:
    """
    Adaptador unificado para sistemas RAG.
    Fornece interface consistente independente da implementação.
    """
    
    def __init__(self, settings: Optional[Dict] = None):
        """
        Inicializa o adaptador RAG.
        
        Args:
            settings: Configurações do sistema
        """
        self.settings = settings or {}
        self.rag_config = self.settings.get('rag', {})
        self.enabled = self.rag_config.get('enabled', True)
        self.provider = self.rag_config.get('provider', 'chroma')
        self.k = self.rag_config.get('k', 8)
        
        # Inicializar componentes se disponíveis
        if RAG_AVAILABLE and self.enabled:
            try:
                self.hyde = HyDE()
                self.raptor = RAPTOR()
                self.self_rag = SelfRAG()
                logger.info("✅ Módulos RAG avançados carregados")
            except Exception as e:
                logger.error(f"Erro ao inicializar módulos RAG: {e}")
                self.hyde = None
                self.raptor = None
                self.self_rag = None
        else:
            self.hyde = None
            self.raptor = None
            self.self_rag = None
            
        # Cache de resultados
        self._cache = {}
        
        # Base de conhecimento (stub para testes)
        self._knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> List[Dict]:
        """
        Carrega base de conhecimento (PDFs, documentos, etc).
        
        Returns:
            Lista de documentos
        """
        knowledge = []
        
        # Tentar carregar PDFs se existirem
        pdf_dirs = [
            Path(__file__).parent.parent.parent / 'data' / 'pdfs',
            Path(__file__).parent.parent.parent / 'data' / 'cinema_knowledge' / 'pdfs',
            Path(__file__).parent.parent.parent / 'CINEMA_KNOWLEDGE'
        ]
        
        for pdf_dir in pdf_dirs:
            if pdf_dir.exists():
                for pdf_file in pdf_dir.glob('**/*.pdf'):
                    knowledge.append({
                        'source': str(pdf_file.name),
                        'type': 'pdf',
                        'path': str(pdf_file),
                        'content': f"[Conteúdo de {pdf_file.name}]"  # Stub
                    })
                    logger.info(f"📄 PDF encontrado: {pdf_file.name}")
        
        # Se não houver PDFs, criar conhecimento stub
        if not knowledge:
            logger.info("Nenhum PDF encontrado. Usando base de conhecimento stub.")
            knowledge = self._create_stub_knowledge()
        
        return knowledge
    
    def _create_stub_knowledge(self) -> List[Dict]:
        """
        Cria base de conhecimento stub para testes.
        
        Returns:
            Lista de documentos stub
        """
        return [
            {
                'source': 'manual_roteiro.pdf',
                'type': 'stub',
                'content': """Manual de Roteiro Cinematográfico
                
                Capítulo 1: Estrutura de Três Atos
                A estrutura clássica divide o roteiro em Setup (25%), Confrontação (50%) 
                e Resolução (25%). Pontos de virada conectam os atos.
                
                Capítulo 2: Desenvolvimento de Personagens
                Personagens precisam de objetivos claros, conflitos internos e externos,
                e arcos de transformação que ressoem com o tema.""",
                'meta': {'pages': 120, 'author': 'Sistema Stub'}
            },
            {
                'source': 'dialogos_cinema.pdf',
                'type': 'stub',
                'content': """Diálogos no Cinema
                
                Princípios fundamentais:
                - Subtexto: o que não é dito é mais importante
                - Economia: cada linha deve avançar trama ou revelar caráter
                - Voz única: cada personagem tem ritmo e vocabulário próprios
                - Show don't tell: evitar exposição direta""",
                'meta': {'pages': 85, 'author': 'Sistema Stub'}
            },
            {
                'source': 'tecnicas_visuais.pdf',
                'type': 'stub',
                'content': """Narrativa Visual para Roteiristas
                
                Como escrever visualmente:
                - Descrições econômicas mas evocativas
                - Foco em ações e comportamentos
                - Criar imagens que transmitam emoção
                - Pensar em composição e movimento de câmera
                - Usar objetos e ambiente como extensão dos personagens""",
                'meta': {'pages': 156, 'author': 'Sistema Stub'}
            }
        ]
    
    def add_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """
        Adiciona documento ao knowledge base.
        Criado para compatibilidade com harness.
        
        Args:
            doc_id: ID do documento
            content: Conteúdo do documento
            metadata: Metadados opcionais
            
        Returns:
            bool indicando sucesso
        """
        doc = {
            'id': doc_id,
            'content': content,
            'metadata': metadata or {},
            'type': 'synthetic',
            'source': metadata.get('source', 'test') if metadata else 'test'
        }
        
        self._knowledge_base.append(doc)
        logger.info(f"Documento adicionado: {doc_id}")
        return True
    
    def query(self, query_text: str, k: Optional[int] = None) -> List[Dict]:
        """
        Alias para retrieve - compatibilidade com harness.
        """
        return self.retrieve(query_text, k)
    
    def query_with_hyde(self, query_text: str, k: int = 5) -> List[Dict]:
        """
        Query usando HyDE (Hypothetical Document Embeddings).
        """
        # Por ora, usar retrieve normal
        return self.retrieve(query_text, k)
    
    def format_citations(self, results: List[Dict]) -> str:
        """
        Formata citações dos resultados.
        """
        if not results:
            return ""
        
        citations = []
        for i, r in enumerate(results[:3], 1):
            source = r.get('metadata', {}).get('source', 'Unknown')
            content_preview = r.get('content', '')[:100]
            citations.append(f"[{i}] Source: {source}\n    {content_preview}...")
        
        return "\n\n📚 Citations:\n" + "\n".join(citations)
    
    def cite(self, snippet: Dict) -> str:
        """
        Gera citação formatada para um snippet - HARDENED V3.
        
        Args:
            snippet: Dict com text, source, meta
            
        Returns:
            String de citação formatada
        """
        if not self.enabled or not snippet:
            return "[Citation: RAG disabled or empty snippet]"
        
        source = snippet.get('source', 'Unknown')
        meta = snippet.get('meta', {})
        score = snippet.get('score', 0.0)
        
        # Formatação determinística
        if source == "stub":
            return f"[Stub Source - Score: {score:.2f}]"
        
        # Citação com metadados
        parts = [f"[{source}"]
        if 'page' in meta:
            parts.append(f"p.{meta['page']}")
        if 'chapter' in meta:
            parts.append(f"ch.{meta['chapter']}")
        parts.append(f"score:{score:.2f}]")
        
        return " ".join(parts)
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Dict]:
        """
        Recupera documentos relevantes usando RAG avançado.
        
        Args:
            query: Query de busca
            k: Número de documentos a retornar
            
        Returns:
            Lista de documentos com [text, source, meta, score]
        """
        if not self.enabled:
            logger.debug("RAG desabilitado, retornando lista vazia")
            return []
        
        k = k or self.k
        logger.info(f"Recuperando {k} documentos para query: {query[:50]}...")
        
        # Check cache
        cache_key = f"{query}_{k}"
        if cache_key in self._cache:
            logger.debug(f"Cache hit para: {query[:30]}...")
            return self._cache[cache_key]
        
        results = []
        
        try:
            # 1. Expandir query com HyDE se disponível
            if self.hyde:
                expanded_query = self.hyde.generate_hypothetical(query)
                logger.debug(f"Query expandida com HyDE: {len(query)} → {len(expanded_query)} chars")
            else:
                expanded_query = query
            
            # 2. Buscar com RAPTOR se disponível
            if self.raptor:
                # RAPTOR constrói árvore hierárquica
                docs = [{'content': expanded_query, 'type': 'query'}]
                tree = self.raptor.build_tree(docs)
                # Extrair nós relevantes
                for level, nodes in tree.items():
                    for node in nodes[:k//2]:  # Metade de cada nível
                        if isinstance(node, dict) and 'summary' in node:
                            results.append({
                                'text': node['summary'],
                                'source': f'RAPTOR_{level}',
                                'meta': {'level': level, 'method': 'raptor'},
                                'score': 0.8  # Score base para RAPTOR
                            })
            
            # 3. Busca na base de conhecimento
            for doc in self._knowledge_base:
                # Calcular relevância simples (overlap de palavras)
                query_words = set(expanded_query.lower().split())
                doc_words = set(doc['content'].lower().split())
                overlap = len(query_words & doc_words)
                
                if overlap > 0:
                    score = min(overlap / len(query_words), 1.0)
                    results.append({
                        'text': doc['content'][:500],  # Primeiros 500 chars
                        'source': doc['source'],
                        'meta': doc.get('meta', {}),
                        'score': score
                    })
            
            # 4. Auto-avaliação com Self-RAG se disponível
            if self.self_rag and results:
                for result in results:
                    eval_score = self.self_rag.evaluate_retrieval(
                        query, 
                        result['text'], 
                        "relevance"
                    )
                    # Ajustar score baseado na auto-avaliação
                    result['score'] = (result['score'] + eval_score) / 2
            
            # 5. Ordenar por score e retornar top-k
            results.sort(key=lambda x: x['score'], reverse=True)
            results = results[:k]
            
            # Adicionar citação formatada
            for i, result in enumerate(results):
                result['citation'] = self.cite(result)
                result['rank'] = i + 1
            
            # Cache resultado
            self._cache[cache_key] = results
            
        except Exception as e:
            logger.error(f"Erro em retrieve: {e}")
            # Retornar resultado stub em caso de erro
            results = self._stub_retrieve(query, k)
        
        return results
    
    def _stub_retrieve(self, query: str, k: int) -> List[Dict]:
        """
        Recuperação stub quando RAG real não está disponível.
        
        Args:
            query: Query de busca
            k: Número de resultados
            
        Returns:
            Resultados stub
        """
        stub_results = []
        
        # Gerar resultados baseados na query
        topics = {
            'estrutura': "A estrutura de três atos é fundamental. Setup (25%), Confrontação (50%), Resolução (25%).",
            'personagem': "Personagens precisam de objetivos claros, conflitos e arcos de transformação.",
            'diálogo': "Diálogos devem ter subtexto, economia e voz única para cada personagem.",
            'tema': "O tema deve permear toda a narrativa sem ser didático ou óbvio.",
            'visual': "Escreva visualmente com descrições econômicas mas evocativas.",
            'conflito': "Conflito é o motor da narrativa, podendo ser interno, externo ou ambos."
        }
        
        # Encontrar tópicos relevantes
        query_lower = query.lower()
        for topic, content in topics.items():
            if topic in query_lower or any(word in query_lower for word in topic.split()):
                stub_results.append({
                    'text': content,
                    'source': f'{topic}_manual.pdf',
                    'meta': {'type': 'stub', 'topic': topic},
                    'score': 0.7,
                    'rank': len(stub_results) + 1
                })
        
        # Adicionar resultado genérico se necessário
        if not stub_results:
            stub_results.append({
                'text': f"Informação sobre '{query[:50]}' seria encontrada em manuais de roteiro profissionais.",
                'source': 'generic_manual.pdf',
                'meta': {'type': 'stub'},
                'score': 0.5,
                'rank': 1
            })
        
        # Adicionar citações
        for result in stub_results:
            result['citation'] = self.cite(result)
        
        return stub_results[:k]
    
    def cite(self, snippet: Dict) -> str:
        """
        Formata citação para um snippet recuperado.
        
        Args:
            snippet: Dicionário com informações do documento
            
        Returns:
            String de citação formatada
        """
        source = snippet.get('source', 'Unknown')
        rank = snippet.get('rank', 0)
        score = snippet.get('score', 0)
        meta = snippet.get('meta', {})
        
        # Remover extensão se for arquivo
        if source.endswith('.pdf'):
            source = source[:-4]
        
        # Formatar citação
        citation_parts = [f"[{rank}]"]
        
        if source:
            citation_parts.append(source)
        
        if meta.get('pages'):
            citation_parts.append(f"p.{meta['pages']}")
        
        if meta.get('author'):
            citation_parts.append(f"por {meta['author']}")
        
        citation_parts.append(f"(relevância: {score:.1%})")
        
        return " ".join(citation_parts)
    
    def rerank(self, results: List[Dict], query: str = None) -> List[Dict]:
        """
        Re-rankeia resultados usando critérios avançados.
        
        Args:
            results: Lista de resultados
            query: Query original (opcional)
            
        Returns:
            Lista re-rankeada
        """
        if not results:
            return results
        
        # Re-rankear por score composto
        for result in results:
            # Boost por tipo de fonte
            if 'pdf' in result.get('source', '').lower():
                result['score'] *= 1.1
            
            # Boost por método
            meta = result.get('meta', {})
            if meta.get('method') == 'raptor':
                result['score'] *= 1.2
            elif meta.get('method') == 'hyde':
                result['score'] *= 1.15
            
            # Normalizar score
            result['score'] = min(result['score'], 1.0)
        
        # Ordenar novamente
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Atualizar ranks
        for i, result in enumerate(results):
            result['rank'] = i + 1
            result['citation'] = self.cite(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do sistema RAG.
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            'enabled': self.enabled,
            'provider': self.provider,
            'rag_modules': {
                'hyde': self.hyde is not None,
                'raptor': self.raptor is not None,
                'self_rag': self.self_rag is not None
            },
            'knowledge_base_size': len(self._knowledge_base),
            'cache_size': len(self._cache),
            'default_k': self.k
        }


def retrieve(query: str, k: int = 8) -> List[Dict]:
    """
    Função conveniente para recuperação RAG.
    
    Args:
        query: Query de busca
        k: Número de resultados
        
    Returns:
        Lista de documentos relevantes
    """
    adapter = RAGAdapter()
    return adapter.retrieve(query, k)


def cite(snippet: Dict) -> str:
    """
    Função conveniente para citação.
    
    Args:
        snippet: Snippet para citar
        
    Returns:
        Citação formatada
    """
    adapter = RAGAdapter()
    return adapter.cite(snippet)