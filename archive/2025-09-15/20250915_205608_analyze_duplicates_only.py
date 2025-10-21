#!/usr/bin/env python3
"""
APENAS ANÁLISE DE DUPLICADOS - SEM DELEÇÃO
Mostra o que PODERIA ser deletado para você decidir
"""

import os
import re
from pathlib import Path
from datetime import datetime
import hashlib

def find_google_drive_duplicates(scan_path):
    """Encontra duplicados típicos do Google Drive"""

    # Padrões específicos do Google Drive
    drive_patterns = [
        r'^(.+) \(\d+\)(\.[^.]+)?$',        # arquivo (1).ext
        r'^(.+) - Copy(\.[^.]+)?$',         # arquivo - Copy.ext
        r'^Copy of (.+)(\.[^.]+)?$',        # Copy of arquivo.ext
    ]

    print(f"🔍 Analisando {scan_path}...")

    # Encontrar arquivos com padrões suspeitos
    suspicious_files = []

    for file_path in Path(scan_path).rglob("*"):
        if file_path.is_file():
            filename = file_path.name

            for pattern in drive_patterns:
                if re.match(pattern, filename):
                    suspicious_files.append({
                        'path': str(file_path),
                        'filename': filename,
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                        'pattern': pattern
                    })
                    break

    # Agrupar por diretório
    by_directory = {}
    for f in suspicious_files:
        dir_name = str(Path(f['path']).parent)
        if dir_name not in by_directory:
            by_directory[dir_name] = []
        by_directory[dir_name].append(f)

    return by_directory

def main():
    scan_path = "/Users/clubproducoes/Digimundo/RECOVERED_CODE"

    if not os.path.exists(scan_path):
        print(f"❌ Pasta não encontrada: {scan_path}")
        return

    duplicates_by_dir = find_google_drive_duplicates(scan_path)

    if not duplicates_by_dir:
        print("✅ Nenhum padrão de duplicado do Google Drive encontrado!")
        return

    print(f"\n📊 ENCONTRADOS PADRÕES SUSPEITOS EM {len(duplicates_by_dir)} DIRETÓRIOS:")
    print("=" * 80)

    total_suspicious = 0
    potential_savings = 0

    for directory, files in duplicates_by_dir.items():
        print(f"\n📁 {directory.replace('/Users/clubproducoes/Digimundo/RECOVERED_CODE/', './')}")
        print("-" * 60)

        for f in files:
            size_mb = f['size'] / (1024*1024)
            print(f"  🔍 {f['filename']}")
            print(f"      Tamanho: {size_mb:.1f}MB")
            print(f"      Modificado: {f['modified'].strftime('%Y-%m-%d %H:%M')}")
            print()

            total_suspicious += 1
            potential_savings += f['size']

    savings_mb = potential_savings / (1024*1024)
    print("=" * 80)
    print(f"📊 RESUMO:")
    print(f"   Arquivos suspeitos: {total_suspicious}")
    print(f"   Potencial economia: {savings_mb:.1f}MB")
    print()
    print("🤔 PRÓXIMOS PASSOS:")
    print("   1. Revise a lista acima")
    print("   2. Identifique quais são realmente duplicados")
    print("   3. Delete manualmente os que confirmar")
    print("   4. Ou me peça para gerar script específico")

if __name__ == "__main__":
    main()