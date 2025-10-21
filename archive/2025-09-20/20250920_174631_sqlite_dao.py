"""
SQLite DAO para gerenciamento de memórias.
CRUD completo e busca básica por LIKE.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class MemoryDAO:
    """Data Access Object para memórias SQLite."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa o DAO.

        Args:
            db_path: Caminho para o banco SQLite. Se None, usa padrão.
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / 'data' / 'memory' / 'mem.db'

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Criar conexão
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        # Configure pragmas for performance
        self._configure_pragmas()

        # Garantir que tabela existe
        self._ensure_table()

    def _configure_pragmas(self):
        """Configure SQLite for optimal performance and reliability"""
        try:
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")
            self.conn.execute("PRAGMA foreign_keys=ON")
            self.conn.execute("PRAGMA cache_size=10000")
            self.conn.execute("PRAGMA temp_store=MEMORY")
        except Exception as e:
            print(f"Failed to set SQLite pragmas: {e}")

    def _ensure_table(self):
        """Garante que a tabela memories existe com estrutura correta."""
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                tags TEXT,
                importance REAL DEFAULT 0.5,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_accessed TEXT DEFAULT CURRENT_TIMESTAMP,
                hits INTEGER DEFAULT 0,
                kind TEXT DEFAULT 'L3' CHECK(kind IN ('L1', 'L2', 'L3', 'L4'))
            )
        ''')

        # Criar índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_kind ON memories(kind)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_last_accessed ON memories(last_accessed)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hits ON memories(hits)')

        self.conn.commit()

    # === CRUD Operations ===

    def create(self, id: str, content: str, tags: Optional[List[str]] = None,
               importance: float = 0.5, kind: str = 'L3') -> bool:
        """
        Cria uma nova memória.

        Args:
            id: ID único da memória
            content: Conteúdo da memória
            tags: Lista de tags (será convertida para JSON)
            importance: Importância (0-1)
            kind: Tipo da memória (L1, L2, L3, L4)

        Returns:
            True se criado com sucesso
        """
        try:
            cursor = self.conn.cursor()

            tags_json = json.dumps(tags) if tags else None
            now = datetime.now().isoformat()

            cursor.execute('''
                INSERT INTO memories (id, content, tags, importance, created_at, last_accessed, kind)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (id, content, tags_json, importance, now, now, kind))

            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            # ID já existe
            return False
        except Exception as e:
            print(f"Erro ao criar memória: {e}")
            return False

    def read(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Lê uma memória por ID.

        Args:
            id: ID da memória

        Returns:
            Dict com dados da memória ou None se não existir
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM memories WHERE id = ?', (id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_dict(row)
        return None

    def update(self, id: str, **kwargs) -> bool:
        """
        Atualiza campos de uma memória.

        Args:
            id: ID da memória
            **kwargs: Campos a atualizar (content, tags, importance, kind, etc)

        Returns:
            True se atualizado com sucesso
        """
        if not kwargs:
            return False

        # Construir query UPDATE dinamicamente
        valid_fields = ['content', 'tags', 'importance', 'kind', 'hits', 'last_accessed']
        fields_to_update = []
        values = []

        for field, value in kwargs.items():
            if field in valid_fields:
                fields_to_update.append(f'{field} = ?')

                # Converter tags para JSON se necessário
                if field == 'tags' and isinstance(value, list):
                    value = json.dumps(value)

                values.append(value)

        if not fields_to_update:
            return False

        values.append(id)  # Para WHERE clause

        try:
            cursor = self.conn.cursor()
            query = f"UPDATE memories SET {', '.join(fields_to_update)} WHERE id = ?"
            cursor.execute(query, values)
            self.conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Erro ao atualizar memória: {e}")
            return False

    def delete(self, id: str) -> bool:
        """
        Remove uma memória.

        Args:
            id: ID da memória

        Returns:
            True se removido com sucesso
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM memories WHERE id = ?', (id,))
        self.conn.commit()

        return cursor.rowcount > 0

    # === Search Operations ===

    def search_by_content(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca memórias por conteúdo usando LIKE.

        Args:
            query: String de busca
            limit: Número máximo de resultados

        Returns:
            Lista de memórias encontradas
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC, last_accessed DESC
            LIMIT ?
        ''', (f'%{query}%', limit))

        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def get_by_kind(self, kind: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca memórias por tipo (L1, L2, L3, L4).

        Args:
            kind: Tipo da memória
            limit: Limite de resultados (None = sem limite)

        Returns:
            Lista de memórias do tipo especificado
        """
        cursor = self.conn.cursor()

        if limit:
            cursor.execute('''
                SELECT * FROM memories
                WHERE kind = ?
                ORDER BY importance DESC, last_accessed DESC
                LIMIT ?
            ''', (kind, limit))
        else:
            cursor.execute('''
                SELECT * FROM memories
                WHERE kind = ?
                ORDER BY importance DESC, last_accessed DESC
            ''', (kind,))

        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca memórias que contenham qualquer uma das tags.

        Args:
            tags: Lista de tags para buscar
            limit: Número máximo de resultados

        Returns:
            Lista de memórias com as tags
        """
        if not tags:
            return []

        cursor = self.conn.cursor()

        # Construir query com múltiplos LIKE para tags JSON
        tag_conditions = ' OR '.join(['tags LIKE ?' for _ in tags])
        tag_values = [f'%"{tag}"%' for tag in tags]

        query = f'''
            SELECT * FROM memories
            WHERE {tag_conditions}
            ORDER BY importance DESC, last_accessed DESC
            LIMIT ?
        '''

        cursor.execute(query, tag_values + [limit])

        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def search_memories(self, query: str, limit: int = 10):
        """
        Legacy search method for compatibility.
        Returns raw tuples instead of dicts.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, content, created_at, last_accessed, importance, hits, kind, tags
            FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC, last_accessed DESC
            LIMIT ?
        ''', (f'%{query}%', limit))

        return cursor.fetchall()

    def get_memory(self, mem_id: str):
        """
        Legacy get method for compatibility.
        Returns raw tuple instead of dict.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, content, created_at, last_accessed, importance, hits, kind, tags
            FROM memories WHERE id = ?
        ''', (mem_id,))

        return cursor.fetchone()

    # === Utility Operations ===

    def increment_hits(self, id: str) -> bool:
        """
        Incrementa o contador de hits e atualiza last_accessed.

        Args:
            id: ID da memória

        Returns:
            True se incrementado com sucesso
        """
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        cursor.execute('''
            UPDATE memories
            SET hits = hits + 1, last_accessed = ?
            WHERE id = ?
        ''', (now, id))

        self.conn.commit()
        return cursor.rowcount > 0

    def promote(self, id: str, new_kind: str) -> bool:
        """
        Promove uma memória para outro nível.

        Args:
            id: ID da memória
            new_kind: Novo tipo (L1, L2, L3, L4)

        Returns:
            True se promovido com sucesso
        """
        return self.update(id, kind=new_kind, last_accessed=datetime.now().isoformat())

    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas do banco de memórias.

        Returns:
            Dict com estatísticas
        """
        cursor = self.conn.cursor()

        # Total por tipo
        cursor.execute('''
            SELECT kind, COUNT(*) as count
            FROM memories
            GROUP BY kind
        ''')

        kind_counts = {row['kind']: row['count'] for row in cursor.fetchall()}

        # Total geral
        cursor.execute('SELECT COUNT(*) as total FROM memories')
        total = cursor.fetchone()['total']

        # Média de hits e importance
        cursor.execute('''
            SELECT
                AVG(hits) as avg_hits,
                AVG(importance) as avg_importance
            FROM memories
        ''')

        row = cursor.fetchone()

        return {
            'total': total,
            'by_kind': kind_counts,
            'avg_hits': row['avg_hits'] or 0,
            'avg_importance': row['avg_importance'] or 0
        }

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Converte uma linha SQLite em dicionário."""
        result = dict(row)

        # Parse tags JSON
        if result.get('tags'):
            try:
                result['tags'] = json.loads(result['tags'])
            except:
                result['tags'] = []
        else:
            result['tags'] = []

        return result

    def close(self):
        """Fecha a conexão com o banco."""
        if self.conn:
            self.conn.close()