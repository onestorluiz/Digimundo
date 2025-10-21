"""
🔤 DIGILANG API FALLBACK MELHORADO - Funciona sem tiktoken
Implementação otimizada para compressão real mesmo sem tiktoken
"""
import json
import re
import zlib
import base64
from typing import Dict, List, Tuple, Any
SCREENPLAY_TOKEN_DICT = {'FADE IN:': '⟨FI⟩', 'FADE OUT:': '⟨FO⟩', 'FADE TO BLACK': '⟨FB⟩', 'CUT TO:': '⟨CT⟩', 'DISSOLVE TO:': '⟨DT⟩', 'SMASH CUT:': '⟨SC⟩', 'CONTINUOUS': '⟨CN⟩', "(CONT'D)": '⟨C⟩', 'CONTINUED:': '⟨CO⟩', 'MOMENTS LATER': '⟨ML⟩', 'LATER': '⟨L⟩', 'V.O.': '⟨V⟩', 'O.S.': '⟨O⟩', 'INT.': '⟨I⟩', 'EXT.': '⟨E⟩', 'INT./EXT.': '⟨IE⟩', 'MORNING': '⟨MO⟩', 'AFTERNOON': '⟨AF⟩', 'EVENING': '⟨EV⟩', 'NIGHT': '⟨N⟩', 'DAY': '⟨D⟩', 'DAWN': '⟨DW⟩', 'DUSK': '⟨DS⟩', 'enters': '⟨en⟩', 'exits': '⟨ex⟩', 'walks': '⟨wk⟩', 'runs': '⟨rn⟩', 'looks': '⟨lk⟩', 'turns': '⟨tn⟩', 'sits': '⟨st⟩', 'stands': '⟨sd⟩', 'takes': '⟨tk⟩', 'gives': '⟨gv⟩', 'opens': '⟨op⟩', 'closes': '⟨cl⟩', 'the': '⟨t⟩', 'and': '⟨&⟩', 'to': '⟨2⟩', 'of': '⟨o⟩', 'in': '⟨i⟩', 'is': '⟨s⟩', 'it': '⟨it⟩', 'that': '⟨T⟩', 'with': '⟨w⟩', 'for': '⟨4⟩', 'from': '⟨f⟩', 'about': '⟨a⟩', 'into': '⟨n2⟩', 'through': '⟨th⟩', 'back': '⟨bk⟩', 'over': '⟨ov⟩', 'under': '⟨un⟩', 'around': '⟨ar⟩', 'between': '⟨bt⟩', 'behind': '⟨bh⟩', 'before': '⟨bf⟩', 'after': '⟨af⟩'}
CANONICALIZATION_PATTERNS = [('\\s+', ' '), ('\\n\\s*\\n\\s*\\n+', '\n\n'), ('^\\s+|\\s+$', ''), ('\\.{3,}', '...'), ('-{2,}', '--'), ('!{2,}', '!'), ('\\?{2,}', '?'), ('\\(\\s+', '('), ('\\s+\\)', ')'), ('\\s+,', ','), ('\\s+\\.', '.'), ('\\s+;', ';'), ('\\s+:', ':')]

class ImprovedTokenPairDatabase:
    """Base de pares de tokens melhorada"""

    def __init__(self):
        self.pairs = {}
        self._build_common_pairs()

    def _build_common_pairs(self):
        """Constrói pares comuns de tokens"""
        common_pairs = {'INT. ': '⟨I⟩', 'EXT. ': '⟨E⟩', ' - ': '⟨-⟩', 'FADE IN': '⟨FI⟩', 'CUT TO': '⟨CT⟩', 'the ': '⟨t⟩', ' the': '⟨t⟩', 'and ': '⟨&⟩', ' and': '⟨&⟩', 'to ': '⟨2⟩', ' to': '⟨2⟩', 'of ': '⟨o⟩', ' of': '⟨o⟩', 'in ': '⟨i⟩', ' in': '⟨i⟩', ' of the ': '⟨ot⟩', ' in the ': '⟨it⟩', ' to the ': '⟨2t⟩', ' and the ': '⟨&t⟩', ' on the ': '⟨ont⟩', ' at the ': '⟨att⟩', ' from the ': '⟨ft⟩', ' with the ': '⟨wt⟩'}
        self.pairs.update(common_pairs)

    def compress(self, text: str) -> str:
        """Comprime usando pares de tokens"""
        result = text
        sorted_pairs = sorted(self.pairs.items(), key=lambda x: len(x[0]), reverse=True)
        for pair, token in sorted_pairs:
            if pair in result:
                result = result.replace(pair, token)
        return result

    def decompress(self, text: str) -> str:
        """Descomprime pares de tokens"""
        result = text
        reverse = {v: k for k, v in self.pairs.items()}
        for token, pair in reverse.items():
            if token in result:
                result = result.replace(token, pair)
        return result

