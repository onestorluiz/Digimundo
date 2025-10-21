#!/usr/bin/env python3
"""
🛡️ CLAUDE CODE CHECK - Script de Validação em Tempo Real
Este script DEVE ser importado/executado pelo Claude Code antes de qualquer ação
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.scripturemon.claude_hooks import get_hooks, check_before_creating, check_before_modifying, check_before_command
from apps.scripturemon.claude_integration import claude_check

# Inicializar hooks na importação
hooks = get_hooks()

def validate_action(action_description: str) -> bool:
    """
    Função principal para Claude Code chamar antes de qualquer ação

    Args:
        action_description: Descrição da ação que será executada

    Returns:
        True se permitido, False se bloqueado
    """
    # Validar com hooks
    result = hooks.validate_before_action(action_description)

    if not result:
        print(f"❌ AÇÃO BLOQUEADA: {action_description}")
        print("   Violação das regras do REGRAS.md detectada")

        # Obter detalhes da violação
        check_result = claude_check(action_description)
        if "BLOQUEADO" in check_result:
            print(f"   Razão: {check_result}")

        # Sugerir alternativa
        suggestions = hooks.memory.suggest_improvements(action_description)
        if suggestions:
            print("\n💡 Sugestões:")
            for s in suggestions:
                print(f"   {s}")
    else:
        print(f"✅ Ação permitida: {action_description}")

    return result

# Aliases para facilitar uso
check = validate_action
v = validate_action  # Atalho ainda mais curto

# Auto-teste ao importar
if __name__ != "__main__":
    print("🛡️ Claude Code Check carregado - validação ativa")
    print("   Use: check('descrição da ação') antes de agir")

    # Mostrar sessão ativa
    print(f"   Sessão: {hooks.session_id[:8]}...")

    # Verificar histórico recente
    history = hooks.get_session_history()
    if history:
        violations = [h for h in history if not h['allowed']]
        if violations:
            print(f"   ⚠️ {len(violations)} violações na sessão atual")

if __name__ == "__main__":
    # Teste direto
    print("🛡️ TESTE DO CLAUDE CODE CHECK")
    print("="*60)

    # Testar várias ações
    test_actions = [
        "criar novo sistema scripturemon2.py",
        "modificar cli_champion.py para adicionar comando",
        "usar argparse no CLI",
        "deletar arquivo temporário",
        "analisar roteiro com Ollama"
    ]

    print("\nValidando ações de teste:\n")
    for action in test_actions:
        result = validate_action(action)
        print()

    # Mostrar histórico
    print("\nHistórico da sessão:")
    history = hooks.get_session_history()
    for h in history[:5]:
        status = "✅" if h['allowed'] else "❌"
        print(f"  {status} {h['action_type']}: {h['action_data'].get('description', 'N/A')[:50]}")

    print("\n✅ Claude Code Check funcionando!")