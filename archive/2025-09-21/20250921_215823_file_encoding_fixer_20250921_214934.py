#!/usr/bin/env python3
"""
File Encoding Validator & Fixer - DIGIMUNDO STYLE
Timestamp: 20250921_214934
Detecta e corrige problemas de encoding
"""

import os
from pathlib import Path
import chardet
from typing import List, Tuple

def validate_and_fix_file(filepath: Path) -> Tuple[bool, str]:
    """
    Detecta encoding e converte para UTF-8.

    Returns:
        tuple: (success, message)
    """
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']

    # Primeiro tenta detectar automaticamente
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']
            confidence = result['confidence']

            if detected_encoding and confidence > 0.7:
                encodings_to_try.insert(0, detected_encoding)
    except Exception as e:
        pass

    # Tenta cada encoding
    for encoding in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()

            # Se conseguiu ler e não é UTF-8, converte
            if encoding.lower() != 'utf-8':
                backup_path = filepath.with_suffix(filepath.suffix + '.backup_20250921_214934')

                # Faz backup primeiro
                with open(backup_path, 'wb') as f:
                    f.write(raw_data)

                # Salva em UTF-8
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                return True, f"Convertido de {encoding} para UTF-8 (backup: {backup_path.name})"

            return True, "Já estava em UTF-8"

        except UnicodeDecodeError:
            continue
        except Exception as e:
            continue

    return False, "Não foi possível detectar encoding válido"


def validate_all_screenplays(base_dir: Path = Path("screenplays")) -> List[Tuple[str, bool, str]]:
    """
    Valida e corrige todos os arquivos de roteiro.

    Returns:
        list: [(filename, success, message), ...]
    """
    results = []

    # Busca arquivos relevantes
    patterns = ['*.txt', '*.docx.txt']
    files_to_check = []

    for pattern in patterns:
        files_to_check.extend(base_dir.rglob(pattern))

    print(f"🔍 Encontrados {len(files_to_check)} arquivos para validar")

    for filepath in sorted(files_to_check):
        success, message = validate_and_fix_file(filepath)
        results.append((filepath.name, success, message))

        status = "✅" if success else "⚠️"
        print(f"{status} {filepath.name}: {message}")

    return results


def fix_apocalypse_now():
    """
    Corrige especificamente o arquivo problemático.
    """
    problem_file = Path("screenplays/Apocalypse-Now-Screenplay.txt")

    if not problem_file.exists():
        print(f"⚠️ Arquivo não encontrado: {problem_file}")
        return False

    print(f"\n🔧 Tentando corrigir {problem_file.name}...")

    # Tenta encodings menos comuns
    exotic_encodings = [
        'utf-16', 'utf-16-le', 'utf-16-be',
        'utf-32', 'utf-32-le', 'utf-32-be',
        'mac_roman', 'windows-1250', 'windows-1251'
    ]

    for encoding in exotic_encodings:
        try:
            with open(problem_file, 'r', encoding=encoding) as f:
                content = f.read()[:100]  # Lê só início para testar
                print(f"  ✅ Encoding detectado: {encoding}")
                print(f"  Prévia: {content[:50]}...")

                # Lê todo arquivo
                with open(problem_file, 'r', encoding=encoding) as f:
                    full_content = f.read()

                # Salva backup
                backup_path = problem_file.with_suffix('.txt.backup_encoding')
                with open(problem_file, 'rb') as f:
                    with open(backup_path, 'wb') as b:
                        b.write(f.read())

                # Salva em UTF-8
                with open(problem_file, 'w', encoding='utf-8') as f:
                    f.write(full_content)

                print(f"  ✅ Arquivo convertido para UTF-8!")
                print(f"  📋 Backup salvo em: {backup_path.name}")
                return True

        except Exception as e:
            continue

    print(f"  ⚠️ Não foi possível corrigir o arquivo")
    return False


if __name__ == "__main__":
    print("🧹 VALIDADOR DE ENCODING - DIGIMUNDO STYLE")
    print("=" * 50)

    # Testa arquivo específico primeiro
    fix_apocalypse_now()

    print("\n" + "=" * 50)
    print("📂 Validando todos os arquivos...")

    # Valida todos
    results = validate_all_screenplays()

    # Sumário
    success_count = sum(1 for _, success, _ in results if success)
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {success_count}/{len(results)} arquivos válidos")

    if success_count < len(results):
        print("\n⚠️ Arquivos com problemas:")
        for name, success, message in results:
            if not success:
                print(f"  - {name}: {message}")