#!/usr/bin/env python
"""
Advanced entity mapping system for narrative compression.
Maps characters, locations, and objects to compact representations.
"""

import re
import spacy
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from collections import Counter
import tiktoken

# Try to load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    print("Installing spaCy model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

@dataclass
class Entity:
    """Represents a narrative entity."""
    text: str
    type: str  # PERSON, LOC, ORG, OBJECT
    count: int = 1
    aliases: Set[str] = field(default_factory=set)
    code: Optional[str] = None
    
@dataclass
class EntityMap:
    """Manages entity mappings for compression."""
    persons: Dict[str, Entity] = field(default_factory=dict)
    locations: Dict[str, Entity] = field(default_factory=dict)
    objects: Dict[str, Entity] = field(default_factory=dict)
    organizations: Dict[str, Entity] = field(default_factory=dict)
    
    # Reverse mappings for decompression
    code_to_entity: Dict[str, Entity] = field(default_factory=dict)
    
    # Statistics
    total_replacements: int = 0
    tokens_saved: int = 0

class NarrativeEntityMapper:
    """
    Advanced entity recognition and mapping for narrative compression.
    Identifies recurring entities and maps them to short codes.
    """
    
    def __init__(self, min_occurrences: int = 3, max_code_length: int = 3):
        self.min_occurrences = min_occurrences
        self.max_code_length = max_code_length
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.entity_map = EntityMap()
        
        # Code generation counters
        self.counters = {
            'PERSON': 0,
            'LOC': 0,
            'ORG': 0,
            'OBJECT': 0
        }
        
        # Common screenplay/narrative patterns
        self.character_patterns = [
            r'\b([A-Z][A-Z\s]+)\s*\n',  # ALL CAPS character names
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*:',  # Name before dialogue
            r'^\s*([A-Z][A-Z\s]+)\s*$',  # Character slug lines
        ]
        
        self.location_patterns = [
            r'(?:INT\.|EXT\.)\s+([A-Z][A-Z\s\-]+)',  # Scene headers
            r'(?:at|in|on|near)\s+the\s+([A-Z][a-z]+(?:\s+[A-Z]?[a-z]+)*)',
        ]
        
    def analyze_text(self, text: str) -> EntityMap:
        """
        Analyze text and build entity map.
        Returns EntityMap with all identified entities.
        """
        # Reset map for new text
        self.entity_map = EntityMap()
        
        # Method 1: Use spaCy NER
        self._extract_with_spacy(text)
        
        # Method 2: Pattern matching for screenplay format
        self._extract_with_patterns(text)
        
        # Method 3: Frequency analysis for repeated proper nouns
        self._extract_frequent_terms(text)
        
        # Generate codes for frequent entities
        self._generate_codes()
        
        return self.entity_map
    
    def _extract_with_spacy(self, text: str):
        """Extract entities using spaCy NER."""
        doc = nlp(text[:1000000])  # Limit to 1M chars for performance
        
        entity_counts = Counter()
        entity_types = {}
        
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'LOC', 'GPE', 'ORG']:
                entity_counts[ent.text] += 1
                entity_types[ent.text] = ent.label_
        
        # Add to entity map if frequent enough
        for entity_text, count in entity_counts.items():
            if count >= self.min_occurrences:
                entity_type = entity_types[entity_text]
                entity = Entity(
                    text=entity_text,
                    type=entity_type if entity_type != 'GPE' else 'LOC',
                    count=count
                )
                
                if entity_type == 'PERSON':
                    self.entity_map.persons[entity_text] = entity
                elif entity_type in ['LOC', 'GPE']:
                    self.entity_map.locations[entity_text] = entity
                elif entity_type == 'ORG':
                    self.entity_map.organizations[entity_text] = entity
    
    def _extract_with_patterns(self, text: str):
        """Extract entities using regex patterns."""
        # Extract characters
        for pattern in self.character_patterns:
            for match in re.finditer(pattern, text, re.MULTILINE):
                name = match.group(1).strip()
                if name and len(name) > 2:
                    if name in self.entity_map.persons:
                        self.entity_map.persons[name].count += 1
                    else:
                        self.entity_map.persons[name] = Entity(
                            text=name,
                            type='PERSON',
                            count=1
                        )
        
        # Extract locations
        for pattern in self.location_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                location = match.group(1).strip()
                if location and len(location) > 3:
                    if location in self.entity_map.locations:
                        self.entity_map.locations[location].count += 1
                    else:
                        self.entity_map.locations[location] = Entity(
                            text=location,
                            type='LOC',
                            count=1
                        )
    
    def _extract_frequent_terms(self, text: str):
        """Extract frequently occurring capitalized terms."""
        # Find all capitalized words/phrases
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Count occurrences
        term_counts = Counter(capitalized)
        
        # Add frequent terms as potential entities
        for term, count in term_counts.items():
            if count >= self.min_occurrences * 2:  # Higher threshold
                # Check if already identified
                if (term not in self.entity_map.persons and 
                    term not in self.entity_map.locations and
                    term not in self.entity_map.organizations):
                    
                    # Guess type based on context
                    if any(title in term.lower() for title in ['mr', 'mrs', 'ms', 'dr']):
                        self.entity_map.persons[term] = Entity(term, 'PERSON', count)
                    elif any(word in term.lower() for word in ['street', 'avenue', 'road', 'city']):
                        self.entity_map.locations[term] = Entity(term, 'LOC', count)
                    else:
                        self.entity_map.objects[term] = Entity(term, 'OBJECT', count)
    
    def _generate_codes(self):
        """Generate short codes for entities."""
        # Sort entities by frequency (most frequent get shortest codes)
        all_entities = []
        
        for entity_dict in [self.entity_map.persons, self.entity_map.locations,
                          self.entity_map.organizations, self.entity_map.objects]:
            all_entities.extend(entity_dict.values())
        
        all_entities.sort(key=lambda e: e.count, reverse=True)
        
        # Generate codes
        for entity in all_entities:
            if entity.count >= self.min_occurrences:
                # Generate type-specific code
                prefix = {
                    'PERSON': 'P',
                    'LOC': 'L',
                    'ORG': 'O',
                    'OBJECT': 'X'
                }.get(entity.type, 'E')
                
                self.counters[entity.type] = self.counters.get(entity.type, 0) + 1
                
                # Use base-36 for compact representation
                if self.counters[entity.type] < 10:
                    code = f"{prefix}{self.counters[entity.type]}"
                elif self.counters[entity.type] < 36:
                    code = f"{prefix}{chr(55 + self.counters[entity.type])}"  # A-Z
                else:
                    code = f"{prefix}{self.counters[entity.type]:02d}"
                
                entity.code = code
                self.entity_map.code_to_entity[code] = entity
    
    def compress_with_entities(self, text: str, entity_map: Optional[EntityMap] = None) -> Tuple[str, Dict]:
        """
        Compress text by replacing entities with codes.
        Returns compressed text and statistics.
        """
        if entity_map is None:
            entity_map = self.analyze_text(text)
        
        compressed = text
        stats = {
            'original_tokens': len(self.encoder.encode(text)),
            'entities_replaced': 0,
            'tokens_saved': 0
        }
        
        # Replace entities with codes (longest first to avoid partial matches)
        replacements = []
        for entity_dict in [entity_map.persons, entity_map.locations,
                          entity_map.organizations, entity_map.objects]:
            for entity in entity_dict.values():
                if entity.code:
                    replacements.append((entity.text, entity.code, entity.count))
        
        # Sort by length (longest first) and frequency
        replacements.sort(key=lambda x: (len(x[0]), x[2]), reverse=True)
        
        for entity_text, code, count in replacements:
            if entity_text in compressed:
                # Calculate token savings
                original_tokens = len(self.encoder.encode(entity_text))
                code_tokens = len(self.encoder.encode(code))
                
                if code_tokens < original_tokens:
                    # Use word boundaries for safety
                    pattern = r'\b' + re.escape(entity_text) + r'\b'
                    compressed, n_replacements = re.subn(pattern, code, compressed)
                    
                    if n_replacements > 0:
                        stats['entities_replaced'] += n_replacements
                        stats['tokens_saved'] += n_replacements * (original_tokens - code_tokens)
        
        stats['final_tokens'] = len(self.encoder.encode(compressed))
        stats['compression_ratio'] = 1 - (stats['final_tokens'] / stats['original_tokens'])
        stats['entity_count'] = len(entity_map.code_to_entity)
        
        return compressed, stats
    
    def decompress_entities(self, compressed_text: str, entity_map: EntityMap) -> str:
        """
        Decompress text by replacing codes with original entities.
        """
        decompressed = compressed_text
        
        # Replace codes with entities (shortest codes first to avoid conflicts)
        for code, entity in sorted(entity_map.code_to_entity.items(), key=lambda x: len(x[0])):
            decompressed = decompressed.replace(code, entity.text)
        
        return decompressed
    
    def get_entity_glossary(self, entity_map: EntityMap) -> str:
        """
        Generate a human-readable glossary of entity mappings.
        """
        glossary = []
        glossary.append("ENTITY COMPRESSION GLOSSARY")
        glossary.append("=" * 40)
        
        sections = [
            ("Characters", entity_map.persons),
            ("Locations", entity_map.locations),
            ("Organizations", entity_map.organizations),
            ("Objects", entity_map.objects)
        ]
        
        for section_name, entities in sections:
            if entities:
                glossary.append(f"\n{section_name}:")
                for entity in sorted(entities.values(), key=lambda e: e.count, reverse=True):
                    if entity.code:
                        glossary.append(f"  {entity.code} = {entity.text} ({entity.count}x)")
        
        return "\n".join(glossary)


