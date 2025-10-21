import json, re
def try_parse_json(text: str) -> dict:
    try: return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, flags=re.S)
        if not m: raise
        body = m.group(0).replace('\n',' ').replace(', }',' }').replace(',]',' ]')
        return json.loads(body)
