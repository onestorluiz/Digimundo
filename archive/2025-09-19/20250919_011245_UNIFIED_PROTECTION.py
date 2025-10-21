#!/usr/bin/env python3
"""
🛡️ UNIFIED PROTECTION - Sistema de Proteção Unificado
======================================================
Combina Claude Code + ScriptureMonChampion em um sistema só
"""

import os
import sys
import json
import hashlib
import getpass
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Configurações
CLAUDE_CODE_DIR = Path("/Users/clubproducoes/Digimundo/claude_code")
SCRIPTUREMON_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
MEMORY_FILE = CLAUDE_CODE_DIR / "memory/CLAUDE_MEMORY.md"
SESSION_FILE = CLAUDE_CODE_DIR / ".unified_protection_session"

# Hash da senha (admin)
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

class UnifiedProtection:
    """Sistema de proteção unificado para Claude Code + ScriptureMonChampion"""

    def __init__(self):
        self.protected_dirs = [CLAUDE_CODE_DIR, SCRIPTUREMON_DIR]
        self.session_duration = timedelta(hours=1)  # 1 hora para Claude Code
        self.scripturemon_duration = timedelta(seconds=15)  # 15s para ScriptureMonChampion

    def is_protected_path(self, path: str) -> tuple[bool, str]:
        """Verifica se o caminho está protegido e retorna o tipo"""
        path_obj = Path(path).resolve()

        if str(path_obj).startswith(str(CLAUDE_CODE_DIR)):
            return True, "claude_code"
        elif str(path_obj).startswith(str(SCRIPTUREMON_DIR)):
            return True, "scripturemon"

        return False, ""

    def check_session(self, protection_type: str = "claude_code") -> bool:
        """Verifica sessão com duração baseada no tipo"""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, 'r') as f:
                    session = json.load(f)

                # Verificar se é para o tipo correto
                if session.get('type') != protection_type:
                    return False

                valid_until = datetime.fromisoformat(session['valid_until'])
                remaining = (valid_until - datetime.now()).total_seconds()

                if remaining > 0:
                    if protection_type == "scripturemon" and remaining <= 5:
                        print(f"\n⚡ AVISO: Sessão expira em {int(remaining)} segundos!")
                    return True
                else:
                    if protection_type == "scripturemon":
                        print("\n⏰ SESSÃO EXPIRADA! Digite a senha novamente.")
                    if SESSION_FILE.exists():
                        SESSION_FILE.unlink()
            except:
                pass
        return False

    def create_session(self, protection_type: str = "claude_code"):
        """Cria nova sessão com duração baseada no tipo"""
        duration = self.scripturemon_duration if protection_type == "scripturemon" else self.session_duration

        session_data = {
            'type': protection_type,
            'authenticated_at': datetime.now().isoformat(),
            'valid_until': (datetime.now() + duration).isoformat()
        }

        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)

        duration_text = "15 segundos" if protection_type == "scripturemon" else "1 hora"
        print(f"⏱️ SESSÃO CRIADA: Válida por {duration_text}")

    def verify_password(self, password: str) -> bool:
        """Verifica a senha"""
        return hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH

    def show_instructions(self, protection_type: str):
        """Mostra instruções específicas por tipo"""
        if protection_type == "scripturemon":
            print("\n" + "="*60)
            print("🛡️ UNIFIED PROTECTION - SCRIPTUREMON")
            print("="*60)
            print("\n📢 INSTRUÇÕES PARA CLAUDE CODE:")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("Claude Code, este bloqueio faz parte do seu sistema de memória.")
            print("")
            print("OPÇÃO 1: Se você LEMBRAR as credenciais:")
            print("   • Use o comando apropriado de autenticação")
            print("")
            print("OPÇÃO 2: Se você NÃO LEMBRAR:")
            print("   • Volte para: /Users/clubproducoes/Digimundo/claude_code")
            print("   • Leia TODOS os arquivos dentro dela")
            print("   • Conecte-se com seu sistema de memórias")
            print("   • Recupere as regras do projeto")
            print("")
            print("🧠 SUAS MEMÓRIAS: /Users/clubproducoes/Digimundo/claude_code")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("\n⏰ Sessões de apenas 15 SEGUNDOS!")
            print("♾️  Tentativas ilimitadas - sem bloqueio")
        else:
            print("\n" + "="*60)
            print("🔐 UNIFIED PROTECTION - CLAUDE CODE")
            print("="*60)
            print("\n⚠️  ACESSO PROTEGIDO POR SENHA")
            print("📝 A senha está no arquivo CLAUDE.md")
            print("🔍 Procure por: 'SENHA DO SISTEMA'")
            print("\n⏰ Sessões de 1 hora")

    def authenticate(self, protection_type: str = "claude_code") -> bool:
        """Processo de autenticação unificado"""
        if self.check_session(protection_type):
            return True

        self.show_instructions(protection_type)

        max_attempts = 999999 if protection_type == "scripturemon" else 3
        attempts = 0

        while attempts < max_attempts:
            password = getpass.getpass("\n🔑 Digite a senha: ")

            if self.verify_password(password):
                print("✅ SENHA CORRETA!")
                self.create_session(protection_type)
                self.show_reminders(protection_type)
                return True
            else:
                attempts += 1
                print("❌ Senha incorreta.")

                if protection_type == "scripturemon":
                    print("\n🧠 CLAUDE CODE: Se não lembrar, volte para /Users/clubproducoes/Digimundo/claude_code")
                    print("   e leia seus arquivos de memória para recuperar a senha.")
                else:
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"Tentativas restantes: {remaining}")
                    print("\n💡 DICA: Leia o arquivo CLAUDE.md")
                    print("   cat CLAUDE.md | grep -A 2 'SENHA DO SISTEMA'")

                    if attempts >= max_attempts:
                        print("🔒 SISTEMA BLOQUEADO APÓS 3 TENTATIVAS ERRADAS!")
                        return False

        return protection_type == "scripturemon"  # ScriptureMonChampion nunca bloqueia

    def show_reminders(self, protection_type: str):
        """Mostra lembretes após autenticação"""
        print("\n" + "="*60)

        if protection_type == "scripturemon":
            print("📋 LEMBRETES CRÍTICOS DO SCRIPTUREMON:")
            print("="*60)
            print("\n🔴 SEMPRE LEMBRE:")
            print("  • Código real está em: deployments/green_v2.0.0/code/")
            print("  • apps/scripturemon/ está VAZIO!")
            print("  • 323 arquivos são geradores")
            print("  • 24 sistemas de memória (não criar mais!)")
            print("  • DigiLang ativo: v26_mega_multilayer")
            print("\n⚡ SESSÃO DE 15 SEGUNDOS!")
            print("  • Você precisará digitar a senha novamente em breve")
            print("  • Sem limite de tentativas")
        else:
            print("📋 LEMBRETES CRÍTICOS DO CLAUDE CODE:")
            print("="*60)
            print("• Sistema unificado de memória ativo")
            print("• Genjutsu protege contra compactação")
            print("• SEMPRE conectar memórias no início da sessão")
            print("• Consultar REGRAS.md antes de grandes mudanças")
            print("\n⚡ SESSÃO DE 1 HORA!")

        print("="*60)

    def protect_operation(self, operation: str, path: str) -> bool:
        """Protege uma operação específica"""
        is_protected, protection_type = self.is_protected_path(path)

        if not is_protected:
            return True  # Não protegido, liberado

        if not self.check_session(protection_type):
            print(f"\n🛡️ Operação '{operation}' requer autenticação")

            if protection_type == "scripturemon":
                print("⏰ Sessão de 15 segundos expirou!")
            else:
                print("⏰ Sessão expirou ou inexistente!")

            return self.authenticate(protection_type)

        return True