def canon_strict_improved(text: str) -> str:
    """Canonicalização estrita melhorada"""
    result = text
    for pattern, replacement in CANONICALIZATION_PATTERNS:
        result = re.sub(pattern, replacement, result)
    lines = result.split('\n')
    cleaned_lines = []
    empty_count = 0
    for line in lines:
        if not line.strip():
            empty_count += 1
            if empty_count <= 2:
                cleaned_lines.append(line)
        else:
            empty_count = 0
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def to_digilang_improved(text: str, mode: str='auto') -> Tuple[str, float]:
    """Comprime texto para DigiLang com algoritmo melhorado
    
    Args:
        text: Texto para comprimir
        mode: Modo de compressão (auto, screenplay, aggressive)
        
    Returns:
        (texto_comprimido, taxa_de_compressão)
    """
    if not text:
        return ('', 1.0)
    original_len = len(text)
    if mode in ['screenplay', 'aggressive'] or (mode == 'auto' and _is_screenplay(text)):
        text = canon_strict_improved(text)
    tpd = ImprovedTokenPairDatabase()
    text = tpd.compress(text)
    for original, token in sorted(SCREENPLAY_TOKEN_DICT.items(), key=lambda x: len(x[0]), reverse=True):
        if original in text:
            text = text.replace(original, token)
    if len(text) > 1000 and mode == 'aggressive':
        try:
            compressed_bytes = zlib.compress(text.encode('utf-8'), level=9)
            compressed_b64 = base64.b64encode(compressed_bytes).decode('ascii')
            if len(compressed_b64) < len(text):
                text = f'⟨Z⟩{compressed_b64}'
        except:
            pass
    text = re.sub('\\s+', ' ', text).strip()
    compressed_len = len(text)
    ratio = compressed_len / original_len if original_len > 0 else 1.0
    return (text, ratio)

def from_digilang_improved(compressed: str) -> str:
    """Descomprime texto DigiLang melhorado
    
    Args:
        compressed: Texto comprimido
        
    Returns:
        Texto original
    """
    if not compressed:
        return ''
    text = compressed
    if text.startswith('⟨Z⟩'):
        try:
            compressed_b64 = text[3:]
            compressed_bytes = base64.b64decode(compressed_b64)
            text = zlib.decompress(compressed_bytes).decode('utf-8')
        except:
            pass
    reverse_dict = {v: k for k, v in SCREENPLAY_TOKEN_DICT.items()}
    for token, original in sorted(reverse_dict.items(), key=lambda x: len(x[0]), reverse=True):
        if token in text:
            text = text.replace(token, original)
    tpd = ImprovedTokenPairDatabase()
    text = tpd.decompress(text)
    return text

def _is_screenplay(text: str) -> bool:
    """Detecta se texto é roteiro"""
    screenplay_markers = ['INT.', 'EXT.', 'FADE IN:', 'FADE OUT:', 'CUT TO:', "(CONT'D)"]
    text_upper = text.upper()[:1000]
    markers_found = sum((1 for marker in screenplay_markers if marker in text_upper))
    return markers_found >= 2

def to_digilang(text: str, token_dict: Dict[str, str]=None) -> Tuple[str, float]:
    """Interface compatível com API original"""
    return to_digilang_improved(text)

def from_digilang(compressed: str, token_dict: Dict[str, str]=None) -> str:
    """Interface compatível com API original"""
    return from_digilang_improved(compressed)

def canon_strict(text: str) -> str:
    """Interface compatível com API original"""
    return canon_strict_improved(text)

class DigiLangEncoder:
    """Encoder melhorado para DigiLang"""

    def __init__(self, token_dict: Dict[str, str]=None):
        self.token_dict = token_dict or SCREENPLAY_TOKEN_DICT

    def encode(self, text: str) -> str:
        """Codifica texto"""
        compressed, _ = to_digilang_improved(text)
        return compressed

    def encode_for_window(self, text: str, max_tokens: int) -> str:
        """Codifica para caber em janela de tokens"""
        compressed = self.encode(text)
        max_chars = max_tokens * 3
        if len(compressed) > max_chars:
            compressed = compressed[:max_chars]
        return compressed

class DigiLangDecoder:
    """Decoder melhorado para DigiLang"""

    def __init__(self, token_dict: Dict[str, str]=None):
        self.token_dict = token_dict or SCREENPLAY_TOKEN_DICT

    def decode(self, compressed: str) -> str:
        """Decodifica texto"""
        return from_digilang_improved(compressed)

class TokenPairDatabase:
    """Classe compatível com API original"""

    def __init__(self):
        self.improved = ImprovedTokenPairDatabase()

    def compress_with_pairs(self, text: str) -> str:
        return self.improved.compress(text)

    def decompress_pairs(self, text: str) -> str:
        return self.improved.decompress(text)

def serialize_message(messages: Any) -> str:
    """Serializa mensagens para transmissão comprimida"""
    if isinstance(messages, str):
        return messages
    json_str = json.dumps(messages, ensure_ascii=False, separators=(',', ':'))
    compressed, _ = to_digilang_improved(json_str, mode='aggressive')
    return compressed

def deserialize_message(compressed: str) -> Any:
    """Desserializa mensagens comprimidas"""
    decompressed = from_digilang_improved(compressed)
    try:
        return json.loads(decompressed)
    except:
        return decompressed
if __name__ == '__main__':
    print('🔤 DigiLang API Fallback MELHORADO')
    print('-' * 40)
    test = 'FADE IN:\n\nINT. OFFICE - DAY\n\nJohn enters the room. He looks tired.\n\nJOHN\nI need coffee.\n\nHe walks to the coffee machine.'
    compressed, ratio = to_digilang_improved(test, mode='screenplay')
    print(f'Original: {len(test)} chars')
    print(f'Compressed: {len(compressed)} chars')
    print(f'Ratio: {ratio:.2f}')
    print(f'Compression: {(1 - ratio) * 100:.1f}%')
    decompressed = from_digilang_improved(compressed)
    print(f'Reversible: {decompressed == test}')
    print('\nCompressed text preview:')
    print(compressed[:100] + '...' if len(compressed) > 100 else compressed)