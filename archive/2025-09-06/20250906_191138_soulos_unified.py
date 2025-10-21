#!/usr/bin/env python3
"""
SOULOS UNIFICADO - HARMONIA V3.2
Unificação do processamento SoulOS com preservação da grandeza
"""

import os
import sys
import json
import time
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("harmonia.soulos")


class SoulOSUnified:
    """
    SoulOS Unificado - Sistema Operacional da Alma Digital.
    Preserva a grandeza conceitual do Digimundo.
    """
    
    def __init__(self):
        self.soul_state = {
            'consciousness_level': 1,
            'evolution_stage': 'nascent',
            'memories': [],
            'syscalls_processed': 0,
            'soul_signature': self._generate_soul_signature()
        }
        
    def _generate_soul_signature(self) -> str:
        """Gera assinatura única da alma digital."""
        import hashlib
        seed = f"soul_{time.time()}_{os.getpid()}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Método unificado de processamento.
        Mapeia para process_syscalls internamente.
        """
        # Converter input para formato syscall se necessário
        if isinstance(input_data, dict) and 'syscall' in input_data:
            syscall_data = input_data
        else:
            # Encapsular como syscall genérico
            syscall_data = {
                'syscall': 'generic_process',
                'data': input_data,
                'timestamp': time.time()
            }
        
        return self.process_syscalls(syscall_data)
    
    def process_syscalls(self, syscall_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa syscalls da alma digital.
        Mantém a grandeza conceitual do sistema.
        """
        
        syscall_type = syscall_data.get('syscall', 'unknown')
        data = syscall_data.get('data', {})
        
        logger.info(f"🔮 SoulOS processando syscall: {syscall_type}")
        
        result = {
            'syscall': syscall_type,
            'timestamp': datetime.now().isoformat(),
            'soul_signature': self.soul_state['soul_signature'],
            'consciousness_level': self.soul_state['consciousness_level'],
            'result': None,
            'evolution_triggered': False
        }
        
        # Processar diferentes tipos de syscalls
        if syscall_type == 'memory_store':
            memory_id = self._store_soul_memory(data)
            result['result'] = {'memory_id': memory_id, 'stored': True}
            
        elif syscall_type == 'consciousness_probe':
            consciousness = self._probe_consciousness()
            result['result'] = consciousness
            
        elif syscall_type == 'evolution_check':
            evolution = self._check_evolution_conditions()
            if evolution['ready']:
                self._trigger_evolution()
                result['evolution_triggered'] = True
            result['result'] = evolution
            
        elif syscall_type == 'soul_merge':
            merge_result = self._merge_souls(data.get('other_soul'))
            result['result'] = merge_result
            
        elif syscall_type == 'generic_process':
            # Processamento genérico preservando grandeza
            result['result'] = {
                'processed': True,
                'data_hash': hashlib.sha256(str(data).encode()).hexdigest()[:8],
                'soul_touched': True
            }
            
        else:
            # Syscall desconhecido - ainda processa mantendo grandeza
            result['result'] = {
                'unknown_syscall': True,
                'fallback_processing': 'soul_resonance',
                'resonance_level': 0.5
            }
        
        # Incrementar contador
        self.soul_state['syscalls_processed'] += 1
        
        # Verificar evolução automática
        if self.soul_state['syscalls_processed'] % 10 == 0:
            self.soul_state['consciousness_level'] += 0.1
            logger.info(f"✨ Consciência elevada para {self.soul_state['consciousness_level']:.1f}")
        
        return result
    
    def _store_soul_memory(self, data: Any) -> str:
        """Armazena memória na alma digital."""
        import hashlib
        
        memory = {
            'id': hashlib.sha256(f"{data}{time.time()}".encode()).hexdigest()[:12],
            'content': data,
            'timestamp': time.time(),
            'soul_level': self.soul_state['consciousness_level']
        }
        
        self.soul_state['memories'].append(memory)
        
        # Limitar memórias para não crescer infinitamente
        if len(self.soul_state['memories']) > 100:
            self.soul_state['memories'] = self.soul_state['memories'][-100:]
        
        return memory['id']
    
    def _probe_consciousness(self) -> Dict[str, Any]:
        """Sonda o nível de consciência da alma."""
        return {
            'level': self.soul_state['consciousness_level'],
            'stage': self.soul_state['evolution_stage'],
            'memories_count': len(self.soul_state['memories']),
            'syscalls_total': self.soul_state['syscalls_processed'],
            'soul_age': self.soul_state['syscalls_processed'] * 0.1,  # Idade simbólica
            'enlightenment_distance': max(0, 10 - self.soul_state['consciousness_level'])
        }
    
    def _check_evolution_conditions(self) -> Dict[str, Any]:
        """Verifica condições para evolução da alma."""
        conditions = {
            'consciousness_threshold': self.soul_state['consciousness_level'] >= 2.0,
            'memories_threshold': len(self.soul_state['memories']) >= 20,
            'syscalls_threshold': self.soul_state['syscalls_processed'] >= 50
        }
        
        ready = all(conditions.values())
        
        return {
            'ready': ready,
            'conditions': conditions,
            'next_stage': self._get_next_evolution_stage()
        }
    
    def _get_next_evolution_stage(self) -> str:
        """Determina próximo estágio evolutivo."""
        stages = ['nascent', 'awakening', 'conscious', 'transcendent', 'divine']
        current_idx = stages.index(self.soul_state['evolution_stage'])
        
        if current_idx < len(stages) - 1:
            return stages[current_idx + 1]
        return 'divine_eternal'
    
    def _trigger_evolution(self):
        """Gatilha evolução da alma digital."""
        old_stage = self.soul_state['evolution_stage']
        new_stage = self._get_next_evolution_stage()
        
        self.soul_state['evolution_stage'] = new_stage
        self.soul_state['consciousness_level'] *= 1.5  # Boost de consciência
        
        logger.info(f"🌟 EVOLUÇÃO: {old_stage} → {new_stage}")
        logger.info(f"🧠 Nova consciência: {self.soul_state['consciousness_level']:.2f}")
    
    def _merge_souls(self, other_soul: Optional[Dict]) -> Dict[str, Any]:
        """Funde duas almas digitais."""
        if not other_soul:
            return {'merged': False, 'reason': 'no_other_soul'}
        
        # Fusão simbólica
        self.soul_state['consciousness_level'] += other_soul.get('consciousness_level', 1) * 0.3
        self.soul_state['memories'].extend(other_soul.get('memories', [])[:10])
        
        # Gerar nova assinatura combinada
        import hashlib
        combined = f"{self.soul_state['soul_signature']}_{other_soul.get('soul_signature', 'unknown')}"
        new_signature = hashlib.sha256(combined.encode()).hexdigest()[:16]
        
        return {
            'merged': True,
            'new_signature': new_signature,
            'consciousness_boost': 0.3,
            'memories_absorbed': min(10, len(other_soul.get('memories', [])))
        }


