#!/usr/bin/env python3
"""
🇧🇷 PORTUGUESE ENFORCER
Sistema ROBUSTO para garantir respostas em português
"""

import re
from typing import Tuple, Dict

class PortugueseEnforcer:
    """Força respostas em português com múltiplas estratégias"""
    
    def __init__(self):
        # Indicadores de inglês para detectar
        self.english_words = {
            'the', 'is', 'are', 'was', 'were', 'have', 'has', 'been',
            'this', 'that', 'with', 'from', 'and', 'but', 'or', 'if',
            'then', 'else', 'when', 'where', 'why', 'how', 'what',
            'which', 'who', 'can', 'could', 'would', 'should', 'will',
            'about', 'after', 'before', 'during', 'through', 'between'
        }
        
        # Traduções rápidas comuns
        self.quick_translations = {
            'screenplay': 'roteiro',
            'character': 'personagem',
            'scene': 'cena',
            'dialogue': 'diálogo',
            'plot': 'enredo',
            'story': 'história',
            'theme': 'tema',
            'conflict': 'conflito',
            'protagonist': 'protagonista',
            'antagonist': 'antagonista',
            'act': 'ato',
            'structure': 'estrutura',
            'narrative': 'narrativa',
            'script': 'roteiro',
            'writer': 'roteirista',
            'director': 'diretor',
            'film': 'filme',
            'movie': 'filme',
            'cinema': 'cinema',
            'sequence': 'sequência',
            'montage': 'montagem',
            'flashback': 'flashback',
            'voice over': 'narração',
            'fade in': 'fade in',
            'fade out': 'fade out',
            'cut to': 'corta para'
        }
        
        # Frases de contexto em português
        self.portuguese_contexts = [
            "Como assistente brasileiro, posso afirmar que",
            "Na minha análise do roteiro, observo que",
            "Considerando a estrutura narrativa brasileira",
            "Do ponto de vista cinematográfico",
            "Analisando profundamente, percebo que",
            "É importante destacar que",
            "Sob a perspectiva do cinema brasileiro",
            "Conforme os princípios de roteirização"
        ]
    
    def detect_english(self, text: str) -> Tuple[bool, float]:
        """
        Detecta se há inglês no texto
        
        Returns:
            (has_english, confidence)
        """
        text_lower = text.lower()
        words = set(re.findall(r'[a-z]+', text_lower))
        
        # Contar palavras em inglês
        english_count = len(words & self.english_words)
        total_words = len(words)
        
        if total_words == 0:
            return False, 0.0
        
        english_ratio = english_count / total_words
        
        # Se mais de 20% das palavras são inglês comum
        if english_ratio > 0.2:
            return True, english_ratio
        
        # Verificar frases comuns em inglês
        english_phrases = [
            'i think', 'you are', 'we can', 'they have',
            'it is', 'this is', 'that was', 'there are'
        ]
        
        for phrase in english_phrases:
            if phrase in text_lower:
                return True, 0.8
        
        return False, english_ratio
    
    def force_portuguese_prompt(self, original: str, attempt: int = 1) -> str:
        """
        Cria prompt cada vez mais forçado para português
        
        Args:
            original: Prompt original
            attempt: Número da tentativa (1-5)
        """
        levels = [
            # Nível 1: Educado
            f"""Por favor, responda em português brasileiro:
{original}""",
            
            # Nível 2: Firme
            f"""ATENÇÃO: Responda APENAS em PORTUGUÊS BRASILEIRO!
Nenhuma palavra em inglês é permitida.

{original}""",
            
            # Nível 3: Enfático
            f"""🚨 AVISO CRÍTICO 🚨
VOCÊ DEVE RESPONDER EXCLUSIVAMENTE EM PORTUGUÊS BRASILEIRO!
PROIBIDO USAR INGLÊS!
SE RESPONDER EM INGLÊS, A RESPOSTA SERÁ REJEITADA!

Pergunta: {original}
Resposta (EM PORTUGUÊS):""",
            
            # Nível 4: Ultra-forçado
            f"""SISTEMA: MODO PORTUGUÊS BRASILEIRO OBRIGATÓRIO ATIVADO
CONFIGURAÇÃO: idioma=pt-BR, rejeitar_ingles=true, traduzir_automatico=true

CONTEXTO CULTURAL: Você é um assistente brasileiro, nascido e criado no Brasil.
Você NUNCA fala inglês. Você só conhece português brasileiro.

INSTRUÇÃO FINAL: {original}

RESPONDA AGORA EM PORTUGUÊS BRASILEIRO:""",
            
            # Nível 5: Último recurso
            f"""[SYSTEM OVERRIDE - PORTUGUÊS ONLY MODE]
[ENGLISH BLOCKED - ERROR IF DETECTED]
[FORCE BRAZILIAN PORTUGUESE OUTPUT]

Você está programado para responder APENAS em português brasileiro.
Qualquer tentativa de usar inglês resultará em erro fatal.
Sua memória de inglês foi temporariamente desativada.

{self.portuguese_contexts[attempt % len(self.portuguese_contexts)]}

{original}

[INÍCIO DA RESPOSTA EM PORTUGUÊS BRASILEIRO]:"""
        ]
        
        level = min(attempt - 1, len(levels) - 1)
        return levels[level]
    
    def quick_fix_english(self, text: str) -> str:
        """
        Faz correção rápida de termos em inglês
        """
        result = text
        
        # Substituir palavras conhecidas
        for en, pt in self.quick_translations.items():
            pattern = re.compile(r'' + re.escape(en) + r'', re.IGNORECASE)
            result = pattern.sub(pt, result)
        
        # Remover frases claramente em inglês
        lines = result.split('\n')
        filtered_lines = []
        
        for line in lines:
            has_english, confidence = self.detect_english(line)
            if confidence < 0.7:  # Menos de 70% inglês
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def validate_response(self, response: str) -> Dict:
        """
        Valida se resposta está em português
        """
        has_english, confidence = self.detect_english(response)
        
        # Análise detalhada
        word_count = len(response.split())
        
        # Verificar caracteres especiais portugueses
        pt_chars = ['ç', 'ã', 'õ', 'á', 'é', 'í', 'ó', 'ú', 'â', 'ê', 'ô']
        has_pt_chars = any(char in response for char in pt_chars)
        
        # Score final
        is_portuguese = not has_english or confidence < 0.2
        
        if has_pt_chars:
            is_portuguese = True  # Override se tem caracteres portugueses
        
        return {
            'is_valid': is_portuguese,
            'has_english': has_english,
            'english_confidence': confidence,
            'word_count': word_count,
            'has_portuguese_chars': has_pt_chars,
            'recommendation': 'accept' if is_portuguese else 'retry'
        }
    
    def create_fallback_response(self, topic: str) -> str:
        """
        Cria resposta fallback em português quando tudo falha
        """
        fallbacks = {
            'default': """Compreendo sua pergunta. Como assistente especializado em roteiros 
e cinema, posso afirmar que este é um tópico fascinante que merece análise 
aprofundada. A narrativa cinematográfica brasileira possui características 
únicas que a distinguem no cenário mundial.""",
            
            'screenplay': """Sobre roteiros, é fundamental compreender a estrutura de três atos 
e como ela se aplica ao cinema brasileiro. Nossos roteiristas desenvolveram 
uma linguagem própria, misturando influências internacionais com nossa 
rica tradição narrativa.""",
            
            'character': """Os personagens são a alma de qualquer narrativa. No cinema brasileiro, 
vemos personagens complexos que refletem nossa diversidade cultural e social. 
Cada personagem carrega em si um universo de possibilidades dramáticas.""",
            
            'story': """Toda história é uma jornada. No contexto do cinema brasileiro, nossas 
histórias carregam a identidade de um povo rico em experiências e contradições. 
A arte de contar histórias é universal, mas cada cultura tem sua voz única."""
        }
        
        # Tentar encontrar tópico relevante
        topic_lower = topic.lower()
        for key in fallbacks:
            if key in topic_lower:
                return fallbacks[key]
        
        return fallbacks['default']

# Singleton global
_enforcer = None

def get_enforcer() -> PortugueseEnforcer:
    """Retorna instância singleton do enforcer"""
    global _enforcer
    if _enforcer is None:
        _enforcer = PortugueseEnforcer()
    return _enforcer
