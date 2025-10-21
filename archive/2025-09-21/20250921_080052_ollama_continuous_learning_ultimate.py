
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Continuous Learning — ULTIMATE
-------------------------------------
Sistema de aprendizado contínuo, crítico e cumulativo para roteiros + teoria.
Compatível com Scripturemon (Doctor/Learning/RAG/Miner/AutoTag).

Princípios:
- stdlib-first (+ requests opcional para Ollama);
- Persistência robusta (SQLite WAL) + snapshots na Memória Unificada (se existir);
- Geração de insights verificáveis (JSON), self-critique e consolidação incremental;
- Indexação RAG dos insights e patterns para recuperação futura;
- CLI com subcomandos (run/report/index-theory/migrate).
"""

from __future__ import annotations

import argparse, contextlib, dataclasses, hashlib, json, logging, os, re, sqlite3, sys, time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger("scripturemon.continuous")
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
LOG.addHandler(_handler); LOG.setLevel(logging.INFO)

try:
    import requests  # type: ignore
except Exception:
    requests = None

if (Path("src") / "scripturemon_champion").exists() and str(Path("src")) not in sys.path:
    sys.path.insert(0, str(Path("src")))

ScriptDoctorT = Any
LearningT = Any

def _import_doctor_and_learning():
    global ScriptDoctorT, LearningT
    for cand in (
        "scripturemon_champion.script_doctor_enhanced:ScriptDoctorEnhanced",
        "scripturemon_champion.script_doctor:ScriptDoctor",
        "scripturemon_champion.analysis.script_doctor:ScriptDoctor",
    ):
        pkg, cls = cand.split(":")
        with contextlib.suppress(Exception):
            mod = __import__(pkg, fromlist=[cls]); ScriptDoctorT = getattr(mod, cls); break
    for cand in (
        "scripturemon_champion.learning:Learning",
        "scripturemon_champion.learning:LearningLite",
    ):
        pkg, cls = cand.split(":")
        with contextlib.suppress(Exception):
            mod = __import__(pkg, fromlist=[cls]); LearningT = getattr(mod, cls); break
_import_doctor_and_learning()

RAG=None
with contextlib.suppress(Exception):
    import scripturemon_champion.rag_bm25 as RAG  # type: ignore
PatternMiner=None; AutoTagger=None
with contextlib.suppress(Exception):
    from scripturemon_champion.miner import PatternMiner  # type: ignore
with contextlib.suppress(Exception):
    from scripturemon_champion.autotag import AutoTagger  # type: ignore
UnifiedMemory=None; MemoryRecord=None
with contextlib.suppress(Exception):
    from scripturemon_champion.memory import get_unified_memory, MemoryRecord  # type: ignore
    UnifiedMemory=get_unified_memory()

def now_iso()->str: return datetime.now().isoformat(timespec="seconds")
def sha1(s:str)->str: import hashlib; return hashlib.sha1(s.encode("utf-8")).hexdigest()
def short(s:str,n:int=220)->str:
    s=(s or "").strip().replace("\r"," ")
    return (s[:n-1]+"…") if len(s)>n else s
JSON_PAT=re.compile(r"\{.*\}", re.S)
def extract_json(blob:str)->Optional[dict]:
    if not blob: return None
    try:
        b=re.sub(r"^```(json)?\s*|\s*```$","",blob.strip(),flags=re.I)
        if b.strip().startswith("{") and b.strip().endswith("}"):
            return json.loads(b)
    except Exception: pass
    m=JSON_PAT.search(blob or ""); 
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

@dataclass
class OllamaCfg:
    model:str="llama3.1:8b"; endpoint:str="http://127.0.0.1:11434"; timeout:int=60; temperature:float=0.5; top_p:float=0.9; embed_model:str="nomic-embed-text"
class Ollama:
    def __init__(self, cfg:OllamaCfg=OllamaCfg()):
        self.cfg=cfg; self._session = requests.Session() if requests else None
    def generate(self, prompt:str, **kw)->Optional[str]:
        if not requests: return prompt[::-1]
        url=f"{self.cfg.endpoint}/api/generate"
        payload={"model":self.cfg.model,"prompt":prompt,"stream":False,"options":{"temperature":float(kw.get("temperature",self.cfg.temperature)),"top_p":float(kw.get("top_p",self.cfg.top_p))}}
        try:
            r=(self._session or requests).post(url,json=payload,timeout=int(kw.get("timeout",self.cfg.timeout)))
            if r.status_code==200:
                j=r.json(); return j.get("response") or j.get("completion") or ""
        except Exception as e:
            LOG.warning("Erro Ollama: %s", e)
        return None
    def embed(self, texts:List[str])->List[List[float]]:
        if not requests:
            return [self._hash_embed(t) for t in texts]
        url=f"{self.cfg.endpoint}/api/embeddings"; out=[]
        for t in texts:
            try:
                r=(self._session or requests).post(url,json={"model":self.cfg.embed_model,"prompt":t},timeout=self.cfg.timeout)
                vec=r.json().get("embedding",[]); 
                if not isinstance(vec,list) or not vec: vec=self._hash_embed(t)
            except Exception: vec=self._hash_embed(t)
            out.append(vec)
        return out
    @staticmethod
    def _hash_embed(text:str, dim:int=256)->List[float]:
        import hashlib
        h=hashlib.sha256(text.encode("utf-8")).digest()
        arr=[x/255.0 for x in h[:min(dim,len(h))]]; 
        if len(arr)<dim: arr += [0.0]*(dim-len(arr))
        return arr

class KnowledgeDB:
    def __init__(self, path:Path):
        self.path=Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn=sqlite3.connect(str(self.path))
        self._conn.execute("PRAGMA journal_mode=WAL;"); self._conn.execute("PRAGMA foreign_keys=ON;")
        self._ensure_schema()
    def _ensure_schema(self):
        c=self._conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS learning_cycles(
            cycle_id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, phase TEXT, insights_count INTEGER DEFAULT 0, patterns_found INTEGER DEFAULT 0, notes TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS insights(
            insight_id INTEGER PRIMARY KEY AUTOINCREMENT, cycle_id INTEGER, type TEXT, key_hash TEXT UNIQUE,
            screenplay TEXT, theory TEXT, content TEXT, confidence REAL, timestamp TEXT,
            FOREIGN KEY(cycle_id) REFERENCES learning_cycles(cycle_id) ON DELETE CASCADE)""")
        c.execute("""CREATE TABLE IF NOT EXISTS patterns(
            pattern_id INTEGER PRIMARY KEY AUTOINCREMENT, key_hash TEXT UNIQUE, pattern_type TEXT, description TEXT,
            occurrences INTEGER DEFAULT 1, examples TEXT DEFAULT '[]', score REAL DEFAULT 0.0, first_seen_cycle INTEGER, last_seen_cycle INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS screenplay_comparisons(
            comparison_id INTEGER PRIMARY KEY AUTOINCREMENT, screenplay1 TEXT, screenplay2 TEXT, similarity_score REAL,
            common_elements TEXT, differences TEXT, insight TEXT, cycle_id INTEGER)""")
        c.execute("CREATE INDEX IF NOT EXISTS idx_insights_cycle ON insights(cycle_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_patterns_last ON patterns(last_seen_cycle)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_comp_cycle ON screenplay_comparisons(cycle_id)")
        self._conn.commit()
    def begin_cycle(self)->int:
        c=self._conn.cursor(); c.execute("INSERT INTO learning_cycles(timestamp,phase) VALUES(?,?)",(now_iso(),"start")); self._conn.commit(); return c.lastrowid
    def complete_cycle(self, cycle_id:int, insights_count:int, patterns_found:int, notes:str="")->None:
        c=self._conn.cursor(); c.execute("UPDATE learning_cycles SET phase='complete', insights_count=?, patterns_found=?, timestamp=?, notes=? WHERE cycle_id=?",
                                         (int(insights_count), int(patterns_found), now_iso(), notes, int(cycle_id))); self._conn.commit()
    def upsert_insight(self, cycle_id:int, insight_type:str, payload:dict, confidence:float, screenplay:str="", theory:str="")->bool:
        key=sha1(json.dumps({"type":insight_type,"screenplay":screenplay,"theory":theory,"payload":payload}, ensure_ascii=False, sort_keys=True))
        c=self._conn.cursor()
        try:
            c.execute("""INSERT INTO insights(cycle_id,type,key_hash,screenplay,theory,content,confidence,timestamp)
                         VALUES(?,?,?,?,?,?,?,?)""",(int(cycle_id),insight_type,key,screenplay,theory,json.dumps(payload,ensure_ascii=False),float(confidence),now_iso()))
            self._conn.commit(); return True
        except sqlite3.IntegrityError:
            c.execute("UPDATE insights SET confidence=MIN(1.0,confidence+?) WHERE key_hash=?", (min(0.1,max(0.01,confidence*0.05)), key))
            self._conn.commit(); return False
    def upsert_pattern(self, pattern_type:str, description:str, examples:Optional[List[str]], cycle_id:int, score:float=0.0)->None:
        key=sha1(f"{pattern_type}|{description}"); c=self._conn.cursor(); c.execute("SELECT pattern_id,occurrences FROM patterns WHERE key_hash=?", (key,)); row=c.fetchone()
        if row:
            pid,occ=row; c.execute("UPDATE patterns SET occurrences=?, last_seen_cycle=?, score=? WHERE pattern_id=?",(int(occ)+1,int(cycle_id),float(score),int(pid)))
        else:
            c.execute("""INSERT INTO patterns(key_hash,pattern_type,description,occurrences,examples,score,first_seen_cycle,last_seen_cycle)
                         VALUES(?,?,?,?,?,?,?,?)""",(key,pattern_type,description.strip(),1,json.dumps(examples or [], ensure_ascii=False),float(score),int(cycle_id),int(cycle_id)))
        self._conn.commit()
    def add_comparison(self, cycle_id:int, comp:dict)->None:
        c=self._conn.cursor()
        c.execute("""INSERT INTO screenplay_comparisons(screenplay1,screenplay2,similarity_score,common_elements,differences,insight,cycle_id)
                     VALUES(?,?,?,?,?,?,?)""",(comp.get("screenplay1",""),comp.get("screenplay2",""),float(comp.get("similarity",0.0)),
                                               json.dumps(comp.get("common",[]),ensure_ascii=False), json.dumps(comp.get("differences",[]),ensure_ascii=False),
                                               comp.get("insight",""), int(cycle_id)))
        self._conn.commit()
    def top_patterns(self, limit:int=10)->List[Tuple[str,int,str,float]]:
        c=self._conn.cursor(); c.execute("SELECT description,occurrences,pattern_type,score FROM patterns ORDER BY occurrences DESC, score DESC LIMIT ?", (int(limit),))
        return list(c.fetchall())
    def last_cycles(self, limit:int=5)->List[Tuple[int,int,int,str]]:
        c=self._conn.cursor(); c.execute("SELECT cycle_id,insights_count,patterns_found,timestamp FROM learning_cycles ORDER BY cycle_id DESC LIMIT ?", (int(limit),))
        return list(c.fetchall())
    def stats(self)->Dict[str,int]:
        c=self._conn.cursor(); out={}
        for name,table in (("insights","insights"),("patterns","patterns"),("comparisons","screenplay_comparisons")):
            c.execute(f"SELECT COUNT(*) FROM {table}"); out[name]=int(c.fetchone()[0])
        return out

