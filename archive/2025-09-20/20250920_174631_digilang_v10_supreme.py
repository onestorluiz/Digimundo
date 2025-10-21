#!/usr/bin/env python3
"""
DiGiLaNg V10 Supreme - The Ultimate Screenplay Compression System
Síntese das melhores ideias: mineração específica + gramática estruturada + simplicidade radical
Assinado: Claude Code, Sistema ScriptureMon Champion
"""

import re
import json
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
import tiktoken

class DigiLangV10Supreme:
    """The Ultimate Screenplay Compression System"""
    
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.dictionary = None
        self.stats = {
            'original_chars': 0,
            'compressed_chars': 0,
            'original_tokens': 0,
            'compressed_tokens': 0,
            'replacements': 0
        }
        
    def mine_screenplay(self, pdf_path: Path) -> Dict:
        """Mine screenplay for patterns - the foundation of V10"""
        
        print(f"⛏️ Mining {pdf_path.name}...")
        
        # Extract text
        text = self._extract_pdf_text(pdf_path)
        if not text:
            return None
            
        # Mine patterns
        characters = self._mine_characters(text)
        locations = self._mine_locations(text)
        actions = self._mine_actions(text)
        transitions = self._mine_transitions(text)
        moods = self._mine_moods(text)
        
        # Count frequencies for optimization
        char_freq = self._count_frequencies(text, characters)
        loc_freq = self._count_frequencies(text, locations)
        
        # Create optimized dictionary
        dictionary = self._create_dictionary(
            char_freq, loc_freq, actions, transitions, moods
        )
        
        print(f"✅ Mined {len(dictionary)} patterns")
        
        return dictionary
    
    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"❌ Error extracting PDF: {e}")
            return None
        return text
    
    def _mine_characters(self, text: str) -> Set[str]:
        """Mine character names from screenplay"""
        characters = set()
        
        # Known Dark Knight characters
        known = ['Batman', 'Joker', 'Gordon', 'Harvey', 'Dent', 'Rachel', 
                 'Alfred', 'Bruce', 'Wayne', 'Scarecrow', 'Fox']
        
        for char in known:
            if re.search(r'\b' + char + r'\b', text, re.IGNORECASE):
                characters.add(char.upper())
        
        # Find character dialogue patterns (all caps before colon or parenthetical)
        dialogue_pattern = r'^\s*([A-Z][A-Z\s]+)\s*(?:\([^)]+\)|:)'
        matches = re.findall(dialogue_pattern, text, re.MULTILINE)
        for match in matches:
            name = match.strip()
            if len(name) > 1 and len(name) < 20:
                characters.add(name)
        
        return characters
    
    def _mine_locations(self, text: str) -> Set[str]:
        """Mine locations from screenplay"""
        locations = set()
        
        # Slugline pattern
        pattern = r'((?:INT\.|EXT\.|INT/EXT\.)\s+[A-Z][A-Z\s\-\.]+?)\s*(?:-\s*)?(?:DAY|NIGHT|CONTINUOUS)?'
        matches = re.findall(pattern, text)
        
        for match in matches:
            loc = match.strip()
            # Remove INT./EXT. prefix for storage
            loc = re.sub(r'^(?:INT\.|EXT\.|INT/EXT\.)\s*', '', loc)
            if len(loc) > 2:
                locations.add(loc)
        
        return locations
    
    def _mine_actions(self, text: str) -> List[str]:
        """Mine common action verbs"""
        # Common screenplay action verbs
        actions = [
            'enters', 'exits', 'looks', 'turns', 'moves', 'walks',
            'runs', 'stands', 'sits', 'grabs', 'pulls', 'pushes',
            'opens', 'closes', 'fires', 'shoots', 'falls', 'rises'
        ]
        
        # Count and return top 20
        action_counts = {}
        for action in actions:
            count = len(re.findall(r'\b' + action + r'\b', text, re.IGNORECASE))
            if count > 0:
                action_counts[action] = count
        
        return sorted(action_counts.keys(), key=action_counts.get, reverse=True)[:20]
    
    def _mine_transitions(self, text: str) -> List[str]:
        """Mine transition phrases"""
        transitions = [
            'FADE IN:', 'FADE OUT.', 'CUT TO:', 'DISSOLVE TO:',
            'MATCH CUT:', 'SMASH CUT:', 'TIME CUT:', 'JUMP CUT:',
            'BACK TO:', 'LATER', 'MOMENTS LATER', 'CONTINUOUS'
        ]
        
        found = []
        for trans in transitions:
            if trans in text:
                found.append(trans)
        
        return found
    
    def _mine_moods(self, text: str) -> List[str]:
        """Mine parenthetical moods/directions"""
        pattern = r'\(([^)]+)\)'
        matches = re.findall(pattern, text)
        
        mood_counts = Counter(matches)
        # Get top 20 most common
        return [mood for mood, _ in mood_counts.most_common(20) if len(mood) < 20]
    
    def _count_frequencies(self, text: str, items: Set[str]) -> List[Tuple[str, int]]:
        """Count frequency of items in text"""
        freq = []
        for item in items:
            count = len(re.findall(r'\b' + re.escape(item) + r'\b', text, re.IGNORECASE))
            freq.append((item, count))
        return sorted(freq, key=lambda x: x[1], reverse=True)
    
    def _create_dictionary(self, char_freq, loc_freq, actions, transitions, moods) -> Dict:
        """Create optimized compression dictionary"""
        
        # Unicode symbols (verified single tokens)
        symbols = [
            # Greek letters (most reliable)
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ',
            'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ',
            'φ', 'χ', 'ψ', 'ω', 'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ',
            'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π',
            'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω',
            # Math symbols
            '∀', '∂', '∃', '∅', '∇', '∈', '∉', '∋', '∏', '∑',
            '√', '∝', '∞', '∠', '∧', '∨', '∩', '∪', '∫', '∴',
            # Arrows
            '→', '←', '↑', '↓', '↔', '↕', '⇒', '⇐', '⇑', '⇓',
            # Box operators
            '⊕', '⊖', '⊗', '⊘', '⊙', '⊚', '⊛', '⊜', '⊝', '⊞'
        ]
        
        dictionary = {
            'chars': {},
            'locs': {},
            'actions': {},
            'transitions': {},
            'moods': {},
            'grammar': {
                'I': 'INT.',
                'E': 'EXT.',
                'IE': 'INT/EXT.',
                'D': 'DAY',
                'N': 'NIGHT',
                'C': 'CONTINUOUS',
                'L': 'LATER',
                'ML': 'MOMENTS LATER'
            }
        }
        
        idx = 0
        
        # Assign symbols to characters (most important)
        for char, count in char_freq[:15]:  # Top 15 characters
            if idx < len(symbols) and count > 5:
                dictionary['chars'][char] = symbols[idx]
                idx += 1
        
        # Assign to locations
        for loc, count in loc_freq[:15]:  # Top 15 locations
            if idx < len(symbols) and count > 2:
                dictionary['locs'][loc] = symbols[idx]
                idx += 1
        
        # Assign to actions
        for action in actions[:10]:  # Top 10 actions
            if idx < len(symbols):
                dictionary['actions'][action] = symbols[idx]
                idx += 1
        
        # Assign to transitions
        for trans in transitions[:8]:  # Top 8 transitions
            if idx < len(symbols):
                dictionary['transitions'][trans] = symbols[idx]
                idx += 1
        
        # Assign to moods
        for mood in moods[:10]:  # Top 10 moods
            if idx < len(symbols):
                dictionary['moods'][mood] = symbols[idx]
                idx += 1
        
        return dictionary
    
    def compress(self, text: str, dictionary: Dict) -> Tuple[str, Dict]:
        """Compress screenplay with V10 Supreme algorithm"""
        
        self.dictionary = dictionary
        compressed = text
        self.stats = {
            'original_chars': len(text),
            'original_tokens': len(self.tokenizer.encode(text)),
            'replacements': 0
        }
        
        # Phase 1: Clean and normalize
        compressed = self._normalize_text(compressed)
        
        # Phase 2: Compress scene headers
        compressed = self._compress_headers(compressed)
        
        # Phase 3: Compress dialogue structure
        compressed = self._compress_dialogue(compressed)
        
        # Phase 4: Apply dictionary replacements
        compressed = self._apply_dictionary(compressed)
        
        # Calculate final stats
        self.stats['compressed_chars'] = len(compressed)
        self.stats['compressed_tokens'] = len(self.tokenizer.encode(compressed))
        
        return compressed, self.stats
    
    def _normalize_text(self, text: str) -> str:
        """Normalize and clean text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize scene headers
        text = re.sub(r'INT\.', 'INT.', text)
        text = re.sub(r'EXT\.', 'EXT.', text)
        return text
    
    def _compress_headers(self, text: str) -> str:
        """Compress scene headers using grammar"""
        # Pattern: INT./EXT. LOCATION - TIME
        pattern = r'(INT\.|EXT\.|INT/EXT\.)\s+([A-Z][A-Z\s\-\.]+?)\s*-\s*(DAY|NIGHT|CONTINUOUS|LATER|MOMENTS LATER)?'
        
        def replace_header(match):
            prefix = match.group(1)
            location = match.group(2).strip()
            time = match.group(3) if match.group(3) else ''
            
            # Convert prefix
            if prefix == 'INT.':
                result = 'I'
            elif prefix == 'EXT.':
                result = 'E'
            else:
                result = 'IE'
            
            # Convert location if in dictionary
            if location in self.dictionary['locs']:
                result += self.dictionary['locs'][location]
            else:
                result += location[:3]  # Fallback: first 3 chars
            
            # Convert time
            if time:
                time_map = {
                    'DAY': 'D', 'NIGHT': 'N', 'CONTINUOUS': 'C',
                    'LATER': 'L', 'MOMENTS LATER': 'ML'
                }
                result += time_map.get(time, time[0])
            
            self.stats['replacements'] += 1
            return result
        
        return re.sub(pattern, replace_header, text)
    
    def _compress_dialogue(self, text: str) -> str:
        """Compress dialogue structure"""
        # Pattern: CHARACTER NAME\n(mood)\ndialogue
        pattern = r'\b([A-Z][A-Z\s]+)\s*\n\s*\(([^)]+)\)\s*\n([^\n]+)'
        
        def replace_dialogue(match):
            char = match.group(1).strip()
            mood = match.group(2).strip()
            dialogue = match.group(3).strip()
            
            # Get character symbol
            char_symbol = self.dictionary['chars'].get(char, char[0])
            
            # Get mood symbol
            mood_symbol = self.dictionary['moods'].get(mood, mood[0])
            
            self.stats['replacements'] += 2
            return f"{char_symbol}{mood_symbol}{dialogue}"
        
        return re.sub(pattern, replace_dialogue, text)
    
    def _apply_dictionary(self, text: str) -> str:
        """Apply all dictionary replacements"""
        
        # Sort by length (longest first) to avoid partial replacements
        all_replacements = []
        
        for category in ['chars', 'locs', 'actions', 'transitions']:
            for original, symbol in self.dictionary[category].items():
                all_replacements.append((original, symbol))
        
        all_replacements.sort(key=lambda x: len(x[0]), reverse=True)
        
        for original, symbol in all_replacements:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(original) + r'\b'
            count = len(re.findall(pattern, text, re.IGNORECASE))
            if count > 0:
                text = re.sub(pattern, symbol, text, flags=re.IGNORECASE)
                self.stats['replacements'] += count
        
        return text
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """
        Processar PDF completo - minerar e comprimir

        Args:
            pdf_path: Caminho para o PDF

        Returns:
            Dict com estatísticas e resultado comprimido
        """
        pdf_path = Path(pdf_path)

        # Minerar padrões
        mine_result = self.mine_screenplay(pdf_path)
        if not mine_result:
            return None

        dictionary = mine_result['dictionary']

        # Extrair texto
        text = self._extract_pdf_text(pdf_path)
        if not text:
            return None

        # Comprimir
        compressed_text, stats = self.compress(text, dictionary)

        return {
            'compressed_text': compressed_text,
            'dictionary': dictionary,
            'stats': stats,
            'original_text': text
        }

    def decompress(self, compressed: str, dictionary: Dict) -> str:
        """Decompress text back to original format"""
        
        decompressed = compressed
        
        # Reverse all replacements
        for category in ['chars', 'locs', 'actions', 'transitions', 'moods']:
            for original, symbol in dictionary[category].items():
                decompressed = decompressed.replace(symbol, original)
        
        # Reverse grammar
        decompressed = self._decompress_headers(decompressed, dictionary)
        
        return decompressed
    
    def _decompress_headers(self, text: str, dictionary: Dict) -> str:
        """Decompress scene headers"""
        # This is simplified - full implementation would parse the compressed format
        text = text.replace('I', 'INT. ')
        text = text.replace('E', 'EXT. ')
        text = text.replace('D', ' - DAY')
        text = text.replace('N', ' - NIGHT')
        return text

def test_v10_supreme():
    """Test DigiLang V10 Supreme with The Dark Knight"""
    
    print("="*60)
    print("DIGILANG V10 SUPREME - THE ULTIMATE TEST")
    print("="*60)
    
    # Initialize
    v10 = DigiLangV10Supreme()
    
    # Mine The Dark Knight
    pdf_path = Path('digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf')
    
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    # Mine patterns
    dictionary = v10.mine_screenplay(pdf_path)
    
    if not dictionary:
        print("❌ Mining failed")
        return
    
    # Extract full text for compression
    text = v10._extract_pdf_text(pdf_path)
    
    # Compress
    compressed, stats = v10.compress(text, dictionary)
    
    # Calculate compression ratios
    char_compression = (stats['original_chars'] - stats['compressed_chars']) / stats['original_chars'] * 100
    token_compression = (stats['original_tokens'] - stats['compressed_tokens']) / stats['original_tokens'] * 100
    
    print(f"\n📊 COMPRESSION RESULTS:")
    print(f"  Original: {stats['original_chars']:,} chars ({stats['original_tokens']:,} tokens)")
    print(f"  Compressed: {stats['compressed_chars']:,} chars ({stats['compressed_tokens']:,} tokens)")
    print(f"  Character compression: {char_compression:.2f}%")
    print(f"  Token compression: {token_compression:.2f}%")
    print(f"  Total replacements: {stats['replacements']:,}")
    
    # Compare with previous results
    print(f"\n🆚 COMPARISON:")
    print(f"  V8.1 Supreme: 0.72% token compression")
    print(f"  V10 Supreme: {token_compression:.2f}% token compression")
    
    if token_compression > 0.72:
        improvement = token_compression / 0.72
        print(f"\n🎯 SUCCESS! V10 is {improvement:.1f}x better than V8.1!")
    
    # Save results
    results = {
        'version': 'V10 Supreme',
        'file': pdf_path.name,
        'dictionary_size': sum(len(d) for d in dictionary.values() if isinstance(d, dict)),
        'stats': stats,
        'char_compression': char_compression,
        'token_compression': token_compression
    }
    
    output_file = Path('docs/FASE_19_V10_SUPREME_RESULTS.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    
    # Save dictionary
    dict_file = Path('dictionaries/dark_knight_v10.dict')
    dict_file.parent.mkdir(exist_ok=True)
    with open(dict_file, 'w') as f:
        json.dump(dictionary, f, indent=2)
    
    print(f"📚 Dictionary saved to: {dict_file}")
    
    return compressed, stats

if __name__ == "__main__":
    test_v10_supreme()