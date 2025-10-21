#!/usr/bin/env python3
"""
Teste do sistema batch DigiLang V8.1 Supreme
"""

import sys
import os
from pathlib import Path

# Importar o batch translator
sys.path.append('/Users/clubproducoes/Digimundo/scripturemon-champion')
from batch_translate_v8 import BatchTranslatorV8, PDF_SUPPORT, DOCX_SUPPORT, DIGILANG_AVAILABLE

def test_with_sample_files():
    """Teste com alguns arquivos da biblioteca"""

    print("🧪 TESTE BATCH DIGILANG V8.1 SUPREME")
    print("="*50)

    # Verificar dependências
    print("📋 Dependências:")
    print(f"   DigiLang V8.1: {'✅' if DIGILANG_AVAILABLE else '❌'}")
    print(f"   PDF Support: {'✅' if PDF_SUPPORT else '❌'}")
    print(f"   DOCX Support: {'✅' if DOCX_SUPPORT else '❌'}")

    if not DIGILANG_AVAILABLE:
        print("❌ DigiLang não disponível - abortando teste")
        return

    # Criar diretório de teste
    test_dir = "/tmp/test_digilang_v8"
    os.makedirs(test_dir, exist_ok=True)

    library_path = "/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS"

    # Encontrar alguns arquivos de teste
    test_files = []

    # Buscar 2-3 arquivos TXT
    txt_files = list(Path(library_path).glob("**/*.txt"))[:2]
    test_files.extend(txt_files)

    # Buscar 2-3 PDFs se disponível
    if PDF_SUPPORT:
        pdf_files = list(Path(library_path).glob("**/*.pdf"))[:2]
        test_files.extend(pdf_files)

    if not test_files:
        print("❌ Nenhum arquivo de teste encontrado")
        return

    print(f"\n📁 Arquivos de teste encontrados: {len(test_files)}")
    for f in test_files:
        print(f"   - {f.name}")

    # Copiar arquivos para diretório de teste temporário
    test_library = Path(test_dir) / "test_library"
    test_library.mkdir(exist_ok=True)

    import shutil
    for file_path in test_files:
        dest_path = test_library / file_path.name
        shutil.copy2(file_path, dest_path)
        print(f"   Copiado: {file_path.name}")

    # Executar batch translator no diretório de teste
    print(f"\n🚀 Executando teste batch...")

    output_path = Path(test_dir) / "output"
    translator = BatchTranslatorV8(str(test_library), str(output_path))

    # Processar com apenas 2 workers para teste
    report = translator.process_batch(max_workers=2)

    # Mostrar resultados
    translator.print_summary(report)

    print(f"\n📂 Arquivos de teste em: {test_dir}")
    print(f"📊 Relatórios em: {output_path}/reports/")

    # Verificar se arquivos foram criados
    compressed_files = list((output_path / "compressed_files").glob("*"))
    print(f"\n✅ Arquivos comprimidos criados: {len(compressed_files)}")

    # Mostrar exemplo de arquivo comprimido se existir
    if compressed_files:
        sample_file = compressed_files[0]
        print(f"\n📄 Exemplo de compressão ({sample_file.name}):")
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content[:500] + "..." if len(content) > 500 else content)
        except Exception as e:
            print(f"Erro lendo arquivo: {e}")

if __name__ == "__main__":
    test_with_sample_files()