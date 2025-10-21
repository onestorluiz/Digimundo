#!/usr/bin/env python3
"""
🔧 FIX CONSTRUCTOR CORRUPTION
==============================
Corrige automaticamente o problema de __init__ para __init__
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

class ConstructorCorruptionFixer:
    """Corrige constructor corruption em arquivos Python"""

    def __init__(self, root_path: str = "/Users/clubproducoes/Digimundo/scripturemon-champion"):
        self.root_path = Path(root_path)
        self.fixed_files = []
        self.errors = []

    def find_corrupted_files(self) -> List[Tuple[Path, int]]:
        """Encontra arquivos com constructor corruption"""
        corrupted = []
        pattern = re.compile(r'__init__')

        for py_file in self.root_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    if matches:
                        corrupted.append((py_file, len(matches)))
            except Exception as e:
                self.errors.append(f"Error reading {py_file}: {e}")

        return corrupted

    def fix_file(self, file_path: Path) -> bool:
        """Corrige um arquivo específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Corrige __init__ para __init__
            fixed_content = content.replace('__init__', '__init__')

            if fixed_content != content:
                # Backup do arquivo original
                backup_path = file_path.with_suffix('.py.bak')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Salva arquivo corrigido
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

                self.fixed_files.append(file_path)
                return True

        except Exception as e:
            self.errors.append(f"Error fixing {file_path}: {e}")
            return False

        return False

    def fix_all(self) -> dict:
        """Corrige todos os arquivos com problema"""
        print("🔍 Procurando arquivos com constructor corruption...")
        corrupted = self.find_corrupted_files()

        if not corrupted:
            print("✅ Nenhum arquivo com constructor corruption encontrado!")
            return {"fixed": 0, "errors": 0}

        print(f"📋 Encontrados {len(corrupted)} arquivos com problemas:")
        for file_path, count in corrupted:
            print(f"  - {file_path.relative_to(self.root_path)}: {count} ocorrências")

        print("\n🔧 Aplicando correções...")
        fixed_count = 0

        for file_path, _ in corrupted:
            if self.fix_file(file_path):
                fixed_count += 1
                print(f"  ✅ Corrigido: {file_path.name}")
            else:
                print(f"  ❌ Erro ao corrigir: {file_path.name}")

        print(f"\n📊 Resumo:")
        print(f"  - Arquivos corrigidos: {fixed_count}/{len(corrupted)}")
        print(f"  - Erros: {len(self.errors)}")

        if self.errors:
            print("\n⚠️ Erros encontrados:")
            for error in self.errors[:5]:
                print(f"  - {error}")

        return {
            "fixed": fixed_count,
            "errors": len(self.errors),
            "fixed_files": [str(f) for f in self.fixed_files]
        }


if __name__ == "__main__":
    fixer = ConstructorCorruptionFixer()
    result = fixer.fix_all()

    if result["fixed"] > 0:
        print("\n✅ Constructor corruption corrigido com sucesso!")
    else:
        print("\n✅ Nenhuma correção necessária!")