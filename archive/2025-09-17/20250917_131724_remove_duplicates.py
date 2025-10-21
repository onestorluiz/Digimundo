#!/usr/bin/env python3
"""
🧹 REMOVE DUPLICATE FILES
==========================
Remove arquivos duplicados mantendo apenas uma cópia
"""

import hashlib
import os
from pathlib import Path
from typing import Dict, List, Set
import shutil

class DuplicateRemover:
    """Remove arquivos duplicados do sistema"""

    def __init__(self, root_path: str = "/Users/clubproducoes/Digimundo/scripturemon-champion"):
        self.root_path = Path(root_path)
        self.removed_files = []
        self.kept_files = []
        self.errors = []

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calcula hash MD5 de um arquivo"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.errors.append(f"Error hashing {file_path}: {e}")
            return None

    def find_duplicates(self) -> Dict[str, List[Path]]:
        """Encontra todos os arquivos duplicados"""
        hash_map = {}

        # Focar em diretórios com alta redundância
        target_dirs = [
            "deployments",
            "scripts",
            "batch"
        ]

        print("🔍 Procurando arquivos duplicados...")

        for target_dir in target_dirs:
            target_path = self.root_path / target_dir
            if not target_path.exists():
                continue

            for py_file in target_path.rglob("*.py"):
                if py_file.name.endswith('.bak'):
                    continue

                file_hash = self.calculate_file_hash(py_file)
                if file_hash:
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    hash_map[file_hash].append(py_file)

        # Filtrar apenas duplicados
        duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}

        return duplicates

    def remove_duplicates(self, dry_run: bool = True) -> dict:
        """Remove arquivos duplicados"""
        duplicates = self.find_duplicates()

        if not duplicates:
            print("✅ Nenhum arquivo duplicado encontrado!")
            return {"removed": 0, "kept": 0, "errors": 0}

        print(f"\n📋 Encontrados {sum(len(v) - 1 for v in duplicates.values())} arquivos duplicados:")

        removed_count = 0
        kept_count = 0

        for file_hash, file_list in duplicates.items():
            # Ordenar por caminho para manter o mais importante
            file_list.sort(key=lambda x: (
                'deployments/green_v2.0.0' not in str(x),  # Priorizar green deployment
                'scripts' not in str(x),  # Depois scripts
                len(str(x))  # Caminhos mais curtos primeiro
            ))

            kept_file = file_list[0]
            self.kept_files.append(kept_file)
            kept_count += 1

            print(f"\n  📁 Hash: {file_hash[:8]}...")
            print(f"     ✅ Mantendo: {kept_file.relative_to(self.root_path)}")

            for dup_file in file_list[1:]:
                print(f"     ❌ Removendo: {dup_file.relative_to(self.root_path)}")

                if not dry_run:
                    try:
                        # Criar backup antes de remover
                        backup_dir = self.root_path / "backups" / "duplicates"
                        backup_dir.mkdir(parents=True, exist_ok=True)

                        backup_path = backup_dir / dup_file.name
                        counter = 1
                        while backup_path.exists():
                            backup_path = backup_dir / f"{dup_file.stem}_{counter}{dup_file.suffix}"
                            counter += 1

                        shutil.copy2(dup_file, backup_path)
                        dup_file.unlink()

                        self.removed_files.append(dup_file)
                        removed_count += 1
                    except Exception as e:
                        self.errors.append(f"Error removing {dup_file}: {e}")
                else:
                    removed_count += 1

        print(f"\n📊 Resumo:")
        print(f"  - Arquivos a remover: {removed_count}")
        print(f"  - Arquivos a manter: {kept_count}")
        print(f"  - Erros: {len(self.errors)}")

        if dry_run:
            print("\n⚠️ Modo DRY RUN - nenhum arquivo foi removido")
            print("   Execute com --apply para remover os duplicados")

        return {
            "removed": removed_count,
            "kept": kept_count,
            "errors": len(self.errors),
            "removed_files": [str(f) for f in self.removed_files],
            "kept_files": [str(f) for f in self.kept_files]
        }


if __name__ == "__main__":
    import sys

    remover = DuplicateRemover()

    # Verificar se deve aplicar ou só mostrar
    apply_changes = "--apply" in sys.argv

    if not apply_changes:
        print("🔍 MODO DRY RUN - Analisando duplicados...")
        result = remover.remove_duplicates(dry_run=True)
    else:
        print("⚠️ APLICANDO MUDANÇAS - Removendo duplicados...")
        result = remover.remove_duplicates(dry_run=False)

        if result["removed"] > 0:
            print(f"\n✅ {result['removed']} arquivos duplicados removidos com sucesso!")
            print(f"   Backups salvos em: backups/duplicates/")