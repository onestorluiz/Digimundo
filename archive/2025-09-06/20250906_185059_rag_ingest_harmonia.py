#!/usr/bin/env python3
"""
RAG Ingest Magistral - HARMONIA V3.2
Sistema completo de ingestão com chunking inteligente
"""

import os
import sys
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.pdf_utils import extract_text, get_pdf_metadata
from src.rag.chunking import smart_chunk
from src.rag.adapter import RAGAdapter, SCHEMA_KEYS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("harmonia.rag_ingest")


class MagistralIngester:
    """Sistema magistral de ingestão RAG."""
    
    def __init__(self):
        self.adapter = RAGAdapter({'rag': {'enabled': True, 'provider': 'chroma'}})
        self.stats = {
            'docs_total': 0,
            'indexed_files': 0,
            'total_chunks': 0,
            'duplicates': 0,
            'errors': [],
            'deviation': None
        }
        
    def compute_doc_hash(self, file_path: Path) -> str:
        """Calcula hash único do documento."""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:12]
    
    def intelligent_chunking(self, text: str, filename: str) -> List[Dict]:
        """
        Chunking inteligente baseado no tipo de documento.
        
        - Roteiros: detecta INT./EXT. como âncoras
        - Teóricos: detecta capítulos/seções
        """
        chunks = []
        
        # Detectar tipo de documento
        is_screenplay = any(keyword in filename.lower() for keyword in 
                          ['screenplay', 'script', 'draft', 'release'])
        
        if is_screenplay:
            # Chunking para roteiros: âncoras em cenas
            logger.info(f"Usando chunking de ROTEIRO para {filename}")
            
            # Buscar marcadores de cena
            scene_markers = []
            lines = text.split('\n')
            for i, line in enumerate(lines):
                upper_line = line.strip().upper()
                if (upper_line.startswith('INT.') or 
                    upper_line.startswith('EXT.') or
                    upper_line.startswith('INT ') or
                    upper_line.startswith('EXT ')):
                    scene_markers.append(i)
            
            # Criar chunks baseados em cenas
            if scene_markers:
                for i in range(len(scene_markers)):
                    start_idx = scene_markers[i]
                    end_idx = scene_markers[i+1] if i+1 < len(scene_markers) else len(lines)
                    
                    # Incluir overlap de contexto
                    overlap_start = max(0, start_idx - 5)
                    overlap_end = min(len(lines), end_idx + 5)
                    
                    chunk_lines = lines[overlap_start:overlap_end]
                    chunk_text = '\n'.join(chunk_lines)
                    
                    if len(chunk_text) > 100:  # Mínimo de conteúdo
                        chunks.append({
                            'text': chunk_text,
                            'chunk_no': len(chunks),
                            'type': 'scene',
                            'anchor': lines[start_idx][:50]
                        })
            
        else:
            # Chunking para textos teóricos: detectar capítulos
            logger.info(f"Usando chunking TEÓRICO para {filename}")
            
            # Buscar cabeçalhos (Chapter, CHAPTER, números romanos, etc)
            import re
            chapter_pattern = re.compile(
                r'^(CHAPTER|Chapter|CAPÍTULO|Part|PART|Section|SECTION|\d+\.|[IVX]+\.)',
                re.MULTILINE
            )
            
            matches = list(chapter_pattern.finditer(text))
            
            if matches:
                for i in range(len(matches)):
                    start = matches[i].start()
                    end = matches[i+1].start() if i+1 < len(matches) else len(text)
                    
                    chunk_text = text[start:end]
                    if len(chunk_text) > 100:
                        chunks.append({
                            'text': chunk_text,
                            'chunk_no': len(chunks),
                            'type': 'chapter',
                            'anchor': matches[i].group()
                        })
        
        # Fallback: chunking padrão se não detectou estrutura
        if not chunks:
            logger.info(f"Usando chunking PADRÃO para {filename}")
            base_chunks = smart_chunk(text, chunk_size=1000, overlap=120)
            for i, chunk_data in enumerate(base_chunks):
                chunks.append({
                    'text': chunk_data.get('text', ''),
                    'chunk_no': i,
                    'type': 'standard',
                    'anchor': None
                })
        
        # Limpar headers/footers simples
        for chunk in chunks:
            lines = chunk['text'].split('\n')
            # Remover linhas que parecem headers/footers
            filtered_lines = []
            for line in lines:
                # Skip page numbers, dates, headers comuns
                if not (line.strip().isdigit() or 
                       'Page' in line and any(c.isdigit() for c in line) or
                       line.strip().startswith('©') or
                       len(line.strip()) < 3):
                    filtered_lines.append(line)
            
            chunk['text'] = '\n'.join(filtered_lines)
        
        return chunks
    
    def ingest_directory(self, directory: Path) -> Dict[str, Any]:
        """Ingere todos os PDFs de um diretório."""
        pdf_files = list(directory.glob('*.pdf'))
        self.stats['docs_total'] = len(pdf_files)
        
        logger.info(f"Iniciando ingestão de {len(pdf_files)} PDFs de {directory}")
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Processando: {pdf_file.name}")
                
                # Extrair texto
                text = extract_text(pdf_file)
                
                # Skip stubs
                if len(text) < 500 or text.startswith('[PDF Content:'):
                    logger.warning(f"Pulando stub: {pdf_file.name}")
                    continue
                
                # Chunking inteligente
                chunks = self.intelligent_chunking(text, pdf_file.name)
                
                # Hash do documento
                doc_hash = self.compute_doc_hash(pdf_file)
                
                # Verificar duplicatas
                existing = self.adapter.chroma_collection.get(
                    where={'doc_hash': doc_hash},
                    limit=1
                )
                
                if existing and existing.get('ids'):
                    logger.info(f"Documento já indexado: {pdf_file.name}")
                    self.stats['duplicates'] += 1
                    continue
                
                # Adicionar chunks ao índice
                chunks_added = 0
                for chunk in chunks:
                    # Garantir SCHEMA_KEYS completas
                    metadata = {
                        'source': pdf_file.name,
                        'path': str(pdf_file),
                        'doc_hash': doc_hash,
                        'mtime': int(pdf_file.stat().st_mtime),
                        'chunk_no': chunk['chunk_no'],
                        'total_chunks': len(chunks),
                        'type': chunk.get('type', 'standard'),
                        'lang': 'en'
                    }
                    
                    # Verificar que todas as SCHEMA_KEYS estão presentes
                    for key in SCHEMA_KEYS:
                        if key not in metadata:
                            metadata[key] = 'unknown'
                    
                    # Criar ID determinístico
                    chunk_id = f"{doc_hash}#c{chunk['chunk_no']}"
                    
                    # Adicionar ao ChromaDB
                    self.adapter.chroma_collection.add(
                        ids=[chunk_id],
                        documents=[chunk['text']],
                        metadatas=[metadata]
                    )
                    
                    chunks_added += 1
                
                self.stats['indexed_files'] += 1
                self.stats['total_chunks'] += chunks_added
                
                logger.info(f"✅ {pdf_file.name}: {chunks_added} chunks indexados")
                
            except Exception as e:
                logger.error(f"❌ Erro em {pdf_file.name}: {e}")
                self.stats['errors'].append({
                    'file': pdf_file.name,
                    'error': str(e)
                })
        
        return self.stats
    
    def verify_alignment(self) -> Dict[str, Any]:
        """Verifica alinhamento do sistema RAG."""
        alignment = {
            'adapter_backend': 'chroma',
            'collection_adapter': None,
            'collection_tooling': 'v3_1_docs',
            'schema_ok': False,
            'missing_keys': []
        }
        
        # Verificar coleção
        if self.adapter.chroma_collection:
            alignment['collection_adapter'] = self.adapter.chroma_collection.name
            
            # Verificar schema em amostra
            sample = self.adapter.chroma_collection.get(limit=1)
            if sample and sample.get('metadatas'):
                meta = sample['metadatas'][0]
                missing = [key for key in SCHEMA_KEYS if key not in meta]
                alignment['missing_keys'] = missing
                alignment['schema_ok'] = len(missing) == 0
        
        return alignment
    
    def generate_citations(self, num_samples: int = 6) -> List[Dict]:
        """Gera amostras de citações."""
        citations = []
        
        test_queries = [
            "three act structure",
            "character development", 
            "dialogue techniques",
            "cinematography",
            "plot twist",
            "emotional arc",
            "screenplay format",
            "visual storytelling"
        ]
        
        for query in test_queries[:num_samples]:
            try:
                results = self.adapter.retrieve(query, k=1)
                if results:
                    doc = results[0]
                    meta = doc.get('metadata', {})
                    
                    # Formatar citação
                    source = meta.get('source', 'unknown')
                    chunk_no = meta.get('chunk_no', 0)
                    total_chunks = meta.get('total_chunks', 1)
                    
                    # Remover .pdf da fonte
                    if source.endswith('.pdf'):
                        source = source[:-4]
                    
                    citation = {
                        'query': query,
                        'citation': f"{source} · c{chunk_no}/{total_chunks}",
                        'has_metadata': bool(meta),
                        'text_preview': doc.get('text', '')[:100] + '...'
                    }
                    
                    citations.append(citation)
                    
            except Exception as e:
                logger.error(f"Erro ao gerar citação para '{query}': {e}")
        
        return citations


