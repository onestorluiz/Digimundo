#!/usr/bin/env python3
"""
DigiLang V3 Token-Aware (TA) - Compressão real de tokens para LLMs
Implementa macro-léxico ASCII com seleção automática por ganho líquido
"""

import re
import json
import argparse
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
from pathlib import Path

try:
    import tiktoken
    TOKENIZER = tiktoken.get_encoding('cl100k_base')
    HAS_TIKTOKEN = True
except ImportError:
    print("⚠️ tiktoken não instalado. Usando fallback aproximado.")
    HAS_TIKTOKEN = False
    TOKENIZER = None

# Semente de macros para roteiros PT-BR
SEED_EXPANSIONS = {
    # Direções de cena / transições
    'FI': 'FADE IN:',
    'FO': 'FADE OUT.',
    'CT': 'CUT TO:',
    'DT': 'DISSOLVE TO:',
    'SC': 'SMASH CUT TO:',
    'MC': 'MATCH CUT TO:',
    'I': 'INT.',
    'E': 'EXT.',
    'IE': 'INT./EXT.',
    'DY': 'DAY',
    'NT': 'NIGHT',
    'CON': 'CONTINUOUS',
    'LAT': 'LATER',
    'ML': 'MOMENTS LATER',
    
    # Marcadores de fala / estilo
    'VO': 'V.O.',
    'OS': 'O.S.',
    'CONT': "CONT'D",
    'FOQ': 'FORA DE QUADRO',
    'EMO': 'EM OFF',
    'NAR': 'NARRAÇÃO',
    'SFX': 'SFX:',
    'MUS': 'MÚSICA:',
    
    # Expressões frequentes de ação (pt-BR)
    'ES': 'está sentado',
    'ESA': 'está sentada',
    'OP': 'olha para',
    'ELEOP': 'Ele olha para',
    'ELAOP': 'Ela olha para',
    'SS': 'sussurrando',
    'CO': 'continua',
    'EN': 'entra',
    'SA': 'sai',
    'LE': 'levanta',
    'SE': 'senta',
    'VI': 'vira',
    'AN': 'anda',
    'COR': 'corre',
    'PA': 'para',
    'PE': 'pega',
    'DE': 'deixa',
    'AB': 'abre',
    'FE': 'fecha',
    
    # Camera/Shot (opcional)
    'CLOSE': 'CLOSE ON:',
    'CU': 'CLOSE-UP',
    'WS': 'WIDE SHOT',
    'MS': 'MEDIUM SHOT',
    'PAN': 'PANORÂMICA',
    'DOL': 'DOLLY',
    'TRAV': 'TRAVELLING',
    'RF': 'RACK FOCUS',
    'CUTAW': 'CUTAWAY',
    'SUPER': 'SUPER:',
    'INTPT': 'INTERTÍTULO:',
    'BG': 'BACKGROUND:',
}


