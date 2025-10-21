
#!/usr/bin/env python3
"""
Learning Lite — Evolved & Doctor‑Compatible (stdlib‑only)
--------------------------------------------------------
Propósito: aprender padrões de estrutura/personagem/arquétipo e métricas
a partir do Script Doctor (legado e evoluído), persistir de forma robusta,
recuperar via BM25 e enriquecer prompts ou recomendações de reescrita.

Compatibilidade:
  - Mantém a classe/public API `LearningLite` (drop‑in replacement);
  - Aceita `ScriptAnalysis` com `beats` como lista de `Beat` (dict/obj);
  - Opcionalmente consome `archetypes` e `character_arcs` (se fornecidos);
  - Usa `scripturemon_champion.rag` quando disponível, com fallback BM25 stdlib.

Evoluções chave vs. versão refatorada:
  - Tipos de conceito (`kind`) e `key` normalizados (ex.: beat:midpoint);
  - Fusão/dedup mais forte + reforço de confiança;
  - Indexação rica (kind/tags/meta/exemplos) + filtros por `kinds`/tags;
  - Estatísticas agregadas (ex.: média/DP de posição por beat);
  - `enrich_prompt_pro()` (seções por tipo) e `recommend_for()` (sugestões);
  - Import/export (JSON), pruning por confiança/recência; snapshot em memória unificada.
"""

from __future__ import annotations

import json, math, re, hashlib, threading
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# ---------- Infra opcional (integração com o núcleo refatorado) ----------

def _discover_paths() -> Dict[str, Path]:
    """Tenta usar scripturemon_champion.paths; cai para pastas locais se não existir."""
    try:
        from scripturemon_champion.paths import DATA_DIR as _DATA_DIR  # type: ignore
        data_dir = Path(_DATA_DIR)
    except Exception:
        data_dir = Path("data")
    learn_dir = data_dir / "learning"
    learn_dir.mkdir(parents=True, exist_ok=True)
    return {"data_dir": data_dir, "learn_dir": learn_dir}

def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

# ---------- BM25 minimal (fallback) ----------

_TOKEN_RE = re.compile(r"[\w\-']+", re.U)

def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "")]

class _BM25Index:
    """BM25 simples (fallback quando scripturemon_champion.rag não estiver disponível)."""
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = float(k1), float(b)
        self.docs: Dict[str, str] = {}
        self.tf: Dict[str, Dict[str, int]] = {}
        self.df: Dict[str, int] = {}
        self.doc_len: Dict[str, int] = {}
        self.N = 0
        self.avgdl = 0.0

    def _recompute_avg(self):
        self.avgdl = (sum(self.doc_len.values()) / self.N) if self.N else 0.0

    def add(self, doc_id: str, text: str):
        tokens = _tokenize(text)
        cnt: Dict[str, int] = {}
        for t in tokens:
            cnt[t] = cnt.get(t, 0) + 1

        if doc_id in self.docs:
            # remove contribuição antiga (simples)
            old = self.tf.get(doc_id, {})
            for t in old:
                self.df[t] -= 1
                if self.df[t] <= 0:
                    self.df.pop(t, None)
            self.N -= 1

        self.docs[doc_id] = text
        self.tf[doc_id] = cnt
        self.doc_len[doc_id] = sum(cnt.values())
        for t in cnt:
            self.df[t] = self.df.get(t, 0) + 1
        self.N += 1
        self._recompute_avg()

    def _idf(self, term: str) -> float:
        df = self.df.get(term, 0)
        if df == 0 or self.N == 0:
            return 0.0
        return math.log(((self.N - df + 0.5) / (df + 0.5)) + 1.0)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        if self.N == 0:
            return []
        terms = set(_tokenize(query))
        scores: Dict[str, float] = {}
        avgdl = self.avgdl or 1.0
        for doc_id, dcnt in self.tf.items():
            dl = self.doc_len.get(doc_id, 1) or 1
            score = 0.0
            for t in terms:
                f = dcnt.get(t, 0)
                if not f:
                    continue
                idf = self._idf(t)
                denom = f + self.k1 * (1 - self.b + self.b * (dl / avgdl))
                score += idf * ((f * (self.k1 + 1)) / denom)
            if score > 0:
                scores[doc_id] = score
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max(1, top_k)]

# ---------- Domínio: Conceitos Aprendidos ----------

