#!/usr/bin/env python3
"""
🧹 SCRIPT DE LIMPEZA EXECUTÁVEL
Gerado automaticamente - Execute para limpar
"""

from pathlib import Path
import shutil

def execute_cleanup():
    root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    # Criar estrutura de backup
    backup_base = root / "Pre_Limpeza_Minimalista"

    directories = {
        'backup_files': backup_base / "backups_antigos",
        'test_files': backup_base / "arquivos_teste",
        'temp_files': backup_base / "temporarios",
        'old_versions': backup_base / "versoes_antigas",
        'unused_directories': backup_base / "diretorios_nao_usados",
        'config_files': backup_base / "configs_obsoletos"
    }

    # Criar diretórios
    for dir_path in directories.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    # Items para mover (gerado automaticamente)
    moves = {
        'backup_files': [
            '/Users/clubproducoes/Digimundo/scripturemon-champion/backup_20250919_163641_before_unification.tar.gz',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/memory_ecosystem_integration.py.backup',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/scripturemon_start.py.backup',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/test_enhanced_system.py.backup',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/deploy_production.py.backup',
        ],
        'test_files': [
            '/Users/clubproducoes/Digimundo/scripturemon-champion/test2.txt',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/test_output.log',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/test.txt',
        ],
        'temp_files': [
            '/Users/clubproducoes/Digimundo/scripturemon-champion/ast_refactoring_report.txt',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/benchmark_results',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/cache',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/output',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/legacy',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/__pycache__',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/forensic_results',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/.validation_cache',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/logs',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/.ast_backups',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/backups',
        ],
        'unused_directories': [
            '/Users/clubproducoes/Digimundo/scripturemon-champion/pipeline',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/01_ORIGINAIS_PDF',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/Pesquisas_Digilab',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/runtime',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/library',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/utils',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/models',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/knowledge',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/dictionaries',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/sistemas_nao_utilizados',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/apps',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/deployments',
        ],
        'config_files': [
            '/Users/clubproducoes/Digimundo/scripturemon-champion/.DS_Store',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/.claude_session',
            '/Users/clubproducoes/Digimundo/scripturemon-champion/.claude_protected_session',
        ],
    }

    # Executar movimentos
    moved = 0
    errors = 0

    for category, paths in moves.items():
        dest_dir = directories.get(category)
        if not dest_dir:
            continue

        for path_str in paths:
            path = Path(path_str)
            if path.exists():
                try:
                    dest = dest_dir / path.name
                    if path.is_dir():
                        shutil.move(str(path), str(dest))
                    else:
                        shutil.move(str(path), str(dest))
                    print(f"✅ Movido: {path.name} -> {dest_dir.name}")
                    moved += 1
                except Exception as e:
                    print(f"❌ Erro ao mover {path.name}: {e}")
                    errors += 1

    print(f"\n📊 RESULTADO: {moved} movidos, {errors} erros")

if __name__ == "__main__":
    print("🧹 INICIANDO LIMPEZA DA RAIZ")
    print("=" * 60)
    execute_cleanup()
