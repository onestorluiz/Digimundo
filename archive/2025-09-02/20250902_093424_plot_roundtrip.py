#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera figuras para C7 (round-trip):
- reports/figures/integrity_boxplot.png  (integrity_score por dataset)
- reports/figures/entity_retain_hist.png (distribuição de entity_retain; por dataset se existir)
Robusto: se CSV/colunas faltarem ou se matplotlib não estiver disponível, faz SKIP elegante.
"""
from pathlib import Path
import sys

# tenta importar matplotlib de forma segura
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception as e:
    print("[SKIP] matplotlib indisponível:", e)
    sys.exit(0)

import pandas as pd

RT = Path("results/compression/roundtrip_samples.csv")
FIG = Path("reports/figures")
FIG.mkdir(parents=True, exist_ok=True)

def main():
    if not RT.exists():
        print("[SKIP] roundtrip_samples.csv não encontrado:", RT)
        return
    try:
        df = pd.read_csv(RT)
    except Exception as e:
        print("[SKIP] erro lendo CSV:", e)
        return

    # -------- integrity_boxplot.png --------
    if "integrity_score" in df.columns:
        vals = pd.to_numeric(df["integrity_score"], errors="coerce")
        if "dataset" in df.columns:
            order = list(df["dataset"].dropna().unique())
            data = [pd.to_numeric(df.loc[df["dataset"]==g, "integrity_score"], errors="coerce").dropna().tolist()
                    for g in order]
            if any(len(x)>0 for x in data):
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.boxplot(data, labels=[str(g) for g in order], showmeans=True)
                ax.set_title("Integrity Score by Dataset")
                ax.set_ylabel("integrity_score")
                fig.savefig(FIG/"integrity_boxplot.png", dpi=120)
                plt.close(fig)
        else:
            s = vals.dropna()
            if len(s):
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.boxplot([s.tolist()], labels=["all"], showmeans=True)
                ax.set_title("Integrity Score")
                ax.set_ylabel("integrity_score")
                fig.savefig(FIG/"integrity_boxplot.png", dpi=120)
                plt.close(fig)

    # -------- entity_retain_hist.png --------
    if "entity_retain" in df.columns:
        if "dataset" in df.columns:
            order = list(df["dataset"].dropna().unique())
            # hist por grupo em múltiplas séries (sem escolher cores explicitamente)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            for g in order:
                s = pd.to_numeric(df.loc[df["dataset"]==g, "entity_retain"], errors="coerce").dropna()
                if len(s):
                    ax.hist(s, bins=20, alpha=0.5, label=str(g))
            ax.set_title("Entity Retain — Distribution (by dataset)")
            ax.set_xlabel("entity_retain")
            ax.set_ylabel("count")
            try:
                ax.legend()
            except Exception:
                pass
            fig.savefig(FIG/"entity_retain_hist.png", dpi=120)
            plt.close(fig)
        else:
            s = pd.to_numeric(df["entity_retain"], errors="coerce").dropna()
            if len(s):
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.hist(s, bins=20)
                ax.set_title("Entity Retain — Distribution")
                ax.set_xlabel("entity_retain")
                ax.set_ylabel("count")
                fig.savefig(FIG/"entity_retain_hist.png", dpi=120)
                plt.close(fig)

    print("[OK] figures ->", FIG)

if __name__ == "__main__":
    main()