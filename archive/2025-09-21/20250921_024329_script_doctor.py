
#!/usr/bin/env python3
"""
Script Doctor — Evolved (stdlib-only, growth-ready)
--------------------------------------------------
Propósito no Digimundo: análise sólida de roteiros com métricas ricas,
detecção adaptativa de beats (Save the Cat) sensível a gênero e ritmo,
inferência de arquétipos de história e integração opcional com o
sistema de aprendizado (Learning Lite).

Princípios:
  - stdlib-only, sem rede; integra LearningLite se estiver disponível;
  - APIs estáveis: analyze_script(), analyze_save_the_cat(), analyze_characters(), infer_archetypes();
  - Heurísticas determinísticas, explicáveis e fáceis de curar (dicionários).

Compatibilidade:
  - Mantém dataclasses Beat/SaveTheCatAnalysis/ScriptAnalysis e função analyze_script(text) para legado.
"""

from __future__ import annotations

import logging
import math
import re
import statistics
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

logger = logging.getLogger("scripturemon.script_doctor_evolved")

# -------------------------- Padrões básicos de roteiro --------------------------

SCENE_RE = re.compile(r'^(INT\.|EXT\.|INT/EXT\.)\s+.+', re.I | re.M)
CHAR_RE  = re.compile(r'^[A-Z][A-Z0-9\- ]+$', re.M)
DIALOGUE_RE = re.compile(r'^[A-Z][A-Z0-9\- ]+\n(.+?)(?=\n[A-Z]|\n\n|\Z)', re.M | re.S)

# ------------------------------- Dataclasses -------------------------------------

@dataclass
class Beat:
    name: str
    position_pct: float
    content: str
    confidence: float
    explanation: Dict[str, float] = field(default_factory=dict)  # contribuição por sinal

@dataclass
class SaveTheCatAnalysis:
    beats: List[Beat]
    missing_beats: List[str]
    structure_score: float
    notes: List[str]

@dataclass
class ScriptAnalysis:
    scenes: int
    characters: int
    words: int
    avg_scene_len: float
    top_characters: List[str]
    notes: List[str]
    dialogue_ratio: float = 0.0
    pacing_score: float = 0.0
    beats: List[Beat] = field(default_factory=list)
    type_token_ratio: float = 0.0
    action_ratio: float = 0.0
    avg_sentence_len: float = 0.0
    int_ext_ratio: Dict[str, float] = field(default_factory=dict)
    show_dont_tell_score: float = 0.0  # aproximação

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenes": self.scenes,
            "characters": self.characters,
            "words": self.words,
            "avg_scene_len": self.avg_scene_len,
            "top_characters": self.top_characters,
            "notes": self.notes,
            "dialogue_ratio": self.dialogue_ratio,
            "pacing_score": self.pacing_score,
            "beats": [asdict(b) for b in self.beats],
            "type_token_ratio": self.type_token_ratio,
            "action_ratio": self.action_ratio,
            "avg_sentence_len": self.avg_sentence_len,
            "int_ext_ratio": self.int_ext_ratio,
            "show_dont_tell_score": self.show_dont_tell_score,
        }

@dataclass
class CharacterArc:
    name: str
    appearances: int
    dialogue_count: int
    want: Optional[str] = None
    need: Optional[str] = None
    ghost: Optional[str] = None
    lie: Optional[str] = None
    truth: Optional[str] = None
    arc_detected: bool = False
    evidence: Dict[str, str] = field(default_factory=dict)

@dataclass
class ArchetypeMatch:
    name: str
    score: float
    evidence: List[str]

# ------------------------------- Dicionários -------------------------------------

SAVE_THE_CAT_BEATS: Dict[str, Tuple[int, int]] = {
    "opening_image": (0, 1),
    "setup": (1, 10),
    "theme_stated": (5, 5),
    "catalyst": (10, 12),
    "debate": (12, 25),
    "break_into_2": (25, 25),
    "b_story": (30, 30),
    "fun_and_games": (30, 50),
    "midpoint": (50, 50),
    "bad_guys_close_in": (50, 75),
    "all_is_lost": (75, 75),
    "dark_night": (75, 85),
    "break_into_3": (85, 85),
    "finale": (85, 99),
    "final_image": (99, 100),
}

