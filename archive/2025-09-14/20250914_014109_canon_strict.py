# -*- coding: utf-8 -*-
import re
def canon_strict(text:str)->str:
    t = text.replace("—","-").replace("–","-").replace(""","\"").replace(""","\"").replace("'","'")
    t = re.sub(r"\r\n?", "\n", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)  # compacta múltiplas linhas vazias
    return t.strip()