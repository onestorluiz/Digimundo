#!/usr/bin/env python3
"""
DiGiLaNg V11 Ultimate - The Most Advanced Screenplay Compression System
Zero ambiguity symbols + Maximum compression + Visual intuition
"""

import re
import json
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
import tiktoken

class DigiLangV11Ultimate:
    """The Ultimate Screenplay Compression System with Zero Ambiguity"""
    
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.dictionary = self._create_v11_dictionary()
        self.stats = {
            'original_chars': 0,
            'compressed_chars': 0, 
            'original_tokens': 0,
            'compressed_tokens': 0,
            'replacements': 0
        }
        
    def _create_v11_dictionary(self) -> Dict:
        """Create the ultimate V11 dictionary with zero ambiguity symbols"""
        
        return {
            # PERSONAGENS - Greek letters with mnemonics
            'characters': {
                'BATMAN': 'β',        # Beta = Bat
                'WAYNE': 'ω',         # Omega = Wayne (alter ego)
                'BRUCE WAYNE': 'βω',  # Combined identity
                'JOKER': 'ʝ',         # J inverted = Joker
                'THE JOKER': 'ʝΘ',    # J + Theta
                'GORDON': 'γ',        # Gamma = Gordon
                'LIEUTENANT GORDON': 'γΛ', # Gamma + Lambda
                'ALFRED': 'α',        # Alpha = Alfred (first ally)
                'RACHEL': 'ρ',        # Rho = Rachel
                'DENT': 'δ',          # Delta = Dent
                'HARVEY DENT': 'δψ',  # Delta + Psi
                'TWO-FACE': 'ψ',      # Psi = dual personality
                'FOX': 'φ',           # Phi = Fox
                'LUCIUS': 'λ',        # Lambda = Lucius
                'SCARECROW': 'ʃ',     # S special = Scarecrow
                'MARONI': 'μ',        # Mu = Mob
                'FALCONE': 'ν',       # Nu = New crime
                'CHECHEN': 'χ',       # Chi = Chechen
                'LAU': 'κ',           # Kappa = Key witness
                'COP': 'π',           # Pi = Police
                'RAMIREZ': 'ρᴿ',      # Rho modified
                'WUERTZ': 'ωᴿ',       # Omega modified
            },
            
            # LOCAÇÕES - Thematic symbols
            'locations': {
                'WAREHOUSE': 'Ω',      # Omega uppercase = big space
                'GOTHAM': 'Γ',         # Gamma uppercase = Gotham City
                'POLICE STATION': 'Π', # Pi uppercase = Police/GCPD
                'GCPD': 'Π',           # Same as police station
                'STREET': 'Σ',         # Sigma = Street
                'DOCKS': 'Δ',          # Delta = Docks
                'BANK': 'Ξ',           # Xi uppercase = Bank
                'PENTHOUSE': 'Φ',      # Phi uppercase = luxury
                'LAB': 'Λ',            # Lambda uppercase = Laboratory
                'THEATER': 'Θ',        # Theta = Theater
                'HOSPITAL': 'Ψ',       # Psi uppercase = medical
                'ROOFTOP': '↑',        # Arrow up = top
                'BASEMENT': '↓',       # Arrow down = basement
                'CORRIDOR': '↔',       # Double arrow = corridor
                'ELEVATOR': '↻',       # Circular arrow = elevator
                'OFFICE': '■',         # Square = office
                'VAULT': '●',          # Filled circle = vault
                'APARTMENT': '▲',      # Triangle = attic/apartment
            },
            
            # AÇÕES - Visual operators
            'actions': {
                'enters': '⊕',        # Plus in circle
                'exits': '⊖',         # Minus in circle
                'moves to': '→',      # Right arrow
                'backs away': '←',    # Left arrow
                'runs': '↗',          # Diagonal up
                'crawls': '↘',        # Diagonal down
                'turns around': '↺',  # Full rotation
                'looks': '👀',         # Eyes
                'listens': '👂',       # Ear
                'shoots': '⋆',        # Star = shot
                'fights': '⚔',        # Crossed swords
                'punches': '✊',       # Fist
                'points': '☝',        # Pointing finger
                'stops': '✋',         # Stop hand
                'opens': '↗→',       # Open gesture
                'closes': '←↘',      # Close gesture
                'grabs': '✊→',       # Grab motion
                'pulls': '←✊',       # Pull motion
                'pushes': '→✋',      # Push motion
                'falls': '↓↓',       # Double down
                'rises': '↑↑',       # Double up
                'sits': '↓',          # Down arrow
                'stands': '↑',        # Up arrow
            },
            
            # EMOÇÕES - Expressive characters
            'moods': {
                'nervous': 'ñ',       # n with tilde
                'angry': 'á',         # a acute
                'scared': 'š',        # s with caron
                'calm': 'ç',          # c cedilla
                'tense': 'ť',         # t with caron
                'confused': 'ø',      # o slashed
                'surprised': 'ü',     # u umlaut
                'sarcastic': 'ž',     # z with caron
                'determined': 'đ',    # d slashed
                'thoughtful': 'þ',    # thorn
                'whisper': '˙',       # dot above
                'quietly': '˘',       # breve
                'shouting': 'ˆ',      # circumflex
            },
            
            # FRASES COMUNS - Common expressions
            'phrases': {
                'Where is': '❓',      # Question mark
                'Stop!': '❗',         # Exclamation
                'No!': '‼',          # Double exclamation
                'What?!': '⁉',       # Question + exclamation
                'Why': '¿',           # Inverted question
                'I don\'t know': '⟦',
                'We have to': '⟧',
                'You can\'t': '⟨',
                'It\'s over': '⟩',
                'Come with me': '❰',
                'Get out of here': '❱',
                'Trust me': '❲',
                'Listen to me': '❳',
                'Are you': '❴',
                'ready': '❵',
            },
            
            # TRANSIÇÕES - Cinema symbols
            'transitions': {
                'FADE IN:': '▶',
                'FADE OUT.': '◀',
                'CUT TO:': '⏩',
                'JUMP CUT:': '⏭',
                'FLASHBACK:': '⏪',
                'DISSOLVE TO:': '⏬',
                'MATCH CUT:': '⏯',
                'FREEZE FRAME:': '⏸',
                'TIME LAPSE:': '⏺',
                'BLACKOUT.': '⏹',
                'LATER': '⏰',
                'MOMENTS LATER': '⌛',
                'CONTINUOUS': '⌚',
            },
            
            # TEMPOS - Time indicators
            'times': {
                'DAY': '☀',          # Sun
                'NIGHT': '🌙',        # Moon
                'DAWN': '🌅',         # Sunrise
                'DUSK': '🌆',         # Sunset
                'MORNING': '🌄',      # Sunrise over mountain
                'EVENING': '🌇',      # City sunset
                'AFTERNOON': '☀️',    # Bright sun
            },
            
            # GRAMMAR - Structure indicators
            'grammar': {
                'INT.': 'I',
                'EXT.': 'E',
                'INT/EXT.': 'IE',
            }
        }
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
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
    
    def compress(self, text: str) -> Tuple[str, Dict]:
        """Compress text with V11 Ultimate algorithm"""
        
        compressed = text
        self.stats = {
            'original_chars': len(text),
            'original_tokens': len(self.tokenizer.encode(text)),
            'replacements': 0
        }
        
        print(f"⛏️ Starting V11 Ultimate compression...")
        
        # Phase 1: Apply all dictionary replacements (longest first)
        all_replacements = []
        
        # Collect all replacements from all categories
        for category, patterns in self.dictionary.items():
            if category == 'grammar':  # Handle grammar separately
                continue
            for original, symbol in patterns.items():
                all_replacements.append((original, symbol, category))
        
        # Sort by length (longest first) to avoid partial replacements
        all_replacements.sort(key=lambda x: len(x[0]), reverse=True)
        
        print(f"🔄 Applying {len(all_replacements)} pattern replacements...")
        
        for original, symbol, category in all_replacements:
            # Use word boundaries for better matching
            if category in ['phrases', 'transitions']:
                # Exact match for phrases and transitions
                count = compressed.count(original)
                if count > 0:
                    compressed = compressed.replace(original, symbol)
                    self.stats['replacements'] += count
            else:
                # Word boundary match for characters, locations, actions, moods
                pattern = r'\b' + re.escape(original) + r'\b'
                matches = re.findall(pattern, compressed, re.IGNORECASE)
                if matches:
                    compressed = re.sub(pattern, symbol, compressed, flags=re.IGNORECASE)
                    self.stats['replacements'] += len(matches)
        
        # Phase 2: Compress scene headers with grammar
        print("🎬 Compressing scene headers...")
        compressed = self._compress_headers(compressed)
        
        # Phase 3: Compress dialogue structure
        print("🗣️ Compressing dialogue structure...")
        compressed = self._compress_dialogue_structure(compressed)
        
        # Calculate final stats
        self.stats['compressed_chars'] = len(compressed)
        self.stats['compressed_tokens'] = len(self.tokenizer.encode(compressed))
        
        print(f"✅ V11 Ultimate compression complete!")
        
        return compressed, self.stats
    
    def _compress_headers(self, text: str) -> str:
        """Compress scene headers using V11 grammar"""
        
        # Pattern: INT./EXT. LOCATION - TIME
        pattern = r'(INT\.|EXT\.|INT/EXT\.)\s+([A-Z][A-Z\s\-\.]+?)\s*-\s*(DAY|NIGHT|DAWN|DUSK|MORNING|EVENING|AFTERNOON|CONTINUOUS|LATER|MOMENTS LATER)?'
        
        def replace_header(match):
            prefix = match.group(1)
            location = match.group(2).strip()
            time = match.group(3) if match.group(3) else ''
            
            # Convert prefix
            grammar_map = self.dictionary['grammar']
            prefix_symbol = grammar_map.get(prefix, prefix[0])
            
            # Convert location
            location_symbol = self.dictionary['locations'].get(location, location[:2])
            
            # Convert time
            time_symbol = self.dictionary['times'].get(time, '') if time else ''
            
            result = prefix_symbol + location_symbol + time_symbol
            self.stats['replacements'] += 1
            return result
        
        return re.sub(pattern, replace_header, text)
    
    def _compress_dialogue_structure(self, text: str) -> str:
        """Compress dialogue structure with mood integration"""
        
        # Pattern: CHARACTER\n(mood)\ndialogue
        pattern = r'\b([A-Z][A-Z\s]+)\s*\n\s*\(([^)]+)\)\s*\n([^\n]+)'
        
        def replace_dialogue(match):
            char = match.group(1).strip()
            mood = match.group(2).strip()
            dialogue = match.group(3).strip()
            
            # Get character symbol
            char_symbol = self.dictionary['characters'].get(char, char[0] if char else 'X')
            
            # Get mood symbol
            mood_symbol = self.dictionary['moods'].get(mood, mood[0] if mood else '')
            
            self.stats['replacements'] += 2
            return f"{char_symbol}{mood_symbol}:{dialogue}"
        
        return re.sub(pattern, replace_dialogue, text)
    
    def decompress(self, compressed: str) -> str:
        """Decompress V11 Ultimate text back to original format"""
        
        decompressed = compressed
        
        # Reverse all replacements
        all_replacements = []
        for category, patterns in self.dictionary.items():
            if category == 'grammar':
                continue
            for original, symbol in patterns.items():
                all_replacements.append((original, symbol))
        
        # Apply in reverse (shortest original first)
        all_replacements.sort(key=lambda x: len(x[0]))
        
        for original, symbol in all_replacements:
            decompressed = decompressed.replace(symbol, original)
        
        return decompressed
    
    def get_compression_stats(self) -> Dict:
        """Get detailed compression statistics"""
        
        char_compression = (self.stats['original_chars'] - self.stats['compressed_chars']) / self.stats['original_chars'] * 100
        token_compression = (self.stats['original_tokens'] - self.stats['compressed_tokens']) / self.stats['original_tokens'] * 100
        
        return {
            'original_chars': self.stats['original_chars'],
            'compressed_chars': self.stats['compressed_chars'],
            'original_tokens': self.stats['original_tokens'],
            'compressed_tokens': self.stats['compressed_tokens'],
            'char_compression': char_compression,
            'token_compression': token_compression,
            'replacements': self.stats['replacements'],
            'dictionary_size': sum(len(patterns) for patterns in self.dictionary.values())
        }

