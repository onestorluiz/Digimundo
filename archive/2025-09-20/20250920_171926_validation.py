from typing import List, dict

def validate_techniques(techs: List[dict]) -> List[dict]:
    return [t for t in techs if isinstance(t, dict) and t.get("nome") and t.get("pagina") is not None and float(t.get("eficacia", 0)) >= 5.0]
