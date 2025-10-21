#!/usr/bin/env python3
"""
DigiLang Unified - Sistema completo PT→EN→DigiLang→EN→PT
Integra normalização linguística com compressão token-aware
"""

import json
from pathlib import Path
from typing import Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import tiktoken

from .screenplay_normalizer import ScreenplayNormalizer
from .digilang_v3_ta import DigiLangV3Encoder, DigiLangV3Decoder, TokenCounter


@dataclass
class UnifiedCompressionResult:
    """Resultado da compressão unificada."""
    # Textos
    original_pt: str
    normalized_en: str
    compressed: str
    decompressed_en: str
    final_pt: str
    
    # Métricas
    tokens_original_pt: int
    tokens_normalized_en: int
    tokens_compressed: int
    compression_ratio_total: float
    compression_ratio_en: float
    
    # Metadados
    language_mappings: Dict[str, str]
    macros_used: int
    reversible: bool
    

class DigiLangUnified:
    """
    Pipeline unificado de compressão:
    
    1. PT (original) → EN (normalizado)
    2. EN → DigiLang (comprimido)
    3. DigiLang → EN (descomprimido)
    4. EN → PT (revertido)
    
    Vantagens:
    - Padrões em inglês são mais consistentes
    - Termos técnicos em EN usam menos tokens
    - DigiLang otimizado para padrões Hollywood
    - Reversão completa PT↔EN
    """
    
    def __init__(self, max_macros: int = 100):
        self.normalizer = ScreenplayNormalizer()
        self.encoder = DigiLangV3Encoder(max_macros=max_macros)
        self.decoder = DigiLangV3Decoder()
        self.max_macros = max_macros
    
    def compress(self, text_pt: str) -> UnifiedCompressionResult:
        """
        Comprime texto PT através de normalização EN.
        
        Pipeline:
        PT → EN → DigiLang
        """
        
        # Passo 1: PT → EN (normalização)
        normalized = self.normalizer.normalize(text_pt)
        text_en = normalized.normalized_text
        
        # Passo 2: EN → DigiLang (compressão)
        compressed_text, stats = self.encoder.encode(text_en)
        
        # Passo 3: DigiLang → EN (descompressão para validação)
        decompressed_en = self.decoder.decode(compressed_text)
        
        # Passo 4: EN → PT (reversão)
        final_pt = self.normalizer.denormalize(decompressed_en, normalized.language_map)
        
        # Calcula métricas
        tokens_pt = TokenCounter.count(text_pt)
        tokens_en = TokenCounter.count(text_en)
        tokens_compressed = stats['tokens_encoded']
        
        return UnifiedCompressionResult(
            original_pt=text_pt,
            normalized_en=text_en,
            compressed=compressed_text,
            decompressed_en=decompressed_en,
            final_pt=final_pt,
            tokens_original_pt=tokens_pt,
            tokens_normalized_en=tokens_en,
            tokens_compressed=tokens_compressed,
            compression_ratio_total=1 - (tokens_compressed / tokens_pt),
            compression_ratio_en=1 - (tokens_compressed / tokens_en),
            language_mappings=normalized.language_map,
            macros_used=stats.get('macros_used', 0),
            reversible=(final_pt.strip() == text_pt.strip())
        )
    
    def decompress(self, compressed_text: str, language_map: Dict[str, str]) -> str:
        """
        Descomprime e reverte para PT.
        
        Pipeline:
        DigiLang → EN → PT
        """
        
        # DigiLang → EN
        text_en = self.decoder.decode(compressed_text)
        
        # EN → PT
        text_pt = self.normalizer.denormalize(text_en, language_map)
        
        return text_pt


def test_unified_compression():
    """Testa compressão unificada."""
    
    # Texto de teste em PT com repetições
    test_text = """
INT. ESCRITÓRIO - DIA

JOÃO entra. Ele olha para MARIA.

JOÃO
Onde você estava?

MARIA
Esperando.

CORTA PARA:

INT. SALA - DIA

JOÃO entra novamente. MARIA está sentada.

JOÃO
Precisamos conversar.

CORTA PARA:

EXT. PARQUE - NOITE

MARIA está sentada no banco. JOÃO chega.

FADE OUT.

INT. CASA - DIA

JOÃO entra pela porta. Ele olha ao redor.

CORTA PARA:

INT. QUARTO - NOITE

MARIA está deitada. JOÃO entra.

FADE OUT.
"""
    
    print("="*60)
    print("TESTE DE COMPRESSÃO UNIFICADA PT→EN→DIGILANG")
    print("="*60)
    
    # Cria pipeline
    unified = DigiLangUnified(max_macros=100)
    
    # Comprime
    result = unified.compress(test_text)
    
    print(f"\n1. ORIGINAL (PT): {result.tokens_original_pt} tokens")
    print(test_text[:200] + "...")
    
    print(f"\n2. NORMALIZADO (EN): {result.tokens_normalized_en} tokens")
    print(result.normalized_en[:200] + "...")
    
    print(f"\n3. COMPRIMIDO (DIGILANG): {result.tokens_compressed} tokens")
    print(result.compressed[:200] + "...")
    
    print("\n" + "="*60)
    print("MÉTRICAS DE COMPRESSÃO")
    print("="*60)
    print(f"Tokens PT original:     {result.tokens_original_pt:,}")
    print(f"Tokens EN normalizado:  {result.tokens_normalized_en:,}")
    print(f"Tokens comprimido:      {result.tokens_compressed:,}")
    print(f"Compressão total (PT):  {result.compression_ratio_total:.1%}")
    print(f"Compressão EN:          {result.compression_ratio_en:.1%}")
    print(f"Macros usadas:          {result.macros_used}")
    print(f"Reversível:             {result.reversible}")
    
    if result.compression_ratio_total > 0:
        print(f"\n✅ SUCESSO! Economia de {result.tokens_original_pt - result.tokens_compressed} tokens")
    else:
        print(f"\n⚠️ Sem compressão efetiva")
    
    # Testa reversão
    print("\n" + "="*60)
    print("TESTE DE REVERSÃO")
    print("="*60)
    
    reverted = unified.decompress(result.compressed, result.language_mappings)
    print(f"Reversão perfeita: {reverted.strip() == test_text.strip()}")
    
    if reverted.strip() != test_text.strip():
        print("\nDiferenças:")
        import difflib
        diff = difflib.unified_diff(
            test_text.splitlines(),
            reverted.splitlines(),
            lineterm=''
        )
        for line in list(diff)[:10]:
            print(line)


if __name__ == "__main__":
    test_unified_compression()