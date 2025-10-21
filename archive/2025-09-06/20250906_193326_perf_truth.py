#!/usr/bin/env python3
"""
V3.2 R4.4 PERFTRUTH - Medições REAIS de performance com RAG retrieve.

Correções aplicadas:
1. Cache invalidado entre medições
2. Queries variadas para evitar cache hits
3. Séries cold/warm separadas apropriadamente
4. Lista completa de measurements_ms preservada
5. Estatísticas calculadas corretamente (p95, p99, std)

Uso:
  python tools/fix_v3/perf_truth.py --out reports/fix_v3/v32_r4_4_perftruth/perf_summary.json
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("perf_truth")


class RAGPerformanceTester:
    """Tester de performance real para RAG retrieve."""
    
    def __init__(self):
        """Inicializa o tester com RAG adapter."""
        self.rag_adapter = None
        self.queries = [
            "screenplay three act structure fundamentals",
            "dialogue subtext technique examples",
            "character development arc transformation",
            "visual storytelling cinematography principles",
            "plot twist revelation methods",
            "emotional journey protagonist evolution",
            "scene transition techniques editing",
            "theme symbolism recurring motifs"
        ]
        self._init_rag()
    
    def _init_rag(self):
        """Inicializa RAG adapter com configuração real."""
        try:
            from src.rag.adapter import RAGAdapter
            self.rag_adapter = RAGAdapter({
                'rag': {
                    'enabled': True,
                    'provider': 'chroma',
                    'k': 8
                }
            })
            
            # Verificar se ChromaDB está conectado
            if self.rag_adapter.chroma_collection:
                count = self.rag_adapter.chroma_collection.count()
                logger.info(f"✅ RAG inicializado com ChromaDB - {count} documentos na collection '{self.rag_adapter.chroma_collection.name}'")
            else:
                logger.warning("⚠️ ChromaDB não disponível - usando fallback")
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar RAG: {e}")
            raise
    
    def _clear_cache(self):
        """Limpa cache do RAG adapter."""
        if self.rag_adapter:
            self.rag_adapter._cache.clear()
            logger.debug("Cache limpo")
    
    def _measure_single(self, query: str, k: int = 8) -> float:
        """
        Mede uma única execução de retrieve.
        
        Returns:
            Tempo em millisegundos
        """
        t0 = time.perf_counter()
        try:
            results = self.rag_adapter.retrieve(query, k=k)
            # Verificar que obtivemos resultados reais
            if not results:
                logger.warning(f"Nenhum resultado para query: {query[:30]}...")
        except Exception as e:
            logger.error(f"Erro durante retrieve: {e}")
            raise
        
        dt_ms = (time.perf_counter() - t0) * 1000.0
        return dt_ms
    
    def measure_cold_series(self, n_measurements: int = 5) -> Dict:
        """
        Mede série COLD (sem warmup, cache limpo).
        
        Args:
            n_measurements: Número de medições
            
        Returns:
            Dict com measurements_ms e estatísticas
        """
        logger.info(f"📊 Iniciando série COLD com {n_measurements} medições...")
        
        measurements_ms = []
        queries_used = []
        
        for i in range(n_measurements):
            # Limpar cache antes de cada medição cold
            self._clear_cache()
            
            # Usar query diferente para cada medição
            query = self.queries[i % len(self.queries)]
            queries_used.append(query[:50])  # Primeiros 50 chars para log
            
            # Medir
            dt_ms = self._measure_single(query)
            measurements_ms.append(dt_ms)
            logger.debug(f"Cold #{i+1}: {dt_ms:.2f}ms - Query: {query[:30]}...")
        
        # Calcular estatísticas
        stats = self._calculate_stats(measurements_ms)
        stats['queries_used'] = queries_used
        stats['series_type'] = 'cold'
        
        logger.info(f"✅ Série COLD completa: avg={stats['avg_ms']:.2f}ms, p95={stats['p95_ms']:.2f}ms")
        
        return stats
    
    def measure_warm_series(self, n_warmup: int = 3, n_measurements: int = 10) -> Dict:
        """
        Mede série WARM (com warmup, cache aquecido).
        
        Args:
            n_warmup: Número de warmup (descartados)
            n_measurements: Número de medições reais
            
        Returns:
            Dict com measurements_ms e estatísticas
        """
        logger.info(f"📊 Iniciando série WARM com {n_warmup} warmups + {n_measurements} medições...")
        
        # Warmup (descartar)
        logger.debug(f"Executando {n_warmup} warmups...")
        for i in range(n_warmup):
            query = self.queries[i % len(self.queries)]
            _ = self._measure_single(query)
        
        # Medições reais (manter cache aquecido)
        measurements_ms = []
        queries_used = []
        
        for i in range(n_measurements):
            # Usar queries variadas mas permitir cache hits parciais
            query = self.queries[i % len(self.queries)]
            queries_used.append(query[:50])
            
            # Medir
            dt_ms = self._measure_single(query)
            measurements_ms.append(dt_ms)
            logger.debug(f"Warm #{i+1}: {dt_ms:.2f}ms - Query: {query[:30]}...")
        
        # Calcular estatísticas
        stats = self._calculate_stats(measurements_ms)
        stats['queries_used'] = queries_used
        stats['series_type'] = 'warm'
        stats['warmup_rounds'] = n_warmup
        
        logger.info(f"✅ Série WARM completa: avg={stats['avg_ms']:.2f}ms, p95={stats['p95_ms']:.2f}ms")
        
        return stats
    
    def _calculate_stats(self, measurements_ms: list) -> Dict:
        """
        Calcula estatísticas completas das medições.
        
        Args:
            measurements_ms: Lista de medições em ms
            
        Returns:
            Dict com todas as estatísticas
        """
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
            'measurements_ms': [round(m, 2) for m in measurements_ms],  # Lista preservada
            'n': len(measurements_ms),
            'avg_ms': round(float(np.mean(measurements)), 2),
            'std_ms': round(float(np.std(measurements)), 2),
            'p95_ms': round(float(np.percentile(measurements, 95)), 2),
            'p99_ms': round(float(np.percentile(measurements, 99)), 2),
            'min_ms': round(float(np.min(measurements)), 2),
            'max_ms': round(float(np.max(measurements)), 2)
        }
    
    def validate_results(self, cold_stats: Dict, warm_stats: Dict) -> Dict:
        """
        Valida invariantes dos resultados.
        
        Returns:
            Dict com status das validações
        """
        validations = {
            'p95_ge_avg': True,
            'no_negative': True,
            'units_suspect': False
        }
        
        # Validar p95 >= avg (com tolerância numérica)
        tolerance = 0.001  # 1 microsegundo de tolerância
        
        if cold_stats['p95_ms'] < cold_stats['avg_ms'] - tolerance:
            validations['p95_ge_avg'] = False
            logger.warning(f"❌ Invariante violada: cold p95 ({cold_stats['p95_ms']}) < avg ({cold_stats['avg_ms']})")
        
        if warm_stats['p95_ms'] < warm_stats['avg_ms'] - tolerance:
            validations['p95_ge_avg'] = False
            logger.warning(f"❌ Invariante violada: warm p95 ({warm_stats['p95_ms']}) < avg ({warm_stats['avg_ms']})")
        
        # Validar não-negativos
        all_measurements = cold_stats['measurements_ms'] + warm_stats['measurements_ms']
        if any(m < 0 for m in all_measurements):
            validations['no_negative'] = False
            logger.warning("❌ Invariante violada: medições negativas encontradas")
        
        # Verificar se unidades estão suspeitas
        if warm_stats['avg_ms'] < 1.0:
            validations['units_suspect'] = True
            logger.warning(f"⚠️ Unidades suspeitas: warm avg = {warm_stats['avg_ms']}ms (< 1ms sugere cache excessivo ou stub)")
        
        return validations
    
    def run_complete_test(self) -> Dict:
        """
        Executa teste completo com séries cold e warm.
        
        Returns:
            Dict com todos os resultados
        """
        logger.info("=" * 60)
        logger.info("🚀 Iniciando teste de performance REAL do RAG")
        logger.info("=" * 60)
        
        # Verificar backend
        backend = "chroma" if self.rag_adapter.chroma_collection else "fallback"
        collection = self.rag_adapter.chroma_collection.name if self.rag_adapter.chroma_collection else "none"
        
        # Executar séries
        cold_stats = self.measure_cold_series(n_measurements=5)
        warm_stats = self.measure_warm_series(n_warmup=3, n_measurements=10)
        
        # Validar resultados
        invariants = self.validate_results(cold_stats, warm_stats)
        
        # Compilar resultado final
        result = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'version': 'V3.2_R4.4_PERFTRUTH',
            'backend': backend,
            'collection': collection,
            'series': {
                'cold': cold_stats,
                'warm': warm_stats
            },
            'budgets': {
                'cold_target_ms': 1500,
                'warm_target_ms': 400,
                'cold_within_budget': cold_stats['avg_ms'] <= 1500,
                'warm_within_budget': warm_stats['avg_ms'] <= 400
            },
            'units_verified': 'ms',
            'backend_verified': backend == 'chroma',
            'collection_verified': collection == 'v3_1_docs',
            'queries_used': list(set(cold_stats['queries_used'] + warm_stats['queries_used'])),
            'invariants': invariants
        }
        
        # Log resumo
        logger.info("=" * 60)
        logger.info("📊 RESUMO DOS RESULTADOS:")
        logger.info(f"Backend: {backend} | Collection: {collection}")
        logger.info(f"COLD: avg={cold_stats['avg_ms']:.2f}ms, p95={cold_stats['p95_ms']:.2f}ms (n={cold_stats['n']})")
        logger.info(f"WARM: avg={warm_stats['avg_ms']:.2f}ms, p95={warm_stats['p95_ms']:.2f}ms (n={warm_stats['n']})")
        logger.info(f"Invariantes: p95≥avg={invariants['p95_ge_avg']}, no_negative={invariants['no_negative']}")
        logger.info(f"Budgets: cold={result['budgets']['cold_within_budget']}, warm={result['budgets']['warm_within_budget']}")
        logger.info("=" * 60)
        
        return result


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Performance testing for RAG retrieve')
    parser.add_argument('--out', default='reports/fix_v3/v32_r4_4_perftruth/perf_summary.json',
                       help='Output path for results')
    args = parser.parse_args()
    
    # Criar diretório de saída
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Executar teste
    tester = RAGPerformanceTester()
    results = tester.run_complete_test()
    
    # Salvar resultados
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Resultados salvos em: {out_path}")
    
    # Salvar relatório markdown
    md_path = out_path.parent / 'phase_perftruth.md'
    with open(md_path, 'w') as f:
        f.write(f"""# FASE PERFTRUTH - V3.2 R4.4