def main():
    """Executa ingestão magistral completa."""
    
    # Inicializar
    ingester = MagistralIngester()
    
    # Determinar diretório de PDFs
    priority_dir = Path("03_MEMORY/01_ORIGINAIS_PDF")
    fallback_dir = Path("data/cinema_knowledge/01_ORIGINAIS_PDF")
    
    if priority_dir.exists():
        pdf_dir = priority_dir
        logger.info(f"Usando diretório PRIORITÁRIO: {priority_dir}")
    else:
        pdf_dir = fallback_dir
        ingester.stats['deviation'] = f"Using fallback directory: {fallback_dir}"
        logger.warning(f"Usando diretório FALLBACK: {fallback_dir}")
    
    # Executar ingestão
    stats = ingester.ingest_directory(pdf_dir)
    
    # Verificar alinhamento
    alignment = ingester.verify_alignment()
    
    # Gerar citações
    citations = ingester.generate_citations(6)
    
    # Estatísticas de chunking
    chunking_stats = {
        'total_documents': stats['docs_total'],
        'successfully_chunked': stats['indexed_files'],
        'total_chunks': stats['total_chunks'],
        'avg_chunks_per_doc': (
            stats['total_chunks'] / stats['indexed_files'] 
            if stats['indexed_files'] > 0 else 0
        ),
        'chunking_methods_used': ['scene', 'chapter', 'standard'],
        'overlap_size': 120
    }
    
    # Salvar relatórios
    output_dir = Path("reports/harmonia_v32/rag")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Index report
    with open(output_dir / "index_report.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'docs_total': stats['docs_total'],
            'indexed_files': stats['indexed_files'],
            'total_chunks': stats['total_chunks'],
            'duplicates': stats['duplicates'],
            'schema_ok': alignment['schema_ok'],
            'errors': stats['errors'],
            'deviation': stats['deviation']
        }, f, indent=2)
    
    # Alignment report
    with open(output_dir / "alignment.json", 'w') as f:
        json.dump(alignment, f, indent=2)
    
    # Citations report
    with open(output_dir / "cite_samples.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'num_samples': len(citations),
            'samples': citations
        }, f, indent=2)
    
    # Chunking stats
    with open(output_dir / "chunking_stats.json", 'w') as f:
        json.dump(chunking_stats, f, indent=2)
    
    logger.info(f"✅ Ingestão completa! {stats['indexed_files']} arquivos, {stats['total_chunks']} chunks")
    return stats


if __name__ == "__main__":
    main()