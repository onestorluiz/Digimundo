
from pathlib import Path
import json as _json, json, time
from .config_loader import load_config
from .llm_adapter import LLMAdapter, LLMConfig
from .cache import DiskCache
from .artifacts import ArtifactWriter
from .telemetry import Metrics, Timer
from .json_repair import try_parse_json
from .specialists_registry import load_specialists
from .rag_api import RAGService
from .memory_store import Doc
from .run_id import make_run_id
from .evidence_policy import enforce_evidence
from .presets import resolve_preset, preset_requires_reflection
from .baseline_metrics import ratio_dialogue, avg_scene_len
from .validators import validate_spec
from .reflection import reflect_once
from .evidence_gate import require_evidence_or_retry
from .evaluation import evaluate, write_html_report
from .modes import Modes, apply_modes
from .script_indexer import parse_scenes, format_offset
from .consistency import check_consistency
from .structure_baseline import compute_structure
from .snippet_utils import make_queries
from .entity_detect import detect_entities_topics, queries_for_entities
from .beats import segment_beats_dynamic, acts_from_line_count
from .hier_omega_plus import HierOmegaPlusConfig, hierarchical_search, build_blocks
from .lore_router import index_lore_projects, route_projects, build_lore_blocks
from .scene_graph import build_scene_graph
from .beats_meta_util import build_beats_meta
from .arc_router import select_arcs_from_graph, score_beats_for_arcs
from .arc_progress import compute_arc_progress
from .arc_fsm import build_fsm
from .cite_check import spot_check_support

PRIORITY = {'logline':100,'pacing':90,'theme':80,'market':70,'structure':60}
DEFAULT_FEATURES = {"entities": True, "mmr": True, "tfidf": True, "lore_route": True, "locality_gate": True, "auto_arc": True}

