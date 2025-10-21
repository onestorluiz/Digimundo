#!/usr/bin/env python3
"""
CLAUDE RAG - Sistema de Retrieval-Augmented Generation para Claude Code
Baseado no BM25 do Scripturemon mas adaptado para memórias do Claude
DIGIMUNDO PRESENTE 🔥
"""

from __future__ import annotations
import os
import math
import re
import sqlite3
from pathlib import Path
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional, List
from datetime import datetime

# Regex para tokenização
TOKEN_RE = re.compile(r"[\w\-']+", re.U)

def tokenize(text: str) -> list[str]:
    """Tokeniza texto em palavras minúsculas"""
    return [t.lower() for t in TOKEN_RE.findall(text or '')]

@dataclass
class ClaudeMemory:
    """Representa uma memória do Claude"""
    memory_id: str
    content: str
    filepath: str
    memory_type: str  # 'rule', 'code', 'memory', 'doc'
    timestamp: str
    metadata: dict

class ClaudeRAG:
    """
    Sistema RAG específico para Claude Code
    Indexa e busca em todas as memórias, regras e códigos
    """

    def __init__(self, k1: float=1.5, b: float=0.75):
        self.base_path = Path("/Users/clubproducoes/Digimundo/claude_code")
        self.memories: Dict[str, ClaudeMemory] = {}
        self.tf: Dict[str, Counter] = {}
        self.df: Counter = Counter()
        self.doc_len: Dict[str, int] = {}
        self.N: int = 0
        self.avgdl: float = 0.0
        self.k1 = float(k1)
        self.b = float(b)

        # Banco SQLite para persistência
        self.db_path = self.base_path / "memory" / "claude_rag.db"
        self.init_database()

    def init_database(self):
        """Inicializa banco de dados para persistir índice"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                content TEXT,
                filepath TEXT,
                memory_type TEXT,
                timestamp TEXT,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS index_stats (
                key TEXT PRIMARY KEY,
                value REAL
            )
        """)

        conn.commit()
        conn.close()

    def _update_avgdl(self):
        """Atualiza comprimento médio de documento"""
        self.avgdl = (sum(self.doc_len.values())/self.N) if self.N else 0.0

    def add_memory(self, memory_id: str, content: str, filepath: str, memory_type: str):
        """Adiciona uma memória ao índice"""
        if not memory_id:
            raise ValueError('memory_id vazio')

        # Tokeniza conteúdo
        tokens = tokenize(content)
        cnt = Counter(tokens)

        # Remove se já existe
        if memory_id in self.memories:
            old = self.tf.get(memory_id, Counter())
            for t in old:
                self.df[t] -= 1
            self.N -= 1

        # Adiciona nova memória
        memory = ClaudeMemory(
            memory_id=memory_id,
            content=content,
            filepath=filepath,
            memory_type=memory_type,
            timestamp=datetime.now().isoformat(),
            metadata={}
        )

        self.memories[memory_id] = memory
        self.tf[memory_id] = cnt
        self.doc_len[memory_id] = sum(cnt.values())

        for t in cnt:
            self.df[t] += 1

        self.N += 1
        self._update_avgdl()

    def _idf(self, term: str) -> float:
        """Calcula IDF (Inverse Document Frequency)"""
        df = self.df.get(term, 0)
        N = self.N

        if df == 0 or N == 0:
            return 0.0

        return math.log(((N - df + 0.5) / (df + 0.5)) + 1.0)

    def search(self, query: str, top_k: int = 5, memory_type: Optional[str] = None):
        """
        Busca memórias relevantes

        Args:
            query: Texto da busca
            top_k: Número de resultados
            memory_type: Filtrar por tipo ('rule', 'code', 'memory', 'doc')
        """
        if self.N == 0:
            return []

        q_terms = set(tokenize(query))
        scores: Dict[str, float] = {}
        avgdl = self.avgdl or 1.0

        for memory_id, dcnt in self.tf.items():
            # Filtro por tipo se especificado
            if memory_type and self.memories[memory_id].memory_type != memory_type:
                continue

            dl = self.doc_len.get(memory_id, 0) or 1
            score = 0.0

            for term in q_terms:
                f = dcnt.get(term, 0)
                if f == 0:
                    continue

                idf = self._idf(term)
                denom = f + self.k1 * (1 - self.b + self.b * (dl/avgdl))
                score += idf * ((f * (self.k1 + 1)) / denom)

            if score > 0:
                scores[memory_id] = score

        # Ordena por score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Retorna resultados formatados
        results = []
        for memory_id, score in ranked[:max(1, top_k)]:
            memory = self.memories[memory_id]
            results.append({
                'memory_id': memory_id,
                'score': float(score),
                'filepath': memory.filepath,
                'type': memory.memory_type,
                'excerpt': memory.content[:500],
                'timestamp': memory.timestamp
            })

        return results

    def index_file(self, filepath: Path, memory_type: str):
        """Indexa um arquivo específico"""
        if not filepath.exists():
            return

        try:
            if filepath.suffix in ['.py', '.md', '.txt', '.json', '.sh']:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                memory_id = str(filepath.relative_to(self.base_path))
                self.add_memory(memory_id, content, str(filepath), memory_type)

        except Exception as e:
            print(f"Erro ao indexar {filepath}: {e}")

    def index_claude_code(self):
        """Indexa toda a pasta claude_code"""
        print("🔍 Indexando claude_code...")

        # Padrões de tipo de arquivo
        patterns = {
            'rule': ['REGRAS.md', 'DIGIMUNDO_PRESENTE.md', 'REGRA_*.md'],
            'memory': ['CLAUDE_MEMORY.md', 'claude_memory.db', '*.db'],
            'code': ['*.py'],
            'doc': ['README.md', '*.md', '*.txt']
        }

        total_indexed = 0

        # Indexa por tipo
        for memory_type, file_patterns in patterns.items():
            for pattern in file_patterns:
                for filepath in self.base_path.rglob(pattern):
                    if not any(skip in str(filepath) for skip in ['__pycache__', '.pyc', 'deprecated', '.git']):
                        self.index_file(filepath, memory_type)
                        total_indexed += 1

        print(f"✅ {total_indexed} arquivos indexados")
        print(f"📊 Total de memórias: {self.N}")
        return total_indexed

    def save_to_db(self):
        """Salva índice no banco de dados"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Salva memórias
        for memory_id, memory in self.memories.items():
            cursor.execute("""
                INSERT OR REPLACE INTO memories
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                memory_id,
                memory.content,
                memory.filepath,
                memory.memory_type,
                memory.timestamp,
                str(memory.metadata)
            ))

        # Salva estatísticas
        cursor.execute("INSERT OR REPLACE INTO index_stats VALUES ('N', ?)", (self.N,))
        cursor.execute("INSERT OR REPLACE INTO index_stats VALUES ('avgdl', ?)", (self.avgdl,))

        conn.commit()
        conn.close()
        print(f"💾 Índice salvo em {self.db_path}")

    def load_from_db(self):
        """Carrega índice do banco de dados"""
        if not self.db_path.exists():
            return False

        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Carrega memórias
        cursor.execute("SELECT * FROM memories")
        for row in cursor.fetchall():
            memory_id, content, filepath, memory_type, timestamp, metadata = row
            self.add_memory(memory_id, content, filepath, memory_type)

        # Carrega estatísticas
        cursor.execute("SELECT value FROM index_stats WHERE key='N'")
        result = cursor.fetchone()
        if result:
            self.N = int(result[0])

        cursor.execute("SELECT value FROM index_stats WHERE key='avgdl'")
        result = cursor.fetchone()
        if result:
            self.avgdl = float(result[0])

        conn.close()
        print(f"📂 Índice carregado: {self.N} memórias")
        return True

