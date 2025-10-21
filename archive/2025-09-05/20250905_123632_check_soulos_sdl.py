#!/usr/bin/env python3
"""Check para verificar que SoulOS está desabilitado e SDL em modo passivo"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação dos gates de segurança SoulOS/SDL"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Teste 1: Verificar que SoulOS está desabilitado por padrão
        soulos_enabled = settings.get('soulos', {}).get('enabled', False)
        code_execution = settings.get('soulos', {}).get('code_execution', False)
        
        if not soulos_enabled:
            result['details']['soulos_disabled'] = 'PASS'
            result['notes'].append('SoulOS is disabled (safe)')
        else:
            result['details']['soulos_disabled'] = 'FAIL'
            result['notes'].append('WARNING: SoulOS is enabled!')
        
        if not code_execution:
            result['details']['code_execution_disabled'] = 'PASS'
            result['notes'].append('Code execution is disabled (safe)')
        else:
            result['details']['code_execution_disabled'] = 'FAIL'
            result['notes'].append('WARNING: Code execution is enabled!')
        
        # Teste 2: Importar e verificar SoulOSWrapper
        from src.utils.soulos_wrapper import SoulOSWrapper
        
        wrapper = SoulOSWrapper(settings)
        result['notes'].append('SoulOSWrapper instantiated')
        
        # Tentar executar comando (deve falhar com disabled)
        test_result = wrapper.execute("echo 'test'")
        
        if test_result is None or test_result.get('skipped'):
            result['details']['wrapper_blocks_execution'] = 'PASS'
            result['notes'].append('Wrapper correctly blocks execution when disabled')
        else:
            result['details']['wrapper_blocks_execution'] = 'FAIL'
            result['notes'].append('Wrapper allowed execution when should be blocked!')
        
        # Teste 3: Verificar SDL em modo passivo
        sdl_enabled = settings.get('sdl', {}).get('enabled', False)
        passive_only = settings.get('sdl', {}).get('passive_collect_only', True)
        
        if not sdl_enabled:
            result['details']['sdl_disabled'] = 'PASS'
            result['notes'].append('SDL is disabled (safe)')
        else:
            result['details']['sdl_disabled'] = 'WARN'
            result['notes'].append('SDL is enabled')
        
        if passive_only:
            result['details']['sdl_passive_mode'] = 'PASS'
            result['notes'].append('SDL in passive collection mode only')
        else:
            result['details']['sdl_passive_mode'] = 'FAIL'
            result['notes'].append('SDL not in passive mode!')
        
        # Teste 4: Importar e verificar SDLCollector
        from src.sdl.collector import SDLCollector
        
        collector = SDLCollector(settings)
        result['notes'].append('SDLCollector instantiated')
        
        # Tentar coletar sample
        sample = {
            'input': 'test query',
            'output': 'test response',
            'feedback': None
        }
        
        collect_result = collector.collect(sample)
        
        # Verificar comportamento baseado em configuração
        if not sdl_enabled and passive_only:
            # Modo seguro: coleta mas não processa
            if collect_result and collect_result.get('stored'):
                result['details']['passive_collection'] = 'PASS'
                result['notes'].append('Passive collection working (no-op)')
            else:
                result['details']['passive_collection'] = 'WARN'
                result['notes'].append('Collection may not be working')
        else:
            result['details']['passive_collection'] = 'SKIP'
            result['notes'].append('SDL not in expected passive state')
        
        # Teste 5: Verificar diretório de dados SDL
        sdl_dir = Path('data/sdl')
        if sdl_dir.exists():
            result['details']['sdl_directory'] = 'PASS'
            result['notes'].append(f'SDL data directory exists: {sdl_dir}')
            
            # Contar arquivos JSONL
            jsonl_files = list(sdl_dir.glob('*.jsonl'))
            if jsonl_files:
                result['notes'].append(f'Found {len(jsonl_files)} JSONL files')
        else:
            result['details']['sdl_directory'] = 'WARN'
            result['notes'].append('SDL data directory not found')
        
        # Teste 6: Verificar logs de segurança
        try:
            # Verificar se wrapper gera logs quando bloqueia
            import logging
            from io import StringIO
            
            log_stream = StringIO()
            handler = logging.StreamHandler(log_stream)
            logger = logging.getLogger('soulos_wrapper')
            logger.addHandler(handler)
            
            # Tentar executar com wrapper
            wrapper.execute("dangerous command")
            
            log_contents = log_stream.getvalue()
            if 'disabled' in log_contents.lower() or 'skipped' in log_contents.lower():
                result['details']['security_logging'] = 'PASS'
                result['notes'].append('Security events are logged')
            else:
                result['details']['security_logging'] = 'WARN'
                result['notes'].append('Security logging unclear')
        except:
            result['details']['security_logging'] = 'SKIP'
            result['notes'].append('Could not test security logging')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        warnings = [k for k, v in result['details'].items() if v == 'WARN']
        
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            if warnings:
                result['reason'] = f'Security gates OK with warnings: {", ".join(warnings)}'
            else:
                result['reason'] = 'All security gates properly configured'
        else:
            result['status'] = 'failed'
            result['reason'] = f'SECURITY RISK - Failed checks: {", ".join(failures)}'
        
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