# Base EN/PT; será enriquecido por gênero
BASE_BEAT_KEYWORDS: Dict[str, List[str]] = {
    "opening_image": ["opening image","imagem de abertura","snapshot","visão inicial","ordinary world","mundo comum"],
    "setup": ["setup","rotina","apresentação","estabelece","context","ordinary world","introdução"],
    "theme_stated": ["theme","tema","verdade","lição","moral","o tema","lesson"],
    "catalyst": ["catalyst","inciting incident","incidente incitante","chamado","convite","mensagem"],
    "debate": ["debate","dúvida","hesita","questiona","devo","deveria","decisão","choose"],
    "break_into_2": ["break into 2","ato 2","act two","cruza o limiar","começa a jornada"],
    "b_story": ["b story","subtrama","mentor","love interest","interesse amoroso","subplot"],
    "fun_and_games": ["fun and games","promessa da premissa","treino","montagem","aventuras"],
    "midpoint": ["midpoint","reviravolta","twist","vitória falsa","derrota falsa","reversal","clímax do meio"],
    "bad_guys_close_in": ["bad guys close in","pressão","complicações","antagonistas","apertam o cerco","piora"],
    "all_is_lost": ["all is lost","tudo está perdido","morte","fracasso","rompimento","desespero","sem esperança"],
    "dark_night": ["dark night","noite escura","reflexão","introspecção","ponto baixo"],
    "break_into_3": ["break into 3","ato 3","act three","plano final","síntese","decisão final"],
    "finale": ["finale","batalha final","confronto","resolução","último esforço","showdown"],
    "final_image": ["final image","imagem final","espelho da abertura","mudança","novo mundo"],
}

GENRE_KEYWORDS: Dict[str, Dict[str, List[str]]] = {
    "generic": {},
    "terror": {
        "catalyst": ["assombração","sussurro","aparicao","aparition","possuído","possessed"],
        "fun_and_games": ["assusta","espreita","investiga a casa","estranho ruído","ritual"],
        "all_is_lost": ["sangue","grito","sacrifício"],
        "finale": ["exorcismo","fuga da entidade","selar"],
    },
    "comedia": {
        "fun_and_games": ["gag","trapalhada","mal-entendido","sitcom","confusão"],
        "midpoint": ["virada cômica","plano absurdo"],
        "finale": ["reconciliação engraçada","confissão atrapalhada"],
    },
    "acao": {
        "catalyst": ["explosão","emboscada","assalto","roubo","agente"],
        "fun_and_games": ["perseguição","tiroteio","luta","montagem de treino"],
        "finale": ["duelo final","desarmar a bomba","resgate"],
    },
    "drama": {
        "theme_stated": ["o preço","sacrifício","pertence","culpa","redenção"],
        "all_is_lost": ["luto","perda","separação"],
        "finale": ["reconciliação","aceitação","catarse"],
    },
    "romance": {
        "b_story": ["namoro","paquera","encontro","date","ciúmes"],
        "fun_and_games": ["montagem romântica","mensagens","passeio"],
        "all_is_lost": ["término","coração partido"],
        "finale": ["declaração de amor","reunião","pedido"],
    },
    "ficcao": {
        "catalyst": ["anomalia","nave","experimento","portal","IA"],
        "fun_and_games": ["descoberta","exploração","teste de protótipo"],
        "finale": ["colapso do portal","paradoxo","primeira comunicação"],
    },
}

ARCHETYPES: Dict[str, List[str]] = {
    "buddy_love": ["parceria","amizade","química","romance","dupla","bromance","companheiro"],
    "whydunit": ["por quê","motivo real","verdade oculta","investigação moral"],
    "superhero": ["poderes","máscara","identidade secreta","salvar a cidade","vilão"],
    "fool_triumphant": ["ingênuo","bobo","subestimação","vira o jogo","esperteza"],
    "institutionalized": ["instituição","regras","rebeldia","conformidade","escape"],
}

# -------------------------- Utilidades e métricas ------------------------------

def _tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+", text.lower())

def _sentence_split(text: str) -> List[str]:
    return re.split(r"[.!?]+(?=\s+|$)", text.strip())

def _scene_spans(text: str) -> List[Tuple[int, int, str]]:
    """Retorna [(start,end,heading)] das cenas."""
    spans = [(m.span()[0], None, m.group(0)) for m in SCENE_RE.finditer(text)]
    out: List[Tuple[int, int, str]] = []
    for i, (s, _, h) in enumerate(spans):
        e = spans[i + 1][0] if i + 1 < len(spans) else len(text)
        out.append((s, e, h))
    return out

