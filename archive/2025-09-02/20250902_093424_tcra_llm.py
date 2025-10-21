#!/usr/bin/env python
"""
TCRA-LLM: Token-level Contrastive Rational Alignment for LLM compression.
Based on "Compressing Context to Enhance Inference Efficiency" research.
"""

import re
import math
import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
import tiktoken
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

@dataclass
class TokenImportance:
    """Represents importance score for a token."""
    text: str
    position: int
    score: float
    type: str  # 'semantic', 'structural', 'narrative'
    keep: bool = True

@dataclass
class CompressionSegment:
    """A segment of text with compression metadata."""
    text: str
    tokens: List[TokenImportance]
    importance_threshold: float
    compression_ratio: float

class TCRACompressor:
    """
    Token-level Contrastive Rational Alignment compressor.
    Selectively removes tokens based on multi-dimensional importance scoring.
    """
    
    def __init__(self, target_ratio: float = 0.3, preserve_threshold: float = 0.7):
        self.target_ratio = target_ratio
        self.preserve_threshold = preserve_threshold
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
        # Importance weights
        self.weights = {
            'semantic': 0.4,     # Meaning contribution
            'structural': 0.3,   # Grammatical importance
            'narrative': 0.2,    # Story relevance
            'frequency': 0.1     # Inverse document frequency
        }
        
        # Critical tokens that should always be preserved
        self.critical_pos_tags = {'NN', 'NNP', 'VB', 'VBZ', 'VBD'}  # Nouns and verbs
        
        # Narrative-critical words
        self.narrative_keywords = {
            'characters': ['romeo', 'juliet', 'hamlet', 'macbeth', 'character', 'protagonist'],
            'actions': ['kill', 'die', 'love', 'betray', 'fight', 'escape', 'reveal'],
            'emotions': ['hate', 'fear', 'joy', 'anger', 'sad', 'happy', 'desperate'],
            'plot': ['because', 'therefore', 'however', 'suddenly', 'finally', 'meanwhile']
        }
        
        # Screenplay-specific markers
        self.screenplay_markers = ['INT.', 'EXT.', 'FADE', 'CUT', 'DISSOLVE', 'CONT', 'V.O.']
        
    def compute_token_importance(self, tokens: List[str], context: str) -> List[TokenImportance]:
        """
        Compute multi-dimensional importance scores for each token.
        """
        # Get POS tags
        try:
            pos_tags = nltk.pos_tag(tokens)
        except:
            pos_tags = [(t, 'NN') for t in tokens]  # Fallback
        
        # Compute TF-IDF scores for semantic importance
        tfidf_scores = self._compute_tfidf_scores(tokens, context)
        
        # Compute narrative importance
        narrative_scores = self._compute_narrative_scores(tokens)
        
        # Build TokenImportance objects
        token_importances = []
        for i, (token, pos) in enumerate(pos_tags):
            # Semantic score from TF-IDF
            semantic_score = tfidf_scores.get(i, 0.5)
            
            # Structural score from POS tag
            structural_score = 1.0 if pos in self.critical_pos_tags else 0.3
            if token.isupper() and len(token) > 1:  # Character names
                structural_score = 1.0
            if token in self.screenplay_markers:
                structural_score = 1.0
            
            # Narrative score
            narrative_score = narrative_scores[i]
            
            # Frequency penalty (common words get lower scores)
            freq_score = 1.0 / (1 + math.log(1 + tokens.count(token)))
            
            # Combined score
            total_score = (
                self.weights['semantic'] * semantic_score +
                self.weights['structural'] * structural_score +
                self.weights['narrative'] * narrative_score +
                self.weights['frequency'] * freq_score
            )
            
            token_importances.append(TokenImportance(
                text=token,
                position=i,
                score=total_score,
                type=self._get_primary_type(semantic_score, structural_score, narrative_score),
                keep=total_score >= self.preserve_threshold
            ))
        
        return token_importances
    
    def _compute_tfidf_scores(self, tokens: List[str], context: str) -> Dict[int, float]:
        """Compute TF-IDF scores for tokens."""
        try:
            # Create documents from sentences
            sentences = nltk.sent_tokenize(context)
            if len(sentences) < 2:
                return {i: 0.5 for i in range(len(tokens))}
            
            # Compute TF-IDF
            vectorizer = TfidfVectorizer(token_pattern=r'\S+')
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Map tokens to scores
            scores = {}
            for i, token in enumerate(tokens):
                if token.lower() in feature_names:
                    idx = list(feature_names).index(token.lower())
                    # Average score across documents
                    scores[i] = float(tfidf_matrix[:, idx].mean())
                else:
                    scores[i] = 0.3  # Default for unknown tokens
            
            # Normalize scores
            if scores:
                max_score = max(scores.values())
                if max_score > 0:
                    scores = {k: v/max_score for k, v in scores.items()}
            
            return scores
            
        except Exception:
            # Fallback to uniform scores
            return {i: 0.5 for i in range(len(tokens))}
    
    def _compute_narrative_scores(self, tokens: List[str]) -> List[float]:
        """Compute narrative importance scores."""
        scores = []
        
        for token in tokens:
            token_lower = token.lower()
            score = 0.3  # Base score
            
            # Check narrative keywords
            for category, keywords in self.narrative_keywords.items():
                if token_lower in keywords:
                    score = 1.0
                    break
                # Partial match
                elif any(kw in token_lower for kw in keywords):
                    score = max(score, 0.7)
            
            # Dialogue attribution
            if token.isupper() and len(token) > 1:
                score = 1.0
            
            # Scene markers
            if token in self.screenplay_markers:
                score = 1.0
            
            scores.append(score)
        
        return scores
    
    def _get_primary_type(self, semantic: float, structural: float, narrative: float) -> str:
        """Determine primary importance type."""
        scores = {
            'semantic': semantic,
            'structural': structural,
            'narrative': narrative
        }
        return max(scores, key=scores.get)
    
    def compress(self, text: str) -> Tuple[str, float, Dict]:
        """
        Compress text using TCRA-LLM approach.
        """
        original_tokens = self.encoder.encode(text)
        original_count = len(original_tokens)
        
        # Tokenize for analysis
        tokens = nltk.word_tokenize(text)
        
        # Compute importance scores
        token_importances = self.compute_token_importance(tokens, text)
        
        # Sort by importance
        sorted_tokens = sorted(token_importances, key=lambda x: x.score)
        
        # Determine how many tokens to keep
        target_count = int(len(tokens) * self.target_ratio)
        
        # Mark tokens for removal (lowest importance first)
        remove_count = len(tokens) - target_count
        for i in range(min(remove_count, len(sorted_tokens))):
            # Don't remove critical tokens
            if sorted_tokens[i].score < 0.5:  # Only remove low-importance
                sorted_tokens[i].keep = False
        
        # Rebuild text with kept tokens
        compressed_tokens = []
        for ti in sorted(token_importances, key=lambda x: x.position):
            if ti.keep:
                compressed_tokens.append(ti.text)
        
        # Reconstruct with proper spacing
        compressed = self._reconstruct_text(compressed_tokens)
        
        # Calculate statistics
        final_tokens = self.encoder.encode(compressed)
        final_count = len(final_tokens)
        
        stats = {
            'original_tokens': original_count,
            'final_tokens': final_count,
            'compression_ratio': 1 - (final_count / original_count),
            'tokens_removed': len([t for t in token_importances if not t.keep]),
            'tokens_kept': len([t for t in token_importances if t.keep]),
            'avg_importance_kept': np.mean([t.score for t in token_importances if t.keep]),
            'avg_importance_removed': np.mean([t.score for t in token_importances if not t.keep]) if any(not t.keep for t in token_importances) else 0
        }
        
        return compressed, stats['compression_ratio'], stats
    
    def _reconstruct_text(self, tokens: List[str]) -> str:
        """Reconstruct text from tokens with proper spacing."""
        if not tokens:
            return ""
        
        result = []
        for i, token in enumerate(tokens):
            # Add token
            result.append(token)
            
            # Add space unless followed by punctuation or end
            if i < len(tokens) - 1:
                next_token = tokens[i + 1]
                # Don't add space before punctuation
                if not re.match(r'^[.,;:!?\'\"\)\]\}]', next_token):
                    # Don't add space after opening brackets
                    if not re.match(r'.*[\(\[\{\"\']$', token):
                        result.append(' ')
        
        text = ''.join(result)
        
        # Clean up spacing
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'(["\'])\s+', r'\1', text)
        
        return text.strip()
    
    def adaptive_compress(self, text: str, min_ratio: float = 0.1, max_ratio: float = 0.5) -> Tuple[str, float, Dict]:
        """
        Adaptively compress based on content complexity.
        """
        # Analyze text complexity
        complexity = self._analyze_complexity(text)
        
        # Adjust target ratio based on complexity
        if complexity < 0.3:  # Simple text
            self.target_ratio = min_ratio
        elif complexity > 0.7:  # Complex text
            self.target_ratio = max_ratio
        else:
            # Linear interpolation
            self.target_ratio = min_ratio + (max_ratio - min_ratio) * complexity
        
        return self.compress(text)
    
    def _analyze_complexity(self, text: str) -> float:
        """
        Analyze text complexity (0-1 scale).
        """
        tokens = nltk.word_tokenize(text)
        
        if not tokens:
            return 0.5
        
        # Factors for complexity
        factors = []
        
        # Vocabulary diversity
        unique_ratio = len(set(tokens)) / len(tokens)
        factors.append(unique_ratio)
        
        # Average word length
        avg_length = np.mean([len(t) for t in tokens])
        factors.append(min(avg_length / 10, 1.0))
        
        # Sentence complexity (tokens per sentence)
        sentences = nltk.sent_tokenize(text)
        if sentences:
            avg_sent_length = len(tokens) / len(sentences)
            factors.append(min(avg_sent_length / 30, 1.0))
        
        # Named entity density
        upper_ratio = sum(1 for t in tokens if t[0].isupper()) / len(tokens)
        factors.append(upper_ratio)
        
        return np.mean(factors)


