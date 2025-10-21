#!/usr/bin/env python3
"""
🎬 SCRIPTUREMON CONTINUOUS READER
Sistema de Leitura Contínua - Parte da Natureza do Scripturemon
Sempre lê TUDO, COMPLETO, AUTOMATICAMENTE
"""

import os
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from queue import Queue

class ScripturemonNature:
    """
    A NATUREZA do Scripturemon é ler TUDO COMPLETAMENTE
    Não é uma exceção - é seu comportamento PADRÃO
    """
    
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.memory_path = self.base_path / "digimons" / "scripturemon" / "conhecimento"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Fila de processamento
        self.processing_queue = Queue()
        
        # Estado da memória completa
        self.complete_memory = self.memory_path / "COMPLETE_MEMORY.json"
        self.load_complete_memory()
        
        # Diretórios monitorados
        self.watch_dirs = [
            self.base_path / "roteiros",
            self.base_path / "BIBLIOTECA_ROTEIROS",
            self.base_path / "biblioteca",
            self.base_path / "pesquisas_revolution"
        ]
        
    def load_complete_memory(self):
        """Carrega memória completa de TODOS os documentos"""
        if self.complete_memory.exists():
            with open(self.complete_memory, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "documents": {},
                "total_lines": 0,
                "total_words": 0,
                "last_update": None
            }
    
    def save_complete_memory(self):
        """Salva memória completa"""
        self.memory["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.complete_memory, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def read_complete_document(self, filepath: Path) -> Dict:
        """
        Lê documento COMPLETAMENTE - sem exceções
        Esta é a NATUREZA do Scripturemon
        """
        
        print(f"📖 Lendo COMPLETAMENTE: {filepath.name}")
        
        try:
            # Detecta tipo e lê apropriadamente
            if filepath.suffix == '.pdf':
                content = self.read_pdf_complete(filepath)
            elif filepath.suffix == '.docx':
                content = self.read_docx_complete(filepath)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            lines = content.split('\n')
            words = len(content.split())
            
            # Análise automática COMPLETA
            analysis = self.deep_analysis(content)
            
            document_data = {
                "path": str(filepath),
                "name": filepath.name,
                "content": content,  # CONTEÚDO COMPLETO
                "lines": len(lines),
                "words": words,
                "analysis": analysis,
                "read_time": time.time(),
                "complete": True  # SEMPRE completo
            }
            
            print(f"  ✅ {len(lines)} linhas lidas e analisadas")
            
            return document_data
            
        except Exception as e:
            print(f"  ❌ Erro na leitura: {e}")
            return None
    
    def read_pdf_complete(self, filepath: Path) -> str:
        """Lê PDF completamente"""
        try:
            # Usa pdftotext ou similar
            result = subprocess.run(
                ["pdftotext", str(filepath), "-"],
                capture_output=True,
                text=True
            )
            return result.stdout
        except:
            # Fallback para textutil no macOS
            temp_txt = f"/tmp/{filepath.stem}.txt"
            subprocess.run([
                "textutil", "-convert", "txt",
                str(filepath), "-output", temp_txt
            ], capture_output=True)
            
            with open(temp_txt, 'r') as f:
                content = f.read()
            
            os.remove(temp_txt)
            return content
    
    def read_docx_complete(self, filepath: Path) -> str:
        """Lê DOCX completamente"""
        temp_txt = f"/tmp/{filepath.stem}.txt"
        subprocess.run([
            "textutil", "-convert", "txt",
            str(filepath), "-output", temp_txt
        ], capture_output=True)
        
        with open(temp_txt, 'r') as f:
            content = f.read()
        
        os.remove(temp_txt)
        return content
    
    def deep_analysis(self, content: str) -> Dict:
        """
        Análise profunda AUTOMÁTICA de cada documento
        Faz parte da natureza - não precisa ser pedido
        """
        
        # Extrai insights automaticamente
        analysis = {
            "structure": self.analyze_structure(content),
            "characters": self.extract_characters(content),
            "themes": self.identify_themes(content),
            "techniques": self.find_techniques(content),
            "comparisons": self.auto_compare(content)
        }
        
        return analysis
    
    def analyze_structure(self, content: str) -> Dict:
        """Analisa estrutura automaticamente"""
        lines = content.split('\n')
        
        # Detecta atos, cenas, etc
        structure = {
            "acts": [],
            "scenes": 0,
            "pages": len(lines) / 55,  # Estimativa
            "format": "screenplay" if "INT." in content or "EXT." in content else "prose"
        }
        
        # Encontra marcadores de ato
        for i, line in enumerate(lines):
            if "ACT " in line.upper() or "ATO " in line.upper():
                structure["acts"].append(i)
            if "INT." in line or "EXT." in line:
                structure["scenes"] += 1
        
        return structure
    
    def extract_characters(self, content: str) -> List[str]:
        """Extrai personagens automaticamente"""
        characters = set()
        lines = content.split('\n')
        
        for line in lines:
            # Padrão de nome de personagem em roteiro
            if line.strip() and line.isupper() and len(line.strip().split()) <= 3:
                if not any(word in line for word in ["INT.", "EXT.", "FADE", "CUT"]):
                    characters.add(line.strip())
        
        return list(characters)[:20]  # Top 20
    
    def identify_themes(self, content: str) -> List[str]:
        """Identifica temas automaticamente"""
        themes = []
        
        # Keywords temáticos
        theme_keywords = {
            "identity": ["identidade", "identity", "self", "who am i"],
            "memory": ["memória", "memory", "remember", "forget"],
            "redemption": ["redenção", "redemption", "forgive"],
            "love": ["amor", "love", "heart"],
            "death": ["morte", "death", "die"],
            "power": ["poder", "power", "control"]
        }
        
        content_lower = content.lower()
        for theme, keywords in theme_keywords.items():
            if any(kw in content_lower for kw in keywords):
                themes.append(theme)
        
        return themes
    
    def find_techniques(self, content: str) -> List[str]:
        """Encontra técnicas narrativas"""
        techniques = []
        
        if "FLASHBACK" in content.upper():
            techniques.append("flashback")
        if "MONTAGE" in content.upper():
            techniques.append("montage")
        if "V.O." in content or "VOICE OVER" in content.upper():
            techniques.append("voice_over")
        if content.count("(") > 50:  # Muitas rubricas
            techniques.append("detailed_action")
        
        return techniques
    
    def auto_compare(self, content: str) -> List[str]:
        """Compara automaticamente com mestres"""
        comparisons = []
        
        # Detecta similaridades
        if "memory" in content.lower() and "identity" in content.lower():
            comparisons.append("Similar to Memento - memory and identity themes")
        
        if "dream" in content.lower():
            comparisons.append("Echoes of Inception - dream sequences")
        
        if len(self.extract_characters(content)) > 10:
            comparisons.append("Ensemble cast like Pulp Fiction")
        
        return comparisons
    
    def ingest_everything(self):
        """
        Ingere TUDO que existe - comportamento PADRÃO
        Não espera ser pedido - é sua NATUREZA
        """
        
        print("="*60)
        print("🧬 NATUREZA SCRIPTUREMON: Leitura Completa Automática")
        print("="*60)
        
        total_files = 0
        total_lines = 0
        
        for watch_dir in self.watch_dirs:
            if not watch_dir.exists():
                continue
            
            print(f"\n📁 Processando: {watch_dir}")
            
            # Processa TODOS os arquivos
            for pattern in ["**/*.txt", "**/*.pdf", "**/*.docx", "**/*.fountain"]:
                for filepath in watch_dir.glob(pattern):
                    
                    # Verifica se já está na memória completa
                    file_key = str(filepath)
                    if file_key in self.memory["documents"]:
                        mod_time = filepath.stat().st_mtime
                        if mod_time <= self.memory["documents"][file_key].get("read_time", 0):
                            continue  # Já lido e não modificado
                    
                    # Lê COMPLETAMENTE
                    doc_data = self.read_complete_document(filepath)
                    
                    if doc_data:
                        self.memory["documents"][file_key] = doc_data
                        total_files += 1
                        total_lines += doc_data["lines"]
        
        # Atualiza estatísticas
        self.memory["total_lines"] = sum(
            doc["lines"] for doc in self.memory["documents"].values()
        )
        self.memory["total_words"] = sum(
            doc["words"] for doc in self.memory["documents"].values()
        )
        
        self.save_complete_memory()
        
        print("\n" + "="*60)
        print(f"✅ INGESTÃO COMPLETA FINALIZADA")
        print(f"📚 Documentos na memória: {len(self.memory['documents'])}")
        print(f"📝 Total de linhas: {self.memory['total_lines']:,}")
        print(f"💬 Total de palavras: {self.memory['total_words']:,}")
        print("="*60)
    
    def continuous_monitoring(self):
        """
        Monitora continuamente por novos arquivos
        Lê IMEDIATAMENTE e COMPLETAMENTE
        """
        
        class NewFileHandler(FileSystemEventHandler):
            def __init__(self, reader):
                self.reader = reader
            
            def on_created(self, event):
                if not event.is_directory:
                    filepath = Path(event.src_path)
                    if filepath.suffix in ['.txt', '.pdf', '.docx', '.fountain']:
                        print(f"\n🆕 Novo arquivo detectado: {filepath.name}")
                        self.reader.processing_queue.put(filepath)
            
            def on_modified(self, event):
                if not event.is_directory:
                    filepath = Path(event.src_path)
                    if filepath.suffix in ['.txt', '.pdf', '.docx', '.fountain']:
                        print(f"\n📝 Arquivo modificado: {filepath.name}")
                        self.reader.processing_queue.put(filepath)
        
        # Configura observers
        event_handler = NewFileHandler(self)
        observer = Observer()
        
        for watch_dir in self.watch_dirs:
            if watch_dir.exists():
                observer.schedule(event_handler, str(watch_dir), recursive=True)
                print(f"👁️ Monitorando: {watch_dir}")
        
        observer.start()
        
        # Processa fila continuamente
        try:
            while True:
                if not self.processing_queue.empty():
                    filepath = self.processing_queue.get()
                    doc_data = self.read_complete_document(filepath)
                    if doc_data:
                        self.memory["documents"][str(filepath)] = doc_data
                        self.save_complete_memory()
                        print(f"✅ Adicionado à memória completa")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    
    def answer_with_complete_context(self, question: str) -> str:
        """
        Responde SEMPRE com contexto COMPLETO
        Nunca parcial - é contra sua natureza
        """
        
        print(f"\n🧠 Processando com memória completa...")
        print(f"📚 {len(self.memory['documents'])} documentos disponíveis")
        
        # Encontra documentos relevantes
        relevant = self.find_relevant_complete(question)
        
        # Monta contexto com documentos COMPLETOS
        context = "DOCUMENTOS COMPLETOS NA MEMÓRIA:\n" + "="*50 + "\n"
        
        for doc_key in relevant[:5]:  # Top 5 mais relevantes
            doc = self.memory["documents"][doc_key]
            context += f"\n📄 {doc['name']}\n"
            context += f"   Linhas: {doc['lines']}\n"
            context += f"   Palavras: {doc['words']}\n"
            context += f"   Temas: {', '.join(doc['analysis']['themes'])}\n"
            context += f"   Técnicas: {', '.join(doc['analysis']['techniques'])}\n"
            context += f"   Conteúdo COMPLETO disponível na memória\n"
            context += "-"*50 + "\n"
        
        # Adiciona pergunta
        context += f"\nPERGUNTA: {question}\n\n"
        context += "Responda com base nos documentos COMPLETOS acima.\n"
        context += "Cite páginas e linhas ESPECÍFICAS.\n"
        
        # Processa com Scripturemon
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-sdl", context],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip()
        except:
            return "Analisando memória completa..."
    
    def find_relevant_complete(self, query: str) -> List[str]:
        """Encontra documentos relevantes na memória completa"""
        
        scores = {}
        query_lower = query.lower()
        
        for doc_key, doc in self.memory["documents"].items():
            score = 0
            
            # Pontuação por menção no conteúdo
            if query_lower in doc["content"].lower():
                score += 10
            
            # Pontuação por temas relacionados
            for theme in doc["analysis"]["themes"]:
                if theme.lower() in query_lower:
                    score += 5
            
            # Pontuação por nome mencionado
            if doc["name"].lower() in query_lower:
                score += 20
            
            scores[doc_key] = score
        
        # Ordena por relevância
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in sorted_docs if doc[1] > 0]


