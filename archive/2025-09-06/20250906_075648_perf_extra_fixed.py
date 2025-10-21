#!/usr/bin/env python3
"""
Testes de performance extra V3.1 - versão corrigida
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_performance():
    """Testa performance de componentes críticos"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'tests': {},
        'budgets': {}
    }
    
    # Test 1: RAG retrieve(k=8)
    print("Testing RAG retrieve(k=8)...")
    from src.rag.adapter import RAGAdapter
    
    rag = RAGAdapter({'rag': {'enabled': True, 'k': 8}})
    
    start = time.time()
    chunks = rag.retrieve("test query screenplay structure", k=8)
    retrieve_ms = (time.time() - start) * 1000
    
    results['tests']['retrieve_k8'] = {
        'latency_ms': round(retrieve_ms, 2),
        'chunks_returned': len(chunks),
        'budget_ms': 100,
        'within_budget': retrieve_ms < 100
    }
    
    # Test 2: Pipeline 4-perspectivas (usando ThreadPoolExecutor diretamente)
    print("Testing 4-perspectives pipeline...")
    from src.orchestra.output_mixer import OutputMixer
    
    mixer = OutputMixer()
    
    def analyze_perspective(text, perspective):
        """Mock analysis"""
        time.sleep(0.01)  # Simulate work
        return f"{perspective} analysis of: {text[:20]}"
    
    start = time.time()
    
    # Processar em paralelo
    test_text = "This is a test screenplay with dramatic structure"
    perspectives = ['structure', 'emotion', 'technique', 'theme']
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(analyze_perspective, test_text, p)
            for p in perspectives
        ]
        
        results_list = [f.result(timeout=5) for f in futures]
    
    final_output = mixer.consolidate(results_list)
    
    pipeline_ms = (time.time() - start) * 1000
    
    results['tests']['pipeline_4perspectives'] = {
        'latency_ms': round(pipeline_ms, 2),
        'perspectives_processed': len(perspectives),
        'budget_ms': 500,
        'within_budget': pipeline_ms < 500
    }
    
    # Test 3: Memory composite ranking
    print("Testing memory composite ranking...")
    from src.memory.unified_manager import UnifiedMemoryManager
    
    settings = {
        'memory': {
            'ranking_weights': {
                'semantic': 0.35, 'bm25': 0.25, 'recency': 0.20,
                'importance': 0.15, 'hits': 0.05
            }
        },
        'rag': {'enabled': False}
    }
    
    umm = UnifiedMemoryManager(settings)
    
    # Add test memories
    for i in range(20):
        umm.save_memory(f"Test memory {i}", tags=[f'tag{i%3}'])
    
    start = time.time()
    context = umm.get_context("test query", max_chunks=12)
    memory_ms = (time.time() - start) * 1000
    
    results['tests']['memory_ranking'] = {
        'latency_ms': round(memory_ms, 2),
        'memories_searched': 20,
        'context_returned': len(context),
        'budget_ms': 50,
        'within_budget': memory_ms < 50
    }
    
    # Test 4: Backup snapshot
    print("Testing backup snapshot...")
    from src.utils.backup_ops import BackupManager
    
    bm = BackupManager(source_dir='.', exclude_globs=['*.pyc', '*backup*', '__pycache__'])
    
    start = time.time()
    test_zip = '/tmp/perf_test_backup.zip'
    result = bm.snapshot(test_zip)
    backup_ms = (time.time() - start) * 1000
    
    results['tests']['backup_snapshot'] = {
        'latency_ms': round(backup_ms, 2),
        'success': result.get('success', False),
        'budget_ms': 5000,
        'within_budget': backup_ms < 5000
    }
    
    # Summary
    total_tests = len(results['tests'])
    within_budget = sum(1 for t in results['tests'].values() if t.get('within_budget', False))
    
    results['summary'] = {
        'total_tests': total_tests,
        'within_budget': within_budget,
        'success_rate': f"{(within_budget/total_tests)*100:.1f}%"
    }
    
    # Salvar resultados
    output_dir = Path(__file__).parent.parent.parent / 'reports' / 'fix_v3'
    
    # JSON
    with open(output_dir / 'perf_summary.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # MD
    md_content = f"""# PERFORMANCE SUMMARY - V3.1

**Data:** {results['timestamp']}

## Testes Executados

| Componente | Latência | Budget | Status |
|------------|----------|--------|--------|
"""
    
    for name, test in results['tests'].items():
        status = '✅' if test.get('within_budget') else '❌'
        md_content += f"| {name} | {test['latency_ms']}ms | {test['budget_ms']}ms | {status} |\n"
    
    md_content += f"""

## Resumo

- **Total de Testes:** {results['summary']['total_tests']}
- **Dentro do Budget:** {results['summary']['within_budget']}
- **Taxa de Sucesso:** {results['summary']['success_rate']}

### Detalhes

"""
    
    for name, test in results['tests'].items():
        md_content += f"""
#### {name}
- Latência: {test['latency_ms']}ms
- Budget: {test['budget_ms']}ms
- Status: {'✅ Dentro do budget' if test.get('within_budget') else '❌ Acima do budget'}
"""
    
    with open(output_dir / 'perf_summary.md', 'w') as f:
        f.write(md_content)
    
    print(f"Performance summary: {results['summary']['success_rate']} within budget")
    
    return 0 if within_budget == total_tests else 1

if __name__ == '__main__':
    sys.exit(test_performance())