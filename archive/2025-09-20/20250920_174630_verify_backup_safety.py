#!/usr/bin/env python3
"""
Verify Backup Safety - Verifica que todos os backups estão seguros
Previne recursão e garante que backups vão para SURGICAL_PRESERVATION
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

def check_backup_systems():
    """Verifica todos os sistemas de backup"""
    print("=" * 60)
    print("🔍 VERIFICAÇÃO DE SEGURANÇA DOS BACKUPS")
    print("=" * 60)

    results = []
    issues = []

    # 1. Check backup_config.py
    config_path = Path("config/backup_config.py")
    if config_path.exists():
        results.append("✅ backup_config.py existe")

        # Verify it points to SURGICAL_PRESERVATION
        with open(config_path, 'r') as f:
            content = f.read()
            if "SURGICAL_PRESERVATION" in content:
                results.append("✅ backup_config.py usa SURGICAL_PRESERVATION")
            else:
                issues.append("❌ backup_config.py NÃO usa SURGICAL_PRESERVATION")
    else:
        issues.append("❌ backup_config.py não encontrado")

    # 2. Check backup_manager.py
    backup_manager = Path("deployments/green_v2.0.0/code/apps/scripturemon/backup_manager.py")
    if backup_manager.exists():
        with open(backup_manager, 'r') as f:
            content = f.read()
            if "SURGICAL_PRESERVATION" in content:
                results.append("✅ backup_manager.py atualizado para SURGICAL_PRESERVATION")
            else:
                issues.append("❌ backup_manager.py ainda usa pasta local")

    # 3. Check for old backup directories
    old_backup_dirs = [
        Path("backups"),
        Path("BACKUPS_SISTEMA"),
        Path("deployments/backups"),
        Path("data/backups"),
        Path("data/memory/backups"),
        Path("data/souls/backups"),
        Path("data/revolutionary/backups")
    ]

    for backup_dir in old_backup_dirs:
        if backup_dir.exists():
            files = list(backup_dir.glob("*"))
            if files:
                issues.append(f"⚠️  Pasta de backup antiga encontrada com {len(files)} arquivos: {backup_dir}")
            else:
                results.append(f"📁 Pasta vazia (ok): {backup_dir}")

    # 4. Check SURGICAL_PRESERVATION exists
    surgical_base = Path("/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION")
    if surgical_base.exists():
        results.append(f"✅ SURGICAL_PRESERVATION existe: {surgical_base}")

        # Check today's folder
        date_str = datetime.now().strftime("%Y-%m-%d")
        today_folder = surgical_base / f"{date_str}_SCRIPTUREMON_CHAMPION"
        if today_folder.exists():
            results.append(f"✅ Pasta de hoje criada: {today_folder}")
        else:
            results.append(f"📁 Pasta de hoje será criada: {today_folder}")
    else:
        issues.append("❌ SURGICAL_PRESERVATION não existe!")

    # 5. Check for tar.gz files in project
    tar_files = list(Path(".").rglob("*.tar.gz"))
    zip_files = list(Path(".").rglob("*.zip"))

    if tar_files or zip_files:
        total = len(tar_files) + len(zip_files)
        issues.append(f"⚠️  {total} arquivos de backup encontrados no projeto (podem causar recursão)")
        for f in (tar_files + zip_files)[:5]:  # Show first 5
            print(f"    - {f} ({f.stat().st_size / 1024 / 1024:.1f} MB)")

    # Print results
    print("\n📋 RESULTADOS:")
    for result in results:
        print(f"  {result}")

    if issues:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"  {issue}")

        print("\n🔧 RECOMENDAÇÕES:")
        print("  1. Mover todos os backups antigos para SURGICAL_PRESERVATION")
        print("  2. Deletar pastas de backup vazias")
        print("  3. Atualizar scripts que ainda usam pastas locais")
        print("  4. Adicionar regra: NUNCA criar backups dentro do projeto")
    else:
        print("\n✨ PERFEITO! Todos os sistemas de backup estão seguros!")

    # 6. Test backup location validation
    print("\n🧪 TESTE DE VALIDAÇÃO DE LOCALIZAÇÃO:")
    try:
        from config.backup_config import validate_backup_location
        validate_backup_location()
        print("  ✅ Validação passou - backups NÃO estão dentro do projeto")
    except Exception as e:
        print(f"  ❌ Erro na validação: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMO:")
    print(f"  ✅ Sucessos: {len(results)}")
    print(f"  ⚠️  Problemas: {len(issues)}")
    print("=" * 60)

    # Create report
    report = {
        "timestamp": datetime.now().isoformat(),
        "successes": results,
        "issues": issues,
        "backup_safety": len(issues) == 0,
        "recommendation": "Sistema seguro!" if len(issues) == 0 else "Correções necessárias"
    }

    # Save report
    report_path = surgical_base / f"{date_str}_BACKUP_SAFETY_REPORT.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Relatório salvo em: {report_path}")

if __name__ == "__main__":
    check_backup_systems()