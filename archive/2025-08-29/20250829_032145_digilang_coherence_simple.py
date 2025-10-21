#!/usr/bin/env python3
"""
🔄 Teste de Coerência Bilíngue do DigiLang (Versão Simplificada)
Valida a qualidade de tradução através da língua comprimida
"""

import json
import re
from pathlib import Path
from difflib import SequenceMatcher
from collections import Counter

class DigiLangCoherenceTest:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
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
            base_symbol = symbol.rstrip('⁺⁻~ᶜˢⁿᵐᵗˡᶠ⁰¹²³♂♀⚪')
            if base_symbol not in self.reverse_dict:
                self.reverse_dict[base_symbol] = []
            self.reverse_dict[base_symbol].append(word)
        
        print(f"   ✅ {len(self.symbols):,} palavras")
        print(f"   ✅ {len(self.reverse_dict):,} símbolos únicos")
        
        # Dicionário de tradução manual expandido
        self.translation_dict = self.build_translation_dict()
        
        # Estatísticas
        self.stats = {
            'total_tests': 0,
            'avg_coherence': 0,
            'best_coherence': 0,
            'worst_coherence': 100,
            'improvements': []
        }
    
    def build_translation_dict(self):
        """Constrói dicionário de tradução PT↔EN expandido"""
        translations = {
            # Palavras mais comuns
            'the': 'o', 'a': 'um', 'and': 'e', 'of': 'de', 'to': 'para',
            'in': 'em', 'is': 'é', 'it': 'isso', 'that': 'que', 'for': 'para',
            'with': 'com', 'as': 'como', 'was': 'foi', 'on': 'em', 'be': 'ser',
            'have': 'ter', 'from': 'de', 'or': 'ou', 'had': 'tinha', 'by': 'por',
            'not': 'não', 'but': 'mas', 'what': 'o que', 'all': 'todo', 'were': 'foram',
            'when': 'quando', 'we': 'nós', 'there': 'lá', 'can': 'pode', 'an': 'um',
            'your': 'seu', 'which': 'qual', 'their': 'deles', 'said': 'disse',
            'if': 'se', 'do': 'fazer', 'will': 'vai', 'each': 'cada', 'about': 'sobre',
            'how': 'como', 'up': 'cima', 'out': 'fora', 'them': 'eles', 'then': 'então',
            'she': 'ela', 'many': 'muitos', 'some': 'alguns', 'so': 'então', 'these': 'estes',
            'would': 'seria', 'other': 'outro', 'into': 'em', 'has': 'tem', 'more': 'mais',
            'her': 'dela', 'two': 'dois', 'like': 'como', 'him': 'dele', 'see': 'ver',
            'time': 'tempo', 'could': 'poderia', 'no': 'não', 'make': 'fazer', 'than': 'que',
            'first': 'primeiro', 'been': 'sido', 'its': 'seu', 'who': 'quem', 'now': 'agora',
            'people': 'pessoas', 'my': 'meu', 'made': 'feito', 'over': 'sobre', 'know': 'saber',
            'after': 'depois', 'back': 'volta', 'through': 'através', 'me': 'eu', 'year': 'ano',
            'where': 'onde', 'much': 'muito', 'before': 'antes', 'go': 'ir', 'good': 'bom',
            'new': 'novo', 'write': 'escrever', 'our': 'nosso', 'used': 'usado', 'man': 'homem',
            'find': 'encontrar', 'day': 'dia', 'did': 'fez', 'get': 'obter', 'come': 'vir',
            'may': 'pode', 'part': 'parte', 'what': 'que', 'take': 'pegar', 'see': 'ver',
            'him': 'ele', 'call': 'chamar', 'am': 'sou', 'now': 'agora', 'find': 'encontrar',
            'look': 'olhar', 'only': 'apenas', 'come': 'vir', 'think': 'pensar', 'also': 'também',
            
            # Substantivos comuns
            'water': 'água', 'life': 'vida', 'love': 'amor', 'world': 'mundo',
            'house': 'casa', 'man': 'homem', 'woman': 'mulher', 'child': 'criança',
            'friend': 'amigo', 'family': 'família', 'work': 'trabalho', 'school': 'escola',
            'city': 'cidade', 'country': 'país', 'place': 'lugar', 'home': 'lar',
            'room': 'sala', 'book': 'livro', 'hand': 'mão', 'money': 'dinheiro',
            'face': 'rosto', 'door': 'porta', 'car': 'carro', 'tree': 'árvore',
            'road': 'estrada', 'name': 'nome', 'father': 'pai', 'mother': 'mãe',
            'son': 'filho', 'daughter': 'filha', 'brother': 'irmão', 'sister': 'irmã',
            
            # Verbos comuns
            'be': 'ser', 'have': 'ter', 'do': 'fazer', 'say': 'dizer', 'go': 'ir',
            'get': 'obter', 'make': 'fazer', 'know': 'saber', 'think': 'pensar',
            'take': 'pegar', 'see': 'ver', 'come': 'vir', 'want': 'querer',
            'look': 'olhar', 'use': 'usar', 'find': 'encontrar', 'give': 'dar',
            'tell': 'contar', 'work': 'trabalhar', 'call': 'chamar', 'try': 'tentar',
            'ask': 'perguntar', 'need': 'precisar', 'feel': 'sentir', 'become': 'tornar',
            'leave': 'deixar', 'put': 'colocar', 'mean': 'significar', 'keep': 'manter',
            'let': 'deixar', 'begin': 'começar', 'seem': 'parecer', 'help': 'ajudar',
            'show': 'mostrar', 'hear': 'ouvir', 'play': 'jogar', 'run': 'correr',
            'move': 'mover', 'live': 'viver', 'believe': 'acreditar', 'bring': 'trazer',
            'happen': 'acontecer', 'write': 'escrever', 'sit': 'sentar', 'stand': 'ficar',
            'lose': 'perder', 'pay': 'pagar', 'meet': 'encontrar', 'include': 'incluir',
            'continue': 'continuar', 'set': 'definir', 'learn': 'aprender', 'change': 'mudar',
            
            # Adjetivos comuns
            'good': 'bom', 'new': 'novo', 'first': 'primeiro', 'last': 'último',
            'long': 'longo', 'great': 'grande', 'little': 'pequeno', 'own': 'próprio',
            'other': 'outro', 'old': 'velho', 'right': 'certo', 'big': 'grande',
            'high': 'alto', 'different': 'diferente', 'small': 'pequeno', 'large': 'grande',
            'next': 'próximo', 'early': 'cedo', 'young': 'jovem', 'important': 'importante',
            'few': 'poucos', 'public': 'público', 'bad': 'mau', 'same': 'mesmo',
            'able': 'capaz', 'political': 'político', 'late': 'tarde', 'general': 'geral',
            'full': 'cheio', 'sure': 'certo', 'clear': 'claro', 'major': 'maior',
            'better': 'melhor', 'true': 'verdadeiro', 'whole': 'inteiro', 'free': 'livre',
            'economic': 'econômico', 'strong': 'forte', 'possible': 'possível',
            'certain': 'certo', 'open': 'aberto', 'difficult': 'difícil', 'power': 'poder',
            'special': 'especial', 'short': 'curto', 'single': 'único', 'medical': 'médico',
            'current': 'atual', 'wrong': 'errado', 'private': 'privado', 'past': 'passado',
            'foreign': 'estrangeiro', 'fine': 'bom', 'common': 'comum', 'poor': 'pobre',
            'natural': 'natural', 'significant': 'significativo', 'similar': 'similar',
            
            # Termos de cinema/roteiro
            'scene': 'cena', 'act': 'ato', 'character': 'personagem',
            'protagonist': 'protagonista', 'antagonist': 'antagonista',
            'dialogue': 'diálogo', 'action': 'ação', 'cut': 'corte',
            'fade': 'fusão', 'script': 'roteiro', 'director': 'diretor',
            'actor': 'ator', 'actress': 'atriz', 'film': 'filme',
            'movie': 'filme', 'cinema': 'cinema', 'screen': 'tela',
            'camera': 'câmera', 'shot': 'tomada', 'angle': 'ângulo',
            'close': 'perto', 'wide': 'amplo', 'zoom': 'zoom',
            'pan': 'panorâmica', 'tracking': 'travelling', 'dolly': 'dolly',
            'montage': 'montagem', 'edit': 'editar', 'frame': 'quadro',
            'sequence': 'sequência', 'transition': 'transição',
            'flashback': 'flashback', 'voiceover': 'narração',
            'soundtrack': 'trilha', 'lighting': 'iluminação',
            'costume': 'figurino', 'makeup': 'maquiagem', 'props': 'adereços',
            'set': 'cenário', 'location': 'locação', 'studio': 'estúdio',
            'production': 'produção', 'producer': 'produtor',
            'writer': 'roteirista', 'screenplay': 'roteiro',
            'story': 'história', 'plot': 'trama', 'conflict': 'conflito',
            'climax': 'clímax', 'resolution': 'resolução', 'ending': 'final',
            'beginning': 'início', 'middle': 'meio', 'hero': 'herói',
            'villain': 'vilão', 'journey': 'jornada', 'quest': 'busca',
            'love': 'amor', 'death': 'morte', 'life': 'vida',
            'hope': 'esperança', 'fear': 'medo', 'dream': 'sonho',
            'reality': 'realidade', 'illusion': 'ilusão', 'truth': 'verdade',
            'lie': 'mentira', 'secret': 'segredo', 'mystery': 'mistério',
            'adventure': 'aventura', 'drama': 'drama', 'comedy': 'comédia',
            'thriller': 'suspense', 'horror': 'terror', 'romance': 'romance',
            'fantasy': 'fantasia', 'scifi': 'ficção', 'documentary': 'documentário',
            'animation': 'animação', 'musical': 'musical', 'western': 'faroeste',
            'noir': 'noir', 'epic': 'épico', 'blockbuster': 'blockbuster',
            
            # Direções de roteiro
            'interior': 'interior', 'exterior': 'exterior',
            'day': 'dia', 'night': 'noite', 'morning': 'manhã',
            'afternoon': 'tarde', 'evening': 'noite', 'dawn': 'amanhecer',
            'dusk': 'anoitecer', 'continuous': 'contínuo',
            'later': 'depois', 'moments': 'momentos', 'flashback': 'flashback',
            'dream': 'sonho', 'memory': 'memória', 'fantasy': 'fantasia',
            'closeup': 'close', 'medium': 'médio', 'establishing': 'estabelecimento',
            'overhead': 'aéreo', 'tracking': 'travelling', 'handheld': 'câmera na mão',
            'steadicam': 'steadicam', 'crane': 'grua', 'underwater': 'subaquático',
            
            # Emoções e ações
            'happy': 'feliz', 'sad': 'triste', 'angry': 'bravo',
            'afraid': 'com medo', 'surprised': 'surpreso', 'confused': 'confuso',
            'excited': 'animado', 'nervous': 'nervoso', 'calm': 'calmo',
            'desperate': 'desesperado', 'hopeful': 'esperançoso',
            'run': 'correr', 'walk': 'andar', 'jump': 'pular',
            'fall': 'cair', 'climb': 'escalar', 'swim': 'nadar',
            'fly': 'voar', 'drive': 'dirigir', 'ride': 'cavalgar',
            'fight': 'lutar', 'kiss': 'beijar', 'hug': 'abraçar',
            'cry': 'chorar', 'laugh': 'rir', 'scream': 'gritar',
            'whisper': 'sussurrar', 'sing': 'cantar', 'dance': 'dançar',
            
            # Lugares
            'house': 'casa', 'apartment': 'apartamento', 'building': 'prédio',
            'street': 'rua', 'road': 'estrada', 'highway': 'rodovia',
            'park': 'parque', 'garden': 'jardim', 'forest': 'floresta',
            'beach': 'praia', 'mountain': 'montanha', 'valley': 'vale',
            'river': 'rio', 'lake': 'lago', 'ocean': 'oceano',
            'city': 'cidade', 'town': 'cidade', 'village': 'vila',
            'country': 'país', 'world': 'mundo', 'universe': 'universo',
            'office': 'escritório', 'store': 'loja', 'restaurant': 'restaurante',
            'cafe': 'café', 'bar': 'bar', 'hotel': 'hotel',
            'hospital': 'hospital', 'school': 'escola', 'church': 'igreja',
            'prison': 'prisão', 'castle': 'castelo', 'palace': 'palácio',
            
            # Elementos narrativos
            'story': 'história', 'tale': 'conto', 'legend': 'lenda',
            'myth': 'mito', 'fable': 'fábula', 'saga': 'saga',
            'chapter': 'capítulo', 'verse': 'verso', 'stanza': 'estrofe',
            'paragraph': 'parágrafo', 'sentence': 'frase', 'word': 'palavra',
            'letter': 'letra', 'symbol': 'símbolo', 'sign': 'sinal',
            'meaning': 'significado', 'message': 'mensagem', 'theme': 'tema',
            'moral': 'moral', 'lesson': 'lição', 'purpose': 'propósito',
            'goal': 'objetivo', 'mission': 'missão', 'quest': 'busca',
            'challenge': 'desafio', 'obstacle': 'obstáculo', 'problem': 'problema',
            'solution': 'solução', 'answer': 'resposta', 'question': 'pergunta',
            'doubt': 'dúvida', 'certainty': 'certeza', 'possibility': 'possibilidade',
            
            # Cognatos idênticos
            'hotel': 'hotel', 'hospital': 'hospital', 'animal': 'animal',
            'natural': 'natural', 'social': 'social', 'total': 'total',
            'capital': 'capital', 'central': 'central', 'digital': 'digital',
            'federal': 'federal', 'final': 'final', 'global': 'global',
            'ideal': 'ideal', 'legal': 'legal', 'local': 'local',
            'mental': 'mental', 'moral': 'moral', 'normal': 'normal',
            'oral': 'oral', 'real': 'real', 'rural': 'rural',
            'sexual': 'sexual', 'tropical': 'tropical', 'universal': 'universal',
            'vertical': 'vertical', 'vital': 'vital', 'visual': 'visual',
            'chocolate': 'chocolate', 'cinema': 'cinema', 'drama': 'drama',
            'panorama': 'panorama', 'programa': 'programa', 'sistema': 'sistema',
            'problema': 'problema', 'trauma': 'trauma', 'plasma': 'plasma',
            
            # Cognatos com padrões
            'action': 'ação', 'creation': 'criação', 'emotion': 'emoção',
            'nation': 'nação', 'operation': 'operação', 'situation': 'situação',
            'solution': 'solução', 'tradition': 'tradição', 'translation': 'tradução',
            'condition': 'condição', 'position': 'posição', 'question': 'questão',
            'attention': 'atenção', 'intention': 'intenção', 'dimension': 'dimensão',
            'extension': 'extensão', 'tension': 'tensão', 'version': 'versão',
            'decision': 'decisão', 'division': 'divisão', 'vision': 'visão',
            'television': 'televisão', 'revision': 'revisão', 'provision': 'provisão',
            'ability': 'habilidade', 'activity': 'atividade', 'capacity': 'capacidade',
            'community': 'comunidade', 'difficulty': 'dificuldade', 'facility': 'facilidade',
            'identity': 'identidade', 'quality': 'qualidade', 'reality': 'realidade',
            'responsibility': 'responsabilidade', 'university': 'universidade',
            'velocity': 'velocidade', 'possibility': 'possibilidade',
            'probability': 'probabilidade', 'stability': 'estabilidade'
        }
        
        # Criar mapa bidirecional
        bidirectional = {}
        for en, pt in translations.items():
            bidirectional[en] = pt
            bidirectional[pt] = en
        
        return bidirectional
    
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
                word = symbol[1:-1]
                # Tentar traduzir palavra desconhecida
                if word in self.translation_dict:
                    decompressed.append(self.translation_dict[word])
                else:
                    decompressed.append(word)
                continue
            
            # Remover modificadores morfológicos
            base_symbol = symbol.rstrip('⁺⁻~')
            modifier = symbol[len(base_symbol):]
            
            if base_symbol in self.reverse_dict:
                words = self.reverse_dict[base_symbol]
                
                # Escolher palavra apropriada para o idioma alvo
                chosen_word = None
                
                for word in words:
                    # Se a palavra está no dicionário de tradução
                    if word in self.translation_dict:
                        translated = self.translation_dict[word]
                        if target_lang == 'pt':
                            # Se a tradução parece ser portuguesa
                            if any(c in translated for c in 'áàâãéêíóôõúç') or \
                               any(translated.endswith(end) for end in ['ção', 'são', 'dade', 'mente']):
                                chosen_word = translated
                                break
                        else:  # en
                            # Se não tem acentos, provavelmente é inglês
                            if not any(c in translated for c in 'áàâãéêíóôõúç'):
                                chosen_word = translated
                                break
                
                # Se não encontrou tradução, usar primeira palavra disponível
                if not chosen_word:
                    chosen_word = words[0]
                    # Tentar traduzir
                    if chosen_word in self.translation_dict:
                        chosen_word = self.translation_dict[chosen_word]
                
                # Aplicar modificador morfológico
                if modifier == '⁺':  # Plural
                    chosen_word += 's'
                elif modifier == '⁻':  # Passado
                    if target_lang == 'pt':
                        chosen_word = f"[passado:{chosen_word}]"
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
    
    def direct_translate(self, text, source='en', target='pt'):
        """Tradução direta usando dicionário"""
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
        translated = []
        
        for word in text.split():
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            
            if clean_word in self.translation_dict:
                translated_word = self.translation_dict[clean_word]
                # Preservar capitalização
                if word[0].isupper():
                    translated_word = translated_word.capitalize()
                translated.append(translated_word)
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
        
        # Contar palavras traduzidas corretamente
        correct_translations = 0
        total_words = 0
        
        for w1 in words1:
            if w1 in self.translation_dict:
                expected = self.translation_dict[w1]
                if expected in words2:
                    correct_translations += 1
            total_words += 1
        
        translation_accuracy = (correct_translations / total_words * 100) if total_words > 0 else 0
        
        # Média ponderada
        final_score = (seq_similarity * 0.3 + jaccard * 0.3 + translation_accuracy * 0.4)
        
        return final_score
    
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
            if len(unknown) <= 10:
                print(f"      {unknown}")
        
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
        improvements = []
        
        for word, count in word_freq.most_common(10):
            print(f"   • {word}: {count} ocorrências")
            
            # Sugerir símbolo
            if word not in self.symbols:
                # Encontrar símbolo disponível
                for code in range(0x2600, 0x26FF):
                    symbol = chr(code)
                    if symbol not in self.reverse_dict:
                        improvements.append({
                            'word': word,
                            'symbol': symbol,
                            'reason': 'alta frequência em testes'
                        })
                        print(f"     → Sugestão: adicionar '{word}' com símbolo '{symbol}'")
                        break
        
        self.stats['improvements'] = improvements
        
        # Analisar padrões de erro
        print(f"\n🔍 Padrões identificados:")
        
        if self.stats['avg_coherence'] < 70:
            print("   ⚠️ Coerência baixa - necessário expandir vocabulário bilíngue")
        
        if any(r['coverage'] < 80 for r in test_results):
            print("   ⚠️ Cobertura insuficiente - adicionar mais palavras do domínio")
        
        # Sugestões de melhoria
        print(f"\n💡 Sugestões de otimização:")
        print(f"   1. Adicionar {len(improvements)} palavras frequentes")
        print(f"   2. Melhorar mapeamento de {len(word_freq)} cognatos")
        print(f"   3. Implementar regras morfológicas para {len(all_unknown)} variações")
    
    def save_improvements(self):
        """Salva melhorias no sistema DigiLang"""
        if not self.stats.get('improvements'):
            print("\n✅ Nenhuma melhoria necessária!")
            return
        
        print(f"\n💾 SALVANDO MELHORIAS")
        print(f"{'='*60}")
        
        # Adicionar novas palavras
        added = 0
        for improvement in self.stats['improvements'][:100]:  # Limitar a 100 por vez
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