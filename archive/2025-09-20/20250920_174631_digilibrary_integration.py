"""
DigiLibrary Integration - Sistema de integração com biblioteca de roteiros.
Usa DigiLang para compressão e indexação eficiente.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime

# Import DigiLang components
try:
    from .digilang.encoder import Encoder as DigiLangEncoder
    from .digilang.decoder import Decoder as DigiLangDecoder
    from .digilang.tokenizer import Tokenizer
    from .digilang.tpd_adaptive import TPDAdaptive as AdaptiveTPD
except ImportError:
    # Fallback imports if names are different
    try:
        from .digilang import encoder, decoder
        DigiLangEncoder = getattr(encoder, 'DigiLangEncoder', object)
        DigiLangDecoder = getattr(decoder, 'DigiLangDecoder', object)
        Tokenizer = object
        AdaptiveTPD = object
    except:
        # Minimal fallback
        DigiLangEncoder = object
        DigiLangDecoder = object
        Tokenizer = object
        AdaptiveTPD = object

logger = logging.getLogger(__name__)


class DigiLibraryManager:
    """
    Gerenciador da biblioteca de roteiros com compressão DigiLang.
    Integra PDFs de roteiros e teoria cinematográfica.
    """

    def __init__(self, library_path: Optional[str] = None):
        """
        Inicializa o gerenciador da biblioteca.

        Args:
            library_path: Caminho para a biblioteca de roteiros
        """
        self.library_path = Path(library_path or "/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")

        # Inicializa DigiLang
        self.tokenizer = Tokenizer()
        self.encoder = DigiLangEncoder()
        self.decoder = DigiLangDecoder()
        self.tpd = AdaptiveTPD()

        # Índice de documentos
        self.index = {}
        self.compressed_cache = {}

        # Estatísticas
        self.stats = {
            'total_documents': 0,
            'total_size_original': 0,
            'total_size_compressed': 0,
            'compression_ratio': 0.0
        }

        # Carrega índice existente ou cria novo
        self._load_or_create_index()

        logger.info(f"DigiLibrary inicializada com {self.stats['total_documents']} documentos")

    def _load_or_create_index(self):
        """Carrega índice existente ou cria um novo."""
        index_path = self.library_path / ".digilibrary_index.json"

        if index_path.exists():
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.index = data.get('index', {})
                    self.stats = data.get('stats', self.stats)
                logger.info("Índice carregado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao carregar índice: {e}")
                self._build_index()
        else:
            self._build_index()

    def _build_index(self):
        """Constrói índice da biblioteca."""
        logger.info("Construindo índice da biblioteca...")

        categories = {
            'roteiros_mestres': 'master_scripts',
            'teoria': 'theory',
            'meus_filmes': 'my_films'
        }

        for category_dir, category_name in categories.items():
            category_path = self.library_path / category_dir

            if not category_path.exists():
                continue

            for file_path in category_path.rglob("*.pdf"):
                doc_id = self._generate_doc_id(file_path)

                self.index[doc_id] = {
                    'path': str(file_path),
                    'name': file_path.stem,
                    'category': category_name,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'compressed': False,
                    'compression_ratio': 0.0
                }

                self.stats['total_documents'] += 1
                self.stats['total_size_original'] += file_path.stat().st_size

        self._save_index()
        logger.info(f"Índice construído: {self.stats['total_documents']} documentos encontrados")

    def _generate_doc_id(self, file_path: Path) -> str:
        """Gera ID único para documento."""
        content = f"{file_path.name}{file_path.stat().st_size}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _save_index(self):
        """Salva índice em disco."""
        index_path = self.library_path / ".digilibrary_index.json"

        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'index': self.index,
                    'stats': self.stats,
                    'updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar índice: {e}")

    def compress_document(self, doc_id: str) -> Tuple[bool, float]:
        """
        Comprime documento usando DigiLang.

        Args:
            doc_id: ID do documento

        Returns:
            (sucesso, taxa_compressão)
        """
        if doc_id not in self.index:
            return False, 0.0

        doc_info = self.index[doc_id]

        try:
            # Lê conteúdo do PDF (simplificado - em produção usar PyPDF2)
            with open(doc_info['path'], 'rb') as f:
                content = f.read()

            # Converte para texto (placeholder - usar extração real de PDF)
            text = str(content[:10000])  # Primeiros 10KB para teste

            # Tokeniza
            tokens = self.tokenizer.tokenize(text)

            # Comprime com DigiLang
            compressed = self.encoder.encode(tokens)

            # Calcula taxa de compressão
            original_size = len(text.encode())
            compressed_size = len(compressed)
            compression_ratio = 1 - (compressed_size / original_size)

            # Armazena no cache
            self.compressed_cache[doc_id] = compressed

            # Atualiza índice
            doc_info['compressed'] = True
            doc_info['compression_ratio'] = compression_ratio
            doc_info['compressed_size'] = compressed_size

            self.stats['total_size_compressed'] += compressed_size

            logger.info(f"Documento {doc_info['name']} comprimido: {compression_ratio:.2%} de redução")

            return True, compression_ratio

        except Exception as e:
            logger.error(f"Erro ao comprimir documento {doc_id}: {e}")
            return False, 0.0

    def decompress_document(self, doc_id: str) -> Optional[str]:
        """
        Descomprime documento.

        Args:
            doc_id: ID do documento

        Returns:
            Texto descomprimido ou None
        """
        if doc_id not in self.compressed_cache:
            return None

        try:
            compressed = self.compressed_cache[doc_id]
            tokens = self.decoder.decode(compressed)
            text = self.tokenizer.detokenize(tokens)
            return text
        except Exception as e:
            logger.error(f"Erro ao descomprimir documento {doc_id}: {e}")
            return None

    def search(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Busca documentos na biblioteca.

        Args:
            query: Query de busca
            category: Categoria opcional para filtrar

        Returns:
            Lista de documentos encontrados
        """
        results = []
        query_lower = query.lower()

        for doc_id, doc_info in self.index.items():
            # Filtro por categoria
            if category and doc_info['category'] != category:
                continue

            # Busca no nome
            if query_lower in doc_info['name'].lower():
                results.append({
                    'id': doc_id,
                    'name': doc_info['name'],
                    'category': doc_info['category'],
                    'relevance': 1.0
                })

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas da biblioteca."""
        if self.stats['total_size_original'] > 0:
            self.stats['compression_ratio'] = 1 - (
                self.stats['total_size_compressed'] / self.stats['total_size_original']
            )

        return {
            **self.stats,
            'categories': {
                'master_scripts': len([d for d in self.index.values() if d['category'] == 'master_scripts']),
                'theory': len([d for d in self.index.values() if d['category'] == 'theory']),
                'my_films': len([d for d in self.index.values() if d['category'] == 'my_films'])
            },
            'compressed_documents': len([d for d in self.index.values() if d['compressed']]),
            'cache_size': len(self.compressed_cache)
        }

    def process_all_documents(self, batch_size: int = 5) -> Dict[str, Any]:
        """
        Processa todos os documentos da biblioteca.

        Args:
            batch_size: Tamanho do batch para processamento

        Returns:
            Relatório do processamento
        """
        report = {
            'processed': 0,
            'compressed': 0,
            'failed': 0,
            'avg_compression': 0.0
        }

        total_compression = 0.0

        for i, doc_id in enumerate(self.index.keys()):
            if self.index[doc_id]['compressed']:
                continue

            success, ratio = self.compress_document(doc_id)

            if success:
                report['compressed'] += 1
                total_compression += ratio
            else:
                report['failed'] += 1

            report['processed'] += 1

            # Salva índice a cada batch
            if (i + 1) % batch_size == 0:
                self._save_index()

        # Calcula média de compressão
        if report['compressed'] > 0:
            report['avg_compression'] = total_compression / report['compressed']

        self._save_index()

        return report


class DigiLangIntegration:
    """
    Integração do DigiLang com o pipeline principal.
    """

    def __init__(self):
        """Inicializa a integração."""
        self.library_manager = DigiLibraryManager()
        self.encoder = DigiLangEncoder()
        self.decoder = DigiLangDecoder()

        logger.info("DigiLang Integration inicializada")

    def compress_text(self, text: str) -> Tuple[str, float]:
        """
        Comprime texto usando DigiLang.

        Args:
            text: Texto para comprimir

        Returns:
            (texto_comprimido, taxa_compressão)
        """
        try:
            original_size = len(text.encode())
            compressed = self.encoder.encode_text(text)
            compressed_size = len(compressed.encode() if isinstance(compressed, str) else compressed)

            compression_ratio = 1 - (compressed_size / original_size)

            return compressed, compression_ratio

        except Exception as e:
            logger.error(f"Erro na compressão: {e}")
            return text, 0.0

    def decompress_text(self, compressed_text: str) -> str:
        """
        Descomprime texto.

        Args:
            compressed_text: Texto comprimido

        Returns:
            Texto original
        """
        try:
            return self.decoder.decode_text(compressed_text)
        except Exception as e:
            logger.error(f"Erro na descompressão: {e}")
            return compressed_text

    def optimize_for_ollama(self, prompt: str) -> str:
        """
        Otimiza prompt para Ollama usando compressão DigiLang.

        Args:
            prompt: Prompt original

        Returns:
            Prompt otimizado
        """
        # Se prompt muito grande, comprime partes menos importantes
        if len(prompt) > 10000:
            # Divide em seções
            sections = prompt.split('\n\n')
            optimized = []

            for section in sections:
                if len(section) > 1000:
                    # Comprime seções grandes
                    compressed, ratio = self.compress_text(section)
                    if ratio > 0.3:  # Se boa compressão
                        optimized.append(f"[COMPRESSED: {ratio:.1%}]\n{compressed[:500]}...")
                    else:
                        optimized.append(section[:500] + "...")
                else:
                    optimized.append(section)

            return '\n\n'.join(optimized)

        return prompt

    def enrich_with_library(self, query: str) -> str:
        """
        Enriquece query com conhecimento da biblioteca.

        Args:
            query: Query original

        Returns:
            Query enriquecida
        """
        # Busca documentos relevantes
        relevant_docs = self.library_manager.search(query)

        if relevant_docs:
            enrichment = "\n\n[CONHECIMENTO DA BIBLIOTECA]:\n"
            for doc in relevant_docs[:3]:  # Top 3
                enrichment += f"- {doc['name']} ({doc['category']})\n"

            return query + enrichment

        return query


# Singleton global
_digilibrary_manager: Optional[DigiLibraryManager] = None
_digilang_integration: Optional[DigiLangIntegration] = None


def get_digilibrary_manager() -> DigiLibraryManager:
    """Retorna instância singleton do DigiLibrary Manager."""
    global _digilibrary_manager
    if _digilibrary_manager is None:
        _digilibrary_manager = DigiLibraryManager()
    return _digilibrary_manager


def get_digilang_integration() -> DigiLangIntegration:
    """Retorna instância singleton da integração DigiLang."""
    global _digilang_integration
    if _digilang_integration is None:
        _digilang_integration = DigiLangIntegration()
    return _digilang_integration