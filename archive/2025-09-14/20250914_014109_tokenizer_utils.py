import tiktoken, unicodedata, string
from typing import List, Tuple, Dict, Set
from collections import defaultdict

ENC_NAME = "cl100k_base"

def get_single_token_strings(max_candidates: int = 8000) -> List[str]:
    """
    Varre o mergeable_ranks do cl100k_base e retorna strings que:
      - tokenizam em len == 1
      - são imprimíveis, não-controle, sem whitespace
      - curtas em bytes (<= 4 preferencialmente)
      - priorizadas por raridade/adequação para símbolos
    Ordena por: raridade estimada, bytes_len asc, categoria unicode.
    """
    enc = tiktoken.get_encoding(ENC_NAME)
    
    # Categorize tokens by type for better selection
    categories = {
        'math_symbols': [],     # ∀∃∆∇⊕⊗∏∑∫ etc
        'arrows': [],           # →←↑↓⇒⇐⇑⇓ etc  
        'shapes': [],           # ◆◇●○■□▲△ etc
        'diacritics': [],       # àáâãäåæçèé etc
        'punctuation': [],      # ‖„""''–— etc
        'currency': [],         # €£¥₹₽ etc
        'other_rare': []        # Various rare but useful symbols
    }
    
    for token_bytes, token_id in enc._mergeable_ranks.items():
        try:
            text = token_bytes.decode("utf-8", errors='strict')
        except Exception:
            continue
            
        if not text or len(text) == 0:
            continue
            
        # Skip if contains whitespace or control chars
        if any(ch.isspace() or unicodedata.category(ch)[0] in ("C","Z") for ch in text):
            continue
            
        # Must be single token
        if len(enc.encode(text)) != 1:
            continue
            
        # Skip common ASCII letters/digits/underscore
        if all(ch in (string.ascii_letters + string.digits + "_-") for ch in text):
            continue
            
        # Limit byte size for efficiency
        if len(text.encode("utf-8")) > 4:
            continue
            
        # Categorize by unicode properties
        first_char = text[0]
        cat = unicodedata.category(first_char)
        
        if first_char in "→←↑↓⇒⇐⇑⇓⟶⟵⟷↔⇄↕⇕⤴⤵⤶⤷":
            categories['arrows'].append(text)
        elif first_char in "∀∃∆∇⊕⊗⊙⊚⊛⊜⊝∏∑∫∮∯∰∱∲∳":
            categories['math_symbols'].append(text)
        elif first_char in "◆◇●○◐◑◒◓■□▲△▼▽◢◣◤◥":
            categories['shapes'].append(text)
        elif cat.startswith('S'):  # Symbol categories
            categories['other_rare'].append(text)
        elif cat.startswith('P') and first_char not in ".,!?:;()[]{}":
            categories['punctuation'].append(text)
        elif first_char in "€£¥₹₽₨₩₪₫₴₵₦₡₢₣₤₥₦₧₨₩₪₫€₭₮₯":
            categories['currency'].append(text)
        else:
            categories['other_rare'].append(text)
    
    # Build final list with preference order
    result = []
    priorities = ['arrows', 'math_symbols', 'shapes', 'punctuation', 'currency', 'other_rare', 'diacritics']
    
    for category in priorities:
        # Sort by byte length first, then lexicographically
        category_tokens = sorted(categories[category], 
                               key=lambda x: (len(x.encode('utf-8')), x))
        result.extend(category_tokens)
        
        if len(result) >= max_candidates:
            break
    
    return result[:max_candidates]

def estimate_compression_potential(text: str, vocab_symbols: Dict[str, str]) -> float:
    """Quick heuristic estimate of compression potential for given text."""
    enc = tiktoken.get_encoding(ENC_NAME)
    original_tokens = len(enc.encode(text))
    
    # Count potential replacements
    saved_tokens = 0
    words = text.split()
    
    for symbol_key, symbol_val in vocab_symbols.items():
        if symbol_key.upper() in text.upper():
            # Rough estimate: each match saves ~2-4 tokens
            matches = text.upper().count(symbol_key.upper())
            saved_tokens += matches * 2
    
    return min(saved_tokens / original_tokens if original_tokens > 0 else 0, 0.8)