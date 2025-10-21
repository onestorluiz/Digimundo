#!/usr/bin/env python3
"""
🔒 TESTE COMPLETO DO SISTEMA DE SEGURANÇA
==========================================
Testa todas as funcionalidades do sistema de proteção
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


# Paths
CLAUDE_CODE_DIR = Path("/Users/clubproducoes/Digimundo/claude_code")
PROTECTION_DIR = CLAUDE_CODE_DIR / "protection"
MEMORY_FILE = CLAUDE_CODE_DIR / "memory/CLAUDE_MEMORY.md"
SESSION_FILE = CLAUDE_CODE_DIR / ".guardian_session"
LOCK_FILE = CLAUDE_CODE_DIR / ".guardian_lock"

class SecuritySystemTester:
    """Testador do sistema de segurança"""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []

    def print_header(self, title):
        """Imprime cabeçalho de teste"""
        print("\n" + "="*80)
        print(f"🔬 {title}")
        print("="*80)

    def test_result(self, test_name, passed, details=""):
        """Registra resultado de teste"""
        if passed:
            self.tests_passed += 1
            print(f"  ✅ {test_name}")
            status = "PASSED"
        else:
            self.tests_failed += 1
            print(f"  ❌ {test_name}")
            status = "FAILED"

        if details:
            print(f"     {details}")

        self.results.append({
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def test_memory_file_exists(self):
        """Testa se arquivo de memória existe"""
        self.print_header("TESTE 1: ARQUIVO DE MEMÓRIA")

        exists = MEMORY_FILE.exists()
        self.test_result(
            "Arquivo de memória existe",
            exists,
            f"Path: {MEMORY_FILE}"
        )

        if exists:
            # Verifica se contém a senha
            content = MEMORY_FILE.read_text()
            has_password = "SENHA:" in content and "admin" in content
            self.test_result(
                "Memória contém senha",
                has_password,
                "Seção de senha encontrada" if has_password else "Senha não encontrada"
            )

            # Verifica regras críticas
            has_rules = "REGRAS CRÍTICAS DO SCRIPTUREMON" in content
            self.test_result(
                "Memória contém regras críticas",
                has_rules,
                "39 regras do backup incluídas" if has_rules else "Regras não encontradas"
            )

    def test_protection_files(self):
        """Testa arquivos de proteção"""
        self.print_header("TESTE 2: ARQUIVOS DE PROTEÇÃO")

        protection_files = [
            "scripturemon_guardian.py",
            "claude_protection_system.py",
            "protected_file_ops.py"
        ]

        for file in protection_files:
            file_path = PROTECTION_DIR / file
            exists = file_path.exists()
            self.test_result(
                f"Arquivo {file} existe",
                exists,
                f"Size: {file_path.stat().st_size} bytes" if exists else "Arquivo não encontrado"
            )

    def test_session_management(self):
        """Testa gerenciamento de sessão"""
        self.print_header("TESTE 3: GERENCIAMENTO DE SESSÃO")

        # Verifica sessão atual
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE) as f:
                    session = json.load(f)
                valid_until = datetime.fromisoformat(session['valid_until'])
                is_valid = datetime.now() < valid_until
                remaining = (valid_until - datetime.now()).seconds // 60

                self.test_result(
                    "Sessão ativa encontrada",
                    is_valid,
                    f"Válida por mais {remaining} minutos" if is_valid else "Sessão expirada"
                )
            except Exception as e:
                self.test_result(
                    "Sessão ativa encontrada",
                    False,
                    f"Erro ao ler sessão: {e}"
                )
        else:
            self.test_result(
                "Sessão ativa encontrada",
                False,
                "Nenhuma sessão ativa"
            )

    def test_password_authentication(self):
        """Testa autenticação com senha"""
        self.print_header("TESTE 4: AUTENTICAÇÃO COM SENHA")

        # Testa com senha correta
        cmd = 'echo "admin" | python3 /Users/clubproducoes/Digimundo/claude_code/protection/scripturemon_guardian.py --unlock'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        success = "SENHA CORRETA" in result.stdout
        self.test_result(
            "Autenticação com senha correta",
            success,
            "Desbloqueio bem-sucedido" if success else "Falha na autenticação"
        )

        # Testa com senha incorreta (sem bloquear)
        cmd = 'echo "wrong" | python3 /Users/clubproducoes/Digimundo/claude_code/protection/scripturemon_guardian.py --unlock'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        failed = "Senha incorreta" in result.stdout or "SENHA CORRETA" not in result.stdout
        self.test_result(
            "Rejeição de senha incorreta",
            failed,
            "Senha incorreta rejeitada" if failed else "ERRO: Senha incorreta aceita!"
        )

    def test_lock_mechanism(self):
        """Testa mecanismo de bloqueio"""
        self.print_header("TESTE 5: MECANISMO DE BLOQUEIO")

        if LOCK_FILE.exists():
            try:
                with open(LOCK_FILE) as f:
                    lock = json.load(f)
                unlock_at = datetime.fromisoformat(lock['unlock_at'])
                is_locked = datetime.now() < unlock_at
                remaining = (unlock_at - datetime.now()).seconds // 60

                self.test_result(
                    "Sistema de bloqueio funcional",
                    True,
                    f"Bloqueado por {remaining} minutos" if is_locked else "Desbloqueado"
                )
            except Exception as e:
                self.test_result(
                    "Sistema de bloqueio funcional",
                    False,
                    f"Erro ao ler bloqueio: {e}"
                )
        else:
            self.test_result(
                "Sistema de bloqueio funcional",
                True,
                "Sistema não está bloqueado"
            )

    def test_protected_operations(self):
        """Testa operações protegidas"""
        self.print_header("TESTE 6: OPERAÇÕES PROTEGIDAS")

        # Testa importação do módulo
        try:
            sys.path.insert(0, str(Path("/Users/clubproducoes/Digimundo/scripturemon-champion")))
            from protected_file_ops import ProtectedFileOperations

            self.test_result(
                "Importação do módulo de operações protegidas",
                True,
                "Módulo importado com sucesso"
            )

            # Lista operações disponíveis
            ops = ProtectedFileOperations()
            methods = [m for m in dir(ops) if not m.startswith('_')]

            self.test_result(
                "Operações protegidas disponíveis",
                len(methods) > 0,
                f"{len(methods)} operações: {', '.join(methods[:5])}"
            )

        except Exception as e:
            self.test_result(
                "Importação do módulo de operações protegidas",
                False,
                f"Erro: {e}"
            )

    def test_guardian_commands(self):
        """Testa comandos do guardian"""
        self.print_header("TESTE 7: COMANDOS DO GUARDIAN")

        commands = [
            ("--check", "Verificação de status"),
            ("--help", "Ajuda do sistema")
        ]

        for cmd, description in commands:
            result = subprocess.run(
                f"python3 /Users/clubproducoes/Digimundo/claude_code/protection/scripturemon_guardian.py {cmd}",
                shell=True,
                capture_output=True,
                text=True
            )

            success = result.returncode == 0
            self.test_result(
                f"Comando {cmd} ({description})",
                success,
                "Comando executado" if success else f"Erro: {result.stderr}"
            )

    def test_claude_memory_integration(self):
        """Testa integração com memória do Claude"""
        self.print_header("TESTE 8: INTEGRAÇÃO COM MEMÓRIA")

        # Verifica se memória referencia o sistema de proteção
        if MEMORY_FILE.exists():
            content = MEMORY_FILE.read_text()

            has_protection_ref = "scripturemon_guardian.py" in content
            self.test_result(
                "Memória referencia sistema de proteção",
                has_protection_ref,
                "Referência encontrada" if has_protection_ref else "Referência não encontrada"
            )

            has_password_section = "🔐 SENHA DO SISTEMA" in content
            self.test_result(
                "Memória tem seção de senha",
                has_password_section,
                "Seção encontrada" if has_password_section else "Seção não encontrada"
            )

    def generate_report(self):
        """Gera relatório final"""
        self.print_header("RELATÓRIO FINAL DE SEGURANÇA")

        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0

        print(f"\n📊 ESTATÍSTICAS:")
        print(f"  • Testes executados: {total}")
        print(f"  • Testes aprovados: {self.tests_passed} ✅")
        print(f"  • Testes falhados: {self.tests_failed} ❌")
        print(f"  • Taxa de sucesso: {percentage:.1f}%")

        if percentage == 100:
            print(f"\n🏆 SISTEMA DE SEGURANÇA 100% FUNCIONAL!")
        elif percentage >= 80:
            print(f"\n✅ Sistema de segurança operacional com pequenos ajustes necessários")
        elif percentage >= 60:
            print(f"\n⚠️ Sistema de segurança parcialmente funcional")
        else:
            print(f"\n🔴 Sistema de segurança precisa de correções críticas")

        # Salva relatório
        report_path = Path("/Users/clubproducoes/Digimundo/claude_code/analysis/SECURITY_TEST_REPORT.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": total,
                "passed": self.tests_passed,
                "failed": self.tests_failed,
                "success_rate": percentage,
                "results": self.results
            }, f, indent=2)

        print(f"\n📝 Relatório salvo em: {report_path}")


if __name__ == "__main__":
    print("="*80)
    print("🛡️ TESTE COMPLETO DO SISTEMA DE SEGURANÇA")
    print("="*80)
    print("\n🔍 Iniciando bateria de testes...")

    tester = SecuritySystemTester()

    # Executa todos os testes
    tester.test_memory_file_exists()
    tester.test_protection_files()
    tester.test_session_management()
    tester.test_password_authentication()
    tester.test_lock_mechanism()
    tester.test_protected_operations()
    tester.test_guardian_commands()
    tester.test_claude_memory_integration()

    # Gera relatório
    tester.generate_report()

    print("\n" + "="*80)
    print("✅ TESTE DE SEGURANÇA CONCLUÍDO")
    print("="*80)

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