def _scene_lengths_words(text: str, spans: List[Tuple[int, int, str]]) -> List[int]:
    return [len(text[a:b].split()) for a, b, _ in spans]

def _dialogue_ratio_block(block: str) -> float:
    ds = DIALOGUE_RE.findall(block)
    w_total = len(block.split()) or 1
    w_dial = sum(len(d.split()) for d in ds)
    return w_dial / w_total

def _int_ext_ratio(spans: List[Tuple[int, int, str]]) -> Dict[str, float]:
    total = len(spans) or 1
    c_int = sum(1 for _, _, h in spans if h.strip().upper().startswith("INT"))
    c_ext = sum(1 for _, _, h in spans if h.strip().upper().startswith("EXT"))
    return {"INT": c_int / total, "EXT": c_ext / total}

# -------------------------- Integração com Learning -----------------------------

class _LearningAdapter:
    def __init__(self):
        self._impl = None
        try:
            from learning_lite_refactored import LearningLite as LL  # refatorado
            self._impl = LL()
        except Exception:
            try:
                from learning_lite import LearningLite as LL  # legado
                self._impl = LL()
            except Exception:
                self._impl = None

    def enabled(self) -> bool:
        return self._impl is not None

    def learn_from_analysis(self, analysis: ScriptAnalysis, screenplay_name: str):
        if not self._impl:
            return []
        try:
            return self._impl.learn_from_analysis(analysis, screenplay_name)  # type: ignore
        except Exception as e:
            logger.warning("LearningLite falhou: %s", e)
            return []

    def enrich_prompt(self, base: str, context: str = "") -> str:
        if not self._impl:
            return base
        try:
            return self._impl.enrich_prompt(base, context)  # type: ignore
        except Exception:
            return base

    def get_statistics(self) -> Dict[str, Any]:
        if not self._impl:
            return {"total_concepts": 0}
        try:
            return self._impl.get_statistics()  # type: ignore
        except Exception:
            return {"total_concepts": 0}

# ------------------------------- Núcleo ----------------------------------------

