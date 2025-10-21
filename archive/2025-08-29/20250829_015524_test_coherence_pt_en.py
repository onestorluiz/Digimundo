#!/usr/bin/env python3
"""
🧪 Teste de Coerência Bilíngue DigiLang
Verifica se palavras equivalentes PT/EN usam o mesmo símbolo
"""

import json
from pathlib import Path
from datetime import datetime
from googletrans import Translator
import time

class DigiLangCoherenceTest:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        # Carregar dicionário
        self.load_dictionary()
        
        # Tradutor
        self.translator = Translator()
        
        # Pares conhecidos PT/EN que devem ter mesmo símbolo
        self.known_pairs = {
            # Conceitos básicos
            'life': 'vida',
            'death': 'morte',
            'love': 'amor',
            'hate': 'ódio',
            'peace': 'paz',
            'war': 'guerra',
            'time': 'tempo',
            'space': 'espaço',
            'light': 'luz',
            'dark': 'escuro',
            'water': 'água',
            'fire': 'fogo',
            'earth': 'terra',
            'air': 'ar',
            'soul': 'alma',
            'body': 'corpo',
            'mind': 'mente',
            'heart': 'coração',
            'spirit': 'espírito',
            'god': 'deus',
            
            # Ações comuns
            'walk': 'andar',
            'run': 'correr',
            'eat': 'comer',
            'drink': 'beber',
            'sleep': 'dormir',
            'wake': 'acordar',
            'speak': 'falar',
            'listen': 'ouvir',
            'see': 'ver',
            'feel': 'sentir',
            'think': 'pensar',
            'know': 'saber',
            'understand': 'entender',
            'create': 'criar',
            'destroy': 'destruir',
            'build': 'construir',
            'break': 'quebrar',
            'open': 'abrir',
            'close': 'fechar',
            'begin': 'começar',
            
            # Objetos
            'house': 'casa',
            'door': 'porta',
            'window': 'janela',
            'table': 'mesa',
            'chair': 'cadeira',
            'book': 'livro',
            'computer': 'computador',
            'phone': 'telefone',
            'car': 'carro',
            'tree': 'árvore',
            'flower': 'flor',
            'sun': 'sol',
            'moon': 'lua',
            'star': 'estrela',
            'cloud': 'nuvem',
            'mountain': 'montanha',
            'river': 'rio',
            'sea': 'mar',
            'ocean': 'oceano',
            'forest': 'floresta',
            
            # Adjetivos
            'big': 'grande',
            'small': 'pequeno',
            'good': 'bom',
            'bad': 'mau',
            'new': 'novo',
            'old': 'velho',
            'young': 'jovem',
            'beautiful': 'belo',
            'ugly': 'feio',
            'happy': 'feliz',
            'sad': 'triste',
            'angry': 'bravo',
            'calm': 'calmo',
            'hot': 'quente',
            'cold': 'frio',
            'fast': 'rápido',
            'slow': 'lento',
            'strong': 'forte',
            'weak': 'fraco',
            'rich': 'rico',
            
            # Números
            'one': 'um',
            'two': 'dois',
            'three': 'três',
            'four': 'quatro',
            'five': 'cinco',
            'six': 'seis',
            'seven': 'sete',
            'eight': 'oito',
            'nine': 'nove',
            'ten': 'dez',
            
            # Cores
            'red': 'vermelho',
            'blue': 'azul',
            'green': 'verde',
            'yellow': 'amarelo',
            'black': 'preto',
            'white': 'branco',
            'gray': 'cinza',
            'orange': 'laranja',
            'purple': 'roxo',
            'pink': 'rosa'
        }
        
    def load_dictionary(self):
        """Carrega dicionário DigiLang"""
        print("📚 Carregando dicionário DigiLang...")
        
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.dictionary = data.get('symbols', {})
            self.metadata = data
            
        print(f"   ✅ {len(self.dictionary)} palavras carregadas")
        
    def test_known_pairs(self):
        """Testa pares conhecidos PT/EN"""
        print("\n🧪 TESTE 1: PARES CONHECIDOS PT/EN")
        print("="*60)
        
        correct = 0
        incorrect = []
        missing = []
        
        for en_word, pt_word in self.known_pairs.items():
            en_symbol = self.dictionary.get(en_word, None)
            pt_symbol = self.dictionary.get(pt_word, None)
            
            if not en_symbol:
                missing.append(f"EN: {en_word}")
                continue
            if not pt_symbol:
                missing.append(f"PT: {pt_word}")
                continue
                
            if en_symbol == pt_symbol:
                correct += 1
                print(f"   ✅ {en_word}/{pt_word} → {en_symbol}")
            else:
                incorrect.append({
                    'en': en_word,
                    'pt': pt_word,
                    'en_symbol': en_symbol,
                    'pt_symbol': pt_symbol
                })
                print(f"   ❌ {en_word} → {en_symbol} | {pt_word} → {pt_symbol}")
        
        print(f"\n📊 Resultados:")
        print(f"   • Corretos: {correct}/{len(self.known_pairs)} ({correct/len(self.known_pairs)*100:.1f}%)")
        print(f"   • Incorretos: {len(incorrect)}")
        print(f"   • Não encontrados: {len(missing)}")
        
        return correct, incorrect, missing
    
    def test_symbol_uniqueness(self):
        """Testa unicidade dos símbolos"""
        print("\n🧪 TESTE 2: UNICIDADE DOS SÍMBOLOS")
        print("="*60)
        
        # Inverter dicionário
        symbol_to_words = {}
        for word, symbol in self.dictionary.items():
            if symbol not in symbol_to_words:
                symbol_to_words[symbol] = []
            symbol_to_words[symbol].append(word)
        
        # Verificar símbolos com múltiplas palavras
        multi_word_symbols = []
        conceptual_matches = []
        
        for symbol, words in symbol_to_words.items():
            if len(words) > 1:
                multi_word_symbols.append((symbol, words))
                
                # Verificar se são conceitos equivalentes
                if self.are_equivalent_concepts(words):
                    conceptual_matches.append((symbol, words))
        
        print(f"   📊 Total de símbolos: {len(symbol_to_words)}")
        print(f"   📊 Símbolos únicos (1 palavra): {len([s for s in symbol_to_words if len(symbol_to_words[s]) == 1])}")
        print(f"   📊 Símbolos compartilhados: {len(multi_word_symbols)}")
        print(f"   📊 Conceitos unificados corretamente: {len(conceptual_matches)}")
        
        # Mostrar exemplos
        print(f"\n   Exemplos de conceitos unificados:")
        for symbol, words in conceptual_matches[:10]:
            print(f"      {symbol} → {', '.join(words)}")
            
        return len(symbol_to_words), len(multi_word_symbols), len(conceptual_matches)
    
    def are_equivalent_concepts(self, words):
        """Verifica se palavras são conceitos equivalentes"""
        # Verificar pares conhecidos
        for en, pt in self.known_pairs.items():
            if en in words and pt in words:
                return True
                
        # Verificar variações (plural, tempos verbais)
        base_forms = set()
        for word in words:
            # Remover sufixos comuns
            base = word
            for suffix in ['s', 'es', 'ed', 'ing', 'er', 'est', 'ly', 'ness', 
                          'ção', 'ções', 'mente', 'ando', 'endo', 'indo']:
                if word.endswith(suffix):
                    base = word[:-len(suffix)]
                    break
            base_forms.add(base)
        
        # Se todas as palavras têm a mesma base, são equivalentes
        return len(base_forms) == 1
    
    def test_translation_consistency(self):
        """Testa consistência de tradução"""
        print("\n🧪 TESTE 3: CONSISTÊNCIA DE TRADUÇÃO")
        print("="*60)
        
        # Testar frases simples
        test_phrases = [
            ("The book is on the table", "O livro está na mesa"),
            ("I love you", "Eu amo você"),
            ("Good morning", "Bom dia"),
            ("Thank you", "Obrigado"),
            ("How are you", "Como está você"),
            ("The sun is shining", "O sol está brilhando"),
            ("Life is beautiful", "A vida é bela"),
            ("Time flies", "O tempo voa"),
            ("Open the door", "Abra a porta"),
            ("Close the window", "Feche a janela")
        ]
        
        consistent = 0
        inconsistent = []
        
        for en_phrase, pt_phrase in test_phrases:
            en_symbols = self.translate_phrase(en_phrase)
            pt_symbols = self.translate_phrase(pt_phrase)
            
            # Comparar palavras principais (substantivos, verbos)
            en_main = self.extract_main_words(en_phrase)
            pt_main = self.extract_main_words(pt_phrase)
            
            match = self.compare_main_symbols(en_main, pt_main)
            
            if match:
                consistent += 1
                print(f"   ✅ Consistente: {en_phrase[:30]}")
            else:
                inconsistent.append((en_phrase, pt_phrase))
                print(f"   ❌ Inconsistente: {en_phrase[:30]}")
        
        print(f"\n📊 Resultados:")
        print(f"   • Frases consistentes: {consistent}/{len(test_phrases)}")
        print(f"   • Taxa de consistência: {consistent/len(test_phrases)*100:.1f}%")
        
        return consistent, inconsistent
    
    def translate_phrase(self, phrase):
        """Traduz frase para símbolos DigiLang"""
        words = phrase.lower().split()
        symbols = []
        
        for word in words:
            # Limpar pontuação
            clean_word = word.strip('.,!?;:')
            symbol = self.dictionary.get(clean_word, '?')
            symbols.append(symbol)
            
        return symbols
    
    def extract_main_words(self, phrase):
        """Extrai palavras principais da frase"""
        # Palavras comuns a ignorar
        stop_words = {'the', 'a', 'an', 'is', 'are', 'on', 'in', 'at', 
                     'o', 'a', 'um', 'uma', 'está', 'estão', 'na', 'no', 'em'}
        
        words = phrase.lower().split()
        main_words = []
        
        for word in words:
            clean = word.strip('.,!?;:')
            if clean not in stop_words:
                main_words.append(clean)
                
        return main_words
    
    def compare_main_symbols(self, en_words, pt_words):
        """Compara símbolos das palavras principais"""
        # Simplificado: verificar se pelo menos metade coincide
        matches = 0
        total = min(len(en_words), len(pt_words))
        
        for en_word in en_words:
            en_symbol = self.dictionary.get(en_word)
            for pt_word in pt_words:
                pt_symbol = self.dictionary.get(pt_word)
                if en_symbol and pt_symbol and en_symbol == pt_symbol:
                    matches += 1
                    break
                    
        return matches >= total / 2
    
    def generate_report(self, results):
        """Gera relatório de testes"""
        print("\n" + "="*60)
        print("📄 RELATÓRIO FINAL DE COERÊNCIA")
        print("="*60)
        
        report_path = self.base_path / f"coherence_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report = f"""# 🧪 Relatório de Coerência DigiLang PT/EN

