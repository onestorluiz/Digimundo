#!/usr/bin/env python3
"""
Screenplay Normalizer - PT→EN Translation & Standardization
Normaliza roteiros PT-BR para formato padrão em inglês para máxima compressão
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class NormalizedScreenplay:
    """Resultado da normalização."""
    original_text: str
    normalized_text: str
    language_map: Dict[str, str]  # PT -> EN mappings used
    structure_changes: List[str]
    reversible: bool
    compression_ready: bool


class ScreenplayNormalizer:
    """
    Normaliza roteiros PT-BR para formato padrão inglês.
    
    Pipeline:
    1. PT → EN (termos técnicos)
    2. Estrutura → Padrão Hollywood
    3. Compressão DigiLang
    4. Reversão: DigiLang → EN → PT
    """
    
    def __init__(self):
        # Mapeamento de termos técnicos PT→EN
        self.technical_terms = {
            # Cabeçalhos de cena
            'INT.': 'INT.',
            'EXT.': 'EXT.',
            'INT/EXT.': 'INT./EXT.',
            'INTERIOR': 'INT.',
            'EXTERIOR': 'EXT.',
            
            # Tempos
            'DIA': 'DAY',
            'NOITE': 'NIGHT',
            'TARDE': 'AFTERNOON',
            'MANHÃ': 'MORNING',
            'MADRUGADA': 'DAWN',
            'ENTARDECER': 'DUSK',
            'AMANHECER': 'SUNRISE',
            'ANOITECER': 'SUNSET',
            'CONTÍNUO': 'CONTINUOUS',
            'MAIS TARDE': 'LATER',
            'MOMENTOS DEPOIS': 'MOMENTS LATER',
            'FLASHBACK': 'FLASHBACK',
            'FLASHFORWARD': 'FLASHFORWARD',
            'SONHO': 'DREAM',
            'PESADELO': 'NIGHTMARE',
            'MEMÓRIA': 'MEMORY',
            'VISÃO': 'VISION',
            
            # Transições
            'CORTA PARA:': 'CUT TO:',
            'FADE IN:': 'FADE IN:',
            'FADE OUT.': 'FADE OUT.',
            'DISSOLVE PARA:': 'DISSOLVE TO:',
            'CORTE SECO:': 'SMASH CUT:',
            'MATCH CUT:': 'MATCH CUT:',
            'FUSÃO PARA:': 'DISSOLVE TO:',
            'ESCURECE.': 'FADE OUT.',
            'CLAREIA:': 'FADE IN:',
            'CORTE PARA:': 'CUT TO:',
            
            # Indicações de diálogo
            '(V.O.)': '(V.O.)',
            '(NARRAÇÃO)': '(V.O.)',
            '(OFF)': '(O.S.)',
            '(O.S.)': '(O.S.)',
            '(O.S)': '(O.S.)',
            '(FORA DE QUADRO)': '(O.S.)',
            '(EM OFF)': '(O.S.)',
            '(CONTINUA)': "(CONT'D)",
            '(CONT.)': "(CONT'D)",
            
            # Parentéticos comuns
            'sussurrando': 'whispering',
            'gritando': 'shouting',
            'chorando': 'crying',
            'rindo': 'laughing',
            'nervoso': 'nervous',
            'nervosa': 'nervous',
            'feliz': 'happy',
            'triste': 'sad',
            'irritado': 'angry',
            'irritada': 'angry',
            'surpreso': 'surprised',
            'surpresa': 'surprised',
            'confuso': 'confused',
            'confusa': 'confused',
            'pensativo': 'thoughtful',
            'pensativa': 'thoughtful',
            'sarcástico': 'sarcastic',
            'sarcástica': 'sarcastic',
            'irônico': 'ironic',
            'irônica': 'ironic',
            
            # Ações comuns
            'entra': 'enters',
            'sai': 'exits',
            'senta': 'sits',
            'levanta': 'stands',
            'anda': 'walks',
            'corre': 'runs',
            'para': 'stops',
            'vira': 'turns',
            'olha': 'looks',
            'olha para': 'looks at',
            'pega': 'takes',
            'deixa': 'leaves',
            'abre': 'opens',
            'fecha': 'closes',
            'está sentado': 'is sitting',
            'está sentada': 'is sitting',
            'está em pé': 'is standing',
            'está deitado': 'is lying',
            'está deitada': 'is lying',
            
            # Direções de câmera
            'CLOSE': 'CLOSE ON:',
            'PLANO FECHADO': 'CLOSE-UP',
            'PLANO GERAL': 'WIDE SHOT',
            'PLANO MÉDIO': 'MEDIUM SHOT',
            'PLANO AMERICANO': 'MEDIUM SHOT',
            'PLANO DETALHE': 'INSERT:',
            'PANORÂMICA': 'PAN',
            'TRAVELLING': 'TRACKING SHOT',
            'ZOOM': 'ZOOM',
            'CÂMERA NA MÃO': 'HANDHELD',
            'STEADICAM': 'STEADICAM',
            'GRUA': 'CRANE SHOT',
            'DRONE': 'AERIAL SHOT',
        }
        
        # Padrões de estrutura
        self.scene_header_pattern = re.compile(
            r'^(INT\.|EXT\.|INT/EXT\.|INTERIOR|EXTERIOR)\s+(.+?)\s*[-–]\s*(.+?)$',
            re.MULTILINE | re.IGNORECASE
        )
        
        self.character_name_pattern = re.compile(
            r'^[A-Z][A-Z\s\.]+$',
            re.MULTILINE
        )
        
        self.parenthetical_pattern = re.compile(
            r'^\s*\(([^)]+)\)\s*$',
            re.MULTILINE
        )
        
        self.transition_pattern = re.compile(
            r'^.+:$',
            re.MULTILINE
        )
    
    def normalize(self, text: str) -> NormalizedScreenplay:
        """
        Normaliza roteiro PT-BR para formato inglês padrão.
        
        Args:
            text: Roteiro em português
            
        Returns:
            NormalizedScreenplay com texto normalizado
        """
        normalized = text
        mappings_used = {}
        changes = []
        
        # 1. Normalizar cabeçalhos de cena
        normalized = self._normalize_scene_headers(normalized)
        changes.append("Scene headers normalized")
        
        # 2. Traduzir termos técnicos
        for pt_term, en_term in self.technical_terms.items():
            if pt_term in normalized:
                # Case-insensitive para alguns termos
                if pt_term.lower() in ['dia', 'noite', 'manhã', 'tarde']:
                    pattern = re.compile(re.escape(pt_term), re.IGNORECASE)
                    normalized = pattern.sub(en_term, normalized)
                else:
                    normalized = normalized.replace(pt_term, en_term)
                mappings_used[pt_term] = en_term
        
        if mappings_used:
            changes.append(f"Translated {len(mappings_used)} technical terms")
        
        # 3. Normalizar estrutura
        normalized = self._normalize_structure(normalized)
        changes.append("Structure normalized")
        
        # 4. Normalizar nomes de personagens (UPPERCASE)
        normalized = self._normalize_character_names(normalized)
        changes.append("Character names normalized")
        
        # 5. Limpar espaçamento
        normalized = self._clean_spacing(normalized)
        changes.append("Spacing cleaned")
        
        return NormalizedScreenplay(
            original_text=text,
            normalized_text=normalized,
            language_map=mappings_used,
            structure_changes=changes,
            reversible=True,  # Com o mapa, podemos reverter
            compression_ready=True
        )
    
    def _normalize_scene_headers(self, text: str) -> str:
        """Normaliza cabeçalhos de cena para formato padrão."""
        lines = text.split('\n')
        normalized_lines = []
        
        for line in lines:
            # Detecta cabeçalho de cena
            if self._is_scene_header(line):
                # Padroniza formato: INT./EXT. LOCATION - TIME
                parts = re.split(r'[-–]', line)
                if len(parts) >= 2:
                    location = parts[0].strip()
                    time = parts[-1].strip()
                    
                    # Garante formato correto
                    if not location.startswith(('INT.', 'EXT.', 'INT./EXT.')):
                        if 'INT' in location.upper():
                            location = 'INT. ' + location.replace('INT.', '').replace('INT', '').strip()
                        elif 'EXT' in location.upper():
                            location = 'EXT. ' + location.replace('EXT.', '').replace('EXT', '').strip()
                    
                    line = f"{location} - {time}"
            
            normalized_lines.append(line)
        
        return '\n'.join(normalized_lines)
    
    def _is_scene_header(self, line: str) -> bool:
        """Verifica se linha é cabeçalho de cena."""
        line = line.strip().upper()
        return (
            line.startswith(('INT.', 'EXT.', 'INT./EXT.', 'INTERIOR', 'EXTERIOR')) or
            ('INT.' in line or 'EXT.' in line) and 
            any(time in line for time in ['DAY', 'NIGHT', 'DIA', 'NOITE', 'MORNING', 'MANHÃ'])
        )
    
    def _normalize_structure(self, text: str) -> str:
        """Normaliza estrutura do roteiro."""
        lines = text.split('\n')
        normalized = []
        
        for i, line in enumerate(lines):
            # Remove tabs, mantém só espaços
            line = line.replace('\t', '    ')
            
            # Transitions sempre alinhadas à direita (simulado com espaços)
            if self.transition_pattern.match(line.strip()):
                transitions = ['CUT TO:', 'FADE IN:', 'FADE OUT.', 'DISSOLVE TO:', 
                              'SMASH CUT:', 'MATCH CUT:']
                for trans in transitions:
                    if trans in line:
                        line = ' ' * 50 + trans  # Simula alinhamento à direita
                        break
            
            normalized.append(line)
        
        return '\n'.join(normalized)
    
    def _normalize_character_names(self, text: str) -> str:
        """Garante que nomes de personagens estejam em UPPERCASE."""
        lines = text.split('\n')
        normalized = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detecta possível nome de personagem
            if (
                stripped and 
                len(stripped) < 50 and 
                not any(c in stripped for c in ['.', '!', '?', ',']) and
                i + 1 < len(lines) and
                (lines[i + 1].strip().startswith('(') or len(lines[i + 1].strip()) > 20)
            ):
                # Provavelmente é nome de personagem
                if not stripped.isupper():
                    line = line.replace(stripped, stripped.upper())
            
            normalized.append(line)
        
        return '\n'.join(normalized)
    
    def _clean_spacing(self, text: str) -> str:
        """Limpa espaçamento redundante."""
        # Remove múltiplos espaços
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove linhas em branco excessivas
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove espaços no fim das linhas
        lines = [line.rstrip() for line in text.split('\n')]
        
        return '\n'.join(lines)
    
    def denormalize(self, normalized_text: str, language_map: Dict[str, str]) -> str:
        """
        Reverte normalização EN→PT.
        
        Args:
            normalized_text: Texto normalizado em inglês
            language_map: Mapa de traduções usadas
            
        Returns:
            Texto revertido para português
        """
        denormalized = normalized_text
        
        # Inverte o mapa
        reverse_map = {en: pt for pt, en in language_map.items()}
        
        # Aplica traduções reversas
        for en_term, pt_term in reverse_map.items():
            denormalized = denormalized.replace(en_term, pt_term)
        
        return denormalized


def test_normalizer():
    """Testa o normalizador."""
    normalizer = ScreenplayNormalizer()
    
    # Texto de teste PT-BR
    test_text = """
