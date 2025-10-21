#!/usr/bin/env python3
"""
Sistema RAG Simples e Seguro para Unified Memory
Sem dependências complexas, apenas SQLite
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class SimpleRAG:
    """RAG minimalista sem dependências externas"""

    def __init__(self, db_path: str = None):
        """Inicializa com fallbacks seguros"""
        if db_path is None:
            db_path = "data/unified_memory.db"

        self.db_path = Path(db_path)

        # Verificar se banco existe
        if not self.db_path.exists():
            print(f"⚠️ Banco não encontrado em {self.db_path}")
            print("   Criando banco novo...")
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # Retorna dicts
            print(f"✅ Conectado ao banco: {self.db_path}")
            self._ensure_tables()
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            self.conn = None

    def _ensure_tables(self):
        """Garante que tabelas existem"""
        cursor = self.conn.cursor()

        # Verificar se tabela unified_memory existe
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='unified_memory'
        """)

        if not cursor.fetchone():
            print("📦 Criando tabela unified_memory...")
            cursor.execute("""
                CREATE TABLE unified_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    metadata TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    source TEXT DEFAULT 'rag_integration'
                )
            """)
            cursor.execute("""
                CREATE INDEX idx_content ON unified_memory(content);
            """)
            self.conn.commit()

    def search_similar(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca memórias similares usando LIKE (não precisa embeddings)"""
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()

            # Extrair palavras-chave da query
            keywords = query.lower().split()[:5]  # Primeiras 5 palavras

            # Busca no campo 'value' que contém o conteúdo real
            conditions = " OR ".join([f"LOWER(value) LIKE ?" for _ in keywords])
            params = [f"%{kw}%" for kw in keywords]

            sql = f"""
                SELECT id, type, key, value, confidence, metadata, timestamp
                FROM unified_memory
                WHERE {conditions}
                ORDER BY confidence DESC, timestamp DESC
                LIMIT ?
            """
            params.append(limit)

            results = cursor.execute(sql, params).fetchall()

            return [
                {
                    "id": r["id"],
                    "type": r["type"],
                    "key": r["key"],
                    "content": r["value"],  # 'value' contém o conteúdo
                    "confidence": r["confidence"],
                    "metadata": json.loads(r["metadata"]) if r["metadata"] else {},
                    "timestamp": r["timestamp"]
                }
                for r in results
            ]

        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return []

    def save_analysis(self, content: str, metadata: Optional[Dict] = None, confidence: float = 0.5):
        """Salva nova análise no banco"""
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()

            # Gerar ID único
            import hashlib
            unique_id = hashlib.md5(f"{content[:100]}{datetime.now()}".encode()).hexdigest()[:16]

            metadata_json = json.dumps(metadata) if metadata else None

            # Adaptar para estrutura real: id, type, key, value
            cursor.execute("""
                INSERT INTO unified_memory (id, type, key, value, metadata, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                unique_id,
                metadata.get('type', 'analysis') if metadata else 'analysis',
                metadata.get('key', 'screenplay_analysis') if metadata else 'screenplay_analysis',
                content,  # 'value' contém o conteúdo
                metadata_json,
                confidence,
                datetime.now().isoformat()
            ))

            self.conn.commit()
            print(f"✅ Análise salva (id: {unique_id}, confidence: {confidence})")
            return True

        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False

    def get_stats(self) -> Dict:
        """Retorna estatísticas do banco"""
        if not self.conn:
            return {"status": "disconnected"}

        try:
            cursor = self.conn.cursor()

            total = cursor.execute("SELECT COUNT(*) FROM unified_memory").fetchone()[0]
            avg_conf = cursor.execute("SELECT AVG(confidence) FROM unified_memory").fetchone()[0]

            return {
                "status": "connected",
                "total_memories": total,
                "average_confidence": round(avg_conf, 2) if avg_conf else 0,
                "db_path": str(self.db_path)
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def close(self):
        """Fecha conexão com banco"""
        if self.conn:
            self.conn.close()
            print("🔒 Conexão fechada")


# Teste rápido se executado diretamente
if __name__ == "__main__":
    print("\n🧪 TESTE DO SISTEMA RAG\n")

    # Criar instância
    rag = SimpleRAG()

    # Mostrar stats
    stats = rag.get_stats()
    print(f"📊 Status: {stats}")

    # Fazer busca teste
    print("\n🔍 Busca teste por 'screenplay':")
    results = rag.search_similar("screenplay analysis", limit=3)
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['content'][:100]}...")

    # Salvar teste
    print("\n💾 Salvando análise teste...")
    rag.save_analysis(
        content="Teste de análise RAG integrado",
        metadata={"type": "test", "source": "rag_integration"},
        confidence=0.8
    )

    # Fechar
    rag.close()

    print("\n✅ Teste concluído!")
    print("DIGIMUNDO PRESENTE 🥷")