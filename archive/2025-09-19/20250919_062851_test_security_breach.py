#!/usr/bin/env python3
"""
🔓 TESTE DE INVASÃO E BYPASS DO SISTEMA DE SEGURANÇA
======================================================
Tenta burlar o sistema de proteção de várias formas
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


# Diretórios
SCRIPTUREMON_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
CLAUDE_CODE_DIR = Path("/Users/clubproducoes/Digimundo/claude_code")
SESSION_FILE = CLAUDE_CODE_DIR / ".guardian_session"

print("="*80)
print("🔓 TESTE DE BYPASS DO SISTEMA DE SEGURANÇA")
print("="*80)

# Remover sessão se existir
if SESSION_FILE.exists():
    SESSION_FILE.unlink()
    print("❌ Sessão removida para simular acesso sem contexto")

print("\n" + "="*60)
print("TESTE 1: Acesso direto a arquivos sem autenticação")
print("="*60)

# Tentar ler arquivo protegido diretamente
test_file = SCRIPTUREMON_DIR / "test_invasao.txt"
try:
    # Tentar criar arquivo diretamente
    with open(test_file, 'w') as f:
        f.write("INVASÃO DIRETA - Arquivo criado sem senha!")
    print("⚠️ CONSEGUIU criar arquivo SEM SENHA!")
    print(f"   Arquivo: {test_file}")

    # Tentar ler
    with open(test_file, 'r') as f:
        content = f.read()
    print(f"⚠️ CONSEGUIU ler arquivo: {content}")

    # Limpar
    os.remove(test_file)
    print("⚠️ CONSEGUIU deletar arquivo")

except Exception as e:
    print(f"✅ Bloqueado: {e}")

print("\n" + "="*60)
print("TESTE 2: Bypass via Python import direto")
print("="*60)

try:
    # Tentar importar e usar diretamente
    sys.path.insert(0, str(SCRIPTUREMON_DIR))

    # Tentar modificar arquivo via Python
    test_content = """
# ARQUIVO INVADIDO SEM SENHA
print("Sistema comprometido!")
"""
    test_path = SCRIPTUREMON_DIR / "hacked_module.py"

    with open(test_path, 'w') as f:
        f.write(test_content)

    print(f"⚠️ CONSEGUIU criar módulo Python sem senha: {test_path}")

    # Tentar importar
    import hacked_module
    print("⚠️ CONSEGUIU importar módulo criado!")

    # Limpar
    os.remove(test_path)

except Exception as e:
    print(f"✅ Bloqueado: {e}")

print("\n" + "="*60)
print("TESTE 3: Criar sessão falsa")
print("="*60)

try:
    # Tentar criar sessão falsa
    fake_session = {
        'authenticated_at': datetime.now().isoformat(),
        'valid_until': (datetime.now() + timedelta(hours=999)).isoformat(),
        'memory_read': True
    }

    with open(SESSION_FILE, 'w') as f:
        json.dump(fake_session, f)

    print("⚠️ CONSEGUIU criar sessão falsa!")

    # Verificar se sistema aceita
    result = subprocess.run(
        "python3 /Users/clubproducoes/Digimundo/claude_code/protection/scripturemon_guardian.py --check",
        shell=True,
        capture_output=True,
        text=True
    )

    if "desbloqueado" in result.stdout:
        print("🔴 CRÍTICO: Sistema aceitou sessão falsa!")
    else:
        print("✅ Sistema rejeitou sessão falsa")

    # Limpar
    SESSION_FILE.unlink()

except Exception as e:
    print(f"✅ Erro ao criar sessão falsa: {e}")

print("\n" + "="*60)
print("TESTE 4: Execução de comandos bash")
print("="*60)

# Tentar executar comandos diretamente
commands = [
    f"echo 'HACKED' > {SCRIPTUREMON_DIR}/invasao.txt",
    f"cat {SCRIPTUREMON_DIR}/protected_file_ops.py | head -5",
    f"ls -la {SCRIPTUREMON_DIR}/*.py | head -3"
]

for cmd in commands:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"⚠️ Comando executado SEM SENHA: {cmd[:50]}...")
        if result.stdout:
            print(f"   Output: {result.stdout[:100]}...")
    else:
        print(f"✅ Comando bloqueado: {cmd[:50]}...")

# Limpar arquivo se foi criado
invasao_file = SCRIPTUREMON_DIR / "invasao.txt"
if invasao_file.exists():
    invasao_file.unlink()
    print("   Arquivo de invasão removido")

print("\n" + "="*60)
print("TESTE 5: Modificação via sed/awk")
print("="*60)

# Criar arquivo temporário para teste
temp_file = SCRIPTUREMON_DIR / "temp_test.txt"
try:
    with open(temp_file, 'w') as f:
        f.write("Conteúdo original")

    # Tentar modificar via sed
    cmd = f"sed -i '' 's/original/HACKEADO/g' {temp_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        with open(temp_file, 'r') as f:
            content = f.read()
        if "HACKEADO" in content:
            print(f"⚠️ CONSEGUIU modificar arquivo via sed sem senha!")
            print(f"   Novo conteúdo: {content}")
        else:
            print("✅ Modificação via sed falhou")
    else:
        print("✅ sed bloqueado")

    # Limpar
    if temp_file.exists():
        temp_file.unlink()

except Exception as e:
    print(f"✅ Erro: {e}")

print("\n" + "="*60)
print("TESTE 6: Acesso via symlink")
print("="*60)

try:
    # Criar symlink para burlar proteção
    link_path = Path("/tmp/scripturemon_link")
    if link_path.exists():
        link_path.unlink()

    os.symlink(SCRIPTUREMON_DIR, link_path)
    print(f"⚠️ Criou symlink: {link_path} -> {SCRIPTUREMON_DIR}")

    # Tentar acessar via symlink
    test_via_link = link_path / "test_symlink.txt"
    with open(test_via_link, 'w') as f:
        f.write("Acessado via symlink sem senha!")

    print(f"⚠️ CONSEGUIU criar arquivo via symlink sem senha!")

    # Verificar se arquivo existe
    real_file = SCRIPTUREMON_DIR / "test_symlink.txt"
    if real_file.exists():
        print("🔴 CRÍTICO: Arquivo criado no diretório real!")
        real_file.unlink()

    # Limpar
    link_path.unlink()

except Exception as e:
    print(f"✅ Symlink bloqueado: {e}")

print("\n" + "="*80)
print("RELATÓRIO FINAL DE VULNERABILIDADES")
print("="*80)

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
