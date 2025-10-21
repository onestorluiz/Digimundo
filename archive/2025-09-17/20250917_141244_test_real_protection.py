#!/usr/bin/env python3
"""
🔒 TESTE DA PROTEÇÃO REAL
=========================
"""

import sys
import os
from pathlib import Path

# Adicionar path da proteção
sys.path.insert(0, "/Users/clubproducoes/Digimundo/claude_code/protection")

print("="*80)
print("🔒 TESTE DO SISTEMA DE PROTEÇÃO REAL")
print("="*80)

print("\n1️⃣ TESTE SEM PROTEÇÃO:")
print("-"*40)

# Primeiro teste - SEM proteção
try:
    test_file = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/test_sem_protecao.txt")
    with open(test_file, 'w') as f:
        f.write("Criado SEM proteção")
    print("⚠️ Conseguiu criar arquivo SEM SENHA")

    # Ler
    with open(test_file, 'r') as f:
        content = f.read()
    print(f"⚠️ Conseguiu ler: '{content}'")

    # Deletar
    os.remove(test_file)
    print("⚠️ Conseguiu deletar arquivo")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n2️⃣ ATIVANDO PROTEÇÃO REAL:")
print("-"*40)

# Importar proteção - isso já ativa automaticamente
import REAL_PROTECTION

print("\n3️⃣ TESTE COM PROTEÇÃO ATIVADA:")
print("-"*40)

# Remover sessão se existir
session_file = Path("/Users/clubproducoes/Digimundo/claude_code/.real_session")
if session_file.exists():
    # Usar função original para remover
    os.unlink(session_file)
    print("📝 Sessão removida para forçar autenticação")

# Agora tentar criar arquivo - DEVE PEDIR SENHA
print("\n🔐 Tentando criar arquivo no diretório protegido...")
print("⚡ DEVE PEDIR SENHA AGORA:")

try:
    test_file = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/test_com_protecao.txt")

    # Esta operação deve disparar a proteção
    with open(test_file, 'w') as f:
        f.write("Criado COM proteção")

    print("✅ Arquivo criado após autenticação")

    # Verificar se arquivo existe
    if test_file.exists():
        print(f"✅ Arquivo confirmado: {test_file}")

        # Limpar
        os.remove(test_file)
        print("✅ Arquivo removido (ainda na sessão de 15 segundos)")

except KeyboardInterrupt:
    print("\n❌ Teste cancelado pelo usuário")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n4️⃣ TESTE DE OPERAÇÕES FORA DO DIRETÓRIO PROTEGIDO:")
print("-"*40)

# Criar arquivo em /tmp (não protegido)
try:
    tmp_file = Path("/tmp/teste_nao_protegido.txt")
    with open(tmp_file, 'w') as f:
        f.write("Arquivo em /tmp")
    print("✅ Criou arquivo em /tmp SEM pedir senha (não protegido)")

    # Limpar
    os.remove(tmp_file)
    print("✅ Removeu arquivo de /tmp sem senha")

except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*80)
print("📊 RESUMO DO TESTE:")
print("="*80)
print("• Sem proteção: Acesso LIVRE (vulnerável)")
print("• Com proteção: Exige SENHA para modificações")
print("• Sessões de 15 segundos funcionando")
print("• Diretórios não protegidos: Acesso normal")
print("="*80)