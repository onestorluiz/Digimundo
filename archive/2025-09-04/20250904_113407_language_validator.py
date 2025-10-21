#!/usr/bin/env python3
"""
🌐 LANGUAGE VALIDATOR - Validador ROBUSTO de Idioma
Garante respostas em português com fallback de tradução
"""

import re
from typing import Dict, Tuple, Optional
from collections import Counter

class LanguageValidator:
    """Validador e corretor ROBUSTO de idioma para garantir PT-BR"""
    
    def __init__(self):
        # Indicadores ROBUSTOS de idioma
        self.portuguese_indicators = {
            # Palavras mais comuns
            'high_frequency': ['é', 'que', 'não', 'com', 'para', 'de', 'em', 'uma', 
                              'um', 'por', 'se', 'mas', 'ou', 'como', 'mais', 'foi',
                              'são', 'dos', 'das', 'na', 'no', 'isso', 'este', 'esta'],
            
            # Caracteres especiais PT
            'special_chars': ['ç', 'ã', 'õ', 'á', 'é', 'í', 'ó', 'ú', 'â', 'ê', 'ô'],
            
            # Construções típicas
            'constructions': ['está', 'estão', 'você', 'vocês', 'através', 'também',
                            'já', 'ainda', 'então', 'porque', 'porém', 'todavia'],
            
            # Termos de cinema em PT
            'cinema_terms': ['roteiro', 'cena', 'personagem', 'diálogo', 'ação',
                           'direção', 'montagem', 'fotografia', 'trilha', 'filme']
        }
        
        self.english_indicators = {
            'high_frequency': ['the', 'is', 'are', 'was', 'were', 'have', 'has',
                              'this', 'that', 'with', 'from', 'and', 'but', 'or',
                              'if', 'then', 'else', 'when', 'where', 'why', 'how'],
            
            'constructions': ['have been', 'has been', 'will be', 'would be',
                            'could be', 'should be', "I'm", "you're", "it's"],
            
            'cinema_terms': ['screenplay', 'scene', 'character', 'dialogue', 'action',
                           'director', 'editing', 'cinematography', 'soundtrack']
        }
        
        # Dicionário de tradução básica para fallback
        self.translation_dict = {
            'the': 'o/a', 'is': 'é', 'are': 'são', 'was': 'foi/era', 
            'were': 'foram/eram', 'have': 'ter/tem', 'has': 'tem',
            'this': 'este/esta', 'that': 'aquele/aquela', 'with': 'com',
            'from': 'de', 'and': 'e', 'but': 'mas', 'or': 'ou',
            'screenplay': 'roteiro', 'scene': 'cena', 'character': 'personagem',
            'dialogue': 'diálogo', 'action': 'ação', 'director': 'diretor',
            'story': 'história', 'plot': 'enredo', 'theme': 'tema',
            'conflict': 'conflito', 'resolution': 'resolução'
        }
    
    def detect_language(self, text: str) -> Tuple[str, float, Dict]:
        """
        Detecta idioma do texto com análise ROBUSTA
        
        Returns:
            (idioma, confiança, detalhes)
        """
        if not text:
            return ('unknown', 0.0, {})
        
        text_lower = text.lower()
        text_sample = text_lower[:1000]  # Analisar primeiro 1000 chars
        
        # Contadores
        pt_score = 0
        en_score = 0
        details = {
            'pt_words': [],
            'en_words': [],
            'special_chars': [],
            'sample_size': len(text_sample)
        }
        
        # 1. Verificar palavras de alta frequência
        words = re.findall(r'\b\w+\b', text_sample)
        word_freq = Counter(words)
        
        for word, count in word_freq.most_common(20):
            if word in self.portuguese_indicators['high_frequency']:
                pt_score += count * 2
                details['pt_words'].append(word)
            elif word in self.english_indicators['high_frequency']:
                en_score += count * 2
                details['en_words'].append(word)
        
        # 2. Verificar caracteres especiais
        for char in self.portuguese_indicators['special_chars']:
            if char in text_sample:
                pt_score += 5
                details['special_chars'].append(char)
        
        # 3. Verificar construções
        for construction in self.portuguese_indicators['constructions']:
            if construction in text_sample:
                pt_score += 3
                
        for construction in self.english_indicators['constructions']:
            if construction in text_sample:
                en_score += 3
        
        # 4. Verificar termos de cinema
        for term in self.portuguese_indicators['cinema_terms']:
            if term in text_sample:
                pt_score += 4
                
        for term in self.english_indicators['cinema_terms']:
            if term in text_sample:
                en_score += 4
        
        # Calcular confiança
        total_score = pt_score + en_score
        if total_score == 0:
            return ('unknown', 0.0, details)
        
        pt_confidence = pt_score / total_score
        
        # Determinar idioma
        if pt_confidence > 0.6:
            return ('pt-br', pt_confidence, details)
        elif pt_confidence < 0.4:
            return ('en', 1 - pt_confidence, details)
        else:
            return ('mixed', 0.5, details)
    
    def validate_portuguese(self, text: str, min_confidence: float = 0.6) -> bool:
        """
        Valida se o texto está em português com confiança mínima
        """
        language, confidence, _ = self.detect_language(text)
        return language == 'pt-br' and confidence >= min_confidence
    
    def force_portuguese_prompt(self, original_prompt: str, attempt: int = 1) -> str:
        """
        Cria prompt FORÇADO para português baseado na tentativa
        """
        prefixes = [
            # Tentativa 1 - Gentil
            "Por favor, responda em português brasileiro:\n\n",
            
            # Tentativa 2 - Firme
            "ATENÇÃO: Responda APENAS em PORTUGUÊS BRASILEIRO!\n\n",
            
            # Tentativa 3 - Enfático
            """🚨 IMPORTANTE 🚨
VOCÊ DEVE RESPONDER EXCLUSIVAMENTE EM PORTUGUÊS BRASILEIRO!
NENHUMA PALAVRA EM INGLÊS É PERMITIDA!

""",
            
            # Tentativa 4 - Contexto completo
            """CONTEXTO OBRIGATÓRIO:
- Idioma: PORTUGUÊS BRASILEIRO
- Proibido: Qualquer palavra em inglês
- Obrigatório: Resposta 100% em português
- Você é SCRIPTUREMON, assistente brasileiro

PERGUNTA EM PORTUGUÊS:
"""
        ]
        
        prefix_index = min(attempt - 1, len(prefixes) - 1)
        return prefixes[prefix_index] + original_prompt
    
    def quick_translate_fallback(self, text: str) -> str:
        """
        Tradução rápida de fallback para termos básicos
        """
        result = text
        
        # Traduzir termos conhecidos
        for en_term, pt_term in self.translation_dict.items():
            # Case insensitive replacement
            pattern = re.compile(re.escape(en_term), re.IGNORECASE)
            result = pattern.sub(pt_term, result)
        
        # Adicionar nota sobre tradução
        if result != text:
            result = f"[Resposta traduzida automaticamente]\n\n{result}"
        
        return result
    
    def analyze_response_quality(self, response: str) -> Dict:
        """
        Análise completa da qualidade da resposta
        """
        language, confidence, details = self.detect_language(response)
        
        # Análise adicional
        analysis = {
            'language': language,
            'confidence': confidence,
            'is_portuguese': language == 'pt-br',
            'word_count': len(response.split()),
            'char_count': len(response),
            'has_special_chars': len(details.get('special_chars', [])) > 0,
            'pt_word_ratio': len(details.get('pt_words', [])) / max(1, len(details.get('pt_words', []) + details.get('en_words', []))),
            'quality_score': 0.0
        }
        
        # Calcular score de qualidade
        if analysis['is_portuguese']:
            analysis['quality_score'] = confidence
        else:
            analysis['quality_score'] = 0.0
        
        # Ajustar por tamanho (respostas muito curtas podem ter detecção imprecisa)
        if analysis['word_count'] < 10:
            analysis['quality_score'] *= 0.8
            analysis['note'] = 'Resposta muito curta para análise precisa'
        
        return analysis

# Singleton global
_validator = None

def get_language_validator() -> LanguageValidator:
    """Retorna instância singleton do validador"""
    global _validator
    if _validator is None:
        _validator = LanguageValidator()
    return _validator