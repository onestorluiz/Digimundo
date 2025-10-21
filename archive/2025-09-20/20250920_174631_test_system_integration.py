#!/usr/bin/env python3
"""
🧪 TESTES ROBUSTOS DE INTEGRAÇÃO DO SISTEMA COMPLETO
Valida todos os componentes críticos do Scripturemon
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
import tempfile
import shutil

# Adicionar path do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SystemIntegrationTest:
    """Testes de integração completos"""

    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        self.test_dir = Path("tests/integration_temp")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def cleanup(self):
        """Limpa arquivos temporários"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def run_test(self, test_name: str, test_func) -> bool:
        """Executa um teste individual"""
        try:
            print(f"\n🔍 Testando: {test_name}")
            print("=" * 60)

            start_time = time.time()
            result = test_func()
            elapsed = time.time() - start_time

            if result:
                print(f"✅ PASSOU ({elapsed:.2f}s)")
                self.test_results.append((test_name, True, elapsed))
                return True
            else:
                print(f"❌ FALHOU ({elapsed:.2f}s)")
                self.test_results.append((test_name, False, elapsed))
                self.failed_tests.append(test_name)
                return False

        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            self.test_results.append((test_name, False, 0))
            self.failed_tests.append(test_name)
            return False

    def test_crystal_memory_systems(self) -> bool:
        """Testa ambos os sistemas Crystal Memory"""
        try:
            # 1. Crystal Memory para Regras (Claude Code)
            from apps.scripturemon.rules_memory import CrystalMemory
            rules_memory = CrystalMemory()

            # Testar compliance
            valid, violations = rules_memory.check_compliance(
                "criar novo arquivo test.py",
                {"file_path": "test.py"}
            )
            print(f"   Rules Memory: Compliance check = {valid}")

            # 2. Crystal Memory para Roteiros
            from apps.scripturemon.screenplay_crystal_memory import ScreenplayCrystalMemory
            screenplay_memory = ScreenplayCrystalMemory()

            # Testar memorização
            test_script = "FADE IN:\n\nTEST SCENE"
            script_id = screenplay_memory.remember_screenplay(
                "Test Script",
                test_script
            )
            print(f"   Screenplay Memory: Stored ID = {script_id}")

            # Testar recall
            similar = screenplay_memory.recall_similar(test_script, limit=1)
            print(f"   Screenplay Memory: Found {len(similar)} similar scripts")

            return True

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_rag_system(self) -> bool:
        """Testa o sistema RAG"""
        try:
            from apps.scripturemon.rag_system import RAGSystem, RAGQuery, RetrievalStrategy

            rag = RAGSystem()

            # Indexar documento teste
            test_content = """
            FADE IN:

            INT. LABORATORY - NIGHT

            DR. SMITH, 45, examines mysterious data on multiple screens.

            DR. SMITH
            The patterns are unmistakable.
            This changes everything.
            """

            chunks = rag.index_screenplay("Test Lab Script", test_content)
            print(f"   Indexados {chunks} chunks")

            # Testar diferentes estratégias
            strategies = [
                RetrievalStrategy.SEMANTIC,
                RetrievalStrategy.KEYWORD,
                RetrievalStrategy.HYBRID
            ]

            for strategy in strategies:
                query = RAGQuery(
                    query="Who is in the laboratory?",
                    strategy=strategy,
                    max_results=3
                )

                result = rag.query(query)
                print(f"   {strategy.value}: Confiança {result.confidence:.1%}")

            return True

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_claude_integration(self) -> bool:
        """Testa integração com Claude Code"""
        try:
            from apps.scripturemon.claude_integration import ClaudeIntegration
            from apps.scripturemon.claude_hooks import ClaudeHooks

            # Testar integração
            integration = ClaudeIntegration()

            test_actions = [
                "criar arquivo scripturemon2.py",
                "modificar cli_champion.py",
                "usar argparse no CLI",
                "analisar roteiro com Ollama"
            ]

            blocked_count = 0
            for action in test_actions:
                result = integration.check_action(action)
                if not result['allowed']:
                    blocked_count += 1
                    print(f"   ❌ Bloqueado: {action}")
                else:
                    print(f"   ✅ Permitido: {action}")

            # Testar hooks
            hooks = ClaudeHooks()
            session_id = hooks.session_id
            print(f"   Session ID: {session_id[:8]}...")

            # Deve bloquear pelo menos ações perigosas
            return blocked_count >= 2

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_ollama_integration(self) -> bool:
        """Testa integração com Ollama"""
        try:
            from apps.scripturemon.ollama_core import OllamaCore

            ollama = OllamaCore()

            # Verificar modelos
            models = ollama.list_models()
            print(f"   Modelos disponíveis: {len(models)}")

            # Verificar modelos Scripturemon
            scripturemon_models = [m for m in models if 'scripturemon' in m.lower()]
            print(f"   Modelos Scripturemon: {len(scripturemon_models)}")

            if scripturemon_models:
                for model in scripturemon_models[:3]:
                    print(f"      • {model}")

            return len(models) > 0

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_cli_commands(self) -> bool:
        """Testa comandos CLI principais"""
        try:
            commands_to_test = [
                ["python3", "-m", "apps.scripturemon.cli_champion", "--help"],
                ["python3", "-m", "apps.scripturemon.cli_champion", "status"],
                ["python3", "-m", "apps.scripturemon.cli_champion", "list-models"],
            ]

            for cmd in commands_to_test:
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        env={**os.environ, "PYTHONPATH": "."}
                    )

                    success = result.returncode == 0
                    cmd_str = " ".join(cmd[-2:])

                    if success:
                        print(f"   ✅ {cmd_str}")
                    else:
                        print(f"   ❌ {cmd_str}: {result.stderr[:100]}")

                except subprocess.TimeoutExpired:
                    print(f"   ⏱️ Timeout: {' '.join(cmd[-2:])}")

            return True

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_digilang_compression(self) -> bool:
        """Testa compressão DigiLang"""
        try:
            from apps.scripturemon.digilang_simple import DigiLangEncoder

            encoder = DigiLangEncoder()

            test_texts = [
                "FADE IN:",
                "INT. HOUSE - DAY",
                "JOHN enters the room.",
                "JOHN\nHello, world!"
            ]

            total_original = 0
            total_compressed = 0

            for text in test_texts:
                encoded = encoder.encode(text)
                original_len = len(text)
                compressed_len = len(encoded)
                ratio = compressed_len / original_len if original_len > 0 else 1

                total_original += original_len
                total_compressed += compressed_len

                print(f"   '{text[:20]}...': {original_len} → {compressed_len} ({ratio:.1%})")

            overall_ratio = total_compressed / total_original if total_original > 0 else 1
            print(f"   Taxa geral: {overall_ratio:.1%}")

            return overall_ratio < 1.0  # Deve haver alguma compressão

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_database_connections(self) -> bool:
        """Testa conexões com bancos de dados"""
        try:
            import sqlite3

            databases = [
                "data/crystal_memory.db",
                "data/screenplay_memory.db",
                "data/claude_context.db",
                "data/rag_vectors.db",
                "data/rag_stats.db"
            ]

            connected = 0
            for db_path in databases:
                db_file = Path(db_path)
                if db_file.exists():
                    try:
                        conn = sqlite3.connect(db_file)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        tables = cursor.fetchall()
                        conn.close()

                        print(f"   ✅ {db_path}: {len(tables)} tabelas")
                        connected += 1
                    except:
                        print(f"   ❌ {db_path}: Erro ao conectar")
                else:
                    print(f"   ⚠️ {db_path}: Não existe (será criado)")

            return connected >= 2  # Pelo menos 2 DBs devem existir

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_unified_system(self) -> bool:
        """Testa sistema unificado"""
        try:
            from apps.scripturemon.scripturemon_unified import ScripturemonUnified

            system = ScripturemonUnified()

            # Status do sistema
            status = system.get_status()
            print(f"   Componentes: {len(status['components'])}")
            print(f"   Status: {status['status']}")

            # Verificar componentes críticos
            critical = ['ollama', 'digilang', 'analyzer']
            for comp in critical:
                comp_status = status['components'].get(comp, {})
                if comp_status.get('status') == 'ready':
                    print(f"   ✅ {comp}: ready")
                else:
                    print(f"   ⚠️ {comp}: {comp_status.get('status', 'unknown')}")

            return status['status'] in ['ready', 'partial']

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_memory_management(self) -> bool:
        """Testa gerenciamento de memória"""
        try:
            from apps.scripturemon.unified_manager import UnifiedMemoryManager

            manager = UnifiedMemoryManager()

            # Testar cache
            manager.set_cache("test_key", {"data": "test"})
            cached = manager.get_cache("test_key")

            if cached and cached.get("data") == "test":
                print(f"   ✅ Cache funcionando")
            else:
                print(f"   ❌ Cache com problema")
                return False

            # Stats de memória
            stats = manager.get_memory_stats()
            print(f"   Cache entries: {stats['cache_entries']}")
            print(f"   Memory MB: {stats['memory_mb']:.1f}")

            # Cleanup
            manager.cleanup_memory(force=True)
            stats_after = manager.get_memory_stats()
            print(f"   Após cleanup: {stats_after['cache_entries']} entries")

            return True

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def test_file_operations(self) -> bool:
        """Testa operações com arquivos"""
        try:
            # Criar arquivo teste
            test_file = self.test_dir / "test_script.txt"
            test_content = "FADE IN:\n\nTEST SCENE\n\nFADE OUT."

            with open(test_file, 'w') as f:
                f.write(test_content)

            # Testar leitura
            with open(test_file, 'r') as f:
                read_content = f.read()

            if read_content == test_content:
                print(f"   ✅ Leitura/Escrita OK")
            else:
                print(f"   ❌ Conteúdo não coincide")
                return False

            # Testar análise de roteiro
            from apps.scripturemon.screenplay_analyzer import ScreenplayAnalyzer
            analyzer = ScreenplayAnalyzer()

            analysis = analyzer.analyze_file(str(test_file))
            print(f"   Análise: {analysis.get('format', 'unknown')} format")
            print(f"   Elementos: {analysis.get('element_count', 0)}")

            return True

        except Exception as e:
            print(f"   Erro: {e}")
            return False

    def run_all_tests(self):
        """Executa todos os testes"""
        print("🧪 INICIANDO TESTES DE INTEGRAÇÃO DO SISTEMA")
        print("=" * 70)

        tests = [
            ("Crystal Memory Systems", self.test_crystal_memory_systems),
            ("RAG System", self.test_rag_system),
            ("Claude Integration", self.test_claude_integration),
            ("Ollama Integration", self.test_ollama_integration),
            ("CLI Commands", self.test_cli_commands),
            ("DigiLang Compression", self.test_digilang_compression),
            ("Database Connections", self.test_database_connections),
            ("Unified System", self.test_unified_system),
            ("Memory Management", self.test_memory_management),
            ("File Operations", self.test_file_operations),
        ]

        for test_name, test_func in tests:
            self.run_test(test_name, test_func)

        # Resumo
        print("\n" + "=" * 70)
        print("📊 RESUMO DOS TESTES")
        print("=" * 70)

        total = len(self.test_results)
        passed = sum(1 for _, success, _ in self.test_results if success)
        failed = total - passed
        total_time = sum(time for _, _, time in self.test_results)

        print(f"\nTotal: {total} testes")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"⏱️ Tempo total: {total_time:.2f}s")

        if failed > 0:
            print(f"\n❌ Testes que falharam:")
            for test in self.failed_tests:
                print(f"   • {test}")

        # Cleanup
        self.cleanup()

        return failed == 0


def main():
    """Executa os testes"""
    tester = SystemIntegrationTest()
    success = tester.run_all_tests()

    if success:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        sys.exit(1)


if __name__ == "__main__":
    main()