class SmartEntityCompressor:
    """
    Combines entity mapping with LLMLingua for optimal compression.
    """
    
    def __init__(self):
        self.entity_mapper = NarrativeEntityMapper()
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def compress(self, text: str) -> Tuple[str, EntityMap, Dict]:
        """
        Two-stage compression: entities first, then LLMLingua.
        """
        # Stage 1: Entity compression
        entity_map = self.entity_mapper.analyze_text(text)
        compressed, entity_stats = self.entity_mapper.compress_with_entities(text, entity_map)
        
        # Import LLMLingua for stage 2
        from src.compressors.llmlingua import LLMLinguaCompressor, CompressionConfig
        
        # Stage 2: LLMLingua on entity-compressed text
        llm_compressor = LLMLinguaCompressor(
            CompressionConfig(target_ratio=0.3, preserve_entities=False)
        )
        final_compressed, llm_ratio, llm_stats = llm_compressor.compress(compressed)
        
        # Combined statistics
        combined_stats = {
            'original_tokens': entity_stats['original_tokens'],
            'after_entities': entity_stats['final_tokens'],
            'final_tokens': llm_stats['final_tokens'],
            'entity_compression': entity_stats['compression_ratio'],
            'llm_compression': llm_ratio,
            'total_compression': 1 - (llm_stats['final_tokens'] / entity_stats['original_tokens']),
            'entities_mapped': entity_stats['entity_count'],
            'tokens_saved_by_entities': entity_stats['tokens_saved']
        }
        
        return final_compressed, entity_map, combined_stats


if __name__ == "__main__":
    # Test entity mapper
    test_text = """
    INT. CAPULET'S HOUSE - NIGHT
    
    ROMEO enters the grand ballroom of the Capulet mansion. 
    He sees JULIET across the room. Lord Capulet welcomes guests.
    
    ROMEO
    Did my heart love till now? Forswear it, sight!
    
    JULIET
    My only love sprung from my only hate!
    
    They meet again at the Capulet mansion the next day.
    Romeo returns to the Capulet house. Juliet waits.
    """
    
    mapper = NarrativeEntityMapper()
    entity_map = mapper.analyze_text(test_text)
    
    print("Entities found:")
    print(mapper.get_entity_glossary(entity_map))
    
    compressed, stats = mapper.compress_with_entities(test_text, entity_map)
    print(f"\nCompression stats: {stats}")
    print(f"Compressed text:\n{compressed}")
    
    # Test smart compressor
    smart = SmartEntityCompressor()
    final, entities, combined = smart.compress(test_text)
    print(f"\nSmart compression: {combined['total_compression']:.1%}")