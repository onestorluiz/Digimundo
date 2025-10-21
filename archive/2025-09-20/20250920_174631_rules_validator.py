#!/usr/bin/env python3
"""
🛡️ RULES VALIDATOR - Sistema de Validação Proativa
FASE 23: Validação automática de ações contra regras
"""

import re
import ast
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from enum import Enum
import logging

from .rules_memory import CrystalMemory, RuleLayer

logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """Níveis de validação"""
    STRICT = "strict"       # Valida todas as regras
    NORMAL = "normal"       # Valida L1 e L2
    LENIENT = "lenient"     # Valida apenas L1

class ActionType(Enum):
    """Tipos de ações no sistema"""
    FILE_CREATE = "file_create"
    FILE_MODIFY = "file_modify"
    FILE_DELETE = "file_delete"
    COMMAND_ADD = "command_add"
    ANALYSIS_RUN = "analysis_run"
    OLLAMA_QUERY = "ollama_query"
    SYSTEM_CONFIG = "system_config"
    TEST_RUN = "test_run"
    DEPLOYMENT = "deployment"

class RulesValidator:
    """
    Validador proativo de regras do Scripturemon Champion
    Integra com Crystal Memory para validação em tempo real
    """

    def __init__(self, memory: Optional[CrystalMemory] = None,
                 level: ValidationLevel = ValidationLevel.NORMAL):
        """
        Inicializa o validador

        Args:
            memory: Instância do Crystal Memory (ou cria nova)
            level: Nível de validação padrão
        """
        self.memory = memory or CrystalMemory()
        self.level = level
        self.validation_cache = {}

        # Padrões para detecção de violações
        self.violation_patterns = {
            'new_system': [
                r'scripturemon[_\-]?2',
                r'new[_\-]?system',
                r'improved[_\-]?system',
                r'better[_\-]?version'
            ],
            'permission_request': [
                r'\bposso\b',
                r'\bdevo\b',
                r'\bpermitir\b',
                r'\bautorizar\b',
                r'\bconfirmar\b',
                r'\bpode\b'
            ],
            'wrong_cli': [
                r'import\s+argparse',
                r'import\s+click',
                r'from\s+argparse',
                r'from\s+click'
            ],
            'duplicate_functionality': [
                r'translate.*v\d+',
                r'compress.*v\d+',
                r'analyze.*v\d+'
            ]
        }

        logger.info(f"🛡️ Rules Validator inicializado (nível: {level.value})")

    def validate_action(self, action_type: ActionType, action_data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Valida uma ação antes de executá-la

        Args:
            action_type: Tipo da ação
            action_data: Dados da ação (arquivo, código, etc)

        Returns:
            Tupla (válido, avisos, erros)
        """
        warnings = []
        errors = []

        # Prepara contexto para Crystal Memory
        context = {
            **action_data,
            'action_type': action_type.value
        }

        # Validação via Crystal Memory
        compliant, violations = self.memory.check_compliance(
            f"{action_type.value}: {action_data.get('description', '')}",
            context
        )

        # Processa violações por nível
        for violation in violations:
            layer = RuleLayer[violation['layer'].replace('RuleLayer.', '')]

            # L1 sempre é erro
            if layer == RuleLayer.L1_CRITICAL:
                errors.append(f"❌ CRÍTICO: {violation['rule']}")

            # L2 é erro em modo STRICT, aviso em NORMAL
            elif layer == RuleLayer.L2_IMPORTANT:
                if self.level == ValidationLevel.STRICT:
                    errors.append(f"❌ IMPORTANTE: {violation['rule']}")
                else:
                    warnings.append(f"⚠️ IMPORTANTE: {violation['rule']}")

            # L3 é aviso em STRICT/NORMAL
            elif layer == RuleLayer.L3_CONTEXTUAL:
                if self.level != ValidationLevel.LENIENT:
                    warnings.append(f"💡 CONTEXTUAL: {violation['rule']}")

            # L4 sempre é apenas informativo
            else:
                if self.level == ValidationLevel.STRICT:
                    warnings.append(f"ℹ️ CONSULTIVO: {violation['rule']}")

        # Validações específicas por tipo
        if action_type == ActionType.FILE_CREATE:
            self._validate_file_creation(action_data, warnings, errors)
        elif action_type == ActionType.FILE_MODIFY:
            self._validate_file_modification(action_data, warnings, errors)
        elif action_type == ActionType.COMMAND_ADD:
            self._validate_command_addition(action_data, warnings, errors)
        elif action_type == ActionType.OLLAMA_QUERY:
            self._validate_ollama_usage(action_data, warnings, errors)

        # Determina se é válido
        valid = len(errors) == 0

        return valid, warnings, errors

    def _validate_file_creation(self, data: Dict, warnings: List[str], errors: List[str]):
        """Valida criação de arquivo"""
        file_path = Path(data.get('file_path', ''))

        # Verifica se é um sistema duplicado
        for pattern in self.violation_patterns['new_system']:
            if re.search(pattern, str(file_path), re.IGNORECASE):
                errors.append(f"Sistema duplicado detectado: {file_path.name}")
                return

        # Verifica se já existe funcionalidade similar
        if file_path.suffix == '.py':
            stem = file_path.stem
            parent = file_path.parent

            # Procura arquivos similares
            similar_patterns = [
                f"*{stem[:-1]}*.py",
                f"*{stem[:-2]}*.py" if len(stem) > 2 else None,
                f"{stem.split('_')[0]}_*.py" if '_' in stem else None
            ]

            for pattern in filter(None, similar_patterns):
                similar = list(parent.glob(pattern))
                if similar and similar[0] != file_path:
                    warnings.append(f"Arquivo similar existe: {similar[0].name}")
                    warnings.append("Considere modificar o existente")
                    break

    def _validate_file_modification(self, data: Dict, warnings: List[str], errors: List[str]):
        """Valida modificação de arquivo"""
        code = data.get('code', '')
        file_path = Path(data.get('file_path', ''))

        # Verifica imports proibidos em CLI
        if 'cli' in str(file_path).lower():
            for pattern in self.violation_patterns['wrong_cli']:
                if re.search(pattern, code):
                    errors.append("CLI deve usar Typer, não argparse/click")
                    return

        # Verifica remoção de funções (compatibilidade)
        if 'def ' in data.get('old_code', '') and 'def ' not in code:
            warnings.append("Remoção de função pode quebrar compatibilidade")

    def _validate_command_addition(self, data: Dict, warnings: List[str], errors: List[str]):
        """Valida adição de comando CLI"""
        command_name = data.get('command_name', '')

        # Verifica se comando já existe
        existing_commands = data.get('existing_commands', [])
        if command_name in existing_commands:
            errors.append(f"Comando '{command_name}' já existe")
            return

        # Verifica uso de Typer
        implementation = data.get('implementation', '')
        if implementation and '@app.command' not in implementation:
            errors.append("Comandos CLI devem usar decorator @app.command do Typer")

    def _validate_ollama_usage(self, data: Dict, warnings: List[str], errors: List[str]):
        """Valida uso do Ollama"""
        model = data.get('model', '')
        available_models = data.get('available_models', [])

        # Verifica prioridade Scripturemon
        scripturemon_available = any('scripturemon' in m.lower() for m in available_models)

        if scripturemon_available and 'scripturemon' not in model.lower():
            warnings.append(f"Modelo Scripturemon disponível mas usando {model}")

        # Verifica respeito ao Digimon Produtor
        if 'replace' in data.get('action', '').lower():
            errors.append("Não substituir sistema Digimon Produtor existente")

    def validate_code(self, code: str, file_path: Optional[Path] = None) -> Tuple[bool, List[str]]:
        """
        Valida código Python contra regras

        Args:
            code: Código a validar
            file_path: Caminho do arquivo (para contexto)

        Returns:
            Tupla (válido, problemas encontrados)
        """
        issues = []

        try:
            # Parse do código
            tree = ast.parse(code)

            # Verifica imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ['argparse', 'click']:
                            if file_path and 'cli' in str(file_path).lower():
                                issues.append(f"❌ Import proibido: {alias.name} (use Typer)")

                elif isinstance(node, ast.ImportFrom):
                    if node.module in ['argparse', 'click']:
                        if file_path and 'cli' in str(file_path).lower():
                            issues.append(f"❌ Import proibido: {node.module} (use Typer)")

            # Verifica padrões Python
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                # Tabs
                if '\t' in line:
                    issues.append(f"⚠️ Linha {i}: Use 4 espaços, não tabs")

                # CamelCase em variáveis
                if '=' in line and 'class' not in line:
                    var_match = re.match(r'\s*([a-zA-Z_]+)\s*=', line)
                    if var_match:
                        var_name = var_match.group(1)
                        if re.match(r'^[a-z]+[A-Z]', var_name):
                            issues.append(f"⚠️ Linha {i}: Use snake_case para variáveis ({var_name})")

        except SyntaxError as e:
            issues.append(f"❌ Erro de sintaxe: {e}")

        valid = not any('❌' in issue for issue in issues)
        return valid, issues

    def suggest_fixes(self, violations: List[Dict]) -> List[str]:
        """
        Sugere correções para violações

        Args:
            violations: Lista de violações detectadas

        Returns:
            Lista de sugestões de correção
        """
        fixes = []

        for violation in violations:
            rule_id = violation.get('rule_id')
            details = violation.get('details', '')

            # Sugestões específicas por regra
            if rule_id == 1:  # Não criar novos sistemas
                fixes.append("📝 Modifique o arquivo existente ao invés de criar novo")
                fixes.append("📝 Use o sistema de versionamento para melhorias")

            elif rule_id == 2:  # Não pedir permissão
                fixes.append("✅ Execute a ação diretamente")
                fixes.append("✅ Remova pedidos de confirmação")

            elif rule_id == 3:  # Usar Typer
                fixes.append("🔧 Substitua 'import argparse' por 'import typer'")
                fixes.append("🔧 Use decorators @app.command() do Typer")

            elif rule_id == 5:  # Modificar apenas necessário
                fixes.append("🎯 Foque apenas nos arquivos essenciais")
                fixes.append("🎯 Use funções existentes quando possível")

            elif rule_id == 6:  # Respeitar Digimon Produtor
                fixes.append("🤝 Integre com sistema existente")
                fixes.append("🤝 Use como auxiliar, não substituto")

        return fixes

    def pre_commit_hook(self, changed_files: List[Path]) -> Tuple[bool, str]:
        """
        Hook para validação pré-commit

        Args:
            changed_files: Lista de arquivos modificados

        Returns:
            Tupla (pode_commitar, mensagem)
        """
        all_valid = True
        messages = []

        for file_path in changed_files:
            if file_path.suffix == '.py':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    valid, issues = self.validate_code(code, file_path)

                    if not valid:
                        all_valid = False
                        messages.append(f"\n{file_path}:")
                        messages.extend(f"  {issue}" for issue in issues)

                except Exception as e:
                    messages.append(f"⚠️ Erro validando {file_path}: {e}")

        if all_valid:
            return True, "✅ Todos os arquivos passaram na validação"
        else:
            return False, "❌ Violações encontradas:\n" + "\n".join(messages)

    def interactive_fix(self, code: str, violations: List[Dict]) -> str:
        """
        Tenta corrigir código automaticamente

        Args:
            code: Código com violações
            violations: Violações detectadas

        Returns:
            Código corrigido
        """
        fixed_code = code

        for violation in violations:
            rule_id = violation.get('rule_id')

            # Correções automáticas simples
            if rule_id == 3:  # Typer
                fixed_code = fixed_code.replace('import argparse', 'import typer')
                fixed_code = fixed_code.replace('from argparse', 'from typer')
                fixed_code = fixed_code.replace('import click', 'import typer')
                fixed_code = fixed_code.replace('from click', 'from typer')

            elif rule_id == 9:  # Python standards
                # Converte tabs para espaços
                fixed_code = fixed_code.replace('\t', '    ')

        return fixed_code

    def generate_report(self, action_history: List[Dict]) -> Dict[str, Any]:
        """
        Gera relatório de validação

        Args:
            action_history: Histórico de ações validadas

        Returns:
            Relatório detalhado
        """
        total = len(action_history)
        valid = sum(1 for a in action_history if a.get('valid', False))

        violations_by_rule = {}
        for action in action_history:
            for violation in action.get('violations', []):
                rule_id = violation.get('rule_id')
                violations_by_rule[rule_id] = violations_by_rule.get(rule_id, 0) + 1

        return {
            'total_actions': total,
            'valid_actions': valid,
            'invalid_actions': total - valid,
            'validation_rate': (valid / total * 100) if total > 0 else 100,
            'most_violated_rules': sorted(
                violations_by_rule.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            'level': self.level.value
        }


def test_rules_validator():
    """Testa o Rules Validator"""
    print("🛡️ TESTANDO RULES VALIDATOR")
    print("="*60)

    # Inicializa
    validator = RulesValidator(level=ValidationLevel.NORMAL)

    # Teste 1: Validação de criação de arquivo
    print("\n1. Teste de Criação de Arquivo:")

    # Arquivo válido
    valid, warnings, errors = validator.validate_action(
        ActionType.FILE_CREATE,
        {
            'file_path': 'apps/scripturemon/new_feature.py',
            'description': 'Adicionar nova funcionalidade'
        }
    )
    print(f"   Arquivo válido: {valid}")

    # Arquivo inválido
    valid, warnings, errors = validator.validate_action(
        ActionType.FILE_CREATE,
        {
            'file_path': 'apps/scripturemon/scripturemon2.py',
            'description': 'Criar sistema melhorado'
        }
    )
    print(f"   Sistema duplicado: {not valid}")
    if errors:
        print(f"   Erro: {errors[0]}")

    # Teste 2: Validação de código
    print("\n2. Teste de Validação de Código:")

    # Código com violação
    bad_code = """
import argparse

def main():
    parser = argparse.ArgumentParser()
    print("Hello")
"""

    valid, issues = validator.validate_code(bad_code, Path("cli_champion.py"))
    print(f"   Código com argparse: {not valid}")
    if issues:
        print(f"   Issue: {issues[0]}")

    # Teste 3: Validação Ollama
    print("\n3. Teste de Validação Ollama:")

    valid, warnings, errors = validator.validate_action(
        ActionType.OLLAMA_QUERY,
        {
            'model': 'mistral:latest',
            'available_models': ['scripturemon:latest', 'mistral:latest'],
            'action': 'query'
        }
    )
    print(f"   Aviso sobre Scripturemon: {len(warnings) > 0}")

    # Teste 4: Correção automática
    print("\n4. Teste de Correção Automática:")

    fixed = validator.interactive_fix(
        "import argparse\n\tdef test():\n\t\tpass",
        [{'rule_id': 3}, {'rule_id': 9}]
    )
    print(f"   Import corrigido: {'import typer' in fixed}")
    print(f"   Tabs corrigidos: {'\t' not in fixed}")

    print("\n✅ Rules Validator funcionando!")


if __name__ == "__main__":
    test_rules_validator()