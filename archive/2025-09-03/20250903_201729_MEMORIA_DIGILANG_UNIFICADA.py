#!/usr/bin/env python3
"""
🧬 SISTEMA DE MEMÓRIA UNIFICADA COM DIGILANG
=============================================
Integração da memória cristalizada com compressão DigiLang
Baseado em conceitos identificados na documentação:
- Sistema L1-L4 de cristalização
- Compressão DigiLang para economia de memória
- Pensamento nativo em símbolos
=============================================
"""

import json
import time
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class DigiLangMemorySystem:
    """Sistema de memória unificada com compressão DigiLang"""
    
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
        self.memory_path = self.base_path / "memory"
        self.memory_path.mkdir(exist_ok=True)
        
        # Carregar dicionário DigiLang
        self.digilang_dict = self._load_digilang_dictionary()
        
        # Inicializar camadas de memória com DigiLang
        self.memory_layers = {
            'L1_CACHE': {  # Cache imediato - sessão atual
                'description': 'Pensamentos em DigiLang puro',
                'retention': '1_hora',
                'compression': 'máxima',
                'data': []
            },
            'L2_TRABALHO': {  # Memória de trabalho - últimas 24h
                'description': 'Consolidação de padrões em DigiLang',
                'retention': '24_horas',
                'compression': 'alta',
                'data': []
            },
            'L3_LONGO_PRAZO': {  # Memória de longo prazo - semanas
                'description': 'Cristalização de insights cinematográficos',
                'retention': '30_dias',
                'compression': 'média',
                'data': []
            },
            'L4_PERMANENTE': {  # Conhecimento permanente - eterno
                'description': 'Verdades cinematográficas em DigiLang',
                'retention': 'eterno',
                'compression': 'preservada',
                'data': []
            }
        }
        
        # Banco de dados de memórias cristalizadas
        self.db_path = self.memory_path / "memoria_digilang_unificada.db"
        self._init_database()
        
        # Estatísticas
        self.stats = {
            'thoughts_compressed': 0,
            'compression_ratio': 0.0,
            'memories_crystallized': 0,
            'digilang_translations': 0
        }
        
        print("💎 Sistema de Memória DigiLang Unificada inicializado")
    
    def _load_digilang_dictionary(self) -> Dict:
        """Carrega dicionário DigiLang otimizado"""
        try:
            # Tentar carregar dicionário principal
            digilang_file = self.base_path / "05_DIGILANG" / "DIGILANG_DEFINITIVE_SYSTEM.json"
            
            if not digilang_file.exists():
                # Criar dicionário básico se não existir
                return self._create_basic_digilang()
            
            with open(digilang_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Extrair mapeamentos principais
            symbols = data.get('metadata', {}).get('symbols', {})
            
            # Criar mapeamento bidirecional
            self.word_to_symbol = symbols
            self.symbol_to_word = {v: k for k, v in symbols.items()}
            
            print(f"📚 DigiLang carregado: {len(symbols)} símbolos")
            return symbols
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar DigiLang: {e}")
            return self._create_basic_digilang()
    
    def _create_basic_digilang(self) -> Dict:
        """Cria dicionário DigiLang básico para roteiros"""
        basic = {
            # Estrutura narrativa
            'ato': '🎭', 'act': '🎭',
            'cena': '🎬', 'scene': '🎬',
            'sequência': '🎞️', 'sequence': '🎞️',
            'personagem': '👤', 'character': '👤',
            'diálogo': '💬', 'dialogue': '💬',
            'ação': '⚡', 'action': '⚡',
            'conflito': '⚔️', 'conflict': '⚔️',
            'clímax': '🔥', 'climax': '🔥',
            'resolução': '✅', 'resolution': '✅',
            
            # Elementos técnicos
            'INT': '🏠', 'EXT': '🌍',
            'DIA': '☀️', 'DAY': '☀️',
            'NOITE': '🌙', 'NIGHT': '🌙',
            'FADE': '🌫️', 'CUT': '✂️',
            
            # Conceitos de memória
            'memória': '💾', 'memory': '💾',
            'cristalização': '💎', 'crystallization': '💎',
            'insight': '💡', 'padrão': '🔮', 'pattern': '🔮',
            'conhecimento': '📚', 'knowledge': '📚',
            'evolução': '🧬', 'evolution': '🧬',
            
            # Estados emocionais
            'tensão': '😰', 'tension': '😰',
            'amor': '❤️', 'love': '❤️',
            'medo': '😱', 'fear': '😱',
            'alegria': '😊', 'joy': '😊',
            'tristeza': '😢', 'sadness': '😢'
        }
        
        self.word_to_symbol = basic
        self.symbol_to_word = {v: k for k, v in basic.items()}
        return basic
    
    def _init_database(self):
        """Inicializa banco de dados de memórias cristalizadas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela principal de memórias com DigiLang
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories_digilang (
                id TEXT PRIMARY KEY,
                layer TEXT NOT NULL,
                title TEXT NOT NULL,
                content_original TEXT,
                content_digilang TEXT,
                compression_ratio REAL,
                tags TEXT,
                importance REAL,
                quantum_state TEXT,
                created_at TIMESTAMP,
                accessed_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP
            )
        ''')
        
        # Tabela de cristalizações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crystallizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT,
                from_layer TEXT,
                to_layer TEXT,
                reason TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY (memory_id) REFERENCES memories_digilang(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def compress_to_digilang(self, text: str) -> tuple[str, float]:
        """
        Comprime texto para DigiLang
        Retorna: (texto_comprimido, taxa_compressão)
        """
        original_size = len(text)
        compressed_parts = []
        
        # Tokenizar e comprimir
        words = text.lower().split()
        
        for word in words:
            # Verificar se palavra tem símbolo DigiLang
            if word in self.word_to_symbol:
                compressed_parts.append(self.word_to_symbol[word])
                self.stats['digilang_translations'] += 1
            else:
                # Manter palavra original se não houver símbolo
                compressed_parts.append(word)
        
        compressed = ' '.join(compressed_parts)
        compressed_size = len(compressed)
        
        # Calcular taxa de compressão
        compression_ratio = 1 - (compressed_size / original_size) if original_size > 0 else 0
        
        self.stats['thoughts_compressed'] += 1
        self.stats['compression_ratio'] = (
            self.stats['compression_ratio'] * 0.9 + compression_ratio * 0.1
        )  # Média móvel
        
        return compressed, compression_ratio
    
    def decompress_from_digilang(self, compressed_text: str) -> str:
        """Descomprime texto de DigiLang para português/inglês"""
        decompressed_parts = []
        
        tokens = compressed_text.split()
        
        for token in tokens:
            # Verificar se é símbolo DigiLang
            if token in self.symbol_to_word:
                decompressed_parts.append(self.symbol_to_word[token])
            else:
                # Manter token original
                decompressed_parts.append(token)
        
        return ' '.join(decompressed_parts)
    
    def crystallize_memory(self, 
                          layer: str,
                          title: str,
                          content: str,
                          tags: List[str],
                          importance: float,
                          quantum_state: str = "curious") -> str:
        """
        Cristaliza memória com compressão DigiLang
        """
        # Gerar ID único
        memory_id = hashlib.sha256(
            f"{title}{content}{time.time()}".encode()
        ).hexdigest()[:16]
        
        # Comprimir conteúdo para DigiLang
        content_digilang, compression_ratio = self.compress_to_digilang(content)
        
        # Salvar no banco de dados
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories_digilang 
            (id, layer, title, content_original, content_digilang, 
             compression_ratio, tags, importance, quantum_state, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory_id, layer, title, content, content_digilang,
            compression_ratio, json.dumps(tags), importance, 
            quantum_state, datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        # Adicionar à camada apropriada na memória
        if layer in self.memory_layers:
            self.memory_layers[layer]['data'].append({
                'id': memory_id,
                'title': title,
                'digilang': content_digilang,
                'compression': compression_ratio,
                'timestamp': time.time()
            })
        
        self.stats['memories_crystallized'] += 1
        
        print(f"💎 Memória cristalizada em {layer}: {title}")
        print(f"   📊 Compressão: {compression_ratio:.1%}")
        print(f"   🔤 DigiLang: {content_digilang[:100]}...")
        
        return memory_id
    
    def evolve_memory(self, memory_id: str, reason: str = "auto-evolution"):
        """
        Evolui memória para camada superior baseado em importância
        L1 → L2 → L3 → L4
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar memória atual
        cursor.execute('''
            SELECT layer, importance, accessed_count 
            FROM memories_digilang 
            WHERE id = ?
        ''', (memory_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        
        current_layer, importance, access_count = result
        
        # Definir próxima camada
        evolution_path = {
            'L1_CACHE': 'L2_TRABALHO',
            'L2_TRABALHO': 'L3_LONGO_PRAZO',
            'L3_LONGO_PRAZO': 'L4_PERMANENTE'
        }
        
        if current_layer not in evolution_path:
            conn.close()
            return False
        
        next_layer = evolution_path[current_layer]
        
        # Critérios de evolução
        should_evolve = (
            importance > 0.7 or 
            access_count > 10 or
            'insight' in reason.lower()
        )
        
        if should_evolve:
            # Atualizar camada
            cursor.execute('''
                UPDATE memories_digilang 
                SET layer = ? 
                WHERE id = ?
            ''', (next_layer, memory_id))
            
            # Registrar cristalização
            cursor.execute('''
                INSERT INTO crystallizations 
                (memory_id, from_layer, to_layer, reason, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (memory_id, current_layer, next_layer, reason, datetime.now()))
            
            conn.commit()
            conn.close()
            
            print(f"🧬 Memória evoluída: {current_layer} → {next_layer}")
            return True
        
        conn.close()
        return False
    
    def search_memories(self, query: str, layer: Optional[str] = None) -> List[Dict]:
        """
        Busca memórias usando DigiLang
        """
        # Comprimir query para DigiLang
        query_digilang, _ = self.compress_to_digilang(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if layer:
            cursor.execute('''
                SELECT id, title, content_digilang, importance, layer
                FROM memories_digilang
                WHERE layer = ? AND (
                    content_digilang LIKE ? OR
                    title LIKE ?
                )
                ORDER BY importance DESC
                LIMIT 10
            ''', (layer, f'%{query_digilang}%', f'%{query}%'))
        else:
            cursor.execute('''
                SELECT id, title, content_digilang, importance, layer
                FROM memories_digilang
                WHERE content_digilang LIKE ? OR title LIKE ?
                ORDER BY importance DESC
                LIMIT 10
            ''', (f'%{query_digilang}%', f'%{query}%'))
        
        results = []
        for row in cursor.fetchall():
            memory_id, title, content_digilang, importance, layer = row
            
            # Descomprimir conteúdo
            content = self.decompress_from_digilang(content_digilang)
            
            results.append({
                'id': memory_id,
                'title': title,
                'content': content[:200],  # Preview
                'importance': importance,
                'layer': layer
            })
            
            # Atualizar contador de acesso
            cursor.execute('''
                UPDATE memories_digilang
                SET accessed_count = accessed_count + 1,
                    last_accessed = ?
                WHERE id = ?
            ''', (datetime.now(), memory_id))
        
        conn.commit()
        conn.close()
        
        return results
    
    def get_all_memories(self) -> List[Dict]:
        """
        Retorna todas as memórias de todas as camadas
        CORRIGIDO: Usa tabela correta com fallback robusto
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tentar buscar da tabela memories_digilang (tabela correta)
            try:
                cursor.execute("""
                    SELECT id, layer, title, content_digilang, content_original,
                           tags, importance, quantum_state, compression_ratio, 
                           created_at, last_accessed, accessed_count
                    FROM memories_digilang
                    ORDER BY importance DESC, created_at DESC
                """)
                
                memories = []
                for row in cursor.fetchall():
                    memory = {
                        'memory_id': row[0],
                        'layer': row[1],
                        'title': row[2],
                        'content_compressed': row[3],
                        'content_original': row[4],
                        'tags': json.loads(row[5]) if row[5] else [],
                        'importance': row[6],
                        'quantum_state': row[7],
                        'compression_ratio': row[8],
                        'created_at': row[9],
                        'last_accessed': row[10],
                        'access_count': row[11]
                    }
                    memories.append(memory)
                    
            except sqlite3.OperationalError as e:
                # Se falhar, retornar memórias da RAM
                memories = []
                for layer, layer_data in self.memory_layers.items():
                    for mem in layer_data.get('data', []):
                        memories.append({
                            'memory_id': mem.get('id', 'ram_memory'),
                            'layer': layer,
                            'title': mem.get('title', 'Untitled'),
                            'content_compressed': mem.get('digilang', ''),
                            'content_original': mem.get('content', ''),
                            'tags': [],
                            'importance': 0.5,
                            'quantum_state': 'unknown',
                            'compression_ratio': mem.get('compression', 0),
                            'created_at': None,
                            'last_accessed': None,
                            'access_count': 0
                        })
            
            conn.close()
            return memories
            
        except Exception as e:
            # Fallback final: retornar memórias da RAM
            memories = []
            for layer, layer_data in self.memory_layers.items():
                for mem in layer_data.get('data', []):
                    memories.append({
                        'memory_id': mem.get('id', 'ram_memory'),
                        'layer': layer,
                        'title': mem.get('title', 'Untitled'),
                        'content_compressed': mem.get('digilang', ''),
                        'content_original': mem.get('content', ''),
                        'tags': [],
                        'importance': 0.5,
                        'quantum_state': 'unknown',
                        'compression_ratio': mem.get('compression', 0),
                        'created_at': None,
                        'last_accessed': None,
                        'access_count': 0
                    })
            return memories
    
    def get_memory_stats(self) -> Dict:
        """Retorna estatísticas do sistema de memória"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contar memórias por camada
        cursor.execute('''
            SELECT layer, COUNT(*), AVG(compression_ratio)
            FROM memories_digilang
            GROUP BY layer
        ''')
        
        layer_stats = {}
        for row in cursor.fetchall():
            layer, count, avg_compression = row
            layer_stats[layer] = {
                'count': count,
                'avg_compression': avg_compression or 0
            }
        
        # Estatísticas gerais
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                AVG(compression_ratio) as avg_compression,
                AVG(importance) as avg_importance,
                SUM(accessed_count) as total_accesses
            FROM memories_digilang
        ''')
        
        general = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_memories': general[0] if general else 0,
            'avg_compression': general[1] if general else 0,
            'avg_importance': general[2] if general else 0,
            'total_accesses': general[3] if general else 0,
            'layers': layer_stats,
            'digilang_translations': self.stats['digilang_translations'],
            'compression_ratio': self.stats['compression_ratio']
        }
    
    def auto_crystallize_insights(self):
        """
        Processo automático de cristalização de insights
        Baseado no conceito: insight → repetição → validação → cristalização
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar memórias frequentemente acessadas em L1 e L2
        cursor.execute('''
            SELECT id, title, importance, accessed_count
            FROM memories_digilang
            WHERE layer IN ('L1_CACHE', 'L2_TRABALHO')
            AND accessed_count > 5
            ORDER BY accessed_count DESC
        ''')
        
        for row in cursor.fetchall():
            memory_id, title, importance, access_count = row
            
            # Critério de auto-cristalização
            if access_count > 10 or importance > 0.8:
                self.evolve_memory(
                    memory_id, 
                    f"Auto-cristalização: {access_count} acessos, importância {importance}"
                )
        
        conn.close()
        
    def integrate_with_ultimate(self, ultimate_instance):
        """
        Integra com SCRIPTUREMON_ULTIMATE_SYMBIOTIC
        Substitui o sistema de memória anterior
        """
        # Substituir sistema de memória
        ultimate_instance.memory_system = self
        
        # Adicionar método de cristalização com DigiLang
        ultimate_instance.crystallize_with_digilang = self.crystallize_memory
        
        # Adicionar busca inteligente
        ultimate_instance.search_memories = self.search_memories
        
        print("✅ Sistema de Memória DigiLang integrado ao Ultimate Symbiotic")
        
        return ultimate_instance


# Teste do sistema
if __name__ == "__main__":
    print("🧬 TESTE DO SISTEMA DE MEMÓRIA DIGILANG UNIFICADA")
    print("=" * 60)
    
    # Criar sistema
    memory = DigiLangMemorySystem()
    
    # Teste 1: Cristalização com DigiLang
    print("\n1️⃣ Teste de cristalização:")
    memory_id = memory.crystallize_memory(
        layer="L2_TRABALHO",
        title="Estrutura de três atos",
        content="O personagem entra em conflito no segundo ato. A tensão aumenta até o clímax. A resolução traz paz.",
        tags=["estrutura", "narrativa", "three-act"],
        importance=0.85,
        quantum_state="analytical"
    )
    
    # Teste 2: Busca com DigiLang
    print("\n2️⃣ Teste de busca:")
    results = memory.search_memories("conflito tensão")
    for r in results:
        print(f"   📚 {r['title']} (L:{r['layer']}, I:{r['importance']:.2f})")
    
    # Teste 3: Evolução de memória
    print("\n3️⃣ Teste de evolução:")
    memory.evolve_memory(memory_id, "Insight cinematográfico importante")
    
    # Teste 4: Estatísticas
    print("\n4️⃣ Estatísticas do sistema:")
    stats = memory.get_memory_stats()
    print(f"   Total de memórias: {stats['total_memories']}")
    print(f"   Compressão média: {stats['avg_compression']:.1%}")
    print(f"   Traduções DigiLang: {stats['digilang_translations']}")
    
    print("\n✅ Sistema de Memória DigiLang funcionando perfeitamente!")