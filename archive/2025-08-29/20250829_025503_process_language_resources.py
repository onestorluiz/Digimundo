#!/usr/bin/env python3
"""
🚀 Processador de Recursos Linguísticos para DigiLang Universal v30.0
Processa os arquivos baixados e expande o dicionário para 300k+ palavras
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

class LanguageResourceProcessor:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.resources_path = self.base_path / "language_resources"
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        print("╔" + "═"*58 + "╗")
        print("║  🚀 DIGILANG UNIVERSAL v30.0 - MEGA EXPANSÃO          ║")
        print("╚" + "═"*58 + "╝")
        
        # Carregar dicionário atual
        print("\n📚 Carregando dicionário base...")
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.dictionary = data.get('symbols', {})
            self.metadata = data
        
        print(f"   ✅ Base atual: {len(self.dictionary):,} palavras")
        
        # Símbolos usados
        self.used_symbols = set(self.dictionary.values())
        
        # Novo dicionário expandido
        self.expanded_dict = dict(self.dictionary)
        
        # Estatísticas
        self.stats = {
            'initial': len(self.dictionary),
            'en_words': 0,
            'pt_words': 0,
            'cognates': 0,
            'total_added': 0
        }
        
        # Contador de símbolos por tipo
        self.symbol_counter = {
            'ascii': 33,  # Começar do !
            'math': 0x2200,
            'arrows': 0x2190,
            'emoji': 0x1F300,
            'cjk': 0x4E00,
            'hangul': 0xAC00
        }
    
    def load_english_resources(self):
        """Carrega e processa recursos em inglês"""
        print("\n🇬🇧 PROCESSANDO RECURSOS EM INGLÊS")
        print("="*60)
        
        en_words = set()
        en_freq = {}
        
        # 1. Google 10k
        google_10k = self.resources_path / "google-10000-english.txt"
        if google_10k.exists():
            print("📖 Processando Google 10k...")
            with open(google_10k, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    word = line.strip().lower()
                    if word and word.isalpha():
                        en_words.add(word)
                        en_freq[word] = 10000 - i  # Maior score = mais frequente
            print(f"   ✅ {len(en_words):,} palavras")
        
        # 2. Top 50k com frequência
        en_50k = self.resources_path / "en_50k.txt"
        if en_50k.exists():
            print("📖 Processando top 50k inglês...")
            with open(en_50k, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        freq = int(parts[1]) if parts[1].isdigit() else 0
                        if word.isalpha():
                            en_words.add(word)
                            en_freq[word] = max(en_freq.get(word, 0), freq)
            print(f"   ✅ Total: {len(en_words):,} palavras únicas")
        
        # 3. Dicionário completo (para cobertura)
        full_dict = self.resources_path / "english-words.txt"
        if full_dict.exists():
            print("📖 Processando dicionário completo inglês...")
            with open(full_dict, 'r', encoding='utf-8') as f:
                before = len(en_words)
                for line in f:
                    word = line.strip().lower()
                    if word and word.isalpha() and len(word) > 2:
                        en_words.add(word)
                added = len(en_words) - before
                print(f"   ✅ +{added:,} palavras adicionais")
        
        self.stats['en_words'] = len(en_words)
        print(f"\n📊 Total inglês: {len(en_words):,} palavras únicas")
        
        return en_words, en_freq
    
    def load_portuguese_resources(self):
        """Carrega e processa recursos em português"""
        print("\n🇧🇷 PROCESSANDO RECURSOS EM PORTUGUÊS")
        print("="*60)
        
        pt_words = set()
        pt_freq = {}
        
        # 1. Top 50k português
        pt_50k = self.resources_path / "pt_50k.txt"
        if pt_50k.exists():
            print("📖 Processando top 50k português...")
            with open(pt_50k, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        freq = int(parts[1]) if parts[1].isdigit() else 0
                        if self.is_portuguese_word(word):
                            pt_words.add(word)
                            pt_freq[word] = freq
            print(f"   ✅ {len(pt_words):,} palavras")
        
        # 2. Dicionário PT-BR completo
        pt_dict = self.resources_path / "palavras-ptbr.txt"
        if pt_dict.exists():
            print("📖 Processando dicionário PT-BR...")
            with open(pt_dict, 'r', encoding='utf-8', errors='ignore') as f:
                before = len(pt_words)
                for line in f:
                    word = line.strip().lower()
                    if self.is_portuguese_word(word) and len(word) > 2:
                        pt_words.add(word)
                added = len(pt_words) - before
                print(f"   ✅ +{added:,} palavras adicionais")
        
        self.stats['pt_words'] = len(pt_words)
        print(f"\n📊 Total português: {len(pt_words):,} palavras únicas")
        
        return pt_words, pt_freq
    
    def is_portuguese_word(self, word):
        """Verifica se é palavra portuguesa válida"""
        if not word or not isinstance(word, str):
            return False
        # Permitir letras, acentos e hífen
        return bool(re.match(r'^[a-záàâãéèêíïóôõöúçñ\-]+$', word))
    
    def detect_cognates(self, en_words, pt_words):
        """Detecta e mapeia cognatos PT/EN"""
        print("\n🔗 DETECTANDO COGNATOS")
        print("="*60)
        
        cognate_map = {}
        
        # Padrões de cognatos
        patterns = [
            ('tion', 'ção'),
            ('sion', 'são'),
            ('ty', 'dade'),
            ('ble', 'vel'),
            ('ive', 'ivo'),
            ('ous', 'oso'),
            ('al', 'al'),
            ('ic', 'ico'),
            ('ism', 'ismo'),
            ('ist', 'ista'),
            ('ment', 'mento'),
            ('ure', 'ura'),
            ('ary', 'ário'),
            ('ory', 'ório'),
            ('age', 'agem'),
            ('cy', 'cia'),
            ('ny', 'nia'),
            ('phy', 'fia'),
            ('logy', 'logia'),
            ('graphy', 'grafia')
        ]
        
        # Buscar cognatos por padrão
        for en_suffix, pt_suffix in patterns:
            en_candidates = [w for w in en_words if w.endswith(en_suffix)]
            
            for en_word in en_candidates:
                stem = en_word[:-len(en_suffix)]
                pt_word = stem + pt_suffix
                
                if pt_word in pt_words:
                    cognate_map[en_word] = pt_word
        
        # Cognatos idênticos
        identical = en_words.intersection(pt_words)
        for word in identical:
            cognate_map[word] = word
        
        self.stats['cognates'] = len(cognate_map)
        print(f"✅ {len(cognate_map):,} cognatos detectados")
        
        return cognate_map
    
    def get_next_simple_symbol(self):
        """Obtém próximo símbolo simples para palavras frequentes"""
        # Tentar ASCII primeiro
        if self.symbol_counter['ascii'] < 127:
            symbol = chr(self.symbol_counter['ascii'])
            if symbol not in self.used_symbols:
                self.symbol_counter['ascii'] += 1
                self.used_symbols.add(symbol)
                return symbol
            self.symbol_counter['ascii'] += 1
            return self.get_next_simple_symbol()
        
        # Depois matemáticos
        if self.symbol_counter['math'] < 0x2300:
            symbol = chr(self.symbol_counter['math'])
            if symbol not in self.used_symbols:
                self.symbol_counter['math'] += 1
                self.used_symbols.add(symbol)
                return symbol
            self.symbol_counter['math'] += 1
            return self.get_next_simple_symbol()
        
        # Setas
        if self.symbol_counter['arrows'] < 0x21FF:
            symbol = chr(self.symbol_counter['arrows'])
            if symbol not in self.used_symbols:
                self.symbol_counter['arrows'] += 1
                self.used_symbols.add(symbol)
                return symbol
            self.symbol_counter['arrows'] += 1
            return self.get_next_simple_symbol()
        
        return None
    
    def get_next_complex_symbol(self):
        """Obtém próximo símbolo complexo para palavras menos frequentes"""
        # Emoji
        if self.symbol_counter['emoji'] < 0x1F9FF:
            symbol = chr(self.symbol_counter['emoji'])
            if symbol not in self.used_symbols:
                self.symbol_counter['emoji'] += 1
                self.used_symbols.add(symbol)
                return symbol
            self.symbol_counter['emoji'] += 1
            return self.get_next_complex_symbol()
        
        # CJK
        if self.symbol_counter['cjk'] < 0x9FFF:
            symbol = chr(self.symbol_counter['cjk'])
            if symbol not in self.used_symbols:
                self.symbol_counter['cjk'] += 1
                self.used_symbols.add(symbol)
                return symbol
            self.symbol_counter['cjk'] += 1
            return self.get_next_complex_symbol()
        
        # Hangul
        if self.symbol_counter['hangul'] < 0xD7AF:
            symbol = chr(self.symbol_counter['hangul'])
            if symbol not in self.used_symbols:
                self.symbol_counter['hangul'] += 1
                self.used_symbols.add(symbol)
                return symbol
            self.symbol_counter['hangul'] += 1
            return self.get_next_complex_symbol()
        
        return None
    
    def expand_dictionary(self, en_words, en_freq, pt_words, pt_freq, cognate_map):
        """Expande o dicionário com todas as palavras"""
        print("\n🔧 EXPANDINDO DICIONÁRIO")
        print("="*60)
        
        added = 0
        
        # 1. Adicionar top palavras frequentes com símbolos simples
        print("⚡ Adicionando palavras frequentes...")
        
        # Combinar frequências EN e PT
        all_freq = {}
        for word, freq in en_freq.items():
            all_freq[word] = freq
        for word, freq in pt_freq.items():
            all_freq[word] = all_freq.get(word, 0) + freq
        
        # Ordenar por frequência
        sorted_freq = sorted(all_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Top 5000 com símbolos simples
        for word, freq in sorted_freq[:5000]:
            if word not in self.expanded_dict:
                symbol = self.get_next_simple_symbol()
                if symbol:
                    self.expanded_dict[word] = symbol
                    added += 1
                    
                    # Se é cognato, adicionar o par também
                    if word in cognate_map:
                        pt_word = cognate_map[word]
                        if pt_word not in self.expanded_dict:
                            self.expanded_dict[pt_word] = symbol
                            added += 1
        
        print(f"   ✅ {added} palavras frequentes adicionadas")
        
        # 2. Adicionar resto das palavras EN
        print("🇬🇧 Adicionando palavras inglesas...")
        en_added = 0
        for word in en_words:
            if word not in self.expanded_dict:
                symbol = self.get_next_complex_symbol()
                if symbol:
                    self.expanded_dict[word] = symbol
                    en_added += 1
                    
                    # Cognato?
                    if word in cognate_map:
                        pt_word = cognate_map[word]
                        if pt_word not in self.expanded_dict:
                            self.expanded_dict[pt_word] = symbol
                            en_added += 1
                
                if en_added >= 50000:  # Limitar para não explodir
                    break
        
        print(f"   ✅ {en_added} palavras inglesas adicionadas")
        
        # 3. Adicionar palavras PT restantes
        print("🇧🇷 Adicionando palavras portuguesas...")
        pt_added = 0
        for word in pt_words:
            if word not in self.expanded_dict:
                symbol = self.get_next_complex_symbol()
                if symbol:
                    self.expanded_dict[word] = symbol
                    pt_added += 1
                
                if pt_added >= 50000:  # Limitar
                    break
        
        print(f"   ✅ {pt_added} palavras portuguesas adicionadas")
        
        self.stats['total_added'] = added + en_added + pt_added
        
    def save_expanded_dictionary(self):
        """Salva o dicionário expandido"""
        print("\n💾 SALVANDO DICIONÁRIO EXPANDIDO")
        print("="*60)
        
        # Estatísticas finais
        total_words = len(self.expanded_dict)
        unique_symbols = len(set(self.expanded_dict.values()))
        
        print(f"   📊 Total de palavras: {total_words:,}")
        print(f"   📊 Símbolos únicos: {unique_symbols:,}")
        print(f"   📊 Taxa de compressão: {(1 - unique_symbols/total_words)*100:.1f}%")
        print(f"   📊 Expansão: {((total_words/self.stats['initial'])-1)*100:.0f}%")
        
        # Preparar metadata
        self.metadata['version'] = '30.0-MEGA-UNIVERSAL'
        self.metadata['total_words'] = total_words
        self.metadata['unique_symbols'] = unique_symbols
        self.metadata['statistics'] = self.stats
        self.metadata['coverage'] = {
            'english': f"{self.stats['en_words']:,} words",
            'portuguese': f"{self.stats['pt_words']:,} palavras",
            'cognates': f"{self.stats['cognates']:,} detected"
        }
        self.metadata['last_update'] = datetime.now().isoformat()
        
        # Salvar
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Backup
        backup_path = self.base_path / f"DIGILANG_BACKUP_v20_{timestamp}.json"
        with open(self.dict_path, 'r') as f:
            backup = json.load(f)
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup, f, ensure_ascii=False)
        print(f"   💾 Backup: {backup_path}")
        
        # Salvar novo
        final_data = {
            'version': self.metadata['version'],
            'metadata': self.metadata,
            'symbols': self.expanded_dict
        }
        
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False)
        
        print(f"   ✅ Dicionário atualizado: {self.dict_path}")
        
        # Salvar versão completa com análise
        analysis_path = self.base_path / f"DIGILANG_v30_ANALYSIS_{timestamp}.json"
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump({
                'version': self.metadata['version'],
                'statistics': self.stats,
                'total_words': total_words,
                'unique_symbols': unique_symbols,
                'sample_words': list(self.expanded_dict.items())[:100]
            }, f, ensure_ascii=False, indent=2)
        
        print(f"   📊 Análise: {analysis_path}")

def main():
    processor = LanguageResourceProcessor()
    
    # Carregar recursos
    en_words, en_freq = processor.load_english_resources()
    pt_words, pt_freq = processor.load_portuguese_resources()
    
    # Detectar cognatos
    cognate_map = processor.detect_cognates(en_words, pt_words)
    
    # Expandir dicionário
    processor.expand_dictionary(en_words, en_freq, pt_words, pt_freq, cognate_map)
    
    # Salvar
    processor.save_expanded_dictionary()
    
    print("\n" + "="*60)
    print("🎉 MEGA EXPANSÃO COMPLETA!")
    print("="*60)
    print(f"""
DigiLang Universal v30.0 criada com sucesso!

📊 RESULTADOS FINAIS:
   • Palavras iniciais: {processor.stats['initial']:,}
   • Palavras finais: {len(processor.expanded_dict):,}
   • Expansão: {((len(processor.expanded_dict)/processor.stats['initial'])-1)*100:.0f}%
   • Palavras adicionadas: {processor.stats['total_added']:,}
   
📈 COBERTURA:
   • Inglês: {processor.stats['en_words']:,} palavras
   • Português: {processor.stats['pt_words']:,} palavras
   • Cognatos: {processor.stats['cognates']:,} detectados
   
✨ DigiLang agora tem cobertura MASSIVA de PT/EN!
""")

if __name__ == "__main__":
    main()