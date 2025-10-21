#!/usr/bin/env python3
"""
DiGiLaNg V9 Academic - Adaptive Content-Aware Compression
Combines screenplay patterns (V8.1) with theory patterns (17.b)
Automatically detects content type and applies appropriate patterns
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DigiLangV9Academic")

class DigiLangV9Academic:
    """Adaptive compression with content type detection"""
    
    def __init__(self):
        # Load both pattern sets
        self.screenplay_patterns = self._load_screenplay_patterns()
        self.theory_patterns = self._load_theory_patterns()
        
        # Content detection keywords
        self.screenplay_indicators = [
            "INT.", "EXT.", "FADE IN", "CUT TO", "(CONT'D)",
            "CONTINUED:", "ANGLE ON", "CLOSE UP", "PAN TO"
        ]
        
        self.theory_indicators = [
            "Chapter", "Section", "Introduction", "Conclusion",
            "Figure", "Table", "References", "Bibliography",
            "Abstract", "Keywords"
        ]
        
        # Technical terms for theory detection
        self.technical_terms = [
            "protagonist", "antagonist", "three-act", "character arc",
            "plot structure", "narrative", "exposition", "denouement"
        ]
        
    def _load_screenplay_patterns(self) -> Dict[str, str]:
        """Load V8.1 Supreme screenplay patterns"""
        # Verified single-token Unicode characters from V8.1
        patterns = {}
        
        # ASCII symbols (all verified as single tokens)
        ascii_symbols = ['~', '!', '@', '#', '$', '%', '^', '&', '*']
        
        # Greek letters (all verified as single tokens)
        greek_letters = [
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ',
            'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ',
            'φ', 'χ', 'ψ', 'ω', 'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ'
        ]
        
        # Mathematical symbols (verified single tokens)
        math_symbols = [
            '∀', '∂', '∃', '∅', '∇', '∈', '∉', '∋', '∏', '∑',
            '√', '∝', '∞', '∠', '∧', '∨', '∩', '∪', '∫', '∴'
        ]
        
        # Currency and other symbols (verified single tokens)
        currency_symbols = ['€', '£', '¥', '¢', '¤', '§', '©', '®', '°', '±']
        
        # Combine all single-token characters
        all_chars = ascii_symbols + greek_letters + math_symbols + currency_symbols
        
        # Top screenplay patterns from V8.1
        screenplay_terms = [
            "FADE IN:", "FADE OUT.", "CUT TO:", "DISSOLVE TO:",
            "INT.", "EXT.", "CONTINUED:", "(CONT'D)",
            "CLOSE UP", "ANGLE ON", "PAN TO", "ZOOM IN",
            "BACK TO:", "LATER", "CONTINUOUS", "SAME",
            "MORNING", "NIGHT", "DAY", "EVENING"
        ]
        
        # Assign patterns
        for i, term in enumerate(screenplay_terms[:len(all_chars)]):
            patterns[term] = all_chars[i]
            
        return patterns
    
    def _load_theory_patterns(self) -> Dict[str, str]:
        """Load theory patterns from FASE 17.b"""
        theory_file = Path('theory_patterns.json')
        
        if theory_file.exists():
            with open(theory_file, 'r') as f:
                raw_patterns = json.load(f)
        else:
            # Fallback patterns from mining
            raw_patterns = {
                "TT_SCENE": "scene",
                "TT_CONFLICT": "conflict",
                "TT_PLOT": "plot",
                "TT_DIALOGUE": "dialogue",
                "TT_THEME": "theme",
                "TT_NARRATIVE": "narrative",
                "TT_PROTAGONIS": "protagonist",
                "TT_BEAT": "beat",
                "TT_CLIMAX": "climax",
                "TT_CHARACTER_": "character arc",
                "SN_BEGINNING": "beginning",
                "SN_ENDING": "ending",
                "SN_MIDDLE": "middle",
                "SN_FIRST_ACT": "first act",
                "SN_SECOND_ACT": "second act"
            }
        
        # Map to Unicode characters (starting after screenplay patterns)
        patterns = {}
        
        # Additional Unicode blocks for theory patterns
        theory_chars = [
            '⊕', '⊖', '⊗', '⊘', '⊙', '⊚', '⊛', '⊜', '⊝', '⊞',
            '⊟', '⊠', '⊡', '⊢', '⊣', '⊤', '⊥', '⊦', '⊧', '⊨',
            '⊩', '⊪', '⊫', '⊬', '⊭', '⊮', '⊯', '⊰', '⊱', '⊲'
        ]
        
        # Convert theory patterns to compression codes
        i = 0
        for code, term in raw_patterns.items():
            if i < len(theory_chars):
                patterns[term] = theory_chars[i]
                i += 1
            else:
                break
                
        return patterns
    
    def detect_content_type(self, text: str) -> str:
        """Detect if content is screenplay or theory book"""
        text_sample = text[:5000]  # Analyze first 5000 chars
        
        # Count indicators
        screenplay_score = 0
        theory_score = 0
        
        # Check screenplay indicators
        for indicator in self.screenplay_indicators:
            screenplay_score += text_sample.count(indicator)
        
        # Check theory indicators
        for indicator in self.theory_indicators:
            theory_score += text_sample.count(indicator) * 2  # Weight theory higher
        
        # Check technical terms
        text_lower = text_sample.lower()
        for term in self.technical_terms:
            if term in text_lower:
                theory_score += 5
        
        # Check formatting patterns
        if re.search(r'^\s{10,}[A-Z][A-Z\s]+$', text_sample, re.MULTILINE):
            screenplay_score += 10  # Character names in screenplay format
        
        if re.search(r'^Chapter \d+', text_sample, re.MULTILINE):
            theory_score += 20
        
        logger.info(f"Content detection - Screenplay: {screenplay_score}, Theory: {theory_score}")
        
        if screenplay_score > theory_score:
            return "screenplay"
        elif theory_score > screenplay_score:
            return "theory"
        else:
            return "mixed"
    
    def compress(self, text: str, force_type: Optional[str] = None) -> Tuple[str, Dict]:
        """Compress text with adaptive pattern selection"""
        
        # Detect content type if not forced
        content_type = force_type or self.detect_content_type(text)
        
        # Select appropriate patterns
        if content_type == "screenplay":
            patterns = self.screenplay_patterns
            logger.info("Using screenplay patterns")
        elif content_type == "theory":
            patterns = self.theory_patterns
            logger.info("Using theory patterns")
        else:
            # Mixed content - use both
            patterns = {**self.screenplay_patterns, **self.theory_patterns}
            logger.info("Using mixed patterns")
        
        # Apply compression
        compressed = text
        replacements = 0
        tokens_saved = 0
        
        # Sort patterns by length (longest first) to avoid partial replacements
        sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[0]), reverse=True)
        
        for original, replacement in sorted_patterns:
            # Use word boundaries for multi-word patterns
            if ' ' in original:
                pattern = r'\b' + re.escape(original) + r'\b'
            else:
                pattern = r'\b' + re.escape(original) + r'\b'
            
            matches = len(re.findall(pattern, compressed, re.IGNORECASE))
            if matches > 0:
                compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
                replacements += matches
                # Estimate token savings (rough estimate)
                tokens_saved += matches * (len(original.split()) - 1)
        
        # Calculate statistics
        original_len = len(text)
        compressed_len = len(compressed)
        compression_ratio = (original_len - compressed_len) / original_len if original_len > 0 else 0
        
        stats = {
            'content_type': content_type,
            'original_length': original_len,
            'compressed_length': compressed_len,
            'compression_ratio': compression_ratio,
            'replacements': replacements,
            'tokens_saved': tokens_saved,
            'patterns_used': len([p for p in patterns if p in text])
        }
        
        return compressed, stats
    
    def decompress(self, compressed_text: str, content_type: Optional[str] = None) -> str:
        """Decompress text"""
        
        # Determine which patterns to use
        if content_type == "screenplay":
            patterns = self.screenplay_patterns
        elif content_type == "theory":
            patterns = self.theory_patterns
        else:
            patterns = {**self.screenplay_patterns, **self.theory_patterns}
        
        # Reverse the patterns
        decompressed = compressed_text
        
        # Apply in reverse order (shortest patterns first)
        sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[0]))
        
        for original, replacement in sorted_patterns:
            decompressed = decompressed.replace(replacement, original)
        
        return decompressed
    
    def analyze_document(self, file_path: str) -> Dict:
        """Analyze a document and return detailed metrics"""
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Detect type
        content_type = self.detect_content_type(text)
        
        # Try compression with both pattern sets
        screenplay_compressed, screenplay_stats = self.compress(text, force_type="screenplay")
        theory_compressed, theory_stats = self.compress(text, force_type="theory")
        mixed_compressed, mixed_stats = self.compress(text, force_type="mixed")
        
        # Determine best approach
        best_compression = max(
            screenplay_stats['compression_ratio'],
            theory_stats['compression_ratio'],
            mixed_stats['compression_ratio']
        )
        
        if best_compression == screenplay_stats['compression_ratio']:
            best_type = "screenplay"
        elif best_compression == theory_stats['compression_ratio']:
            best_type = "theory"
        else:
            best_type = "mixed"
        
        return {
            'file': file_path,
            'detected_type': content_type,
            'best_type': best_type,
            'screenplay_compression': screenplay_stats['compression_ratio'],
            'theory_compression': theory_stats['compression_ratio'],
            'mixed_compression': mixed_stats['compression_ratio'],
            'best_compression': best_compression,
            'recommendation': f"Use {best_type} patterns for {best_compression:.2%} compression"
        }

def test_v9_academic():
    """Test the V9 Academic system"""
    
    print("="*60)
    print("DIGILANG V9 ACADEMIC - ADAPTIVE COMPRESSION TEST")
    print("="*60)
    
    encoder = DigiLangV9Academic()
    
    # Test screenplay content
    screenplay_text = """
    FADE IN:
    
    INT. COFFEE SHOP - DAY
    
    JOHN enters the coffee shop. He looks around nervously.
    
    JOHN
    (to himself)
    Where is she?
    
    CUT TO:
    
    EXT. STREET - CONTINUOUS
    
    MARY walks quickly down the street.
    """
    
    print("\n1. SCREENPLAY CONTENT TEST:")
    compressed, stats = encoder.compress(screenplay_text)
    print(f"   Content type detected: {stats['content_type']}")
    print(f"   Compression ratio: {stats['compression_ratio']:.2%}")
    print(f"   Replacements made: {stats['replacements']}")
    
    # Test theory content
    theory_text = """
    Chapter 3: Understanding Character Development
    
    The protagonist in any narrative must undergo a character arc that 
    demonstrates growth. This character arc is essential to the plot 
    structure. In the first act, we establish the protagonist's normal 
    world. The conflict arises when the antagonist challenges this 
    equilibrium.
    
    The theme emerges through the protagonist's journey from the beginning 
    through the middle to the ending. Each scene must advance either plot 
    or character development, ideally both.
    """
    
    print("\n2. THEORY BOOK CONTENT TEST:")
    compressed, stats = encoder.compress(theory_text)
    print(f"   Content type detected: {stats['content_type']}")
    print(f"   Compression ratio: {stats['compression_ratio']:.2%}")
    print(f"   Replacements made: {stats['replacements']}")
    
    # Test mixed content
    mixed_text = screenplay_text + "\n\n" + theory_text
    
    print("\n3. MIXED CONTENT TEST:")
    compressed, stats = encoder.compress(mixed_text)
    print(f"   Content type detected: {stats['content_type']}")
    print(f"   Compression ratio: {stats['compression_ratio']:.2%}")
    print(f"   Replacements made: {stats['replacements']}")
    
    # Test decompression
    print("\n4. DECOMPRESSION TEST:")
    decompressed = encoder.decompress(compressed, stats['content_type'])
    match_ratio = len([i for i, j in zip(mixed_text, decompressed) if i == j]) / len(mixed_text)
    print(f"   Decompression accuracy: {match_ratio:.2%}")
    
    print("\n" + "="*60)
    print("V9 ACADEMIC TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_v9_academic()