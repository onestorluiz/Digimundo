#!/usr/bin/env python3
"""
DigiLang Simple - Módulo de compressão simplificado
Baseado no sistema de validação para resolver imports ausentes
"""

import json
from typing import Dict, Tuple, Optional, Any

# Importa do sistema de validação se disponível
try:
    from .digilang_validation.api_fallback_improved import (
        DigiLangEncoder,
        DigiLangDecoder,
        to_digilang_improved,
        from_digilang_improved,
        serialize_message,
        deserialize_message
    )
    validation_available = True
except ImportError:
    validation_available = False

class ValidationCompressorWrapper:
    """Wrapper para tornar DigiLangEncoder compatível com interface compress/decompress"""

    def __init__(self):
        self.encoder = DigiLangEncoder()

    def compress(self, text: str) -> Tuple[str, float]:
        """Compressão usando validation encoder"""
        compressed = self.encoder.encode(text)
        ratio = len(compressed) / len(text) if text else 1.0
        return compressed, ratio

    def encode(self, text: str) -> str:
        """Método encode direto"""
        return self.encoder.encode(text)

    def decompress(self, text: str) -> str:
        """Descompressão usando validation"""
        return from_digilang_improved(text)

    def decode(self, text: str) -> str:
        """Método decode direto"""
        return self.decompress(text)

def get_digilang_compressor():
    """Retorna um compressor DigiLang"""
    if validation_available:
        return ValidationCompressorWrapper()
    else:
        # Fallback simples
        return SimpleCompressor()

def get_token_optimizer():
    """Retorna um otimizador de tokens"""
    if validation_available:
        return TokenOptimizer()
    else:
        return SimpleOptimizer()

class SimpleCompressor:
    """Compressor fallback quando validation não está disponível"""

    def compress(self, text: str) -> Tuple[str, float]:
        """Compressão básica"""
        # Substituições simples de padrões comuns
        replacements = {
            "FADE IN:": "↑",
            "FADE OUT.": "↓",
            "INT.": "→",
            "EXT.": "←",
            "CUT TO:": "✂",
            "CONTINUED": "⋯",
            "(V.O.)": "🔊",
            "(O.S.)": "📢"
        }

        compressed = text
        for pattern, symbol in replacements.items():
            compressed = compressed.replace(pattern, symbol)

        ratio = len(compressed) / len(text) if text else 1.0
        return compressed, ratio

    def encode(self, text: str) -> str:
        """Método encode compatível com validation"""
        compressed, _ = self.compress(text)
        return compressed

    def decompress(self, text: str) -> str:
        """Descompressão básica"""
        replacements = {
            "↑": "FADE IN:",
            "↓": "FADE OUT.",
            "→": "INT.",
            "←": "EXT.",
            "✂": "CUT TO:",
            "⋯": "CONTINUED",
            "🔊": "(V.O.)",
            "📢": "(O.S.)"
        }

        decompressed = text
        for symbol, pattern in replacements.items():
            decompressed = decompressed.replace(symbol, pattern)

        return decompressed

    def decode(self, text: str) -> str:
        """Método decode compatível com validation"""
        return self.decompress(text)

class SimpleOptimizer:
    """Otimizador de tokens fallback"""

    def optimize(self, text: str) -> str:
        """Otimização básica de tokens"""
        # Remove espaços duplos e normaliza
        import re
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def estimate_tokens(self, text: str) -> int:
        """Estimativa simples de tokens"""
        # Aproximação: 1 token = 4 caracteres
        return len(text) // 4

class TokenOptimizer:
    """Otimizador avançado quando validation está disponível"""

    def __init__(self):
        self.encoder = ValidationCompressorWrapper() if validation_available else SimpleCompressor()

    def optimize(self, text: str) -> str:
        """Otimiza texto para menor uso de tokens"""
        if validation_available:
            compressed, _ = to_digilang_improved(text, mode="aggressive")
            return compressed
        else:
            compressed, _ = self.encoder.compress(text)
            return compressed

    def estimate_tokens(self, text: str) -> int:
        """Estima número de tokens"""
        # Usa tiktoken se disponível
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except:
            # Fallback para estimativa simples
            return len(text) // 4

# Funções de conveniência
def compress_text(text: str, aggressive: bool = False) -> Tuple[str, float]:
    """Comprime texto usando o melhor método disponível"""
    if validation_available and aggressive:
        return to_digilang_improved(text, mode="aggressive")
    else:
        compressor = get_digilang_compressor()
        return compressor.compress(text)

def decompress_text(text: str) -> str:
    """Descomprime texto"""
    if validation_available:
        return from_digilang_improved(text)
    else:
        compressor = get_digilang_compressor()
        return compressor.decompress(text)

def serialize_for_api(data: Any) -> str:
    """Serializa dados para API com compressão"""
    if validation_available:
        return serialize_message(data)
    else:
        json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        compressed, _ = compress_text(json_str)
        return compressed

def deserialize_from_api(data: str) -> Any:
    """Deserializa dados da API"""
    if validation_available:
        return deserialize_message(data)
    else:
        decompressed = decompress_text(data)
        return json.loads(decompressed)