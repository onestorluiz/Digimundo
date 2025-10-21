#!/usr/bin/env python3
"""
📚 DigiLang Dictionary Manager
Sistema para salvar/carregar dicionários de tradução únicos para cada texto/PDF
Cada arquivo tem seu próprio conjunto de símbolos e padrões
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DigiLangDictionary:
    """Gerenciador de dicionários de tradução para DigiLang"""

    def __init__(self, dict_dir: str = "data/digilang_dicts"):
        self.dict_dir = Path(dict_dir)
        self.dict_dir.mkdir(parents=True, exist_ok=True)
        self.current_dict = None
        self.current_file_id = None

    def create_file_id(self, text: str) -> str:
        """Cria ID único para o texto/arquivo"""
        # Usa hash do início do texto para identificar
        text_sample = text[:1000] if len(text) > 1000 else text
        return hashlib.md5(text_sample.encode()).hexdigest()[:16]

    def save_dictionary(self, file_id: str, compressed_text: str,
                       layers: List[Dict], original_size: int) -> str:
        """Salva dicionário de tradução para um arquivo específico"""
        dict_path = self.dict_dir / f"{file_id}.digidict"

        dictionary = {
            'file_id': file_id,
            'compressed_text': compressed_text,
            'layers': layers,
            'original_size': original_size,
            'compression_rate': 1 - (len(compressed_text) / original_size),
            'version': 'v26_mega_multilayer'
        }

        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=2)

        logger.info(f"📚 Dicionário salvo: {file_id} ({len(layers)} layers)")
        return str(dict_path)

    def load_dictionary(self, file_id: str) -> Optional[Dict]:
        """Carrega dicionário de tradução"""
        dict_path = self.dict_dir / f"{file_id}.digidict"

        if not dict_path.exists():
            logger.warning(f"❌ Dicionário não encontrado: {file_id}")
            return None

        with open(dict_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)

        logger.info(f"📚 Dicionário carregado: {file_id}")
        return dictionary

    def compress_with_dict(self, text: str, save: bool = True) -> Tuple[str, str]:
        """Comprime texto e salva dicionário"""
        from apps.scripturemon.digilang_v26_mega_multilayer import DigiLangV26MegaMultiLayer

        # Cria ID único para o texto
        file_id = self.create_file_id(text)

        # Verifica se já existe dicionário
        existing = self.load_dictionary(file_id)
        if existing:
            logger.info(f"✅ Usando dicionário existente: {file_id}")
            return existing['compressed_text'], file_id

        # Comprime o texto
        digilang = DigiLangV26MegaMultiLayer()
        compressed, layers, stats = digilang.compress(text)

        # Salva dicionário se solicitado
        if save:
            self.save_dictionary(file_id, compressed, layers, len(text))

        return compressed, file_id

    def decompress_with_dict(self, compressed_text: str, file_id: str) -> str:
        """Descomprime usando dicionário salvo"""
        from apps.scripturemon.digilang_v26_mega_multilayer import DigiLangV26MegaMultiLayer

        # Carrega dicionário
        dictionary = self.load_dictionary(file_id)
        if not dictionary:
            logger.error(f"❌ Não é possível descomprimir sem dicionário: {file_id}")
            return compressed_text

        # Descomprime usando as layers salvas
        digilang = DigiLangV26MegaMultiLayer()
        decompressed = digilang.decompress(compressed_text, dictionary['layers'])

        return decompressed

    def list_dictionaries(self) -> List[Dict]:
        """Lista todos os dicionários salvos"""
        dictionaries = []

        for dict_path in self.dict_dir.glob("*.digidict"):
            try:
                with open(dict_path, 'r') as f:
                    dict_info = json.load(f)
                    dictionaries.append({
                        'file_id': dict_info['file_id'],
                        'compression_rate': dict_info.get('compression_rate', 0),
                        'layers': len(dict_info.get('layers', [])),
                        'size': len(dict_info.get('compressed_text', ''))
                    })
            except:
                continue

        return dictionaries


def fix_digilang_test():
    """Corrige o teste do DigiLang para usar dicionários"""
    print("\n" + "="*60)
    print("🔧 FIXING DIGILANG TEST WITH DICTIONARIES")
    print("="*60)

    manager = DigiLangDictionary()

    # Texto de teste
    original = "FADE IN: INT. OFFICE - DAY\nJohn enters the room." * 10
    print(f"\n📄 Original: {len(original)} chars")
    print(f"First 50: {original[:50]}...")

    # Comprime e salva dicionário
    compressed, file_id = manager.compress_with_dict(original)
    print(f"\n✅ Compressed: {len(compressed)} chars")
    print(f"📚 Dictionary ID: {file_id}")
    print(f"💾 Compression: {(1 - len(compressed)/len(original))*100:.1f}%")

    # Descomprime usando dicionário
    decompressed = manager.decompress_with_dict(compressed, file_id)
    print(f"\n📄 Decompressed: {len(decompressed)} chars")
    print(f"First 50: {decompressed[:50]}...")

    # Verifica se funcionou
    if decompressed == original:
        print("\n✅ PERFEITO! Compressão e descompressão funcionando!")
        print("   Cada texto tem seu próprio dicionário de tradução")
    else:
        print("\n❌ Ainda há problemas na descompressão")
        print(f"   Original: {original[:100]}")
        print(f"   Decompressed: {decompressed[:100]}")

    # Lista dicionários
    print(f"\n📚 Dicionários salvos:")
    for dict_info in manager.list_dictionaries():
        print(f"  - {dict_info['file_id']}: {dict_info['compression_rate']*100:.1f}% compression")

    print("\n" + "="*60)
    return decompressed == original


if __name__ == "__main__":
    fix_digilang_test()