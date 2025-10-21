#!/usr/bin/env python3
"""
ScriptureMonChampion V2.1 - Sistema Unificado com Correções
Versão debugada e otimizada com saúde melhorada
"""

import os
import sys
import json
import hashlib
import re
import ast
import gc
import time
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
import asyncio
from datetime import datetime

# Tenta importar OmniMemory V4, senão usa versão simplificada
try:
    from omnimemory import OmniMemoryV4
except ImportError:
    print("⚠️ OmniMemory V4 não encontrado, usando versão simplificada")

    class OmniMemoryV4:
        """Versão simplificada do OmniMemory para testes"""
        def __init__(self, path):
            self.path = path
            self.nodes = {}
            self.harmony = 0.95  # Começa com boa harmonia

        def store(self, key, value, context="", importance=0.5):
            self.nodes[key] = {
                'content': value,
                'context': context,
                'importance': importance,
                'timestamp': datetime.now()
            }
            # Simula aumento de harmonia
            self.harmony = min(1.0, self.harmony + 0.001)

        def retrieve(self, key):
            return self.nodes.get(key, {}).get('content')

        def semantic_search(self, predicate, limit=10):
            results = []
            for key, node in self.nodes.items():
                if predicate(node['content']):
                    results.append(type('Node', (), {'key': key, 'content': node['content']})())
                    if len(results) >= limit:
                        break
            return results

        def get_harmony_report(self):
            return {
                'global_harmony': self.harmony,
                'nodes_count': len(self.nodes)
            }

# ==================== CONFIGURAÇÃO MELHORADA ====================

@dataclass
class Config:
    """Configuração unificada com valores otimizados"""
    memory_path: str = "/tmp/scripturemon_v2"
    max_workers: int = 4
    cache_size: int = 1000
    harmony_threshold: float = 0.8
    compression_cascade_levels: int = 3
    cross_modal_enabled: bool = True
    self_healing_enabled: bool = True
    ensemble_models: List[str] = field(default_factory=lambda: ["llama3.2:3b"])
    health_check_interval: int = 60  # segundos
    auto_repair_threshold: float = 0.7
    debug_mode: bool = False

# ==================== SISTEMA DE LOGGING MELHORADO ====================

class Logger:
    """Sistema de logging simples mas efetivo"""

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __init__(self, level=INFO):
        self.level = level
        self.history = deque(maxlen=1000)

    def log(self, level, message, component="system"):
        if level >= self.level:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{self._level_name(level)}] [{component}] {message}"
            print(log_entry)
            self.history.append(log_entry)

    def _level_name(self, level):
        names = {0: "DEBUG", 1: "INFO", 2: "WARN", 3: "ERROR", 4: "CRIT"}
        return names.get(level, "UNKNOWN")

    def debug(self, message, component="system"):
        self.log(self.DEBUG, message, component)

    def info(self, message, component="system"):
        self.log(self.INFO, message, component)

    def warning(self, message, component="system"):
        self.log(self.WARNING, message, component)

    def error(self, message, component="system"):
        self.log(self.ERROR, message, component)

    def critical(self, message, component="system"):
        self.log(self.CRITICAL, message, component)

# Logger global
logger = Logger(level=Logger.INFO)

# ==================== INOVAÇÃO 1: SINESTESIA CROSS-MODAL (CORRIGIDA) ====================

class CrossModalEmbedding:
    """Converte dados entre modalidades sensoriais - versão otimizada"""

    def __init__(self):
        self.modality_map = {
            'text': self._text_features,
            'color': self._color_features,
            'emotion': self._emotion_features,
            'rhythm': self._rhythm_features,
            'shape': self._shape_features
        }
        self.cache = {}

    def transform(self, data: Any, source: str, target: str) -> Any:
        """Transforma dados de uma modalidade para outra com cache"""
        cache_key = f"{hash(str(data))}_{source}_{target}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Extrai features da origem
            features = self.modality_map.get(source, self._default_features)(data)
            # Converte para modalidade alvo
            result = self._features_to_modality(features, target)

            # Cache do resultado
            self.cache[cache_key] = result

            # Limita tamanho do cache
            if len(self.cache) > 100:
                # Remove metade mais antiga
                keys_to_remove = list(self.cache.keys())[:50]
                for key in keys_to_remove:
                    del self.cache[key]

            return result

        except Exception as e:
            logger.error(f"Erro na transformação cross-modal: {e}", "CrossModal")
            return data  # Retorna original se falhar

    def _text_features(self, text: str) -> Dict:
        """Extrai features de texto com tratamento de erro"""
        if not text or not isinstance(text, str):
            return {'length': 0, 'complexity': 0, 'sentiment': 0.5, 'rhythm': 0}

        words = text.split()
        return {
            'length': len(text),
            'complexity': len(set(words)) / max(len(words), 1),
            'sentiment': sum(ord(c) for c in text[:min(100, len(text))]) % 100 / 100,
            'rhythm': len(re.findall(r'[.!?]', text))
        }

    def _color_features(self, color: int) -> Dict:
        """Features de cor RGB"""
        try:
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            return {
                'brightness': (r + g + b) / (3 * 255),
                'saturation': (max(r, g, b) - min(r, g, b)) / 255,
                'hue': (r * 0.3 + g * 0.59 + b * 0.11) / 255
            }
        except:
            return {'brightness': 0.5, 'saturation': 0.5, 'hue': 0.5}

    def _emotion_features(self, emotion: str) -> Dict:
        """Features emocionais"""
        emotions = {
            'joy': (1.0, 0.8), 'sadness': (0.2, 0.3),
            'anger': (0.9, 0.9), 'fear': (0.3, 0.8),
            'neutral': (0.5, 0.5)
        }
        arousal, valence = emotions.get(str(emotion).lower(), (0.5, 0.5))
        return {'arousal': arousal, 'valence': valence}

    def _rhythm_features(self, text: str) -> Dict:
        """Features rítmicas do texto"""
        if not text:
            return {'tempo': 0.5, 'variation': 0.5}

        sentences = text.split('.')
        return {
            'tempo': len(sentences) / max(len(text), 1),
            'variation': len(set(len(s) for s in sentences)) / max(len(sentences), 1)
        }

    def _shape_features(self, data: Any) -> Dict:
        """Features de forma/estrutura"""
        return {'complexity': 0.5, 'symmetry': 0.5, 'density': 0.5}

    def _default_features(self, data: Any) -> Dict:
        """Features padrão para modalidades desconhecidas"""
        return {'value': 0.5}

    def _features_to_modality(self, features: Dict, target: str) -> Any:
        """Converte features para modalidade alvo"""
        if target == 'color':
            brightness = sum(features.values()) / max(len(features), 1)
            return int(min(brightness, 1.0) * 0xFFFFFF)
        elif target == 'emotion':
            arousal = sum(features.values()) / max(len(features), 1)
            if arousal > 0.7:
                return 'joy'
            elif arousal < 0.3:
                return 'sadness'
            else:
                return 'neutral'
        elif target == 'text':
            return f"Features: {', '.join(f'{k}={v:.2f}' for k, v in features.items())}"
        return features

# ==================== MEMORY GRAPH MELHORADO ====================

