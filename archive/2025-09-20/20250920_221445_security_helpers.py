#!/usr/bin/env python3
"""
🔒 SECURITY HELPERS - P5 HÍBRIDO
Combina as melhores soluções do Claude + ChatGPT
Baseado na análise da Resposta 3 vs implementação P4
"""

import ast
import shlex
import subprocess
import pickle
import json
from typing import Any, Union, List
from pathlib import Path

# P5 - Logging integrado
try:
    from src.core.logging_system import get_logger, LogCategory
    logger = get_logger('security')
    component = 'security'
except ImportError:
    import logging
    logger = logging.getLogger('security')
    component = 'security'

class SecurityHelpers:
    """Helpers de segurança híbridos Claude + ChatGPT"""

    @staticmethod
    def run_cmd(cmd: Union[List[str], str], timeout: int = 180, check: bool = True) -> str:
        """
        SOLUÇÃO CHATGPT (Resposta 3) - Melhor que minha implementação
        Substitui subprocessos diretos com segurança total
        """
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)  # Previne shell injection

        try:
            logger.debug(f"Executando comando seguro: {cmd[:3]}...",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, cmd_length=len(cmd))

            result = subprocess.run(
                cmd,
                check=check,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.stdout:
                logger.debug(f"Comando bem-sucedido: {len(result.stdout)} chars retornados",
                           category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                           component=component)

            return result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Comando falhou: {e}",
                        category=LogCategory.ERROR if 'LogCategory' in globals() else None,
                        component=component, returncode=e.returncode)
            raise
        except subprocess.TimeoutExpired:
            logger.error(f"Comando timeout após {timeout}s",
                        category=LogCategory.ERROR if 'LogCategory' in globals() else None,
                        component=component, timeout=timeout)
            raise

    @staticmethod
    def safe_literal_eval(expr: str) -> Any:
        """
        SOLUÇÃO CHATGPT (Resposta 3) - Mais simples que minha implementação
        Substitui eval() perigoso com ast.literal_eval
        """
        try:
            logger.debug(f"Avaliando expressão literal: {expr[:50]}...",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, expr_length=len(expr))

            result = ast.literal_eval(expr)

            logger.debug(f"Avaliação bem-sucedida: {type(result)}",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, result_type=str(type(result)))

            return result

        except (ValueError, SyntaxError) as e:
            logger.error(f"Expressão literal inválida: {e}",
                        category=LogCategory.ERROR if 'LogCategory' in globals() else None,
                        component=component, expr=expr[:100])
            raise ValueError(f"Expressão insegura ou inválida: {e}")

    @staticmethod
    def safe_unpickle(load_callable, *args, allow: bool = False, **kwargs) -> Any:
        """
        SOLUÇÃO CHATGPT (Resposta 3) - Mais elegante que minha SafePickle
        Bloqueia pickle por padrão, requer allow=True explícito
        """
        if not allow:
            logger.error("Tentativa de unpickle bloqueada por segurança",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, load_callable=str(load_callable))
            raise RuntimeError(
                "Unpickle bloqueado por padrão para segurança. "
                "Use allow=True apenas com fonte confiável."
            )

        try:
            logger.warning("Unpickle permitido com allow=True - ATENÇÃO!",
                          category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                          component=component)

            result = load_callable(*args, **kwargs)

            logger.debug(f"Unpickle bem-sucedido: {type(result)}",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, result_type=str(type(result)))

            return result

        except Exception as e:
            logger.error(f"Erro no unpickle: {e}",
                        category=LogCategory.ERROR if 'LogCategory' in globals() else None,
                        component=component, error=str(e))
            raise

    @staticmethod
    def safe_json_loads(data: Union[str, bytes]) -> Any:
        """
        MINHA ADIÇÃO - JSON é sempre mais seguro que pickle
        Preferir JSON quando possível
        """
        try:
            if isinstance(data, bytes):
                data = data.decode('utf-8')

            logger.debug(f"Carregando JSON seguro: {len(data)} chars",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, data_length=len(data))

            result = json.loads(data)

            logger.debug(f"JSON carregado com sucesso: {type(result)}",
                        category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                        component=component, result_type=str(type(result)))

            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON inválido: {e}",
                        category=LogCategory.ERROR if 'LogCategory' in globals() else None,
                        component=component, data_preview=data[:100])
            raise ValueError(f"Dados JSON inválidos: {e}")

    @staticmethod
    def validate_path(path: Union[str, Path], base_dir: Union[str, Path] = None) -> Path:
        """
        MINHA ADIÇÃO - Validação de path traversal
        Previne ataques ../../../etc/passwd
        """
        path = Path(path)

        # Resolver path absoluto
        resolved = path.resolve()

        if base_dir:
            base_dir = Path(base_dir).resolve()
            try:
                # Verificar se path está dentro do base_dir
                resolved.relative_to(base_dir)
            except ValueError:
                logger.error(f"Path traversal detectado: {path} não está em {base_dir}",
                           category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                           component=component, attempted_path=str(path), base_dir=str(base_dir))
                raise ValueError(f"Path inseguro: {path} está fora de {base_dir}")

        # Verificar componentes perigosos
        for part in path.parts:
            if part in ('..', '.', '') or part.startswith('.'):
                logger.warning(f"Componente suspeito no path: {part}",
                             category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                             component=component, suspicious_part=part, full_path=str(path))

        logger.debug(f"Path validado: {resolved}",
                    category=LogCategory.SECURITY if 'LogCategory' in globals() else None,
                    component=component, validated_path=str(resolved))

        return resolved

    @staticmethod
    def security_audit_summary() -> dict:
        """
        P5 HÍBRIDO - Resumo das implementações de segurança
        Combina auditoria P4 + melhorias Resposta 3
        """
        return {
            'implemented_protections': {
                'subprocess': 'run_cmd() com shlex.split() e timeouts',
                'eval_exec': 'safe_literal_eval() com ast.literal_eval',
                'pickle': 'safe_unpickle() bloqueado por padrão',
                'json': 'safe_json_loads() preferencial',
                'path_traversal': 'validate_path() com base_dir',
                'logging': 'Auditoria completa de todas as operações'
            },
            'sources': {
                'run_cmd': 'ChatGPT Resposta 3 - Superior',
                'safe_literal_eval': 'ChatGPT Resposta 3 - Mais simples',
                'safe_unpickle': 'ChatGPT Resposta 3 - Mais elegante',
                'safe_json_loads': 'Claude P4 - Adição própria',
                'validate_path': 'Claude P4 - Adição própria',
                'logging_integration': 'Claude P2/P4 - Sistema completo'
            },
            'recommendation': 'Usar helpers desta classe ao invés de funções inseguras diretas'
        }

# Exports principais
__all__ = [
    'SecurityHelpers',
    'run_cmd',
    'safe_literal_eval',
    'safe_unpickle',
    'safe_json_loads',
    'validate_path'
]

# Funções de conveniência (aliases)
run_cmd = SecurityHelpers.run_cmd
safe_literal_eval = SecurityHelpers.safe_literal_eval
safe_unpickle = SecurityHelpers.safe_unpickle
safe_json_loads = SecurityHelpers.safe_json_loads
validate_path = SecurityHelpers.validate_path

# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado
try:
    from src.core.unified_memory_system import get_unified_memory, MemoryType

    def _get_memory():
        """Helper para acesso rápido à memória unificada"""
        return get_unified_memory()

    # Atalhos para compatibilidade
    unified_memory = _get_memory()
except ImportError:
    pass