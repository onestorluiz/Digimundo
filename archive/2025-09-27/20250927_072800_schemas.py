
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any
@dataclass
class PacingPayload: pace: str | None = None; dialogue_ratio: float | None = None
@dataclass
class LoglinePayload: logline: str | None = None; genre: str | None = None
@dataclass
class ThemePayload: primary_theme: str | None = None; motifs: List[str] = field(default_factory=list)
@dataclass
class MarketPayload: audience: str | None = None; comparables: List[str] = field(default_factory=list)
SPEC_SCHEMAS = {"pacing": PacingPayload, "logline": LoglinePayload, "theme": ThemePayload, "market": MarketPayload}
def coerce_payload(spec_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    cls = SPEC_SCHEMAS.get(spec_id)
    if not cls: return payload
    kwargs = {f: payload.get(f) for f in cls.__dataclass_fields__.keys()}
    obj = cls(**kwargs)  # type: ignore
    return asdict(obj)
