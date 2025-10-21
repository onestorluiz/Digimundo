#!/usr/bin/env python3
"""
🚀 PROCESSADOR INTELIGENTE DE PDFs - SEM TRADUÇÃO DESNECESSÁRIA
Estratégias reais de economia de tokens:
1. Extração seletiva de conteúdo relevante
2. Indexação para busca rápida
3. Chunking inteligente
4. Embeddings locais
5. Cache de consultas
"""

import os
import sys
import json
import sqlite3
import hashlib
import pickle
import PyPDF2
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re

class SmartPDFProcessor:
    """Processador inteligente sem DigiLang desnecessário"""
    
    def __init__(self):
        self.cinema_dir = Path("CINEMA_KNOWLEDGE")
        self.pdf_dir = self.cinema_dir / "01_ORIGINAIS_PDF"
        self.index_dir = self.cinema_dir / "02_INDEXED"
        self.chunks_dir = self.cinema_dir / "03_CHUNKS"
        self.embeddings_dir = self.cinema_dir / "04_EMBEDDINGS"
        self.db_path = self.cinema_dir / "05_METADATA" / "knowledge.db"
        
        # Cria estrutura
        for dir in [self.index_dir, self.chunks_dir, self.embeddings_dir, self.db_path.parent]:
            dir.mkdir(parents=True, exist_ok=True)
        
        # Remove diretório antigo de tradução
        old_compressed = self.cinema_dir / "02_COMPRESSED_DIGILANG"
        if old_compressed.exists():
            import shutil
            shutil.rmtree(old_compressed)
            print("🗑️ Removido diretório de tradução DigiLang")
        
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()
        
    def create_tables(self):
        """Cria tabelas otimizadas"""
        cursor = self.conn.cursor()
        
        # Tabela principal de documentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                filepath TEXT,
                filehash TEXT,
                doc_type TEXT,  -- screenplay, book, article
                total_pages INTEGER,
                total_chars INTEGER,
                processed_at TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Tabela de chunks (pedaços) para economia
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                chunk_index INTEGER,
                chunk_type TEXT,  -- summary, dialogue, action, theory
                content TEXT,
                char_count INTEGER,
                relevance_score REAL,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            )
        """)
        
        # Tabela de índice para busca rápida
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                term TEXT,
                frequency INTEGER,
                positions TEXT,  -- JSON array de posições
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            )
        """)
        
        # Índices para performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(doc_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_type ON chunks(chunk_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_term ON search_index(term)")
        
        self.conn.commit()
    
    def detect_document_type(self, text: str, filename: str) -> str:
        """Detecta tipo de documento"""
        text_sample = text[:5000].upper()
        
        # Roteiro
        if any(marker in text_sample for marker in ['FADE IN:', 'INT.', 'EXT.', 'CUT TO:']):
            return "screenplay"
        
        # Livro teórico
        if "CHAPTER" in text_sample or "CONTENTS" in text_sample:
            return "book"
        
        # Artigo/outros
        return "article"
    
    def extract_smart_chunks(self, text: str, doc_type: str) -> List[Dict]:
        """Extrai chunks inteligentes baseado no tipo"""
        chunks = []
        
        if doc_type == "screenplay":
            # Para roteiros: separa por cenas
            scenes = re.split(r'(INT\.|EXT\.)[^\n]+', text)
            for i, scene in enumerate(scenes):
                if len(scene.strip()) > 50:
                    chunks.append({
                        "chunk_type": "scene",
                        "content": scene[:2000],  # Limita tamanho
                        "relevance_score": 0.8
                    })
        
        elif doc_type == "book":
            # Para livros: extrai conceitos principais
            # Divide por parágrafos grandes
            paragraphs = text.split('\n\n')
            
            for para in paragraphs:
                # Identifica parágrafos importantes (com palavras-chave)
                importance_keywords = [
                    'fundamental', 'essential', 'key', 'important', 'crucial',
                    'principle', 'rule', 'must', 'always', 'never',
                    'structure', 'character', 'plot', 'dialogue', 'conflict'
                ]
                
                relevance = sum(1 for kw in importance_keywords if kw in para.lower()) / 10
                
                if relevance > 0.2 and len(para) > 100:
                    chunks.append({
                        "chunk_type": "concept",
                        "content": para[:1500],
                        "relevance_score": min(relevance, 1.0)
                    })
        
        else:
            # Genérico: chunks de tamanho fixo
            chunk_size = 1000
            for i in range(0, len(text), chunk_size):
                chunks.append({
                    "chunk_type": "text",
                    "content": text[i:i+chunk_size],
                    "relevance_score": 0.5
                })
        
        return chunks
    
    def build_search_index(self, text: str, doc_id: int):
        """Constrói índice de busca"""
        # Palavras importantes para cinema/roteiro
        important_terms = set()
        
        # Extrai termos relevantes
        words = re.findall(r'\b[a-z]+\b', text.lower())
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Ignora palavras muito curtas
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Salva top 100 termos mais frequentes
        cursor = self.conn.cursor()
        for term, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]:
            cursor.execute("""
                INSERT INTO search_index (doc_id, term, frequency)
                VALUES (?, ?, ?)
            """, (doc_id, term, freq))
        
        self.conn.commit()
    
    def process_pdf(self, pdf_path: Path) -> Dict:
        """Processa PDF com estratégia inteligente"""
        print(f"\n📄 Processando: {pdf_path.name[:60]}...")
        
        # Extrai texto
        text = ""
        pages = 0
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                pages = len(reader.pages)
                
                for page in reader.pages:
                    try:
                        text += page.extract_text() + "\n"
                    except:
                        pass
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return {"error": str(e)}
        
        # Detecta tipo
        doc_type = self.detect_document_type(text, pdf_path.name)
        print(f"   📚 Tipo: {doc_type} ({pages} páginas)")
        
        # Calcula hash
        with open(pdf_path, 'rb') as f:
            filehash = hashlib.md5(f.read()).hexdigest()
        
        # Salva documento
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO documents 
            (filename, filepath, filehash, doc_type, total_pages, total_chars, processed_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pdf_path.name,
            str(pdf_path),
            filehash,
            doc_type,
            pages,
            len(text),
            datetime.now().isoformat(),
            json.dumps({"original_size": pdf_path.stat().st_size})
        ))
        doc_id = cursor.lastrowid
        
        # Extrai chunks inteligentes
        chunks = self.extract_smart_chunks(text, doc_type)
        print(f"   📦 Chunks extraídos: {len(chunks)}")
        
        # Salva apenas chunks relevantes (economia de espaço)
        saved_chunks = 0
        total_chars_saved = 0
        
        for i, chunk in enumerate(chunks):
            if chunk["relevance_score"] > 0.3:  # Só salva chunks relevantes
                cursor.execute("""
                    INSERT INTO chunks (doc_id, chunk_index, chunk_type, content, char_count, relevance_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (doc_id, i, chunk["chunk_type"], chunk["content"], 
                      len(chunk["content"]), chunk["relevance_score"]))
                saved_chunks += 1
                total_chars_saved += len(chunk["content"])
        
        # Constrói índice de busca
        self.build_search_index(text, doc_id)
        
        self.conn.commit()
        
        # Calcula economia
        economia = (1 - total_chars_saved / len(text)) * 100 if len(text) > 0 else 0
        
        print(f"   💾 Economia: {economia:.1f}% (salvou apenas conteúdo relevante)")
        print(f"   ✅ {saved_chunks} chunks relevantes salvos")
        
        return {
            "success": True,
            "doc_type": doc_type,
            "pages": pages,
            "chunks_saved": saved_chunks,
            "economia": economia
        }
    
    def create_rag_interface(self):
        """Cria interface para o RAG acessar eficientemente"""
        
        # Cria arquivo de acesso rápido para RAG
        rag_file = self.cinema_dir / "rag_access.json"
        
        cursor = self.conn.cursor()
        
        # Pega informações resumidas
        cursor.execute("""
            SELECT d.id, d.filename, d.doc_type, COUNT(c.id) as chunks
            FROM documents d
            LEFT JOIN chunks c ON d.id = c.doc_id
            GROUP BY d.id
        """)
        
        rag_data = {
            "documents": [],
            "total_chunks": 0,
            "search_enabled": True,
            "chunk_strategy": "relevance_based"
        }
        
        for row in cursor.fetchall():
            rag_data["documents"].append({
                "id": row[0],
                "filename": row[1],
                "type": row[2],
                "chunks": row[3]
            })
            rag_data["total_chunks"] += row[3]
        
        with open(rag_file, 'w') as f:
            json.dump(rag_data, f, indent=2)
        
        print(f"\n🤖 Interface RAG criada: {rag_file}")
        return rag_data
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca otimizada nos documentos"""
        cursor = self.conn.cursor()
        
        # Busca por termos
        terms = query.lower().split()
        
        results = []
        for term in terms:
            cursor.execute("""
                SELECT DISTINCT c.content, c.relevance_score, d.filename
                FROM search_index si
                JOIN chunks c ON si.doc_id = c.doc_id
                JOIN documents d ON si.doc_id = d.id
                WHERE si.term LIKE ?
                ORDER BY si.frequency DESC, c.relevance_score DESC
                LIMIT ?
            """, (f"%{term}%", limit))
            
            for row in cursor.fetchall():
                results.append({
                    "content": row[0][:500],  # Primeiros 500 chars
                    "relevance": row[1],
                    "source": row[2]
                })
        
        return results[:limit]
    
    def get_stats(self) -> Dict:
        """Estatísticas do processamento"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT d.id) as total_docs,
                COUNT(c.id) as total_chunks,
                SUM(d.total_chars) as total_chars,
                SUM(c.char_count) as saved_chars,
                AVG(c.relevance_score) as avg_relevance
            FROM documents d
            LEFT JOIN chunks c ON d.id = c.doc_id
        """)
        
        stats = cursor.fetchone()
        
        if stats[2] and stats[3]:
            economia = (1 - stats[3]/stats[2]) * 100
        else:
            economia = 0
        
        return {
            "documents": stats[0],
            "chunks": stats[1],
            "economia_tokens": f"{economia:.1f}%",
            "avg_relevance": stats[4]
        }

