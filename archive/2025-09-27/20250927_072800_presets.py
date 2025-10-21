
PRESETS = {
  "champion": ["pacing","logline"],
  "quick": ["pacing", "logline"],
  "complete": ["pacing","logline","theme","market"],
  "enterprise": ["pacing","logline","theme","market","structure"],
  "ritual:acorde": "complete",
  "ritual:embala": "quick",
  "ritual:restaura": "complete"
}
RITUAL_REFLECT = {"ritual:restaura": True}
def resolve_preset(name: str) -> list[str]:
    name = PRESETS.get(name, name)
    return PRESETS[name] if isinstance(name, str) else name
def preset_requires_reflection(name: str) -> bool:
    return bool(RITUAL_REFLECT.get(name, False))
