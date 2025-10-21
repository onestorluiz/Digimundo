#!/usr/bin/env python3
"""
🔄 DIGILANG ENGLISH MAPPING - Mapeia vocabulário inglês para símbolos únicos
Método super eficiente: 1 palavra inglesa = 1 símbolo único
"""

import json
from pathlib import Path
from datetime import datetime

class DigiLangEnglishMapper:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║     🔄 DIGILANG ENGLISH→SYMBOL MAPPER (1:1 MAPPING)          ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        
    def get_all_unicode_symbols(self):
        """Get ALL available Unicode symbols (tens of thousands)"""
        symbols = []
        
        # MASSIVE Unicode collection
        unicode_ranges = [
            # Mathematical Alphanumeric Symbols (996 chars)
            (0x1D400, 0x1D7FF),
            
            # CJK Unified Ideographs (20,976 chars) - Chinese/Japanese/Korean
            (0x4E00, 0x9FFF),
            
            # Hangul Syllables (11,172 chars) - Korean
            (0xAC00, 0xD7AF),
            
            # Arabic (255 chars)
            (0x0600, 0x06FF),
            
            # Hebrew (112 chars)
            (0x0590, 0x05FF),
            
            # Thai (128 chars)
            (0x0E00, 0x0E7F),
            
            # Georgian (96 chars)
            (0x10A0, 0x10FF),
            
            # Cherokee (96 chars)
            (0x13A0, 0x13FF),
            
            # Unified Canadian Aboriginal Syllabics (640 chars)
            (0x1400, 0x167F),
            
            # Mathematical Operators (256 chars)
            (0x2200, 0x22FF),
            
            # Miscellaneous Technical (256 chars)
            (0x2300, 0x23FF),
            
            # Geometric Shapes (96 chars)
            (0x25A0, 0x25FF),
            
            # Miscellaneous Symbols (256 chars)
            (0x2600, 0x26FF),
            
            # Dingbats (192 chars)
            (0x2700, 0x27BF),
            
            # Braille Patterns (256 chars)
            (0x2800, 0x28FF),
            
            # Box Drawing (128 chars)
            (0x2500, 0x257F),
            
            # Block Elements (32 chars)
            (0x2580, 0x259F),
            
            # Arrows (112 chars)
            (0x2190, 0x21FF),
            
            # Greek and Coptic (135 chars)
            (0x0370, 0x03FF),
            
            # Cyrillic (256 chars)
            (0x0400, 0x04FF),
        ]
        
        for start, end in unicode_ranges:
            for codepoint in range(start, end + 1):
                try:
                    char = chr(codepoint)
                    # Skip control characters and whitespace
                    if not char.isspace() and char.isprintable():
                        symbols.append(char)
                except:
                    pass
                    
        print(f"📊 Total de símbolos Unicode disponíveis: {len(symbols):,}")
        return symbols
        
    def get_english_vocabulary(self):
        """Get most common English words"""
        # Most common 3000 English words
        common_words = [
            # Top 100 most common
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
            
            # Programming & Tech vocabulary (essential for DigiLang)
            'function', 'variable', 'class', 'method', 'object', 'array', 'list', 'string',
            'integer', 'float', 'boolean', 'null', 'undefined', 'true', 'false', 'if', 'else',
            'for', 'while', 'return', 'break', 'continue', 'switch', 'case', 'default',
            'try', 'catch', 'finally', 'throw', 'async', 'await', 'promise', 'callback',
            'import', 'export', 'module', 'package', 'library', 'framework', 'api', 'http',
            'https', 'get', 'post', 'put', 'delete', 'patch', 'request', 'response',
            'header', 'body', 'status', 'error', 'success', 'warning', 'info', 'debug',
            'server', 'client', 'database', 'table', 'column', 'row', 'index', 'query',
            'select', 'insert', 'update', 'create', 'drop', 'alter', 'join', 'where',
            'group', 'order', 'limit', 'offset', 'transaction', 'commit', 'rollback',
            'connection', 'session', 'cookie', 'token', 'authentication', 'authorization',
            'user', 'password', 'email', 'username', 'role', 'permission', 'admin',
            'encrypt', 'decrypt', 'hash', 'salt', 'key', 'certificate', 'ssl', 'tls',
            
            # Common verbs
            'run', 'start', 'stop', 'pause', 'resume', 'reset', 'init', 'load', 'save',
            'open', 'close', 'read', 'write', 'send', 'receive', 'connect', 'disconnect',
            'bind', 'listen', 'accept', 'reject', 'allow', 'deny', 'grant', 'revoke',
            'add', 'remove', 'append', 'prepend', 'push', 'pop', 'shift', 'unshift',
            'map', 'filter', 'reduce', 'sort', 'reverse', 'shuffle', 'merge', 'split',
            'join', 'concat', 'slice', 'splice', 'replace', 'trim', 'pad', 'format',
            'parse', 'stringify', 'encode', 'decode', 'compress', 'decompress',
            'validate', 'sanitize', 'escape', 'normalize', 'transform', 'convert',
            
            # Common adjectives
            'big', 'small', 'large', 'tiny', 'huge', 'fast', 'slow', 'quick', 'rapid',
            'high', 'low', 'top', 'bottom', 'left', 'right', 'center', 'middle',
            'first', 'last', 'next', 'previous', 'current', 'active', 'inactive',
            'enabled', 'disabled', 'visible', 'hidden', 'public', 'private', 'protected',
            'static', 'dynamic', 'abstract', 'concrete', 'virtual', 'real', 'fake',
            'valid', 'invalid', 'correct', 'incorrect', 'right', 'wrong', 'good', 'bad',
            'new', 'old', 'modern', 'legacy', 'deprecated', 'stable', 'unstable', 'beta',
            
            # Numbers and quantities
            'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
            'ten', 'hundred', 'thousand', 'million', 'billion', 'first', 'second', 'third',
            'half', 'quarter', 'double', 'triple', 'single', 'multiple', 'many', 'few',
            'all', 'none', 'some', 'any', 'each', 'every', 'both', 'either', 'neither',
            
            # Time-related
            'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'decade',
            'century', 'now', 'then', 'before', 'after', 'during', 'while', 'until',
            'since', 'always', 'never', 'sometimes', 'often', 'rarely', 'usually',
            'yesterday', 'today', 'tomorrow', 'morning', 'afternoon', 'evening', 'night',
            
            # Space and position
            'here', 'there', 'where', 'everywhere', 'nowhere', 'somewhere', 'anywhere',
            'above', 'below', 'beside', 'between', 'behind', 'front', 'back', 'inside',
            'outside', 'near', 'far', 'close', 'distant', 'adjacent', 'opposite',
            'horizontal', 'vertical', 'diagonal', 'parallel', 'perpendicular',
            
            # Data structures specific
            'stack', 'queue', 'heap', 'tree', 'graph', 'node', 'edge', 'vertex', 'leaf',
            'root', 'parent', 'child', 'sibling', 'ancestor', 'descendant', 'depth',
            'height', 'level', 'degree', 'path', 'cycle', 'loop', 'recursion',
            'iteration', 'traversal', 'search', 'sort', 'hash', 'bucket', 'collision',
            
            # Networking
            'tcp', 'udp', 'ip', 'dns', 'dhcp', 'mac', 'arp', 'icmp', 'ping', 'traceroute',
            'port', 'socket', 'packet', 'frame', 'segment', 'datagram', 'protocol',
            'handshake', 'timeout', 'retry', 'acknowledgment', 'sequence', 'window',
            'bandwidth', 'latency', 'throughput', 'congestion', 'routing', 'switching',
            
            # Security
            'vulnerability', 'exploit', 'patch', 'firewall', 'antivirus', 'malware',
            'virus', 'trojan', 'worm', 'ransomware', 'phishing', 'spoofing', 'injection',
            'xss', 'csrf', 'ddos', 'mitm', 'backdoor', 'rootkit', 'keylogger',
            'encryption', 'decryption', 'cipher', 'plaintext', 'ciphertext', 'signature',
            
            # Cloud & DevOps
            'container', 'docker', 'kubernetes', 'pod', 'service', 'deployment', 'replica',
            'scale', 'load', 'balance', 'cluster', 'node', 'master', 'worker', 'agent',
            'pipeline', 'build', 'test', 'deploy', 'release', 'rollback', 'monitor',
            'log', 'metric', 'trace', 'alert', 'incident', 'runbook', 'automation',
            
            # AI/ML
            'neural', 'network', 'layer', 'neuron', 'weight', 'bias', 'activation',
            'gradient', 'backpropagation', 'optimizer', 'learning', 'training', 'validation',
            'testing', 'epoch', 'batch', 'iteration', 'loss', 'accuracy', 'precision',
            'recall', 'f1score', 'confusion', 'matrix', 'overfitting', 'underfitting',
            'regularization', 'dropout', 'normalization', 'standardization',
            
            # Business/Common
            'company', 'business', 'customer', 'product', 'service', 'price', 'cost',
            'revenue', 'profit', 'loss', 'market', 'share', 'growth', 'strategy',
            'plan', 'goal', 'objective', 'target', 'milestone', 'deadline', 'budget',
            'resource', 'team', 'project', 'task', 'issue', 'bug', 'feature', 'requirement'
        ]
        
        # Extend with more words to reach 3000
        extended_words = []
        
        # Add variations
        for word in common_words[:500]:  # Take first 500 and create variations
            extended_words.append(word)
            extended_words.append(f"{word}s")  # plural
            extended_words.append(f"{word}ed")  # past tense
            extended_words.append(f"{word}ing")  # gerund
            extended_words.append(f"{word}er")  # comparative
            extended_words.append(f"un{word}")  # negation
            
        # Combine and deduplicate
        all_words = list(set(common_words + extended_words))[:3000]
        
        print(f"📚 Vocabulário inglês carregado: {len(all_words)} palavras")
        return all_words
        
    def create_mapping(self):
        """Create 1:1 mapping between English words and Unicode symbols"""
        
        # Get symbols and words
        symbols = self.get_all_unicode_symbols()
        words = self.get_english_vocabulary()
        
        # Create the mapping
        mapping = {
            "metadata": {
                "name": "DigiLang",
                "version": "4.0",
                "method": "English→Symbol Direct Mapping",
                "created": datetime.now().isoformat(),
                "total_words": min(len(words), len(symbols))
            },
            "english_to_symbol": {},
            "symbol_to_english": {},
            "categories": {
                "core": {},
                "tech": {},
                "common": {}
            }
        }
        
        print("\n🔄 MAPEANDO PALAVRAS PARA SÍMBOLOS...")
        print()
        
        # Map each word to a unique symbol
        for i, word in enumerate(words):
            if i >= len(symbols):
                break
                
            symbol = symbols[i]
            
            # Add to mappings
            mapping["english_to_symbol"][word] = symbol
            mapping["symbol_to_english"][symbol] = word
            
            # Categorize
            if any(tech in word for tech in ['function', 'class', 'array', 'server', 'data']):
                mapping["categories"]["tech"][word] = symbol
            elif i < 100:  # First 100 are most common
                mapping["categories"]["core"][word] = symbol
            else:
                mapping["categories"]["common"][word] = symbol
                
            if (i + 1) % 500 == 0:
                print(f"   ✓ {i + 1} palavras mapeadas...")
                
        # Update metadata
        mapping["metadata"]["total_words"] = len(mapping["english_to_symbol"])
        
        # Calculate compression
        avg_word_length = sum(len(w) for w in mapping["english_to_symbol"].keys()) / len(mapping["english_to_symbol"])
        compression = (1 - 1/avg_word_length) * 100  # Each symbol is 1 char
        mapping["metadata"]["compression_rate"] = round(compression, 1)
        
        # Save the mapping
        output_path = self.base_path / "DIGILANG_ENGLISH_MAPPED.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
            
        print()
        print("═══════════════════════════════════════════════════════════════")
        print("✅ DIGILANG MAPEADO COM SUCESSO!")
        print()
        print(f"   Total de palavras: {len(mapping['english_to_symbol']):,}")
        print(f"   Taxa de compressão: {compression:.1f}%")
        print(f"   Categorias: {len(mapping['categories'])}")
        print()
        print("📖 EXEMPLOS DE MAPEAMENTO:")
        print()
        
        # Show examples
        examples = list(mapping["english_to_symbol"].items())[:20]
        for eng, sym in examples:
            print(f"   {eng:15} → {sym}")
            
        print()
        print(f"💾 Arquivo salvo: {output_path}")
        print()
        print("🚀 VANTAGENS DESTE MÉTODO:")
        print("   • INSTANTÂNEO - Sem espera de IA")
        print("   • GARANTIDO único - Cada palavra tem símbolo exclusivo")
        print("   • REVERSÍVEL - Pode traduzir de volta perfeitamente")
        print("   • EXTENSÍVEL - Fácil adicionar mais palavras")
        
        return output_path

if __name__ == "__main__":
    mapper = DigiLangEnglishMapper()
    mapper.create_mapping()