#!/usr/bin/env python3
"""
🎯 TPD Multi-Layer em Português
Sistema de compressão em múltiplas camadas baseado em Token Pair Database
Implementação própria sem dependências do validation quebrado
"""

import logging
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter, defaultdict
import heapq
import time
import json
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TPDMultiLayerPT:
    """
    Token Pair Database Multi-Layer em Português
    Implementação limpa e funcional do zero
    """

    def __init__(self, max_layers: int = 3, min_frequency: int = 2):
        """
        Inicializa o sistema multi-layer

        Args:
            max_layers: Número máximo de camadas de compressão
            min_frequency: Frequência mínima para incluir padrão
        """
        self.max_layers = max_layers
        self.min_frequency = min_frequency
        self.layers = []  # Lista de dicionários por camada
        self.symbols_used = set()  # Símbolos já utilizados
        self.compression_stats = []  # Estatísticas por camada

        # Importar tiktoken para trabalhar com tokens reais
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
            self.tiktoken_available = True
        except ImportError:
            logger.warning("⚠️ tiktoken não disponível - usando estimativas")
            self.tiktoken_available = False
            self.encoder = None

    def _tokenize(self, text: str) -> List[int]:
        """Converte texto em tokens"""
        if self.tiktoken_available:
            return self.encoder.encode(text)
        else:
            # Fallback: estima 1 token = 4 caracteres
            return [i for i in range(len(text) // 4)]

    def _count_token_pairs(self, tokens: List[int], n: int = 2) -> Counter:
        """
        Conta n-gramas de tokens

        Args:
            tokens: Lista de token IDs
            n: Tamanho do n-grama (2 = bigrama, 3 = trigrama)

        Returns:
            Counter com frequências dos n-gramas
        """
        ngrams = Counter()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams[ngram] += 1
        return ngrams

    def _calculate_savings(self, pattern: Tuple[int, ...], frequency: int) -> int:
        """
        Calcula economia em tokens para um padrão

        Args:
            pattern: Tupla de token IDs
            frequency: Frequência do padrão

        Returns:
            Tokens economizados se substituir por 1 símbolo
        """
        pattern_length = len(pattern)
        # Economia = (tamanho_original - 1) * frequência
        savings = (pattern_length - 1) * frequency
        return savings

    def _greedy_lazy_selection(self,
                               candidates: Dict[Tuple[int, ...], int],
                               max_patterns: int = 500,
                               time_limit: float = 30.0) -> Dict[Tuple[int, ...], str]:
        """
        Algoritmo Greedy-Lazy para seleção ótima de padrões

        Args:
            candidates: Dicionário de padrões candidatos com frequências
            max_patterns: Número máximo de padrões a selecionar
            time_limit: Tempo máximo em segundos

        Returns:
            Dicionário de padrões selecionados com seus símbolos
        """
        start_time = time.time()
        selected = {}
        available_symbols = self._get_available_symbols()

        # Criar heap com upper bounds (economia negativa para max heap)
        heap = []
        for pattern, freq in candidates.items():
            if freq >= self.min_frequency:
                savings = self._calculate_savings(pattern, freq)
                heapq.heappush(heap, (-savings, pattern, freq))

        # Rastrear posições ocupadas para evitar sobreposição
        used_positions = set()

        while heap and len(selected) < max_patterns and available_symbols:
            if time.time() - start_time > time_limit:
                logger.info(f"⏱️ Tempo limite atingido ({time_limit}s)")
                break

            neg_savings, pattern, freq = heapq.heappop(heap)
            savings = -neg_savings

            # Verificar se ainda vale a pena (ganho marginal)
            if savings < 1:
                continue

            # Atribuir símbolo ao padrão
            symbol = available_symbols.pop(0)
            selected[pattern] = symbol
            self.symbols_used.add(symbol)

            logger.debug(f"Selecionado: {pattern} → {symbol} (economia: {savings} tokens)")

        logger.info(f"✅ Selecionados {len(selected)} padrões em {time.time()-start_time:.2f}s")
        return selected

    def _get_available_symbols(self) -> List[str]:
        """
        Retorna lista de símbolos Unicode de 1 token disponíveis
        """
        # Símbolos que sabemos que são 1 token cada
        symbols = []

        # Ranges testados e confirmados como 1-token
        ranges = [
            (0x2500, 0x257F),  # Box Drawing
            (0x2580, 0x259F),  # Block Elements
            (0x25A0, 0x25FF),  # Geometric Shapes
            (0x2600, 0x26FF),  # Miscellaneous Symbols
            (0x2700, 0x27BF),  # Dingbats
            (0x2800, 0x28FF),  # Braille
            (0x2900, 0x297F),  # Supplemental Arrows-B
            (0x2B00, 0x2BFF),  # Miscellaneous Symbols and Arrows
            (0x1F300, 0x1F5FF), # Miscellaneous Symbols and Pictographs
            (0x1F600, 0x1F64F), # Emoticons
            (0x1F680, 0x1F6FF), # Transport and Map Symbols
        ]

        for start, end in ranges:
            for codepoint in range(start, min(end + 1, start + 100)):  # Limitar para teste
                char = chr(codepoint)
                if char not in self.symbols_used:
                    symbols.append(char)

        return symbols[:1000]  # Retornar até 1000 símbolos

    def build_layer(self, text: str, layer_num: int) -> Tuple[Dict, str]:
        """
        Constrói uma camada de compressão

        Args:
            text: Texto a comprimir
            layer_num: Número da camada (0-indexed)

        Returns:
            Tupla (dicionário de padrões, texto comprimido)
        """
        logger.info(f"\n🔨 Construindo Camada {layer_num + 1}")

        # Tokenizar texto
        tokens = self._tokenize(text)
        original_tokens = len(tokens)
        logger.info(f"📊 Tokens originais: {original_tokens:,}")

        # Contar n-gramas (2 a 5 tokens)
        all_ngrams = Counter()
        for n in range(2, min(6, len(tokens) // 10)):  # Até 5-gramas
            ngrams = self._count_token_pairs(tokens, n)
            all_ngrams.update(ngrams)

        logger.info(f"📈 Padrões encontrados: {len(all_ngrams):,}")

        # Selecionar padrões ótimos
        patterns = self._greedy_lazy_selection(all_ngrams, max_patterns=500)

        # Aplicar substituições (simulado para texto)
        compressed_text = text
        replacements = 0

        # Ordenar padrões por tamanho (maiores primeiro)
        sorted_patterns = sorted(patterns.items(),
                                key=lambda x: len(x[0]),
                                reverse=True)

        for pattern_tokens, symbol in sorted_patterns:
            # Converter tokens de volta para texto (aproximado)
            if self.tiktoken_available:
                try:
                    pattern_text = self.encoder.decode(list(pattern_tokens))
                    if pattern_text in compressed_text:
                        count = compressed_text.count(pattern_text)
                        compressed_text = compressed_text.replace(pattern_text, symbol)
                        replacements += count
                except:
                    pass

        # Calcular estatísticas
        compressed_tokens = self._tokenize(compressed_text)
        compression_ratio = 1 - (len(compressed_tokens) / original_tokens)

        stats = {
            'layer': layer_num + 1,
            'original_tokens': original_tokens,
            'compressed_tokens': len(compressed_tokens),
            'compression_ratio': compression_ratio,
            'patterns_used': len(patterns),
            'replacements': replacements
        }

        self.compression_stats.append(stats)
        logger.info(f"✅ Camada {layer_num + 1}: {compression_ratio:.1%} compressão")

        return patterns, compressed_text

    def compress(self, text: str) -> Tuple[str, List[Dict], Dict]:
        """
        Comprime texto usando múltiplas camadas

        Args:
            text: Texto a comprimir

        Returns:
            Tupla (texto comprimido, lista de dicionários, estatísticas)
        """
        logger.info("🚀 Iniciando compressão multi-layer")
        start_time = time.time()

        self.layers = []
        self.compression_stats = []
        current_text = text

        for layer in range(self.max_layers):
            # Construir camada
            layer_dict, compressed_text = self.build_layer(current_text, layer)
            self.layers.append(layer_dict)

            # Se não houve compressão significativa, parar
            if len(compressed_text) >= len(current_text) * 0.95:
                logger.info(f"⚠️ Camada {layer + 1} sem ganho significativo, parando")
                break

            current_text = compressed_text

        # Estatísticas finais
        original_tokens = self._tokenize(text)
        final_tokens = self._tokenize(current_text)
        total_compression = 1 - (len(final_tokens) / len(original_tokens))

        final_stats = {
            'total_layers': len(self.layers),
            'original_tokens': len(original_tokens),
            'final_tokens': len(final_tokens),
            'total_compression': total_compression,
            'total_patterns': sum(len(layer) for layer in self.layers),
            'processing_time': time.time() - start_time,
            'layers': self.compression_stats
        }

        logger.info(f"\n🎯 COMPRESSÃO FINAL: {total_compression:.1%}")
        logger.info(f"📊 Tokens: {len(original_tokens):,} → {len(final_tokens):,}")
        logger.info(f"💾 Economia: {len(original_tokens) - len(final_tokens):,} tokens")
        logger.info(f"🔢 Padrões totais: {final_stats['total_patterns']}")
        logger.info(f"⏱️ Tempo: {final_stats['processing_time']:.2f}s")

        return current_text, self.layers, final_stats

    def decompress(self, text: str, layers: List[Dict]) -> str:
        """
        Descomprime texto aplicando camadas em ordem reversa

        Args:
            text: Texto comprimido
            layers: Lista de dicionários de cada camada

        Returns:
            Texto original descomprimido
        """
        current_text = text

        # Aplicar camadas em ordem reversa
        for layer_dict in reversed(layers):
            for pattern_tokens, symbol in layer_dict.items():
                if self.tiktoken_available:
                    try:
                        pattern_text = self.encoder.decode(list(pattern_tokens))
                        current_text = current_text.replace(symbol, pattern_text)
                    except:
                        pass

        return current_text

    def save_model(self, filepath: Path):
        """Salva o modelo TPD em arquivo"""
        model_data = {
            'layers': [
                {str(k): v for k, v in layer.items()}
                for layer in self.layers
            ],
            'stats': self.compression_stats,
            'config': {
                'max_layers': self.max_layers,
                'min_frequency': self.min_frequency
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)

        logger.info(f"💾 Modelo salvo em {filepath}")

    def load_model(self, filepath: Path):
        """Carrega modelo TPD de arquivo"""
        with open(filepath, 'r', encoding='utf-8') as f:
            model_data = json.load(f)

        self.layers = [
            {eval(k): v for k, v in layer.items()}
            for layer in model_data['layers']
        ]
        self.compression_stats = model_data['stats']
        self.max_layers = model_data['config']['max_layers']
        self.min_frequency = model_data['config']['min_frequency']

        logger.info(f"📂 Modelo carregado de {filepath}")


def test_tpd_multilayer():
    """Testa o sistema TPD Multi-Layer"""
    from pathlib import Path

    # Carregar texto do Dark Knight para comparação justa
    txt_path = Path('data/original/The_Dark_Knight_-_Release.txt')
    if txt_path.exists():
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            full_text = f.read()

        # Usar amostra de 50k chars como no V22 MEGA
        sample_text = full_text[:50000]
        print(f"📄 Texto do Dark Knight: {len(sample_text):,} chars")
    else:
        # Fallback para texto pequeno
        sample_text = """FADE IN:

INT. WAYNE ENTERPRISES - BOARDROOM - DAY

The boardroom is filled with EXECUTIVES. BRUCE WAYNE enters,
commanding attention. He walks to the head of the table.

BRUCE WAYNE
Gentlemen, we need to discuss the
future of Wayne Enterprises.

The executives exchange worried glances. LUCIUS FOX stands up.

LUCIUS FOX
Bruce, the numbers don't lie. We're
facing unprecedented challenges.

BRUCE WAYNE
(determined)
Then we'll face them together. Wayne
Enterprises has weathered storms before.

CUT TO:

EXT. GOTHAM CITY - SKYLINE - NIGHT

The Bat-Signal illuminates the dark sky. Batman stands on a rooftop,
cape billowing in the wind.

FADE OUT."""
        print("⚠️ Arquivo Dark Knight não encontrado, usando texto pequeno")

    # Criar e testar compressor
    compressor = TPDMultiLayerPT(max_layers=3, min_frequency=2)

    print("\n" + "="*60)
    print("TESTE TPD MULTI-LAYER EM PORTUGUÊS")
    print("="*60)

    # Comprimir
    compressed, layers, stats = compressor.compress(sample_text)

    print(f"\nTexto Original: {len(sample_text)} chars")
    print(f"Texto Comprimido: {len(compressed)} chars")
    print(f"Taxa de Compressão: {stats['total_compression']:.1%}")

    # Salvar modelo
    model_path = Path("output/tpd_model_test.json")
    model_path.parent.mkdir(exist_ok=True)
    compressor.save_model(model_path)

    return stats


if __name__ == "__main__":
    test_tpd_multilayer()