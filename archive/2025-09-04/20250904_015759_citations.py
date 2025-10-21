import re
def extract_citations(text:str)->list[str]:
    return re.findall(r"\[\[K:[^\]]+\]\]", text or "")