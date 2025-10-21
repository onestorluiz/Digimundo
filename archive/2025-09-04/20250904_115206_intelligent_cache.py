#!/usr/bin/env python3
"""
🧠 INTELLIGENT CACHE SYSTEM - Cache Multi-Nível EXTREMAMENTE ROBUSTO
Sistema avançado de cache com LRU, TTL, compressão e predição
"""

import time
import json
import pickle
import hashlib
import zlib
import asyncio
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
import threading
import sqlite3

class IntelligentCache:
    """Sistema de cache multi-nível com inteligência preditiva"""
    
    def __init__(self, base_path: Path = None, max_memory_mb: int = 500):
        self.base_path = base_path or Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
        self.cache_path = self.base_path / "runtime" / "cache"
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Configurações ROBUSTAS
        self.max_memory_mb = max_memory_mb
        self.current_memory_usage = 0
        
        # Cache L1 - Memória (Hot Cache) - Ultra rápido
        self.l1_cache = OrderedDict()
        self.l1_max_items = 1000
        self.l1_ttl = 300  # 5 minutos
        
        # Cache L2 - Memória comprimida (Warm Cache)
        self.l2_cache = OrderedDict()
        self.l2_max_items = 5000
        self.l2_ttl = 3600  # 1 hora
        
        # Cache L3 - Disco SQLite (Cold Cache)
        self.l3_db = self.cache_path / "l3_cache.db"
        self._init_l3_cache()
        self.l3_ttl = 86400  # 24 horas
        
        # Estatísticas ROBUSTAS
        self.stats = {
            'hits': defaultdict(int),  # Por nível
            'misses': defaultdict(int),
            'evictions': defaultdict(int),
            'compressions': 0,
            'decompressions': 0,
            'total_saved_bytes': 0
        }
        
        # Preditor de acesso (Machine Learning simples)
        self.access_patterns = defaultdict(lambda: {
            'count': 0,
            'last_access': 0,
            'avg_interval': 0,
            'predictions': []
        })
        
        # Thread de manutenção
        self.maintenance_thread = threading.Thread(
            target=self._maintenance_worker,
            daemon=True
        )
        self.maintenance_thread.start()
        
        print("🧠 Sistema de Cache Inteligente inicializado")
        print(f"   L1: {self.l1_max_items} items (5min TTL)")
        print(f"   L2: {self.l2_max_items} items comprimidos (1h TTL)")
        print(f"   L3: SQLite persistente (24h TTL)")
    
    def _init_l3_cache(self):
        """Inicializa cache L3 em SQLite"""
        conn = sqlite3.connect(str(self.l3_db))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache_entries (
                key TEXT PRIMARY KEY,
                value BLOB,
                compressed BOOLEAN,
                size_bytes INTEGER,
                created_at REAL,
                accessed_at REAL,
                access_count INTEGER DEFAULT 1,
                ttl INTEGER,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_accessed_at 
            ON cache_entries(accessed_at DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ttl 
            ON cache_entries(created_at, ttl)
        """)
        
        conn.commit()
        conn.close()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Busca valor no cache multi-nível
        L1 -> L2 -> L3 -> default
        """
        key_hash = self._hash_key(key)
        
        # Registrar padrão de acesso
        self._record_access_pattern(key_hash)
        
        # L1 - Hot cache
        if key_hash in self.l1_cache:
            entry = self.l1_cache[key_hash]
            if time.time() < entry['expires_at']:
                # Move to end (LRU)
                self.l1_cache.move_to_end(key_hash)
                self.stats['hits']['L1'] += 1
                return entry['value']
            else:
                # Expirado
                del self.l1_cache[key_hash]
                self.stats['evictions']['L1'] += 1
        
        # L2 - Warm cache (comprimido)
        if key_hash in self.l2_cache:
            entry = self.l2_cache[key_hash]
            if time.time() < entry['expires_at']:
                # Descomprimir
                value = self._decompress(entry['compressed_value'])
                self.stats['decompressions'] += 1
                
                # Promover para L1
                self._promote_to_l1(key_hash, value)
                
                # Move to end (LRU)
                self.l2_cache.move_to_end(key_hash)
                self.stats['hits']['L2'] += 1
                return value
            else:
                del self.l2_cache[key_hash]
                self.stats['evictions']['L2'] += 1
        
        # L3 - Cold cache (SQLite)
        value = self._get_from_l3(key_hash)
        if value is not None:
            # Promover para L1 e L2
            self._promote_to_l1(key_hash, value)
            self._promote_to_l2(key_hash, value)
            self.stats['hits']['L3'] += 1
            return value
        
        # Cache miss
        self.stats['misses']['total'] += 1
        return default
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Define valor no cache multi-nível com TTL customizado
        """
        key_hash = self._hash_key(key)
        
        # Calcular tamanho
        try:
            serialized = pickle.dumps(value)
            size_bytes = len(serialized)
        except:
            return False
        
        # Verificar limite de memória
        if self._estimate_memory_usage() + size_bytes > self.max_memory_mb * 1024 * 1024:
            self._evict_lru()
        
        # L1 - Sempre adicionar em hot cache
        ttl_l1 = min(ttl or self.l1_ttl, self.l1_ttl)
        self.l1_cache[key_hash] = {
            'value': value,
            'expires_at': time.time() + ttl_l1,
            'size_bytes': size_bytes
        }
        
        # Aplicar limite LRU em L1
        if len(self.l1_cache) > self.l1_max_items:
            # Remover mais antigo
            oldest = next(iter(self.l1_cache))
            old_entry = self.l1_cache.pop(oldest)
            
            # Demote para L2
            self._promote_to_l2(oldest, old_entry['value'])
            self.stats['evictions']['L1'] += 1
        
        # L2 - Adicionar versão comprimida se grande
        if size_bytes > 1024:  # > 1KB
            self._promote_to_l2(key_hash, value, ttl)
        
        # L3 - Persistir se importante (TTL longo)
        if ttl and ttl > 3600:  # > 1 hora
            self._save_to_l3(key_hash, value, ttl)
        
        return True
    
    def set_many(self, items: Dict[str, Any], ttl: int = None) -> int:
        """Define múltiplos valores de uma vez (batch)"""
        count = 0
        for key, value in items.items():
            if self.set(key, value, ttl):
                count += 1
        return count
    
    def delete(self, key: str) -> bool:
        """Remove do cache em todos os níveis"""
        key_hash = self._hash_key(key)
        deleted = False
        
        # L1
        if key_hash in self.l1_cache:
            del self.l1_cache[key_hash]
            deleted = True
        
        # L2
        if key_hash in self.l2_cache:
            del self.l2_cache[key_hash]
            deleted = True
        
        # L3
        conn = sqlite3.connect(str(self.l3_db))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cache_entries WHERE key = ?", (key_hash,))
        if cursor.rowcount > 0:
            deleted = True
        conn.commit()
        conn.close()
        
        return deleted
    
    def clear(self, level: str = None):
        """Limpa cache por nível ou todos"""
        if level == 'L1' or level is None:
            self.l1_cache.clear()
            
        if level == 'L2' or level is None:
            self.l2_cache.clear()
            
        if level == 'L3' or level is None:
            conn = sqlite3.connect(str(self.l3_db))
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cache_entries")
            conn.commit()
            conn.close()
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas detalhadas do cache"""
        l1_size = sum(e.get('size_bytes', 0) for e in self.l1_cache.values())
        l2_size = sum(e.get('size_bytes', 0) for e in self.l2_cache.values())
        
        # L3 size
        conn = sqlite3.connect(str(self.l3_db))
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(size_bytes), COUNT(*) FROM cache_entries")
        l3_size, l3_count = cursor.fetchone()
        conn.close()
        
        total_hits = sum(self.stats['hits'].values())
        total_requests = total_hits + self.stats['misses']['total']
        hit_rate = (total_hits / max(1, total_requests)) * 100
        
        return {
            'levels': {
                'L1': {
                    'items': len(self.l1_cache),
                    'size_mb': l1_size / (1024 * 1024),
                    'hits': self.stats['hits']['L1'],
                    'evictions': self.stats['evictions']['L1']
                },
                'L2': {
                    'items': len(self.l2_cache),
                    'size_mb': l2_size / (1024 * 1024),
                    'hits': self.stats['hits']['L2'],
                    'evictions': self.stats['evictions']['L2'],
                    'compressions': self.stats['compressions']
                },
                'L3': {
                    'items': l3_count or 0,
                    'size_mb': (l3_size or 0) / (1024 * 1024),
                    'hits': self.stats['hits']['L3'],
                    'evictions': self.stats['evictions']['L3']
                }
            },
            'performance': {
                'hit_rate': f"{hit_rate:.2f}%",
                'total_hits': total_hits,
                'total_misses': self.stats['misses']['total'],
                'compression_ratio': self._get_compression_ratio(),
                'saved_mb': self.stats['total_saved_bytes'] / (1024 * 1024)
            }
        }
    
    def predict_next_access(self, key: str) -> Optional[float]:
        """
        Prediz próximo acesso baseado em padrões
        Retorna timestamp previsto ou None
        """
        key_hash = self._hash_key(key)
        pattern = self.access_patterns[key_hash]
        
        if pattern['count'] < 3:
            return None
        
        # Previsão simples baseada em intervalo médio
        predicted = pattern['last_access'] + pattern['avg_interval']
        return predicted if predicted > time.time() else None
    
    def optimize(self):
        """Otimiza cache baseado em padrões de uso"""
        print("🔧 Otimizando cache...")
        
        # Análise de padrões
        hot_keys = []
        cold_keys = []
        
        for key, pattern in self.access_patterns.items():
            if pattern['count'] > 10 and pattern['avg_interval'] < 60:
                hot_keys.append(key)
            elif pattern['count'] < 2 and time.time() - pattern['last_access'] > 3600:
                cold_keys.append(key)
        
        # Pre-load hot keys para L1
        for key in hot_keys[:100]:  # Top 100
            value = self._get_from_l3(key)
            if value:
                self._promote_to_l1(key, value)
        
        # Evict cold keys
        for key in cold_keys:
            self.delete(key)
        
        print(f"   Promovidos: {len(hot_keys[:100])} hot keys")
        print(f"   Removidos: {len(cold_keys)} cold keys")
    
    # Métodos auxiliares privados
    
    def _hash_key(self, key: str) -> str:
        """Gera hash consistente da chave"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _compress(self, data: Any) -> bytes:
        """Comprime dados com zlib"""
        serialized = pickle.dumps(data)
        compressed = zlib.compress(serialized, level=6)
        self.stats['compressions'] += 1
        self.stats['total_saved_bytes'] += len(serialized) - len(compressed)
        return compressed
    
    def _decompress(self, data: bytes) -> Any:
        """Descomprime dados"""
        decompressed = zlib.decompress(data)
        return pickle.loads(decompressed)
    
    def _promote_to_l1(self, key_hash: str, value: Any, ttl: int = None):
        """Promove valor para L1"""
        ttl = ttl or self.l1_ttl
        self.l1_cache[key_hash] = {
            'value': value,
            'expires_at': time.time() + ttl,
            'size_bytes': len(pickle.dumps(value))
        }
        
        # Aplicar limite
        if len(self.l1_cache) > self.l1_max_items:
            oldest = next(iter(self.l1_cache))
            del self.l1_cache[oldest]
    
    def _promote_to_l2(self, key_hash: str, value: Any, ttl: int = None):
        """Promove valor para L2 (comprimido)"""
        ttl = ttl or self.l2_ttl
        compressed = self._compress(value)
        
        self.l2_cache[key_hash] = {
            'compressed_value': compressed,
            'expires_at': time.time() + ttl,
            'size_bytes': len(compressed)
        }
        
        # Aplicar limite
        if len(self.l2_cache) > self.l2_max_items:
            oldest = next(iter(self.l2_cache))
            del self.l2_cache[oldest]
    
    def _save_to_l3(self, key_hash: str, value: Any, ttl: int = None):
        """Salva no cache L3 (SQLite)"""
        ttl = ttl or self.l3_ttl
        
        # Comprimir se grande
        serialized = pickle.dumps(value)
        if len(serialized) > 10240:  # > 10KB
            data = self._compress(value)
            compressed = True
        else:
            data = serialized
            compressed = False
        
        conn = sqlite3.connect(str(self.l3_db))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO cache_entries
            (key, value, compressed, size_bytes, created_at, accessed_at, ttl)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (key_hash, data, compressed, len(data), time.time(), time.time(), ttl))
        
        conn.commit()
        conn.close()
    
    def _get_from_l3(self, key_hash: str) -> Optional[Any]:
        """Busca no cache L3"""
        conn = sqlite3.connect(str(self.l3_db))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT value, compressed, created_at, ttl
            FROM cache_entries
            WHERE key = ?
        """, (key_hash,))
        
        row = cursor.fetchone()
        
        if row:
            value_data, compressed, created_at, ttl = row
            
            # Verificar TTL
            if time.time() > created_at + ttl:
                # Expirado
                cursor.execute("DELETE FROM cache_entries WHERE key = ?", (key_hash,))
                conn.commit()
                conn.close()
                self.stats['evictions']['L3'] += 1
                return None
            
            # Atualizar accessed_at
            cursor.execute("""
                UPDATE cache_entries 
                SET accessed_at = ?, access_count = access_count + 1
                WHERE key = ?
            """, (time.time(), key_hash))
            
            conn.commit()
            conn.close()
            
            # Descomprimir se necessário
            if compressed:
                return self._decompress(value_data)
            else:
                return pickle.loads(value_data)
        
        conn.close()
        return None
    
    def _evict_lru(self):
        """Remove itens menos recentemente usados"""
        # L1 - remover 10%
        to_remove = max(1, len(self.l1_cache) // 10)
        for _ in range(to_remove):
            if self.l1_cache:
                key = next(iter(self.l1_cache))
                del self.l1_cache[key]
                self.stats['evictions']['L1'] += 1
        
        # L2 - remover 5%
        to_remove = max(1, len(self.l2_cache) // 20)
        for _ in range(to_remove):
            if self.l2_cache:
                key = next(iter(self.l2_cache))
                del self.l2_cache[key]
                self.stats['evictions']['L2'] += 1
    
    def _estimate_memory_usage(self) -> int:
        """Estima uso de memória em bytes"""
        l1_size = sum(e.get('size_bytes', 0) for e in self.l1_cache.values())
        l2_size = sum(e.get('size_bytes', 0) for e in self.l2_cache.values())
        return l1_size + l2_size
    
    def _get_compression_ratio(self) -> float:
        """Calcula taxa de compressão média"""
        if self.stats['compressions'] == 0:
            return 1.0
        
        total_saved = self.stats['total_saved_bytes']
        total_compressed = sum(e.get('size_bytes', 0) for e in self.l2_cache.values())
        
        if total_compressed == 0:
            return 1.0
        
        original = total_compressed + total_saved
        return original / total_compressed
    
    def _record_access_pattern(self, key_hash: str):
        """Registra padrão de acesso para predição"""
        pattern = self.access_patterns[key_hash]
        now = time.time()
        
        if pattern['last_access'] > 0:
            interval = now - pattern['last_access']
            # Média móvel exponencial
            if pattern['avg_interval'] > 0:
                pattern['avg_interval'] = 0.7 * pattern['avg_interval'] + 0.3 * interval
            else:
                pattern['avg_interval'] = interval
        
        pattern['count'] += 1
        pattern['last_access'] = now
    
    def _maintenance_worker(self):
        """Thread de manutenção periódica"""
        while True:
            time.sleep(300)  # 5 minutos
            
            try:
                # Limpar expirados
                self._cleanup_expired()
                
                # Otimizar a cada hora
                if int(time.time()) % 3600 < 300:
                    self.optimize()
            except Exception as e:
                print(f"❌ Erro na manutenção do cache: {e}")
    
    def _cleanup_expired(self):
        """Remove entradas expiradas"""
        now = time.time()
        
        # L1
        expired = [k for k, v in self.l1_cache.items() if v['expires_at'] < now]
        for key in expired:
            del self.l1_cache[key]
            self.stats['evictions']['L1'] += 1
        
        # L2
        expired = [k for k, v in self.l2_cache.items() if v['expires_at'] < now]
        for key in expired:
            del self.l2_cache[key]
            self.stats['evictions']['L2'] += 1
        
        # L3
        conn = sqlite3.connect(str(self.l3_db))
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM cache_entries
            WHERE created_at + ttl < ?
        """, (now,))
        self.stats['evictions']['L3'] += cursor.rowcount
        conn.commit()
        conn.close()


# Singleton global
_cache = None

def get_cache() -> IntelligentCache:
    """Retorna instância singleton do cache"""
    global _cache
    if _cache is None:
        _cache = IntelligentCache()
    return _cache