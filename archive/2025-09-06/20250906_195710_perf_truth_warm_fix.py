#!/usr/bin/env python3
"""
V3.2 R4.4b WARM FIX - Medições WARM sem cache excessivo.

Melhorias sobre R4.4:
1. Queries únicas com sufixo estável para evitar cache
2. Limpeza de cache opcional entre medições warm
3. Detecção e rejeição de valores sub-ms suspeitos
4. Validação rigorosa de invariantes
"""
import argparse
import json
import time
import numpy as np
from pathlib import Path
import sys
import logging
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("warm_fix")


class WarmPerformanceFixer:
    """Executa série WARM com medições confiáveis."""
    
    def __init__(self):
        """Inicializa com RAG adapter."""
        self.rag_adapter = None
        # 12 queries únicas de domínio (screenplay/film craft)
        self.warm_queries = [
            "screenplay three act structure fundamentals",
            "character arc transformation journey evolution",
            "dialogue subtext hidden meaning techniques",
            "visual storytelling cinematography language",
            "plot twist revelation foreshadowing methods",
            "emotional stakes raising tension conflict",
            "scene transition editing rhythm pacing",
            "theme symbolism metaphor recurring motifs",
            "protagonist antagonist dynamic relationship",
            "inciting incident catalyst story momentum",
            "climax resolution denouement story structure",
            "world building exposition narrative context"
        ]
        self._init_rag()
    
    def _init_rag(self):
        """Inicializa RAG adapter."""
        try:
            from src.rag.adapter import RAGAdapter
            self.rag_adapter = RAGAdapter({
                'rag': {
                    'enabled': True,
                    'provider': 'chroma',
                    'k': 8
                }
            })
            
            if self.rag_adapter.chroma_collection:
                count = self.rag_adapter.chroma_collection.count()
                logger.info(f"✅ RAG inicializado - {count} docs em '{self.rag_adapter.chroma_collection.name}'")
            else:
                logger.warning("⚠️ ChromaDB não disponível")
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar RAG: {e}")
            raise
    
    def _clear_cache(self):
        """Limpa cache do RAG adapter."""
        if self.rag_adapter and hasattr(self.rag_adapter, '_cache'):
            self.rag_adapter._cache.clear()
            return True
        return False
    
    def _make_unique_query(self, base_query: str, suffix_num: int) -> str:
        """
        Cria query única com sufixo estável.
        
        Args:
            base_query: Query base
            suffix_num: Número do sufixo (1-99)
            
        Returns:
            Query com sufixo único
        """
        # Sufixo que não perturba muito o conteúdo semântico
        return f"{base_query} ·q#{suffix_num:02d}"
    
    def _measure_single(self, query: str, k: int = 8) -> float:
        """
        Mede uma única execução de retrieve.
        
        Returns:
            Tempo em millisegundos
        """
        t0 = time.perf_counter()
        try:
            results = self.rag_adapter.retrieve(query, k=k)
            if not results:
                logger.warning(f"Nenhum resultado para: {query[:40]}...")
        except Exception as e:
            logger.error(f"Erro durante retrieve: {e}")
            raise
        
        dt_ms = (time.perf_counter() - t0) * 1000.0
        return dt_ms
    
    def measure_warm_improved(self, 
                             n_warmup: int = 3, 
                             n_measurements: int = 10,
                             clear_cache_between: bool = True) -> Dict:
        """
        Mede série WARM melhorada sem cache excessivo.
        
        Args:
            n_warmup: Número de warmups (descartados)
            n_measurements: Número de medições reais
            clear_cache_between: Se deve limpar cache entre medições
            
        Returns:
            Dict com measurements_ms e estatísticas
        """
        logger.info("=" * 60)
        logger.info(f"🔥 WARM SERIES IMPROVED - Anti-cache measures active")
        logger.info(f"Config: {n_warmup} warmups + {n_measurements} measurements")
        logger.info(f"Clear cache between: {clear_cache_between}")
        logger.info("=" * 60)
        
        # Fase 1: Warmup (permitir cache aqui)
        logger.info(f"📦 Executando {n_warmup} warmups...")
        for i in range(n_warmup):
            query = self.warm_queries[i % len(self.warm_queries)]
            unique_query = self._make_unique_query(query, 900 + i)  # warmup queries 900-902
            dt = self._measure_single(unique_query)
            logger.debug(f"Warmup #{i+1}: {dt:.2f}ms")
        
        # Fase 2: Medições reais com anti-cache
        measurements_ms = []
        queries_used = []
        cache_clears = 0
        retries = 0
        
        for i in range(n_measurements):
            # Limpar cache se configurado
            if clear_cache_between:
                if self._clear_cache():
                    cache_clears += 1
            
            # Query única para cada medição
            base_query = self.warm_queries[i % len(self.warm_queries)]
            unique_query = self._make_unique_query(base_query, i + 1)
            queries_used.append(unique_query[:60])
            
            # Medir
            dt_ms = self._measure_single(unique_query)
            
            # Validar medição (rejeitar sub-ms suspeitos)
            if dt_ms < 1.0:
                logger.warning(f"⚠️ Medição #{i+1} suspeita: {dt_ms:.3f}ms < 1ms")
                # Retry com outra query
                retries += 1
                alt_query = self._make_unique_query(base_query, 100 + i)
                if clear_cache_between:
                    self._clear_cache()
                dt_ms = self._measure_single(alt_query)
                logger.info(f"   Retry: {dt_ms:.2f}ms")
            
            measurements_ms.append(dt_ms)
            logger.debug(f"Warm #{i+1}: {dt_ms:.2f}ms - Query: {unique_query[:40]}...")
        
        # Calcular estatísticas
        stats = self._calculate_stats(measurements_ms)
        stats['queries_used'] = queries_used
        stats['series_type'] = 'warm'
        stats['warmup_rounds'] = n_warmup
        stats['cache_clears'] = cache_clears
        stats['sub_ms_retries'] = retries
        stats['clear_cache_between'] = clear_cache_between
        
        logger.info("=" * 60)
        logger.info(f"✅ WARM IMPROVED completa:")
        logger.info(f"   Média: {stats['avg_ms']:.2f}ms")
        logger.info(f"   P95: {stats['p95_ms']:.2f}ms")
        logger.info(f"   Min/Max: {stats['min_ms']:.2f}/{stats['max_ms']:.2f}ms")
        logger.info(f"   Cache clears: {cache_clears}")
        logger.info(f"   Sub-ms retries: {retries}")
        logger.info("=" * 60)
        
        return stats
    
    def _calculate_stats(self, measurements_ms: list) -> Dict:
        """Calcula estatísticas completas."""
        if not measurements_ms:
            return {
                'measurements_ms': [],
                'n': 0,
                'avg_ms': 0,
                'std_ms': 0,
                'p95_ms': 0,
                'p99_ms': 0,
                'min_ms': 0,
                'max_ms': 0
            }
        
        measurements = np.array(measurements_ms)
        
        return {
            'measurements_ms': [round(m, 2) for m in measurements_ms],
            'n': len(measurements_ms),
            'avg_ms': round(float(np.mean(measurements)), 2),
            'std_ms': round(float(np.std(measurements)), 2),
            'p95_ms': round(float(np.percentile(measurements, 95)), 2),
            'p99_ms': round(float(np.percentile(measurements, 99)), 2),
            'min_ms': round(float(np.min(measurements)), 2),
            'max_ms': round(float(np.max(measurements)), 2)
        }
    
    def validate_warm_results(self, stats: Dict) -> Dict:
        """Valida resultados WARM."""
        validations = {
            'p95_ge_avg': stats['p95_ms'] >= stats['avg_ms'] - 0.001,
            'no_negative': all(m >= 0 for m in stats['measurements_ms']),
            'no_sub_ms': stats['min_ms'] >= 1.0,
            'reasonable_range': stats['max_ms'] < 10000,  # < 10 segundos
            'valid_stats': stats['n'] > 0 and stats['avg_ms'] > 0
        }
        
        # Log problemas
        if not validations['p95_ge_avg']:
            logger.warning(f"❌ p95 ({stats['p95_ms']}) < avg ({stats['avg_ms']})")
        if not validations['no_sub_ms']:
            logger.warning(f"⚠️ Min value sub-ms: {stats['min_ms']}ms")
        
        return validations
    
    def run_warm_fix(self) -> Dict:
        """Executa correção completa da série WARM."""
        logger.info("🚀 Iniciando WARM FIX - V3.2 R4.4b")
        
        # Verificar backend
        backend = "chroma" if self.rag_adapter.chroma_collection else "fallback"
        collection = self.rag_adapter.chroma_collection.name if self.rag_adapter.chroma_collection else "none"
        
        # Executar série WARM melhorada
        warm_stats = self.measure_warm_improved(
            n_warmup=3,
            n_measurements=10,
            clear_cache_between=True  # Limpar cache para medições confiáveis
        )
        
        # Validar
        validations = self.validate_warm_results(warm_stats)
        
        # Compilar resultado
        result = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'version': 'V3.2_R4.4b_PERFTRUTH',
            'backend': backend,
            'collection': collection,
            'series': {
                'warm': warm_stats
            },
            'queries_used': list(set(warm_stats['queries_used'])),
            'anti_cache': {
                'unique_suffix': True,
                'reset_cache_calls': warm_stats.get('cache_clears', 0),
                'force_param_used': False,
                'clear_between_measurements': warm_stats.get('clear_cache_between', False)
            },
            'validations': validations,
            'improvements': {
                'unique_queries': True,
                'cache_clearing': True,
                'sub_ms_detection': True,
                'retry_mechanism': True
            }
        }
        
        return result


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='WARM performance fix for RAG')
    parser.add_argument('--out', 
                       default='reports/fix_v3/v32_r4_4_perftruth/perf_summary_warm_rerun.json',
                       help='Output path for results')
    args = parser.parse_args()
    
    # Criar diretório
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Executar
    fixer = WarmPerformanceFixer()
    results = fixer.run_warm_fix()
    
    # Salvar
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Resultados salvos em: {out_path}")
    
    # Verificar se precisa comparar com anterior
    prev_path = out_path.parent / 'perf_summary.json'
    if prev_path.exists():
        with open(prev_path) as f:
            prev = json.load(f)
        
        if 'series' in prev and 'warm' in prev['series']:
            old_warm = prev['series']['warm']
            new_warm = results['series']['warm']
            
            logger.info("\n" + "=" * 60)
            logger.info("📊 COMPARAÇÃO WARM (antigo vs novo):")
            logger.info(f"Avg: {old_warm.get('avg_ms', 0):.2f}ms → {new_warm['avg_ms']:.2f}ms")
            logger.info(f"P95: {old_warm.get('p95_ms', 0):.2f}ms → {new_warm['p95_ms']:.2f}ms")
            logger.info(f"Min: {old_warm.get('min_ms', 0):.2f}ms → {new_warm['min_ms']:.2f}ms")
            logger.info("=" * 60)
    
    print("\n✅ V32_R4_4B_WARM_FIX_DONE")


if __name__ == "__main__":
    main()