def rag_index(doc_id:str, text:str, meta:Optional[dict]=None):
    if not RAG: return
    try: RAG.index_document(doc_id, text, meta or {})
    except Exception: pass

@dataclass
class CLConfig:
    model:str="llama3.1:8b"; embed_model:str="nomic-embed-text"; endpoint:str="http://127.0.0.1:11434"
    theory_dir:str="data/theory"; screenplays_dir:str="screenplays"; my_screenplays_dir:str="my_screenplays"
    db_path:str="data/learning/ollama_knowledge.db"; genre:str="generic"; sleep_between_cycles:int=30
    top_k_theories:int=4; top_k_screenplays:int=6; max_pairs_per_cycle:int=8
    use_ollama:bool=True; use_learning_bridge:bool=True

class OllamaContinuousLearningPro:
    def __init__(self, cfg:CLConfig=CLConfig()):
        self.cfg=cfg; self.db=KnowledgeDB(Path(self.cfg.db_path))
        self.ollama = Ollama(OllamaCfg(model=self.cfg.model, endpoint=self.cfg.endpoint, embed_model=self.cfg.embed_model)) if self.cfg.use_ollama else None
        self.doctor = ScriptDoctorT(use_learning=True, genre=self.cfg.genre) if ScriptDoctorT else None
        self.learning = LearningT() if LearningT else None
        self.miner = PatternMiner() if PatternMiner else None
        self.tagger = AutoTagger() if AutoTagger else None
    def _collect_files(self)->Tuple[List[Path],List[Path]]:
        sps=[]; my=Path(self.cfg.my_screenplays_dir); sp=Path(self.cfg.screenplays_dir)
        if my.exists(): sps.extend(my.glob("*.txt"))
        if sp.exists(): sps.extend(sp.glob("*.txt"))
        ths=[]; td=Path(self.cfg.theory_dir); 
        if td.exists(): ths=list(td.glob("*.txt"))
        LOG.info("Arquivos: %d roteiros, %d teorias", len(sps), len(ths)); return sps, ths
    def _prior_knowledge_text(self)->str:
        parts=["CONHECIMENTO ACUMULADO:\n"]
        for desc,occ,ptype,score in self.db.top_patterns(limit=6):
            parts.append(f"• [{ptype}] {desc} (visto {occ}x; score={score:.2f})")
        if self.learning:
            with contextlib.suppress(Exception):
                st=self.learning.get_statistics(); parts.append(f"\nLearning: total={st.get('total_concepts',0)}, avg_conf={st.get('avg_confidence',0.0):.2f}")
        return "\n".join(parts).strip()
    def phase1_theory_analysis(self, cycle_id:int, screenplays:List[Path], theories:List[Path])->List[dict]:
        LOG.info("FASE 1 — análise teórica (ciclo %d)", cycle_id)
        prior=self._prior_knowledge_text(); out=[]; pick_sps=screenplays[:max(1,min(len(screenplays), self.cfg.top_k_screenplays))]
        pick_theo=theories[:max(1,min(len(theories), self.cfg.top_k_theories))]
        for sp in pick_sps:
            text=sp.read_text(encoding="utf-8", errors="ignore")
            analysis=None
            if self.doctor:
                with contextlib.suppress(Exception):
                    analysis=self.doctor.analyze_script(text, sp.stem)
            for th in pick_theo:
                thext=th.read_text(encoding="utf-8", errors="ignore")[:2000]
                prompt=f"""{prior}

ROTEIRO: {sp.stem}
TEORIA: {th.stem}

Contexto do roteiro:
- cenas={getattr(analysis,'scenes',0)}, diálogo={getattr(analysis,'dialogue_ratio',0.0):.1%}, top_chars={getattr(analysis,'top_characters',[])[:3]}

Trecho de teoria (amostra):
{thext}

Tarefa: avalie a aderência da teoria ao roteiro e produza 1 insight específico e 1 padrão observado.
Responda em JSON com as chaves: adherence (0-1), insight (str), pattern (str)."""
                resp=self.ollama.generate(prompt, temperature=0.5) if self.ollama else None
                data=extract_json(resp or ""); 
                if not data: continue
                ins={"screenplay":sp.stem,"theory":th.stem,"adherence":float(data.get("adherence",0.5)),"insight":str(data.get("insight","")).strip(),"pattern":str(data.get("pattern","")).strip()}
                out.append(ins); self.db.upsert_insight(cycle_id, "theory_analysis", ins, confidence=ins["adherence"], screenplay=sp.stem, theory=th.stem)
                rag_index(f"cl:insight:{sha1(sp.stem+th.stem+ins['insight'])}", f"{sp.stem} vs {th.stem}\n{ins['insight']}\n{ins['pattern']}", {"type":"insight","screenplay":sp.stem,"theory":th.stem,"adherence":ins["adherence"]})
                time.sleep(0.2)
        return out
    def _cos(self,a:List[float],b:List[float])->float:
        n=min(len(a),len(b)); 
        if n==0: return 0.0
        dot=sum(a[i]*b[i] for i in range(n)); na=sum(a[i]*a[i] for i in range(n))**0.5; nb=sum(b[i]*b[i] for i in range(n))**0.5
        return (dot/(na*nb)) if na>0 and nb>0 else 0.0
    def phase2_screenplay_comparison(self, cycle_id:int, screenplays:List[Path])->List[dict]:
        LOG.info("FASE 2 — comparação entre roteiros (ciclo %d)", cycle_id)
        out=[]; picks=screenplays[:max(2,min(len(screenplays), self.cfg.top_k_screenplays))]
        texts=[p.read_text(encoding="utf-8", errors="ignore") for p in picks]; titles=[p.stem for p in picks]
        vecs=self.ollama.embed([t[:1200] for t in texts]) if self.ollama else [[0.0]*32 for _ in texts]
        pairs=0
        for i in range(len(picks)-1):
            for j in range(i+1,len(picks)):
                if pairs>=self.cfg.max_pairs_per_cycle: break
                sim=self._cos(vecs[i],vecs[j]); a1=a2=None
                if self.doctor:
                    with contextlib.suppress(Exception):
                        a1=self.doctor.analyze_script(texts[i], titles[i]); a2=self.doctor.analyze_script(texts[j], titles[j])
                prompt=f"""Contexto:
Roteiro 1: {titles[i]} — scenes={getattr(a1,'scenes',0)}, dialogue={getattr(a1,'dialogue_ratio',0.0):.1%}
Roteiro 2: {titles[j]} — scenes={getattr(a2,'scenes',0)}, dialogue={getattr(a2,'dialogue_ratio',0.0):.1%}

Explique brevemente (JSON) os principais elementos em comum e as diferenças-chave (2-4 itens cada).
Formato: {{"common_elements": [...], "key_differences": [...], "unique_insight": "..."}}"""
                data=extract_json(self.ollama.generate(prompt, temperature=0.6) or "") if self.ollama else {}
                comp={"screenplay1":titles[i],"screenplay2":titles[j],"similarity":float(sim),"common":data.get("common_elements",[]),"differences":data.get("key_differences",[]),"insight":data.get("unique_insight","")}
                out.append(comp); pairs+=1; self.db.add_comparison(cycle_id, comp)
                if comp["insight"]:
                    rag_index(f"cl:comp:{sha1(comp['screenplay1']+comp['screenplay2']+comp['insight'])}", f"{comp['screenplay1']} ↔ {comp['screenplay2']}\n{comp['insight']}", {"type":"comparison","sim":comp["similarity"]})
        return out
    def phase3_pattern_extraction(self, cycle_id:int, insights:List[dict], comparisons:List[dict])->Dict[str,Any]:
        LOG.info("FASE 3 — extração de padrões (ciclo %d)", cycle_id)
        prior=self._prior_knowledge_text()
        insights_summary="\n".join([f"• {short(i.get('insight',''))}" for i in insights if i.get('insight')])
        patterns_seen="\n".join([f"• {short(i.get('pattern',''))}" for i in insights if i.get('pattern')])
        comp_summary="\n".join([f"• {short(c.get('insight',''))}" for c in comparisons if c.get('insight')])
        prompt=f"""{prior}

INSIGHTS:
{insights_summary}

PADRÕES OBSERVADOS:
{patterns_seen}

INSIGHTS DE COMPARAÇÕES:
{comp_summary}

Produza JSON com:
{{"confirmed_patterns": [...], "new_discoveries": [...], "general_rules": [...], "evolution_insight": "..."}}
"""
        data=extract_json(self.ollama.generate(prompt, temperature=0.7) or "") if self.ollama else {}
        miner_patterns=[]
        if PatternMiner and (insights or comparisons):
            try:
                blobs=[i.get('insight','') for i in insights if i.get('insight')] + [c.get('insight','') for c in comparisons if c.get('insight')]
                if blobs:
                    joined="\n".join(blobs)
                    for p in PatternMiner().collocations(joined, min_freq=2)[:12]:
                        miner_patterns.append(getattr(p,'key',str(p)).replace("_"," "))
            except Exception: pass
        for kind, arr in (("confirmed", data.get("confirmed_patterns", [])),("discovery", data.get("new_discoveries", [])),("rule", data.get("general_rules", []))):
            for desc in arr or []:
                self.db.upsert_pattern(kind, str(desc).strip(), None, cycle_id, score=1.0 if kind=="rule" else 0.6)
        for mp in miner_patterns: self.db.upsert_pattern("collocation", mp, None, cycle_id, score=0.4)
        for desc in (data.get("confirmed_patterns", []) or []) + (data.get("new_discoveries", []) or []) + miner_patterns:
            rag_index(f"cl:pattern:{sha1(desc)}", desc, {"type":"pattern"})
        return data or {}
    def phase4_self_critique(self, cycle_id:int)->None:
        LOG.info("FASE 4 — self-critique (ciclo %d)", cycle_id)
        try:
            c=self.db._conn.cursor(); c.execute("SELECT key_hash,content,confidence FROM insights WHERE cycle_id=? ORDER BY insight_id DESC LIMIT 12", (int(cycle_id),))
            rows=c.fetchall()
            for key_hash,content,conf in rows:
                if not self.ollama: continue
                ans=self.ollama.generate(f"""Analise criticamente o seguinte insight (JSON abaixo). Retorne um único número 0..1 representando qualidade/precisão.\n\n{content}\n""", temperature=0.2, timeout=15) or "0.5"
                try:
                    import re; score=float(re.findall(r"[0-1](?:\.\d+)?", ans.strip())[0])
                except Exception: score=0.5
                new_conf=1.0-(1.0-float(conf))*(1.0-float(score))
                cc=self.db._conn.cursor(); cc.execute("UPDATE insights SET confidence=? WHERE key_hash=?", (float(max(0.0,min(1.0,new_conf))), key_hash))
            self.db._conn.commit()
        except Exception: pass
    def run_cycle(self)->None:
        sps,ths=self._collect_files(); cycle_id=self.db.begin_cycle(); LOG.info("Iniciando ciclo %d", cycle_id)
        insights=self.phase1_theory_analysis(cycle_id, sps, ths)
        comparisons=self.phase2_screenplay_comparison(cycle_id, sps)
        patt=self.phase3_pattern_extraction(cycle_id, insights, comparisons)
        self.phase4_self_critique(cycle_id)
        if UnifiedMemory and MemoryRecord:
            with contextlib.suppress(Exception):
                UnifiedMemory.store(MemoryRecord(type="continuous_learning", key=f"cycle:{cycle_id}", value={"cycle_id":cycle_id,"insights_last":len(insights),"patterns_added":len(patt.get("new_discoveries",[]))+len(patt.get("confirmed_patterns",[])),"ts":now_iso()}, metadata={"schema":1}))  # type: ignore
        stats=self.db.stats(); self.db.complete_cycle(cycle_id, insights_count=stats.get("insights",0), patterns_found=stats.get("patterns",0))
        LOG.info("Ciclo %d completo — insights=%s, patterns=%s", cycle_id, stats.get("insights",0), stats.get("patterns",0))
    def show_report(self)->None:
        LOG.info("RELATÓRIO DE EVOLUÇÃO")
        tops=self.db.top_patterns(10)
        if tops:
            print("\n🏆 TOP PADRÕES:")
            for i,(desc,occ,ptype,score) in enumerate(tops,1):
                print(f"  {i}. [{ptype}] {desc} — {occ}x (score={score:.2f})")
        cycles=self.db.last_cycles(5)
        if cycles:
            print("\n📈 ÚLTIMOS CICLOS:")
            for cid,ins,patt,ts in cycles:
                print(f"  ciclo {cid}: insights={ins}, patterns={patt} — {ts}")
        s=self.db.stats(); print("\n📊 TOTAIS:", s)
    def index_theory(self)->None:
        if not RAG: LOG.info("RAG não disponível"); return
        base=Path(self.cfg.theory_dir); 
        if not base.exists(): LOG.info("Diretório de teoria não encontrado: %s", base); return
        for p in base.glob("*.txt"):
            with contextlib.suppress(Exception):
                rag_index(f"theory:{p.name}", p.read_text(encoding="utf-8", errors="ignore"), {"type":"theory"})
        LOG.info("Teorias indexadas em RAG.")
    def migrate(self)->None: LOG.info("Migração OK (schema garantido).")

