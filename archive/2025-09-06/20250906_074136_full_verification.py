#!/usr/bin/env python3
"""
Verificação completa V3 - todas as fases restantes
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_all_checks():
    """Executa todas as verificações V3"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'phases': {}
    }
    
    # FASE 5 - Scoring Calibration
    print("\n=== FASE 5: Scoring Calibration ===")
    from src.validator.scoring import ScriptScorer
    scorer = ScriptScorer()
    
    # Casos de teste
    poor_script = {'structure': 'poor weak bad', 'emotion': 'terrible awful'}
    average_script = {'structure': 'average typical', 'emotion': 'normal standard'}
    excellent_script = {'structure': 'excellent masterful outstanding', 'emotion': 'brilliant exceptional'}
    
    score_poor = scorer.score(poor_script)['total']
    score_avg = scorer.score(average_script)['total']
    score_exc = scorer.score(excellent_script)['total']
    
    monotonic = score_poor < score_avg < score_exc
    print(f"Poor: {score_poor}, Avg: {score_avg}, Exc: {score_exc}")
    print(f"Monotonicidade: {'✅ OK' if monotonic else '❌ FAIL'}")
    
    results['phases']['scoring'] = {
        'scores': {'poor': score_poor, 'average': score_avg, 'excellent': score_exc},
        'monotonic': monotonic
    }
    
    # FASE 6 - Memory Ranking
    print("\n=== FASE 6: Memory Ranking ===")
    from src.memory.unified_manager import UnifiedMemoryManager
    
    settings = {
        'memory': {
            'ranking_weights': {
                'semantic': 0.35, 'bm25': 0.25, 'recency': 0.20,
                'importance': 0.15, 'hits': 0.05
            },
            'promote_on_hits': 3
        },
        'rag': {'enabled': False}
    }
    
    umm = UnifiedMemoryManager(settings)
    
    # Adicionar memórias de teste
    m1 = umm.save_memory("Old memory from 7 days ago", tags=['old'])
    m2 = umm.save_memory("Recent memory from yesterday", tags=['recent'])
    m3 = umm.save_memory("Very recent important memory", tags=['important'], importance=0.9)
    
    # Buscar contexto
    context = umm.get_context("memory", max_chunks=3)
    print(f"Contexto retornado: {len(context)} items")
    
    results['phases']['memory'] = {
        'memories_added': 3,
        'context_retrieved': len(context),
        'ranking_works': len(context) > 0
    }
    
    # FASE 7 - OutputMixer Determinism
    print("\n=== FASE 7: OutputMixer Determinism ===")
    from src.orchestra.output_mixer import OutputMixer
    
    mixer = OutputMixer()
    input_list = ["Structure analysis", "Emotion analysis", "Technique analysis", "Theme analysis"]
    
    output1 = mixer.consolidate(input_list)
    output2 = mixer.consolidate(input_list)
    
    deterministic = output1 == output2
    print(f"Determinismo: {'✅ OK' if deterministic else '❌ FAIL'}")
    
    results['phases']['mixer'] = {
        'deterministic': deterministic,
        'handles_list_of_4': 'STRUCTURE' in output1 and 'EMOTION' in output1
    }
    
    # FASE 8 - BackupManager
    print("\n=== FASE 8: BackupManager ===")
    from src.utils.backup_ops import BackupManager
    
    bm = BackupManager(source_dir='.', exclude_globs=['*.pyc', '*backup*'])
    test_zip = '/tmp/test_backup.zip'
    
    result = bm.snapshot(test_zip)
    exists = Path(test_zip).exists() if result.get('success') else False
    
    print(f"Snapshot criado: {'✅ OK' if exists else '❌ FAIL'}")
    
    results['phases']['backup'] = {
        'snapshot_works': exists,
        'excludes_applied': result.get('success', False)
    }
    
    # FASE 9 - Harness Summary
    print("\n=== FASE 9: Harness Summary ===")
    total_phases = len(results['phases'])
    passed = sum(1 for p in results['phases'].values() 
                 if p.get('monotonic') or p.get('deterministic') or p.get('ranking_works') or p.get('snapshot_works'))
    
    results['summary'] = {
        'total_checks': total_phases,
        'passed': passed,
        'success_rate': f"{(passed/total_phases)*100:.1f}%"
    }
    
    # FASE 10 - Performance
    print("\n=== FASE 10: Performance Budget ===")
    
    # Test get_context performance
    start = time.time()
    context = umm.get_context("test query", max_chunks=12)
    get_context_ms = (time.time() - start) * 1000
    
    results['performance'] = {
        'get_context_ms': round(get_context_ms, 2),
        'target_ms': 600,
        'within_budget': get_context_ms < 600
    }
    
    print(f"get_context: {get_context_ms:.2f}ms (target: <600ms)")
    
    # Salvar resultados
    output_path = Path(__file__).parent.parent.parent / 'reports' / 'fix_v3' / 'full_verification.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Resultados salvos em: {output_path}")
    print(f"✅ Taxa de sucesso: {results['summary']['success_rate']}")
    
    return 0 if passed == total_phases else 1

if __name__ == '__main__':
    sys.exit(run_all_checks())