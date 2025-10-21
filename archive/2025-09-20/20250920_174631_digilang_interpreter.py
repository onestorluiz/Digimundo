#!/usr/bin/env python3
"""
DigiLang Interpreter - Módulo de Interpretação para AI/Ollama/Digimon
======================================================================

Este módulo permite que qualquer AI, Ollama ou Digimon interprete
arquivos comprimidos com DigiLang V23 ULTIMATE.

Autor: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
import tiktoken

logger = logging.getLogger(__name__)


class DigiLangInterpreter:
    """
    Interpretador universal para arquivos DigiLang

    Funcionalidades:
    - Decodifica textos comprimidos
    - Fornece acesso ao conteúdo original
    - Calcula estatísticas
    - Interface simples para AI/Ollama
    """

    def __init__(self):
        """Inicializar interpretador"""
        self.encoder = tiktoken.get_encoding("cl100k_base")
        logger.info("🔍 DigiLang Interpreter inicializado")

    def load_compressed_package(self, package_dir: str) -> Dict[str, Any]:
        """
        Carregar pacote completo de compressão

        Args:
            package_dir: Diretório contendo os arquivos comprimidos

        Returns:
            Dict com todos os dados do pacote
        """
        package_path = Path(package_dir)

        if not package_path.exists():
            raise FileNotFoundError(f"Pacote não encontrado: {package_dir}")

        package = {}

        # Carregar texto comprimido
        compressed_file = package_path / "compressed_text.txt"
        if compressed_file.exists():
            with open(compressed_file, 'r', encoding='utf-8') as f:
                package['compressed_text'] = f.read()

        # Carregar dicionário
        dict_file = package_path / "dictionary.json"
        if dict_file.exists():
            with open(dict_file, 'r', encoding='utf-8') as f:
                package['dictionary'] = json.load(f)

        # Carregar metadados
        meta_file = package_path / "metadata.json"
        if meta_file.exists():
            with open(meta_file, 'r', encoding='utf-8') as f:
                package['metadata'] = json.load(f)

        return package

    def decompress(self, compressed_text: str, dictionary: Dict[str, Dict]) -> str:
        """
        Descomprimir texto usando dicionário

        Args:
            compressed_text: Texto com símbolos Unicode
            dictionary: Dicionário símbolo→texto

        Returns:
            Texto original descomprimido
        """
        decompressed = compressed_text

        # Ordenar por tamanho do símbolo (evitar substituições parciais)
        sorted_items = sorted(
            dictionary.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for symbol, info in sorted_items:
            original_text = info['text'] if isinstance(info, dict) else info
            decompressed = decompressed.replace(symbol, original_text)

        return decompressed

    def interpret(self, package_dir: str) -> Dict[str, Any]:
        """
        Interpretar pacote completo e retornar análise

        Args:
            package_dir: Diretório do pacote DigiLang

        Returns:
            Dict com texto descomprimido e estatísticas
        """
        # Carregar pacote
        package = self.load_compressed_package(package_dir)

        # Descomprimir
        decompressed_text = self.decompress(
            package['compressed_text'],
            package['dictionary']
        )

        # Calcular estatísticas
        compressed_tokens = len(self.encoder.encode(package['compressed_text']))
        decompressed_tokens = len(self.encoder.encode(decompressed_text))

        result = {
            'success': True,
            'decompressed_text': decompressed_text,
            'stats': {
                'compressed_tokens': compressed_tokens,
                'decompressed_tokens': decompressed_tokens,
                'compression_rate': package['metadata']['stats']['token_compression'],
                'dictionary_size': len(package['dictionary']),
                'substitutions': package['metadata']['stats']['substitutions_made']
            },
            'metadata': package['metadata']
        }

        return result

    def get_summary(self, package_dir: str) -> str:
        """
        Obter resumo do pacote sem descomprimir completamente

        Args:
            package_dir: Diretório do pacote

        Returns:
            String com resumo formatado
        """
        package = self.load_compressed_package(package_dir)
        meta = package['metadata']
        stats = meta['stats']

        summary = f"""
