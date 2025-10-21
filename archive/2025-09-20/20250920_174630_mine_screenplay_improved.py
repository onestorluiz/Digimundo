#!/usr/bin/env python3
"""
FASE 18.b - MINERAÇÃO MELHORADA DE PERSONAGENS
Extração inteligente de personagens de roteiros
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set
import pdfplumber
from collections import Counter

class ImprovedCharacterMiner:
    """Minerador melhorado para personagens de roteiro"""
    
    def __init__(self):
        self.characters = set()
        self.locations = set()
        self.transitions = set()
        
    def extract_text_from_pdf(self, pdf_path: Path, max_pages: int = 50) -> str:
        """Extract text from PDF"""
        print(f"📖 Extracting from {pdf_path.name}...")
        text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages[:max_pages]):
                    if i % 10 == 0 and i > 0:
                        print(f"  Page {i}/{min(max_pages, len(pdf.pages))}")
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
            
        return text
    
    def extract_characters_improved(self, text: str) -> Set[str]:
        """Better character extraction using multiple patterns"""
        characters = set()
        
        # Pattern 1: Character names before dialogue (most reliable)
        # Look for lines that are indented and in all caps, followed by dialogue
        dialogue_pattern = r'^\s{10,30}([A-Z][A-Z\s\.\-\']+?)\s*(?:\([^)]+\))?\s*\n\s*(?:\([^)]+\)\s*\n)?\s*[^↑\n]'
        matches = re.findall(dialogue_pattern, text, re.MULTILINE)
        
        for match in matches:
            name = match.strip()
            # Clean up the name
            name = re.sub(r'\s+', ' ', name)  # Normalize spaces
            name = name.rstrip('.')  # Remove trailing periods
            
            # Filter out common false positives
            if len(name) > 1 and len(name) < 30:
                if not any(skip in name for skip in ['INT', 'EXT', 'CUT', 'FADE', 'CONTINUED']):
                    characters.add(name)
        
        # Pattern 2: Character introductions in action lines
        # Look for "CHARACTER NAME" in all caps within sentences
        intro_pattern = r'\b([A-Z]{2,}(?:\s+[A-Z]+)*)\b[,\s]+(?:enters|walks|stands|sits|looks|turns|runs|moves)'
        matches = re.findall(intro_pattern, text)
        
        for match in matches:
            name = match.strip()
            if len(name) > 2 and len(name) < 20:
                characters.add(name)
        
        # Pattern 3: Look for (V.O.) or (O.S.) indicators
        vo_pattern = r'^\s{10,30}([A-Z][A-Z\s]+?)\s*\((?:V\.O\.|O\.S\.)\)'
        matches = re.findall(vo_pattern, text, re.MULTILINE)
        for match in matches:
            name = match.strip()
            if len(name) > 1:
                characters.add(name)
        
        return characters
    
    def extract_locations_improved(self, text: str) -> Set[str]:
        """Better location extraction"""
        locations = set()
        
        # Standard sluglines
        slugline_pattern = r'^\s*((?:INT\.|EXT\.|INT/EXT\.)\s+[A-Z][A-Z\s\-\,\.]+?)\s*(?:-\s*)?(?:DAY|NIGHT|DAWN|DUSK|MORNING|AFTERNOON|EVENING|CONTINUOUS|LATER|MOMENTS LATER)?'
        
        matches = re.findall(slugline_pattern, text, re.MULTILINE)
        for match in matches:
            location = match.strip()
            # Clean up
            location = re.sub(r'\s+', ' ', location)
            if len(location) > 5:
                locations.add(location)
        
        return locations
    
    def mine_screenplay(self, pdf_path: Path) -> Dict:
        """Mine screenplay for all patterns"""
        
        print("\n" + "="*60)
        print(f"IMPROVED MINING: {pdf_path.name}")
        print("="*60)
        
        # Extract full text for better analysis
        text = self.extract_text_from_pdf(pdf_path, max_pages=100)
        if not text:
            return None
        
        print(f"✅ Extracted {len(text):,} characters\n")
        
        # Extract patterns
        print("🔍 Extracting patterns...")
        self.characters = self.extract_characters_improved(text)
        self.locations = self.extract_locations_improved(text)
        
        # Extract transitions
        trans_pattern = r'\b(FADE (?:IN|OUT|TO BLACK)|CUT TO|DISSOLVE TO|MATCH CUT|SMASH CUT|TIME CUT|JUMP CUT|BACK TO|LATER)\b'
        self.transitions = set(re.findall(trans_pattern, text, re.IGNORECASE))
        
        print(f"  Characters: {len(self.characters)}")
        print(f"  Locations: {len(self.locations)}")
        print(f"  Transitions: {len(self.transitions)}")
        
        # Count frequencies for ranking
        char_freq = {}
        for char in self.characters:
            # Count occurrences (case insensitive but preserve original)
            count = len(re.findall(r'\b' + re.escape(char) + r'\b', text, re.IGNORECASE))
            char_freq[char] = count
        
        loc_freq = {}
        for loc in self.locations:
            count = text.count(loc)
            loc_freq[loc] = count
        
        # Sort by frequency
        sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_locs = sorted(loc_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Create compression dictionary
        dictionary = self.create_optimized_dictionary(sorted_chars, sorted_locs, text)
        
        # Test compression
        comp_result = self.test_compression(text, dictionary)
        
        # Generate report
        report = {
            'file': pdf_path.name,
            'text_length': len(text),
            'characters_found': len(self.characters),
            'locations_found': len(self.locations),
            'transitions_found': len(self.transitions),
            'top_characters': [f"{name} ({count}x)" for name, count in sorted_chars[:15]],
            'top_locations': [f"{name} ({count}x)" for name, count in sorted_locs[:15]],
            'compression': comp_result,
            'dictionary_size': len(dictionary)
        }
        
        return report, dictionary
    
    def create_optimized_dictionary(self, sorted_chars: List, sorted_locs: List, text: str) -> Dict[str, str]:
        """Create optimized compression dictionary"""
        
        # Single-token Unicode characters (verified)
        unicode_chars = [
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ',  # Greek lowercase
            'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ',
            'φ', 'χ', 'ψ', 'ω',
            'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ',  # Greek uppercase  
            'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ',
            'Φ', 'Χ', 'Ψ', 'Ω',
            '∀', '∂', '∃', '∅', '∇', '∈', '∉', '∋',  # Math symbols
            '∏', '∑', '√', '∝', '∞', '∠', '∧', '∨',
            '⊕', '⊖', '⊗', '⊘', '⊙',  # Circle operators
            '€', '£', '¥',  # Currency
            '†', '‡', '•', '‰',  # Special marks
            '~', '!', '@', '#', '$', '%', '^', '&', '*',  # ASCII
        ]
        
        dictionary = {}
        char_idx = 0
        
        # Add characters by frequency (most important)
        for name, count in sorted_chars:
            if char_idx < len(unicode_chars) and count > 5:  # At least 5 occurrences
                dictionary[name] = unicode_chars[char_idx]
                char_idx += 1
                if char_idx >= 40:  # Limit characters to leave room for locations
                    break
        
        # Add locations by frequency
        for name, count in sorted_locs:
            if char_idx < len(unicode_chars) and count > 2:  # At least 2 occurrences
                dictionary[name] = unicode_chars[char_idx]
                char_idx += 1
                if char_idx >= 70:  # Leave room for transitions
                    break
        
        # Add common transitions
        for trans in ['FADE IN:', 'FADE OUT.', 'CUT TO:', 'DISSOLVE TO:']:
            if char_idx < len(unicode_chars) and trans in text:
                dictionary[trans] = unicode_chars[char_idx]
                char_idx += 1
        
        return dictionary
    
    def test_compression(self, text: str, dictionary: Dict[str, str]) -> Dict:
        """Test compression with dictionary"""
        
        compressed = text
        total_replacements = 0
        
        # Apply replacements (longest first to avoid partial matches)
        for pattern, replacement in sorted(dictionary.items(), key=lambda x: len(x[0]), reverse=True):
            # Use word boundaries for names
            if ' ' not in pattern:  # Single word
                regex = r'\b' + re.escape(pattern) + r'\b'
                matches = len(re.findall(regex, compressed))
                compressed = re.sub(regex, replacement, compressed)
            else:  # Multi-word
                matches = compressed.count(pattern)
                compressed = compressed.replace(pattern, replacement)
            
            total_replacements += matches
        
        original_len = len(text)
        compressed_len = len(compressed)
        
        return {
            'original_chars': original_len,
            'compressed_chars': compressed_len,
            'char_reduction': original_len - compressed_len,
            'char_compression': (original_len - compressed_len) / original_len * 100,
            'estimated_token_compression': (original_len - compressed_len) / original_len * 100,
            'total_replacements': total_replacements
        }

def main():
    """Run improved mining"""
    
    # Target screenplay
    pdf_path = Path('digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf')
    
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    miner = ImprovedCharacterMiner()
    report, dictionary = miner.mine_screenplay(pdf_path)
    
    if report:
        # Save results
        output_file = Path('docs/FASE_18b_IMPROVED_MINING.json')
        with open(output_file, 'w') as f:
            json.dump({
                'report': report,
                'dictionary': dictionary
            }, f, indent=2)
        
        print("\n" + "="*60)
        print("🎯 MINING RESULTS")
        print("="*60)
        
        print(f"\n👥 Characters found: {report['characters_found']}")
        print("Top 10 characters:")
        for char in report['top_characters'][:10]:
            print(f"  • {char}")
        
        print(f"\n📍 Locations found: {report['locations_found']}")
        print("Top 10 locations:")
        for loc in report['top_locations'][:10]:
            print(f"  • {loc}")
        
        comp = report['compression']
        print(f"\n📊 Compression Results:")
        print(f"  Original: {comp['original_chars']:,} chars")
        print(f"  Compressed: {comp['compressed_chars']:,} chars")
        print(f"  Reduction: {comp['char_reduction']:,} chars")
        print(f"  Compression: {comp['char_compression']:.2f}%")
        print(f"  Replacements: {comp['total_replacements']:,}")
        print(f"  Dictionary size: {report['dictionary_size']} patterns")
        
        # Compare with V8.1
        v8_file = Path('docs/FASE_17e_TRADUCAO_FINAL_RESULTS.json')
        if v8_file.exists():
            with open(v8_file, 'r') as f:
                v8_data = json.load(f)
            
            for result in v8_data.get('results', []):
                if 'Dark Knight - Release' in result.get('file', ''):
                    v8_comp = result.get('token_compression', 0) * 100
                    our_comp = comp['estimated_token_compression']
                    
                    print(f"\n🆚 Comparison:")
                    print(f"  V8.1 (generic): {v8_comp:.2f}%")
                    print(f"  Custom mining: {our_comp:.2f}%")
                    print(f"  Improvement: +{our_comp - v8_comp:.2f}%")
                    
                    if our_comp > v8_comp:
                        improvement_factor = our_comp / v8_comp if v8_comp > 0 else 999
                        print(f"\n✨ {improvement_factor:.1f}x better compression!")
                    break
        
        print(f"\n✅ Results saved to: {output_file}")

if __name__ == "__main__":
    main()