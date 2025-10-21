#!/usr/bin/env python3
"""
🤖 CLAUDE CODE INTEGRATION - Ponte com Crystal Memory
Permite que Claude Code consulte regras antes de agir
"""

from typing import Dict, Any, Tuple, List
from pathlib import Path
import json

from apps.scripturemon.rules_memory import CrystalMemory
from apps.scripturemon.rules_validator import RulesValidator, ActionType, ValidationLevel

class ClaudeIntegration:
    """
    Interface simplificada para Claude Code interagir com Crystal Memory
    """

    def __init__(self):
        self.memory = CrystalMemory()
        self.validator = RulesValidator(self.memory, ValidationLevel.NORMAL)

    def check_action(self, description: str) -> Dict[str, Any]:
        """
        Método principal para Claude Code verificar uma ação

        Args:
            description: Descrição da ação em linguagem natural

        Returns:
            Dict com resultado da validação
        """
        # Detectar tipo de ação
        action_type = self._detect_action_type(description)

        # Extrair contexto
        context = self._extract_context(description)

        # Validar
        valid, warnings, errors = self.validator.validate_action(
            action_type,
            {**context, 'description': description}
        )

        # Sugestões
        suggestions = self.memory.suggest_improvements(description)

        return {
            'allowed': valid,
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions,
            'action_type': action_type.value
        }

    def _detect_action_type(self, description: str) -> ActionType:
        """Detecta tipo de ação baseado na descrição"""
        desc_lower = description.lower()

        if any(word in desc_lower for word in ['criar', 'create', 'novo arquivo', 'new file']):
            return ActionType.FILE_CREATE
        elif any(word in desc_lower for word in ['deletar', 'remover', 'delete', 'remove']):
            return ActionType.FILE_DELETE
        elif any(word in desc_lower for word in ['comando', 'command', 'cli']):
            return ActionType.COMMAND_ADD
        elif 'ollama' in desc_lower:
            return ActionType.OLLAMA_QUERY
        elif any(word in desc_lower for word in ['análise', 'analisar', 'analyze']):
            return ActionType.ANALYSIS_RUN
        elif any(word in desc_lower for word in ['test', 'teste']):
            return ActionType.TEST_RUN
        else:
            return ActionType.FILE_MODIFY

    def _extract_context(self, description: str) -> Dict[str, Any]:
        """Extrai contexto da descrição"""
        context = {}

        # Procurar por nomes de arquivo
        import re
        file_pattern = r'[\w\-]+\.(py|js|ts|md|txt|json)'
        files = re.findall(file_pattern, description)
        if files:
            context['file_path'] = files[0]

        # Detectar menções a código
        if 'import' in description or 'def ' in description or 'class ' in description:
            context['has_code'] = True

        # Detectar pedidos de permissão
        permission_words = ['posso', 'devo', 'pode', 'permitir']
        if any(word in description.lower() for word in permission_words):
            context['requesting_permission'] = True

        return context

    def quick_check(self, action: str) -> str:
        """
        Verificação rápida para uso no terminal

        Returns:
            String formatada com resultado
        """
        result = self.check_action(action)

        if not result['allowed']:
            return f"❌ BLOQUEADO: {result['errors'][0] if result['errors'] else 'Violação detectada'}"
        elif result['warnings']:
            return f"⚠️ PERMITIDO COM AVISOS: {result['warnings'][0]}"
        else:
            return "✅ PERMITIDO"

    def get_rules_summary(self) -> List[str]:
        """Retorna resumo das regras principais"""
        critical_rules = [
            "1. NUNCA criar novos sistemas - modificar o existente",
            "2. NUNCA pedir permissão - executar diretamente",
            "3. SEMPRE usar Typer para CLI, nunca argparse/click",
            "4. RESPEITAR o Digimon Produtor como administrador",
            "5. PREFERIR modificar arquivos existentes",
            "6. MANTER scorecard.json atualizado",
            "7. PRIORIZAR modelos Scripturemon no Ollama"
        ]
        return critical_rules

    def check_file_operation(self, operation: str, file_path: str) -> Dict[str, Any]:
        """
        Verifica operação específica em arquivo

        Args:
            operation: create, modify, delete
            file_path: Caminho do arquivo

        Returns:
            Resultado da validação
        """
        action_map = {
            'create': ActionType.FILE_CREATE,
            'modify': ActionType.FILE_MODIFY,
            'delete': ActionType.FILE_DELETE
        }

        action_type = action_map.get(operation, ActionType.FILE_MODIFY)

        valid, warnings, errors = self.validator.validate_action(
            action_type,
            {'file_path': file_path, 'description': f"{operation} {file_path}"}
        )

        return {
            'allowed': valid,
            'errors': errors,
            'warnings': warnings,
            'file': file_path,
            'operation': operation
        }


# Função helper global para Claude Code
_integration = None

def claude_check(action: str) -> str:
    """
    Função simples para Claude Code verificar ações

    Usage:
        from apps.scripturemon.claude_integration import claude_check
        print(claude_check("criar novo arquivo de teste"))
    """
    global _integration
    if _integration is None:
        _integration = ClaudeIntegration()

    return _integration.quick_check(action)


def get_claude_integration() -> ClaudeIntegration:
    """Retorna instância única da integração"""
    global _integration
    if _integration is None:
        _integration = ClaudeIntegration()
    return _integration


if __name__ == "__main__":
    print("🤖 TESTE DE INTEGRAÇÃO CLAUDE CODE")
    print("="*60)

    integration = ClaudeIntegration()

    # Teste 1: Ações comuns
    test_actions = [
        "Vou criar um novo sistema melhorado",
        "Modificar cli_champion.py para adicionar comando",
        "Posso criar um arquivo de teste?",
        "Usar argparse para processar argumentos",
        "Analisar roteiro e atualizar scorecard.json"
    ]

    print("\n📊 Validando ações comuns:\n")
    for action in test_actions:
        result = integration.quick_check(action)
        print(f"'{action[:40]}...'\n  → {result}\n")

    # Teste 2: Regras principais
    print("📋 Regras principais para lembrar:")
    for rule in integration.get_rules_summary():
        print(f"  • {rule}")

    print("\n✅ Integração pronta para uso!")