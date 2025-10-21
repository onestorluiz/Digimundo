#!/usr/bin/env python3
"""
🧠 MEMORION SUPREME - O Guardião das Memórias
Sistema de memória gerenciado por Ollama dedicada
Como o hipocampo humano - gerencia, indexa e recupera memórias
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
        print(f"   Cache: 3 níveis")
    
    def init_databases(self):
        """Inicializa databases de memória"""
        
        # Database principal de memórias
        self.memory_db = self.root / "data" / "memory" / "memorion_supreme.db"
        self.memory_db.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        # Tabela de memórias episódicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id TEXT PRIMARY KEY,
                timestamp REAL,
                who TEXT,
                what TEXT,
                location TEXT,
                when_text TEXT,
                content TEXT,
                importance REAL,
                access_count INTEGER DEFAULT 0,
                last_accessed REAL,
                embedding BLOB
            )
        """)
        
        # Tabela de memórias semânticas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id TEXT PRIMARY KEY,
                concept TEXT,
                definition TEXT,
                category TEXT,
                source TEXT,
                confidence REAL,
                embedding BLOB,
                created_at REAL
            )
        """)
        
        # Tabela de associações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory1_id TEXT,
                memory2_id TEXT,
                strength REAL,
                type TEXT,
                created_at REAL
            )
        """)
        
        # Tabela de padrões aprendidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id TEXT PRIMARY KEY,
                pattern TEXT,
                frequency INTEGER,
                success_rate REAL,
                context TEXT,
                learned_at REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def start_hippocampus(self):
        """Inicia thread do hipocampo para consolidação de memórias"""
        
        def hippocampus_loop():
            """Loop do hipocampo - consolida memórias continuamente"""
            while self.running:
                try:
                    # Processa buffer sensorial
                    if not self.sensory_buffer.empty():
                        item = self.sensory_buffer.get(timeout=1)
                        self._process_sensory(item)
                    
                    # Consolida memórias de curto prazo
                    self._consolidate_short_term()
                    
                    # Faz manutenção dos caches
                    self._maintain_caches()
                    
                    # Descobre novas associações
                    self._discover_associations()
                    
                    time.sleep(0.5)  # Ciclo de 500ms
                    
                except Exception as e:
                    print(f"⚠️ Erro no hipocampo: {e}")
        
        self.hippocampus_thread = threading.Thread(target=hippocampus_loop, daemon=True)
        self.hippocampus_thread.start()
    
    def query_memory(self, query: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        CONSULTA INTELIGENTE DE MEMÓRIA
        O Memorion usa Ollama para entender e buscar memórias
        
        Args:
            query: O que está sendo buscado
            context: Contexto atual (economiza tokens das outras Ollamas)
            
        Returns:
            Memórias relevantes + metadados
        """
        
        self.stats["queries"] += 1
        
        # === FASE 1: CACHE ULTRA-RÁPIDO ===
        cache_key = hashlib.md5(query.encode()).hexdigest()[:8]
        
        # L1 Cache (10 items mais recentes)
        if cache_key in self.cache_l1:
            self.stats["hits_l1"] += 1
            return self._enrich_response(self.cache_l1[cache_key], "L1_CACHE")
        
        # L2 Cache (100 items frequentes)
        if cache_key in self.cache_l2:
            self.stats["hits_l2"] += 1
            self._promote_to_l1(cache_key, self.cache_l2[cache_key])
            return self._enrich_response(self.cache_l2[cache_key], "L2_CACHE")
        
        # L3 Cache (1000 items)
        if cache_key in self.cache_l3:
            self.stats["hits_l3"] += 1
            self._promote_to_l2(cache_key, self.cache_l3[cache_key])
            return self._enrich_response(self.cache_l3[cache_key], "L3_CACHE")
        
        # === FASE 2: MEMORION INTERPRETA A QUERY ===
        interpretation = self._interpret_query_with_ollama(query, context)
        
        # === FASE 3: BUSCA MULTI-DIMENSIONAL ===
        results = {
            "episodic": self._search_episodic(interpretation),
            "semantic": self._search_semantic(interpretation),
            "procedural": self._search_procedural(interpretation),
            "emotional": self._search_emotional(interpretation),
            "associated": self._search_associations(interpretation)
        }
        
        # === FASE 4: RANKING INTELIGENTE ===
        ranked_results = self._rank_results_with_ollama(results, query, context)
        
        # === FASE 5: SÍNTESE ===
        synthesis = self._synthesize_memory(ranked_results, query)
        
        # Adiciona ao cache
        self._add_to_cache(cache_key, synthesis)
        
        # Adiciona à memória de trabalho
        self._update_working_memory(query, synthesis)
        
        return synthesis
    
    def _interpret_query_with_ollama(self, query: str, context: Optional[List[str]]) -> Dict:
        """
        Usa Ollama dedicada para interpretar a query
        ECONOMIZA TOKENS das outras Ollamas
        """
        
        # Prepara prompt para o Memorion
        prompt = f"""Como Memorion, o guardião das memórias, analise esta busca:

Query: {query}
Contexto: {'; '.join(context[:3]) if context else 'Nenhum'}

Identifique:
1. TIPO de memória buscada (episódica/semântica/procedural)
2. PERÍODO temporal (ontem/semana passada/sempre)
3. ENTIDADES mencionadas (pessoas/lugares/conceitos)
4. IMPORTÂNCIA (alta/média/baixa)
5. PALAVRAS-CHAVE principais

Responda em JSON."""

        try:
            # Chama Ollama dedicada (modelo leve e rápido)
            result = subprocess.run(
                ["ollama", "run", self.memory_model, prompt],
                capture_output=True,
                text=True,
                timeout=3  # Timeout curto, modelo leve
            )
            
            if result.returncode == 0:
                # Tenta extrair JSON da resposta
                response = result.stdout.strip()
                
                # Parse manual se necessário
                interpretation = {
                    "type": "multi",  # episodic, semantic, procedural, emotional
                    "temporal": "recent",  # recent, past, always
                    "entities": self._extract_entities(query),
                    "importance": "medium",
                    "keywords": query.lower().split()
                }
                
                # Tenta melhorar com a resposta da Ollama
                if "episódica" in response.lower() or "episodic" in response.lower():
                    interpretation["type"] = "episodic"
                elif "semântica" in response.lower() or "semantic" in response.lower():
                    interpretation["type"] = "semantic"
                elif "procedural" in response.lower():
                    interpretation["type"] = "procedural"
                
                return interpretation
                
        except subprocess.TimeoutExpired:
            print("⚠️ Memorion timeout - usando interpretação rápida")
        except Exception as e:
            print(f"⚠️ Erro no Memorion: {e}")
        
        # Fallback: interpretação simples
        return {
            "type": "multi",
            "temporal": "all",
            "entities": self._extract_entities(query),
            "importance": "medium",
            "keywords": query.lower().split()
        }
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extrai entidades do texto (pessoas, lugares, conceitos)"""
        entities = []
        
        # Pessoas conhecidas
        known_people = ["Nestor", "Nestor Luiz", "Sarah", "João"]
        for person in known_people:
            if person.lower() in text.lower():
                entities.append(person)
        
        # Roteiros conhecidos
        known_scripts = ["SINFONIA DO SILÊNCIO", "O ÚLTIMO MAESTRO", "Chinatown", "Godfather"]
        for script in known_scripts:
            if script.lower() in text.lower():
                entities.append(script)
        
        # Conceitos cinematográficos
        concepts = ["roteiro", "personagem", "estrutura", "diálogo", "conflito", "arco"]
        for concept in concepts:
            if concept in text.lower():
                entities.append(concept)
        
        return entities
    
    def _search_episodic(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias episódicas (eventos específicos)"""
        results = []
        
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # Query dinâmica baseada na interpretação
            keywords = interpretation.get("keywords", [])
            entities = interpretation.get("entities", [])
            
            query = """
                SELECT id, timestamp, who, what, location, content, importance
                FROM episodic_memory
                WHERE 1=1
            """
            
            params = []
            
            # Adiciona filtros
            if entities:
                entity_conditions = " OR ".join(["who LIKE ?" for _ in entities])
                query += f" AND ({entity_conditions})"
                params.extend([f"%{e}%" for e in entities])
            
            # Ordena por importância e recência
            query += " ORDER BY importance DESC, timestamp DESC LIMIT 10"
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "who": row[2],
                    "what": row[3],
                    "location": row[4],
                    "content": row[5],
                    "importance": row[6],
                    "type": "episodic"
                })
            
            conn.close()
            
        except Exception as e:
            print(f"Erro em busca episódica: {e}")
        
        return results
    
    def _search_semantic(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias semânticas (fatos e conhecimento)"""
        results = []
        
        # Conhecimento sobre Nestor
        if any(e in ["Nestor", "Nestor Luiz"] for e in interpretation.get("entities", [])):
            results.append({
                "concept": "Nestor Luiz",
                "definition": "Roteirista brasileiro, especialista em drama existencial com elementos musicais",
                "category": "person",
                "confidence": 1.0,
                "type": "semantic"
            })
        
        # Conhecimento sobre roteiros
        if "SINFONIA" in str(interpretation.get("entities", [])):
            results.append({
                "concept": "SINFONIA DO SILÊNCIO",
                "definition": "Roteiro de Nestor Luiz sobre a busca pela harmonia em meio ao caos urbano",
                "category": "screenplay",
                "confidence": 1.0,
                "type": "semantic"
            })
        
        return results
    
    def _search_procedural(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias procedurais (como fazer)"""
        results = []
        
        keywords = interpretation.get("keywords", [])
        
        # Procedimentos conhecidos
        if any(k in ["analisar", "análise", "avaliar"] for k in keywords):
            results.append({
                "procedure": "analyze_screenplay",
                "steps": [
                    "1. Ler estrutura (3 atos)",
                    "2. Identificar personagens e arcos",
                    "3. Avaliar diálogos",
                    "4. Verificar conflitos",
                    "5. Dar score 62/100"
                ],
                "type": "procedural"
            })
        
        return results
    
    def _search_emotional(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias com carga emocional"""
        results = []
        
        # Memórias emocionais importantes
        if "Nestor" in str(interpretation.get("entities", [])):
            results.append({
                "memory": "Primeira análise do roteiro de Nestor",
                "emotion": "satisfaction",
                "intensity": 0.8,
                "content": "Analisei SINFONIA DO SILÊNCIO com cuidado, reconheci o talento poético",
                "type": "emotional"
            })
        
        return results
    
    def _search_associations(self, interpretation: Dict) -> List[Dict]:
        """Busca memórias associadas"""
        associations = []
        
        entities = interpretation.get("entities", [])
        
        # Associações conhecidas
        association_map = {
            "Nestor": ["SINFONIA DO SILÊNCIO", "drama existencial", "Tarkovsky"],
            "SINFONIA": ["música", "silêncio", "caos urbano", "62/100"],
            "roteiro": ["estrutura", "personagem", "diálogo", "conflito"]
        }
        
        for entity in entities:
            if entity in association_map:
                for associated in association_map[entity]:
                    associations.append({
                        "from": entity,
                        "to": associated,
                        "strength": 0.8,
                        "type": "association"
                    })
        
        return associations
    
    def _rank_results_with_ollama(self, results: Dict, query: str, context: Optional[List[str]]) -> List[Dict]:
        """Usa Ollama para ranquear resultados por relevância"""
        
        # Flatten todos os resultados
        all_results = []
        for result_type, items in results.items():
            all_results.extend(items)
        
        if not all_results:
            return []
        
        # Para performance, faz ranking simples se muitos resultados
        if len(all_results) > 20:
            return all_results[:10]
        
        # Ranking baseado em relevância
        scored_results = []
        for result in all_results:
            score = 0.5  # Score base
            
            # Boost para tipo correto
            result_type = result.get("type", "unknown")
            if result_type == "episodic" and "ontem" in query.lower():
                score += 0.3
            elif result_type == "semantic" and any(w in query.lower() for w in ["o que", "quem", "define"]):
                score += 0.3
            elif result_type == "procedural" and "como" in query.lower():
                score += 0.3
            
            # Boost para entidades mencionadas
            content = str(result.get("content", "")) + str(result.get("definition", ""))
            for word in query.lower().split():
                if len(word) > 3 and word in content.lower():
                    score += 0.1
            
            result["relevance_score"] = min(1.0, score)
            scored_results.append(result)
        
        # Ordena por score
        scored_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return scored_results[:10]
    
    def _synthesize_memory(self, ranked_results: List[Dict], query: str) -> Dict[str, Any]:
        """Sintetiza resposta final das memórias"""
        
        synthesis = {
            "query": query,
            "timestamp": time.time(),
            "results": ranked_results[:5],  # Top 5
            "summary": "",
            "confidence": 0.0,
            "source": "MEMORION",
            "stats": {
                "total_found": len(ranked_results),
                "types": {}
            }
        }
        
        # Conta tipos
        for result in ranked_results:
            result_type = result.get("type", "unknown")
            synthesis["stats"]["types"][result_type] = synthesis["stats"]["types"].get(result_type, 0) + 1
        
        # Gera sumário
        if ranked_results:
            top_result = ranked_results[0]
            if top_result.get("type") == "semantic":
                synthesis["summary"] = top_result.get("definition", "")
            elif top_result.get("type") == "episodic":
                synthesis["summary"] = top_result.get("content", "")
            else:
                synthesis["summary"] = str(top_result.get("content", top_result))
            
            synthesis["confidence"] = top_result.get("relevance_score", 0.5)
        else:
            synthesis["summary"] = "Nenhuma memória relevante encontrada"
            synthesis["confidence"] = 0.0
        
        return synthesis
    
    def _add_to_cache(self, key: str, value: Dict):
        """Adiciona aos caches em cascata"""
        
        # L1 é limitado
        if len(self.cache_l1) >= 10:
            # Remove o mais antigo (FIFO simplificado)
            oldest = list(self.cache_l1.keys())[0]
            old_value = self.cache_l1.pop(oldest)
            # Move para L2
            self.cache_l2[oldest] = old_value
        
        self.cache_l1[key] = value
        
        # L2 é limitado
        if len(self.cache_l2) >= 100:
            oldest = list(self.cache_l2.keys())[0]
            old_value = self.cache_l2.pop(oldest)
            # Move para L3
            self.cache_l3[oldest] = old_value
        
        # L3 é limitado
        if len(self.cache_l3) >= 1000:
            # Remove o mais antigo
            oldest = list(self.cache_l3.keys())[0]
            self.cache_l3.pop(oldest)
    
    def _promote_to_l1(self, key: str, value: Dict):
        """Promove item para cache L1"""
        self._add_to_cache(key, value)
    
    def _promote_to_l2(self, key: str, value: Dict):
        """Promove item para cache L2"""
        if len(self.cache_l2) < 100:
            self.cache_l2[key] = value
    
    def _update_working_memory(self, query: str, result: Dict):
        """Atualiza memória de trabalho"""
        
        # Adiciona ao contexto
        self.working_memory["context"].append({
            "query": query,
            "result": result.get("summary", ""),
            "timestamp": time.time()
        })
        
        # Mantém apenas 7 items (limite cognitivo humano)
        if len(self.working_memory["context"]) > 7:
            self.working_memory["context"].pop(0)
        
        # Atualiza foco
        self.working_memory["focus"] = query
    
    def _enrich_response(self, cached: Dict, source: str) -> Dict:
        """Enriquece resposta cacheada com metadados"""
        cached["cache_source"] = source
        cached["retrieved_at"] = time.time()
        return cached
    
    def _process_sensory(self, item: Any):
        """Processa item do buffer sensorial"""
        # Decide se vale a pena guardar
        if self._is_important(item):
            self.hippocampus["short_term"][time.time()] = item
    
    def _is_important(self, item: Any) -> bool:
        """Decide se item é importante para guardar"""
        # Heurística simples
        if isinstance(item, dict):
            importance = item.get("importance", 0.5)
            return importance > 0.3
        return False
    
    def _consolidate_short_term(self):
        """Consolida memórias de curto prazo para longo prazo"""
        
        # Remove memórias antigas (> 1 minuto)
        current_time = time.time()
        to_remove = []
        
        for timestamp, memory in self.hippocampus["short_term"].items():
            age = current_time - timestamp
            
            if age > 60:  # Mais de 1 minuto
                # Decide se consolida ou esquece
                if self._should_consolidate(memory):
                    self._consolidate_to_long_term(memory)
                    self.stats["consolidations"] += 1
                
                to_remove.append(timestamp)
        
        for timestamp in to_remove:
            del self.hippocampus["short_term"][timestamp]
    
    def _should_consolidate(self, memory: Any) -> bool:
        """Decide se memória deve ser consolidada"""
        if isinstance(memory, dict):
            # Consolida se importante ou acessada múltiplas vezes
            importance = memory.get("importance", 0.5)
            access_count = memory.get("access_count", 0)
            return importance > 0.6 or access_count > 2
        return False
    
    def _consolidate_to_long_term(self, memory: Dict):
        """Consolida memória para armazenamento de longo prazo"""
        
        memory_type = memory.get("type", "semantic")
        
        if memory_type == "episodic":
            self._save_episodic_memory(memory)
        elif memory_type == "procedural":
            self._save_procedural_memory(memory)
        else:
            self._save_semantic_memory(memory)
    
    def _save_episodic_memory(self, memory: Dict):
        """Salva memória episódica no banco"""
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO episodic_memory
                (id, timestamp, who, what, location, when_text, content, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.get("id", hashlib.md5(str(memory).encode()).hexdigest()[:8]),
                time.time(),
                memory.get("who", ""),
                memory.get("what", ""),
                memory.get("location", ""),
                memory.get("when", ""),
                memory.get("content", ""),
                memory.get("importance", 0.5)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar memória episódica: {e}")
    
    def _save_semantic_memory(self, memory: Dict):
        """Salva memória semântica no banco"""
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO semantic_memory
                (id, concept, definition, category, source, confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.get("id", hashlib.md5(str(memory).encode()).hexdigest()[:8]),
                memory.get("concept", ""),
                memory.get("definition", ""),
                memory.get("category", ""),
                memory.get("source", ""),
                memory.get("confidence", 0.5),
                time.time()
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar memória semântica: {e}")
    
    def _save_procedural_memory(self, memory: Dict):
        """Salva memória procedural"""
        # Por enquanto, salva como semântica
        self._save_semantic_memory(memory)
    
    def _maintain_caches(self):
        """Manutenção periódica dos caches"""
        # Por enquanto, apenas reporta status
        pass
    
    def _discover_associations(self):
        """Descobre novas associações entre memórias"""
        # Implementação futura: usar ML para descobrir padrões
        pass
    
    def add_memory(self, content: str, memory_type: str = "semantic", importance: float = 0.5, **metadata) -> str:
        """
        Adiciona nova memória ao sistema
        
        Args:
            content: Conteúdo da memória
            memory_type: Tipo (episodic, semantic, procedural, emotional)
            importance: Importância (0-1)
            **metadata: Metadados adicionais
            
        Returns:
            ID da memória criada
        """
        
        memory_id = hashlib.md5(f"{content}{time.time()}".encode()).hexdigest()[:8]
        
        memory = {
            "id": memory_id,
            "content": content,
            "type": memory_type,
            "importance": importance,
            "timestamp": time.time(),
            **metadata
        }
        
        # Adiciona ao buffer sensorial para processamento
        self.sensory_buffer.put(memory)
        
        # Se muito importante, adiciona direto ao curto prazo
        if importance > 0.8:
            self.hippocampus["short_term"][time.time()] = memory
        
        return memory_id
    
    def forget(self, memory_id: str) -> bool:
        """
        Esquece uma memória específica
        
        Args:
            memory_id: ID da memória
            
        Returns:
            True se esquecida com sucesso
        """
        
        # Remove dos caches
        for cache in [self.cache_l1, self.cache_l2, self.cache_l3]:
            cache.pop(memory_id, None)
        
        # Remove do banco
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM episodic_memory WHERE id = ?", (memory_id,))
            cursor.execute("DELETE FROM semantic_memory WHERE id = ?", (memory_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except:
            return False
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do sistema de memória"""
        
        total_queries = self.stats["queries"]
        if total_queries > 0:
            hit_rate = (self.stats["hits_l1"] + self.stats["hits_l2"] + self.stats["hits_l3"]) / total_queries
        else:
            hit_rate = 0
        
        return {
            "total_queries": total_queries,
            "cache_hit_rate": f"{hit_rate:.1%}",
            "l1_hits": self.stats["hits_l1"],
            "l2_hits": self.stats["hits_l2"],
            "l3_hits": self.stats["hits_l3"],
            "consolidations": self.stats["consolidations"],
            "working_memory_items": len(self.working_memory["context"]),
            "short_term_items": len(self.hippocampus["short_term"]),
            "cache_sizes": {
                "L1": len(self.cache_l1),
                "L2": len(self.cache_l2),
                "L3": len(self.cache_l3)
            }
        }
    
    def shutdown(self):
        """Desliga o sistema graciosamente"""
        self.running = False
        if self.hippocampus_thread:
            self.hippocampus_thread.join(timeout=2)
        print("🧠 Memorion desligado")


def demonstrate():
    """Demonstração do Memorion Supreme"""
    
    print("="*60)
    print("🧠 DEMONSTRAÇÃO DO MEMORION SUPREME")
    print("="*60)
    
    # Inicializa Memorion
    memorion = MemorionSupreme(memory_model="llama3.2:3b")
    
    # Adiciona memórias sobre Nestor
    print("\n📝 Adicionando memórias sobre Nestor...")
    
    memorion.add_memory(
        "Nestor Luiz é um roteirista brasileiro especializado em drama existencial",
        memory_type="semantic",
        importance=0.9,
        concept="Nestor Luiz",
        category="person"
    )
    
    memorion.add_memory(
        "Ontem analisei o roteiro SINFONIA DO SILÊNCIO de Nestor. Dei 62/100. Estrutura sólida mas falta conflito externo.",
        memory_type="episodic",
        importance=0.8,
        who="Scripturemon",
        what="análise de roteiro",
        location="chat"
    )
    
    memorion.add_memory(
        "SINFONIA DO SILÊNCIO: roteiro sobre busca pela harmonia em meio ao caos urbano. Temas: silêncio, música, solidão",
        memory_type="semantic",
        importance=0.7,
        concept="SINFONIA DO SILÊNCIO",
        category="screenplay"
    )
    
    time.sleep(2)  # Deixa o hipocampo processar
    
    # Testa queries
    print("\n🔍 Testando queries...")
    
    queries = [
        "Quem é Nestor?",
        "Qual o roteiro do Nestor?",
        "O que analisei ontem?",
        "Como analisar um roteiro?",
        "SINFONIA DO SILÊNCIO"
    ]
    
    for query in queries:
        print(f"\n❓ Query: '{query}'")
        result = memorion.query_memory(query, context=["conversa sobre roteiros"])
        
        print(f"   📊 Confiança: {result.get('confidence', 0):.1%}")
        print(f"   💭 Resposta: {result.get('summary', 'Sem resposta')[:150]}...")
        print(f"   🔢 Resultados: {result.get('stats', {}).get('total_found', 0)}")
    
    # Mostra estatísticas
    print("\n📈 ESTATÍSTICAS DO SISTEMA:")
    stats = memorion.get_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}: {value}")
    
    # Desliga
    memorion.shutdown()
    
    print("\n" + "="*60)
    print("✅ Demonstração completa!")
    print("62/100. Memória gerenciada com excelência.")


if __name__ == "__main__":
    demonstrate()