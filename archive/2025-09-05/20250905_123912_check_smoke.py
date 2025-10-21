#!/usr/bin/env python3
"""Check smoke test - teste end-to-end básico"""

import sys
import json
import time
import traceback
from pathlib import Path
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa smoke test end-to-end"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Teste 1: Importar todos os módulos principais
        modules_to_import = [
            ('src.memory.unified_manager', 'UnifiedMemoryManager'),
            ('src.orchestra.output_mixer', 'OutputMixer'),
            ('src.validator.scoring', 'ScriptScorer'),
            ('src.telepathy.channel', 'TelepathyChannel'),
            ('src.rag.adapter', 'RAGAdapter'),
            ('src.utils.soulos_wrapper', 'SoulOSWrapper'),
            ('src.sdl.collector', 'SDLCollector'),
            ('src.utils.backup_ops', 'BackupManager'),
            ('src.utils.logging_setup', 'setup_logging')
        ]
        
        imported_count = 0
        for module_path, class_name in modules_to_import:
            try:
                module = __import__(module_path, fromlist=[class_name])
                if hasattr(module, class_name):
                    imported_count += 1
                else:
                    result['notes'].append(f'Missing class: {class_name} in {module_path}')
            except ImportError as e:
                result['notes'].append(f'Failed to import {module_path}: {e}')
        
        if imported_count == len(modules_to_import):
            result['details']['all_imports'] = 'PASS'
            result['notes'].append(f'All {imported_count} modules imported')
        else:
            result['details']['all_imports'] = 'FAIL'
            result['notes'].append(f'Only imported {imported_count}/{len(modules_to_import)}')
        
        # Teste 2: Pipeline completo simples
        try:
            from src.memory.unified_manager import UnifiedMemoryManager
            from src.validator.scoring import ScriptScorer
            from src.rag.adapter import RAGAdapter
            
            # Inicializar componentes
            memory = UnifiedMemoryManager(settings)
            scorer = ScriptScorer(settings)
            rag = RAGAdapter(settings)
            
            # Adicionar conhecimento
            rag.add_document('doc1', 'Test screenplay content', {'type': 'script'})
            
            # Adicionar memória
            memory.add_memory('Test memory', time.time(), 0.5, {'test': True})
            
            # Fazer query
            context = memory.get_context('test', max_memories=1)
            
            # Pontuar algo
            score_result = scorer.score('INT. ROOM - DAY\n\nA simple test.')
            
            if context and score_result:
                result['details']['simple_pipeline'] = 'PASS'
                result['notes'].append('Simple pipeline executed')
            else:
                result['details']['simple_pipeline'] = 'FAIL'
                result['notes'].append('Pipeline execution incomplete')
        except Exception as e:
            result['details']['simple_pipeline'] = 'FAIL'
            result['notes'].append(f'Pipeline failed: {e}')
        
        # Teste 3: Verificar diretórios essenciais
        essential_dirs = ['data', 'data/memory', 'logs', 'backups', 'reports']
        missing_dirs = []
        
        for dir_name in essential_dirs:
            if not Path(dir_name).exists():
                missing_dirs.append(dir_name)
        
        if not missing_dirs:
            result['details']['essential_dirs'] = 'PASS'
            result['notes'].append('All essential directories exist')
        else:
            result['details']['essential_dirs'] = 'FAIL'
            result['notes'].append(f'Missing dirs: {missing_dirs}')
        
        # Teste 4: Verificar arquivos de dados
        data_files = {
            'data/memory/unified_memory.db': 'Unified memory DB',
            'data/memory/bm25_index.db': 'BM25 index',
            'data/memory/vector_store.db': 'Vector store'
        }
        
        existing_data = []
        for file_path, description in data_files.items():
            if Path(file_path).exists():
                existing_data.append(description)
        
        if len(existing_data) >= 1:  # Pelo menos um DB deve existir
            result['details']['data_files'] = 'PASS'
            result['notes'].append(f'Found data files: {existing_data}')
        else:
            result['details']['data_files'] = 'WARN'
            result['notes'].append('No data files found')
        
        # Teste 5: Teste de integração básico
        try:
            # Simular fluxo típico
            from src.utils.logging_setup import get_logger
            
            logger = get_logger('smoke_test')
            logger.info('Starting smoke test integration')
            
            # Criar backup
            from src.utils.backup_ops import BackupManager
            backup_mgr = BackupManager(settings)
            backup_result = backup_mgr.create_backup('smoke_test')
            
            if backup_result and backup_result.get('success'):
                result['details']['integration_test'] = 'PASS'
                result['notes'].append('Integration test successful')
            else:
                result['details']['integration_test'] = 'FAIL'
                result['notes'].append('Integration test failed')
        except:
            result['details']['integration_test'] = 'FAIL'
            result['notes'].append('Integration test crashed')
        
        # Teste 6: Verificar que componentes perigosos estão desabilitados
        soulos_enabled = settings.get('soulos', {}).get('enabled', False)
        if not soulos_enabled:
            result['details']['safety_check'] = 'PASS'
            result['notes'].append('Dangerous components disabled')
        else:
            result['details']['safety_check'] = 'FAIL'
            result['notes'].append('WARNING: Dangerous components enabled!')
        
        # Teste 7: Performance básica
        start_time = time.time()
        
        # Operações simples
        for _ in range(10):
            memory.get_context('test', max_memories=1)
        
        elapsed = time.time() - start_time
        ops_per_second = 10 / elapsed
        
        if ops_per_second > 5:  # Pelo menos 5 ops/segundo
            result['details']['basic_performance'] = 'PASS'
            result['notes'].append(f'Performance OK: {ops_per_second:.1f} ops/s')
        else:
            result['details']['basic_performance'] = 'WARN'
            result['notes'].append(f'Slow performance: {ops_per_second:.1f} ops/s')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        warnings = [k for k, v in result['details'].items() if v == 'WARN']
        
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            if warnings:
                result['reason'] = f'Smoke test passed with warnings: {", ".join(warnings)}'
            else:
                result['reason'] = 'All smoke tests passed'
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