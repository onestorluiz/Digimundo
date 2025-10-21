from __future__ import annotations
from pathlib import Path
from typing import List, Tuple

def _svg_header(w:int,h:int)->str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
def _svg_footer()->str: return '</svg>'

def bar_chart(data:List[Tuple[str,float]], path:Path, width:int=360, height:int=100, pad:int=8)->Path:
    """data: [(label, value)] — barra horizontal com labels no eixo X"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not data:
        path.write_text(_svg_header(width,height)+'<text x="10" y="55" fill="#94a3b8" font-size="12">no data</text>'+_svg_footer(), encoding="utf-8"); return path
    maxv = max(v for _,v in data) or 1.0
    n = len(data)
    bw = (width - pad*2) / max(n,1)
    svg=[_svg_header(width,height), f'<rect width="{width}" height="{height}" fill="#0b0f17"/>']
    for i,(lab,val) in enumerate(data):
        x = pad + i*bw + 2
        h = int((height - 30) * (val/maxv))
        y = height - 20 - h
        svg.append(f'<rect x="{x}" y="{y}" width="{bw-4:.1f}" height="{h}" fill="#38bdf8"/>')
        svg.append(f'<text x="{x+ (bw-4)/2:.1f}" y="{height-6}" fill="#94a3b8" font-size="10" text-anchor="middle">{lab}</text>')
    svg.append(_svg_footer())
    path.write_text("".join(svg), encoding="utf-8")
    return path

def sparkline(vals:List[float], path:Path, width:int=360, height:int=60, pad:int=8)->Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not vals:
        path.write_text(_svg_header(width,height)+'<text x="10" y="32" fill="#94a3b8" font-size="12">no data</text>'+_svg_footer(), encoding="utf-8"); return path
    minv, maxv = min(vals), max(vals)
    rng = (maxv - minv) or 1.0
    dx = (width - pad*2) / max(1, len(vals)-1)
    points=[]
    for i,v in enumerate(vals):
        x = pad + i*dx
        y = pad + (height-2*pad) * (1 - (v-minv)/rng)
        points.append(f"{x:.1f},{y:.1f}")
    svg=[_svg_header(width,height), f'<rect width="{width}" height="{height}" fill="#0b0f17"/>',
         f'<polyline fill="none" stroke="#7dd3fc" stroke-width="2" points="{" ".join(points)}"/>', _svg_footer()]
    path.write_text("".join(svg), encoding="utf-8")
    return path