"""
SoulOS Wrapper - Encapsula SoulOS com segurança e controles.
Garante que SoulOS seja inofensivo por padrão.
"""

import time
import logging
from typing import Optional, Dict, Any, Callable
from pathlib import Path
import threading

# Configurar logger
logger = logging.getLogger("scripturemon.soulos_wrapper")


class SoulOSWrapper:
    """
    Wrapper seguro para SoulOS.
    Verifica configurações e adiciona proteções.
    """
    
    def __init__(self, settings: Optional[Dict] = None):
        """
        Inicializa wrapper com configurações.
        
        Args:
            settings: Dicionário de configurações
        """
        self.settings = settings or {}
        self.soulos_config = self.settings.get('soulos', {})
        
        # Configurações de segurança
        self.enabled = self.soulos_config.get('enabled', False)
        self.code_execution = self.soulos_config.get('code_execution', False)
        self.timeout = self.soulos_config.get('timeout', 5.0)  # 5 segundos padrão
        self.max_retries = self.soulos_config.get('max_retries', 3)
        
        # SoulOS real (carregado apenas se habilitado)
        self.soulos = None
        
        if self.enabled:
            self._init_soulos()
        else:
            logger.info("SoulOS desabilitado nas configurações")
    
    def _init_soulos(self):
        """Inicializa SoulOS real se disponível."""
        try:
            # Tentar importar SoulOS
            from apps.scripturemon.soulos import SoulOS
            
            self.soulos = SoulOS()
            logger.info("✅ SoulOS inicializado com sucesso")
            
        except ImportError as e:
            logger.warning(f"SoulOS não disponível: {e}")
            self.soulos = None
            
        except Exception as e:
            logger.error(f"Erro ao inicializar SoulOS: {e}")
            self.soulos = None
    
    def execute(self, syscall: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Executa syscall - no-op seguro quando desabilitado.
        Criado para compatibilidade com harness.
        
        Args:
            syscall: Comando do sistema a executar
            payload: Payload opcional
            
        Returns:
            Dict com resultado da execução
        """
        logger.info(f"SoulOS.execute chamado: {syscall}")
        
        if not self.enabled:
            logger.info("SoulOS desabilitado - retornando no-op")
            return {
                'executed': False,
                'reason': 'disabled',
                'skipped': True
            }
        
        if not self.code_execution:
            logger.warning("Code execution desabilitado")
            return {
                'executed': False,
                'reason': 'code_execution_disabled',
                'skipped': True
            }
        
        # Se habilitado e tiver SoulOS real, executar
        if self.soulos:
            try:
                result = self.execute_with_timeout(
                    lambda: self.soulos.execute(syscall, payload),
                    timeout=self.default_timeout
                )
                return {
                    'executed': True,
                    'result': result
                }
            except Exception as e:
                logger.error(f"Erro ao executar syscall: {e}")
                return {
                    'executed': False,
                    'error': str(e)
                }
        
        # Fallback
        return {
            'executed': False,
            'reason': 'soulos_not_available'
        }
    
    def is_available(self) -> bool:
        """
        Verifica se SoulOS está disponível.
        
        Returns:
            True se disponível e habilitado
        """
        return self.enabled and self.soulos is not None
    
    def execute_with_timeout(self, func: Callable, *args, timeout: Optional[float] = None, **kwargs) -> Any:
        """
        Executa função com timeout.
        
        Args:
            func: Função a executar
            args: Argumentos posicionais
            timeout: Timeout em segundos
            kwargs: Argumentos nomeados
            
        Returns:
            Resultado da função ou None se timeout/erro
        """
        timeout = timeout or self.timeout
        result = [None]
        exception = [None]
        
        def wrapper():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=wrapper)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            logger.warning(f"Timeout executando {func.__name__} após {timeout}s")
            return None
        
        if exception[0]:
            logger.error(f"Erro executando {func.__name__}: {exception[0]}")
            return None
        
        return result[0]
    
    def process_response(self, response: str, context: Optional[Dict] = None) -> str:
        """
        Processa resposta procurando por syscalls SoulOS.
        
        Args:
            response: Resposta a processar
            context: Contexto opcional
            
        Returns:
            Resposta processada (ou original se SoulOS desabilitado)
        """
        # Se desabilitado, retornar resposta original
        if not self.enabled:
            logger.debug("SoulOS desabilitado, retornando resposta original")
            return response
        
        # Se não tem SoulOS, retornar original
        if not self.soulos:
            logger.debug("SoulOS não disponível, retornando resposta original")
            return response
        
        # Verificar se code_execution está habilitado
        if not self.code_execution:
            logger.info("Code execution desabilitado, syscalls ignoradas")
            return response
        
        # Processar com timeout e proteção
        try:
            logger.info("Processando resposta com SoulOS")
            
            processed = self.execute_with_timeout(
                self.soulos.process_response,
                response,
                context,
                timeout=self.timeout
            )
            
            if processed:
                logger.info(f"✅ Resposta processada com sucesso")
                return processed
            else:
                logger.warning("Processamento retornou None, usando resposta original")
                return response
                
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return response
    
    def save_memory(self, content: str, tags: Optional[list] = None) -> bool:
        """
        Salva memória no SoulOS.
        
        Args:
            content: Conteúdo a salvar
            tags: Tags opcionais
            
        Returns:
            True se salvou, False se erro/desabilitado
        """
        if not self.is_available():
            logger.debug("SoulOS não disponível para salvar memória")
            return False
        
        try:
            logger.info(f"Salvando memória no SoulOS ({len(content)} chars)")
            
            # Chamar com timeout
            result = self.execute_with_timeout(
                self.soulos.crystallize_memory,
                content,
                tags=tags,
                timeout=self.timeout
            )
            
            if result:
                logger.info("✅ Memória salva com sucesso")
                return True
            else:
                logger.warning("Falha ao salvar memória")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao salvar memória: {e}")
            return False
    
    def get_memories(self, query: str, limit: int = 5) -> list:
        """
        Busca memórias no SoulOS.
        
        Args:
            query: Query de busca
            limit: Limite de resultados
            
        Returns:
            Lista de memórias ou lista vazia
        """
        if not self.is_available():
            logger.debug("SoulOS não disponível para buscar memórias")
            return []
        
        try:
            logger.info(f"Buscando memórias: '{query}' (limit={limit})")
            
            # Chamar com timeout
            memories = self.execute_with_timeout(
                self.soulos.search_memories,
                query,
                limit=limit,
                timeout=self.timeout
            )
            
            if memories:
                logger.info(f"✅ Encontradas {len(memories)} memórias")
                return memories
            else:
                logger.debug("Nenhuma memória encontrada")
                return []
                
        except Exception as e:
            logger.error(f"Erro ao buscar memórias: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtém estatísticas do SoulOS.
        
        Returns:
            Dicionário com estatísticas
        """
        stats = {
            'enabled': self.enabled,
            'code_execution': self.code_execution,
            'available': self.is_available(),
            'timeout': self.timeout,
            'max_retries': self.max_retries
        }
        
        if self.is_available():
            try:
                # Obter stats do SoulOS real
                soulos_stats = self.execute_with_timeout(
                    lambda: {
                        'memories_count': len(self.soulos.syscall_log),
                        'soul_signature': self.soulos.soul_signature
                    },
                    timeout=1.0
                )
                
                if soulos_stats:
                    stats.update(soulos_stats)
                    
            except Exception as e:
                logger.error(f"Erro ao obter stats do SoulOS: {e}")
        
        return stats


def get_soulos_wrapper(settings: Optional[Dict] = None) -> SoulOSWrapper:
    """
    Factory function para obter wrapper SoulOS.
    
    Args:
        settings: Configurações
        
    Returns:
        Instância de SoulOSWrapper
    """
    return SoulOSWrapper(settings)


# Exemplo de configuração segura
SAFE_SOULOS_CONFIG = {
    'soulos': {
        'enabled': False,  # Desabilitado por padrão
        'code_execution': False,  # Sem execução de código
        'timeout': 5.0,  # Timeout de 5 segundos
        'max_retries': 3  # Máximo 3 tentativas
    }
}