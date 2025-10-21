from __future__ import annotations
from pathlib import Path
from math import cos, sin, pi
from typing import List
def radar_svg(labels:List[str], values:List[float], path:Path, size:int=320)->Path:
    # values em 0..100
    N=len(labels); R=size//2-24; cx=cy=size//2
    def pt(i,v):
        ang = -pi/2 + (2*pi*i/N)
        r = R*(max(0,min(100,v))/100.0)
        return cx + r*cos(ang), cy + r*sin(ang)
    # grid
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}"><rect width="100%" height="100%" fill="#0b0f17"/>']
    for k in (20,40,60,80,100):
        rr=R*(k/100.0); svg.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="#1f2937" stroke-width="1"/>')
    # axes + labels
    for i,l in enumerate(labels):
        x,y = pt(i,100)
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#1f2937" stroke-width="1"/>')
        lx,ly = pt(i,115)
        svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#94a3b8" font-size="10" text-anchor="middle">{l}</text>')
    # polygon
    P=" ".join(f'{pt(i,values[i])[0]:.1f},{pt(i,values[i])[1]:.1f}' for i in range(N))
    svg.append(f'<polygon points="{P}" fill="#38bdf833" stroke="#38bdf8" stroke-width="2"/>')
    svg.append('</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(svg), encoding="utf-8")
    return path