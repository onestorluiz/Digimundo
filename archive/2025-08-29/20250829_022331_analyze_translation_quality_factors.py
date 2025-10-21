#!/usr/bin/env python3
"""
🔬 Análise dos Fatores de Qualidade de Tradução DigiLang
Explora elementos além da coerência que impactam a qualidade
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
import re

class TranslationQualityAnalyzer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        # Carregar dicionário
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.dictionary = data.get('symbols', {})
            self.metadata = data
        
        # Inverter para análise
        self.symbol_to_words = defaultdict(list)
        for word, symbol in self.dictionary.items():
            self.symbol_to_words[symbol].append(word)
    
    def analyze_semantic_clustering(self):
        """Analisa agrupamento semântico - palavras relacionadas usando símbolos similares"""
        print("\n🧠 FATOR 1: AGRUPAMENTO SEMÂNTICO")
        print("="*60)
        print("Palavras relacionadas deveriam usar símbolos visualmente similares")
        print("para facilitar compreensão e memorização.\n")
        
        # Grupos semânticos que deveriam ter símbolos relacionados
        semantic_groups = {
            'Família': ['father', 'mother', 'son', 'daughter', 'brother', 'sister', 
                       'pai', 'mãe', 'filho', 'filha', 'irmão', 'irmã'],
            
            'Emoções': ['happy', 'sad', 'angry', 'fear', 'love', 'hate',
                       'feliz', 'triste', 'bravo', 'medo', 'amor', 'ódio'],
            
            'Cores': ['red', 'blue', 'green', 'yellow', 'black', 'white',
                     'vermelho', 'azul', 'verde', 'amarelo', 'preto', 'branco'],
            
            'Números': ['one', 'two', 'three', 'four', 'five',
                       'um', 'dois', 'três', 'quatro', 'cinco'],
            
            'Tempo': ['yesterday', 'today', 'tomorrow', 'now', 'then',
                     'ontem', 'hoje', 'amanhã', 'agora', 'então'],
            
            'Movimento': ['walk', 'run', 'jump', 'fly', 'swim',
                         'andar', 'correr', 'pular', 'voar', 'nadar'],
            
            'Cinema': ['scene', 'cut', 'fade', 'action', 'camera',
                      'cena', 'corte', 'fade', 'ação', 'câmera']
        }
        
        clustering_score = 0
        total_groups = len(semantic_groups)
        
        for group_name, words in semantic_groups.items():
            symbols = []
            for word in words:
                if word in self.dictionary:
                    symbols.append(self.dictionary[word])
            
            # Analisar se símbolos são visualmente relacionados
            if symbols:
                # Verificar se usam mesmo range Unicode (emoji, CJK, etc)
                ranges = self.categorize_symbols(symbols)
                most_common_range = max(ranges.values())
                consistency = most_common_range / len(symbols) if symbols else 0
                
                clustering_score += consistency
                
                print(f"   {group_name}:")
                print(f"      • Consistência visual: {consistency*100:.1f}%")
                if consistency < 0.5:
                    print(f"      ⚠️ Grupo disperso - símbolos não relacionados visualmente")
                else:
                    print(f"      ✅ Boa coesão visual")
        
        final_score = (clustering_score / total_groups) * 100 if total_groups > 0 else 0
        print(f"\n   📊 Score de Agrupamento Semântico: {final_score:.1f}%")
        
        return final_score
    
    def categorize_symbols(self, symbols):
        """Categoriza símbolos por range Unicode"""
        ranges = defaultdict(int)
        for symbol in symbols:
            if len(symbol) == 1:
                code = ord(symbol)
                if 0x1F300 <= code <= 0x1F9FF:
                    ranges['emoji'] += 1
                elif 0x4E00 <= code <= 0x9FFF:
                    ranges['cjk'] += 1
                elif 0xAC00 <= code <= 0xD7AF:
                    ranges['hangul'] += 1
                elif 0x2190 <= code <= 0x27BF:
                    ranges['symbols'] += 1
                else:
                    ranges['other'] += 1
        return ranges
    
    def analyze_morphological_patterns(self):
        """Analisa padrões morfológicos - preservação de estrutura"""
        print("\n📐 FATOR 2: PADRÕES MORFOLÓGICOS")
        print("="*60)
        print("Preservação de padrões gramaticais (plural, tempo verbal, etc)\n")
        
        patterns_preserved = 0
        patterns_broken = 0
        
        # Padrões a verificar
        patterns = {
            'Plural EN (-s)': [
                ('book', 'books'),
                ('car', 'cars'),
                ('house', 'houses'),
                ('tree', 'trees')
            ],
            'Plural PT (-s)': [
                ('livro', 'livros'),
                ('carro', 'carros'),
                ('casa', 'casas'),
                ('árvore', 'árvores')
            ],
            'Past EN (-ed)': [
                ('walk', 'walked'),
                ('talk', 'talked'),
                ('play', 'played')
            ],
            'Gerund EN (-ing)': [
                ('walk', 'walking'),
                ('run', 'running'),
                ('eat', 'eating')
            ],
            'Infinitive PT (-ar/-er/-ir)': [
                ('andar', 'andando'),
                ('comer', 'comendo'),
                ('dormir', 'dormindo')
            ]
        }
        
        for pattern_name, pairs in patterns.items():
            preserved = 0
            total = 0
            
            for base, derived in pairs:
                if base in self.dictionary and derived in self.dictionary:
                    base_sym = self.dictionary[base]
                    derived_sym = self.dictionary[derived]
                    
                    # Verificar se há alguma relação visual/estrutural
                    if self.symbols_related(base_sym, derived_sym):
                        preserved += 1
                        patterns_preserved += 1
                    else:
                        patterns_broken += 1
                    total += 1
            
            if total > 0:
                preservation_rate = (preserved / total) * 100
                print(f"   {pattern_name}: {preservation_rate:.1f}% preservado")
                if preservation_rate < 50:
                    print(f"      ⚠️ Padrão morfológico perdido")
        
        total_patterns = patterns_preserved + patterns_broken
        morphology_score = (patterns_preserved / total_patterns * 100) if total_patterns > 0 else 0
        
        print(f"\n   📊 Score de Preservação Morfológica: {morphology_score:.1f}%")
        
        return morphology_score
    
    def symbols_related(self, sym1, sym2):
        """Verifica se dois símbolos têm alguma relação visual"""
        if len(sym1) == 1 and len(sym2) == 1:
            code1, code2 = ord(sym1), ord(sym2)
            # Considerar relacionados se próximos no Unicode
            return abs(code1 - code2) < 10
        return False
    
    def analyze_contextual_disambiguation(self):
        """Analisa disambiguação contextual"""
        print("\n🎯 FATOR 3: DISAMBIGUAÇÃO CONTEXTUAL")
        print("="*60)
        print("Capacidade de distinguir significados pelo contexto\n")
        
        # Palavras que precisam contexto
        context_dependent = {
            'bank': {
                'financial': 'I need to go to the bank to withdraw money',
                'river': 'We sat on the river bank to fish'
            },
            'light': {
                'illumination': 'Turn on the light',
                'weight': 'This bag is very light'
            },
            'right': {
                'correct': 'You are right about that',
                'direction': 'Turn right at the corner',
                'entitlement': 'You have the right to remain silent'
            },
            'play': {
                'game': 'Let us play chess',
                'theater': 'We saw a play at the theater',
                'music': 'She can play the piano'
            }
        }
        
        disambiguation_needed = len(context_dependent)
        disambiguation_possible = 0
        
        for word, contexts in context_dependent.items():
            if word in self.dictionary:
                symbol = self.dictionary[word]
                # Verificar se existem variantes contextuais
                variants = self.find_contextual_variants(word)
                
                if len(variants) > 1:
                    disambiguation_possible += 1
                    print(f"   ✅ '{word}' tem {len(variants)} variantes contextuais")
                else:
                    print(f"   ⚠️ '{word}' usa símbolo único '{symbol}' para todos contextos")
        
        disambiguation_score = (disambiguation_possible / disambiguation_needed * 100) if disambiguation_needed > 0 else 0
        
        print(f"\n   📊 Score de Disambiguação: {disambiguation_score:.1f}%")
        
        return disambiguation_score
    
    def find_contextual_variants(self, word):
        """Busca variantes contextuais de uma palavra"""
        variants = []
        base = word.lower()
        
        # Buscar variações com prefixos/sufixos contextuais
        for w in self.dictionary:
            if base in w and w != base:
                # Potencial variante contextual
                if w.startswith(base) or w.endswith(base):
                    variants.append(w)
        
        return variants
    
    def analyze_frequency_optimization(self):
        """Analisa otimização por frequência"""
        print("\n⚡ FATOR 4: OTIMIZAÇÃO POR FREQUÊNCIA")
        print("="*60)
        print("Palavras mais frequentes deveriam ter símbolos mais simples\n")
        
        # Palavras mais frequentes em inglês (top 100)
        high_freq_en = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                       'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
                       'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
                       'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what']
        
        # Palavras mais frequentes em português (top 100)
        high_freq_pt = ['o', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com',
                       'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos',
                       'como', 'mas', 'ao', 'ele', 'das', 'à', 'seu', 'sua', 'ou', 'quando',
                       'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso']
        
        simple_symbols = 0
        complex_symbols = 0
        
        all_freq_words = high_freq_en[:20] + high_freq_pt[:20]
        
        for word in all_freq_words:
            if word in self.dictionary:
                symbol = self.dictionary[word]
                if len(symbol) == 1:
                    code = ord(symbol)
                    # Símbolos simples: emoji comum, ou caracteres básicos
                    if (0x1F300 <= code <= 0x1F5FF) or (0x2600 <= code <= 0x26FF):
                        simple_symbols += 1
                    else:
                        complex_symbols += 1
        
        optimization_score = (simple_symbols / (simple_symbols + complex_symbols) * 100) if (simple_symbols + complex_symbols) > 0 else 0
        
        print(f"   📊 Palavras frequentes com símbolos simples: {simple_symbols}")
        print(f"   📊 Palavras frequentes com símbolos complexos: {complex_symbols}")
        print(f"\n   📊 Score de Otimização por Frequência: {optimization_score:.1f}%")
        
        return optimization_score
    
    def analyze_visual_mnemonics(self):
        """Analisa mnemônicos visuais"""
        print("\n🎨 FATOR 5: MNEMÔNICOS VISUAIS")
        print("="*60)
        print("Símbolos que se parecem com seu significado\n")
        
        # Palavras que poderiam ter símbolos mnemônicos
        mnemonic_candidates = {
            'sun': '☀️',
            'star': '⭐',
            'heart': '❤️',
            'tree': '🌳',
            'water': '💧',
            'fire': '🔥',
            'moon': '🌙',
            'cloud': '☁️',
            'mountain': '⛰️',
            'house': '🏠',
            'book': '📚',
            'music': '🎵',
            'phone': '📱',
            'car': '🚗',
            'airplane': '✈️',
            'smile': '😊',
            'cry': '😢',
            'sleep': '😴',
            'eat': '🍽️',
            'drink': '🥤'
        }
        
        mnemonic_matches = 0
        total_candidates = 0
        
        for word, ideal_symbol in mnemonic_candidates.items():
            if word in self.dictionary:
                actual_symbol = self.dictionary[word]
                total_candidates += 1
                
                # Verificar se o símbolo é visualmente relacionado
                if self.is_visual_mnemonic(actual_symbol, word):
                    mnemonic_matches += 1
                    print(f"   ✅ '{word}' → '{actual_symbol}' (mnemônico)")
                elif total_candidates <= 10:
                    print(f"   ❌ '{word}' → '{actual_symbol}' (não mnemônico)")
        
        mnemonic_score = (mnemonic_matches / total_candidates * 100) if total_candidates > 0 else 0
        
        print(f"\n   📊 Score de Mnemônicos Visuais: {mnemonic_score:.1f}%")
        
        return mnemonic_score
    
    def is_visual_mnemonic(self, symbol, word):
        """Verifica se símbolo é mnemônico para a palavra"""
        if len(symbol) == 1:
            code = ord(symbol)
            # Emoji são geralmente mnemônicos
            if 0x1F300 <= code <= 0x1F9FF:
                return True
            # Símbolos pictográficos
            if 0x2600 <= code <= 0x26FF:
                return True
        return False
    
    def analyze_compression_efficiency(self):
        """Analisa eficiência de compressão"""
        print("\n📦 FATOR 6: EFICIÊNCIA DE COMPRESSÃO")
        print("="*60)
        print("Razão entre texto original e texto comprimido\n")
        
        # Texto de exemplo
        test_texts = [
            "The quick brown fox jumps over the lazy dog",
            "O rápido cão marrom pula sobre a raposa preguiçosa",
            "In the beginning, God created the heavens and the earth",
            "No princípio, Deus criou os céus e a terra",
            "To be or not to be, that is the question",
            "Ser ou não ser, eis a questão"
        ]
        
        total_original = 0
        total_compressed = 0
        
        for text in test_texts:
            words = text.lower().split()
            original_length = len(text)
            compressed_length = 0
            
            for word in words:
                clean_word = re.sub(r'[^\w\s]', '', word)
                if clean_word in self.dictionary:
                    compressed_length += 1  # 1 símbolo por palavra
                else:
                    compressed_length += len(clean_word)  # Não comprimido
            
            total_original += original_length
            total_compressed += compressed_length
            
            compression_rate = (1 - compressed_length/original_length) * 100
            print(f"   • '{text[:30]}...': {compression_rate:.1f}% compressão")
        
        overall_compression = (1 - total_compressed/total_original) * 100
        
        print(f"\n   📊 Taxa de Compressão Média: {overall_compression:.1f}%")
        
        return overall_compression
    
    def generate_improvement_roadmap(self):
        """Gera roadmap de melhorias"""
        print("\n" + "="*60)
        print("🗺️ ROADMAP DE MELHORIAS PARA DIGILANG")
        print("="*60)
        
        improvements = {
            '🥇 PRIORIDADE ALTA': [
                {
                    'nome': 'Agrupamento Semântico Visual',
                    'descrição': 'Reorganizar símbolos para que palavras relacionadas usem símbolos similares',
                    'impacto': 'Facilita aprendizado e memorização',
                    'exemplo': 'Família: 👨 pai, 👩 mãe, 👦 filho, 👧 filha'
                },
                {
                    'nome': 'Mnemônicos Visuais',
                    'descrição': 'Usar emoji/símbolos que se parecem com significado',
                    'impacto': 'Compreensão intuitiva',
                    'exemplo': 'sun → ☀️, water → 💧, tree → 🌳'
                }
            ],
            '🥈 PRIORIDADE MÉDIA': [
                {
                    'nome': 'Otimização por Frequência',
                    'descrição': 'Atribuir símbolos simples às palavras mais comuns',
                    'impacto': 'Melhora velocidade de leitura',
                    'exemplo': 'the → ⬤, de → ⬡, que → ⬢'
                },
                {
                    'nome': 'Padrões Morfológicos',
                    'descrição': 'Criar sistema de modificadores para plural/tempo verbal',
                    'impacto': 'Preserva estrutura gramatical',
                    'exemplo': 'book → 📖, books → 📖+'
                }
            ],
            '🥉 PRIORIDADE BAIXA': [
                {
                    'nome': 'Variantes Contextuais',
                    'descrição': 'Adicionar prefixos/sufixos para disambiguação',
                    'impacto': 'Maior precisão em textos técnicos',
                    'exemplo': 'bank₁ (financeiro), bank₂ (margem)'
                }
            ]
        }
        
        for priority, items in improvements.items():
            print(f"\n{priority}")
            print("-"*40)
            for item in items:
                print(f"\n📌 {item['nome']}")
                print(f"   📝 {item['descrição']}")
                print(f"   💡 Impacto: {item['impacto']}")
                print(f"   🔍 Exemplo: {item['exemplo']}")
        
        return improvements
    
    def calculate_overall_quality(self, scores):
        """Calcula qualidade geral da tradução"""
        weights = {
            'coherence': 0.25,      # 25% - já temos 84.2%
            'semantic': 0.20,       # 20% - agrupamento semântico
            'mnemonic': 0.15,       # 15% - mnemônicos visuais
            'frequency': 0.15,      # 15% - otimização por frequência
            'compression': 0.10,    # 10% - eficiência de compressão
            'morphology': 0.10,     # 10% - padrões morfológicos
            'disambiguation': 0.05  # 5% - disambiguação contextual
        }
        
        weighted_score = (
            84.2 * weights['coherence'] +
            scores['semantic'] * weights['semantic'] +
            scores['mnemonic'] * weights['mnemonic'] +
            scores['frequency'] * weights['frequency'] +
            scores['compression'] * weights['compression'] +
            scores['morphology'] * weights['morphology'] +
            scores['disambiguation'] * weights['disambiguation']
        )
        
        return weighted_score

def main():
    print("╔" + "═"*58 + "╗")
    print("║  🔬 ANÁLISE DE FATORES DE QUALIDADE DE TRADUÇÃO       ║")
    print("╚" + "═"*58 + "╝")
    
    analyzer = TranslationQualityAnalyzer()
    
    # Executar análises
    scores = {
        'semantic': analyzer.analyze_semantic_clustering(),
        'morphology': analyzer.analyze_morphological_patterns(),
        'disambiguation': analyzer.analyze_contextual_disambiguation(),
        'frequency': analyzer.analyze_frequency_optimization(),
        'mnemonic': analyzer.analyze_visual_mnemonics(),
        'compression': analyzer.analyze_compression_efficiency()
    }
    
    # Gerar roadmap
    improvements = analyzer.generate_improvement_roadmap()
    
    # Calcular qualidade geral
    overall_quality = analyzer.calculate_overall_quality(scores)
    
    print("\n" + "="*60)
    print("📊 ANÁLISE FINAL DE QUALIDADE")
    print("="*60)
    
    print(f"""
