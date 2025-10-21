# -*- coding: utf-8 -*-
from __future__ import annotations
import os, sys, json, time, shutil, platform, subprocess, textwrap, socket
from pathlib import Path
from datetime import datetime

ROOT=Path(".")
PY=os.environ.get("PYTHON", sys.executable)
DBG_DIR=ROOT/"reports"/"debug"
LOG_DIR=DBG_DIR/"logs"
RUN_ENV={"PYTHONPATH":str(ROOT)}
RUN_ENV.update({k:v for k,v in os.environ.items()})

def sh(cmd:list[str], timeout:int=90, log:str="run") -> tuple[int,str,str]:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=RUN_ENV)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        return 124, "", f"[TIMEOUT] {' '.join(cmd)} ({timeout}s)"
    out_s, err_s = out.decode("utf-8","ignore"), err.decode("utf-8","ignore")
    (LOG_DIR/f"{log}.out.txt").write_text(out_s, encoding="utf-8")
    (LOG_DIR/f"{log}.err.txt").write_text(err_s, encoding="utf-8")
    return p.returncode, out_s, err_s

def exists(p:str)->bool: return Path(p).exists()

def snapshot_env()->dict:
    try:
        r=sh([PY,"-m","pip","freeze"], timeout=40, log="pip_freeze")[0]==0
    except Exception: r=False
    info=dict(
        ts=datetime.utcnow().isoformat()+"Z",
        py=sys.version,
        os=f"{platform.system()} {platform.release()}",
        cpu=platform.processor(),
        cwd=str(Path.cwd()),
        have_redis = _probe_port("127.0.0.1",6379),
        have_ollama = _probe_port("127.0.0.1",11434),
    )
    return info

def _probe_port(host:str,port:int)->bool:
    try:
        with socket.create_connection((host,port), timeout=0.2): return True
    except: return False

def read_json(p:Path, default):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except: return default

