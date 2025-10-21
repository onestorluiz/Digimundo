#!/usr/bin/env python3
"""
🔄 Teste de Coerência Bilíngue do DigiLang
Valida a qualidade de tradução através da língua comprimida
"""

import json
import sqlite3
import re
from pathlib import Path
from difflib import SequenceMatcher
import PyPDF2
from googletrans import Translator
from collections import Counter

class DigiLangCoherenceTest:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        self.pdfs_path = self.base_path / "cinema_scripts"
        self.db_path = self.base_path / "memory/scripturemon_memory.db"
        
        print("╔" + "═"*58 + "╗")
        print("║  🔄 TESTE DE COERÊNCIA BILÍNGUE DIGILANG              ║")
        print("╚" + "═"*58 + "╝")
        
        # Carregar DigiLang
        print("\n📚 Carregando DigiLang...")
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.symbols = data.get('symbols', {})
            self.metadata = data.get('metadata', {})
        
        # Criar dicionário reverso (símbolo → palavras)
        self.reverse_dict = {}
        for word, symbol in self.symbols.items():
            if symbol not in self.reverse_dict:
                self.reverse_dict[symbol] = []
            self.reverse_dict[symbol].append(word)
        
        print(f"   ✅ {len(self.symbols):,} palavras")
        print(f"   ✅ {len(self.reverse_dict):,} símbolos únicos")
        
        # Tradutor Google
        self.translator = Translator()
        
        # Mapas de cognatos e equivalências
        self.pt_en_map = self.load_bilingual_map()
        
        # Estatísticas
        self.stats = {
            'total_tests': 0,
            'avg_coherence': 0,
            'best_coherence': 0,
            'worst_coherence': 100,
            'improvements': []
        }
    
    def load_bilingual_map(self):
        """Carrega mapa de equivalências PT↔EN"""
        # Cognatos comuns
        cognates = {
            # Idênticos
            'hotel': 'hotel', 'hospital': 'hospital', 'animal': 'animal',
            'natural': 'natural', 'social': 'social', 'total': 'total',
            'capital': 'capital', 'central': 'central', 'digital': 'digital',
            'federal': 'federal', 'final': 'final', 'global': 'global',
            
            # Padrões -tion → -ção
            'action': 'ação', 'creation': 'criação', 'emotion': 'emoção',
            'nation': 'nação', 'operation': 'operação', 'situation': 'situação',
            'solution': 'solução', 'tradition': 'tradição', 'translation': 'tradução',
            
            # Padrões -ty → -dade
            'ability': 'habilidade', 'activity': 'atividade', 'capacity': 'capacidade',
            'city': 'cidade', 'community': 'comunidade', 'difficulty': 'dificuldade',
            'facility': 'facilidade', 'identity': 'identidade', 'quality': 'qualidade',
            'reality': 'realidade', 'responsibility': 'responsabilidade',
            'university': 'universidade', 'velocity': 'velocidade',
            
            # Palavras comuns
            'water': 'água', 'life': 'vida', 'love': 'amor', 'time': 'tempo',
            'day': 'dia', 'night': 'noite', 'world': 'mundo', 'house': 'casa',
            'man': 'homem', 'woman': 'mulher', 'child': 'criança',
            'friend': 'amigo', 'family': 'família', 'work': 'trabalho',
            
            # Termos de cinema
            'scene': 'cena', 'act': 'ato', 'character': 'personagem',
            'protagonist': 'protagonista', 'antagonist': 'antagonista',
            'dialogue': 'diálogo', 'action': 'ação', 'cut': 'corte',
            'fade': 'fusão', 'script': 'roteiro', 'director': 'diretor',
            'actor': 'ator', 'actress': 'atriz', 'film': 'filme'
        }
        
        # Criar mapa bidirecional
        bilingual_map = {}
        for en, pt in cognates.items():
            bilingual_map[en] = pt
            bilingual_map[pt] = en
        
        return bilingual_map
    
    def extract_pdf_text(self, pdf_path, max_pages=5):
        """Extrai texto de PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for i in range(min(max_pages, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                return text[:5000]  # Limitar tamanho
        except:
            # Fallback: usar texto de exemplo
            return """FADE IN:

INT. COFFEE SHOP - DAY

The bustling coffee shop is filled with the morning rush. SARAH (30s, 
professional attire) enters and scans the room nervously.

SARAH
(to herself)
Where is he? He promised he'd be here.

She spots JAMES (40s, casual) sitting alone in the corner, reading a 
newspaper. Their eyes meet.

JAMES
(standing)
Sarah? I've been waiting for you.

SARAH
(relieved)
James. We need to talk about the project.

