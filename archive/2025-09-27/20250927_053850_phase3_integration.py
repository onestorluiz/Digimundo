#!/usr/bin/env python3
"""
Fase 3: Integration
Integra componentes principais de várias rodadas
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

def integrate_components():
    """Integra componentes de múltiplas rodadas"""
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")
    rounds_base = Path("/Users/clubproducoes/Digimundo/Novos_arquivos")
    doc = AutoDocumenter()

    # Integração por categoria
    integrations = {
        "beat_systems": [
            ("rodada_6/scripturemon-omega-ascent-hplus/scripturemon/beats.py", "beats/beats_dynamic.py"),
            ("rodada_7/scripturemon-omega-ascent-hpp/scripturemon/beats.py", "beats/beats_enhanced.py"),
        ],
        "hierarchical": [
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/hier_rag.py", "hierarchy/hier_rag.py"),
            ("rodada_6/scripturemon-omega-ascent-hplus/scripturemon/hier_plus.py", "hierarchy/hier_plus.py"),
            ("rodada_11/scripturemon-omega-ascent-homega-plus/scripturemon/hier_omega_plus.py", "hierarchy/hier_omega_plus.py"),
        ],
        "evidence_systems": [
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/evidence_gate.py", "evidence/evidence_gate.py"),
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/evidence_policy.py", "evidence/evidence_policy.py"),
        ],
        "memory_systems": [
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/memory_store.py", "memory/memory_store.py"),
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/cache.py", "memory/cache.py"),
        ],
        "validation": [
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/validators.py", "validation/validators.py"),
            ("rodada_5/scripturemon-omega-ascent-h/scripturemon/consistency.py", "validation/consistency.py"),
        ]
    }

    copied = 0
    failed = 0

    for category, files in integrations.items():
        print(f"\n📦 Integrando {category}...")

        for source_rel, dest_rel in files:
            source = rounds_base / source_rel
            dest = base_path / dest_rel

            # Cria diretório de destino
            dest.parent.mkdir(parents=True, exist_ok=True)

            try:
                if source.exists():
                    shutil.copy2(source, dest)
                    doc.track_file(str(dest), "integrated")
                    print(f"  ✅ {dest_rel}")
                    copied += 1
                else:
                    print(f"  ⚠️  Não encontrado: {source_rel}")
                    failed += 1
            except Exception as e:
                print(f"  ❌ Erro: {e}")
                failed += 1

    return copied, failed

def create_integration_config():
    """Cria configuração de integração"""
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")

    config_path = base_path / "config" / "integration.yaml"
    config_content = """# Configuração de Integração OMEGA-ASCENT
version: 4.0.0
stage: integration

components:
  beats:
    enabled: true
    dynamic: true
    enhanced: true

  hierarchy:
    enabled: true
    levels: [hier_rag, hier_plus, hier_omega_plus]
    default: hier_omega_plus

  evidence:
    gate_enabled: true
    policy_enabled: true
    threshold: 0.7

  memory:
    store_enabled: true
    cache_enabled: true
    max_size_gb: 2

  validation:
    enabled: true
    consistency_checks: true
    auto_fix: true

pipeline:
  - script_indexer
  - beat_processor
  - hierarchical_search
  - evidence_gate
  - memory_store
  - validator
  - output_generator

performance:
  parallel: true
  batch_size: 32
  timeout_seconds: 300
"""

    config_path.write_text(config_content)
    print("✅ Configuração de integração criada")
    return True

def run_integration_tests():
    """Executa testes de integração"""
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")

    tests_passed = []
    tests_failed = []

    # Testa importações básicas
    test_imports = [
        "core.auto_documenter",
        "core.sanity_checker",
        "core.snapshot_manager"
    ]

    for module in test_imports:
        try:
            __import__(module)
            tests_passed.append(f"Import {module}")
        except ImportError as e:
            tests_failed.append(f"Import {module}: {e}")

    # Testa estrutura de diretórios
    required_dirs = [
        "beats", "hierarchy", "evidence", "memory", "validation",
        "config", "snapshots", "logs"
    ]

    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            tests_passed.append(f"Dir {dir_name}")
        else:
            tests_failed.append(f"Dir {dir_name} não existe")

    return tests_passed, tests_failed

def main():
    print("=" * 60)
    print("FASE 3: INTEGRATION")
    print("=" * 60)

    # Cria snapshot antes de iniciar
    snapshot = SnapshotManager()
    snap_id = snapshot.create_snapshot(3, "phase3_start", "Iniciando Fase 3")
    print(f"📸 Snapshot criado: {snap_id}")

    # Integra componentes
    print("\n🔧 Integrando componentes...")
    copied, failed = integrate_components()

    # Cria configuração
    print("\n⚙️  Criando configuração de integração...")
    create_integration_config()

    # Executa testes
    print("\n🧪 Executando testes de integração...")
    passed, failed_tests = run_integration_tests()

    print(f"\n  ✅ Testes passaram: {len(passed)}")
    if failed_tests:
        print(f"  ❌ Testes falharam: {len(failed_tests)}")
        for test in failed_tests[:3]:  # Mostra apenas os 3 primeiros
            print(f"    - {test}")

    # Executa sanity check
    print("\n🔍 Executando validação final...")
    checker = SanityChecker()
    valid, errors = checker.run_all()

    if valid:
        print("✅ Validação passou!")
    else:
        print("⚠️  Erros encontrados:")
        for error in errors[:3]:  # Mostra apenas os 3 primeiros
            print(f"  - {error}")

    # Atualiza documentação
    doc = AutoDocumenter()
    doc.evolve_stage("rookie")

    print("\n" + "=" * 60)
    print(f"FASE 3 CONCLUÍDA")
    print(f"  Componentes integrados: {copied}")
    print(f"  Componentes falhados: {failed}")
    print(f"  Testes passaram: {len(passed)}/{len(passed) + len(failed_tests)}")
    print(f"  Validação: {'✅' if valid else '⚠️'}")
    print(f"  Stage atual: rookie")
    print("=" * 60)

    return 0 if valid else 1

if __name__ == "__main__":
    sys.exit(main())