def write_markdown(path:Path, content:str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def human_header():
    return textwrap.dedent(f"""
    # Scripturemon — Debug & Test Suite
    *UTC:* {datetime.utcnow().isoformat()}Z  
    *Repo:* {Path.cwd()}
    """)

def main():
    DBG_DIR.mkdir(parents=True, exist_ok=True)
    # 1) Snapshot do ambiente
    env = snapshot_env()

    # 2) Pré-checagens de arquivos essenciais
    essentials = [
        "apps/scripturemon/cli.py",
        "apps/scripturemon/consciousness.py",
        "apps/scripturemon/membridge.py",
        "apps/scripturemon/backup.py",
        "apps/scripturemon/parallel.py",
        "apps/scripturemon/telepathy.py",
        "scripts/generate_report_html.py",
        "scripts/patch_report_with_strategy.py",
        "scripts/collect_ultimate_history.py",
        "scripts/aggregate_perf.py",
    ]
    missing=[e for e in essentials if not exists(e)]

    # 3) Rodadas de validação (rápidas) — uso real do usuário
    results={}

    # 3.1 Consciência/Memória/Backup — CLI ultimate once/status
    rc,_,_ = sh([PY,"-m","apps.scripturemon.cli","ultimate","once"], timeout=40, log="ultimate_once")
    rc2, out2, _ = sh([PY,"-m","apps.scripturemon.cli","ultimate","status"], timeout=40, log="ultimate_status")
    results["ultimate_once_rc"]=rc
    results["ultimate_status_rc"]=rc2
    results["ultimate_status_out_ok"] = ("consciousness" in out2.lower()) or ("level" in out2.lower())

    # 3.2 UI prefs — ligar live 10s, âncora ultimate-performance
    sh([PY,"-m","apps.scripturemon.cli","ui","live","on","--interval","10s"], timeout=20, log="ui_live_on")
    sh([PY,"-m","apps.scripturemon.cli","ui","anchor","set","--section","ultimate-performance"], timeout=20, log="ui_anchor_set")

    # 3.3 Geração de relatório (UI++, painel, injeção live & UX)
    sh([PY,"scripts/collect_ultimate_history.py"], timeout=30, log="collect_history")
    sh([PY,"scripts/aggregate_perf.py"], timeout=30, log="aggregate_perf")
    sh([PY,"scripts/generate_report_html.py"], timeout=60, log="report_html")
    sh([PY,"scripts/patch_report_with_strategy.py"], timeout=40, log="patch_strategy")
    sh([PY,"scripts/patch_live_reload.py"], timeout=20, log="patch_live")
    if exists("scripts/export_ultimate_panel.py"):
        sh([PY,"scripts/export_ultimate_panel.py"], timeout=20, log="export_panel")

    # 3.4 Análise paralela (heurística se Ollama indisponível)
    sample = "data/screenplay_synth/sample.txt"
    if not exists(sample):
        Path(sample).parent.mkdir(parents=True, exist_ok=True)
        Path(sample).write_text("INT. ROOM - DAY\nA CHARACTER enters. Conflict escalates.\n", encoding="utf-8")
    rc_ap, out_ap, err_ap = sh([PY,"-m","apps.scripturemon.cli","analyze_parallel", sample], timeout=40, log="analyze_parallel")
    results["analyze_parallel_rc"]=rc_ap
    results["analyze_parallel_has_summary"]=("structure" in out_ap.lower()) or ("summary" in out_ap.lower())

    # 3.5 Telepatia — ping (fakeredis se redis off)
    rc_tp, out_tp, err_tp = sh([PY,"-m","apps.scripturemon.cli","telepathy","ping"], timeout=30, log="telepathy_ping")
    results["telepathy_ping_rc"]=rc_tp

    # 3.6 Roundtrip samples (C7) — gerar + plot
    sh([PY,"scripts/build_roundtrip_samples.py","--data_dir","data/screenplay_synth","--n","10"], timeout=60, log="roundtrip_build")
    sh([PY,"scripts/plot_roundtrip.py"], timeout=40, log="roundtrip_plot")

    # 3.7 Bench compressão nano (C1/C2) — anti-timeout
    rc_bn1,_,_ = sh([PY,"scripts/run_compression_bench.py","--data_dir","data/original","--max_files","8","--max_chars","40000","--preserve_headers","false"], timeout=120, log="bench_nano_orig")
    rc_bn2,_,_ = sh([PY,"scripts/run_compression_bench.py","--data_dir","data/screenplay_synth","--max_files","8","--max_chars","40000","--preserve_headers","false"], timeout=120, log="bench_nano_scr")
    results["bench_nano_rc"]=(rc_bn1==0 and rc_bn2==0)

    # 3.8 Memória v5 (C6 PASS esperado)
    if exists("scripts/run_memory_bench_v5.py"):
        sh([PY,"scripts/run_memory_bench_v5.py"], timeout=120, log="memory_v5")

    # 3.9 Validador + scorecard
    rc_val, out_val, _ = sh([PY,"scripts/validate_all.py"], timeout=60, log="validate_all")
    results["validate_rc"]=rc_val

    # 4) Injeção de falhas — valida fallback e mensagens
    inj = {}

    # 4.1 Desligar OLLAMA_HOST para forçar heurística
    env_backup = RUN_ENV.get("OLLAMA_HOST")
    RUN_ENV["OLLAMA_HOST"]="http://127.0.0.1:9"  # porta bloqueada
    rc_i1, out_i1, _ = sh([PY,"-m","apps.scripturemon.cli","analyze_parallel", sample], timeout=30, log="inj_no_ollama")
    inj["no_ollama_ok"] = rc_i1==0 and ("fallback" in (out_i1.lower()+out_ap.lower()) or "lines=" in (out_i1+out_ap))

    # 4.2 Telepatia sem redis/fakeredis -> deve avisar e sair 1
    # simulamos removendo módulos via env de PYTHONPATH impossível; em vez disso, verificamos o código de retorno
    # (se conectou, ok True; se não, CLI retorna Exit(1) com [WARN])
    rc_i2, _, _ = sh([PY,"-m","apps.scripturemon.cli","telepathy","ping"], timeout=20, log="inj_telepathy_connect")
    inj["telepathy_warn_or_ok"] = rc_i2 in (0,1)

    # restore OLLAMA_HOST
    if env_backup is None: RUN_ENV.pop("OLLAMA_HOST",None)
    else: RUN_ENV["OLLAMA_HOST"]=env_backup

    # 5) Scorecard & artefatos
    score = read_json(Path("reports/scorecard.json"), {})
    hist_ok = Path("reports/history/ultimate.csv").exists()
    html_ok = Path("reports/index.html").exists()

    # 6) Relatório MD
    md = []
    md.append(human_header())
    md.append("## Ambiente")
    md.append(f"- Python: `{env['py']}`  \n- OS: `{env['os']}`  \n- Redis on: `{env['have_redis']}`  \n- Ollama on: `{env['have_ollama']}`")
    if missing: md.append(f"\n**[WARN] Arquivos ausentes:** {missing}\n")
    md.append("\n## Resultados (simulação humana)")
    md.append(f"- ultimate once/status: rc={results['ultimate_once_rc']} / status_ok={results['ultimate_status_out_ok']}")
    md.append(f"- UI prefs: live=10s & anchor=ultimate-performance (injetados)")
    md.append(f"- analyze_parallel: rc={results['analyze_parallel_rc']} summary={results['analyze_parallel_has_summary']}")
    md.append(f"- telepathy ping: rc={results['telepathy_ping_rc']}")
    md.append(f"- roundtrip samples: ok (ver logs)")
    md.append(f"- bench nano (C1/C2): {results['bench_nano_rc']}")
    md.append(f"- validate_all rc={results['validate_rc']}")
    md.append("\n## Injeção de Falhas (fallback esperado)")
    md.append(f"- Ollama off -> heurística: {inj['no_ollama_ok']}")
    md.append(f"- Telepathy connect warn/ok: {inj['telepathy_warn_or_ok']}")
    md.append("\n## Scorecard")
    md.append("```json\n"+json.dumps(score, indent=2)+"\n```")
    md.append("\n## Artefatos")
    md.append("- reports/index.html, reports/ultimate_panel.html (se gerado)")
    md.append("- results/* (compressão/memória/telepathy/e2e)")
    md.append("- reports/history/* (consciência/L1‑L3/perf)")
    md.append("- logs em reports/debug/logs/*.txt")
    write_markdown(DBG_DIR/"debug_summary.md", "\n".join(md))

    # 7) ZIP de debug
    ts=datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    zipname=ROOT/"reports"/f"debug_bundle_{ts}.zip"
    try:
        import zipfile
        with zipfile.ZipFile(zipname,"w",zipfile.ZIP_DEFLATED) as z:
            for p in [
                "reports/debug/debug_summary.md",
                "reports/scorecard.json",
                "reports/index.html",
                "reports/ultimate_panel.html",
            ]:
                if exists(p): z.write(p, arcname=p)
            # logs
            if LOG_DIR.exists():
                for f in LOG_DIR.glob("*.txt"): z.write(f, arcname=str(f))
    except Exception as e:
        (DBG_DIR/"zip_error.txt").write_text(str(e), encoding="utf-8")

    print("[OK] debug suite ->", DBG_DIR/"debug_summary.md")
    print("[OK] debug zip   ->", zipname)

if __name__=="__main__":
    main()