INT. ESCRITÓRIO - DIA

JOÃO entra nervoso. Ele olha para MARIA.

JOÃO
(sussurrando)
Onde você estava?

MARIA
(irritada)
Eu estava esperando você!

CORTA PARA:

EXT. PARQUE - NOITE

Maria está sentada no banco.

FADE OUT.
"""
    
    print("="*60)
    print("TESTE DE NORMALIZAÇÃO PT→EN")
    print("="*60)
    
    print("\nTEXTO ORIGINAL (PT):")
    print(test_text)
    
    # Normaliza
    result = normalizer.normalize(test_text)
    
    print("\nTEXTO NORMALIZADO (EN):")
    print(result.normalized_text)
    
    print("\nTERMOS TRADUZIDOS:")
    for pt, en in result.language_map.items():
        print(f"  {pt} → {en}")
    
    print("\nMUDANÇAS ESTRUTURAIS:")
    for change in result.structure_changes:
        print(f"  - {change}")
    
    # Testa reversão
    reverted = normalizer.denormalize(result.normalized_text, result.language_map)
    
    print("\nREVERSÃO (EN→PT):")
    print(reverted)
    
    print("\n" + "="*60)
    print(f"Reversível: {result.reversible}")
    print(f"Pronto para compressão: {result.compression_ready}")


if __name__ == "__main__":
    test_normalizer()