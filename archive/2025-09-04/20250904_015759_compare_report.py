from __future__ import annotations
from pathlib import Path
from typing import Dict, List
from .charts_svg import bar_chart, sparkline
from .charts_radar import radar_svg
from .score_breakdown import compute_breakdown

def export_compare(session, comp:Dict)->Path:
    home=Path(getattr(session,"home","."))
    out=home/"reports"/"compare"; out.mkdir(parents=True, exist_ok=True)
    # radars A/B
    # reconstruir scenes/acts rapidamente lendo novamente (leve)
    from .compare_core import _read_text, _split_scenes, _acts_from_scenes
    A=Path(comp["A"]); B=Path(comp["B"])
    scenesA=_split_scenes(_read_text(A)); scenesB=_split_scenes(_read_text(B))
    actsA=_acts_from_scenes(scenesA); actsB=_acts_from_scenes(scenesB)
    bdA=compute_breakdown(scenesA, actsA, [])
    bdB=compute_breakdown(scenesB, actsB, [])
    labels=["Structure","Characters","Pacing","Theme","StoryIQ"]
    valsA=[bdA[k] for k in labels]; valsB=[bdB[k] for k in labels]
    svgA=radar_svg(labels, valsA, out/"radar_A.svg", size=360)
    svgB=radar_svg(labels, valsB, out/"radar_B.svg", size=360)
    # alignment sparkline por sim
    sims=[s for _,_,s in comp.get("alignment",[])]
    if sims:
        sparkline(sims, out/"alignment.svg", width=420, height=80)
    # markdown
    md=out/"compare.md"
    def row(k,v): return f"| {k} | {v} |"
    lines=[
      f"# Compare — A vs B",
      f"**A:** {A.name}  \n**B:** {B.name}",
      "",
      "## Deltas (B - A)",
      "| Métrica | Delta |",
      "|---|---|",
      row("midpoint_pos_delta", f"{comp['deltas']['midpoint_pos_delta']:.2f}"),
      row("char_nodes_delta", comp['deltas']['char_nodes_delta']),
      row("char_edges_delta", comp['deltas']['char_edges_delta']),
      row("pacing_var_delta", f"{comp['deltas']['pacing_var_delta']:.3f}"),
      row("theme_drift_delta", f"{comp['deltas']['theme_drift_delta']:.3f}"),
      row("scene_count_delta", comp['deltas']['scene_count_delta']),
      row("avg_len_delta", f"{comp['deltas']['avg_len_delta']:.1f}"),
      "",
      "## Radar",
      f"![]({svgA.name})  ![]({svgB.name})",
      "",
      "## Alignment (similarity per matched scene)",
      f"![](alignment.svg)" if sims else "_no alignment_",
      "",
      "## Beats presentes apenas em um dos roteiros",
      f"- {', '.join(comp['deltas']['beats_present_delta']) or '—'}",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return md