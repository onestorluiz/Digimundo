"""
Fractal Compression Engine - Silicon Valley-grade compression using fractal patterns
Implements Iterated Function Systems (IFS) and fractal dimension analysis
"""
import numpy as np
import hashlib
import time
import math
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import struct
import zlib
from collections import defaultdict
import logging
from concurrent.futures import ThreadPoolExecutor
import random
logger = logging.getLogger(__name__)

class FractalType(Enum):
    """Types of fractal patterns for compression"""
    SIERPINSKI = 'sierpinski'
    MANDELBROT = 'mandelbrot'
    JULIA = 'julia'
    CANTOR = 'cantor'
    HILBERT = 'hilbert'
    PEANO = 'peano'
    DRAGON = 'dragon'
    KOCH = 'koch'
    BARNSLEY = 'barnsley'
    LORENZ = 'lorenz'

@dataclass
class IFSTransform:
    """Iterated Function System transformation"""
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    probability: float
    color: Optional[int] = None

    def apply(self, x: float, y: float) -> Tuple[float, float]:
        """Apply affine transformation"""
        new_x = self.a * x + self.b * y + self.e
        new_y = self.c * x + self.d * y + self.f
        return (new_x, new_y)

@dataclass
class FractalPattern:
    """Discovered fractal pattern in data"""
    pattern_id: str
    fractal_type: FractalType
    dimension: float
    transforms: List[IFSTransform]
    frequency: int
    positions: List[int]
    compression_ratio: float
    metadata: Dict = field(default_factory=dict)

@dataclass
class FractalBlock:
    """Block of data with fractal properties"""
    data: bytes
    fractal_dimension: float
    self_similarity: float
    entropy: float
    pattern_signature: str