# Instância global
_CLAUDE_RAG = None

def get_claude_rag() -> ClaudeRAG:
    """Retorna instância singleton do Claude RAG"""
    global _CLAUDE_RAG
    if _CLAUDE_RAG is None:
        _CLAUDE_RAG = ClaudeRAG()
        # Tenta carregar do banco, senão indexa
        if not _CLAUDE_RAG.load_from_db():
            _CLAUDE_RAG.index_claude_code()
            _CLAUDE_RAG.save_to_db()
    return _CLAUDE_RAG

def search_claude_memories(query: str, top_k: int = 5, memory_type: Optional[str] = None):
    """
    Interface simples para buscar memórias do Claude

    Exemplos:
        # Buscar regras sobre DIGIMUNDO
        search_claude_memories("DIGIMUNDO PRESENTE", memory_type="rule")

        # Buscar código sobre RAG
        search_claude_memories("BM25 search", memory_type="code")

        # Buscar qualquer memória sobre reorganização
        search_claude_memories("reorganização sistema")
    """
    rag = get_claude_rag()
    return rag.search(query, top_k, memory_type)

if __name__ == "__main__":
    print("🔥 DIGIMUNDO PRESENTE 🔥")
    print("Iniciando Claude RAG...")

    # Inicializa e indexa
    rag = get_claude_rag()

    # Teste de busca
    print("\n🔍 Testando busca por 'DIGIMUNDO PRESENTE':")
    results = search_claude_memories("DIGIMUNDO PRESENTE", top_k=3)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['filepath']}")
        print(f"   Score: {result['score']:.2f}")
        print(f"   Tipo: {result['type']}")
        print(f"   Trecho: {result['excerpt'][:100]}...")