"""
Token Trie for efficient longest-match search in token sequences.
"""
from typing import Dict, List, Tuple, Optional

class TrieNode:
    """Node in the token trie."""

    def __init__(self):
        self.children: Dict[int, 'TrieNode'] = {}
        self.glyph: Optional[str] = None
        self.length: int = 0

class TokenTrie:
    """
    Trie structure for token sequences with longest-match search.
    """

    def __init__(self, patterns: Dict[Tuple[int, ...], str]):
        """
        Initialize trie with patterns.
        patterns: Dict mapping token tuples to glyph strings
        """
        self.root = TrieNode()
        for token_seq, glyph in patterns.items():
            self._insert(token_seq, glyph)

    def _insert(self, token_seq: Tuple[int, ...], glyph: str):
        """Insert a token sequence into the trie."""
        node = self.root
        for token in token_seq:
            if token not in node.children:
                node.children[token] = TrieNode()
            node = node.children[token]
        node.glyph = glyph
        node.length = len(token_seq)

    def longest_match(self, ids: List[int], pos: int) -> Optional[Tuple[int, str]]:
        """
        Find the longest pattern matching at position pos.
        Returns (length, glyph) or None if no match.
        """
        node = self.root
        last_match = None
        length = 0
        for i in range(pos, len(ids)):
            token = ids[i]
            if token not in node.children:
                break
            node = node.children[token]
            length += 1
            if node.glyph is not None:
                last_match = (length, node.glyph)
        return last_match

    def all_matches(self, ids: List[int], pos: int) -> List[Tuple[int, str]]:
        """
        Find all patterns matching at position pos.
        Returns list of (length, glyph) tuples.
        """
        matches = []
        node = self.root
        length = 0
        for i in range(pos, len(ids)):
            token = ids[i]
            if token not in node.children:
                break
            node = node.children[token]
            length += 1
            if node.glyph is not None:
                matches.append((length, node.glyph))
        return matches

    def encode_sequence(self, ids: List[int]) -> List[int]:
        """
        Encode a sequence of token IDs using longest-match substitution.
        Returns new sequence with glyphs replacing matched patterns.
        """
        import tiktoken
        enc = tiktoken.get_encoding('cl100k_base')
        out_ids = []
        i = 0
        while i < len(ids):
            match = self.longest_match(ids, i)
            if match:
                length, glyph = match
                glyph_id = enc.encode(glyph)[0]
                out_ids.append(glyph_id)
                i += length
            else:
                out_ids.append(ids[i])
                i += 1
        return out_ids

    def stats(self) -> Dict:
        """Get statistics about the trie."""

        def count_nodes(node):
            count = 1
            for child in node.children.values():
                count += count_nodes(child)
            return count

        def count_patterns(node):
            count = 1 if node.glyph else 0
            for child in node.children.values():
                count += count_patterns(child)
            return count

        def max_depth(node, depth=0):
            if not node.children:
                return depth
            return max((max_depth(child, depth + 1) for child in node.children.values()))
        return {'nodes': count_nodes(self.root), 'patterns': count_patterns(self.root), 'max_depth': max_depth(self.root)}

class FastTokenTrie:
    """
    Optimized token trie using dictionary for O(1) lookups.
    Better for smaller pattern sets.
    """

    def __init__(self, patterns: Dict[Tuple[int, ...], str]):
        """Initialize with patterns sorted by length (longest first)."""
        self.patterns = sorted(patterns.items(), key=lambda x: len(x[0]), reverse=True)
        self.first_token_map: Dict[int, List[Tuple[Tuple[int, ...], str]]] = {}
        for token_seq, glyph in self.patterns:
            if token_seq:
                first = token_seq[0]
                if first not in self.first_token_map:
                    self.first_token_map[first] = []
                self.first_token_map[first].append((token_seq, glyph))

    def longest_match(self, ids: List[int], pos: int) -> Optional[Tuple[int, str]]:
        """Find longest pattern matching at position."""
        if pos >= len(ids):
            return None
        first_token = ids[pos]
        if first_token not in self.first_token_map:
            return None
        for token_seq, glyph in self.first_token_map[first_token]:
            seq_len = len(token_seq)
            if pos + seq_len > len(ids):
                continue
            if tuple(ids[pos:pos + seq_len]) == token_seq:
                return (seq_len, glyph)
        return None

    def encode_sequence(self, ids: List[int]) -> List[int]:
        """Encode sequence using longest-match substitution."""
        import tiktoken
        enc = tiktoken.get_encoding('cl100k_base')
        out_ids = []
        i = 0
        while i < len(ids):
            match = self.longest_match(ids, i)
            if match:
                length, glyph = match
                glyph_id = enc.encode(glyph)[0]
                out_ids.append(glyph_id)
                i += length
            else:
                out_ids.append(ids[i])
                i += 1
        return out_ids
if __name__ == '__main__':
    patterns = {(100, 200, 300): 'α', (100, 200): 'β', (200, 300): 'γ', (400,): 'δ'}
    trie = TokenTrie(patterns)
    test_ids = [100, 200, 300, 400, 500]
    print('Testing longest match:')
    for i in range(len(test_ids)):
        match = trie.longest_match(test_ids, i)
        if match:
            print(f'  Position {i}: {match}')
    encoded = trie.encode_sequence(test_ids)
    print(f'\nOriginal: {test_ids}')
    print(f'Encoded: {encoded}')
    print(f'\nTrie stats: {trie.stats()}')
    fast_trie = FastTokenTrie(patterns)
    fast_encoded = fast_trie.encode_sequence(test_ids)
    print(f'\nFast trie encoded: {fast_encoded}')
    assert encoded == fast_encoded, 'Tries should produce same result'