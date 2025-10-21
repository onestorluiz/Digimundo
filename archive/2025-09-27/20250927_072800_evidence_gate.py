
from .json_repair import try_parse_json
REQUIRED = ["script_offset", "rag_doc_id", "baseline_metric"]
def has_min_evidence(d: dict) -> bool:
    ev = d.get("evidence", {}) or {}
    return all(bool(ev.get(k)) for k in REQUIRED)
def require_evidence_or_retry(llm, spec_id: str, payload: dict, tries: int = 1) -> dict:
    if has_min_evidence(payload): return payload
    j = __import__("json").dumps(payload, ensure_ascii=False)
    for _ in range(tries):
        prompt = (f"### SPECIALIST_ID: {spec_id}\n"
                  "Reescreva o JSON abaixo ADICIONANDO as três evidências obrigatórias "
                  "(script_offset, rag_doc_id, baseline_metric). Responda APENAS o JSON final.\n\n"
                  f"{j}\n")
        fixed = llm.generate(prompt)
        try:
            payload = try_parse_json(fixed)
            if has_min_evidence(payload): return payload
        except Exception: continue
    return payload
