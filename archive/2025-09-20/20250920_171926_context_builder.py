from typing import List, Dict, Any
import tiktoken

def pack_context(query: str, docs: List[Dict[str, Any]], model_name: str = "cl100k_base", max_tokens: int = 32000, reserve_for_output: int = 1024) -> str:
    enc = tiktoken.get_encoding("cl100k_base")
    budget = max_tokens - reserve_for_output
    parts = [f"[QUERY]\n{query}\n", "[CONTEXT]\n"]
    used = len(enc.encode("".join(parts)))
    for r in docs:
        block = f"\n---\n[CHUNK id={r.get('id')} p≈{r.get('meta',{}).get('page_hint','?')}]\n{r['doc'][:4000]}\n"
        toks = len(enc.encode(block))
        if used + toks > budget:
            break
        parts.append(block)
        used += toks
    return "".join(parts)