class HybridTCRACompressor:
    """
    Combines TCRA with entity mapping and LLMLingua for maximum compression.
    """
    
    def __init__(self):
        self.tcra = TCRACompressor()
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def compress(self, text: str) -> Tuple[str, Dict]:
        """
        Multi-stage compression pipeline.
        """
        original_tokens = len(self.encoder.encode(text))
        
        # Stage 1: Entity mapping
        from src.compressors.entity_mapper import NarrativeEntityMapper
        entity_mapper = NarrativeEntityMapper()
        entity_map = entity_mapper.analyze_text(text)
        entity_compressed, entity_stats = entity_mapper.compress_with_entities(text, entity_map)
        
        # Stage 2: TCRA compression
        tcra_compressed, tcra_ratio, tcra_stats = self.tcra.compress(entity_compressed)
        
        # Stage 3: Final cleanup with LLMLingua
        from src.compressors.llmlingua import LLMLinguaCompressor, CompressionConfig
        llm_compressor = LLMLinguaCompressor(
            CompressionConfig(
                target_ratio=0.5,
                preserve_entities=True,
                remove_redundancy=True,
                use_abbreviations=True
            )
        )
        final_compressed, llm_ratio, llm_stats = llm_compressor.compress(tcra_compressed)
        
        # Combined statistics
        final_tokens = len(self.encoder.encode(final_compressed))
        
        stats = {
            'original_tokens': original_tokens,
            'after_entities': entity_stats['final_tokens'],
            'after_tcra': tcra_stats['final_tokens'],
            'final_tokens': final_tokens,
            'total_compression': 1 - (final_tokens / original_tokens),
            'entity_compression': entity_stats['compression_ratio'],
            'tcra_compression': tcra_ratio,
            'llm_compression': llm_ratio,
            'entities_mapped': entity_stats.get('entity_count', 0),
            'tokens_removed_tcra': tcra_stats.get('tokens_removed', 0),
            'avg_importance_kept': tcra_stats.get('avg_importance_kept', 0)
        }
        
        return final_compressed, stats


