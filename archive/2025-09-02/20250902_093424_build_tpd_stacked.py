#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Constrói TPD em camadas: aplica L1 (greedy-lazy) no corpus cru,
em seguida comprime o corpus com L1 e minera L2 sobre a sequência comprimida, etc.
Salva em formato multilayer (multitpd).
"""
import argparse, time, json
from pathlib import Path
import tiktoken
from src.digilang.tpd_greedy_lazy import build_tpd_greedy_lazy_for_corpus
from src.digilang.multitpd import save_layers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/screenplay_synth")
    ap.add_argument("--outdir", default="data/tpd/stacked")
    ap.add_argument("--layers", default="1500,1500")  # K por camada
    ap.add_argument("--nmin", type=int, default=2)
    ap.add_argument("--nmax", type=int, default=8)
    ap.add_argument("--fmin", type=int, default=3)
    ap.add_argument("--time_budget_s", type=float, default=30.0)
    args = ap.parse_args()

    Ks = [int(x) for x in args.layers.split(",") if x.strip()]
    enc = tiktoken.get_encoding("cl100k_base")

    # L1 no corpus cru
    mapping_layers = []
    m1 = build_tpd_greedy_lazy_for_corpus(args.corpus, K=Ks[0], n_min=args.nmin, n_max=args.nmax, freq_min=args.fmin, time_budget_s=args.time_budget_s)
    mapping_layers.append(m1)

    # Comprimir o corpus com L1 para gerar "texto base" da próxima camada
    def apply_layer_text(text: str, mapping):
        # substitui token-level por glyphs (1 token)
        from src.digilang.token_trie import TokenTrie
        patterns = {tuple(v): k for k,v in mapping.items()}
        trie = TokenTrie(patterns)
        ids = enc.encode(text); out=[]; i=0
        while i<len(ids):
            m = trie.longest_match(ids, i)
            if m:
                ln, glyph = m
                out.append(enc.encode(glyph)[0]); i+=ln
            else:
                out.append(ids[i]); i+=1
        return enc.decode(out)

    # Gerar corpus comprimido L1 (concatenado)
    texts=[]
    for p in Path(args.corpus).rglob("*.txt"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
            texts.append(t)
        except: pass
    base = "\n\n".join(texts)
    comp1 = apply_layer_text(base, m1)

    # L2 sobre a sequência comprimida
    if len(Ks) >= 2 and Ks[1] > 0:
        # escreve comp1 temporariamente
        tmp = Path("data/_tmp_comp1"); tmp.mkdir(parents=True, exist_ok=True)
        (tmp/"all.txt").write_text(comp1, encoding="utf-8")
        m2 = build_tpd_greedy_lazy_for_corpus(str(tmp), K=Ks[1], n_min=args.nmin, n_max=args.nmax, freq_min=args.fmin, time_budget_s=args.time_budget_s)
        mapping_layers.append(m2)

    # (Opcional) L3: repetir processo mais uma vez se necessário
    # para manter simples, duas camadas já dão ganhos substanciais

    outdir = Path(args.outdir)/f"K{'-'.join(map(str, Ks))}"
    outdir.mkdir(parents=True, exist_ok=True)
    meta = {"tokenizer":"cl100k_base","layers":Ks,"built_at":time.time(),"strategy":"stacked_greedy_lazy"}
    save_layers(mapping_layers, str(outdir/"token_dict.json"), meta)
    print(f"[OK] stacked TPD -> {outdir}/token_dict.json")

if __name__ == "__main__":
    main()