#!/usr/bin/env python
"""
PCToolkit: Prompt Compression Toolkit
Integrates multiple compression methods with intelligent selection.
"""

import time
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import tiktoken
import numpy as np
from pathlib import Path

# Import all compression methods
from src.digilang.encoder import DigiLangEncoder
from src.compressors.llmlingua import LLMLinguaCompressor, HierarchicalCompressor, CompressionConfig
from src.compressors.naive_tiktoken import NaiveTiktokenCompressor
from src.compressors.entity_mapper import NarrativeEntityMapper, SmartEntityCompressor
from src.compressors.tcra_llm import TCRACompressor, HybridTCRACompressor

class CompressionMethod(Enum):
    """Available compression methods."""
    DIGILANG = "digilang"
    LLMLINGUA = "llmlingua"
    HIERARCHICAL = "hierarchical"
    NAIVE = "naive"
    ENTITY = "entity"
    TCRA = "tcra"
    HYBRID_TCRA = "hybrid_tcra"
    SMART_ENTITY = "smart_entity"
    AUTO = "auto"

@dataclass
class CompressionProfile:
    """Profile for different use cases."""
    name: str
    methods: List[CompressionMethod]
    target_ratio: float
    preserve_semantic: bool = True
    max_latency_ms: float = 100
    description: str = ""

@dataclass
class CompressionResult:
    """Result from compression operation."""
    method: CompressionMethod
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    latency_ms: float
    semantic_score: float = 0.0
    metadata: Dict = field(default_factory=dict)
    
    @property
    def tokens_saved(self) -> int:
        return self.original_tokens - self.compressed_tokens
    
    @property
    def context_multiplier(self) -> float:
        return self.original_tokens / max(self.compressed_tokens, 1)

