
import json
from pathlib import Path
def write_arc_fsm_html(run_dir: Path) -> str:
    f = run_dir / "arc_fsm.json"
    if not f.exists(): return ""
    d = json.loads(f.read_text(encoding="utf-8"))
    fsm = d.get("fsm", {})
    css = "body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px;} table{border-collapse:collapse;width:100%;} th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;} .mot{font-weight:600;} .pill{display:inline-block;padding:2px 8px;border-radius:999px;background:#eef; margin-right:6px;}"
    html = ["<!doctype html><meta charset='utf-8'><title>Arc FSM</title>", f"<style>{css}</style>", "<h1>Arc FSM — Transições observadas</h1>"]
    for mot, obj in fsm.items():
        html.append(f"<h2 class='mot'>{mot}</h2>")
        html.append("<p>Ordem canônica: " + " → ".join(obj.get("states_order", [])) + "</p>")
        html.append("<h3>Transições</h3>")
        if not obj.get("transitions"):
            html.append("<p><i>Nenhuma transição observada.</i></p>")
        else:
            html.append("<table><thead><tr><th>De</th><th>Para</th><th>Beat</th><th>Δ beats</th></tr></thead><tbody>")
            for t in obj["transitions"]:
                html.append(f"<tr><td>{t['from']}</td><td>{t['to']}</td><td>{t['at_beat']}</td><td>{t['delta']}</td></tr>")
            html.append("</tbody></table>")
        html.append("<h3>Sequência</h3>")
        seq = obj.get("sequence", [])
        if not seq:
            html.append("<p><i>Sem eventos.</i></p>")
        else:
            pills = " ".join([f"<span class='pill'>{s['idx']}: {s['state']}</span>" for s in seq])
            html.append(f"<p>{pills}</p>")
    out = run_dir / "arc_fsm.html"
    out.write_text("".join(html), encoding="utf-8")
    return str(out)
