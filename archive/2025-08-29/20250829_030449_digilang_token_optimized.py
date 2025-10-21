#!/usr/bin/env python3
"""
💰 DigiLang Token-Optimized - Minimiza uso de tokens para Scripturemon
Prioriza caracteres de 1 token sobre visual
"""

import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime
import unicodedata

class TokenOptimizedDigiLang:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.resources_path = self.base_path / "language_resources"
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        print("╔" + "═"*58 + "╗")
        print("║  💰 DIGILANG TOKEN-OPTIMIZED PARA SCRIPTUREMON        ║")
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
            'optimized': 0,
            'expanded': 0,
            'token_savings': 0
        }
        
        # PRIORIDADE DE SÍMBOLOS POR CUSTO DE TOKEN
        self.symbol_priority = self.init_token_efficient_symbols()
        
    def init_token_efficient_symbols(self):
        """
        Inicializa símbolos por ordem de eficiência de token
        PRIORIDADE MÁXIMA: 1 token por símbolo
        """
        print("\n💰 ANÁLISE DE CUSTO DE TOKENS")
        print("="*60)
        
        symbols = []
        
        # 1. ASCII PRINTABLE (1 token cada) - MÁXIMA PRIORIDADE
        print("   1️⃣ ASCII (1 token cada):")
        ascii_chars = []
        for code in range(33, 127):  # ! até ~
            char = chr(code)
            # Pular alguns que podem causar problemas em JSON
            if char not in ['"', '\\', '/']:
                ascii_chars.append(char)
        symbols.extend(ascii_chars)
        print(f"      ✅ {len(ascii_chars)} caracteres ASCII disponíveis")
        
        # 2. LATIN EXTENDED (1 token cada)
        print("   2️⃣ Latin Extended (1 token cada):")
        latin_ext = []
        for code in range(0x00A1, 0x00FF):  # ¡ até ÿ
            char = chr(code)
            latin_ext.append(char)
        symbols.extend(latin_ext)
        print(f"      ✅ {len(latin_ext)} caracteres Latin Extended")
        
        # 3. GREEK (1 token cada)
        print("   3️⃣ Greek (1 token cada):")
        greek = []
        for code in range(0x0391, 0x03C9):  # Α até ω
            char = chr(code)
            greek.append(char)
        symbols.extend(greek)
        print(f"      ✅ {len(greek)} caracteres gregos")
        
        # 4. CYRILLIC (1 token cada)
        print("   4️⃣ Cyrillic (1 token cada):")
        cyrillic = []
        for code in range(0x0410, 0x044F):  # А até я
            char = chr(code)
            cyrillic.append(char)
        symbols.extend(cyrillic)
        print(f"      ✅ {len(cyrillic)} caracteres cirílicos")
        
        # 5. CJK IDEOGRAPHS (1-2 tokens, mas MUITAS opções)
        print("   5️⃣ CJK (1-2 tokens cada):")
        cjk = []
        # Pegar amostra de CJK comuns
        for code in range(0x4E00, 0x9FFF):  # 一 até 鿿
            char = chr(code)
            cjk.append(char)
            if len(cjk) >= 10000:  # Limitar para não explodir
                break
        symbols.extend(cjk)
        print(f"      ✅ {len(cjk)} caracteres CJK")
        
        # 6. HANGUL (1-2 tokens)
        print("   6️⃣ Hangul (1-2 tokens cada):")
        hangul = []
        for code in range(0xAC00, 0xD7AF):  # 가 até 힯
            char = chr(code)
            hangul.append(char)
            if len(hangul) >= 5000:
                break
        symbols.extend(hangul)
        print(f"      ✅ {len(hangul)} caracteres Hangul")
        
        # EVITAR: Emoji (2-4 tokens) - usar só se necessário
        print("\n   ❌ EVITANDO:")
        print("      • Emoji (2-4 tokens cada)")
        print("      • Símbolos compostos")
        print("      • Caracteres com modificadores")
        
        print(f"\n   📊 TOTAL: {len(symbols):,} símbolos eficientes disponíveis")
        
        return symbols
    
    def estimate_token_cost(self, text):
        """Estima custo em tokens de um texto"""
        tokens = 0
        for char in text:
            code = ord(char)
            if code < 128:  # ASCII
                tokens += 1
            elif code < 0x800:  # Latin, Greek, Cyrillic
                tokens += 1
            elif 0x4E00 <= code <= 0x9FFF:  # CJK
                tokens += 1.5  # Média
            elif 0x1F300 <= code <= 0x1F9FF:  # Emoji
                tokens += 3  # Média emoji
            else:
                tokens += 2  # Outros
        return tokens
    
    def optimize_existing_dictionary(self):
        """Otimiza dicionário existente para economia de tokens"""
        print("\n🔧 OTIMIZANDO DICIONÁRIO EXISTENTE")
        print("="*60)
        
        # Análise de custo atual
        current_cost = 0
        for word, symbol in self.dictionary.items():
            current_cost += self.estimate_token_cost(symbol)
        
        print(f"   💰 Custo atual: ~{current_cost:,.0f} tokens")
        
        # Coletar palavras por frequência
        freq_words = self.load_frequency_data()
        
        # Realocar símbolos: mais frequentes = símbolos mais baratos
        print("\n   🔄 Realocando símbolos por frequência...")
        
        symbol_index = 0
        optimized = 0
        
        # Top 10000 palavras mais frequentes com símbolos ASCII/Latin
        for word, freq in freq_words[:10000]:
            if word in self.dictionary and symbol_index < len(self.symbol_priority):
                old_symbol = self.dictionary[word]
                old_cost = self.estimate_token_cost(old_symbol)
                
                new_symbol = self.symbol_priority[symbol_index]
                new_cost = self.estimate_token_cost(new_symbol)
                
                if new_cost < old_cost and new_symbol not in self.used_symbols:
                    self.dictionary[word] = new_symbol
                    self.used_symbols.add(new_symbol)
                    symbol_index += 1
                    optimized += 1
                    
                    saved = (old_cost - new_cost) * (freq / 1000)  # Estimativa de economia
                    self.stats['token_savings'] += saved
                    
                    if optimized <= 10:
                        print(f"      • {word}: {old_symbol}({old_cost:.1f}) → {new_symbol}({new_cost:.1f})")
        
        self.stats['optimized'] = optimized
        print(f"\n   ✅ {optimized} palavras otimizadas")
        print(f"   💰 Economia estimada: {self.stats['token_savings']:,.0f} tokens/1000 palavras")
    
    def load_frequency_data(self):
        """Carrega dados de frequência das palavras"""
        freq_data = []
        
        # Inglês
        en_file = self.resources_path / "en_50k.txt"
        if en_file.exists():
            with open(en_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        freq = int(parts[1]) if parts[1].isdigit() else 1
                        freq_data.append((word, freq))
        
        # Português  
        pt_file = self.resources_path / "pt_50k.txt"
        if pt_file.exists():
            with open(pt_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        freq = int(parts[1]) if parts[1].isdigit() else 1
                        freq_data.append((word, freq))
        
        # Termos de cinema (alta prioridade)
        cinema_terms = [
            'scene', 'cena', 'cut', 'corte', 'action', 'ação',
            'fade', 'character', 'personagem', 'dialogue', 'diálogo',
            'script', 'roteiro', 'director', 'diretor', 'actor', 'ator'
        ]
        
        for term in cinema_terms:
            freq_data.append((term, 1000000))  # Alta frequência artificial
        
        # Ordenar por frequência
        freq_data.sort(key=lambda x: x[1], reverse=True)
        
        return freq_data
    
    def expand_with_efficiency(self):
        """Expande dicionário priorizando eficiência de tokens"""
        print("\n🚀 EXPANDINDO COM EFICIÊNCIA")
        print("="*60)
        
        freq_words = self.load_frequency_data()
        
        added = 0
        for word, freq in freq_words:
            if word not in self.dictionary:
                # Encontrar próximo símbolo eficiente
                for symbol in self.symbol_priority:
                    if symbol not in self.used_symbols:
                        self.dictionary[word] = symbol
                        self.used_symbols.add(symbol)
                        added += 1
                        break
                
                if added >= 20000:  # Limitar expansão
                    break
        
        self.stats['expanded'] = added
        print(f"   ✅ {added} palavras adicionadas com símbolos eficientes")
    
    def calculate_compression_ratio(self):
        """Calcula taxa de compressão real considerando tokens"""
        print("\n📊 ANÁLISE DE COMPRESSÃO")
        print("="*60)
        
        # Texto de exemplo
        sample_texts = [
            "The scene opens with a close-up of the protagonist",
            "A cena abre com um close-up do protagonista",
            "FADE IN: INT. HOUSE - DAY",
            "CUT TO: EXT. STREET - NIGHT"
        ]
        
        for text in sample_texts:
            # Original
            original_tokens = self.estimate_token_cost(text)
            
            # Comprimido
            compressed = []
            for word in text.lower().split():
                clean = re.sub(r'[^\w]', '', word)
                if clean in self.dictionary:
                    compressed.append(self.dictionary[clean])
                else:
                    compressed.append(clean)
            
            compressed_text = ' '.join(compressed)
            compressed_tokens = self.estimate_token_cost(compressed_text)
            
            ratio = (1 - compressed_tokens/original_tokens) * 100
            
            print(f"\n   📝 '{text[:30]}...'")
            print(f"      • Original: {original_tokens:.0f} tokens")
            print(f"      • Comprimido: {compressed_tokens:.0f} tokens")
            print(f"      • Economia: {ratio:.1f}%")
    
    def save_optimized_dictionary(self):
        """Salva dicionário otimizado para tokens"""
        print("\n💾 SALVANDO DICIONÁRIO OTIMIZADO")
        print("="*60)
        
        # Estatísticas
        total_words = len(self.dictionary)
        unique_symbols = len(self.used_symbols)
        
        # Calcular distribuição de tipos de símbolo
        symbol_types = Counter()
        for symbol in self.dictionary.values():
            if symbol in self.used_symbols:
                code = ord(symbol[0]) if symbol else 0
                if code < 128:
                    symbol_types['ASCII'] += 1
                elif code < 256:
                    symbol_types['Latin'] += 1
                elif 0x4E00 <= code <= 0x9FFF:
                    symbol_types['CJK'] += 1
                elif 0x1F300 <= code <= 0x1F9FF:
                    symbol_types['Emoji'] += 1
                else:
                    symbol_types['Other'] += 1
        
        print(f"   📊 Total: {total_words:,} palavras")
        print(f"   📊 Símbolos únicos: {unique_symbols:,}")
        print(f"\n   📊 Distribuição (eficiência de tokens):")
        for type_name, count in symbol_types.most_common():
            print(f"      • {type_name}: {count:,} ({count/total_words*100:.1f}%)")
        
        # Metadata
        self.metadata['version'] = 'TOKEN-OPTIMIZED-v1.0'
        self.metadata['total_words'] = total_words
        self.metadata['unique_symbols'] = unique_symbols
        self.metadata['optimization'] = {
            'prioritizes_token_efficiency': True,
            'words_optimized': self.stats['optimized'],
            'estimated_savings': f"{self.stats['token_savings']:.0f} tokens/1000 words",
            'symbol_distribution': dict(symbol_types)
        }
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
        
        print(f"\n   ✅ Salvo: {self.dict_path}")

def main():
    optimizer = TokenOptimizedDigiLang()
    
    # 1. Otimizar dicionário existente
    optimizer.optimize_existing_dictionary()
    
    # 2. Expandir com eficiência
    optimizer.expand_with_efficiency()
    
    # 3. Calcular compressão real
    optimizer.calculate_compression_ratio()
    
    # 4. Salvar
    optimizer.save_optimized_dictionary()
    
    print("\n" + "="*60)
    print("💰 DIGILANG TOKEN-OPTIMIZED COMPLETA!")
    print("="*60)
    print(f"""
OTIMIZAÇÃO FOCADA EM ECONOMIA DE TOKENS!

📊 RESULTADOS:
   • Palavras otimizadas: {optimizer.stats['optimized']:,}
   • Palavras expandidas: {optimizer.stats['expanded']:,}
   • Economia estimada: {optimizer.stats['token_savings']:,.0f} tokens/1000 palavras

💡 ESTRATÉGIA:
   • ASCII/Latin para palavras frequentes (1 token)
   • CJK para palavras médias (1-2 tokens)
   • Evitar emoji (2-4 tokens)

✅ Ideal para uso com Scripturemon e LLMs!
""")

if __name__ == "__main__":
    main()