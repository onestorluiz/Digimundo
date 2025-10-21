#!/usr/bin/env python3

"""
Script de ingestão inicial dos PDFs existentes no sistema Scripturemon
"""

import os
import sys
from pathlib import Path

# Adicionar pasta app ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

def process_existing_pdfs():
    """Processa PDFs existentes no sistema"""
    
    base_dir = Path(__file__).parent.parent / "cinema"
    
    # Descobrir todos os PDFs existentes
    pdfs_to_process = {
        "teoria_roteiro": list((base_dir / "1_teoria_roteiro").glob("*.pdf")) if (base_dir / "1_teoria_roteiro").exists() else [],
        "roteiro_mestre": list((base_dir / "2_roteiros_mestres").glob("*.pdf")) if (base_dir / "2_roteiros_mestres").exists() else [],
        "roteiro_criador": list((base_dir / "3_roteiros_criador").glob("*.pdf")) if (base_dir / "3_roteiros_criador").exists() else []
    }
    
    # Verificar quais existem
    print("🔍 Descobrindo PDFs disponíveis...\n")
    
    total_found = 0
    for doc_type, files in pdfs_to_process.items():
        if files:
            print(f"✅ {doc_type}: {len(files)} PDFs encontrados")
            for f in files[:5]:  # Mostrar apenas os primeiros 5
                print(f"   - {f.name[:60]}...")
            if len(files) > 5:
                print(f"   ... e mais {len(files) - 5} arquivos")
            total_found += len(files)
    
    if total_found == 0:
        print("❌ Nenhum PDF encontrado para processar")
        print("\n💡 Copie alguns PDFs para as pastas:")
        print("   - cinema/1_teoria_roteiro/ (livros de teoria)")
        print("   - cinema/2_roteiros_mestres/ (roteiros famosos)")
        print("   - cinema/3_roteiros_criador/ (seus roteiros)")
        return
    
    print(f"\n📚 Total: {total_found} PDFs prontos para processar")
    
    print("\n🚀 Iniciando processamento...\n")
    
    # Importar pipeline apenas se for processar
    try:
        from app.processing.pipeline import process_pdf
        
        processed = 0
        errors = 0
        
        for doc_type, files in pdfs_to_process.items():
            if files:
                print(f"\n📁 Processando {doc_type}...")
                print("-" * 40)
                
                for pdf in files:
                    try:
                        print(f"📄 [{processed+1}/{total_found}] {pdf.name[:50]}...")
                        
                        result = process_pdf(str(pdf), doc_type=doc_type)
                        
                        print(f"   ✅ Processado em {result['stats']['processing_seconds']:.1f}s")
                        print(f"   📊 {result['stats']['chunks']} chunks criados")
                        
                        if 'avaliacao' in result and doc_type == 'roteiro_criador':
                            print(f"   💀 Nota brutal: {result['avaliacao'].get('nota_geral', 62)}/100")
                        
                        processed += 1
                        
                    except Exception as e:
                        print(f"   ❌ Erro: {e}")
                        errors += 1
        
        print("="*60)
        print(f"\n📊 RESUMO:")
        print(f"   ✅ Processados com sucesso: {processed}")
        if errors > 0:
            print(f"   ❌ Erros: {errors}")
        print(f"\n✨ Sistema RAG está pronto para uso!")
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("\n💡 Certifique-se de que:")
        print("   1. O ambiente virtual está ativado")
        print("   2. As dependências foram instaladas")
        print("   3. Os arquivos do sistema RAG foram copiados")

if __name__ == "__main__":
    process_existing_pdfs()