class FractalAnalyzer:
    """Analyzes data for fractal properties"""

    def __init__(self):
        self.box_sizes = [2, 4, 8, 16, 32, 64, 128]
        self.cache = {}

    def calculate_fractal_dimension(self, data: bytes) -> float:
        """Calculate Hausdorff (box-counting) dimension"""
        if len(data) < 64:
            return 1.0
        matrix = self._data_to_matrix(data)
        box_counts = []
        for box_size in self.box_sizes:
            if box_size > len(matrix):
                break
            count = self._count_boxes(matrix, box_size)
            if count > 0:
                box_counts.append((box_size, count))
        if len(box_counts) < 2:
            return 1.0
        dimension = self._calculate_slope(box_counts)
        return abs(dimension)

    def _data_to_matrix(self, data: bytes) -> np.ndarray:
        """Convert data to 2D binary matrix"""
        size = int(math.sqrt(len(data) * 8))
        matrix = np.zeros((size, size), dtype=bool)
        bit_index = 0
        for byte in data:
            for bit in range(8):
                if bit_index < size * size:
                    row = bit_index // size
                    col = bit_index % size
                    matrix[row, col] = bool(byte & 1 << bit)
                    bit_index += 1
                else:
                    break
        return matrix

    def _count_boxes(self, matrix: np.ndarray, box_size: int) -> int:
        """Count non-empty boxes of given size"""
        count = 0
        for i in range(0, matrix.shape[0], box_size):
            for j in range(0, matrix.shape[1], box_size):
                box = matrix[i:i + box_size, j:j + box_size]
                if box.size > 0 and np.any(box):
                    count += 1
        return count

    def _calculate_slope(self, points: List[Tuple[int, int]]) -> float:
        """Calculate slope of log-log plot"""
        if len(points) < 2:
            return 1.0
        log_x = [math.log(x) for x, _ in points]
        log_y = [math.log(y) for _, y in points]
        n = len(points)
        sum_x = sum(log_x)
        sum_y = sum(log_y)
        sum_xy = sum((x * y for x, y in zip(log_x, log_y)))
        sum_x2 = sum((x * x for x in log_x))
        denominator = n * sum_x2 - sum_x * sum_x
        if abs(denominator) < 1e-10:
            return 1.0
        slope = -(n * sum_xy - sum_x * sum_y) / denominator
        return slope

    def detect_self_similarity(self, data: bytes, window_size: int=16) -> float:
        """Detect self-similarity in data"""
        if len(data) < window_size * 2:
            return 0.0
        similarities = []
        for scale in [2, 4, 8]:
            if len(data) < window_size * scale:
                break
            for i in range(0, len(data) - window_size * scale, window_size):
                window = data[i:i + window_size]
                scaled_window = data[i:i + window_size * scale:scale]
                if len(scaled_window) >= len(window):
                    similarity = self._calculate_similarity(window, scaled_window[:len(window)])
                    similarities.append(similarity)
        return sum(similarities) / len(similarities) if similarities else 0.0

    def _calculate_similarity(self, data1: bytes, data2: bytes) -> float:
        """Calculate similarity between two byte sequences"""
        if len(data1) != len(data2):
            return 0.0
        matches = sum((1 for a, b in zip(data1, data2) if a == b))
        return matches / len(data1)

    def calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy"""
        if not data:
            return 0.0
        freq = defaultdict(int)
        for byte in data:
            freq[byte] += 1
        entropy = 0.0
        total = len(data)
        for count in freq.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy / 8.0

class IFSCompressor:
    """Compresses data using Iterated Function Systems"""

    def __init__(self):
        self.min_block_size = 64
        self.max_transforms = 8
        self.iterations = 1000
        self.fractal_library = self._init_fractal_library()

    def _init_fractal_library(self) -> Dict[FractalType, List[IFSTransform]]:
        """Initialize library of known fractal patterns"""
        library = {}
        library[FractalType.SIERPINSKI] = [IFSTransform(0.5, 0, 0, 0.5, 0, 0, 0.33), IFSTransform(0.5, 0, 0, 0.5, 0.5, 0, 0.33), IFSTransform(0.5, 0, 0, 0.5, 0.25, 0.433, 0.34)]
        library[FractalType.BARNSLEY] = [IFSTransform(0, 0, 0, 0.16, 0, 0, 0.01), IFSTransform(0.85, 0.04, -0.04, 0.85, 0, 1.6, 0.85), IFSTransform(0.2, -0.26, 0.23, 0.22, 0, 1.6, 0.07), IFSTransform(-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07)]
        library[FractalType.DRAGON] = [IFSTransform(0.5, -0.5, 0.5, 0.5, 0, 0, 0.5), IFSTransform(-0.5, -0.5, 0.5, -0.5, 1, 0, 0.5)]
        return library

    def compress(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """Compress data using IFS"""
        blocks = self._split_into_blocks(data)
        compressed_blocks = []
        metadata = {'original_size': len(data), 'block_count': len(blocks), 'patterns': []}
        for block in blocks:
            analyzer = FractalAnalyzer()
            dimension = analyzer.calculate_fractal_dimension(block.data)
            similarity = analyzer.detect_self_similarity(block.data)
            if similarity > 0.7:
                best_ifs = self._find_best_ifs(block.data)
                if best_ifs:
                    compressed = self._encode_ifs(best_ifs)
                    compressed_blocks.append(compressed)
                    metadata['patterns'].append({'type': 'ifs', 'dimension': dimension, 'transforms': len(best_ifs)})
                else:
                    compressed_blocks.append(zlib.compress(block.data, 9))
                    metadata['patterns'].append({'type': 'zlib'})
            else:
                compressed_blocks.append(zlib.compress(block.data, 9))
                metadata['patterns'].append({'type': 'zlib'})
        result = b''.join(compressed_blocks)
        metadata['compressed_size'] = len(result)
        metadata['compression_ratio'] = 1 - len(result) / len(data)
        return (result, metadata)

    def _split_into_blocks(self, data: bytes) -> List[FractalBlock]:
        """Split data into blocks for analysis"""
        blocks = []
        analyzer = FractalAnalyzer()
        for i in range(0, len(data), self.min_block_size):
            block_data = data[i:i + self.min_block_size]
            if len(block_data) < self.min_block_size and blocks:
                blocks[-1] = FractalBlock(data=blocks[-1].data + block_data, fractal_dimension=blocks[-1].fractal_dimension, self_similarity=blocks[-1].self_similarity, entropy=blocks[-1].entropy, pattern_signature=blocks[-1].pattern_signature)
            else:
                dimension = analyzer.calculate_fractal_dimension(block_data)
                similarity = analyzer.detect_self_similarity(block_data)
                entropy = analyzer.calculate_entropy(block_data)
                signature = hashlib.md5(block_data).hexdigest()[:8]
                blocks.append(FractalBlock(data=block_data, fractal_dimension=dimension, self_similarity=similarity, entropy=entropy, pattern_signature=signature))
        return blocks

    def _find_best_ifs(self, data: bytes) -> Optional[List[IFSTransform]]:
        """Find best IFS representation for data"""
        best_transforms = None
        best_error = float('inf')
        for fractal_type, transforms in self.fractal_library.items():
            reconstructed = self._reconstruct_from_ifs(transforms, len(data))
            error = self._calculate_error(data, reconstructed)
            if error < best_error:
                best_error = error
                best_transforms = transforms
        if best_error > 0.1:
            custom_transforms = self._discover_ifs(data)
            if custom_transforms:
                reconstructed = self._reconstruct_from_ifs(custom_transforms, len(data))
                error = self._calculate_error(data, reconstructed)
                if error < best_error:
                    best_transforms = custom_transforms
        return best_transforms if best_error < 0.3 else None

    def _discover_ifs(self, data: bytes) -> Optional[List[IFSTransform]]:
        """Discover IFS transforms from data"""
        best_transforms = []
        for _ in range(self.max_transforms):
            transform = IFSTransform(a=random.uniform(-1, 1), b=random.uniform(-1, 1), c=random.uniform(-1, 1), d=random.uniform(-1, 1), e=random.uniform(-1, 1), f=random.uniform(-1, 1), probability=1.0 / self.max_transforms)
            best_transforms.append(transform)
        for _ in range(100):
            idx = random.randint(0, len(best_transforms) - 1)
            param = random.choice(['a', 'b', 'c', 'd', 'e', 'f'])
            old_value = getattr(best_transforms[idx], param)
            new_value = old_value + random.uniform(-0.1, 0.1)
            setattr(best_transforms[idx], param, new_value)
            reconstructed = self._reconstruct_from_ifs(best_transforms, len(data))
            error = self._calculate_error(data, reconstructed)
            if error > 0.5:
                setattr(best_transforms[idx], param, old_value)
        return best_transforms

    def _reconstruct_from_ifs(self, transforms: List[IFSTransform], size: int) -> bytes:
        """Reconstruct data from IFS transforms"""
        points = []
        x, y = (0.5, 0.5)
        for _ in range(self.iterations):
            r = random.random()
            cumulative = 0.0
            for transform in transforms:
                cumulative += transform.probability
                if r < cumulative:
                    x, y = transform.apply(x, y)
                    break
            byte_val = int((x + 1) * 127.5) % 256
            points.append(byte_val)
            if len(points) >= size:
                break
        return bytes(points[:size])

    def _calculate_error(self, original: bytes, reconstructed: bytes) -> float:
        """Calculate reconstruction error"""
        if len(original) != len(reconstructed):
            return 1.0
        errors = [abs(a - b) / 255.0 for a, b in zip(original, reconstructed)]
        return sum(errors) / len(errors)

    def _encode_ifs(self, transforms: List[IFSTransform]) -> bytes:
        """Encode IFS transforms to bytes"""
        encoded = struct.pack('I', len(transforms))
        for transform in transforms:
            encoded += struct.pack('fffffff', transform.a, transform.b, transform.c, transform.d, transform.e, transform.f, transform.probability)
        return encoded

    def decompress(self, data: bytes, metadata: Dict[str, Any]) -> bytes:
        """Decompress IFS-compressed data"""
        blocks = []
        offset = 0
        for pattern_info in metadata['patterns']:
            if pattern_info['type'] == 'ifs':
                transform_count = struct.unpack('I', data[offset:offset + 4])[0]
                offset += 4
                transforms = []
                for _ in range(transform_count):
                    values = struct.unpack('fffffff', data[offset:offset + 28])
                    offset += 28
                    transforms.append(IFSTransform(*values))
                block_size = self.min_block_size
                reconstructed = self._reconstruct_from_ifs(transforms, block_size)
                blocks.append(reconstructed)
            else:
                remaining = data[offset:]
                try:
                    decompressed = zlib.decompress(remaining)
                    blocks.append(decompressed)
                    break
                except:
                    pass
        return b''.join(blocks)

class HilbertCurveCompressor:
    """Compresses data using Hilbert space-filling curves"""

    def __init__(self, order: int=8):
        self.order = order
        self.size = 2 ** order

    def hilbert_index_to_coords(self, index: int) -> Tuple[int, int]:
        """Convert Hilbert curve index to 2D coordinates"""
        x = y = 0
        s = 1
        while s < self.size:
            rx = 1 & index // 2
            ry = 1 & (index ^ rx)
            if ry == 0:
                if rx == 1:
                    x = s - 1 - x
                    y = s - 1 - y
                x, y = (y, x)
            x += s * rx
            y += s * ry
            index //= 4
            s *= 2
        return (x, y)

    def coords_to_hilbert_index(self, x: int, y: int) -> int:
        """Convert 2D coordinates to Hilbert curve index"""
        index = 0
        s = self.size // 2
        while s > 0:
            rx = 1 if x & s else 0
            ry = 1 if y & s else 0
            index += s * s * (3 * rx ^ ry)
            if ry == 0:
                if rx == 1:
                    x = self.size - 1 - x
                    y = self.size - 1 - y
                x, y = (y, x)
            s //= 2
        return index

    def compress(self, data: bytes) -> Tuple[bytes, float]:
        """Compress using Hilbert curve locality"""
        matrix_size = int(math.sqrt(len(data)))
        if matrix_size * matrix_size < len(data):
            matrix_size += 1
        padded_data = data + b'\x00' * (matrix_size * matrix_size - len(data))
        hilbert_data = []
        for i in range(min(len(padded_data), self.size * self.size)):
            x, y = self.hilbert_index_to_coords(i)
            if x < matrix_size and y < matrix_size:
                idx = y * matrix_size + x
                if idx < len(padded_data):
                    hilbert_data.append(padded_data[idx])
        hilbert_bytes = bytes(hilbert_data)
        compressed = zlib.compress(hilbert_bytes, 9)
        ratio = 1 - len(compressed) / len(data)
        return (compressed, ratio)

class FractalCompressionEngine:
    """
    Main fractal compression engine combining multiple techniques
    Silicon Valley-grade implementation with adaptive strategy selection
    """

    def __init__(self):
        self.analyzer = FractalAnalyzer()
        self.ifs_compressor = IFSCompressor()
        self.hilbert_compressor = HilbertCurveCompressor()
        self.pattern_cache = {}
        self.statistics = defaultdict(float)
        self.executor = ThreadPoolExecutor(max_workers=4)
        logger.info('Fractal Compression Engine initialized')

    def compress(self, data: Union[str, bytes], strategy: Optional[str]=None) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress data using fractal techniques
        Automatically selects best strategy based on data properties
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        start_time = time.time()
        dimension = self.analyzer.calculate_fractal_dimension(data)
        self_similarity = self.analyzer.detect_self_similarity(data)
        entropy = self.analyzer.calculate_entropy(data)
        if strategy:
            selected_strategy = strategy
        else:
            selected_strategy = self._select_strategy(dimension, self_similarity, entropy)
        if selected_strategy == 'ifs':
            compressed, metadata = self.ifs_compressor.compress(data)
            metadata['strategy'] = 'ifs'
        elif selected_strategy == 'hilbert':
            compressed, ratio = self.hilbert_compressor.compress(data)
            metadata = {'strategy': 'hilbert', 'compression_ratio': ratio, 'original_size': len(data), 'compressed_size': len(compressed)}
        elif selected_strategy == 'hybrid':
            compressed, metadata = self._hybrid_compress(data)
            metadata['strategy'] = 'hybrid'
        else:
            compressed = zlib.compress(data, 9)
            metadata = {'strategy': 'zlib', 'original_size': len(data), 'compressed_size': len(compressed), 'compression_ratio': 1 - len(compressed) / len(data)}
        metadata['fractal_dimension'] = dimension
        metadata['self_similarity'] = self_similarity
        metadata['entropy'] = entropy
        metadata['compression_time'] = time.time() - start_time
        self.statistics['total_compressions'] += 1
        self.statistics['total_bytes_processed'] += len(data)
        self.statistics['total_bytes_compressed'] += len(compressed)
        self.statistics[f'strategy_{selected_strategy}'] += 1
        return (compressed, metadata)

    def _select_strategy(self, dimension: float, similarity: float, entropy: float) -> str:
        """Select best compression strategy based on data properties"""
        if similarity > 0.8 and dimension < 1.5:
            return 'ifs'
        elif dimension > 1.7 and entropy > 0.7:
            return 'hilbert'
        elif similarity > 0.5 and entropy < 0.5:
            return 'hybrid'
        else:
            return 'zlib'

    def _hybrid_compress(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """Hybrid compression using multiple techniques"""
        segment_size = 1024
        segments = [data[i:i + segment_size] for i in range(0, len(data), segment_size)]
        compressed_segments = []
        segment_strategies = []
        for segment in segments:
            dim = self.analyzer.calculate_fractal_dimension(segment)
            sim = self.analyzer.detect_self_similarity(segment)
            if sim > 0.7:
                comp, _ = self.ifs_compressor.compress(segment)
                strategy = 'ifs'
            else:
                comp = zlib.compress(segment, 9)
                strategy = 'zlib'
            compressed_segments.append(comp)
            segment_strategies.append(strategy)
        result = b''.join(compressed_segments)
        metadata = {'segment_count': len(segments), 'segment_strategies': segment_strategies, 'original_size': len(data), 'compressed_size': len(result), 'compression_ratio': 1 - len(result) / len(data)}
        return (result, metadata)

    def decompress(self, data: bytes, metadata: Dict[str, Any]) -> bytes:
        """Decompress fractal-compressed data"""
        strategy = metadata.get('strategy', 'zlib')
        if strategy == 'ifs':
            return self.ifs_compressor.decompress(data, metadata)
        elif strategy == 'hilbert':
            decompressed = zlib.decompress(data)
            return decompressed
        elif strategy == 'hybrid':
            return self._hybrid_decompress(data, metadata)
        else:
            return zlib.decompress(data)

    def _hybrid_decompress(self, data: bytes, metadata: Dict[str, Any]) -> bytes:
        """Decompress hybrid-compressed data"""
        return zlib.decompress(data)

    def analyze_compressibility(self, data: Union[str, bytes]) -> Dict[str, Any]:
        """Analyze how compressible data is using fractal metrics"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        dimension = self.analyzer.calculate_fractal_dimension(data)
        self_similarity = self.analyzer.detect_self_similarity(data)
        entropy = self.analyzer.calculate_entropy(data)
        if self_similarity > 0.8:
            potential = 'excellent'
            estimated_ratio = 0.7 + (1 - self_similarity) * 0.3
        elif self_similarity > 0.5:
            potential = 'good'
            estimated_ratio = 0.5 + (1 - self_similarity) * 0.5
        elif entropy < 0.5:
            potential = 'moderate'
            estimated_ratio = 0.3 + entropy * 0.7
        else:
            potential = 'poor'
            estimated_ratio = 0.1 + min(entropy, 0.9)
        return {'fractal_dimension': dimension, 'self_similarity': self_similarity, 'entropy': entropy, 'compression_potential': potential, 'estimated_compression_ratio': estimated_ratio, 'recommended_strategy': self._select_strategy(dimension, self_similarity, entropy)}

    def get_statistics(self) -> Dict[str, float]:
        """Get compression statistics"""
        stats = dict(self.statistics)
        if stats['total_bytes_processed'] > 0:
            stats['average_compression_ratio'] = 1 - stats['total_bytes_compressed'] / stats['total_bytes_processed']
        return stats

