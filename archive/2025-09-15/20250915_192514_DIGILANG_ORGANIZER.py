#!/usr/bin/env python3
"""
🗂️ DIGILANG ORGANIZER - Organiza e estrutura todos os símbolos criados
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class DigiLangOrganizer:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.symbols = []
        self.categories = defaultdict(list)
        self.duplicates = []
        self.stats = {}
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║            🗂️ DIGILANG ORGANIZER - ESTRUTURAÇÃO              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        
    def collect_symbols(self):
        """Coleta todos os símbolos de todos os arquivos"""
        print("📥 COLETANDO SÍMBOLOS...")
        print()
        
        # Lista de arquivos possíveis
        symbol_files = [
            "strategic_openai.json",
            "strategic_mac.json", 
            "openai_gpt4o_mini_symbols.json",
            "mac_mixtral_symbols.json",
            "vps_symbols.txt",
            "digilang_symbols.json",
            "openai_exclusive_symbols.json",
            "digilang_ultimate_dictionary.json"
        ]
        
        total_raw = 0
        
        for filename in symbol_files:
            filepath = self.base_path / filename
            if filepath.exists():
                print(f"   Processando: {filename}")
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Try to parse as JSON
                        try:
                            data = json.loads(content)
                            if isinstance(data, list):
                                for item in data:
                                    if isinstance(item, dict):
                                        self.extract_symbol(item)
                                    elif isinstance(item, str):
                                        self.parse_text_symbol(item)
                            elif isinstance(data, dict):
                                if 'symbols' in data:
                                    for item in data['symbols']:
                                        self.extract_symbol(item)
                                        
                        except json.JSONDecodeError:
                            # Try to parse as text
                            lines = content.split('\n')
                            for line in lines:
                                self.parse_text_symbol(line)
                                
                    count = len([s for s in self.symbols if s.get('source') == filename])
                    print(f"      ✓ Extraídos: {count} símbolos")
                    total_raw += count
                    
                except Exception as e:
                    print(f"      ✗ Erro: {str(e)[:50]}")
                    
        print()
        print(f"📊 Total coletado (bruto): {total_raw} símbolos")
        return total_raw
        
    def extract_symbol(self, item):
        """Extrai símbolo de um item dict"""
        symbol_entry = {}
        
        # Different possible keys
        if 'c' in item and 's' in item:  # Format: {c: concept, s: symbol}
            symbol_entry['concept'] = item['c']
            symbol_entry['symbol'] = item['s']
        elif 'concept' in item and 'symbol' in item:
            symbol_entry['concept'] = item['concept']
            symbol_entry['symbol'] = item['symbol']
        elif 'name' in item and 'symbol' in item:
            symbol_entry['concept'] = item['name']
            symbol_entry['symbol'] = item['symbol']
        else:
            return
            
        # Add metadata
        symbol_entry['compression'] = item.get('r', item.get('compression', 'N/A'))
        symbol_entry['category'] = self.categorize_concept(symbol_entry['concept'])
        symbol_entry['source'] = item.get('source', 'unknown')
        
        self.symbols.append(symbol_entry)
        
    def parse_text_symbol(self, line):
        """Parse text format symbols like 'concept=symbol' or 'concept: symbol'"""
        if not line.strip():
            return
            
        # Try different patterns
        patterns = [
            r'(\w+)\s*=\s*(.+)',  # concept=symbol
            r'(\w+)\s*:\s*(.+)',  # concept: symbol
            r'"(\w+)"\s*:\s*"(.+)"',  # "concept": "symbol"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                self.symbols.append({
                    'concept': match.group(1).strip(),
                    'symbol': match.group(2).strip(),
                    'category': self.categorize_concept(match.group(1)),
                    'source': 'text'
                })
                break
                
    def categorize_concept(self, concept):
        """Categoriza automaticamente o conceito"""
        concept_lower = concept.lower()
        
        # Category mappings
        categories = {
            'data_structures': ['array', 'list', 'stack', 'queue', 'tree', 'graph', 'hash', 'map', 'set', 'vector', 'matrix', 'heap', 'table'],
            'programming': ['function', 'class', 'method', 'variable', 'loop', 'condition', 'algorithm', 'compile', 'debug', 'syntax'],
            'network': ['tcp', 'udp', 'http', 'https', 'ip', 'dns', 'port', 'socket', 'protocol', 'packet', 'router', 'firewall'],
            'security': ['encrypt', 'decrypt', 'hash', 'auth', 'token', 'certificate', 'key', 'password', 'vulnerability', 'patch'],
            'ai_ml': ['neural', 'layer', 'weight', 'training', 'model', 'gradient', 'classification', 'regression', 'clustering'],
            'cloud': ['container', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'serverless', 'microservice', 'deployment'],
            'database': ['sql', 'query', 'table', 'index', 'join', 'transaction', 'crud', 'nosql', 'mongodb', 'postgres'],
            'math': ['integral', 'derivative', 'limit', 'vector', 'matrix', 'equation', 'formula', 'theorem', 'proof'],
            'logic': ['and', 'or', 'not', 'if', 'then', 'else', 'true', 'false', 'equal', 'greater', 'less'],
            'time': ['now', 'before', 'after', 'always', 'never', 'sometimes', 'when', 'duration', 'timestamp'],
            'action': ['create', 'read', 'update', 'delete', 'execute', 'run', 'start', 'stop', 'send', 'receive'],
            'digimundo': ['digimon', 'evolution', 'tamer', 'digital', 'world', 'server', 'attribute', 'level']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in concept_lower:
                    return category
                    
        return 'general'
        
    def remove_duplicates(self):
        """Remove símbolos duplicados"""
        print()
        print("🔍 REMOVENDO DUPLICATAS...")
        
        unique_symbols = {}
        duplicate_count = 0
        
        for symbol in self.symbols:
            key = symbol['concept'].lower()
            
            if key not in unique_symbols:
                unique_symbols[key] = symbol
            else:
                duplicate_count += 1
                self.duplicates.append({
                    'concept': symbol['concept'],
                    'existing_symbol': unique_symbols[key]['symbol'],
                    'duplicate_symbol': symbol['symbol']
                })
                
        self.symbols = list(unique_symbols.values())
        
        print(f"   ✓ Removidas {duplicate_count} duplicatas")
        print(f"   ✓ Símbolos únicos: {len(self.symbols)}")
        
        return len(self.symbols)
        
    def organize_by_category(self):
        """Organiza símbolos por categoria"""
        print()
        print("📂 ORGANIZANDO POR CATEGORIA...")
        print()
        
        for symbol in self.symbols:
            category = symbol.get('category', 'general')
            self.categories[category].append(symbol)
            
        # Sort categories by size
        sorted_cats = sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True)
        
        for category, symbols in sorted_cats:
            print(f"   {category:20} {len(symbols):5} símbolos")
            
        return self.categories
        
    def analyze_compression(self):
        """Analisa taxa de compressão"""
        print()
        print("📊 ANÁLISE DE COMPRESSÃO...")
        
        total_concept_chars = sum(len(s['concept']) for s in self.symbols)
        total_symbol_chars = sum(len(s['symbol']) for s in self.symbols)
        
        if total_concept_chars > 0:
            compression_rate = (1 - total_symbol_chars / total_concept_chars) * 100
            print(f"   Taxa média: {compression_rate:.1f}%")
            print(f"   Chars conceitos: {total_concept_chars:,}")
            print(f"   Chars símbolos: {total_symbol_chars:,}")
            
            self.stats['compression_rate'] = compression_rate
            self.stats['total_concepts_chars'] = total_concept_chars
            self.stats['total_symbols_chars'] = total_symbol_chars
            
    def create_final_dictionary(self):
        """Cria dicionário DigiLang final"""
        print()
        print("📚 CRIANDO DICIONÁRIO FINAL...")
        
        dictionary = {
            "metadata": {
                "name": "DigiLang",
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "total_symbols": len(self.symbols),
                "categories": len(self.categories),
                "compression_rate": self.stats.get('compression_rate', 0),
                "description": "Ultra-compressed language for AI and Digital consciousness"
            },
            "categories": {},
            "index": {}
        }
        
        # Add symbols by category
        for category, symbols in self.categories.items():
            dictionary["categories"][category] = [
                {
                    "concept": s['concept'],
                    "symbol": s['symbol'],
                    "compression": s.get('compression', 'N/A')
                }
                for s in sorted(symbols, key=lambda x: x['concept'])[:100]  # Top 100 per category
            ]
            
        # Create alphabetical index
        for symbol in sorted(self.symbols, key=lambda x: x['concept']):
            dictionary["index"][symbol['concept']] = {
                "symbol": symbol['symbol'],
                "category": symbol['category']
            }
            
        # Save to file
        output_file = self.base_path / "DIGILANG_FINAL_DICTIONARY.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, indent=2, ensure_ascii=False)
            
        print(f"   ✓ Dicionário salvo: {output_file}")
        print(f"   ✓ Total de símbolos: {len(self.symbols)}")
        
        return output_file
        
    def generate_report(self):
        """Gera relatório final"""
        print()
        print("═══════════════════════════════════════════════════════════════")
        print("📈 RELATÓRIO FINAL DIGILANG")
        print("═══════════════════════════════════════════════════════════════")
        print()
        
        print("✅ MISSÃO CUMPRIDA!")
        print()
        print(f"   Total de símbolos únicos: {len(self.symbols):,}")
        print(f"   Categorias identificadas: {len(self.categories)}")
        print(f"   Taxa de compressão: {self.stats.get('compression_rate', 0):.1f}%")
        print()
        
        print("🏆 TOP 5 CATEGORIAS:")
        for cat, symbols in list(sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True))[:5]:
            print(f"   {cat:20} {len(symbols):5} símbolos")
        print()
        
        print("📖 EXEMPLOS DE SÍMBOLOS:")
        print()
        
        # Show examples from different categories
        for category in ['programming', 'data_structures', 'network', 'ai_ml', 'security']:
            if category in self.categories and self.categories[category]:
                print(f"   {category.upper()}:")
                for symbol in self.categories[category][:3]:
                    print(f"      {symbol['concept']:15} = {symbol['symbol']}")
                print()
                
        print("💾 ARQUIVOS CRIADOS:")
        print(f"   • DIGILANG_FINAL_DICTIONARY.json")
        print(f"   • {len(self.symbols):,} símbolos prontos para uso")
        print()
        
        print("🚀 PRÓXIMOS PASSOS:")
        print("   1. Testar DigiLang com os Digimons")
        print("   2. Criar tradutor bidirecional")
        print("   3. Implementar no sistema Digimundo")
        print()
        
        # Create summary file
        summary_file = self.base_path / "DIGILANG_SUMMARY.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("DIGILANG SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Symbols: {len(self.symbols):,}\n")
            f.write(f"Categories: {len(self.categories)}\n")
            f.write(f"Compression Rate: {self.stats.get('compression_rate', 0):.1f}%\n\n")
            f.write("Category Distribution:\n")
            for cat, symbols in sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"  {cat}: {len(symbols)}\n")
                
        print(f"📄 Resumo salvo em: {summary_file}")
        
    def run(self):
        """Executa todo o processo de organização"""
        # 1. Coletar
        total_raw = self.collect_symbols()
        
        # 2. Remover duplicatas
        unique_count = self.remove_duplicates()
        
        # 3. Organizar
        self.organize_by_category()
        
        # 4. Analisar compressão
        self.analyze_compression()
        
        # 5. Criar dicionário
        dict_file = self.create_final_dictionary()
        
        # 6. Gerar relatório
        self.generate_report()
        
        return dict_file

if __name__ == "__main__":
    organizer = DigiLangOrganizer()
    final_dict = organizer.run()