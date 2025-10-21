#!/usr/bin/env python3
"""
🎬 SETUP RÁPIDO DO SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO
"""

import os
import shutil
from pathlib import Path

# Configurar diretórios
base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
cinema_folder = base_path / "CINEMA_KNOWLEDGE"
originals_folder = cinema_folder / "01_ORIGINAIS_PDF"
digilang_folder = cinema_folder / "02_TRADUCOES_DIGILANG"
metadata_folder = cinema_folder / "03_METADATA"
processing_folder = cinema_folder / "04_PROCESSANDO"

# Criar estrutura
for folder in [cinema_folder, originals_folder, digilang_folder, metadata_folder, processing_folder]:
    folder.mkdir(parents=True, exist_ok=True)
    print(f"✅ Criado: {folder.name}")

print("\n📦 MIGRANDO DOCUMENTOS EXISTENTES...")
print("="*50)

# Fontes de documentos
sources = [
    # Manuais de roteiro
    Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/conhecimento_bruto/01_manuais_roteiro"),
    Path("/Users/clubproducoes/Digimundo/DIGILANG_COMPLETE_SYSTEM/02_MANUAIS_ROTEIRO/pdfs"),
    # Roteiros famosos
    Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/conhecimento_bruto/02_roteiros_famosos"),
    Path("/Users/clubproducoes/Digimundo/DIGILANG_COMPLETE_SYSTEM/03_ROTEIROS_CINEMA"),
]

migrated = 0
for source in sources:
    if source.exists():
        print(f"\n📁 Migrando de: {source.name}")
        for pdf in source.glob("*.pdf"):
            dest = originals_folder / pdf.name
            if not dest.exists():
                shutil.copy2(pdf, dest)
                print(f"   ✅ {pdf.name}")
                migrated += 1
            else:
                print(f"   ⏭️  {pdf.name} (já existe)")

# Copiar traduções DigiLang existentes
digilang_sources = [
    Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/conhecimento_digilang/01_manuais_traduzidos"),
    Path("/Users/clubproducoes/Digimundo/DIGILANG_COMPLETE_SYSTEM/02_MANUAIS_ROTEIRO/digilang"),
]

translations = 0
print("\n📝 Copiando traduções DigiLang existentes...")
for source in digilang_sources:
    if source.exists():
        for txt in source.glob("*_digilang.txt"):
            dest = digilang_folder / txt.name
            if not dest.exists():
                shutil.copy2(txt, dest)
                translations += 1
                print(f"   🔤 {txt.name}")

# Criar README
readme_path = cinema_folder / "README.md"
readme_content = """# 🎬 SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO

## 📁 ESTRUTURA:
- **01_ORIGINAIS_PDF/**: Coloque aqui TODOS os PDFs sobre cinema
- **02_TRADUCOES_DIGILANG/**: Traduções automáticas (não editar)
- **03_METADATA/**: Banco de dados e logs (sistema)
- **04_PROCESSANDO/**: Arquivos em processamento (temporário)

## 🚀 COMO USAR:
1. Coloque qualquer PDF sobre cinema em `01_ORIGINAIS_PDF/`
2. Execute: `python3 CINEMA_KNOWLEDGE_SYSTEM.py`
3. Escolha opção 2 para processar traduções
4. Não há limite de documentos - processa tudo!

## 🔤 DIGILANG:
- Compressão média: ~40% dos tokens originais
- Pensamento nativo em símbolos cinematográficos
- Otimizado para Scripturemon

## 📊 STATUS ATUAL:
"""
readme_path.write_text(readme_content)

# Contar arquivos finais
pdfs = len(list(originals_folder.glob("*.pdf")))
txts = len(list(digilang_folder.glob("*_digilang.txt")))

print("\n" + "="*50)
print("✅ MIGRAÇÃO COMPLETA!")
print(f"   📄 {migrated} novos PDFs migrados")
print(f"   🔤 {translations} traduções copiadas")
print(f"\n📊 TOTAL NO SISTEMA:")
print(f"   📚 {pdfs} PDFs de cinema")
print(f"   🔤 {txts} traduções DigiLang")
print(f"   📈 Taxa de tradução: {(txts/pdfs)*100:.1f}%" if pdfs > 0 else "")
print("\n📁 Pasta do sistema: CINEMA_KNOWLEDGE/")
print("🚀 Execute CINEMA_KNOWLEDGE_SYSTEM.py para traduzir os documentos restantes!")