## 📅 Informações
- **Data**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Versão DigiLang**: {self.metadata.get('version', 'unknown')}
- **Total de palavras**: {len(self.dictionary):,}

## ✅ Teste 1: Pares Conhecidos PT/EN
- **Pares testados**: {len(self.known_pairs)}
- **Corretos**: {results['known_pairs'][0]} ({results['known_pairs'][0]/len(self.known_pairs)*100:.1f}%)
- **Incorretos**: {len(results['known_pairs'][1])}
- **Não encontrados**: {len(results['known_pairs'][2])}

## ✅ Teste 2: Unicidade dos Símbolos
- **Total de símbolos**: {results['uniqueness'][0]:,}
- **Símbolos compartilhados**: {results['uniqueness'][1]}
- **Conceitos unificados**: {results['uniqueness'][2]}

## ✅ Teste 3: Consistência de Tradução
- **Frases testadas**: 10
- **Consistentes**: {results['translation'][0]}
- **Taxa de consistência**: {results['translation'][0]/10*100:.1f}%

## 🎯 Conclusão
"""
        
        if results['known_pairs'][0] / len(self.known_pairs) > 0.8:
            report += "✅ **ALTA COERÊNCIA**: O sistema mantém consistência entre PT/EN acima de 80%\n"
        elif results['known_pairs'][0] / len(self.known_pairs) > 0.6:
            report += "⚠️ **COERÊNCIA MÉDIA**: O sistema tem consistência moderada entre PT/EN\n"
        else:
            report += "❌ **BAIXA COERÊNCIA**: O sistema precisa de ajustes na unificação PT/EN\n"
            
        report += f"""
