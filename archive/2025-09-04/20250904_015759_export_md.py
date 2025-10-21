from __future__ import annotations
import os, re, html
from pathlib import Path
from typing import List, Dict, Any, Tuple
from .charts_svg import bar_chart, sparkline
from .qscore import qscore as _qscore

def _safe_dir()->Path:
    base = Path(os.environ.get("SCRIPTUREMON_HOME","."))/"reports"/"coverage"
    base.mkdir(parents=True, exist_ok=True)
    return base

def _parse_ctx(ctx_text:str)->Dict[str,str]:
    """Extrai blocos [[K:...]] => snippet"""
    if not ctx_text: return {}
    blocks={}
    for m in re.finditer(r'\[\[K:([^\]]+)\]\]\s*(.+?)(?=(\n\n\[\[K:)|\Z)', ctx_text, flags=re.S):
        token = m.group(1).strip(); snippet = m.group(2).strip()
        blocks[token]=snippet
    return blocks

def _acts_from_tokens(tokens:List[str])->Dict[str,int]:
    counts={"A1":0,"A2":0,"A3":0}
    for t in tokens or []:
        parts=t.split(":")
        if len(parts)>=3:
            act = str(parts[1]).strip()  # assumindo [[K:src:ACT:scene:chunk]]
            if act in ("1","A1"): counts["A1"]+=1
            elif act in ("2","A2"): counts["A2"]+=1
            elif act in ("3","A3"): counts["A3"]+=1
    return counts

def export_one_pager(session:Any, answer_text:str, ctx_text:str, ctx_cites:List[str], 
                     qscore_val:float|None, models:List[str]|None, weights:List[float]|None)->Path:
    outdir=_safe_dir()
    doc = getattr(session,"active_doc",None)
    doc_name = Path(doc).name if doc else "—"
    # QScore fallback
    if qscore_val is None:
        qscore_val = _qscore(0.3,0.3,0.3,len(ctx_cites or []), len(answer_text or ""))
    # Charts
    acts = _acts_from_tokens(ctx_cites or [])
    acts_data=[("A1",acts["A1"]),("A2",acts["A2"]),("A3",acts["A3"])]
    acts_svg = bar_chart(acts_data, outdir/"acts.svg", width=360, height=100)
    cites_svg = bar_chart([("cites", float(len(ctx_cites or [])))], outdir/"citations.svg", width=180, height=100)
    # Models table
    mix_lines=[]
    if models and weights:
        for n,w in zip(models,weights):
            mix_lines.append(f"| {n} | {w:.2f} |")
    mix_tbl = "\n".join(["| Model | Weight |","|---|---|"]+mix_lines) if mix_lines else "_no model mix available_"
    # Context map (evidências)
    ctx_map=_parse_ctx(ctx_text or "")
    cites_md="\n".join([f"- `[{k}]` { (v.splitlines()[0] if v else '') }" for k,v in ctx_map.items()]) or "_no citations captured_"
    # Seções editoriais
    md=f"""# Scripturemon — Editorial One‑Pager

**Documento:** {doc_name}  
**QScore:** {qscore_val:.1f}

## Model Mix
{mix_tbl}

## Gráficos
![Acts]({acts_svg.name}) ![Citations]({cites_svg.name})

## Sumário Brutal
{(answer_text or '').strip()}

## Estrutura (Ato/Sequência/Beat)
- **Ato 1:** Setup, promessa do gênero, incidente incitante, lock‑in
- **Ato 2:** midpoint, reversões progressivas, crescente oposição
- **Ato 3:** clímax, resolução, imagem final
> *Notas específicas*: _adicione detalhes por cena/beat aqui quando segmentação estiver disponível._

## Personagem & Arco
- Objetivo consciente vs. necessidade inconsciente
- Relações e conflito dramático
- Transformação ou falha trágica

## Diálogo & Subtexto
- Vozes distintas, compressão de informação, subtexto funcional

## Ritmo & Cenografia
- Pacing por ato/cena; setpieces e variação de energia

## Tema & Metáfora
- Tese, antítese, síntese; imagem‑símbolo recorrente

## Riscos & Oportunidades
- Riscos: _liste os maiores riscos estruturais/dramáticos_
- Oportunidades: _onde dobrar a aposta_

## Próximos Passos
- _tarefas de reescrita priorizadas_

## Evidências (Citações)
{cites_md}

*Gerado pelo Scripturemon (1‑pager).*
"""
    outpath = outdir/"one_pager.md"
    outpath.write_text(md, encoding="utf-8")
    return outpath