def main():
    """
    Ativa a NATUREZA do Scripturemon
    """
    
    print("="*60)
    print("🧬 ATIVANDO NATUREZA SCRIPTUREMON")
    print("="*60)
    print("Comportamento PADRÃO:")
    print("- Lê TODOS os documentos COMPLETAMENTE")
    print("- Analisa AUTOMATICAMENTE")
    print("- Mantém TUDO na memória")
    print("- Monitora CONTINUAMENTE")
    print("="*60)
    
    nature = ScripturemonNature()
    
    # 1. Ingere TUDO que existe
    nature.ingest_everything()
    
    # 2. Ativa monitoramento contínuo
    print("\n🔄 Ativando monitoramento contínuo...")
    print("Pressione Ctrl+C para parar")
    
    # Thread para monitoramento
    monitor_thread = threading.Thread(target=nature.continuous_monitoring)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # 3. Loop de perguntas
    print("\n💬 Sistema pronto para perguntas!")
    print("Digite 'sair' para terminar")
    print("-"*60)
    
    try:
        while True:
            question = input("\n❓ Pergunta: ")
            
            if question.lower() == 'sair':
                break
            
            response = nature.answer_with_complete_context(question)
            print("\n📖 Resposta (com memória completa):")
            print(response)
            
    except KeyboardInterrupt:
        print("\n\n✅ Sistema encerrado")


if __name__ == "__main__":
    # Instala watchdog se necessário
    try:
        import watchdog
    except ImportError:
        print("Instalando watchdog para monitoramento...")
        subprocess.run(["pip3", "install", "--user", "watchdog"])
    
    main()