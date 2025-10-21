"""
🔤 DIGILANG API FALLBACK - Funciona sem tiktoken
Implementação simplificada para quando tiktoken não está disponível
"""
import json
import re
from typing import Dict, List, Tuple, Any
DEFAULT_TOKEN_DICT = {'INT.': '⟨I⟩', 'EXT.': '⟨E⟩', 'FADE IN:': '⟨FI⟩', 'FADE OUT:': '⟨FO⟩', 'CUT TO:': '⟨CT⟩', "(CONT'D)": '⟨C⟩', 'CONTINUOUS': '⟨CN⟩', 'LATER': '⟨L⟩', 'DAY': '⟨D⟩', 'NIGHT': '⟨N⟩', 'MORNING': '⟨M⟩', 'AFTERNOON': '⟨A⟩', 'the': '⟨t⟩', 'and': '⟨&⟩', 'to': '⟨2⟩', 'of': '⟨o⟩', 'in': '⟨i⟩', 'that': '⟨T⟩', 'with': '⟨w⟩', 'for': '⟨4⟩', 'from': '⟨f⟩', 'about': '⟨a⟩'}
SCREENPLAY_PATTERNS = [('\\s+', ' '), ('\\n\\s*\\n\\s*\\n+', '\n\n'), ('\\.{3,}', '...'), ('-{2,}', '--'), ('\\(\\s+', '('), ('\\s+\\)', ')')]

def canon_strict(text: str) -> str:
    """Canonicalização estrita de texto"""
    result = text
    for pattern, replacement in SCREENPLAY_PATTERNS:
        result = re.sub(pattern, replacement, result)
    lines = result.split('\n')
    lines = [line.strip() for line in lines]
    result = '\n'.join(lines)
    return result

def to_digilang(text: str, token_dict: Dict[str, str]=None) -> Tuple[str, float]:
    """Comprime texto para DigiLang
    
    Args:
        text: Texto para comprimir
        token_dict: Dicionário de tokens (usa default se None)
        
    Returns:
        (texto_comprimido, taxa_de_compressão)
    """
    if token_dict is None:
        token_dict = DEFAULT_TOKEN_DICT
    original_len = len(text)
    compressed = text
    for original, token in token_dict.items():
        compressed = compressed.replace(original, token)
    compressed = re.sub('\\s+', ' ', compressed)
    compressed = compressed.strip()
    compressed_len = len(compressed)
    ratio = compressed_len / original_len if original_len > 0 else 1.0
    return (compressed, ratio)

def from_digilang(compressed: str, token_dict: Dict[str, str]=None) -> str:
    """Descomprime texto DigiLang
    
    Args:
        compressed: Texto comprimido
        token_dict: Dicionário de tokens
        
    Returns:
        Texto original
    """
    if token_dict is None:
        token_dict = DEFAULT_TOKEN_DICT
    decompressed = compressed
    reverse_dict = {v: k for k, v in token_dict.items()}
    for token, original in reverse_dict.items():
        decompressed = decompressed.replace(token, original)
    return decompressed

def serialize_message(messages: Any) -> str:
    """Serializa mensagens para transmissão comprimida
    
    Args:
        messages: Mensagens para serializar
        
    Returns:
        String serializada e comprimida
    """
    if isinstance(messages, str):
        return messages
    json_str = json.dumps(messages, ensure_ascii=False, separators=(',', ':'))
    compressed, _ = to_digilang(json_str)
    return compressed

def deserialize_message(compressed: str) -> Any:
    """Desserializa mensagens comprimidas
    
    Args:
        compressed: String comprimida
        
    Returns:
        Objeto original
    """
    decompressed = from_digilang(compressed)
    try:
        return json.loads(decompressed)
    except:
        return decompressed

class DigiLangEncoder:
    """Encoder fallback para DigiLang"""

    def __init__(self, token_dict: Dict[str, str]=None):
        self.token_dict = token_dict or DEFAULT_TOKEN_DICT

    def encode(self, text: str) -> str:
        """Codifica texto"""
        compressed, _ = to_digilang(text, self.token_dict)
        return compressed

    def encode_for_window(self, text: str, max_tokens: int) -> str:
        """Codifica para caber em janela de tokens"""
        compressed = self.encode(text)
        max_chars = max_tokens * 4
        if len(compressed) > max_chars:
            compressed = compressed[:max_chars]
        return compressed

class DigiLangDecoder:
    """Decoder fallback para DigiLang"""

    def __init__(self, token_dict: Dict[str, str]=None):
        self.token_dict = token_dict or DEFAULT_TOKEN_DICT

    def decode(self, compressed: str) -> str:
        """Decodifica texto"""
        return from_digilang(compressed, self.token_dict)

class TokenPairDatabase:
    """Token Pair Database simplificado"""

    def __init__(self):
        self.pairs = {}

    def add_pair(self, token1: str, token2: str, replacement: str):
        """Adiciona par de tokens"""
        self.pairs[f'{token1}{token2}'] = replacement

    def compress_with_pairs(self, text: str) -> str:
        """Comprime usando pares"""
        result = text
        for pair, replacement in self.pairs.items():
            result = result.replace(pair, replacement)
        return result
if __name__ == '__main__':
    print('🔤 DigiLang API Fallback')
    print('-' * 40)
    test = 'INT. OFFICE - DAY\n\nJohn enters the room.'
    compressed, ratio = to_digilang(test)
    print(f'Original: {len(test)} chars')
    print(f'Compressed: {len(compressed)} chars')
    print(f'Ratio: {ratio:.2f}')
    decompressed = from_digilang(compressed)
    print(f'Reversible: {decompressed == test}')