## Mudanças Aplicadas

1. **Cache Invalidado**: Limpa cache antes de cada medição cold
2. **Queries Variadas**: 8 queries diferentes relacionadas ao corpus
3. **Séries Separadas**: Cold (0 warmup + 5) e Warm (3 warmup + 10)
4. **Lista Preservada**: measurements_ms mantido como lista completa
5. **Estatísticas Corretas**: Usa numpy.percentile para p95/p99

## Resultados

### Backend: {results['backend']} | Collection: {results['collection']}

### Série COLD
- Medições: {results['series']['cold']['measurements_ms']}
- Média: {results['series']['cold']['avg_ms']}ms
- P95: {results['series']['cold']['p95_ms']}ms
- P99: {results['series']['cold']['p99_ms']}ms

### Série WARM
- Medições: {results['series']['warm']['measurements_ms']}
- Média: {results['series']['warm']['avg_ms']}ms
- P95: {results['series']['warm']['p95_ms']}ms
- P99: {results['series']['warm']['p99_ms']}ms

### Validações
- p95 ≥ avg: {results['invariants']['p95_ge_avg']}
- Sem negativos: {results['invariants']['no_negative']}
- Unidades suspeitas: {results['invariants']['units_suspect']}

## Por Que Estas Mudanças?

- **Cache**: Impedia medições reais após primeira execução
- **Queries**: "teste" não exercitava o sistema adequadamente
- **Séries**: Misturava cold/warm incorretamente
- **Lista**: Necessária para calcular estatísticas corretas
- **numpy**: Método correto para percentis com amostras pequenas
""")
    
    logger.info(f"✅ Relatório markdown salvo em: {md_path}")


if __name__ == "__main__":
    main()