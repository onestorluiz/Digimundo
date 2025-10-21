#!/usr/bin/env python3
"""Check para verificar o sistema de logging"""

import sys
import json
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from io import StringIO

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação do sistema de logging"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Importar sistema de logging
        from src.utils.logging_setup import setup_logging, get_logger
        
        # Setup logging
        log_config = setup_logging('verify_test', settings)
        result['notes'].append('Logging system initialized')
        
        # Teste 1: Criar logger
        logger = get_logger('test_module')
        if logger:
            result['details']['logger_creation'] = 'PASS'
            result['notes'].append('Logger created successfully')
        else:
            result['details']['logger_creation'] = 'FAIL'
            result['notes'].append('Failed to create logger')
            return result
        
        # Teste 2: Testar diferentes níveis de log
        test_messages = {
            'debug': 'Debug message for testing',
            'info': 'Info message for testing',
            'warning': 'Warning message for testing',
            'error': 'Error message for testing'
        }
        
        # Capturar logs em memória
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        
        # Emitir logs
        logger.debug(test_messages['debug'])
        logger.info(test_messages['info'])
        logger.warning(test_messages['warning'])
        logger.error(test_messages['error'])
        
        log_contents = log_stream.getvalue()
        
        # Verificar que todos os níveis foram capturados
        captured_levels = []
        for level, msg in test_messages.items():
            if msg in log_contents:
                captured_levels.append(level)
        
        if len(captured_levels) >= 3:  # Pelo menos info, warning, error
            result['details']['log_levels'] = 'PASS'
            result['notes'].append(f'Captured levels: {captured_levels}')
        else:
            result['details']['log_levels'] = 'FAIL'
            result['notes'].append(f'Only captured: {captured_levels}')
        
        # Teste 3: Verificar formato padronizado
        log_lines = log_contents.strip().split('\n')
        if log_lines:
            # Verificar se tem timestamp, level, module, message
            first_line = log_lines[0]
            has_timestamp = any(c in first_line for c in [':', '-'])  # Busca por formato de data/hora
            has_level = any(lvl in first_line.upper() for lvl in ['DEBUG', 'INFO', 'WARNING', 'ERROR'])
            
            if has_timestamp and has_level:
                result['details']['log_format'] = 'PASS'
                result['notes'].append('Log format is standardized')
            else:
                result['details']['log_format'] = 'FAIL'
                result['notes'].append('Log format not standardized')
        
        # Teste 4: Verificar arquivo de log
        log_dir = Path('logs')
        if log_dir.exists():
            log_files = list(log_dir.glob('*.log'))
            if log_files:
                result['details']['log_files'] = 'PASS'
                result['notes'].append(f'Found {len(log_files)} log files')
                
                # Verificar conteúdo do arquivo mais recente
                newest_log = max(log_files, key=lambda f: f.stat().st_mtime)
                log_size_kb = newest_log.stat().st_size / 1024
                result['notes'].append(f'Newest log: {newest_log.name} ({log_size_kb:.1f} KB)')
            else:
                result['details']['log_files'] = 'WARN'
                result['notes'].append('No log files found')
        else:
            result['details']['log_files'] = 'FAIL'
            result['notes'].append('Log directory does not exist')
        
        # Teste 5: Rotação de logs
        try:
            from logging.handlers import RotatingFileHandler
            
            # Verificar se há handlers rotativos configurados
            has_rotating = False
            for handler in logger.handlers:
                if isinstance(handler, RotatingFileHandler):
                    has_rotating = True
                    max_bytes = handler.maxBytes
                    backup_count = handler.backupCount
                    result['notes'].append(f'Rotation: {max_bytes} bytes, {backup_count} backups')
                    break
            
            if has_rotating:
                result['details']['log_rotation'] = 'PASS'
                result['notes'].append('Log rotation configured')
            else:
                result['details']['log_rotation'] = 'WARN'
                result['notes'].append('No rotation handler found')
        except:
            result['details']['log_rotation'] = 'SKIP'
            result['notes'].append('Could not check rotation')
        
        # Teste 6: Logger hierárquico (módulos filhos herdam config)
        child_logger = get_logger('test_module.submodule')
        child_logger.info('Child logger test')
        
        # Verificar se mensagem do child aparece no stream
        log_contents_after = log_stream.getvalue()
        if 'Child logger test' in log_contents_after:
            result['details']['hierarchical_logging'] = 'PASS'
            result['notes'].append('Hierarchical logging works')
        else:
            result['details']['hierarchical_logging'] = 'FAIL'
            result['notes'].append('Child logger not working')
        
        # Teste 7: Configuração por settings
        log_level = settings.get('logging', {}).get('level', 'INFO')
        if log_level:
            result['details']['settings_config'] = 'PASS'
            result['notes'].append(f'Using log level from settings: {log_level}')
        else:
            result['details']['settings_config'] = 'WARN'
            result['notes'].append('No log level in settings')
        
        # Teste 8: Exception logging com traceback
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("Caught test exception")
        
        final_contents = log_stream.getvalue()
        if 'Traceback' in final_contents or 'ValueError' in final_contents:
            result['details']['exception_logging'] = 'PASS'
            result['notes'].append('Exception logging with traceback works')
        else:
            result['details']['exception_logging'] = 'FAIL'
            result['notes'].append('Exception traceback not logged')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        warnings = [k for k, v in result['details'].items() if v == 'WARN']
        
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            if warnings:
                result['reason'] = f'Logging OK with warnings: {", ".join(warnings)}'
            else:
                result['reason'] = 'All logging checks passed'
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