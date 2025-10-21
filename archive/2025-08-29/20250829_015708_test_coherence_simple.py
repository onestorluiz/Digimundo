#!/usr/bin/env python3
"""
🧪 Teste de Coerência Bilíngue DigiLang (Versão Simples)
Verifica se palavras equivalentes PT/EN usam o mesmo símbolo
"""

import json
from pathlib import Path
from datetime import datetime

class DigiLangCoherenceTest:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        # Carregar dicionário
        self.load_dictionary()
        
        # Pares conhecidos PT/EN que devem ter mesmo símbolo
        self.known_pairs = {
            # Conceitos básicos
            'life': 'vida',
            'death': 'morte', 
            'love': 'amor',
            'hate': 'odio',
            'peace': 'paz',
            'war': 'guerra',
            'time': 'tempo',
            'space': 'espaco',
            'light': 'luz',
            'dark': 'escuro',
            'water': 'agua',
            'fire': 'fogo',
            'earth': 'terra',
            'air': 'ar',
            'soul': 'alma',
            'body': 'corpo',
            'mind': 'mente',
            'heart': 'coracao',
            'spirit': 'espirito',
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
            'begin': 'comecar',
            
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
            'tree': 'arvore',
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
            'fast': 'rapido',
            'slow': 'lento',
            'strong': 'forte',
            'weak': 'fraco',
            'rich': 'rico',
            
            # Números
            'one': 'um',
            'two': 'dois',
            'three': 'tres',
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
            'pink': 'rosa',
            
            # Termos técnicos de cinema
            'scene': 'cena',
            'character': 'personagem',
            'story': 'historia',
            'plot': 'trama',
            'script': 'roteiro',
            'movie': 'filme',
            'film': 'filme',
            'action': 'acao',
            'drama': 'drama',
            'comedy': 'comedia',
            'hero': 'heroi',
            'villain': 'vilao',
            'protagonist': 'protagonista',
            'antagonist': 'antagonista',
            'conflict': 'conflito',
            'resolution': 'resolucao',
            'beginning': 'inicio',
            'middle': 'meio',
            'end': 'fim',
            'dialogue': 'dialogo'
        }
        
    def load_dictionary(self):
        """Carrega dicionário DigiLang"""
        print("📚 Carregando dicionário DigiLang...")
        
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.dictionary = data.get('symbols', {})
            self.metadata = data
            
        print(f"   ✅ {len(self.dictionary):,} palavras carregadas")
        print(f"   📊 Versão: {self.metadata.get('version', 'unknown')}")
        
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
                if correct <= 20:  # Mostrar primeiros 20
                    print(f"   ✅ {en_word}/{pt_word} → {en_symbol}")
            else:
                incorrect.append({
                    'en': en_word,
                    'pt': pt_word,
                    'en_symbol': en_symbol,
                    'pt_symbol': pt_symbol
                })
                if len(incorrect) <= 10:  # Mostrar primeiros 10 erros
                    print(f"   ❌ {en_word} → {en_symbol} | {pt_word} → {pt_symbol}")
        
        print(f"\n📊 Resultados:")
        print(f"   • Corretos: {correct}/{len(self.known_pairs)} ({correct/len(self.known_pairs)*100:.1f}%)")
        print(f"   • Incorretos: {len(incorrect)}")
        print(f"   • Não encontrados: {len(missing)}")
        
        return correct, incorrect, missing
    
    def test_symbol_distribution(self):
        """Testa distribuição dos símbolos"""
        print("\n🧪 TESTE 2: DISTRIBUIÇÃO DE SÍMBOLOS")
        print("="*60)
        
        # Contar tipos de símbolos
        symbol_types = {
            'basic_latin': 0,
            'latin_extended': 0,
            'mathematical': 0,
            'arrows': 0,
            'box_drawing': 0,
            'geometric': 0,
            'miscellaneous': 0,
            'dingbats': 0,
            'cjk': 0,
            'hangul': 0,
            'emoji': 0,
            'other': 0
        }
        
        for symbol in self.dictionary.values():
            if len(symbol) != 1:
                continue
                
            code = ord(symbol)
            
            if 0x0020 <= code <= 0x007F:
                symbol_types['basic_latin'] += 1
            elif 0x0080 <= code <= 0x024F:
                symbol_types['latin_extended'] += 1
            elif 0x2200 <= code <= 0x22FF:
                symbol_types['mathematical'] += 1
            elif 0x2190 <= code <= 0x21FF:
                symbol_types['arrows'] += 1
            elif 0x2500 <= code <= 0x257F:
                symbol_types['box_drawing'] += 1
            elif 0x25A0 <= code <= 0x25FF:
                symbol_types['geometric'] += 1
            elif 0x2600 <= code <= 0x26FF:
                symbol_types['miscellaneous'] += 1
            elif 0x2700 <= code <= 0x27BF:
                symbol_types['dingbats'] += 1
            elif 0x4E00 <= code <= 0x9FFF:
                symbol_types['cjk'] += 1
            elif 0xAC00 <= code <= 0xD7AF:
                symbol_types['hangul'] += 1
            elif 0x1F300 <= code <= 0x1F9FF:
                symbol_types['emoji'] += 1
            else:
                symbol_types['other'] += 1
        
        print("   📊 Distribuição por tipo de símbolo:")
        total = sum(symbol_types.values())
        for stype, count in sorted(symbol_types.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percent = count / total * 100
                print(f"      • {stype}: {count:,} ({percent:.1f}%)")
        
        return symbol_types
    
    def test_symbol_consistency(self):
        """Testa consistência na atribuição de símbolos"""
        print("\n🧪 TESTE 3: CONSISTÊNCIA DE SÍMBOLOS")
        print("="*60)
        
        # Verificar símbolos duplicados
        symbol_to_words = {}
        for word, symbol in self.dictionary.items():
            if symbol not in symbol_to_words:
                symbol_to_words[symbol] = []
            symbol_to_words[symbol].append(word)
        
        # Contar duplicações
        single_use = 0
        multi_use = 0
        max_words_per_symbol = 0
        most_used_symbol = None
        
        for symbol, words in symbol_to_words.items():
            if len(words) == 1:
                single_use += 1
            else:
                multi_use += 1
                if len(words) > max_words_per_symbol:
                    max_words_per_symbol = len(words)
                    most_used_symbol = (symbol, words)
        
        print(f"   📊 Estatísticas de uso:")
        print(f"      • Símbolos únicos (1 palavra): {single_use:,}")
        print(f"      • Símbolos compartilhados: {multi_use:,}")
        print(f"      • Máximo de palavras por símbolo: {max_words_per_symbol}")
        
        if most_used_symbol and max_words_per_symbol <= 10:
            print(f"      • Símbolo mais usado: {most_used_symbol[0]} → {', '.join(most_used_symbol[1])}")
        
        return single_use, multi_use, max_words_per_symbol
    
    def test_coverage_completeness(self):
        """Testa completude da cobertura"""
        print("\n🧪 TESTE 4: COMPLETUDE DA COBERTURA")
        print("="*60)
        
        # Estatísticas gerais
        total_words = len(self.dictionary)
        unique_symbols = len(set(self.dictionary.values()))
        
        # Verificar palavras básicas em inglês
        basic_english = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at']
        
        # Verificar palavras básicas em português
        basic_portuguese = ['o', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com',
                           'nao', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos']
        
        en_covered = sum(1 for w in basic_english if w in self.dictionary)
        pt_covered = sum(1 for w in basic_portuguese if w in self.dictionary)
        
        print(f"   📊 Estatísticas gerais:")
        print(f"      • Total de palavras: {total_words:,}")
        print(f"      • Símbolos únicos: {unique_symbols:,}")
        print(f"      • Razão palavra/símbolo: {total_words/unique_symbols:.2f}")
        
        print(f"\n   📊 Cobertura de palavras básicas:")
        print(f"      • Inglês: {en_covered}/{len(basic_english)} ({en_covered/len(basic_english)*100:.0f}%)")
        print(f"      • Português: {pt_covered}/{len(basic_portuguese)} ({pt_covered/len(basic_portuguese)*100:.0f}%)")
        
        return total_words, unique_symbols, en_covered, pt_covered
    
    def generate_report(self, results):
        """Gera relatório final"""
        print("\n" + "="*60)
        print("📄 RELATÓRIO FINAL DE COERÊNCIA")
        print("="*60)
        
        # Calcular pontuação geral
        score = results['pairs'][0] / len(self.known_pairs) * 100
        
        if score >= 80:
            status = "✅ EXCELENTE"
            message = "Sistema tem alta coerência bilíngue!"
        elif score >= 60:
            status = "⚠️ BOM"
            message = "Sistema tem boa coerência, mas pode melhorar."
        else:
            status = "❌ PRECISA MELHORAR"
            message = "Sistema precisa de ajustes na unificação PT/EN."
        
        print(f"\n   🎯 PONTUAÇÃO GERAL: {score:.1f}%")
        print(f"   📊 STATUS: {status}")
        print(f"   💬 {message}")
        
        # Salvar relatório
        report_path = self.base_path / f"coherence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report = f"""# 🧪 Relatório de Coerência DigiLang PT/EN

## 📅 Informações
- **Data**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Versão DigiLang**: {self.metadata.get('version', 'unknown')}
- **Total de palavras**: {results['coverage'][0]:,}
- **Símbolos únicos**: {results['coverage'][1]:,}

## 🎯 Pontuação Geral: {score:.1f}%
**Status**: {status}

## ✅ Teste 1: Pares PT/EN
- Pares testados: {len(self.known_pairs)}
- Corretos: {results['pairs'][0]} ({results['pairs'][0]/len(self.known_pairs)*100:.1f}%)
- Incorretos: {len(results['pairs'][1])}
- Não encontrados: {len(results['pairs'][2])}

## ✅ Teste 2: Distribuição de Símbolos
"""
        for stype, count in sorted(results['distribution'].items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                report += f"- {stype}: {count:,}\n"
        
        report += f"""

## ✅ Teste 3: Consistência
- Símbolos únicos: {results['consistency'][0]:,}
- Símbolos compartilhados: {results['consistency'][1]:,}
- Máximo palavras/símbolo: {results['consistency'][2]}

## ✅ Teste 4: Cobertura
- Palavras básicas EN: {results['coverage'][2]}/20 ({results['coverage'][2]*5}%)
- Palavras básicas PT: {results['coverage'][3]}/20 ({results['coverage'][3]*5}%)

## 📊 Conclusão
{message}

---
*Relatório gerado automaticamente*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n   📄 Relatório salvo: {report_path}")
        
        return score, status

def main():
    print("╔" + "═"*58 + "╗")
    print("║     🧪 TESTE DE COERÊNCIA DIGILANG PT/EN               ║")
    print("╚" + "═"*58 + "╝")
    
    tester = DigiLangCoherenceTest()
    
    # Executar todos os testes
    results = {
        'pairs': tester.test_known_pairs(),
        'distribution': tester.test_symbol_distribution(),
        'consistency': tester.test_symbol_consistency(),
        'coverage': tester.test_coverage_completeness()
    }
    
    # Gerar relatório
    score, status = tester.generate_report(results)
    
    print("\n✨ TESTES CONCLUÍDOS!")
    print(f"🎯 Pontuação final: {score:.1f}%")
    print(f"📊 Status: {status}")
    
    return results

if __name__ == "__main__":
    main()