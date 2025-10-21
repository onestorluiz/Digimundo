#!/usr/bin/env python3
"""
🔐 SISTEMA DE PROTEÇÃO REAL - INTERCEPTADOR DE OPERAÇÕES
=========================================================
Este sistema intercepta TODAS as operações de arquivo no Python
"""

import os
import sys
import json
import builtins
import hashlib
import getpass
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional

# Configurações
PROTECTED_DIR = "/Users/clubproducoes/Digimundo/scripturemon-champion"
SESSION_FILE = Path("/Users/clubproducoes/Digimundo/claude_code/.real_session")
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
SESSION_DURATION = 15  # segundos

# Salvar funções originais
_original_open = builtins.open
_original_unlink = os.unlink
_original_remove = os.remove
_original_rename = os.rename
_original_mkdir = os.mkdir
_original_makedirs = os.makedirs
_original_rmdir = os.rmdir

class RealProtection:
    """Sistema de proteção real que intercepta operações"""

    def __init__(self):
        self.install_hooks()

    def check_session(self) -> bool:
        """Verifica se há sessão válida (15 segundos)"""
        if SESSION_FILE.exists():
            try:
                with _original_open(SESSION_FILE, 'r') as f:
                    session = json.load(f)
                valid_until = datetime.fromisoformat(session['valid_until'])
                remaining = (valid_until - datetime.now()).total_seconds()

                if remaining > 0:
                    if remaining <= 5:
                        print(f"\n⚡ SESSÃO EXPIRA EM {int(remaining)} SEGUNDOS!")
                    return True
                else:
                    print("\n⏰ SESSÃO EXPIROU! Autentique-se novamente.")
                    SESSION_FILE.unlink()
            except:
                pass
        return False

    def authenticate(self) -> bool:
        """Força autenticação"""
        print("\n" + "="*60)
        print("🔐 PROTEÇÃO REAL ATIVADA - OPERAÇÃO BLOQUEADA")
        print("="*60)
        print("⚡ Digite a senha para continuar (sessão de 15 segundos)")

        while True:
            password = getpass.getpass("🔑 Senha: ")
            if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
                print("✅ Senha correta!")
                self.create_session()
                return True
            else:
                print("❌ Senha incorreta. Tente novamente.")

    def create_session(self):
        """Cria sessão de 15 segundos"""
        session_data = {
            'authenticated_at': datetime.now().isoformat(),
            'valid_until': (datetime.now() + timedelta(seconds=SESSION_DURATION)).isoformat()
        }
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _original_open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
        print(f"⏱️ Sessão criada - válida por {SESSION_DURATION} segundos")

    def is_protected_path(self, path: Any) -> bool:
        """Verifica se o caminho está protegido"""
        try:
            path_str = str(Path(path).resolve())
            return path_str.startswith(PROTECTED_DIR)
        except:
            return False

    def protected_open(self, file, mode='r', *args, **kwargs):
        """open() protegido"""
        if self.is_protected_path(file) and any(m in mode for m in ['w', 'a', 'x', '+']):
            if not self.check_session():
                self.authenticate()
        return _original_open(file, mode, *args, **kwargs)

    def protected_unlink(self, path, *args, **kwargs):
        """unlink() protegido"""
        if self.is_protected_path(path):
            if not self.check_session():
                self.authenticate()
        return _original_unlink(path, *args, **kwargs)

    def protected_remove(self, path, *args, **kwargs):
        """remove() protegido"""
        if self.is_protected_path(path):
            if not self.check_session():
                self.authenticate()
        return _original_remove(path, *args, **kwargs)

    def protected_rename(self, src, dst, *args, **kwargs):
        """rename() protegido"""
        if self.is_protected_path(src) or self.is_protected_path(dst):
            if not self.check_session():
                self.authenticate()
        return _original_rename(src, dst, *args, **kwargs)

    def protected_mkdir(self, path, *args, **kwargs):
        """mkdir() protegido"""
        if self.is_protected_path(path):
            if not self.check_session():
                self.authenticate()
        return _original_mkdir(path, *args, **kwargs)

    def protected_makedirs(self, path, *args, **kwargs):
        """makedirs() protegido"""
        if self.is_protected_path(path):
            if not self.check_session():
                self.authenticate()
        return _original_makedirs(path, *args, **kwargs)

    def protected_rmdir(self, path, *args, **kwargs):
        """rmdir() protegido"""
        if self.is_protected_path(path):
            if not self.check_session():
                self.authenticate()
        return _original_rmdir(path, *args, **kwargs)

    def install_hooks(self):
        """Instala os hooks de proteção"""
        builtins.open = self.protected_open
        os.unlink = self.protected_unlink
        os.remove = self.protected_remove
        os.rename = self.protected_rename
        os.mkdir = self.protected_mkdir
        os.makedirs = self.protected_makedirs
        os.rmdir = self.protected_rmdir

        # Também proteger Path operations
        if hasattr(Path, 'unlink'):
            Path.unlink = lambda self: protected_unlink(self)

        print("🛡️ PROTEÇÃO REAL INSTALADA - Interceptando todas as operações")

# Auto-instalar ao importar
_protection = RealProtection()

def activate():
    """Ativa a proteção real"""
    global _protection
    if _protection is None:
        _protection = RealProtection()
    print("✅ Proteção real ativada")

def deactivate():
    """Desativa a proteção (restaura funções originais)"""
    builtins.open = _original_open
    os.unlink = _original_unlink
    os.remove = _original_remove
    os.rename = _original_rename
    os.mkdir = _original_mkdir
    os.makedirs = _original_makedirs
    os.rmdir = _original_rmdir
    print("⚠️ Proteção desativada - sistema vulnerável")

if __name__ == "__main__":
    print("="*80)
    print("🔐 SISTEMA DE PROTEÇÃO REAL")
    print("="*80)
    print("\nEste sistema intercepta TODAS as operações de arquivo")
    print("Para ativar, importe este módulo no início do script:")
    print("\n   import REAL_PROTECTION")
    print("\nTodas as operações em", PROTECTED_DIR)
    print("exigirão senha com sessão de", SESSION_DURATION, "segundos")
    print("="*80)