class MemoryGraph:
    """Grafo de conexões entre memórias com persistência"""

    def __init__(self, max_connections=1000):
        self.adjacency = defaultdict(dict)
        self.access_patterns = deque(maxlen=100)
        self.max_connections = max_connections
        self.connection_count = 0

    def link(self, mem1: str, mem2: str, weight: float = 1.0):
        """Cria conexão ponderada entre memórias com limite"""
        # Evita auto-conexão
        if mem1 == mem2:
            return

        # Limita número de conexões
        if self.connection_count >= self.max_connections:
            self._prune_weak_connections()

        self.adjacency[mem1][mem2] = weight
        self.adjacency[mem2][mem1] = weight
        self.connection_count += 1

        logger.debug(f"Linked {mem1[:8]}... to {mem2[:8]}... with weight {weight:.2f}", "MemoryGraph")

    def _prune_weak_connections(self):
        """Remove conexões fracas quando atinge limite"""
        # Coleta todas conexões com pesos
        all_connections = []
        for node, neighbors in self.adjacency.items():
            for neighbor, weight in neighbors.items():
                if node < neighbor:  # Evita duplicatas
                    all_connections.append((weight, node, neighbor))

        # Ordena por peso
        all_connections.sort()

        # Remove 20% mais fracas
        to_remove = int(len(all_connections) * 0.2)
        for weight, node1, node2 in all_connections[:to_remove]:
            if node2 in self.adjacency[node1]:
                del self.adjacency[node1][node2]
            if node1 in self.adjacency[node2]:
                del self.adjacency[node2][node1]
            self.connection_count -= 1

        logger.info(f"Pruned {to_remove} weak connections", "MemoryGraph")

    def find_related(self, memory: str, depth: int = 2) -> List[Tuple[str, float]]:
        """Encontra memórias relacionadas com busca otimizada"""
        if memory not in self.adjacency:
            return []

        visited = set()
        related = []

        # BFS com pesos
        queue = [(memory, 1.0, 0)]

        while queue:
            current, weight, current_depth = queue.pop(0)

            if current in visited or current_depth > depth:
                continue

            visited.add(current)

            for neighbor, edge_weight in self.adjacency.get(current, {}).items():
                if neighbor not in visited:
                    combined_weight = weight * edge_weight
                    related.append((neighbor, combined_weight))
                    if current_depth < depth:
                        queue.append((neighbor, combined_weight, current_depth + 1))

        # Remove duplicatas e ordena
        seen = set()
        unique = []
        for mem, weight in sorted(related, key=lambda x: x[1], reverse=True):
            if mem not in seen and mem != memory:
                seen.add(mem)
                unique.append((mem, weight))
                if len(unique) >= 10:
                    break

        return unique

    def predict_next(self) -> Optional[str]:
        """Prevê próxima memória baseada em padrões"""
        if len(self.access_patterns) < 3:
            return None

        # Busca padrão mais recente
        pattern_length = min(5, len(self.access_patterns) // 2)
        recent_pattern = list(self.access_patterns)[-pattern_length:]

        # Busca padrão similar no histórico
        for i in range(len(self.access_patterns) - pattern_length - 1):
            if list(self.access_patterns)[i:i+pattern_length] == recent_pattern:
                next_index = i + pattern_length
                if next_index < len(self.access_patterns):
                    return self.access_patterns[next_index]

        return None

    def record_access(self, memory: str):
        """Registra acesso para análise de padrões"""
        self.access_patterns.append(memory)

# ==================== COMPRESSION CORRIGIDA ====================

class CascadeCompression:
    """Compressão em cascata com correções"""

    def __init__(self, levels: int = 3):
        self.levels = min(levels, 3)  # Limita níveis
        self.dictionaries = [self._create_dictionary(i) for i in range(self.levels)]
        self.compression_stats = {'total_compressed': 0, 'total_original': 0}

    def compress(self, text: str) -> str:
        """Comprime texto com validação"""
        if not text:
            return text

        original_size = len(text)
        compressed = text

        try:
            for level, dictionary in enumerate(self.dictionaries):
                if level == 0:
                    compressed = self._compress_common_words(compressed, dictionary)
                elif level == 1:
                    compressed = self._compress_screenplay_patterns(compressed, dictionary)
                else:
                    compressed = self._compress_byte_pairs(compressed)

            # Atualiza estatísticas
            self.compression_stats['total_compressed'] += len(compressed)
            self.compression_stats['total_original'] += original_size

            logger.debug(f"Compressed {original_size} → {len(compressed)} bytes", "Compression")

        except Exception as e:
            logger.error(f"Compression error: {e}", "Compression")
            return text  # Retorna original se falhar

        return compressed

    def decompress(self, compressed: str) -> str:
        """Descomprime com tratamento de erro"""
        if not compressed:
            return compressed

        text = compressed

        try:
            for level in reversed(range(self.levels)):
                dictionary = self.dictionaries[level]
                if level == 0:
                    text = self._decompress_common_words(text, dictionary)
                elif level == 1:
                    text = self._decompress_screenplay_patterns(text, dictionary)
                else:
                    text = self._decompress_byte_pairs(text)

        except Exception as e:
            logger.error(f"Decompression error: {e}", "Compression")
            return compressed

        return text

    def _create_dictionary(self, level: int) -> Dict:
        """Cria dicionário específico por nível"""
        if level == 0:
            # Palavras comuns com tokens seguros
            return {
                ' the ': '◊1', ' and ': '◊2', ' to ': '◊3',
                ' a ': '◊4', ' of ': '◊5', ' in ': '◊6',
                ' is ': '◊7', ' it ': '◊8', ' you ': '◊9',
                ' that ': '◊A', ' with ': '◊B', ' for ': '◊C'
            }
        elif level == 1:
            # Padrões de screenplay
            return {
                'INT.': '◊INT', 'EXT.': '◊EXT', 'FADE IN:': '◊FI',
                'FADE OUT.': '◊FO', 'CUT TO:': '◊CT', '(V.O.)': '◊VO',
                '(O.S.)': '◊OS', 'CONTINUED:': '◊CN', '- DAY': '◊DY',
                '- NIGHT': '◊NT', 'CLOSE UP': '◊CU', 'WIDE SHOT': '◊WS'
            }
        else:
            # Pares de bytes comuns
            return {
                'th': '◊t', 'he': '◊h', 'in': '◊i',
                'er': '◊e', 'an': '◊a', 're': '◊r'
            }

    def _compress_common_words(self, text: str, dictionary: Dict) -> str:
        """Comprime palavras comuns com boundaries corretos"""
        for word, token in dictionary.items():
            text = text.replace(word, token)
        return text

    def _compress_screenplay_patterns(self, text: str, dictionary: Dict) -> str:
        """Comprime padrões de roteiro"""
        for pattern, token in dictionary.items():
            text = text.replace(pattern, token)
        return text

    def _compress_byte_pairs(self, text: str) -> str:
        """Compressão de pares de bytes"""
        # Implementação simplificada
        dictionary = self.dictionaries[2]
        for pair, token in dictionary.items():
            text = text.replace(pair, token)
        return text

    def _decompress_common_words(self, text: str, dictionary: Dict) -> str:
        """Descomprime palavras"""
        reverse_dict = {v: k for k, v in dictionary.items()}
        for token, word in reverse_dict.items():
            text = text.replace(token, word)
        return text

    def _decompress_screenplay_patterns(self, text: str, dictionary: Dict) -> str:
        """Descomprime padrões"""
        reverse_dict = {v: k for k, v in dictionary.items()}
        for token, pattern in reverse_dict.items():
            text = text.replace(token, pattern)
        return text

    def _decompress_byte_pairs(self, text: str) -> str:
        """Descompressão de pares"""
        dictionary = self.dictionaries[2]
        reverse_dict = {v: k for k, v in dictionary.items()}
        for token, pair in reverse_dict.items():
            text = text.replace(token, pair)
        return text

    def get_compression_ratio(self) -> float:
        """Retorna taxa de compressão média"""
        if self.compression_stats['total_original'] == 0:
            return 1.0
        return self.compression_stats['total_compressed'] / self.compression_stats['total_original']

# ==================== SELF-HEALING MELHORADO ====================

class SelfHealingSystem:
    """Sistema de auto-reparação com melhorias"""

    def __init__(self):
        self.health_checks = {
            'memory': self._check_memory_health,
            'compression': self._check_compression_health,
            'performance': self._check_performance_health,
            'cache': self._check_cache_health,
            'harmony': self._check_harmony_health
        }
        self.repair_strategies = {
            'memory': self._repair_memory,
            'compression': self._repair_compression,
            'performance': self._repair_performance,
            'cache': self._repair_cache,
            'harmony': self._repair_harmony
        }
        self.health_history = deque(maxlen=100)
        self.last_check = datetime.now()
        self.memory_baseline = None
        self.compression_instance = None  # Referência para compressor

    def check_health(self, omnimemory=None, compressor=None) -> Dict:
        """Verifica saúde do sistema com contexto"""
        # Atualiza referências
        if compressor:
            self.compression_instance = compressor

        health_report = {}

        for component, check_func in self.health_checks.items():
            try:
                # Passa omnimemory para checks que precisam
                if component == 'harmony' and omnimemory:
                    health = check_func(omnimemory)
                else:
                    health = check_func()

                health_report[component] = {
                    'status': 'healthy' if health > 0.8 else 'degraded' if health > 0.5 else 'critical',
                    'score': health,
                    'timestamp': datetime.now().isoformat()
                }

                # Log se status crítico
                if health < 0.5:
                    logger.warning(f"Component {component} in critical state: {health:.2%}", "Health")

            except Exception as e:
                logger.error(f"Health check failed for {component}: {e}", "Health")
                health_report[component] = {
                    'status': 'error',
                    'score': 0.0,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }

        self.health_history.append((datetime.now(), health_report))
        self.last_check = datetime.now()

        return health_report

    def auto_repair(self, omnimemory=None) -> Dict:
        """Tenta reparar componentes com estratégias melhoradas"""
        health = self.check_health(omnimemory)
        repairs = {}

        for component, status in health.items():
            if status['score'] < 0.7:  # Threshold mais agressivo
                logger.info(f"Attempting repair for {component}", "Health")

                try:
                    repair_func = self.repair_strategies.get(component)
                    if repair_func:
                        # Passa contexto se necessário
                        if component == 'harmony' and omnimemory:
                            success = repair_func(omnimemory)
                        else:
                            success = repair_func()

                        # Verifica novo score
                        if component == 'harmony' and omnimemory:
                            new_score = self._check_harmony_health(omnimemory)
                        else:
                            new_score = self.health_checks[component]()

                        repairs[component] = {
                            'repaired': success,
                            'old_score': status['score'],
                            'new_score': new_score,
                            'improvement': new_score - status['score']
                        }

                        if success:
                            logger.info(f"Successfully repaired {component}: {status['score']:.2%} → {new_score:.2%}", "Health")
                        else:
                            logger.warning(f"Failed to repair {component}", "Health")

                except Exception as e:
                    logger.error(f"Repair failed for {component}: {e}", "Health")
                    repairs[component] = {
                        'repaired': False,
                        'error': str(e)
                    }

        return repairs

    def _check_memory_health(self) -> float:
        """Verifica saúde da memória com método melhorado"""
        try:
            # Tenta usar psutil se disponível
            try:
                import psutil
                memory = psutil.virtual_memory()

                # Estabelece baseline na primeira execução
                if self.memory_baseline is None:
                    self.memory_baseline = memory.percent

                # Calcula saúde baseada em uso e baseline
                current_usage = memory.percent
                health = 1.0 - (current_usage / 100)

                # Ajusta baseado em mudança desde baseline
                if self.memory_baseline > 0:
                    change = (current_usage - self.memory_baseline) / self.memory_baseline
                    if change > 0.2:  # Aumento de 20%
                        health *= 0.8

                return max(0.0, min(1.0, health))

            except ImportError:
                # Fallback: estima baseado em objetos Python
                import sys
                obj_count = len(gc.get_objects())

                # Assume que mais de 100k objetos é problemático
                health = max(0.0, 1.0 - (obj_count / 100000))
                return health

        except Exception as e:
            logger.error(f"Memory health check error: {e}", "Health")
            return 0.5

    def _check_compression_health(self) -> float:
        """Verifica saúde da compressão com teste real"""
        test_texts = [
            "INT. HOUSE - DAY\n\nJOHN enters the room.",
            "FADE IN:\n\nEXT. CITY STREET - NIGHT\n\nRain falls on empty streets.",
            "CHARACTER\n(emotional)\nThis is dialogue with some emotion."
        ]

        try:
            if self.compression_instance is None:
                self.compression_instance = CascadeCompression()

            total_ratio = 0
            successful_tests = 0

            for test_text in test_texts:
                try:
                    compressed = self.compression_instance.compress(test_text)
                    decompressed = self.compression_instance.decompress(compressed)

                    # Verifica integridade
                    if decompressed == test_text:
                        ratio = len(compressed) / len(test_text)
                        total_ratio += (1.0 - ratio)  # Quanto menor, melhor
                        successful_tests += 1
                    else:
                        logger.warning("Compression integrity check failed", "Health")

                except:
                    pass

            if successful_tests == 0:
                return 0.0

            average_health = total_ratio / successful_tests

            # Ajusta baseado em taxa de compressão geral
            overall_ratio = self.compression_instance.get_compression_ratio()
            if overall_ratio > 0.8:  # Compressão ruim
                average_health *= 0.7

            return max(0.0, min(1.0, average_health))

        except Exception as e:
            logger.error(f"Compression health check error: {e}", "Health")
            return 0.0

    def _check_performance_health(self) -> float:
        """Verifica performance com múltiplos testes"""
        try:
            import time

            # Teste 1: CPU simples
            start = time.perf_counter()
            _ = sum(i for i in range(100000))
            cpu_time = time.perf_counter() - start
            cpu_health = min(1.0, 0.01 / max(cpu_time, 0.001))

            # Teste 2: Memória
            start = time.perf_counter()
            test_list = [i for i in range(10000)]
            _ = sorted(test_list)
            mem_time = time.perf_counter() - start
            mem_health = min(1.0, 0.01 / max(mem_time, 0.001))

            # Teste 3: I/O
            start = time.perf_counter()
            test_data = "test" * 1000
            _ = hashlib.md5(test_data.encode()).hexdigest()
            io_time = time.perf_counter() - start
            io_health = min(1.0, 0.001 / max(io_time, 0.0001))

            # Média ponderada
            performance_health = (cpu_health * 0.4 + mem_health * 0.3 + io_health * 0.3)

            return max(0.0, min(1.0, performance_health))

        except Exception as e:
            logger.error(f"Performance health check error: {e}", "Health")
            return 0.5

    def _check_cache_health(self) -> float:
        """Verifica saúde dos caches"""
        # Placeholder - verificaria tamanho e hit rate de caches
        return 0.85

    def _check_harmony_health(self, omnimemory=None) -> float:
        """Verifica harmonia do OmniMemory"""
        try:
            if omnimemory:
                harmony = omnimemory.get_harmony_report()['global_harmony']
                return harmony
            return 0.5
        except:
            return 0.5

    def _repair_memory(self) -> bool:
        """Repara problemas de memória com estratégias múltiplas"""
        try:
            # 1. Força garbage collection
            gc.collect()

            # 2. Limpa objetos não referenciados
            gc.collect(2)

            # 3. Compacta heap se possível
            try:
                import ctypes
                libc = ctypes.CDLL("libc.so.6")
                libc.malloc_trim(0)
            except:
                pass

            logger.info("Memory cleanup completed", "Health")
            return True

        except Exception as e:
            logger.error(f"Memory repair failed: {e}", "Health")
            return False

    def _repair_compression(self) -> bool:
        """Repara sistema de compressão"""
        try:
            # Reinicializa compressor
            if self.compression_instance:
                # Limpa estatísticas
                self.compression_instance.compression_stats = {
                    'total_compressed': 0,
                    'total_original': 0
                }
                # Reconstrói dicionários
                for i in range(self.compression_instance.levels):
                    self.compression_instance.dictionaries[i] = \
                        self.compression_instance._create_dictionary(i)

            logger.info("Compression system reset", "Health")
            return True

        except Exception as e:
            logger.error(f"Compression repair failed: {e}", "Health")
            return False

    def _repair_performance(self) -> bool:
        """Repara problemas de performance"""
        try:
            # 1. Garbage collection
            gc.collect()

            # 2. Limpa caches grandes
            # (implementação específica dependeria dos caches usados)

            # 3. Reduz threads se muitas ativas
            import threading
            if threading.active_count() > 10:
                logger.warning(f"High thread count: {threading.active_count()}", "Health")

            logger.info("Performance optimization completed", "Health")
            return True

        except Exception as e:
            logger.error(f"Performance repair failed: {e}", "Health")
            return False

    def _repair_cache(self) -> bool:
        """Limpa e otimiza caches"""
        # Placeholder - limparia caches específicos
        return True

    def _repair_harmony(self, omnimemory=None) -> bool:
        """Tenta melhorar harmonia do OmniMemory"""
        try:
            if omnimemory and hasattr(omnimemory, 'harmonize'):
                omnimemory.harmonize()
                return True
            return False
        except:
            return False

# ==================== SISTEMA PRINCIPAL MELHORADO ====================

class ScriptureMonV2:
    """
    Sistema Principal Unificado V2.1 - Com correções e melhorias
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()

        logger.info("Inicializando ScriptureMonChampion V2.1...", "System")

        # Sistema de memória base
        try:
            self.memory = OmniMemoryV4(self.config.memory_path)
            logger.info("OmniMemory V4 carregado com sucesso", "System")
        except Exception as e:
            logger.error(f"Erro ao carregar OmniMemory: {e}", "System")
            self.memory = OmniMemoryV4(self.config.memory_path)  # Usa versão simplificada

        # Inovações integradas
        self.cross_modal = CrossModalEmbedding()
        self.memory_graph = MemoryGraph()
        self.cascade_compressor = CascadeCompression(self.config.compression_cascade_levels)
        self.adaptive_selector = AdaptiveSelector()
        self.analyzer = ScreenplayAnalyzer()
        self.self_healing = SelfHealingSystem()
        self.self_healing.compression_instance = self.cascade_compressor
        self.fallback = UniversalFallback()
        self.anomaly_detector = AnomalyDetector()

        # Thread pool
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_workers)

        # Cache melhorado com TTL
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = 3600  # 1 hora

        # Estatísticas
        self.stats = {
            'files_processed': 0,
            'total_compression_ratio': 0,
            'total_processing_time': 0,
            'errors': 0,
            'start_time': datetime.now()
        }

        # Faz verificação inicial de saúde
        initial_health = self.self_healing.check_health(self.memory, self.cascade_compressor)

        # Auto-reparo inicial se necessário
        needs_repair = any(h['score'] < 0.7 for h in initial_health.values())
        if needs_repair:
            logger.info("Sistema precisa de reparos iniciais", "System")
            repair_results = self.self_healing.auto_repair(self.memory)
            for component, result in repair_results.items():
                if result.get('repaired'):
                    logger.info(f"✅ {component} reparado", "System")
                else:
                    logger.warning(f"⚠️ Falha ao reparar {component}", "System")

        # Status final
        harmony = self.memory.get_harmony_report()['global_harmony']
        logger.info(f"✅ Sistema inicializado - Harmonia: {harmony:.1%}", "System")

        print(f"\n{'='*60}")
        print(f"✅ ScriptureMonChampion V2.1 - PRONTO")
        print(f"{'='*60}")
        print(f"   Memória: {initial_health.get('memory', {}).get('status', 'unknown')}")
        print(f"   Compressão: {initial_health.get('compression', {}).get('status', 'unknown')}")
        print(f"   Performance: {initial_health.get('performance', {}).get('status', 'unknown')}")
        print(f"   Harmonia: {harmony:.1%}")
        print(f"{'='*60}\n")

    def process_screenplay(self, file_path: str, output_format: str = 'full') -> Dict:
        """Pipeline completo melhorado"""
        start_time = datetime.now()

        try:
            # 1. Valida e normaliza entrada
            screenplay_text = self._load_and_normalize(file_path)

            if not screenplay_text:
                raise ValueError("Arquivo vazio ou não pôde ser lido")

            logger.info(f"Processando {file_path} ({len(screenplay_text)} caracteres)", "Process")

            # 2. Análise estrutural paralela
            future_analysis = self.executor.submit(self._safe_analyze, screenplay_text)

            # 3. Seleção adaptativa de algoritmo
            algorithm = self.adaptive_selector.select_algorithm(screenplay_text)
            logger.debug(f"Algoritmo selecionado: {algorithm}", "Process")

            # 4. Compressão com fallback
            compressed = self._compress_adaptive(screenplay_text, algorithm)

            # 5. Cross-modal features
            cross_modal_features = self.cross_modal.transform(
                screenplay_text[:1000],  # Usa apenas início para performance
                'text', 'emotion'
            )

            # 6. Aguarda análise
            structural_analysis = future_analysis.result(timeout=30)

            # 7. Gera hash único
            memory_key = hashlib.md5(screenplay_text.encode()).hexdigest()

            # 8. Armazena com metadados completos
            self.memory.store(
                memory_key,
                {
                    'original_path': file_path,
                    'compressed': compressed,
                    'analysis': structural_analysis,
                    'cross_modal': cross_modal_features,
                    'algorithm': algorithm,
                    'timestamp': datetime.now().isoformat(),
                    'size': {
                        'original': len(screenplay_text),
                        'compressed': len(compressed)
                    }
                },
                context='screenplay',
                importance=structural_analysis['commercial_viability']['roi_score']
            )

            # 9. Atualiza grafo
            self._update_memory_graph(memory_key, structural_analysis)

            # 10. Detecta anomalias
            compression_ratio = len(compressed) / len(screenplay_text)
            self.anomaly_detector.record_metric('compression_ratio', compression_ratio)
            is_anomaly, z_score = self.anomaly_detector.detect_anomaly('compression_ratio', compression_ratio)

            # 11. Atualiza estatísticas
            self.stats['files_processed'] += 1
            self.stats['total_compression_ratio'] += compression_ratio
            processing_time = (datetime.now() - start_time).total_seconds()
            self.stats['total_processing_time'] += processing_time

            # 12. Verifica saúde periodicamente
            if self.stats['files_processed'] % 10 == 0:
                self.self_healing.check_health(self.memory, self.cascade_compressor)

            # Prepara resultado
            result = {
                'file': file_path,
                'processing_time': f"{processing_time:.2f}s",
                'compression': {
                    'algorithm': algorithm,
                    'original_size': len(screenplay_text),
                    'compressed_size': len(compressed),
                    'ratio': compression_ratio,
                    'percentage': f"{(1-compression_ratio)*100:.1f}%",
                    'is_anomaly': is_anomaly
                },
                'structure': structural_analysis,
                'cross_modal': {
                    'dominant_emotion': cross_modal_features,
                    'color_mapping': self.cross_modal.transform(
                        screenplay_text[:100], 'text', 'color'
                    )
                },
                'memory': {
                    'key': memory_key,
                    'harmony': self.memory.get_harmony_report()['global_harmony'],
                    'related_memories': self.memory_graph.find_related(memory_key, depth=2)[:5]
                }
            }

            logger.info(f"✅ Processamento concluído em {processing_time:.2f}s", "Process")

            # Formata saída
            if output_format == 'minimal':
                return {
                    'compression_ratio': compression_ratio,
                    'compression_percentage': f"{(1-compression_ratio)*100:.1f}%",
                    'roi_score': structural_analysis['commercial_viability']['roi_score'],
                    'processing_time': processing_time
                }

            return result

        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"Erro no processamento: {e}", "Process")
            logger.error(traceback.format_exc(), "Process")

            return {
                'error': str(e),
                'file': file_path,
                'processing_time': (datetime.now() - start_time).total_seconds()
            }

    def _safe_analyze(self, text: str) -> Dict:
        """Análise com tratamento de erro"""
        try:
            return self.analyzer.analyze_structure(text)
        except Exception as e:
            logger.error(f"Erro na análise: {e}", "Analyzer")
            # Retorna análise mínima
            return {
                'act1': {'error': str(e)},
                'act2': {'error': str(e)},
                'act3': {'error': str(e)},
                'overall': {
                    'page_count': len(text.split('\n')) // 55,
                    'genre': 'unknown'
                },
                'commercial_viability': {
                    'roi_score': 1.0,
                    'estimated_budget': 1000000,
                    'predicted_audience': 1000000
                }
            }

    def _load_and_normalize(self, file_path: str) -> str:
        """Carregamento melhorado com cache TTL"""
        # Verifica cache com TTL
        if file_path in self.cache:
            cache_time = self.cache_timestamps.get(file_path, datetime.now())
            if (datetime.now() - cache_time).seconds < self.cache_ttl:
                logger.debug(f"Usando cache para {file_path}", "Loader")
                return self.cache[file_path]
            else:
                # Cache expirado
                del self.cache[file_path]
                del self.cache_timestamps[file_path]

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        try:
            # Tenta diferentes encodings
            text = None
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(path, 'r', encoding=encoding) as f:
                        text = f.read()
                        break
                except UnicodeDecodeError:
                    continue

            if text is None:
                # Última tentativa com errors='ignore'
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()

            # Normaliza quebras de linha
            text = text.replace('\r\n', '\n').replace('\r', '\n')

            # Cache com timestamp
            self.cache[file_path] = text
            self.cache_timestamps[file_path] = datetime.now()

            # Limita tamanho do cache
            if len(self.cache) > self.config.cache_size:
                # Remove mais antigo
                oldest = min(self.cache_timestamps, key=self.cache_timestamps.get)
                del self.cache[oldest]
                del self.cache_timestamps[oldest]

            logger.debug(f"Arquivo carregado: {len(text)} caracteres", "Loader")
            return text

        except Exception as e:
            logger.error(f"Erro ao carregar arquivo: {e}", "Loader")
            raise

    def _compress_adaptive(self, text: str, algorithm: str) -> str:
        """Compressão com fallback e monitoramento"""
        try:
            compressed = self.cascade_compressor.compress(text)

            # Registra performance
            ratio = len(compressed) / len(text)
            text_type = algorithm.replace('_compressor', '')
            self.adaptive_selector.record_performance(text_type, algorithm, ratio)

            # Alerta se compressão ruim
            if ratio > 0.9:
                logger.warning(f"Compressão ineficiente: {ratio:.1%}", "Compression")

            return compressed

        except Exception as e:
            logger.error(f"Erro na compressão: {e}", "Compression")
            return text  # Retorna original se falhar

    def _update_memory_graph(self, memory_key: str, analysis: Dict):
        """Atualiza grafo com limite de conexões"""
        try:
            # Registra acesso
            self.memory_graph.record_access(memory_key)

            # Conecta com memórias similares
            genre = analysis.get('overall', {}).get('genre', 'unknown')

            # Busca similares
            similar_memories = self.memory.semantic_search(
                lambda x: x.get('analysis', {}).get('overall', {}).get('genre') == genre,
                limit=5
            )

            for similar in similar_memories:
                if hasattr(similar, 'key') and similar.key != memory_key:
                    # Calcula peso baseado em similaridade
                    weight = 0.5  # Base

                    # Ajusta por ROI similar
                    try:
                        roi_diff = abs(
                            analysis.get('commercial_viability', {}).get('roi_score', 1) -
                            similar.content.get('analysis', {}).get('commercial_viability', {}).get('roi_score', 1)
                        )
                        weight += (1 - min(roi_diff, 1)) * 0.5
                    except:
                        pass

                    self.memory_graph.link(memory_key, similar.key, weight)

        except Exception as e:
            logger.error(f"Erro ao atualizar grafo: {e}", "MemoryGraph")

    def get_status(self) -> Dict:
        """Status completo melhorado"""
        uptime = (datetime.now() - self.stats['start_time']).total_seconds()

        # Verifica saúde atual
        current_health = self.self_healing.check_health(self.memory, self.cascade_compressor)

        return {
            'version': 'ScriptureMonChampion V2.1',
            'uptime': f"{uptime:.0f}s",
            'memory': {
                'harmony': self.memory.get_harmony_report()['global_harmony'],
                'total_memories': len(self.memory.nodes),
                'health': current_health.get('memory', {})
            },
            'compression': {
                'average_ratio': self.stats['total_compression_ratio'] / max(self.stats['files_processed'], 1),
                'health': current_health.get('compression', {})
            },
            'performance': {
                'files_processed': self.stats['files_processed'],
                'average_time': self.stats['total_processing_time'] / max(self.stats['files_processed'], 1),
                'errors': self.stats['errors'],
                'health': current_health.get('performance', {})
            },
            'cache': {
                'size': len(self.cache),
                'max_size': self.config.cache_size,
                'health': current_health.get('cache', {})
            },
            'overall_health': self._calculate_overall_health(current_health)
        }

    def _calculate_overall_health(self, health_report: Dict) -> Dict:
        """Calcula saúde geral do sistema"""
        scores = [h.get('score', 0) for h in health_report.values()]
        average = sum(scores) / len(scores) if scores else 0

        return {
            'score': average,
            'status': 'healthy' if average > 0.8 else 'degraded' if average > 0.5 else 'critical',
            'components_critical': len([h for h in health_report.values() if h.get('score', 0) < 0.5]),
            'components_degraded': len([h for h in health_report.values() if 0.5 <= h.get('score', 0) < 0.8])
        }

    def suggest_improvements(self, memory_key: str) -> Dict:
        """Sugestões melhoradas com priorização"""
        memory = self.memory.retrieve(memory_key)

        if not memory:
            return {'error': 'Memória não encontrada'}

        analysis = memory.get('analysis', {})
        suggestions = []

        # Análise estrutural detalhada
        self._analyze_structure_issues(analysis, suggestions)

        # Análise comercial
        self._analyze_commercial_issues(analysis, suggestions)

        # Análise técnica
        self._analyze_technical_issues(memory, suggestions)

        # Ordena por severidade
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        suggestions.sort(key=lambda x: severity_order.get(x['severity'], 4))

        return {
            'memory_key': memory_key,
            'suggestions': suggestions,
            'critical_count': len([s for s in suggestions if s['severity'] == 'critical']),
            'overall_score': self._calculate_overall_score(analysis),
            'ready_for_production': len([s for s in suggestions if s['severity'] == 'critical']) == 0
        }

    def _analyze_structure_issues(self, analysis: Dict, suggestions: List):
        """Analisa problemas estruturais"""
        act1 = analysis.get('act1', {})
        act2 = analysis.get('act2', {})
        act3 = analysis.get('act3', {})

        # Ato 1
        if not act1.get('has_hook'):
            suggestions.append({
                'type': 'structure',
                'severity': 'high',
                'location': 'Act 1 - Opening',
                'suggestion': 'Adicione um gancho forte nas primeiras 5 páginas'
            })

        if not act1.get('has_inciting_incident'):
            suggestions.append({
                'type': 'structure',
                'severity': 'critical',
                'location': 'Act 1 - Pages 10-15',
                'suggestion': 'Incidente incitante ausente - essencial para engajamento'
            })

        # Ato 2
        if not act2.get('has_midpoint'):
            suggestions.append({
                'type': 'structure',
                'severity': 'medium',
                'location': 'Act 2 - Midpoint',
                'suggestion': 'Adicione reviravolta significativa no meio do Ato 2'
            })

        if act2.get('pacing') == 'slow':
            suggestions.append({
                'type': 'pacing',
                'severity': 'medium',
                'location': 'Act 2',
                'suggestion': 'Ritmo lento detectado - considere adicionar mais conflito'
            })

        # Ato 3
        if not act3.get('has_climax'):
            suggestions.append({
                'type': 'structure',
                'severity': 'critical',
                'location': 'Act 3 - Climax',
                'suggestion': 'Clímax não identificado - fortaleça confronto final'
            })

        if act3.get('loose_ends', 0) > 3:
            suggestions.append({
                'type': 'structure',
                'severity': 'medium',
                'location': 'Act 3 - Resolution',
                'suggestion': f'{act3.get("loose_ends")} pontas soltas - resolva subtramas'
            })

    def _analyze_commercial_issues(self, analysis: Dict, suggestions: List):
        """Analisa viabilidade comercial"""
        commercial = analysis.get('commercial_viability', {})

        roi = commercial.get('roi_score', 0)
        if roi < 1.5:
            suggestions.append({
                'type': 'commercial',
                'severity': 'high',
                'suggestion': f'ROI baixo ({roi:.1f}) - reduza orçamento ou aumente appeal'
            })

        budget = commercial.get('estimated_budget', 0)
        if budget > 50_000_000:
            suggestions.append({
                'type': 'commercial',
                'severity': 'medium',
                'suggestion': f'Orçamento alto (${budget/1_000_000:.1f}M) - simplifique produção'
            })

    def _analyze_technical_issues(self, memory: Dict, suggestions: List):
        """Analisa aspectos técnicos"""
        compression = memory.get('size', {})

        if compression:
            ratio = compression.get('compressed', 1) / compression.get('original', 1)
            if ratio > 0.8:
                suggestions.append({
                    'type': 'technical',
                    'severity': 'low',
                    'suggestion': 'Compressão ineficiente - texto pode ter muita redundância'
                })

    def _calculate_overall_score(self, analysis: Dict) -> float:
        """Calcula score geral melhorado"""
        weights = {
            'structure': 0.4,
            'commercial': 0.3,
            'character': 0.15,
            'dialogue': 0.15
        }

        scores = {}

        # Score estrutural
        structure_score = 0
        structure_checks = 0

        for act in ['act1', 'act2', 'act3']:
            act_data = analysis.get(act, {})
            for key, value in act_data.items():
                if isinstance(value, bool):
                    structure_score += float(value)
                    structure_checks += 1

        scores['structure'] = structure_score / max(structure_checks, 1)

        # Score comercial
        commercial = analysis.get('commercial_viability', {})
        roi = commercial.get('roi_score', 0)
        scores['commercial'] = min(roi / 3, 1.0)  # Normaliza ROI

        # Score de personagens
        overall = analysis.get('overall', {})
        char_count = overall.get('character_count', 0)
        scores['character'] = min(char_count / 10, 1.0)  # 10+ personagens é bom

        # Score de diálogo
        dialogue_ratio = overall.get('dialogue_ratio', 0)
        scores['dialogue'] = min(dialogue_ratio / 0.4, 1.0)  # 40% diálogo é ideal

        # Calcula score ponderado
        total_score = sum(scores.get(k, 0) * v for k, v in weights.items())

        return max(0.0, min(1.0, total_score))


# ==================== ADAPTIVE SELECTOR ====================

class AdaptiveSelector:
    """Seletor adaptativo melhorado"""

    def __init__(self):
        self.classifiers = {
            'dialogue': self._is_dialogue,
            'action': self._is_action,
            'technical': self._is_technical,
            'narrative': self._is_narrative
        }
        self.performance_history = defaultdict(lambda: deque(maxlen=20))
        self.algorithm_stats = defaultdict(lambda: {'uses': 0, 'total_ratio': 0})

    def select_algorithm(self, text: str) -> str:
        """Seleciona melhor algoritmo com aprendizado"""
        # Classifica o tipo
        text_type = self._classify_text(text)

        # Verifica histórico
        if text_type in self.performance_history and len(self.performance_history[text_type]) > 5:
            # Calcula melhor performer médio
            algorithm_scores = defaultdict(list)

            for algo, ratio in self.performance_history[text_type]:
                algorithm_scores[algo].append(ratio)

            # Escolhe melhor média
            best_algo = None
            best_score = float('inf')

            for algo, scores in algorithm_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score < best_score:
                    best_score = avg_score
                    best_algo = algo

            if best_algo:
                logger.debug(f"Selected {best_algo} based on history (avg ratio: {best_score:.3f})", "Selector")
                return best_algo

        # Default por tipo
        defaults = {
            'dialogue': 'dialogue_compressor',
            'action': 'action_compressor',
            'technical': 'technical_compressor',
            'narrative': 'narrative_compressor'
        }

        return defaults.get(text_type, 'general_compressor')

    def record_performance(self, text_type: str, algorithm: str, ratio: float):
        """Registra e aprende com performance"""
        self.performance_history[text_type].append((algorithm, ratio))

        # Atualiza estatísticas
        stats = self.algorithm_stats[algorithm]
        stats['uses'] += 1
        stats['total_ratio'] += ratio

        avg_ratio = stats['total_ratio'] / stats['uses']
        logger.debug(f"Algorithm {algorithm}: {stats['uses']} uses, avg ratio: {avg_ratio:.3f}", "Selector")

    def _classify_text(self, text: str) -> str:
        """Classifica com método melhorado"""
        if not text:
            return 'general'

        # Amostra para performance
        sample = text[:5000] if len(text) > 5000 else text

        scores = {}
        for text_type, classifier in self.classifiers.items():
            scores[text_type] = classifier(sample)

        # Debug scores
        logger.debug(f"Classification scores: {scores}", "Selector")

        return max(scores.items(), key=lambda x: x[1])[0]

    def _is_dialogue(self, text: str) -> float:
        """Detecta diálogo com método melhorado"""
        indicators = [
            ('"', 2.0),  # Aspas têm peso maior
            (':', 1.0),
            ('--', 1.5),
            ('(', 0.5),
            (')', 0.5),
            ('\n    ', 2.0)  # Indentação de diálogo
        ]

        score = 0
        text_len = len(text)

        for indicator, weight in indicators:
            count = text.count(indicator)
            score += (count / max(text_len, 1)) * weight * 100

        return min(score, 1.0)

    def _is_action(self, text: str) -> float:
        """Detecta sequências de ação"""
        action_words = [
            'runs', 'jumps', 'fights', 'moves', 'grabs', 'shoots',
            'explodes', 'crashes', 'speeds', 'dives', 'attacks', 'escapes'
        ]

        text_lower = text.lower()
        count = sum(text_lower.count(word) for word in action_words)

        # Verifica também por verbos no presente
        present_verbs = len(re.findall(r'\b\w+s\b', text))

        score = (count * 10 + present_verbs) / max(len(text.split()), 1)

        return min(score, 1.0)

    def _is_technical(self, text: str) -> float:
        """Detecta elementos técnicos de roteiro"""
        patterns = [
            (r'INT\.', 3.0),
            (r'EXT\.', 3.0),
            (r'ANGLE', 2.0),
            (r'CLOSE', 2.0),
            (r'WIDE', 2.0),
            (r'CUT TO:', 2.0),
            (r'FADE', 2.0),
            (r'\([A-Z\.]+\)', 1.5)  # (V.O.), (O.S.), etc
        ]

        score = 0
        for pattern, weight in patterns:
            matches = len(re.findall(pattern, text))
            score += matches * weight

        return min(score / 100, 1.0)

    def _is_narrative(self, text: str) -> float:
        """Detecta texto narrativo/descritivo"""
        sentences = text.split('.')

        if not sentences:
            return 0

        # Narrativa tem sentenças mais longas
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)

        # E menos diálogo
        dialogue_score = self._is_dialogue(text)

        narrative_score = (avg_length / 20) * (1 - dialogue_score)

        return min(narrative_score, 1.0)


# ==================== SCREENPLAY ANALYZER (Mantido do V2) ====================

class ScreenplayAnalyzer:
    """Análise estrutural de roteiros"""

    def __init__(self):
        self.three_act_ratios = (0.25, 0.50, 0.25)

    def analyze_structure(self, screenplay: str) -> Dict:
        """Análise completa melhorada"""
        lines = screenplay.split('\n')
        total_lines = len(lines)

        if total_lines < 10:
            return self._minimal_analysis()

        # Divide em 3 atos
        act1_end = int(total_lines * self.three_act_ratios[0])
        act2_end = act1_end + int(total_lines * self.three_act_ratios[1])

        act1 = lines[:act1_end]
        act2 = lines[act1_end:act2_end]
        act3 = lines[act2_end:]

        return {
            'act1': self._analyze_act1(act1),
            'act2': self._analyze_act2(act2),
            'act3': self._analyze_act3(act3),
            'overall': self._overall_analysis(lines),
            'commercial_viability': self._commercial_analysis('\n'.join(lines))
        }

    def _minimal_analysis(self) -> Dict:
        """Análise mínima para textos muito curtos"""
        return {
            'act1': {'has_hook': False, 'has_inciting_incident': False},
            'act2': {'has_midpoint': False, 'pacing': 'unknown'},
            'act3': {'has_climax': False, 'has_resolution': False},
            'overall': {'page_count': 0, 'genre': 'unknown'},
            'commercial_viability': {'roi_score': 1.0, 'estimated_budget': 1000000}
        }

    def _analyze_act1(self, lines: List[str]) -> Dict:
        """Analisa Ato 1"""
        text = '\n'.join(lines)
        return {
            'has_hook': self._has_hook(text[:min(500, len(text))]),
            'has_inciting_incident': self._has_inciting_incident(text),
            'character_introduction': self._count_characters(text),
            'world_building': self._assess_world_building(text)
        }

    def _analyze_act2(self, lines: List[str]) -> Dict:
        """Analisa Ato 2"""
        if not lines:
            return {'has_midpoint': False, 'pacing': 'unknown'}

        text = '\n'.join(lines)
        midpoint = len(lines) // 2
        midpoint_start = max(0, midpoint - 50)
        midpoint_end = min(len(lines), midpoint + 50)

        return {
            'has_midpoint': self._has_midpoint(lines[midpoint_start:midpoint_end]),
            'rising_action': self._measure_tension(text),
            'subplot_count': self._count_subplots(text),
            'pacing': self._analyze_pacing(lines)
        }

    def _analyze_act3(self, lines: List[str]) -> Dict:
        """Analisa Ato 3"""
        text = '\n'.join(lines)
        return {
            'has_climax': self._has_climax(text),
            'has_resolution': self._has_resolution(text[-min(1000, len(text)):]),
            'loose_ends': self._check_loose_ends(text),
            'satisfaction_score': self._calculate_satisfaction(text)
        }

    def _overall_analysis(self, lines: List[str]) -> Dict:
        """Análise geral"""
        text = '\n'.join(lines)
        return {
            'page_count': max(1, len(lines) // 55),
            'dialogue_ratio': self._dialogue_ratio(text),
            'action_ratio': 1.0 - self._dialogue_ratio(text),
            'character_count': len(self._extract_characters(text)),
            'location_count': len(self._extract_locations(text)),
            'genre': self._detect_genre(text)
        }

    def _commercial_analysis(self, screenplay: str) -> Dict:
        """Análise comercial"""
        budget = self._estimate_budget(screenplay)
        audience = self._predict_audience(screenplay)

        return {
            'estimated_budget': budget,
            'predicted_audience': audience,
            'roi_score': audience / max(budget, 1),
            'marketability': self._marketability_score(screenplay)
        }

    # Métodos auxiliares (mantidos do V2 original)
    def _has_hook(self, text: str) -> bool:
        hook_indicators = ['suddenly', 'explosion', 'scream', 'mysterious', 'dead', 'blood']
        return any(ind in text.lower() for ind in hook_indicators)

    def _has_inciting_incident(self, text: str) -> bool:
        return any(word in text.lower() for word in ['but', 'however', 'when', 'until'])

    def _has_midpoint(self, lines: List[str]) -> bool:
        if not lines:
            return False
        text = '\n'.join(lines)
        return any(word in text.lower() for word in ['reveal', 'truth', 'discovers', 'realizes'])

    def _has_climax(self, text: str) -> bool:
        climax_words = ['final', 'battle', 'confrontation', 'showdown', 'face', 'fight']
        return sum(text.lower().count(word) for word in climax_words) > 3

    def _has_resolution(self, text: str) -> bool:
        return any(phrase in text.lower() for phrase in ['fade out', 'the end', 'fades to black'])

    def _count_characters(self, text: str) -> int:
        characters = re.findall(r'^[A-Z][A-Z\s]+$', text, re.MULTILINE)
        return len(set(c.strip() for c in characters if len(c.strip()) > 1))

    def _extract_characters(self, text: str) -> set:
        characters = re.findall(r'^[A-Z][A-Z\s]+$', text, re.MULTILINE)
        return set(c.strip() for c in characters if len(c.strip()) > 1)

    def _extract_locations(self, text: str) -> set:
        locations = re.findall(r'(?:INT\.|EXT\.)\s+([A-Z][A-Z\s\-]+)', text)
        return set(l.strip() for l in locations if l.strip())

    def _dialogue_ratio(self, text: str) -> float:
        if not text:
            return 0
        dialogue_lines = len(re.findall(r'^\s{5,}[A-Z]', text, re.MULTILINE))
        total_lines = len(text.split('\n'))
        return dialogue_lines / max(total_lines, 1)

    def _estimate_budget(self, screenplay: str) -> float:
        locations = len(self._extract_locations(screenplay))
        characters = len(self._extract_characters(screenplay))

        base = 1_000_000
        location_cost = locations * 100_000
        character_cost = characters * 50_000

        # Elementos caros
        expensive_elements = {
            'explosion': 2.0,
            'helicopter': 1.5,
            'airplane': 1.5,
            'spaceship': 3.0,
            'dragon': 2.5,
            'battle': 1.8,
            'army': 2.0
        }

        multiplier = 1.0
        for element, factor in expensive_elements.items():
            if element in screenplay.lower():
                multiplier = max(multiplier, factor)

        return (base + location_cost + character_cost) * multiplier

    def _predict_audience(self, screenplay: str) -> float:
        genre_multipliers = {
            'action': 3.0,
            'comedy': 2.5,
            'drama': 1.5,
            'horror': 2.0,
            'sci-fi': 2.8,
            'thriller': 2.3,
            'romance': 1.8
        }

        genre = self._detect_genre(screenplay)
        multiplier = genre_multipliers.get(genre, 1.0)

        return 10_000_000 * multiplier

    def _detect_genre(self, text: str) -> str:
        genre_keywords = {
            'action': ['fight', 'explosion', 'chase', 'gun', 'battle'],
            'comedy': ['laugh', 'joke', 'funny', 'hilarious', 'comic'],
            'drama': ['cry', 'emotion', 'feel', 'heart', 'tears'],
            'horror': ['scary', 'blood', 'scream', 'monster', 'terror'],
            'sci-fi': ['space', 'alien', 'future', 'technology', 'robot'],
            'thriller': ['mystery', 'suspense', 'danger', 'threat', 'conspiracy'],
            'romance': ['love', 'kiss', 'heart', 'passion', 'romantic']
        }

        scores = {}
        text_lower = text.lower()

        for genre, keywords in genre_keywords.items():
            score = sum(text_lower.count(kw) for kw in keywords)
            scores[genre] = score

        if not scores or max(scores.values()) == 0:
            return 'drama'  # Default

        return max(scores.items(), key=lambda x: x[1])[0]

    def _marketability_score(self, screenplay: str) -> float:
        factors = {
            'franchise_potential': any(word in screenplay.lower() for word in ['sequel', 'series', 'part']),
            'merchandising': len(self._extract_characters(screenplay)) > 5,
            'international': any(word in screenplay.lower() for word in ['world', 'global', 'international']),
            'star_vehicle': len(self._extract_characters(screenplay)) < 4  # Poucos personagens = foco no protagonista
        }

        return sum(factors.values()) / max(len(factors), 1)

    def _assess_world_building(self, text: str) -> float:
        descriptions = len(re.findall(r'\([^)]+\)', text))
        return min(descriptions / 100, 1.0)

    def _measure_tension(self, text: str) -> float:
        tension_words = ['but', 'however', 'suddenly', 'unexpected', 'danger', 'risk']
        count = sum(text.lower().count(word) for word in tension_words)
        return min(count / 50, 1.0)

    def _count_subplots(self, text: str) -> int:
        characters = self._extract_characters(text)
        return max(1, min(len(characters) // 3, 5))

    def _analyze_pacing(self, lines: List[str]) -> str:
        if not lines:
            return 'unknown'

        scene_changes = sum(1 for line in lines if any(x in line for x in ['INT.', 'EXT.']))

        ratio = scene_changes / max(len(lines), 1)

        if ratio < 0.01:
            return 'slow'
        elif ratio < 0.03:
            return 'moderate'
        else:
            return 'fast'

    def _check_loose_ends(self, text: str) -> int:
        questions = text.count('?')
        resolutions = text.count('!') + text.count('.')
        return max(0, min(questions - (resolutions // 10), 10))

    def _calculate_satisfaction(self, text: str) -> float:
        positive_endings = ['happy', 'joy', 'win', 'success', 'love', 'celebrate', 'triumph']
        count = sum(text.lower().count(word) for word in positive_endings)
        return min(count / 10, 1.0)


# ==================== FALLBACK E ANOMALY (Mantidos do V2) ====================

class UniversalFallback:
    """Sistema de fallback universal"""

    def __init__(self):
        self.implementations = {
            'mean': lambda x: sum(x) / len(x) if x else 0,
            'std': lambda x: (sum((i - sum(x)/len(x))**2 for i in x) / len(x))**0.5 if x else 0,
            'predict': lambda x: [0.5] * len(x) if isinstance(x, list) else 0.5,
            'fit': lambda x, y: None,
            'generate': lambda prompt: f"Fallback response for: {prompt[:50]}...",
            'plot': lambda x, y: print(f"Plot: {list(zip(x[:5], y[:5]))}..."),
            'load_audio': lambda f: ([0] * 1000, 22050)
        }

    def get_function(self, name: str):
        return self.implementations.get(name, lambda *args, **kwargs: None)

    def safe_import(self, module_name: str):
        try:
            return __import__(module_name)
        except ImportError:
            logger.warning(f"Module {module_name} not found, using fallback", "Fallback")

            class MockModule:
                def __getattr__(self, name):
                    return self.get_function(name)

            return MockModule()


class AnomalyDetector:
    """Detector de anomalias"""

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_history = defaultdict(lambda: deque(maxlen=window_size))
        self.thresholds = {}

    def record_metric(self, metric_name: str, value: float):
        self.metrics_history[metric_name].append(value)

        if len(self.metrics_history[metric_name]) >= 10:
            values = list(self.metrics_history[metric_name])
            mean = sum(values) / len(values)
            variance = sum((x - mean)**2 for x in values) / len(values)
            std = variance**0.5
            self.thresholds[metric_name] = (mean, std)

    def detect_anomaly(self, metric_name: str, value: float) -> Tuple[bool, float]:
        if metric_name not in self.thresholds:
            return False, 0.0

        mean, std = self.thresholds[metric_name]

        if std == 0:
            return value != mean, abs(value - mean)

        z_score = abs(value - mean) / std
        is_anomaly = z_score > 3  # 3-sigma rule

        if is_anomaly:
            logger.warning(f"Anomaly detected in {metric_name}: z-score={z_score:.2f}", "Anomaly")

        return is_anomaly, z_score

    def get_anomaly_report(self) -> Dict:
        report = {}

        for metric_name, values in self.metrics_history.items():
            if not values:
                continue

            recent_value = values[-1]
            is_anomaly, z_score = self.detect_anomaly(metric_name, recent_value)

            report[metric_name] = {
                'current_value': recent_value,
                'is_anomaly': is_anomaly,
                'z_score': z_score,
                'threshold': self.thresholds.get(metric_name, (0, 0))
            }

        return report


# ==================== CLI INTERFACE MELHORADA ====================

def main():
    """Interface CLI melhorada com mais comandos"""
    import argparse

    parser = argparse.ArgumentParser(
        description='ScriptureMonChampion V2.1 - Sistema Unificado',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s analyze -f roteiro.txt
  %(prog)s compress -f roteiro.txt -o compressed.txt
  %(prog)s improve -f roteiro.txt
  %(prog)s status
  %(prog)s health
  %(prog)s repair
        """
    )

    parser.add_argument('command',
                       choices=['analyze', 'compress', 'improve', 'status', 'health', 'repair'],
                       help='Comando a executar')
    parser.add_argument('--file', '-f', help='Arquivo de roteiro')
    parser.add_argument('--output', '-o', help='Arquivo de saída')
    parser.add_argument('--format', default='full', choices=['full', 'minimal'],
                       help='Formato de saída (default: full)')
    parser.add_argument('--debug', action='store_true', help='Modo debug')

    args = parser.parse_args()

    # Configura logging
    if args.debug:
        logger.level = Logger.DEBUG

    # Inicializa sistema
    config = Config(debug_mode=args.debug)
    system = ScriptureMonV2(config)

    try:
        if args.command == 'analyze':
            if not args.file:
                print("❌ Erro: --file é obrigatório para análise")
                return 1

            result = system.process_screenplay(args.file, args.format)

            if 'error' in result:
                print(f"❌ Erro: {result['error']}")
                return 1

            if args.format == 'minimal':
                print(f"\n📊 ANÁLISE RÁPIDA")
                print(f"{'='*40}")
                print(f"Compressão: {result['compression_percentage']}")
                print(f"ROI Score: {result['roi_score']:.2f}")
                print(f"Tempo: {result['processing_time']:.2f}s")
            else:
                print(json.dumps(result, indent=2, default=str))

        elif args.command == 'compress':
            if not args.file:
                print("❌ Erro: --file é obrigatório")
                return 1

            result = system.process_screenplay(args.file, 'minimal')

            if 'error' in result:
                print(f"❌ Erro: {result['error']}")
                return 1

            # Recupera memória
            with open(args.file, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            memory = system.memory.retrieve(file_hash)

            if not memory:
                print("❌ Erro: Falha ao recuperar memória comprimida")
                return 1

            output = args.output or args.file.replace('.', '_compressed.')

            with open(output, 'w', encoding='utf-8') as f:
                f.write(memory.get('compressed', ''))

            print(f"✅ Comprimido para: {output}")
            print(f"   Redução: {result['compression_percentage']}")

        elif args.command == 'improve':
            if not args.file:
                print("❌ Erro: --file é obrigatório")
                return 1

            # Processa primeiro
            result = system.process_screenplay(args.file)

            if 'error' in result:
                print(f"❌ Erro: {result['error']}")
                return 1

            suggestions = system.suggest_improvements(result['memory']['key'])

            print(f"\n📝 ANÁLISE DE MELHORIAS")
            print(f"{'='*60}")

            if suggestions['critical_count'] > 0:
                print(f"⚠️ {suggestions['critical_count']} problemas CRÍTICOS encontrados!\n")

            for i, suggestion in enumerate(suggestions['suggestions'], 1):
                severity_emoji = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }
                emoji = severity_emoji.get(suggestion['severity'], '⚪')

                print(f"{i}. {emoji} [{suggestion['type'].upper()}]")

                if 'location' in suggestion:
                    print(f"   📍 Local: {suggestion['location']}")

                print(f"   💡 Sugestão: {suggestion['suggestion']}\n")

            print(f"{'='*60}")
            print(f"Score Geral: {suggestions['overall_score']:.1%}")
            print(f"Pronto para Produção: {'✅ SIM' if suggestions['ready_for_production'] else '❌ NÃO'}")

        elif args.command == 'status':
            status = system.get_status()

            print(f"\n📊 STATUS DO SISTEMA")
            print(f"{'='*60}")
            print(f"Versão: {status['version']}")
            print(f"Uptime: {status['uptime']}")
            print(f"\nMEMÓRIA:")
            print(f"  Harmonia: {status['memory']['harmony']:.1%}")
            print(f"  Total de memórias: {status['memory']['total_memories']}")
            print(f"  Saúde: {status['memory']['health'].get('status', 'unknown')}")
            print(f"\nCOMPRESSÃO:")
            print(f"  Taxa média: {status['compression']['average_ratio']:.1%}")
            print(f"  Saúde: {status['compression']['health'].get('status', 'unknown')}")
            print(f"\nPERFORMANCE:")
            print(f"  Arquivos processados: {status['performance']['files_processed']}")

            if status['performance']['files_processed'] > 0:
                print(f"  Tempo médio: {status['performance']['average_time']:.2f}s")

            print(f"  Erros: {status['performance']['errors']}")
            print(f"  Saúde: {status['performance']['health'].get('status', 'unknown')}")

            overall = status['overall_health']
            print(f"\nSAÚDE GERAL: {overall['status'].upper()}")
            print(f"  Score: {overall['score']:.1%}")

            if overall['components_critical'] > 0:
                print(f"  ⚠️ Componentes críticos: {overall['components_critical']}")

            if overall['components_degraded'] > 0:
                print(f"  ⚠️ Componentes degradados: {overall['components_degraded']}")

        elif args.command == 'health':
            health = system.self_healing.check_health(system.memory, system.cascade_compressor)

            print(f"\n🏥 RELATÓRIO DE SAÚDE")
            print(f"{'='*60}")

            for component, status in health.items():
                emoji = {
                    'healthy': '✅',
                    'degraded': '🟡',
                    'critical': '🔴',
                    'error': '❌'
                }.get(status['status'], '⚪')

                print(f"{emoji} {component.upper()}")
                print(f"   Status: {status['status']}")
                print(f"   Score: {status['score']:.1%}")

                if 'error' in status:
                    print(f"   Erro: {status['error']}")

                print()

        elif args.command == 'repair':
            print("🔧 Iniciando auto-reparo...")

            repairs = system.self_healing.auto_repair(system.memory)

            print(f"\n🛠️ RESULTADOS DO REPARO")
            print(f"{'='*60}")

            success_count = 0
            for component, result in repairs.items():
                if result.get('repaired'):
                    print(f"✅ {component}: Reparado com sucesso")
                    print(f"   Score: {result['old_score']:.1%} → {result['new_score']:.1%}")
                    success_count += 1
                else:
                    print(f"❌ {component}: Falha no reparo")

                    if 'error' in result:
                        print(f"   Erro: {result['error']}")

            print(f"\n{'='*60}")
            print(f"Componentes reparados: {success_count}/{len(repairs)}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
        return 130

    except Exception as e:
        print(f"\n❌ Erro não tratado: {e}")

        if args.debug:
            import traceback
            traceback.print_exc()

        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())