class TokenCounter:
    """Contador de tokens com fallback."""
    
    @staticmethod
    def count(text: str) -> int:
        """Conta tokens usando tiktoken ou aproximação."""
        if HAS_TIKTOKEN and TOKENIZER:
            return len(TOKENIZER.encode(text))
        else:
            # Fallback: aproximação baseada em palavras
            # ~1.3 tokens por palavra em inglês, ~1.5 em português
            words = len(text.split())
            chars = len(text)
            return max(words * 1.4, chars // 4)


class PlaceholderOptimizer:
    """Otimizador de placeholders ASCII."""
    
    FORMATS = [
        '#{id}#',   # Hash
        '@{id}@',   # At
        '[{id}]',   # Brackets
        '<{id}>',   # Angle
        '%%{id}%%', # Percent
    ]
    
    @classmethod
    def find_best_format(cls, macro_id: str, text: str) -> Tuple[str, int]:
        """Encontra o formato de placeholder com menos tokens."""
        best_format = None
        best_tokens = float('inf')
        
        for fmt in cls.FORMATS:
            placeholder = fmt.replace('{id}', macro_id)
            
            # Evita colisão se o placeholder já existe no texto
            if placeholder in text:
                continue
            
            tokens = TokenCounter.count(placeholder)
            if tokens < best_tokens:
                best_tokens = tokens
                best_format = placeholder
        
        return best_format or f'#{macro_id}#', best_tokens


class MacroSelector:
    """Seletor de macros por ganho líquido."""
    
    def __init__(self, text: str, max_macros: int = 64):
        self.text = text
        self.max_macros = max_macros
        self.selected_macros = {}
    
    def analyze_expansions(self) -> List[Tuple[str, str, int, int, float]]:
        """Analisa expansões candidatas e calcula ganhos."""
        candidates = []
        
        for macro_id, expansion in SEED_EXPANSIONS.items():
            # Conta frequência (case-sensitive para preservar semântica)
            freq = self.text.count(expansion)
            
            if freq == 0:
                continue
            
            # Tokens da expansão original
            t_orig = TokenCounter.count(expansion)
            
            # Melhor placeholder
            placeholder, t_macro = PlaceholderOptimizer.find_best_format(
                macro_id, self.text
            )
            
            # Custo do header (definição da macro)
            header_line = f"{placeholder} = \"{expansion}\""
            t_header = TokenCounter.count(header_line)
            
            # Ganho líquido
            gain = freq * (t_orig - t_macro) - t_header
            
            if gain > 0:
                candidates.append((
                    macro_id, placeholder, freq, t_orig, gain
                ))
        
        # Ordena por ganho decrescente
        candidates.sort(key=lambda x: x[4], reverse=True)
        
        return candidates[:self.max_macros]
    
    def select_macros(self) -> Dict[str, Tuple[str, str]]:
        """Seleciona macros com ganho líquido positivo."""
        candidates = self.analyze_expansions()
        
        result = {}
        for macro_id, placeholder, freq, t_orig, gain in candidates:
            expansion = SEED_EXPANSIONS[macro_id]
            result[expansion] = (placeholder, macro_id)
        
        return result


class DigiLangV3Encoder:
    """Encoder token-aware para LLMs."""
    
    def __init__(self, max_macros: int = 64):
        self.max_macros = max_macros
    
    def encode(self, text: str) -> Tuple[str, Dict]:
        """Codifica texto com macros selecionadas automaticamente."""
        
        # Seleciona macros com ganho líquido positivo
        selector = MacroSelector(text, self.max_macros)
        macros = selector.select_macros()
        
        if not macros:
            # Sem ganho, retorna original
            return text, {
                'tokens_original': TokenCounter.count(text),
                'tokens_header': 0,
                'tokens_body': TokenCounter.count(text),
                'tokens_encoded': TokenCounter.count(text),
                'compression_ratio': 0.0,
                'macros_used': 0,
                'gain_net': 0
            }
        
        # Gera header
        header_lines = ['MACROS_BEGIN']
        for expansion, (placeholder, macro_id) in macros.items():
            header_lines.append(f'{placeholder} = "{expansion}"')
        header_lines.append('MACROS_END')
        header = '\n'.join(header_lines)
        
        # Codifica corpo (greedy, maior match primeiro)
        encoded_body = text
        replacements = sorted(
            macros.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        for expansion, (placeholder, _) in replacements:
            encoded_body = encoded_body.replace(expansion, placeholder)
        
        # Resultado completo
        encoded_full = f"{header}\n\n{encoded_body}"
        
        # Métricas
        tokens_original = TokenCounter.count(text)
        tokens_header = TokenCounter.count(header)
        tokens_body = TokenCounter.count(encoded_body)
        tokens_total = tokens_header + tokens_body + 2  # +2 para \n\n
        
        stats = {
            'tokens_original': tokens_original,
            'tokens_header': tokens_header,
            'tokens_body': tokens_body,
            'tokens_encoded': tokens_total,
            'compression_ratio': 1 - (tokens_total / tokens_original),
            'macros_used': len(macros),
            'gain_net': tokens_original - tokens_total
        }
        
        return encoded_full, stats


class DigiLangV3Decoder:
    """Decoder para reversão perfeita."""
    
    @staticmethod
    def decode(encoded_text: str) -> str:
        """Decodifica texto com macros."""
        
        # Detecta header
        if 'MACROS_BEGIN' not in encoded_text:
            # Sem header, retorna como está
            return encoded_text
        
        # Separa header e corpo
        parts = encoded_text.split('MACROS_END')
        if len(parts) != 2:
            return encoded_text
        
        header_part = parts[0]
        body_part = parts[1].strip()
        
        # Extrai macros do header
        macros = {}
        for line in header_part.split('\n'):
            if '=' in line and '"' in line:
                # Parse: PLACEHOLDER = "expansion"
                match = re.match(r'\s*(.+?)\s*=\s*"(.+?)"', line)
                if match:
                    placeholder = match.group(1).strip()
                    expansion = match.group(2)
                    macros[placeholder] = expansion
        
        # Decodifica corpo (ordem reversa, maior primeiro)
        decoded = body_part
        replacements = sorted(
            macros.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        for placeholder, expansion in replacements:
            decoded = decoded.replace(placeholder, expansion)
        
        return decoded


def main():
    """CLI para encode/decode."""
    parser = argparse.ArgumentParser(
        description='DigiLang V3 Token-Aware - Compressão real de tokens'
    )
    
    parser.add_argument(
        'command',
        choices=['encode', 'decode', 'test'],
        help='Comando a executar'
    )
    
    parser.add_argument(
        'input',
        type=Path,
        help='Arquivo de entrada'
    )
    
    parser.add_argument(
        'output',
        type=Path,
        nargs='?',
        help='Arquivo de saída (opcional)'
    )
    
    parser.add_argument(
        '--max-macros',
        type=int,
        default=64,
        help='Máximo de macros a usar (default: 64)'
    )
    
    args = parser.parse_args()
    
    # Lê entrada
    with open(args.input, 'r', encoding='utf-8') as f:
        input_text = f.read()
    
    if args.command == 'encode':
        encoder = DigiLangV3Encoder(max_macros=args.max_macros)
        encoded, stats = encoder.encode(input_text)
        
        # Salva resultado
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(encoded)
        
        # Relatório
        print("="*60)
        print("DIGILANG V3 TOKEN-AWARE - RELATÓRIO DE COMPRESSÃO")
        print("="*60)
        print(f"Tokens originais:  {stats['tokens_original']:,}")
        print(f"Tokens header:     {stats['tokens_header']:,}")
        print(f"Tokens corpo:      {stats['tokens_body']:,}")
        print(f"Tokens total:      {stats['tokens_encoded']:,}")
        print(f"Ganho líquido:     {stats['gain_net']:,} tokens")
        print(f"Taxa compressão:   {stats['compression_ratio']:.1%}")
        print(f"Macros usadas:     {stats['macros_used']}")
        
        if stats['compression_ratio'] > 0:
            print(f"\n✅ SUCESSO! Compressão real de {stats['compression_ratio']:.1%}")
        else:
            print(f"\n⚠️ Sem ganho líquido. Considere texto maior ou ajustar macros.")
    
    elif args.command == 'decode':
        decoded = DigiLangV3Decoder.decode(input_text)
        
        # Salva resultado
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(decoded)
        else:
            print(decoded)
    
    elif args.command == 'test':
        # Teste de round-trip
        encoder = DigiLangV3Encoder(max_macros=args.max_macros)
        encoded, stats = encoder.encode(input_text)
        decoded = DigiLangV3Decoder.decode(encoded)
        
        print("="*60)
        print("TESTE DE ROUND-TRIP")
        print("="*60)
        print(f"Compressão: {stats['compression_ratio']:.1%}")
        print(f"Macros: {stats['macros_used']}")
        print(f"Round-trip: {'✅ PERFEITO' if decoded == input_text else '❌ FALHOU'}")
        
        if decoded != input_text:
            print("\n⚠️ Diferenças encontradas!")
            # Mostra primeiras diferenças
            for i, (c1, c2) in enumerate(zip(input_text, decoded)):
                if c1 != c2:
                    print(f"Posição {i}: '{c1}' != '{c2}'")
                    break


if __name__ == '__main__':
    main()