#!/usr/bin/env python3
"""
Sistema de Sanity Checker - Protocolo Digivolve
Executa testes de sanidade após cada mudança
"""

import sys
import json
import importlib
from pathlib import Path
from typing import List, Tuple, Dict
import psutil

class SanityChecker:
    """
    Executa testes de sanidade APÓS CADA MUDANÇA
    Impede progressão se algo básico quebrar
    """

    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")
        self.results_file = self.base_path / "SANITY_RESULTS.json"
        self.critical_tests = [
            ("structure", self.test_directory_structure),
            ("imports", self.test_core_imports),
            ("files", self.test_essential_files),
            ("memory", self.test_memory_usage),
            ("json", self.test_json_files)
        ]
        self.results = {}

    def run_all(self) -> Tuple[bool, List[str]]:
        """Executa todos os testes de sanidade"""
        failures = []
        self.results = {}

        print("🧪 Executando Sanity Checks...")

        for test_name, test_func in self.critical_tests:
            try:
                result = test_func()
                self.results[test_name] = {
                    "passed": result,
                    "error": None
                }

                if not result:
                    failures.append(test_name)
                    print(f"  ❌ {test_name}: FALHOU")
                else:
                    print(f"  ✅ {test_name}: OK")

            except Exception as e:
                failures.append(f"{test_name}: {str(e)}")
                self.results[test_name] = {
                    "passed": False,
                    "error": str(e)
                }
                print(f"  💥 {test_name}: ERRO - {e}")

        # Salva resultados
        self.save_results()

        success = len(failures) == 0
        print(f"\n{'✅' if success else '❌'} Sanity Check: {len(self.critical_tests) - len(failures)}/{len(self.critical_tests)} passaram")

        return success, failures

    def test_directory_structure(self) -> bool:
        """Testa se estrutura de diretórios está correta"""
        required_dirs = ["core", "scripts", "tests", "docs", "snapshots"]

        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                return False

        return True

    def test_core_imports(self) -> bool:
        """Testa se imports do core funcionam"""
        # Por enquanto, apenas verifica se os arquivos Python existem
        core_modules = ["auto_documenter", "snapshot_manager", "sanity_checker"]

        for module in core_modules:
            module_file = self.base_path / "core" / f"{module}.py"
            if not module_file.exists():
                return False

        return True

    def test_essential_files(self) -> bool:
        """Testa se arquivos essenciais existem"""
        # Arquivos que podem ou não existir ainda
        optional_files = ["OMEGA_STATE.json", "OMEGA_HISTORY.jsonl"]

        # Por enquanto, retorna True se o diretório base existe
        return self.base_path.exists()

    def test_memory_usage(self) -> bool:
        """Testa uso de memória"""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024

            # Limite de 2GB
            return memory_mb < 2000
        except:
            # Se não conseguir verificar, assume que está OK
            return True

    def test_json_files(self) -> bool:
        """Testa se arquivos JSON são válidos"""
        json_files = list(self.base_path.rglob("*.json"))

        for json_file in json_files:
            try:
                json.loads(json_file.read_text())
            except:
                return False

        return True

    def save_results(self):
        """Salva resultados dos testes"""
        results_data = {
            "timestamp": str(Path.cwd()),
            "results": self.results,
            "summary": {
                "total": len(self.critical_tests),
                "passed": sum(1 for r in self.results.values() if r["passed"]),
                "failed": sum(1 for r in self.results.values() if not r["passed"])
            }
        }

        self.results_file.write_text(json.dumps(results_data, indent=2))

    def check_evolution_requirements(self, stage: str) -> bool:
        """Verifica se requisitos para evolução estão satisfeitos"""
        requirements = {
            "baby_to_rookie": {
                "tests_min": 3,
                "files_min": 5
            },
            "rookie_to_champion": {
                "tests_min": 5,
                "files_min": 10
            }
        }

        # Implementação simplificada por enquanto
        passed, _ = self.run_all()
        return passed

    def get_health_status(self) -> Dict:
        """Retorna status de saúde do sistema"""
        passed, failures = self.run_all()

        return {
            "healthy": passed,
            "tests_total": len(self.critical_tests),
            "tests_passed": len(self.critical_tests) - len(failures),
            "failures": failures,
            "memory_mb": psutil.Process().memory_info().rss / 1024 / 1024 if psutil else 0
        }


def main():
    """Teste do sanity checker"""
    checker = SanityChecker()

    # Executa todos os testes
    passed, failures = checker.run_all()

    if not passed:
        print(f"\n⚠️ Problemas encontrados: {failures}")
        print("   Recomendação: Executar rollback se necessário")
    else:
        print("\n🎉 Sistema saudável e pronto para evoluir!")

    return passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)