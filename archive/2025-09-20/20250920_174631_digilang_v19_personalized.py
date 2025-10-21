#!/usr/bin/env python3
"""
FASE 19 - DigiLang Personalizado
Sistema de compressão personalizada por documento

Cada PDF recebe seu próprio dicionário otimizado baseado em:
- Mineração específica do conteúdo
- Análise de frequência personalizada
- Dicionário único por documento

Assinado: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
from dataclasses import dataclass
import PyPDF2
import tiktoken

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PersonalizedDictionary:
    """Dicionário personalizado para um documento"""
    document_path: str
    patterns: Dict[str, str]  # pattern -> symbol
    frequencies: Dict[str, int]  # pattern -> count
    token_savings: int
    compression_rate: float
    document_type: str  # screenplay, book, mixed

class DigiLangV19Personalized:
    """DigiLang Personalizado - Compressão específica por documento"""
    
    def __init__(self):
        """Inicializar sistema personalizado"""
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
        # Pool de símbolos Unicode que garantidamente são 1 token
        self.symbol_pool = self._create_symbol_pool()
        
        # Cache de dicionários personalizados
        self.dictionaries_cache = {}
        
        logger.info("🎯 DigiLang V19 Personalizado inicializado")
    
    def _create_symbol_pool(self) -> List[str]:
        """Criar pool de símbolos de 1 token validados"""
        pool = []
        
        # Símbolos validados como 1 token
        ranges = [
            (0x00A1, 0x00FF),  # Latin-1 Supplement
            (0x0100, 0x017F),  # Latin Extended-A
            (0x0180, 0x024F),  # Latin Extended-B
            (0x1E00, 0x1EFF),  # Latin Extended Additional
            (0x2070, 0x209F),  # Superscripts and Subscripts
            (0x2100, 0x214F),  # Letterlike Symbols
            (0x2190, 0x21FF),  # Arrows
            (0x2200, 0x22FF),  # Mathematical Operators
            (0x2300, 0x23FF),  # Miscellaneous Technical
            (0x2460, 0x24FF),  # Enclosed Alphanumerics
            (0x2500, 0x257F),  # Box Drawing
            (0x2580, 0x259F),  # Block Elements
            (0x25A0, 0x25FF),  # Geometric Shapes
            (0x2600, 0x26FF),  # Miscellaneous Symbols
        ]
        
        for start, end in ranges:
            for codepoint in range(start, end + 1):
                char = chr(codepoint)
                # Validar que é exatamente 1 token
                if len(self.encoder.encode(char)) == 1:
                    pool.append(char)
        
        logger.info(f"📊 Pool de símbolos: {len(pool)} caracteres de 1 token")
        return pool
    
    def analyze_document(self, pdf_path: str) -> Dict:
        """Analisar documento para identificar tipo e padrões"""
        try:
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return None
            
            # Detectar tipo de documento
            doc_type = self._detect_document_type(text)
            
            # Estatísticas básicas
            stats = {
                'total_chars': len(text),
                'total_tokens': len(self.encoder.encode(text)),
                'document_type': doc_type,
                'unique_patterns': 0
            }
            
            logger.info(f"📄 Documento: {Path(pdf_path).name}")
            logger.info(f"📑 Tipo: {doc_type}")
            logger.info(f"📊 Tokens: {stats['total_tokens']:,}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro analisando {pdf_path}: {e}")
            return None
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extrair texto do PDF"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Erro extraindo texto: {e}")
            return ""
    
    def _detect_document_type(self, text: str) -> str:
        """Detectar tipo de documento"""
        # Indicadores de roteiro
        screenplay_indicators = [
            r'FADE IN:', r'FADE OUT', r'CUT TO:', r'INT\.', r'EXT\.',
            r'\([A-Z]+\)', r'CONTINUED:', r'V\.O\.', r'O\.S\.'
        ]
        
        screenplay_score = sum(
            1 for pattern in screenplay_indicators 
            if re.search(pattern, text[:5000])
        )
        
        # Indicadores de livro/documento acadêmico
        book_indicators = [
            r'Chapter \d+', r'Section \d+', r'\d+\.\d+', 
            r'References', r'Bibliography', r'Abstract'
        ]
        
        book_score = sum(
            1 for pattern in book_indicators 
            if re.search(pattern, text[:5000], re.IGNORECASE)
        )
        
        if screenplay_score >= 3:
            return "screenplay"
        elif book_score >= 2:
            return "book"
        else:
            return "mixed"
    
    def mine_document_patterns(self, pdf_path: str) -> Dict:
        """Minerar padrões específicos do documento"""
        try:
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return {}
            
            doc_type = self._detect_document_type(text)
            
            # Coletar todos os padrões
            all_patterns = Counter()
            
            # 1. Nomes de personagens (maiúsculas)
            if doc_type == "screenplay":
                character_pattern = r'^[A-Z][A-Z\s\.]{2,}(?=\n|\(|$)'
                for match in re.finditer(character_pattern, text, re.MULTILINE):
                    name = match.group().strip()
                    if 2 < len(name) < 20:  # Filtrar nomes válidos
                        all_patterns[name] += 1
            
            # 2. Localizações
            location_pattern = r'(?:INT\.|EXT\.)\s+([A-Z][A-Z\s\-]+)'
            for match in re.finditer(location_pattern, text):
                location = match.group(1).strip()
                if location:
                    all_patterns[f"LOC:{location}"] += 1
            
            # 3. Palavras frequentes (3+ caracteres)
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
            word_freq = Counter(words)
            
            # Adicionar palavras mais frequentes
            for word, count in word_freq.most_common(200):
                if count > 5:  # Mínimo de 5 ocorrências
                    all_patterns[word] += count
            
            # 4. Frases e expressões recorrentes
            # Buscar padrões de 2-4 palavras
            sentences = text.split('.')
            phrase_counter = Counter()
            
            for sentence in sentences:
                words = sentence.split()
                # Bigrams
                for i in range(len(words) - 1):
                    phrase = ' '.join(words[i:i+2])
                    if 5 < len(phrase) < 30:
                        phrase_counter[phrase] += 1
                
                # Trigrams
                for i in range(len(words) - 2):
                    phrase = ' '.join(words[i:i+3])
                    if 8 < len(phrase) < 40:
                        phrase_counter[phrase] += 1
            
            # Adicionar frases frequentes
            for phrase, count in phrase_counter.most_common(100):
                if count > 3:
                    all_patterns[phrase] += count
            
            # 5. Padrões técnicos do formato
            technical_patterns = [
                'FADE IN:', 'FADE OUT', 'CUT TO:', 'CONTINUED:',
                'V.O.', 'O.S.', 'CLOSE ON:', 'ANGLE ON:',
                'BACK TO:', 'LATER', 'MOMENTS LATER'
            ]
            
            for pattern in technical_patterns:
                count = text.count(pattern)
                if count > 0:
                    all_patterns[pattern] = count
            
            logger.info(f"⛏️ Minerados {len(all_patterns)} padrões únicos")
            
            return dict(all_patterns)
            
        except Exception as e:
            logger.error(f"Erro na mineração: {e}")
            return {}
    
    def create_personalized_dictionary(
        self, 
        pdf_path: str,
        max_patterns: int = 500
    ) -> PersonalizedDictionary:
        """Criar dicionário personalizado para o documento"""
        
        logger.info(f"\n🎯 Criando dicionário personalizado para: {Path(pdf_path).name}")
        
        # Minerar padrões
        patterns = self.mine_document_patterns(pdf_path)
        if not patterns:
            logger.error("Falha na mineração de padrões")
            return None
        
        # Calcular economia de tokens para cada padrão
        pattern_savings = []
        
        for pattern, frequency in patterns.items():
            original_tokens = len(self.encoder.encode(pattern))
            if original_tokens > 1:  # Só vale a pena se usar mais de 1 token
                # Economia = (tokens_originais - 1) * frequência
                savings = (original_tokens - 1) * frequency
                pattern_savings.append((pattern, frequency, savings))
        
        # Ordenar por economia de tokens
        pattern_savings.sort(key=lambda x: x[2], reverse=True)
        
        # Selecionar os melhores padrões
        selected_patterns = pattern_savings[:min(max_patterns, len(self.symbol_pool))]
        
        # Criar mapeamento padrão -> símbolo
        dictionary = {}
        frequencies = {}
        total_savings = 0
        
        for i, (pattern, freq, savings) in enumerate(selected_patterns):
            if i < len(self.symbol_pool):
                symbol = self.symbol_pool[i]
                dictionary[pattern] = symbol
                frequencies[pattern] = freq
                total_savings += savings
        
        # Calcular texto original
        text = self._extract_pdf_text(pdf_path)
        original_tokens = len(self.encoder.encode(text))
        
        # Estimar compressão
        compression_rate = (total_savings / original_tokens * 100) if original_tokens > 0 else 0
        
        # Detectar tipo
        doc_type = self._detect_document_type(text)
        
        logger.info(f"📊 Dicionário criado:")
        logger.info(f"   - Padrões: {len(dictionary)}")
        logger.info(f"   - Economia estimada: {total_savings:,} tokens")
        logger.info(f"   - Taxa de compressão: {compression_rate:.2f}%")
        
        # Mostrar top 10 padrões
        logger.info("\n🔝 Top 10 padrões por economia:")
        for pattern, freq, savings in selected_patterns[:10]:
            symbol = dictionary.get(pattern, '?')
            logger.info(f"   '{pattern[:30]}' ({freq}x) → '{symbol}' = {savings} tokens salvos")
        
        return PersonalizedDictionary(
            document_path=pdf_path,
            patterns=dictionary,
            frequencies=frequencies,
            token_savings=total_savings,
            compression_rate=compression_rate,
            document_type=doc_type
        )
    
    def compress_with_dictionary(
        self, 
        text: str, 
        dictionary: PersonalizedDictionary
    ) -> Tuple[str, Dict]:
        """Comprimir texto usando dicionário personalizado"""
        
        compressed = text
        replacements = 0
        
        # Ordenar padrões por tamanho (maiores primeiro)
        sorted_patterns = sorted(
            dictionary.patterns.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        # Aplicar substituições
        for pattern, symbol in sorted_patterns:
            count = compressed.count(pattern)
            if count > 0:
                compressed = compressed.replace(pattern, symbol)
                replacements += count
        
        # Calcular estatísticas
        original_tokens = len(self.encoder.encode(text))
        compressed_tokens = len(self.encoder.encode(compressed))
        
        stats = {
            'original_chars': len(text),
            'compressed_chars': len(compressed),
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'replacements': replacements,
            'patterns_used': len([p for p in dictionary.patterns if p in text]),
            'char_compression': ((len(text) - len(compressed)) / len(text) * 100) if len(text) > 0 else 0,
            'token_compression': ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0
        }
        
        return compressed, stats
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """Processar PDF com compressão personalizada"""
        
        try:
            # Analisar documento
            analysis = self.analyze_document(pdf_path)
            if not analysis:
                return None
            
            # Criar dicionário personalizado
            dictionary = self.create_personalized_dictionary(pdf_path)
            if not dictionary:
                return None
            
            # Extrair e comprimir texto
            text = self._extract_pdf_text(pdf_path)
            compressed_text, stats = self.compress_with_dictionary(text, dictionary)
            
            # Salvar dicionário no cache
            self.dictionaries_cache[pdf_path] = dictionary
            
            logger.info(f"\n✅ Compressão personalizada concluída:")
            logger.info(f"   - Tokens: {stats['original_tokens']:,} → {stats['compressed_tokens']:,}")
            logger.info(f"   - Compressão: {stats['token_compression']:.2f}%")
            logger.info(f"   - Padrões usados: {stats['patterns_used']}")
            
            return {
                'success': True,
                'compressed_text': compressed_text,
                'dictionary': dictionary.patterns,
                'stats': stats,
                'document_info': {
                    'path': pdf_path,
                    'type': dictionary.document_type,
                    'dictionary_size': len(dictionary.patterns)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro processando {pdf_path}: {e}")
            return None
    
    def decompress_with_dictionary(
        self,
        compressed_text: str,
        dictionary: Dict[str, str]
    ) -> str:
        """Descomprimir texto usando dicionário"""
        
        # Criar dicionário reverso
        reverse_dict = {v: k for k, v in dictionary.items()}
        
        # Ordenar símbolos por tamanho do padrão original (maiores primeiro)
        sorted_symbols = sorted(
            reverse_dict.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        # Aplicar substituições reversas
        decompressed = compressed_text
        for symbol, pattern in sorted_symbols:
            decompressed = decompressed.replace(symbol, pattern)
        
        return decompressed


def main():
    """Função de teste"""
    print("🌟 FASE 19 - DigiLang Personalizado")
    print("Compressão específica por documento")
    print("=" * 50)
    
    # Testar com The Dark Knight
    pdf_path = "./digilibrary/The Dark Knight - Release.pdf"
    
    v19 = DigiLangV19Personalized()
    result = v19.process_pdf(pdf_path)
    
    if result:
        print(f"\n✅ Sucesso!")
        print(f"Compressão: {result['stats']['token_compression']:.2f}%")
        print(f"Dicionário: {result['document_info']['dictionary_size']} padrões")
        
        # Testar descompressão
        decompressed = v19.decompress_with_dictionary(
            result['compressed_text'],
            result['dictionary']
        )
        
        # Verificar integridade
        original_text = v19._extract_pdf_text(pdf_path)
        if decompressed == original_text:
            print("✅ Descompressão perfeita!")
        else:
            print("⚠️ Descompressão com diferenças")
    else:
        print("❌ Falhou")
    
    return 0

if __name__ == "__main__":
    main()