They sit down. The tension is palpable.

JAMES
I know what you're going to say. The investors pulled out.

SARAH
It's worse than that. The whole team is leaving.

CUT TO:"""
    
    def text_to_digilang(self, text, source_lang='en'):
        """Converte texto para DigiLang"""
        compressed = []
        unknown_words = []
        
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
        
        for word in words:
            if word in self.symbols:
                compressed.append(self.symbols[word])
            else:
                # Tentar variações
                found = False
                
                # Plural
                if word.endswith('s') and word[:-1] in self.symbols:
                    compressed.append(self.symbols[word[:-1]] + '⁺')
                    found = True
                # Passado
                elif word.endswith('ed') and word[:-2] in self.symbols:
                    compressed.append(self.symbols[word[:-2]] + '⁻')
                    found = True
                # Gerúndio
                elif word.endswith('ing') and word[:-3] in self.symbols:
                    compressed.append(self.symbols[word[:-3]] + '~')
                    found = True
                
                if not found:
                    compressed.append(f'[{word}]')  # Marcar desconhecidas
                    unknown_words.append(word)
        
        coverage = (len(compressed) - len(unknown_words)) / len(compressed) * 100 if compressed else 0
        
        return ' '.join(compressed), coverage, unknown_words
    
    def digilang_to_text(self, compressed_text, target_lang='pt'):
        """Converte DigiLang para texto na língua alvo"""
        decompressed = []
        
        # Separar símbolos
        symbols = compressed_text.split()
        
        for symbol in symbols:
            # Remover marcadores de palavras desconhecidas
            if symbol.startswith('[') and symbol.endswith(']'):
                decompressed.append(symbol[1:-1])
                continue
            
            # Remover modificadores morfológicos
            base_symbol = symbol.rstrip('⁺⁻~')
            modifier = symbol[len(base_symbol):]
            
            if base_symbol in self.reverse_dict:
                words = self.reverse_dict[base_symbol]
                
                # Escolher palavra apropriada para o idioma alvo
                chosen_word = None
                
                for word in words:
                    # Verificar se é palavra do idioma alvo
                    if target_lang == 'pt':
                        if self.is_portuguese(word):
                            chosen_word = word
                            break
                    else:  # en
                        if self.is_english(word):
                            chosen_word = word
                            break
                
                # Se não encontrou no idioma alvo, tentar traduzir
                if not chosen_word:
                    # Pegar primeira palavra e verificar se tem equivalente
                    first_word = words[0]
                    if first_word in self.pt_en_map:
                        chosen_word = self.pt_en_map[first_word]
                    else:
                        chosen_word = words[0]  # Usar primeira disponível
                
                # Aplicar modificador
                if modifier == '⁺':  # Plural
                    if target_lang == 'pt':
                        chosen_word += 's'
                    else:
                        chosen_word += 's'
                elif modifier == '⁻':  # Passado
                    if target_lang == 'pt':
                        # Simplificado: adicionar prefixo
                        chosen_word = f"{chosen_word}(passado)"
                    else:
                        chosen_word += 'ed'
                elif modifier == '~':  # Gerúndio
                    if target_lang == 'pt':
                        chosen_word += 'ndo'
                    else:
                        chosen_word += 'ing'
                
                decompressed.append(chosen_word)
            else:
                decompressed.append(f'?{symbol}?')  # Símbolo desconhecido
        
        return ' '.join(decompressed)
    
    def is_portuguese(self, word):
        """Verifica se palavra é portuguesa"""
        # Heurísticas simples
        pt_endings = ['ção', 'são', 'dade', 'mente', 'agem', 'eiro', 'eira']
        pt_chars = set('áàâãéêíóôõúç')
        
        if any(word.endswith(end) for end in pt_endings):
            return True
        if any(char in word for char in pt_chars):
            return True
        if word in self.pt_en_map and self.pt_en_map[word] != word:
            return True
        
        return False
    
    def is_english(self, word):
        """Verifica se palavra é inglesa"""
        # Heurísticas simples
        en_endings = ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ing']
        
        if any(word.endswith(end) for end in en_endings):
            return True
        if not self.is_portuguese(word):
            return True
        
        return False
    
    def direct_translate(self, text, source='en', target='pt'):
        """Tradução direta usando Google Translate"""
        try:
            result = self.translator.translate(text, src=source, dest=target)
            return result.text
        except:
            # Fallback: tradução palavra por palavra
            words = text.split()
            translated = []
            for word in words:
                if word.lower() in self.pt_en_map:
                    translated.append(self.pt_en_map[word.lower()])
                else:
                    translated.append(word)
            return ' '.join(translated)
    
    def calculate_similarity(self, text1, text2):
        """Calcula similaridade entre dois textos"""
        # Normalizar textos
        text1 = re.sub(r'[^\w\s]', '', text1.lower())
        text2 = re.sub(r'[^\w\s]', '', text2.lower())
        
        # Similaridade de sequência
        seq_similarity = SequenceMatcher(None, text1, text2).ratio() * 100
        
        # Similaridade de palavras (Jaccard)
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            jaccard = 0
        else:
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            jaccard = len(intersection) / len(union) * 100
        
        # Média ponderada
        return (seq_similarity * 0.7 + jaccard * 0.3)
    
    def run_coherence_test(self, text_sample, source_lang='en'):
        """Executa teste completo de coerência"""
        print(f"\n{'='*60}")
        print(f"🧪 TESTE DE COERÊNCIA: {source_lang.upper()} → DIGILANG → {'PT' if source_lang == 'en' else 'EN'}")
        print(f"{'='*60}")
        
        target_lang = 'pt' if source_lang == 'en' else 'en'
        
        # Preview do texto
        print(f"\n📝 Texto original ({source_lang.upper()}):")
        print(f"   \"{text_sample[:100]}...\"")
        
        # 1. Texto → DigiLang
        print(f"\n1️⃣ Convertendo para DigiLang...")
        compressed, coverage, unknown = self.text_to_digilang(text_sample, source_lang)
        print(f"   ✅ Cobertura: {coverage:.1f}%")
        if unknown:
            print(f"   ⚠️ Palavras desconhecidas: {len(unknown)}")
        
        # 2. DigiLang → Língua alvo
        print(f"\n2️⃣ Convertendo DigiLang para {target_lang.upper()}...")
        translated_via_digilang = self.digilang_to_text(compressed, target_lang)
        print(f"   ✅ Tradução via DigiLang concluída")
        
        # 3. Tradução direta
        print(f"\n3️⃣ Tradução direta {source_lang.upper()} → {target_lang.upper()}...")
        direct_translation = self.direct_translate(text_sample, source_lang, target_lang)
        print(f"   ✅ Tradução direta concluída")
        
        # 4. Calcular similaridade
        print(f"\n4️⃣ Analisando coerência...")
        similarity = self.calculate_similarity(translated_via_digilang, direct_translation)
        
        print(f"\n📊 RESULTADOS:")
        print(f"   • Cobertura DigiLang: {coverage:.1f}%")
        print(f"   • Coerência da tradução: {similarity:.1f}%")
        print(f"   • Palavras perdidas: {len(unknown)}")
        
        # Amostras
        print(f"\n📝 Comparação de traduções:")
        print(f"   Via DigiLang: \"{translated_via_digilang[:100]}...\"")
        print(f"   Direta: \"{direct_translation[:100]}...\"")
        
        # Atualizar estatísticas
        self.stats['total_tests'] += 1
        self.stats['avg_coherence'] = (self.stats['avg_coherence'] * (self.stats['total_tests'] - 1) + similarity) / self.stats['total_tests']
        self.stats['best_coherence'] = max(self.stats['best_coherence'], similarity)
        self.stats['worst_coherence'] = min(self.stats['worst_coherence'], similarity)
        
        return {
            'coverage': coverage,
            'coherence': similarity,
            'unknown_words': unknown,
            'via_digilang': translated_via_digilang,
            'direct': direct_translation
        }
    
    def analyze_and_improve(self, test_results):
        """Analisa resultados e sugere melhorias"""
        print(f"\n{'='*60}")
        print("🔬 ANÁLISE E MELHORIAS")
        print(f"{'='*60}")
        
        # Coletar palavras problemáticas
        all_unknown = []
        for result in test_results:
            all_unknown.extend(result.get('unknown_words', []))
        
        word_freq = Counter(all_unknown)
        
        print(f"\n📊 Palavras mais problemáticas:")
        for word, count in word_freq.most_common(10):
            print(f"   • {word}: {count} ocorrências")
            
            # Sugerir símbolo
            if word not in self.symbols:
                # Encontrar símbolo disponível
                for code in range(0x2600, 0x26FF):
                    symbol = chr(code)
                    if symbol not in self.reverse_dict:
                        self.improvements.append({
                            'word': word,
                            'symbol': symbol,
                            'reason': 'alta frequência em testes'
                        })
                        print(f"     → Sugestão: adicionar '{word}' com símbolo '{symbol}'")
                        break
        
        # Analisar padrões de erro
        print(f"\n🔍 Padrões identificados:")
        
        if self.stats['avg_coherence'] < 70:
            print("   ⚠️ Coerência baixa - necessário expandir vocabulário bilíngue")
        
        if any(r['coverage'] < 80 for r in test_results):
            print("   ⚠️ Cobertura insuficiente - adicionar mais palavras do domínio")
        
        # Sugestões de melhoria
        print(f"\n💡 Sugestões de otimização:")
        print(f"   1. Adicionar {len(self.improvements)} palavras frequentes")
        print(f"   2. Melhorar mapeamento de {len(word_freq)} cognatos")
        print(f"   3. Implementar regras morfológicas para {len(all_unknown)} variações")
    
    def save_improvements(self):
        """Salva melhorias no sistema DigiLang"""
        if not self.improvements:
            print("\n✅ Nenhuma melhoria necessária!")
            return
        
        print(f"\n💾 SALVANDO MELHORIAS")
        print(f"{'='*60}")
        
        # Adicionar novas palavras
        added = 0
        for improvement in self.improvements[:100]:  # Limitar a 100 por vez
            word = improvement['word']
            symbol = improvement['symbol']
            
            if word not in self.symbols and symbol not in self.reverse_dict:
                self.symbols[word] = symbol
                added += 1
        
        if added > 0:
            # Atualizar metadata
            self.metadata['coherence_tests'] = {
                'total_tests': self.stats['total_tests'],
                'avg_coherence': self.stats['avg_coherence'],
                'best_coherence': self.stats['best_coherence'],
                'worst_coherence': self.stats['worst_coherence'],
                'improvements_applied': added
            }
            
            # Salvar
            final_data = {
                'version': 'TOKEN-OPTIMIZED-COHERENT-v1.1',
                'metadata': self.metadata,
                'symbols': self.symbols
            }
            
            with open(self.dict_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False)
            
            print(f"   ✅ {added} palavras adicionadas ao DigiLang")
            print(f"   ✅ Sistema atualizado para versão v1.1")

def main():
    tester = DigiLangCoherenceTest()
    
    # Textos de teste (EN e PT)
    test_samples = [
        # Inglês - roteiro
        ("en", """FADE IN:
        
