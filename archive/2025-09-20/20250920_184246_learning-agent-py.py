#!/usr/bin/env python3
"""
📚 LEARNING AGENT - Sistema de Aprendizado Contínuo
Monitora arquivos e aprende incrementalmente
"""

import asyncio
import os
import json
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ollama

logger = logging.getLogger("LearningAgent")


class FileChangeHandler(FileSystemEventHandler):
    """Handler para mudanças no sistema de arquivos"""
    
    def __init__(self, learning_agent):
        self.learning_agent = learning_agent
        self.pending_files = set()
    
    def on_modified(self, event):
        if not event.is_directory:
            self.pending_files.add(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.pending_files.add(event.src_path)


class LearningAgent:
    """Agente responsável por aprender continuamente de arquivos"""
    
    def __init__(self, paths_to_monitor: List[str], memory_agent):
        self.paths_to_monitor = [Path(p).expanduser() for p in paths_to_monitor]
        self.memory_agent = memory_agent
        
        # Estado do aprendizado
        self.learned_files = {}  # arquivo -> hash
        self.learning_queue = asyncio.Queue()
        self.file_handler = FileChangeHandler(self)
        
        # Configurações
        self.config = {
            'max_file_size_mb': 10,
            'supported_extensions': {
                '.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml',
                '.csv', '.log', '.sh', '.bash', '.conf', '.ini',
                '.html', '.css', '.xml', '.rst', '.tex'
            },
            'chunk_size': 1000,  # Caracteres por chunk
            'overlap': 200       # Overlap entre chunks
        }
        
        # Estatísticas
        self.stats = {
            'files_processed': 0,
            'files_skipped': 0,
            'chunks_created': 0,
            'errors': 0,
            'total_size_processed': 0
        }
        
        # Inicializar observador de arquivos
        self._init_file_watcher()
        
        logger.info(f"✅ Learning Agent inicializado para: {paths_to_monitor}")
    
    def _init_file_watcher(self):
        """Inicializar observador de mudanças em arquivos"""
        self.observer = Observer()
        
        for path in self.paths_to_monitor:
            if path.exists():
                self.observer.schedule(
                    self.file_handler,
                    str(path),
                    recursive=True
                )
                logger.info(f"👀 Monitorando: {path}")
            else:
                logger.warning(f"⚠️ Caminho não existe: {path}")
        
        self.observer.start()
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcular hash do arquivo"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Erro ao calcular hash de {file_path}: {e}")
            return ""
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Verificar se arquivo deve ser processado"""
        # Verificar se existe
        if not file_path.exists():
            return False
        
        # Verificar tamanho
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config['max_file_size_mb']:
            logger.warning(f"📏 Arquivo muito grande: {file_path} ({size_mb:.1f}MB)")
            return False
        
        # Verificar extensão
        if file_path.suffix.lower() not in self.config['supported_extensions']:
            return False
        
        # Verificar se já foi processado com mesmo conteúdo
        current_hash = self._calculate_file_hash(file_path)
        if str(file_path) in self.learned_files:
            if self.learned_files[str(file_path)] == current_hash:
                return False  # Já processado e não mudou
        
        return True
    
    def _chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Dividir texto em chunks com overlap"""
        chunks = []
        chunk_size = self.config['chunk_size']
        overlap = self.config['overlap']
        
        # Se texto é menor que chunk_size, retornar como único chunk
        if len(text) <= chunk_size:
            return [{
                'content': text,
                'start': 0,
                'end': len(text),
                'index': 0
            }]
        
        # Criar chunks com overlap
        start = 0
        index = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Tentar encontrar fim de sentença
            if end < len(text):
                # Procurar pontuação
                for punct in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                    last_punct = text.rfind(punct, start, end)
                    if last_punct != -1:
                        end = last_punct + len(punct)
                        break
            
            chunk_content = text[start:end].strip()
            
            if chunk_content:
                chunks.append({
                    'content': chunk_content,
                    'start': start,
                    'end': end,
                    'index': index
                })
                index += 1
            
            # Próximo chunk com overlap
            start = end - overlap if end < len(text) else end
        
        return chunks
    
    async def _extract_file_content(self, file_path: Path) -> Optional[str]:
        """Extrair conteúdo do arquivo"""
        try:
            # Determinar encoding
            mime_type = mimetypes.guess_type(str(file_path))[0]
            
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        return content
                except UnicodeDecodeError:
                    continue
            
            logger.warning(f"⚠️ Não foi possível decodificar {file_path}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao ler {file_path}: {e}")
            return None
    
    async def _analyze_content(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Analisar conteúdo usando LLM"""
        try:
            # Prompt para análise
            prompt = f"""Analise o seguinte conteúdo e extraia informações importantes:

Arquivo: {file_path.name}
Conteúdo (primeiros 500 caracteres):
{content[:500]}...

Responda em formato JSON com:
1. tipo: tipo de conteúdo (código, documentação, configuração, dados, etc)
2. linguagem: linguagem ou formato (se aplicável)
3. resumo: resumo breve do conteúdo
4. conceitos: lista de conceitos principais
5. entidades: nomes, tecnologias ou entidades mencionadas
6. importancia: nota de 1-10 sobre a importância

Responda APENAS com o JSON, sem explicações."""

            # Gerar análise
            response = ollama.generate(
                model="llama3.2:latest",
                prompt=prompt,
                options={
                    'temperature': 0.3,
                    'format': 'json'
                }
            )
            
            # Parse do JSON
            try:
                analysis = json.loads(response['response'])
                return analysis
            except json.JSONDecodeError:
                # Fallback para análise básica
                return {
                    'tipo': 'texto',
                    'resumo': content[:200],
                    'conceitos': [],
                    'entidades': [],
                    'importancia': 5
                }
                
        except Exception as e:
            logger.error(f"Erro na análise: {e}")
            return {
                'tipo': 'desconhecido',
                'erro': str(e)
            }
    
    async def learn_from_file(self, file_path: str) -> Dict[str, Any]:
        """Aprender de um arquivo específico"""
        path = Path(file_path).expanduser()
        
        # Verificar se deve processar
        if not self._should_process_file(path):
            self.stats['files_skipped'] += 1
            return {
                'success': False,
                'reason': 'Arquivo não elegível para processamento'
            }
        
        try:
            logger.info(f"📖 Aprendendo de: {path}")
            
            # Extrair conteúdo
            content = await self._extract_file_content(path)
            if not content:
                return {
                    'success': False,
                    'reason': 'Não foi possível extrair conteúdo'
                }
            
            # Analisar conteúdo
            analysis = await self._analyze_content(content, path)
            
            # Criar chunks
            chunks = self._chunk_text(content)
            
            # Armazenar cada chunk na memória
            chunk_ids = []
            for chunk in chunks:
                # Metadados do chunk
                metadata = {
                    'type': 'file_content',
                    'file_path': str(path),
                    'file_name': path.name,
                    'file_type': analysis.get('tipo', 'unknown'),
                    'chunk_index': chunk['index'],
                    'chunk_total': len(chunks),
                    'analysis': analysis,
                    'learned_at': datetime.now().isoformat()
                }
                
                # Armazenar na memória
                chunk_id = await self.memory_agent.store(
                    content=chunk['content'],
                    metadata=metadata
                )
                
                if chunk_id:
                    chunk_ids.append(chunk_id)
                    self.stats['chunks_created'] += 1
            
            # Armazenar resumo do arquivo
            file_summary = {
                'file_path': str(path),
                'content_summary': analysis.get('resumo', ''),
                'chunks': len(chunks),
                'chunk_ids': chunk_ids,
                'analysis': analysis
            }
            
            await self.memory_agent.store(
                content=file_summary,
                metadata={
                    'type': 'file_summary',
                    'file_path': str(path),
                    'importance': analysis.get('importancia', 5)
                }
            )
            
            # Atualizar registro de arquivos aprendidos
            file_hash = self._calculate_file_hash(path)
            self.learned_files[str(path)] = file_hash
            
            # Atualizar estatísticas
            self.stats['files_processed'] += 1
            self.stats['total_size_processed'] += path.stat().st_size
            
            logger.info(f"✅ Aprendido: {path.name} ({len(chunks)} chunks)")
            
            return {
                'success': True,
                'file': str(path),
                'chunks': len(chunks),
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao aprender de {path}: {e}")
            self.stats['errors'] += 1
            return {
                'success': False,
                'error': str(e)
            }
    
    async def scan_all(self) -> Dict[str, Any]:
        """Escanear todos os diretórios monitorados"""
        logger.info("🔍 Iniciando scan completo...")
        
        results = {
            'scanned_paths': [],
            'files_found': 0,
            'files_processed': 0,
            'files_skipped': 0,
            'errors': []
        }
        
        for base_path in self.paths_to_monitor:
            if not base_path.exists():
                continue
            
            results['scanned_paths'].append(str(base_path))
            
            # Percorrer recursivamente
            for file_path in base_path.rglob('*'):
                if file_path.is_file():
                    results['files_found'] += 1
                    
                    # Verificar se deve processar
                    if self._should_process_file(file_path):
                        result = await self.learn_from_file(str(file_path))
                        
                        if result['success']:
                            results['files_processed'] += 1
                        else:
                            results['files_skipped'] += 1
                            if 'error' in result:
                                results['errors'].append({
                                    'file': str(file_path),
                                    'error': result['error']
                                })
                    else:
                        results['files_skipped'] += 1
        
        logger.info(f"✅ Scan completo: {results['files_processed']} arquivos processados")
        return results
    
    async def process_pending(self):
        """Processar arquivos pendentes (do file watcher)"""
        if hasattr(self.file_handler, 'pending_files'):
            pending = list(self.file_handler.pending_files)
            self.file_handler.pending_files.clear()
            
            for file_path in pending:
                await self.learn_from_file(file_path)
    
    async def forget_file(self, file_path: str) -> bool:
        """Esquecer um arquivo específico"""
        try:
            path = Path(file_path).expanduser()
            
            # Buscar todas as memórias relacionadas
            memories = await self.memory_agent.search(
                str(path),
                n_results=100,
                filter_dict={'file_path': str(path)}
            )
            
            # Deletar cada memória
            deleted = 0
            for memory in memories:
                if await self.memory_agent.delete(memory['id']):
                    deleted += 1
            
            # Remover do registro
            if str(path) in self.learned_files:
                del self.learned_files[str(path)]
            
            logger.info(f"🗑️ Esquecido: {path} ({deleted} memórias removidas)")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao esquecer arquivo: {e}")
            return False
    
    async def get_file_knowledge(self, file_path: str) -> Dict[str, Any]:
        """Obter conhecimento sobre um arquivo específico"""
        try:
            path = Path(file_path).expanduser()
            
            # Buscar resumo do arquivo
            summaries = await self.memory_agent.search(
                f"file_summary {str(path)}",
                n_results=1,
                filter_dict={'type': 'file_summary', 'file_path': str(path)}
            )
            
            if not summaries:
                return {
                    'found': False,
                    'file': str(path)
                }
            
            summary = summaries[0]
            
            # Buscar chunks relacionados
            chunks = await self.memory_agent.search(
                str(path),
                n_results=10,
                filter_dict={'type': 'file_content', 'file_path': str(path)}
            )
            
            return {
                'found': True,
                'file': str(path),
                'summary': summary['content'],
                'chunks_count': len(chunks),
                'analysis': summary['metadata'].get('analysis', {}),
                'learned_at': summary['metadata'].get('learned_at')
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter conhecimento: {e}")
            return {
                'found': False,
                'error': str(e)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do agente"""
        return {
            'files_processed': self.stats['files_processed'],
            'files_skipped': self.stats['files_skipped'],
            'chunks_created': self.stats['chunks_created'],
            'errors': self.stats['errors'],
            'total_size_mb': self.stats['total_size_processed'] / (1024 * 1024),
            'learned_files': len(self.learned_files),
            'monitored_paths': [str(p) for p in self.paths_to_monitor]
        }
    
    async def health_check(self) -> bool:
        """Verificar saúde do agente"""
        try:
            # Verificar se observer está rodando
            if not self.observer.is_alive():
                return False
            
            # Verificar se pode acessar paths
            for path in self.paths_to_monitor:
                if not path.exists():
                    logger.warning(f"Path não acessível: {path}")
            
            return True
        except:
            return False
    
    def stop(self):
        """Parar o agente"""
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
        logger.info("🛑 Learning Agent parado")


# Teste do agente
async def test_learning_agent():
    """Testar o Learning Agent"""
    from memory_agent import MemoryAgent
    
    print("🧪 Testando Learning Agent...")
    
    # Criar memory agent
    memory = MemoryAgent()
    
    # Criar learning agent
    agent = LearningAgent(
        paths_to_monitor=["~/Digimundo"],
        memory_agent=memory
    )
    
    # Teste 1: Scan inicial
    print("\n1️⃣ Fazendo scan inicial...")
    results = await agent.scan_all()
    print(f"   Arquivos encontrados: {results['files_found']}")
    print(f"   Arquivos processados: {results['files_processed']}")
    
    # Teste 2: Estatísticas
    print("\n2️⃣ Estatísticas:")
    stats = agent.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Parar agent
    agent.stop()
    
    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    asyncio.run(test_learning_agent())
