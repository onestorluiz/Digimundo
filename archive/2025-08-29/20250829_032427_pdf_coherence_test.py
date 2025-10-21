#!/usr/bin/env python3
"""
🎬 Teste de Coerência com PDFs Reais
Testa coerência PT↔EN usando roteiros reais extraídos de PDFs
"""

import json
import re
from pathlib import Path
import PyPDF2
from difflib import SequenceMatcher
from collections import Counter

class PDFCoherenceTest:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        print("╔" + "═"*58 + "╗")
        print("║  🎬 TESTE DE COERÊNCIA COM PDFS REAIS                ║")
        print("╚" + "═"*58 + "╝")
        
        # Carregar DigiLang
        print("\n📚 Carregando DigiLang...")
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.symbols = data.get('symbols', {})
            self.metadata = data.get('metadata', {})
        
        print(f"   ✅ {len(self.symbols):,} palavras no dicionário")
        
        # Criar dicionário reverso
        self.reverse_dict = {}
        for word, symbol in self.symbols.items():
            base_symbol = symbol.rstrip('⁺⁻~ᶜˢⁿᵐᵗˡᶠ⁰¹²³♂♀⚪')
            if base_symbol not in self.reverse_dict:
                self.reverse_dict[base_symbol] = []
            self.reverse_dict[base_symbol].append(word)
        
        # Dicionário de tradução expandido
        self.translation_dict = self.build_expanded_translation()
        
        # Resultados
        self.test_results = []
    
    def build_expanded_translation(self):
        """Constrói dicionário de tradução expandido para cinema"""
        translations = {
            # Palavras fundamentais
            'the': 'o', 'a': 'um', 'and': 'e', 'of': 'de', 'to': 'para',
            'in': 'em', 'is': 'é', 'it': 'isso', 'that': 'que', 'for': 'para',
            'with': 'com', 'as': 'como', 'was': 'foi', 'on': 'em', 'be': 'ser',
            'have': 'ter', 'from': 'de', 'or': 'ou', 'had': 'tinha', 'by': 'por',
            'not': 'não', 'but': 'mas', 'what': 'que', 'all': 'todo', 'were': 'foram',
            'when': 'quando', 'we': 'nós', 'there': 'lá', 'can': 'pode', 'an': 'um',
            'your': 'seu', 'which': 'qual', 'their': 'deles', 'said': 'disse',
            'if': 'se', 'do': 'fazer', 'will': 'vai', 'each': 'cada', 'about': 'sobre',
            'up': 'cima', 'out': 'fora', 'many': 'muitos', 'then': 'então',
            'them': 'eles', 'she': 'ela', 'some': 'alguns', 'her': 'dela',
            'would': 'seria', 'other': 'outro', 'into': 'em', 'time': 'tempo',
            'has': 'tem', 'two': 'dois', 'more': 'mais', 'like': 'como',
            'him': 'ele', 'see': 'ver', 'no': 'não', 'could': 'poderia',
            'first': 'primeiro', 'been': 'sido', 'its': 'seu', 'who': 'quem',
            'now': 'agora', 'people': 'pessoas', 'my': 'meu', 'made': 'feito',
            'over': 'sobre', 'know': 'saber', 'where': 'onde', 'much': 'muito',
            'go': 'ir', 'new': 'novo', 'write': 'escrever', 'our': 'nosso',
            'man': 'homem', 'day': 'dia', 'get': 'obter', 'come': 'vir',
            'water': 'água', 'way': 'caminho', 'may': 'pode', 'say': 'dizer',
            'part': 'parte', 'little': 'pequeno', 'right': 'certo', 'old': 'velho',
            'any': 'qualquer', 'same': 'mesmo', 'tell': 'contar', 'boy': 'menino',
            'follow': 'seguir', 'came': 'veio', 'want': 'querer', 'show': 'mostrar',
            'also': 'também', 'around': 'ao redor', 'form': 'forma', 'three': 'três',
            'small': 'pequeno', 'set': 'definir', 'put': 'colocar', 'end': 'fim',
            'why': 'por que', 'again': 'novamente', 'turn': 'virar', 'here': 'aqui',
            'how': 'como', 'after': 'depois', 'name': 'nome', 'good': 'bom',
            'sentence': 'frase', 'man': 'homem', 'think': 'pensar', 'say': 'dizer',
            'great': 'grande', 'where': 'onde', 'help': 'ajudar', 'through': 'através',
            'much': 'muito', 'before': 'antes', 'line': 'linha', 'right': 'direito',
            'too': 'também', 'mean': 'significar', 'old': 'velho', 'any': 'qualquer',
            'same': 'mesmo', 'tell': 'contar', 'boy': 'menino', 'follow': 'seguir',
            'came': 'veio', 'want': 'querer', 'show': 'mostrar',
            
            # Termos de cinema específicos
            'scene': 'cena', 'act': 'ato', 'character': 'personagem',
            'dialogue': 'diálogo', 'action': 'ação', 'cut': 'corte',
            'fade': 'fusão', 'interior': 'interior', 'exterior': 'exterior',
            'day': 'dia', 'night': 'noite', 'morning': 'manhã', 'evening': 'noite',
            'close': 'perto', 'medium': 'médio', 'wide': 'amplo', 'shot': 'plano',
            'angle': 'ângulo', 'camera': 'câmera', 'zoom': 'zoom', 'pan': 'panorâmica',
            'tilt': 'inclinação', 'tracking': 'travelling', 'dolly': 'dolly',
            'crane': 'grua', 'handheld': 'mão', 'steadicam': 'steadicam',
            'montage': 'montagem', 'sequence': 'sequência', 'transition': 'transição',
            'flashback': 'flashback', 'voiceover': 'narração', 'narrator': 'narrador',
            'soundtrack': 'trilha', 'music': 'música', 'sound': 'som',
            'lighting': 'iluminação', 'shadow': 'sombra', 'bright': 'brilhante',
            'dark': 'escuro', 'costume': 'figurino', 'makeup': 'maquiagem',
            'props': 'adereços', 'set': 'cenário', 'location': 'locação',
            'studio': 'estúdio', 'stage': 'palco', 'backdrop': 'fundo',
            'script': 'roteiro', 'screenplay': 'roteiro', 'story': 'história',
            'plot': 'trama', 'conflict': 'conflito', 'climax': 'clímax',
            'resolution': 'resolução', 'ending': 'final', 'beginning': 'início',
            'protagonist': 'protagonista', 'antagonist': 'antagonista',
            'hero': 'herói', 'villain': 'vilão', 'supporting': 'coadjuvante',
            'lead': 'protagonista', 'cast': 'elenco', 'actor': 'ator',
            'actress': 'atriz', 'performer': 'intérprete', 'role': 'papel',
            'director': 'diretor', 'producer': 'produtor', 'writer': 'roteirista',
            'cinematographer': 'diretor de fotografia', 'editor': 'editor',
            'composer': 'compositor', 'designer': 'designer', 'coordinator': 'coordenador',
            'assistant': 'assistente', 'crew': 'equipe', 'team': 'equipe',
            'production': 'produção', 'filming': 'filmagem', 'shooting': 'filmagem',
            'takes': 'tomadas', 'rehearsal': 'ensaio', 'preparation': 'preparação',
            'film': 'filme', 'movie': 'filme', 'cinema': 'cinema',
            'theater': 'teatro', 'screen': 'tela', 'projection': 'projeção',
            'premiere': 'estreia', 'release': 'lançamento', 'distribution': 'distribuição',
            'box': 'bilheteria', 'office': 'escritório', 'audience': 'público',
            'viewers': 'espectadores', 'critics': 'críticos', 'reviews': 'resenhas',
            'awards': 'prêmios', 'nomination': 'nomeação', 'winner': 'vencedor',
            'festival': 'festival', 'competition': 'competição', 'jury': 'júri',
            'genre': 'gênero', 'drama': 'drama', 'comedy': 'comédia',
            'romance': 'romance', 'thriller': 'suspense', 'horror': 'terror',
            'mystery': 'mistério', 'adventure': 'aventura', 'fantasy': 'fantasia',
            'science': 'ciência', 'fiction': 'ficção', 'documentary': 'documentário',
            'animation': 'animação', 'cartoon': 'desenho', 'musical': 'musical',
            'western': 'faroeste', 'noir': 'noir', 'epic': 'épico',
            'blockbuster': 'blockbuster', 'independent': 'independente',
            'mainstream': 'comercial', 'art': 'arte', 'experimental': 'experimental',
            'budget': 'orçamento', 'financing': 'financiamento', 'investment': 'investimento',
            'profit': 'lucro', 'loss': 'prejuízo', 'revenue': 'receita',
            'copyright': 'direitos', 'license': 'licença', 'contract': 'contrato',
            'deal': 'acordo', 'negotiation': 'negociação', 'agent': 'agente',
            'manager': 'empresário', 'lawyer': 'advogado', 'studio': 'estúdio',
            'company': 'empresa', 'corporation': 'corporação', 'industry': 'indústria',
            'business': 'negócio', 'market': 'mercado', 'trend': 'tendência',
            'style': 'estilo', 'technique': 'técnica', 'method': 'método',
            'approach': 'abordagem', 'vision': 'visão', 'concept': 'conceito',
            'idea': 'ideia', 'inspiration': 'inspiração', 'creativity': 'criatividade',
            'imagination': 'imaginação', 'innovation': 'inovação', 'originality': 'originalidade',
            'quality': 'qualidade', 'standard': 'padrão', 'level': 'nível',
            'professional': 'profissional', 'amateur': 'amador', 'student': 'estudante',
            'school': 'escola', 'course': 'curso', 'workshop': 'oficina',
            'training': 'treinamento', 'education': 'educação', 'learning': 'aprendizado',
            'experience': 'experiência', 'skill': 'habilidade', 'talent': 'talento',
            'ability': 'capacidade', 'potential': 'potencial', 'development': 'desenvolvimento',
            'improvement': 'melhoria', 'progress': 'progresso', 'success': 'sucesso',
            'failure': 'fracasso', 'mistake': 'erro', 'problem': 'problema',
            'solution': 'solução', 'challenge': 'desafio', 'opportunity': 'oportunidade',
            'goal': 'objetivo', 'target': 'meta', 'purpose': 'propósito',
            'meaning': 'significado', 'message': 'mensagem', 'theme': 'tema',
            'subject': 'assunto', 'topic': 'tópico', 'content': 'conteúdo',
            'material': 'material', 'source': 'fonte', 'reference': 'referência',
            'influence': 'influência', 'impact': 'impacto', 'effect': 'efeito',
            'result': 'resultado', 'outcome': 'resultado', 'consequence': 'consequência',
            'reaction': 'reação', 'response': 'resposta', 'feedback': 'feedback',
            'opinion': 'opinião', 'view': 'visão', 'perspective': 'perspectiva',
            'point': 'ponto', 'aspect': 'aspecto', 'element': 'elemento',
            'component': 'componente', 'part': 'parte', 'section': 'seção',
            'chapter': 'capítulo', 'episode': 'episódio', 'season': 'temporada',
            'series': 'série', 'sequel': 'sequência', 'prequel': 'prequela',
            'remake': 'remake', 'reboot': 'reinicialização', 'adaptation': 'adaptação',
            'version': 'versão', 'edition': 'edição', 'cut': 'corte',
            'director': 'diretor', 'final': 'final', 'theatrical': 'teatral',
            'extended': 'estendido', 'deleted': 'deletado', 'bonus': 'bônus',
            'extras': 'extras', 'features': 'recursos', 'commentary': 'comentário',
            'interview': 'entrevista', 'documentary': 'documentário', 'making': 'bastidores',
            'behind': 'por trás', 'scenes': 'cenas', 'bloopers': 'erros',
            'outtakes': 'sobras', 'alternate': 'alternativo', 'ending': 'final'
        }
        
        # Criar mapa bidirecional
        bidirectional = {}
        for en, pt in translations.items():
            bidirectional[en] = pt
            bidirectional[pt] = en
        
        return bidirectional
    
    def extract_pdf_text(self, pdf_path, max_pages=3):
        """Extrai texto de PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                pages_to_read = min(max_pages, len(reader.pages))
                
                for i in range(pages_to_read):
                    page_text = reader.pages[i].extract_text()
                    # Limpar texto
                    cleaned = re.sub(r'\s+', ' ', page_text)
                    text += cleaned + " "
                
                # Limitar tamanho para teste
                return text[:3000]
        except Exception as e:
            print(f"   ⚠️ Erro ao extrair PDF: {e}")
            return None
    
    def text_to_digilang(self, text):
        """Converte texto para DigiLang"""
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
        compressed = []
        unknown = []
        
        for word in words:
            if word in self.symbols:
                compressed.append(self.symbols[word])
            else:
                # Tentar variações morfológicas
                found = False
                if word.endswith('s') and word[:-1] in self.symbols:
                    compressed.append(self.symbols[word[:-1]] + '⁺')
                    found = True
                elif word.endswith('ed') and word[:-2] in self.symbols:
                    compressed.append(self.symbols[word[:-2]] + '⁻')
                    found = True
                elif word.endswith('ing') and word[:-3] in self.symbols:
                    compressed.append(self.symbols[word[:-3]] + '~')
                    found = True
                
                if not found:
                    compressed.append(f'[{word}]')
                    unknown.append(word)
        
        coverage = (len(compressed) - len(unknown)) / len(compressed) * 100 if compressed else 0
        return ' '.join(compressed), coverage, unknown
    
    def digilang_to_text(self, compressed_text, target_lang='pt'):
        """Converte DigiLang para texto"""
        symbols = compressed_text.split()
        decompressed = []
        
        for symbol in symbols:
            # Remover marcadores de palavras desconhecidas
            if symbol.startswith('[') and symbol.endswith(']'):
                word = symbol[1:-1]
                if word in self.translation_dict:
                    decompressed.append(self.translation_dict[word])
                else:
                    decompressed.append(word)
                continue
            
            # Processar símbolo normal
            base_symbol = symbol.rstrip('⁺⁻~')
            modifier = symbol[len(base_symbol):]
            
            if base_symbol in self.reverse_dict:
                words = self.reverse_dict[base_symbol]
                
                # Escolher palavra apropriada para idioma
                chosen_word = words[0]  # Default
                
                for word in words:
                    if word in self.translation_dict:
                        translation = self.translation_dict[word]
                        
                        # Verificar se tradução é do idioma alvo
                        if target_lang == 'pt':
                            # Caracteres portugueses ou terminações
                            if any(c in translation for c in 'áàâãéêíóôõúç') or \
                               any(translation.endswith(end) for end in ['ção', 'são', 'dade']):
                                chosen_word = translation
                                break
                        else:  # inglês
                            if not any(c in translation for c in 'áàâãéêíóôõúç'):
                                chosen_word = translation
                                break
                
                # Aplicar modificador
                if modifier == '⁺':
                    chosen_word += 's'
                elif modifier == '⁻':
                    if target_lang == 'en':
                        chosen_word += 'ed'
                elif modifier == '~':
                    if target_lang == 'en':
                        chosen_word += 'ing'
                    else:
                        chosen_word += 'ndo'
                
                decompressed.append(chosen_word)
            else:
                decompressed.append(f'?{symbol}?')
        
        return ' '.join(decompressed)
    
    def direct_translate(self, text, target='pt'):
        """Tradução direta usando dicionário"""
        words = text.split()
        translated = []
        
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            
            if clean_word in self.translation_dict:
                trans_word = self.translation_dict[clean_word]
                # Preservar capitalização
                if word[0].isupper():
                    trans_word = trans_word.capitalize()
                translated.append(trans_word)
            else:
                translated.append(word)
        
        return ' '.join(translated)
    
    def calculate_similarity(self, text1, text2):
        """Calcula similaridade entre textos"""
        # Normalizar
        norm1 = re.sub(r'[^\w\s]', '', text1.lower())
        norm2 = re.sub(r'[^\w\s]', '', text2.lower())
        
        # Similaridade de sequência
        seq_sim = SequenceMatcher(None, norm1, norm2).ratio() * 100
        
        # Similaridade de palavras
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        
        if words1 and words2:
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            jaccard = len(intersection) / len(union) * 100
        else:
            jaccard = 0
        
        # Verificar traduções corretas
        correct = 0
        total = 0
        
        for w1 in words1:
            if w1 in self.translation_dict:
                expected = self.translation_dict[w1]
                if expected in words2:
                    correct += 1
            total += 1
        
        accuracy = (correct / total * 100) if total > 0 else 0
        
        # Média ponderada
        return (seq_sim * 0.2 + jaccard * 0.3 + accuracy * 0.5)
    
    def test_pdf_coherence(self, pdf_path):
        """Testa coerência usando PDF"""
        print(f"\n🎬 Testando PDF: {pdf_path.name}")
        print("="*60)
        
        # Extrair texto
        print("📄 Extraindo texto do PDF...")
        text = self.extract_pdf_text(pdf_path)
        
        if not text:
            print("❌ Falha ao extrair texto")
            return None
        
        print(f"   ✅ Texto extraído: {len(text)} caracteres")
        print(f"   📝 Preview: \"{text[:100]}...\"")
        
        # Detectar idioma (heurística simples)
        portuguese_words = ['de', 'da', 'do', 'com', 'para', 'em', 'uma', 'que', 'não']
        english_words = ['the', 'and', 'of', 'to', 'in', 'a', 'that', 'is', 'for']
        
        pt_count = sum(1 for word in portuguese_words if word in text.lower())
        en_count = sum(1 for word in english_words if word in text.lower())
        
        source_lang = 'pt' if pt_count > en_count else 'en'
        target_lang = 'en' if source_lang == 'pt' else 'pt'
        
        print(f"   🌍 Idioma detectado: {source_lang.upper()}")
        
        # Teste de tradução via DigiLang
        print(f"\n1️⃣ Convertendo {source_lang.upper()} → DigiLang...")
        compressed, coverage, unknown = self.text_to_digilang(text)
        print(f"   ✅ Cobertura: {coverage:.1f}%")
        print(f"   ⚠️ Palavras desconhecidas: {len(unknown)}")
        
        print(f"\n2️⃣ Convertendo DigiLang → {target_lang.upper()}...")
        via_digilang = self.digilang_to_text(compressed, target_lang)
        print(f"   ✅ Tradução via DigiLang concluída")
        
        print(f"\n3️⃣ Tradução direta {source_lang.upper()} → {target_lang.upper()}...")
        direct = self.direct_translate(text, target_lang)
        print(f"   ✅ Tradução direta concluída")
        
        # Análise de coerência
        print(f"\n4️⃣ Analisando coerência...")
        coherence = self.calculate_similarity(via_digilang, direct)
        
        print(f"\n📊 RESULTADOS FINAIS:")
        print(f"   • Cobertura DigiLang: {coverage:.1f}%")
        print(f"   • Coerência: {coherence:.1f}%")
        print(f"   • Palavras perdidas: {len(unknown)}")
        
        # Amostras das traduções
        print(f"\n📝 COMPARAÇÃO DE TRADUÇÕES:")
        print(f"   Via DigiLang: \"{via_digilang[:100]}...\"")
        print(f"   Direta: \"{direct[:100]}...\"")
        
        if unknown:
            print(f"\n⚠️ PALAVRAS PROBLEMÁTICAS:")
            word_freq = Counter(unknown)
            for word, count in word_freq.most_common(5):
                print(f"   • {word}: {count}x")
        
        result = {
            'pdf': pdf_path.name,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'coverage': coverage,
            'coherence': coherence,
            'unknown_count': len(unknown),
            'text_length': len(text),
            'unknown_words': list(Counter(unknown).most_common(10))
        }
        
        self.test_results.append(result)
        return result

def main():
    tester = PDFCoherenceTest()
    
    # Lista de PDFs para testar
    pdf_paths = [
        "/Users/clubproducoes/Digimundo/digimons/scripturemon_backup_20250827_165659/cinema/2_roteiros_mestres/Chinatown - Screenplay.pdf",
        "/Users/clubproducoes/Digimundo/digimons/scripturemon_backup_20250827_165659/cinema/2_roteiros_mestres/Pulp Fiction - Release.pdf",
        "/Users/clubproducoes/Digimundo/digimons/scripturemon_backup_20250827_165659/cinema/2_roteiros_mestres/The Godfather - Screenplay.pdf"
    ]
    
    print("\n🎯 INICIANDO TESTES DE COERÊNCIA COM PDFS REAIS")
    
    # Testar cada PDF
    for pdf_path in pdf_paths[:2]:  # Limitar a 2 PDFs para o teste
        path = Path(pdf_path)
        if path.exists():
            result = tester.test_pdf_coherence(path)
        else:
            print(f"❌ PDF não encontrado: {pdf_path}")
    
    # Relatório consolidado
    if tester.test_results:
        print(f"\n{'='*60}")
        print("📊 RELATÓRIO CONSOLIDADO DE COERÊNCIA")
        print(f"{'='*60}")
        
        avg_coverage = sum(r['coverage'] for r in tester.test_results) / len(tester.test_results)
        avg_coherence = sum(r['coherence'] for r in tester.test_results) / len(tester.test_results)
        total_unknown = sum(r['unknown_count'] for r in tester.test_results)
        
        print(f"\nTestes realizados: {len(tester.test_results)}")
        print(f"Cobertura média: {avg_coverage:.1f}%")
        print(f"Coerência média: {avg_coherence:.1f}%")
        print(f"Total de palavras perdidas: {total_unknown}")
        
        print(f"\n📋 RESULTADOS POR PDF:")
        for result in tester.test_results:
            print(f"   • {result['pdf']}: {result['coherence']:.1f}% coerência")
        
        # Palavras mais problemáticas
        all_unknown = []
        for result in tester.test_results:
            all_unknown.extend([word for word, count in result['unknown_words']])
        
        if all_unknown:
            problem_words = Counter(all_unknown)
            print(f"\n🔍 PALAVRAS MAIS PROBLEMÁTICAS:")
            for word, count in problem_words.most_common(10):
                print(f"   • {word}: {count} ocorrências")
        
        # Avaliação final
        if avg_coherence >= 70:
            print(f"\n✅ SISTEMA APROVADO! Coerência satisfatória ({avg_coherence:.1f}%)")
        else:
            print(f"\n⚠️ SISTEMA NECESSITA MELHORIAS. Coerência baixa ({avg_coherence:.1f}%)")
            print("   Sugestões:")
            print("   1. Adicionar palavras problemáticas ao dicionário")
            print("   2. Melhorar mapeamento bilíngue PT↔EN")
            print("   3. Implementar regras morfológicas")
    
    print("\n🎉 Teste completo!")

if __name__ == "__main__":
    main()