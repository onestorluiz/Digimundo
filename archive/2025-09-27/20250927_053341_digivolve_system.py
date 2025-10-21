#!/usr/bin/env python3
"""
Sistema Principal de Digivolução OMEGA-ASCENT
Controla toda a evolução do sistema de forma autônoma
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Importa sistemas de proteção
sys.path.append('/Users/clubproducoes/Digimundo/scripturemon-Omega')
from core.auto_documenter import AutoDocumenter
from core.snapshot_manager import SnapshotManager
from core.sanity_checker import SanityChecker


class DigivolveSystem:
    """
    Sistema principal de evolução controlada
    Gerencia todo o processo de digivolução do OMEGA-ASCENT
    """

    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")
        self.documenter = AutoDocumenter()
        self.snapshot = SnapshotManager()
        self.sanity = SanityChecker()

        # Estágios de evolução
        self.stages = {
            "baby": {"power": 100, "quality": 0.70, "harmony": 0.40},
            "in_training": {"power": 300, "quality": 0.75, "harmony": 0.50},
            "rookie": {"power": 500, "quality": 0.82, "harmony": 0.60},
            "champion": {"power": 1500, "quality": 0.86, "harmony": 0.75},
            "ultimate": {"power": 5000, "quality": 0.90, "harmony": 0.85},
            "mega": {"power": 10000, "quality": 0.94, "harmony": 0.95},
            "mega_plus": {"power": 9001, "quality": 0.95, "harmony": 1.00}
        }

        # Requisitos para evolução
        self.evolution_requirements = {
            "baby_to_in_training": {"files": 5, "tests": 3, "features": 2},
            "in_training_to_rookie": {"files": 10, "tests": 5, "features": 4},
            "rookie_to_champion": {"files": 20, "tests": 10, "features": 8},
            "champion_to_ultimate": {"files": 40, "tests": 20, "features": 15},
            "ultimate_to_mega": {"files": 60, "tests": 30, "features": 20},
            "mega_to_mega_plus": {"files": 80, "tests": 40, "features": 25}
        }

        self.current_stage = self.documenter.current_state.get("stage", "baby")
        self.phase = self.documenter.current_state.get("phase", 0)

    def check_evolution_ready(self) -> Tuple[bool, Dict]:
        """Verifica se está pronto para evoluir"""
        stage_list = list(self.stages.keys())
        current_idx = stage_list.index(self.current_stage)

        if current_idx >= len(stage_list) - 1:
            return False, {"reason": "Already at maximum evolution"}

        next_stage = stage_list[current_idx + 1]
        req_key = f"{self.current_stage}_to_{next_stage}"

        if req_key not in self.evolution_requirements:
            return False, {"reason": "No evolution path defined"}

        requirements = self.evolution_requirements[req_key]

        # Verifica requisitos
        files_count = len(self.documenter.current_state.get("files", {}))
        tests_passing = sum(1 for t in self.documenter.current_state.get("tests_passing", {}).values()
                           if t.get("passed"))
        features_working = len(self.documenter.current_state.get("working_features", []))

        checks = {
            "files": files_count >= requirements["files"],
            "tests": tests_passing >= requirements["tests"],
            "features": features_working >= requirements["features"],
            "sanity": self.sanity.run_all()[0]
        }

        ready = all(checks.values())

        status = {
            "ready": ready,
            "next_stage": next_stage,
            "requirements": requirements,
            "current": {
                "files": files_count,
                "tests": tests_passing,
                "features": features_working
            },
            "checks": checks
        }

        return ready, status

    def evolve(self) -> bool:
        """Executa evolução para próximo estágio"""
        ready, status = self.check_evolution_ready()

        if not ready:
            print(f"❌ Não pronto para evoluir: {status}")
            return False

        next_stage = status["next_stage"]
        print(f"\n🌟 INICIANDO DIGIVOLUÇÃO: {self.current_stage} → {next_stage}")

        # Cria snapshot antes de evoluir
        snapshot_id = self.snapshot.create_snapshot(
            phase=self.phase + 1,
            stage=self.current_stage,
            description=f"Antes de evoluir para {next_stage}"
        )

        try:
            # Atualiza métricas
            new_metrics = self.stages[next_stage]
            self.documenter.update_metrics(
                power_level=new_metrics["power"],
                quality_score=new_metrics["quality"],
                harmony=new_metrics["harmony"]
            )

            # Marca evolução
            self.documenter.evolve_stage(next_stage)
            self.current_stage = next_stage
            self.phase += 1

            # Marca snapshot como bem-sucedido
            self.snapshot.mark_successful(snapshot_id)

            print(f"✅ DIGIVOLUÇÃO COMPLETA! Agora em estágio: {next_stage}")
            print(f"   ⚡ Power Level: {new_metrics['power']}")
            print(f"   📊 Quality: {new_metrics['quality']:.2f}")
            print(f"   🎯 Harmony: {new_metrics['harmony']:.2f}")

            return True

        except Exception as e:
            print(f"❌ Erro durante evolução: {e}")
            print("   🔄 Executando rollback...")
            self.snapshot.rollback(snapshot_id)
            return False

    def auto_evolve(self):
        """Tenta evoluir automaticamente quando requisitos são atendidos"""
        while self.current_stage != "mega_plus":
            ready, status = self.check_evolution_ready()

            if ready:
                print(f"\n🎉 Requisitos atendidos para evolução!")
                if self.evolve():
                    time.sleep(2)  # Pausa dramática
                else:
                    break
            else:
                print(f"\n⏳ Aguardando requisitos para evoluir para {status.get('next_stage', 'unknown')}")
                print(f"   Files: {status['current']['files']}/{status['requirements']['files']}")
                print(f"   Tests: {status['current']['tests']}/{status['requirements']['tests']}")
                print(f"   Features: {status['current']['features']}/{status['requirements']['features']}")
                break

    def get_status(self) -> str:
        """Retorna status completo do sistema"""
        return self.documenter.get_summary()

    def run_phase_0_preparation(self):
        """Executa Fase 0 - Preparação do sistema"""
        print("\n" + "="*60)
        print("🎮 FASE 0: PREPARAÇÃO DO SISTEMA DIGIVOLVE")
        print("="*60)

        tasks = [
            ("Estrutura de diretórios", self._create_directory_structure),
            ("Sistemas de proteção", self._verify_protection_systems),
            ("Configurações iniciais", self._create_initial_configs),
            ("Validação do ambiente", self._validate_environment)
        ]

        for task_name, task_func in tasks:
            print(f"\n📌 {task_name}...")
            try:
                result = task_func()
                if result:
                    print(f"   ✅ {task_name} completo")
                    self.documenter.mark_feature(task_name.lower().replace(" ", "_"), "working")
                else:
                    print(f"   ⚠️ {task_name} com avisos")
            except Exception as e:
                print(f"   ❌ {task_name} falhou: {e}")
                self.documenter.mark_feature(task_name.lower().replace(" ", "_"), "broken")

        # Verifica sanidade final
        passed, _ = self.sanity.run_all()
        if passed:
            print("\n✅ FASE 0 COMPLETA - Sistema pronto para Fase 1")
            self.documenter.create_checkpoint("Fase 0 completa")
            return True
        else:
            print("\n❌ FASE 0 com problemas - verificar logs")
            return False

    def _create_directory_structure(self) -> bool:
        """Cria estrutura completa de diretórios"""
        directories = [
            "scripturemon/core",
            "scripturemon/retrieval",
            "scripturemon/analysis",
            "scripturemon/validation",
            "scripturemon/specialists",
            "scripturemon/evaluation",
            "scripturemon/interface",
            "scripturemon/utils",
            "config",
            "data/lore",
            "tests/unit",
            "tests/integration",
            "tests/harmony"
        ]

        for dir_path in directories:
            (self.base_path / dir_path).mkdir(parents=True, exist_ok=True)

        return True

    def _verify_protection_systems(self) -> bool:
        """Verifica se sistemas de proteção estão funcionando"""
        systems_ok = True

        # Verifica auto-documentador
        if self.documenter:
            self.documenter.track_file(__file__, "verified")
        else:
            systems_ok = False

        # Verifica snapshot manager
        if not self.snapshot.snapshots_dir.exists():
            systems_ok = False

        # Verifica sanity checker
        sanity_ok, _ = self.sanity.run_all()
        systems_ok = systems_ok and sanity_ok

        return systems_ok

    def _create_initial_configs(self) -> bool:
        """Cria arquivos de configuração iniciais"""
        config_dir = self.base_path / "config"
        config_dir.mkdir(exist_ok=True)

        # Configuração padrão
        defaults = {
            "engine": "omega",
            "mode": "development",
            "specialists": ["logline", "theme", "pacing", "structure", "market"],
            "hierarchical": {
                "enabled": True,
                "levels": ["beat", "scene", "act", "global"]
            }
        }

        (config_dir / "defaults.json").write_text(json.dumps(defaults, indent=2))
        self.documenter.track_file(str(config_dir / "defaults.json"), "created")

        return True

    def _validate_environment(self) -> bool:
        """Valida ambiente de execução"""
        validations = []

        # Python version
        validations.append(sys.version_info >= (3, 10))

        # Diretório base existe
        validations.append(self.base_path.exists())

        # Permissões de escrita
        test_file = self.base_path / ".write_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            validations.append(True)
        except:
            validations.append(False)

        return all(validations)


def main():
    """Execução principal do sistema Digivolve"""
    print("""
╔════════════════════════════════════════════════════════════╗
║          🌟 SISTEMA DIGIVOLVE OMEGA-ASCENT 🌟             ║
║                    Versão 1.0.0                           ║
╚════════════════════════════════════════════════════════════╝
    """)

    system = DigivolveSystem()

    # Mostra status inicial
    print(system.get_status())

    # Executa Fase 0
    if system.run_phase_0_preparation():
        print("\n🚀 Sistema Digivolve inicializado com sucesso!")

        # Verifica se pode evoluir
        system.auto_evolve()

        # Status final
        print("\n" + system.get_status())
    else:
        print("\n❌ Falha na inicialização do Sistema Digivolve")

    return system


if __name__ == "__main__":
    system = main()