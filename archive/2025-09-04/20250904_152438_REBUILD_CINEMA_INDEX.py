#!/usr/bin/env python3
"""
🎬 REBUILD CINEMA INDEX
Reconstrói o índice de cinema incluindo SONHOS SEM LEMBRANÇAS
"""

import json
import hashlib
from pathlib import Path

def rebuild_cinema_index():
    """Reconstrói índice de cinema com todos os PDFs"""
    
    print("🎬 RECONSTRUINDO ÍNDICE DE CINEMA")
    print("="*70)
    
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
    
    # Diretórios onde procurar PDFs
    pdf_dirs = [
        base_path / "data/pdfs",
        base_path / "data/cinema_knowledge/pdfs",
        base_path / "data/cinema_knowledge/pdfs/1_roteiros_famosos",
        base_path / "data/cinema_knowledge/pdfs/2_teoria_cinema", 
        base_path / "data/cinema_knowledge/pdfs/3_roteiros_criador",
        base_path / "data/cinema_knowledge/pdfs/4_manuais_escrita"
    ]
    
    index = {}
    total_pdfs = 0
    sonhos_found = False
    
    print("\n📁 Procurando PDFs em:")
    
    for pdf_dir in pdf_dirs:
        if pdf_dir.exists():
            print(f"  ✓ {pdf_dir.relative_to(base_path)}")
            
            # Procurar PDFs recursivamente
            for pdf_file in pdf_dir.rglob("*.pdf"):
                # Gerar ID único
                doc_id = hashlib.md5(str(pdf_file).encode()).hexdigest()[:12]
                
                # Adicionar ao índice
                index[doc_id] = {
                    "name": pdf_file.stem,
                    "path": str(pdf_file.relative_to(base_path)),
                    "size": pdf_file.stat().st_size,
                    "category": pdf_file.parent.name
                }
                
                total_pdfs += 1
                
                # Verificar se é SONHOS
                if "SONHOS" in pdf_file.name.upper():
                    sonhos_found = True
                    print(f"\n  🎯 SONHOS ENCONTRADO: {pdf_file.name}")
                    print(f"     Path: {pdf_file.relative_to(base_path)}")
                    print(f"     ID: {doc_id}")
        else:
            print(f"  ✗ {pdf_dir.relative_to(base_path)} (não existe)")
    
    # Adicionar TXTs importantes também
    txt_files = [
        base_path / "data/SONHOS_SEM_LEMBRANCAS.txt",
        base_path / "SONHOS_SEM_LEMBRANCAS.txt"
    ]
    
    print("\n📄 Procurando TXTs importantes:")
    for txt_file in txt_files:
        if txt_file.exists():
            doc_id = "txt_" + hashlib.md5(str(txt_file).encode()).hexdigest()[:8]
            
            index[doc_id] = {
                "name": txt_file.stem,
                "path": str(txt_file.relative_to(base_path)),
                "size": txt_file.stat().st_size,
                "category": "text",
                "type": "txt"
            }
            
            print(f"  ✓ {txt_file.name}")
    
    # Salvar índice
    index_path = base_path / "data/cinema_index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RESUMO:")
    print(f"  Total de documentos: {len(index)}")
    print(f"  PDFs: {total_pdfs}")
    print(f"  TXTs: {len(index) - total_pdfs}")
    print(f"  SONHOS SEM LEMBRANÇAS: {'✅ INCLUÍDO' if sonhos_found else '❌ NÃO ENCONTRADO'}")
    print(f"\n💾 Índice salvo em: {index_path}")
    
    # Verificar conteúdo do índice
    if sonhos_found:
        print("\n🔍 Entradas com SONHOS no índice:")
        for doc_id, info in index.items():
            if "SONHOS" in info["name"].upper():
                print(f"  - {info['name']}")
                print(f"    ID: {doc_id}")
                print(f"    Path: {info['path']}")
    
    return index_path

if __name__ == "__main__":
    rebuild_cinema_index()