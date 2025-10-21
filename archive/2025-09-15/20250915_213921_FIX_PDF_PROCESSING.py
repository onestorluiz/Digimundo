#!/usr/bin/env python3
"""
🔧 CORRETOR DO PROCESSAMENTO DE PDFs
Reprocessa os PDFs com compressão efetiva e integração completa
"""

import os
import sys
import sqlite3
import hashlib
import zlib
import base64
from pathlib import Path
from datetime import datetime
import PyPDF2
from typing import Dict, Tuple, List

# Adiciona diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importa DigiLang melhorado
from src.digilang.api_fallback_improved import to_digilang, from_digilang

class PDFProcessorFixed:
    """Processador de PDFs corrigido com compressão real"""
    
    def __init__(self):
        self.cinema_dir = Path("CINEMA_KNOWLEDGE")
        self.pdf_dir = self.cinema_dir / "01_ORIGINAIS_PDF"
        self.compressed_dir = self.cinema_dir / "02_COMPRESSED_DIGILANG"
        self.metadata_dir = self.cinema_dir / "03_METADATA"
        self.db_path = self.metadata_dir / "cinema_knowledge.db"
        
        # Cria diretórios
        self.compressed_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # Conecta ao banco
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()
        
        # Estatísticas
        self.stats = {
            "total_pdfs": 0,
            "processed": 0,
            "total_pages": 0,
            "compression_improved": 0,
            "total_original_size": 0,
            "total_compressed_size": 0
        }
    
    def create_tables(self):
        """Cria tabelas melhoradas no banco"""
        cursor = self.conn.cursor()
        
        # Tabela principal com campos adicionais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                original_path TEXT,
                compressed_path TEXT,
                file_hash TEXT,
                total_pages INTEGER,
                processed_pages INTEGER,
                original_size INTEGER,
                compressed_size INTEGER,
                compression_rate REAL,
                compression_method TEXT,
                tokens_saved INTEGER,
                processed_at TIMESTAMP,
                metadata TEXT
            )
        """)
        
        self.conn.commit()
    
    def extract_pdf_text(self, pdf_path: Path) -> Tuple[str, int]:
        """Extrai texto completo do PDF
        
        Returns:
            (texto_completo, número_de_páginas)
        """
        text = ""
        pages = 0
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                pages = len(reader.pages)
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n\n--- PÁGINA {page_num + 1} ---\n\n"
                            text += page_text
                    except:
                        text += f"\n\n--- PÁGINA {page_num + 1}: ERRO NA EXTRAÇÃO ---\n\n"
                
        except Exception as e:
            print(f"❌ Erro ao ler {pdf_path.name}: {e}")
            return "", 0
        
        return text, pages
    
    def compress_smart(self, text: str, filename: str) -> Tuple[str, float, str]:
        """Compressão inteligente baseada no tipo de conteúdo
        
        Returns:
            (texto_comprimido, taxa_de_compressão, método_usado)
        """
        original_size = len(text)
        
        # Detecta tipo de conteúdo
        is_screenplay = any(marker in text.upper()[:5000] for marker in 
                          ['FADE IN:', 'INT.', 'EXT.', 'CUT TO:', '(CONT\'D)'])
        
        if is_screenplay:
            # Usa DigiLang para roteiros
            compressed, ratio = to_digilang(text, mode="screenplay")
            method = "digilang_screenplay"
            
        elif len(text) > 10000:
            # Para textos longos (livros), usa ZLIB + chunking
            try:
                # Divide em chunks para melhor compressão
                chunks = []
                chunk_size = 50000  # 50KB chunks
                
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size]
                    
                    # Tenta DigiLang primeiro
                    digilang_chunk, digilang_ratio = to_digilang(chunk, mode="aggressive")
                    
                    if digilang_ratio < 0.9:  # Se comprimir pelo menos 10%
                        chunks.append(f"DL:{digilang_chunk}")
                    else:
                        # Senão, usa ZLIB
                        zlib_chunk = zlib.compress(chunk.encode('utf-8'), level=9)
                        b64_chunk = base64.b64encode(zlib_chunk).decode('ascii')
                        chunks.append(f"Z:{b64_chunk}")
                
                compressed = "\n|||CHUNK|||\n".join(chunks)
                ratio = len(compressed) / original_size
                method = "hybrid_chunked"
                
            except:
                # Fallback para ZLIB simples
                compressed_bytes = zlib.compress(text.encode('utf-8'), level=9)
                compressed = base64.b64encode(compressed_bytes).decode('ascii')
                ratio = len(compressed) / original_size
                method = "zlib_base64"
        
        else:
            # Textos pequenos: DigiLang agressivo
            compressed, ratio = to_digilang(text, mode="aggressive")
            method = "digilang_aggressive"
        
        # Se ainda não comprimiu, usa ZLIB
        if ratio >= 1.0:
            compressed_bytes = zlib.compress(text.encode('utf-8'), level=9)
            compressed = base64.b64encode(compressed_bytes).decode('ascii')
            ratio = len(compressed) / original_size
            method = "zlib_fallback"
        
        return compressed, ratio, method
    
    def process_pdf(self, pdf_path: Path) -> Dict:
        """Processa um PDF individual"""
        print(f"\n📄 Processando: {pdf_path.name}")
        
        # Extrai texto
        text, pages = self.extract_pdf_text(pdf_path)
        if not text:
            return {"error": "Não foi possível extrair texto"}
        
        print(f"   📖 Páginas: {pages}")
        print(f"   📝 Texto extraído: {len(text)} caracteres")
        
        # Comprime
        compressed, ratio, method = self.compress_smart(text, pdf_path.name)
        
        # Calcula estatísticas
        original_size = len(text)
        compressed_size = len(compressed)
        compression_rate = 1 - ratio
        tokens_saved = max(0, (original_size - compressed_size) // 4)
        
        print(f"   🗜️ Método: {method}")
        print(f"   📊 Taxa de compressão: {compression_rate*100:.1f}%")
        
        # Salva arquivo comprimido
        output_path = self.compressed_dir / f"{pdf_path.stem}_compressed.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(compressed)
        
        # Calcula hash
        with open(pdf_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        # Salva no banco
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO documents_v2 
            (filename, original_path, compressed_path, file_hash, 
             total_pages, processed_pages, original_size, compressed_size, 
             compression_rate, compression_method, tokens_saved, processed_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pdf_path.name,
            str(pdf_path),
            str(output_path),
            file_hash,
            pages,
            pages,  # Processamos todas as páginas
            original_size,
            compressed_size,
            compression_rate,
            method,
            tokens_saved,
            datetime.now().isoformat(),
            f'{{"type": "{"screenplay" if "screenplay" in method else "book"}"}}'
        ))
        self.conn.commit()
        
        # Atualiza estatísticas
        self.stats["processed"] += 1
        self.stats["total_pages"] += pages
        self.stats["total_original_size"] += original_size
        self.stats["total_compressed_size"] += compressed_size
        if compression_rate > 0:
            self.stats["compression_improved"] += 1
        
        return {
            "success": True,
            "pages": pages,
            "compression_rate": compression_rate,
            "method": method,
            "tokens_saved": tokens_saved
        }
    
    def process_all(self, limit: int = None):
        """Processa todos os PDFs"""
        print("=" * 60)
        print("🚀 REPROCESSAMENTO DE PDFs COM COMPRESSÃO MELHORADA")
        print("=" * 60)
        
        # Lista PDFs
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        self.stats["total_pdfs"] = len(pdf_files)
        
        print(f"📚 Total de PDFs: {len(pdf_files)}")
        
        if limit:
            pdf_files = pdf_files[:limit]
            print(f"⚠️ Limitando a {limit} PDFs para teste")
        
        # Processa cada PDF
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}]", end="")
            result = self.process_pdf(pdf_path)
            
            if "error" in result:
                print(f"   ❌ {result['error']}")
        
        # Relatório final
        self.print_report()
    
    def print_report(self):
        """Imprime relatório final"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL")
        print("=" * 60)
        
        if self.stats["total_original_size"] > 0:
            overall_compression = 1 - (self.stats["total_compressed_size"] / 
                                      self.stats["total_original_size"])
        else:
            overall_compression = 0
        
        print(f"""
📚 PDFs processados: {self.stats["processed"]}/{self.stats["total_pdfs"]}
📖 Total de páginas: {self.stats["total_pages"]}
✅ Com compressão positiva: {self.stats["compression_improved"]}
📊 Taxa de compressão geral: {overall_compression*100:.1f}%
💾 Tamanho original total: {self.stats["total_original_size"]/1024/1024:.1f} MB
💾 Tamanho comprimido total: {self.stats["total_compressed_size"]/1024/1024:.1f} MB
💰 Economia: {(self.stats["total_original_size"] - self.stats["total_compressed_size"])/1024/1024:.1f} MB
        """)
        
        # Mostra métodos usados
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT compression_method, COUNT(*) 
            FROM documents_v2 
            GROUP BY compression_method
        """)
        
        print("\n🔧 Métodos de compressão usados:")
        for method, count in cursor.fetchall():
            print(f"   • {method}: {count} documentos")
    
    def verify_integration(self):
        """Verifica integração com o sistema"""
        print("\n" + "=" * 60)
        print("🔗 VERIFICANDO INTEGRAÇÃO")
        print("=" * 60)
        
        # Verifica arquivos
        compressed_files = list(self.compressed_dir.glob("*.txt"))
        print(f"✅ Arquivos comprimidos: {len(compressed_files)}")
        
        # Verifica banco
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents_v2")
        db_count = cursor.fetchone()[0]
        print(f"✅ Registros no banco: {db_count}")
        
        # Verifica se RAG pode acessar
        try:
            from apps.scripturemon.rag_advanced import AdvancedRAG
            rag = AdvancedRAG()
            print(f"✅ RAG pode acessar knowledge_dir: {rag.knowledge_dir}")
        except:
            print("❌ RAG não consegue acessar")
        
        return compressed_files

def main():
    """Executa reprocessamento"""
    processor = PDFProcessorFixed()
    
    # Processa primeiro 5 PDFs como teste
    processor.process_all(limit=5)
    
    # Verifica integração
    processor.verify_integration()
    
    print("\n🏁 Reprocessamento concluído!")
    print("Para processar TODOS os PDFs, rode: python3 FIX_PDF_PROCESSING.py --all")

if __name__ == "__main__":
    import sys
    if "--all" in sys.argv:
        processor = PDFProcessorFixed()
        processor.process_all()  # Processa todos
        processor.verify_integration()
    else:
        main()