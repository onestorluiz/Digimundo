from .schemas import coerce_payload

def validate_spec(spec_id: str, data: dict) -> dict:
    data.setdefault('payload', {})
    data['payload'] = coerce_payload(spec_id, data['payload'])
    try: q = float(data.get('quality', 0.0))
    except Exception: q = 0.0
    data['quality'] = 0.0 if q < 0 else (1.0 if q > 1.0 else q)
    return data
