"""
DigiLang Translator - Sistema de tradução batch de PDFs para formato DigiLang
Processa todos os PDFs uma única vez e salva versão comprimida
"""
import os
import json
import hashlib
import pickle
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from datetime import datetime
try:
    import PyPDF2
    pdf_reader = 'PyPDF2'
except ImportError:
    try:
        import pdfplumber
        pdf_reader = 'pdfplumber'
    except ImportError:
        pdf_reader = None
from .digilang_simple import get_digilang_compressor, get_token_optimizer
logger = logging.getLogger(__name__)

class DigiLangTranslator:
    """
    Tradutor de PDFs para formato DigiLang comprimido.
    Processa uma vez, usa para sempre.
    """

    def __init__(self, source_dir: str=None, target_dir: str=None):
        """
        Inicializa o tradutor.

        Args:
            source_dir: Diretório com PDFs originais
            target_dir: Diretório para arquivos DigiLang
        """
        self.source_dir = Path(source_dir or '/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        self.target_dir = Path(target_dir or '/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG/DIGILANG_ROTEIROS')
        self._create_directory_structure()
        self.compressor = get_digilang_compressor()
        self.optimizer = get_token_optimizer()
        self.stats = {'total_files': 0, 'processed': 0, 'success': 0, 'failed': 0, 'total_original_size': 0, 'total_compressed_size': 0, 'processing_time': 0, 'compression_ratios': []}
        self.index_path = self.target_dir / '.digilang_index.json'
        self.index = self._load_index()
        logger.info(f'DigiLang Translator inicializado: {self.source_dir} -> {self.target_dir}')

    def _create_directory_structure(self):
        """Cria estrutura de diretórios espelhada."""
        for subdir in ['roteiros_mestres', 'teoria', 'meus_filmes']:
            source_subdir = self.source_dir / subdir
            if source_subdir.exists():
                target_subdir = self.target_dir / subdir
                target_subdir.mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> Dict:
        """Carrega índice de arquivos já processados."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_index(self):
        """Salva índice de arquivos processados."""
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def extract_pdf_text(self, pdf_path: Path) -> Optional[str]:
        """
        Extrai texto de PDF.

        Args:
            pdf_path: Caminho do PDF

        Returns:
            Texto extraído ou None
        """
        if pdf_reader == 'PyPDF2':
            return self._extract_with_pypdf2(pdf_path)
        elif pdf_reader == 'pdfplumber':
            return self._extract_with_pdfplumber(pdf_path)
        else:
            try:
                with open(pdf_path, 'rb') as f:
                    content = f.read()
                    text = self._extract_ascii_from_binary(content)
                    return text if text else None
            except Exception as e:
                logger.error(f'Erro ao extrair {pdf_path}: {e}')
                return None

    def _extract_with_pypdf2(self, pdf_path: Path) -> Optional[str]:
        """Extrai usando PyPDF2."""
        try:
            text = []
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            logger.error(f'PyPDF2 error: {e}')
            return None

    def _extract_with_pdfplumber(self, pdf_path: Path) -> Optional[str]:
        """Extrai usando pdfplumber."""
        try:
            import pdfplumber
            text = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text.append(page.extract_text() or '')
            return '\n'.join(text)
        except Exception as e:
            logger.error(f'pdfplumber error: {e}')
            return None

    def _extract_ascii_from_binary(self, content: bytes) -> str:
        """Extração básica de texto ASCII de binário."""
        text_parts = []
        current_text = []
        for byte in content:
            if 32 <= byte <= 126:
                current_text.append(chr(byte))
            elif current_text:
                if len(current_text) > 10:
                    text_parts.append(''.join(current_text))
                current_text = []
        return ' '.join(text_parts)

    def translate_file(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Traduz um arquivo PDF para DigiLang.

        Args:
            pdf_path: Caminho do PDF

        Returns:
            Relatório da tradução
        """
        start_time = time.time()
        file_id = hashlib.md5(str(pdf_path).encode()).hexdigest()[:12]
        if file_id in self.index:
            logger.info(f'Arquivo já processado: {pdf_path.name}')
            return self.index[file_id]
        report = {'file_id': file_id, 'source_path': str(pdf_path), 'original_size': pdf_path.stat().st_size, 'status': 'processing'}
        try:
            logger.info(f'Extraindo texto de {pdf_path.name}...')
            text = self.extract_pdf_text(pdf_path)
            if not text:
                report['status'] = 'failed'
                report['error'] = 'Não foi possível extrair texto'
                return report
            text = self._clean_text(text)
            original_size = len(text)
            logger.info(f'Comprimindo {pdf_path.name}...')
            compressed, ratio = self.compressor.compress(text)
            optimized, metrics = self.optimizer.optimize(compressed, 'aggressive')
            metadata = {'original_name': pdf_path.name, 'original_size': original_size, 'compressed_size': len(optimized), 'compression_ratio': ratio, 'optimization_metrics': metrics, 'processed_at': datetime.now().isoformat(), 'checksum': hashlib.md5(text.encode()).hexdigest()}
            relative_path = pdf_path.relative_to(self.source_dir)
            target_path = self.target_dir / relative_path.with_suffix('.dlg')
            target_path.parent.mkdir(parents=True, exist_ok=True)
            digilang_data = {'version': '1.0', 'metadata': metadata, 'compressed_text': optimized, 'index': self._create_text_index(text)}
            with open(target_path, 'wb') as f:
                pickle.dump(digilang_data, f)
            report.update({'status': 'success', 'target_path': str(target_path), 'original_size': original_size, 'compressed_size': len(optimized), 'compression_ratio': ratio, 'processing_time': time.time() - start_time})
            self.index[file_id] = report
            self._save_index()
            self.stats['processed'] += 1
            self.stats['total_original_size'] += original_size
            self.stats['total_compressed_size'] += len(optimized)
            logger.info(f'✓ {pdf_path.name}: {ratio:.2%} compressão')
        except Exception as e:
            logger.error(f'Erro ao processar {pdf_path}: {e}')
            report['status'] = 'failed'
            report['error'] = str(e)
            self.stats['failed'] += 1
        return report

    def _clean_text(self, text: str) -> str:
        """Limpa e normaliza texto extraído."""
        import re
        text = re.sub('\\s+', ' ', text)
        text = ''.join((char for char in text if ord(char) >= 32 or char == '\n'))
        text = re.sub('\\n{3,}', '\n\n', text)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            if re.match('^\\s*\\d+\\s*$', line):
                continue
            if len(line.strip()) < 3:
                continue
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

    def _create_text_index(self, text: str) -> Dict:
        """Cria índice do texto para busca rápida."""
        sections = text.split('\n\n')
        index = {'sections_count': len(sections), 'keywords': self._extract_keywords(text), 'characters': self._extract_characters(text), 'scenes': self._extract_scenes(text)}
        return index

    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave do texto."""
        import re
        keywords = []
        patterns = ['INT\\.\\s+(\\w+)', 'EXT\\.\\s+(\\w+)', '^([A-Z]+)$']
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            keywords.extend(matches)
        return list(set(keywords))[:50]

    def _extract_characters(self, text: str) -> List[str]:
        """Extrai nomes de personagens."""
        import re
        pattern = '^([A-Z][A-Z\\s]+)$'
        matches = re.findall(pattern, text, re.MULTILINE)
        characters = []
        for match in matches:
            name = match.strip()
            if 2 < len(name) < 30:
                characters.append(name)
        return list(set(characters))

    def _extract_scenes(self, text: str) -> List[str]:
        """Extrai cabeçalhos de cenas."""
        import re
        pattern = '(INT\\.|EXT\\.)[^\\n]+'
        scenes = re.findall(pattern, text)
        return scenes[:100]

    def translate_all(self, max_workers: int=4) -> Dict[str, Any]:
        """
        Traduz todos os PDFs em paralelo.

        Args:
            max_workers: Número de workers paralelos

        Returns:
            Relatório completo
        """
        start_time = time.time()
        pdf_files = []
        for ext in ['*.pdf', '*.PDF']:
            pdf_files.extend(self.source_dir.rglob(ext))
        self.stats['total_files'] = len(pdf_files)
        logger.info(f'Iniciando tradução de {len(pdf_files)} arquivos...')
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.translate_file, pdf): pdf for pdf in pdf_files}
            for future in as_completed(futures):
                pdf = futures[future]
                try:
                    report = future.result()
                    if report['status'] == 'success':
                        print(f'✓ {pdf.name}')
                    else:
                        print(f"✗ {pdf.name}: {report.get('error', 'Unknown error')}")
                except Exception as e:
                    print(f'✗ {pdf.name}: {e}')
                    self.stats['failed'] += 1
        self.stats['processing_time'] = time.time() - start_time
        if self.stats['total_original_size'] > 0:
            self.stats['average_compression'] = 1 - self.stats['total_compressed_size'] / self.stats['total_original_size']
        else:
            self.stats['average_compression'] = 0
        report_path = self.target_dir / 'translation_report.json'
        with open(report_path, 'w') as f:
            json.dump({'stats': self.stats, 'timestamp': datetime.now().isoformat(), 'source_dir': str(self.source_dir), 'target_dir': str(self.target_dir)}, f, indent=2)
        self.stats['files_processed'] = self.stats['success'] + self.stats['failed']
        self.stats['avg_compression'] = self.stats.get('average_compression', 0)
        self.stats['total_saved'] = self.stats.get('total_original_size', 0) - self.stats.get('total_compressed_size', 0)
        self.stats['total_time'] = self.stats.get('processing_time', 0)
        return self.stats

class DigiLangSearcher:
    """
    Sistema de busca otimizado em arquivos DigiLang.
    Busca primeiro em DigiLang, fallback para originais.
    """

    def __init__(self, digilang_dir: str=None, fallback_dir: str=None):
        """
        Inicializa o buscador.

        Args:
            digilang_dir: Diretório com arquivos DigiLang
            fallback_dir: Diretório com PDFs originais (fallback)
        """
        self.digilang_dir = Path(digilang_dir or '/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG/DIGILANG_ROTEIROS')
        self.fallback_dir = Path(fallback_dir or '/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        self.dlg_dir = self.digilang_dir
        self.pdf_dir = self.fallback_dir
        self.index = self._load_master_index()
        self.cache = {}
        logger.info(f'DigiLang Searcher inicializado com {len(self.index)} arquivos')

    def _load_master_index(self) -> Dict:
        """Carrega índice mestre de todos os arquivos DigiLang."""
        index = {}
        for dlg_file in self.digilang_dir.rglob('*.dlg'):
            try:
                with open(dlg_file, 'rb') as f:
                    data = pickle.load(f)
                    file_id = hashlib.md5(str(dlg_file).encode()).hexdigest()[:12]
                    index[file_id] = {'path': str(dlg_file), 'metadata': data['metadata'], 'index': data.get('index', {})}
            except Exception as e:
                logger.error(f'Erro ao carregar {dlg_file}: {e}')
        return index

    def search(self, query: str, max_results: int=10) -> List[Dict]:
        """
        Busca nos arquivos DigiLang.

        Args:
            query: Query de busca
            max_results: Máximo de resultados

        Returns:
            Lista de resultados
        """
        results = []
        query_lower = query.lower()
        for file_id, file_info in self.index.items():
            relevance = 0
            if 'index' in file_info:
                keywords = file_info['index'].get('keywords', [])
                for keyword in keywords:
                    if query_lower in keyword.lower():
                        relevance += 2
                characters = file_info['index'].get('characters', [])
                for char in characters:
                    if query_lower in char.lower():
                        relevance += 3
                scenes = file_info['index'].get('scenes', [])
                for scene in scenes[:20]:
                    if query_lower in scene.lower():
                        relevance += 1
            if relevance > 0:
                results.append({'file_id': file_id, 'name': file_info['metadata']['original_name'], 'relevance': relevance, 'compression_ratio': file_info['metadata']['compression_ratio'], 'path': file_info['path']})
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:max_results]

    def get_content(self, file_id: str) -> Optional[str]:
        """
        Recupera conteúdo de um arquivo.

        Args:
            file_id: ID do arquivo

        Returns:
            Conteúdo descomprimido ou None
        """
        if file_id in self.cache:
            return self.cache[file_id]
        if file_id not in self.index:
            return None
        try:
            dlg_path = Path(self.index[file_id]['path'])
            with open(dlg_path, 'rb') as f:
                data = pickle.load(f)
            compressed_text = data['compressed_text']
            decompressed = self._decompress(compressed_text)
            self.cache[file_id] = decompressed
            return decompressed
        except Exception as e:
            logger.error(f'Erro ao recuperar conteúdo {file_id}: {e}')
            return self._fallback_to_original(file_id)

    def _decompress(self, compressed_text: str) -> str:
        """Descomprime texto DigiLang."""
        compressor = get_digilang_compressor()
        return compressor.decompress(compressed_text)

    def _fallback_to_original(self, file_id: str) -> Optional[str]:
        """Fallback para PDF original se DigiLang falhar."""
        logger.info(f'Fallback para PDF original: {file_id}')
        if file_id in self.index:
            original_name = self.index[file_id]['metadata']['original_name']
            for pdf_path in self.fallback_dir.rglob(original_name):
                translator = DigiLangTranslator()
                text = translator.extract_pdf_text(pdf_path)
                if text:
                    return text
        return None
_translator: Optional[DigiLangTranslator] = None
_searcher: Optional[DigiLangSearcher] = None

def get_translator() -> DigiLangTranslator:
    """Retorna instância singleton do tradutor."""
    global _translator
    if _translator is None:
        _translator = DigiLangTranslator()
    return _translator

def get_searcher() -> DigiLangSearcher:
    """Retorna instância singleton do buscador."""
    global _searcher
    if _searcher is None:
        _searcher = DigiLangSearcher()
    return _searcher