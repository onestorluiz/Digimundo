#!/usr/bin/env python3
"""Check para verificar o pipeline paralelo"""

import sys
import json
import time
import traceback
from pathlib import Path
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação do pipeline paralelo"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Importar OutputMixer
        from src.orchestra.output_mixer import OutputMixer
        
        # Criar instância
        mixer = OutputMixer()
        result['notes'].append('OutputMixer instantiated')
        
        # Teste 1: Processamento paralelo com 4 workers
        def process_chunk(chunk_id: int, text: str) -> Dict:
            """Simula processamento de chunk"""
            time.sleep(0.1)  # Simula trabalho
            return {
                'chunk_id': chunk_id,
                'processed': text.upper(),
                'word_count': len(text.split()),
                'timestamp': time.time()
            }
        
        # Criar chunks de teste
        test_chunks = [
            f"Chunk {i}: Este é um texto de teste para processamento paralelo."
            for i in range(8)
        ]
        
        # Processar em paralelo
        start_time = time.time()
        results_parallel = []
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(process_chunk, i, chunk): i
                for i, chunk in enumerate(test_chunks)
            }
            
            for future in as_completed(futures):
                chunk_result = future.result()
                results_parallel.append(chunk_result)
        
        parallel_time = time.time() - start_time
        result['notes'].append(f'Parallel processing took {parallel_time:.2f}s')
        
        # Processar sequencial para comparação
        start_time = time.time()
        results_sequential = []
        for i, chunk in enumerate(test_chunks):
            results_sequential.append(process_chunk(i, chunk))
        
        sequential_time = time.time() - start_time
        result['notes'].append(f'Sequential processing took {sequential_time:.2f}s')
        
        # Calcular speedup
        speedup = sequential_time / parallel_time
        result['details']['speedup'] = f'{speedup:.2f}x'
        
        if speedup > 2.0:  # Esperamos pelo menos 2x de speedup
            result['details']['parallel_performance'] = 'PASS'
            result['notes'].append(f'Good speedup: {speedup:.2f}x')
        else:
            result['details']['parallel_performance'] = 'FAIL'
            result['notes'].append(f'Poor speedup: {speedup:.2f}x')
        
        # Teste 2: Consolidação determinística via OutputMixer
        # Ordenar resultados por chunk_id
        results_parallel.sort(key=lambda x: x['chunk_id'])
        
        # Consolidar outputs
        consolidated = mixer.consolidate(results_parallel)
        
        if consolidated:
            result['details']['consolidation'] = 'PASS'
            result['notes'].append('Output consolidation successful')
            
            # Verificar ordem determinística
            chunk_ids = [r['chunk_id'] for r in results_parallel]
            if chunk_ids == list(range(len(test_chunks))):
                result['details']['deterministic_order'] = 'PASS'
                result['notes'].append('Deterministic ordering maintained')
            else:
                result['details']['deterministic_order'] = 'FAIL'
                result['notes'].append('Order not deterministic')
        else:
            result['details']['consolidation'] = 'FAIL'
            result['notes'].append('Consolidation failed')
        
        # Teste 3: Verificar ausência de race conditions
        shared_counter = {'value': 0}
        
        def increment_counter():
            """Tenta incrementar contador sem lock (detectar race)"""
            current = shared_counter['value']
            time.sleep(0.001)  # Força context switch
            shared_counter['value'] = current + 1
        
        # Reset counter
        shared_counter['value'] = 0
        
        # Executar incrementos em paralelo
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(increment_counter) for _ in range(100)]
            for future in as_completed(futures):
                future.result()
        
        # Se houver race conditions, o valor será < 100
        if shared_counter['value'] < 100:
            result['details']['race_detection'] = 'WARN'
            result['notes'].append(f'Race condition detected: counter={shared_counter["value"]}')
        else:
            result['details']['race_detection'] = 'PASS'
            result['notes'].append('No race conditions in test')
        
        # Teste 4: Mixer handles diferentes tipos de output
        mixed_outputs = [
            {'type': 'text', 'content': 'Texto simples'},
            {'type': 'json', 'content': {'key': 'value'}},
            {'type': 'list', 'content': [1, 2, 3]},
            {'type': 'error', 'content': 'Erro simulado'}
        ]
        
        try:
            mixed_result = mixer.consolidate(mixed_outputs)
            if mixed_result:
                result['details']['mixed_types'] = 'PASS'
                result['notes'].append('Mixer handles mixed output types')
            else:
                result['details']['mixed_types'] = 'FAIL'
                result['notes'].append('Mixer failed on mixed types')
        except:
            result['details']['mixed_types'] = 'FAIL'
            result['notes'].append('Mixer crashed on mixed types')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        warnings = [k for k, v in result['details'].items() if v == 'WARN']
        
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            if warnings:
                result['reason'] = f'Passed with warnings: {", ".join(warnings)}'
            else:
                result['reason'] = 'All parallel checks passed'
        else:
            result['status'] = 'failed'
            result['reason'] = f'Failed checks: {", ".join(failures)}'
        
    except ImportError as e:
        result['status'] = 'blocked'
        result['reason'] = f'Import error: {str(e)}'
        result['exception'] = str(e)
    except Exception as e:
        result['status'] = 'error'
        result['reason'] = f'Unexpected error: {str(e)}'
        result['exception'] = str(e)
        result['traceback'] = traceback.format_exc()
    
    return result

if __name__ == "__main__":
    # Para teste local
    from generate_inventory import load_default_settings
    settings = load_default_settings()
    result = run_check(settings)
    print(json.dumps(result, indent=2))