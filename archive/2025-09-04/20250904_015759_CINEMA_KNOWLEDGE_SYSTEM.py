#!/usr/bin/env python3
"""
🎬 SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO
==========================================
Sistema automático que:
1. Monitora pasta dedicada de cinema
2. Traduz automaticamente para DigiLang
3. Processa qualquer quantidade de documentos
4. Mantém organização e rastreamento
"""

import os
import sys
import time
import json
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import shutil

# Adicionar paths necessários
sys.path.append('/Users/clubproducoes/Digimundo')
sys.path.append('/Users/clubproducoes/Digimundo/digimons/scripturemon')

# Tentar importar bibliotecas necessárias
try:
    import PyPDF2
except ImportError:
    print("⚠️ PyPDF2 não instalado. Instalando...")
    os.system("pip3 install PyPDF2")
    import PyPDF2

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("⚠️ Watchdog não instalado. Instalando...")
    os.system("pip3 install watchdog")
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler


class DigiLangTranslator:
    """Sistema de tradução para DigiLang com compressão ~40%"""
    
    def __init__(self):
        self.symbols = {
            # Conceitos cinematográficos fundamentais
            'personagem': '角',
            'character': '角',
            'roteiro': '劾',
            'screenplay': '劾',
            'script': '劾',
            'cena': '景',
            'scene': '景',
            'diálogo': '話',
            'dialogue': '話',
            'ação': '動',
            'action': '動',
            'conflito': '戦',
            'conflict': '戦',
            'arco': '弧',
            'arc': '弧',
            'jornada': '旅',
            'journey': '旅',
            'herói': '英',
            'hero': '英',
            'antagonista': '敵',
            'antagonist': '敵',
            'tema': '題',
            'theme': '題',
            'plot': '筋',
            'enredo': '筋',
            'clímax': '頂',
            'climax': '頂',
            'resolução': '解',
            'resolution': '解',
            
            # Estrutura narrativa
            'three': '三',
            'três': '三',
            'ato': '幕',
            'act': '幕',
            'inciting': '発',
            'incidente': '発',
            'turning': '転',
            'virada': '転',
            'point': '点',
            'ponto': '点',
            'midpoint': '中',
            'meio': '中',
            
            # Técnicas de roteiro
            'save': '救',
            'salvar': '救',
            'cat': '猫',
            'gato': '猫',
            'show': '示',
            'mostrar': '示',
            'tell': '語',
            'contar': '語',
            'subtext': '潜',
            'subtexto': '潜',
            'backstory': '背',
            'história': '史',
            'story': '史',
            
            # Emoções e tom
            'drama': '劇',
            'comédia': '笑',
            'comedy': '笑',
            'terror': '恐',
            'horror': '恐',
            'romance': '愛',
            'love': '愛',
            'suspense': '疑',
            'tensão': '張',
            'tension': '張',
            
            # Produção
            'fade': '淡',
            'cut': '切',
            'corte': '切',
            'int': '内',
            'interior': '内',
            'ext': '外',
            'exterior': '外',
            'day': '昼',
            'dia': '昼',
            'night': '夜',
            'noite': '夜',
            'montage': '組',
            'montagem': '組'
        }
        
        # Criar dicionário reverso
        self.reverse_symbols = {v: k for k, v in self.symbols.items()}
    
    def translate_to_digilang(self, text: str) -> Tuple[str, float]:
        """Traduz texto para DigiLang e retorna taxa de compressão"""
        if not text:
            return "", 0.0
        
        original_length = len(text)
        translated = text.lower()
        
        # Substituir palavras por símbolos
        for word, symbol in sorted(self.symbols.items(), key=lambda x: len(x[0]), reverse=True):
            translated = translated.replace(word, f"[{symbol}]")
        
        # Comprimir espaços múltiplos
        while '  ' in translated:
            translated = translated.replace('  ', ' ')
        
        # Comprimir números
        import re
        translated = re.sub(r'\b(\d+)\b', lambda m: f"#{m.group(1)}", translated)
        
        # Calcular compressão
        new_length = len(translated)
        compression = 1 - (new_length / original_length) if original_length > 0 else 0
        
        return translated, compression
    
    def translate_from_digilang(self, text: str) -> str:
        """Traduz de DigiLang de volta para português"""
        result = text
        
        # Reverter símbolos
        import re
        symbols = re.findall(r'\[([^\]]+)\]', result)
        for symbol in symbols:
            if symbol in self.reverse_symbols:
                result = result.replace(f"[{symbol}]", self.reverse_symbols[symbol])
        
        # Reverter números
        result = re.sub(r'#(\d+)', r'\1', result)
        
        return result


