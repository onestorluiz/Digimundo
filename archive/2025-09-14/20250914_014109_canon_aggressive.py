# -*- coding: utf-8 -*-
from __future__ import annotations
import re, unicodedata

# Mapeamentos para headers
TIME_MAP = {
    "MORNING":"DAY","AFTERNOON":"DAY","NOON":"DAY",
    "EVENING":"NIGHT","MIDNIGHT":"NIGHT",
    "DAWN":"DAWN","DUSK":"DUSK","LATER":"LATER",
    "CONTINUOUS":"CONT.","CONT.":"CONT.","SAME":"SAME"
}
HEAD_PREFIX = {"I/E":"INT/EXT","EXT/INT":"INT/EXT"}

# Regexes robustos
RE_WS_MULTI = re.compile(r"[ \t]{2,}")
RE_DASH = re.compile(r"[—–]+")
RE_TRAIL_WS = re.compile(r"[ \t]+$")
RE_MULTI_NL = re.compile(r"\n{3,}")
RE_TRANS_CUT = re.compile(r"\bCUT TO\b:?", flags=re.I)
RE_FADE_IN   = re.compile(r"\bFADE IN\b:?", flags=re.I)
RE_SCENE_NUM_END = re.compile(r"[ \t]*(?:\(#?\d+\)|#\d+|\d+)$")

# Headers tolerantes: INT./EXT./INT/EXT./I/E, vários separadores e tempos
RE_HEADER = re.compile(
    r"^\s*(INT|EXT|INT/EXT|EXT/INT|I/E)\.?\s+([A-Z0-9 _'&/().-]+?)\s*[—–-]\s*([A-Z ]+)\s*$",
    flags=re.I
)

# Linhas totalmente maiúsculas curtas (nomes de personagem)
RE_CHARLINE = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")

def _norm_unicode(s:str)->str:
    s = unicodedata.normalize("NFC", s)
    # aspas/traços
    s = s.replace(""","\"").replace(""","\"").replace("'","'").replace("'","'")
    s = RE_DASH.sub("-", s)
    return s

def _canon_header(line:str)->str|None:
    m = RE_HEADER.match(line.upper())
    if not m: return None
    pref, loc, tod = m.groups()
    pref = HEAD_PREFIX.get(pref, pref)
    loc  = RE_SCENE_NUM_END.sub("", loc.strip()).upper()
    tod  = TIME_MAP.get(tod.strip().upper(), tod.strip().upper())
    return f"{pref if pref=='INT/EXT' else pref+'.'} {loc} - {tod}"

def canon_aggressive(text:str, drop_parentheticals:bool=True, drop_stage:bool=True)->str:
    """
    Canon agressivo para C1/C2: padroniza headers/tempos/transições,
    remove ruído pouco semântico (parentéticos/indicadores de câmera),
    compacta espaços/linhas. NÃO usar para C7.
    """
    t = _norm_unicode(text)
    lines = t.splitlines()
    out=[]
    for raw in lines:
        l = raw.rstrip()
        u = l.upper().strip()

        # Transições
        l = RE_TRANS_CUT.sub("CUT TO:", l)
        l = RE_FADE_IN.sub("FADE IN:", l)

        # Header?
        h = _canon_header(l)
        if h:
            out.append(h); continue

        # Parentéticos "isolados" ou após nome de personagem
        if drop_parentheticals:
            if u.startswith("(") and u.endswith(")"):
                # descarta linha só de parentético
                continue
            # remove sufixos de personagem (CONT'D, V.O., O.S.)
            if RE_CHARLINE.match(u):
                l = re.sub(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$","",l, flags=re.I)

        # Direções de câmera/transições menos úteis (opcional)
        if drop_stage:
            if u.startswith("ANGLE ON") or u.startswith("CLOSE ON") or u.startswith("INSERT"):
                continue
            if u.endswith(" TO:") and "CUT" not in u:  # ex: SMASH CUT TO:
                l = "CUT TO:"

        # espaços
        l = RE_WS_MULTI.sub(" ", l)
        l = RE_TRAIL_WS.sub("", l)
        out.append(l)

    t2 = "\n".join(out)
    t2 = RE_MULTI_NL.sub("\n\n", t2).strip()
    return t2