class PCToolkit:
    """
    Prompt Compression Toolkit with intelligent method selection.
    """
    
    def __init__(self):
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
        # Initialize all compressors
        self.compressors = {
            CompressionMethod.DIGILANG: DigiLangEncoder(),
            CompressionMethod.LLMLINGUA: LLMLinguaCompressor(CompressionConfig(target_ratio=0.3)),
            CompressionMethod.HIERARCHICAL: HierarchicalCompressor(),
            CompressionMethod.NAIVE: NaiveTiktokenCompressor(),
            CompressionMethod.ENTITY: NarrativeEntityMapper(),
            CompressionMethod.TCRA: TCRACompressor(target_ratio=0.3),
            CompressionMethod.HYBRID_TCRA: HybridTCRACompressor(),
            CompressionMethod.SMART_ENTITY: SmartEntityCompressor()
        }
        
        # Predefined profiles for common use cases
        self.profiles = {
            "max_compression": CompressionProfile(
                name="max_compression",
                methods=[CompressionMethod.HYBRID_TCRA, CompressionMethod.HIERARCHICAL],
                target_ratio=0.1,
                preserve_semantic=False,
                max_latency_ms=1000,
                description="Maximum compression, quality may suffer"
            ),
            "balanced": CompressionProfile(
                name="balanced",
                methods=[CompressionMethod.SMART_ENTITY, CompressionMethod.LLMLINGUA],
                target_ratio=0.3,
                preserve_semantic=True,
                max_latency_ms=100,
                description="Balance between compression and quality"
            ),
            "fast": CompressionProfile(
                name="fast",
                methods=[CompressionMethod.NAIVE, CompressionMethod.ENTITY],
                target_ratio=0.5,
                preserve_semantic=True,
                max_latency_ms=10,
                description="Fast compression with decent quality"
            ),
            "narrative": CompressionProfile(
                name="narrative",
                methods=[CompressionMethod.HIERARCHICAL, CompressionMethod.SMART_ENTITY],
                target_ratio=0.2,
                preserve_semantic=True,
                max_latency_ms=200,
                description="Optimized for screenplay/book compression"
            ),
            "structured": CompressionProfile(
                name="structured",
                methods=[CompressionMethod.DIGILANG],
                target_ratio=0.4,
                preserve_semantic=True,
                max_latency_ms=50,
                description="For structured data (JSON, tables, etc)"
            )
        }
        
        # Cache for method performance
        self.performance_cache = {}
    
    def compress(self, 
                text: str,
                method: CompressionMethod = CompressionMethod.AUTO,
                profile: Optional[str] = None,
                target_ratio: Optional[float] = None) -> CompressionResult:
        """
        Compress text using specified method or profile.
        """
        # Use profile if specified
        if profile and profile in self.profiles:
            return self._compress_with_profile(text, self.profiles[profile])
        
        # Auto-select method if needed
        if method == CompressionMethod.AUTO:
            method = self._auto_select_method(text, target_ratio)
        
        # Compress with selected method
        return self._compress_with_method(text, method, target_ratio)
    
    def _auto_select_method(self, text: str, target_ratio: Optional[float] = None) -> CompressionMethod:
        """
        Automatically select best compression method based on text characteristics.
        """
        tokens = len(self.encoder.encode(text))
        
        # Analyze text characteristics
        is_structured = self._is_structured(text)
        is_narrative = self._is_narrative(text)
        is_long = tokens > 4000
        
        # Decision tree
        if is_structured:
            return CompressionMethod.DIGILANG
        elif is_narrative:
            if is_long:
                return CompressionMethod.HIERARCHICAL
            else:
                return CompressionMethod.SMART_ENTITY
        elif target_ratio and target_ratio < 0.2:
            return CompressionMethod.HYBRID_TCRA
        elif tokens < 1000:
            return CompressionMethod.NAIVE
        else:
            return CompressionMethod.LLMLINGUA
    
    def _is_structured(self, text: str) -> bool:
        """Check if text is structured data."""
        # Check for JSON-like structure
        if text.strip().startswith('{') or text.strip().startswith('['):
            try:
                json.loads(text)
                return True
            except:
                pass
        
        # Check for high ratio of special characters
        special_chars = sum(1 for c in text if c in '{}[](),:;')
        return special_chars / len(text) > 0.1
    
    def _is_narrative(self, text: str) -> bool:
        """Check if text is narrative/screenplay."""
        narrative_markers = ['INT.', 'EXT.', 'FADE', 'ACT', 'SCENE', ':', '"']
        marker_count = sum(1 for marker in narrative_markers if marker in text)
        
        # Check for dialogue pattern
        import re
        dialogue_pattern = r'\b[A-Z][A-Z\s]+\s*\n'
        dialogue_matches = len(re.findall(dialogue_pattern, text))
        
        return marker_count > 3 or dialogue_matches > 2
    
    def _compress_with_method(self, 
                             text: str,
                             method: CompressionMethod,
                             target_ratio: Optional[float] = None) -> CompressionResult:
        """
        Compress with specific method.
        """
        original_tokens = len(self.encoder.encode(text))
        
        start_time = time.perf_counter()
        
        try:
            # Call appropriate compressor
            if method == CompressionMethod.DIGILANG:
                compressed, ratio = self.compressors[method].encode(text)
                metadata = {}
                
            elif method == CompressionMethod.LLMLINGUA:
                if target_ratio:
                    self.compressors[method].config.target_ratio = target_ratio
                compressed, ratio, metadata = self.compressors[method].compress(text)
                
            elif method == CompressionMethod.HIERARCHICAL:
                compressed, metadata = self.compressors[method].compress_narrative(
                    text, max_tokens=int(original_tokens * (target_ratio or 0.3))
                )
                ratio = metadata.get('compression_ratio', 0)
                
            elif method == CompressionMethod.NAIVE:
                compressed, ratio = self.compressors[method].compress(text)
                metadata = {}
                
            elif method == CompressionMethod.ENTITY:
                entity_map = self.compressors[method].analyze_text(text)
                compressed, metadata = self.compressors[method].compress_with_entities(text, entity_map)
                ratio = metadata.get('compression_ratio', 0)
                metadata['entity_map'] = entity_map
                
            elif method == CompressionMethod.TCRA:
                if target_ratio:
                    self.compressors[method].target_ratio = target_ratio
                compressed, ratio, metadata = self.compressors[method].compress(text)
                
            elif method == CompressionMethod.HYBRID_TCRA:
                compressed, metadata = self.compressors[method].compress(text)
                ratio = metadata.get('total_compression', 0)
                
            elif method == CompressionMethod.SMART_ENTITY:
                compressed, entity_map, metadata = self.compressors[method].compress(text)
                ratio = metadata.get('total_compression', 0)
                metadata['entity_map'] = entity_map
                
            else:
                compressed = text
                ratio = 0
                metadata = {}
            
        except Exception as e:
            # Fallback on error
            compressed = text[:int(len(text) * 0.5)]
            ratio = 0.5
            metadata = {'error': str(e)}
        
        latency_ms = (time.perf_counter() - start_time) * 1000
        compressed_tokens = len(self.encoder.encode(compressed))
        
        # Calculate semantic score (simplified)
        semantic_score = self._calculate_semantic_score(text, compressed)
        
        return CompressionResult(
            method=method,
            compressed_text=compressed,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=ratio,
            latency_ms=latency_ms,
            semantic_score=semantic_score,
            metadata=metadata
        )
    
    def _compress_with_profile(self, text: str, profile: CompressionProfile) -> CompressionResult:
        """
        Compress using profile settings.
        """
        best_result = None
        
        for method in profile.methods:
            result = self._compress_with_method(text, method, profile.target_ratio)
            
            # Check if meets profile requirements
            if result.latency_ms <= profile.max_latency_ms:
                if not best_result or result.compression_ratio > best_result.compression_ratio:
                    if not profile.preserve_semantic or result.semantic_score > 0.5:
                        best_result = result
        
        return best_result or self._compress_with_method(
            text, CompressionMethod.NAIVE, profile.target_ratio
        )
    
    def _calculate_semantic_score(self, original: str, compressed: str) -> float:
        """
        Calculate semantic preservation score (0-1).
        """
        # Simple heuristic: check key term preservation
        import re
        
        # Extract important terms from original
        words = re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z]+\b', original)
        if not words:
            return 1.0
        
        # Count preserved terms
        preserved = sum(1 for word in words if word in compressed)
        
        return preserved / len(words)
    
    def benchmark(self, text: str) -> Dict[str, CompressionResult]:
        """
        Benchmark all methods on given text.
        """
        results = {}
        
        for method in CompressionMethod:
            if method == CompressionMethod.AUTO:
                continue
                
            try:
                result = self._compress_with_method(text, method)
                results[method.value] = result
            except Exception as e:
                print(f"Error benchmarking {method.value}: {e}")
        
        return results
    
    def recommend_method(self, 
                        text: str,
                        max_latency_ms: float = 100,
                        min_compression: float = 0.5,
                        preserve_quality: bool = True) -> CompressionMethod:
        """
        Recommend best method based on requirements.
        """
        # Run benchmark
        results = self.benchmark(text)
        
        # Filter by requirements
        candidates = []
        for method_name, result in results.items():
            if (result.latency_ms <= max_latency_ms and
                result.compression_ratio >= min_compression and
                (not preserve_quality or result.semantic_score >= 0.5)):
                candidates.append((method_name, result))
        
        if not candidates:
            return CompressionMethod.NAIVE
        
        # Sort by compression ratio
        candidates.sort(key=lambda x: x[1].compression_ratio, reverse=True)
        
        return CompressionMethod(candidates[0][0])
    
    def get_stats(self, result: CompressionResult) -> str:
        """
        Get formatted statistics for compression result.
        """
        stats = []
        stats.append(f"Method: {result.method.value}")
        stats.append(f"Compression: {result.compression_ratio:.1%}")
        stats.append(f"Tokens: {result.original_tokens} → {result.compressed_tokens}")
        stats.append(f"Context multiplier: {result.context_multiplier:.2f}x")
        stats.append(f"Latency: {result.latency_ms:.1f}ms")
        stats.append(f"Semantic score: {result.semantic_score:.1%}")
        
        if result.metadata:
            if 'entities_mapped' in result.metadata:
                stats.append(f"Entities mapped: {result.metadata['entities_mapped']}")
            if 'tokens_removed' in result.metadata:
                stats.append(f"Tokens removed: {result.metadata['tokens_removed']}")
        
        return "\n".join(stats)


