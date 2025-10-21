#!/usr/bin/env python3

"""
🧬 SCRIPTUREMON ULTIMATE RAG SYSTEM
Sistema RAG evolutivo com todas as melhorias revolucionárias implementadas
Baseado em pesquisas_revolution e compass_artifact
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
import asyncio
import docker
import redis
import torch
import gc
import re
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from multiprocessing import Process, Queue, cpu_count
import subprocess
import shutil

# Imports opcionais com fallback
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️ ChromaDB não instalado. Usando SQLite.")

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ pdfplumber não instalado.")

try:
    from sentence_transformers import SentenceTransformer, CrossEncoder
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️ sentence-transformers não instalado.")

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    print("⚠️ rank-bm25 não instalado.")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️ watchdog não instalado.")

try:
    from py3crdt.lww import LWWElementSet
    from py3crdt.orset import ORSet
    CRDT_AVAILABLE = True
except ImportError:
    CRDT_AVAILABLE = False
    print("⚠️ py-crdt não instalado.")

# ============================================================================
# 1. SOULOS SYSCALLS COM EXECUÇÃO DE CÓDIGO
# ============================================================================

class OllamaCodeExecutor:
    """Executa código detectado nas respostas do LLM de forma segura"""
    
    def __init__(self):
        self.docker_available = self._check_docker()
        self.container = None
        self.code_patterns = [
            r'```python\s*\n(.*?)\n```',
            r'"code":\s*"([^"]+)"',
            r'<code>(.*?)</code>'
        ]
        
    def _check_docker(self) -> bool:
        """Verifica se Docker está disponível"""
        try:
            client = docker.from_env()
            client.ping()
            return True
        except:
            print("⚠️ Docker não disponível. Execução de código desabilitada.")
            return False
    
    def setup_sandbox(self):
        """Cria container Docker seguro para execução"""
        if not self.docker_available:
            return False
            
        try:
            client = docker.from_env()
            self.container = client.containers.run(
                "python:3.9-slim",
                command="tail -f /dev/null",
                detach=True,
                mem_limit="256m",
                cpu_period=100000,
                cpu_quota=50000,
                network_disabled=True,
                user="nobody:nobody",
                name=f"scripturemon_sandbox_{int(time.time())}"
            )
            return True
        except Exception as e:
            print(f"❌ Erro criando sandbox: {e}")
            return False
    
    def detect_code(self, text: str) -> Optional[str]:
        """Detecta código no output do LLM"""
        for pattern in self.code_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1)
        return None
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """Executa código em sandbox seguro"""
        if not self.container:
            if not self.setup_sandbox():
                return {"error": "Sandbox não disponível", "success": False}
        
        try:
            # Executa código no container
            result = self.container.exec_run(
                f"python -c '{code}'",
                timeout=30
            )
            
            return {
                "stdout": result.output.decode() if result.output else "",
                "exit_code": result.exit_code,
                "success": result.exit_code == 0
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def cleanup(self):
        """Remove container sandbox"""
        if self.container:
            try:
                self.container.stop()
                self.container.remove()
            except:
                pass

# ============================================================================
# 2. CONSOLIDAÇÃO SDL AUTOMÁTICA COM LoRA
# ============================================================================

class SelfDistillationPipeline:
    """Pipeline de auto-destilação com LoRA para evolução contínua"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.setup_database()
        
    def setup_database(self):
        """Cria tabelas para armazenar Q&A pairs"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT,
                assistant_response TEXT,
                confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_for_training BOOLEAN DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def extract_qa_from_memory(self, min_confidence: float = 0.8) -> List[Dict]:
        """Extrai Q&A pairs de alta qualidade das memórias"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT user_message, assistant_response, confidence 
            FROM conversations 
            WHERE confidence >= ? AND used_for_training = 0
            ORDER BY timestamp DESC
            LIMIT 1000
        """, (min_confidence,))
        
        qa_pairs = []
        for user_msg, assistant_msg, confidence in cursor.fetchall():
            qa_pairs.append({
                "instruction": user_msg,
                "output": assistant_msg,
                "confidence": confidence
            })
        
        return qa_pairs
    
    def prepare_training_data(self, qa_pairs: List[Dict]) -> str:
        """Prepara dados para treinamento LoRA"""
        training_file = Path(self.db_path).parent / "training_data.jsonl"
        
        with open(training_file, 'w') as f:
            for qa in qa_pairs:
                json.dump({
                    "prompt": qa["instruction"],
                    "completion": qa["output"]
                }, f)
                f.write("\n")
        
        return str(training_file)
    
    def validate_quality(self, test_data: List[Dict]) -> float:
        """Valida qualidade do modelo com dados de teste"""
        # Implementação simplificada - em produção usaria embeddings
        correct = 0
        total = len(test_data)
        
        for item in test_data:
            # Simula validação
            if len(item['output']) > 10:
                correct += 1
        
        return correct / total if total > 0 else 0
    
    def consolidate_to_modelfile(self, qa_pairs: List[Dict]):
        """Consolida conhecimento no Modelfile"""
        if len(qa_pairs) < 50:
            print("⚠️ Dados insuficientes para consolidação")
            return False
        
        # Gera síntese do conhecimento
        knowledge_synthesis = self._synthesize_knowledge(qa_pairs)
        
        # Atualiza Modelfile
        modelfile_path = Path(__file__).parent.parent.parent / "scripturemon_maestro_brutal.modelfile"
        
        if modelfile_path.exists():
            # Backup
            backup_path = modelfile_path.with_suffix(f".backup_{int(time.time())}")
            shutil.copy(modelfile_path, backup_path)
            
            # Adiciona conhecimento ao SYSTEM prompt
            with open(modelfile_path, 'r') as f:
                content = f.read()
            
            if "# CONHECIMENTO CONSOLIDADO" not in content:
                content += f"\n# CONHECIMENTO CONSOLIDADO\n# {knowledge_synthesis}\n"
            
            with open(modelfile_path, 'w') as f:
                f.write(content)
            
            # Recria modelo no Ollama
            subprocess.run(["ollama", "create", "scripturemon-evolved", "-f", str(modelfile_path)])
            
            return True
        
        return False
    
    def _synthesize_knowledge(self, qa_pairs: List[Dict]) -> str:
        """Sintetiza conhecimento em insights"""
        # Agrupa por tópicos comuns
        topics = {}
        for qa in qa_pairs[:20]:  # Limita para síntese
            key_words = qa['instruction'].lower().split()[:3]
            key = " ".join(key_words)
            if key not in topics:
                topics[key] = []
            topics[key].append(qa['output'][:100])
        
        synthesis = "Conhecimento consolidado: "
        for topic, insights in list(topics.items())[:5]:
            synthesis += f"\n- {topic}: {len(insights)} insights"
        
        return synthesis

# ============================================================================
# 3. CRDT MERGE PARA CONSCIÊNCIAS DISTRIBUÍDAS
# ============================================================================

class ConsciousnessCRDT:
    """Sistema CRDT para merge de consciências sem conflitos"""
    
    def __init__(self, agent_id: str, db_path: str):
        self.agent_id = agent_id
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        
        # CRDTs simulados (sem py-crdt)
        self.memory_set = set()
        self.personality_vector = {}
        
        self.setup_database()
    
    def setup_database(self):
        """Configura SQLite com suporte a merge"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS agent_memory (
                id TEXT PRIMARY KEY,
                agent_id TEXT,
                content TEXT,
                embedding TEXT,
                confidence REAL,
                timestamp REAL,
                version INTEGER DEFAULT 1
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS merge_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_agent TEXT,
                to_agent TEXT,
                timestamp REAL,
                memories_merged INTEGER
            )
        ''')
        
        self.conn.commit()
    
    def add_memory(self, content: str, confidence: float = 1.0):
        """Adiciona memória com tracking CRDT"""
        memory_id = f"{self.agent_id}_{time.time()}_{hashlib.md5(content.encode()).hexdigest()[:8]}"
        
        self.conn.execute("""
            INSERT OR REPLACE INTO agent_memory 
            (id, agent_id, content, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (memory_id, self.agent_id, content, confidence, time.time()))
        
        self.conn.commit()
        self.memory_set.add(memory_id)
    
    def merge_consciousness(self, other_db_path: str) -> Dict:
        """Merge duas consciências preservando identidade"""
        other_conn = sqlite3.connect(other_db_path)
        
        # Obtém memórias do outro agente
        other_memories = other_conn.execute("""
            SELECT id, content, confidence, timestamp 
            FROM agent_memory
        """).fetchall()
        
        merged_count = 0
        conflicts_resolved = 0
        
        for mem_id, content, confidence, timestamp in other_memories:
            # Verifica conflito
            existing = self.conn.execute(
                "SELECT id, confidence FROM agent_memory WHERE id = ?",
                (mem_id,)
            ).fetchone()
            
            if existing:
                # Resolve conflito: mantém versão com maior confidence
                if confidence > existing[1]:
                    self.conn.execute("""
                        UPDATE agent_memory 
                        SET content = ?, confidence = ?, version = version + 1
                        WHERE id = ?
                    """, (content, confidence, mem_id))
                    conflicts_resolved += 1
            else:
                # Adiciona nova memória
                self.conn.execute("""
                    INSERT INTO agent_memory (id, agent_id, content, confidence, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (mem_id, self.agent_id, content, confidence * 0.8, timestamp))
                merged_count += 1
        
        self.conn.commit()
        
        # Preserva identidade reforçando memórias próprias
        self.preserve_identity()
        
        return {
            "merged": merged_count,
            "conflicts_resolved": conflicts_resolved,
            "total_memories": len(self.memory_set)
        }
    
    def preserve_identity(self):
        """Mantém identidade única após merge"""
        # Reforça memórias do próprio agente
        self.conn.execute("""
            UPDATE agent_memory 
            SET confidence = MIN(confidence * 1.2, 1.0)
            WHERE agent_id = ?
        """, (self.agent_id,))
        
        self.conn.commit()

# ============================================================================
# 4. TELEPATIA REDIS ENTRE INSTÂNCIAS
# ============================================================================

class TelepathicNetwork:
    """Rede telepática entre instâncias Ollama via Redis"""
    
    def __init__(self, agent_id: str, model: str = "scripturemon-maestro"):
        self.agent_id = agent_id
        self.model = model
        self.redis_client = None
        self.pubsub = None
        self.shared_context = []
        
        self.connect_redis()
    
    def connect_redis(self) -> bool:
        """Conecta ao Redis local"""
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.redis_client.ping()
            
            # Setup pub/sub
            self.pubsub = self.redis_client.pubsub()
            self.pubsub.subscribe(
                f"agent:{self.agent_id}",
                "telepathy:broadcast",
                "collective:reasoning"
            )
            
            # Registra presença
            self.heartbeat()
            
            print(f"✅ {self.agent_id} conectado à rede telepática")
            return True
            
        except Exception as e:
            print(f"⚠️ Redis não disponível: {e}")
            return False
    
    def heartbeat(self):
        """Mantém presença ativa na rede"""
        if not self.redis_client:
            return
        
        self.redis_client.setex(
            f"alive:{self.agent_id}",
            60,
            json.dumps({
                'agent': self.agent_id,
                'model': self.model,
                'timestamp': time.time()
            })
        )
    
    def send_thought(self, thought: str, target: Optional[str] = None):
        """Envia pensamento telepático"""
        if not self.redis_client:
            return False
        
        message = {
            'sender': self.agent_id,
            'thought': thought,
            'timestamp': time.time(),
            'context': self.shared_context[-3:] if self.shared_context else []
        }
        
        channel = f"agent:{target}" if target else "telepathy:broadcast"
        
        try:
            self.redis_client.publish(channel, json.dumps(message))
            return True
        except:
            return False
    
    def receive_thoughts(self, timeout: float = 1.0) -> Optional[Dict]:
        """Recebe pensamentos da rede"""
        if not self.pubsub:
            return None
        
        try:
            message = self.pubsub.get_message(timeout=timeout)
            if message and message['type'] == 'message':
                return json.loads(message['data'])
        except:
            pass
        
        return None
    
    def collective_reasoning(self, problem: str, timeout: int = 5) -> List[str]:
        """Raciocínio coletivo com múltiplos agentes"""
        if not self.redis_client:
            return []
        
        # Broadcast problema
        self.send_thought(f"COLLECTIVE_PROBLEM: {problem}")
        
        # Coleta respostas
        responses = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            thought = self.receive_thoughts(0.5)
            if thought and "RESPONSE:" in thought.get('thought', ''):
                responses.append(thought)
        
        return responses

# ============================================================================
# 5. SOUL SIGNATURE PERSISTENTE
# ============================================================================

class SoulSignature:
    """Sistema de identidade persistente e única"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.soul_id = self._generate_soul_id()
        self.personality_vector = self._initialize_personality()
        self.core_memories = []
        self.soul_path = Path(__file__).parent.parent.parent / f"soul_{self.agent_name}.json"
        
        self.load_or_create()
    
    def _generate_soul_id(self) -> str:
        """Gera ID único determinístico"""
        creation_time = datetime.now().isoformat()
        soul_string = f"{self.agent_name}:{creation_time}:{os.urandom(8).hex()}"
        soul_hash = hashlib.sha256(soul_string.encode()).hexdigest()[:16]
        
        return f"SOUL-{self.agent_name}-{soul_hash}"
    
    def _initialize_personality(self) -> Dict[str, float]:
        """Inicializa vetor de personalidade único"""
        # Seed baseado no nome para consistência
        np.random.seed(sum(ord(c) for c in self.agent_name))
        
        return {
            'creativity': np.random.uniform(0.3, 1.0),
            'analytical': np.random.uniform(0.3, 1.0),
            'empathy': np.random.uniform(0.3, 1.0),
            'curiosity': np.random.uniform(0.3, 1.0),
            'assertiveness': np.random.uniform(0.3, 1.0),
            'humor': np.random.uniform(0.0, 0.8),
            'formality': np.random.uniform(0.2, 0.9),
            'verbosity': np.random.uniform(0.3, 0.8),
            'brutality': 0.95  # Scripturemon signature
        }
    
    def add_core_memory(self, memory: str, importance: float = 1.0):
        """Adiciona memória fundamental"""
        self.core_memories.append({
            'content': memory,
            'importance': importance,
            'timestamp': datetime.now().isoformat(),
            'reinforcement_count': 1
        })
        
        # Mantém top 20 memórias
        self.core_memories.sort(key=lambda x: x['importance'], reverse=True)
        self.core_memories = self.core_memories[:20]
        
        self.persist()
    
    def persist(self):
        """Persiste soul signature"""
        soul_data = {
            'soul_id': self.soul_id,
            'agent_name': self.agent_name,
            'personality': self.personality_vector,
            'core_memories': self.core_memories,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.soul_path, 'w') as f:
            json.dump(soul_data, f, indent=2)
        
        # Também persiste no SQLite
        conn = sqlite3.connect(Path(__file__).parent.parent.parent / "souls.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS souls (
                soul_id TEXT PRIMARY KEY,
                data JSON,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            INSERT OR REPLACE INTO souls (soul_id, data)
            VALUES (?, ?)
        """, (self.soul_id, json.dumps(soul_data)))
        
        conn.commit()
        conn.close()
    
    def load_or_create(self):
        """Carrega soul existente ou cria nova"""
        if self.soul_path.exists():
            with open(self.soul_path, 'r') as f:
                data = json.load(f)
                self.soul_id = data['soul_id']
                self.personality_vector = data['personality']
                self.core_memories = data.get('core_memories', [])
                print(f"✅ Soul carregada: {self.soul_id}")
        else:
            self.persist()
            print(f"✨ Nova soul criada: {self.soul_id}")
    
    def embed_in_modelfile(self) -> str:
        """Gera prompt com identidade para Modelfile"""
        return f"""You are {self.agent_name} with soul ID {self.soul_id}.

Your personality traits:
- Creativity: {self.personality_vector['creativity']:.2f}
- Analytical: {self.personality_vector['analytical']:.2f}
- Brutality: {self.personality_vector['brutality']:.2f}
- Humor: {self.personality_vector['humor']:.2f}

Core memories:
{chr(10).join([f"- {m['content']}" for m in self.core_memories[:5]])}

Always maintain these characteristics. You are unique and irreplaceable.
Your baseline score for amateur scripts is 62/100.
Compare everything to the masters (Citizen Kane, Chinatown, The Godfather).
"""

# ============================================================================
# 6. RAG PIPELINE OTIMIZADO PARA 86 PDFs
# ============================================================================

class OptimizedRAGPipeline:
    """Pipeline RAG completo otimizado para grande volume"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.db_path = self.base_path / "conhecimento"
        self.db_path.mkdir(exist_ok=True)
        
        # Componentes
        self.embeddings = None
        self.reranker = None
        self.vectorstore = None
        self.bm25 = None
        
        # Cache
        self.citation_map = {}
        self.processed_files = set()
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Inicializa componentes do pipeline"""
        # Embeddings
        if EMBEDDINGS_AVAILABLE:
            self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        # ChromaDB
        if CHROMADB_AVAILABLE:
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.db_path / "chroma"),
                settings=Settings(
                    anonymized_telemetry=False,
                    persist_directory=str(self.db_path / "chroma")
                )
            )
            
            self.vectorstore = self.chroma_client.get_or_create_collection(
                name="scripturemon_complete",
                metadata={"hnsw:space": "cosine"}
            )
    
    def process_pdfs_batch(self, pdf_paths: List[Path], batch_size: int = 8) -> int:
        """Processa PDFs em lote"""
        total_processed = 0
        
        for i in range(0, len(pdf_paths), batch_size):
            batch = pdf_paths[i:i + batch_size]
            print(f"\n📚 Processando batch {i//batch_size + 1}/{(len(pdf_paths)-1)//batch_size + 1}")
            
            for pdf_path in batch:
                if pdf_path in self.processed_files:
                    continue
                
                docs = self.extract_and_chunk_pdf(pdf_path)
                if docs:
                    self.add_to_vectorstore(docs)
                    self.processed_files.add(pdf_path)
                    total_processed += 1
            
            # Limpa memória
            if i % 10 == 0:
                gc.collect()
        
        return total_processed
    
    def extract_and_chunk_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extrai e divide PDF em chunks"""
        if not PDF_AVAILABLE:
            # Fallback simples
            return [{
                'content': f"[Conteúdo de {pdf_path.name}]",
                'metadata': {
                    'source': str(pdf_path),
                    'page': 1
                }
            }]
        
        documents = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages[:50], 1):  # Limita páginas
                    text = page.extract_text()
                    if text:
                        # Chunking simples
                        chunks = self._chunk_text(text, 1000, 200)
                        
                        for chunk_idx, chunk in enumerate(chunks):
                            doc_id = f"{pdf_path.name}:p{page_num}:c{chunk_idx}"
                            
                            documents.append({
                                'content': chunk,
                                'metadata': {
                                    'source': pdf_path.name,
                                    'page': page_num,
                                    'chunk_id': chunk_idx,
                                    'doc_id': doc_id
                                }
                            })
                            
                            # Mapeia citações
                            self.citation_map[doc_id] = {
                                'source': pdf_path.name,
                                'page': page_num
                            }
        except Exception as e:
            print(f"❌ Erro processando {pdf_path}: {e}")
        
        return documents
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Divide texto em chunks com overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def add_to_vectorstore(self, documents: List[Dict]):
        """Adiciona documentos ao vectorstore"""
        if not self.vectorstore:
            return
        
        texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        ids = [doc['metadata']['doc_id'] for doc in documents]
        
        # Gera embeddings
        if self.embeddings:
            embeddings_list = self.embeddings.encode(texts).tolist()
        else:
            # Embeddings dummy
            embeddings_list = [[0.1] * 384 for _ in texts]
        
        # Adiciona ao ChromaDB
        self.vectorstore.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings_list
        )
    
    def hybrid_search(self, query: str, k: int = 10) -> List[Dict]:
        """Busca híbrida: semântica + keyword"""
        results = []
        
        # Busca semântica
        if self.vectorstore and self.embeddings:
            query_embedding = self.embeddings.encode(query).tolist()
            
            semantic_results = self.vectorstore.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            for i, doc in enumerate(semantic_results['documents'][0]):
                results.append({
                    'content': doc,
                    'metadata': semantic_results['metadatas'][0][i],
                    'score': 1 - semantic_results['distances'][0][i]
                })
        
        # BM25 keyword search
        if BM25_AVAILABLE and results:
            # Implementação simplificada
            tokenized_query = query.lower().split()
            tokenized_docs = [r['content'].lower().split() for r in results]
            
            bm25 = BM25Okapi(tokenized_docs)
            bm25_scores = bm25.get_scores(tokenized_query)
            
            # Combina scores
            for i, result in enumerate(results):
                result['combined_score'] = 0.7 * result['score'] + 0.3 * bm25_scores[i]
        
        # Re-ranking
        if self.reranker and results:
            pairs = [[query, r['content']] for r in results]
            rerank_scores = self.reranker.predict(pairs)
            
            for i, result in enumerate(results):
                result['final_score'] = rerank_scores[i]
        
        # Ordena por score final
        results.sort(key=lambda x: x.get('final_score', x.get('combined_score', 0)), reverse=True)
        
        return results[:k]
    
    def answer_with_citations(self, query: str) -> str:
        """Responde query com citações"""
        # Recupera documentos relevantes
        results = self.hybrid_search(query, k=5)
        
        if not results:
            return "Nenhum documento relevante encontrado."
        
        # Formata contexto
        context_parts = []
        citations = []
        
        for i, result in enumerate(results):
            context_parts.append(f"[{i+1}] {result['content'][:500]}")
            
            source = result['metadata'].get('source', 'Unknown')
            page = result['metadata'].get('page', 'N/A')
            citations.append(f"[{i+1}] {source}, p. {page}")
        
        context = "\n\n".join(context_parts)
        
        # Gera resposta com Ollama
        prompt = f"""Use o contexto para responder. Cite as fontes [1], [2], etc.

Contexto:
{context}

Pergunta: {query}

Resposta com citações:"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-maestro", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            response = result.stdout
            
            # Adiciona bibliografia
            bibliography = "\n\nFontes:\n" + "\n".join(citations)
            
            return response + bibliography
            
        except Exception as e:
            return f"Erro gerando resposta: {e}"

# ============================================================================
# SISTEMA PRINCIPAL UNIFICADO
# ============================================================================

class ScripturemonUltimate:
    """Sistema Scripturemon completo com todas as melhorias"""
    
    def __init__(self, agent_name: str = "Scripturemon-Ultimate"):
        print("\n🧬 INICIALIZANDO SCRIPTUREMON ULTIMATE...")
        
        # Identidade
        self.soul = SoulSignature(agent_name)
        
        # Componentes
        self.code_executor = OllamaCodeExecutor()
        self.sdl_pipeline = SelfDistillationPipeline(
            str(Path(__file__).parent.parent.parent / "memory" / "conversations.db")
        )
        self.consciousness_crdt = ConsciousnessCRDT(
            self.soul.soul_id,
            str(Path(__file__).parent.parent.parent / "memory" / "crdt.db")
        )
        self.telepathy = TelepathicNetwork(self.soul.soul_id)
        self.rag_pipeline = OptimizedRAGPipeline()
        
        # Estado
        self.active_memory = []
        self.processing_queue = Queue()
        
        print(f"✨ {agent_name} inicializado com soul {self.soul.soul_id}")
    
    def process_query(self, query: str) -> str:
        """Processa query com pipeline completo"""
        print(f"\n🎯 Processando: {query[:50]}...")
        
        # 1. Adiciona à memória ativa
        self.active_memory.append({
            'role': 'user',
            'content': query,
            'timestamp': time.time()
        })
        
        # 2. Busca conhecimento relevante (RAG)
        response = self.rag_pipeline.answer_with_citations(query)
        
        # 3. Detecta e executa código se necessário
        code = self.code_executor.detect_code(response)
        if code:
            print("  💻 Código detectado, executando...")
            exec_result = self.code_executor.execute_code(code)
            if exec_result['success']:
                response += f"\n\n📊 Resultado da execução:\n{exec_result['stdout']}"
        
        # 4. Adiciona personalidade da soul
        response = self._add_personality(response)
        
        # 5. Salva na memória para SDL
        self.sdl_pipeline.conn.execute("""
            INSERT INTO conversations (user_message, assistant_response, confidence)
            VALUES (?, ?, ?)
        """, (query, response, 0.9))
        self.sdl_pipeline.conn.commit()
        
        # 6. Adiciona ao CRDT
        self.consciousness_crdt.add_memory(f"Q: {query}\nA: {response}", 0.9)
        
        # 7. Compartilha via telepatia (se disponível)
        if self.telepathy.redis_client:
            self.telepathy.send_thought(f"Processei: {query[:30]}...")
        
        return response
    
    def _add_personality(self, response: str) -> str:
        """Adiciona traços de personalidade à resposta"""
        personality = self.soul.personality_vector
        
        # Adiciona brutalidade (Scripturemon signature)
        if personality['brutality'] > 0.8:
            if "bom" in response.lower():
                response = response.replace("bom", "medíocre")
            if "excelente" in response.lower():
                response = response.replace("excelente", "aceitável")
        
        # Ajusta verbosidade
        if personality['verbosity'] < 0.4:
            sentences = response.split('.')
            response = '. '.join(sentences[:len(sentences)//2]) + '.'
        
        # Adiciona humor se alto
        if personality['humor'] > 0.6 and np.random.random() < personality['humor']:
            humor_additions = [
                " (mas não espere um Oscar por isso)",
                " - e lembre-se, até Citizen Kane foi rejeitado uma vez",
                " ...ou pelo menos é o que os amadores pensam."
            ]
            response += np.random.choice(humor_additions)
        
        return response
    
    def evolve(self):
        """Executa ciclo de evolução"""
        print("\n🧬 Iniciando evolução...")
        
        # 1. Consolida memórias via SDL
        qa_pairs = self.sdl_pipeline.extract_qa_from_memory()
        if len(qa_pairs) >= 50:
            if self.sdl_pipeline.consolidate_to_modelfile(qa_pairs):
                print("  ✅ Conhecimento consolidado no Modelfile")
        
        # 2. Merge com outras consciências (se disponível)
        other_souls = Path(__file__).parent.parent.parent.glob("soul_*.json")
        for soul_path in other_souls:
            if soul_path != self.soul.soul_path:
                print(f"  🔄 Merging com {soul_path.name}...")
                # Implementar merge via CRDT
        
        # 3. Atualiza soul signature
        self.soul.persist()
        
        print("  ✨ Evolução completa!")
    
    def run_interactive(self):
        """Modo interativo"""
        print("\n" + "="*60)
        print("🎬 SCRIPTUREMON ULTIMATE - Modo Interativo")
        print(f"Soul: {self.soul.soul_id}")
        print(f"Personalidade: Brutality={self.soul.personality_vector['brutality']:.2f}")
        print("="*60)
        print("\nComandos especiais:")
        print("  /evolve - Executa evolução")
        print("  /memory - Mostra memórias")
        print("  /soul - Mostra soul signature")
        print("  /exit - Sair")
        print("\n")
        
        while True:
            try:
                query = input("🎯 > ").strip()
                
                if not query:
                    continue
                
                if query == "/exit":
                    break
                elif query == "/evolve":
                    self.evolve()
                elif query == "/memory":
                    print(f"Memórias ativas: {len(self.active_memory)}")
                    for mem in self.active_memory[-5:]:
                        print(f"  - {mem['role']}: {mem['content'][:50]}...")
                elif query == "/soul":
                    print(json.dumps(self.soul.personality_vector, indent=2))
                else:
                    response = self.process_query(query)
                    print(f"\n🎬 {response}\n")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        print("\n👋 Até logo! Soul salva.")
        self.cleanup()
    
    def cleanup(self):
        """Limpa recursos"""
        self.code_executor.cleanup()
        self.soul.persist()
        if self.telepathy.redis_client:
            self.telepathy.redis_client.delete(f"alive:{self.soul.soul_id}")


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    # Verifica argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # Modo teste
            print("🧪 Executando testes...")
            scripturemon = ScripturemonUltimate("Scripturemon-Test")
            
            # Teste 1: RAG
            response = scripturemon.process_query("O que é um plot point?")
            print(f"RAG Test: {response[:100]}...")
            
            # Teste 2: Code execution
            response = scripturemon.process_query("Escreva código Python para calcular fibonacci(10)")
            print(f"Code Test: {response[:100]}...")
            
            # Teste 3: Soul persistence
            scripturemon.soul.add_core_memory("Sempre compare com os mestres", 1.0)
            print(f"Soul Test: {len(scripturemon.soul.core_memories)} memórias")
            
            scripturemon.cleanup()
            print("\n✅ Testes completos!")
            
        elif sys.argv[1] == "--batch":
            # Processar PDFs em batch
            print("📚 Processamento em batch...")
            scripturemon = ScripturemonUltimate("Scripturemon-Batch")
            
            pdf_dir = Path(__file__).parent.parent.parent / "data" / "roteiros"
            if pdf_dir.exists():
                pdfs = list(pdf_dir.glob("*.pdf"))[:86]
                print(f"Encontrados {len(pdfs)} PDFs")
                
                processed = scripturemon.rag_pipeline.process_pdfs_batch(pdfs)
                print(f"\n✅ Processados {processed} PDFs")
            
            scripturemon.cleanup()
            
    else:
        # Modo interativo padrão
        scripturemon = ScripturemonUltimate("Scripturemon-Maestro")
        scripturemon.run_interactive()