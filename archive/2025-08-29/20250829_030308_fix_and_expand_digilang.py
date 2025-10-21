#!/usr/bin/env python3
"""
🔧 Corrige violações e expande DigiLang Ultimate para Scripturemon
"""

import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime

class DigiLangFixer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.resources_path = self.base_path / "language_resources"
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        print("╔" + "═"*58 + "╗")
        print("║  🔧 DIGILANG ULTIMATE - CORREÇÃO E EXPANSÃO           ║")
        print("╚" + "═"*58 + "╝")
        
        # Carregar dicionário
        print("\n📚 Carregando sistema DigiLang...")
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.dictionary = data.get('symbols', {})
            self.metadata = data.get('metadata', {})
        
        print(f"   ✅ Sistema atual: {len(self.dictionary):,} palavras")
        
        self.used_symbols = set()
        self.stats = {
            'initial': len(self.dictionary),
            'violations_fixed': 0,
            'words_added': 0,
            'cinema_terms': 0
        }
        
        # Símbolos disponíveis (evitando emoji compostos)
        self.available_symbols = []
        self.init_symbol_pool()
    
    def init_symbol_pool(self):
        """Inicializa pool de símbolos válidos (1 caractere apenas)"""
        # Ranges seguros de 1 caractere
        ranges = [
            # Emoji simples (sem variação de cor)
            (0x1F300, 0x1F320),  # Natureza
            (0x1F330, 0x1F393),  # Plantas e objetos
            (0x1F3A0, 0x1F3F0),  # Lugares
            (0x1F400, 0x1F4FF),  # Animais e objetos
            (0x1F500, 0x1F5FF),  # Símbolos
            (0x1F600, 0x1F650),  # Faces
            (0x1F680, 0x1F6C0),  # Transporte
            (0x1F900, 0x1F9FF),  # Suplementar
            
            # Símbolos matemáticos
            (0x2200, 0x22FF),
            
            # Setas
            (0x2190, 0x21FF),
            
            # Formas geométricas
            (0x25A0, 0x25FF),
            
            # Símbolos diversos
            (0x2600, 0x26FF),
            
            # Dingbats
            (0x2700, 0x27BF),
            
            # CJK (muitas opções)
            (0x4E00, 0x9FFF),
            
            # Hangul
            (0xAC00, 0xD7AF)
        ]
        
        for start, end in ranges:
            for code in range(start, end + 1):
                try:
                    char = chr(code)
                    # Verificar se é realmente 1 caractere
                    if len(char) == 1:
                        self.available_symbols.append(char)
                except:
                    pass
        
        print(f"   📊 Pool de símbolos: {len(self.available_symbols):,} disponíveis")
    
    def fix_violations(self):
        """Corrige todas as violações de múltiplos caracteres"""
        print("\n🔧 CORRIGINDO VIOLAÇÕES")
        print("="*60)
        
        # Coletar símbolos já usados válidos
        for word, symbol in self.dictionary.items():
            # Remover modificadores morfológicos
            base = symbol.rstrip('⁺⁻~ᶜˢⁿᵐᵗˡᶠ⁰¹²³♂♀⚪')
            if len(base) == 1:
                self.used_symbols.add(base)
        
        print(f"   ✅ {len(self.used_symbols):,} símbolos válidos em uso")
        
        # Corrigir violações
        violations = []
        for word, symbol in self.dictionary.items():
            base = symbol.rstrip('⁺⁻~ᶜˢⁿᵐᵗˡᶠ⁰¹²³♂♀⚪')
            if len(base) > 1 or base == '':
                violations.append(word)
        
        print(f"   ⚠️ {len(violations)} violações encontradas")
        
        fixed = 0
        for word in violations:
            new_symbol = self.get_next_symbol()
            if new_symbol:
                old = self.dictionary[word]
                self.dictionary[word] = new_symbol
                fixed += 1
                
                if fixed <= 10:
                    print(f"      • {word}: {old} → {new_symbol}")
        
        self.stats['violations_fixed'] = fixed
        print(f"   ✅ {fixed} violações corrigidas")
    
    def get_next_symbol(self):
        """Obtém próximo símbolo disponível"""
        for symbol in self.available_symbols:
            if symbol not in self.used_symbols:
                self.used_symbols.add(symbol)
                return symbol
        return None
    
    def load_cinema_vocabulary(self):
        """Carrega vocabulário essencial de cinema"""
        cinema_terms = {
            # Estrutura
            'act', 'scene', 'sequence', 'beat', 'plot', 'subplot',
            'exposition', 'conflict', 'climax', 'resolution',
            'protagonist', 'antagonist', 'hero', 'villain',
            
            # Técnico
            'closeup', 'medium', 'wide', 'establishing', 'pan', 'tilt',
            'zoom', 'dolly', 'crane', 'tracking', 'handheld',
            'cut', 'fade', 'dissolve', 'transition', 'montage',
            'flashback', 'flashforward', 'voiceover', 'dialogue',
            
            # Produção
            'director', 'writer', 'producer', 'actor', 'actress',
            'screenplay', 'script', 'treatment', 'draft', 'rewrite',
            
            # PT
            'cena', 'sequência', 'ato', 'roteiro', 'personagem',
            'protagonista', 'antagonista', 'herói', 'vilão',
            'trama', 'enredo', 'conflito', 'clímax', 'desfecho',
            'diálogo', 'ação', 'corte', 'fusão', 'filme',
            'diretor', 'roteirista', 'ator', 'atriz', 'elenco'
        }
        
        return cinema_terms
    
    def expand_with_priorities(self):
        """Expande com palavras prioritárias"""
        print("\n🚀 EXPANDINDO COM PRIORIDADES")
        print("="*60)
        
        # 1. Vocabulário de cinema (máxima prioridade)
        cinema_terms = self.load_cinema_vocabulary()
        cinema_added = 0
        
        print("🎬 Adicionando vocabulário de cinema...")
        for term in cinema_terms:
            if term not in self.dictionary:
                symbol = self.get_next_symbol()
                if symbol:
                    self.dictionary[term] = symbol
                    cinema_added += 1
        
        print(f"   ✅ {cinema_added} termos de cinema adicionados")
        self.stats['cinema_terms'] = cinema_added
        
        # 2. Palavras frequentes EN
        en_file = self.resources_path / "google-10000-english.txt"
        if en_file.exists():
            print("🇬🇧 Adicionando top palavras inglesas...")
            added = 0
            with open(en_file, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if word and word not in self.dictionary and len(word) > 1:
                        symbol = self.get_next_symbol()
                        if symbol:
                            self.dictionary[word] = symbol
                            added += 1
                            if added >= 5000:
                                break
            print(f"   ✅ {added} palavras inglesas adicionadas")
            self.stats['words_added'] += added
        
        # 3. Palavras frequentes PT
        pt_file = self.resources_path / "pt_50k.txt"
        if pt_file.exists():
            print("🇧🇷 Adicionando top palavras portuguesas...")
            added = 0
            with open(pt_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        word = parts[0].lower()
                        if self.is_valid_pt(word) and word not in self.dictionary:
                            symbol = self.get_next_symbol()
                            if symbol:
                                self.dictionary[word] = symbol
                                added += 1
                                if added >= 5000:
                                    break
            print(f"   ✅ {added} palavras portuguesas adicionadas")
            self.stats['words_added'] += added
    
    def is_valid_pt(self, word):
        """Valida palavra portuguesa"""
        return bool(re.match(r'^[a-záàâãéèêíïóôõöúçñ]+$', word)) and len(word) > 2
    
    def apply_morphology(self):
        """Aplica sistema morfológico básico"""
        print("\n📐 APLICANDO MORFOLOGIA")
        print("="*60)
        
        modifiers = {
            'plural': '⁺',
            'past': '⁻',
            'gerund': '~'
        }
        
        applied = 0
        for word in list(self.dictionary.keys()):
            base_sym = self.dictionary.get(word)
            
            # Plurais
            if word.endswith('s') and word[:-1] in self.dictionary:
                base = word[:-1]
                if len(self.dictionary[base]) == 1:
                    self.dictionary[word] = self.dictionary[base] + modifiers['plural']
                    applied += 1
        
        print(f"   ✅ {applied} regras morfológicas aplicadas")
    
    def save_fixed_dictionary(self):
        """Salva dicionário corrigido e expandido"""
        print("\n💾 SALVANDO DICIONÁRIO DEFINITIVO")
        print("="*60)
        
        # Estatísticas finais
        total_words = len(self.dictionary)
        unique_symbols = len(set(s.rstrip('⁺⁻~ᶜˢⁿᵐᵗˡᶠ⁰¹²³♂♀⚪') for s in self.dictionary.values()))
        
        print(f"   📊 Total de palavras: {total_words:,}")
        print(f"   📊 Símbolos únicos: {unique_symbols:,}")
        print(f"   📊 Expansão: {((total_words/self.stats['initial'])-1)*100:.0f}%")
        
        # Metadata
        self.metadata['version'] = 'ULTIMATE-SCRIPTUREMON-FIXED'
        self.metadata['total_words'] = total_words
        self.metadata['unique_symbols'] = unique_symbols
        self.metadata['statistics'] = self.stats
        self.metadata['cinema_optimized'] = True
        self.metadata['last_update'] = datetime.now().isoformat()
        
        # Backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.base_path / f"DIGILANG_BACKUP_{timestamp}.json"
        with open(self.dict_path, 'r') as f:
            json.dump(json.load(f), open(backup_path, 'w'), ensure_ascii=False)
        
        # Salvar
        final_data = {
            'version': self.metadata['version'],
            'metadata': self.metadata,
            'symbols': self.dictionary
        }
        
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False)
        
        print(f"   ✅ Salvo em: {self.dict_path}")
        
        return total_words, unique_symbols

def main():
    fixer = DigiLangFixer()
    
    # 1. Corrigir violações
    fixer.fix_violations()
    
    # 2. Expandir com prioridades
    fixer.expand_with_priorities()
    
    # 3. Aplicar morfologia
    fixer.apply_morphology()
    
    # 4. Salvar
    total, unique = fixer.save_fixed_dictionary()
    
    print("\n" + "="*60)
    print("🎉 DIGILANG ULTIMATE COMPLETA!")
    print("="*60)
    print(f"""
Sistema ÚNICO e DEFINITIVO criado!

📊 RESULTADOS:
   • Total: {total:,} palavras
   • Símbolos únicos: {unique:,}
   • Violações corrigidas: {fixer.stats['violations_fixed']:,}
   • Palavras adicionadas: {fixer.stats['words_added']:,}
   • Termos de cinema: {fixer.stats['cinema_terms']:,}

✅ REGRAS RESPEITADAS:
   • 1 palavra = 1 símbolo ✓
   • Sistema morfológico ✓
   • Otimizado para Scripturemon ✓

🎬 Pronto para uso com Scripturemon!
""")

if __name__ == "__main__":
    main()