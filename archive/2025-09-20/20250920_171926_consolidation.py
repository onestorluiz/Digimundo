from ..storage.memory_layers import stream_l2, append_l2
from .validation import validate_techniques

def nightly_consolidation():
    items = stream_l2(limit=1000)
    all_techs = []
    for it in items:
        all_techs.extend(it.get("tecnicas", []))
    good = validate_techniques(all_techs)
    if good:
        append_l2({"consolidated": True, "techniques": good[:100]})
    return {"consolidated": len(good)}