class CompressionPipeline:
    """
    Advanced compression pipeline with cascading methods.
    """
    
    def __init__(self):
        self.toolkit = PCToolkit()
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def cascade_compress(self, 
                        text: str,
                        stages: List[CompressionMethod],
                        target_ratio: float = 0.2) -> Tuple[str, Dict]:
        """
        Apply multiple compression methods in sequence.
        """
        current_text = text
        original_tokens = len(self.encoder.encode(text))
        stage_results = []
        
        for i, method in enumerate(stages):
            result = self.toolkit.compress(current_text, method=method)
            stage_results.append({
                'stage': i + 1,
                'method': method.value,
                'compression': result.compression_ratio,
                'tokens': result.compressed_tokens,
                'latency': result.latency_ms
            })
            
            current_text = result.compressed_text
            
            # Stop if target reached
            current_ratio = 1 - (result.compressed_tokens / original_tokens)
            if current_ratio >= target_ratio:
                break
        
        final_tokens = len(self.encoder.encode(current_text))
        
        stats = {
            'original_tokens': original_tokens,
            'final_tokens': final_tokens,
            'total_compression': 1 - (final_tokens / original_tokens),
            'stages': stage_results,
            'total_latency': sum(s['latency'] for s in stage_results)
        }
        
        return current_text, stats
    
    def adaptive_compress(self, text: str) -> Tuple[str, Dict]:
        """
        Adaptively compress based on text analysis.
        """
        tokens = len(self.encoder.encode(text))
        
        # Choose pipeline based on size and content
        if tokens < 1000:
            # Small text: single method
            result = self.toolkit.compress(text, profile="fast")
            return result.compressed_text, {
                'method': result.method.value,
                'compression': result.compression_ratio,
                'tokens': result.compressed_tokens
            }
        
        elif tokens < 4000:
            # Medium text: two-stage
            stages = [CompressionMethod.ENTITY, CompressionMethod.LLMLINGUA]
            
        else:
            # Large text: multi-stage
            stages = [
                CompressionMethod.ENTITY,
                CompressionMethod.TCRA,
                CompressionMethod.HIERARCHICAL
            ]
        
        return self.cascade_compress(text, stages)


