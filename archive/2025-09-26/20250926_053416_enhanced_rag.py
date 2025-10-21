#!/usr/bin/env python3
"""
Enhanced RAG System with Screenplay Integration
Acessa tanto memórias antigas quanto roteiros famosos
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import BM25 for fast search
from scripturemon_champion.core.rag_bm25 import BM25Index

class EnhancedRAG:
    """RAG com acesso a memórias E roteiros famosos"""

    def __init__(self, db_path: str = None):
        """Inicializa com acesso completo"""
        if db_path is None:
            db_path = "data/unified_memory.db"

        self.db_path = Path(db_path)
        self.bm25_index = BM25Index()

        # Conectar ao banco
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            print(f"✅ RAG Conectado: {self.db_path}")

            # Carregar índice de roteiros se existir
            index_path = Path("data/screenplay_index.json")
            if index_path.exists():
                self._load_screenplay_index(index_path)

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.conn = None

    def _load_screenplay_index(self, index_path: Path):
        """Carrega o índice BM25 dos roteiros"""
        try:
            with open(index_path, 'r') as f:
                data = json.load(f)

            # Reconstruir índice
            for doc_id, doc_data in data['docs'].items():
                self.bm25_index.add(
                    doc_id,
                    doc_data['text'],
                    doc_data['metadata']
                )

            print(f"📚 Carregados {self.bm25_index.N} roteiros no índice BM25")

        except Exception as e:
            print(f"⚠️ Erro ao carregar índice: {e}")

    def search_all(self, query: str, limit: int = 10) -> Dict:
        """
        Busca em TODAS as fontes:
        - Memórias antigas (unified_memory)
        - Roteiros famosos (screenplay_memories)
        - Índice BM25 para busca rápida
        """
        results = {
            'memories': [],
            'screenplays': [],
            'bm25_matches': []
        }

        if not self.conn:
            return results

        try:
            cursor = self.conn.cursor()

            # 1. Buscar nas memórias antigas
            keywords = query.lower().split()[:5]
            conditions = " OR ".join([f"LOWER(value) LIKE ?" for _ in keywords])
            params = [f"%{kw}%" for kw in keywords]

            sql_memories = f"""
                SELECT key, value, confidence, source
                FROM unified_memory
                WHERE {conditions}
                ORDER BY confidence DESC
                LIMIT ?
            """
            params.append(limit)

            cursor.execute(sql_memories, params)
            for row in cursor.fetchall():
                results['memories'].append(dict(row))

            # 2. Buscar nos roteiros famosos
            sql_screenplays = f"""
                SELECT title, content, metadata
                FROM screenplay_memories
                WHERE {conditions}
                ORDER BY id DESC
                LIMIT ?
            """

            cursor.execute(sql_screenplays, params)
            for row in cursor.fetchall():
                results['screenplays'].append({
                    'title': row['title'],
                    'content': row['content'][:500],  # Primeiros 500 chars
                    'metadata': json.loads(row['metadata']) if row['metadata'] else {}
                })

            # 3. Busca BM25 (mais precisa)
            bm25_results = self.bm25_index.search(query, top_k=5)
            for doc_id, score in bm25_results:
                doc = self.bm25_index.docs[doc_id]
                results['bm25_matches'].append({
                    'doc_id': doc_id,
                    'score': score,
                    'title': doc.metadata.get('title', 'Unknown'),
                    'type': doc.metadata.get('type', 'unknown')
                })

            # Estatísticas
            print(f"🔍 Busca '{query}':")
            print(f"   - {len(results['memories'])} memórias antigas")
            print(f"   - {len(results['screenplays'])} roteiros famosos")
            print(f"   - {len(results['bm25_matches'])} matches BM25")

        except Exception as e:
            print(f"❌ Erro na busca: {e}")

        return results

    def get_similar_examples(self, scene_type: str) -> List[Dict]:
        """
        Busca exemplos similares nos roteiros famosos

        Args:
            scene_type: Tipo de cena (dialogue, action, tension, etc.)

        Returns:
            Lista de exemplos dos roteiros famosos
        """
        examples = []

        # Mapear tipos para queries
        query_map = {
            'dialogue': 'character dialogue conversation',
            'action': 'explosion chase fight battle',
            'tension': 'suspense fear anticipation',
            'opening': 'fade in opening scene first',
            'climax': 'final battle climactic moment',
            'twist': 'revelation surprise plot twist'
        }

        query = query_map.get(scene_type, scene_type)
        results = self.search_all(query, limit=5)

        # Priorizar roteiros famosos
        for screenplay in results['screenplays']:
            examples.append({
                'source': screenplay['title'],
                'example': screenplay['content'],
                'type': 'screenplay'
            })

        # Adicionar matches BM25
        for match in results['bm25_matches']:
            if match['type'] == 'master_screenplay':
                examples.append({
                    'source': match['title'],
                    'score': match['score'],
                    'type': 'bm25_match'
                })

        return examples[:5]  # Top 5 exemplos

    def get_theory_reference(self, author: str) -> Optional[str]:
        """
        Busca referências teóricas de um autor específico

        Args:
            author: Nome do teórico (McKee, Field, Snyder, etc.)

        Returns:
            Texto relevante do autor ou None
        """
        results = self.search_all(author, limit=3)

        # Priorizar conteúdo teórico
        for screenplay in results['screenplays']:
            meta = screenplay.get('metadata', {})
            if 'theory' in str(meta).lower() or author.lower() in str(meta).lower():
                return screenplay['content']

        # Fallback para memórias
        if results['memories']:
            return results['memories'][0].get('value', '')

        return None

# Teste rápido
if __name__ == "__main__":
    rag = EnhancedRAG()

    print("\n🧪 TESTE DO SISTEMA ENHANCED RAG")
    print("=" * 50)

    # Teste 1: Buscar diálogos
    print("\n1. Buscando exemplos de diálogo...")
    dialogues = rag.get_similar_examples('dialogue')
    for d in dialogues[:2]:
        print(f"   - {d['source']}: {d.get('example', '')[:100]}...")

    # Teste 2: Buscar teoria
    print("\n2. Buscando teoria de McKee...")
    mckee = rag.get_theory_reference('McKee')
    if mckee:
        print(f"   Encontrado: {mckee[:200]}...")

    # Teste 3: Busca geral
    print("\n3. Busca geral por 'inception'...")
    results = rag.search_all("inception dream", limit=3)
    print(f"   Total de resultados: {sum(len(v) for v in results.values())}")

    print("\n✅ Sistema Enhanced RAG funcionando!")