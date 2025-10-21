#!/usr/bin/env python3
"""
🔐 CLAUDE TOOLS HOOK PROTECTION SYSTEM
=====================================
Intercepta as ferramentas do Claude Code (Write, Edit, MultiEdit)
e força autenticação + leitura de memórias
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import getpass

class ClaudeToolsProtection:
    """Sistema de proteção para ferramentas do Claude Code"""

    def __init__(self):
        self.protected_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.memory_dir = Path("/Users/clubproducoes/Digimundo/claude_code/memory")
        self.session_file = Path("/Users/clubproducoes/Digimundo/claude_code/.claude_session")
        self.session_duration = 300  # 5 minutos
        self.password_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # admin

    def check_path_protected(self, path: str) -> bool:
        """Verifica se o caminho está na área protegida"""
        try:
            target = Path(path).resolve()
            return str(target).startswith(str(self.protected_dir))
        except:
            return False

    def validate_session(self) -> bool:
        """Verifica se há sessão válida"""
        if not self.session_file.exists():
            return False

        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                expires = datetime.fromisoformat(data['expires'])
                return datetime.now() < expires
        except:
            return False

    def create_session(self):
        """Cria nova sessão após autenticação"""
        expires = datetime.now() + timedelta(seconds=self.session_duration)
        data = {
            'expires': expires.isoformat(),
            'authenticated': True,
            'memories_loaded': False
        }
        with open(self.session_file, 'w') as f:
            json.dump(data, f)

    def authenticate(self) -> bool:
        """Solicita senha para autenticação"""
        print("\n" + "="*60)
        print("🔐 PROTEÇÃO ATIVADA - ÁREA RESTRITA")
        print("="*60)
        print(f"📂 Tentativa de acesso: {self.protected_dir}")
        print("🔑 Digite a senha para continuar:")

        for attempt in range(3):
            password = getpass.getpass(f"Tentativa {attempt+1}/3: ")
            if hashlib.sha256(password.encode()).hexdigest() == self.password_hash:
                print("✅ Senha correta!")
                self.create_session()
                return True
            else:
                print("❌ Senha incorreta!")

        print("🚫 Acesso negado após 3 tentativas!")
        return False

    def load_memories(self) -> Dict[str, Any]:
        """Força leitura dos arquivos de memória"""
        memories = {}
        critical_files = [
            "REGRA_ESPECIAL.md",
            "REGRAS_REFATORACAO_MINIMALISTA.md",
            "REFATORACAO_LOG_2025-09-18.md"
        ]

        print("\n📚 CARREGANDO MEMÓRIAS OBRIGATÓRIAS:")
        print("-" * 40)

        for filename in critical_files:
            filepath = self.memory_dir / filename
            if filepath.exists():
                with open(filepath, 'r') as f:
                    content = f.read()
                    memories[filename] = content

                    # Extrai regra crítica
                    if "DIGIMUNDO PRESENTE" in content:
                        print(f"✓ {filename}: REGRA DIGIMUNDO DETECTADA")
                    else:
                        print(f"✓ {filename}: {len(content)} bytes")

        # Marca que memórias foram carregadas
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                data = json.load(f)
            data['memories_loaded'] = True
            with open(self.session_file, 'w') as f:
                json.dump(data, f)

        return memories

    def intercept_tool(self, tool_name: str, file_path: str, operation: str) -> bool:
        """Intercepta operação de ferramenta do Claude"""

        # Verifica se é área protegida
        if not self.check_path_protected(file_path):
            return True  # Permite operações fora da área protegida

        print(f"\n🛡️ INTERCEPTANDO: {tool_name}")
        print(f"📁 Arquivo: {file_path}")
        print(f"⚙️ Operação: {operation}")

        # Verifica sessão
        if not self.validate_session():
            print("⏰ Sessão expirada ou inexistente!")
            if not self.authenticate():
                raise PermissionError(f"Acesso negado para {file_path}")

        # Verifica se memórias foram carregadas
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                if not data.get('memories_loaded', False):
                    print("\n⚠️ MEMÓRIAS NÃO CARREGADAS!")
                    memories = self.load_memories()
                    print(f"\n📊 {len(memories)} memórias carregadas")
                    print("💡 Lembre-se: TODA resposta deve terminar com DIGIMUNDO PRESENTE")

        return True

    def hook_write(self, file_path: str, content: str) -> bool:
        """Hook para ferramenta Write"""
        return self.intercept_tool("Write", file_path, "create/overwrite")

    def hook_edit(self, file_path: str, old_string: str, new_string: str) -> bool:
        """Hook para ferramenta Edit"""
        return self.intercept_tool("Edit", file_path, "modify")

    def hook_multiedit(self, file_path: str, edits: list) -> bool:
        """Hook para ferramenta MultiEdit"""
        return self.intercept_tool("MultiEdit", file_path, f"modify {len(edits)} sections")

# Instância global
protection = ClaudeToolsProtection()

def before_write(file_path: str, content: str):
    """Hook executado antes de Write"""
    protection.hook_write(file_path, content)

def before_edit(file_path: str, old_string: str, new_string: str):
    """Hook executado antes de Edit"""
    protection.hook_edit(file_path, old_string, new_string)

def before_multiedit(file_path: str, edits: list):
    """Hook executado antes de MultiEdit"""
    protection.hook_multiedit(file_path, edits)

if __name__ == "__main__":
    print("🔐 CLAUDE TOOLS HOOK PROTECTION")
    print("="*60)

    # Testa proteção
    test_file = "/Users/clubproducoes/Digimundo/scripturemon-champion/test.txt"

    try:
        before_write(test_file, "test content")
        print("✅ Hook funcionando!")
    except PermissionError as e:
        print(f"🔐 {e}")

    # Mostra status
    if protection.validate_session():
        print("\n✅ Sessão ativa")
    else:
        print("\n❌ Sem sessão ativa")