## 📊 Detalhes dos Erros

### Pares Incorretos
"""
        
        for error in results['known_pairs'][1][:20]:
            report += f"- {error['en']}/{error['pt']}: {error['en_symbol']} ≠ {error['pt_symbol']}\n"
            
        report += """

---
*Teste automático de coerência bilíngue DigiLang*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"   📄 Relatório salvo: {report_path}")
        
        return report_path

def main():
    print("╔" + "═"*58 + "╗")
    print("║     🧪 TESTE DE COERÊNCIA DIGILANG PT/EN               ║")
    print("╚" + "═"*58 + "╝")
    
    tester = DigiLangCoherenceTest()
    
    results = {
        'known_pairs': tester.test_known_pairs(),
        'uniqueness': tester.test_symbol_uniqueness(),
        'translation': tester.test_translation_consistency()
    }
    
    # Gerar relatório
    report_path = tester.generate_report(results)
    
    print("\n✨ TESTES CONCLUÍDOS!")
    print(f"📊 Coerência geral: {results['known_pairs'][0]/len(tester.known_pairs)*100:.1f}%")
    
    if results['known_pairs'][0] / len(tester.known_pairs) >= 0.8:
        print("✅ Sistema DigiLang tem ALTA coerência bilíngue!")
    else:
        print("⚠️ Sistema precisa de ajustes para melhorar coerência PT/EN")
    
    return results

if __name__ == "__main__":
    main()