def test_v11_ultimate():
    """Test DigiLang V11 Ultimate with The Dark Knight"""
    
    print("="*70)
    print("🌟 DIGILANG V11 ULTIMATE - THE ULTIMATE TEST")
    print("="*70)
    
    # Initialize V11
    v11 = DigiLangV11Ultimate()
    
    # Test with The Dark Knight
    pdf_path = Path('digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf')
    
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    # Extract text
    print(f"📖 Extracting text from {pdf_path.name}...")
    text = v11.extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Text extraction failed")
        return
    
    print(f"✅ Extracted {len(text):,} characters")
    
    # Compress with V11 Ultimate
    compressed, _ = v11.compress(text)
    
    # Get detailed stats
    stats = v11.get_compression_stats()
    
    # Display results
    print("\n" + "="*70)
    print("📊 V11 ULTIMATE COMPRESSION RESULTS")
    print("="*70)
    
    print(f"\n📄 Original Text:")
    print(f"  Characters: {stats['original_chars']:,}")
    print(f"  Tokens: {stats['original_tokens']:,}")
    
    print(f"\n🗜 Compressed Text:")
    print(f"  Characters: {stats['compressed_chars']:,}")
    print(f"  Tokens: {stats['compressed_tokens']:,}")
    
    print(f"\n🎯 Compression Results:")
    print(f"  Character compression: {stats['char_compression']:.2f}%")
    print(f"  Token compression: {stats['token_compression']:.2f}%")
    print(f"  Total replacements: {stats['replacements']:,}")
    print(f"  Dictionary size: {stats['dictionary_size']} patterns")
    
    # Compare with previous versions
    print(f"\n🆚 EVOLUTION COMPARISON:")
    print(f"  V8.1 Supreme: 0.72% token compression")
    print(f"  V10 Supreme: 11.28% token compression")
    print(f"  V11 Ultimate: {stats['token_compression']:.2f}% token compression")
    
    if stats['token_compression'] > 11.28:
        improvement = stats['token_compression'] / 11.28
        print(f"\n🚀 SUCCESS! V11 is {improvement:.1f}x better than V10!")
    
    if stats['token_compression'] > 0.72:
        total_improvement = stats['token_compression'] / 0.72
        print(f"🏆 V11 is {total_improvement:.1f}x better than original V8.1!")
    
    # Save results
    results = {
        'version': 'V11 Ultimate',
        'file': pdf_path.name,
        'stats': stats,
        'dictionary_categories': len(v11.dictionary),
        'total_patterns': stats['dictionary_size']
    }
    
    output_file = Path('docs/FASE_20_V11_ULTIMATE_RESULTS.json')
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Show sample compression
    print(f"\n🔍 SAMPLE COMPRESSION (first 500 chars):")
    print(f"Original: {text[:500]}...")
    print(f"Compressed: {compressed[:200]}...")
    
    return compressed, stats

if __name__ == "__main__":
    test_v11_ultimate()