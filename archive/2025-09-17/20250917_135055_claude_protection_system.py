#!/usr/bin/env python3
"""
🔐 CLAUDE PROTECTION SYSTEM - Sistema de Proteção por Senha
============================================================
A senha está na memória. Se você não leu, não consegue trabalhar!
"""

import os
import sys
import json
import hashlib
import getpass
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# A senha real está no CLAUDE.md
# Mas o hash está aqui para validação
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # admin
CORRECT_PASSWORD = None  # Deve ser descoberto lendo CLAUDE.md

class ClaudeProtectionSystem:
    """Sistema de proteção que força leitura da memória"""

    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.session_file = self.root / ".claude_protected_session"
        self.locked_file = self.root / ".system_locked"
        self.attempts_file = self.root / ".password_attempts"
        self.max_attempts = 3

    def is_system_locked(self) -> bool:
        """Verifica se o sistema está bloqueado"""
        if self.locked_file.exists():
            with open(self.locked_file, 'r') as f:
                lock_data = json.load(f)
                lock_time = datetime.fromisoformat(lock_data['locked_at'])
                # Bloqueia por 10 minutos após 3 tentativas erradas
                if datetime.now() - lock_time < timedelta(minutes=10):
                    remaining = 10 - ((datetime.now() - lock_time).seconds // 60)
                    print(f"🔒 SISTEMA BLOQUEADO! Aguarde {remaining} minutos.")
                    return True
                else:
                    os.remove(self.locked_file)
        return False

    def check_password(self, password: str) -> bool:
        """Verifica se a senha está correta"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == PASSWORD_HASH

    def get_attempts(self) -> int:
        """Retorna número de tentativas erradas"""
        if self.attempts_file.exists():
            with open(self.attempts_file, 'r') as f:
                return json.load(f)['attempts']
        return 0

    def increment_attempts(self):
        """Incrementa tentativas erradas"""
        attempts = self.get_attempts() + 1
        with open(self.attempts_file, 'w') as f:
            json.dump({'attempts': attempts, 'last_attempt': datetime.now().isoformat()}, f)

        if attempts >= self.max_attempts:
            self.lock_system()

    def lock_system(self):
        """Bloqueia o sistema"""
        with open(self.locked_file, 'w') as f:
            json.dump({'locked_at': datetime.now().isoformat()}, f)
        print("🔒 SISTEMA BLOQUEADO APÓS 3 TENTATIVAS ERRADAS!")
        print("⏰ Aguarde 10 minutos ou leia CLAUDE.md para descobrir a senha.")

    def reset_attempts(self):
        """Reseta contador de tentativas"""
        if self.attempts_file.exists():
            os.remove(self.attempts_file)

    def create_session(self):
        """Cria sessão autenticada"""
        session_data = {
            'authenticated_at': datetime.now().isoformat(),
            'valid_until': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)

    def is_authenticated(self) -> bool:
        """Verifica se há sessão válida"""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                session = json.load(f)
                valid_until = datetime.fromisoformat(session['valid_until'])
                if datetime.now() < valid_until:
                    return True
        return False

    def authenticate(self) -> bool:
        """Processo de autenticação"""
        # Verifica se já está autenticado
        if self.is_authenticated():
            print("✅ Sessão ainda válida.")
            return True

        # Verifica se está bloqueado
        if self.is_system_locked():
            return False

        print("\n" + "="*60)
        print("🔐 SISTEMA DE PROTEÇÃO CLAUDE CODE")
        print("="*60)
        print("\n⚠️  ACESSO PROTEGIDO POR SENHA")
        print("📝 A senha está no arquivo CLAUDE.md")
        print("🔍 Procure por: 'SENHA DO SISTEMA'\n")

        attempts_left = self.max_attempts - self.get_attempts()
        print(f"Tentativas restantes: {attempts_left}")

        password = getpass.getpass("Digite a senha: ")

        if self.check_password(password):
            print("✅ SENHA CORRETA! Acesso liberado.")
            self.reset_attempts()
            self.create_session()
            self.show_memory_reminder()
            return True
        else:
            print("❌ SENHA INCORRETA!")
            self.increment_attempts()
            print("\n💡 DICA: Leia o arquivo CLAUDE.md")
            print("   cat CLAUDE.md | grep -A 2 'SENHA DO SISTEMA'")
            return False

    def show_memory_reminder(self):
        """Mostra lembretes após login bem-sucedido"""
        print("\n" + "="*60)
        print("📋 LEMBRETES CRÍTICOS:")
        print("="*60)
        print("• Código real está em: deployments/green_v2.0.0/code/")
        print("• apps/scripturemon/ está VAZIO")
        print("• 323 arquivos geram outros arquivos")
        print("• Não criar mais sistemas de memória (já tem 24)")
        print("• Sempre verificar se arquivo existe antes de criar")
        print("="*60)

def protect_operation(operation: str) -> bool:
    """Wrapper para proteger operações"""
    protection = ClaudeProtectionSystem()

    if not protection.is_authenticated():
        print(f"\n🚫 OPERAÇÃO BLOQUEADA: {operation}")
        print("❌ Você precisa se autenticar primeiro!")
        return protection.authenticate()

    return True

def unlock_with_hint():
    """Mostra dica para desbloquear"""
    print("\n" + "="*60)
    print("🔓 COMO DESBLOQUEAR O SISTEMA")
    print("="*60)
    print("\n1. LEIA A MEMÓRIA:")
    print("   cat CLAUDE.md | grep -B2 -A2 'SENHA'")
    print("\n2. PROCURE A SEÇÃO:")
    print("   ## 🔐 SENHA DO SISTEMA")
    print("\n3. USE A SENHA PARA DESBLOQUEAR:")
    print("   python3 claude_protection_system.py")
    print("\n4. APÓS DESBLOQUEAR, LEIA TODO O CLAUDE.md")
    print("="*60)


if __name__ == "__main__":
    protection = ClaudeProtectionSystem()

    if "--unlock" in sys.argv:
        unlock_with_hint()
    elif "--check" in sys.argv:
        if protection.is_authenticated():
            print("✅ Sistema desbloqueado. Sessão válida.")
        else:
            print("🔒 Sistema bloqueado. Autenticação necessária.")
    else:
        if protection.authenticate():
            print("\n✅ SISTEMA DESBLOQUEADO!")
            print("📝 Agora leia CLAUDE.md completo antes de trabalhar.")
        else:
            print("\n❌ ACESSO NEGADO!")
            unlock_with_hint()