def analyze_screenplay(screenplay_text: str, preset: str="complete", reflect: bool|None=None, max_workers: int=1, report: bool=True, autofix: bool=False, features: dict | None = None, arc_labels: list[str] | None = None, arc_top: int = 2, contig_window: int = 4, k_clusters: int = 2, gate_mode: str = "window") -> dict:
    cfg = load_config()
    features = {**DEFAULT_FEATURES, **(features or {})}
    run_id = make_run_id({"screenplay": screenplay_text[:1000], "version": cfg["version"], "preset": preset, "features": features, "arc_labels": arc_labels, "arc_top": arc_top, "contig": contig_window, "k": k_clusters, "gate": gate_mode})
    aw = ArtifactWriter(cfg["paths"]["outputs"], run_id)
    metrics = Metrics(f"{cfg['paths']['outputs']}/{run_id}/metrics.csv")
    cache = DiskCache(f"{cfg['paths']['outputs']}/{run_id}/cache")
    rag = RAGService()

    # Lore
    lore_root = str(Path(cfg["paths"]["data"]) / "lore")
    projects = index_lore_projects(rag, lore_root) if features.get("lore_route", True) else []

    scenes = parse_scenes(screenplay_text)
    if scenes:
        first = scenes[0]
        excerpt_text = first.text
        default_script_offset = format_offset(first.start_line, first.end_line)
        struct = compute_structure(screenplay_text)
        acts = acts_from_line_count(struct.get("lines", 0))
        beats = segment_beats_dynamic(scenes)
        for b in beats:
            rag.index(Doc(id=f"beat_{b.id}", text=b.text, ns="script_beat", meta={"scene_index": str(b.scene_index), "idx_in_scene": str(b.idx_in_scene), "weight": str(b.weight)}))
        for i, sc in enumerate(scenes, start=1):
            rag.index(Doc(id=f"scene_{i}", text=sc.text, ns="script_scene", meta={"title": sc.title, "scene_index": str(i)}))
        for act_id, (start_line, end_line) in acts.items():
            buf = []
            for i, sc in enumerate(scenes, start=1):
                if sc.start_line >= start_line and sc.end_line <= end_line:
                    buf.append(sc.text)
            rag.index(Doc(id=act_id, text="\\n\\n".join(buf), ns="script_act", meta={"range": f"{start_line}-{end_line}"}))
        rag.index(Doc(id="global1", text="\\n\\n".join(sc.text for sc in scenes), ns="script_global", meta={"src":"all"}))
        focus_scene_idx = 1
        meta = build_beats_meta(beats); aw.write("beats_meta.json", meta)
        sg = build_scene_graph(beats, len(scenes)); aw.write("scene_graph.json", sg)
        aw.write("beats_texts.json", {b.id: b.text for b in beats})
    else:
        excerpt_text = screenplay_text[:1200]
        default_script_offset = "p1:l1-55"
        rag.index(Doc(id="global1", text=screenplay_text, ns="script_global", meta={"src":"all"}))
        focus_scene_idx = 1
        meta = {"total_beats": 1, "index_map": {"dyn_1_1": 0}, "weights": [1.0], "by_scene": {"1":[{"beat_id":"dyn_1_1","global_index":0}]}}; aw.write("beats_meta.json", meta)
        sg = {"nodes": [], "edges": [], "beats": [], "scenes": 0}; aw.write("scene_graph.json", sg)
        aw.write("beats_texts.json", {"dyn_1_1": excerpt_text})

    # LLM
    llm_cfg = LLMConfig(backend=str(cfg.get("backend","mock")), model=str(cfg.get("model","mock")))
    if preset == "champion":
        llm_cfg = apply_modes(llm_cfg, Modes(no_internet=True, deterministic=True))
    llm = LLMAdapter(llm_cfg)

    # Specialists
    from .specialists_registry import load_specialists
    specs_all = [s for s in load_specialists(cfg["paths"]["specialists"]) if s.enabled]
    wanted = resolve_preset(preset)
    specs = [s for s in specs_all if s.id in wanted]
    if reflect is None: reflect = preset_requires_reflection(preset)

    # Baselines
    dlg_ratio = ratio_dialogue(screenplay_text)
    scene_len = avg_scene_len(screenplay_text)
    baseline_str = f"dialogue_ratio:{dlg_ratio:.2f}; avg_scene_len:{scene_len:.2f}"
    aw.write("inputs.json", {"preset": preset, "run_id": run_id, "baseline": {"dialogue_ratio": dlg_ratio, "avg_scene_len": scene_len},
                             "specialists": [s.id for s in specs], "default_script_offset": default_script_offset, "features": features,
                             "arc_labels": arc_labels, "arc_top": arc_top, "contig_window": contig_window, "k_clusters": k_clusters, "gate_mode": gate_mode})

    # Entities & queries
    ent = detect_entities_topics(screenplay_text) if features.get("entities", True) else {"characters": [], "proper": [], "topics": []}
    ent_qs = queries_for_entities(ent, max_q=6) if features.get("entities", True) else []
    qlist = list(dict.fromkeys(make_queries(excerpt_text) + ent_qs))

    # Arcos (nós)
    arc_nodes = []
    if arc_labels:
        label_set = set(arc_labels)
        for n in sg.get("nodes", []):
            if n.get("label") in label_set:
                arc_nodes.append(n)
        for lab in arc_labels:
            if not any(n.get("label")==lab for n in arc_nodes):
                arc_nodes.append({"id": f"topic:{lab}", "label": lab, "type": "topic", "score": 0.0})
    elif features.get("auto_arc", True):
        from .arc_router import select_arcs_from_graph
        arc_nodes = select_arcs_from_graph(sg, top_k=int(arc_top))
    text_by_beat = {f"beat_{k}": (rag.get_text(f"beat_{k}") or "") for k in meta.get("index_map", {}).keys()}
    from .arc_router import score_beats_for_arcs
    arc_scores = score_beats_for_arcs(sg.get("beats", []), text_by_beat, arc_nodes) if arc_nodes else {}

    # Arc progress + FSM
    pr = compute_arc_progress({k: (rag.get_text(f"beat_{k}") or "") for k in meta.get("index_map", {}).keys()}, arc_labels=arc_labels)
    aw.write("arc_progress.json", pr)
    progress_scores = pr.get("progress_scores", {})
    fsm = build_fsm({k: (rag.get_text(f"beat_{k}") or "") for k in meta.get("index_map", {}).keys()}, meta.get("index_map", {}), pr.get("events", []))
    aw.write("arc_fsm.json", fsm)

    outputs: dict[str, dict] = {}; theme_motifs: list[str] | None = None

    for sid in sorted([s.id for s in specs], key=lambda x: PRIORITY.get(x,50), reverse=True):
        spec = next(s for s in specs if s.id == sid)
        if getattr(spec, 'mode', 'llm') == 'deterministic' and spec.id == 'structure':
            base = compute_structure(screenplay_text)
            data = {"quality": 0.95, "evidence": {"script_offset": default_script_offset,
                    "rag_doc_id": "beat:dyn_1_1", "baseline_metric": f"dialogue_ratio:{dlg_ratio:.2f}"}, "payload": base}
            outputs[sid]=data; aw.write(f"parsed_{spec.id}.json", data); continue

        rag_blocks = []
        cfgH = HierOmegaPlusConfig(contig_window=int(contig_window), clusters_k=int(k_clusters), gate_mode=gate_mode)
        docs = hierarchical_search(rag, qlist, focus_scene_idx, cfgH, features, arc_scores, progress_scores, meta.get("index_map", {}), motifs=theme_motifs)
        rag_blocks += build_blocks(rag, docs, excerpt_text, features)
        if features.get("lore_route", True) and qlist:
            projs = route_projects(rag, qlist[0], projects, top_k=2)
            rag_blocks += build_lore_blocks(rag, projs, qlist[0], max_chars=420)
        rag_marker = "\\n\\n".join(rag_blocks)

        prompt_tpl = Path(spec.prompt_path).read_text(encoding="utf-8")
        prompt = (f"### SPECIALIST_ID: {spec.id}\\n" + prompt_tpl.replace("{EXCERPT}", excerpt_text)
                  .replace("{RAG_DOCS}", rag_marker).replace("{BASELINE}", baseline_str))

        key = cache.key_of(cfg.get("model","mock"), prompt, cfg["version"], preset)
        raw = cache.get(key)
        if not raw:
            raw = llm.generate(prompt); cache.set(key, raw)

        try: data = try_parse_json(raw)
        except Exception: data = {"quality": 0.0, "evidence": {}, "payload": {"error": "parse_failed"}}

        ev = data.get("evidence", {}) or {}
        ev.setdefault("script_offset", default_script_offset)
        ev.setdefault("rag_doc_id", (rag_blocks[0].split(']')[0]+']') if rag_blocks else "beat:dyn_1_1")
        ev.setdefault("baseline_metric", f"dialogue_ratio:{dlg_ratio:.2f}")
        data["evidence"] = ev

        data = validate_spec(spec.id, enforce_evidence(data))

        if reflect:
            try:
                before = json.loads(_json.dumps(data, ensure_ascii=False))
                fixed = reflect_once(llm, _json.dumps(data, ensure_ascii=False), specialist_id=spec.id)
                data2 = try_parse_json(fixed)
                data = validate_spec(spec.id, enforce_evidence(data2))
            except Exception:
                pass

        data = require_evidence_or_retry(llm, spec.id, data, tries=1)

        outputs[sid]=data
        aw.write(f"raw_{spec.id}.txt", raw)
        aw.write(f"parsed_{spec.id}.json", data)
        aw.write(f"retrieval_{spec.id}.json", {"queries": qlist, "rag_blocks": rag_blocks, "features": features, "arc_nodes": arc_nodes})

        if sid == "theme":
            try:
                theme_motifs = data.get("payload",{}).get("motifs",[]) or None
                aw.write("parsed_theme.json", data)
            except Exception:
                pass

    aw.write("consistency.json", check_consistency(outputs))

    sc = spot_check_support(Path(cfg["paths"]["outputs"])/run_id, outputs)
    aw.write("spot_check.json", sc)

    evalres = evaluate(outputs, run_dir=Path(cfg["paths"]["outputs"])/run_id); aw.write("evaluation.json", evalres)
    if report:
        write_html_report(f"{cfg['paths']['outputs']}/{run_id}/report.html",
                          {"preset": preset, "run_id": run_id, "features": features, "arcs_used": arc_nodes, "contig_window": contig_window, "k_clusters": k_clusters, "gate_mode": gate_mode},
                          outputs, evalres, run_dir=Path(cfg["paths"]["outputs"])/run_id)

    from .locality import locality_metrics
    loc = locality_metrics(Path(cfg["paths"]["outputs"])/run_id)
    aw.append_history({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_id": run_id,
        "preset": preset,
        "quality": evalres["macro"]["quality"],
        "faithfulness": evalres["macro"]["faithfulness"],
        "relevancy": evalres["macro"]["relevancy"],
        "locality": loc.get("locality_coherence", 0.0),
        "production_score": evalres["macro"]["production_score"],
        "specialists": ",".join([s.id for s in specs])
    })

    aw.stamp("done", {"specialists": [s.id for s in specs]})
    return outputs

def list_specialists():
    cfg = load_config()
    return [s.id for s in load_specialists(cfg["paths"]["specialists"])]