📄 Documento: {meta['pdf_name']}
📊 Compressão: {stats['token_compression']:.2f}%
💾 Economia: {stats['tokens_saved']:,} tokens
📚 Dicionário: {stats['dictionary_size']} padrões
🔤 Símbolos disponíveis: {meta['symbols_available']['1_token']} (1-token), {meta['symbols_available']['2_token']} (2-token)
⏰ Processado em: {meta['timestamp']}
"""
        return summary

    def search_in_compressed(self, package_dir: str, search_term: str) -> bool:
        """
        Buscar termo no texto comprimido

        Args:
            package_dir: Diretório do pacote
            search_term: Termo a buscar

        Returns:
            True se encontrado, False caso contrário
        """
        result = self.interpret(package_dir)
        return search_term.lower() in result['decompressed_text'].lower()

    def extract_section(self, package_dir: str, start_marker: str, end_marker: str) -> Optional[str]:
        """
        Extrair seção específica do texto

        Args:
            package_dir: Diretório do pacote
            start_marker: Marcador de início
            end_marker: Marcador de fim

        Returns:
            Texto da seção ou None
        """
        result = self.interpret(package_dir)
        text = result['decompressed_text']

        start_idx = text.find(start_marker)
        if start_idx == -1:
            return None

        end_idx = text.find(end_marker, start_idx)
        if end_idx == -1:
            return None

        return text[start_idx:end_idx + len(end_marker)]


class OllamaDigiLangAdapter:
    """
    Adaptador específico para integração com Ollama
    """

    def __init__(self):
        """Inicializar adaptador"""
        self.interpreter = DigiLangInterpreter()

    def prepare_for_ollama(self, package_dir: str) -> Dict[str, Any]:
        """
        Preparar dados para processamento por Ollama

        Args:
            package_dir: Diretório do pacote

        Returns:
            Dict formatado para Ollama
        """
        result = self.interpreter.interpret(package_dir)

        return {
            'model': 'digilang-v23',
            'content': result['decompressed_text'],
            'metadata': {
                'original_format': 'PDF',
                'compression': f"{result['stats']['compression_rate']:.2f}%",
                'tokens_saved': result['stats']['decompressed_tokens'] - result['stats']['compressed_tokens']
            },
            'instructions': [
                'Este texto foi descomprimido de DigiLang V23',
                'Símbolos Unicode foram substituídos pelos textos originais',
                'O conteúdo está pronto para processamento'
            ]
        }

    def stream_decompressed(self, package_dir: str, chunk_size: int = 1000):
        """
        Stream do texto descomprimido em chunks

        Args:
            package_dir: Diretório do pacote
            chunk_size: Tamanho de cada chunk

        Yields:
            Chunks do texto descomprimido
        """
        result = self.interpreter.interpret(package_dir)
        text = result['decompressed_text']

        for i in range(0, len(text), chunk_size):
            yield text[i:i + chunk_size]


def main():
    """Exemplo de uso do interpretador"""
    interpreter = DigiLangInterpreter()

    # Exemplo: interpretar pacote do Dark Knight
    package_dir = "./output/v23_ultimate/The Dark Knight - Release"

    if Path(package_dir).exists():
        print("🔍 Interpretando pacote DigiLang...")

        # Obter resumo
        summary = interpreter.get_summary(package_dir)
        print(summary)

        # Interpretar completamente
        result = interpreter.interpret(package_dir)

        print(f"\n✅ Texto descomprimido:")
        print(f"   Tamanho: {len(result['decompressed_text']):,} caracteres")
        print(f"   Tokens: {result['stats']['decompressed_tokens']:,}")

        # Buscar termo
        if interpreter.search_in_compressed(package_dir, "Batman"):
            print("\n🦇 'Batman' encontrado no texto!")

        # Exemplo para Ollama
        ollama_adapter = OllamaDigiLangAdapter()
        ollama_data = ollama_adapter.prepare_for_ollama(package_dir)
        print(f"\n🤖 Dados preparados para Ollama:")
        print(f"   Modelo: {ollama_data['model']}")
        print(f"   Instruções: {len(ollama_data['instructions'])} items")

    else:
        print(f"❌ Pacote não encontrado: {package_dir}")
        print("   Execute primeiro o DigiLang V23 Ultimate para criar o pacote")


if __name__ == "__main__":
    main()