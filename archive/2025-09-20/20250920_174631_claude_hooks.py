#!/usr/bin/env python3
"""
🪝 CLAUDE CODE HOOKS - Sistema de Interceptação de Comandos
Integração REAL entre Claude Code e Crystal Memory
"""

import sys
import os
import json
import subprocess
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import hashlib
import pickle

from apps.scripturemon.rules_memory import CrystalMemory
from apps.scripturemon.rules_validator import RulesValidator, ActionType, ValidationLevel
from apps.scripturemon.claude_integration import ClaudeIntegration

class ClaudeHooks:
    """
    Sistema de hooks que intercepta comandos do Claude Code
    e valida contra Crystal Memory antes de executar
    """

    def __init__(self):
        self.memory = CrystalMemory()
        self.validator = RulesValidator(self.memory, ValidationLevel.NORMAL)
        self.integration = ClaudeIntegration()

        # Contexto persistente
        self.context_db = Path("data/claude_context.db")
        self.context_db.parent.mkdir(parents=True, exist_ok=True)
        self._init_context_db()

        # Hooks registrados
        self.hooks = {
            'pre_file_create': [],
            'pre_file_modify': [],
            'pre_file_delete': [],
            'pre_command_run': [],
            'post_action': []
        }

        # Registrar hooks padrão
        self._register_default_hooks()

        # Session ID único
        self.session_id = self._get_or_create_session()

        print(f"🪝 Claude Hooks inicializado (sessão: {self.session_id[:8]}...)")

    def _init_context_db(self):
        """Inicializa banco de contexto persistente"""
        conn = sqlite3.connect(self.context_db)
        cursor = conn.cursor()

        # Tabela de sessões
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TEXT,
                last_active TEXT,
                context_data TEXT,
                rules_state TEXT
            )
        """)

        # Tabela de ações interceptadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intercepted_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                action_type TEXT,
                action_data TEXT,
                allowed BOOLEAN,
                violations TEXT,
                executed BOOLEAN
            )
        """)

        conn.commit()
        conn.close()

    def _get_or_create_session(self) -> str:
        """Obtém ou cria sessão persistente"""
        # Tentar recuperar sessão ativa
        conn = sqlite3.connect(self.context_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT session_id, context_data
            FROM sessions
            WHERE datetime(last_active) > datetime('now', '-1 hour')
            ORDER BY last_active DESC
            LIMIT 1
        """)

        result = cursor.fetchone()

        if result:
            session_id = result[0]
            # Atualizar última atividade
            cursor.execute("""
                UPDATE sessions
                SET last_active = ?
                WHERE session_id = ?
            """, (datetime.now().isoformat(), session_id))

            # Recuperar contexto
            if result[1]:
                try:
                    context = json.loads(result[1])
                    self._restore_context(context)
                except:
                    pass

            conn.commit()
            conn.close()
            return session_id

        # Criar nova sessão
        session_id = hashlib.sha256(
            f"{datetime.now().isoformat()}{os.getpid()}".encode()
        ).hexdigest()

        cursor.execute("""
            INSERT INTO sessions (session_id, created_at, last_active)
            VALUES (?, ?, ?)
        """, (session_id, datetime.now().isoformat(), datetime.now().isoformat()))

        conn.commit()
        conn.close()

        return session_id

    def _register_default_hooks(self):
        """Registra hooks padrão para validação"""

        # Hook para criação de arquivo
        self.register_hook('pre_file_create', self._validate_file_creation)

        # Hook para modificação
        self.register_hook('pre_file_modify', self._validate_file_modification)

        # Hook para comandos
        self.register_hook('pre_command_run', self._validate_command)

        # Hook pós-ação para aprendizado
        self.register_hook('post_action', self._learn_from_action)

    def register_hook(self, event: str, callback: Callable):
        """Registra um hook para evento"""
        if event in self.hooks:
            self.hooks[event].append(callback)

    def intercept_action(self, action_type: str, action_data: Dict) -> Dict[str, Any]:
        """
        Intercepta e valida ação antes de executar

        Args:
            action_type: Tipo da ação (file_create, file_modify, etc)
            action_data: Dados da ação

        Returns:
            Dict com resultado da interceptação
        """
        # Determinar tipo de ação
        action_enum = self._map_action_type(action_type)

        # Adicionar descrição se não existe
        if 'description' not in action_data:
            action_data['description'] = f"{action_type}: {action_data.get('file_path', 'unknown')}"

        # Validar com Crystal Memory
        valid, warnings, errors = self.validator.validate_action(action_enum, action_data)

        # Executar hooks pre-action
        hook_results = []
        for hook in self.hooks.get(f'pre_{action_type}', []):
            result = hook(action_data)
            hook_results.append(result)

            # Se algum hook bloqueia, parar
            if result and not result.get('allow', True):
                valid = False
                errors.append(result.get('reason', 'Bloqueado por hook'))

        # Registrar interceptação
        self._log_interception(action_type, action_data, valid, errors)

        # Preparar resposta
        response = {
            'allowed': valid,
            'errors': errors,
            'warnings': warnings,
            'action_type': action_type,
            'session_id': self.session_id,
            'hook_results': hook_results
        }

        # Se permitido, executar hooks post-action
        if valid:
            for hook in self.hooks.get('post_action', []):
                hook(action_data, response)

        # Salvar contexto
        self._save_context()

        return response

    def _map_action_type(self, action_type: str) -> ActionType:
        """Mapeia string para enum ActionType"""
        mapping = {
            'file_create': ActionType.FILE_CREATE,
            'file_modify': ActionType.FILE_MODIFY,
            'file_delete': ActionType.FILE_DELETE,
            'command_run': ActionType.COMMAND_ADD,
            'analysis': ActionType.ANALYSIS_RUN,
            'test': ActionType.TEST_RUN,
            'ollama': ActionType.OLLAMA_QUERY
        }
        return mapping.get(action_type, ActionType.FILE_MODIFY)

    def _validate_file_creation(self, action_data: Dict) -> Dict:
        """Hook para validar criação de arquivo"""
        file_path = Path(action_data.get('file_path', ''))

        # Verificar se é sistema duplicado
        if 'scripturemon' in file_path.stem.lower() and any(
            x in file_path.stem.lower() for x in ['2', 'new', 'improved', 'better']
        ):
            return {
                'allow': False,
                'reason': 'Sistema duplicado detectado - modificar existente'
            }

        # Verificar se arquivo similar existe
        if file_path.suffix == '.py':
            similar_files = list(file_path.parent.glob(f"*{file_path.stem[:-2]}*.py"))
            if similar_files:
                return {
                    'allow': True,
                    'warning': f'Arquivo similar existe: {similar_files[0].name}'
                }

        return {'allow': True}

    def _validate_file_modification(self, action_data: Dict) -> Dict:
        """Hook para validar modificação de arquivo"""
        file_path = action_data.get('file_path', '')
        code = action_data.get('code', '')

        # Verificar uso de argparse/click em CLI
        if 'cli' in file_path.lower() and code:
            if 'import argparse' in code or 'import click' in code:
                return {
                    'allow': False,
                    'reason': 'CLI deve usar Typer, não argparse/click'
                }

        return {'allow': True}

    def _validate_command(self, action_data: Dict) -> Dict:
        """Hook para validar execução de comando"""
        command = action_data.get('command', '')

        # Verificar comandos perigosos
        dangerous = ['rm -rf', 'sudo rm', 'format', 'del /f']
        for danger in dangerous:
            if danger in command.lower():
                return {
                    'allow': False,
                    'reason': f'Comando perigoso detectado: {danger}'
                }

        return {'allow': True}

    def _learn_from_action(self, action_data: Dict, result: Dict):
        """Hook para aprender com ações executadas"""
        if not result.get('allowed'):
            # Aprender com violação
            for error in result.get('errors', []):
                self.memory.learn_from_violation(
                    rule_id=1,  # Simplificado
                    pattern=action_data.get('description', '')
                )

    def _log_interception(self, action_type: str, action_data: Dict,
                          allowed: bool, violations: List[str]):
        """Registra interceptação no banco"""
        conn = sqlite3.connect(self.context_db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO intercepted_actions
            (session_id, timestamp, action_type, action_data, allowed, violations, executed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.session_id,
            datetime.now().isoformat(),
            action_type,
            json.dumps(action_data),
            allowed,
            json.dumps(violations),
            allowed
        ))

        conn.commit()
        conn.close()

    def _save_context(self):
        """Salva contexto da sessão"""
        context = {
            'session_id': self.session_id,
            'memory_stats': self.memory.get_stats() if hasattr(self.memory, 'get_stats') else {},
            'validator_level': self.validator.level.value
        }

        conn = sqlite3.connect(self.context_db)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE sessions
            SET context_data = ?, last_active = ?
            WHERE session_id = ?
        """, (
            json.dumps(context),
            datetime.now().isoformat(),
            self.session_id
        ))

        conn.commit()
        conn.close()

    def _restore_context(self, context: Dict):
        """Restaura contexto da sessão anterior"""
        # Restaurar nível de validação
        if 'validator_level' in context:
            self.validator.level = ValidationLevel(context['validator_level'])

    def get_session_history(self) -> List[Dict]:
        """Retorna histórico de ações da sessão"""
        conn = sqlite3.connect(self.context_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, action_type, action_data, allowed, violations
            FROM intercepted_actions
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT 20
        """, (self.session_id,))

        history = []
        for row in cursor.fetchall():
            history.append({
                'timestamp': row[0],
                'action_type': row[1],
                'action_data': json.loads(row[2]),
                'allowed': bool(row[3]),
                'violations': json.loads(row[4]) if row[4] else []
            })

        conn.close()
        return history

    def validate_before_action(self, description: str) -> bool:
        """
        Método simplificado para Claude Code chamar antes de agir

        Returns:
            True se ação é permitida
        """
        result = self.integration.check_action(description)

        # Interceptar e registrar
        self.intercept_action(
            result['action_type'],
            {'description': description}
        )

        return result['allowed']


# Singleton global
_hooks = None

def get_hooks() -> ClaudeHooks:
    """Retorna instância única dos hooks"""
    global _hooks
    if _hooks is None:
        _hooks = ClaudeHooks()
    return _hooks


# Wrapper para interceptação automática
def intercept(action_type: str):
    """
    Decorator para interceptar funções automaticamente

    Usage:
        @intercept('file_create')
        def create_file(path, content):
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            hooks = get_hooks()

            # Preparar dados da ação
            action_data = {
                'function': func.__name__,
                'args': str(args)[:100],
                'kwargs': str(kwargs)[:100]
            }

            # Adicionar file_path se disponível
            if 'path' in kwargs:
                action_data['file_path'] = kwargs['path']
            elif 'file_path' in kwargs:
                action_data['file_path'] = kwargs['file_path']
            elif args and isinstance(args[0], (str, Path)):
                action_data['file_path'] = str(args[0])

            # Interceptar
            result = hooks.intercept_action(action_type, action_data)

            if not result['allowed']:
                print(f"❌ Ação bloqueada: {result['errors'][0] if result['errors'] else 'Violação detectada'}")
                return None

            # Executar função original
            return func(*args, **kwargs)

        return wrapper
    return decorator


# Funções de conveniência para Claude Code
def check_before_creating(file_path: str) -> bool:
    """Verifica se pode criar arquivo"""
    hooks = get_hooks()
    result = hooks.intercept_action('file_create', {'file_path': file_path})
    return result['allowed']


def check_before_modifying(file_path: str, code: str = "") -> bool:
    """Verifica se pode modificar arquivo"""
    hooks = get_hooks()
    result = hooks.intercept_action('file_modify', {'file_path': file_path, 'code': code})
    return result['allowed']


def check_before_command(command: str) -> bool:
    """Verifica se pode executar comando"""
    hooks = get_hooks()
    result = hooks.intercept_action('command_run', {'command': command})
    return result['allowed']


if __name__ == "__main__":
    print("🪝 TESTE DO SISTEMA DE HOOKS")
    print("="*60)

    hooks = ClaudeHooks()

    # Teste 1: Interceptar criação de arquivo
    print("\n1. Teste de criação de arquivo:")

    result = hooks.intercept_action('file_create', {
        'file_path': 'scripturemon2.py',
        'description': 'criar novo sistema melhorado'
    })
    print(f"   scripturemon2.py: {'✅ Permitido' if result['allowed'] else '❌ Bloqueado'}")
    if result['errors']:
        print(f"   Razão: {result['errors'][0]}")

    # Teste 2: Interceptar modificação
    print("\n2. Teste de modificação:")

    result = hooks.intercept_action('file_modify', {
        'file_path': 'cli_champion.py',
        'code': 'import argparse',
        'description': 'adicionar argparse ao CLI'
    })
    print(f"   cli com argparse: {'✅ Permitido' if result['allowed'] else '❌ Bloqueado'}")

    # Teste 3: Histórico
    print("\n3. Histórico da sessão:")
    history = hooks.get_session_history()
    for item in history[:3]:
        print(f"   • {item['action_type']}: {item['allowed']}")

    print("\n✅ Sistema de hooks funcionando!")