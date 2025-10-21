#!/usr/bin/env python3
"""
Fase 2: Extended Core
Copia arquivos estendidos e configura sistemas avançados
"""

import os
import sys
import shutil
from pathlib import Path

# Adiciona ao path para importar módulos core
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.auto_documenter import AutoDocumenter
from core.sanity_checker import SanityChecker
from core.snapshot_manager import SnapshotManager

def copy_extended_files():
    """Copia arquivos estendidos das rodadas"""
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")
    rounds_base = Path("/Users/clubproducoes/Digimundo/Novos_arquivos")

    doc = AutoDocumenter()

    # Lista de arquivos estendidos para copiar
    extended_files = [
        # Rodada 8 - Coverage Systems
        ("rodada_8/scripturemon-omega-ascent-theta-plus/scripturemon/coverage_tracker.py", "analysis/coverage_tracker.py"),
        ("rodada_8/scripturemon-omega-ascent-theta-plus/scripturemon/spot_checker_omega.py", "validation/spot_checker_omega.py"),

        # Rodada 9 - Enhanced Systems
        ("rodada_9/scripturemon-omega-ascent-iota-plus/scripturemon/arc_extractor.py", "narrative/arc_extractor.py"),
        ("rodada_9/scripturemon-omega-ascent-iota-plus/scripturemon/motif_tracker.py", "narrative/motif_tracker.py"),

        # Rodada 10 - Advanced Features
        ("rodada_10/scripturemon-omega-ascent-homega-plus/scripturemon/locality_gate.py", "optimization/locality_gate.py"),
        ("rodada_10/scripturemon-omega-ascent-homega-plus/scripturemon/kmedoids.py", "optimization/kmedoids.py"),

        # Rodada 11 - Final Systems
        ("rodada_11/scripturemon-omega-ascent-homega-plus/scripturemon/citation_validator.py", "validation/citation_validator.py"),
        ("rodada_11/scripturemon-omega-ascent-homega-plus/scripturemon/router_motifs.py", "routing/router_motifs.py"),
    ]

    copied = 0
    failed = 0

    for source_rel, dest_rel in extended_files:
        source = rounds_base / source_rel
        dest = base_path / dest_rel

        # Cria diretório de destino
        dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            if source.exists():
                shutil.copy2(source, dest)
                doc.track_file(str(dest), "added")
                print(f"✅ Copiado: {dest_rel}")
                copied += 1
            else:
                print(f"⚠️  Arquivo não encontrado: {source_rel}")
                failed += 1
        except Exception as e:
            print(f"❌ Erro ao copiar {dest_rel}: {e}")
            failed += 1

    return copied, failed

def setup_extended_systems():
    """Configura sistemas avançados"""
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")

    # Cria estrutura de diretórios estendidos
    dirs = [
        "analysis/reports",
        "validation/logs",
        "narrative/arcs",
        "optimization/benchmarks",
        "routing/configs"
    ]

    for d in dirs:
        dir_path = base_path / d
        dir_path.mkdir(parents=True, exist_ok=True)

    # Cria configuração estendida
    config_extended = base_path / "config" / "extended.yaml"
    config_extended.parent.mkdir(exist_ok=True)

    config_content = """# Configuração Estendida OMEGA-ASCENT
version: 4.0.0
stage: extended_core

features:
  coverage_tracking: true
  spot_checking: true
  arc_extraction: true
  motif_tracking: true
  locality_gates: true
  kmedoids_clustering: true
  citation_validation: true
  motif_routing: true

optimization:
  cache_enabled: true
  parallel_processing: true
  memory_limit_gb: 4

validation:
  strict_mode: true
  auto_correction: true
  error_threshold: 0.1
"""

    config_extended.write_text(config_content)

    print("✅ Sistemas estendidos configurados")
    return True

def main():
    print("=" * 60)
    print("FASE 2: EXTENDED CORE")
    print("=" * 60)

    # Cria snapshot antes de iniciar
    snapshot = SnapshotManager()
    snap_id = snapshot.create_snapshot(2, "phase2_start", "Iniciando Fase 2")
    print(f"📸 Snapshot criado: {snap_id}")

    # Copia arquivos estendidos
    print("\n📂 Copiando arquivos estendidos...")
    copied, failed = copy_extended_files()

    # Configura sistemas
    print("\n⚙️  Configurando sistemas avançados...")
    setup_extended_systems()

    # Executa sanity check
    print("\n🔍 Executando validação...")
    checker = SanityChecker()
    valid, errors = checker.run_all()

    if valid:
        print("✅ Validação passou!")
    else:
        print("⚠️  Erros encontrados:")
        for error in errors:
            print(f"  - {error}")

    # Atualiza documentação
    doc = AutoDocumenter()
    doc.evolve_stage("in_training")

    print("\n" + "=" * 60)
    print(f"FASE 2 CONCLUÍDA")
    print(f"  Arquivos copiados: {copied}")
    print(f"  Arquivos falhados: {failed}")
    print(f"  Validação: {'✅' if valid else '⚠️'}")
    print(f"  Stage atual: in_training")
    print("=" * 60)

    return 0 if valid else 1

if __name__ == "__main__":
    sys.exit(main())