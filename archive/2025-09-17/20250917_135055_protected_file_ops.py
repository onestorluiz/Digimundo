#!/usr/bin/env python3
"""
🔒 PROTECTED FILE OPERATIONS
=============================
Todas as operações de arquivo devem passar por aqui.
Requer autenticação via senha que está em CLAUDE.md
"""

import os
import sys
from pathlib import Path
from typing import Optional, Any
from claude_protection_system import ClaudeProtectionSystem, protect_operation

class ProtectedFileOperations:
    """Operações de arquivo protegidas por senha"""

    def __init__(self):
        self.protection = ClaudeProtectionSystem()

    def read_file(self, file_path: str) -> Optional[str]:
        """Lê arquivo (requer autenticação)"""
        if not protect_operation(f"READ {file_path}"):
            print("❌ Leitura bloqueada. Autentique-se primeiro!")
            print("💡 Dica: A senha está em CLAUDE.md")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return None

    def write_file(self, file_path: str, content: str) -> bool:
        """Escreve arquivo (requer autenticação)"""
        if not protect_operation(f"WRITE {file_path}"):
            print("❌ Escrita bloqueada. Autentique-se primeiro!")
            print("💡 Dica: cat CLAUDE.md | grep 'SENHA DO SISTEMA'")
            return False

        try:
            # Verificar se já existe
            if Path(file_path).exists():
                print(f"⚠️ Arquivo já existe: {file_path}")
                response = input("Sobrescrever? (s/n): ")
                if response.lower() != 's':
                    return False

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Arquivo escrito: {file_path}")
            return True
        except Exception as e:
            print(f"Erro ao escrever arquivo: {e}")
            return False

    def create_file(self, file_path: str, content: str = "") -> bool:
        """Cria novo arquivo (requer autenticação)"""
        if not protect_operation(f"CREATE {file_path}"):
            print("❌ Criação bloqueada. Autentique-se primeiro!")
            print("📝 Leia CLAUDE.md para encontrar a senha")
            return False

        # Verificar se já existe
        if Path(file_path).exists():
            print(f"❌ ERRO: Arquivo já existe: {file_path}")
            print("💡 Use modify_file() para modificar arquivos existentes")
            return False

        return self.write_file(file_path, content)

    def modify_file(self, file_path: str, old_content: str, new_content: str) -> bool:
        """Modifica arquivo existente (requer autenticação)"""
        if not protect_operation(f"MODIFY {file_path}"):
            print("❌ Modificação bloqueada. Autentique-se primeiro!")
            return False

        if not Path(file_path).exists():
            print(f"❌ ERRO: Arquivo não existe: {file_path}")
            print("💡 Use create_file() para criar novos arquivos")
            return False

        current = self.read_file(file_path)
        if current is None:
            return False

        if old_content not in current:
            print("❌ Conteúdo antigo não encontrado no arquivo")
            return False

        new_full_content = current.replace(old_content, new_content)
        return self.write_file(file_path, new_full_content)

    def delete_file(self, file_path: str) -> bool:
        """Deleta arquivo (requer autenticação E confirmação)"""
        if not protect_operation(f"DELETE {file_path}"):
            print("❌ Deleção bloqueada. Autentique-se primeiro!")
            return False

        if not Path(file_path).exists():
            print(f"Arquivo não existe: {file_path}")
            return False

        print(f"⚠️ ATENÇÃO: Deletar {file_path}?")
        print("Digite 'CONFIRMAR DELEÇÃO' para prosseguir:")
        confirm = input()

        if confirm != "CONFIRMAR DELEÇÃO":
            print("Deleção cancelada")
            return False

        try:
            os.remove(file_path)
            print(f"✅ Arquivo deletado: {file_path}")
            return True
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False


# Funções wrapper para uso direto
_ops = ProtectedFileOperations()

def safe_read(file_path: str) -> Optional[str]:
    """Leitura segura de arquivo"""
    return _ops.read_file(file_path)

def safe_write(file_path: str, content: str) -> bool:
    """Escrita segura de arquivo"""
    return _ops.write_file(file_path, content)

def safe_create(file_path: str, content: str = "") -> bool:
    """Criação segura de arquivo"""
    return _ops.create_file(file_path, content)

def safe_modify(file_path: str, old: str, new: str) -> bool:
    """Modificação segura de arquivo"""
    return _ops.modify_file(file_path, old, new)

def safe_delete(file_path: str) -> bool:
    """Deleção segura de arquivo"""
    return _ops.delete_file(file_path)


if __name__ == "__main__":
    print("🔒 SISTEMA DE OPERAÇÕES PROTEGIDAS")
    print("="*60)

    # Testar autenticação
    if not _ops.protection.is_authenticated():
        print("Sistema bloqueado. Tentando autenticar...")
        if not _ops.protection.authenticate():
            print("❌ Falha na autenticação!")
            print("💡 Leia CLAUDE.md para encontrar a senha")
            sys.exit(1)

    print("\n✅ Sistema desbloqueado!")
    print("\nOperações disponíveis:")
    print("  • safe_read(file_path)")
    print("  • safe_write(file_path, content)")
    print("  • safe_create(file_path, content)")
    print("  • safe_modify(file_path, old, new)")
    print("  • safe_delete(file_path)")
    print("\nTodas requerem autenticação prévia!")