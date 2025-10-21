#!/usr/bin/env python3
"""
🔒 MAXIMUM PROTECTION HOOKS - Auto-loaded Python Protection
===========================================================
"""

import os
import sys
import builtins
import hashlib
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

PROTECTED_DIR = "/Users/clubproducoes/Digimundo/scripturemon-champion"
PROTECTION_DIR = "/Users/clubproducoes/Digimundo/claude_code/protection"
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
AUTH_FILE = f"{PROTECTION_DIR}/.python_auth"

# Salva funções originais
_original_open = builtins.open
_original_exec = builtins.exec
_original_eval = builtins.eval
_original_compile = builtins.compile
_original_import = builtins.__import__

# Também intercepta os e sys
_original_os_remove = os.remove if hasattr(os, 'remove') else None
_original_os_unlink = os.unlink if hasattr(os, 'unlink') else None
_original_os_rename = os.rename if hasattr(os, 'rename') else None
_original_os_system = os.system if hasattr(os, 'system') else None

def check_authorization():
    """Verifica se há autorização válida"""
    if Path(AUTH_FILE).exists():
        try:
            with _original_open(AUTH_FILE, 'r') as f:
                data = json.load(f)

            expiry = datetime.fromisoformat(data['expiry'])
            if datetime.now() < expiry:
                remaining = (expiry - datetime.now()).seconds
                if remaining <= 5:
                    print(f"⚡ Autorização expira em {remaining} segundos!")
                return True
            else:
                Path(AUTH_FILE).unlink()
                print("⏰ Autorização Python expirou!")
        except:
            pass

    return False

def request_authorization():
    """Solicita autorização do usuário"""
    print("\n" + "="*60)
    print("🔐 MAXIMUM PROTECTION - AUTORIZAÇÃO REQUERIDA")
    print("="*60)
    print("Tentativa de acessar área protegida detectada!")

    import getpass
    password = getpass.getpass("Digite a senha: ")

    if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
        # Cria autorização de 15 segundos
        auth_data = {
            'expiry': (datetime.now() + timedelta(seconds=15)).isoformat(),
            'pid': os.getpid()
        }

        with _original_open(AUTH_FILE, 'w') as f:
            json.dump(auth_data, f)

        print("✅ Autorizado por 15 segundos!")
        return True

    print("❌ Senha incorreta!")
    return False

def is_protected_path(path):
    """Verifica se o caminho está protegido"""
    try:
        path_str = str(Path(path).resolve())
        return path_str.startswith(PROTECTED_DIR)
    except:
        return False

def protected_open(file, mode='r', *args, **kwargs):
    """open() protegido"""
    if is_protected_path(file):
        # Operações de escrita precisam de autorização
        if any(m in mode for m in ['w', 'a', 'x', '+']):
            if not check_authorization():
                if not request_authorization():
                    raise PermissionError(f"MAXIMUM PROTECTION: Acesso negado a {file}")

            # Log da operação
            log_operation('open', file, mode)

    return _original_open(file, mode, *args, **kwargs)

def protected_exec(source, globals=None, locals=None):
    """exec() protegido"""
    # Verifica se está executando código no diretório protegido
    if globals and '__file__' in globals:
        if is_protected_path(globals['__file__']):
            if not check_authorization():
                if not request_authorization():
                    raise PermissionError("MAXIMUM PROTECTION: exec() bloqueado")

    return _original_exec(source, globals, locals)

def protected_eval(expression, globals=None, locals=None):
    """eval() protegido"""
    # Log de eval suspeito
    if 'os.' in str(expression) or 'subprocess' in str(expression):
        log_operation('eval', str(expression)[:100], 'suspicious')

    return _original_eval(expression, globals, locals)

def protected_import(name, *args, **kwargs):
    """__import__() protegido"""
    # Detecta imports perigosos
    dangerous_modules = ['subprocess', 'shutil', 'ctypes', 'multiprocessing']

    if name in dangerous_modules:
        # Verifica contexto
        import inspect
        frame = inspect.currentframe()
        caller_file = frame.f_back.f_code.co_filename if frame else ''

        if is_protected_path(caller_file):
            log_operation('import', name, 'from protected area')

    return _original_import(name, *args, **kwargs)

def protected_os_remove(path):
    """os.remove() protegido"""
    if is_protected_path(path):
        if not check_authorization():
            if not request_authorization():
                raise PermissionError(f"MAXIMUM PROTECTION: Não pode deletar {path}")

        log_operation('os.remove', path, 'DELETE')

    return _original_os_remove(path) if _original_os_remove else None

def protected_os_system(command):
    """os.system() protegido"""
    # Bloqueia comandos perigosos
    if PROTECTED_DIR in command:
        if not check_authorization():
            if not request_authorization():
                raise PermissionError(f"MAXIMUM PROTECTION: Comando bloqueado")

        log_operation('os.system', command, 'COMMAND')

    return _original_os_system(command) if _original_os_system else None

def log_operation(operation, target, details=''):
    """Registra operação no log"""
    log_file = Path(PROTECTION_DIR) / "python_operations.log"

    timestamp = datetime.now().isoformat()
    pid = os.getpid()

    log_entry = f"[{timestamp}] PID:{pid} {operation} -> {target} ({details})\n"

    try:
        with _original_open(log_file, 'a') as f:
            f.write(log_entry)
    except:
        pass

def activate():
    """Ativa os hooks de proteção"""
    # Substitui funções built-in
    builtins.open = protected_open
    builtins.exec = protected_exec
    builtins.eval = protected_eval
    builtins.__import__ = protected_import

    # Substitui funções do os
    if _original_os_remove:
        os.remove = protected_os_remove
        os.unlink = protected_os_remove

    if _original_os_rename:
        def protected_rename(src, dst):
            if is_protected_path(src) or is_protected_path(dst):
                if not check_authorization():
                    if not request_authorization():
                        raise PermissionError("MAXIMUM PROTECTION: rename bloqueado")
            return _original_os_rename(src, dst)

        os.rename = protected_rename

    if _original_os_system:
        os.system = protected_os_system

    # Adiciona verificação em subprocess
    try:
        import subprocess
        _original_run = subprocess.run

        def protected_run(args, **kwargs):
            cmd_str = ' '.join(args) if isinstance(args, list) else str(args)

            if PROTECTED_DIR in cmd_str:
                if not check_authorization():
                    if not request_authorization():
                        raise PermissionError("MAXIMUM PROTECTION: subprocess bloqueado")

            return _original_run(args, **kwargs)

        subprocess.run = protected_run
    except:
        pass

    # Adiciona aviso
    print("🔐 MAXIMUM PROTECTION HOOKS ATIVADOS")
    print("   • open() protegido")
    print("   • exec/eval protegidos")
    print("   • os.* protegidos")
    print("   • subprocess protegido")
    print("   • Sessões de 15 segundos")

def deactivate():
    """Desativa os hooks (para emergências)"""
    # Restaura funções originais
    builtins.open = _original_open
    builtins.exec = _original_exec
    builtins.eval = _original_eval
    builtins.__import__ = _original_import

    if _original_os_remove:
        os.remove = _original_os_remove
        os.unlink = _original_os_unlink

    if _original_os_rename:
        os.rename = _original_os_rename

    if _original_os_system:
        os.system = _original_os_system

    print("⚠️ PROTEÇÃO DESATIVADA")

# Auto-ativa se importado diretamente
if __name__ != "__main__":
    activate()