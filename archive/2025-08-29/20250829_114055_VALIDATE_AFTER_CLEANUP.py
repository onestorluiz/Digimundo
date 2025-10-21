#!/usr/bin/env python3
"""
✅ VALIDADOR PÓS-LIMPEZA
Verifica que sistema continua 100% funcional
"""

import subprocess
import sys
from pathlib import Path

# Cores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
END = '\033[0m'
BOLD = '\033[1m'

print(BOLD + "\n🔍 VALIDAÇÃO PÓS-LIMPEZA" + END)
print("=" * 50)

errors = []
warnings = []

# 1. TESTAR COMANDO SCRIPTUREMON
print("\n📌 1. COMANDO PRINCIPAL")
try:
    result = subprocess.run("~/bin/scripturemon help", shell=True, capture_output=True, timeout=5)
    if result.returncode == 0:
        print(f"{GREEN}✅ Comando scripturemon funcionando{END}")
    else:
        errors.append("Comando scripturemon falhou")
        print(f"{RED}❌ Comando scripturemon falhou{END}")
except Exception as e:
    errors.append(f"Erro no comando: {e}")

# 2. VERIFICAR SISTEMA DE CONHECIMENTO
print("\n📌 2. SISTEMA DE CONHECIMENTO")
CINEMA_DIR = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/CINEMA_KNOWLEDGE")

dirs_to_check = [
    CINEMA_DIR / "01_ORIGINAIS_PDF",
    CINEMA_DIR / "02_TRADUCOES_DIGILANG",
    CINEMA_DIR / "03_METADATA",
    CINEMA_DIR / "04_PROCESSANDO"
]

for dir_path in dirs_to_check:
    if dir_path.exists():
        print(f"{GREEN}✅ {dir_path.name} existe{END}")
    else:
        errors.append(f"Diretório faltando: {dir_path.name}")
        print(f"{RED}❌ {dir_path.name} faltando{END}")

# 3. VERIFICAR ARQUIVOS ESSENCIAIS
print("\n📌 3. ARQUIVOS ESSENCIAIS")
BASE_DIR = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")

essential_files = [
    "scripturemon",
    "CINEMA_KNOWLEDGE_SYSTEM.py",
    "CINEMA_MONITOR_DAEMON.py",
    "MEMORIA_DIGILANG_UNIFICADA.py",
    "SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py"
]

for file_name in essential_files:
    file_path = BASE_DIR / file_name
    if file_path.exists():
        print(f"{GREEN}✅ {file_name} presente{END}")
    else:
        errors.append(f"Arquivo essencial faltando: {file_name}")
        print(f"{RED}❌ {file_name} FALTANDO!{END}")

# 4. VERIFICAR DOCUMENTOS
print("\n📌 4. DOCUMENTOS DE CINEMA")
pdfs = len(list((CINEMA_DIR / "01_ORIGINAIS_PDF").glob("*.pdf")))
translations = len(list((CINEMA_DIR / "02_TRADUCOES_DIGILANG").glob("*_digilang.txt")))

print(f"📚 PDFs: {pdfs}")
print(f"🔤 Traduções: {translations}")

if pdfs > 0 and translations > 0:
    print(f"{GREEN}✅ Documentos preservados{END}")
else:
    errors.append("Documentos perdidos")
    print(f"{RED}❌ Documentos perdidos!{END}")

# 5. VERIFICAR MONITOR
print("\n📌 5. MONITOR AUTOMÁTICO")
result = subprocess.run(
    "ps aux | grep CINEMA_MONITOR_DAEMON | grep -v grep",
    shell=True, capture_output=True, text=True
)

if result.stdout:
    print(f"{GREEN}✅ Monitor rodando{END}")
else:
    warnings.append("Monitor não está rodando")
    print(f"{YELLOW}⚠️ Monitor não está rodando{END}")

# 6. TESTAR FUNCIONALIDADE
print("\n📌 6. TESTE DE FUNCIONALIDADE")
try:
    result = subprocess.run(
        "~/bin/scripturemon status",
        shell=True, capture_output=True, text=True, timeout=5
    )
    if "SCRIPTUREMON" in result.stdout:
        print(f"{GREEN}✅ Sistema respondendo corretamente{END}")
    else:
        warnings.append("Resposta inesperada do sistema")
except:
    errors.append("Sistema não respondeu")

# 7. VERIFICAR LEGACY
print("\n📌 7. ARQUIVO LEGACY")
legacy_dir = BASE_DIR / "LEGACY_ARCHIVE"
if legacy_dir.exists():
    archives = list(legacy_dir.glob("archive_*"))
    if archives:
        latest = sorted(archives)[-1]
        files_in_archive = len(list(latest.glob("*")))
        print(f"{GREEN}✅ Legacy organizado: {files_in_archive} arquivos{END}")
    else:
        warnings.append("Nenhum arquivo legacy")
else:
    errors.append("Diretório legacy não criado")

# RELATÓRIO FINAL
print("\n" + "=" * 50)
print(BOLD + "📊 RELATÓRIO FINAL" + END)
print("=" * 50)

if not errors and not warnings:
    print(f"\n{GREEN}{BOLD}🎉 SISTEMA 100% FUNCIONAL!{END}")
    print(f"{GREEN}Todos os componentes essenciais preservados{END}")
    print(f"{GREEN}Limpeza bem-sucedida sem quebrar nada{END}")
    sys.exit(0)
else:
    if errors:
        print(f"\n{RED}❌ ERROS ENCONTRADOS:{END}")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print(f"\n{YELLOW}⚠️ AVISOS:{END}")
        for warning in warnings:
            print(f"   • {warning}")
    
    if errors:
        print(f"\n{RED}Sistema pode estar quebrado!{END}")
        sys.exit(1)
    else:
        print(f"\n{YELLOW}Sistema funcional com avisos menores{END}")
        sys.exit(0)