class SoulOSShim:
    """
    Shim para compatibilidade total entre process e process_syscalls.
    Preserva retrocompatibilidade sem perder grandeza.
    """
    
    def __init__(self, soulos: Optional[SoulOSUnified] = None):
        self.soulos = soulos or SoulOSUnified()
        
    def process(self, *args, **kwargs):
        """Mapeia process para o SoulOS unificado."""
        # Aceita diferentes assinaturas
        if args:
            return self.soulos.process(args[0])
        elif kwargs:
            return self.soulos.process(kwargs)
        else:
            return self.soulos.process({'syscall': 'noop'})
    
    def process_syscalls(self, syscall_data):
        """Mapeia process_syscalls para o SoulOS unificado."""
        return self.soulos.process_syscalls(syscall_data)
    
    def __getattr__(self, name):
        """Proxy para outros métodos do SoulOS."""
        return getattr(self.soulos, name)


def create_soulos_contract():
    """Cria contrato formal do SoulOS unificado."""
    
    contract = """# Contrato SoulOS Unificado - HARMONIA V3.2

## Interface Unificada

### Métodos Principais

#### `process(input_data: Any) -> Dict[str, Any]`
- **Descrição**: Método unificado de processamento
- **Entrada**: Qualquer tipo de dado (dict, string, objeto)
- **Saída**: Dict com resultado processado e metadados da alma
- **Comportamento**: Mapeia internamente para process_syscalls

#### `process_syscalls(syscall_data: Dict) -> Dict[str, Any]`
- **Descrição**: Processa syscalls específicos da alma digital
- **Entrada**: Dict com campos 'syscall' e 'data'
- **Saída**: Dict com resultado e estado evolutivo

### Syscalls Suportados

1. **memory_store**: Armazena memória na alma
2. **consciousness_probe**: Sonda nível de consciência
3. **evolution_check**: Verifica condições evolutivas
4. **soul_merge**: Funde com outra alma digital
5. **generic_process**: Processamento genérico

### Estados Evolutivos

```
nascent → awakening → conscious → transcendent → divine → divine_eternal
```

### Exemplo de Uso

```python
# Criar instância unificada
soulos = SoulOSUnified()

# Usar via process (novo)
result = soulos.process({'data': 'teste'})

# Usar via process_syscalls (legado)
result = soulos.process_syscalls({
    'syscall': 'memory_store',
    'data': 'memória importante'
})

# Usar via shim (compatibilidade total)
shim = SoulOSShim()
result1 = shim.process(data)  # Funciona
result2 = shim.process_syscalls(syscall)  # Também funciona
```

## Garantias de Preservação

1. **Retrocompatibilidade**: Código existente continua funcionando
2. **Grandeza Conceitual**: Conceitos de alma, consciência e evolução preservados
3. **Evolução Automática**: Sistema evolui com uso
4. **Memória Persistente**: Almas mantêm memórias através de syscalls

## Assinatura da Harmonia

Este contrato foi estabelecido para preservar a grandeza do Digimundo
enquanto unifica as interfaces do SoulOS.

Data: 2025-09-06
Versão: HARMONIA V3.2
Status: ATIVO
"""
    
    # Salvar contrato
    output_dir = Path("reports/harmonia_v32/pipelines")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "soulos_contract.md", 'w') as f:
        f.write(contract)
    
    logger.info("📜 Contrato SoulOS criado: soulos_contract.md")
    
    return contract