@dataclass
class LearnedConcept:
    # Novo: `kind` e `key` ajudam na dedup e nas consultas específicas
    kind: str
    key: str
    concept: str
    source: str
    confidence: float
    timestamp: str
    examples: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    id: str = ""  # id estável para deduplicação

    def ensure_id(self):
        if not self.id:
            base = f"{self.kind}|{self.key}|{self.source}".lower()
            self.id = hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]

    def reinforce(self, add_conf: float, example: Optional[str] = None, extra_tags: Optional[List[str]] = None, extra_meta: Optional[Dict[str, Any]] = None):
        """Reforça a confiança: 1 - (1-a)*(1-b) e agrega evidências/tags/meta."""
        a = max(0.0, min(1.0, self.confidence))
        b = max(0.0, min(1.0, add_conf))
        self.confidence = 1.0 - (1.0 - a) * (1.0 - b)
        if example:
            if example not in self.examples:
                self.examples.append(example)
        if extra_tags:
            for t in extra_tags:
                if t not in self.tags:
                    self.tags.append(t)
        if extra_meta:
            for k, v in extra_meta.items():
                if k not in self.meta:
                    self.meta[k] = v
        self.timestamp = _now_iso()

# ---------- Núcleo Learning (Evolved) ----------

class LearningLite:
    """
    Armazena e consulta conceitos aprendidos (versão evoluída, retro‑compatível).
    - Persistência: JSON em `data/learning/learned_concepts.json` + snapshot em memória unificada (se disponível).
    - Busca: BM25 (`scripturemon_champion.rag` quando possível; senão, fallback).
    - API: learn_from_analysis, get_relevant_concepts, enrich_prompt(_pro), get_statistics, export/import, recommend_for.
    """

    SCHEMA_VERSION = 2

    def __init__(self, max_concepts: int = 800):
        paths = _discover_paths()
        self.learning_file = paths["learn_dir"] / "learned_concepts.json"
        self.max_concepts = int(max_concepts)
        self._lock = threading.RLock()

        # memória unificada (opcional)
        self._memory = None
        try:
            from scripturemon_champion.memory import get_unified_memory  # type: ignore
            self._memory = get_unified_memory()
        except Exception:
            self._memory = None

        # índice BM25 (preferir o do núcleo; senão, fallback)
        try:
            from scripturemon_champion import rag as _rag  # type: ignore
            def _idx(doc_id: str, text: str, metadata: Optional[dict] = None):
                return _rag.index_document(f"learn:{doc_id}", text, metadata or {})
            def _search(q: str, k: int) -> List[Tuple[str, float]]:
                res = _rag.search_documents(q, top_k=k)
                out = []
                for r in res:
                    if r.get("doc_id", "").startswith("learn:"):
                        out.append((r["doc_id"], float(r.get("score", 0.0))))
                return out
            self._index_api = (True, _idx, _search)  # (is_global, idx_fn, search_fn)
        except Exception:
            self._bm25 = _BM25Index()
            def _idx(doc_id: str, text: str, metadata: Optional[dict] = None):
                return self._bm25.add(f"learn:{doc_id}", text)
            def _search(q: str, k: int) -> List[Tuple[str, float]]:
                return self._bm25.search(q, top_k=k)
            self._index_api = (False, _idx, _search)

        # cache em memória
        self.concepts: Dict[str, LearnedConcept] = {}
        self._load_all()
        self._rebuild_index()

    # ----- Persistência -----

    def _load_all(self):
        """Carrega snapshot da memória unificada (se existir), senão do JSON local; migra registros antigos."""
        data = None

        # 1) memória unificada (snapshot mais recente)
        if self._memory is not None:
            try:
                snap = self._memory.get("learning", "concepts")  # type: ignore
                if snap and isinstance(snap.value, list):
                    data = snap.value
            except Exception:
                data = None

        # 2) arquivo JSON
        if data is None and self.learning_file.exists():
            try:
                with self.learning_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = None

        # 3) inicialização vazia
        if not data:
            self.concepts = {}
            return

        tmp: Dict[str, LearnedConcept] = {}
        for c in data:
            try:
                # Migração: versão antiga não tinha 'kind'/'key'/id
                if "kind" not in c or "key" not in c:
                    # heurística simples
                    concept = c.get("concept", "")
                    tags = c.get("tags", []) or []
                    if concept.lower().startswith("beat "):
                        kind = "beat"
                        name = concept.split(" ", 2)[1].lower() if " " in concept else "unknown"
                        key = f"beat:{name}"
                        tags = list(set(tags + ["beat", name]))
                    elif "protagonist" in concept.lower():
                        kind = "character"
                        key = "protagonist"
                        tags = list(set(tags + ["character", "protagonist"]))
                    elif "pacing" in concept.lower():
                        kind = "metric"
                        key = "pacing"
                        tags = list(set(tags + ["metric", "pacing"]))
                    else:
                        kind = "concept"
                        key = re.sub(r"\s+", ":", concept.lower())[:40]
                    c["kind"], c["key"] = kind, key
                lc = LearnedConcept(
                    kind=c["kind"],
                    key=c["key"],
                    concept=c.get("concept",""),
                    source=c.get("source",""),
                    confidence=float(c.get("confidence", 0.5)),
                    timestamp=c.get("timestamp", _now_iso()),
                    examples=c.get("examples") or [],
                    tags=c.get("tags") or [],
                    meta=c.get("meta") or {},
                    id=c.get("id",""),
                )
                lc.ensure_id()
                tmp[lc.id] = lc
            except Exception:
                continue
        self.concepts = tmp

    def _snapshot(self):
        """Salva JSON + escreve snapshot na memória unificada (se disponível)."""
        with self._lock:
            rows = [asdict(c) for c in self.concepts.values()]
            self.learning_file.parent.mkdir(parents=True, exist_ok=True)
            with self.learning_file.open("w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
            if self._memory is not None:
                try:
                    payload = json.loads(json.dumps(rows, ensure_ascii=False))
                    from scripturemon_champion.memory import MemoryRecord  # type: ignore
                    rec = MemoryRecord(type="learning", key="concepts", value=payload, metadata={"schema": self.SCHEMA_VERSION})
                    self._memory.store(rec)  # type: ignore
                except Exception:
                    pass

    # ----- Indexação -----

    def _index_text_for(self, c: LearnedConcept) -> str:
        parts = [c.kind, c.key, c.concept, c.source]
        if c.tags: parts.append(" ".join(c.tags))
        if c.examples: parts.extend(c.examples[:3])
        if c.meta:
            meta_frag = " ".join(f"{k}:{v}" for k, v in list(c.meta.items())[:8])
            parts.append(meta_frag)
        return "\n".join(parts)

    def _rebuild_index(self):
        _, idx, _ = self._index_api
        for c in self.concepts.values():
            idx(c.id, self._index_text_for(c), {"source": c.source, "kind": c.kind, "key": c.key, "confidence": c.confidence})

    def _update_index(self, concepts: Iterable[LearnedConcept]):
        _, idx, _ = self._index_api
        for c in concepts:
            idx(c.id, self._index_text_for(c), {"source": c.source, "kind": c.kind, "key": c.key, "confidence": c.confidence})

    # ----- Utilidades internas -----

    def _upsert(self, c: LearnedConcept) -> LearnedConcept:
        c.ensure_id()
        cur = self.concepts.get(c.id)
        if cur is None:
            self.concepts[c.id] = c
            return c
        cur.reinforce(c.confidence, (c.examples or [None])[0], extra_tags=c.tags, extra_meta=c.meta)
        return cur

    def _prune(self):
        if len(self.concepts) <= self.max_concepts:
            return
        # manter por score composto (confiança + recência)
        def _score(x: LearnedConcept) -> Tuple[float, float]:
            try:
                ts = datetime.fromisoformat(x.timestamp).timestamp()
            except Exception:
                ts = 0.0
            return (x.confidence, ts)
        keep = sorted(self.concepts.values(), key=_score, reverse=True)[: self.max_concepts]
        self.concepts = {c.id: c for c in keep}

    @staticmethod
    def _has(obj: Any, name: str) -> bool:
        return (isinstance(obj, dict) and name in obj) or hasattr(obj, name)

    @staticmethod
    def _get(obj: Any, name: str, default=None):
        if isinstance(obj, dict):
            return obj.get(name, default)
        return getattr(obj, name, default)

    # ----- Aprendizado (compatível com Script Doctor) -----

    def learn_from_analysis(self, analysis_result: Any, screenplay_name: str, confidence_threshold: float = 0.7, *, genre: Optional[str]=None, extras: Optional[Dict[str, Any]] = None) -> List[LearnedConcept]:
        """
        Extrai e registra conceitos a partir de um resultado de análise do Script Doctor.

        Compatível com:
          - Script Doctor (legado): beats simples, protagonista, pacing;
          - Script Doctor Evolved: beats com explanation, métricas extras e entradas opcionais em `extras`.
        """
        ts = _now_iso()
        learned: List[LearnedConcept] = []
        extras = extras or {}

        # 1) Beats
        if self._has(analysis_result, "beats") and self._get(analysis_result, "beats"):
            for beat in self._get(analysis_result, "beats", []):
                b_conf = float(self._get(beat, "confidence", 0.0) or 0.0)
                if b_conf < confidence_threshold:
                    continue
                name = str(self._get(beat, "name", "beat")).strip().lower()
                pos = self._get(beat, "position_pct", None)
                content = str(self._get(beat, "content", ""))[:300]
                explanation = self._get(beat, "explanation", {}) or {}

                c = LearnedConcept(
                    kind="beat",
                    key=f"beat:{name}",
                    concept=f"Beat {name} typically at {pos}%" if pos is not None else f"Beat {name} detected",
                    source=screenplay_name,
                    confidence=b_conf,
                    timestamp=ts,
                    examples=[content] if content else [],
                    tags=(["beat", name] + ([f"genre:{genre}"] if genre else [])),
                    meta={"position_pct": pos, "signals": explanation} if pos is not None else {"signals": explanation},
                )
                learned.append(self._upsert(c))

        # 2) Protagonista (top_characters[0])
        if self._has(analysis_result, "top_characters") and self._get(analysis_result, "top_characters"):
            first = str(self._get(analysis_result, "top_characters")[0])
            c = LearnedConcept(
                kind="character",
                key=f"protagonist:{first}",
                concept=f"Protagonist pattern: {first}",
                source=screenplay_name,
                confidence=0.8,
                timestamp=ts,
                tags=["character", "protagonist"] + ([f"genre:{genre}"] if genre else []),
            )
            learned.append(self._upsert(c))

        # 3) Métricas (e.g., pacing)
        if self._has(analysis_result, "pacing_score"):
            ps = float(self._get(analysis_result, "pacing_score", 0.0) or 0.0)
            if ps > 0.5:
                c = LearnedConcept(
                    kind="metric",
                    key="pacing>0.5",
                    concept=f"Good pacing with variation score {ps:.2f}",
                    source=screenplay_name,
                    confidence=0.75,
                    timestamp=ts,
                    tags=["metric", "pacing"] + ([f"genre:{genre}"] if genre else []),
                    meta={"pacing_score": ps},
                )
                learned.append(self._upsert(c))

        # 4) Arquétipos (se fornecidos em extras)
        arch = extras.get("archetypes") or self._get(analysis_result, "archetypes", None)
        if arch:
            for a in arch:
                name = str(self._get(a, "name", "")).lower()
                score = float(self._get(a, "score", 0.0) or 0.0)
                if not name or score < 0.5:
                    continue
                evid = self._get(a, "evidence", []) or []
                c = LearnedConcept(
                    kind="archetype",
                    key=f"archetype:{name}",
                    concept=f"Archetype match: {name} (score {score:.2f})",
                    source=screenplay_name,
                    confidence=min(1.0, 0.6 + 0.4*score),
                    timestamp=ts,
                    examples=evid[:3],
                    tags=["archetype", name] + ([f"genre:{genre}"] if genre else []),
                    meta={"score": score},
                )
                learned.append(self._upsert(c))

        # 5) Arcos de personagem (se fornecidos em extras)
        arcs = extras.get("character_arcs") or self._get(analysis_result, "character_arcs", None)
        if arcs:
            for a in arcs:
                nm = str(self._get(a, "name", "")).strip()
                if not nm:
                    continue
                # confiança heurística: presença de WANT + (NEED ou TRUTH)
                want = self._get(a, "want", None)
                need = self._get(a, "need", None)
                truth = self._get(a, "truth", None)
                conf = 0.6 + 0.2*int(bool(want)) + 0.2*int(bool(need or truth))
                ev = {}
                for k in ("want","need","ghost","lie","truth"):
                    v = self._get(a, k, None)
                    if v: ev[k]=str(v)[:160]
                c = LearnedConcept(
                    kind="character_arc",
                    key=f"arc:{nm}",
                    concept=f"Character arc signals present for {nm}",
                    source=screenplay_name,
                    confidence=min(1.0, conf),
                    timestamp=ts,
                    examples=[v for v in ev.values()][:3],
                    tags=["character_arc", nm] + ([f"genre:{genre}"] if genre else []),
                    meta=ev,
                )
                learned.append(self._upsert(c))

        if not learned:
            return []

        # pruning + snapshot + index
        self._prune()
        self._snapshot()
        self._update_index(learned)
        return learned

    # ----- Consulta / Enriquecimento -----

    def get_relevant_concepts(self, query: str, top_k: int = 5, *, kinds: Optional[List[str]]=None, tags: Optional[List[str]]=None) -> List[LearnedConcept]:
        if not self.concepts:
            return []
        _, _, search = self._index_api
        hits = search(query, max(1, int(top_k*3)))  # busca mais larga e filtra
        out: List[LearnedConcept] = []
        for doc_id, _ in hits:
            cid = doc_id.split(":", 1)[-1]  # remove prefixo learn:
            c = self.concepts.get(cid)
            if not c:
                continue
            if kinds and c.kind not in kinds:
                continue
            if tags and not any(t in c.tags for t in tags):
                continue
            out.append(c)
            if len(out) >= top_k:
                break
        return out

    def enrich_prompt(self, base_prompt: str, context: str = "", top_k: int = 3, max_chars: int = 600) -> str:
        search_text = f"{base_prompt} {context}".strip()
        concepts = self.get_relevant_concepts(search_text, top_k=top_k)
        if not concepts:
            return base_prompt
        lines = ["\n\n[LEARNING CONTEXT] Consider these learned patterns:"]
        used = 0
        for c in concepts:
            frag = f"- ({c.kind}) {c.concept} (from {c.source}; conf={c.confidence:.2f})"
            if used + len(frag) > max_chars:
                break
            lines.append(frag)
            used += len(frag) + 1
        return base_prompt + "\n".join(lines)

    def enrich_prompt_pro(self, base_prompt: str, *, q: str = "", k_beats: int = 3, k_arch: int = 2, k_chars: int = 2, max_chars: int = 800) -> str:
        q = q or base_prompt
        sections = []
        used = 0

        def _add(title: str, items: List[LearnedConcept]):
            nonlocal used
            if not items: return
            hdr = f"\n\n[{title}]"
            if used + len(hdr) > max_chars: return
            sections.append(hdr); used += len(hdr)
            for c in items:
                frag = f"\n- {c.concept} (conf={c.confidence:.2f})"
                if used + len(frag) > max_chars: break
                sections.append(frag); used += len(frag)

        _add("BEATS", self.get_relevant_concepts(q, top_k=k_beats, kinds=["beat"]))
        _add("ARCHETYPES", self.get_relevant_concepts(q, top_k=k_arch, kinds=["archetype"]))
        _add("CHARACTER ARCS", self.get_relevant_concepts(q, top_k=k_chars, kinds=["character_arc"]))

        return base_prompt + "".join(sections)

    # ----- Estatísticas & Recomendações -----

    def beat_stats(self) -> Dict[str, Dict[str, float]]:
        """Resumo estatístico de posições por beat: média e contagem."""
        agg: Dict[str, List[float]] = {}
        for c in self.concepts.values():
            if c.kind == "beat" and "position_pct" in c.meta and isinstance(c.meta["position_pct"], (int,float)):
                name = c.key.split(":",1)[-1]
                agg.setdefault(name, []).append(float(c.meta["position_pct"]))
        out: Dict[str, Dict[str, float]] = {}
        for name, arr in agg.items():
            if not arr: continue
            m = sum(arr)/len(arr)
            # desvio padrão simples
            var = sum((x-m)*(x-m) for x in arr)/max(1, len(arr)-1)
            out[name] = {"mean_pct": round(m,2), "stdev_pct": round(var**0.5,2), "n": len(arr)}
        return out

    def recommend_for(self, analysis: Any, stc: Optional[Any] = None, *, max_items: int = 6) -> List[str]:
        """Sugestões de reescrita simples a partir do diagnóstico e do acervo aprendido."""
        notes: List[str] = []
        # Estrutura
        missing = []
        if stc is None and self._has(analysis,"beats"):
            # se `analysis` já traz os beats (como no ScriptAnalysis evoluído)
            beats = self._get(analysis,"beats") or []
            expected = {"opening_image","setup","theme_stated","catalyst","debate","break_into_2","b_story","fun_and_games","midpoint","bad_guys_close_in","all_is_lost","dark_night","break_into_3","finale","final_image"}
            present = { (self._get(b,"name","") or "").lower() for b in beats }
            missing = sorted(list(expected - present))
        elif stc is not None:
            missing = list(getattr(stc, "missing_beats", []) or [])

        stats = self.beat_stats()
        for mb in missing[:3]:
            if mb in stats:
                target = stats[mb]["mean_pct"]
                notes.append(f"Reforce o beat '{mb}' por volta de ~{target:.0f}% (média do acervo).")
            else:
                notes.append(f"Reforce o beat '{mb}' com um momento reconhecível do gênero.")

        # Pacing/Diálogo
        ps = float(self._get(analysis,"pacing_score",0.0) or 0.0)
        dr = float(self._get(analysis,"dialogue_ratio",0.0) or 0.0)
        if ps < 0.3: notes.append("Intercale cenas curtas entre cenas longas para variar o ritmo.")
        if dr > 0.65: notes.append("Converta falas expositivas em ações observáveis (show, don't tell).")
        if dr < 0.20: notes.append("Inclua trocas de diálogo objetivas para revelar objetivos/conflitos.")

        # Limite
        return notes[:max_items]

    # ----- Administração -----

    def get_statistics(self) -> Dict[str, Any]:
        if not self.concepts:
            return {"total_concepts": 0, "sources": [], "avg_confidence": 0.0, "top_concepts": []}
        total = len(self.concepts)
        sources = sorted({c.source for c in self.concepts.values()})
        avg_conf = sum(c.confidence for c in self.concepts.values()) / total
        top = sorted(self.concepts.values(), key=lambda x: x.confidence, reverse=True)[: min(5, total)]
        return {
            "total_concepts": total,
            "sources": sources,
            "avg_confidence": round(avg_conf,3),
            "top_concepts": [c.concept for c in top],
        }

    def export_json(self, path: str | Path) -> None:
        rows = [asdict(c) for c in self.concepts.values()]
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def import_json(self, path: str | Path, merge: bool = True) -> int:
        p = Path(path)
        if not p.exists():
            return 0
        try:
            rows = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return 0
        added = 0
        for c in rows:
            try:
                lc = LearnedConcept(**c)
                lc.ensure_id()
                if merge:
                    self._upsert(lc)
                else:
                    self.concepts[lc.id] = lc
                added += 1
            except Exception:
                continue
        self._snapshot()
        self._rebuild_index()
        return added

# ---------- Execução direta (smoke) ----------
if __name__ == "__main__":
    ll = LearningLite(max_concepts=250)

    # Mock compatível com Script Doctor Evolved
    analysis = {
        "top_characters": ["JOHN", "MARY"],
        "dialogue_ratio": 0.42,
        "pacing_score": 0.72,
        "beats": [
            {"name": "catalyst", "position_pct": 10, "content": "O evento que desestabiliza a rotina.", "confidence": 0.82, "explanation": {"keywords":0.7}},
            {"name": "all_is_lost", "position_pct": 75, "content": "Tudo parece perdido para o herói.", "confidence": 0.88, "explanation": {"keywords":0.8}},
        ],
    }
    archetypes = [{"name":"whydunit","score":0.8,"evidence":["por quê real do crime"]}]
    arcs = [{"name":"JOHN","want":"I want to save her","need":"I need to accept loss","truth":"love is letting go"}]

    learned = ll.learn_from_analysis(analysis, "Sample_Screenplay", extras={"archetypes":archetypes, "character_arcs":arcs}, genre="terror")
    print("📚 Aprendeu:", len(learned), "itens")

    tips = ll.recommend_for(analysis)
    print("💡 Recomendações:", tips[:3])

    enriched = ll.enrich_prompt_pro("Analyze Act II", q="midpoint reversal, hero under pressure")
    print("🧠 Enriched:", enriched[:200].replace("\n"," ") + "...")
