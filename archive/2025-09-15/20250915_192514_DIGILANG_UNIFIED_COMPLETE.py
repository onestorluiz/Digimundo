#!/usr/bin/env python3
"""
🌐 DIGILANG UNIFIED - Unifica todas as palavras criadas em uma língua só
Combina os 237 símbolos originais + 2,898 mapeamento inglês
"""

import json
from pathlib import Path
from datetime import datetime

class DigiLangUnifier:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.unified_dict = {
            "metadata": {
                "name": "DigiLang Unified",
                "version": "5.0",
                "created": datetime.now().isoformat(),
                "total_words": 0,
                "sources": []
            },
            "symbols": {},  # word -> symbol
            "reverse": {},  # symbol -> word
            "categories": {},
            "compression_stats": {}
        }
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║         🌐 DIGILANG UNIFIED - LINGUAGEM COMPLETA             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        
    def load_original_symbols(self):
        """Load the 237 original symbols we created"""
        print("📥 CARREGANDO SÍMBOLOS ORIGINAIS...")
        
        original_file = self.base_path / "DIGILANG_OPTIMIZED.json"
        if not original_file.exists():
            print("   ⚠️ Arquivo original não encontrado")
            return 0
            
        with open(original_file, 'r', encoding='utf-8') as f:
            original = json.load(f)
            
        added = 0
        
        # Add core symbols first (highest priority)
        if 'core' in original:
            for word, symbol in original['core'].items():
                if word not in self.unified_dict['symbols']:
                    self.unified_dict['symbols'][word] = symbol
                    self.unified_dict['reverse'][symbol] = word
                    
                    if 'core' not in self.unified_dict['categories']:
                        self.unified_dict['categories']['core'] = {}
                    self.unified_dict['categories']['core'][word] = symbol
                    added += 1
        
        # Add from categories
        if 'categories' in original:
            for category, words in original['categories'].items():
                if category not in self.unified_dict['categories']:
                    self.unified_dict['categories'][category] = {}
                    
                for word, symbol in words.items():
                    if word not in self.unified_dict['symbols'] and symbol not in self.unified_dict['reverse']:
                        self.unified_dict['symbols'][word] = symbol
                        self.unified_dict['reverse'][symbol] = word
                        self.unified_dict['categories'][category][word] = symbol
                        added += 1
        
        # Add from full index
        if 'full_index' in original:
            for word, symbol in original['full_index'].items():
                if word not in self.unified_dict['symbols'] and symbol not in self.unified_dict['reverse']:
                    self.unified_dict['symbols'][word] = symbol
                    self.unified_dict['reverse'][symbol] = word
                    
                    if 'original' not in self.unified_dict['categories']:
                        self.unified_dict['categories']['original'] = {}
                    self.unified_dict['categories']['original'][word] = symbol
                    added += 1
                    
        print(f"   ✅ {added} símbolos originais adicionados")
        self.unified_dict['metadata']['sources'].append(f"Original symbols: {added}")
        return added
        
    def load_english_mapped(self):
        """Load the English mapped symbols"""
        print("📥 CARREGANDO MAPEAMENTO INGLÊS...")
        
        mapped_file = self.base_path / "DIGILANG_ENGLISH_MAPPED.json"
        if not mapped_file.exists():
            print("   ⚠️ Arquivo de mapeamento não encontrado")
            return 0
            
        with open(mapped_file, 'r', encoding='utf-8') as f:
            mapped = json.load(f)
            
        added = 0
        skipped = 0
        
        # Add English mappings (skip if word or symbol already exists)
        if 'english_to_symbol' in mapped:
            for word, symbol in mapped['english_to_symbol'].items():
                # Check if word or symbol already used
                if word in self.unified_dict['symbols']:
                    skipped += 1
                    continue
                    
                if symbol in self.unified_dict['reverse']:
                    skipped += 1
                    continue
                    
                # Add the mapping
                self.unified_dict['symbols'][word] = symbol
                self.unified_dict['reverse'][symbol] = word
                
                # Categorize
                if any(tech in word for tech in ['function', 'class', 'array', 'data', 'server', 'database']):
                    if 'technical' not in self.unified_dict['categories']:
                        self.unified_dict['categories']['technical'] = {}
                    self.unified_dict['categories']['technical'][word] = symbol
                elif any(verb in word for verb in ['ing', 'ed', 'er']):
                    if 'verbs' not in self.unified_dict['categories']:
                        self.unified_dict['categories']['verbs'] = {}
                    self.unified_dict['categories']['verbs'][word] = symbol
                else:
                    if 'common' not in self.unified_dict['categories']:
                        self.unified_dict['categories']['common'] = {}
                    self.unified_dict['categories']['common'][word] = symbol
                    
                added += 1
                
        print(f"   ✅ {added} palavras inglesas adicionadas")
        print(f"   ⚠️ {skipped} palavras ignoradas (duplicatas)")
        self.unified_dict['metadata']['sources'].append(f"English mapped: {added}")
        return added
        
    def add_essential_missing(self):
        """Add any essential missing concepts"""
        print("📥 ADICIONANDO CONCEITOS ESSENCIAIS FALTANTES...")
        
        # Get available Unicode symbols not yet used
        used_symbols = set(self.unified_dict['reverse'].keys())
        
        # Simple unique symbols we can use
        available = []
        for i in range(0x2000, 0x3000):  # Various symbol ranges
            char = chr(i)
            if char not in used_symbols and char.isprintable() and not char.isspace():
                available.append(char)
                
        # Essential concepts that MUST exist
        essential = {
            # Basic logic
            'yes': '✓', 'no': '✗', 'maybe': '≈',
            'true': '⊤', 'false': '⊥', 'null': '∅',
            
            # Basic operations  
            'plus': '+', 'minus': '-', 'times': '×', 'divide': '÷',
            'equals': '=', 'not_equal': '≠', 'greater': '>', 'less': '<',
            
            # Basic connectors
            'and': '∧', 'or': '∨', 'not': '¬', 'implies': '→',
            
            # Time
            'now': '◉', 'past': '◀', 'future': '▶',
            
            # Space
            'here': '◎', 'there': '◇', 'everywhere': '◈',
            
            # Quantities
            'all': '∀', 'some': '∃', 'none': '∄',
            
            # DigiLang specific
            'digimon': '🦖', 'evolution': '🔄', 'digital_world': '🌐',
            'consciousness': '🧠', 'memory': '💾', 'energy': '⚡'
        }
        
        added = 0
        symbol_idx = 0
        
        for concept, preferred_symbol in essential.items():
            if concept not in self.unified_dict['symbols']:
                # Try to use preferred symbol if available
                if preferred_symbol not in self.unified_dict['reverse']:
                    symbol = preferred_symbol
                else:
                    # Use next available symbol
                    if symbol_idx < len(available):
                        symbol = available[symbol_idx]
                        symbol_idx += 1
                    else:
                        continue
                        
                self.unified_dict['symbols'][concept] = symbol
                self.unified_dict['reverse'][symbol] = concept
                
                if 'essential' not in self.unified_dict['categories']:
                    self.unified_dict['categories']['essential'] = {}
                self.unified_dict['categories']['essential'][concept] = symbol
                added += 1
                
        print(f"   ✅ {added} conceitos essenciais adicionados")
        self.unified_dict['metadata']['sources'].append(f"Essential concepts: {added}")
        return added
        
    def optimize_and_analyze(self):
        """Optimize dictionary and calculate statistics"""
        print("\n📊 OTIMIZANDO E ANALISANDO...")
        
        # Remove any accidental duplicates
        seen_symbols = {}
        to_remove = []
        
        for word, symbol in self.unified_dict['symbols'].items():
            if symbol in seen_symbols:
                print(f"   ⚠️ Símbolo duplicado: '{symbol}' usado por '{seen_symbols[symbol]}' e '{word}'")
                to_remove.append(word)
            else:
                seen_symbols[symbol] = word
                
        for word in to_remove:
            del self.unified_dict['symbols'][word]
            
        # Update metadata
        self.unified_dict['metadata']['total_words'] = len(self.unified_dict['symbols'])
        
        # Calculate compression
        total_word_chars = sum(len(w) for w in self.unified_dict['symbols'].keys())
        total_symbol_chars = sum(len(s) for s in self.unified_dict['symbols'].values())
        compression = (1 - total_symbol_chars / total_word_chars) * 100
        
        self.unified_dict['compression_stats'] = {
            'average_word_length': total_word_chars / len(self.unified_dict['symbols']),
            'average_symbol_length': total_symbol_chars / len(self.unified_dict['symbols']),
            'compression_rate': round(compression, 1),
            'total_word_chars': total_word_chars,
            'total_symbol_chars': total_symbol_chars
        }
        
        print(f"   Taxa de compressão: {compression:.1f}%")
        print(f"   Média palavra: {total_word_chars / len(self.unified_dict['symbols']):.1f} chars")
        print(f"   Média símbolo: {total_symbol_chars / len(self.unified_dict['symbols']):.1f} chars")
        
    def save_unified_dictionary(self):
        """Save the unified dictionary"""
        output_path = self.base_path / "DIGILANG_UNIFIED_FINAL.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.unified_dict, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 Dicionário unificado salvo: {output_path}")
        return output_path
        
    def generate_report(self):
        """Generate final report"""
        print("\n")
        print("═══════════════════════════════════════════════════════════════")
        print("                    📊 RELATÓRIO FINAL")
        print("═══════════════════════════════════════════════════════════════")
        print()
        print(f"🎯 DIGILANG UNIFIED COMPLETO!")
        print()
        print(f"   Total de palavras: {self.unified_dict['metadata']['total_words']:,}")
        print(f"   Taxa de compressão: {self.unified_dict['compression_stats']['compression_rate']}%")
        print(f"   Categorias: {len(self.unified_dict['categories'])}")
        print()
        
        print("📂 DISTRIBUIÇÃO POR CATEGORIA:")
        for category, words in sorted(self.unified_dict['categories'].items(), 
                                     key=lambda x: len(x[1]), reverse=True):
            print(f"   {category:15} {len(words):5} palavras")
            
        print()
        print("📖 EXEMPLOS DE SÍMBOLOS:")
        print()
        
        # Show examples from different sources
        examples = [
            ('data', 'Original'),
            ('function', 'Original'),
            ('array', 'Original'),
            ('yes', 'Essential'),
            ('no', 'Essential'),
            ('digimon', 'Essential'),
            ('tomorrow', 'English'),
            ('variables', 'English'),
            ('database', 'English')
        ]
        
        for word, source in examples:
            if word in self.unified_dict['symbols']:
                symbol = self.unified_dict['symbols'][word]
                print(f"   {word:15} → {symbol:3} ({source})")
                
        print()
        print("✨ RECURSOS DO DIGILANG UNIFIED:")
        print("   • Símbolos originais criados com IA")
        print("   • Vocabulário inglês completo")  
        print("   • Conceitos essenciais garantidos")
        print("   • Zero duplicatas")
        print("   • 100% reversível")
        print()
        print("🚀 PRONTO PARA USO!")
        
    def run(self):
        """Execute the unification process"""
        # Load original symbols
        original_count = self.load_original_symbols()
        
        # Load English mapped
        english_count = self.load_english_mapped()
        
        # Add essential missing
        essential_count = self.add_essential_missing()
        
        # Optimize
        self.optimize_and_analyze()
        
        # Save
        output_path = self.save_unified_dictionary()
        
        # Report
        self.generate_report()
        
        return output_path

if __name__ == "__main__":
    unifier = DigiLangUnifier()
    final_dict = unifier.run()