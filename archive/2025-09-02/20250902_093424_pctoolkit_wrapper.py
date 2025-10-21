# -*- coding: utf-8 -*-
from __future__ import annotations

def methods_available():
    avail=[]
    try:
        import llmlingua  # noqa
        avail.append("llmlingua")
    except: pass
    try:
        import pctoolkit  # hipotético; se não existir, ficará ausente
        avail.append("pctoolkit")
    except: pass
    return avail

def compress_llmlingua(text:str, ratio:float=0.85, preserve_entities:bool=True) -> str:
    try:
        from llmlingua import PromptCompressor  # API pode variar; fallback abaixo
        comp = PromptCompressor()
        return comp.compress(text, ratio=ratio, preserve_entities=preserve_entities)
    except Exception:
        return text  # SKIPPED

def compress_pctoolkit(text:str, method:str="selective_context", strength:float=0.8) -> str:
    """
    Rascunho defensivo: se pctoolkit não estiver disponível, retorna o texto.
    """
    try:
        import pctoolkit  # noqa
        # TODO: chamar método real quando disponível
        return text  # placeholder até instalação real
    except Exception:
        return text