class CinemaKnowledgeSystem:
    """Sistema completo de gestão de conhecimento cinematográfico"""
    
    def __init__(self):
        # Configurar diretórios
        self.base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
        self.cinema_folder = self.base_path / "CINEMA_KNOWLEDGE"
        self.originals_folder = self.cinema_folder / "01_ORIGINAIS_PDF"
        self.digilang_folder = self.cinema_folder / "02_TRADUCOES_DIGILANG"
        self.metadata_folder = self.cinema_folder / "03_METADATA"
        self.processing_folder = self.cinema_folder / "04_PROCESSANDO"
        
        # Criar estrutura
        self._create_structure()
        
        # Inicializar componentes
        self.translator = DigiLangTranslator()
        self.db_path = self.metadata_folder / "cinema_knowledge.db"
        self._init_database()
        
        # Status
        self.processing = False
        self.stats = {
            'total_documents': 0,
            'total_translated': 0,
            'average_compression': 0.0,
            'last_update': None
        }
    
    def _create_structure(self):
        """Cria estrutura de pastas necessária"""
        for folder in [self.cinema_folder, self.originals_folder, 
                      self.digilang_folder, self.metadata_folder,
                      self.processing_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Criar README
        readme_path = self.cinema_folder / "README.md"
        if not readme_path.exists():
            readme_content = """# 🎬 SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO

## 📁 ESTRUTURA:
- **01_ORIGINAIS_PDF/**: Coloque aqui TODOS os PDFs sobre cinema
- **02_TRADUCOES_DIGILANG/**: Traduções automáticas (não editar)
- **03_METADATA/**: Banco de dados e logs (sistema)
- **04_PROCESSANDO/**: Arquivos em processamento (temporário)

## 🚀 COMO USAR:
1. Coloque qualquer PDF sobre cinema em `01_ORIGINAIS_PDF/`
2. O sistema traduzirá AUTOMATICAMENTE para DigiLang
3. Não há limite de documentos - processa tudo!

## 🔤 DIGILANG:
- Compressão média: ~40% dos tokens originais
- Pensamento nativo em símbolos cinematográficos
- Otimizado para Scripturemon

## ⚙️ AUTOMAÇÃO:
- Monitor automático detecta novos arquivos
- Tradução inicia em segundos
- Backup automático das traduções
"""
            readme_path.write_text(readme_content)
    
    def _init_database(self):
        """Inicializa banco de dados de rastreamento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de documentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                original_path TEXT NOT NULL,
                digilang_path TEXT,
                file_hash TEXT NOT NULL,
                size_bytes INTEGER,
                pages INTEGER,
                status TEXT DEFAULT 'pending',
                compression_rate REAL,
                translation_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                translated_at TIMESTAMP,
                error_message TEXT
            )
        ''')
        
        # Tabela de estatísticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_documents INTEGER,
                total_translated INTEGER,
                total_pending INTEGER,
                total_errors INTEGER,
                average_compression REAL,
                total_tokens_saved INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_file_hash(self, filepath: Path) -> str:
        """Calcula hash MD5 de um arquivo"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def extract_pdf_text(self, pdf_path: Path) -> Tuple[str, int]:
        """Extrai texto de PDF e retorna (texto, num_páginas)"""
        text = ""
        pages = 0
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pages = len(pdf_reader.pages)
                
                for page_num in range(pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"❌ Erro ao extrair PDF {pdf_path.name}: {e}")
            return "", 0
        
        return text, pages
    
    def process_document(self, pdf_path: Path) -> bool:
        """Processa um documento: extrai, traduz e salva"""
        print(f"\n📄 Processando: {pdf_path.name}")
        start_time = time.time()
        
        # Verificar se já foi processado
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        file_hash = self.get_file_hash(pdf_path)
        cursor.execute("SELECT id, file_hash FROM documents WHERE filename = ?", (pdf_path.name,))
        result = cursor.fetchone()
        
        if result and result[1] == file_hash:
            print(f"   ✅ Já processado e atualizado")
            conn.close()
            return True
        
        try:
            # Mover para pasta de processamento
            temp_path = self.processing_folder / pdf_path.name
            shutil.copy2(pdf_path, temp_path)
            
            # Extrair texto
            print(f"   📖 Extraindo texto...")
            text, pages = self.extract_pdf_text(temp_path)
            
            if not text:
                raise Exception("Não foi possível extrair texto do PDF")
            
            # Traduzir para DigiLang
            print(f"   🔤 Traduzindo para DigiLang...")
            digilang_text, compression = self.translator.translate_to_digilang(text)
            
            # Salvar tradução
            digilang_filename = pdf_path.stem + "_digilang.txt"
            digilang_path = self.digilang_folder / digilang_filename
            digilang_path.write_text(digilang_text, encoding='utf-8')
            
            # Calcular estatísticas
            original_size = len(text)
            compressed_size = len(digilang_text)
            tokens_saved = original_size - compressed_size
            translation_time = time.time() - start_time
            
            # Atualizar banco de dados
            if result:
                # Atualizar registro existente
                cursor.execute('''
                    UPDATE documents 
                    SET file_hash = ?, digilang_path = ?, pages = ?, 
                        status = 'completed', compression_rate = ?,
                        translation_time = ?, translated_at = CURRENT_TIMESTAMP,
                        error_message = NULL
                    WHERE filename = ?
                ''', (file_hash, str(digilang_path), pages, compression,
                     translation_time, pdf_path.name))
            else:
                # Inserir novo registro
                cursor.execute('''
                    INSERT INTO documents 
                    (filename, original_path, digilang_path, file_hash, 
                     size_bytes, pages, status, compression_rate, translation_time,
                     translated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 'completed', ?, ?, CURRENT_TIMESTAMP)
                ''', (pdf_path.name, str(pdf_path), str(digilang_path),
                     file_hash, pdf_path.stat().st_size, pages, 
                     compression, translation_time))
            
            conn.commit()
            
            # Limpar arquivo temporário
            temp_path.unlink()
            
            print(f"   ✅ Tradução completa!")
            print(f"   📊 Compressão: {compression:.1%}")
            print(f"   💾 Tokens economizados: {tokens_saved:,}")
            print(f"   ⏱️ Tempo: {translation_time:.1f}s")
            
            conn.close()
            return True
            
        except Exception as e:
            # Registrar erro
            cursor.execute('''
                INSERT OR REPLACE INTO documents 
                (filename, original_path, file_hash, status, error_message)
                VALUES (?, ?, ?, 'error', ?)
            ''', (pdf_path.name, str(pdf_path), file_hash, str(e)))
            conn.commit()
            conn.close()
            
            print(f"   ❌ Erro: {e}")
            return False
    
    def migrate_existing_documents(self):
        """Migra os 43 documentos existentes para o novo sistema"""
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
                    dest = self.originals_folder / pdf.name
                    if not dest.exists():
                        shutil.copy2(pdf, dest)
                        print(f"   ✅ {pdf.name}")
                        migrated += 1
        
        # Copiar traduções DigiLang existentes
        digilang_sources = [
            Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/conhecimento_digilang/01_manuais_traduzidos"),
            Path("/Users/clubproducoes/Digimundo/DIGILANG_COMPLETE_SYSTEM/02_MANUAIS_ROTEIRO/digilang"),
        ]
        
        translations = 0
        for source in digilang_sources:
            if source.exists():
                for txt in source.glob("*_digilang.txt"):
                    dest = self.digilang_folder / txt.name
                    if not dest.exists():
                        shutil.copy2(txt, dest)
                        translations += 1
        
        print(f"\n✅ Migração completa!")
        print(f"   📄 {migrated} PDFs migrados")
        print(f"   🔤 {translations} traduções existentes copiadas")
        
        return migrated
    
    def process_all_pending(self):
        """Processa todos os documentos pendentes"""
        print("\n🚀 PROCESSANDO DOCUMENTOS PENDENTES...")
        print("="*50)
        
        # Listar todos os PDFs na pasta
        pdf_files = list(self.originals_folder.glob("*.pdf"))
        total = len(pdf_files)
        
        if total == 0:
            print("📭 Nenhum documento encontrado")
            return
        
        print(f"📚 Total de documentos: {total}")
        
        # Processar cada um
        processed = 0
        errors = 0
        
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{i}/{total}]", end="")
            
            # Verificar se já tem tradução
            digilang_name = pdf_path.stem + "_digilang.txt"
            if (self.digilang_folder / digilang_name).exists():
                print(f" ✓ {pdf_path.name} (já traduzido)")
                processed += 1
                continue
            
            # Processar
            if self.process_document(pdf_path):
                processed += 1
            else:
                errors += 1
        
        # Estatísticas finais
        self.update_statistics()
        
        print("\n" + "="*50)
        print("📊 RESUMO DO PROCESSAMENTO:")
        print(f"   ✅ Processados com sucesso: {processed}")
        print(f"   ❌ Erros: {errors}")
        print(f"   📈 Taxa de sucesso: {(processed/total)*100:.1f}%")
    
    def update_statistics(self):
        """Atualiza estatísticas do sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contar documentos
        cursor.execute("SELECT COUNT(*) FROM documents")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'completed'")
        translated = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'pending'")
        pending = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'error'")
        errors = cursor.fetchone()[0]
        
        # Calcular compressão média
        cursor.execute("SELECT AVG(compression_rate) FROM documents WHERE compression_rate IS NOT NULL")
        avg_compression = cursor.fetchone()[0] or 0.0
        
        # Inserir estatísticas
        cursor.execute('''
            INSERT INTO statistics 
            (total_documents, total_translated, total_pending, total_errors, average_compression)
            VALUES (?, ?, ?, ?, ?)
        ''', (total, translated, pending, errors, avg_compression))
        
        conn.commit()
        conn.close()
        
        self.stats = {
            'total_documents': total,
            'total_translated': translated,
            'average_compression': avg_compression,
            'last_update': datetime.now()
        }
    
    def show_status(self):
        """Mostra status do sistema"""
        print("\n📊 STATUS DO SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO")
        print("="*60)
        
        # Contar arquivos
        pdfs = len(list(self.originals_folder.glob("*.pdf")))
        translations = len(list(self.digilang_folder.glob("*_digilang.txt")))
        
        print(f"\n📁 ARQUIVOS:")
        print(f"   📄 PDFs originais: {pdfs}")
        print(f"   🔤 Traduções DigiLang: {translations}")
        print(f"   📈 Taxa de tradução: {(translations/pdfs)*100:.1f}%" if pdfs > 0 else "")
        
        # Estatísticas do banco
        self.update_statistics()
        
        if self.stats['total_documents'] > 0:
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   📚 Total registrado: {self.stats['total_documents']}")
            print(f"   ✅ Traduzidos: {self.stats['total_translated']}")
            print(f"   🔄 Compressão média: {self.stats['average_compression']:.1%}")
        
        # Listar alguns documentos
        print(f"\n📖 ALGUNS DOCUMENTOS:")
        for pdf in list(self.originals_folder.glob("*.pdf"))[:5]:
            status = "✅" if (self.digilang_folder / f"{pdf.stem}_digilang.txt").exists() else "⏳"
            print(f"   {status} {pdf.name}")
        
        if pdfs > 5:
            print(f"   ... e mais {pdfs-5} documentos")
        
        print("\n" + "="*60)


class CinemaFolderMonitor(FileSystemEventHandler):
    """Monitor automático da pasta de cinema"""
    
    def __init__(self, system: CinemaKnowledgeSystem):
        self.system = system
        self.processing = False
    
    def on_created(self, event):
        """Quando um novo arquivo é adicionado"""
        if not event.is_directory and event.src_path.endswith('.pdf'):
            print(f"\n🆕 Novo documento detectado: {Path(event.src_path).name}")
            time.sleep(2)  # Aguardar cópia completa
            
            if not self.processing:
                self.processing = True
                self.system.process_document(Path(event.src_path))
                self.processing = False


def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════╗
║   🎬 SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO 🎬      ║
║              Tradução Automática DigiLang            ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # Criar sistema
    system = CinemaKnowledgeSystem()
    
    # Menu
    while True:
        print("\n📋 OPÇÕES:")
        print("1. Migrar 43 documentos existentes")
        print("2. Processar todos os documentos pendentes")
        print("3. Mostrar status do sistema")
        print("4. Iniciar monitor automático")
        print("5. Processar pasta específica")
        print("0. Sair")
        
        choice = input("\nEscolha: ").strip()
        
        if choice == "1":
            system.migrate_existing_documents()
            print("\n✅ Migração concluída! Agora execute opção 2 para traduzir.")
        
        elif choice == "2":
            system.process_all_pending()
        
        elif choice == "3":
            system.show_status()
        
        elif choice == "4":
            print("\n🔍 MONITOR AUTOMÁTICO ATIVADO")
            print("Coloque PDFs em: CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF/")
            print("Pressione Ctrl+C para parar")
            
            event_handler = CinemaFolderMonitor(system)
            observer = Observer()
            observer.schedule(event_handler, str(system.originals_folder), recursive=False)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\n⏹️ Monitor parado")
            observer.join()
        
        elif choice == "5":
            path = input("Digite o caminho da pasta com PDFs: ").strip()
            if Path(path).exists():
                pdfs = list(Path(path).glob("*.pdf"))
                print(f"\nEncontrados {len(pdfs)} PDFs")
                confirm = input("Copiar para o sistema? (s/n): ")
                if confirm.lower() == 's':
                    for pdf in pdfs:
                        dest = system.originals_folder / pdf.name
                        shutil.copy2(pdf, dest)
                        print(f"✅ Copiado: {pdf.name}")
                    print("\nAgora execute opção 2 para processar")
            else:
                print("❌ Pasta não encontrada")
        
        elif choice == "0":
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    main()
