from __future__ import annotations
from pathlib import Path
import csv, math, html

def heatmap_from_matrix(csv_path:Path, out_svg:Path, max_cells:int=2500, size:int=720)->Path:
    rows=[]
    with open(csv_path,"r",encoding="utf-8") as f:
        r=csv.DictReader(f)
        for row in r:
            try:
                rows.append((row["A"], row["B"], float(row["dist"])))
            except Exception:
                continue
    # Mapear nomes para índices
    names=set()
    for a,b,_ in rows: 
        names.add(a); names.add(b)
    names=sorted(list(names))
    if not names:
        out_svg.write_text("<svg xmlns='http://www.w3.org/2000/svg' width='640' height='200'><text x='10' y='50' fill='#888'>empty matrix</text></svg>", encoding="utf-8")
        return out_svg
    idx={n:i for i,n in enumerate(names)}
    N=len(names)
    # Limite de células para não estourar
    cap=min(N*N, max_cells)
    cell=min(18, max(6, size//max(1,N+6)))
    pad=cell*3
    W=pad*2 + cell*N
    H=W
    # normalização simples
    vals=[d for _,_,d in rows]
    if not vals: 
        minv,maxv=0.0,1.0
    else:
        minv,maxv=min(vals),max(vals)
        if maxv-minv < 1e-9:
            maxv=minv+1.0
    def col(v):
        # azul claro (baixo) -> rosa (alto)
        t=(v-minv)/(maxv-minv)
        r=int(255*min(1.0,max(0.0,t)))
        g=int(80 + 80*(1.0-t))
        b=int(180 + 60*(1.0-t))
        return f"rgb({r},{g},{b})"
    # monta SVG
    out=["<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}'>".format(W=W,H=H),
         "<rect width='100%' height='100%' fill='#0b0f17'/>",
         f"<text x='10' y='20' fill='#9ca3af' font-size='12'>matrix: {html.escape(csv_path.name)}</text>"]
    # eixos
    for i,name in enumerate(names):
        x=pad + i*cell; y=pad + i*cell
        out.append(f"<text x='{pad-6}' y='{pad + i*cell + cell*0.7:.1f}' fill='#94a3b8' font-size='9' text-anchor='end'>{html.escape(Path(name).stem[:22])}</text>")
        out.append(f"<text transform='translate({pad + i*cell + cell*0.5:.1f},{pad-8}) rotate(-60)' fill='#94a3b8' font-size='9' text-anchor='end'>{html.escape(Path(name).stem[:22])}</text>")
    # células
    count=0
    for a,b,d in rows:
        ia=idx[a]; ib=idx[b]
        x=pad + ib*cell; y=pad + ia*cell
        out.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{cell-1}' height='{cell-1}' fill='{col(d)}'/>")
        out.append(f"<rect x='{pad + ia*cell:.1f}' y='{pad + ib*cell:.1f}' width='{cell-1}' height='{cell-1}' fill='{col(d)}'/>") # simetria
        count+=2
        if count>=cap: break
    out.append("</svg>")
    out_svg.parent.mkdir(parents=True, exist_ok=True)
    out_svg.write_text("".join(out), encoding="utf-8")
    return out_svg