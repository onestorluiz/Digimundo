#!/usr/bin/env python3
"""
🔒 DIGILANG ZERO DUPLICATE SYSTEM - Produção sem repetições
Sistema que verifica ANTES de criar e corrige duplicatas existentes
"""

import json
import random
import string
from pathlib import Path
from datetime import datetime
import hashlib

class DigiLangZeroDuplicateSystem:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.dictionary_file = self.base_path / "DIGILANG_MASTER_DICTIONARY.json"
        
        # Load or create master dictionary
        self.master_dict = self.load_master_dictionary()
        
        # Track all used symbols AND concepts
        self.used_symbols = set(self.master_dict['symbols'].values())
        self.used_concepts = set(self.master_dict['symbols'].keys())
        
        # Available Unicode ranges (total ~50,000 characters available)
        self.available_chars = self.load_available_characters()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║       🔒 DIGILANG ZERO DUPLICATE PRODUCTION SYSTEM           ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print(f"📊 Estado atual:")
        print(f"   Palavras existentes: {len(self.used_concepts)}")
        print(f"   Símbolos usados: {len(self.used_symbols)}")
        print(f"   Caracteres disponíveis: {len(self.available_chars):,}")
        print()
        
    def load_master_dictionary(self):
        """Load or create the master dictionary"""
        if self.dictionary_file.exists():
            with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create new dictionary structure
            return {
                "metadata": {
                    "version": "2.0",
                    "created": datetime.now().isoformat(),
                    "total_words": 0,
                    "last_check": datetime.now().isoformat()
                },
                "symbols": {},  # concept -> symbol mapping
                "reverse": {},  # symbol -> concept mapping
                "categories": {},
                "history": []  # Track all changes
            }
            
    def load_available_characters(self):
        """Load all available Unicode characters for symbols"""
        chars = []
        
        # Basic Latin symbols
        chars.extend(['!', '#', '$', '%', '&', '*', '+', '/', '=', '?', '@', '^', '~'])
        
        # Greek letters (24 + 24)
        chars.extend([chr(i) for i in range(0x0391, 0x03A9+1)])  # Α-Ω
        chars.extend([chr(i) for i in range(0x03B1, 0x03C9+1)])  # α-ω
        
        # Mathematical symbols
        chars.extend([chr(i) for i in range(0x2200, 0x22FF+1)])  # ∀-⋿
        
        # Arrows
        chars.extend([chr(i) for i in range(0x2190, 0x21FF+1)])  # ←-⇿
        
        # Box drawing
        chars.extend([chr(i) for i in range(0x2500, 0x257F+1)])  # ─-╿
        
        # Geometric shapes
        chars.extend([chr(i) for i in range(0x25A0, 0x25FF+1)])  # ■-◿
        
        # Miscellaneous symbols
        chars.extend([chr(i) for i in range(0x2600, 0x26FF+1)])  # ☀-⛿
        
        # Dingbats
        chars.extend([chr(i) for i in range(0x2700, 0x27BF+1)])  # ✀-➿
        
        # Braille
        chars.extend([chr(i) for i in range(0x2800, 0x28FF+1)])  # ⠀-⣿
        
        # CJK Symbols
        chars.extend([chr(i) for i in range(0x3000, 0x303F+1)])  # 　-〿
        
        # Hiragana (for unique symbols)
        chars.extend([chr(i) for i in range(0x3040, 0x309F+1)])  # ぀-ゟ
        
        # Katakana
        chars.extend([chr(i) for i in range(0x30A0, 0x30FF+1)])  # ゠-ヿ
        
        # Enclosed alphanumerics
        chars.extend([chr(i) for i in range(0x2460, 0x24FF+1)])  # ①-⓿
        
        # Remove already used symbols
        available = [c for c in chars if c not in self.used_symbols]
        
        return available
        
    def check_duplicate_before_create(self, concept, proposed_symbol):
        """Check if concept or symbol already exists BEFORE creating"""
        concept_lower = concept.lower().strip()
        
        # Check concept
        if concept_lower in self.used_concepts:
            existing_symbol = self.master_dict['symbols'][concept_lower]
            print(f"   ⚠️ Conceito '{concept}' já existe com símbolo '{existing_symbol}'")
            return False, "duplicate_concept"
            
        # Check symbol
        if proposed_symbol in self.used_symbols:
            existing_concept = self.master_dict['reverse'].get(proposed_symbol, 'unknown')
            print(f"   ⚠️ Símbolo '{proposed_symbol}' já usado para '{existing_concept}'")
            return False, "duplicate_symbol"
            
        return True, "ok"
        
    def get_unique_symbol(self):
        """Get a guaranteed unique symbol"""
        if not self.available_chars:
            # If we run out of single chars, start combining
            return self.generate_compound_symbol()
            
        # Pick random available character
        symbol = random.choice(self.available_chars)
        self.available_chars.remove(symbol)
        
        return symbol
        
    def generate_compound_symbol(self):
        """Generate compound symbols when single chars are exhausted"""
        # Use 2-character combinations
        base_chars = "αβγδεζηθικλμνξοπρστυφχψω"
        
        for c1 in base_chars:
            for c2 in base_chars:
                compound = c1 + c2
                if compound not in self.used_symbols:
                    return compound
                    
        # Fallback to hash-based generation
        timestamp = str(datetime.now().timestamp())
        hash_val = hashlib.md5(timestamp.encode()).hexdigest()[:4]
        return f"§{hash_val}"
        
    def fix_existing_duplicates(self):
        """Scan and fix any existing duplicates"""
        print("🔍 ESCANEANDO DUPLICATAS EXISTENTES...")
        
        # Check for duplicate symbols
        symbol_count = {}
        duplicates_found = []
        
        for concept, symbol in self.master_dict['symbols'].items():
            if symbol in symbol_count:
                duplicates_found.append({
                    'symbol': symbol,
                    'concept1': symbol_count[symbol],
                    'concept2': concept
                })
            else:
                symbol_count[symbol] = concept
                
        if duplicates_found:
            print(f"   ❌ Encontradas {len(duplicates_found)} duplicatas!")
            
            for dup in duplicates_found:
                # Keep first occurrence, change second
                new_symbol = self.get_unique_symbol()
                old_concept = dup['concept2']
                
                print(f"   🔄 '{old_concept}': '{dup['symbol']}' → '{new_symbol}'")
                
                # Update dictionary
                self.master_dict['symbols'][old_concept] = new_symbol
                del self.master_dict['reverse'][dup['symbol']]
                self.master_dict['reverse'][new_symbol] = old_concept
                
                # Track change
                self.master_dict['history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'fix_duplicate',
                    'concept': old_concept,
                    'old_symbol': dup['symbol'],
                    'new_symbol': new_symbol
                })
                
            self.save_dictionary()
            print(f"   ✅ Corrigidas {len(duplicates_found)} duplicatas")
        else:
            print("   ✅ Nenhuma duplicata encontrada")
            
    def add_new_symbol(self, concept, category=None):
        """Add new symbol with duplicate checking"""
        concept_lower = concept.lower().strip()
        
        # Check if concept exists
        if concept_lower in self.used_concepts:
            return None, f"Concept '{concept}' already exists"
            
        # Get unique symbol
        symbol = self.get_unique_symbol()
        
        # Double-check uniqueness
        is_valid, reason = self.check_duplicate_before_create(concept_lower, symbol)
        
        if not is_valid:
            # Try again with different symbol
            symbol = self.get_unique_symbol()
            
        # Add to dictionary
        self.master_dict['symbols'][concept_lower] = symbol
        self.master_dict['reverse'][symbol] = concept_lower
        
        if category:
            if category not in self.master_dict['categories']:
                self.master_dict['categories'][category] = []
            self.master_dict['categories'][category].append(concept_lower)
            
        # Update tracking
        self.used_concepts.add(concept_lower)
        self.used_symbols.add(symbol)
        
        # Add to history
        self.master_dict['history'].append({
            'timestamp': datetime.now().isoformat(),
            'action': 'add',
            'concept': concept_lower,
            'symbol': symbol,
            'category': category
        })
        
        return symbol, "success"
        
    def batch_create_concepts(self, concepts_list):
        """Create multiple concepts with verification"""
        print(f"\n📝 CRIANDO {len(concepts_list)} CONCEITOS...")
        
        created = 0
        skipped = 0
        
        for item in concepts_list:
            if isinstance(item, dict):
                concept = item.get('concept', '')
                category = item.get('category', 'general')
            else:
                concept = item
                category = 'general'
                
            symbol, status = self.add_new_symbol(concept, category)
            
            if symbol:
                created += 1
                print(f"   ✅ {concept} = {symbol}")
            else:
                skipped += 1
                
        print(f"\n   Criados: {created} | Ignorados: {skipped}")
        
        # Save after batch
        self.save_dictionary()
        
        return created
        
    def save_dictionary(self):
        """Save the master dictionary"""
        self.master_dict['metadata']['total_words'] = len(self.master_dict['symbols'])
        self.master_dict['metadata']['last_update'] = datetime.now().isoformat()
        
        with open(self.dictionary_file, 'w', encoding='utf-8') as f:
            json.dump(self.master_dict, f, indent=2, ensure_ascii=False)
            
        print(f"   💾 Dicionário salvo: {len(self.master_dict['symbols'])} palavras")
        
    def generate_smart_concepts(self, category, count=100):
        """Generate smart non-duplicate concepts for a category"""
        
        templates = {
            'programming': [
                'function_{}', 'method_{}', 'class_{}', 'variable_{}',
                'loop_{}', 'condition_{}', 'module_{}', 'package_{}',
                'thread_{}', 'process_{}', 'callback_{}', 'promise_{}',
                'async_{}', 'sync_{}', 'compile_{}', 'runtime_{}'
            ],
            'networking': [
                'protocol_{}', 'port_{}', 'socket_{}', 'packet_{}',
                'request_{}', 'response_{}', 'header_{}', 'payload_{}',
                'route_{}', 'gateway_{}', 'proxy_{}', 'firewall_{}',
                'dns_{}', 'ip_{}', 'tcp_{}', 'udp_{}'
            ],
            'data': [
                'array_{}', 'list_{}', 'map_{}', 'set_{}',
                'queue_{}', 'stack_{}', 'heap_{}', 'tree_{}',
                'graph_{}', 'node_{}', 'edge_{}', 'vertex_{}',
                'index_{}', 'key_{}', 'value_{}', 'pair_{}'
            ],
            'operations': [
                'create_{}', 'read_{}', 'update_{}', 'delete_{}',
                'insert_{}', 'remove_{}', 'append_{}', 'prepend_{}',
                'merge_{}', 'split_{}', 'join_{}', 'filter_{}',
                'map_{}', 'reduce_{}', 'transform_{}', 'convert_{}'
            ]
        }
        
        concepts = []
        template_list = templates.get(category, ['concept_{}'])
        
        for i in range(count):
            template = random.choice(template_list)
            
            # Generate variations
            variations = ['basic', 'advanced', 'fast', 'secure', 'async', 
                         'cached', 'compressed', 'encrypted', 'optimized',
                         'parallel', 'distributed', 'atomic', 'bulk']
            
            concept = template.format(random.choice(variations))
            
            # Check if not already exists
            if concept.lower() not in self.used_concepts:
                concepts.append({
                    'concept': concept,
                    'category': category
                })
                
        return concepts
        
    def run_production(self, target=3000):
        """Run production until target is reached"""
        print(f"\n🚀 INICIANDO PRODUÇÃO ATÉ {target} PALAVRAS...")
        print(f"   Atual: {len(self.master_dict['symbols'])}")
        print(f"   Faltam: {target - len(self.master_dict['symbols'])}")
        print()
        
        # First, fix any existing duplicates
        self.fix_existing_duplicates()
        
        categories = ['programming', 'networking', 'data', 'operations']
        
        while len(self.master_dict['symbols']) < target:
            remaining = target - len(self.master_dict['symbols'])
            
            for category in categories:
                if len(self.master_dict['symbols']) >= target:
                    break
                    
                # Generate batch of concepts
                batch_size = min(100, remaining)
                concepts = self.generate_smart_concepts(category, batch_size)
                
                print(f"\n📂 Categoria: {category}")
                created = self.batch_create_concepts(concepts)
                
                # Show progress
                progress = len(self.master_dict['symbols']) / target * 100
                print(f"\n📊 Progresso: {len(self.master_dict['symbols'])}/{target} ({progress:.1f}%)")
                
        print("\n✅ PRODUÇÃO COMPLETA!")
        print(f"   Total de palavras: {len(self.master_dict['symbols'])}")
        print(f"   Caracteres disponíveis restantes: {len(self.available_chars):,}")
        
        return self.dictionary_file

if __name__ == "__main__":
    system = DigiLangZeroDuplicateSystem()
    
    # Import existing symbols first
    print("\n📥 IMPORTANDO SÍMBOLOS EXISTENTES...")
    
    existing_file = Path.home() / "Digimundo" / "DIGILANG_OPTIMIZED.json"
    if existing_file.exists():
        with open(existing_file, 'r') as f:
            existing = json.load(f)
            
        concepts_to_import = []
        for concept, symbol in existing.get('full_index', {}).items():
            concepts_to_import.append({
                'concept': concept,
                'category': 'imported'
            })
            
        system.batch_create_concepts(concepts_to_import)
    
    # Run production to 3000
    final_dict = system.run_production(target=3000)
    
    print(f"\n📚 Dicionário final: {final_dict}")
    print("🎯 Use DIGILANG_MASTER_DICTIONARY.json para o sistema final")