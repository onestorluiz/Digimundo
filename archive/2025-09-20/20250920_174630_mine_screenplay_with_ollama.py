#!/usr/bin/env python3
"""
FASE 18 - MINERAÇÃO INTELIGENTE COM OLLAMA
Mineração específica de padrões de um roteiro usando Ollama
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pdfplumber
import ollama
from collections import Counter
import time

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class IntelligentScreenplayMiner:
    """Minerador inteligente de padrões de roteiro usando Ollama"""
    
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.patterns = {
            'characters': set(),
            'locations': set(),
            'transitions': set(),
            'actions': set(),
            'dialogues': set(),
            'frequent_phrases': Counter()
        }
        
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        print(f"📖 Extracting text from {pdf_path.name}...")
        text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages[:50]):  # First 50 pages for testing
                    if i % 10 == 0:
                        print(f"  Processing page {i}...")
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"❌ Error extracting PDF: {e}")
            return None
            
        print(f"✅ Extracted {len(text):,} characters")
        return text
    
    def mine_with_ollama(self, text_chunk: str, task: str) -> List[str]:
        """Use Ollama to intelligently mine patterns"""
        
        prompts = {
            'characters': """
                Extract ALL character names from this screenplay excerpt.
                Return ONLY the names, one per line, in UPPERCASE.
                Include main characters, supporting characters, and even minor characters.
                Do not include descriptions or explanations.
                Example output:
                BATMAN
                JOKER
                GORDON
                """,
            'locations': """
                Extract ALL location sluglines from this screenplay.
                Return ONLY the locations in screenplay format (INT./EXT. LOCATION - TIME).
                One per line. No explanations.
                Example output:
                INT. WAREHOUSE - NIGHT
                EXT. GOTHAM STREETS - DAY
                """,
            'transitions': """
                Extract ALL transition terms from this screenplay.
                Return ONLY the transitions, one per line.
                Include CUT TO:, FADE IN:, DISSOLVE TO:, etc.
                No explanations.
                """,
            'actions': """
                Extract the 20 most frequently repeated action verbs or phrases.
                Return ONLY the verbs/phrases, one per line.
                Focus on screenplay-specific actions.
                """
        }
        
        prompt = prompts.get(task, "")
        if not prompt:
            return []
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a screenplay analysis expert. Extract patterns precisely as requested.'
                    },
                    {
                        'role': 'user',
                        'content': f"{prompt}\n\nScreenplay excerpt:\n{text_chunk[:3000]}"
                    }
                ]
            )
            
            # Parse response
            result = response['message']['content']
            items = [line.strip() for line in result.split('\n') if line.strip()]
            return items
            
        except Exception as e:
            print(f"⚠️ Ollama error for {task}: {e}")
            return []
    
    def mine_with_regex(self, text: str):
        """Fallback regex-based mining"""
        
        # Character names (all caps on their own line)
        char_pattern = r'^\s{10,}([A-Z][A-Z\s]+)$'
        characters = re.findall(char_pattern, text, re.MULTILINE)
        self.patterns['characters'].update([c.strip() for c in characters])
        
        # Locations (INT./EXT. patterns)
        loc_pattern = r'((?:INT\.|EXT\.)\s+[A-Z][A-Z\s\-\.]+(?:DAY|NIGHT|CONTINUOUS|LATER)?)'  
        locations = re.findall(loc_pattern, text)
        self.patterns['locations'].update(locations)
        
        # Transitions
        trans_pattern = r'((?:FADE|CUT|DISSOLVE|MATCH CUT|SMASH CUT|TIME CUT)\s+(?:IN|OUT|TO):?)'
        transitions = re.findall(trans_pattern, text, re.IGNORECASE)
        self.patterns['transitions'].update([t.upper() for t in transitions])
        
    def analyze_frequency(self, text: str):
        """Analyze word frequency for additional patterns"""
        
        # Clean text
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        
        # Count frequencies
        word_freq = Counter(words)
        
        # Filter common words
        common_words = {'the', 'and', 'but', 'for', 'with', 'from', 'into', 'that', 'this', 'they', 'them', 'his', 'her'}
        
        # Get top frequent words (potential patterns)
        for word, count in word_freq.most_common(100):
            if word not in common_words and count > 10:
                self.patterns['frequent_phrases'][word] = count
    
    def mine_screenplay(self, pdf_path: Path) -> Dict:
        """Mine complete screenplay for patterns"""
        
        print("="*60)
        print(f"MINING: {pdf_path.name}")
        print("="*60)
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return None
            
        # 1. Regex-based mining (fast)
        print("\n🔍 Phase 1: Regex-based mining...")
        self.mine_with_regex(text)
        print(f"  Found {len(self.patterns['characters'])} characters")
        print(f"  Found {len(self.patterns['locations'])} locations")
        print(f"  Found {len(self.patterns['transitions'])} transitions")
        
        # 2. Ollama-based mining (intelligent)
        print("\n🤖 Phase 2: Ollama-based intelligent mining...")
        
        # Check if Ollama is available
        try:
            models = ollama.list()
            print(f"  Available models: {[m['name'] for m in models['models']]}")
            
            # Mine characters
            print("  Mining characters with Ollama...")
            chunks = [text[i:i+5000] for i in range(0, min(len(text), 20000), 5000)]
            
            for i, chunk in enumerate(chunks):
                print(f"    Processing chunk {i+1}/{len(chunks)}...")
                chars = self.mine_with_ollama(chunk, 'characters')
                self.patterns['characters'].update(chars)
                time.sleep(1)  # Rate limiting
            
            # Mine locations
            print("  Mining locations with Ollama...")
            locs = self.mine_with_ollama(text[:10000], 'locations')
            self.patterns['locations'].update(locs)
            
        except Exception as e:
            print(f"⚠️ Ollama not available: {e}")
            print("  Falling back to regex-only mining")
        
        # 3. Frequency analysis
        print("\n📊 Phase 3: Frequency analysis...")
        self.analyze_frequency(text)
        print(f"  Found {len(self.patterns['frequent_phrases'])} frequent terms")
        
        # Generate report
        return self.generate_mining_report(pdf_path.name, text)
    
    def generate_mining_report(self, filename: str, original_text: str) -> Dict:
        """Generate detailed mining report"""
        
        report = {
            'file': filename,
            'original_chars': len(original_text),
            'patterns_found': {
                'characters': sorted(list(self.patterns['characters']))[:50],  # Top 50
                'locations': sorted(list(self.patterns['locations']))[:50],
                'transitions': sorted(list(self.patterns['transitions'])),
                'frequent_terms': dict(self.patterns['frequent_phrases'].most_common(50))
            },
            'statistics': {
                'total_characters': len(self.patterns['characters']),
                'total_locations': len(self.patterns['locations']),
                'total_transitions': len(self.patterns['transitions']),
                'total_frequent_terms': len(self.patterns['frequent_phrases'])
            }
        }
        
        # Create custom dictionary for compression
        custom_dict = self.create_custom_dictionary()
        report['custom_dictionary'] = custom_dict
        
        # Test compression with custom dictionary
        compressed = self.test_compression(original_text, custom_dict)
        report['compression_test'] = compressed
        
        return report
    
    def create_custom_dictionary(self) -> Dict[str, str]:
        """Create custom compression dictionary from mined patterns"""
        
        # Unicode characters for compression (verified single tokens)
        unicode_chars = [
            # Greek letters
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ',
            'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ',
            'φ', 'χ', 'ψ', 'ω', 'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ',
            # Math symbols
            '∀', '∂', '∃', '∅', '∇', '∈', '∉', '∋', '∏', '∑',
            '√', '∝', '∞', '∠', '∧', '∨', '∩', '∪', '∫', '∴',
            # Box drawing
            '⊕', '⊖', '⊗', '⊘', '⊙', '⊚', '⊛', '⊜', '⊝', '⊞',
            # Currency
            '€', '£', '¥', '¢', '¤', '§', '©', '®', '°', '±',
            # Additional symbols
            '†', '‡', '•', '‰', '′', '″', '‴', '※', '‼', '⁇',
            '⁈', '⁉', '⁎', '⁑', '⁒', '⁓', '⁔', '⁕', '⁖', '⁗'
        ]
        
        dictionary = {}
        char_index = 0
        
        # Add top characters (most important)
        for char in sorted(self.patterns['characters'], 
                          key=lambda x: original_text.count(x) if hasattr(self, 'original_text') else 0,
                          reverse=True)[:30]:
            if char_index < len(unicode_chars):
                dictionary[char] = unicode_chars[char_index]
                char_index += 1
        
        # Add top locations
        for loc in sorted(self.patterns['locations'],
                         key=lambda x: original_text.count(x) if hasattr(self, 'original_text') else 0,
                         reverse=True)[:20]:
            if char_index < len(unicode_chars):
                dictionary[loc] = unicode_chars[char_index]
                char_index += 1
        
        # Add transitions
        for trans in self.patterns['transitions']:
            if char_index < len(unicode_chars):
                dictionary[trans] = unicode_chars[char_index]
                char_index += 1
        
        # Add frequent terms
        for term, count in self.patterns['frequent_phrases'].most_common(20):
            if char_index < len(unicode_chars) and count > 20:
                dictionary[term] = unicode_chars[char_index]
                char_index += 1
        
        return dictionary
    
    def test_compression(self, text: str, dictionary: Dict[str, str]) -> Dict:
        """Test compression with custom dictionary"""
        
        compressed = text
        replacements = 0
        
        # Apply dictionary (longest patterns first)
        for pattern, replacement in sorted(dictionary.items(), key=lambda x: len(x[0]), reverse=True):
            count = compressed.count(pattern)
            if count > 0:
                compressed = compressed.replace(pattern, replacement)
                replacements += count
        
        original_chars = len(text)
        compressed_chars = len(compressed)
        compression_ratio = (original_chars - compressed_chars) / original_chars if original_chars > 0 else 0
        
        # Estimate token compression
        original_tokens = original_chars // 4
        compressed_tokens = compressed_chars // 4
        token_compression = (original_tokens - compressed_tokens) / original_tokens if original_tokens > 0 else 0
        
        return {
            'original_chars': original_chars,
            'compressed_chars': compressed_chars,
            'char_compression': compression_ratio,
            'token_compression': token_compression,
            'replacements': replacements,
            'dictionary_size': len(dictionary)
        }

def main():
    """Main execution"""
    
    print("="*60)
    print("FASE 18 - MINERAÇÃO INTELIGENTE COM OLLAMA")
    print("="*60)
    
    # Target screenplay
    pdf_path = Path('digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf')
    
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    # Initialize miner
    miner = IntelligentScreenplayMiner()
    
    # Mine screenplay
    report = miner.mine_screenplay(pdf_path)
    
    if report:
        # Save report
        output_file = Path('docs/FASE_18_MINING_REPORT.json')
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("MINING SUMMARY")
        print("="*60)
        
        stats = report['statistics']
        print(f"\n📊 Patterns Found:")
        print(f"  Characters: {stats['total_characters']}")
        print(f"  Locations: {stats['total_locations']}")
        print(f"  Transitions: {stats['total_transitions']}")
        print(f"  Frequent Terms: {stats['total_frequent_terms']}")
        
        print(f"\n🔤 Top 10 Characters:")
        for char in report['patterns_found']['characters'][:10]:
            print(f"  - {char}")
        
        print(f"\n📍 Top 10 Locations:")
        for loc in report['patterns_found']['locations'][:10]:
            print(f"  - {loc}")
        
        comp = report['compression_test']
        print(f"\n💾 Compression Test:")
        print(f"  Original: {comp['original_chars']:,} chars")
        print(f"  Compressed: {comp['compressed_chars']:,} chars")
        print(f"  Character Compression: {comp['char_compression']:.2%}")
        print(f"  Token Compression: {comp['token_compression']:.2%}")
        print(f"  Dictionary Size: {comp['dictionary_size']} patterns")
        
        print(f"\n✅ Report saved to: {output_file}")
        
        # Compare with V8.1 results
        print("\n" + "="*60)
        print("COMPARISON WITH V8.1 SUPREME")
        print("="*60)
        
        v8_file = Path('docs/FASE_17e_TRADUCAO_FINAL_RESULTS.json')
        if v8_file.exists():
            with open(v8_file, 'r') as f:
                v8_data = json.load(f)
            
            # Find Dark Knight in V8 results
            for result in v8_data.get('results', []):
                if 'Dark Knight - Release' in result.get('file', ''):
                    v8_comp = result.get('token_compression', 0)
                    our_comp = comp['token_compression']
                    
                    print(f"\n📊 Token Compression Comparison:")
                    print(f"  V8.1 Supreme (generic patterns): {v8_comp:.2%}")
                    print(f"  Custom Mining (specific patterns): {our_comp:.2%}")
                    print(f"  Improvement: {(our_comp - v8_comp):.2%}")
                    
                    if our_comp > v8_comp:
                        print(f"\n🎯 SUCCESS! Custom mining achieved {(our_comp/v8_comp - 1)*100:.1f}% better compression!")
                    break
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Integrate custom dictionaries into DigiLang V10")
        print("2. Create per-document compression profiles")
        print("3. Use deepseek:70b for more advanced pattern extraction")
        print("4. Implement continuous learning from each processed document")

if __name__ == "__main__":
    main()