class ScriptDoctor:
    """
    Analisador de roteiros com beats adaptativos e inferência de arquétipos.
    """

    def __init__(self, use_learning: bool = True, genre: str = "generic"):
        self.learning = _LearningAdapter() if use_learning else None
        self.genre = genre if genre in GENRE_KEYWORDS else "generic"
        # cache de keywords mesclados (base + gênero)
        self._kw_cache: Dict[str, List[str]] = {}

    # --------------------------- Configuração ---------------------------------

    def set_genre(self, genre: str) -> None:
        self.genre = genre if genre in GENRE_KEYWORDS else "generic"
        self._kw_cache.clear()

    def register_genre_keywords(self, genre: str, beat_keywords: Dict[str, List[str]]) -> None:
        g = GENRE_KEYWORDS.setdefault(genre, {})
        for beat, kws in beat_keywords.items():
            base = g.setdefault(beat, [])
            for k in kws:
                if k not in base:
                    base.append(k)
        self._kw_cache.clear()

    def _keywords_for(self, beat: str) -> List[str]:
        if beat in self._kw_cache:
            return self._kw_cache[beat]
        base = list(BASE_BEAT_KEYWORDS.get(beat, []))
        addon = GENRE_KEYWORDS.get(self.genre, {}).get(beat, [])
        merged = list(dict.fromkeys(base + addon))
        self._kw_cache[beat] = merged
        return merged

    # ---------------------------- Análise Básica ------------------------------

    def analyze_script(self, text: str, screenplay_name: str = "Unknown") -> ScriptAnalysis:
        spans = _scene_spans(text)
        lens = _scene_lengths_words(text, spans)
        avg = statistics.mean(lens) if lens else 0.0

        # Personagens (linhas em caixa alta; remove tokens comuns)
        chars = [m.group(0).strip() for m in CHAR_RE.finditer(text)]
        blacklist = {"INT", "EXT", "INT/EXT", "FADE", "CUT", "CONTINUED"}
        cc: Dict[str, int] = {}
        for c in chars:
            if len(c) < 3 or c in blacklist or c.endswith("."):
                continue
            cc[c] = cc.get(c, 0) + 1
        top = sorted(cc.items(), key=lambda x: x[1], reverse=True)[:8]

        # Diálogo/ação e métricas
        words_total = len(text.split())
        dialogues = DIALOGUE_RE.findall(text)
        dialogue_words = sum(len(d.split()) for d in dialogues)
        dialogue_ratio = (dialogue_words / words_total) if words_total else 0.0

        # Pacing (coeficiente de variação truncado)
        pacing_score = 0.0
        if lens and len(lens) > 1 and avg > 0:
            pacing_score = min(1.5, statistics.stdev(lens) / avg) / 1.5

        # Type-token ratio (riqueza vocabular)
        tokens = _tokenize(text)
        unique = len(set(tokens))
        ttr = unique / max(1, len(tokens))

        # Ação aproximada: 1 - diálogo
        action_ratio = 1.0 - dialogue_ratio

        # Comprimento médio de sentença
        sents = [s for s in _sentence_split(text) if s.strip()]
        avg_sent_len = (sum(len(s.split()) for s in sents) / max(1, len(sents))) if sents else 0.0

        # INT/EXT ratio
        ie_ratio = _int_ext_ratio(spans)

        # Show-don't-tell (aproximação: média ponderada de ação + variação de cena - excesso de fala)
        sdt = max(0.0, min(1.0, 0.5 * action_ratio + 0.3 * pacing_score + 0.2 * (1.0 - abs(dialogue_ratio - 0.45))))

        # Notas
        notes: List[str] = []
        if len(spans) < 5:
            notes.append("Poucas cenas — verifique headings (INT./EXT.).")
        if avg > 400:
            notes.append("Cenas longas — considere respiros/variações.")
        if dialogue_ratio < 0.2:
            notes.append("Pouco diálogo — roteiro possivelmente descritivo demais.")
        if dialogue_ratio > 0.7:
            notes.append("Muito diálogo — considere mais ação visual.")
        if pacing_score < 0.3:
            notes.append("Ritmo possivelmente monótono — varie o tamanho das cenas.")

        stc = self.analyze_save_the_cat(text, spans=spans, lens=lens)

        analysis = ScriptAnalysis(
            scenes=len(spans),
            characters=len(top),
            words=words_total,
            avg_scene_len=avg,
            top_characters=[n for n, _ in top],
            notes=notes,
            dialogue_ratio=dialogue_ratio,
            pacing_score=pacing_score,
            beats=stc.beats,
            type_token_ratio=ttr,
            action_ratio=action_ratio,
            avg_sentence_len=avg_sent_len,
            int_ext_ratio=ie_ratio,
            show_dont_tell_score=sdt,
        )

        # Aprendizado opcional
        if self.learning and self.learning.enabled() and screenplay_name != "Unknown":
            learned = self.learning.learn_from_analysis(analysis, screenplay_name)
            if learned:
                logger.info("Learning: %d conceitos aprendidos de %s", len(learned), screenplay_name)

        return analysis

    # -------------------- Beats (adaptativo + por gênero) --------------------

    def _position_prior(self, pos_pct: float, expected_pct: float, sigma: float = 6.0) -> float:
        """Peso gaussiano pelo desvio em % (sigma default 6%)."""
        d = (pos_pct - expected_pct) / max(1e-6, sigma)
        return math.exp(-0.5 * d * d)

    def _candidate_score(self, snippet: str, keywords: List[str]) -> float:
        s = snippet.lower()
        hits = 0
        for kw in keywords:
            if kw in s:
                hits += 1
        return min(1.0, hits / max(1.0, math.log(10 + len(_tokenize(snippet)))))

    def analyze_save_the_cat(self, text: str, spans: Optional[List[Tuple[int,int,str]]] = None, lens: Optional[List[int]] = None) -> SaveTheCatAnalysis:
        spans = spans or _scene_spans(text)
        lens = lens or _scene_lengths_words(text, spans)
        total_chars = len(text) or 1

        beats_found: List[Beat] = []
        missing_beats: List[str] = []

        # Pré-cálculos por cena
        dial_by_scene = []
        for a, b, _ in spans:
            dial_by_scene.append(_dialogue_ratio_block(text[a:b]))
        avg_len = statistics.mean(lens) if lens else 0.0

        for name, (a_pct, b_pct) in SAVE_THE_CAT_BEATS.items():
            exp_pct = (a_pct + b_pct) / 2
            # Converter % esperada -> índice de cena aproximado
            exp_pos = int(total_chars * exp_pct / 100)
            center_scene = 0
            for i, (a, b, _) in enumerate(spans):
                if a <= exp_pos < b:
                    center_scene = i
                    break

            # Janela adaptativa em torno da cena central
            radius = max(2, int(0.03 * len(spans)))  # ~3% das cenas
            lo = max(0, center_scene - radius)
            hi = min(len(spans) - 1, center_scene + radius)

            best_score = 0.0
            best_idx = center_scene
            best_expl: Dict[str, float] = {}

            kws = self._keywords_for(name)

            for i in range(lo, hi + 1):
                a, b, _ = spans[i]
                snippet = text[a:b]

                # 1) keywords
                kw_score = self._candidate_score(snippet, kws)

                # 2) densidade de headings ~ curtamente: mais cenas na janela local indicam virada
                # (como usamos uma cena, aproximamos por inverso do comprimento dessa cena vs média)
                density = 1.0 - min(1.0, (lens[i] / max(1.0, 2 * avg_len)))  # cenas curtas => maior densidade local

                # 3) mudança de pacing (diferença de média antes/depois)
                pre = lens[max(0, i-2):i] or [avg_len]
                pos = lens[i+1:i+3] or [avg_len]
                pacing_change = abs((statistics.mean(pre) - statistics.mean(pos)) / max(1.0, avg_len))
                pacing_change = min(1.0, pacing_change)

                # 4) mudança de diálogo
                pre_d = dial_by_scene[max(0, i-2):i] or [0.0]
                pos_d = dial_by_scene[i+1:i+3] or [0.0]
                dial_change = abs((statistics.mean(pre_d) - statistics.mean(pos_d)))
                dial_change = min(1.0, dial_change)

                # 5) prior de posição (gaussiano em %)
                scene_mid_pct = (a + b) / (2 * total_chars) * 100.0
                prior = self._position_prior(scene_mid_pct, exp_pct, sigma=6.0)

                # combinação (ponderações ajustadas)
                score = 0.45 * kw_score + 0.2 * density + 0.2 * pacing_change + 0.05 * dial_change + 0.1 * prior
                if score > best_score:
                    best_score = score
                    best_idx = i
                    best_expl = {
                        "keywords": round(kw_score, 3),
                        "density": round(density, 3),
                        "pacing_change": round(pacing_change, 3),
                        "dialogue_change": round(dial_change, 3),
                        "position_prior": round(prior, 3),
                    }

            a, b, heading = spans[best_idx]
            content = text[a:b][:220]
            conf = min(1.0, 0.7 * best_score + 0.3 * self._position_prior(((a + b) / (2 * total_chars) * 100.0), exp_pct))
            if conf >= 0.4:
                beats_found.append(Beat(name=name, position_pct=(a + b) / (2 * total_chars) * 100.0, content=content, confidence=conf, explanation=best_expl))
            else:
                missing_beats.append(name)

        structure_score = (len(beats_found) / len(SAVE_THE_CAT_BEATS)) if SAVE_THE_CAT_BEATS else 0.0
        notes: List[str] = []
        if structure_score < 0.5:
            notes.append("Estrutura incompleta — muitos beats ausentes.")
        elif structure_score > 0.8:
            notes.append("Boa estrutura Save the Cat.")
        if "opening_image" in missing_beats:
            notes.append("Falta imagem de abertura forte.")
        if "midpoint" in missing_beats:
            notes.append("Midpoint não identificado — revisar ponto de virada.")

        return SaveTheCatAnalysis(
            beats=beats_found,
            missing_beats=missing_beats,
            structure_score=structure_score,
            notes=notes,
        )

    # ---------------------------- Personagens --------------------------------

    def analyze_characters(self, text: str, character_name: str) -> CharacterArc:
        arc = CharacterArc(name=character_name, appearances=0, dialogue_count=0)

        # Aparições nominalizadas
        pattern = re.compile(rf"\b{re.escape(character_name)}\b", re.I)
        arc.appearances = len(pattern.findall(text))

        # Diálogos do personagem
        dialogue_pattern = re.compile(rf"^{re.escape(character_name)}\n(.+?)(?=\n[A-Z]|\n\n|\Z)", re.M | re.S)
        dialogues = dialogue_pattern.findall(text)
        arc.dialogue_count = len(dialogues)

        joined = "\n".join(dialogues[:10]).lower()

        def _extract_first(*phrases: str) -> Optional[str]:
            for ph in phrases:
                m = re.search(rf"{ph}\s*[:\-–]\s*(.+?)(?:[\.!\?]\s|$)", joined)
                if m:
                    return m.group(1).strip()[:160]
            return None

        arc.want  = _extract_first(r"\bi want\b", r"\beu quero\b")
        arc.need  = _extract_first(r"\bi need\b", r"\beu preciso\b")
        arc.ghost = _extract_first(r"\bghost\b", r"\bpassado\b", r"\bferida\b", r"\btrauma\b")
        arc.lie   = _extract_first(r"\blie\b", r"\bmentira\b", r"\bfalsa crença\b")
        arc.truth = _extract_first(r"\btruth\b", r"\bverdade\b", r"\brealização\b")

        arc.arc_detected = bool(arc.want and (arc.need or arc.truth))
        if arc.want:  arc.evidence["want"]  = arc.want
        if arc.need:  arc.evidence["need"]  = arc.need
        if arc.ghost: arc.evidence["ghost"] = arc.ghost
        if arc.lie:   arc.evidence["lie"]   = arc.lie
        if arc.truth: arc.evidence["truth"] = arc.truth
        return arc

    # --------------------------- Arquétipos de história ----------------------

    def infer_archetypes(self, text: str, top_k: int = 2) -> List[ArchetypeMatch]:
        lower = text.lower()
        matches: List[ArchetypeMatch] = []
        for name, kws in ARCHETYPES.items():
            score = 0
            evidence = []
            for kw in kws:
                if kw in lower:
                    score += 1
                    # captura pequeno contexto
                    m = re.search(rf"(.{{0,30}}{re.escape(kw)}.{{0,30}})", lower)
                    if m:
                        evidence.append(m.group(1))
            if score > 0:
                norm = min(1.0, score / max(3, len(kws)))
                matches.append(ArchetypeMatch(name=name, score=norm, evidence=evidence[:3]))
        matches.sort(key=lambda x: x.score, reverse=True)
        return matches[:max(1, top_k)]

    # --------------------------- Validação & Sugestões -----------------------

    def validate_structure(self, stc: SaveTheCatAnalysis, analysis: Optional[ScriptAnalysis] = None) -> List[str]:
        notes: List[str] = list(stc.notes)
        if "midpoint" in stc.missing_beats:
            notes.append("Sugestão: crie uma reversão clara no meio (vitória/derrota falsa).")
        if "theme_stated" in stc.missing_beats:
            notes.append("Sugestão: explicite o tema cedo, preferencialmente em diálogo breve.")
        if analysis:
            if analysis.pacing_score < 0.3:
                notes.append("Sugestão: introduza cenas curtas entre cenas longas para variar o ritmo.")
            if analysis.dialogue_ratio > 0.65:
                notes.append("Sugestão: converta falas expositivas em ações observáveis (show, don't tell).")
        return notes

    # ------------------------------- Utilitários -----------------------------

    def get_learning_stats(self) -> Dict[str, Any]:
        if self.learning and self.learning.enabled():
            return self.learning.get_statistics()
        return {"total_concepts": 0}

