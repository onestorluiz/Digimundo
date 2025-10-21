"""
SoulOS Shims - Unificação de métodos process/process_syscalls
HARMONIA V3.2 - Mantendo a essência do processamento de alma
"""

from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger("harmonia.soulos_shims")


class SoulOSShims:
    """Shims para compatibilidade entre diferentes interfaces do SoulOS."""
    
    def __init__(self, wrapper):
        """
        Inicializa shims com referência ao wrapper.
        
        Args:
            wrapper: Instância de SoulOSWrapper
        """
        self.wrapper = wrapper
    
    def process(self, command: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Shim: process -> execute
        Processa comando através do SoulOS.
        
        Args:
            command: Comando a processar
            context: Contexto opcional
            
        Returns:
            Resultado do processamento
        """
        # Mapear para execute que é o método real
        payload = {
            'command': command,
            'context': context or {}
        }
        
        return self.wrapper.execute(command, payload)
    
    def process_syscalls(self, syscalls: List[str], batch: bool = False) -> List[Dict[str, Any]]:
        """
        Shim: process_syscalls -> execute (batch)
        Processa múltiplas syscalls.
        
        Args:
            syscalls: Lista de syscalls
            batch: Se deve processar em batch
            
        Returns:
            Lista de resultados
        """
        results = []
        
        if batch and hasattr(self.wrapper, 'execute_batch'):
            # Se suporta batch nativo
            return self.wrapper.execute_batch(syscalls)
        else:
            # Processar uma por vez
            for syscall in syscalls:
                result = self.wrapper.execute(syscall)
                results.append(result)
        
        return results
    
    def process_with_soul(self, input_data: Any, soul_signature: str = "default") -> Dict[str, Any]:
        """
        Processa com assinatura de alma específica.
        Mantém a grandeza do conceito SoulOS.
        
        Args:
            input_data: Dados de entrada
            soul_signature: Assinatura da alma
            
        Returns:
            Resultado com contexto de alma
        """
        # Enriquecer com contexto de alma
        payload = {
            'data': input_data,
            'soul': {
                'signature': soul_signature,
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'consciousness_level': 0.8  # Nível padrão de consciência
            }
        }
        
        if hasattr(self.wrapper, 'execute'):
            result = self.wrapper.execute('process_with_soul', payload)
        else:
            # Fallback se execute não existir
            result = {
                'executed': False,
                'reason': 'SoulOS not fully initialized',
                'soul_echo': soul_signature
            }
        
        return result


def install_soulos_shims(wrapper):
    """
    Instala shims no SoulOSWrapper.
    
    Args:
        wrapper: Instância de SoulOSWrapper
        
    Returns:
        Wrapper com shims instalados
    """
    shims = SoulOSShims(wrapper)
    
    # Adicionar métodos unificados
    if not hasattr(wrapper, 'process'):
        wrapper.process = shims.process
    
    if not hasattr(wrapper, 'process_syscalls'):
        wrapper.process_syscalls = shims.process_syscalls
    
    # Adicionar método especial com alma
    wrapper.process_with_soul = shims.process_with_soul
    
    logger.info("✅ SoulOS shims instalados - process/process_syscalls unificados")
    
    return wrapper