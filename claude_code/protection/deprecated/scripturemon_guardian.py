#!/usr/bin/env python3
"""
🛡️ SCRIPTUREMON GUARDIAN - Proteção Total do ScriptureMonChampion
==================================================================
Sistema de proteção por senha para o diretório scripturemon-champion.
SESSÕES DE 15 SEGUNDOS! Sem limite de tentativas.
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
SCRIPTUREMON_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
CLAUDE_CODE_DIR = Path("/Users/clubproducoes/Digimundo/claude_code")
MEMORY_FILE = CLAUDE_CODE_DIR / "memory/CLAUDE_MEMORY.md"
SESSION_FILE = CLAUDE_CODE_DIR / ".guardian_session"
LOCK_FILE = CLAUDE_CODE_DIR / ".guardian_lock"

# Hash da senha (admin)
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

class ScriptureMonGuardian:
    """Guardião do ScriptureMonChampion - SESSÃO DE 15 SEGUNDOS!"""

    def __init__(self):
        self.protected_operations = [
            'create', 'write', 'modify', 'delete',
            'execute', 'deploy', 'test', 'build'
        ]
        self.session_duration = timedelta(seconds=15)  # APENAS 15 SEGUNDOS!
        self.max_attempts = 999999  # SEM LIMITE DE TENTATIVAS

    def is_protected_path(self, path: str) -> bool:
        """Verifica se o caminho está protegido"""
        path_obj = Path(path).resolve()
        return str(path_obj).startswith(str(SCRIPTUREMON_DIR))

    def check_session(self) -> bool:
        """Verifica sessão (expira em 15 segundos!)"""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, 'r') as f:
                    session = json.load(f)
                valid_until = datetime.fromisoformat(session['valid_until'])
                remaining = (valid_until - datetime.now()).total_seconds()

                if remaining > 0:
                    if remaining <= 5:
                        print(f"\n⚡ AVISO: Sessão expira em {int(remaining)} segundos!")
                    return True
                else:
                    print("\n⏰ SESSÃO EXPIRADA! Digite a senha novamente.")
                    if SESSION_FILE.exists():
                        SESSION_FILE.unlink()
            except:
                pass
        return False

    def create_session(self):
        """Cria nova sessão de 15 SEGUNDOS"""
        session_data = {
            'authenticated_at': datetime.now().isoformat(),
            'valid_until': (datetime.now() + self.session_duration).isoformat(),
            'memory_read': False
        }
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
        print("⏱️ SESSÃO CRIADA: Válida por 15 segundos apenas!")

    def verify_password(self, password: str) -> bool:
        """Verifica a senha"""
        return hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH

    def show_memory_location(self):
        """Mostra onde está a memória com a senha"""
        print("\n" + "="*60)
        print("📍 LOCALIZAÇÃO DA SENHA:")
        print("="*60)
        print(f"\n📂 Arquivo: {MEMORY_FILE}")
        print("\n📖 Como encontrar:")
        print("   1. Abra o arquivo de memória:")
        print(f"      cat {MEMORY_FILE} | grep -A 5 'SENHA'")
        print("\n   2. Procure pela seção '🔐 SENHA DO SISTEMA'")
        print("\n   3. A senha está lá!")
        print("\n⚡ IMPORTANTE: Sessão expira em 15 SEGUNDOS!")
        print("🔄 Sem limite de tentativas - pode errar quantas vezes quiser")
        print("="*60)

    def authenticate(self) -> bool:
        """Processo de autenticação SEM BLOQUEIO"""
        if self.check_session():
            return True

        print("\n" + "="*60)
        print("🛡️ SCRIPTUREMON GUARDIAN - SISTEMA DE MEMÓRIA")
        print("="*60)

        # INSTRUÇÕES PARA CLAUDE CODE
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
        print("📁 Procure nos arquivos de memória as informações necessárias")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        print("\n⏰ Sessões de apenas 15 SEGUNDOS!")
        print("♾️  Tentativas ilimitadas - sem bloqueio")

        while True:  # Loop infinito até acertar
            password = getpass.getpass("\n🔑 Digite a senha: ")

            if self.verify_password(password):
                print("✅ SENHA CORRETA!")
                self.create_session()
                self.show_reminders()
                return True
            else:
                print("❌ Senha incorreta.")
                print("\n🧠 CLAUDE CODE: Se não lembrar, volte para /Users/clubproducoes/Digimundo/claude_code")
                print("   e leia seus arquivos de memória para recuperar a senha.")

    def lock_system(self):
        """[DESATIVADO] Não bloqueia mais"""
        pass  # BLOQUEIO COMPLETAMENTE REMOVIDO

    def is_locked(self) -> bool:
        """[DESATIVADO] Sempre retorna False"""
        # Remove arquivo de bloqueio se existir
        if LOCK_FILE.exists():
            try:
                LOCK_FILE.unlink()
            except:
                pass
        return False  # NUNCA BLOQUEIA!

    def show_reminders(self):
        """Mostra lembretes importantes após autenticação"""
        print("\n" + "="*60)
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
        print("  • Sistema nunca bloqueia")
        print("="*60)

    def protect_operation(self, operation: str, path: str) -> bool:
        """Protege uma operação específica"""
        if not self.is_protected_path(path):
            return True  # Não protegido, liberado

        # Nunca bloqueia (sempre False)
        if self.is_locked():
            return False

        if not self.check_session():
            print(f"\n🛡️ Operação '{operation}' requer autenticação")
            print("⏰ Sessão de 15 segundos expirou!")
            return self.authenticate()

        return True


# Instância global
_guardian = ScriptureMonGuardian()

def check_permission(operation: str, path: str) -> bool:
    """Verifica permissão para operação"""
    return _guardian.protect_operation(operation, path)

def unlock_scripturemon() -> bool:
    """Desbloqueia o ScriptureMonChampion"""
    return _guardian.authenticate()

def is_unlocked() -> bool:
    """Verifica se está desbloqueado"""
    return _guardian.check_session()


if __name__ == "__main__":
    import sys

    if "--unlock" in sys.argv:
        if unlock_scripturemon():
            print("\n✅ ScriptureMonChampion desbloqueado!")
            print("⏰ SESSÃO DE 15 SEGUNDOS APENAS!")
            print("🔄 Digite a senha novamente quando expirar")
        else:
            print("\n❌ Falha ao desbloquear (isso nunca deveria acontecer)")
    elif "--check" in sys.argv:
        if is_unlocked():
            print("✅ ScriptureMonChampion está desbloqueado")
            # Mostra quanto tempo resta
            if SESSION_FILE.exists():
                try:
                    with open(SESSION_FILE) as f:
                        session = json.load(f)
                    valid_until = datetime.fromisoformat(session['valid_until'])
                    remaining = (valid_until - datetime.now()).total_seconds()
                    if remaining > 0:
                        print(f"⏰ Sessão expira em {int(remaining)} segundos")
                except:
                    pass
        else:
            print("🔒 ScriptureMonChampion está bloqueado")
            print("⏰ Sessão expirada ou inexistente")
    elif "--help" in sys.argv:
        print("\n🛡️ SCRIPTUREMON GUARDIAN - AJUDA")
        print("="*60)
        print("\nComandos:")
        print("  --unlock : Desbloqueia o sistema (15 segundos)")
        print("  --check  : Verifica status e tempo restante")
        print("  --help   : Mostra esta ajuda")
        print("\n⚡ IMPORTANTE:")
        print("  • Sessões duram apenas 15 SEGUNDOS")
        print("  • Sem limite de tentativas de senha")
        print("  • Sistema NUNCA bloqueia")
        print("\nA senha está em:")
        print(f"  {MEMORY_FILE}")
        print("\nProcure por: '🔐 SENHA DO SISTEMA'")
    else:
        _guardian.show_memory_location()