🎯 SCORES INDIVIDUAIS:
   • Coerência PT/EN: 84.2% ✅
   • Agrupamento Semântico: {scores['semantic']:.1f}%
   • Padrões Morfológicos: {scores['morphology']:.1f}%
   • Disambiguação: {scores['disambiguation']:.1f}%
   • Otimização Frequência: {scores['frequency']:.1f}%
   • Mnemônicos Visuais: {scores['mnemonic']:.1f}%
   • Compressão: {scores['compression']:.1f}%

📈 QUALIDADE GERAL: {overall_quality:.1f}%

💡 INSIGHTS PRINCIPAIS:
   1. Coerência bilíngue está EXCELENTE (84.2%)
   2. Maior oportunidade: Agrupamento Semântico e Mnemônicos
   3. Compressão eficiente mas pode melhorar
   4. Padrões morfológicos precisam atenção

🚀 PRÓXIMOS PASSOS:
   1. Implementar agrupamento semântico visual
   2. Adicionar mnemônicos visuais onde possível
   3. Otimizar símbolos por frequência de uso
   4. DEPOIS disso, aumentar coerência para ~90%
""")
    
    # Salvar relatório
    report = {
        'scores': scores,
        'overall_quality': overall_quality,
        'improvements': {k: [item['nome'] for item in v] for k, v in improvements.items()}
    }
    
    report_path = analyzer.base_path / "translation_quality_analysis.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Análise salva: {report_path}")
    
    return scores, overall_quality

if __name__ == "__main__":
    main()