if __name__ == "__main__":
    # Test PCToolkit
    test_text = """
    INT. CASTLE - THRONE ROOM - DAY
    
    HAMLET stands before CLAUDIUS and GERTRUDE. The court watches.
    
    HAMLET
    To be, or not to be, that is the question.
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune,
    Or to take arms against a sea of troubles.
    
    CLAUDIUS
    Madness in great ones must not unwatch'd go.
    
    The scene demonstrates Hamlet's internal conflict and Claudius's suspicion.
    """
    
    print("PCToolkit Compression Test")
    print("=" * 60)
    
    toolkit = PCToolkit()
    
    # Test auto mode
    print("\n1. AUTO MODE:")
    result = toolkit.compress(test_text)
    print(toolkit.get_stats(result))
    
    # Test profile
    print("\n2. NARRATIVE PROFILE:")
    result = toolkit.compress(test_text, profile="narrative")
    print(toolkit.get_stats(result))
    
    # Test recommendation
    print("\n3. RECOMMENDATION:")
    recommended = toolkit.recommend_method(
        test_text,
        max_latency_ms=50,
        min_compression=0.3
    )
    print(f"Recommended method: {recommended.value}")
    
    # Test cascade
    print("\n4. CASCADE COMPRESSION:")
    pipeline = CompressionPipeline()
    compressed, stats = pipeline.cascade_compress(
        test_text,
        [CompressionMethod.ENTITY, CompressionMethod.TCRA]
    )
    print(f"Total compression: {stats['total_compression']:.1%}")
    print(f"Stages: {len(stats['stages'])}")
    for stage in stats['stages']:
        print(f"  {stage['method']}: {stage['compression']:.1%} ({stage['latency']:.1f}ms)")