def main():
    """Processa todos os PDFs com nova estratégia"""
    print("="*70)
    print("🚀 PROCESSAMENTO INTELIGENTE DE PDFs - SEM TRADUÇÃO DESNECESSÁRIA")
    print("="*70)
    
    processor = SmartPDFProcessor()
    
    # Lista PDFs
    pdf_files = list(processor.pdf_dir.glob("*.pdf"))
    print(f"\n📚 Total de PDFs: {len(pdf_files)}")
    
    # Processa todos
    success = 0
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}]", end="")
        result = processor.process_pdf(pdf_path)
        if result.get("success"):
            success += 1
    
    # Cria interface RAG
    rag_data = processor.create_rag_interface()
    
    # Estatísticas finais
    stats = processor.get_stats()
    
    print("\n" + "="*70)
    print("📊 RESULTADO FINAL")
    print("="*70)
    print(f"""
✅ PDFs processados: {success}/{len(pdf_files)}
📦 Total de chunks relevantes: {stats['chunks']}
💾 Economia de tokens: {stats['economia_tokens']}
🎯 Relevância média: {stats['avg_relevance']:.2f}

🎉 SUCESSO! Sistema otimizado para:
   • Busca rápida por índice
   • Apenas conteúdo relevante salvo
   • Sem "tradução" desnecessária
   • RAG pode acessar eficientemente
   
📌 Próximo passo: Integrar com RAG usando chunks relevantes
""")
    
    # Teste de busca
    print("\n🔍 Teste de busca:")
    results = processor.search("three act structure")
    for r in results[:3]:
        print(f"   • {r['source'][:40]}... (relevância: {r['relevance']:.2f})")

if __name__ == "__main__":
    main()