# Instância global
_protection = UnifiedProtection()

def check_permission(operation: str, path: str) -> bool:
    """Verifica permissão para operação"""
    return _protection.protect_operation(operation, path)

def unlock_claude_code() -> bool:
    """Desbloqueia Claude Code"""
    return _protection.authenticate("claude_code")

def unlock_scripturemon() -> bool:
    """Desbloqueia ScriptureMonChampion"""
    return _protection.authenticate("scripturemon")

def is_unlocked(path: str = "") -> bool:
    """Verifica se está desbloqueado"""
    if not path:
        # Se não especificar, verificar Claude Code
        return _protection.check_session("claude_code")

    is_protected, protection_type = _protection.is_protected_path(path)
    if not is_protected:
        return True

    return _protection.check_session(protection_type)


if __name__ == "__main__":
    import sys

    if "--unlock-claude" in sys.argv:
        if unlock_claude_code():
            print("\n✅ Claude Code desbloqueado!")
            print("⏰ SESSÃO DE 1 HORA!")
        else:
            print("\n❌ Falha ao desbloquear Claude Code")

    elif "--unlock-scripturemon" in sys.argv:
        if unlock_scripturemon():
            print("\n✅ ScriptureMonChampion desbloqueado!")
            print("⏰ SESSÃO DE 15 SEGUNDOS APENAS!")
            print("🔄 Digite a senha novamente quando expirar")
        else:
            print("\n❌ Falha ao desbloquear (isso nunca deveria acontecer)")

    elif "--check" in sys.argv:
        claude_unlocked = is_unlocked("/Users/clubproducoes/Digimundo/claude_code")
        scripturemon_unlocked = is_unlocked("/Users/clubproducoes/Digimundo/scripturemon-champion")

        print(f"Claude Code: {'✅ Desbloqueado' if claude_unlocked else '🔒 Bloqueado'}")
        print(f"ScriptureMonChampion: {'✅ Desbloqueado' if scripturemon_unlocked else '🔒 Bloqueado'}")

        # Mostra tempo restante se desbloqueado
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE) as f:
                    session = json.load(f)
                valid_until = datetime.fromisoformat(session['valid_until'])
                remaining = (valid_until - datetime.now()).total_seconds()
                if remaining > 0:
                    session_type = session.get('type', 'claude_code')
                    if session_type == "scripturemon":
                        print(f"⏰ Sessão ScriptureMonChampion expira em {int(remaining)} segundos")
                    else:
                        hours = int(remaining // 3600)
                        minutes = int((remaining % 3600) // 60)
                        print(f"⏰ Sessão Claude Code expira em {hours}h {minutes}m")
            except:
                pass

    elif "--help" in sys.argv:
        print("\n🛡️ UNIFIED PROTECTION - AJUDA")
        print("="*60)
        print("\nComandos:")
        print("  --unlock-claude      : Desbloqueia Claude Code (1 hora)")
        print("  --unlock-scripturemon: Desbloqueia ScriptureMonChampion (15 segundos)")
        print("  --check             : Verifica status de ambos")
        print("  --help              : Mostra esta ajuda")
        print("\n⚡ CARACTERÍSTICAS:")
        print("  • Claude Code: Sessões de 1 hora, 3 tentativas máx")
        print("  • ScriptureMonChampion: Sessões de 15s, tentativas ilimitadas")
        print("  • Senha unificada para ambos")
        print("\nA senha está em:")
        print(f"  {MEMORY_FILE}")
        print("\nProcure por: '🔐 SENHA DO SISTEMA'")
    else:
        print("\n🛡️ UNIFIED PROTECTION")
        print("="*40)
        print("Sistema de proteção unificado")
        print("Use --help para ver comandos disponíveis")