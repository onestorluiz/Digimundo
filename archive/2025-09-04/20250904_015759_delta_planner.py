from __future__ import annotations
from pathlib import Path

def build_delta_plan(comp:dict)->str:
    d=comp.get("deltas",{})
    lines=["# DELTA PLAN (B - A)",
           f"- midpoint_pos_delta: {d.get('midpoint_pos_delta',0.0):.2f}",
           f"- pacing_var_delta: {d.get('pacing_var_delta',0.0):.3f}",
           f"- theme_drift_delta: {d.get('theme_drift_delta',0.0):.3f}",
           f"- char_nodes_delta: {d.get('char_nodes_delta',0)}",
           f"- char_edges_delta: {d.get('char_edges_delta',0)}",
           f"- scene_count_delta: {d.get('scene_count_delta',0)}",
           f"- avg_len_delta: {d.get('avg_len_delta',0.0):.1f}",
           "",
           "## Intervenções Prioritárias"]
    # Regras simples de priorização
    if d.get("midpoint_pos_delta",0.0)>0.08:
        lines.append("1) Reposicionar MIDPOINT (± 5-10% da duração) — aumentar tensão antes do AIL.")
    if abs(d.get("pacing_var_delta",0.0))>0.08:
        lines.append("2) Ajustar ritmo: fundir cenas curtas consecutivas e cortar platôs (curva de energia mais elástica).")
    if abs(d.get("theme_drift_delta",0.0))>0.10:
        lines.append("3) Reforçar motivos por ato (callbacks de tema em A2→A3).")
    if d.get("char_nodes_delta",0)!=0 or d.get("char_edges_delta",0)!=0:
        lines.append("4) Redesenhar rede de personagens: foco em protagonistas/coortes; remover coadjuvantes rasos.")
    if d.get("scene_count_delta",0)!=0 or abs(d.get("avg_len_delta",0.0))>120:
        lines.append("5) Rebalancear granularidade: menos cenas, mais densidade por cena (ou vice‑versa).")
    if len(lines)==10:
        lines.append("1) Passos finos: revisar beats essenciais e sequência midpoint→AIL→climax.")
    lines.append("")
    lines.append("## Ancoragem")
    lines.append("- Marcar cenas-alvo com [[BEAT:...]] e registrar âncoras (/beats align, /anchors).")
    return "\n".join(lines)

def export_delta_plan(session, comp:dict)->Path:
    home=Path(getattr(session,"home","."))
    out=home/"reports"/"compare"; out.mkdir(parents=True, exist_ok=True)
    p=out/"delta_plan.md"
    p.write_text(build_delta_plan(comp), encoding="utf-8")
    return p

def plan_to_commands(comp:dict)->list[str]:
    d=comp.get("deltas",{})
    cmds=[]
    # ordem baseada em impacto típico
    if d.get("midpoint_pos_delta",0.0)>0.08:
        cmds += ["/beats", "/draft"]
    if abs(d.get("pacing_var_delta",0.0))>0.08:
        cmds += ["/pace", "/surgery"]
    if abs(d.get("theme_drift_delta",0.0))>0.10:
        cmds += ["/theme", "/anchors"]
    if d.get("char_nodes_delta",0)!=0 or d.get("char_edges_delta",0)!=0:
        cmds += ["/characters", "/chargraph export"]
    cmds += ["/export md", "/export html"]
    # dedupe preservando ordem
    seen=set(); seq=[]
    for c in cmds:
        if c in seen: continue
        seen.add(c); seq.append(c)
    return seq