
import argparse
from pathlib import Path
from .engine import analyze_screenplay, list_specialists
from .dashboard import write_dashboard
from .config_loader import load_config
from .locality import write_timeline_html, write_timeline_specialists_html, write_timeline_motifs_html
from .script_indexer import parse_scenes
from .scene_graph import build_scene_graph
from .beats import segment_beats_dynamic
from .report_arc_fsm import write_arc_fsm_html

def main():
    ap = argparse.ArgumentParser("scripturemon")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("--file", required=True)
    a.add_argument("--preset", default="enterprise")
    a.add_argument("--reflect", action="store_true")
    a.add_argument("--autofix", action="store_true")
    a.add_argument("--max-workers", type=int, default=1)
    a.add_argument("--no-report", action="store_true")
    a.add_argument("--no-entities", action="store_true")
    a.add_argument("--no-mmr", action="store_true")
    a.add_argument("--no-tfidf", action="store_true")
    a.add_argument("--no-lore-route", action="store_true")
    a.add_argument("--no-locality-gate", action="store_true")
    a.add_argument("--auto-arc", action="store_true")
    a.add_argument("--arc", action="append", help="Label de nó do arco (char:JOÃO ou topic:Memória ou só rótulo)")
    a.add_argument("--arc-top", type=int, default=2)
    a.add_argument("--contig-window", type=int, default=4)
    a.add_argument("--k-clusters", type=int, default=2)
    a.add_argument("--gate-mode", choices=["window","kmedoids"], default="window")

    sub.add_parser("list-specialists")
    sub.add_parser("dashboard")
    sg = sub.add_parser("scene-graph"); sg.add_argument("--file", required=True)
    tl = sub.add_parser("export-timeline"); tl.add_argument("--run", required=True)
    tls = sub.add_parser("export-timeline-specialists"); tls.add_argument("--run", required=True)
    tlm = sub.add_parser("export-timeline-themes"); tlm.add_argument("--run", required=True)
    af = sub.add_parser("export-arc-fsm"); af.add_argument("--run", required=True)

    args = ap.parse_args()
    if args.cmd == "analyze":
        text = Path(args.file).read_text(encoding="utf-8")
        feats = {
            "entities": not args.no_entities,
            "mmr": not args.no_mmr,
            "tfidf": not args.no_tfidf,
            "lore_route": not args.no_lore_route,
            "locality_gate": not args.no_locality_gate,
            "auto_arc": bool(args.auto_arc),
        }
        arc_labels = None
        if args.arc:
            arc_labels = []
            for a in args.arc:
                lab = a.split(":",1)[-1] if ":" in a else a
                arc_labels.append(lab)
        out = analyze_screenplay(text, preset=args.preset, reflect=args.reflect, autofix=args.autofix,
                                 max_workers=args.max_workers, report=(not args.no_report), features=feats,
                                 arc_labels=arc_labels, arc_top=args.arc_top, contig_window=args.contig_window,
                                 k_clusters=args.k_clusters, gate_mode=args.gate_mode)
        print(out)
    elif args.cmd == "list-specialists":
        for s in list_specialists():
            print(s)
    elif args.cmd == "dashboard":
        cfg = load_config()
        path = write_dashboard(cfg["paths"]["outputs"])
        print(f"Dashboard gerado em: {path}")
    elif args.cmd == "scene-graph":
        text = Path(args.file).read_text(encoding="utf-8")
        scenes = parse_scenes(text)
        beats = segment_beats_dynamic(scenes)
        sg = build_scene_graph(beats, len(scenes))
        import json as _json
        print(_json.dumps(sg, ensure_ascii=False, indent=2))
    elif args.cmd == "export-timeline":
        cfg = load_config(); run_dir = Path(cfg["paths"]["outputs"]) / args.run
        path = write_timeline_html(run_dir); print(f"Timeline em: {path}")
    elif args.cmd == "export-timeline-specialists":
        cfg = load_config(); run_dir = Path(cfg["paths"]["outputs"]) / args.run
        path = write_timeline_specialists_html(run_dir); print(f"Timeline por especialista em: {path}")
    elif args.cmd == "export-timeline-themes":
        cfg = load_config(); run_dir = Path(cfg["paths"]["outputs"]) / args.run
        path = write_timeline_motifs_html(run_dir); print(f"Timeline por motivos em: {path}")
    elif args.cmd == "export-arc-fsm":
        cfg = load_config(); run_dir = Path(cfg["paths"]["outputs"]) / args.run
        path = write_arc_fsm_html(run_dir); print(f"Arc FSM em: {path}")

if __name__ == "__main__":
    main()
