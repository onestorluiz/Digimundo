from __future__ import annotations
import json
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
try:
    import requests
except Exception:
    requests = None

from .theory import TheoryComparator
from .script_doctor import ScriptDoctor
from ..learning import Learning
from .coach import DoctorCoach
from .autotag import AutoTagger
from .frameworks import three_act, story_circle
from .miner import PatternMiner
from .author import AuthorModel

@dataclass
class ChatConfig:
    model: str = "llama3.1:8b"
    endpoint: str = "http://127.0.0.1:11434/api/generate"
    timeout: int = 60
    theory_dir: str = "data/theory"

class ScripturemonChat:
    def __init__(self, cfg: ChatConfig = ChatConfig(), genre: str = "generic"):
        self.cfg = cfg
        self.doctor = ScriptDoctor(use_learning=True, genre=genre)
        self.learn = Learning()
        self.theory = TheoryComparator(Path(self.cfg.theory_dir))
        try: self.theory.build()
        except Exception: pass
        self.coach = DoctorCoach(genre=genre, theory_dir=self.cfg.theory_dir, ollama_model=self.cfg.model, endpoint=self.cfg.endpoint)
        self.tagger = AutoTagger()
        self.miner = PatternMiner()
        self.author = AuthorModel()

    def _ollama(self, prompt: str) -> str:
        if requests is None: return "(Ollama indisponível) " + prompt[::-1]
        try:
            r = requests.post(self.cfg.endpoint, json={"model": self.cfg.model, "prompt": prompt, "stream": False}, timeout=self.cfg.timeout)
            j = r.json()
            return j.get("response") or j.get("completion") or "(sem resposta)"
        except Exception as e:
            return f"(erro Ollama: {e})"

    def _format_context(self, user_text: str) -> str:
        rich = self.learn.enrich_prompt_pro("[USER PROMPT]", q=user_text, k_beats=3, k_arch=2, k_chars=2)
        hits = self.theory.compare(user_text, k=3) if self.theory else []
        if hits:
            frag = "\n".join([f"- {h.doc_id}: {h.excerpt[:200]}..." for h in hits])
            rich += "\n\n[THEORY]\n" + frag
        return rich

    def chat_loop(self):
        print("✨ Scripturemon Chat — /help para comandos, Ctrl+C para sair.")
        while True:
            try:
                inp = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nAté logo!"); break
            if not inp: continue
            if inp.startswith('/'):
                if inp in ("/quit","/exit"): break
                if inp == "/help":
                    print("Comandos: /analyze <arquivo>, /compare <arquivo>, /coach <arquivo>, /tags <arquivo>, /frameworks <arquivo>, /learn <arquivo>, /mine <dir>, /persona <texto>, /stats, /quit"); continue
                if inp.startswith("/analyze "):
                    path = inp.split(" ",1)[1].strip()
                    try:
                        txt = Path(path).read_text(encoding="utf-8", errors="replace")
                        sa = self.doctor.analyze_script(txt, screenplay_name=Path(path).stem)
                        print(json.dumps(sa.to_dict(), ensure_ascii=False, indent=2))
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/compare "):
                    path = inp.split(" ",1)[1].strip()
                    try:
                        txt = Path(path).read_text(encoding="utf-8", errors="replace")
                        stc = self.doctor.analyze_save_the_cat(txt)
                        tips = self.learn.recommend_for({"beats":[b.__dict__ for b in stc.beats], "pacing_score":0.0, "dialogue_ratio":0.0})
                        print("Sugestões:", json.dumps(tips, ensure_ascii=False, indent=2))
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/coach "):
                    path = inp.split(" ",1)[1].strip()
                    try:
                        txt = Path(path).read_text(encoding="utf-8", errors="replace")
                        plan, _ = self.coach.coach(txt, screenplay_name=Path(path).stem)
                        print(json.dumps({"plan": plan.__dict__}, ensure_ascii=False, indent=2))
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/tags "):
                    path = inp.split(" ",1)[1].strip()
                    try:
                        txt = Path(path).read_text(encoding="utf-8", errors="replace")
                        tags = [t.__dict__ for t in self.tagger.tag_script(txt)]
                        print(json.dumps({"tags": tags}, ensure_ascii=False, indent=2))
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/frameworks "):
                    path = inp.split(" ",1)[1].strip()
                    try:
                        txt = Path(path).read_text(encoding="utf-8", errors="replace")
                        out = {"three_act": [f.__dict__ for f in three_act(txt)["three_act"]], "story_circle": [f.__dict__ for f in story_circle(txt)["story_circle"]]}
                        print(json.dumps(out, ensure_ascii=False, indent=2))
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/learn "):
                    path = inp.split(" ",1)[1].strip()
                    try:
                        txt = Path(path).read_text(encoding="utf-8", errors="replace")
                        sa = self.doctor.analyze_script(txt, screenplay_name=Path(path).stem)
                        self.learn.learn_from_analysis(sa, Path(path).stem)
                        print("Aprendido com", path)
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/mine "):
                    p = inp.split(" ",1)[1].strip()
                    try:
                        pth = Path(p)
                        texts = []
                        if pth.is_dir():
                            for f in pth.rglob("*.txt"):
                                texts.append(f.read_text(encoding="utf-8", errors="replace"))
                        else:
                            texts.append(pth.read_text(encoding="utf-8", errors="replace"))
                        colls = []
                        for tx in texts:
                            colls.extend([c.__dict__ for c in self.miner.collocations(tx, min_freq=2)])
                        print(json.dumps({"patterns": colls[:50]}, ensure_ascii=False, indent=2))
                    except Exception as e: print("Erro:", e)
                    continue
                if inp.startswith("/persona "):
                    txt = inp.split(" ",1)[1].strip()
                    try:
                        self.author.note(txt); print("Persona atualizada.")
                    except Exception as e: print("Erro:", e)
                    continue
                if inp == "/stats":
                    print(json.dumps(self.learn.get_statistics(), ensure_ascii=False, indent=2)); continue

            ctx = self._format_context(inp)
            prompt = ('''You are Scripturemon, a unified Script Doctor and Learning system.
[CONTEXT]
''' + ctx + '''
[USER]
''' + inp + '''
[INSTRUCTIONS]
- Use Portuguese when the user speaks Portuguese.
- Analyze the user's idea or script; compare with theory; give concrete notes and alternatives.
- Ask one focused question to advance the draft.
''')
            print(self._ollama(prompt))
