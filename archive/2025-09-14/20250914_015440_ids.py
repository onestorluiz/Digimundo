from typing import List

def to_baseN(num: int, alphabet: List[str]) -> str:
    if num == 0: return alphabet[0]
    base = len(alphabet)
    out = []
    n = num
    while n > 0:
        n, r = divmod(n, base)
        out.append(alphabet[r])
    return "".join(reversed(out))