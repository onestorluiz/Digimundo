#!/usr/bin/env python3
"""Check para verificar o sistema de telepathy/Redis com fallbacks"""

import sys
import json
import time
import traceback
from pathlib import Path
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação do sistema de telepathy"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Importar TelepathyChannel
        from src.telepathy.channel import TelepathyChannel
        
        # Verificar se Redis está habilitado nas settings
        redis_enabled = settings.get('redis', {}).get('enabled', True)
        result['notes'].append(f'Redis enabled in settings: {redis_enabled}')
        
        # Criar instância
        channel = TelepathyChannel(settings)
        result['notes'].append('TelepathyChannel instantiated')
        
        # Teste 1: Healthcheck
        is_healthy = channel.healthcheck()
        if is_healthy:
            result['details']['healthcheck'] = 'PASS'
            result['notes'].append('Channel is healthy')
        else:
            result['details']['healthcheck'] = 'WARN'
            result['notes'].append('Channel unhealthy but has fallback')
        
        # Teste 2: Enviar e receber mensagem
        test_message = {
            'type': 'test',
            'content': 'Hello from verification',
            'timestamp': time.time()
        }
        
        # Enviar
        send_success = channel.send('test_channel', test_message)
        if send_success:
            result['details']['send_message'] = 'PASS'
            result['notes'].append('Message sent successfully')
        else:
            result['details']['send_message'] = 'FAIL'
            result['notes'].append('Failed to send message')
        
        # Receber
        received = channel.receive('test_channel', timeout=1)
        if received and received.get('content') == test_message['content']:
            result['details']['receive_message'] = 'PASS'
            result['notes'].append('Message received correctly')
        else:
            result['details']['receive_message'] = 'FAIL'
            result['notes'].append('Failed to receive message')
        
        # Teste 3: Verificar fallback chain
        backend_type = channel.get_backend_type()
        result['notes'].append(f'Using backend: {backend_type}')
        
        if redis_enabled:
            # Se Redis está habilitado, deve usar Redis ou fakeredis
            if backend_type in ['redis', 'fakeredis']:
                result['details']['backend_selection'] = 'PASS'
            else:
                result['details']['backend_selection'] = 'WARN'
                result['notes'].append('Redis enabled but using fallback')
        else:
            # Se Redis está desabilitado, deve usar fallback
            if backend_type in ['fakeredis', 'mock']:
                result['details']['backend_selection'] = 'PASS'
                result['notes'].append('Correctly using fallback')
            else:
                result['details']['backend_selection'] = 'FAIL'
                result['notes'].append('Should use fallback when Redis disabled')
        
        # Teste 4: Pub/Sub funcionalidade
        def callback(msg):
            """Callback para subscription"""
            result['details']['pubsub_callback'] = 'PASS'
            return msg
        
        # Subscribe
        sub_success = channel.subscribe('pubsub_test', callback)
        if sub_success:
            result['details']['subscribe'] = 'PASS'
            result['notes'].append('Subscription successful')
            
            # Publish
            pub_success = channel.publish('pubsub_test', {'test': 'data'})
            if pub_success:
                result['details']['publish'] = 'PASS'
                result['notes'].append('Publish successful')
            else:
                result['details']['publish'] = 'FAIL'
                result['notes'].append('Publish failed')
        else:
            result['details']['subscribe'] = 'FAIL'
            result['notes'].append('Subscription failed')
        
        # Teste 5: Timeout behavior (não deve bloquear)
        start = time.time()
        timeout_result = channel.receive('empty_channel', timeout=0.5)
        elapsed = time.time() - start
        
        if elapsed < 1.0:  # Deve retornar em menos de 1 segundo
            result['details']['timeout_behavior'] = 'PASS'
            result['notes'].append(f'Timeout worked correctly ({elapsed:.2f}s)')
        else:
            result['details']['timeout_behavior'] = 'FAIL'
            result['notes'].append(f'Timeout too long ({elapsed:.2f}s)')
        
        # Teste 6: Cleanup
        cleanup_success = channel.cleanup()
        if cleanup_success:
            result['details']['cleanup'] = 'PASS'
            result['notes'].append('Cleanup successful')
        else:
            result['details']['cleanup'] = 'WARN'
            result['notes'].append('Cleanup may have failed')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        warnings = [k for k, v in result['details'].items() if v == 'WARN']
        
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            if warnings:
                result['reason'] = f'Passed with warnings: {", ".join(warnings)}'
            else:
                result['reason'] = 'All telepathy checks passed'
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