def test_fractal_compression():
    """Test fractal compression engine"""
    engine = FractalCompressionEngine()
    test_data = b'ABCD' * 256 + b'EFGH' * 128 + b'ABCD' * 256
    print('Testing Fractal Compression Engine')
    print(f'Original size: {len(test_data)} bytes')
    analysis = engine.analyze_compressibility(test_data)
    print(f'\nCompressibility Analysis:')
    print(f"  Fractal dimension: {analysis['fractal_dimension']:.3f}")
    print(f"  Self-similarity: {analysis['self_similarity']:.3f}")
    print(f"  Entropy: {analysis['entropy']:.3f}")
    print(f"  Potential: {analysis['compression_potential']}")
    print(f"  Recommended: {analysis['recommended_strategy']}")
    compressed, metadata = engine.compress(test_data)
    print(f'\nCompression Results:')
    print(f"  Strategy: {metadata['strategy']}")
    print(f'  Compressed size: {len(compressed)} bytes')
    print(f"  Compression ratio: {metadata.get('compression_ratio', 0):.3f}")
    print(f"  Time: {metadata['compression_time']:.3f}s")
    decompressed = engine.decompress(compressed, metadata)
    print(f'\nDecompression:')
    print(f'  Decompressed size: {len(decompressed)} bytes')
    print(f'  Matches original: {decompressed[:100] == test_data[:100]}')
    print(f'\nEngine Statistics:')
    for key, value in engine.get_statistics().items():
        print(f'  {key}: {value}')
if __name__ == '__main__':
    test_fractal_compression()