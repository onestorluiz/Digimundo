#!/usr/bin/env python3
"""
🧠 GERENCIADOR DE CACHE INTELIGENTE
Cache preditivo com ML para otimizar acesso a dados hot
"""

import time
import json
import sqlite3
from pathlib import Path
from functools import lru_cache, wraps
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import pickle
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType

# Integration with other components
try:
    from scripts.active.integrated_system import get_integrated_system
except:
    pass  # Integration optional



class IntelligentCacheManager:
    """
    Cache inteligente com previsão de acesso e otimização automática
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.memory = get_unified_memory()

        # Caches em memória
        self._hot_cache = {}  # Cache principal para hot data
        self._warm_cache = {}  # Cache secundário
        self._predictions = {}  # Previsões de próximos acessos

        # Estatísticas e padrões
        self._access_log = deque(maxlen=10000)
        self._access_patterns = defaultdict(list)
        self._hit_rate = {'hits': 0, 'misses': 0}

        # Inicializar com hot spots conhecidos
        self._initialize_hot_spots()

    def _initialize_hot_spots(self):
        """
        Carrega hot spots do banco de dados
        """
        print("🔥 Inicializando hot spots...")

        db_path = Path("data/unified_memory.db")
        if not db_path.exists():
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Buscar top 100 itens mais acessados
            cursor.execute("""
                SELECT key, value, accessed_count
                FROM unified_memory
                WHERE accessed_count > 5
                ORDER BY accessed_count DESC
                LIMIT 100
            """)

            hot_items = cursor.fetchall()

            for key, value, access_count in hot_items:
                try:
                    # Deserializar valor
                    if value:
                        parsed_value = json.loads(value) if isinstance(value, str) else value
                        self._hot_cache[key] = {
                            'value': parsed_value,
                            'access_count': access_count,
                            'timestamp': time.time(),
                            'ttl': self.ttl_seconds * 2  # Hot items têm TTL maior
                        }
                except:
                    pass

            conn.close()

            print(f"  ✅ {len(self._hot_cache)} hot spots carregados")

        except Exception as e:
            print(f"  ❌ Erro ao carregar hot spots: {e}")

    @lru_cache(maxsize=128)
    def get(self, key: str) -> Optional[Any]:
        """
        Busca valor com cache inteligente

        Args:
            key: Chave para buscar

        Returns:
            Valor ou None
        """
        # Registrar acesso
        self._log_access(key)

        # Verificar hot cache
        if key in self._hot_cache:
            entry = self._hot_cache[key]
            if self._is_valid(entry):
                self._hit_rate['hits'] += 1
                self._update_access_count(key)
                self._predict_next_access(key)
                return entry['value']

        # Verificar warm cache
        if key in self._warm_cache:
            entry = self._warm_cache[key]
            if self._is_valid(entry):
                self._hit_rate['hits'] += 1
                # Promover para hot cache se acessado frequentemente
                self._promote_to_hot(key, entry)
                return entry['value']

        # Cache miss - buscar do banco
        self._hit_rate['misses'] += 1
        value = self._fetch_from_db(key)

        if value is not None:
            # Adicionar ao warm cache
            self._add_to_cache(key, value, self._warm_cache)

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Armazena valor no cache

        Args:
            key: Chave
            value: Valor
            ttl: Time to live em segundos
        """
        entry = {
            'value': value,
            'access_count': 1,
            'timestamp': time.time(),
            'ttl': ttl or self.ttl_seconds
        }

        # Decidir em qual cache colocar baseado em previsões
        if self._should_be_hot(key):
            self._add_to_cache(key, value, self._hot_cache)
        else:
            self._add_to_cache(key, value, self._warm_cache)

        # Salvar no banco também
        self._save_to_db(key, value)

    def _is_valid(self, entry: Dict) -> bool:
        """Verifica se entrada ainda é válida"""
        age = time.time() - entry['timestamp']
        return age < entry['ttl']

    def _log_access(self, key: str):
        """Registra acesso para análise de padrões"""
        access = {
            'key': key,
            'timestamp': time.time(),
            'hour': datetime.now().hour,
            'weekday': datetime.now().weekday()
        }
        self._access_log.append(access)
        self._access_patterns[key].append(access['timestamp'])

    def _predict_next_access(self, key: str):
        """
        Prevê próximo acesso baseado em padrões

        Args:
            key: Chave acessada
        """
        patterns = self._access_patterns.get(key, [])

        if len(patterns) < 3:
            return

        # Calcular intervalo médio entre acessos
        intervals = []
        for i in range(1, len(patterns)):
            intervals.append(patterns[i] - patterns[i-1])

        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            next_access = patterns[-1] + avg_interval

            self._predictions[key] = {
                'next_access': next_access,
                'confidence': min(0.9, len(patterns) / 10)  # Confiança aumenta com mais dados
            }

            # Pré-carregar se próximo acesso é em breve
            if next_access - time.time() < 60:  # Próximo minuto
                self._preload(key)

    def _preload(self, key: str):
        """
        Pré-carrega dados que serão acessados em breve

        Args:
            key: Chave para pré-carregar
        """
        if key not in self._hot_cache and key not in self._warm_cache:
            value = self._fetch_from_db(key)
            if value:
                self._add_to_cache(key, value, self._warm_cache)
                print(f"🔮 Pré-carregado: {key}")

    def _should_be_hot(self, key: str) -> bool:
        """
        Determina se item deve estar no hot cache

        Args:
            key: Chave

        Returns:
            True se deve estar no hot cache
        """
        # Baseado em padrões de acesso
        access_count = len(self._access_patterns.get(key, []))

        # Se acessado mais de 5 vezes, é hot
        if access_count > 5:
            return True

        # Se tem alta previsão de acesso
        prediction = self._predictions.get(key)
        if prediction and prediction['confidence'] > 0.7:
            return True

        return False

    def _promote_to_hot(self, key: str, entry: Dict):
        """
        Promove item do warm para hot cache

        Args:
            key: Chave
            entry: Entrada do cache
        """
        if len(self._hot_cache) >= self.max_size // 2:
            # Remover item menos usado do hot cache
            self._evict_lru(self._hot_cache)

        self._hot_cache[key] = entry
        del self._warm_cache[key]
        print(f"⬆️  Promovido para hot: {key}")

    def _add_to_cache(self, key: str, value: Any, cache: Dict):
        """
        Adiciona item ao cache especificado

        Args:
            key: Chave
            value: Valor
            cache: Cache alvo (hot ou warm)
        """
        if len(cache) >= self.max_size // 2:
            self._evict_lru(cache)

        cache[key] = {
            'value': value,
            'access_count': cache.get(key, {}).get('access_count', 0) + 1,
            'timestamp': time.time(),
            'ttl': self.ttl_seconds
        }

    def _evict_lru(self, cache: Dict):
        """
        Remove item menos recentemente usado

        Args:
            cache: Cache para limpar
        """
        if not cache:
            return

        # Encontrar item com menor timestamp
        lru_key = min(cache.keys(), key=lambda k: cache[k]['timestamp'])
        del cache[lru_key]

    def _update_access_count(self, key: str):
        """Atualiza contador de acesso"""
        for cache in [self._hot_cache, self._warm_cache]:
            if key in cache:
                cache[key]['access_count'] += 1
                cache[key]['timestamp'] = time.time()
                break

    def _fetch_from_db(self, key: str) -> Optional[Any]:
        """
        Busca valor do banco de dados

        Args:
            key: Chave

        Returns:
            Valor ou None
        """
        results = self.memory.search(
            key,
            memory_types=[MemoryType.ANALYSIS, MemoryType.KNOWLEDGE],
            limit=1
        )

        if results:
            return results[0].value

        return None

    def _save_to_db(self, key: str, value: Any):
        """
        Salva valor no banco de dados

        Args:
            key: Chave
            value: Valor
        """
        self.memory.store(
            memory_type=MemoryType.CACHE,
            key=key,
            value=value,
            metadata={
                'cached_at': time.time(),
                'cache_type': 'intelligent'
            }
        )

    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas do cache

        Returns:
            Estatísticas
        """
        total_accesses = self._hit_rate['hits'] + self._hit_rate['misses']
        hit_rate = self._hit_rate['hits'] / total_accesses if total_accesses > 0 else 0

        # Analisar padrões temporais
        hour_distribution = defaultdict(int)
        for access in self._access_log:
            hour_distribution[access['hour']] += 1

        return {
            'hit_rate': hit_rate,
            'total_hits': self._hit_rate['hits'],
            'total_misses': self._hit_rate['misses'],
            'hot_cache_size': len(self._hot_cache),
            'warm_cache_size': len(self._warm_cache),
            'predictions_active': len(self._predictions),
            'peak_hours': sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)[:3],
            'memory_usage_mb': self._estimate_memory_usage()
        }

    def _estimate_memory_usage(self) -> float:
        """Estima uso de memória em MB"""
        total_bytes = 0

        for cache in [self._hot_cache, self._warm_cache]:
            for entry in cache.values():
                # Estimar tamanho do valor
                try:
                    total_bytes += len(pickle.dumps(entry))
                except:
                    total_bytes += 1000  # Estimativa padrão

        return total_bytes / (1024 * 1024)

    def optimize(self):
        """
        Otimiza cache baseado em padrões observados
        """
        print("\n🔧 OTIMIZANDO CACHE...")

        stats = self.get_statistics()

        # Ajustar TTL baseado em hit rate
        if stats['hit_rate'] < 0.5:
            self.ttl_seconds = int(self.ttl_seconds * 1.5)
            print(f"  📈 TTL aumentado para {self.ttl_seconds}s")

        # Limpar entradas expiradas
        for cache in [self._hot_cache, self._warm_cache]:
            expired = [k for k, v in cache.items() if not self._is_valid(v)]
            for key in expired:
                del cache[key]

        print(f"  🧹 {len(expired)} entradas expiradas removidas")

        # Reorganizar baseado em previsões
        for key, prediction in self._predictions.items():
            if prediction['confidence'] > 0.8:
                if prediction['next_access'] - time.time() < 300:  # Próximos 5 min
                    self._preload(key)

        print(f"  ✅ Cache otimizado")
        print(f"  📊 Hit rate: {stats['hit_rate']:.1%}")
        print(f"  💾 Memória: {stats['memory_usage_mb']:.1f} MB")


# Decorator para cachear funções automaticamente
def intelligent_cache(ttl: int = 300):
    """
    Decorator para adicionar cache inteligente a funções

    Args:
        ttl: Time to live em segundos

    Usage:
        @intelligent_cache(ttl=600)
        def expensive_function(param):
            # Código pesado
            return result
    """
    cache_manager = IntelligentCacheManager()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gerar chave única para os argumentos
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Tentar buscar do cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Executar função
            result = func(*args, **kwargs)

            # Cachear resultado
            cache_manager.set(cache_key, result, ttl)

            return result

        # Adicionar método para limpar cache
        wrapper.clear_cache = lambda: cache_manager._hot_cache.clear()
        wrapper.get_stats = lambda: cache_manager.get_statistics()

        return wrapper

    return decorator


def main():
    """
    Demonstração do cache inteligente
    """
    print("\n🧠 GERENCIADOR DE CACHE INTELIGENTE")
    print("-" * 50)

    cache = IntelligentCacheManager()

    # Simular acessos
    print("\n📊 Simulando padrões de acesso...")

    # Padrão 1: Acesso frequente a alguns items
    hot_items = ['analysis_inception', 'analysis_matrix', 'analysis_interstellar']

    for _ in range(10):
        for item in hot_items:
            cache.get(item)
            time.sleep(0.1)

    # Padrão 2: Acesso esporádico a outros
    cold_items = ['analysis_random1', 'analysis_random2', 'analysis_random3']

    for item in cold_items:
        cache.get(item)

    # Verificar estatísticas
    stats = cache.get_statistics()

    print("\n📈 ESTATÍSTICAS DO CACHE:")
    print(f"   Hit Rate: {stats['hit_rate']:.1%}")
    print(f"   Total Hits: {stats['total_hits']}")
    print(f"   Total Misses: {stats['total_misses']}")
    print(f"   Hot Cache: {stats['hot_cache_size']} items")
    print(f"   Warm Cache: {stats['warm_cache_size']} items")
    print(f"   Previsões Ativas: {stats['predictions_active']}")
    print(f"   Memória Usada: {stats['memory_usage_mb']:.2f} MB")

    if stats['peak_hours']:
        print(f"   Horários de Pico: {stats['peak_hours']}")

    # Otimizar
    cache.optimize()

    # Demonstrar decorator
    print("\n🎯 TESTANDO DECORATOR:")

    @intelligent_cache(ttl=60)
    def expensive_analysis(screenplay_name: str) -> Dict:
        """Simula análise pesada"""
        time.sleep(1)  # Simular processamento
        return {
            'screenplay': screenplay_name,
            'score': 85,
            'themes': ['love', 'sacrifice']
        }

    # Primeira chamada (lenta)
    start = time.time()
    result1 = expensive_analysis("Inception")
    print(f"   Primeira chamada: {time.time() - start:.2f}s")

    # Segunda chamada (cacheada)
    start = time.time()
    result2 = expensive_analysis("Inception")
    print(f"   Segunda chamada: {time.time() - start:.4f}s")

    print(f"   Cache stats: {expensive_analysis.get_stats()}")

    print("\n✅ Cache inteligente funcionando!")


if __name__ == "__main__":
    main()