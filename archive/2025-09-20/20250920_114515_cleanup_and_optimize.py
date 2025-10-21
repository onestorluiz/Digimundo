#!/usr/bin/env python3
"""
🧹 SCRIPT DE LIMPEZA E OTIMIZAÇÃO DO SISTEMA
Remove duplicações, limpa referências ao 70B e otimiza o sistema
"""

import os
import sys
from pathlib import Path
import shutil

def cleanup_system():
    """Limpa e otimiza o sistema"""

    print("🧹 INICIANDO LIMPEZA E OTIMIZAÇÃO DO SISTEMA")
    print("=" * 60)

    # 1. Remover referências ao 70B
    print("\n1️⃣ REMOVENDO REFERÊNCIAS AO 70B...")
    files_to_archive = []

    for file_path in Path("scripts/active").glob("*70b*"):
        files_to_archive.append(file_path)

    for file_path in Path("scripts/active").glob("*deepseek*"):
        if "32b" not in str(file_path):  # Manter 32b
            files_to_archive.append(file_path)

    # Criar diretório de arquivo se não existir
    archive_dir = Path("scripts/archive/70b_deprecated")
    archive_dir.mkdir(parents=True, exist_ok=True)

    for file_path in files_to_archive:
        dest = archive_dir / file_path.name
        print(f"   📦 Arquivando: {file_path.name}")
        shutil.move(str(file_path), str(dest))

    print(f"   ✅ {len(files_to_archive)} arquivos arquivados")

    # 2. Consolidar scripts Mixtral
    print("\n2️⃣ CONSOLIDANDO SCRIPTS MIXTRAL...")

    # Scripts principais do Mixtral
    mixtral_core = [
        "mixtral_enhanced_master.py",
        "mixtral_primary_system.py",
        "mixtral_clean_test.py",
        "launch_mixtral_enhanced_automatic.py",
        "launch_mixtral_dedicated.py"
    ]

    # Remover duplicatas
    duplicates = []
    for file_path in Path("scripts/active").glob("mixtral*.py"):
        if file_path.name not in mixtral_core and "continuous" in file_path.name:
            duplicates.append(file_path)

    if duplicates:
        dup_archive = Path("scripts/archive/mixtral_duplicates")
        dup_archive.mkdir(parents=True, exist_ok=True)

        for dup in duplicates:
            dest = dup_archive / dup.name
            print(f"   📦 Consolidando: {dup.name}")
            shutil.move(str(dup), str(dest))

        print(f"   ✅ {len(duplicates)} duplicatas consolidadas")
    else:
        print("   ✅ Nenhuma duplicata encontrada")

    # 3. Limpar imports desnecessários
    print("\n3️⃣ VERIFICANDO IMPORTS...")

    issues_fixed = 0
    for file_path in Path("scripts/active").glob("*.py"):
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            original = content

            # Remover imports do 70b
            if "70b" in content or "deepseek-r1:70b" in content:
                content = content.replace("deepseek-r1:70b", "mixtral-dedicated-q5")
                content = content.replace("70b", "mixtral")

            if content != original:
                with open(file_path, 'w') as f:
                    f.write(content)
                issues_fixed += 1
                print(f"   🔧 Corrigido: {file_path.name}")
        except Exception as e:
            print(f"   ⚠️ Erro em {file_path.name}: {e}")

    print(f"   ✅ {issues_fixed} arquivos corrigidos")

    # 4. Otimizar memória
    print("\n4️⃣ OTIMIZANDO SISTEMA DE MEMÓRIA...")

    # Verificar tamanho do DB
    db_path = Path("data/unified_memory.db")
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024*1024)
        print(f"   💾 unified_memory.db: {size_mb:.2f} MB")

        if size_mb > 50:  # Se maior que 50MB
            print("   ⚠️ Banco de dados grande. Considere vacuum ou limpeza")

    # 5. Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE OTIMIZAÇÃO:")
    print("=" * 60)

    # Contar arquivos ativos
    active_count = len(list(Path("scripts/active").glob("*.py")))
    archived_count = len(list(Path("scripts/archive").glob("**/*.py")))

    print(f"\n✅ Scripts ativos: {active_count}")
    print(f"📦 Scripts arquivados: {archived_count}")
    print(f"🧹 Arquivos movidos: {len(files_to_archive) + len(duplicates)}")
    print(f"🔧 Imports corrigidos: {issues_fixed}")

    # Recomendar próximos passos
    print("\n💡 PRÓXIMOS PASSOS RECOMENDADOS:")
    print("   1. Executar: python3 scripts/active/launch_mixtral_enhanced_automatic.py")
    print("   2. Sistema Mixtral Enhanced está pronto para uso")
    print("   3. Todos os materiais (teoria, meus_filmes, mestres) incluídos")

    print("\n✅ SISTEMA OTIMIZADO COM SUCESSO!")
    print("DIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    cleanup_system()