#!/usr/bin/env python3
"""
📊 VERIFICADOR COMPLETO DO STATUS DOS PDFs
"""

import sqlite3
from pathlib import Path
import PyPDF2

def check_pdf_processing_status():
    """Verifica status completo do processamento"""
    
    cinema_dir = Path("CINEMA_KNOWLEDGE")
    pdf_dir = cinema_dir / "01_ORIGINAIS_PDF"
    compressed_dir = cinema_dir / "02_COMPRESSED_DIGILANG"
    db_path = cinema_dir / "03_METADATA" / "cinema_knowledge.db"
    
    print("=" * 70)
    print("📊 STATUS COMPLETO DO PROCESSAMENTO DE PDFs")
    print("=" * 70)
    
    # 1. Contar PDFs originais
    pdf_files = list(pdf_dir.glob("*.pdf"))
    print(f"\n📚 PDFs ORIGINAIS: {len(pdf_files)}")
    
    # 2. Contar páginas totais dos PDFs
    total_pages = 0
    pages_by_pdf = {}
    
    print("\n📖 CONTANDO PÁGINAS DOS PDFs...")
    for i, pdf_path in enumerate(pdf_files[:10], 1):  # Primeiros 10 para amostra
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = len(reader.pages)
                total_pages += pages
                pages_by_pdf[pdf_path.name] = pages
                print(f"   {i}. {pdf_path.name[:50]}... = {pages} páginas")
        except Exception as e:
            print(f"   ❌ Erro em {pdf_path.name}: {e}")
    
    print(f"\n📄 Total de páginas (amostra de 10): {total_pages}")
    
    # 3. Verificar arquivos comprimidos
    compressed_files = list(compressed_dir.glob("*.txt"))
    print(f"\n🗜️ ARQUIVOS COMPRIMIDOS: {len(compressed_files)}")
    
    # 4. Analisar banco de dados
    print("\n💾 BANCO DE DADOS:")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM documents")
    total_docs = cursor.fetchone()[0]
    print(f"   Total de documentos: {total_docs}")
    
    # Analisar compressão
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN compression_rate > 0 THEN 1 ELSE 0 END) as positive,
            SUM(CASE WHEN compression_rate <= 0 THEN 1 ELSE 0 END) as negative,
            AVG(compression_rate) as avg_rate,
            SUM(original_size) as total_orig,
            SUM(compressed_size) as total_comp
        FROM documents
    """)
    
    stats = cursor.fetchone()
    if stats[4] and stats[5]:
        real_compression = (1 - stats[5]/stats[4]) * 100
    else:
        real_compression = 0
    
    print(f"   Com compressão positiva: {stats[1]}")
    print(f"   Com compressão negativa: {stats[2]}")
    print(f"   Taxa média registrada: {stats[3]*100:.1f}%")
    print(f"   Taxa REAL de compressão: {real_compression:.1f}%")
    
    # 5. Verificar sincronização
    print("\n🔗 SINCRONIZAÇÃO:")
    
    # PDFs processados vs registrados
    cursor.execute("SELECT filename FROM documents")
    db_files = {row[0] for row in cursor.fetchall()}
    pdf_names = {p.name for p in pdf_files}
    
    processed = db_files & pdf_names
    not_processed = pdf_names - db_files
    
    print(f"   ✅ Processados e sincronizados: {len(processed)}")
    print(f"   ⏳ Aguardando processamento: {len(not_processed)}")
    
    if len(not_processed) > 0:
        print("\n   📝 PDFs não processados (primeiros 10):")
        for i, name in enumerate(list(not_processed)[:10], 1):
            print(f"      {i}. {name[:60]}...")
    
    # 6. Verificar integração com RAG
    print("\n🤖 INTEGRAÇÃO COM SISTEMA RAG:")
    
    # Verifica link simbólico
    rag_link = Path("data/cinema_knowledge")
    if rag_link.exists():
        print(f"   ✅ Link simbólico existe: {rag_link} -> {rag_link.resolve()}")
    else:
        print(f"   ❌ Link simbólico NÃO existe em data/cinema_knowledge")
    
    # Verifica se RAG pode ler
    try:
        import sys
        sys.path.insert(0, str(Path.cwd()))
        from apps.scripturemon.rag_advanced import AdvancedRAG
        rag = AdvancedRAG()
        print(f"   ✅ RAG inicializado com {len(rag.knowledge_base)} documentos base")
    except Exception as e:
        print(f"   ❌ RAG não pode ser inicializado: {e}")
    
    # 7. Resumo final
    print("\n" + "=" * 70)
    print("📊 RESUMO EXECUTIVO")
    print("=" * 70)
    
    completion = (len(processed) / len(pdf_files)) * 100 if pdf_files else 0
    
    status_emoji = "✅" if completion >= 90 else "⚠️" if completion >= 50 else "❌"
    
    print(f"""
{status_emoji} Status Geral: {completion:.1f}% completo

📚 Total de PDFs: {len(pdf_files)}
✅ Processados: {len(processed)}
⏳ Pendentes: {len(not_processed)}
🗜️ Arquivos comprimidos: {len(compressed_files)}
💾 Registros no banco: {total_docs}
📊 Taxa de compressão real: {real_compression:.1f}%

{'⚠️ PROBLEMA: Compressão negativa! Os arquivos estão MAIORES depois do processamento.' if real_compression < 0 else ''}
{'✅ Compressão funcionando corretamente.' if real_compression > 10 else ''}
    """)
    
    conn.close()
    
    return {
        "total_pdfs": len(pdf_files),
        "processed": len(processed),
        "pending": len(not_processed),
        "compression_rate": real_compression,
        "completion": completion
    }

if __name__ == "__main__":
    check_pdf_processing_status()