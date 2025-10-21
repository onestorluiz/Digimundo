
from pathlib import Path
import json, re

def _sanitize(s: str) -> str:
    return "".join(ch if 32 <= ord(ch) <= 126 else "?" for ch in s)

def export_markdown(outputs_root: str, run_id: str) -> str:
    p = Path(outputs_root) / run_id / "evaluation.json"
    outp = Path(outputs_root) / run_id / "export.md"
    if not p.exists(): raise FileNotFoundError("evaluation.json não encontrado")
    data = json.loads(p.read_text(encoding="utf-8"))
    out = ["# Scripturemon — Export (Markdown)"]
    out.append(f"Run: `{run_id}`\n")
    macro = data.get("macro", {})
    out.append("## KPIs")
    out.append(f"- Quality: **{macro.get('quality',0.0):.2f}**")
    out.append(f"- Faithfulness: **{macro.get('faithfulness',0.0):.2f}**")
    out.append(f"- Relevancy: **{macro.get('relevancy',0.0):.2f}**\n")
    out.append("## Detalhes por especialista")
    det = data.get("details", {})
    for sid, s in det.items():
        out.append(f"### {sid}")
        out.append(f"- Quality: {s.get('quality',0.0):.2f}")
        out.append(f"- Faithfulness: {s.get('faithfulness',0.0):.2f}")
        out.append(f"- Relevancy: {s.get('relevancy',0.0):.2f}")
    # Add evidence snapshot
    evp = Path(outputs_root) / run_id / "parsed_logline.json"
    if evp.exists():
        out.append("\n## Evidence snapshot (logline)")
        d = json.loads(evp.read_text(encoding="utf-8"))
        out.append("```json\n" + json.dumps(d, ensure_ascii=False, indent=2) + "\n```")
    outp.write_text("\n".join(out), encoding="utf-8")
    return str(outp)

def export_json_scene_agg(outputs_root: str, run_id: str) -> str:
    # aggregate offsets/snippets by scene based on p:l mapping
    base = Path(outputs_root) / run_id
    ev_files = list(base.glob("parsed_*.json"))
    # load screenplay to map scenes
    inputs = json.loads((base / "inputs.json").read_text(encoding="utf-8"))
    # We don't have full screenplay here; scene boundaries unknown — export raw offsets with computed absolute line
    from .script_indexer import page_line_to_abs
    agg = {}
    for f in ev_files:
        sid = f.stem.replace("parsed_","")
        d = json.loads(f.read_text(encoding="utf-8"))
        ev = d.get("evidence", {}) or {}
        off = ev.get("script_offset","")
        m = re.match(r"p(\d+):l(\d+)", str(off))
        abs_line = None
        if m:
            p, l = int(m.group(1)), int(m.group(2))
            abs_line = page_line_to_abs(p, l, page_lines=55)
        agg.setdefault(sid, []).append({"offset": off, "abs_line": abs_line, "rag": ev.get("rag_doc_id")})
    outp = base / "export_scene_agg.json"
    outp.write_text(json.dumps(agg, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(outp)

def export_pdf(outputs_root: str, run_id: str) -> str:
    # Very simple text PDF with KPIs; ASCII-only
    evalp = Path(outputs_root) / run_id / "evaluation.json"
    outp = Path(outputs_root) / run_id / "export.pdf"
    data = json.loads(evalp.read_text(encoding="utf-8"))
    macro = data.get("macro", {})
    text = f"Scripturemon Report\\nRun: {run_id}\\nQuality: {macro.get('quality',0.0):.2f}\\nFaithfulness: {macro.get('faithfulness',0.0):.2f}\\nRelevancy: {macro.get('relevancy',0.0):.2f}\\n"
    text = _sanitize(text)
    # Build minimal PDF
    lines = text.split("\\n")
    content = ["BT", "/F1 12 Tf", "1 0 0 1 72 770 Tm"]
    y = 0
    for ln in lines:
        content.append(f"({ln}) Tj")
        content.append("0 -16 Td")
    content.append("ET")
    stream = "\\n".join(content).encode("latin-1", errors="ignore")
    xref = []
    pdf = b"%PDF-1.4\\n"
    def obj(idx, body):
        off = len(pdf)
        nonlocal xref
        xref.append(off)
        return pdf + f"{idx} 0 obj\\n".encode() + body + b"\\nendobj\\n"
    # Font
    pdf = obj(1, b"<< /Type /Font /Subtype /Type1 /Name /F1 /BaseFont /Helvetica >>")
    # Contents
    pdf = obj(2, b"<< /Length %d >>\\nstream\\n%s\\nendstream" % (len(stream), stream))
    # Page
    pdf = obj(3, b"<< /Type /Page /Parent 4 0 R /Resources << /Font << /F1 1 0 R >> >> /MediaBox [0 0 595 842] /Contents 2 0 R >>")
    # Pages
    pdf = obj(4, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    # Catalog
    pdf = obj(5, b"<< /Type /Catalog /Pages 4 0 R >>")
    # Xref
    xref_off = len(pdf)
    pdf += b"xref\\n0 6\\n0000000000 65535 f \\n"
    for off in xref:
        pdf += f"{off:010} 00000 n \\n".encode()
    pdf += b"trailer<< /Size 6 /Root 5 0 R >>\\nstartxref\\n" + str(xref_off).encode() + b"\\n%%EOF"
    outp.write_bytes(pdf)
    return str(outp)
