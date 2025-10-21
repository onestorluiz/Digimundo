REQUIRE_EVIDENCE_KEYS = ['script_offset','rag_doc_id','baseline_metric']

def enforce_evidence(d: dict) -> dict:
    d.setdefault('evidence', {})
    for k in REQUIRE_EVIDENCE_KEYS:
        d['evidence'].setdefault(k, None)
    return d
