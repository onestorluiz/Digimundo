#!/usr/bin/env python3
"""
🧬 COGNITIVE CORE - Núcleo de Memória do Digimundo
Implementa ChromaDB para memória vetorial com <100ms de recall
"""

import chromadb
from chromadb.config import Settings
import sqlite3
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import numpy as np

class CognitiveCore:
    """
    Interface principal para memória híbrida:
    - ChromaDB: Memória vetorial compartilhada
    - SQLite: Memória individual de cada Digimon
    - Cache L1/L2: Resposta <100ms
    """
    
    def __init__(self, digimon_name: str = "collective"):
        self.digimon_name = digimon_name
        self.base_path = Path("/Users/clubproducoes/Digimundo/core/memory")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Inicializar ChromaDB (memória vetorial)
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.base_path / "chromadb"),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Collection para memória coletiva
        self.collective_memory = self._get_or_create_collection("collective_memory")
        
        # Collection para memória individual se não for collective
        self.personal_memory = None
        if digimon_name != "collective":
            self.personal_memory = self._get_or_create_collection(f"{digimon_name}_memory")
        
        # SQLite para memória estruturada individual
        self.db_path = self.base_path / f"{digimon_name}.db"
        self._init_sqlite()
        
        # Cache L1 (em memória) para <100ms
        self.cache_l1: Dict[str, Tuple[Any, float]] = {}
        self.cache_l1_ttl = 300  # 5 minutos
        
        # Cache L2 (SQLite) para persistência
        self._init_cache_l2()
        
        # Métricas de performance
        self.metrics = {
            "recalls": 0,
            "avg_recall_time": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
    
    def _get_or_create_collection(self, name: str):
        """Cria ou obtém uma collection ChromaDB"""
        try:
            return self.chroma_client.get_collection(name)
        except:
            return self.chroma_client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def _init_sqlite(self):
        """Inicializa banco SQLite para memória estruturada"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de memórias episódicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                context TEXT,
                content TEXT,
                importance REAL,
                emotion TEXT,
                tags TEXT
            )
        """)
        
        # Tabela de memórias semânticas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT UNIQUE,
                definition TEXT,
                relations TEXT,
                confidence REAL,
                last_updated REAL
            )
        """)
        
        # Tabela de memórias procedurais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS procedural_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                steps TEXT,
                success_rate REAL,
                last_execution REAL,
                optimizations TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _init_cache_l2(self):
        """Inicializa cache L2 persistente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache_l2 (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp REAL,
                hits INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_memory(self, content: str, metadata: Dict = None, memory_type: str = "episodic") -> str:
        """
        Armazena uma nova memória
        
        Args:
            content: Conteúdo da memória
            metadata: Metadados adicionais
            memory_type: episodic, semantic, ou procedural
            
        Returns:
            ID da memória armazenada
        """
        timestamp = time.time()
        memory_id = hashlib.md5(f"{content}{timestamp}".encode()).hexdigest()
        
        # Armazenar no ChromaDB (vetorial)
        # ChromaDB não aceita listas/dicts nos metadados, converter para strings
        chroma_metadata = {}
        if metadata:
            for key, value in metadata.items():
                if isinstance(value, (list, dict)):
                    chroma_metadata[key] = json.dumps(value)
                else:
                    chroma_metadata[key] = value
        
        collection = self.personal_memory or self.collective_memory
        collection.add(
            documents=[content],
            metadatas=[chroma_metadata],
            ids=[memory_id]
        )
        
        # Armazenar no SQLite (estruturado)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if memory_type == "episodic":
            cursor.execute("""
                INSERT INTO episodic_memory (timestamp, content, context, importance, emotion, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                content,
                json.dumps(metadata or {}),
                metadata.get("importance", 0.5) if metadata else 0.5,
                metadata.get("emotion", "neutral") if metadata else "neutral",
                json.dumps(metadata.get("tags", []) if metadata else [])
            ))
        elif memory_type == "semantic":
            cursor.execute("""
                INSERT OR REPLACE INTO semantic_memory (concept, definition, relations, confidence, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (
                metadata.get("concept", content[:50]) if metadata else content[:50],
                content,
                json.dumps(metadata.get("relations", {}) if metadata else {}),
                metadata.get("confidence", 0.8) if metadata else 0.8,
                timestamp
            ))
        elif memory_type == "procedural":
            cursor.execute("""
                INSERT INTO procedural_memory (task, steps, success_rate, last_execution, optimizations)
                VALUES (?, ?, ?, ?, ?)
            """, (
                metadata.get("task", content[:50]) if metadata else content[:50],
                content,
                metadata.get("success_rate", 0.0) if metadata else 0.0,
                timestamp,
                json.dumps(metadata.get("optimizations", []) if metadata else [])
            ))
        
        conn.commit()
        conn.close()
        
        # Invalidar cache L1 relacionado
        self._invalidate_cache(content[:50])
        
        return memory_id
    
    def recall(self, query: str, top_k: int = 5, threshold: float = 0.7) -> List[Dict]:
        """
        Recupera memórias relevantes em <100ms
        
        Args:
            query: Query de busca
            top_k: Número máximo de resultados
            threshold: Threshold de relevância
            
        Returns:
            Lista de memórias relevantes
        """
        start_time = time.time()
        
        # Verificar cache L1
        cache_key = f"{query}:{top_k}:{threshold}"
        if cache_key in self.cache_l1:
            cached_value, cached_time = self.cache_l1[cache_key]
            if time.time() - cached_time < self.cache_l1_ttl:
                self.metrics["cache_hits"] += 1
                self._update_metrics(time.time() - start_time)
                return cached_value
        
        # Verificar cache L2
        cached = self._get_cache_l2(cache_key)
        if cached:
            self.cache_l1[cache_key] = (cached, time.time())
            self.metrics["cache_hits"] += 1
            self._update_metrics(time.time() - start_time)
            return cached
        
        self.metrics["cache_misses"] += 1
        
        # Buscar no ChromaDB
        collection = self.personal_memory or self.collective_memory
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Processar resultados
        memories = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if "distances" in results else 0
                similarity = 1 - distance  # Converter distância em similaridade
                
                if similarity >= threshold:
                    memories.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if "metadatas" in results else {},
                        "similarity": similarity,
                        "id": results["ids"][0][i] if "ids" in results else None
                    })
        
        # Buscar memórias estruturadas relacionadas
        structured_memories = self._search_structured(query, top_k)
        memories.extend(structured_memories)
        
        # Ordenar por relevância
        memories.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        memories = memories[:top_k]
        
        # Cachear resultado
        self.cache_l1[cache_key] = (memories, time.time())
        self._set_cache_l2(cache_key, memories)
        
        self._update_metrics(time.time() - start_time)
        return memories
    
    def _search_structured(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca em memórias estruturadas SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        memories = []
        
        # Buscar em memórias episódicas
        cursor.execute("""
            SELECT content, context, importance, emotion, tags
            FROM episodic_memory
            WHERE content LIKE ?
            ORDER BY timestamp DESC, importance DESC
            LIMIT ?
        """, (f"%{query}%", limit))
        
        for row in cursor.fetchall():
            memories.append({
                "content": row[0],
                "metadata": {
                    "context": json.loads(row[1]),
                    "importance": row[2],
                    "emotion": row[3],
                    "tags": json.loads(row[4]),
                    "type": "episodic"
                },
                "similarity": 0.8  # Estimativa
            })
        
        # Buscar em memórias semânticas
        cursor.execute("""
            SELECT concept, definition, relations, confidence
            FROM semantic_memory
            WHERE concept LIKE ? OR definition LIKE ?
            ORDER BY confidence DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))
        
        for row in cursor.fetchall():
            memories.append({
                "content": row[1],
                "metadata": {
                    "concept": row[0],
                    "relations": json.loads(row[2]),
                    "confidence": row[3],
                    "type": "semantic"
                },
                "similarity": row[3]
            })
        
        conn.close()
        return memories
    
    def _get_cache_l2(self, key: str) -> Optional[Any]:
        """Recupera do cache L2"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT value, timestamp FROM cache_l2
            WHERE key = ?
        """, (key,))
        
        row = cursor.fetchone()
        if row and time.time() - row[1] < 3600:  # 1 hora de TTL
            # Atualizar hits
            cursor.execute("UPDATE cache_l2 SET hits = hits + 1 WHERE key = ?", (key,))
            conn.commit()
            conn.close()
            return json.loads(row[0])
        
        conn.close()
        return None
    
    def _set_cache_l2(self, key: str, value: Any):
        """Armazena no cache L2"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO cache_l2 (key, value, timestamp, hits)
            VALUES (?, ?, ?, 0)
        """, (key, json.dumps(value), time.time()))
        
        conn.commit()
        conn.close()
    
    def _invalidate_cache(self, pattern: str):
        """Invalida cache relacionado a um padrão"""
        # Limpar cache L1
        keys_to_remove = [k for k in self.cache_l1 if pattern.lower() in k.lower()]
        for key in keys_to_remove:
            del self.cache_l1[key]
        
        # Limpar cache L2
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cache_l2 WHERE key LIKE ?", (f"%{pattern}%",))
        conn.commit()
        conn.close()
    
    def _update_metrics(self, recall_time: float):
        """Atualiza métricas de performance"""
        self.metrics["recalls"] += 1
        self.metrics["avg_recall_time"] = (
            (self.metrics["avg_recall_time"] * (self.metrics["recalls"] - 1) + recall_time)
            / self.metrics["recalls"]
        )
    
    def get_metrics(self) -> Dict:
        """Retorna métricas de performance"""
        total_requests = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_rate = (
            self.metrics["cache_hits"] / total_requests * 100
            if total_requests > 0 else 0
        )
        
        return {
            **self.metrics,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "avg_recall_time_ms": f"{self.metrics['avg_recall_time'] * 1000:.2f}ms",
            "target_time_ms": "100ms",
            "performance": "✅ OPTIMAL" if self.metrics['avg_recall_time'] < 0.1 else "⚠️ NEEDS OPTIMIZATION"
        }
    
    def share_with_collective(self, memory_id: str):
        """Compartilha memória pessoal com o coletivo"""
        if not self.personal_memory:
            return False
        
        # Buscar memória pessoal
        result = self.personal_memory.get(ids=[memory_id])
        
        if result and result["documents"]:
            # Adicionar ao coletivo
            self.collective_memory.add(
                documents=result["documents"],
                metadatas=result["metadatas"],
                ids=[f"shared_{memory_id}"]
            )
            return True
        
        return False
    
    def evolve_memory(self, feedback: Dict):
        """
        Evolui memórias baseado em feedback
        Ajusta importância, confiança e otimizações
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if feedback.get("type") == "episodic":
            cursor.execute("""
                UPDATE episodic_memory
                SET importance = importance * ?
                WHERE id = ?
            """, (feedback.get("importance_multiplier", 1.0), feedback.get("id")))
        
        elif feedback.get("type") == "semantic":
            cursor.execute("""
                UPDATE semantic_memory
                SET confidence = confidence * ?
                WHERE concept = ?
            """, (feedback.get("confidence_multiplier", 1.0), feedback.get("concept")))
        
        elif feedback.get("type") == "procedural":
            cursor.execute("""
                UPDATE procedural_memory
                SET success_rate = ?,
                    optimizations = ?
                WHERE task = ?
            """, (
                feedback.get("new_success_rate", 0.0),
                json.dumps(feedback.get("optimizations", [])),
                feedback.get("task")
            ))
        
        conn.commit()
        conn.close()
        
        # Invalidar caches relacionados
        self._invalidate_cache(feedback.get("query", ""))


if __name__ == "__main__":
    # Teste do Cognitive Core
    print("🧬 TESTANDO COGNITIVE CORE")
    print("=" * 50)
    
    # Inicializar para Sabiamon
    core = CognitiveCore("sabiamon")
    
    # Armazenar memórias
    print("\n📝 Armazenando memórias...")
    
    # Memória episódica
    id1 = core.store_memory(
        "Hoje aprendi sobre honestidade brutal e a importância de testes objetivos",
        {
            "importance": 0.9,
            "emotion": "enlightenment",
            "tags": ["aprendizado", "evolução", "valores"]
        },
        "episodic"
    )
    print(f"✅ Memória episódica: {id1}")
    
    # Memória semântica
    id2 = core.store_memory(
        "Digimundo é um ecossistema digital onde Digimons evoluem através de aprendizado contínuo",
        {
            "concept": "Digimundo",
            "relations": {"contains": ["Digimons", "Q-Com", "Memory"], "purpose": "evolution"},
            "confidence": 0.95
        },
        "semantic"
    )
    print(f"✅ Memória semântica: {id2}")
    
    # Memória procedural
    id3 = core.store_memory(
        "1. Receber pergunta\n2. Buscar contexto\n3. Processar com modelo\n4. Cachear resposta",
        {
            "task": "responder_pergunta",
            "success_rate": 0.98,
            "optimizations": ["cache L1", "batch processing"]
        },
        "procedural"
    )
    print(f"✅ Memória procedural: {id3}")
    
    # Testar recall
    print("\n🔍 Testando recall...")
    
    import time
    queries = [
        "honestidade brutal",
        "Digimundo",
        "responder pergunta",
        "evolução e aprendizado"
    ]
    
    for query in queries:
        start = time.time()
        memories = core.recall(query, top_k=3)
        elapsed = (time.time() - start) * 1000
        
        print(f"\nQuery: '{query}'")
        print(f"⏱️  Tempo: {elapsed:.2f}ms")
        print(f"📊 Resultados: {len(memories)}")
        
        for i, mem in enumerate(memories, 1):
            print(f"  {i}. {mem['content'][:60]}... (sim: {mem.get('similarity', 0):.2f})")
    
    # Métricas
    print("\n📈 MÉTRICAS DE PERFORMANCE")
    print("=" * 50)
    metrics = core.get_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    # Compartilhar com coletivo
    print(f"\n🌐 Compartilhando memória {id1} com coletivo...")
    if core.share_with_collective(id1):
        print("✅ Memória compartilhada com sucesso!")
    
    print("\n✨ Cognitive Core operacional!")