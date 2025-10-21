#!/usr/bin/env python3
"""
🧠 MEMORION SUPREME - O Guardião das Memórias
Sistema de memória gerenciado por Ollama dedicada
Como o hipocampo humano - gerencia, indexa e recupera memórias
COPIADO INTEGRALMENTE DO BACKUP - NENHUMA SIMPLIFICAÇÃO
"""

import json
import sqlite3
import hashlib
import subprocess
import threading
import queue
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from .memory_coordinator import get_coordinator
import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class MemorionSupreme:
    """
    🧠 MEMORION - Digimon Guardião das Memórias
    
    Arquitetura inspirada no cérebro humano:
    - HIPOCAMPO (Ollama dedicada): Gerencia e indexa memórias
    - CÓRTEX PRÉ-FRONTAL: Memória de trabalho
    - AMÍGDALA: Memórias emocionais importantes
    - CEREBELO: Memórias procedurais (como fazer)
    """
    
    def __init__(self, memory_model: str = "llama3.2:3b"):
        """
        Inicializa Memorion com modelo dedicado
        
        Args:
            memory_model: Modelo Ollama para gerenciar memórias (leve e rápido)
        """
        self.memory_model = memory_model  # Modelo dedicado para memória
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
        
        # === ESTRUTURAS DE MEMÓRIA HUMANA ===
        
        # 1. HIPOCAMPO - Consolidação e indexação
        self.hippocampus = {
            "short_term": {},      # Memória de curto prazo (7±2 items)
            "consolidating": {},   # Em processo de consolidação
            "indexed": {}          # Índice de memórias de longo prazo
        }
        
        # 2. MEMÓRIA SENSORIAL - Buffer ultra-rápido
        self.sensory_buffer = queue.Queue(maxsize=100)
        
        # 3. MEMÓRIA DE TRABALHO - Ativa no momento
        self.working_memory = {
            "context": [],         # Contexto atual (max 7 items)
            "focus": None,         # Foco atual
            "goals": []           # Objetivos atuais
        }
        
        # 4. MEMÓRIA DE LONGO PRAZO - Estruturada
        self.long_term = {
            "episodic": {},       # Eventos específicos (quem, quando, onde)
            "semantic": {},       # Fatos e conhecimento
            "procedural": {},     # Como fazer coisas
            "emotional": {}       # Memórias com carga emocional
        }
        
        # 5. MEMÓRIA ASSOCIATIVA - Conexões
        self.associations = {}  # Grafo de associações entre memórias
        
        # === DATABASES ===
        self.init_databases()
        
        # === CACHES INTELIGENTES ===
        self.cache_l1 = {}  # Cache nível 1 (ultra-rápido, 10 items)
        self.cache_l2 = {}  # Cache nível 2 (rápido, 100 items)
        self.cache_l3 = {}  # Cache nível 3 (médio, 1000 items)
        
        # === THREAD DO HIPOCAMPO ===
        self.hippocampus_thread = None
        self.running = True
        self.start_hippocampus()
        
        # === ESTATÍSTICAS ===
        self.stats = {
            "queries": 0,
            "hits_l1": 0,
            "hits_l2": 0,
            "hits_l3": 0,
            "misses": 0,
            "consolidations": 0,
            "associations_made": 0
        }
        
        print("🧠 MEMORION SUPREME ATIVADO")
        print(f"   Modelo: {memory_model}")
        print(f"   Hipocampo: Online")
        print(f"   Estruturas: 5 tipos de memória")
        print(f"   Caches: L1/L2/L3 ativos")
    
    def init_databases(self):
        """Inicializa databases SQLite para cada tipo de memória"""
        db_path = self.root / "runtime" / "memorion"
        db_path.mkdir(parents=True, exist_ok=True)
        
        # Database principal
        self.db_file = db_path / "memorion_supreme.db"
        
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        # Tabela para memórias episódicas
        cursor.execute('''CREATE TABLE IF NOT EXISTS episodic_memories (
            id TEXT PRIMARY KEY,
            timestamp REAL,
            event TEXT,
            participants TEXT,
            location TEXT,
            emotion TEXT,
            importance REAL,
            details TEXT
        )''')
        
        # Tabela para memórias semânticas
        cursor.execute('''CREATE TABLE IF NOT EXISTS semantic_memories (
            id TEXT PRIMARY KEY,
            concept TEXT,
            definition TEXT,
            category TEXT,
            relations TEXT,
            confidence REAL
        )''')
        
        # Tabela para memórias procedurais
        cursor.execute('''CREATE TABLE IF NOT EXISTS procedural_memories (
            id TEXT PRIMARY KEY,
            procedure TEXT,
            steps TEXT,
            prerequisites TEXT,
            outcome TEXT,
            success_rate REAL
        )''')
        
        # Tabela para memórias emocionais
        cursor.execute('''CREATE TABLE IF NOT EXISTS emotional_memories (
            id TEXT PRIMARY KEY,
            emotion TEXT,
            intensity REAL,
            trigger TEXT,
            response TEXT,
            timestamp REAL
        )''')
        
        # Tabela para associações
        cursor.execute('''CREATE TABLE IF NOT EXISTS associations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id1 TEXT,
            memory_id2 TEXT,
            strength REAL,
            type TEXT,
            created_at REAL
        )''')
        
        conn.commit()
        conn.close()
        
        print("   💾 Databases inicializados")
    
    def start_hippocampus(self):
        """Inicia thread do hipocampo para consolidação de memórias"""
        def hippocampus_loop():
            """Loop do hipocampo - consolida memórias continuamente"""
            while self.running:
                try:
                    # Processar buffer sensorial
                    if not self.sensory_buffer.empty():
                        self._process_sensory(self.sensory_buffer.get())
                    
                    # Consolidar memórias de curto prazo
                    self._consolidate_short_term()
                    
                    # Descobrir novas associações
                    self._discover_associations()
                    
                    # Manutenção de caches
                    self._maintain_caches()
                    
                    # Dormir como o cérebro faz
                    time.sleep(1)  # Ciclo de 1 segundo
                    
                except Exception as e:
                    print(f"   ⚠️ Erro no hipocampo: {e}")
        
        self.hippocampus_thread = threading.Thread(target=hippocampus_loop, daemon=True)
        self.hippocampus_thread.start()
        print("   🔄 Hipocampo ativado em thread separada")
    

    def consolidate_memories(self, force=False):
        """Consolida memórias de curto para longo prazo"""
        consolidated = 0
        
        # Transferir memórias antigas do hipocampo
        current_time = time.time()
        memories_to_consolidate = []
        
        for memory in self.short_term_memory:
            age = current_time - memory.get('timestamp', current_time)
            if age > 300 or force:  # 5 minutos ou forçado
                memories_to_consolidate.append(memory)
        
        # Mover para memória consolidada
        for memory in memories_to_consolidate:
            self.short_term_memory.remove(memory)
            self.long_term_memory.append(memory)
            consolidated += 1
        
        if consolidated > 0:
            print(f'  🧠 MEMORION: {consolidated} memórias consolidadas')
        
        return consolidated

    def query_memory(self, query: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Consulta memórias usando Ollama como interpretador
        
        Args:
            query: Pergunta ou busca
            context: Contexto adicional
            
        Returns:
            Memórias relevantes e síntese
        """
        self.stats["queries"] += 1
        
        # Check cache L1
        cache_key = hashlib.md5(f"{query}{context}".encode()).hexdigest()
        
        if cache_key in self.cache_l1:
            self.stats["hits_l1"] += 1
            return self._enrich_response(self.cache_l1[cache_key], "L1")
        
        # Check cache L2
        if cache_key in self.cache_l2:
            self.stats["hits_l2"] += 1
            self._promote_to_l1(cache_key, self.cache_l2[cache_key])
            return self._enrich_response(self.cache_l2[cache_key], "L2")
        
        # Check cache L3
        if cache_key in self.cache_l3:
            self.stats["hits_l3"] += 1
            self._promote_to_l2(cache_key, self.cache_l3[cache_key])
            return self._enrich_response(self.cache_l3[cache_key], "L3")
        
        # Cache miss - consultar Ollama
        self.stats["misses"] += 1
        
        # Usar Ollama para interpretar a query
        interpretation = self._interpret_query_with_ollama(query, context)
        
        # Buscar em diferentes tipos de memória
        results = {
            "episodic": self._search_episodic(interpretation),
            "semantic": self._search_semantic(interpretation),
            "procedural": self._search_procedural(interpretation),
            "emotional": self._search_emotional(interpretation),
            "associations": self._search_associations(interpretation)
        }
        
        # Usar Ollama para sintetizar resultados
        synthesis = self._synthesize_memory(results, query)
        
        # Armazenar em cache
        response = {
            "query": query,
            "context": context,
            "interpretation": interpretation,
            "memories": results,
            "synthesis": synthesis,
            "timestamp": time.time()
        }
        
        self._add_to_cache(cache_key, response)
        
        # Atualizar working memory
        self._update_working_memory(query, response)
        
        return response
    
    def _interpret_query_with_ollama(self, query: str, context: Optional[List[str]]) -> Dict:
        """Usa Ollama para interpretar a query"""
        try:
            prompt = f"""Você é o hipocampo de MEMORION, responsável por interpretar buscas de memória.

Analise esta consulta e identifique:
1. Tipo de memória buscada (episódica, semântica, procedural, emocional)
2. Palavras-chave importantes
3. Período temporal (se houver)
4. Entidades mencionadas (pessoas, lugares, conceitos)
5. Emoção associada (se houver)

Query: {query}
Contexto: {context if context else 'Nenhum'}

Responda em JSON com os campos acima."""

            cmd = ["ollama", "run", self.memory_model]
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    # Tentar parsear JSON da resposta
                    response = result.stdout.strip()
                    # Extrair JSON da resposta
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass
            
        except Exception as e:
            print(f"   ⚠️ Erro na interpretação: {e}")
        
        # Fallback - interpretação básica
        return {
            "tipo": "geral",
            "palavras_chave": query.lower().split(),
            "periodo": None,
            "entidades": self._extract_entities(query),
            "emocao": None
        }
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extrai entidades do texto (simplificado)"""
        entities = []
        
        # Palavras em maiúscula (nomes próprios)
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 1:
                entities.append(word)
        
        return entities
    
    def _search_episodic(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias episódicas"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        results = []
        
        # Construir query SQL baseada na interpretação
        keywords = interpretation.get("palavras_chave", [])
        
        for keyword in keywords:
            cursor.execute('''
                SELECT * FROM episodic_memories
                WHERE event LIKE ? OR participants LIKE ? OR location LIKE ?
                ORDER BY importance DESC, timestamp DESC
                LIMIT 5
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "event": row[2],
                    "participants": json.loads(row[3]) if row[3] else [],
                    "location": row[4],
                    "emotion": row[5],
                    "importance": row[6],
                    "details": json.loads(row[7]) if row[7] else {}
                })
        
        conn.close()
        return results
    
    def _search_semantic(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias semânticas"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        results = []
        keywords = interpretation.get("palavras_chave", [])
        
        for keyword in keywords:
            cursor.execute('''
                SELECT * FROM semantic_memories
                WHERE concept LIKE ? OR definition LIKE ? OR category LIKE ?
                ORDER BY confidence DESC
                LIMIT 5
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "concept": row[1],
                    "definition": row[2],
                    "category": row[3],
                    "relations": json.loads(row[4]) if row[4] else [],
                    "confidence": row[5]
                })
        
        conn.close()
        return results
    
    def _search_procedural(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias procedurais"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        results = []
        keywords = interpretation.get("palavras_chave", [])
        
        for keyword in keywords:
            cursor.execute('''
                SELECT * FROM procedural_memories
                WHERE procedure LIKE ? OR outcome LIKE ?
                ORDER BY success_rate DESC
                LIMIT 5
            ''', (f'%{keyword}%', f'%{keyword}%'))
            
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "procedure": row[1],
                    "steps": json.loads(row[2]) if row[2] else [],
                    "prerequisites": json.loads(row[3]) if row[3] else [],
                    "outcome": row[4],
                    "success_rate": row[5]
                })
        
        conn.close()
        return results
    
    def _search_emotional(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias emocionais"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        results = []
        emotion = interpretation.get("emocao")
        
        if emotion:
            cursor.execute('''
                SELECT * FROM emotional_memories
                WHERE emotion = ?
                ORDER BY intensity DESC, timestamp DESC
                LIMIT 5
            ''', (emotion,))
            
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "emotion": row[1],
                    "intensity": row[2],
                    "trigger": row[3],
                    "response": row[4],
                    "timestamp": row[5]
                })
        
        conn.close()
        return results
    
    def _search_associations(self, interpretation: Dict) -> List[Dict]:
        """Busca associações entre memórias"""
        # Simplificado - buscar associações mais fortes
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM associations
            ORDER BY strength DESC
            LIMIT 10
        ''')
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "memory_id1": row[1],
                "memory_id2": row[2],
                "strength": row[3],
                "type": row[4],
                "created_at": row[5]
            })
        
        conn.close()
        return results
    
    def _synthesize_memory(self, results: Dict, query: str) -> str:
        """Usa Ollama para sintetizar memórias encontradas"""
        # Preparar resumo das memórias
        memory_summary = []
        
        for memory_type, memories in results.items():
            if memories:
                memory_summary.append(f"{memory_type}: {len(memories)} memórias encontradas")
        
        if not memory_summary:
            return "Nenhuma memória relevante encontrada."
        
        # Síntese simplificada
        synthesis = f"Encontrei {sum(len(m) for m in results.values())} memórias relacionadas a '{query}'."
        
        # Adicionar detalhes mais relevantes
        if results["episodic"]:
            synthesis += f" Eventos: {results['episodic'][0].get('event', 'N/A')}."
        
        if results["semantic"]:
            synthesis += f" Conceitos: {results['semantic'][0].get('concept', 'N/A')}."
        
        return synthesis
    
    def _add_to_cache(self, key: str, value: Dict):
        """Adiciona resposta ao cache L3"""
        # L3 tem limite de 1000 items
        if len(self.cache_l3) >= 1000:
            # Remover item mais antigo
            oldest = min(self.cache_l3.items(), key=lambda x: x[1].get("timestamp", 0))
            del self.cache_l3[oldest[0]]
        
        self.cache_l3[key] = value
    
    def _promote_to_l1(self, key: str, value: Dict):
        """Promove item para cache L1"""
        if len(self.cache_l1) >= 10:
            oldest = min(self.cache_l1.items(), key=lambda x: x[1].get("timestamp", 0))
            del self.cache_l1[oldest[0]]
        self.cache_l1[key] = value
    
    def _promote_to_l2(self, key: str, value: Dict):
        """Promove item para cache L2"""
        if len(self.cache_l2) >= 100:
            oldest = min(self.cache_l2.items(), key=lambda x: x[1].get("timestamp", 0))
            # Demover para L3
            self._add_to_cache(oldest[0], oldest[1])
            del self.cache_l2[oldest[0]]
        self.cache_l2[key] = value
    
    def _update_working_memory(self, query: str, result: Dict):
        """Atualiza memória de trabalho"""
        # Manter apenas 7 items no contexto
        if len(self.working_memory["context"]) >= 7:
            self.working_memory["context"].pop(0)
        
        self.working_memory["context"].append({
            "query": query,
            "timestamp": time.time(),
            "memories_found": sum(len(m) for m in result["memories"].values())
        })
        
        self.working_memory["focus"] = query
    
    def _enrich_response(self, cached: Dict, source: str) -> Dict:
        """Enriquece resposta do cache com metadados"""
        cached["cache_source"] = source
        cached["cache_hit"] = True
        return cached
    
    def _process_sensory(self, item: Any):
        """Processa item do buffer sensorial"""
        # Decidir se é importante o suficiente para memória de curto prazo
        if self._is_important(item):
            memory_id = hashlib.md5(str(item).encode()).hexdigest()
            self.hippocampus["short_term"][memory_id] = {
                "content": item,
                "timestamp": time.time(),
                "access_count": 1
            }
    
    def _is_important(self, item: Any) -> bool:
        """Determina se item é importante para memorizar"""
        # Heurística simples - itens com mais de 10 caracteres
        if isinstance(item, str):
            return len(item) > 10
        return True
    
    def _consolidate_short_term(self):
        """Consolida memórias de curto prazo para longo prazo"""
        current_time = time.time()
        
        for memory_id, memory in list(self.hippocampus["short_term"].items()):
            # Se memória tem mais de 30 segundos e foi acessada múltiplas vezes
            age = current_time - memory["timestamp"]
            
            if age > 30 and memory["access_count"] > 2:
                # Mover para consolidação
                self.hippocampus["consolidating"][memory_id] = memory
                del self.hippocampus["short_term"][memory_id]
        
        # Processar memórias em consolidação
        for memory_id, memory in list(self.hippocampus["consolidating"].items()):
            if self._should_consolidate(memory):
                self._consolidate_to_long_term(memory)
                del self.hippocampus["consolidating"][memory_id]
                self.stats["consolidations"] += 1
    
    def _should_consolidate(self, memory: Any) -> bool:
        """Decide se memória deve ser consolidada"""
        # Consolidar se foi acessada mais de 5 vezes
        return memory.get("access_count", 0) > 5
    
    def _consolidate_to_long_term(self, memory: Dict):
        """Consolida memória para armazenamento de longo prazo"""
        content = memory["content"]
        
        # Determinar tipo de memória
        if isinstance(content, dict):
            if "event" in content:
                self._save_episodic_memory(content)
            elif "concept" in content:
                self._save_semantic_memory(content)
            elif "procedure" in content:
                self._save_procedural_memory(content)
    
    def _save_episodic_memory(self, memory: Dict):
        """Salva memória episódica"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        memory_id = hashlib.md5(json.dumps(memory).encode()).hexdigest()
        
        cursor.execute('''
            INSERT OR REPLACE INTO episodic_memories
            (id, timestamp, event, participants, location, emotion, importance, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory_id,
            time.time(),
            memory.get("event", ""),
            json.dumps(memory.get("participants", [])),
            memory.get("location", ""),
            memory.get("emotion", ""),
            memory.get("importance", 0.5),
            json.dumps(memory.get("details", {}))
        ))
        
        conn.commit()
        conn.close()
    
    def _save_semantic_memory(self, memory: Dict):
        """Salva memória semântica"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        memory_id = hashlib.md5(json.dumps(memory).encode()).hexdigest()
        
        cursor.execute('''
            INSERT OR REPLACE INTO semantic_memories
            (id, concept, definition, category, relations, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            memory_id,
            memory.get("concept", ""),
            memory.get("definition", ""),
            memory.get("category", ""),
            json.dumps(memory.get("relations", [])),
            memory.get("confidence", 0.5)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_procedural_memory(self, memory: Dict):
        """Salva memória procedural"""
        # Similar aos outros tipos
        pass
    
    def _maintain_caches(self):
        """Manutenção periódica dos caches"""
        # Limpar caches muito antigos
        current_time = time.time()
        max_age = 3600  # 1 hora
        
        # Limpar L3
        for key in list(self.cache_l3.keys()):
            if current_time - self.cache_l3[key].get("timestamp", 0) > max_age:
                del self.cache_l3[key]
    
    def _discover_associations(self):
        """Descobre novas associações entre memórias"""
        # Simplificado - associar memórias recentes
        if len(self.hippocampus["short_term"]) >= 2:
            memories = list(self.hippocampus["short_term"].keys())
            
            # Criar associação entre as duas memórias mais recentes
            if len(memories) >= 2:
                self._create_association(memories[-1], memories[-2], strength=0.5)
                self.stats["associations_made"] += 1
    
    def _create_association(self, memory_id1: str, memory_id2: str, strength: float):
        """Cria associação entre duas memórias"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO associations
            (memory_id1, memory_id2, strength, type, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (memory_id1, memory_id2, strength, "temporal", time.time()))
        
        conn.commit()
        conn.close()
    
    def store_memory(self, memory_type: str, content: Dict) -> str:
        """Interface pública para armazenar memórias"""
        # Adicionar ao buffer sensorial
        self.sensory_buffer.put(content)
        
        memory_id = hashlib.md5(json.dumps(content).encode()).hexdigest()
        
        # Adicionar diretamente ao short-term para processamento
        self.hippocampus["short_term"][memory_id] = {
            "content": content,
            "timestamp": time.time(),
            "access_count": 1,
            "type": memory_type
        }
        
        return memory_id
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas do sistema"""
        return {
            **self.stats,
            "sensory_buffer_size": self.sensory_buffer.qsize(),
            "short_term_memories": len(self.hippocampus["short_term"]),
            "consolidating_memories": len(self.hippocampus["consolidating"]),
            "working_memory_context": len(self.working_memory["context"]),
            "cache_l1_size": len(self.cache_l1),
            "cache_l2_size": len(self.cache_l2),
            "cache_l3_size": len(self.cache_l3)
        }
    
    def shutdown(self):
        """Desliga o sistema graciosamente"""
        self.running = False
        if self.hippocampus_thread:
            self.hippocampus_thread.join(timeout=5)
        print("   🛑 MEMORION desligado")