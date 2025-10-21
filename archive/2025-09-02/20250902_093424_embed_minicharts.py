# -*- coding: utf-8 -*-
from __future__ import annotations
import html

def _svg_wrap(w:int,h:int,body:str)->str:
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{body}</svg>'

def sparkline(values:list[float], w:int=160, h:int=28, pad:int=3)->str:
    vals=[float(v) for v in values if v is not None]
    if not vals: return _svg_wrap(w,h,'<text x="2" y="16" font-size="10">n/a</text>')
    mn,mx=min(vals),max(vals)
    rng=(mx-mn) or 1.0
    step=max(1,(w-2*pad)//max(1,len(vals)-1))
    points=[]
    for i,v in enumerate(vals):
        x=pad+i*step
        y=h-pad - int((v-mn)/rng*(h-2*pad))
        points.append((x,y))
    d='M ' + ' L '.join(f'{x} {y}' for x,y in points)
    body=f'<polyline fill="none" stroke="currentColor" stroke-width="1.5" points="{" ".join(f"{x},{y}" for x,y in points)}" />'
    # min/max dots
    body+=f'<circle cx="{points[0][0]}" cy="{points[0][1]}" r="1.5" fill="currentColor"/>' if points else ''
    body+=f'<circle cx="{points[-1][0]}" cy="{points[-1][1]}" r="1.5" fill="currentColor"/>' if points else ''
    return _svg_wrap(w,h,body)

def hbars(labels:list[str], values:list[float], w:int=220, bar_h:int=10, gap:int=4)->str:
    n=len(values)
    if n==0: return _svg_wrap(w,bar_h+2,'<text x="2" y="10" font-size="10">n/a</text>')
    h = n*(bar_h+gap)+gap
    mx = max(1.0, max(values))
    rows=[]
    for i,(lab,val) in enumerate(zip(labels,values)):
        y = i*(bar_h+gap)+gap
        ww = int((val/mx)*(w-80))
        rows.append(f'<rect x="70" y="{y}" width="{ww}" height="{bar_h}" fill="currentColor" opacity="0.35"/>'
                    f'<text x="2" y="{y+bar_h-2}" font-size="9">{html.escape(lab[:14])}</text>'
                    f'<text x="{70+ww+4}" y="{y+bar_h-2}" font-size="9">{int(val)}</text>')
    return _svg_wrap(w,h,"".join(rows))

def hist(values:list[float], bins:int=16, w:int=220, h:int=36, pad:int=2)->str:
    vals=[float(v) for v in values if v is not None]
    if not vals: return _svg_wrap(w,h,'<text x="2" y="16" font-size="10">n/a</text>')
    mn,mx=min(vals),max(vals); rng=(mx-mn) or 1.0
    counts=[0]*bins
    for v in vals:
        idx=min(bins-1,int((v-mn)/rng*bins))
        counts[idx]+=1
    cmax=max(counts) or 1
    bw=(w-2*pad)/bins
    rects=[]
    for i,c in enumerate(counts):
        bh=int((c/cmax)*(h-2*pad))
        x=int(pad+i*bw); y=h-pad-bh
        rects.append(f'<rect x="{x}" y="{y}" width="{int(bw)-1}" height="{bh}" fill="currentColor" opacity="0.35"/>')
    return _svg_wrap(w,h,"".join(rects))

def heatmap_grid(x_labels:list[str], y_labels:list[str], values:list[list[float]], 
                 cell:int=18, pad:int=4, show_text:bool=True)->str:
    if not x_labels or not y_labels or not values:
        return _svg_wrap(220,36,'<text x="2" y="16" font-size="10">n/a</text>')
    rows=len(y_labels); cols=len(x_labels)
    w = pad*2 + cols*cell; h = pad*2 + rows*cell + 12
    # max normalizado p/ opacidade
    mx=0.0
    for r in values:
        for v in r:
            try: mx=max(mx, float(v))
            except: pass
    mx = mx or 1.0
    parts=[]
    # eixos
    for j,lab in enumerate(x_labels):
        x = pad + j*cell + cell/2
        parts.append(f'<text x="{int(x)-4}" y="{pad-2}" font-size="8" transform="rotate(-45 {int(x)-4},{pad-2})">{html.escape(lab[:10])}</text>')
    for i,lab in enumerate(y_labels):
        y = pad + i*cell + cell-3
        parts.append(f'<text x="2" y="{int(y)}" font-size="8">{html.escape(lab[:12])}</text>')
    # células
    for i in range(rows):
        for j in range(cols):
            v = 0.0
            try: v=float(values[i][j])
            except: v=0.0
            op = 0.15 + 0.75*(v/mx)  # 0.15..0.90
            x = pad + j*cell + 60
            y = pad + i*cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell-1}" height="{cell-1}" fill="currentColor" opacity="{op:.3f}"/>')
            if show_text:
                txt = f"{v:.1f}"
                parts.append(f'<text x="{x+2}" y="{y+cell-5}" font-size="7" fill="black" opacity="0.8">{txt}</text>')
    return _svg_wrap(int(w+60),int(h), "".join(parts))