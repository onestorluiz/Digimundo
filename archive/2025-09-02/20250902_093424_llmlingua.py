#!/usr/bin/env python
"""
Simplified LLMLingua implementation for narrative compression.
Based on Microsoft's approach but adapted for screenplay/book compression.
"""

import re
import nltk
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import tiktoken

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)

@dataclass
class CompressionConfig:
    """Configuration for LLMLingua compression."""
    target_ratio: float = 0.3  # Target 70% reduction
    preserve_entities: bool = True
    preserve_structure: bool = True
    remove_redundancy: bool = True
    use_abbreviations: bool = True
    
class LLMLinguaCompressor:
    """
    Simplified LLMLingua compressor focusing on narrative text.
    Combines multiple techniques for optimal compression.
    """
    
    def __init__(self, config: Optional[CompressionConfig] = None):
        self.config = config or CompressionConfig()
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
        # Entity mappings for consistent abbreviation
        self.entity_map = {}
        self.entity_counter = {'CHAR': 0, 'LOC': 0, 'OBJ': 0}
        
        # Common redundant patterns in narratives
        self.redundancy_patterns = [
            (r'\b(very|really|quite|rather|somewhat|fairly)\s+', ''),  # Intensifiers
            (r'\b(just|simply|merely|only)\s+', ''),  # Minimizers
            (r'\b(basically|essentially|fundamentally)\s+', ''),  # Fillers
            (r'\s+(?:in order|so as)\s+to\b', ' to'),  # Verbose infinitives
            (r'\b(?:the fact that|the way that)\b', 'that'),  # Wordiness
            (r'\s*,\s*(?:however|therefore|moreover|furthermore),\s*', '. '),  # Heavy connectives
        ]
        
        # Screenplay/narrative specific abbreviations
        self.abbreviations = {
            'interior': 'INT',
            'exterior': 'EXT',
            'continuous': 'CONT',
            'voice over': 'V.O.',
            'point of view': 'POV',
            'close up': 'CU',
            'establishing shot': 'EST',
            'fade in': 'FI',
            'fade out': 'FO',
            'cut to': 'CT',
            'dissolve to': 'DT',
            'the protagonist': 'PROTAG',
            'the antagonist': 'ANTAG',
        }
        
    def compress(self, text: str) -> Tuple[str, float, Dict]:
        """
        Compress text using multi-stage approach.
        Returns compressed text, compression ratio, and statistics.
        """
        original_tokens = len(self.encoder.encode(text))
        stats = {'original_tokens': original_tokens}
        
        # Stage 1: Entity recognition and mapping
        if self.config.preserve_entities:
            text = self._map_entities(text)
            stats['entities_mapped'] = len(self.entity_map)
        
        # Stage 2: Remove redundancy
        if self.config.remove_redundancy:
            text = self._remove_redundancy(text)
        
        # Stage 3: Apply abbreviations
        if self.config.use_abbreviations:
            text = self._apply_abbreviations(text)
        
        # Stage 4: Structural compression (for screenplays)
        if self.config.preserve_structure:
            text = self._compress_structure(text)
        
        # Stage 5: Token-level filtering (selective removal)
        text = self._selective_token_removal(text, self.config.target_ratio)
        
        # Calculate final metrics
        final_tokens = len(self.encoder.encode(text))
        compression_ratio = 1 - (final_tokens / original_tokens)
        
        stats['final_tokens'] = final_tokens
        stats['compression_ratio'] = compression_ratio
        stats['target_achieved'] = compression_ratio >= (1 - self.config.target_ratio)
        
        return text, compression_ratio, stats
    
    def _map_entities(self, text: str) -> str:
        """Map recurring entities to short codes."""
        import re
        
        # Find potential character names (capitalized words in dialogue attribution)
        char_pattern = r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\s*:'
        for match in re.finditer(char_pattern, text):
            name = match.group(1)
            if name not in self.entity_map and len(name) > 4:
                self.entity_counter['CHAR'] += 1
                abbr = f"C{self.entity_counter['CHAR']}"
                self.entity_map[name] = abbr
        
        # Apply mappings
        for entity, abbr in sorted(self.entity_map.items(), key=lambda x: len(x[0]), reverse=True):
            text = text.replace(entity, abbr)
        
        return text
    
    def _remove_redundancy(self, text: str) -> str:
        """Remove redundant words and patterns."""
        for pattern, replacement in self.redundancy_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        return text.strip()
    
    def _apply_abbreviations(self, text: str) -> str:
        """Apply domain-specific abbreviations."""
        for full, abbr in sorted(self.abbreviations.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = r'\b' + re.escape(full) + r'\b'
            text = re.sub(pattern, abbr, text, flags=re.IGNORECASE)
        
        return text
    
    def _compress_structure(self, text: str) -> str:
        """Compress structural elements (scene headers, transitions, etc)."""
        # Compress scene headers
        text = re.sub(r'(INT\.|EXT\.)\s+([A-Z\s]+)\s*[-–]\s*(DAY|NIGHT|DAWN|DUSK)', 
                     r'\1\2-\3', text)
        
        # Compress parentheticals
        text = re.sub(r'\(\s*([^)]+)\s*\)', r'(\1)', text)
        
        # Remove unnecessary line breaks in dialogue
        text = re.sub(r'\n(?=[a-z])', ' ', text)
        
        return text
    
    def _selective_token_removal(self, text: str, target_ratio: float) -> str:
        """
        Selectively remove tokens based on importance scoring.
        This is a simplified version of LLMLingua's approach.
        """
        sentences = nltk.sent_tokenize(text)
        
        if len(sentences) == 0:
            return text
        
        # Score sentences by importance (simplified heuristic)
        sentence_scores = []
        for sent in sentences:
            score = 0
            # Dialogue gets higher score
            if ':' in sent or '"' in sent:
                score += 2
            # Action/scene headers get highest score  
            if any(marker in sent.upper() for marker in ['INT.', 'EXT.', 'CUT TO', 'FADE']):
                score += 3
            # Shorter sentences are often more important
            score += 1 / (1 + len(sent.split()) / 10)
            # Contains important keywords
            if any(word in sent.lower() for word in ['kill', 'die', 'love', 'betray', 'reveal']):
                score += 1
            
            sentence_scores.append((sent, score))
        
        # Sort by importance and keep top sentences until target ratio
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        current_tokens = 0
        target_tokens = int(len(self.encoder.encode(text)) * target_ratio)
        kept_sentences = []
        
        for sent, score in sentence_scores:
            sent_tokens = len(self.encoder.encode(sent))
            if current_tokens + sent_tokens <= target_tokens:
                kept_sentences.append(sent)
                current_tokens += sent_tokens
            elif current_tokens < target_tokens * 0.5:  # Ensure minimum content
                kept_sentences.append(sent)
                current_tokens += sent_tokens
        
        # Reconstruct in original order (maintain narrative flow)
        result = []
        for sent in sentences:
            if sent in kept_sentences:
                result.append(sent)
        
        return ' '.join(result) if result else text[:1000]  # Fallback
    
    def decompress_hints(self, compressed_text: str) -> Dict[str, any]:
        """
        Provide hints for decompression/interpretation.
        Returns entity mappings and structural markers.
        """
        return {
            'entity_mappings': {v: k for k, v in self.entity_map.items()},
            'abbreviations': {v: k for k, v in self.abbreviations.items()},
            'structural_markers': ['INT.', 'EXT.', 'CUT TO:', 'FADE'],
            'preserved_structure': self.config.preserve_structure
        }


class HierarchicalCompressor:
    """
    Hierarchical compression for long narratives (books/scripts).
    Compresses at multiple levels: chapter -> scene -> beat.
    """
    
    def __init__(self, base_compressor: Optional[LLMLinguaCompressor] = None):
        self.base_compressor = base_compressor or LLMLinguaCompressor()
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def compress_narrative(self, text: str, max_tokens: int = 4000) -> Tuple[str, Dict]:
        """
        Compress a long narrative hierarchically.
        """
        # Split into chapters/acts
        chapters = self._split_chapters(text)
        
        compressed_chapters = []
        total_stats = {'chapters': len(chapters), 'original_tokens': 0, 'final_tokens': 0}
        
        for i, chapter in enumerate(chapters):
            # Compress each chapter
            compressed, ratio, stats = self.base_compressor.compress(chapter)
            
            # Further compress if needed
            if len(self.encoder.encode(compressed)) > max_tokens // len(chapters):
                # Extract key beats only
                compressed = self._extract_beats(compressed)
            
            compressed_chapters.append(f"[CH{i+1}] {compressed}")
            total_stats['original_tokens'] += stats['original_tokens']
            total_stats['final_tokens'] += stats['final_tokens']
        
        result = '\n'.join(compressed_chapters)
        total_stats['compression_ratio'] = 1 - (total_stats['final_tokens'] / total_stats['original_tokens'])
        
        return result, total_stats
    
    def _split_chapters(self, text: str) -> List[str]:
        """Split text into chapters or major sections."""
        # Look for chapter markers
        chapter_patterns = [
            r'Chapter\s+\d+',
            r'CHAPTER\s+[IVXLCDM]+',
            r'ACT\s+[IVXLCDM]+',
            r'\n\s*\d+\.\s*\n',
            r'\n\s*#{2,}\s*\n'  # Markdown headers
        ]
        
        for pattern in chapter_patterns:
            splits = re.split(pattern, text)
            if len(splits) > 1:
                return splits
        
        # Fallback: split by size
        words = text.split()
        chunk_size = len(words) // 10  # 10 pseudo-chapters
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(' '.join(words[i:i+chunk_size]))
        return chunks
    
    def _extract_beats(self, text: str) -> str:
        """Extract only story beats and key events."""
        sentences = nltk.sent_tokenize(text)
        
        # Keep sentences with action verbs and key narrative elements
        beats = []
        for sent in sentences:
            if any(marker in sent for marker in [
                ':', '"', 'INT.', 'EXT.',  # Dialogue and scene markers
                'kill', 'die', 'reveal', 'discover', 'escape',  # Action
                'love', 'hate', 'betray', 'forgive',  # Emotion
                'decide', 'choose', 'realize', 'understand'  # Decisions
            ]):
                beats.append(sent)
        
        return ' '.join(beats[:20])  # Keep top 20 beats