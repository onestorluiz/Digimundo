from __future__ import annotations
from typing import List, Dict
from .capabilities import list_caps

def _has_doc(session)->bool:
    return bool(getattr(session,"active_doc",None))

def suggest(session, last_answer:str, last_qscore, last_cites:list[str], history_len:int)->List[Dict]:
    caps=list_caps()
    sug=[]
    # Heurísticas simples (sem bloquear persona):
    if not _has_doc(session):
        sug.append({"title":"Abrir documento","cmd":"/open <arquivo>", "why":"sem documento ativo; análises mais profundas dependem do texto"})
    if _has_doc(session) and not last_cites:
        sug.append({"title":"Indexar e gerar evidências","cmd":"/audit | /anchors | /export md","why":"respostas com [[K:...]] ficam rastreáveis"})
    if _has_doc(session) and (last_qscore is not None and last_qscore<60):
        sug.append({"title":"Diagnóstico de estrutura","cmd":"/beats | /pace | /theme","why":"melhorar QScore exige ver beats, energia e motivos"})
    if _has_doc(session) and history_len>=2:
        sug.append({"title":"Comparar iterações","cmd":"/audit diff","why":"ver o que mudou (texto, citações, mix de modelos)"})
    if _has_doc(session):
        sug.append({"title":"Pacote editorial","cmd":"/export md | /export short | /export html | /pack","why":"entregáveis para compartilhar"})
    # Retorna no máximo 3
    return sug[:3]