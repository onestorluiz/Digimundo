import argparse, json, sys
from pathlib import Path

from .script_doctor import ScriptDoctor
from ..learning import Learning
from .theory import TheoryComparator
from .training import ProtoTrainer, ProtoModel
from .chat_terminal import ScripturemonChat, ChatConfig
from .coach import DoctorCoach
from .autotag import AutoTagger
from .frameworks import three_act, story_circle
from .miner import PatternMiner
from .author import AuthorModel

def cmd_status(a):
    ll = Learning()
    print(json.dumps({"learning": ll.get_statistics()}, ensure_ascii=False, indent=2))

def cmd_doctor_analyze(a):
    txt = Path(a.file).read_text(encoding="utf-8", errors="replace")
    doc = ScriptDoctor(use_learning=True, genre=a.genre)
    sa = doc.analyze_script(txt, screenplay_name=Path(a.file).stem)
    print(json.dumps(sa.to_dict(), ensure_ascii=False, indent=2))

def cmd_doctor_stc(a):
    txt = Path(a.file).read_text(encoding="utf-8", errors="replace")
    doc = ScriptDoctor(use_learning=False, genre=a.genre)
    stc = doc.analyze_save_the_cat(txt)
    out = {"beats":[b.__dict__ for b in stc.beats], "missing_beats": stc.missing_beats, "structure_score": stc.structure_score, "notes": stc.notes}
    print(json.dumps(out, ensure_ascii=False, indent=2))

def cmd_doctor_coach(a):
    txt = Path(a.file).read_text(encoding="utf-8", errors="replace")
    coach = DoctorCoach(genre=a.genre, theory_dir=a.theory, ollama_model=a.model, endpoint=a.endpoint)
    plan, rew = coach.coach(txt, screenplay_name=Path(a.file).stem, out_path=a.out if a.out else None)
    print(json.dumps({"plan": {"structure": plan.structure, "character": plan.character, "rhythm": plan.rhythm, "dialogue": plan.dialogue, "visuals": plan.visuals, "custom": plan.custom}, "rewritten": bool(rew)}, ensure_ascii=False, indent=2))

def cmd_learning_recommend(a):
    txt = Path(a.file).read_text(encoding="utf-8", errors="replace")
    doc = ScriptDoctor(use_learning=False, genre=a.genre)
    stc = doc.analyze_save_the_cat(txt)
    ll = Learning()
    tips = ll.recommend_for({"beats":[b.__dict__ for b in stc.beats], "dialogue_ratio":0.0, "pacing_score":0.0})
    print(json.dumps(tips, ensure_ascii=False, indent=2))

def cmd_theory_index(a):
    tc = TheoryComparator(Path(a.dir))
    n = tc.build()
    print(json.dumps({"indexed": n}, ensure_ascii=False, indent=2))

def cmd_theory_compare(a):
    tc = TheoryComparator(Path(a.dir))
    tc.build()
    hits = tc.compare(a.query, k=a.top_k)
    print(json.dumps([h.__dict__ for h in hits], ensure_ascii=False, indent=2))

def cmd_train_protos(a):
    labeled = {}
    for spec in a.spec:
        if "=" not in spec: continue
        label, file = spec.split("=",1)
        labeled.setdefault(label, []).append(Path(file).read_text(encoding="utf-8", errors="replace")[:4000])
    model = ProtoTrainer().fit(labeled)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    model.save(out)
    print(json.dumps({"saved": str(out)}, ensure_ascii=False))

def cmd_chat(a):
    cfg = ChatConfig(model=a.model, endpoint=a.endpoint, theory_dir=a.theory)
    ScripturemonChat(cfg, genre=a.genre).chat_loop()

def cmd_tags(a):
    txt = Path(a.file).read_text(encoding="utf-8", errors="replace")
    tags = [t.__dict__ for t in AutoTagger().tag_script(txt)]
    print(json.dumps(tags, ensure_ascii=False, indent=2))

