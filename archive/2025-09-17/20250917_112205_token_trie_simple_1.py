class TokenTrie:
    __slots__ = ('root',)

    def __init__(self, patterns):
        self.root = {}
        for ngram, glyph in patterns.items():
            node = self.root
            for tid in ngram:
                node = node.setdefault(tid, {})
            node['#'] = glyph

    def longest_match(self, ids, pos: int):
        node = self.root
        best_len = 0
        best_glyph = None
        i = pos
        while i < len(ids) and ids[i] in node:
            node = node[ids[i]]
            i += 1
            if '#' in node:
                best_len = i - pos
                best_glyph = node['#']
        if best_len > 0:
            return (best_len, best_glyph)
        return None