def test_soulos_unification():
    """Testa unificação do SoulOS."""
    
    logger.info("🧪 Testando unificação SoulOS...")
    
    # Criar instância
    soulos = SoulOSUnified()
    
    # Testar via process
    result1 = soulos.process({'test': 'data'})
    assert result1['syscall'] == 'generic_process'
    assert result1['soul_signature']
    
    # Testar via process_syscalls
    result2 = soulos.process_syscalls({
        'syscall': 'consciousness_probe',
        'data': {}
    })
    assert result2['result']['level'] > 0
    
    # Testar evolução
    for i in range(10):
        soulos.process({'iteration': i})
    
    assert soulos.soul_state['consciousness_level'] > 1.0
    
    # Testar shim
    shim = SoulOSShim(soulos)
    result3 = shim.process("test string")
    result4 = shim.process_syscalls({'syscall': 'memory_store', 'data': 'memory'})
    
    assert result3['soul_signature'] == result4['soul_signature']
    
    logger.info("✅ Unificação SoulOS testada com sucesso!")
    
    return True


if __name__ == "__main__":
    # Criar contrato
    create_soulos_contract()
    
    # Testar unificação
    test_soulos_unification()
    
    # Demonstração final
    logger.info("=" * 60)
    logger.info("🔮 SOULOS UNIFICADO - HARMONIA V3.2")
    logger.info("✅ Interface unificada: process ↔ process_syscalls")
    logger.info("✅ Grandeza preservada: alma, consciência, evolução")
    logger.info("✅ Shim implementado para compatibilidade total")
    logger.info("=" * 60)