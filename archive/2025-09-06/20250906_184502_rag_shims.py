"""
RAG Shims - Camada de compatibilidade para RAGAdapter
HARMONIA V3.2 - Preservando o conhecimento cinematográfico
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path
import hashlib
import logging

logger = logging.getLogger("harmonia.rag_shims")


class RAGShims:
    """Shims para compatibilidade com RAGAdapter."""
    
    def __init__(self, adapter):
        """
        Inicializa shims com referência ao adapter.
        
        Args:
            adapter: Instância de RAGAdapter
        """
        self.adapter = adapter
        
        # Diretório prioritário de PDFs
        self.pdf_priority_dir = Path("03_MEMORY/01_ORIGINAIS_PDF")
        self.pdf_fallback_dir = Path("data/cinema_knowledge/01_ORIGINAIS_PDF")
    
    def ingest(self, file_path: Optional[str] = None, 
               directory: Optional[str] = None,
               recursive: bool = True) -> Dict[str, Any]:
        """
        Shim: ingest -> add_document (batch)
        Ingere documentos no sistema RAG.
        
        Args:
            file_path: Arquivo específico para ingerir
            directory: Diretório para ingerir
            recursive: Se deve buscar recursivamente
            
        Returns:
            Relatório de ingestão
        """
        report = {
            'status': 'started',
            'files_processed': 0,
            'chunks_created': 0,
            'errors': [],
            'deviation': None
        }
        
        # Determinar fonte de PDFs
        if file_path:
            files_to_process = [Path(file_path)]
        elif directory:
            dir_path = Path(directory)
            if not dir_path.exists():
                report['errors'].append(f"Directory not found: {directory}")
                report['status'] = 'failed'
                return report
            pattern = "**/*.pdf" if recursive else "*.pdf"
            files_to_process = list(dir_path.glob(pattern))
        else:
            # Usar diretório prioritário
            if self.pdf_priority_dir.exists():
                files_to_process = list(self.pdf_priority_dir.glob("*.pdf"))
                logger.info(f"Usando diretório prioritário: {self.pdf_priority_dir}")
            elif self.pdf_fallback_dir.exists():
                files_to_process = list(self.pdf_fallback_dir.glob("*.pdf"))
                report['deviation'] = f"Using fallback directory: {self.pdf_fallback_dir}"
                logger.warning(f"Usando fallback: {self.pdf_fallback_dir}")
            else:
                report['errors'].append("No PDF directory found")
                report['status'] = 'failed'
                return report
        
        # Processar cada arquivo
        for pdf_file in files_to_process:
            try:
                # Extrair texto do PDF
                from src.rag.pdf_utils import extract_text, get_pdf_metadata
                from src.rag.chunking import smart_chunk
                
                text = extract_text(pdf_file)
                metadata = get_pdf_metadata(pdf_file)
                
                # Chunking inteligente
                chunks = smart_chunk(text, chunk_size=1000, overlap=120)
                
                # Calcular hash do documento
                with open(pdf_file, 'rb') as f:
                    doc_hash = hashlib.sha256(f.read()).hexdigest()[:12]
                
                # Adicionar cada chunk
                for i, chunk_data in enumerate(chunks):
                    chunk_metadata = {
                        'source': pdf_file.name,
                        'path': str(pdf_file),
                        'doc_hash': doc_hash,
                        'mtime': int(pdf_file.stat().st_mtime),
                        'chunk_no': i,
                        'total_chunks': len(chunks),
                        'type': 'screenplay' if 'screenplay' in pdf_file.name.lower() else 'pdf',
                        'lang': 'en'
                    }
                    
                    # Adicionar ao adapter
                    success = self.adapter.add_document(
                        text=chunk_data.get('text', ''),
                        metadata=chunk_metadata
                    )
                    
                    if success:
                        report['chunks_created'] += 1
                
                report['files_processed'] += 1
                logger.info(f"✅ Ingerido: {pdf_file.name} ({len(chunks)} chunks)")
                
            except Exception as e:
                report['errors'].append(f"{pdf_file.name}: {str(e)}")
                logger.error(f"❌ Erro ao ingerir {pdf_file.name}: {e}")
        
        report['status'] = 'completed' if report['files_processed'] > 0 else 'failed'
        return report
    
    def batch_add(self, documents: List[Dict[str, Any]]) -> int:
        """
        Adiciona múltiplos documentos em batch.
        
        Args:
            documents: Lista de documentos com 'text' e 'metadata'
            
        Returns:
            Número de documentos adicionados com sucesso
        """
        added = 0
        for doc in documents:
            try:
                success = self.adapter.add_document(
                    text=doc.get('text', ''),
                    metadata=doc.get('metadata', {})
                )
                if success:
                    added += 1
            except Exception as e:
                logger.error(f"Erro ao adicionar documento: {e}")
        
        return added


def install_rag_shims(adapter):
    """
    Instala shims no RAGAdapter.
    
    Args:
        adapter: Instância de RAGAdapter
        
    Returns:
        Adapter com shims instalados
    """
    shims = RAGShims(adapter)
    
    # Adicionar método ingest
    if not hasattr(adapter, 'ingest'):
        adapter.ingest = shims.ingest
    
    # Adicionar batch_add
    if not hasattr(adapter, 'batch_add'):
        adapter.batch_add = shims.batch_add
    
    logger.info("✅ RAG shims instalados - ingest disponível")
    
    return adapter