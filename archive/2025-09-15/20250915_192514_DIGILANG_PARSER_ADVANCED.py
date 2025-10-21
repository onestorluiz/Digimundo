#!/usr/bin/env python3
"""
🔧 DIGILANG ADVANCED PARSER - Extrai símbolos de qualquer formato
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter

class DigiLangAdvancedParser:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.all_symbols = []
        self.unique_symbols = {}
        self.categories = defaultdict(list)
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║         🔧 DIGILANG ADVANCED PARSER & ORGANIZER              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        
    def parse_all_files(self):
        """Parse all DigiLang files"""
        print("📥 PARSING TODOS OS ARQUIVOS...")
        print()
        
        # Find all potential files
        patterns = ['*digilang*.json', '*strategic*.json', '*symbols*.json', '*symbols*.txt']
        all_files = []
        
        for pattern in patterns:
            all_files.extend(self.base_path.glob(pattern))
            
        for filepath in all_files:
            if filepath.stat().st_size > 0:  # Skip empty files
                print(f"   📄 {filepath.name} ({filepath.stat().st_size / 1024:.1f} KB)")
                self.parse_file(filepath)
                
        print()
        print(f"📊 Total símbolos encontrados (bruto): {len(self.all_symbols)}")
        
    def parse_file(self, filepath):
        """Parse individual file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Try to extract JSON arrays from content
            json_arrays = re.findall(r'\[[\s\S]*?\]', content)
            
            for json_str in json_arrays:
                try:
                    # Clean up the JSON
                    json_str = json_str.replace('\n', '').replace('    ', '')
                    data = json.loads(json_str)
                    
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'c' in item and 's' in item:
                                self.all_symbols.append({
                                    'concept': item['c'],
                                    'symbol': item['s'],
                                    'source': filepath.name
                                })
                            elif isinstance(item, dict) and 'concept' in item:
                                self.all_symbols.append({
                                    'concept': item.get('concept', ''),
                                    'symbol': item.get('symbol', ''),
                                    'source': filepath.name
                                })
                except:
                    pass
                    
            # Also try line-by-line parsing for text formats
            lines = content.split('\n')
            for line in lines:
                # Pattern: concept=symbol or concept:symbol
                matches = re.findall(r'(\w+)\s*[=:]\s*([^\s,]+)', line)
                for match in matches:
                    if len(match) == 2:
                        self.all_symbols.append({
                            'concept': match[0],
                            'symbol': match[1],
                            'source': filepath.name
                        })
                        
        except Exception as e:
            print(f"      ⚠️ Erro parsing {filepath.name}: {str(e)[:50]}")
            
    def deduplicate_symbols(self):
        """Remove duplicates keeping best quality"""
        print()
        print("🔍 DEDUPLICANDO SÍMBOLOS...")
        
        for symbol in self.all_symbols:
            concept = symbol['concept'].lower().strip()
            
            # Skip empty or invalid
            if not concept or not symbol['symbol']:
                continue
                
            # Keep first occurrence or shorter symbols
            if concept not in self.unique_symbols:
                self.unique_symbols[concept] = symbol
            elif len(symbol['symbol']) < len(self.unique_symbols[concept]['symbol']):
                self.unique_symbols[concept] = symbol
                
        print(f"   ✓ Símbolos únicos: {len(self.unique_symbols)}")
        print(f"   ✓ Duplicatas removidas: {len(self.all_symbols) - len(self.unique_symbols)}")
        
    def categorize_symbols(self):
        """Categorize all unique symbols"""
        print()
        print("📂 CATEGORIZANDO SÍMBOLOS...")
        print()
        
        category_keywords = {
            'data_structures': ['array', 'list', 'stack', 'queue', 'tree', 'graph', 'hash', 'heap', 'map', 'set', 'table', 'vector', 'matrix'],
            'programming': ['function', 'method', 'class', 'object', 'variable', 'constant', 'loop', 'condition', 'algorithm', 'compile', 'debug', 'code'],
            'networking': ['tcp', 'udp', 'http', 'https', 'ip', 'dns', 'port', 'socket', 'protocol', 'packet', 'router', 'network', 'web'],
            'security': ['encrypt', 'decrypt', 'hash', 'auth', 'token', 'password', 'key', 'certificate', 'secure', 'vulnerability'],
            'database': ['sql', 'query', 'select', 'insert', 'update', 'delete', 'join', 'index', 'transaction', 'crud'],
            'ai_ml': ['neural', 'model', 'training', 'layer', 'weight', 'gradient', 'learning', 'classification', 'regression'],
            'cloud': ['docker', 'kubernetes', 'container', 'aws', 'azure', 'gcp', 'serverless', 'microservice', 'deploy'],
            'operations': ['create', 'read', 'update', 'delete', 'execute', 'run', 'start', 'stop', 'process'],
            'logic': ['and', 'or', 'not', 'if', 'then', 'else', 'true', 'false', 'equal', 'greater', 'less'],
            'math': ['add', 'subtract', 'multiply', 'divide', 'sum', 'integral', 'derivative', 'limit', 'equation']
        }
        
        for concept, symbol_data in self.unique_symbols.items():
            categorized = False
            
            for category, keywords in category_keywords.items():
                for keyword in keywords:
                    if keyword in concept:
                        self.categories[category].append(symbol_data)
                        categorized = True
                        break
                if categorized:
                    break
                    
            if not categorized:
                self.categories['general'].append(symbol_data)
                
        # Print category summary
        for category in sorted(self.categories.keys()):
            count = len(self.categories[category])
            print(f"   {category:20} {count:5} símbolos")
            
    def create_optimized_dictionary(self):
        """Create the final optimized dictionary"""
        print()
        print("📚 CRIANDO DICIONÁRIO OTIMIZADO...")
        
        # Select best symbols for core concepts
        core_symbols = {}
        
        # Priority concepts
        priority_concepts = [
            # Core programming
            'data', 'process', 'input', 'output', 'system',
            'function', 'variable', 'class', 'method', 'object',
            'array', 'list', 'stack', 'queue', 'tree', 'graph',
            'loop', 'if', 'else', 'while', 'for',
            
            # Operations
            'create', 'read', 'update', 'delete', 'execute',
            'start', 'stop', 'run', 'send', 'receive',
            
            # Logic
            'and', 'or', 'not', 'true', 'false',
            'equal', 'greater', 'less', 'between',
            
            # Network
            'tcp', 'udp', 'http', 'https', 'api',
            'request', 'response', 'server', 'client',
            
            # Data
            'database', 'table', 'query', 'index', 'transaction',
            'sql', 'json', 'xml', 'file', 'stream'
        ]
        
        # Get priority symbols
        for concept in priority_concepts:
            if concept in self.unique_symbols:
                core_symbols[concept] = self.unique_symbols[concept]['symbol']
                
        # Create final structure
        dictionary = {
            "metadata": {
                "name": "DigiLang",
                "version": "1.0.0",
                "total_symbols": len(self.unique_symbols),
                "core_symbols": len(core_symbols),
                "categories": len(self.categories)
            },
            "core": core_symbols,
            "categories": {},
            "full_index": {}
        }
        
        # Add categorized symbols
        for category, symbols in self.categories.items():
            dictionary["categories"][category] = {
                s['concept']: s['symbol'] 
                for s in symbols[:50]  # Top 50 per category
            }
            
        # Add full index
        for concept, data in self.unique_symbols.items():
            dictionary["full_index"][concept] = data['symbol']
            
        # Save
        output_path = self.base_path / "DIGILANG_OPTIMIZED.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, indent=2, ensure_ascii=False)
            
        print(f"   ✓ Salvo em: {output_path}")
        print(f"   ✓ Core symbols: {len(core_symbols)}")
        print(f"   ✓ Total symbols: {len(self.unique_symbols)}")
        
        return output_path, core_symbols
        
    def generate_quick_reference(self, core_symbols):
        """Generate a quick reference card"""
        print()
        print("═══════════════════════════════════════════════════════════════")
        print("📋 DIGILANG QUICK REFERENCE")
        print("═══════════════════════════════════════════════════════════════")
        print()
        
        sections = {
            "ESTRUTURAS": ['array', 'list', 'stack', 'queue', 'tree', 'graph'],
            "OPERAÇÕES": ['create', 'read', 'update', 'delete', 'execute'],
            "LÓGICA": ['if', 'else', 'and', 'or', 'not', 'true', 'false'],
            "REDE": ['http', 'tcp', 'api', 'server', 'client'],
            "DADOS": ['data', 'database', 'query', 'json', 'file']
        }
        
        for section, concepts in sections.items():
            print(f"{section}:")
            for concept in concepts:
                if concept in core_symbols:
                    print(f"   {concept:10} = {core_symbols[concept]}")
            print()
            
        # Save reference
        reference_path = self.base_path / "DIGILANG_REFERENCE.txt"
        with open(reference_path, 'w', encoding='utf-8') as f:
            f.write("DIGILANG QUICK REFERENCE\n")
            f.write("=" * 40 + "\n\n")
            
            for section, concepts in sections.items():
                f.write(f"{section}:\n")
                for concept in concepts:
                    if concept in core_symbols:
                        f.write(f"  {concept:15} = {core_symbols[concept]}\n")
                f.write("\n")
                
        print(f"📄 Referência salva em: {reference_path}")
        
    def run(self):
        """Execute the complete parsing and organization"""
        # Parse all files
        self.parse_all_files()
        
        # Deduplicate
        self.deduplicate_symbols()
        
        # Categorize
        self.categorize_symbols()
        
        # Create dictionary
        dict_path, core_symbols = self.create_optimized_dictionary()
        
        # Generate reference
        self.generate_quick_reference(core_symbols)
        
        print()
        print("✅ DIGILANG ORGANIZADO COM SUCESSO!")
        print(f"   • {len(self.unique_symbols)} símbolos únicos")
        print(f"   • {len(self.categories)} categorias")
        print(f"   • {len(core_symbols)} core symbols")
        print()
        print("📚 Use DIGILANG_OPTIMIZED.json para implementação")
        print("📋 Use DIGILANG_REFERENCE.txt para consulta rápida")
        
        return dict_path

if __name__ == "__main__":
    parser = DigiLangAdvancedParser()
    final_dict = parser.run()