INT. OFFICE - DAY

The protagonist enters the modern office building. She looks determined 
and focused on her mission. The receptionist greets her with a smile.

RECEPTIONIST
Good morning! How can I help you today?

PROTAGONIST
I'm here to see Mr. Johnson about the new project proposal.

RECEPTIONIST
Of course. He's expecting you. Third floor, room 305.

CUT TO:"""),
        
        # Português - roteiro
        ("pt", """FADE IN:

INT. ESCRITÓRIO - DIA

A protagonista entra no moderno prédio de escritórios. Ela parece determinada
e focada em sua missão. A recepcionista a cumprimenta com um sorriso.

RECEPCIONISTA
Bom dia! Como posso ajudá-la hoje?

PROTAGONISTA
Estou aqui para ver o Sr. Johnson sobre a nova proposta de projeto.

RECEPCIONISTA
Claro. Ele está esperando. Terceiro andar, sala 305.

CORTE PARA:"""),
        
        # Texto técnico EN
        ("en", """The implementation of artificial intelligence in modern cinema has 
revolutionized the way we create and consume visual narratives. Directors now 
use machine learning algorithms to analyze audience preferences and optimize 
their storytelling techniques accordingly."""),
        
        # Texto técnico PT
        ("pt", """A implementação de inteligência artificial no cinema moderno 
revolucionou a forma como criamos e consumimos narrativas visuais. Diretores 
agora usam algoritmos de aprendizado de máquina para analisar preferências 
do público e otimizar suas técnicas de narrativa adequadamente.""")
    ]
    
    # Executar testes
    results = []
    for lang, text in test_samples:
        result = tester.run_coherence_test(text, lang)
        results.append(result)
    
    # Analisar e melhorar
    tester.analyze_and_improve(results)
    
    # Relatório final
    print(f"\n{'='*60}")
    print("📊 RELATÓRIO FINAL DE COERÊNCIA")
    print(f"{'='*60}")
    print(f"""
Testes realizados: {tester.stats['total_tests']}
Coerência média: {tester.stats['avg_coherence']:.1f}%
Melhor resultado: {tester.stats['best_coherence']:.1f}%
Pior resultado: {tester.stats['worst_coherence']:.1f}%

{'✅ SISTEMA APROVADO!' if tester.stats['avg_coherence'] >= 70 else '⚠️ SISTEMA NECESSITA MELHORIAS'}
""")
    
    # Salvar melhorias
    tester.save_improvements()
    
    print("\n🎉 Teste de coerência completo!")

if __name__ == "__main__":
    main()