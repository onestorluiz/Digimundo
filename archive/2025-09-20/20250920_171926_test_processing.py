#!/usr/bin/env python3
"""
Script de teste para processar apenas alguns PDFs
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.processing.pipeline import process_pdf

# Processar apenas 3 PDFs para teste
test_pdfs = [
    ("cinema/2_roteiros_mestres/Chinatown - Screenplay.pdf", "roteiro_mestre"),
    ("cinema/3_roteiros_criador/SONHOS SEM LEMBRANÇAS T.3.pdf", "roteiro_criador"),
    ("cinema/1_teoria_roteiro/The Departed - Scriptment.pdf", "teoria_roteiro")
]

print("🧪 Teste de processamento RAG - Scripturemon")
print("=" * 50)

for pdf_path, doc_type in test_pdfs:
    pdf_full = Path(__file__).parent.parent / pdf_path
    if pdf_full.exists():
        print(f"\n📄 Processando: {pdf_full.name}")
        print(f"   Tipo: {doc_type}")
        
        try:
            result = process_pdf(str(pdf_full), doc_type=doc_type)
            print(f"   ✅ Sucesso!")
            print(f"   ⏱️  {result['stats']['processing_seconds']:.1f}s")
            print(f"   📊 {result['stats']['chunks']} chunks")
            if 'avaliacao' in result:
                print(f"   💀 Nota: {result['avaliacao'].get('nota_geral', 62)}/100")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    else:
        print(f"   ⚠️  Arquivo não encontrado")

print("\n" + "=" * 50)
print("✅ Teste concluído!")
print("\n💡 Use o endpoint http://localhost:8092/knowledge/search?query=roteiro")
print("   para testar a busca no conhecimento processado")