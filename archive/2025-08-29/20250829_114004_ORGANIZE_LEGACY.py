#!/usr/bin/env python3
"""
🗂️ ORGANIZADOR DE ARQUIVOS LEGACY
Separa arquivos ativos dos legacy
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
LEGACY_DIR = BASE_DIR / "LEGACY_ARCHIVE"
LEGACY_DIR.mkdir(exist_ok=True)

# ARQUIVOS DO SISTEMA ATIVO (NÃO MOVER)
ACTIVE_FILES = {
    # Sistema principal
    "scripturemon",
    "CINEMA_KNOWLEDGE_SYSTEM.py",
    "CINEMA_MONITOR_DAEMON.py",
    "ACTIVATE_CINEMA_KNOWLEDGE.sh",
    
    # Diretórios ativos
    "CINEMA_KNOWLEDGE",
    "conhecimento_bruto",
    "conhecimento_digilang",
    
    # Scripts essenciais
    "MEMORIA_DIGILANG_UNIFICADA.py",
    "SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py",
    
    # Documentação importante
    "README.md",
    "RELATORIO_FINAL_17_MANUAIS.md",
    "100_PERCENT_ACHIEVED.md",
}

# DIRETÓRIOS A MANTER
KEEP_DIRS = {
    "CINEMA_KNOWLEDGE",
    "conhecimento_bruto", 
    "conhecimento_digilang",
    "bin",
    "digiknowledge",
    "LEGACY_ARCHIVE"
}

print("🗂️ ORGANIZANDO ARQUIVOS LEGACY")
print("=" * 50)

# Criar timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
legacy_subdir = LEGACY_DIR / f"archive_{timestamp}"
legacy_subdir.mkdir(exist_ok=True)

# Contadores
moved = 0
kept = 0
errors = 0

# 1. MOVER DIRETÓRIOS ANTIGOS
old_dirs = ["04_EVOLUTION", "05_DIGILANG", "06_TESTS", "07_DOCS", "08_SCRIPTS", "09_LEGACY"]
for dir_name in old_dirs:
    dir_path = BASE_DIR / dir_name
    if dir_path.exists():
        dest = legacy_subdir / dir_name
        try:
            shutil.move(str(dir_path), str(dest))
            print(f"📁 Movido: {dir_name}")
            moved += 1
        except Exception as e:
            print(f"❌ Erro ao mover {dir_name}: {e}")
            errors += 1

# 2. MOVER ARQUIVOS DE TESTE E TEMPORÁRIOS
test_patterns = [
    "*TEST*.py",
    "*test*.py",
    "*_REPORT_*.md",
    "*_LOG_*.md",
    "SILICON_VALLEY*.py",
    "QUICK_*.py",
    "FIX_*.py",
    "VALIDATE_*.py",
    "SIMULATE_*.py",
    "ANALYZE_*.py",
    "CHECK_*.py"
]

for pattern in test_patterns:
    for file in BASE_DIR.glob(pattern):
        if file.name not in ACTIVE_FILES and file.is_file():
            dest = legacy_subdir / file.name
            try:
                shutil.move(str(file), str(dest))
                print(f"📄 Movido: {file.name[:40]}...")
                moved += 1
            except:
                errors += 1

# 3. MOVER SCRIPTS ANTIGOS E RELATÓRIOS
old_files = [
    "HARMONIZATION_REPORT*.md",
    "IMPORT_REPORT*.md",
    "PDF_IDENTIFICATION*.md",
    "DIGILANG_TRANSLATION_REPORT.md",
    "IMPROVEMENTS_REPORT.md",
    "FINAL_CHANGES_REPORT.md",
    "TELEPATHY_IMPROVEMENTS.py",
    "NEXT_STEPS_IMPLEMENTATION.py",
    "AUTOMATE_CINEMA_IMPORT.py",
    "CINEMA_IMPORT_DEFINITIVE.py",
    "IDENTIFY_AND_ORGANIZE_PDFS.py",
    "TRANSLATE_REMAINING_PDFS.py",
    "COPY_MISSING_MANUALS.sh",
    "validate_documents.sh",
    "SETUP_ALIASES_PRATICOS.sh",
    "CONSOLIDATE_ALL_KNOWLEDGE.sh",
    "ACTIVATE_ULTIMATE_SYMBIOTIC.sh"
]

for pattern in old_files:
    for file in BASE_DIR.glob(pattern):
        if file.is_file():
            dest = legacy_subdir / file.name
            try:
                shutil.move(str(file), str(dest))
                print(f"📄 Movido: {file.name[:40]}...")
                moved += 1
            except:
                errors += 1

# 4. MOVER DOCUMENTAÇÃO DE ANÁLISE
analysis_docs = [
    "ANALISE_*.md",
    "DOCUMENTACAO_*.md",
    "LICOES_APRENDIDAS.md",
    "OBRA_PRIMA_COMPLETA.md",
    "COMPLETE_CINEMA_GUIDE.md",
    "SCRIPTUREMON_PHILOSOPHY.md"
]

for pattern in analysis_docs:
    for file in BASE_DIR.glob(pattern):
        if file.is_file() and file.name not in ACTIVE_FILES:
            dest = legacy_subdir / file.name
            try:
                shutil.move(str(file), str(dest))
                print(f"📄 Movido: {file.name[:40]}...")
                moved += 1
            except:
                errors += 1

# 5. CONTAR ARQUIVOS MANTIDOS
for item in BASE_DIR.iterdir():
    if item.is_file() and item.name not in ["ORGANIZE_LEGACY.py"]:
        kept += 1
        print(f"✅ Mantido: {item.name}")

print("\n" + "=" * 50)
print("📊 RESULTADO DA ORGANIZAÇÃO:")
print(f"   📁 Movidos para legacy: {moved}")
print(f"   ✅ Mantidos ativos: {kept}")
print(f"   ❌ Erros: {errors}")

# Criar índice do legacy
index_file = legacy_subdir / "INDEX.md"
index_content = f"""# 📚 ARQUIVO LEGACY - {timestamp}

## Arquivos arquivados em {datetime.now().strftime('%d/%m/%Y %H:%M')}

Este diretório contém:
- Testes antigos
- Relatórios temporários
- Scripts de migração
- Documentação de desenvolvimento
- Arquivos não mais necessários para operação

Total de arquivos: {moved}
"""

index_file.write_text(index_content)
print(f"\n📄 Índice criado: {index_file.name}")
print("\n✨ Organização completa!")
