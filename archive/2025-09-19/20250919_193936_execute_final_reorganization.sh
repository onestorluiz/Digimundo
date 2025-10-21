#!/bin/bash
# Script de reorganização final

mkdir -p '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_old'
mkdir -p '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration'
mkdir -p '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/docs_archive'
mkdir -p '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/src_unused'

# Mover arquivos
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/soul_os' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/immortality_vault_fixed' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/memory' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/original' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/test_revolutionary' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/tpd' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/harmony' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/ollama_cache' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/books' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/data/samples' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/data_cleanup/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/complete_unification_plan.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/consolidate_remaining_databases.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/execute_complete_migration.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/update_main_system.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/execute_root_cleanup.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/analyze_and_cleanup_root.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/cleanup_legacy_memory.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/unify_all_memory_systems.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/force_total_unification.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null
mv '/Users/clubproducoes/Digimundo/scripturemon-champion/scripts/final_unification_push.py' '/Users/clubproducoes/Digimundo/scripturemon-champion/Pre_Limpeza_Minimalista_Final/scripts_migration/' 2>/dev/null

# Reorganizar estrutura
mv src/advanced src/features 2>/dev/null
mv src/learning src/ml 2>/dev/null
mkdir -p scripts/active scripts/archive
mv scripts/*migration*.py scripts/archive/ 2>/dev/null
mv scripts/*unif*.py scripts/archive/ 2>/dev/null
mv scripts/*cleanup*.py scripts/archive/ 2>/dev/null

echo '✅ Reorganização completa!'