# --------------------------- Função de compatibilidade ---------------------------

def analyze_script(text: str) -> ScriptAnalysis:
    """Compatível com chamadas legadas."""
    return ScriptDoctor(use_learning=False).analyze_script(text)

# --------------------------------- Smoke ---------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    sample = """INT. APARTAMENTO - NOITE
    MARIA olha a janela. Silêncio.

    MARIA
    Eu preciso encontrar a verdade.

    INT. CORREDOR - NOITE
    Um sussurro distante.

    MARIA
    Eu quero saber o que aconteceu aqui.

    EXT. RUA - CONTÍNUO
    Passos apressados sob a chuva.

    INT. PORÃO - NOITE
    O ritual começa. Velas tremulam.

    MARIA
    Não vou fugir desta vez.
    """

    doc = ScriptDoctor(use_learning=False, genre="terror")
    sa = doc.analyze_script(sample, "Sample_Script")
    print("📊 Básico:", {k:v for k,v in sa.to_dict().items() if k in ("scenes","dialogue_ratio","pacing_score","type_token_ratio")})
    stc = doc.analyze_save_the_cat(sample)
    print("🎬 STC score:", f"{stc.structure_score:.1%}", "beats:", len(stc.beats), "missing:", stc.missing_beats)
    arcs = doc.analyze_characters(sample, "MARIA")
    print("🧭 Arc:", arcs)
    arch = doc.infer_archetypes(sample)
    print("🧩 Archetypes:", arch)
    print("✅ OK")