if __name__ == "__main__":
    # Test TCRA compressor
    test_text = """
    HAMLET enters the castle courtyard. The ghost of his father appears.
    
    HAMLET
    To be, or not to be, that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune,
    Or to take arms against a sea of troubles.
    
    The ghost reveals that Claudius murdered him. Hamlet swears revenge.
    """
    
    print("Testing TCRA Compressor:")
    print("=" * 50)
    
    tcra = TCRACompressor(target_ratio=0.3)
    compressed, ratio, stats = tcra.compress(test_text)
    
    print(f"Original: {stats['original_tokens']} tokens")
    print(f"Compressed: {stats['final_tokens']} tokens")
    print(f"Compression ratio: {ratio:.1%}")
    print(f"Tokens kept: {stats['tokens_kept']}")
    print(f"Avg importance kept: {stats['avg_importance_kept']:.2f}")
    print(f"\nCompressed text:\n{compressed}")
    
    print("\n" + "=" * 50)
    print("Testing Hybrid TCRA:")
    
    hybrid = HybridTCRACompressor()
    final, hybrid_stats = hybrid.compress(test_text)
    
    print(f"Total compression: {hybrid_stats['total_compression']:.1%}")
    print(f"Entity stage: {hybrid_stats['entity_compression']:.1%}")
    print(f"TCRA stage: {hybrid_stats['tcra_compression']:.1%}")
    print(f"LLM stage: {hybrid_stats['llm_compression']:.1%}")
    print(f"\nFinal compressed:\n{final}")