def cmd_frameworks(a):
    txt = Path(a.file).read_text(encoding="utf-8", errors="replace")
    out = {"three_act": [f.__dict__ for f in three_act(txt)["three_act"]], "story_circle": [f.__dict__ for f in story_circle(txt)["story_circle"]]}
    print(json.dumps(out, ensure_ascii=False, indent=2))

def cmd_mine(a):
    miner = PatternMiner()
    texts = []
    p = Path(a.path)
    if p.is_dir():
        for f in p.rglob("*.txt"): texts.append(f.read_text(encoding="utf-8", errors="replace"))
    else:
        texts.append(p.read_text(encoding="utf-8", errors="replace"))
    colls = []
    for tx in texts: colls.extend([c.__dict__ for c in miner.collocations(tx, min_freq=2)])
    print(json.dumps({"patterns": colls[:50]}, ensure_ascii=False, indent=2))

def cmd_persona(a):
    m = AuthorModel(); m.note(a.text); print(json.dumps({"persona_updated": True}, ensure_ascii=False))

def build_parser():
    p = argparse.ArgumentParser(prog="scripturemon")
    s = p.add_subparsers()

    sp = s.add_parser("status"); sp.set_defaults(func=cmd_status)

    d = s.add_parser("doctor"); sd = d.add_subparsers()
    da = sd.add_parser("analyze"); da.add_argument("file"); da.add_argument("--genre", default="generic"); da.set_defaults(func=cmd_doctor_analyze)
    ds = sd.add_parser("stc"); ds.add_argument("file"); ds.add_argument("--genre", default="generic"); ds.set_defaults(func=cmd_doctor_stc)
    dcoach = sd.add_parser("coach"); dcoach.add_argument("file"); dcoach.add_argument("--genre", default="generic"); dcoach.add_argument("--model", default="llama3.1:8b"); dcoach.add_argument("--endpoint", default="http://127.0.0.1:11434/api/generate"); dcoach.add_argument("--theory", default="data/theory"); dcoach.add_argument("--out", default=""); dcoach.set_defaults(func=cmd_doctor_coach)

    lr = s.add_parser("learning"); lrs = lr.add_subparsers()
    lrec = lrs.add_parser("recommend"); lrec.add_argument("file"); lrec.add_argument("--genre", default="generic"); lrec.set_defaults(func=cmd_learning_recommend)

    th = s.add_parser("theory"); ths = th.add_subparsers()
    thi = ths.add_parser("index"); thi.add_argument("--dir", default="data/theory"); thi.set_defaults(func=cmd_theory_index)
    thc = ths.add_parser("compare"); thc.add_argument("--dir", default="data/theory"); thc.add_argument("--query", required=True); thc.add_argument("--top-k", dest="top_k", type=int, default=5); thc.set_defaults(func=cmd_theory_compare)

    tr = s.add_parser("train"); trs = tr.add_subparsers()
    tp = trs.add_parser("protos"); tp.add_argument("--spec", nargs="+", help="label=path ...", required=True); tp.add_argument("--out", default="data/training/prototypes.json"); tp.set_defaults(func=cmd_train_protos)

    ch = s.add_parser("chat"); ch.add_argument("--model", default="llama3.1:8b"); ch.add_argument("--endpoint", default="http://127.0.0.1:11434/api/generate"); ch.add_argument("--theory", default="data/theory"); ch.add_argument("--genre", default="generic"); ch.set_defaults(func=cmd_chat)

    tg = s.add_parser("tags"); tg.add_argument("file"); tg.set_defaults(func=cmd_tags)
    fw = s.add_parser("frameworks"); fw.add_argument("file"); fw.set_defaults(func=cmd_frameworks)
    mn = s.add_parser("mine"); mn.add_argument("path"); mn.set_defaults(func=cmd_mine)
    ps = s.add_parser("persona"); ps.add_argument("text"); ps.set_defaults(func=cmd_persona)

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    if not argv:
        parser.print_help(); return 0
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help(); return 2
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
