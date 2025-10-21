#!/usr/bin/env python3
"""
⚡ DIGILANG FAST 3000 - Criação rápida de 3000 palavras únicas
"""

import json
from pathlib import Path
from datetime import datetime

def create_digilang_3000():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║            ⚡ DIGILANG FAST 3000 GENERATOR                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # All available Unicode characters (no duplicates guaranteed)
    unicode_blocks = [
        # Mathematical operators (256 chars)
        [chr(i) for i in range(0x2200, 0x2300)],
        # Arrows (112 chars)  
        [chr(i) for i in range(0x2190, 0x21FF)],
        # Box drawing (128 chars)
        [chr(i) for i in range(0x2500, 0x257F)],
        # Geometric shapes (96 chars)
        [chr(i) for i in range(0x25A0, 0x25FF)],
        # Miscellaneous symbols (256 chars)
        [chr(i) for i in range(0x2600, 0x26FF)],
        # Dingbats (192 chars)
        [chr(i) for i in range(0x2700, 0x27BF)],
        # Braille (256 chars)
        [chr(i) for i in range(0x2800, 0x28FF)],
        # CJK Symbols (64 chars)
        [chr(i) for i in range(0x3000, 0x303F)],
        # Hiragana (96 chars)
        [chr(i) for i in range(0x3040, 0x309F)],
        # Katakana (96 chars)
        [chr(i) for i in range(0x30A0, 0x30FF)],
        # Greek (48 chars)
        [chr(i) for i in range(0x0391, 0x03C9)],
        # Cyrillic (64 chars)
        [chr(i) for i in range(0x0410, 0x044F)],
    ]
    
    # Flatten all characters
    all_chars = []
    for block in unicode_blocks:
        all_chars.extend(block)
    
    print(f"📊 Total de caracteres únicos disponíveis: {len(all_chars):,}")
    
    # Core concepts categories
    concept_categories = {
        'programming': [
            'function', 'class', 'method', 'variable', 'constant', 'parameter',
            'argument', 'return', 'loop', 'while', 'for', 'if', 'else', 'elif',
            'switch', 'case', 'break', 'continue', 'try', 'catch', 'finally',
            'throw', 'async', 'await', 'promise', 'callback', 'module', 'import',
            'export', 'package', 'library', 'framework', 'compile', 'runtime',
            'debug', 'test', 'deploy', 'build', 'lint', 'format', 'refactor'
        ],
        'data_structures': [
            'array', 'list', 'vector', 'matrix', 'tensor', 'stack', 'queue',
            'deque', 'heap', 'tree', 'binary_tree', 'btree', 'graph', 'node',
            'edge', 'vertex', 'hash', 'hashmap', 'dictionary', 'set', 'multiset',
            'table', 'index', 'key', 'value', 'pair', 'tuple', 'string', 'buffer'
        ],
        'networking': [
            'tcp', 'udp', 'http', 'https', 'ftp', 'ssh', 'telnet', 'smtp', 'pop3',
            'imap', 'dns', 'dhcp', 'ip', 'ipv4', 'ipv6', 'mac', 'arp', 'icmp',
            'port', 'socket', 'connection', 'session', 'packet', 'frame', 'segment',
            'datagram', 'router', 'switch', 'hub', 'gateway', 'firewall', 'proxy',
            'vpn', 'ssl', 'tls', 'certificate', 'handshake', 'request', 'response'
        ],
        'database': [
            'select', 'insert', 'update', 'delete', 'create', 'drop', 'alter',
            'table', 'column', 'row', 'primary_key', 'foreign_key', 'index',
            'constraint', 'join', 'inner_join', 'left_join', 'right_join',
            'union', 'group_by', 'order_by', 'having', 'where', 'like', 'between',
            'transaction', 'commit', 'rollback', 'lock', 'deadlock', 'isolation'
        ],
        'security': [
            'encrypt', 'decrypt', 'hash', 'salt', 'pepper', 'signature', 'verify',
            'authenticate', 'authorize', 'permission', 'role', 'user', 'admin',
            'token', 'jwt', 'oauth', 'saml', 'ldap', 'password', 'passphrase',
            'key', 'public_key', 'private_key', 'certificate', 'ca', 'ssl', 'tls',
            'firewall', 'ids', 'ips', 'waf', 'vulnerability', 'exploit', 'patch'
        ],
        'ai_ml': [
            'neuron', 'layer', 'weight', 'bias', 'activation', 'sigmoid', 'relu',
            'tanh', 'softmax', 'gradient', 'backpropagation', 'optimizer', 'sgd',
            'adam', 'rmsprop', 'learning_rate', 'epoch', 'batch', 'iteration',
            'loss', 'accuracy', 'precision', 'recall', 'f1_score', 'confusion_matrix',
            'overfitting', 'underfitting', 'regularization', 'dropout', 'batch_norm'
        ],
        'cloud': [
            'vm', 'container', 'docker', 'kubernetes', 'pod', 'service', 'deployment',
            'replica', 'scale', 'load_balancer', 'auto_scaling', 'vpc', 'subnet',
            'availability_zone', 'region', 's3', 'ec2', 'lambda', 'api_gateway',
            'cloudfront', 'rds', 'dynamodb', 'sqs', 'sns', 'iam', 'role', 'policy'
        ],
        'operations': [
            'add', 'subtract', 'multiply', 'divide', 'modulo', 'power', 'sqrt',
            'abs', 'min', 'max', 'sum', 'average', 'median', 'mode', 'concat',
            'split', 'join', 'merge', 'filter', 'map', 'reduce', 'sort', 'reverse',
            'shuffle', 'sample', 'slice', 'splice', 'push', 'pop', 'shift', 'unshift'
        ],
        'logic': [
            'and', 'or', 'not', 'xor', 'nand', 'nor', 'xnor', 'implies',
            'true', 'false', 'null', 'undefined', 'none', 'empty', 'exists',
            'equal', 'not_equal', 'greater', 'less', 'greater_equal', 'less_equal',
            'between', 'in', 'contains', 'starts_with', 'ends_with', 'matches'
        ],
        'time': [
            'second', 'millisecond', 'microsecond', 'nanosecond', 'minute', 'hour',
            'day', 'week', 'month', 'year', 'decade', 'century', 'now', 'today',
            'yesterday', 'tomorrow', 'before', 'after', 'during', 'since', 'until',
            'always', 'never', 'sometimes', 'often', 'rarely', 'duration', 'interval'
        ]
    }
    
    # Create the dictionary
    dictionary = {
        "metadata": {
            "name": "DigiLang",
            "version": "3.0",
            "created": datetime.now().isoformat(),
            "total_symbols": 0,
            "compression_rate": 0
        },
        "symbols": {},
        "categories": {},
        "reverse_index": {}
    }
    
    char_index = 0
    total_concepts = 0
    
    print("\n📝 GERANDO 3000 CONCEITOS ÚNICOS...\n")
    
    # First, add all predefined concepts
    for category, concepts in concept_categories.items():
        dictionary["categories"][category] = {}
        
        for concept in concepts:
            if char_index < len(all_chars):
                symbol = all_chars[char_index]
                dictionary["symbols"][concept] = symbol
                dictionary["categories"][category][concept] = symbol
                dictionary["reverse_index"][symbol] = concept
                char_index += 1
                total_concepts += 1
                
    print(f"✅ Conceitos base criados: {total_concepts}")
    
    # Generate additional concepts to reach 3000
    additional_templates = [
        # Technical compounds
        'process_{}', 'service_{}', 'handler_{}', 'manager_{}', 'controller_{}',
        'factory_{}', 'builder_{}', 'adapter_{}', 'wrapper_{}', 'proxy_{}',
        'observer_{}', 'listener_{}', 'emitter_{}', 'dispatcher_{}', 'router_{}',
        
        # Data operations
        'fetch_{}', 'load_{}', 'save_{}', 'store_{}', 'cache_{}',
        'validate_{}', 'sanitize_{}', 'parse_{}', 'serialize_{}', 'encode_{}',
        
        # States and conditions
        'is_{}', 'has_{}', 'can_{}', 'should_{}', 'must_{}',
        'enabled_{}', 'disabled_{}', 'active_{}', 'inactive_{}', 'pending_{}',
        
        # Modifiers
        'fast_{}', 'slow_{}', 'high_{}', 'low_{}', 'new_{}', 'old_{}',
        'first_{}', 'last_{}', 'next_{}', 'previous_{}', 'current_{}',
        
        # Actions
        'start_{}', 'stop_{}', 'pause_{}', 'resume_{}', 'reset_{}',
        'init_{}', 'cleanup_{}', 'destroy_{}', 'allocate_{}', 'free_{}'
    ]
    
    # Generate variations
    variations = [str(i) for i in range(100)] + [
        'alpha', 'beta', 'gamma', 'delta', 'epsilon',
        'primary', 'secondary', 'tertiary', 'auxiliary',
        'main', 'backup', 'temp', 'cache', 'buffer',
        'input', 'output', 'error', 'warning', 'info'
    ]
    
    print("\n📈 Gerando conceitos adicionais...")
    
    for template in additional_templates:
        if total_concepts >= 3000:
            break
            
        for variation in variations:
            if total_concepts >= 3000 or char_index >= len(all_chars):
                break
                
            concept = template.format(variation)
            
            # Skip if already exists
            if concept not in dictionary["symbols"]:
                symbol = all_chars[char_index]
                dictionary["symbols"][concept] = symbol
                dictionary["reverse_index"][symbol] = concept
                
                # Add to general category
                if "general" not in dictionary["categories"]:
                    dictionary["categories"]["general"] = {}
                dictionary["categories"]["general"][concept] = symbol
                
                char_index += 1
                total_concepts += 1
                
                if total_concepts % 500 == 0:
                    print(f"   {total_concepts} conceitos criados...")
    
    # Update metadata
    dictionary["metadata"]["total_symbols"] = total_concepts
    
    # Calculate compression rate
    total_concept_chars = sum(len(c) for c in dictionary["symbols"].keys())
    total_symbol_chars = len(dictionary["symbols"])  # Each symbol is 1 char
    compression_rate = (1 - total_symbol_chars / total_concept_chars) * 100
    dictionary["metadata"]["compression_rate"] = round(compression_rate, 2)
    
    # Save the dictionary
    output_path = Path.home() / "Digimundo" / "DIGILANG_3000.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ DIGILANG 3000 CRIADO COM SUCESSO!")
    print(f"   Total de palavras: {total_concepts:,}")
    print(f"   Taxa de compressão: {compression_rate:.1f}%")
    print(f"   Categorias: {len(dictionary['categories'])}")
    print(f"   Arquivo: {output_path}")
    
    # Print sample
    print("\n📖 AMOSTRA DE SÍMBOLOS:")
    samples = list(dictionary["symbols"].items())[:20]
    for concept, symbol in samples:
        print(f"   {concept:20} = {symbol}")
    
    return output_path

if __name__ == "__main__":
    create_digilang_3000()