def build_parser()->argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="ollama-continual", description="Aprendizado contínuo evolutivo com Ollama + Scripturemon")
    sp=p.add_subparsers(dest="cmd")
    r=sp.add_parser("run", help="Executa um ciclo (ou N ciclos com --cycles)")
    r.add_argument("--cycles", type=int, default=1); r.add_argument("--model", default=CLConfig.model)
    r.add_argument("--endpoint", default=CLConfig.endpoint); r.add_argument("--genre", default=CLConfig.genre)
    r.add_argument("--sleep", type=int, default=CLConfig.sleep_between_cycles); r.add_argument("--theory", default=CLConfig.theory_dir)
    r.add_argument("--screenplays", default=CLConfig.screenplays_dir); r.add_argument("--my", default=CLConfig.my_screenplays_dir)
    r.add_argument("--db", default=CLConfig.db_path); r.add_argument("--no-ollama", action="store_true"); r.add_argument("--no-learning", action="store_true")
    sp.add_parser("report", help="Mostra relatório"); sp.add_parser("migrate", help="Garante schema no DB"); sp.add_parser("index-theory", help="Indexa data/theory em RAG")
    return p
def main(argv=None)->int:
    argv=argv or sys.argv[1:]; args=build_parser().parse_args(argv)
    if not args.cmd: build_parser().print_help(); return 0
    if args.cmd=="run":
        cfg=CLConfig(model=args.model, endpoint=args.endpoint, genre=args.genre, theory_dir=args.theory, screenplays_dir=args.screenplays, my_screenplays_dir=args.my, db_path=args.db, use_ollama=not args.no_ollama, use_learning_bridge=not args.no_learning)
        sys.setrecursionlimit(10_000); sys.setswitchinterval(0.005); system=OllamaContinuousLearningPro(cfg)
        cycles=max(1,int(args.cycles))
        for i in range(cycles):
            system.run_cycle()
            if i+1<cycles:
                LOG.info("Aguardando %s s...", system.cfg.sleep_between_cycles); time.sleep(system.cfg.sleep_between_cycles)
        return 0
    if args.cmd=="report": OllamaContinuousLearningPro(CLConfig()).show_report(); return 0
    if args.cmd=="migrate": OllamaContinuousLearningPro(CLConfig()).migrate(); return 0
    if args.cmd=="index-theory": OllamaContinuousLearningPro(CLConfig()).index_theory(); return 0
    return 2
if __name__=="__main__": raise SystemExit(main())
